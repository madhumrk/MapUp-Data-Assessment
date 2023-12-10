import pandas as pd
import datetime

def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
        distance_matrix = pd.DataFrame(squareform(pdist(df)), columns=df.index, index=df.index)

    return distance_matrix
result_matrix = calculate_distance_matrix(df)
print(result_matrix)



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
        distance_matrix = pd.DataFrame(squareform(pdist(df)), columns=df.index, index=df.index)

    return distance_matrix
result_matrix = calculate_distance_matrix(df)
print(result_matrix)

    


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
        avg_distances = df.groupby('id_start')['distance'].mean().reset_index()

    reference_avg_distance = avg_distances.loc[avg_distances['id_start'] == reference_id, 'distance'].iloc[0]

    threshold = 0.1 * reference_avg_distance
    within_threshold_ids = avg_distances[
        (reference_avg_distance - threshold <= avg_distances['distance']) &
        (avg_distances['distance'] <= reference_avg_distance + threshold)
    ]

    sorted_ids = within_threshold_ids['id_start'].sort_values().tolist()

    return sorted_ids




def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
     if 'vehicle_type' not in df.columns or 'distance' not in df.columns:
        raise ValueError("DataFrame must contain 'vehicle_type' and 'distance' columns.")

    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'
        df[column_name] = df.apply(lambda row: row['distance'] * rate_coefficient if row['vehicle_type'] == vehicle_type else 0, axis=1)

    return df

unrolled_df = pd.DataFrame({
    'id_start': [1, 1, 2, 2, 3, 3],
    'id_end': [2, 3, 1, 3, 1, 2],
    'distance': [0.5, 0.7, 1.0, 1.2, 0.8, 1.5],
    'vehicle_type': ['car', 'truck', 'rv', 'car', 'bus', 'moto']
})

result_df = calculate_toll_rate(unrolled_df)
print(result_df)
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
        required_columns = ['id_start', 'id_end', 'timestamp', 'vehicle_type']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("DataFrame must contain columns 'id_start', 'id_end', 'timestamp', and 'vehicle_type'.")

    weekday_intervals = [
        {'start_time': datetime.time(0, 0, 0), 'end_time': datetime.time(10, 0, 0), 'discount_factor': 0.8},
        {'start_time': datetime.time(10, 0, 0), 'end_time': datetime.time(18, 0, 0), 'discount_factor': 1.2},
        {'start_time': datetime.time(18, 0, 0), 'end_time': datetime.time(23, 59, 59), 'discount_factor': 0.8},
    ]
    weekend_intervals = [
        {'start_time': datetime.time(0, 0, 0), 'end_time': datetime.time(23, 59, 59), 'discount_factor': 0.7},
    ]

    def calculate_rate(row):
        intervals = weekday_intervals if row['timestamp'].weekday() < 5 else weekend_intervals
        for interval in intervals:
            start_time = interval['start_time']
            end_time = interval['end_time']
            discount_factor = interval['discount_factor']
            if start_time <= row['timestamp'].time() <= end_time:
                return discount_factor
        return 1.0 

    df['time_based_toll'] = df.apply(lambda row: calculate_rate(row), axis=1)

    df['start_day'] = df['timestamp'].dt.strftime('%A') 
    df['start_time'] = df['timestamp'].dt.time

    df['end_day'] = (df['timestamp'] + pd.DateOffset(days=6)).dt.strftime('%A')
    df['end_time'] = datetime.time(23, 59, 59)

    return df

df = pd.DataFrame({
    'id_start': [1, 2, 3],
    'id_end': [2, 3, 1],
    'timestamp': pd.to_datetime(['2023-12-10 03:30:00', '2023-12-10 08:45:00', '2023-12-10 14:20:00']),
    'vehicle_type': ['car', 'truck', 'rv']
})

result_df = calculate_time_based_toll_rates(df)
print(result_df)

    return df
