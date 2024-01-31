import pandas as pd
from helper_functions import fetch_data, fetch_granular_data

data_folder = "..\\data"
# Aggregate Data (csv files)
dfs = None
# Granular data (parquet file)
gdf = None


# Data Loading and Caching
def load_agg_data():
    global dfs
    # Load aggregate data
    dfs = fetch_data(mode="server")
    transform_dates()
    # print('data loaded!')
    # print(dfs['donations_state'].iloc[:3,:3])


def load_gdf_data():
    global gdf
    # Load granular data
    gdf = fetch_granular_data(mode="server")


def transform_dates():
    global dfs
    if dfs is None:
        return

    for key, df in dfs.items():
        if "date" in df.columns:
            dfs[key] = df.assign(date=pd.to_datetime(df["date"])).set_index("date")
        else:
            print(f"Dataframe {key} does not have a date column")


# Wrapper Function
def ensure_data_loaded(data_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if data_type == "agg":
                if dfs is None:
                    print('loading agg data')
                    load_agg_data()
            elif data_type == "gdf":
                if gdf is None:
                    print('loading granular data')
                    load_gdf_data()
            else:
                raise ValueError(f"Unknown data type: {data_type}")

            return func(*args, **kwargs)

        return wrapper

    return decorator
