# sqlalchemy-challenge
## Description
The notekook in this repository analyzes the hawaii sqlite database to find precipitation amounts from each station from the database from the last recorded date to the date 365 days before the last recorded date and create a bar graph for the amount of rain over the year. The station with the most temperature observations is then analyzed and the last 365 days of temperature observation data from the database is used to create a histogram. The app.py file creates a simple api webpage using flask. The different endpoints allow the user to see the precipitation info, temperature observation info, weather station info, and they can even input their own start and/or end date to retrieve the minimum, maximum, and average temperature observations from the database.
## Requirements 
The requirements for this repository are matplotlib, numpy, pandas, datetime, sqlalchemy, and flask.
## Installation
Clone the repository: git@github.com:KeeganDavis/sqlalchemy-challenge.git
## Usage
To run the climate_starter notebook, select a kernel and then run all to analyze the temperature and precipitation data. Run the app.py file and then navigate the api through the browser.
## Known Issues
- x axis on the bar chart is unreadable because the dates stack on top of each other. I worked with Michael (TA) to try and fix the issue, but we were unable to fix it even after refactoring my code to match the solution.
