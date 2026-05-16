from pathlib import Path
import gzip
import pandas as pd
import os


def unpack_and_select_columns(input_dir: Path, columns_to_select):
    """
    For all .gz files in the given directory:
      - Unpack each .gz file
      - Read as CSV
      - Select the specified columns
      - Save the filtered DataFrame as a CSV with the same base filename + '_part.csv'
    """
    gz_files = list(input_dir.glob("*.gz"))
    for gz_file in gz_files:
        with gzip.open(gz_file, 'rt') as f:
            # Define column names and types (example: adjust as needed)
            # Proposed column names, based on sample 2 rows:
            column_types = {
                'city': str,
                'vehicle_id': str,
                'vehicle_type': str,
                'line': str,
                'brigade': str,
                'latitude': float,
                'longitude': float,
                'process_date': str,
                'next_latitude': float,
                'next_longitude': float,
                'state': str,
                'speed': float,
                'bearing': float,
                'stop_name_1': str,
                'stop_time_1': str,
                'stop_name_2': str,
                'distance_1': float,
                'stop_longitude_1': float,
                'stop_latitude_1': float,
                'stop_name_3': str,
                'stop_latitude_2': float,
                'stop_longitude_2': float,
                'distance_2': float,
                'prev_stop_time_1': str,
                'prev_stop_time_2': str,
                'stop_name_4': str,
                'stop_latitude_3': float,
                'stop_longitude_3': float,
                'distance_3': float,
                'stop_time_2': str,
                'trip_id': str,
                'final_stop_name': str,
                'trip_time_slot': str,
                'security_status': str,
                'process_start_time': str,
                'process_end_time': str,
                'has_problem': str,
                'has_error': str,
                'field_x_1': str,
                'is_finished': str,
                'unknown_monetary_value': str,
                'unknown_float_1': float,
                'institution': str,
                'unknown_int_1': str,
                'unknown_int_2': str,
                'unknown_int_3': str,
                'bus_line_seg_1': str,
                'bus_line_seg_2': str,
                'bus_line_seg_3': str,
                'bus_line_seg_4': str,
            }

            column_names = list(column_types.keys())

            print(f'Process file {f.name}...')

            try:
                df = pd.read_csv(f, sep=';', names=column_names, dtype=column_types, header=0)
                # Convert 'process_date' to datetime with format 'yyyy-MM-dd HH:MM:SS.sss'
                df['process_date'] = pd.to_datetime(df['process_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
           
         
                selected_df = df[columns_to_select]
                out_file = gz_file.with_suffix('').with_name(gz_file.stem + '_part.csv')
                selected_df.to_csv(out_file, index=False)
            except OSError as e:
                from gzip import BadGzipFile
                if isinstance(e, BadGzipFile):
                    print(f"Skipping file {gz_file} due to BadGzipFile: {e}")
                else:
                    raise

    # Gather all generated "_part.csv" files in the output directory
    part_csv_files = list(gz_file.parent.glob('*_part.csv'))
    if part_csv_files:
        merged_csv = gz_file.parent / 'merged.csv'
        dfs = [pd.read_csv(pf) for pf in part_csv_files]
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_parquet = gz_file.parent / 'merged.parquet'
        merged_df.to_parquet(merged_parquet, index=False)
   
        # Remove the part csv files
        for pf in part_csv_files:
            try:
                os.remove(pf)
            except OSError as ex:
                print(f"Failed to remove {pf}: {ex}")
