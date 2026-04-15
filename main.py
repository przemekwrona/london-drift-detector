import argparse
import sys
from pathlib import Path
from london_drift_detector.merger import file_merger as prqt


def merge_csvs_to_parquet_cmd(args):
    try:
        prqt.merge_csvs_to_parquet(
            directory=Path(args.directory),
            output_path=Path(args.output)
        )
    except Exception as e:
        print(f"Error during merging CSVs to parquet: {e}", file=sys.stderr)
        sys.exit(1)


def merge_csvs_in_directories_to_parquet_cmd(args):
    try:
        prqt.merge_csvs_in_directories_to_parquest(
            directory=Path(args.directory),
            output_path=Path(args.output)
        )
    except Exception as e:
        print(f"Error during merging CSV directories to parquet: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Merge CSV files into Parquet (single or batch mode)."
    )
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='Commands'
    )

    # Single merge parser
    single = subparsers.add_parser(
        'single',
        help='Merge all CSV files in a directory into a single Parquet file.'
    )
    single.add_argument(
        '--directory', '-d', type=str, required=True,
        help='Directory containing the CSV files.'
    )
    single.add_argument(
        '--output', '-o', type=str, required=True,
        help='Path for output Parquet file.'
    )
    single.set_defaults(func=merge_csvs_to_parquet_cmd)

    # Batch merge parser
    batch = subparsers.add_parser(
        'batch',
        help='Merge CSVs in each subdirectory, outputting one Parquet per subdirectory.'
    )
    batch.add_argument(
        '--directory', '-d', type=str, required=True,
        help='Parent directory containing subdirectories with CSVs.'
    )
    batch.add_argument(
        '--output', '-o', type=str, required=True,
        help='Output directory for Parquet files.'
    )
    batch.set_defaults(func=merge_csvs_in_directories_to_parquet_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
