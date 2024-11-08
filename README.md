# Data Simulator

## Installation
- Create and activate virutal environment
```
python -m venv datasimenv
source datasimenv/bin/activate
```

- Install requirements
```
pip install -r requirements.txt
```

## Usage & Options

**Example Usage**
Generate data for 10 seconds in the "outputs" folder at a frequency of 1.0 Hz:
```shell
python datasim.py --duration 10.0  --output "outputs" --frequency 1.0 --onecsv False
```

Generate MatchID input script only:
```shell
python datasim.py --duration 0.0  --output "outputs"
```

**Options**
- --duration : how long data will be generated in seconds, default = 1000
- --output : the directory in which generated data will appear, default = 'outputs'
- --frequency : the frequency at which data is generated in Hz, default = 0.1
- --onecsv : toggle between a single updating csv (True), or multiple csvs (False), default = False
