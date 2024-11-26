'''
================================================================================
datasim
================================================================================
'''
from pathlib import Path
import argparse
from importlib_resources import files
from datasim.datasim import DataSimulator, DataSimulatorParams


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", default = 10, type = float)
    parser.add_argument("--onecsv", default = False, type = bool)
    parser.add_argument("--output", default = 'outputs', type = str)
    parser.add_argument("--frequency", default = 1.0, type = float)
    args = parser.parse_args()

    image_files: list[list[Path]] = [
        [Path(files("datasim.data2d").joinpath("Image_0000_0.tiff")),],
        [Path(files("datasim.data2d").joinpath("Image_0001_0.tiff")),],
        [Path(files("datasim.data2d").joinpath("Image_0002_0.tiff")),],
        [Path(files("datasim.data2d").joinpath("Image_0003_0.tiff")),],
        ]

    setup_files: list[Path] = [
            Path(files("datasim.data2d").joinpath("Job_man_roi.m2inp")),]

    trace_file: Path = Path(files("datasim.data2d").joinpath("tracefile.csv"))

    data_sim_params = DataSimulatorParams(target_path=Path(args.output),
                                          duration=args.duration,
                                          frequency=args.frequency,
                                          trace_file_once=args.onecsv)
    data_sim = DataSimulator(data_sim_params)
    data_sim.load_data_files(setup_files, trace_file, image_files)
    data_sim.generate_data()

if __name__ == "__main__":
    main()