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
df = pandas.read_csv('airports/runways.csv')    # import the CSV as a dataframe
df_airport = df[df['ID']==airport]              # reduce the dataframe to the relevant airport

# get runway names
runways = []
for i,j in zip(df_airport['LowerID'],df_airport['UpperID']):
    if len(i) == 1:
        i = "0" + i
    runways.append(i + "/" + j)

# determine runway directions
rnwy = np.zeros(len(runways))
for i in range(len(runways)):
    rnwy[i] = float(runways[i][0:2]) * 10.0

# compute crosswind component on each runway and print the output
print "Airport: %s" % airport
print "Runway\tCross-wind component"
for j in range(len(rnwy)):
    xwind = windspd * abs(math.sin(math.radians(rnwy[j]-winddir)))
    print "%s\t%.0f" % (runways[j],xwind)
