from pathlib import Path
from london_drift_detector.merger import file_merger as prqt


def test_read_csv_and_save_as_parquest_in_folder_2026_04_12(tmp_path):
    # given
    directory = Path(__file__).resolve().parent.parent / "resources" / "2024-03-10"

    # when
    prqt.merge_csvs_to_parquet(directory=directory)

    # then
