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

def load_gdf_data():
    global gdf
    # Load granular data
    gdf = fetch_granular_data(mode="server")

def transform_dates():
    global dfs
    if dfs is None: return

    for key, df in dfs.items():
        if "date" in df.columns:
            dfs[key] = df.assign(date=pd.to_datetime(df['date'])).set_index('date')
        else:
            print(f"Dataframe {key} does not have a date column")

# Wrapper Function
def ensure_data_loaded(data_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if data_type == 'agg':
                global dfs
                if dfs is None:
                    load_agg_data()
            elif data_type == 'gdf':
                global gdf
                if gdf is None:
                    load_gdf_data()
            else:
                raise ValueError(f"Unknown data type: {data_type}")

            return func(*args, **kwargs)
        return wrapper
    return decorator

    

    

