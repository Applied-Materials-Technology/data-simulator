'''
================================================================================
datasim: mono-repo
================================================================================
'''
from __future__ import annotations
from dataclasses import dataclass
import warnings
from pathlib import Path
import time
import shutil
import csv
import numpy as np
from PIL import Image


class Timer:
    def __init__(self, run_time: float = 0.0) -> None:
        self._start_time: float = 0.0
        self._run_time: float = run_time

    def start(self,run_time: float | None = None) -> None:
        if run_time is not None:
            self._run_time = run_time

        self._start_time = time.perf_counter()

    def finished(self) -> bool:
        return (time.perf_counter() - self._start_time) >= self._run_time

    def elapsed_time(self) -> float:
        return (time.perf_counter() - self._start_time)


@dataclass
class DataSimulatorParams:
    target_path: Path

    duration: float = 10.0  # seconds
    frequency: float = 1.0  # Hz

    setup_file_tag: str = "MatchID"

    trace_file_once: bool  = True
    trace_file_tag: str = "Image"
    trace_file_suffix: str = ".csv"

    image_file_tag: str = "Image"
    image_file_suffix: str = ".tiff"
    image_bits: int = 8
    image_noise_pc: float | None = 1.0

    def __post_init__(self) -> None:
        if not self.target_path.is_dir():
            warnings.warn("Target path does not exist, creating it.")
            self.target_path.mkdir()

        if self.frequency <= 0.0:
            warnings.warn("Frequency must be greater than zero, reseting to 1.0 Hz")
            self.frequency = 1.0

        if self.image_bits <= 0:
            warnings.warn("Image bits must be greater than zero, reseting  to 8 bits")
            self.image_bits = 8

class DataSimulatorError(Exception):
    pass

class DataSimulator:
    def __init__(self, data_sim_params: DataSimulatorParams) -> None:
        self._params: DataSimulatorParams = data_sim_params

        self._output_count: int = 0
        self._output_count_str: str = ""
        self._setup_files: list[Path] | None = None
        self._trace_file: Path | None = None
        self._trace_data: np.ndarray | None = None
        self._trace_headers: str = ""
        self._image_data: list[np.ndarray] | None = None


    def load_data_files(self,
                        setup_files: list[Path],
                        trace_file: Path,
                        image_files: list[Path]) -> None:

        for ss in setup_files:
            if not ss.is_file():
                raise FileExistsError(f"Setup file: {ss}, does not exist.")

        self._setup_files = setup_files

        if not trace_file.is_file():
            raise FileExistsError(f"Trace file: {trace_file}, does not exist.")

        if trace_file.suffix != ".csv":
            raise FileExistsError(f"Trace file: {trace_file}, must be a .csv")

        self._trace_file = trace_file

        if not self._params.trace_file_once:
            with open(self._trace_file,"r",encoding="utf-8") as csv_file:
                self._trace_headers = csv_file.readline().strip("\n")

            self._trace_data = np.genfromtxt(self._trace_file,
                                            delimiter=",",
                                            skip_header=1)

        self._image_data = []
        for ff in image_files:
            if not ff.is_file():
                raise FileNotFoundError("Specified image file: {ff}, does not exist")

            self._image_data.append(np.array(Image.open(ff),dtype=np.float64))


    def generate_data(self) -> None:

        if (self._setup_files is None or
            self._trace_file is None or
            self._image_data is None):
            raise DataSimulatorError("Load data files before generating data.")

        print(f"Data generation duration is {self._params.duration} seconds")
        print(f"Starting data generation at {self._params.frequency} Hz.")

        timer_duration = Timer(self._params.duration)
        timer_output = Timer(1.0/self._params.frequency)
        timer_duration.start()
        timer_output.start()

        print("Writing setup files.")
        for ss in self._setup_files:
            shutil.copyfile(ss, self._params.target_path / \
                str(self._params.setup_file_tag + ss.suffix))

        # If we have one csv file we need to open a handle to it and keep it open
        if not self._params.trace_file_once and self._params.duration > 0.0:
            trace_out_file = open(self._params.target_path /
                                        str(self._params.trace_file_tag +
                                            self._params.trace_file_suffix),"w",
                                            encoding="utf-8")
            trace_writer = csv.writer(trace_out_file)


        while not timer_duration.finished():
            if timer_output.finished():
                timer_output.start()

                print(80*"-")
                print(f"Writing data files for time step: {self._output_count}.")
                print(f"Total elapsed time: {timer_duration.elapsed_time()} seconds")
                print()

                self._output_count_str = str(self._output_count).zfill(4)

                if not self._params.trace_file_once:
                    print("MULTI")
                    self.generate_files_multi_trace(self._params.target_path,
                                                    trace_writer)
                else:
                    if self._output_count == 0:
                        shutil.copyfile(self._trace_file,
                                        self._params.target_path /
                                        str(self._params.trace_file_tag +
                                            self._params.trace_file_suffix))

                    self.generate_images(self._params.target_path)

                self._output_count += 1

        if not self._params.trace_file_once and self._params.duration > 0.0:
            trace_out_file.close()


    def generate_images(self, output_path: Path) -> None:

        for nn,image in enumerate(self._image_data):
            image_to_save = np.copy(image)

            if self._params.image_noise_pc is not None:
                image_to_save = image_add_noise(image_to_save,
                                                self._params.image_bits,
                                                self._params.image_noise_pc)

            image_to_save = image_digitise(image_to_save,self._params.image_bits)

            image_save_file = output_path / str(self._params.image_file_tag +
                                                f"_{self._output_count_str}_{nn}"
                                                + self._params.image_file_suffix)
            im = Image.fromarray(image)
            im.save(image_save_file)


    def generate_files_multi_trace(self,
                                   output_path: Path,
                                   trace_writer) -> None:
        # On the first iteration write the headers
        if self._output_count == 0:
            trace_writer.writerow(self._trace_headers)

        # Write the next row to the csv for this frame
        trace_writer.writerow(self._trace_data[self._output_count,:])

        self.generate_images(output_path)



def image_add_noise(image: np.ndarray,
                    image_bits: int,
                    noise_std_pc: float) -> np.ndarray:

    noise = np.random.default_rng().standard_normal(image.shape)
    noise_bits = (noise * (2**image_bits) * (noise_std_pc/100))
    return image + noise_bits


def image_digitise(image: np.ndarray, n_bits: int) -> np.ndarray:

    image[image < 0] = 0
    image[image > 2**n_bits] = 2**n_bits

    if n_bits > 0 and n_bits <= 8:
        image = np.array(image,dtype=np.uint8)
    else:
        image = np.array(image,dtype=np.uint16)

    return image