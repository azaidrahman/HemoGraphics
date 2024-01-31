import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
from statsmodels.tsa.seasonal import seasonal_decompose as sm

import data_loading

@data_loading.ensure_data_loaded('agg')
def plot_trends(df_name: str, graph_type: str, states='All', entities=None, compare=False):
    """
    Plot different types of trends based on the graph_type and other parameters.
    
    :param df: DataFrame containing the data.
    :param graph_type: Type of graph ('monthly_donations', 'seasonal', 'rates').
    :param entities: List of states or facilities to include in the graph. If None, use all.
    :param compare: Boolean, if True and applicable, add comparison in the graph.
    """
    try:
        if data_loading.dfs is not None:
            df = data_loading.dfs[df_name]
        else:
            return TypeError 
    except TypeError:
        print("dfs not loaded")
        return  
    
    print(df.iloc[:3,:3])
    
    
    #Filter the DataFrame based on the selected entities (states/facilities)
    if entities is not None:
        df = df[df['entity_column'].isin(entities)]  

    # Plot based on the graph_type
    if graph_type == 'monthly_donations':
        return plot_monthly_donations(df,states)
    elif graph_type == 'seasonal':
        return plot_seasonal_donations(df, states)
    # elif graph_type == 'rates':
    #     plot_donation_rates(df)
    else:
        print(f"Graph type {graph_type} is not supported.")

def plot_monthly_donations(df, states):
    if states == 'All': 
        states = ['Johor','Kedah', 'Kelantan','Melaka','Negeri Sembilan','Pahang','Perak',
            'Pulau Pinang','Sabah','Sarawak','Selangor','Terengganu','W.P. Kuala Lumpur']
        
    # Separate the data into two DataFrames: one for Malaysia and one for the states
    df = df.loc[df['state'].isin(states)]
    # Group the data by state and resample to a monthly frequency, summing the daily donations
    monthly_donations_by_state = df.groupby('state').resample('M').sum().loc[:, 'daily']
    # Plotting the trends
    plt.figure(figsize=(25, 15))
    for state in monthly_donations_by_state.index.get_level_values(0).unique():
        monthly_donations_by_state.xs(state, level='state').plot(label=state)
    plt.title('Monthly Blood Donations by State')
    plt.xlabel('Date')
    plt.ylabel('Total Donations')
    plt.legend(title='State')

    # #Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    plt.close()
    # print('test')
    # print(f"Buffer size: {len(buf.getvalue())}")
    
    return buf

def plot_seasonal_donations(df, states):

    if states == 'All': 
        states = ['Johor','Kedah', 'Kelantan','Melaka','Negeri Sembilan','Pahang','Perak',
            'Pulau Pinang','Sabah','Sarawak','Selangor','Terengganu','W.P. Kuala Lumpur']
        
    # Separate the data into two DataFrames: one for Malaysia and one for the states
    df = df.loc[df['state'].isin(states)]
    # Group the data by state and resample to a monthly frequency, summing the daily donations
    monthly_donations_by_state = df.groupby('state').resample('M').sum().loc[:, 'daily']
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
        buf = BytesIO()
        plt.savefig(buf,format='png')
        buf.seek(0)
        plt.close()
        # print('test')
        print(f"Buffer size: {len(buf.getvalue())}")
        return buf

    def df_cleans_before_decompose(df):
        #Forward-fill, replace NA and ensure no negative values in the dataset
        df.ffill()
        df.fillna(0,inplace=True)
        df[df < 0] = 0
        return df
    
    # Calculate mean donations per state to determine highest and lowest
    mean_donations = monthly_donations_by_state.mean().sort_values()

    if mean_donations.empty:
        return 0

    ranked_states = mean_donations.rank(method='min', ascending=False)
    # Take two states with the highest and two with the lowest mean donations
    high_states = ranked_states[ranked_states <= 2]
    low_states = ranked_states[ranked_states >= (ranked_states.max() - 1)]
    
    top_bottom_states = pd.concat([high_states,low_states])
    ranked_states_dict = {int(rank): state for state, rank in top_bottom_states.items()}

    monthly_donations_by_state_ffill = df_cleans_before_decompose(monthly_donations_by_state)

    buffers = {} 
    # Now, can safely proceed with an additive model
    for rank in sorted(ranked_states_dict.keys()):
        # print(state)
        state = ranked_states_dict[rank]
        buf = decompose_and_plot(state, monthly_donations_by_state_ffill, mean_donations,model= 'additive')
        if buf:
            buffers[state] = buf
        else:
            print(f"Failed to generate plot for {state}")
    
    return buffers

@data_loading.ensure_data_loaded('gdf')
def plot_retention():
    donor_data = data_loading.gdf
    
    if donor_data is None:
        return 0

    donor_data['visit_date'] = pd.to_datetime(donor_data['visit_date'])
    donor_data.sort_values(['donor_id','visit_date'], inplace=True)
    donor_data['Cohort'] = donor_data.groupby('donor_id')['visit_date'].transform('min').dt.strftime('%Y-%m')
    donor_data['Order'] = donor_data.groupby('donor_id').cumcount() + 1

    bin_edges = [1, 2, 3, 4, 5, 6, 8, 10, 13, donor_data['Order'].max() + 1]
    bin_labels = ['1', '2', '3', '4', '5', '6-7','8-9', '10-12','13+']

    bin_result = pd.cut(donor_data['Order'], bins=bin_edges, labels=bin_labels, right=False)
    donor_data['Order_Bin_Range'] = bin_result

    # for label in bin_labels:
    # print(f"Bin {label}: {donor_data['Order_Bin_Range'].value_counts()[label]} orders")

    # Extract the year from 'Cohort' and create a new column 'Cohort_Year'
    donor_data['Cohort_Year'] = pd.to_datetime(donor_data['Cohort']).dt.year

    # Adjust the cohort pivot table based on the new 'Order_Bin_Range' and 'Cohort_Year'
    cohort_data_binned = donor_data.groupby(['Cohort_Year', 'Order_Bin_Range']).agg(n_donors=('donor_id', 'nunique')).reset_index()
    cohort_pivot_binned = cohort_data_binned.pivot_table(index='Cohort_Year', columns='Order_Bin_Range', values='n_donors')
    # Filling NaN values with 0 for better visualization
    cohort_pivot_binned.fillna(0, inplace=True)

    # Display the new pivot table
    cohort_size = cohort_pivot_binned.iloc[:,0]
    retention_matrix = cohort_pivot_binned.divide(cohort_size,axis=0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(retention_matrix, 
                annot=True, 
                fmt='.3%', 
                cmap='YlGnBu', 
                vmin=0.0, 
                vmax=0.5,
                linewidths=.5)
    plt.title('Yearly Cohorts: Donor Retention Rate')
    plt.ylabel('Cohort Year')
    plt.xlabel('Order Bin Range')
    plt.yticks(rotation=360)

    buf = BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    plt.close()

    return buf