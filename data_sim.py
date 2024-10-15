'''
================================================================================
pycdata: mono-repo
================================================================================
'''
from pathlib import Path
import time
import shutil
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import csv
import pandas as pd



class Timer:
    def __init__(self, run_time: float = 0.0) -> None:
        self._start_time = 0.0
        self._run_time = run_time

    def start(self,run_time: float | None = None) -> None:
        if run_time is not None:
            self._run_time = run_time

        self._start_time = time.perf_counter()

    def finished(self) -> bool:
        return (time.perf_counter() - self._start_time) >= self._run_time

    def elapsed_time(self) -> float:
        return (time.perf_counter() - self._start_time)


class DataGeneratorError(Exception):
    pass




class ExperimentDataGenerator:
    def __init__(self, frequency: float = 1.0) -> None:

        self._frequency = frequency
        self._target_path = Path.cwd()

        self._csv_count = 0

        self._trace_file = None
        self._csv_files = list([])

        self._trace_file_tag = 'csv'
        self._csv_file_tag = 'csv'


    def set_target_path(self, targ_path: Path) -> None:

        if not targ_path.is_dir():
            raise FileNotFoundError("Target path does not exist.")

        self._target_path = targ_path


    def load_csv_files(self, in_files) -> None:

        csv_df = pd.read_csv(in_files)
        self._csv_files = csv_df


    def reset(self) -> None:
        self._csv_count = 0


    def generate_data(self, duration: float) -> None:

        if duration < 0.0:
            raise DataGeneratorError("Data generation duration must be greater than 0")

        duration_timer = Timer(duration)
        output_timer = Timer(1.0/self._frequency)

        duration_timer.start()
        output_timer.start()

        while not duration_timer.finished():
            if output_timer.finished():
                output_timer.start()
                print(f'Duration = {duration_timer.elapsed_time()}s')

                self.write_traces()
                self.write_csv()


    def write_traces(self) -> None:
        print('Writing traces')


    def write_csv(self) -> None:

        for nn,ii in enumerate(self._csv_files):
            n_bits = 8
            csv_num_str = str(self._csv_count).zfill(4)
            save_file = f'{self._csv_file_tag}_{csv_num_str }_{nn}.csv'

            headers = [i for i in self._csv_files]

            csv_list = []
            for i in headers:
                row = self._csv_files[i]
                csv_list.append(row)



            with open(save_file, 'w') as f:
     
                # using csv.writer method from CSV package
                write = csv.writer(f)
     
                write.writerow(headers)
                write.writerows(csv_list)


        self._csv_count += 1

