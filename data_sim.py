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


class CameraDataGenerator:
    def __init__(self, frequency: float = 1.0) -> None:

        self._frequency = frequency
        self._target_path = Path.cwd()

        self._image_count = 0

        self._trace_file = None
        self._image_files = list([])

        self._trace_file_tag = 'Image'
        self._image_file_tag = 'Image'


    def set_target_path(self, targ_path: Path) -> None:

        if not targ_path.is_dir():
            raise FileNotFoundError("Target path does not exist.")

        self._target_path = targ_path


    def load_image_files(self, in_files: list[Path]) -> None:

        for ff in in_files:
            if not ff.is_file():
                raise FileNotFoundError("Specified image file: {ff}, does not exist")

        self._image_files = list([])
        for ff in in_files:
            image = Image.open(ff)
            self._image_files.append(np.array(image))


    def reset(self) -> None:
        self._image_count = 0


    def generate_data(self, duration: float, std_dev: int) -> None:

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
                self.write_images(std_dev)


    def write_traces(self) -> None:
        print('Writing traces')


    def write_images(self, std_dev) -> None:

        for nn,ii in enumerate(self._image_files):
            #0 = mean, 10 = standard deviation
            n_bits = 8
            #noise = np.random.normal(0, std_dev, size=ii.shape)
            noise = np.random.default_rng().standard_normal(ii.shape)
            noise_bits = noise*2**n_bits*std_dev/100
            img_noised = ii + noise_bits
            final_image = np.array(img_noised,dtype=np.uint8)
            image_num_str = str(self._image_count).zfill(4)
            save_file = f'{self._image_file_tag}_{image_num_str }_{nn}.tiff'
            save_path = self._target_path / save_file

            #im = Image.fromarray(ii)
            #plt.imsave(save_file, img_noised, cmap="gray")
            plt.imsave(save_file, final_image, cmap="gray")
            #im.save(save_path)
            
            with open("sample.csv", "a") as csvFile:
                fieldnames = ['Image path']
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'Image path': save_path })


        self._image_count += 1

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

        #self._csv_files = list([])
        csv_df = pd.read_csv(in_files)
        self._csv_files = csv_df
        #self._csv_files.append(np.array(csv_df))


    def reset(self) -> None:
        self._csv_count = 0


    def generate_data(self, duration: float, std_dev: int) -> None:

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
                self.write_csv(std_dev)


    def write_traces(self) -> None:
        print('Writing traces')


    def write_csv(self, std_dev) -> None:

        for nn,ii in enumerate(self._csv_files):
            #0 = mean, 10 = standard deviation
            n_bits = 8
            #noise = np.random.normal(0, std_dev, size=ii.shape)
            #noise = np.random.default_rng().standard_normal(ii.shape)
            #noise_bits = noise*2**n_bits*std_dev/100
            #img_noised = ii + noise_bits
            #final_image = np.array(img_noised,dtype=np.uint8)
            csv_num_str = str(self._csv_count).zfill(4)
            save_file = f'{self._csv_file_tag}_{csv_num_str }_{nn}.csv'
            #save_path = self._target_path / save_file

            headers = [i for i in self._csv_files]

            csv_list = []
            for i in headers:
                row = self._csv_files[i]
                csv_list.append(row)

            #im = Image.fromarray(ii)
            #plt.imsave(save_file, img_noised, cmap="gray")
            #plt.imsave(save_file, final_image, cmap="gray")
            #im.save(save_path)


            with open(save_file, 'w') as f:
     
                # using csv.writer method from CSV package
                write = csv.writer(f)
     
                write.writerow(headers)
                write.writerows(csv_list)


        self._csv_count += 1

class ExperimentMock:
    def __init__(self, frequency: float = 1.0) -> None:

        self._frequency = frequency
        self._target_path = Path.cwd()

        self._csv_count = 0

        self._trace_file = None
        self._csv_files = list([])

        self._trace_file_tag = 'csv'
        self._csv_file_tag = 'csv'
    
    def generate_data(self, duration: float, std_dev: int) -> None:

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
                self.write_csv(std_dev)

    def write_traces(self) -> None:
        print('Writing traces')

    def write_csv(self, std_dev) -> None:

        for nn,ii in enumerate(self._csv_files):
            #0 = mean, 10 = standard deviation
            n_bits = 8
            #noise = np.random.normal(0, std_dev, size=ii.shape)
            #noise = np.random.default_rng().standard_normal(ii.shape)
            #noise_bits = noise*2**n_bits*std_dev/100
            #img_noised = ii + noise_bits

            headers = [i for i in self._csv_files]

            csv_list = []
            for i in headers:
                row = self._csv_files[i]
                csv_list.append(row)

            #im = Image.fromarray(ii)
            #plt.imsave(save_file, img_noised, cmap="gray")
            #plt.imsave(save_file, final_image, cmap="gray")
            #im.save(save_path)
            
            #with open("sample.csv", "a") as csvFile:
                #fieldnames = ['Image path']
                #writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                #writer.writeheader()
                #writer.writerow({'Image path': save_path })

            with open('out.csv', 'w') as f:
     
                # using csv.writer method from CSV package
                write = csv.writer(f)
     
                write.writerow(headers)
                write.writerows(csv_list)


        self._csv_count += 1