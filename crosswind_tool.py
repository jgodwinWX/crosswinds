#!/usr/bin/env python
''' Cross-wind calculator (v1.0)

This tool will compute cross-wind components for various runway configurations. User inputs wind
speed (in units), direction (degrees on the meteorological compass), and airport (ICAO code). The
runway information is read in from a CSV file containing the runway names (i.e. "18/36L").

Version history:
    1.0: Initial build.

'''
# import modules
import math
import numpy as np
import pandas

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Jason W. Godwin"
__email__ = "jasonwgodwin@gmail.com"
__status__ = "Production"

# user input information
winddir = float(raw_input("Wind direction (degrees): "))
windspd = float(raw_input("Wind speed: "))
airport = raw_input("Airport (ICAO code): ")

# import runway information
df = pandas.read_csv('airports/airports.csv')
airports = np.array(df['Airport'])
rownum = np.where(airports==airport)[0][0]
runways = np.array(df.iloc[rownum,1:])

# get airport latitude/longitude
df2 = pandas.read_csv('airports/airportlatlons.csv')
latitude = float(df2[df2['ICAO'].str.contains(airport)]['Latitude'])
longitude = float(df2[df2['ICAO'].str.contains(airport)]['Longitude'])

# get magnetic declination

# determine runway directions
rnwy = np.zeros(len(runways))
for i in range(len(runways)):
    if type(runways[i]) is float:
        continue
    else:
        rnwy[i] = float(runways[i][0:2]) * 10.0
rnwy = filter(lambda x: x != 0.0, rnwy)

# compute crosswind component on each runway and print the output
print "Airport: %s" % airport
print "Runway\tCross-wind component"
for j in range(len(rnwy)):
    xwind = windspd * abs(math.sin(math.radians(rnwy[j]-winddir)))
    print "%s\t%.0f" % (runways[j],xwind)
