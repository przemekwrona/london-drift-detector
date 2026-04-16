from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_numer_of_active_vehicles_histogram(parquet_data: Path):
    df = pd.read_parquet(parquet_data)

    # Set the index to curr_time if not already set
    df = df.set_index('curr_time')

    # Resample to 15-minute intervals, counting occurrences
    counts = df.resample('15min').size()

    plt.figure(figsize=(12, 6))
    plt.plot(counts.index, counts.values, marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Number of Active Vehicles')
    plt.title('Number of Active Vehicles Over Time (15-min Intervals)')
    plt.tight_layout()
    plt.show()
    