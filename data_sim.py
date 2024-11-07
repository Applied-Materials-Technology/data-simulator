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
import os
import shutil



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


    def set_target_path(self, targ_path: Path) -> None:

        if not targ_path.is_dir():
            raise FileNotFoundError("Target path does not exist.")

        self._target_path = targ_path


    def load_csv_files(self, in_files, img_files, match_id_files) -> None:

        csv_df = pd.read_csv(in_files)
        self._csv_files = csv_df
        self._match_id_files = match_id_files

        for ff in img_files:
            if not ff.is_file():
                raise FileNotFoundError("Specified image file: {ff}, does not exist")

        self._image_files = list([])
        for ff in img_files:
            image = Image.open(ff)
            self._image_files.append(np.array(image))


    def reset(self) -> None:
        self._csv_count = 0
        self._image_count = 0


    def generate_data(self, duration: float, outputloc = str, onecsv = bool) -> None:

        if duration < 0.0:
            raise DataGeneratorError("Data generation duration must be greater than 0")

        duration_timer = Timer(duration)
        output_timer = Timer(1.0/self._frequency)

        duration_timer.start()
        output_timer.start()
        write_metadata = shutil.copyfile(self._match_id_files, os.path.join(outputloc,f'metadata.m3inp'))
        while not duration_timer.finished():
            if output_timer.finished():
                output_timer.start()
                print(f'Duration = {duration_timer.elapsed_time()}s')

                self.write_traces()
                if onecsv == True:
                    self.write_files_onecsv(outputloc)
                else:
                    self.write_files(outputloc)

    def metadata_only(self, outputloc = str) -> None:
        write_metadata = shutil.copyfile(self._match_id_files, os.path.join(outputloc,f'metadata.m3inp'))


    def write_traces(self) -> None:
        print('Writing traces')


    def write_files_onecsv(self, outputloc, std_dev = 10) -> None:


        for nn,ii in enumerate(self._csv_files):
            n_bits = 8
            csv_num_str = str(self._csv_count).zfill(4)
            save_file = os.path.join(outputloc,f'{self._csv_file_tag}_{csv_num_str }_{nn}.csv')

            headers = [i for i in self._csv_files]

            csv_list = []
            for i in headers:
                row = self._csv_files[i]
                csv_list.append(row)

        for nn,ii in enumerate(self._image_files):
            #0 = mean, 10 = standard deviation
            n_bits = 8
            noise = np.random.default_rng().standard_normal(ii.shape)
            noise_bits = noise*2**n_bits*std_dev/100
            img_noised = ii + noise_bits
            final_image = np.array(img_noised,dtype=np.uint8)
            image_num_str = str(self._image_count).zfill(4)
            save_file_img = os.path.join(outputloc,f'{self._csv_file_tag}_{csv_num_str }_{nn}.tiff')
            save_path_img = self._target_path / save_file_img
            plt.imsave(save_file_img, final_image, cmap="gray")


            #updating csv
            with open(os.path.join(outputloc,"images.csv"), "a") as csvFile:
                fieldnames = ['Image path']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
                #writer = csv.writer(csvFile)

                writer.writeheader()
                writer.writerow({'Image path': save_file_img })
                #writer.writerow(save_file_img)


        self._csv_count += 1
        self._image_count += 1



    def write_files(self, outputloc, std_dev = 10) -> None:


        for nn,ii in enumerate(self._csv_files):
            n_bits = 8
            csv_num_str = str(self._csv_count).zfill(4)
            save_file = os.path.join(outputloc,f'{self._csv_file_tag}_{csv_num_str }_{nn}.csv')

            headers = [i for i in self._csv_files]

            csv_list = []
            for i in headers:
                row = self._csv_files[i]
                csv_list.append(row)

        for nn,ii in enumerate(self._image_files):
            #0 = mean, 10 = standard deviation
            n_bits = 8
            noise = np.random.default_rng().standard_normal(ii.shape)
            noise_bits = noise*2**n_bits*std_dev/100
            img_noised = ii + noise_bits
            final_image = np.array(img_noised,dtype=np.uint8)
            image_num_str = str(self._image_count).zfill(4)
            save_file_img = os.path.join(outputloc,f'{self._csv_file_tag}_{csv_num_str }_{nn}.tiff')
            save_path_img = self._target_path / save_file_img
            plt.imsave(save_file_img, final_image, cmap="gray")


            #new csvs
            with open(save_file, 'w') as f:
     
                # using csv.writer method from CSV package
                write = csv.writer(f)
     
                write.writerow(headers)
                write.writerows(csv_list)


        self._csv_count += 1
        self._image_count += 1