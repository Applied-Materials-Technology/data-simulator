# Data Simulator

## Installation
This tool is built to be compatible with python 3.9.

- Create a virtual environment in a location of your choice and activate it:
```
python3.9 -m venv .data-sim-env
source .data-sim-env/bin/activate
```

- Navigate to the root directory of the data-sim package and install it using pip:
```
pip install .
```

- For an editable developer installation use:
```
pip install -e .
```

## Usage & Options

**Example Usage**
Make sure your virtual environment with the package installed is activated.

Generate data for 5 seconds in the "outputs" folder at a frequency of 1.0 Hz writing a single csv:
```shell
python3.9 -m datasim --duration 5.0  --output "outputs" --frequency 1.0 --onecsv True
```

Generate setup files (MatchID input and calibration) only:
```shell
python3.9 -m datasim --duration 0.0  --output "outputs"
```

Generate stereo DIC data for 6 seconds in the "outputs" folder at a frequency of 2.0 Hz writing a csv per data frame:
```shell
python3.9 -m datasim --duration 6.0  --output "outputs" --frequency 2.0 --stereo True
```

**Options**
- --duration : how long data will be generated in seconds, default = 10.0
- --output : the directory in which generated data will appear, default = 'outputs'
- --frequency : the frequency at which data is generated in Hz, default = 0.1
- --onecsv : toggle between a single updating csv (True), or multiple csvs (False), default = False
- --stereo : if True generate stereo DIC data with an m3inp if False then generate 2D DIC data with an m2inp
