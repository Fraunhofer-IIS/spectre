import os

import numpy as np
import pandas as pd

EPSILON = 1e-8


def read_measurement(
    folder: str, int_time: int = 1400, lamb_range: tuple[int, int] = (450, 690)
) -> tuple[np.ndarray, np.ndarray]:
    """
    Reads measurement from path. Wraps the two read_frame and read_spectrum functions into one call.

    Arguments:
        folder -- measurement location

    Keyword Arguments:
        int_time -- Integration time of the CSS frames. Using 1400 is recommended, but [1200, 1000, 800] also work (default: {1400}) (default: {1400})
        lamb_range -- Wavelength range in nanometer (default: {(450, 690)})

    Returns:
        Frame and Spectrum as tuple
    """
    frame = read_frame(folder, int_time)
    spectrum = read_spectrum(folder)
    return frame, spectrum


def read_frame(folder, int_time=1400) -> np.ndarray:
    """
    Reads CSS frame from measurement folder

    Arguments:
        folder -- measurement location

    Keyword Arguments:
        int_time -- Integration time of the CSS frames. Using 1400 is recommended, but [1200, 1000, 800] also work (default: {1400}) (default: {1400})

    Returns:
        Frame and Spectrum as tuple
    """
    frame = np.load(os.path.join(folder, f"{int_time}_frame.npy"))
    frame = np.clip(frame, a_min=EPSILON, a_max=None)
    return frame


def read_spectrum(folder: str, lamb_range: tuple[int, int] = (450, 690)) -> np.ndarray:
    """
    Reads GT Spectrum from folder

    Arguments:
        folder -- measurement location

    Keyword Arguments:
        lamb_range -- Wavelength range in nanometer (default: {(450, 690)})

    Returns:
        Spectrum as numpy array
    """
    # Reading csv file and clipping values smaller than 0 (Epsilon)
    spectrum = pd.read_csv(
        os.path.join(folder, "spectrum.csv"),
        usecols=["Intensity", "wavelengths"],
        index_col="wavelengths",
    ).clip(lower=EPSILON)

    # Limiting wavelength range
    spectrum = spectrum.loc[lamb_range[0] : lamb_range[1] - 1]  # pd does include last index

    # Rounding data to full wavelengths
    spectrum.index = np.round(spectrum.index, 0)
    spectrum = spectrum.groupby("wavelengths").mean()

    return np.squeeze(spectrum.to_numpy())


def normalize_array(array: np.ndarray, dark: np.ndarray, white: np.ndarray) -> np.ndarray:
    """
    Normalizes an array. This array can either be a frame or gt spectrum.
    Also clips values between Epsilon (constant close to zero) and one).

    Arguments:
        array -- numpy array that should be normalized
        dark -- corresponding dark measurement
        white -- corresponding white measurement

    Returns:
        normalized array
    """
    return np.clip((array - dark) / (white - dark), a_min=EPSILON, a_max=1)
