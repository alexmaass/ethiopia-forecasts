#!flask/bin/python
from flask import Flask, render_template, request, g, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import datetime, sys, time

application = Flask(__name__)
# Remote RDS db
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://awsuser:projectdemeter@ethiopia-forecast-postgres.cnkrenytxftx.us-east-1.rds.amazonaws.com/ethiopia_forecast_db'
# Local installation
# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/amaass'

db = SQLAlchemy(application)

class Weather(db.Model):
  __tablename__ = 'weather_agmerra'
  # Fields: date(date),wareda(int),srad(real),tmax(real),tmin(real),rain(real),wind(real)
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  date = db.Column(db.Date, nullable=False)
  wareda = db.Column(db.Integer, nullable=False)
  srad = db.Column(db.Float)
  tmax = db.Column(db.Float)
  tmin = db.Column(db.Float)
  rain = db.Column(db.Float)
  wind = db.Column(db.Float)

  def __init__(self, date, wareda, srad, tmax, tmin, rain, wind):
    self.date = date
    self.wareda = wareda
    self.srad = srad
    self.tmax = tmax
    self.tmin = tmin
    self.rain = rain
    self.wind = wind

  def __repr__(self):
    return str(self.__dict__)

@application.route('/')
@application.route('/index.html')
def main():
  return render_template('index.html')

@application.route('/lookup', methods=['POST'])
def lookup():
  # Parse arguments
  date = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date()
  datatype = request.form['datatype'] 
  print date, datatype
  # Database query 
  try:
    start = time.clock()
    results = Weather.query.with_entities(Weather.wareda, Weather.tmax).filter_by(date = date).all()
    print "Query time: " + str(time.clock() - start)
    json_dict = {}
    for result in results:
      json_dict[result[0]] = result[1]
    print "Number of waredas: " + str(len(json_dict))
    return json.dumps(json_dict)
  except:
    print "Unexpected error:", sys.exc_info()[0]
    return ""

if __name__ == '__main__':
  application.run(debug=True)

