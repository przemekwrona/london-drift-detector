import sys
from pathlib import Path
import argparse
from london_drift_detector.merger import file_merger as prqt


def main():
    """
    An example script for Poetry entry points.

    Usage:
        poetry run merge-csvs single --directory <input_dir> --output <output_file>
        poetry run merge-csvs batch --directory <parent_dir> --output <output_dir>
    """

    parser = argparse.ArgumentParser(description="Merge CSV files into Parquet (single directory or batch mode).")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Single file
    single_parser = subparsers.add_parser(
        'single',
        help='Merge all CSVs in a directory into a single Parquet file.'
    )
    single_parser.add_argument(
        '--directory', '-d', required=True, type=str,
        help="Directory containing CSV files."
    )
    single_parser.add_argument(
        '--output', '-o', required=True, type=str,
        help="Output Parquet file path."
    )

    # Batch mode
    batch_parser = subparsers.add_parser(
        'batch',
        help='Merge all CSVs in each subdirectory, outputting one Parquet per subdirectory.'
    )
    batch_parser.add_argument(
        '--directory', '-d', required=True, type=str,
        help="Parent directory containing subdirectories with CSVs."
    )
    batch_parser.add_argument(
        '--output', '-o', required=True, type=str,
        help="Output directory for Parquet files."
    )

    # Add a 'help' subcommand to show help
    help_parser = subparsers.add_parser(
        'help',
        help='Show help for a specific subcommand'
    )
    help_parser.add_argument(
        'subcommand',
        nargs='?',
        default=None,
        help='Subcommand to show help for (single or batch)'
    )

    args = parser.parse_args()

    # How to call method help for argparse command/subparser in Python:
    try:
        if args.command == 'single':
            prqt.merge_csvs_to_parquet(
                directory=Path(args.directory),
                output_path=Path(args.output)
            )
        elif args.command == 'batch':
            prqt.merge_csvs_in_directories_to_parquest(
                directory=Path(args.directory),
                output_path=Path(args.output)
            )
        elif args.command == 'help':
            # Show help for the specified subcommand or the main parser
            if args.subcommand == 'single':
                single_parser.print_help()
            elif args.subcommand == 'batch':
                batch_parser.print_help()
            else:
                parser.print_help()
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nExample usage:")
        print("  poetry run python main.py single --directory ./input_csvs --output ./output/merged.parquet")
        print("  poetry run python main.py batch --directory ./input_dirs --output ./output_dir")
        sys.exit(1)
