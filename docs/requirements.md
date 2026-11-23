# Đặc tả đặt phòng khách sạn

## Phạm vi

Nhóm thiết kế CSDL cho một khách sạn trên SQL Server. Mỗi yêu cầu đặt tối đa một phòng tại một thời điểm. Khách chọn hạng và khoảng ngày, lễ tân chọn phòng cụ thể. Nhóm giữ buồng phòng, bảo trì, kho vật tư và dịch vụ phát sinh. CSDL lưu chứng từ nội bộ bằng VND và các khoản thu mô phỏng. Đầu ra hiện tại là đặc tả, mô hình dữ liệu, lược đồ đã chuẩn hóa, từ điển dữ liệu và các script SQL triển khai.

Năm tác nhân **Khách hàng, Lễ tân, Nhân viên khách sạn, Thu ngân, Quản lý** mô tả ai tham gia từng nghiệp vụ và cần đọc hoặc cập nhật dữ liệu nào. Nhân viên khách sạn được phân công theo nhiệm vụ buồng phòng, bảo trì hoặc kho. Quản lý, lễ tân và thu ngân cũng có thể dùng hồ sơ nhân viên chung. Nhóm xác định quyền SQL Server theo thao tác cần được phép thực hiện.

## Luồng nghiệp vụ chính

1. Khách tìm theo hạng, ngày đến và ngày đi rồi gửi yêu cầu. Hệ thống hiển thị tình trạng chờ xếp phòng.
2. Lễ tân xếp phòng đúng hạng và xác nhận trong một giao dịch. CSDL kiểm tra lại lịch đặt và lịch bảo trì tại lúc ghi để chặn hai phiên xếp trùng phòng.
3. Khi nhận phòng, lễ tân mở chặng lưu trú. Nhân viên xác nhận tình trạng phòng, ghi yêu cầu bảo trì và ghi dịch vụ tính phí phát sinh.
4. Khi chuyển phòng lúc đang ở, lễ tân kết thúc chặng cũ và mở chặng mới. Hệ thống chốt hóa đơn phòng cũ, tạo hóa đơn nháp của phòng mới và giữ toàn bộ thay đổi trong cùng giao dịch SQL Server.
5. Khi trả phòng, hệ thống chốt hóa đơn chặng cuối và tạo nhiệm vụ dọn. Thu ngân thu cho một hoặc nhiều hóa đơn còn nợ, rồi phát hành hóa đơn tổng theo các khoản đã phân bổ.

Hóa đơn phòng ghi tiền của một chặng ở một phòng. Hóa đơn tổng là chứng từ của một lần thu cho một hoặc nhiều hóa đơn phòng của cùng khách trong cùng lượt lưu trú. Ví dụ, khách đổi phòng từ A sang B. A có hóa đơn 1.200.000 đồng và B có hóa đơn 900.000 đồng. Khi khách trả cả hai trong một lần, hệ thống lập một hóa đơn tổng 2.100.000 đồng, với phân bổ tương ứng 1.200.000 và 900.000 đồng. Báo cáo dùng khoản thu thực tế cho chỉ tiêu tiền đã thu để tránh cộng hai cấp chứng từ.

## Danh sách use case

| Mã | Tác nhân chính | Kết quả mong đợi |
|---|---|---|
| UC01 | Khách hàng | Tìm theo ngày và hạng, nhận danh sách hạng có phòng phù hợp và giá tham khảo |
| UC02 | Khách hàng | Gửi yêu cầu đặt, nhận mã yêu cầu và trạng thái chờ xếp phòng |
| UC03 | Khách hàng | Xem yêu cầu và lịch sử đặt của mình |
| UC04 | Khách hàng | Hủy yêu cầu hoặc đơn đủ điều kiện, giải phóng lịch nếu đã xếp |
| UC05 | Lễ tân | Xem hàng chờ và chọn phòng đúng hạng còn chỗ cho toàn kỳ |
| UC06 | Lễ tân | Xác nhận đặt phòng hoặc báo xung đột khi phòng vừa được giữ |
| UC07 | Lễ tân | Nhận phòng và mở chặng lưu trú |
| UC08 | Lễ tân | Chuyển phòng, kết thúc chặng và chốt hóa đơn cũ, mở chặng và hóa đơn mới |
| UC09 | Lễ tân | Trả phòng, chốt chặng cuối và giao việc dọn phòng |
| UC10 | Nhân viên khách sạn | Nhận và hoàn thành công việc dọn phòng theo phân quyền |
| UC11 | Nhân viên khách sạn | Mở hoặc đóng phiếu bảo trì có thời hạn chặn lịch |
| UC12 | Nhân viên khách sạn | Nhập và xuất vật tư, ghi lý do và chứng từ liên quan |
| UC13 | Nhân viên khách sạn | Ghi dịch vụ hoặc vật tư tính phí đúng chặng phòng |
| UC14 | Thu ngân | Xem bảng kê, hóa đơn từng phòng và số còn phải thu |
| UC15 | Thu ngân | Thu một phần hoặc toàn bộ nhiều hóa đơn trong cùng lượt |
| UC16 | Thu ngân | Phát hành và tra cứu hóa đơn tổng theo lần thu |
| UC17 | Quản lý | Quản lý hạng phòng, phòng, giá và danh mục dịch vụ |
| UC18 | Quản lý | Phân công nhiệm vụ nhân viên theo nhóm công việc |
| UC19 | Quản lý | Xem công suất, doanh thu đã thu và mức sử dụng vật tư |
| UC20 | Quản lý | Tra cứu nhật ký đổi trạng thái, chốt hóa đơn và thu tiền |

## Quy tắc nghiệp vụ

| Mã | Quy tắc | Chủ trì |
|---|---|---|
| BR01 | Ngày đi phải sau ngày đến. Lịch đêm dùng khoảng nửa mở, ngày đi có thể bằng ngày đến của lượt sau. | TV1–2 |
| BR02 | Yêu cầu chờ xếp phòng chưa giữ chỗ. Khách có chỗ sau khi lễ tân xác nhận thành công. | TV1–2 |
| BR03 | Khi xác nhận, phòng đúng hạng phải khả dụng liên tục cho cả kỳ. Một phòng chỉ có một lượt chiếm lịch tại mỗi thời điểm. | TV2 |
| BR04 | Mọi thao tác làm đổi lịch phòng, kể cả bảo trì chặn phòng, dùng cùng cơ chế giao dịch. Hai phiên tranh cùng phòng cho cùng kỳ chỉ một phiên thành công. | TV2–3 |
| BR05 | Chỉ nhận phòng cho đơn đã xác nhận, có phòng sẵn sàng và phù hợp điều kiện nhận. | TV2–3 |
| BR06 | Mỗi lượt có tối đa một chặng đang mở. Chặng nối tiếp phải cùng lượt và có thời điểm bàn giao hợp lệ. | TV2 |
| BR07 | Khi chuyển, phòng mới phải khác phòng cũ, sẵn sàng và trống phần lịch còn lại. Nếu một bước lỗi, giữ nguyên chặng cũ, lịch và hóa đơn. | TV2–4 |
| BR08 | Mỗi đêm chỉ được tính một lần. Bản đầu chuyển phòng trong giờ ban ngày trước giờ nhận phòng tiêu chuẩn và tính đêm ngày chuyển cho phòng mới. | TV2–4 |
| BR09 | Đơn giá phòng và dịch vụ dùng mức đã chốt cho chặng hoặc tại thời điểm ghi nhận tương ứng. Sửa giá danh mục chỉ ảnh hưởng nghiệp vụ phát sinh sau đó. | TV3–5 |
| BR10 | Trả phòng hoặc chuyển phòng tạo công việc dọn phòng cũ. Phòng phải hoàn thành dọn và không bị bảo trì để nhận khách tiếp theo. | TV2–3 |
| BR11 | Bảo trì chặn phòng trong khoảng hiệu lực. Nếu đụng lịch đã xác nhận, báo lễ tân xử lý lịch trước khi tạo lệnh chặn. | TV2–3 |
| BR12 | Nhập, xuất vật tư phải có số lượng dương và căn cứ. Xuất trong giao dịch, số lượng tồn sau xuất phải từ 0 trở lên. | TV3 |
| BR13 | Chỉ dịch vụ hoặc vật tư có đánh dấu tính phí và đã xác nhận mới xuất hiện trên hóa đơn. Vật tư nội bộ vẫn có chứng từ kho. | TV3–4 |
| BR14 | Phí phát sinh thuộc chặng đang sử dụng dịch vụ. Mỗi phát sinh được đưa vào hóa đơn một lần. | TV3–4 |
| BR15 | Mỗi chặng có tối đa một hóa đơn phòng. Hóa đơn nháp có thể cập nhật. CSDL bảo vệ các dòng tiền của hóa đơn đã chốt khỏi sửa trực tiếp. | TV4 |
| BR16 | Khoản thu dương, phân bổ đúng khách và lượt. Tổng phân bổ bằng khoản thu và không vượt nợ từng hóa đơn. Lần gửi lại cùng mã giao dịch không thu lặp. | TV4 |
| BR17 | Hóa đơn tổng giữ các phân bổ của lần thu. Tiền đã thu chỉ tính một lần trong báo cáo, kể cả khi hóa đơn phòng có nhiều lần thu. | TV4–5 |
| BR18 | Khách chỉ đọc hoặc hủy đơn của mình. Chỉ đơn chờ xếp hoặc xác nhận mà chưa nhận phòng và chưa có khoản thu mới được khách hủy trong bản đầu. | TV1–2 |
| BR19 | Nhân viên thực hiện công việc theo quyền được giao. Các thao tác nhạy cảm lưu người, thời điểm và thông tin thay đổi cần kiểm toán. | TV3–5 |
| BR20 | Truy vấn tìm phòng tính từ lịch đặt và bảo trì đã commit trong SQL Server. Sau mỗi thay đổi ảnh hưởng lịch, kết quả truy vấn phản ánh trạng thái mới. | TV1–2–5 |

## Tình huống dùng để đối chiếu khi vẽ ERD

Các tình huống dưới đây mô tả dữ liệu và kết quả mong đợi để chốt quy tắc trước khi thiết kế.

| Ca | Đầu vào | Kết quả |
|---|---|---|
| AC01 · Đặt và xếp phòng | Hạng Deluxe, từ 1 đến 3 tháng 12. Hai lễ tân thử gán cùng phòng trong hai phiên SQL song song. | Một xác nhận thành công. Yêu cầu còn lại vẫn chờ xếp và nhận thông báo xung đột. |
| AC02 · Biên ngày và bảo trì | Phòng có đơn [1, 3) và bảo trì [4, 5). | [3, 4) hợp lệ, [2, 4) và [3, 5) xung đột. |
| AC03 · Chuyển phòng | Khách ở A, lễ tân chuyển sang B vào ban ngày 2 tháng 12. | A chốt đêm 1 tháng 12, B chịu đêm 2 tháng 12, dữ liệu chuyển cùng lúc với hai hóa đơn phòng. |
| AC04 · Hoàn tác khi chuyển | Tạo lỗi giả lập ở bước mở hóa đơn B hoặc có phiên khác chiếm B. | Chặng A và hóa đơn A giữ nguyên trạng trước khi chuyển. |
| AC05 · Kho và dịch vụ | Xuất một vật tư dọn phòng và giao một dịch vụ tính phí. | Cả hai có nghiệp vụ tương ứng. Bảng kê phòng chỉ có dịch vụ tính phí. |
| AC06 · Thu nhiều hóa đơn | Hai hóa đơn 1.200.000 và 900.000 đồng. Thu 1.500.000 lần đầu rồi thu 600.000 lần sau. | Hai lần thu có chứng từ tổng tương ứng. Nợ cuối bằng 0, tổng tiền thu 2.100.000, gửi lại mã lần đầu không tạo khoản thu mới. |
| AC07 · Tra cứu sau khi xác nhận và hủy | Một hạng còn đúng một phòng phù hợp. Lễ tân xác nhận đặt phòng đó, sau đó hủy đơn hợp lệ. | Sau khi xác nhận, truy vấn trả về hết phòng cho kỳ đó. Sau khi hủy, truy vấn hiển thị có phòng trở lại nếu không còn lịch chặn khác. |

Đặc tả ban đầu dùng giờ khách sạn 14:00 nhận phòng và 12:00 trả phòng theo Asia/Ho_Chi_Minh. Giả định một lượt lưu trú cho mỗi chứng từ tổng, hóa đơn nội bộ và quy tắc tính đêm chuyển phòng cần được cả nhóm duyệt trước khi tạo migration nghiệp vụ.
