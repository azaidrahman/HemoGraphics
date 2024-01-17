# Blood Donation Data Analysis Project

## Project Overview
This project involves building an automated data pipeline to ingest daily-updated blood donation data from two sources: aggregate (csv files from a GitHub repository) and granular (a Parquet file). The goal is to perform analysis on the trends of blood donations in Malaysia and to understand the retention rate of blood donors.

## Structure
The project is organized into several directories:

- `data/`: Contains subdirectories for raw and processed data. (Note: Raw data is not stored in the repository).
- `notebooks/`: Jupyter notebooks for exploratory data analysis and results presentation.
- `scripts/`: Python scripts for automating the data ingestion and analysis.
- `output/`: Stores generated figures, plots, and reports.

## Data Ingestion
The script `scripts/data_ingestion.py` is responsible for:
- Fetching the latest CSV files from the GitHub repository.
- Reading the content of the Parquet file from a given URL.
- Loading the content into Pandas DataFrames for further processing.

The script does not save the CSV files to disk but reads them directly into memory for analysis.

## Automation
The process is designed to be automated with scheduled runs, ensuring that the data analysis is updated daily with the latest data available.

## Requirements
All Python dependencies are listed in `requirements.txt`. To install these dependencies, run:
pip install -r requirements.txt


## Running the Scripts
To run the data ingestion script, navigate to the `scripts/` directory and execute:

## Contributions
Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes.

## License
This project is open-sourced under the MIT License.

## Contact
For any additional questions or comments, please contact the repository owner.

---
