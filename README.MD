# Blood Donation Data Analysis Project

## Project Overview

This project serves as my submission for an assessment by the OpenDOSM GovTech Nucleus Unit. This project involves building an automated data pipeline to ingest daily-updated blood donation data from two sources: aggregate (csv files from a GitHub repository) and granular (a Parquet file) and churn it out to a telegram bot. The goal is to perform analysis on the trends of blood donations in Malaysia and to understand the retention rate of blood donors.

## Development Process

The development of HemoGraphics involved the following approach:

Exploratory Data Analysis (EDA) & Trend Analysis: Initially, I delved into the data using the EDA, Trend Analysis, and Retention Analysis notebooks. This step was crucial for understanding the nuances of the blood donation data and setting a solid groundwork for further analysis.

Scripting for Automation: Post-analysis, I encapsulated the data processing and analytical methodologies into Python scripts. These scripts are the backbone of the project, enabling automated data ingestion and analysis, ensuring the system remains up-to-date with the most recent data.

Telegram Bot Integration: The final piece of the puzzle was the creation of a Telegram bot. This bot is designed to leverage the scripts, providing an interactive interface for accessing real-time analysis and insights.

## Structure

The project is organized into several directories:

- `data/`: Contains subdirectories for raw and processed data. (Note: Raw data is not stored in the repository).
- `notebooks/`: Jupyter notebooks for exploratory data analysis and results presentation.
- `scripts/`: Python scripts for automating the data ingestion and analysis.
- `telegram_bot/`: Houses the initialization and scripts for the Telegram bot, enhancing the project's accessibility and interactivity.

## Automation

The process is designed to be automated with scheduled runs, ensuring that the data analysis is updated daily with the latest data available.

## Requirements

All Python dependencies are listed in `requirements.txt`. To install these dependencies, run:
pip install -r requirements.txt

## Contact

For any additional questions or comments, please contact the repository owner.

---
