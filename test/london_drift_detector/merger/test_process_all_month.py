from pathlib import Path
import shutil
import zipfile

from london_drift_detector.merger import month_processor


def test_process_month_unzips_top_level_and_nested_zips(tmp_path):
    # given
    directory = Path(__file__).resolve().parent.parent / "resources" / "process_all_month"
    # output_path = Path(tmp_path).resolve() / "results"
    output_path = Path(__file__).resolve().parent.parent / "resources" / "results"

    # when
    month_processor.process_month(directory)

    # then
    assert True


def test_process_month_with_resource_zip(tmp_path):
    resource_dir = (
        Path(__file__).resolve().parent.parent
        / "resources"
        / "process_all_month"
    )
    work_dir = tmp_path / "month"
    work_dir.mkdir()
    shutil.copy(
        resource_dir / "10_06_24_vehicles-live-with-timetable.zip",
        work_dir,
    )

    extracted = process_month(work_dir)

    assert len(extracted) == 1
    gz_files = list(extracted[0].rglob("*.gz"))
    assert gz_files
