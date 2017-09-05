import requests
import numpy
import pytaf
from bs4 import BeautifulSoup

# prompt user for ICAO code
icao = raw_input('Airport code (ICAO): ')

# request page and parse it
page = requests.get('http://aviationweather.gov/taf/data?ids=%s&format=raw&submit=Get+TAF+data' % icao)
soup = BeautifulSoup(page.content,'html.parser')
taf = "TAF " + soup.find_all('code')[0].get_text()

# decode the TAF
site = taf[0:4]
inittime = taf.split('Z')[0][-6:]

# create TAF object using pytaf
decodedtaf = pytaf.TAF(str(taf.encode('ascii','ignore')))
groups = decodedtaf._weather_groups

# create some empty numpy arrays and lists to hold the information
winddir = [None] * len(groups)          # wind direction (degrees)
windspd = numpy.zeros(len(groups))      # wind speed (knots)
windgst = numpy.zeros(len(groups))      # wind gusts (knots)

# get the valid time, wind speed, wind direction, and wind gusts for each group
for i,group in enumerate(groups):
    winddir[i] = group['wind']['direction']
    windspd[i] = group['wind']['speed']
    windgst[i] = group['wind']['gust']
