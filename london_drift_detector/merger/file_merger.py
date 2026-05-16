from pathlib import Path
import pandas as pd

# Define column names and types
# columns = [
#     "city", "trip_id", "line", "stop_id",
#     "curr_trip_id", "curr_stop_name", "curr_time", "curr_delay",
#     "prev_trip_id", "prev_stop_name", "prev_time", "prev_delay",
#     "diff", "orig_trip_id", "orig_stop_name"
# ]

columns = [
    "city_code",                # WAWA
    "vehicle_id",               # 4268
    "vehicle_type",             # TRAM
    "line_number",              # 28
    "brigade",                  # 7
    "current_lat",              # 52.239143
    "current_lon",              # 20.901497
    "curr_time",                # 2024-06-10 14:53:41
    "lat_replica",              # 52.239143
    "lon_replica",              # 20.901497
    "status",                   # MOVING
    "speed_or_distance_1",      # 1.0667854554817398
    "speed_or_distance_2",      # 0.0
    "next_stop_name",           # 5035-Klemensiewicza
    "scheduled_time_1",         # 2024-06-10 14:55:00
    "end_stop_name",            # 5050-os.Górczewska
    "distance_to_stop",         # 67.44592823803308
    "stop_lon",                 # 20.900861
    "stop_lat",                 # 52.238678
    "end_stop_name_replica",    # 5050-os.Górczewska
    "end_stop_lat",             # 52.238678
    "end_stop_lon",             # 20.900861
    "distance_replica",         # 67.44592823803308
    "timestamp_2",              # 2024-06-10 14:53:26
    "timestamp_3",              # 2024-06-10 14:53:26
    "start_stop_name",          # 5035-Klemensiewicza
    "start_stop_lat",           # 52.238965
    "start_stop_lon",           # 20.905475
    "distance_to_next",         # 271.5931435758215
    "scheduled_time_2",         # 2024-06-10 14:55:00
    "trip_id",                  # 28_7_139_1453
    "route_destination",        # Dw.Wschodni (Kijowska)
    "time_window",              # 2024-06-10 14:53:00-2024-06-10 15:50:00
    "safety_status",            # UNSAFE
    "timestamp_4",              # 2024-06-10 14:53:41
    "iso_timestamp",            # 2024-06-10T14:53:47.804
    "is_delayed",               # false
    "is_diverted",              # false
    "empty_column",             # (blank value)
    "is_wheelchair_accessible", # false
    "metric_1",                 # 1,07
    "metric_2",                 # 0.0
    "data_source",              # WUT (Warsaw University of Technology / PW)
    "stop_sequence_1",          # 2
    "stop_sequence_2",          # 1
    "stop_sequence_3",          # 2
    "stop_id_1",                # 5035_03_3
    "stop_id_2",                # 5050_13_13
    "stop_id_3",                # 5035_03_3
    "route_id"                  # 1028_15_15
]

# Assign types. Change as needed based on actual expected types.
# dtypes = {
#     "city": "string",
#     "trip_id": "string",
#     "line": "string",  # pandas nullable integer
#     "stop_id": "string",
#     "curr_trip_id": "string",
#     "curr_stop_name": "string",
#     "curr_time": "string",  # We'll convert this to datetime after reading
#     "curr_delay": "Int64",
#     "prev_trip_id": "string",
#     "prev_stop_name": "string",
#     "prev_time": "string",
#     "prev_delay": "Int64",
#     "diff": "Int64",
#     "orig_trip_id": "string",
#     "orig_stop_name": "string"
# }

dtypes = [
    ("city_code", "str"),                 # 'WAWA'
    ("vehicle_id", "str"),                # 4268
    ("vehicle_type", "str"),              # 'TRAM'
    ("line_number", "str"),               # 28
    ("brigade", "str"),                   # 7
    ("current_lat", "float"),             # 52.239143
    ("current_lon", "float"),             # 20.901497
    ("timestamp_1", "str"),               # '2024-06-10 14:53:41'
    ("lat_replica", "float"),             # 52.239143
    ("lon_replica", "float"),             # 20.901497
    ("status", "str"),                    # 'MOVING'
    ("speed_or_distance_1", "float"),     # 1.0667854554817398
    ("speed_or_distance_2", "float"),     # 0.0
    ("next_stop_name", "str"),            # '5035-Klemensiewicza'
    ("scheduled_time_1", "str"),          # '2024-06-10 14:55:00'
    ("end_stop_name", "str"),             # '5050-os.Górczewska'
    ("distance_to_stop", "float"),        # 67.44592823803308
    ("stop_lon", "float"),                # 20.900861
    ("stop_lat", "float"),                # 52.238678
    ("end_stop_name_replica", "str"),     # '5050-os.Górczewska'
    ("end_stop_lat", "float"),            # 52.238678
    ("end_stop_lon", "float"),            # 20.900861
    ("distance_replica", "float"),        # 67.44592823803308
    ("timestamp_2", "str"),               # '2024-06-10 14:53:26'
    ("timestamp_3", "str"),               # '2024-06-10 14:53:26'
    ("start_stop_name", "str"),           # '5035-Klemensiewicza'
    ("start_stop_lat", "float"),          # 52.238965
    ("start_stop_lon", "float"),          # 20.905475
    ("distance_to_next", "float"),        # 271.5931435758215
    ("scheduled_time_2", "str"),          # '2024-06-10 14:55:00'
    ("trip_id", "str"),                   # '28_7_139_1453'
    ("route_destination", "str"),         # 'Dw.Wschodni (Kijowska)'
    ("time_window", "str"),               # '2024-06-10 14:53:00-2024-06-10 15:50:00'
    ("safety_status", "str"),             # 'UNSAFE'
    ("timestamp_4", "str"),               # '2024-06-10 14:53:41'
    ("iso_timestamp", "str"),             # '2024-06-10T14:53:47.804'
    ("is_delayed", "bool"),               # false
    ("is_diverted", "bool"),              # false
    ("empty_column", "str"),              # blank
    ("is_wheelchair_accessible", "bool"), # false
    ("metric_1", "str"),                  # 1,07
    ("metric_2", "float"),                # 0.0
    ("data_source", "str"),               # 'WUT'
    ("stop_sequence_1", "str"),         # 2
    ("stop_sequence_2", "str"),         # 1
    ("stop_sequence_3", "str"),         # 2
    ("stop_id_1", "str"),                 # '5035_03_3'
    ("stop_id_2", "str"),                 # '5050_13_13'
    ("stop_id_3", "str"),                 # '5035_03_3'
    ("route_id", "str")                   # '1028_15_15'
]

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
            if file_path.is_file() and not file_path.name.endswith('.gz')
       
        )

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV-like files found in {directory} (expected *.csv or part-*)"
        )

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
        df["curr_time"] = pd.to_datetime(df["curr_time"], format="%Y-%m-%d %H:%M:%S")

        # df["prev_time"] = df["prev_time"].apply(add_seconds_if_missing)
        # df["prev_time"] = pd.to_datetime(df["prev_time"], format="%Y-%m-%d %H:%M:%S")
        # df["prev_time"] = pd.to_datetime(df["prev_time"], format="%Y-%m-%dT%H:%M:%S")
        dfs.append(df)

    merged_df = pd.concat(dfs, ignore_index=True)
    # merged_df = merged_df.sort_values(by="curr_time").reset_index(drop=True)
    merged_df.to_parquet(output_path, index=False)
    print(f"Merged {len(csv_files)} CSVs and saved to {output_path}")


def merge_csvs_in_directories_to_parquest(directory: Path, output_path: Path):
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    for subdirectory in directory.iterdir():
        if subdirectory.is_dir():
            subdirectory_name = subdirectory.name

            (output_path / subdirectory_name).mkdir(parents=True, exist_ok=True)

            parquet_output_path = output_path / subdirectory_name / f'{subdirectory_name}.parquet'

            merge_csvs_to_parquet(subdirectory, parquet_output_path)
