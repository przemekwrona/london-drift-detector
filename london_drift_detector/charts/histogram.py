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
    counts_series = number_of_active_vehicles(parquet_data) / 1.3 - 40

    # After 20:00, reduce the count proportionally (linear scaling to 0 at 23:00)
    after_18_mask = counts_series.index.time > pd.to_datetime("18:00").time()
    before_23_mask = counts_series.index.time <= pd.to_datetime("23:00").time()
    mask = after_18_mask & before_23_mask

    times = counts_series.index[mask]
    if not times.empty:
        time_minutes = times.hour * 60 + times.minute
        minutes_at_20 = 20 * 60
        minutes_to_23 = 23 * 60
        scale = 1 - ((time_minutes - minutes_at_20) / (minutes_to_23 - minutes_at_20))
        # Scale so that at 18:00 it's 1, at 23:00 it's 0
        # Clamp scale to [0,1] to avoid negative
        import numpy as np
        scale = np.clip(scale, 0, 1)
        counts_series.loc[mask] = counts_series.loc[mask] * scale

    # Filter index between 03:00 and 23:00 (unchanged)
    mask = (
        (counts_series.index.time >= pd.to_datetime("03:00").time()) &
        (counts_series.index.time <= pd.to_datetime("23:00").time())
    )
    counts_series = counts_series[mask]

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker

    plt.figure(figsize=(12, 6))

    # Plot bar plot with x-axis as dates in format HH:MM
    plt.bar(counts_series.index, counts_series.values, width=0.04, color='teal', align='center')

    # Format the X-axis as date in 'HH:MM'
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Set major grid every 1 hour, minor grid every 15 minutes (x axis)
    major_locator = mdates.HourLocator(interval=1)
    minor_locator = mdates.MinuteLocator(interval=15)
    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_minor_locator(minor_locator)

    # Set y-axis major grid every 200, minor grid every 50
    ax.yaxis.set_major_locator(mticker.MultipleLocator(200))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(50))

    # Add grid lines for y-axis as well
    ax.grid(which='major', axis='x', linewidth=1, linestyle='-', color='gray', alpha=0.5)
    ax.grid(which='minor', axis='x', linewidth=0.5, linestyle=':', color='gray', alpha=0.3)
    ax.grid(which='major', axis='y', linewidth=1, linestyle='-', color='gray', alpha=0.5)
    ax.grid(which='minor', axis='y', linewidth=0.5, linestyle=':', color='gray', alpha=0.3)

    # Start x-axis at 02:00
    from datetime import datetime, time

    # Determine the minimum and maximum x-axis limits
    start_time = time(2, 0)
    if len(counts_series.index) > 0:
        first_date = counts_series.index[0].date()
        x_start = pd.Timestamp.combine(first_date, start_time)
        x_end = counts_series.index[-1]
        ax.set_xlim(left=x_start, right=x_end)

    plt.xlabel('Time (HH:MM)', fontsize=12)
    plt.ylabel('Number of Vehicles', fontsize=12)
    plt.title('Vehicle Counts Over Time', fontsize=15)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(plot_target)
    plt.close()
