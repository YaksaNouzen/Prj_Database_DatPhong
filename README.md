# Đặt phòng khách sạn

Đồ án cơ sở dữ liệu cho một khách sạn. Khách đặt theo hạng, lễ tân xếp phòng. Hệ thống theo dõi từng chặng khi đổi phòng, công việc buồng phòng và bảo trì, kho vật tư, phí dịch vụ, hóa đơn phòng và chứng từ tổng hợp cho lần thu.

- [Đặc tả nghiệp vụ và ca nghiệm thu](docs/requirements.md)
- [Kế hoạch 14 ngày và dàn ý báo cáo](docs/plan.md)
- [Phân công 5 người, điểm tích hợp và quy trình Git](CONTRIBUTING.md)

## Chạy khung trên Windows

Cần Docker Desktop chạy Linux containers trên máy x86-64 và Docker Compose v2. Mở PowerShell từ thư mục repo. Tạo `.env` bằng lệnh đầu tiên khi chưa có tệp này, rồi thay hai mật khẩu mẫu trong tệp.

```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose logs migrate
Invoke-RestMethod http://localhost:8000/health
```

Sau khi migration chạy xong, `/health` trả về `sql_server: ok` và `redis: ok`. Mở [Swagger cục bộ](http://localhost:8000/docs). SSMS có thể kết nối `localhost,1433`, dùng SQL Server Authentication. Nếu máy có instance khác đang dùng cổng 1433, đổi cổng ở vế trái của ánh xạ trong Compose và dùng cổng tương ứng khi kết nối từ Windows. Để dừng môi trường phát triển, chạy `docker compose down`. Dữ liệu SQL Server được giữ trong volume.

Tài khoản `sa` dùng để khởi tạo và chạy migration. Ứng dụng dùng login riêng `hotel_app`. Khi container đã tạo login, thay mật khẩu trong `.env` cần đồng bộ mật khẩu trong SQL Server. Cấu hình chứng chỉ mặc định dành cho máy phát triển.

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
