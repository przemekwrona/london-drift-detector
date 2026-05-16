from pathlib import Path
import zipfile
from london_drift_detector.merger import file_merger


def process_day_in_month(zip_path: Path) -> (list[Path], list[Path]):
    """
    Extract .zip files in a directory, then walk extracted folders
    and extract any nested .gz files found there.
    """
    if not zip_path.is_file():
        raise ValueError(f"{zip_path} is not a valid file.")

    date_dirs: list[Path] = []
    extracted_dir = _unzip(zip_path)
    _extract_nested_zips(extracted_dir, date_dirs)

    return extracted_dir, date_dirs


def process_month(directory: Path, parquet_result_dir: Path) -> None:
    """
    Extract all .zip files in a directory, then walk extracted folders
    and extract any nested .zip files found there.
    """
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a valid directory.")

    if not parquet_result_dir.exists():
        parquet_result_dir.mkdir(parents=True, exist_ok=True)

    for zip_path in sorted(directory.glob("*.zip")):
        if not zip_path.is_file() or zip_path.name.startswith('.'):
            continue

        extracted_dir, date_dirs = process_day_in_month(zip_path)

        for date_dir in date_dirs:
            parquet_file_name: str = f'{date_dir.name}.parquet'
            output_path = parquet_result_dir / parquet_file_name

            file_merger.merge_csvs_to_parquet(date_dir, output_path)
        
        import shutil
        shutil.rmtree(extracted_dir, ignore_errors=True)
   


def _process_day_in_month(date_dir: Path, parquet_result_dir: Path) -> None:
    parquet_file_name: str = f'{date_dir.name}.parquet'
    output_path = parquet_result_dir / parquet_file_name
    file_merger.merge_csvs_to_parquet(date_dir, output_path)

def _extract_nested_zips(directory: Path, date_directory: list[Path]) -> None:
    for entry in sorted(directory.iterdir()):
        if not entry.is_dir() or entry.name.startswith('.') or '__MACOSX' in entry.parts:
            continue

        import gzip
        import shutil

        if not len(sorted(entry.glob("*.gz"))) == 0:
            date_directory.append(entry)

        for gz_path in sorted(entry.glob("*.gz")):
            if not gz_path.name.startswith('.'):
                # Uncompress .gz file to a file with same name but without .gz extension
                unzipped_path = gz_path.with_suffix('')
                with gzip.open(gz_path, 'rb') as f_in, open(unzipped_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

        _extract_nested_zips(entry, date_directory)


def _unzip(zip_path: Path) -> Path:
    extract_to = zip_path.parent / zip_path.stem
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(extract_to)
    return extract_to
