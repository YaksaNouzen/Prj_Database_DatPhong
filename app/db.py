import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def database_url(database: str = "HotelBooking") -> URL:
    return URL.create(
        "mssql+pyodbc",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=1433,
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
        },
    )


def database_engine(database: str = "HotelBooking", **options):
    return create_engine(database_url(database), pool_pre_ping=True, **options)
