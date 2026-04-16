import sys


def merger():
    """
    An example script for Poetry entry points.

    Usage:
        poetry run merge-csvs single --directory <input_dir> --output <output_file>
        poetry run merge-csvs batch --directory <parent_dir> --output <output_dir>
    """

    from pathlib import Path
    import argparse
    from london_drift_detector.merger import file_merger as prqt

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


def plot_hist():
    import argparse
    import sys
    from pathlib import Path
    import london_drift_detector.charts.histogram as hst

    def plot_hist_single(input_path: Path, output_path: Path):
        """
        Plot a histogram for a single Parquet file, saving to the given output path.
        """
        hst.plot_numer_of_active_vehicles_histogram(
            input_path,
            output_path
        )

    def plot_hist_batch(input_dir: Path):
        """
        Plot histograms for all Parquet files in the directory.
        """
        hst.batch_number_of_active_vehicles(input_dir)

    def plot_hist_help():
        """
        Print detailed usage and examples for plot-hist.
        """
        help_text = """
Usage: poetry run python main.py plot-hist <subcommand> [options]

Subcommands:
  single    Plot a histogram from a single Parquet file.
  batch     Plot histograms for all Parquet files in a directory.
  help      Show help and usage examples.

Examples:
  # Plot for a single Parquet file and save PDF:
  poetry run python main.py plot-hist single --input ./data/day1.parquet --output ./out/hist_day1.pdf

  # Plot histograms for all Parquet files in a directory:
  poetry run python main.py plot-hist batch --input ./parquet_results/
"""
        print(help_text, file=sys.stderr)

    parser = argparse.ArgumentParser(
        description='Plot histogram(s) of number of active vehicles from Parquet files.'
    )
    subparsers = parser.add_subparsers(dest='subcommand', required=True)

    # Single subcommand
    single_parser = subparsers.add_parser(
        'single', help='Plot a histogram from a single Parquet file.'
    )
    single_parser.add_argument(
        '--input', '-i', required=True, type=str,
        help='Input Parquet file.'
    )
    single_parser.add_argument(
        '--output', '-o', required=True, type=str,
        help='Output file for the plot PDF.'
    )

    # Batch subcommand
    batch_parser = subparsers.add_parser(
        'batch', help='Plot histograms for all Parquet files in a directory.'
    )
    batch_parser.add_argument(
        '--input', '-i', required=True, type=str,
        help='Input directory containing Parquet files.'
    )

    # Help subcommand
    help_parser = subparsers.add_parser(
        'help', help='Show help and example calls for plot-hist.'
    )

    args = parser.parse_args()

    try:
        if args.subcommand == 'single':
            input_path = Path(args.input)
            output_path = Path(args.output)
            if not input_path.is_file():
                parser.error(f"The given --input path '{input_path}' is not a file.")
            plot_hist_single(input_path, output_path)
        elif args.subcommand == 'batch':
            input_dir = Path(args.input)
            if not input_dir.is_dir():
                parser.error(f"The given --input path '{input_dir}' is not a directory.")
            plot_hist_batch(input_dir)
        elif args.subcommand == 'help':
            plot_hist_help()
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nExample usage:")
        plot_hist_help()
        sys.exit(1)

