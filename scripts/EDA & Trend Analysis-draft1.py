import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose as sm
from statsmodels.tsa.stattools import adfuller, kpss

from helper_functions import fetch_data

data_folder = '..\\data'
# Aggregate Data
dfs = None

gdf = None

# Data Loading and Caching
def load_agg_data():
    global dfs
    today_str = datetime.now().strftime('%Y-%m-%d')
    # Load aggregate data
    dfs = fetch_data(mode='server')

    


# Wrapper Function
def ensure_agg_data_loaded(func):
    def wrapper(*args, **kwargs):
        global dfs
        # Load data if not loaded. 
        # Then transform the index into the dates.
        if dfs is None:
            load_agg_data()
            
        if dfs is not None:
            for key, df in dfs.items():
                if 'date' in df.columns:
                    dfs[key]['date'] = pd.to_datetime(df['date'])
                    dfs[key].set_index('date',inplace=True)
                else:
                    print(f'Dataframe {key} does not have a date column')

        return func(*args, **kwargs)
    return wrapper

        



@ensure_data_loaded
def test():
    if dfs:
        print(f'dfs loaded!')


test()