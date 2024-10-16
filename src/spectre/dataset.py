import os
import pickle
from collections.abc import Generator

import numpy as np

import spectre.utils as ut


class SPECTRE(Generator):
    def __init__(
        self,
        root_dir: str,
        int_time: int = 1400,
        shuffle: bool = True,
        cache_dir: str = None,
        clean_threshold: float = 0.15,
        lamb_range: tuple[int, int] = (450, 690),
        cache=True,
        augment=True,
    ) -> None:
        """
        Main class to read and pre-process the SPECTRE dataset.
        Use objects from this class as is (generator) or cast it to a list to have the whole dataset in memory

        Arguments:
            root_dir -- Path to the root directory of the dataset

        Keyword Arguments:
            int_time -- Integration time of the CSS frames. Using 1400 is recommended, but [1200, 1000, 800] also work (default: {1400})
            shuffle -- Flag if the dataset should be shuffled before reading the first item (default: {True})
            cache_dir -- Cache location. If None the dataset is cached under '.spectre_cache/' (default: {None})
            clean_threshold -- Minimum average signal strength in relation to the white reference measurement of a sample to be included in the dataset after cleaning (default: {0.15})
            lamb_range -- Wavelength range in nanometer (default: {(450, 690)})
            cache -- Flag wether the caching mechanism should be used (default: {True})
            augment -- Flag if the physics informed augmentation should be used (default: {True})
        """
        # Storing user parameters
        self.int_time = int_time
        self.lamb_range = lamb_range
        self.wavelengths = np.arange(*self.lamb_range)
        self.root_dir = root_dir
        self.cache_dir = cache_dir
        self.cache = cache
        self.clean_threshold = clean_threshold
        self.augment = augment
        self.shuffle = shuffle

        # Initializing dataset
        self._ids = None
        self.i = 0
        self.dark_meas, self.white_meas = self._read_reference()
        self.meas_list = self._scan_root()
        self.num_meas = len(self)

    def __len__(self) -> int:
        if self._ids is None:
            # First call to __len__ initializes dataset. This should be done in the constructor
            self._init_dataset()
        return len(self._ids)

    def send(self, _) -> tuple[np.ndarray, np.ndarray]:
        """
        Overwrites the abstract function from the Generator Class

        Raises:
            StopIteration: If all measurements have been used

        Returns:
            Next dataset item as a Tuple of (CSS Frame, GT Spectrum)
        """
        if self.i < len(self):
            next_value = self._read_meas_file(self.i)
            self.i += 1
            return next_value
        else:
            raise StopIteration

    def throw(self, typ, val=None, tb=None):
        """
        Forwards throw exceptions to super class
        """
        super().throw(typ, val, tb)

    def _scan_root(self) -> list[tuple[str, str]]:
        """
        Function that scans the root directory for measurements.
        The measurement locations are stored in a list of tuples, with each tuple holding two paths.
        The two paths are needed for the data augmentation, so that two measurements can be combined into one.
        If the second item in the Tuple is None it indicates a sample without augmentation.

        Returns:
            List of paths to all raw measurement folders
        """
        # Measurements without augmentation
        raw_meas_list = [
            (os.path.join(self.root_dir, f), None)
            for f in os.listdir(self.root_dir)
            if not f.startswith(".") and f not in ["Dark", "White"]
        ]
        if not self.augment:
            return raw_meas_list
        else:
            # Include path to multiply (one half of the dataset with the other half)
            multiplied_list = []
            for meas_a in raw_meas_list[: len(raw_meas_list) // 2]:
                for meas_b in raw_meas_list[len(raw_meas_list) // 2 :]:
                    multiplied_list.append((meas_a[0], meas_b[0]))
            # Include multiplication with itself
            squared_list = [(meas[0], meas[0]) for meas in raw_meas_list]

            # Add all list together for final potential samples
            return raw_meas_list + multiplied_list + squared_list

    def _init_dataset(self):
        """
        Initializes the dataset by cleaning all measurements/combinations that do not have enough signal strength.
        With the caching mechanism this cleaning has to be done only once during runtime.
        """
        if self.cache_dir is None:
            self.cache_dir = ".spectre_cache/"
        if os.path.exists(os.path.join(self.cache_dir, "dataset_cache.pickle")) and self.cache:
            print(
                "Found dataset cache at: .spectre_cache/dataset_cache.json, skipping data cleaning step"
            )
            with open(os.path.join(self.cache_dir, "dataset_cache.pickle"), "rb") as f:
                self.meas_list = pickle.load(f)
        else:
            print("Cleaning dataset, this might take a while")
            try:
                os.mkdir(self.cache_dir)
            except FileExistsError:
                pass
            for meas in self.meas_list:
                if meas[1] is None:
                    # Non-augmented sample
                    spectrum = ut.read_spectrum(meas[0])
                    spectrum = ut.normalize_array(spectrum, self.dark_meas[1], self.white_meas[1])
                else:
                    # Augmented sample
                    spectrum_a = ut.read_spectrum(meas[0])
                    spectrum_a = ut.normalize_array(
                        spectrum_a, self.dark_meas[1], self.white_meas[1]
                    )
                    spectrum_b = ut.read_spectrum(meas[1])
                    spectrum_b = ut.normalize_array(
                        spectrum_b, self.dark_meas[1], self.white_meas[1]
                    )
                    spectrum = spectrum_a * spectrum_b
                mean_signal = np.mean(spectrum)
                if mean_signal < self.clean_threshold:
                    self.meas_list.remove(meas)
            if self.cache:
                print(
                    "Data Cleaning finished, saving results to .spectre_cache/dataset_cache.pickle"
                )
                with open(os.path.join(self.cache_dir, "dataset_cache.pickle"), "wb") as f:
                    pickle.dump(self.meas_list, f, pickle.HIGHEST_PROTOCOL)
        self._ids = np.arange(len(self.meas_list))
        if self.shuffle:
            np.random.shuffle(self._ids)

    def _read_reference(
        self,
    ) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
        """
        Reads the reference measurements from the root dir

        Returns:
            dark and whiten measurements
        """
        dark = ut.read_measurement(os.path.join(self.root_dir, "Dark"))
        white = ut.read_measurement(os.path.join(self.root_dir, "White"))
        return dark, white

    def _read_meas_file(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Reads measurement from the measurement list based on an index.
        This function can read a tuple of measurements.

        Arguments:
            index -- Index in the file list

        Returns:
            Measurement as tuple (Frame, Spectrum)
        """
        path_tuple = self.meas_list[index]
        if path_tuple[1] is None:
            # No multiplication necessary
            return self._read_meas_file_singular(path_tuple[0])
        else:
            # Sample is augmented (multiplication of two samples)
            frame_a, spectrum_a = self._read_meas_file_singular(path_tuple[0])
            frame_b, spectrum_b = self._read_meas_file_singular(path_tuple[1])
            return frame_a * frame_b, spectrum_a * spectrum_b

    def _read_meas_file_singular(self, path) -> tuple[np.ndarray, np.ndarray]:
        """
        Reads a measurement from path

        Arguments:
            path -- path to measurement

        Returns:
            measurement as tuple (Frame, Spectrum)
        """
        frame, spectrum = ut.read_measurement(path, self.int_time)
        frame, spectrum = self._normalize_measurement(frame, spectrum)
        return frame, spectrum

    def _normalize_measurement(
        self, frame: np.ndarray, spectrum: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Normalizes a measurement using the dark and white reference measurements

        Arguments:
            frame -- frame that should be normalized
            spectrum -- spectrum that should be normalized

        Returns:
            normalized measurement tuple (Frame, Spectrum)
        """
        frame_norm = ut.normalize_array(frame, self.dark_meas[0], self.white_meas[0])
        spectrum_norm = ut.normalize_array(spectrum, self.dark_meas[1], self.white_meas[1])
        return frame_norm, spectrum_norm
