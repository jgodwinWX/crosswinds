#!/usr/bin/env python
''' Cross-wind calculator (v1.0)

This tool will compute cross-wind components for various runway configurations. User inputs wind
speed (in units), direction (degrees on the meteorological compass), and airport (ICAO code). The
runway information is read in from a CSV file containing the runway names (i.e. "18/36L"). The
CSV file was provided courtesy OurAirports (http://ourairports.com/data/).

Disclaimer: This code is provided "as is" with no warranty of any kind. The information provided
by this tool should be considered unofficial and informal, and should not be used for any decisions
that involve the protection of life or property.

Version history:
    1.0: Initial build.
    2.0: Now uses true north runway headings.
    2.1: Added disclaimer and updated block header.

'''
# import modules
import math
import numpy as np
import pandas

__author__ = "Jason W. Godwin"
__copyright__ = "Public Domain"
__license__ = "GPL"
__version__ = "2.1"
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
headings = np.array(df_airport['Heading'])      # runway headings (true north)

# get runway names
runways = []
for i,j in zip(df_airport['LowerID'],df_airport['UpperID']):
    if len(i) == 1:
        i = "0" + i
    runways.append(i + "/" + j)

# compute crosswind component on each runway and print the output
print "Airport: %s" % airport
print "Runway\tCross-wind component"
for j in range(len(headings)):
    xwind = windspd * abs(math.sin(math.radians(headings[j]-winddir)))
    print "%s\t%.2f" % (runways[j],xwind)
