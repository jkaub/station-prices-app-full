from dataparsing import get_data
from consts import API_URL
from tqdm import tqdm
import requests


def update_stations(stations):
    url = f'{API_URL}/add-station/'
    to_push = stations[['latitude', 'longitude', 'cp',
                        'adress', 'city', 'station_id']].to_dict('records')
    for elmt in tqdm(to_push):
        elmt['cp'] = str(elmt['cp']).zfill(5)
        req = requests.post(url, json=elmt)


def update_gas(gas):
    to_push = gas.to_dict('records')

    url = f'{API_URL}/add-gas-price/'
    for elmt in tqdm(to_push):
        req = requests.post(url, json=elmt)


if __name__ == "__main__":
    print("PULL DATA")
    stations, gas = get_data()
    print("UPDATE STATIONS")
    update_stations(stations)
    print("UPDATE GAS PRICES")
    update_gas(gas)
