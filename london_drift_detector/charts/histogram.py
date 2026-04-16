from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def number_of_active_vehicles(parquet_data: Path) -> pd.Series:
    df = pd.read_parquet(parquet_data)

    # Set the index to curr_time if not already set
    df = df.set_index('curr_time')

    # Resample to 60-minute intervals, counting unique trip_ids
    counts = df['trip_id'].resample('10min').nunique()
    counts.index = pd.to_datetime(counts.index, format='%Y-%m-%d %H:%M:%S')

    # Ensure counts are ordered by index (date)
    counts = counts.sort_index()
    return counts


def plot_numer_of_active_vehicles_histogram(parquet_data: Path, plot_target: Path):
    counts_series = number_of_active_vehicles(parquet_data) / 2 - 40

    # Filter index between 03:00 and 23:00
    # The index is datetime, so we can use .index.time for filtering
    mask = (counts_series.index.time >= pd.to_datetime("03:00").time()) & (counts_series.index.time <= pd.to_datetime("23:00").time())
    counts_series = counts_series[mask]

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    plt.figure(figsize=(12, 6))

    # Plot bar plot with x-axis as dates in format HH:MM
    plt.bar(counts_series.index, counts_series.values, width=0.04, color='teal', align='center')

    # Format the X-axis as date in 'HH:MM'
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.xlabel('Time (HH:MM)', fontsize=12)
    plt.ylabel('Number of Vehicles', fontsize=12)
    plt.title('Vehicle Counts Over Time', fontsize=15)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(plot_target)
    plt.close()
