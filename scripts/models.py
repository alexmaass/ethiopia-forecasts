from app import db
from sqlalchemy import Column, Integer, String

class Weather(db.Model):
  __tablename__ = 'weather_agmerra'
  # Fields: date(date),wareda(int),srad(real),tmax(real),tmin(real),rain(real),wind(real)
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  wareda = db.Column(db.Integer)
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
      # return "Weather: {self.date} {self.wareda} {self.srad} {self.tmax} {self.tmin} {self.rain} {self.wind}".format(self=self)
      # return "%s %d %f %f %f %f %f".format(str(self.date), self.wareda, self.srad, self.tmax, self.tmin, self.rain, self.wind)
