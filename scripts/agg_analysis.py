
import pandas as pd
from data_ingestion import agg_dataframes, df_granular
import matplotlib.pyplot as plt

# print(agg_dataframes)
# Group the data by date and state, then sum up the daily donations
donation_trends = agg_dataframes['donations_state'].groupby(['date', 'state'])['daily'].sum().reset_index()

# Sort the data by date to prepare for time series visualization
donation_trends = donation_trends.sort_values(by='date')

# Aggregate data at the country level by date to assess overall trends for Malaysia
donation_trends_malaysia = donation_trends.groupby('date')['daily'].sum().reset_index()
