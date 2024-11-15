'''
================================================================================
datasim: mono-repo
================================================================================
'''
from __future__ import annotations
#from dataclasses import dataclass
from pathlib import Path
import time
import shutil
import os
import csv

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
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
    def __init__(self, frequency: float) -> None:

        self._frequency = frequency
        self._target_path = Path.cwd()

        self._csv_count = 0

        self._trace_file = None
        self._csv_files = list([])
        self._match_id_files = list([])

        self._trace_file_tag = 'csv'
        self._csv_file_tag = 'csv'

        self._image_count = 0

        self._image_files = list([])

        self._trace_file_tag = 'Image'
        self._image_file_tag = 'Image'
        self._data_frame_count = 0
        self.n_bits = 8


    def set_target_path(self, targ_path: Path) -> None:

        if not targ_path.is_dir():
            raise FileNotFoundError("Target path does not exist.")

        self._target_path = targ_path


    def load_data_files(self, csv_file, img_files, match_id_file) -> None:

        csv_df = pd.read_csv(csv_file)
        self._csv_file = csv_df
        self._match_id_file = match_id_file

        self._image_files = list([])
        for ff in img_files:
            if not ff.is_file():
                raise FileNotFoundError("Specified image file: {ff}, does not exist")
            
            image = Image.open(ff)
            self._image_files.append(np.array(image))


    def reset(self) -> None:
        self._data_frame_count = 0


    def generate_data(self, duration, output_loc, onecsv) -> None:

        if duration < 0.0:
            raise DataGeneratorError("Data generation duration must be greater than 0")

        duration_timer = Timer(duration)
        output_timer = Timer(1.0/self._frequency)

        if not Path(output_loc).is_dir():
            os.mkdir(Path(output_loc))

        print(f"Starting data generation at {self._frequency} Hz")

        duration_timer.start()
        output_timer.start()

        print("Writing MatchID input file.")
        #shutil.copyfile(self._match_id_file, Path(output_loc) / self.match_id_file)
        shutil.copyfile(self._match_id_file, os.path.join(output_loc,f'metadata.m3inp'))

        while not duration_timer.finished():
            if output_timer.finished():
                output_timer.start()
                print(f"Writing data files for time step number: {self._data_frame_count}.")
                print(f'Duration = {duration_timer.elapsed_time()}s')

                if onecsv == True:
                    self.write_files_onecsv(output_loc)
                else:
                    self.write_files(output_loc)

                self._data_frame_count += 1


    def metadata_only(self, outputloc = str) -> None:
        shutil.copyfile(self._match_id_files, os.path.join(outputloc,f'metadata.m3inp'))

    def csv_reader(self, output_loc):
        csv_num_str = str(self._data_frame_count).zfill(4)
        save_file = output_loc / f'{self._trace_file_tag}_{csv_num_str }_0.csv' 

        headers = [i for i in self._csv_file]

        csv_list = []
        for i in headers:
            row = self._csv_file[i]
            csv_list.append(row)

            
            return csv_num_str, save_file, csv_list, headers

    def generate_images(self, output_loc, std_dev, csv_num_str):
        for nn,ii in enumerate(self._image_files):
            #0 = mean, 1 = standard deviation
            noise = np.random.default_rng().standard_normal(ii.shape)
            noise_bits = noise*2**self.n_bits**std_dev/100
            img_noised = ii + noise_bits
            final_image = np.array(img_noised,dtype=np.uint8) # NOTE: checkout integer overflow issues here and use np.ceil / np.floor
            save_file_img = os.path.join(output_loc,f'{self._trace_file_tag}_{csv_num_str }_{nn}.tiff')
            save_path_img = self._target_path / save_file_img
            plt.imsave(save_file_img, final_image, cmap="gray")
            return save_file_img


    def write_files_onecsv(self, output_loc: str, std_dev: float = 1.0) -> None:

        output_loc = Path(output_loc)

        csv_num_str, save_file, csv_list, headers = self.csv_reader(output_loc)

        save_file_img = self.generate_images(output_loc, std_dev, csv_num_str)


        #updating csv
        with open(os.path.join(output_loc,"images.csv"), "a") as csvFile:
            fieldnames = ['Image path']
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Image path': save_file_img })


    def write_files(self, output_loc: str, std_dev: float = 1.0) -> None:

        output_loc = Path(output_loc)

        csv_num_str, save_file, csv_list, headers = self.csv_reader(output_loc)

        self.generate_images(output_loc, std_dev, csv_num_str)


        #new csvs
        with open(save_file, 'w') as f:
     
            # using csv.writer method from CSV package
            write = csv.writer(f)
     
            write.writerow(headers)
            write.writerows(csv_list)