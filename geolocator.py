import requests
import subprocess
import re
import json
import math


def get_wifi_data():
    cmd = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s']

    output = str(subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0])
    wifiData = re.findall('((?:[0-9 a-f]{2}[:]){5}[0-9 a-f]{2})\s*(-?\d+)\s*(\d+)', output)

    wifiList = []
    for i in wifiData:
        wifiList.append({"macAddress": i[0],
                         "signalStrength": i[1],
                         "channel": i[2],
                         })

    return wifiList


def get_location(wifi_list = get_wifi_data()):
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDDGDhUvXFgz_x5BaUKRJYIGVEebkcEm_o'

    body = {'considerIp': 'true', 'wifiAccessPoints': wifi_list}

    response = json.loads(requests.post(url, json=body).text)
    return response['location']


# Uses haversine formula to calculate distance between two coordinates
def dist(c1, c2):
    r = 6371;
    phi1 = math.radians(c1['lat'])
    phi2 = math.radians(c2['lat'])
    delta_phi = phi1 - phi2
    delta_lambda = math.radians(c1['long']-c2['long'])
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*(math.sin(delta_lambda/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r*c
