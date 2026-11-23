# Phân công nhóm 5 người

Thay TV1–TV5 bằng tên và tài khoản GitHub của từng người khi nhóm họp. Tác nhân là góc nhìn nghiệp vụ phụ trách. Mỗi thành viên tự làm thiết kế phần mình, viết migration và SQL liên quan, ghi quyết định thiết kế và review PR của người khác.

| Thành viên · tác nhân | Phần thiết kế và triển khai | Truy vấn và minh chứng CSDL | Nhánh |
|---|---|---|---|
| TV1 · Khách hàng | UC01–04, UC21. Hồ sơ khách, tìm theo hạng, gửi yêu cầu, xác nhận phương án, yêu cầu đổi hoặc hủy. | Q01–04, gồm `NOT EXISTS` để tìm phòng theo khoảng ngày. Chủ trì hồ sơ đặc tả và đối chiếu quyền đọc/hủy đơn. | `feature/customer-search` |
| TV2 · Lễ tân | UC05–09, UC23–25. Giữ và xếp phòng, xác nhận đặt, nhận trực tiếp/từ xa, no-show, thay phòng, chuyển phòng, gia hạn và trả sớm. Phối hợp TV5 với danh mục và TV4 với lịch cọc. | Q05–08, gồm `JOIN` ít nhất ba bảng. Đo truy vấn tìm phòng và minh họa hai phiên SQL tranh cùng phòng. | `feature/front-desk` |
| TV3 · Nhân viên khách sạn | UC10–13, buồng phòng, bảo trì, kho và dịch vụ tính phí. Chủ trì procedure điều chỉnh tồn và trigger bảo đảm một quy tắc liên hàng. | Q09–12, gồm `OUTER JOIN` và `HAVING`. Chủ trì seed tiếng Việt và phân biệt vật tư nội bộ với vật tư tính phí. | `feature/hotel-operations` |
| TV4 · Thu ngân | UC14–16, UC22. Cọc, hoàn/giữ/cấn cọc, hóa đơn theo chặng, khoản thu, phân bổ và hóa đơn tổng. Chủ trì procedure thu và function tính công nợ. | Q13–16, gồm truy vấn tương quan và window function. Đối chiếu tổng phân bổ, khoản cọc, khoản thu và số còn nợ. | `feature/cashier-billing` |
| TV5 · Quản lý | UC17–20, UC26–27. Vai trò, danh mục, lịch ngày lễ, báo cáo, duyệt điều chỉnh và bồi thường. Chủ trì ba view gồm view ẩn cột nhạy cảm, function tính chỉ số và trigger audit. | Q17–20, gồm CTE thường và CTE đệ quy. Gom kế hoạch thực thi và kết quả sao lưu, phục hồi. | `feature/management` |

## Hợp đồng dùng chung trước khi tách migration

| Điểm giao | Hai bên chốt |
|---|---|
| TV1 ↔ TV2 | Mã yêu cầu, mã khách, mã hạng, khoảng ngày, hạn giữ, xác nhận của khách và lý do đóng đơn |
| TV2 ↔ TV3 | Mã phòng và chặng, quy tắc khóa lịch bảo trì, công việc dọn sau trả/chuyển |
| TV2 ↔ TV4 | Mã đơn/lượt/chặng, giá chốt, điều kiện cọc, lý do hoàn/giữ cọc, cách chia chặng và điều kiện công nợ khi check-out |
| TV3 ↔ TV4 | Mã phát sinh gốc, chặng sử dụng, số lượng và đơn giá, quy tắc tính phí một lần |
| TV1–4 ↔ TV5 | Lịch ngày lễ, trạng thái cần audit, quyền duyệt điều chỉnh/bồi thường và nguồn tính báo cáo |

Dùng [mẫu hồ sơ thiết kế](docs/design/README.md) để ghi thực thể, bảng, phụ thuộc hàm và từ điển dữ liệu. Gắn bảng với mã UC/BR để cả nhóm review được lý do tồn tại của từng cột và ràng buộc.

## Git và migration

1. Khi khung đã vào `main`, clone hoặc kéo `main`, tạo nhánh trong bảng. Trong ngày 1–2, có thể dùng nhánh để commit tài liệu thiết kế phần mình.
2. Người review theo vòng TV1 → TV2 → TV3 → TV4 → TV5 → TV1. Thay đổi hợp đồng cần người ở phần liên quan cùng review.
3. Chốt thứ tự script T-SQL sau khi duyệt FK. Script tạo bảng được tham chiếu đi trước script tạo FK. Gộp từng thay đổi qua PR và cấp số script theo [quy ước SQL](database/README.md).
4. PR ghi mã UC/BR, thay đổi trong mô hình hoặc DDL và ví dụ dữ liệu nếu cần giải thích hành vi. Viết truy vấn trên nhánh riêng, rồi ghép vào `database/queries.sql` khi review.
