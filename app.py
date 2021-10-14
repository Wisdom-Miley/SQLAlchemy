# Ignore SQLITE warnings related to Decimal numbers in the Chinook database
import warnings
warnings.filterwarnings('ignore')

# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify# Import Dependencies


#################################################
# Database Setup
#################################################
# Create an engine for the chinook.sqlite database
engine = create_engine("sqlite:///hawaii.sqlite",echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

#################################################
# Flask Routes
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
       
    )

@app.route("/api/v1.0/<start>")
def starter(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurment.tobs), func.avg(Measurment.tobs), func.max(Measurment.tobs)).\
        filter(Measurment.date >= start).all()
    session.close()
    
    tobsall = []
    for min, avg, max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Avg"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
    return jsonify(tobsall)


@app.route("/api/v1.0/<start>/<stop>")
def starter(start,stop):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurment.tobs), func.avg(Measurment.tobs), func.max(Measurment.tobs)).\
        filter(Measurment.date >= start).Filter(Measurement.date <= stop).all()
    session.close()
    
    tobsall = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Avg"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)
        
    return jsonify(tobsall)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    lastst = session.query(Measurment.date).order_by(Measurment.date.dosc()).first()[0]
    lastdate = dt.datetime.strptime(lastst, '%y-%m-%d')
    querydate = dt.date(lastdate.year -1, lastdate.month, lastdate.day)
    sel = [Measurment.date, Measurment.tobs]
    results = session.query(*sel).filter(Measurment.date >= querydate).all()
    session.close()

    tobsall = []
    for  min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)
         
    return jsonify(tobsall)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    sel = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    results = session.query(*sel).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    sel = [Measurement.date,Measurement.prcp]
    results = session.query(*sel).all()
    session.close()

    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

if __name__ == '__main__':
    app.run(debug=True)