import math

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
