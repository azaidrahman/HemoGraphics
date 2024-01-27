import sys
import os
import pandas as pd
from datetime import datetime
from helper_functions import fetch_granular_data,fetch_and_save_csv_files, csv_to_df
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose as sm
from statsmodels.tsa.stattools import adfuller, kpss


    
#Todays date
today_str = datetime.now().strftime('%Y-%m-%d')
data_folder = '..\\data'

# Load dataframes from CSVs
dfs = load_csvs_from_data_folder(data_folder, today_str)


def perform_eda(df, name):
    print(f"EDA for {name}:")
    
    # print("\nFirst few rows:")
    print(df.iloc[:,:5].head())
    
    print("\nInfo:")
    df.info()
    
    # Display basic statistics
    print("\nDescribe:")
    print(df.describe())
    
    # Check for null values
    print("\nNull values:")
    print(df.isnull().sum())
    
    # Check for duplicate rows
    print("\nNumber of duplicate rows:")
    print(df.duplicated().sum())

# Define the main outputs and the corresponding columns in dataframes
variable_outputs = {
    'blood_type': ['blood_a', 'blood_b', 'blood_o', 'blood_ab'],
    'location': ['location_centre', 'location_mobile'],
    'donation_type': ['type_wholeblood', 'type_apheresis_platelet', 'type_apheresis_plasma', 'type_other'],
    'social_class': ['social_civilian', 'social_student', 'social_policearmy'],
    'donation_regularity': ['donations_new', 'donations_regular', 'donations_irregular'],
}

donations_state = dfs['donations_state']
donations_state.loc[:,'date'] = pd.to_datetime(donations_state['date'])
donations_state.set_index('date',inplace=True)
malaysia_total = donations_state[donations_state['state'] == 'Malaysia']['daily'].sum()
state_total = donations_state[donations_state['state'] != 'Malaysia']['daily'].sum()

# Separate the data into two DataFrames: one for Malaysia and one for the states
ms_df = donations_state.loc[donations_state['state'] == 'Malaysia', :]
state_df = donations_state.loc[donations_state['state'] != 'Malaysia', :]

def plot_overall_state(df):
    plt.figure(figsize=(25, 15))
    for state in df.index.get_level_values(0).unique():
        df.xs(state, level='state').plot(label=state)
    plt.title('Monthly Blood Donations by State')
    plt.xlabel('Date')
    plt.ylabel('Total Donations')
    plt.legend(title='State')
    plt.show()


monthly_donations_by_state = state_df.groupby(['state', pd.Grouper(freq='M')])['daily'].sum()

# Pivot the table to have states as columns and dates as rows
monthly_donations_by_state = monthly_donations_by_state.unstack(level=0)


def decompose_and_plot(state, df, mean_donations = None, model='additive'):
    # Check if the state's data exists in the DataFrame
    if state not in df.columns:
        print(f"No data for state: {state}")
        return
    
    if mean_donations is not None:
        rank = mean_donations.rank(ascending=False)[state]
    
    # Perform seasonal decomposition
    series = df[state].dropna()  # Drop NA values for decomposition
    decomposition = sm(series, model=model, period=12)  # Monthly data usually has a period of 12
    
    # Plot the decomposed components
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(12, 8))
    decomposition.observed.plot(ax=axes[0], legend=False, title='Observed')
    decomposition.trend.plot(ax=axes[1], legend=False, title='Trend')
    decomposition.seasonal.plot(ax=axes[2], legend=False, title='Seasonal')
    decomposition.resid.plot(ax=axes[3], legend=False, title='Residual')
   
    if mean_donations is not None : 
        plt.suptitle(f'Seasonal Decompose of {state} Blood Donations (Rank {int(rank)})')
    else:
        plt.suptitle(f'Seasonal Decompose of {state} Blood Donations')
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the layout
    plt.show()

# Calculate mean donations per state to determine highest and lowest
mean_donations = monthly_donations_by_state.mean().sort_values()

# Take two states with the highest and two with the lowest mean donations
if mean_donations is not None:
    high_states = mean_donations.index[-2:]
    low_states = mean_donations.index[:2]

def df_cleans_before_decompose(df):
    #Forward-fill, replace NA and ensure no negative values in the dataset
    df.ffill()
    df.fillna(0,inplace=True)
    df[df < 0] = 0
    return df

monthly_donations_by_state_ffill = df_cleans_before_decompose(monthly_donations_by_state)
# Now, we can safely proceed with an additive model
for state in high_states.union(low_states):
    decompose_and_plot(state, monthly_donations_by_state_ffill, mean_donations,model= 'additive')

# Seasonal decompose of Malaysia
monthly_donations_malaysia = ms_df.groupby(['state', pd.Grouper(freq='M')])['daily'].sum().unstack(level=0)

decompose_and_plot('Malaysia',monthly_donations_malaysia,model='additive' )


