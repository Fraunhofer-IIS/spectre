[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13941490.svg)](https://doi.org/10.5281/zenodo.13941490) [![DOI:10.1101/2021.01.08.425840](http://img.shields.io/badge/DOI-10.1101/2021.01.08.425840-B31B1B.svg)](https://doi.org/10.1109/SENSORS60989.2024.10784898)

# SPECTRE Dataset

This repository contains the dataset and code for the paper "SPECTRE: A Dataset for Spectral Reconstruction on Chip-Size Spectrometers With a Physics-Informed Augmentation Method".
You can find all data files in the [Zenodo repository](https://zenodo.org/records/13941490)

## Contents
- `examples/`: Contains examples on how to use the dataset.
- `src/`: Contains the python files of the spectre module.

## Requirements
- Python 3.11+
- Dependencies are listed in the `pyproject.toml` file.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   ```
2. Install the project:
   ```bash
   pip install .
   ```
3. Use the example scripts or notebooks:
   ```bash
   python examples/read_data.py
   ```
   
## License
- The dataset is available under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License.
- The code is available under the Software Copyright License for Academic Use of the Fraunhofer Software, Version 1.0.
  
## Citation
If you use this dataset or code in your work, please cite the corresponding paper:

**SPECTRE: A Dataset for Spectral Reconstruction on Chip-Size Spectrometers With a Physics-Informed Augmentation Method**

Available in the Proceedings of IEEE Sensors 2024. You can access the paper via [IEEE Xplore](https://doi.org/10.1109/SENSORS60989.2024.10784898)

BibTeX entry:

```bibtex
@INPROCEEDINGS{10784898,
  author={Wissing, Julio and Scholz, Teresa and Saloman, Stefan and Fargueta, Lidia and Junger, Stephan and Stefani, Alessio and Tschekalinskij, Wladimir and Scheele, Stephan and Schmid, Ute},
  booktitle={2024 IEEE SENSORS}, 
  title={SPECTRE: A Dataset for Spectral Reconstruction on Chip-Size Spectrometers with a Physics-Informed Augmentation Method}, 
  year={2024},
  volume={},
  number={},
  pages={1-4},
  keywords={Optical filters;Training;Neural networks;Reconstruction algorithms;Benchmark testing;Data augmentation;Optical sensors;Intelligent sensors;Optical arrays;Optical Sensors;Machine Learning;Artificial Intelligence;Spectral Reconstruction;Data Augmentation},
  doi={10.1109/SENSORS60989.2024.10784898}}

```
