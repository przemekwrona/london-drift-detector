from pathlib import Path
from london_drift_detector.charts import histogram as hist
import pandas as pd


def test_load_parquet_and_plot_histogram(tmp_path):
    # given
    parquet_data = Path(__file__).resolve().parent.parent / "results" / "2024-03-10.parquet"
    # "/Users/wronap/workspace/london-drift-detector/test/london_drift_detector/results/2024-03-10.parquet"

    # when
    data = hist.number_of_active_vehicles(parquet_data)

    # then
    assert pd.Timestamp('2024-03-10 15:45:00') in data.index
    assert data.loc[pd.Timestamp('2024-03-10 15:45:00')] == 66
