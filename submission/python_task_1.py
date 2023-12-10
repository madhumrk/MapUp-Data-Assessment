import pandas as pd

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
        df = df.pivot(index='id_1', columns='id_2', values='car')
    return df
print(df)


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
        df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], include_lowest=True)

    car_type_counts = df['car_type'].value_counts().to_dict()

    car_type_counts = dict(sorted(car_type_counts.items()))

    return car_type_counts

result = get_type_count(df)
print(result) 

    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
        bus_indexes = df[df['bus'] > 2 * df['bus'].mean()].index.tolist()
    return bus_indexes

result = get_bus_indexes(df)
print(result)



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    selected_routes.sort()

    return selected_routes

result = filter_routes(df)
print(result)

    return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    modified_matrix = modified_matrix.round(1)

    return modified_matrix

modified_result = multiply_matrix(df)

print(modified_result)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
        df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    completeness_check = df.groupby(['id', 'id_2']).apply(
        lambda group: (
            (group['start_timestamp'].min().time() == pd.Timestamp('00:00:00').time()) and
            (group['end_timestamp'].max().time() == pd.Timestamp('23:59:59').time()) and
            (group['start_timestamp'].min().day_name() == 'Monday') and
            (group['end_timestamp'].max().day_name() == 'Sunday')
        )
    )

    return completeness_check

    return pd.Series()
