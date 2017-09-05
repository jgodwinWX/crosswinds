import requests
import numpy
import pytaf

from avntools import runway_info,crosswind
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
header = decodedtaf._taf_header

# create some empty numpy arrays and lists to hold the information
winddir = [None] * len(groups)          # wind direction (degrees)
vtimes = [None] * len(groups)           # valid times (UTC)
windspd = numpy.zeros(len(groups))      # wind speed (knots)
windgst = numpy.zeros(len(groups))      # wind gusts (knots)

# get the valid time, wind speed, wind direction, and wind gusts for each group
for i,group in enumerate(groups):
    # handle the initial group
    if i == 0:
        vtimes[i] = header['valid_from_date'] + '/' + header['valid_from_hours'] + '00'
    else:
        # handle TEMPO groups
        if group['header']['type'] == 'TEMPO':
            vtimes[i] = group['header']['type'] + " " + group['header']['from_date'] + \
                group['header']['from_hours'] + "/" + group['header']['till_date'] + \
                group['header']['till_hours']
            if group['wind'] == None:
                continue
        else:
            vtimes[i] = group['header']['type'] + group['header']['from_date'] + '/' + \
                group['header']['from_hours'] + group['header']['from_minutes']
    winddir[i] = group['wind']['direction']
    windspd[i] = group['wind']['speed']
    windgst[i] = group['wind']['gust']

# change any None or vrb wind directions to zero
for i,item in enumerate(winddir):
    if item == None or item == 'VRB':
        winddir[i] = 0.0

# get runway information
runways,headings = runway_info(icao)

# compute crosswinds
xwinds = [None] * len(groups)
xwinds_gusts = [None] * len(groups)

for j in range(len(groups)):
    xwinds[j] = crosswind(windspd[j],float(winddir[j]),headings)
    xwinds_gusts[j] = crosswind(windgst[j],float(winddir[j]),headings)

# get colors for crosswinds

color = [None] * len(xwinds)
for i in range(len(color)):
    color[i] = [None] * len(runways)

for i in range(len(runways)):
    for j in range(len(vtimes)):
        if xwinds[j][i] < 20.0:
            color[j][i] = 'green'
        elif xwinds[j][i] >= 20.0 and xwinds[j][i] < 24.0:
            color[j][i] = 'yellow'
        elif xwinds[j][i] >= 24.0:
            color[j][i] = 'red'
        else:
            color[j][i] = 'gray'

# create html for webpage

html_file = open('xwind.html','w')

# page header
html_info = """
    <html>
    <head>
        <title>Crosswind TAF Tool</title>
    </head>
    <body>
        <h1>TAF Crosswinds for %s</h1>
        <h2>Forecast valid: %s UTC</h2>
        <p>%s</p>
    """ % (icao,vtimes[0],str(taf.encode('ascii','ignore')))

# create table
html_table = '''
    <table cols=%i border=1px width=1000px>
    <tr><th width=%ipx>Runway</th>
    ''' % (len(vtimes)+1,1000/(len(vtimes)+1))

# create columns (one for each valid time)
for i in range(len(vtimes)):
    html_table += '<th width=%ipx>%s</th>' % (1000/(len(vtimes)+1),vtimes[i])
html_table += '</tr>'

# create rows (one for each runway)
for i in range(len(runways)):
    html_table += '''
    <tr><td align='center'>%s</td>
    ''' % (runways[i])
    # put data into columns (one for each change group)
    for j in range(len(vtimes)):
        html_table += '''
        <td align='center' bgcolor='%s'>%.0f kt</td>
        ''' % (color[j][i],xwinds[j][i])
    html_table += '</tr>'

html_info += html_table + '</table>'

html_foot = '''
    <p><strong>Note: TEMPO will show winds as 0 kt if no wind given in TAF! Also, variable wind
    directions are set to 000 degrees.</strong></p>
    <p><strong>Disclaimer</strong>: The data provided this tool is for guidance purposes only,
    and should not be used for making decisions regarding the protection of life and property!
    The user agrees that the data provided by this tool is provided "as is", with no warranty
    whatsoever. Bugs in this code continue to be worked out.</p>
    </body></html>
    '''

html_info += html_foot
html_file.write(html_info)
html_file.close()
