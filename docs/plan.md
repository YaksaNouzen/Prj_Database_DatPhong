# Kế hoạch thiết kế CSDL trong 14 ngày

Ngày 1 là ngày nhóm bắt đầu. Mục tiêu ngày 14 là có hồ sơ thiết kế và bản SQL Server để kiểm tra tiến độ. Ngày 15–21 dành cho việc sửa thiết kế, bổ sung minh chứng hoặc hoàn thiện báo cáo nếu cần.

| Mốc | Việc chính | Đầu ra |
|---|---|---|
| Ngày 1–2 | Rà soát use case, quy tắc và các tình huống minh họa trong đặc tả. Mỗi người vẽ ERD phần mình và ghi phụ thuộc hàm. | Cả nhóm thống nhất cách diễn giải lịch giữ, cọc, no-show, đổi phòng và các chặng tính tiền. |
| Ngày 3–4 | Ghép ERD, chốt PK/FK, trạng thái và chủ sở hữu dữ liệu giữa các phần. | ERD tổng, lược đồ quan hệ, bằng chứng 3NF và bản đầu của từ điển dữ liệu. |
| Ngày 5–7 | Viết DDL T-SQL theo thứ tự phụ thuộc. Viết và review ràng buộc, dữ liệu mẫu và các truy vấn nền. | Cấu trúc CSDL có thể dựng bằng SSMS. Có dữ liệu minh họa từ đặt phòng đến thanh toán. |
| Ngày 8–10 | Hoàn thiện truy vấn, view, procedure, function, trigger, chỉ mục và quyền. | Các nghiệp vụ chính và báo cáo có thể minh họa trực tiếp từ SQL Server. |
| Ngày 11–12 | Thu kết quả hai phiên SQL tranh phòng, kế hoạch thực thi trước/sau và sao lưu/phục hồi trên CSDL demo riêng. | Minh chứng CSDL cho ràng buộc và giao dịch, chỉ mục và khôi phục dữ liệu. |
| Ngày 13–14 | Review hồ sơ thiết kế, chạy script theo hướng dẫn trên CSDL mới, hoàn thiện báo cáo tiến độ. | ERD gốc và ảnh xuất, lược đồ, từ điển, script và các minh chứng CSDL đã làm. |

## Tiêu chí phần CSDL

| Hạng mục | Đầu ra |
|---|---|
| Đặc tả | ≥15 use case, ≥10 quy tắc có mã, phân công năm tác nhân. Gắn các tình huống với kết quả mong đợi và vị trí cần ràng buộc. |
| ERD và chuẩn hóa | ERD ≥10 thực thể, đủ 1–1, 1–n, n–n và ≥1 thực thể yếu hoặc phân cấp. Toàn bộ lược đồ đạt ít nhất 3NF. Chứng minh ≥3 bảng qua phụ thuộc hàm. |
| Thiết kế vật lý | ≥12 bảng. Ghi PK, FK và ON DELETE/UPDATE, UNIQUE, CHECK, NOT NULL, DEFAULT phù hợp. Từ điển ghi kiểu, ràng buộc, ý nghĩa, ví dụ cho mọi cột. DDL được quản lý bằng script T-SQL có thứ tự. |
| Dữ liệu mẫu | Dùng script sinh dữ liệu giả tiếng Việt. Theo tiêu chí CSDL trong đề bài, chuẩn bị ≥10.000 bản ghi ở bảng giao dịch chính và ≥100.000 ở một bảng phục vụ đo. Chọn bảng sau khi duyệt ERD. |
| Truy vấn và lập trình CSDL | ≥20 truy vấn có câu hỏi nghiệp vụ, bao phủ các dạng SQL đã chia. ≥3 view gồm một view phục vụ phân quyền, ≥3 procedure, ≥2 function và ≥2 trigger gồm một trigger nghiệp vụ và một trigger audit. |
| Chỉ mục và hiệu năng | ≥5 chỉ mục có lý do, gồm composite và covering hoặc filtered. Đo trước/sau trên ba truy vấn với cùng dữ liệu và tham số. Lưu actual execution plan, thời gian và logical reads qua `SET STATISTICS IO, TIME ON`. |
| Giao dịch, quyền và phục hồi | Dùng hai phiên SQL để minh họa tranh cùng phòng. Thiết kế ≥3 role SQL và cấp quyền theo công việc. Lưu script backup/restore và minh chứng phục hồi trên CSDL demo riêng. |
| Quản lý nhóm | Mỗi thành viên làm trên nhánh riêng, PR có người review. Báo cáo giải thích quyết định thiết kế, phụ lục có từ điển, phân công và khai báo dùng AI. |

Tích hợp ứng dụng và kiểm thử tự động được hoãn theo phạm vi giảng viên đã xác nhận. Các tình huống trong đặc tả giúp nhóm đối chiếu mô hình và giải thích ràng buộc. Có thể minh họa thao tác trực tiếp trong SSMS để lấy minh chứng CSDL.

## Buổi chốt thiết kế

1. Đi qua các tình huống trong [đặc tả](requirements.md), ưu tiên tranh lượt giữ, hết hạn giữ, cọc đến trễ, no-show, hoàn cọc và đổi phòng. Với mỗi thao tác ghi, thống nhất dữ liệu nào đổi cùng giao dịch và trạng thái khi một bước thất bại.
2. Chốt ý nghĩa và chủ sở hữu của mã khách, phòng, yêu cầu đặt, lượt lưu trú và chặng phòng. Dùng các điểm giao trong [phân công](../CONTRIBUTING.md) để chốt khóa ngoại.
3. TV2 và TV3 thống nhất cách chặn xếp trùng phòng và cách ghi lịch bảo trì. Một phương án nhóm có thể đánh giá sau khi duyệt mô hình là khóa theo mã phòng trong giao dịch bằng `sp_getapplock`, rồi kiểm tra lại lịch trước khi ghi. Với giao dịch chuyển phòng, dùng thứ tự lấy khóa cố định. [Tài liệu Microsoft](https://learn.microsoft.com/sql/relational-databases/system-stored-procedures/sp-getapplock-transact-sql)
4. Cả nhóm ghép ERD, rà số lượng và loại quan hệ. Chọn các bảng để trình bày chứng minh 3NF, chốt thứ tự DDL và hoàn thiện [hồ sơ thiết kế](design/README.md).

## Dàn ý báo cáo

| Chương | Nội dung | Chủ trì |
|---|---|---|
| 1 · Tổng quan | Bài toán, phạm vi một khách sạn và lý do dùng SQL Server | TV1 |
| 2 · Phân tích yêu cầu | Tác nhân, use case, quy tắc và tình huống nghiệp vụ | TV1 và cả nhóm |
| 3 · Thiết kế CSDL | ERD gốc và ảnh xuất, lược đồ, phụ thuộc hàm, DDL và giải thích lựa chọn | TV2 và cả nhóm |
| 4 · Cài đặt CSDL | Ràng buộc, view, procedure, function, trigger, quyền | TV3, TV4, TV5 |
| 5 · Truy vấn và tối ưu | Câu hỏi nghiệp vụ, execution plan và số đo trước/sau | TV5 và tác giả truy vấn |
| 6 · Giao dịch và đồng thời | Hai phiên SQL, nguyên nhân xung đột, giải pháp và kết quả | TV2, TV4 |
| 7 · Triển khai CSDL | Thứ tự script, dữ liệu minh họa, sao lưu và phục hồi | TV3, TV5 |
| 8 · Kết luận | Kết quả, hạn chế và phần có thể mở rộng | Cả nhóm |

Khi hoàn thiện báo cáo, theo định dạng trong slide. Báo cáo dài 30–50 trang, Times New Roman 13, giãn dòng 1,3, lề trái 3 cm, các lề còn lại 2 cm. Phụ lục gồm từ điển dữ liệu và bảng phân công.
