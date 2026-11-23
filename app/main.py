import os

from fastapi import FastAPI, HTTPException
from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db import database_engine

app = FastAPI(title="Đặt phòng khách sạn")
engine = database_engine()
cache = Redis.from_url(os.environ["REDIS_URL"], socket_timeout=2)


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            is_admin = connection.scalar(text("SELECT IS_SRVROLEMEMBER('sysadmin')"))
        if is_admin != 0:
            raise HTTPException(503, "Tài khoản ứng dụng phải có quyền giới hạn")
        cache.ping()
    except (SQLAlchemyError, RedisError) as exc:
        raise HTTPException(503, "Chưa kết nối được SQL Server hoặc Redis") from exc
    return {"sql_server": "ok", "redis": "ok"}
