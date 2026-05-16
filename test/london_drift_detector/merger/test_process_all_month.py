from pathlib import Path
from london_drift_detector.merger import month_processor


def test_process_all_month(tmp_path):
    # given
    source_dir = Path('/Volumes/T7/data/delay_v2')
    output_dir = Path('/Volumes/T7/data/delay_v2_results/')

    # when
    month_processor.process_month(source_dir, output_dir)

    assert True


def test_process_month_unzips_top_level_and_nested_zips(tmp_path):
    # given
    directory = Path(__file__).resolve().parent.parent / "resources" / "process_all_month"
    # output_path = Path(tmp_path).resolve() / "results"
    output_path = Path(__file__).resolve().parent.parent / "resources" / "process_all_month" / "results"

    directory = Path(__file__).resolve().parent.parent / "resources" / "process_all_month"
    # output_path = Path(tmp_path).resolve() / "results"
    output_path = Path(__file__).resolve().parent.parent / "resources" / "process_all_month" / "results"

    # when
    month_processor.process_month(directory, output_path)

    # then
    assert True
