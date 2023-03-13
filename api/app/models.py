from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy import Column
from geoalchemy2.types import Geometry
from typing import Any


class Cities(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    postal_code: str
    name: str
    lat: float
    lon: float


class GasPrices(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    station_id: str
    oil_id: str
    nom: str
    valeur: float
    maj: datetime = Field(default_factory=datetime.utcnow)


class Stations(SQLModel, table=True):
    station_id: str = Field(primary_key=True)
    latitude: float
    longitude: float
    cp: str
    city: str
    adress: str
    geom: Optional[Any] = Field(sa_column=Column(Geometry('GEOMETRY')))
