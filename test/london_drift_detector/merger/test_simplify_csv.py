from pathlib import Path
from london_drift_detector.merger import csv_simpliier


def test_read_gz_files_in_directory_unpack_and_simplify_csv(tmp_path):
    # given
    directory_with_gz = Path('/Users/wronap/data/2024-03-01-test')
    directory_with_gz = Path('/Volumes/T7/data/2024-03-01/')
    selected_columns = ['city', 'vehicle_id', 'vehicle_type', 'line', 'brigade', 'latitude', 'longitude', 'process_date']

    # when
    csv_simpliier.unpack_and_select_columns(directory_with_gz, selected_columns)

    # then
    assert True
