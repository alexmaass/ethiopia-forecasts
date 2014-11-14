from app import db, models

inputfilename = "../scripts/AgMERRA_db_test.csv"
with open(inputfilename, 'r') as inputfile:
  lines = inputfile.readlines() 
  for line in lines[:3]:
    # Format DATE,EASE6_ID,SRAD,TMAX,TMIN,RAIN,WIND
    components = lines.split(',')
    date = datetime.datetime.strptime(components[0], "%Y-%m-%d").date()
    wareda = int(components[1])
    srad = float(components[2])
    tmax = float(components[3])
    tmin = float(components[4])
    rain = float(components[5])
    wind = float(components[6])
    r = models.Weather(date, wareda, srad, tmax, tmin, rain, wind)
    # db.session.add(r)
  # db.session.commit()  

# u = models.User(nickname='john', email='john@email.com')
# >>> db.session.add(u)
# >>> db.session.commit()