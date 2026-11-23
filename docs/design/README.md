# Hồ sơ thiết kế CSDL

Trong ngày 1–2, mỗi thành viên tạo một tài liệu theo phần mình phụ trách để nhóm review trên PR. Nhóm lưu ERD gốc có thể sửa cùng một bản xuất ảnh sau khi ghép mô hình.

## Nội dung mỗi phần

1. **Nghiệp vụ và dữ liệu.** Ghi mã UC/BR, mục đích và dữ liệu đầu vào/đầu ra. Chỉ ra trạng thái và dữ liệu nào thay đổi trong cùng giao dịch.
2. **ERD và lược đồ quan hệ.** Ghi thực thể, thuộc tính, khóa và lực lượng tối thiểu/tối đa ở hai đầu quan hệ. Nêu khóa hoặc dữ liệu nhận từ phần khác và ai sở hữu.
3. **Chuẩn hóa.** Ghi khóa ứng viên và phụ thuộc hàm đang xét. Giải thích kết quả 1NF, 2NF và 3NF. Nếu tách bảng, mô tả lý do và đối chiếu khả năng nối lại qua khóa. Nhóm kiểm tra mọi bảng và chọn ít nhất ba bảng để trình bày chứng minh trong báo cáo.
4. **Thiết kế vật lý.** Chỉ ra quy tắc nào do PK, FK, UNIQUE, CHECK, NOT NULL hoặc DEFAULT bảo đảm. Ghi hành vi ON DELETE/UPDATE và xác định các quy tắc liên hàng cần giao dịch hoặc cơ chế phù hợp.
5. **Từ điển dữ liệu.** Điền mỗi cột một dòng theo mẫu dưới đây và dùng dữ liệu ví dụ giả.

| Bảng | Cột | Kiểu SQL Server | Khóa/ràng buộc và mặc định | Ý nghĩa | Ví dụ |
|---|---|---|---|---|---|

## Khi ghép ERD

- Đối chiếu ít nhất 10 thực thể, các quan hệ 1–1, 1–n, n–n và ít nhất một thực thể yếu hoặc phân cấp dựa trên nghiệp vụ. Lược đồ vật lý có ít nhất 12 bảng.
- Chốt tên và ý nghĩa của các khóa dùng chung trước khi viết FK. Ghi ai phụ trách từng bảng và thứ tự đưa DDL vào repo.
- Gắn mỗi quy tắc quan trọng với vị trí thực thi trong CSDL và một ví dụ dữ liệu để nhóm giải thích khi báo cáo.
