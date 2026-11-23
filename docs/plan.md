# Kế hoạch 14 ngày

Ngày 1 là ngày nhóm bắt đầu. Mục tiêu ngày 14 là bản chạy được và có minh chứng kiểm tra tiến độ. Ngày 15–21 là dự phòng cho lỗi tích hợp, số đo, chỉnh báo cáo và diễn tập nếu nhóm cần. Kế hoạch dùng lịch nội bộ của nhóm.

| Mốc | Việc chính | Tiêu chí kết thúc |
|---|---|---|
| Ngày 1–2 | Cả nhóm duyệt UC/BR, chạy thử khung, viết ca nghiệm thu. Mỗi người vẽ ERD phần mình và ghi phụ thuộc hàm. | Chốt quy tắc xác nhận, đổi phòng, tiền phòng, phạm vi hóa đơn tổng và nguồn dữ liệu dùng chung. |
| Ngày 3–4 | Ghép ERD, chốt PK/FK, trạng thái, quyền sở hữu bảng và cách giao tiếp giữa các phần. | ERD ≥10 thực thể, đủ 1–1, 1–n, n–n và ≥1 thực thể yếu hoặc phân cấp. Lược đồ đạt ≥12 bảng, ≥3 bảng có chứng minh bằng phụ thuộc hàm, mọi cột có mục từ điển. |
| Ngày 5–7 | Viết Alembic DDL, procedure, function và trigger theo chuỗi phụ thuộc. Viết truy vấn và test song song khi hợp đồng đã chốt. | Migration chạy trên CSDL mới. Ca đặt, đổi phòng, phát sinh và trả tiền có thể kiểm tra bằng SQL. |
| Ngày 8–10 | Tích hợp ORM/API, Redis, quyền và seed. Mỗi người đưa SQL của mình vào PR có review. | Swagger và giao diện đủ dùng, ≥6 nghiệp vụ cốt lõi xuyên suốt, ≥1 nghiệp vụ qua stored procedure, dữ liệu seed đủ quy mô. |
| Ngày 11–12 | Chạy Testcontainers, hai phiên SQL, benchmark cache và chỉ mục. Tạo backup, phục hồi vào CSDL demo riêng và đối soát. | ≥15 test tự động. Có số liệu hiệu năng, log cạnh tranh, bằng chứng cache cập nhật và phục hồi. |
| Ngày 13–14 | Dựng lại bằng Compose, sửa lỗi, gom báo cáo và tập demo theo một kịch bản. | Repo có hướng dẫn, bản báo cáo và phụ lục đủ để kiểm tra tiến độ. Chuẩn bị PDF, slide, video và tag theo thời điểm nộp của nhóm. |

## Phân bổ chỉ tiêu và minh chứng

| Yêu cầu | Cách thực hiện và minh chứng |
|---|---|
| CLO1–2 | Từ UC/BR đến lược đồ, DDL và test. Nhóm kiểm tra mọi bảng đạt 3NF và chứng minh ≥3 bảng. Ghi khóa ứng viên, các phụ thuộc hàm, giải thích 1NF–3NF, logic tên cột, PK/FK và ON DELETE/UPDATE. Từ điển mọi cột có kiểu, ràng buộc, ý nghĩa và ví dụ. |
| CLO3 | TV1–5 mỗi người viết 4 truy vấn có câu hỏi nghiệp vụ. Chỉ tiêu chung ≥3 view, ≥3 procedure có tham số và xử lý lỗi/giao dịch khi có ghi, ≥2 function có tham số, ≥2 trigger gồm 1 nghiệp vụ liên hàng và 1 audit. |
| CLO4 | ≥5 chỉ mục có lý do, gồm composite và covering hoặc filtered. Đo trước/sau cùng dữ liệu và tham số trên tìm phòng, công nợ và công suất. Lưu actual execution plan, thời gian và logical reads qua `SET STATISTICS IO, TIME ON`. |
| CLO5 | Hai phiên SQL tái hiện tranh phòng trong bản demo tách biệt, sau đó chạy trên thiết kế đã chặn. Dùng ≥3 role SQL có GRANT/REVOKE, app dùng login riêng, truy vấn có tham số và mật khẩu lưu dạng hash Argon2 nếu làm đăng nhập. Backup bằng `BACKUP DATABASE`, phục hồi vào DB riêng, xác minh dòng mẫu đã xóa và kiểm tra quyền. |
| CLO6 | FastAPI/SQLAlchemy/Alembic. Bảy nghiệp vụ ưu tiên là tìm phòng, tạo yêu cầu, xác nhận và xếp phòng, nhận phòng, chuyển phòng, trả phòng và thu tiền. ≥15 test tự động trên SQL Server thật trong Testcontainers, gồm ca vi phạm ràng buộc và rollback. |
| CLO7 | Git, PR có người review, mỗi thành viên giải thích được SQL đã commit. Báo cáo 30–50 trang, Times New Roman 13, giãn dòng 1,3, lề trái 3 cm và còn lại 2 cm. Phụ lục có từ điển dữ liệu, phân công, khai báo dùng AI. Chuẩn bị slide 15 phút và video ≤7 phút. |
| Dữ liệu | Script sinh dữ liệu tiếng Việt giả, chạy lại được, ≥10.000 bản ghi tại tập giao dịch đặt phòng và ≥100.000 tại tập chi tiết giao dịch phục vụ đo, chọn bảng cụ thể khi duyệt ERD. Báo cáo số lượng thực tế và kiểm tra ràng buộc sau seed. Compose bản hoàn thiện tự chạy migration và seed. |
| Demo riêng | Đo độ trễ API tìm phòng với cache tắt và cache đã làm nóng, mỗi chế độ chạy cùng dữ liệu/câu hỏi và ghi p50/p95. Làm nóng cache khi chỉ còn một phòng, xác nhận rồi tìm lại bằng đúng tham số. |

## Nội dung buổi chốt thiết kế

1. Đi qua AC01–AC07 trong [đặc tả](requirements.md). Với mỗi lần ghi, ghi rõ dữ liệu nào đổi cùng giao dịch và hành vi khi một bước thất bại.
2. Chốt ý nghĩa và chủ sở hữu năm định danh dùng giữa các phần gồm khách, phòng, yêu cầu đặt, lượt lưu trú và chặng phòng. Chốt phần dữ liệu cần trao đổi giữa lễ tân, vận hành và thu ngân trước khi đặt FK hoặc viết ORM.
3. TV2 và TV3 chọn một đường ghi lịch dùng chung. Một hướng để thử là khóa ứng dụng theo mã phòng bằng `sp_getapplock`, với chủ sở hữu giao dịch. Kiểm tra mã trả về, đọc lại lịch sau khi lấy khóa và ghi trong cùng giao dịch. Khi chuyển giữa hai phòng, lấy hai khóa theo thứ tự mã. Giới hạn quyền ghi trực tiếp để mọi đường xác nhận, hủy, chuyển phòng và bảo trì đều tuân thủ. [Tài liệu Microsoft](https://learn.microsoft.com/sql/relational-databases/system-stored-procedures/sp-getapplock-transact-sql)
4. TV1, TV2 và TV5 chốt cơ chế nhất quán Redis. Có thể thử khóa cache chứa phiên bản lịch do SQL Server tăng trong giao dịch ghi. Khi cache miss, phải đọc dữ liệu và phiên bản nhất quán trước khi ghi cache. Khi Redis lỗi, tìm trực tiếp từ SQL Server. Khi phục hồi DB, làm mới không gian khóa cache trước khi mở lại ứng dụng. Đo cả chi phí lấy phiên bản trong benchmark.
5. Cả nhóm ghép bản ERD tự vẽ, chọn chủ sở hữu từng bảng và đối chiếu giới hạn số lượng thực thể quan hệ. Chọn ít nhất ba bảng có phụ thuộc hàm đáng giải thích, rồi ghi chứng minh trong báo cáo. Dựng DDL sau khi phần giao nhau được review.

## Dàn ý báo cáo và nơi ghi minh chứng

| Chương | Nội dung cần thu trong lúc làm | Chủ trì |
|---|---|---|
| 1 · Tổng quan | Phạm vi một khách sạn, công nghệ, lý do dùng SQL Server và Redis | TV1 |
| 2 · Phân tích | Đặc tả UC, BR, luồng chính và ngoại lệ, use case diagram của nhóm | TV1 và cả nhóm |
| 3 · Thiết kế | ERD gốc và ảnh xuất, lược đồ, phụ thuộc hàm, DDL, giải thích lựa chọn | TV2 và cả nhóm |
| 4 · Cài đặt | Migration, procedure, function, trigger, view và quyền | TV3, TV4, TV5 |
| 5 · Truy vấn và tối ưu | Câu hỏi, truy vấn, execution plan và số đo trước/sau | TV5 và tác giả truy vấn |
| 6 · Giao dịch | Hai phiên SQL, nguyên nhân lỗi, thứ tự khóa, kết quả rollback | TV2, TV4 |
| 7 · Tích hợp | ORM, Swagger, kiểm thử, cache, backup/restore và demo | TV1, TV3, TV5 |
| 8 · Kết luận | Kết quả đo, phạm vi hoàn thành, hạn chế và hướng mở rộng | Cả nhóm |
