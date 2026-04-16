from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def number_of_active_vehicles(parquet_data: Path) -> pd.Series:
    df = pd.read_parquet(parquet_data)
    # Set the index to curr_time if not already set
    df = df.set_index('curr_time')
    # Resample to 15-minute intervals, counting occurrences, and name the column 'count'
    counts = df.resample('20s').size()
    return counts


def plot_numer_of_active_vehicles_histogram(parquet_data: Path, plot_target: Path):
    counts_series = number_of_active_vehicles(parquet_data)

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # 1. Convert index strings to datetime objects
    # The format matches 'yyyy-MM-dd HH:mm:SS:SSS'
    counts_series.index = pd.to_datetime(counts_series.index, format='%Y-%m-%d %H:%M:%S:%f')

    # 2. Set the visual style
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    # 3. Create the line plot
    sns.lineplot(x=counts_series.index, y=counts_series.values, color='teal')

    # 4. Format the X-axis to make dates readable
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)  # Rotate for better visibility

    plt.title('Vehicle Counts Over Time', fontsize=15)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Number of Vehicles', fontsize=12)
    plt.tight_layout()

    plt.savefig('vehicle_time_series.png')

    # plt.figure(figsize=(12, 6))
    # plt.plot(counts.index, counts.values, marker='o', linestyle='-')
    # # plt.xlabel('Time')
    # plt.ylabel('Number of Active Vehicles')
    # plt.title('Number of Active Vehicles Over Time (15-min Intervals)')
    #
    # # Set x labels from 00:00 to 24:00
    # ax = plt.gca()
    # # Set major locator and formatter for every hour between 00:00 and 24:00
    # ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 25), interval=1))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # # Set minor locator for every 30 minutes
    # ax.xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 15, 30, 45]))
    # plt.xlim(counts.index.min().replace(hour=4, minute=0),
    #          counts.index.max().replace(hour=23, minute=59))
    # plt.ylim(0, 200)
    # plt.grid(True, which='both', axis='both', linestyle='-', alpha=0.7)
    # # Add subgrid for every 30 minutes, lighter grid
    # plt.grid(True, which='minor', axis='x', linestyle='-', alpha=0.2)
    #
    # plt.tight_layout()
    # plt.savefig(plot_target)
    # plt.close()
