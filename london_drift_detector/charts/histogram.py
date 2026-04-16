from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def number_of_active_vehicles(parquet_data: Path) -> pd.Series:
    df = pd.read_parquet(parquet_data)
    # Set the index to curr_time if not already set
    df = df.set_index('curr_time')
    # Resample to 15-minute intervals, counting occurrences
    counts = df.resample('15min').size()
    return counts


def plot_numer_of_active_vehicles_histogram(parquet_data: Path):
    counts = number_of_active_vehicles(parquet_data)

    import matplotlib.dates as mdates

    plt.figure(figsize=(12, 6))
    plt.plot(counts.index, counts.values, marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Number of Active Vehicles')
    plt.title('Number of Active Vehicles Over Time (15-min Intervals)')

    # Set x labels from 00:00 to 24:00
    ax = plt.gca()
    # Set major locator and formatter for every hour between 00:00 and 24:00
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 25), interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xlim(counts.index.min().replace(hour=0, minute=0), 
             counts.index.max().replace(hour=23, minute=59))

    plt.tight_layout()
    plt.show()
