import requests
import json
import geolocator
import math

FEET_PER_KILOMETRE = 0.0003048

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


def get_airport_city(icao):
    url = 'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/airports/locations/indicators-list?api_key=b4d2b410-d86a-11e7-a241-e5060cc78252&airports='
    url += icao
    response = json.loads(requests.get(url).text)
    return response[0]['cityName']


def alt_angle(plane):
    angle = math.atan2(plane.get('GAlt',0)*FEET_PER_KILOMETRE,
                       plane.get('Dst',0))
    return math.degrees(angle)


def bearing(plane, location):
    plane_location = {'lat': plane.get("Lat",0), 'lng': plane.get('Long', 0)}
    return geolocator.direction(location, plane_location)

