#!/usr/bin/env python

# import modules
import math
import numpy
import pandas
import pytaf
import requests

from bs4 import BeautifulSoup

def crosswind(windspd,winddir,headings):
    xwinds = numpy.zeros(len(headings))
    for i in range(len(headings)):
        xwinds[i] = windspd * abs(math.sin(math.radians(headings[i]-winddir)))
    return xwinds

def runway_info(airport):
    # use runway csv to get runway information
    df = pandas.read_csv('airports/runways.csv')    # import the CSV as a dataframe
    df_airport = df[df['ID']==airport]              # reduce the dataframe to the relevant airport
    headings = numpy.array(df_airport['Heading'])   # runway headings (true north)

    # get runway names
    runways = []
    for i,j in zip(df_airport['LowerID'],df_airport['UpperID']):
        if len(i) == 1:
	    i = "0" + i
        runways.append(i + "/" + j)
    return runways,headings
