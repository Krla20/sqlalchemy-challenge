from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )

# Need to iterate the variables to be able to show them on ea. api
# To render a template you can use the render_template() method. - No need to call it out
# All you have to do is provide the name of the template and the variables you want to pass to the template engine as keyword arguments. 
# https://flask.palletsprojects.com/en/1.1.x/quickstart/


def calc_temps(start_date, end_date):

    # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    """TMIN, TAVG, and TMAX for a list of dates.
    
    # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)

    return (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start_date)
        .filter(Measurement.date <= end_date)
        .all()
    )


# Calculate the date 1 year ago from the last data point in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
last_year_date = last_date - dt.timedelta(days=365)

# Query the dates and temperature observations of the most active station for the last year of data.
active_results = (
    session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date.between ("2016-08-23", "2017-08-23")).all()
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary in JSON format where the date is the key and the value is 
    the precipitation data"""

    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    prcp_results = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > last_year_date)
        .order_by(Measurement.date)
        .all()
    )

    # Save the query results as a dictionary with the date as the key and the prcp record as the value
    date_precipitaton = []
    for date, prcp in prcp_results:
        dpdata_dict = {}
        dpdata_dict[date] = prcp
        date_precipitaton.append(dpdata_dict)

    session.close()

    # Return the valid JSON response object
    return jsonify(date_precipitaton)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""

    session = Session(engine)

    stations_results = session.query(Station.station, Station.name).all()

    session.close()
    
    # Return the valid JSON response object
    return jsonify(stations_results)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    """Query the dates and temperature observations of the most active station for the last year of data."""

    active_results = (
    session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date.between ("2016-08-23", "2017-08-23")).all()
)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""

    session.close()

    # Return the valid JSON response object
    return jsonify(active_results)
    # return jsonify(temp_results)

@app.route("/api/v1.0/<start>") # need <> because the start will be replace
# e.i. to call the start date: /api/v1.0/2017-05-02 (add the date after the /)
def start(start):
    """Return a JSON list of the minimum temperature,"""
    """the average temperature, and the max temperature"""
    """for a given start or start-end (YYYY-MM-DD)."""

    temps = calc_temps(start, last_date)

    # Create the list that stores the results
    temperature_list = []
    date_dict = {"Start Date": start, "End Date": last_date}
    temperature_list.append(date_dict)
    temperature_list.append(
        {"Observations": "Minimum Temperature", "Temperature (°F)": temps[0][0]}
    )
    temperature_list.append(
        {"Observations": "Average Temperature", "Temperature (°F)": temps[0][1]}
        )
    temperature_list.append(
        {"Observations": "Maximum Temperature", "Temperature (°F)": temps[0][2]}
        )

    session.close()

    return jsonify(temperature_list)

@app.route("/api/v1.0/start_end") #I don't need <> bc i'm defining below
# e.i. to call the start_end date: /api/v1.0/2017-05-02_2017-08-23 (add the date before and after "_")
def start_end(start_end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    start = request.args.get("Start Date")
    end = request.args.get("End Date")

    temps = calc_temps(start, end)

    # Create the list that stores the results
    temperature_list = []
    date_dict = {"Start Date": start, "End Date": end}
    temperature_list.append(date_dict) 
    temperature_list.append(
        {"Observations": "Minimum Temperature", "Temperature (°F)": temps[0][0]}
    )
    temperature_list.append(
        {"Observations": "Average Temperature", "Temperature (°F)": temps[0][1]}
    )
    temperature_list.append(
        {"Observations": "Maximum Temperature", "Temperature (°F)": temps[0][2]}
    )

    session.close()

    # Return the valid JSON response object
    return jsonify(temperature_list)

#################################################
# Run the application
#################################################

if __name__ == "__main__" :
    app.run(debug=True)