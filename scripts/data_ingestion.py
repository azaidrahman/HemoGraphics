import requests
import pandas as pd
from io import BytesIO

# Base URL for raw GitHub content
base_raw_url = 'https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/'

# GitHub API URL for the contents of the data directory
api_url = 'https://api.github.com/repos/MoH-Malaysia/data-darah-public/contents/'

agg_dataframes = {}

# Send a request to the GitHub API to list the files in the repository
response = requests.get(api_url)
if response.status_code == 200:
    # Parse the JSON response
    repo_contents = response.json()
    
    # Iterate over the files in the repo
    for file_info in repo_contents:
        # Check if the file is a CSV
        if file_info['type'] == 'file' and file_info['name'].endswith('.csv'):
            # Construct the raw URL for the CSV file
            csv_url = base_raw_url + file_info['name']
            
            # Read the CSV file directly into a DataFrame
            df = pd.read_csv(csv_url)
            
            # Add the DataFrame to dictionary, using the file name as the key
            agg_dataframes[file_info['name'].split(".csv")[0]] = df
            
else:
    print("Failed to fetch repository contents")

########################################
# The URL that redirects to the Parquet file
url_granular = 'https://dub.sh/ds-data-granular'

# Send a request to the URL
response = requests.get(url_granular, stream=True)

# Check if the request was successful
if response.status_code == 200:
    # Read the content of the response in bytes
    file_content = response.content
    # Use BytesIO as a buffer for the binary data
    df_granular = pd.read_parquet(BytesIO(file_content), engine='pyarrow')
    
else:
    print("Failed to download the granular data file.")

