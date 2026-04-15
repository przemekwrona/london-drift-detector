from pathlib import Path
import pandas as pd


def merge_csvs_to_parquet(directory: Path, output_filename: str = "merged.parquet"):
    """
    Merges all .csv files in a given directory into a single DataFrame and saves as a parquet file.
    
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

    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=';')
        dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)
    output_path = directory / output_filename
    merged_df.to_parquet(output_path, index=False)
    print(f"Merged {len(csv_files)} CSVs and saved to {output_path}")
