import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import shutil

BASE_RAW_URL = "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/"
API_URL = "https://api.github.com/repos/MoH-Malaysia/data-darah-public/contents/"
DATA_DIRECTORY = "../data/"
GRANULAR_DATA_URL = "https://dub.sh/ds-data-granular"
today_str = datetime.now().strftime("%Y-%m-%d")
today_directory = os.path.join(DATA_DIRECTORY, today_str)


def fetch_data(mode="server"):
    response = requests.get(API_URL)
    dfs = {}

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return

    if response.status_code == 200:
        # Parse the JSON response
        repo_contents = response.json()

        # Iterate over the files in the repo
        for file_info in repo_contents:
            # Check if the file is a CSV
            if file_info["type"] == "file" and file_info["name"].endswith(".csv"):
                # Construct the raw URL for the CSV file
                csv_url = BASE_RAW_URL + file_info["name"]

                # Read the CSV file directly into a DataFrame
                df = pd.read_csv(csv_url)

                match mode:
                    case "server":
                        # Save the df into a dictionary if wish to load directly into memory
                        dfs[file_info["name"]] = df
                    case "local":
                        # Save the DataFrame to a CSV file in today's data directory
                        filename = f"{file_info['name'].split('.csv')[0]}.csv"
                        file_path = os.path.join(today_directory, filename)
                        # Check if the file already exists
                        if not os.path.isfile(file_path):
                            df.to_csv(file_path, index=False)
                            print(f"Data saved to {file_path}")
                        else:
                            print(f"File already exists: {file_path}")

    if mode == "server" and dfs:
        return dfs
    elif mode == "local":
        return
    else:
        return print(f"Failed to fetch data")


def cleanup_old_data_folders():
    today = datetime.now()
    # Get a list of all subdirectories in the data directory
    subdirectories = [
        d
        for d in os.listdir(DATA_DIRECTORY)
        if os.path.isdir(os.path.join(DATA_DIRECTORY, d))
    ]

    # Convert folder names to dates and sort them
    folder_dates = sorted(
        [datetime.strptime(folder_name, "%Y-%m-%d") for folder_name in subdirectories]
    )

    # Check if the oldest folder is at least 7 days old
    if folder_dates and (today - folder_dates[0]).days > 7:
        # Define the cutoff time; folders older than this will be removed
        cutoff_time = today - timedelta(days=7)

        # Iterate through the folders and remove those older than the cutoff time
        for folder_date in folder_dates:
            if folder_date < cutoff_time:
                folder_name = folder_date.strftime("%Y-%m-%d")
                folder_path = os.path.join(DATA_DIRECTORY, folder_name)
                shutil.rmtree(folder_path)
                print(f"Removed old data folder: {folder_name}")
            else:
                # Since the list is sorted, we can break the loop once we find a folder newer than the cutoff
                break


def fetch_and_save_csv_files():
    cleanup_old_data_folders()

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_data_directory = os.path.join(DATA_DIRECTORY, today_str)

    # Check if today's data directory already exists
    if (
        os.path.exists(today_data_directory)
        and len(os.listdir(today_data_directory)) >= 4
    ):
        print(f"Data for today ({today_str}) already exists. Skipping data fetching.")
        return

    os.makedirs(today_data_directory, exist_ok=True)

    # Save csv files locally
    fetch_data(mode="local")


def fetch_granular_data(mode="server"):
    match mode:
        case "server":
            try:
                df = pd.read_parquet(GRANULAR_DATA_URL)

                if df.empty:
                    print("Parquet data is empty")
                    return
            except Exception as e:
                print("Error occurred:", e)
                return

            return df

        case "local":
            cleanup_old_data_folders()

            # Check if the directory exists, if not, create it
            if not os.path.exists(today_directory):
                os.makedirs(today_directory)

            # Define the file path for the new file
            file_path = os.path.join(
                today_directory, f"granular_data_{today_str}.parquet"
            )

            if os.path.exists(file_path):
                print("reading downloaded")
                df = pd.read_parquet(file_path)
            else:
                print("downloading online")
                df = pd.read_parquet(GRANULAR_DATA_URL)
                df.to_parquet(file_path)

            return df


# Load aggregate data from CSVs
def load_csvs_from_data_folder(data_folder, date_str):
    def csv_to_df(date_folder_path):
        dataframes = {}
        for filename in os.listdir(date_folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(date_folder_path, filename)
                dataframe_name = filename.replace(".csv", "")
                dataframes[dataframe_name] = pd.read_csv(file_path)
                dataframes[dataframe_name]["date"] = pd.to_datetime(
                    dataframes[dataframe_name]["date"]
                )

        # print(dataframes)
        return dataframes

    # Create the path to the data folder for the given date
    date_folder_path = os.path.join(data_folder, date_str)
    # print(date_folder_path)

    # Check if the folder exists
    if not os.path.exists(date_folder_path):
        fetch_and_save_csv_files()
    elif len(os.listdir(date_folder_path)) < 4:
        fetch_and_save_csv_files()

    # Dictionary to hold dataframes
    dataframes = {}
    dataframes = csv_to_df(date_folder_path)
    return dataframes
