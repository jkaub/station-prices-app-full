from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from sqlmodel import Session
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_Distance, ST_AsGeoJSON
from sqlalchemy import func, and_
import numpy as np

from .services import engine, create_db_and_tables
from .models import Cities, Stations, GasPrices
from .utils import extend_dict, pretify_address

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/add-city/")
async def add_city(city: Cities):
    with Session(engine) as session:
        exist = session.query(Cities).filter(
            Cities.postal_code == city.postal_code).first()
        print(exist)
        if exist:
            raise HTTPException(
                status_code=400, detail="Postal code already exists")

        session.add(city)
        session.commit()
        session.refresh(city)
        return city


@app.post("/add-station/")
async def add_station(station: Stations):
    with Session(engine) as session:
        exist = session.query(Stations).filter(
            Stations.station_id == station.station_id).first()
        if exist:
            raise HTTPException(
                status_code=400, detail="Station already exists")

        point = f"POINT({station.longitude} {station.latitude})"
        station.geom = WKTElement(point, srid=4326)

        session.add(station)
        session.commit()
        session.refresh(station)

        to_return = {}
        to_return["station_id"] = station.station_id
        to_return["latitude"] = station.latitude
        to_return["longitude"] = station.longitude
        to_return["cp"] = station.cp
        to_return['city'] = station.city
        to_return["adress"] = station.adress

        return to_return


@app.post("/add-gas-price/")
async def add_station(gasPrice: GasPrices):
    with Session(engine) as session:
        exist = session.query(GasPrices). \
            filter(GasPrices.station_id == gasPrice.station_id). \
            filter(GasPrices.oil_id == gasPrice.oil_id). \
            filter(GasPrices.nom == gasPrice.nom). \
            filter(GasPrices.valeur == gasPrice.valeur). \
            filter(GasPrices.maj == gasPrice.maj). \
            first()
        if exist:
            raise HTTPException(
                status_code=400, detail="Entry already exists")

        session.add(gasPrice)
        session.commit()
        session.refresh(gasPrice)
        return gasPrice


@app.get("/stations/")
async def get_prices(oil_type: str, postal_code: str):
    with Session(engine) as session:
        city = session.query(Cities).filter(
            Cities.postal_code == postal_code).first()
        if not city:
            raise HTTPException(
                status_code=404, detail="Postal Code not found")
        stations = session.query(
            Stations.station_id, Stations.adress,  Stations.cp, Stations.city,
            Stations.latitude, Stations.longitude,
        ).filter(
            ST_Distance(
                Stations.geom.ST_GeogFromWKB(),
                WKTElement(f"POINT({city.lon} {city.lat})",
                           srid=4326).ST_GeogFromWKB()
            ) < 30000).subquery()

        price_wanted_gas = session.query(GasPrices).filter(
            GasPrices.nom == oil_type
        ).subquery()

        last_price = session.query(
            price_wanted_gas.c.station_id,
            func.max(price_wanted_gas.c.maj).label("max_maj")
        ).group_by(price_wanted_gas.c.station_id) \
            .subquery()

        last_price_full = session.query(price_wanted_gas).join(
            last_price,
            and_(
                price_wanted_gas.c.station_id == last_price.c.station_id,
                price_wanted_gas.c.maj == last_price.c.max_maj
            )
        ).subquery()

        stations_with_price = session.query(stations, last_price_full).join(
            last_price_full,
            stations.c.station_id == last_price_full.c.station_id
        ).all()

        prices = [float(e["valeur"]) for e in stations_with_price]
        avg_price = float(np.median(prices))

        output = {
            "lat": city.lat,
            "lon": city.lon,
            "city": pretify_address(city.name),
            "station_infos": sorted([extend_dict(x, avg_price, city.lat, city.lon) for x in stations_with_price], key=lambda x: -(x['delta_average']))
        }

        return output
