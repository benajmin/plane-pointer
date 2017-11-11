import requests
import json


# Returns list of planes withing radius km of location
def get_planes(location, radius):
    url = 'http://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?'
    url += "lat={}".format(location['lat'])
    url += '&'
    url += "lng={}".format(location['lng'])
    url += '&'
    url += 'fDstL=0&fDstU={}'.format(radius)

    response = json.loads(requests.get(url).text)

    return response['acList']


# Produces plane closest to location
def get_closest_plane(location):
    radius = 10
    while not get_planes(location, radius):
        radius += 10
    planes = get_planes(location, radius)

    closest_plane = planes[0]
    for i in planes:
        if i['Dst'] < closest_plane['Dst']:
            closest_plane = i

    return closest_plane
