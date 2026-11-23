# Khung SQL Server

## Tạo CSDL phát triển trong SSMS

Mở `00_create_database.sql` trong SSMS, kết nối instance SQL Server dành cho đồ án rồi bấm **Execute**. Tài khoản cần quyền tạo CSDL nếu instance chưa có `HotelBooking`. Script tạo CSDL khi cần và chuyển cửa sổ đang chạy sang CSDL đó. Nếu đã có CSDL cùng tên, hãy xác nhận đó là CSDL phát triển của nhóm trước khi chạy các script DDL sau này.

Khung bắt đầu ở bước tạo CSDL. Nhóm bổ sung bảng, khóa và đối tượng nghiệp vụ sau khi duyệt ERD và lược đồ quan hệ.

## Nơi đặt SQL sau khi chốt thiết kế

| Đường dẫn | Nội dung |
|---|---|
| `migrations/` | DDL T-SQL theo phiên bản, chạy trong SSMS theo số thứ tự. Dùng mẫu `001_mo_ta.sql`, `002_mo_ta.sql`. |
| `seed/` | Dữ liệu mẫu sinh bằng T-SQL. Dùng dữ liệu tiếng Việt giả và ghi rõ cách chạy lại. |
| `programmability/` | Nguồn view, procedure, function và trigger. Ghi thứ tự chạy hoặc chỉ rõ migration triển khai từng đối tượng. |
| `security/` | Role và quyền trên SQL Server theo phạm vi của từng công việc. |
| `queries.sql` | Truy vấn nghiệp vụ, mỗi truy vấn có mã và câu hỏi. |
| `performance/` và `backup/` | Kế hoạch thực thi, chỉ mục và thao tác sao lưu/phục hồi khi tới mốc hoàn thiện CSDL. |

Mỗi thay đổi DDL ghi mã UC/BR liên quan và phụ thuộc vào các script trước đó. Người tích hợp chốt số thứ tự khi review PR. Nếu một script đã được nhóm áp dụng, đưa điều chỉnh vào script có số mới để mọi người chạy theo cùng thứ tự.
