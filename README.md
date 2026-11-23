# Đặt phòng khách sạn

Đồ án cơ sở dữ liệu cho một khách sạn. Khách đặt theo hạng, lễ tân xếp phòng. Hệ thống theo dõi từng chặng khi đổi phòng, công việc buồng phòng và bảo trì, kho vật tư, phí dịch vụ, hóa đơn phòng và chứng từ tổng hợp cho lần thu.

- [Đặc tả nghiệp vụ và ca nghiệm thu](docs/requirements.md)
- [Kế hoạch 14 ngày và dàn ý báo cáo](docs/plan.md)
- [Phân công 5 người, điểm tích hợp và quy trình Git](CONTRIBUTING.md)

## Thành phần

| Thành phần | Phiên bản thiết lập trong khung |
|---|---|
| SQL Server | 2022 Developer, Linux container |
| Python | 3.12 |
| Redis | 7.4 |
| SQLAlchemy / Alembic | SQLAlchemy 2.0.x và Alembic 1.x từ 1.14 |
| FastAPI / ODBC | FastAPI từ 0.115, Microsoft ODBC Driver 18 qua pyodbc 5.x |

`database/migrations/versions/0001_baseline.py` là mốc Alembic dùng chung. Nhóm thêm DDL, dữ liệu seed và model nghiệp vụ sau khi review ERD. `app/db.py` cung cấp URL, engine và metadata ORM dùng chung. `database/bootstrap.py` tạo CSDL phát triển và login cho app rồi chạy migration. `app/main.py` có API kiểm tra kết nối.

## Nguồn tham khảo

- Slide Đồ án Cơ sở dữ liệu K75, phần chuẩn đầu ra, yêu cầu, báo cáo và quy định học thuật.
- `FULL_DATABASE.sql` của thành viên nhóm, dùng để khảo sát nghiệp vụ bản SQL Server trước đây.
- [SQL Server trong Docker](https://learn.microsoft.com/sql/linux/install-upgrade/quickstart-install-docker), [ODBC 18 trên Linux](https://learn.microsoft.com/sql/connect/odbc/linux/installing-the-microsoft-odbc-driver-for-sql-server-on-linux) và [dialect SQL Server của SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/mssql.html).
