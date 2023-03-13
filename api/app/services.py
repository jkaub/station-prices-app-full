from sqlmodel import SQLModel, create_engine

DATABASE_URL = 'postgresql://jkaub:jkaub@stationdb/stations'

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
