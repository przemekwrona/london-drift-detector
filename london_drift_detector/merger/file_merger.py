from pathlib import Path
import pandas as pd


def merge_csvs_to_parquet(directory: Path, output_path: Path):
    """
    Merges all .csv files in a given directory into a single DataFrame and saves as a parquet file.
    When reading CSVs, explicitly sets column names and their types.
    
    Args:
        directory (Path): Directory containing .csv files.
        output_filename (str): Name of the output parquet file.
    """
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory.")

    csv_files = sorted(directory.glob("*.csv"))
    if not csv_files:
        # Test fixtures and GTFS-like snapshots are often exported as part-* files
        # without a .csv suffix. Support them as CSV inputs as well.
        csv_files = sorted(
            file_path
            for file_path in directory.glob("part-*")
            if file_path.is_file()
        )

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV-like files found in {directory} (expected *.csv or part-*)"
        )

    # Define column names and types
    columns = [
        "city", "trip_id", "line", "stop_id",
        "curr_trip_id", "curr_stop_name", "curr_time", "curr_delay",
        "prev_trip_id", "prev_stop_name", "prev_time", "prev_delay",
        "diff", "orig_trip_id", "orig_stop_name"
    ]
    # Assign types. Change as needed based on actual expected types.
    dtypes = {
        "city": "string",
        "trip_id": "string",
        "line": "Int64",  # pandas nullable integer
        "stop_id": "Int64",
        "curr_trip_id": "string",
        "curr_stop_name": "string",
        "curr_time": "string",  # We'll convert this to datetime after reading
        "curr_delay": "Int64",
        "prev_trip_id": "string",
        "prev_stop_name": "string",
        "prev_time": "string",
        "prev_delay": "Int64",
        "diff": "Int64",
        "orig_trip_id": "string",
        "orig_stop_name": "string"
    }

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(
            csv_file,
            sep=';',
            header=None,
            names=columns,
            dtype=dtypes
        )

        # Convert curr_time to datetime in the specified format
        # Ensure all 'curr_time' strings have seconds (add ':00' if missing)
        def add_seconds_if_missing(time_str):
            if pd.isna(time_str):
                return time_str
            # If the time part (after T) does not have seconds, add ':00'
            if 'T' in time_str:
                time_part = time_str.split('T')[1]
                if len(time_part.split(':')) == 2:
                    return time_str + ':00'
            return time_str

        df["curr_time"] = df["curr_time"].apply(add_seconds_if_missing)
        df["curr_time"] = pd.to_datetime(df["curr_time"], format="%Y-%m-%dT%H:%M:%S")

        df["prev_time"] = df["prev_time"].apply(add_seconds_if_missing)
        df["prev_time"] = pd.to_datetime(df["prev_time"], format="%Y-%m-%dT%H:%M:%S")
        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_parquet(output_path, index=False)
    print(f"Merged {len(csv_files)} CSVs and saved to {output_path}")
