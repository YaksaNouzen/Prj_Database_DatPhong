# Phân công nhóm 5 người

Thay TV1–TV5 bằng tên và tài khoản GitHub của từng người khi nhóm họp. Tác nhân là góc nhìn nghiệp vụ phụ trách. Mỗi thành viên tự làm thiết kế phần mình, viết migration và SQL liên quan, ghi quyết định thiết kế và review PR của người khác.

| Thành viên · tác nhân | Phần thiết kế và triển khai | Phần kiểm thử và minh chứng | Nhánh |
|---|---|---|---|
| TV1 · Khách hàng | UC01–04, hồ sơ khách, yêu cầu theo hạng, lịch sử và hủy. Tích hợp ORM, Swagger, tìm phòng và Redis cùng TV5. | Q01–04 gồm truy vấn phong cách NOT EXISTS cho tìm phòng, 3 test tìm, hủy và quyền khách. | `feature/customer-search` |
| TV2 · Lễ tân | UC05–09, danh mục phòng phối hợp TV5, xếp phòng, lịch, chặng lưu trú. Chủ trì procedure xác nhận và chuyển phòng. | Q05–08 gồm JOIN ≥3 bảng. 3 test tranh phòng, biên ngày, chuyển rollback. Đo tìm phòng và lưu demo hai phiên. | `feature/front-desk` |
| TV3 · Nhân viên khách sạn | UC10–13, phân công buồng phòng, bảo trì, kho và dịch vụ tính phí. Chủ trì procedure điều chỉnh tồn và trigger kiểm tra một quy tắc liên hàng. | Q09–12 gồm OUTER JOIN và HAVING. 3 test bảo trì, xuất quá tồn, phân biệt vật tư nội bộ. Phối hợp seed tiếng Việt. | `feature/hotel-operations` |
| TV4 · Thu ngân | UC14–16, hóa đơn theo chặng, khoản thu, phân bổ và hóa đơn tổng. Chủ trì procedure thu và function tính khoản còn phải thu. | Q13–16 gồm truy vấn tương quan, window function. 3 test thu thiếu, thu vượt, gửi trùng mã. Đo công nợ. | `feature/cashier-billing` |
| TV5 · Quản lý | UC17–20, vai trò, danh mục và báo cáo. Chủ trì 3 view gồm view ẩn cột nhạy cảm, function tính chỉ số ngày và trigger audit. | Q17–20 gồm CTE thường và CTE đệ quy sinh dãy ngày công suất. 3 test quyền SQL, audit, cache sau commit. Gom kết quả đo, diễn tập backup/restore. | `feature/management` |

## Hợp đồng dùng chung trước khi tách migration

| Điểm giao | Hai bên chốt |
|---|---|
| TV1 ↔ TV2 | Mã yêu cầu, mã khách, mã hạng, khoảng ngày, trạng thái và điều kiện xác nhận/hủy |
| TV2 ↔ TV3 | Mã phòng và chặng, quy tắc khóa lịch bảo trì, công việc dọn sau trả/chuyển |
| TV2 ↔ TV4 | Mã lượt/chặng, đơn giá chốt, đêm tính tiền và ranh giới giao dịch khi chuyển phòng |
| TV3 ↔ TV4 | Mã phát sinh gốc, chặng sử dụng, số lượng và đơn giá, quy tắc tính phí một lần |
| TV1–4 ↔ TV5 | Trạng thái cần audit, view theo quyền, nguồn tính báo cáo và sự kiện làm đổi kết quả tìm phòng |

Mẫu ghi một bảng trong tài liệu thiết kế của từng thành viên gồm mục đích và mã UC/BR, khóa ứng viên, phụ thuộc hàm, cột và kiểu dữ liệu, null/default/check, FK và hành vi khi cập nhật/xóa, dữ liệu ví dụ, chỉ mục dự kiến và mã test. ERD tổng cần chỉ rõ lực lượng và tính bắt buộc ở hai đầu mỗi quan hệ. Hãy đề xuất quan hệ 1–1, 1–n, n–n và thực thể yếu hoặc phân cấp từ nghiệp vụ thực rồi giải thích trong buổi ghép ERD.

## Git và migration

1. Khi khung đã vào `main`, clone hoặc kéo `main`, tạo nhánh trong bảng. Trong ngày 1–2, có thể dùng nhánh để commit tài liệu thiết kế phần mình.
2. Người review theo vòng TV1 → TV2 → TV3 → TV4 → TV5 → TV1. Thay đổi hợp đồng cần người ở phần liên quan cùng review.
3. Chốt thứ tự migration sau khi duyệt FK. Phần có FK đến đối tượng khác đi sau phần tạo đối tượng đó. Đẩy PR migration lần lượt, cập nhật `down_revision` theo head hiện hành trước khi gộp và kiểm tra Alembic có một head. Kiểm tra upgrade trên DB mới và DB đã chạy bản trước.
4. PR ghi mã UC/BR, thay đổi dữ liệu, câu lệnh kiểm thử và kết quả. Viết SQL truy vấn riêng trên nhánh, rồi ghép vào `database/queries.sql` khi review. Phiên bản hoàn thiện lưu minh chứng trong các thư mục của đề bài.
