import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta
from datetime import datetime
# from oscillation_cython import find_oscillation_points
from spotter_oscillation.oscillation_cython import find_oscillation_points

# License Notice
"""
This software is provided for educational use only. Commercial use, including but not limited to, sale, lease, or provision of services using this software, is strictly prohibited without explicit permission from the author.

Additionally, redistribution or modification of this software without the owner's consent is strictly prohibited.

© Raziel Ella Analytics Module v1.0 - Unauthorized use prohibited.
"""

# Main computation functions
def append_trend_type(df, price_column):
    """
    Append trend type to the DataFrame based on detected oscillations.

    Parameters:
    df (DataFrame): The input DataFrame containing price data.
    price_column (str): The name of the column containing price information.

    Returns:
    DataFrame: DataFrame with an additional column 'trend_type' indicating the trend type ('Stable', 'Positive', 'Negative').
    """
    df['trend_type'] = 'Stable'  # Default to 'Stable'
    oscillation_points = filter_oscillations(find_oscillation_points(df, price_column), df, price_column)

    for start, end, osc_type in oscillation_points:
        df.loc[start:end, 'trend_type'] = osc_type

    return df

def filter_oscillations(oscillation_data, df, price_column):
    """
    Filter oscillations based on a minimum percentage change threshold.

    Parameters:
    oscillation_data (list): List of detected oscillation points (start, end, type).
    df (DataFrame): The input DataFrame containing price data.
    price_column (str): The name of the column containing price information.

    Returns:
    list: Filtered list of oscillation points that meet the minimum percentage change requirement.
    """
    filtered_oscillation_data = [
        (start, end, osc_type) for start, end, osc_type in oscillation_data
        if abs((df.loc[end, price_column] - df.loc[start, price_column]) / df.loc[start, price_column] * 100) >= 0.34
    ]
    return filtered_oscillation_data

def unify_oscillations(oscillation_points):
    """
    Unify consecutive oscillations of the same type if they are close in time.

    Parameters:
    oscillation_points (list): List of detected oscillation points (start, end, type).

    Returns:
    list: Unified list of oscillation points.
    """
    if not oscillation_points:
        return []

    # Start with the first oscillation
    unified_oscillations = [oscillation_points[0]]

    for current_start, current_end, current_type in oscillation_points[1:]:
        # Get the last oscillation from the unified list
        last_start, last_end, last_type = unified_oscillations[-1]

        # Calculate the gap between the last end and the current start
        time_gap = (current_start - last_end).total_seconds()

        # Check if the current and last oscillations are of the same type and the time gap is less than 140 seconds
        if current_type == last_type and time_gap < 140:
            # Merge the current oscillation with the last one
            # Update the end time of the last oscillation
            unified_oscillations[-1] = (last_start, current_end, last_type)
        else:
            # If not mergeable, add the current oscillation to the list
            unified_oscillations.append((current_start, current_end, current_type))

    return unified_oscillations

def find_nearest_index(df, target_time):
    """
    Find the nearest index in the DataFrame to the target time.

    Parameters:
    df (DataFrame): The input DataFrame with a datetime index.
    target_time (datetime): The target time to find the nearest index for.

    Returns:
    int: Index of the row closest to the target time.
    """
    time_diff = abs(df.index - target_time)
    nearest_index = time_diff.argmin()
    return nearest_index

def process_oscillations(df, time_column, price_column, plot=False):
    """
    Main function to process the DataFrame for oscillations.

    Parameters:
    df (DataFrame): The input DataFrame containing price data.
    time_column (str): Name of the time column.
    price_column (str): Name of the price column.
    plot (bool, optional): Whether to plot the results. Defaults to False.

    Returns:
    DataFrame: Processed DataFrame with detected oscillations.
    """
    # Convert the time column to datetime format and drop rows with missing values
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
    df = df[df[price_column] != 0]
    df = df.dropna(subset=[time_column])

    # Sort values by time and set the time column as the index
    df = df.sort_values(by=time_column).reset_index(drop=True)
    df.set_index(time_column, inplace=True)
    df = df[~df.index.duplicated(keep='first')]
    df['time_numeric'] = (df.index - df.index[0]).total_seconds()

    # Process the oscillations
    oscillation_data = filter_oscillations(find_oscillation_points(df, price_column), df, price_column)

    # Optional Plotting
    if plot:
        fig, ax = plt.subplots(figsize=(15, 7))
        ax.plot(df.index, df[price_column], label='Prices')

        for start, end, osc_type in oscillation_data:
            color = 'green' if osc_type == 'Positive' else 'red'
            ax.axvline(x=start, color=color, linestyle='--', linewidth=2, label='New Oscillation Start' if osc_type == 'Positive' else 'New Oscillation End')
            ax.axvline(x=end, color=color, linestyle='--', linewidth=2)
            ax.fill_betweenx(y=[df[price_column].min(), df[price_column].max()], x1=start, x2=end, color=color, alpha=0.3)

            start_price = df.loc[start, price_column]
            end_price = df.loc[end, price_column]
            trend_size = (end_price - start_price) / start_price * 100
            midpoint_time = start + (end - start) / 2
            ax.annotate(f'{trend_size:.2f}%', xy=(midpoint_time, df.loc[start:end, price_column].max()),
                        textcoords='offset points', xytext=(0, 10), ha='center', color=color)

        ax.set_title('Price Oscillations')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price (USD)')
        ax.legend()

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator())
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return df
