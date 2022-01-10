# Thermal Sensors

This small project stores every second images captured with the FLIR Lepton 3.5 sensor and the Pure Thermal 2 board simultaneously to the computer's integrated webcam.

## Features

Each second:

- Stores images captured by the computer's webcam in the ImagesCAMERA folder (160x120).
- Stores RGB (HEATMAP) images captured by FLIR Lepton 3.5 in the ImagesHEATMAP folder (160x120).
- Stores Gray Scale images captured by FLIR Lepton 3.5 in the ImagesGRAYSCALE folder (160x120).

## Installation

Windows:

```sh
pip install -r requirements.txt
```

_Python's version I have installed on my system: Python 3.8.5_

## Setup

Open a command prompt at the root of the project, and run:

```sh
python main.py
```
