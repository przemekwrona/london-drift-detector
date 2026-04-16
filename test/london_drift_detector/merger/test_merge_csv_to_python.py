from pathlib import Path
from london_drift_detector.merger import file_merger as prqt

import pandas as pd


def test_read_csv_and_save_as_parquest_in_folder_2026_04_12(tmp_path):
    # given
    directory = Path(__file__).resolve().parent.parent / "resources" / "2024-03-10"
    output_path = tmp_path / "2024_03_10.parquet"

    # when
    prqt.merge_csvs_to_parquet(directory=directory, output_path=output_path)

    # then
    assert output_path.exists(), f"Expected output parquet file at {output_path} does not exist."

    df = pd.read_parquet(output_path)
    assert df.shape[0] > 0, f"Expected non-empty DataFrame, got {df.shape[0]} rows."
    assert df.shape[1] == 15, f"Expected 13 columns, got {df.shape[1]} columns."
    assert df.columns.tolist() == [
        "city", "trip_id", "line", "stop_id",
        "curr_trip_id", "curr_stop_name", "curr_time", "curr_delay",
        "prev_trip_id", "prev_stop_name", "prev_time", "prev_delay",
        "diff", "orig_trip_id", "orig_stop_name"
    ], f"Expected columns {df.columns.tolist()}, got {df.columns.tolist()}."
    assert df["city"].nunique() == 1, f"Expected 1 unique city, got {df['city'].nunique()}."
    assert df["trip_id"].nunique() > 0, f"Expected non-empty trip_id column, got {df['trip_id'].nunique()} unique values."
    assert df["line"].nunique() > 0, f"Expected non-empty line column, got {df['line'].nunique()} unique values."
    assert df["stop_id"].nunique() > 0, f"Expected non-empty stop_id column, got {df['stop_id'].nunique()} unique values."


def test_read_directory_then_csv_and_save_as_parquest_in_folder(tmp_path):
    # given
    directory = Path(__file__).resolve().parent.parent / "resources"
    output_path = Path(__file__).resolve().parent.parent / "results"
    # output_path = tmp_path / "2024_03_10.parquet"

    # when
    prqt.merge_csvs_in_directories_to_parquest(directory, output_path)

    # then
    assert output_path.exists(), f"Expected output parquet file at {output_path} does not exist."
    assert output_path.is_dir(), f"Expected output path to be a directory, got {output_path.is_dir()}."

    # Check if a file with name '2024-03-10.parquet' exists in output_path
    assert len(list((output_path / "2024-03-10").iterdir())) == 1, f"Expected 1 parquet file in output path, got {len(list(output_path.iterdir()))}."
    expected_file = output_path / "2024-03-10" / "2024-03-10.parquet"
    assert expected_file.exists(), f"Expected output file {expected_file} does not exist."
