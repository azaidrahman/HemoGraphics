import matplotlib.pyplot as plt
import seaborn as sns

from data_loading import ensure_data_loaded,dfs,gdf


@ensure_data_loaded
def plot_trends(df, graph_type, states='All', entities=None, compare=False):
    """
    Plot different types of trends based on the graph_type and other parameters.
    
    :param df: DataFrame containing the data.
    :param graph_type: Type of graph ('monthly_donations', 'seasonal', 'rates').
    :param entities: List of states or facilities to include in the graph. If None, use all.
    :param compare: Boolean, if True and applicable, add comparison in the graph.
    """
    # Filter the DataFrame based on the selected entities (states/facilities)
    if entities is not None:
        df = df[df['entity_column'].isin(entities)]  # replace 'entity_column' with actual column name

    # Plot based on the graph_type
    if graph_type == 'monthly_donations':
        plot_monthly_donations(df,states)
    elif graph_type == 'seasonal':
        plot_seasonal_graph(df, compare)
    elif graph_type == 'rates':
        plot_donation_rates(df)
    else:
        print(f"Graph type {graph_type} is not supported.")

def plot_monthly_donations(df, states):
    if states == 'All': 
        states = ['Johor',
            'Kedah',
            'Kelantan',
            'Melaka',
            'Negeri Sembilan',
            'Pahang',
            'Perak',
            'Pulau Pinang',
            'Sabah',
            'Sarawak',
            'Selangor',
            'Terengganu',
            'W.P. Kuala Lumpur']
        
    donations_state = dfs['donation_state']
    # Separate the data into two DataFrames: one for Malaysia and one for the states
    df = donations_state.loc[donations_state['state'].isin(states)]
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
    plt.show()

def plot_seasonal_donations(df):

def plot_donations_rates(df):
    