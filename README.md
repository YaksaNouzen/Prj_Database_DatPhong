# Đồ án CSDL đặt phòng khách sạn

Đồ án tập trung vào phân tích, thiết kế và triển khai cơ sở dữ liệu trên **Microsoft SQL Server**, thao tác bằng **SSMS và T-SQL**. Phạm vi gồm một khách sạn, đặt theo hạng, xếp phòng, chuyển phòng, buồng phòng, bảo trì, kho, dịch vụ và thanh toán theo từng chặng lưu trú.

## Bắt đầu

1. Đọc [đặc tả nghiệp vụ](docs/requirements.md) và chốt các tình huống liên quan đến giữ chỗ, đổi phòng và gộp hóa đơn.
2. Xem [phân công](CONTRIBUTING.md), tạo nhánh riêng và làm ERD, lược đồ quan hệ, chuẩn hóa cho phần mình theo [mẫu thiết kế](docs/design/README.md).
3. Cả nhóm review ERD tổng và chốt khóa dùng chung. Sau đó dùng [khung SQL Server](database/README.md) để tạo CSDL phát triển và thêm DDL theo thứ tự phụ thuộc.

[Kế hoạch 14 ngày và dàn ý báo cáo](docs/plan.md) ghi các đầu ra cần có ở từng mốc. [Phạm vi làm việc](AGENTS.md) áp dụng cho cả thành viên và công cụ hỗ trợ.

## Nguồn tham khảo

- Slide Đồ án Cơ sở dữ liệu K75, phần chuẩn đầu ra, yêu cầu thiết kế, báo cáo và quy định học thuật. Phạm vi ứng dụng và kiểm thử theo xác nhận mới của giảng viên.
- `FULL_DATABASE.sql` của thành viên nhóm, dùng để khảo sát nghiệp vụ khách sạn trước đây.
