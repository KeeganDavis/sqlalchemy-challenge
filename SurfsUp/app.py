# Import the dependencies.
import numpy as np
import datetime as dt

# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/K/Documents/24_Bootcamp/24.03_Challenges and Projects/Challenge 10 - SQLAlchemy/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    '''List all available api routes.''' 
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )
   
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    '''Retrieve the last 12 months precipitation data''' 
    session = Session(engine)
    # Get most recent date and format to int to be able to calculate timedelta
    most_recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
    most_recent_date_formatted = most_recent_date.split('-')
    most_recent_year = int(most_recent_date_formatted[0])
    most_recent_month = int(most_recent_date_formatted[1])
    most_recent_day = int(most_recent_date_formatted[2])    

    # Calculate the date one year from the last date in data set and convert to string
    year_ago = dt.datetime(most_recent_year, most_recent_month, most_recent_day) - dt.timedelta(days=365)
    year_ago_str = year_ago.strftime('%Y-%m-%d')
    year_ago_str


    # Perform a query to retrieve the data and precipitation scores
    precipitation_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago_str, Measurement.date <= most_recent_date).\
        all()
        
    session.close()
    
    precipitation_dict = [{result.date: result.prcp} for result in precipitation_results]
    
    return jsonify(precipitation_dict)
    
@app.route("/api/v1.0/stations")
def stations():
    '''Return JSON list of all stations''' 
    session = Session(engine)
    
    station_names = session.query(Station.station, Station.name).all()
    
    session.close()
    
    station_dict = [{result.station: result.name} for result in station_names]
    
    return jsonify(station_dict)
    
@app.route("/api/v1.0/tobs")
def tobs():
    '''Return JSON list of temperature observations for last 12 months''' 
    # Get most recent date and format to int to be able to calculate timedelta
    session = Session(engine)
    most_recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
    most_recent_date_formatted = most_recent_date.split('-')
    most_recent_year = int(most_recent_date_formatted[0])
    most_recent_month = int(most_recent_date_formatted[1])
    most_recent_day = int(most_recent_date_formatted[2])    

    # Calculate the date one year from the last date in data set and convert to string
    year_ago = dt.datetime(most_recent_year, most_recent_month, most_recent_day) - dt.timedelta(days=365)
    year_ago_str = year_ago.strftime('%Y-%m-%d')
    year_ago_str
    
    
    most_active_station = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= year_ago_str, Measurement.date <= most_recent_date).\
    all()
    
    session.close()
    
    temps_list = [result.tobs for result in most_active_station]
    
    return jsonify(temps_list)
    
@app.route("/api/v1.0/<start>")
def input_start(start):
    '''Return a JSON list of the min temp, avg temp, and max temp for the date''' 
    date = start
    session = Session(engine)
    
    date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    
    session.close()
    
    date_list = [{'Minimum Temperature': date_query[0][0], 'Average Temperature': date_query[0][1], 'Maximum Temperature': date_query[0][2]}]
    
    return jsonify(date_list)

@app.route("/api/v1.0/<start>/<end>")
def input_start_end(start, end):
    '''Return JSON list of the min temp, avg temp, and max temp for the range''' 
    
    session = Session(engine)
    
    date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    
    session.close()
    
    date_list = [{'Minimum Temperature': date_query[0][0], 'Average Temperature': date_query[0][1], 'Maximum Temperature': date_query[0][2]}]
    
    return jsonify(date_list)
    
if __name__ == '__main__':
    app.run(debug=True)