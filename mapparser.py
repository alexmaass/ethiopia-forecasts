#!/usr/bin/python
from bs4 import BeautifulSoup
import json
import sys

testline = "<html xmlns:fo=\"http://www.w3.org/1999/XSL/Format\" xmlns:msxsl=\"urn:schemas-microsoft-com:xslt\">\r\r\n<head>\r\r\n<META http-equiv=\"Content-Type\" content=\"text/html\">\r\r\n<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">\r\r\n</head>\r\r\n<body style=\"margin:0px 0px 0px 0px;overflow:auto;background:#FFFFFF;\">\r\r\n<table style=\"font-family:Arial,Verdana,Times;font-size:12px;text-align:left;width:100%;border-collapse:collapse;padding:3px 3px 3px 3px\">\r\r\n<tr style=\"text-align:center;font-weight:bold;background:#9CBCE2\">\r\r\n<td>WEREDA 09</td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>\r\r\n<table style=\"font-family:Arial,Verdana,Times;font-size:12px;text-align:left;width:100%;border-spacing:0px; padding:3px 3px 3px 3px\">\r\r\n<tr>\r\r\n<td>FID</td>\r\r\n<td>307</td>\r\r\n</tr>\r\r\n<tr bgcolor=\"#D4E4F3\">\r\r\n<td>W6ID</td>\r\r\n<td>140409</td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>W_NAME</td>\r\r\n<td>WEREDA 09</td>\r\r\n</tr>\r\r\n<tr bgcolor=\"#D4E4F3\">\r\r\n<td>EASE_W6ID</td>\r\r\n<td></td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>EASE_Wored</td>\r\r\n<td></td>\r\r\n</tr>\r\r\n<tr bgcolor=\"#D4E4F3\">\r\r\n<td>EASE_Z4ID</td>\r\r\n<td>1404</td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>EASE_ZoneN</td>\r\r\n<td></td>\r\r\n</tr>\r\r\n<tr bgcolor=\"#D4E4F3\">\r\r\n<td>REGION_R2I</td>\r\r\n<td>14</td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>Area_km2</td>\r\r\n<td>2.442925</td>\r\r\n</tr>\r\r\n<tr bgcolor=\"#D4E4F3\">\r\r\n<td>LAT</td>\r\r\n<td>9.046226</td>\r\r\n</tr>\r\r\n<tr>\r\r\n<td>LONG</td>\r\r\n<td>38.746237</td>\r\r\n</tr>\r\r\n</table>\r\r\n</td>\r\r\n</tr>\r\r\n</table>\r\r\n</body>\r\r\n</html>\r\r\n"

def parse(line):
  # Removing the microsoft bullshit
  line = line[106:]
  line = line[:len(line)-4].strip()
  soup = BeautifulSoup(line)
  text = soup.get_text()
  components = text.split('\n')
  # Convert from Unicode to ASCI
  components = [x.encode('ascii') for x in components]
  # Remove empty components
  components = filter(None, components)
  # Remove the title component
  components = components[1:]
  # Convert object to dictionary object
  json_obj = {}
  k = 0
  while (k < len(components)-1):
    key = components[k]
    val = components[k+1]
    if (key == 'EASE_Z4ID') | (key == 'W6ID') | (key == 'REGION_R2I') | (key == "FID") | (key == "EASE_W6ID"):
      try:
        json_obj[key] = int(val)
        k+=2
      except ValueError:
        json_obj[key] = -1
        k+=1
    elif (key == 'LONG') | (key == 'LAT') | (key == 'Area_km2'):
      try:
        json_obj[key] = float(val)
        k+=2
      except ValueError:
        json_obj[key] = -1.0
        k+=1
    elif (key == 'EASE_ZoneN'):
      if val == 'REGION_R2I':
        json_obj[key] = ""
        k+=1
      else:
        json_obj[key] = val
        k+=2  
    elif (key == 'EASE_Wored'):
      if val == 'EASE_Z4ID':
        json_obj[key] = ""
        k+=1
      else:
        json_obj[key] = val
        k+=2  
    else:
      json_obj[key] = val
      k+=2
  return json_obj

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
input_file = open(input_file_name , 'r')
input_obj = json.load(input_file)
input_file.close()
# Going in and converting the description field
features = input_obj['features']
for feature in features:
  description = feature['properties']['description']
  del feature['properties']['description']
  for key,val in parse(description).iteritems():
    feature['properties'][key] = val
output = open(output_file_name, 'w')
json.dump(input_obj, output)
output.close()




