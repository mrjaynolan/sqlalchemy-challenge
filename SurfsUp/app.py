# Import the dependencies.
import numpy as np
import pandas as pd
from datetime import datetime as dt

# SQLAlchemy Dependencies
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker

# Flask Dependencies
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
    """List all available api routes."""
    return (
        f"Welcome to the Honolulu, Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year."""
    # Find the most recent date in the data set.
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.strptime(most_recent_date, "%Y-%m-%d") - pd.DateOffset(years=1)
    
    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.station).all()

    # Unravel results into a 1D array and convert to a list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations (tobs) for the last year."""
    # Find the most recent date in the data set.
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.strptime(most_recent_date, "%Y-%m-%d") - pd.DateOffset(years=1)

    # Query the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the dates and temperature observations of the most active station for the last year
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    tobs_dict = {date: tobs for date, tobs in tobs_data}

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, and TMAX for a specified start or start-end range."""
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        # Calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        # Calculate TMIN, TAVG, TMAX for dates between start and end
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Unravel results into a 1D array and convert to a list
    temps_list = list(np.ravel(results))
    
    return jsonify(temps_list)

if __name__ == "__main__":
    app.run(debug=True)

# Close the session at the end of the script
session.close()

