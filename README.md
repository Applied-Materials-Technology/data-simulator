# Data Simulator

- Create and activate virutal environment
```
python -m venv datasimenv
source datasimenv/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```
- running generate.py will simulate files being generated every 10 seconds for 1000 seconds, using the files located in the "data" directory as a base, and saving output files to an "outputs" directory as a default.
- change the duration with --duration, the path to the csv with --basefile, and output location with --output

# Options

- --duration : how long data will be generated in seconds, default = 1000
- --output : the directory in which generated data will appear, default = 'outputs'
- --frequency : the frequency at which data is generated in Hz, default = 0.1
