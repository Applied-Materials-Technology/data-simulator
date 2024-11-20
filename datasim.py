'''
================================================================================
datasim
================================================================================
'''
from pathlib import Path
from datasimlib import DataSimulator, DataSimulatorParams
import argparse

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", default = 1000, type = float)
    parser.add_argument("--onecsv", default = False, type = bool)
    parser.add_argument("--output", default = 'outputs', type = str)
    parser.add_argument("--frequency", default = 1.0, type = float)
    args = parser.parse_args()
    print(args)

    # NOTE: if this is run from another directory then it won't work,
    # need to be able to install the package using *.toml with the data
    image_files: list[Path] = [Path('data/OptSpeckle_5Mpx_2464_2056_width5_8bit_GBlur1.tiff'),
                   Path('data/OptSpeckle_5Mpx_2464_2056_width5_8bit_GBlur1.tiff')]
    # Setup files
    setup_files: list[Path] = [Path('data/Test001_19-0kW.m3inp'),
                   Path('data/Calib02_22-03-2023.caldat'),
                   Path('data/Calib02_22-03-2023.cal')]

    trace_file: Path = Path(Path('data/csvfile.csv'))

    data_sim_params = DataSimulatorParams(target_path=Path(args.output),
                                          duration=args.duration,
                                          frequency=args.frequency,
                                          trace_file_once=args.onecsv)
    data_sim = DataSimulator(data_sim_params)
    data_sim.load_data_files(setup_files, trace_file, image_files)
    data_sim.generate_data()

if __name__ == "__main__":
    main()