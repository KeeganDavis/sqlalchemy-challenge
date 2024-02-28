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


def get_year_ago():
    '''finds the most recent date from the dataset and returns the most recent date the date a year before the most recent date'''
    with Session(engine) as session:
        # Get most recent date and format to int to be able to calculate timedelta
        most_recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
        most_recent_date_formatted = most_recent_date.split('-')
        most_recent_year = int(most_recent_date_formatted[0])
        most_recent_month = int(most_recent_date_formatted[1])
        most_recent_day = int(most_recent_date_formatted[2])    

        # Calculate the date one year from the last date in data set and convert to string
        year_ago = dt.datetime(most_recent_year, most_recent_month, most_recent_day) - dt.timedelta(days=365)
        year_ago_str = year_ago.strftime('%Y-%m-%d')

        return most_recent_date, year_ago_str

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
        f"<h1>Climate App</h1><br/>"
        f"<h2>Available Routes:</h2><br/>"
        f"<ul>"
        f"<li>Get precipitation data for the last 12 months of the database - /api/v1.0/precipitation</li><br/>"
        f"<li>Get the name and id of every weather station in the database - /api/v1.0/stations</li><br/>"
        f"<li>Get the temperature observations for the last 12 months of the database data from the most active weather station - /api/v1.0/tobs</li><br/>"
        f"<li>Get the minimum, maximum and average temperature from the date that is passed to the end of the database - /api/v1.0/YYYY-MM-DD</li><br/>"
        f"<li>Get the minimum, maximum and average temperature from the first date passed to the second date passed - /api/v1.0/YYYY-MM-DD/YYYY-MM-DD</li>"
        f"</ul>"
    )
   
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    '''Retrieve the last 12 months precipitation data''' 
    
    # capture the variables returned from the function
    most_recent_date, year_ago_str = get_year_ago()
    
    with Session(engine) as session:
        # Perform a query to retrieve the data and precipitation scores
        precipitation_results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_ago_str, Measurement.date <= most_recent_date).\
            all()
    
    # add the data to a dict in a list where the key is the date and the value is the precipitation
    precipitation_dict = [{result.date: result.prcp} for result in precipitation_results]
    
    return jsonify(precipitation_dict)
    
    
@app.route("/api/v1.0/stations")
def stations():
    '''Return JSON list of all stations''' 
    
    with Session(engine) as session:
        # query the name and id of the stations
        station_names = session.query(Station.station, Station.name).all()
        
    # add the data to a dict in a list where the station id is the key and the station name is the value
    station_dict = [{result.station: result.name} for result in station_names]
    
    return jsonify(station_dict)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    '''Return JSON list of temperature observations for last 12 months''' 
    
    # capture the variables returned from the function
    most_recent_date, year_ago_str = get_year_ago()
    
    with Session(engine) as session:
        # query the tobs from the most active station for the last 12 months of data
        most_active_station = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago_str, Measurement.date <= most_recent_date).\
        all()
    
    # add all temps to a list to be used as JSON for the webpage
    temps_list = [result.tobs for result in most_active_station]
    
    return jsonify(temps_list)
    
    
@app.route("/api/v1.0/<start>")
def input_start(start):
    '''Return a JSON list of the min temp, avg temp, and max temp from the date to the end of the database''' 
    
    with Session(engine) as session:
        # query the database to calculate the min, avg, and max temp
        date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= (start)).all()
            
    # access list and then tuple index to get desired values
    date_list = [{'Minimum Temperature': date_query[0][0], 'Average Temperature': date_query[0][1], 'Maximum Temperature': date_query[0][2]}]
    
    return jsonify(date_list)


@app.route("/api/v1.0/<start>/<end>")
def input_start_end(start, end):
    '''Return JSON list of the min temp, avg temp, and max temp for the range of dates''' 
    with Session(engine) as session:
        # calculate min, avg, and max temp for the date range
        date_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start, Measurement.date <= end).all()
            
    # access list and then tuple index to get desired values
    date_list = [{'Minimum Temperature': date_query[0][0], 'Average Temperature': date_query[0][1], 'Maximum Temperature': date_query[0][2]}]
    
    return jsonify(date_list)
    
    
if __name__ == '__main__':
    app.run(debug=True)