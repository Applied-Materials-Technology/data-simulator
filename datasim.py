from pathlib import Path
from datasimlib import ExperimentDataGenerator
import argparse

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", default = 1000, type = float)
    parser.add_argument("--onecsv", default = False, type = bool)
    parser.add_argument("--output", default = 'outputs', type = str)
    parser.add_argument("--frequency", default = 1.0, type = float)

    args = parser.parse_args()

    image_files = [Path('data/OptSpeckle_5Mpx_2464_2056_width5_8bit_GBlur1.tiff'), 
                   Path('data/OptSpeckle_5Mpx_2464_2056_width5_8bit_GBlur1.tiff')]
    match_id_file = Path('data/Test001_19-0kW.m3inp')
    csv_file = Path('data/csvfile.csv')
    caldat_file = Path('data/Calib02_22-03-2023.caldat')
    cal_file = Path('data/Calib02_22-03-2023.cal')

    example = ExperimentDataGenerator(frequency = args.frequency)

    """csv_file - csv to generate from,
        image_files - base images to generate tiff files from,
        match_id_file - m3inp file to generate from"""
    example.load_data_files(csv_file, image_files, match_id_file, caldat_file, cal_file)

    example.generate_data(duration = args.duration, output_loc = args.output, onecsv = args.onecsv)

if __name__ == "__main__":
    main()