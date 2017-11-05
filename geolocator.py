import requests
import subprocess
import re
import json

def getWifiData():
    cmd = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s']

    output = str(subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0])
    wifiData = re.findall('((?:[0-9 a-f]{2}[:]){5}[0-9 a-f]{2})\s*(-?\d+)\s*(\d+)', output)

    wifiList = []
    for i in wifiData:
        wifiList.append({"macAddress": i[0],
                         "signalStrength": i[1],
                         "channel": i[2]})

    return wifiList


def getLocation(wifiList):
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDDGDhUvXFgz_x5BaUKRJYIGVEebkcEm_o"

    body = {"considerIp": "true", "wifiAccessPoints": wifiList}

    response = json.loads(requests.post(url, json=body).text)
    return response['location']
