import os

from alembic import command
from alembic.config import Config
from sqlalchemy.exc import SQLAlchemyError

from app.db import database_engine


def prepare_database():
    password = os.environ["HOTEL_APP_PASSWORD"]
    if not 8 <= len(password) <= 128 or "\x00" in password:
        raise SystemExit("HOTEL_APP_PASSWORD phải có từ 8 đến 128 ký tự hợp lệ")
    if password == os.environ["DB_PASSWORD"]:
        raise SystemExit("Mật khẩu ứng dụng phải khác mật khẩu quản trị")

    # SQL Server yêu cầu literal cho PASSWORD trong CREATE LOGIN.
    password_literal = "N'" + password.replace("'", "''") + "'"
    master_engine = database_engine("master", isolation_level="AUTOCOMMIT")
    hotel_engine = database_engine()
    try:
        with master_engine.connect() as connection:
            connection.exec_driver_sql(
                "IF DB_ID(N'HotelBooking') IS NULL EXEC(N'CREATE DATABASE [HotelBooking]')"
            )
            try:
                connection.exec_driver_sql(
                    "IF SUSER_ID(N'hotel_app') IS NULL "
                    f"CREATE LOGIN [hotel_app] WITH PASSWORD = {password_literal}"
                )
            except SQLAlchemyError:
                raise SystemExit("Không tạo được login hotel_app. Kiểm tra chính sách mật khẩu.") from None
        with hotel_engine.begin() as connection:
            connection.exec_driver_sql(
                "IF DATABASE_PRINCIPAL_ID(N'hotel_app') IS NULL "
                "CREATE USER [hotel_app] FOR LOGIN [hotel_app]"
            )
    finally:
        master_engine.dispose()
        hotel_engine.dispose()


if __name__ == "__main__":
    prepare_database()
    command.upgrade(Config("alembic.ini"), "head")
