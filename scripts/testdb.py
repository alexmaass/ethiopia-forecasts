import datetime
import psycopg2

# Format DATE,EASE6_ID,SRAD,TMAX,TMIN,RAIN,WIND
# line = [datetime.date(1998, 2, 21), 41008, 21.962108, 26.179384, 11.745811, 0.39856, 210.096345]
# print tuple(line)
#COPY weather_agmerra FROM '/Users/amaass/Documents/Workspace/ethiopia-forecasts/scripts/AgMERRA_db.csv' DELIMITER ',' CSV;
# CREATE TABLE IF NOT EXISTS weather_agmerra(id     INT     PRIMARY KEY NOT NULL,date   date    NOT NULL,wareda INT     NOT NULL,srad   REAL,tmax   REAL,tmin   REAL,rain   REAL,wind   REAL);
# pg_dump -t weather_agmerra amaass | psql --host=ethiopia-forecast-postgres.cnkrenytxftx.us-east-1.rds.amazonaws.com --port=5432 --username=awsuser --password --dbname=ethiopia_forecast_db

# Upload outputmap to PostgresDB
conn = psycopg2.connect("host=localhost port=5432 user=amaass dbname=amaass");
cur = conn.cursor()
# PRIMARY KEY(date,wareda)\
cur.execute("CREATE TABLE IF NOT EXISTS weather_agmerra(\
     id     INT     PRIMARY KEY NOT NULL,\
     date   date    NOT NULL,\
     wareda INT     NOT NULL,\
     srad   REAL,\
     tmax   REAL,\
     tmin   REAL,\
     rain   REAL,\
     wind   REAL\
  );");
ins_query = "INSERT INTO weather_agmerra (date, wareda, srad, tmax, tmin, rain, wind)\
         VALUES (%s, %s, %s, %s, %s, %s, %s);"
data = tuple(line)
print data
cur.execute(ins_query, data)
conn.commit()

sel_query = "SELECT * FROM weather_agmerra WHERE wareda = 41008 AND date BETWEEN '1999-01-01' AND '1999-02-01'"
cur.execute(sel_query)
print len(cur.fetchall())

cur.close()
conn.close()