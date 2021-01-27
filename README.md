***
# SQLAlchemy and Flask Challenge - Surf Up!
***

## Objectives

1. Use Python SQLAlchemy ORM queries for the provided hawaii.sqlite to reflect tables into a new model to analyze Honolulu, Hawaii! Climate.
  - Create engine, inspector, reflect existing database model in a new one, automap classes.
  
      |Requirements|Name of activity|
      |:---|:---|:---|
      |# 1|Precipitation Analysis|
      |# 2|Station Analysis|
      
2. Design Flask API based on the queries developed.
  - Use Flask to create your routes, list all routes, use Flask "jsonify" for the return.

Reference file [climate_starter](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/climate_starter.ipynb)

*********

### Objective 1 - Climate Analysis and Exploration
------------
-- Requirements:
### Precipitation Analysis

- Design a query to retrieve the last 12 months of precipitation data.
- Filter only the date and prcp values.
- Load the query results into a Pandas DataFrame and set the index to the date column.
- Sort the DataFrame values by date.
- Plot the results.
- Used Pandas to print the summary statistics for the precipitation data.

![alt text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/One_year_precipitation.png)

### Station Analysis
- Design a query to calculate the total number of stations.
- Design a query to find the most active stations.
- List the stations and observation counts in descending order.
- Found out which station has the highest number of observations.
- Design a query to retrieve the last 12 months of temperature observation data (tobs).
- Filter by the station with the highest number of observations "USC00519281".
- Plot the results as histogram with bins=12.

![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/Temperature_station_USC00519281.png)

 ***
### Objective 2 - Climate App

- Design a Flask API based on the queries that were developed in step 1.
- Use Flask to create and list all your routes.
- Use Flask jsonify to convert your API data into a valid JSON response object.

  - All Routes
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_routes.PNG)

  - Precipitation
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_precipitation.PNG)

  - Stations
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_stations.PNG)

  - TOBS
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_tobs.PNG)

  - Start Date
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_start_date.PNG)

  - Start End Date
![alt_text](https://github.com/Krla20/sqlalchemy-challenge/blob/main/Instructions/Images/api_start_end_date.PNG)

------
***

