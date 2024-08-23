# Honolulu Climate Analysis and API

## Overview

This project involves analyzing the climate data of Honolulu, Hawaii, to help plan a holiday vacation. The analysis is divided into two main parts:

1. **Climate Data Analysis**: Using Python, SQLAlchemy, Pandas, and Matplotlib to perform data exploration and visualization.
2. **Flask API Development**: Creating a Flask API based on the analysis to serve climate data dynamically.

## Project Structure

- **climate_starter.ipynb**: Jupyter notebook used for data exploration and analysis.
- **hawaii.sqlite**: SQLite database containing climate data for Honolulu, Hawaii.
- **app.py**: Flask application to create API routes for accessing the climate data.
- **README.md**: Overview of the project, instructions for running the analysis, and API usage.

## Part 1: Climate Data Analysis

### Steps

1. **Setup Database Connection**:
   - Use SQLAlchemy to connect to the `hawaii.sqlite` database.
   - Reflect the tables into SQLAlchemy classes using `automap_base()`.
   - Create a session to link Python to the database.

2. **Precipitation Analysis**:
   - Identify the most recent date in the dataset.
   - Retrieve the last 12 months of precipitation data and load it into a Pandas DataFrame.
   - Plot the data to visualize precipitation trends over the year.
   - Display summary statistics for the precipitation data.

3. **Station Analysis**:
   - Calculate the total number of weather stations in the dataset.
   - Identify the most active station with the highest number of observations.
   - Query and display the minimum, maximum, and average temperatures recorded at the most active station.
   - Retrieve and plot temperature observations (TOBS) for the last 12 months from the most active station.

### Requirements

- Python 3.x
- SQLAlchemy
- Pandas
- Matplotlib
- Jupyter Notebook

### Running the Analysis

1. Open the `climate_starter.ipynb` file in Jupyter Notebook.
2. Follow the instructions in each cell to perform the analysis.
3. Ensure the database connection is closed at the end of the notebook.

## Part 2: Flask API Development

### API Endpoints

1. **Home** `/`
   - Lists all available API routes.

2. **Precipitation Data** `/api/v1.0/precipitation`
   - Returns a JSON dictionary with the date as the key and precipitation as the value for the last 12 months.

3. **Stations** `/api/v1.0/stations`
   - Returns a JSON list of all weather stations in the dataset.

4. **Temperature Observations** `/api/v1.0/tobs`
   - Returns a JSON list of temperature observations (TOBS) for the last 12 months from the most active station.

5. **Temperature Statistics** `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
   - Returns a JSON list of the minimum, average, and maximum temperatures for a given start date or start-end date range.

### Running the Flask API

1. Ensure you have Flask installed:
   ```bash
   pip install Flask
