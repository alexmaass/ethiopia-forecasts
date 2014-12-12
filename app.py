#!flask/bin/python
from flask import Flask, render_template, request, g, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import datetime, sys, time

application = Flask(__name__)
# Remote RDS db
# application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://awsuser:projectdemeter@ethiopia-forecast-postgres.cnkrenytxftx.us-east-1.rds.amazonaws.com/ethiopia_forecast_db'
# Local installation
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/amaass'

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

# class Soil(db.Model):
#   __tablename__ = 'soil_csa'
#   # Fields: REG,ZONE,DIST,FA,EA,HH,HHSEX,HID,PARCEL,FLD,FWEIGHT,PART,FLDT,CROP,OWNTYPE,EXT,IRRG,SIRRG,SEEDTYPE,WTIMSEED,COSTIMPS,WTNISEED,DAMAGE,DREASON,DPERCENT,DMEASURE,DMTYPE,DMCHEM,FERT,FERTTYPE,D22A,D22B,D23,APERCENT,AMONTH,ADAY,CERROR,ANOTMEAS,ENUMAREA,COMPAREA,AREB,PLUNIT,PLOCAL,PRODUCT,YIELD98,COND98,CONDDA,CONDFA,AVGCOND,CONDF,PRODC,PRODDA,PROD98FA,PROD98P,PROD98V,id,HWEIGHT,V09,V10,V11,V12,V13,HRATIO,time,AREAH,AREA,PRODQ,PROD,PROD98CQ,PROD98CK,PRODDAQ,PRODDAKG,PRODFAQ,PRODFKG,PRODPQ,AreaH,new_area,new_product,TREES,TREESBA,REC_TYPE,FLDTYPE,SERRO,MERRO,D24,D25,D26,LANDUSE,AGE,SEX,EDUC,HTYPE,SOWING,ENSETTRE,D22C,D22D,D22E,G3_HECT,G4LACODE,G4_LOCA,D27A,CONDH,AVPROD,WGTF,RATEF,YLDENST_AM,YLDENST_KO,YLDENST_BU,PRODAM,PROD_AMQ,PROD_AMKG,PRODKO,PROD_KOQ,PROD_KOKG,PROD_BU,PROD_BUQ,PROD_BUKG,PRODD,merge_id,M_ID
#   id = db.Column(db.Integer, primary_key=True, nullable=False)
#   date = db.Column(db.Date, nullable=False)
#   wareda = db.Column(db.Integer, nullable=False)
#   srad = db.Column(db.Float)
#   tmax = db.Column(db.Float)
#   tmin = db.Column(db.Float)
#   rain = db.Column(db.Float)
#   wind = db.Column(db.Float)

#   def __init__(self, date, wareda, srad, tmax, tmin, rain, wind):
#     self.date = date
#     self.wareda = wareda
#     self.srad = srad
#     self.tmax = tmax
#     self.tmin = tmin
#     self.rain = rain
#     self.wind = wind

#   def __repr__(self):
#     return str(self.__dict__)

@application.route('/')
@application.route('/index.html')
def main():
  return render_template('index.html')

@application.route('/lookup', methods=['POST'])
def lookup():
  # Parse arguments
  date = datetime.datetime.strptime(request.form['date'], "%m/%d/%Y").date()
  variable = request.form['variable'] 
  print date, variable
  # Database query 
  try:
    start = time.clock()
    # Switch statement for fields
    results = []
    if (variable == "srad"):
      results = Weather.query.with_entities(Weather.wareda, Weather.srad).filter_by(date = date).all()
    elif (variable == "tmax"):
      results = Weather.query.with_entities(Weather.wareda, Weather.tmax).filter_by(date = date).all()
    elif (variable == "tmin"):
      results = Weather.query.with_entities(Weather.wareda, Weather.tmin).filter_by(date = date).all()
    elif (variable == "rain"):
      results = Weather.query.with_entities(Weather.wareda, Weather.rain).filter_by(date = date).all()
    elif (variable == "wind"):
      results = Weather.query.with_entities(Weather.wareda, Weather.wind).filter_by(date = date).all()
    else:
      print "Variable requested not recognized"
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

