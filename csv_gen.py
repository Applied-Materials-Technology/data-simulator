from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
#import pycdata
from data_sim import *
import os
import pandas as pd
import csv

example = ExperimentDataGenerator()
#base_file = pd.read_csv('data/newcsvfile.csv')
base_file = 'data/newcsvfile.csv'
example.load_csv_files(base_file)
example.generate_data(duration=3.1, std_dev=10)