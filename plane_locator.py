import requests
import json
import geolocator
import math
import serial
import time

FEET_PER_KILOMETRE = 0.0003048


def main():
    ser = serial.Serial('/dev/cu.usbserial-A9MLDZZZ', 9600)
    my_location = geolocator.get_location()

    while True:
        plane = get_closest_plane(my_location)
        pitch = alt_angle(plane)
        yaw = bearing(plane, my_location)
        plane_info = parse_plane(plane)

        send_serial(plane_info, pitch, yaw, ser)

        time.sleep(10)
    return


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
    if icao == '':
        return icao

    url = 'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/airports/locations/indicators-list?'
    url += 'api_key=b4d2b410-d86a-11e7-a241-e5060cc78252&airports='
    url += icao
    response = json.loads(requests.get(url).text)
    return response[0]['cityName']


def alt_angle(plane):
    angle = math.atan2(plane.get('GAlt', 0)*FEET_PER_KILOMETRE,
                       plane.get('Dst', 0))
    return math.degrees(angle)


def bearing(plane, location):
    plane_location = {'lat': plane.get("Lat", 0), 'lng': plane.get('Long', 0)}
    return geolocator.direction(location, plane_location)


def parse_plane(plane):
    result = dict()
    if plane.get('Mil', False):
        result['Op'] = 'Military'
    else:
        result['Op'] = plane.get('Op', '')[:16]

    result['Dst'] = plane.get('Dst', 0)
    result['GAlt'] = plane.get('GAlt', 0)

    # remove year at beginning of model
    if plane.get('Mdl', '')[0].isdigit():
        result['Mdl'] = plane.get('Mdl', '')[5:21]
    else:
        result['Mdl'] = plane.get('Mdl', '')[:16]

    p_to = get_airport_city(plane.get('To', '')[:4])
    p_from = get_airport_city(plane.get('From', '')[:4])

    # ensure both cities will fit on lcd
    if len(p_to)+len(p_from) <= 15:
        result['To'] = p_to
        result['From'] = p_from
    elif len(p_to) < 7:
        result['To'] = p_to
        result['From'] = p_from[:(15-len(p_to))]
    elif len(p_from) < 7:
        result['To'] = p_to[:(15-len(p_from))]
        result['From'] = p_from
    else:
        result['To'] = p_to[:7]
        result['From'] = p_from[:8]

    return result


def send_serial(plane_info, pitch, yaw, ser):
    output = ''
    for key in plane_info:
        output += '<' + key  + '>' + str(plane_info[key])
    output += '<Yaw>' + str(yaw)
    output += '<Pitch>' + str(pitch)
    ser.write(output.encode('ascii', 'ignore'))
    print(output)
    return


if __name__ == "__main__":
    main()


