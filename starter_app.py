# Import everything you used in the starter_climate_analysis.ipynb file, along with Flask modules

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/hawaii.sqlite")

# reflect an existing database into a new model using automap_base()
Base = automap_base()

# reflect the tables with Base.prepare(), passing in the engine and reflect=True
Base.prepare(engine, reflect=True)


# We can view all of the classes that automap found with Base.classes
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our Session() and bind it to the engine
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Instantiate a Flask object at __name__, and save it to a variable called app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Set the app.route() decorator for the base '/'
# define a welcome() function that returns a multiline string message to anyone who visits the route
@app.route("/")
def welcome():
    return (
        f"Welcome to the ultimate surfer's resource<br/>"
        f"You will be able to find the best surfing spots using this page! <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/temp/ENTER-DATE-HERE <br/>"
        f"/api/v1.0/temp/ENTER-START-DATE/ENTER-END-DATE <br/>"
    )

# Set the app.route() decorator for the "/api/v1.0/precipitation" route
@app.route("/api/v1.0/precipitation")
# define a precipitation() function that returns jsonified precipitation data from the database
def precipitation():
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database
    # Finding last date in the dataset
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date

    # converting result date into datetime object
    last_date_object = dt.datetime(2017,8,23)

    # Use the datetime.timedelta() function to help calculating the difference of one year, 12 months, or 365 days
    first_date_object = last_date_object - dt.timedelta(days=365)
    

    # Use session.query() to retrieve the date and prcp columns, .filter() by the date you calculated above, and selecting .all() results
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > first_date_object).all()
    
    session.close()

    # Create a dictionary to store the date: prcp pairs. 
    # Hint: check out a dictionary comprehension, which is similar to a list comprehension but allows you to create dictionaries
    
    # Return the jsonify() representation of the dictionary
    all_prcp = []

    for date, prcp in results:
        results_dict = {}
        results_dict["date"] = date
        results_dict["prcp"] = prcp
        all_prcp.append(results_dict)
    return jsonify(all_prcp)

    
# Set the app.route() decorator for the "/api/v1.0/stations" route
@app.route("/api/v1.0/stations")
# define a stations() function that returns jsonified station data from the database
def stations():
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Query for the list of stations
    results_2 = session.query(measurement.station).all()
    session.close()
    # Unravel results into a 1D array and convert to a list
    all_results_2 = []
    for station in results_2:
        results_dict_2 = {}
        results_dict_2["station_id"] = station
        all_results_2.append(results_dict_2)
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    return jsonify(all_results_2)
    # Return the jsonify() representation of the list


# Set the app.route() decorator for the "/api/v1.0/tobs" route
@app.route("/api/v1.0/tobs")
# define a temp_monthly() function that returns jsonified temperature observations (tobs) data from the database
def temp_monthly():
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    last_date_object = dt.datetime(2017,8,23)

    # Use the datetime.timedelta() function to help calculating the difference of one year, 12 months, or 365 days
    first_date_object = last_date_object - dt.timedelta(days=365)
    

    # Use session.query() to retrieve the date and prcp columns, .filter() by the date you calculated above, and selecting .all() results
    results_tobs = session.query(measurement.date, measurement.tobs).filter(measurement.date > first_date_object).all()
    
    session.close()
    # Return the jsonify() representation of the list
    all_tobs = []

    for date, tobs in results_tobs:
        results_tobs_dict = {}
        results_tobs_dict["date"] = date
        results_tobs_dict["tobs"] = tobs
        all_tobs.append(results_tobs_dict)
    return jsonify(all_tobs)

# Set the app.route() decorator for the "/api/v1.0/temp/<start>" route and "/api/v1.0/temp/<start>/<end>" route
@app.route("/api/v1.0/temp/<start>")
# define a stats() function that takes a start and end argument, and returns jsonified TMIN, TAVG, TMAX data from the database
def stats(start):
    results_temps = session.query(measurement.date, measurement.tobs).filter(measurement.date>start).all()
    session.close()

    all_temps = []
    date = []
    for date, tobs in results_temps:
        all_temps.append(tobs)
    
    TMIN = min(all_temps)
    TMAX = max(all_temps)
    TAVG = sum(all_temps)/len(all_temps)
    summary_dict = {"TMIN":TMIN, "TMAX": TMAX, "DATE":start, "TAVG": TAVG}

    return jsonify(summary_dict)

@app.route("/api/v1.0/temp/<start>/<end>")
def stats_2(start=None, end=None):
    if end == None:
        results_temps = session.query(measurement.date, measurement.tobs).filter(measurement.date>start).all()
        session.close()

        all_temps = []
        date = []
        for date, tobs in results_temps:
            all_temps.append(tobs)
        
        TMIN = min(all_temps)
        TMAX = max(all_temps)
        TAVG = sum(all_temps)/len(all_temps)
        summary_dict = {"TMIN":TMIN, "TMAX": TMAX, "DATE":start, "TAVG": TAVG}

        return jsonify(summary_dict)
    else:
        results_temps = session.query(measurement.date, measurement.tobs).filter(measurement.date>start).filter(measurement.date<end).all()
        session.close()

        all_temps = []
        date = []
        for date, tobs in results_temps:
            all_temps.append(tobs)
        
        TMIN = min(all_temps)
        TMAX = max(all_temps)
        TAVG = sum(all_temps)/len(all_temps)
        summary_dict = {"TMIN":TMIN, "TMAX": TMAX, "START DATE":start, "TAVG": TAVG, "END DATE":end}

        return jsonify(summary_dict)


if __name__ == '__main__':
    app.run(debug=True)
