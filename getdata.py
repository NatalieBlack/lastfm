#!/usr/bin/env python

import requests
import json
import time
import os
from config import api_key, username

def download(method, dirname, charts):
    for chart in reversed(charts['weeklychartlist']['chart']):
        startdate = chart['from']
        enddate = chart['to']
        time.sleep(5)
        payload = {'method': method, 'api_key': api_key,
                   'user': username, 'format': 'json', 
                   'from': startdate, 'to': enddate
                  }
     
        r = requests.get(base_url, params=payload)
        fn = os.path.join(dirname, str(startdate) + "-" + str(enddate) + ".json")
        with open(fn, 'w+') as outfile:
         json.dump(r.json(), outfile)
         outfile.close()

base_url = 'http://ws.audioscrobbler.com/2.0/'

payload = {'method': 'user.getWeeklyChartList', 'api_key': api_key,
           'user': username, 'format': 'json'
          }

print "downloading charts list"
r = requests.get(base_url, params=payload)

print r.status_code
print r.url

charts = r.json()
chartsfile = open('chartslist.json', 'w+')
json.dump(charts, chartsfile)
chartsfile.close()

print 'downloading weekly album charts'
download('user.getWeeklyAlbumChart', 'charts', charts)

print 'downloading weekly track charts'
download('user.getWeeklyTrackChart', 'trackcharts', charts)
