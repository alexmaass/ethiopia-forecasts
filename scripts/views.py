from flask import render_template, request, g
from models import Weather
from app import application
import datetime

@application.route('/')
@application.route('/index.html')
def main():
  return render_template('index.html')

@application.route('/lookup', methods=['POST'])
def lookup():
  # Parse arguments
  date = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d").date()
  datatype = request.form['datatype'] 
  print date
  print datatype
  # Database query
  ret = Weather.query.filter(Weather.wareda == 41008, Weather.date == date).all()
  print len(ret)
  print ret
  try:
    ret = Weather.query.filter(Weather.wareda == 41008, Weather.date <= date).first()
    print ret
    return "Success!"
  except:
    print "Fail.."
    return "Fail.."
  cur = getDB().cursor()
  try:
    results = weatherTable.query.filter_by(weatherTable.c.date == date).execute()
    print results
    # sel_query = cur.mogrify("SELECT wareda, %s FROM weather_agmerra WHERE date = %s", (datatype, date))
    # cur.execute(sel_query)
    # print len(cur.fetchall())
    # return "Success!"
  except:
    pass
    return "Fail..."
