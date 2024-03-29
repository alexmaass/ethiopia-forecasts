import os
import fnmatch
import datetime
import csv
import time

import psycopg2

start_time = time.time()
data_directory = "../data/Weather_Data/AgMERRA_SSA/"
weights_filename = data_directory + "AgMERRA_WeightMatrix.csv"
output_filename = "AgMERRA_db.csv"

valuemap = {}
weightmap = {}
waredas = set()
dates = set()
outputmap = {}

def parseWTH(filename, index):
  with open(filename, 'r') as input_file:
    lines = input_file.readlines()
    for line in lines[4:]:
      components = line.split()
      if int(components[0][0]) < 8:
        date = datetime.datetime.strptime('20'+components[0], '%Y%j').date()
      else:
        date = datetime.datetime.strptime('19'+components[0], '%Y%j').date()
      dates.add(date)
      values = components[1:]
      # Converting all values to float
      for i in range(0,len(values)):
        values[i] = float(values[i])
      valuemap[(date, index)] = values

# Parse through the weights file. 
weights_file = open(weights_filename, 'r')
weights_lines = weights_file.readlines()
weights_lines = weights_lines[0].split('\r')
for line in weights_lines[1:]:
  components = line.split(',')
  waredaID = int(components[0])
  waredas.add(waredaID)
  weights = components[1:]
  # Convert all weights to floats
  for i in range(0,len(weights)):
    weights[i] = float(weights[i])
  weightmap[waredaID] = weights

# Iterate over all files in the current directory
index = 0
for f in sorted(os.listdir(data_directory)):
  f = data_directory + f
  # If f is a file and has the .WTH extension, parse it
  if os.path.isfile(f) and fnmatch.fnmatch(f, '*.WTH'):
    parseWTH(f, index)
    index+=1

# Begin calculations
print "Number of dates: " + str(len(dates))
print "Number of waredas: " + str(len(waredas)) 
print "Ideal number of rows: " + str(len(dates) * len(waredas))
for date in sorted(dates):
  for waredaID in sorted(waredas):
    weights = weightmap[waredaID]
    # Used to store final averaged values. Declaring an array of zeros
    averagedValues = [0.0] * len(valuemap[(date,0)])
    for weightIndex in range(0, len(weights)):
      if weights[weightIndex] > 0.0:
        values = valuemap[(date,weightIndex)]
        for i in range(0, len(values)):
          # averagedValues[i] = averagedValues[i] + weights[weightIndex]*values[i]
          # Rounds the values to six decimal places to fit in real DB type
          averagedValues[i] = round(averagedValues[i] + weights[weightIndex]*values[i], 6)
    outputmap[(date, waredaID)] = averagedValues
print "Actual number of rows: " + str(len(outputmap))

# Upload outputmap to PostgresDB
# conn = psycopg2.connect("host=localhost port=5432 user=amaass dbname=amaass");
# cur = conn.cursor()
# # Create the table
# crt_query = "CREATE TABLE IF NOT EXISTS weather_agmerra(\
#      id     INT,\        
#      date   DATE,\
#      wareda INT,\
#      srad   REAL,\
#      tmax   REAL,\
#      tmin   REAL,\
#      rain   REAL,\
#      wind   REAL\
#   );"
# cur.execute(crt_query);
# # Inserts
# ins_query = "INSERT INTO weather_agmerra (date, wareda, srad, tmax, tmin, rain, wind)\
#          VALUES (%s, %s, %s, %s, %s, %s, %s);"
# counter = 0
# for k,v in outputmap.iteritems():
#   k+=1;
#   out = [k[0],k[1]] + v
#   data = tuple(out)
#   cur.execute(ins_query, data)
#   if k % 1000 == 0:
#     print k
# conn.commit()
# cur.close()
# conn.close()

# Write outputmap to disk
with open(output_filename, 'wb') as outputfile:
  # wr = csv.writer(outputfile, quoting=csv.QUOTE_ALL)
  wr = csv.writer(outputfile)
  id = 1;
  for k,v in outputmap.iteritems():
    out = [id,k[0],k[1]] + v
    # Out has format ID,DATE,EASE6_ID,SRAD,TMAX,TMIN,RAIN,WIND
    wr.writerow(out)
    id+=1

# Track time
print str(time.time() - start_time)




