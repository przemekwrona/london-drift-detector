from pathlib import Path
from london_drift_detector.charts import histogram as hist
import pandas as pd


def test_load_parquet_and_plot_histogram(tmp_path):
    # given
    parquet_path = Path(__file__).resolve().parent.parent / "results" / "2024-03-10.parquet"

    # when
    data = hist.number_of_active_vehicles(parquet_path)

    # then
    assert pd.Timestamp('2024-03-10 15:40:00') in data.index
    assert data.loc[pd.Timestamp('2024-03-10 15:40:00')] == 65
