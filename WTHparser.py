import os
import fnmatch
import datetime
import csv
import time

start_time = time.time()
weights_filename = "AgMERRA_WeightMatrix.csv"
output_filename = "AgMERRA_averaged_rounded2.csv"

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
for f in sorted(os.listdir('.')):
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
          averagedValues[i] = round(averagedValues[i] + weights[weightIndex]*values[i], 2)
    outputmap[(date, waredaID)] = averagedValues

# Write outputmap to disk
print "Actual number of rows: " + str(len(outputmap))
with open(output_filename, 'wb') as outputfile:
  wr = csv.writer(outputfile, quoting=csv.QUOTE_ALL)
  for k,v in outputmap.iteritems():
    out = [k[0],k[1]] + v
    # out = k + v
    wr.writerow(out)
print str(time.time() - start_time)




