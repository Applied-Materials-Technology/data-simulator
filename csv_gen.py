from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from data_sim import *
import os
import pandas as pd
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--duration", default = 3.1, type = float)
parser.add_argument("--basefile", default = 'data/newcsvfile.csv', type = str)

args = parser.parse_args()

example = ExperimentDataGenerator()
example.load_csv_files(args.basefile)
example.generate_data(duration = args.duration)