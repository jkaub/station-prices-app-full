import numpy as np

R = 6371


def build_adress(x):

    adress = x['adress'].lower() + " " + str(x['cp'])+" " + x['city'].lower()
    adress = " ".join([e.capitalize() if len(
        e) >= 3 else e for e in adress.split(" ")]).replace(" l ", " l'")

    adress = "-".join([e[0].upper()+e[1:] if len(
        e) >= 3 else e for e in adress.split("-")])

    return pretify_address(adress)


def pretify_address(adress):
    adress = " ".join([e.capitalize() if len(
        e) >= 3 else e for e in adress.lower().split(" ")]).replace(" l ", " l'")

    adress = "-".join([e[0].upper()+e[1:] if len(
        e) >= 3 else e for e in adress.split("-")])

    return adress


def haversine_distance(lat1, lon1, lat2, lon2):
    '''Calculate the distance between two points (lat1,lon1) and (lat2, lon2) in km'''

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance


def extend_dict(x_, avg, clat, clon):

    new_address = build_adress(x_)
    delta_average = -float(np.round(float(x_['valeur'])*60 - avg*60, 1))
    return {
        "address": new_address,
        "price_per_L": float(np.round(float(x_['valeur']), 2)),
        "price_tank": round(float(x_['valeur'])*60),
        "delta_average": delta_average,
        "better_average": (delta_average > 0) * 1 + (delta_average < 0)*-1,
        "google_map_link": f"https://www.google.com/maps/search/?api=1&query={new_address.replace(' ','+')}",
        "distance": haversine_distance(x_['latitude'], x_['longitude'], clat, clon),
        "latitude": x_['latitude'],
        "longitude": x_['longitude']
    }
