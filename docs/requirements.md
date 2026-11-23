# Đặc tả đặt phòng khách sạn

## Phạm vi

Nhóm thiết kế CSDL cho một khách sạn trên SQL Server. Một lượt lưu trú nhóm các đơn thuộc cùng một khách hàng trong một kỳ thuê liên tiếp. Các đơn trong cùng lượt có thể trùng ngày. Mỗi đơn dành cho một phòng tại một thời điểm, có lịch đặt, trạng thái và khoản cọc riêng. Khách chọn hạng và khoảng ngày, lễ tân chọn phòng cụ thể cho từng đơn. Nhóm giữ buồng phòng, bảo trì, kho vật tư và dịch vụ phát sinh. CSDL lưu chứng từ nội bộ bằng VND và các khoản thu mô phỏng. Đầu ra hiện tại là đặc tả, mô hình dữ liệu, lược đồ đã chuẩn hóa, từ điển dữ liệu và các script SQL triển khai.

Năm tác nhân **Khách hàng, Lễ tân, Nhân viên khách sạn, Thu ngân, Quản lý** mô tả ai tham gia từng nghiệp vụ và cần đọc hoặc cập nhật dữ liệu nào. Nhân viên khách sạn được phân công theo nhiệm vụ buồng phòng, bảo trì hoặc kho. Quản lý, lễ tân và thu ngân cũng có thể dùng hồ sơ nhân viên chung. Nhóm xác định quyền SQL Server theo thao tác cần được phép thực hiện.

## Luồng nghiệp vụ chính

1. Khách tìm theo hạng, ngày đến và ngày đi rồi gửi yêu cầu. Đơn chờ xếp phòng.
2. Lễ tân chọn phòng còn trống cho toàn bộ kỳ ở và tạo lượt giữ **30 phút**. Đơn chuyển sang chờ khách xác nhận. Khi khách đồng ý, đơn chờ lễ tân xác nhận cuối. Lượt giữ tiếp tục tới khi xác nhận thành công hoặc hết hạn. CSDL kiểm tra lại lịch đặt, giữ tạm và bảo trì tại lúc ghi.
3. Lễ tân xác nhận đặt ngay khi khách đã đồng ý và đủ cọc. Với đơn miễn cọc, lễ tân xác nhận sau khi khách đồng ý. Xác nhận thành công chuyển lượt giữ thành lịch đặt cho cả kỳ và ghi ngày, giờ check-in đã thông báo.
4. Trước ngày đến, khách có thể yêu cầu đổi hoặc hủy theo chính sách cọc. Khi khách đến muộn, lễ tân ghi kết quả liên hệ để quyết định giữ phòng tới giờ đến mới, nhận phòng từ xa hoặc đóng đơn do khách không đến.
5. Lễ tân check-in theo từng đơn, ghi thời điểm và hình thức nhận rồi mở chặng tính tiền cho đơn đó. Nhân viên ghi phí dịch vụ, đồ ăn, thức uống và các vật tư tính phí vào chặng thực tế sử dụng. Khi có sự cố, vận hành ghi nhận, lễ tân đề xuất đổi phòng và lấy xác nhận của khách, quản lý quyết định cách xử lý và duyệt bồi thường.
6. Khi chuyển phòng lúc đang ở, lễ tân giữ nguyên đơn và khoản cọc, kết thúc chặng cũ rồi mở chặng mới. CSDL chốt hóa đơn cũ và mở hóa đơn nháp cho chặng mới trong cùng giao dịch. Các đơn khác trong lượt tiếp tục theo lịch riêng. Với gia hạn ở cùng phòng, chặng tính tiền mới bắt đầu ở cuối kỳ cũ.
7. Khi khách yêu cầu trả một phòng, lễ tân chốt các chi phí của đơn đó và thu ngân đối soát cọc, khoản thu và công nợ. Lễ tân có thể hoàn tất check-out cho đơn đã hết nợ trong khi các đơn khác vẫn đang ở. Nếu trả hoặc thanh toán nhiều phòng cùng lúc, thu ngân có thể thu chung.

Hóa đơn phòng ghi tiền của một chặng, gồm tiền phòng và các phí phát sinh thuộc chặng. Hóa đơn tổng thể hiện số tiền trả cho một hoặc nhiều hóa đơn phòng của cùng khách trong cùng lượt. Các hóa đơn phòng có thể thuộc nhiều chặng hoặc nhiều đơn. Ví dụ, khách trả hai phòng cùng lúc. Hóa đơn A là 1.200.000 đồng, cọc được cấn 300.000 đồng. Hóa đơn B là 900.000 đồng, cọc được cấn 200.000 đồng. Hóa đơn tổng thể hiện chi phí 2.100.000 đồng, cấn cọc 500.000 đồng và số tiền thu thêm 1.600.000 đồng. Báo cáo tiền thực thu ghi cọc ở lúc nhận cọc và ghi phần thu thêm ở lúc thanh toán.

### Lịch phòng và tình trạng sử dụng

- Lượt giữ 30 phút và đơn đã xác nhận đều chặn kết quả tìm phòng trong khoảng ngày bị trùng. Xác nhận đặt chuyển lượt giữ thành lịch đặt chính thức.
- Phòng chuyển sang đang sử dụng khi khách check-in trực tiếp hoặc từ xa. Khi khách đổi hoặc trả phòng, ghi thời điểm kết thúc sử dụng và tạo việc dọn. Phòng sẵn sàng giao sau khi dọn xong nếu không còn bảo trì.
- Ví dụ, đơn 03/11–05/11 chiếm hai đêm 03 và 04/11. Truy vấn cho kỳ bắt đầu 06/11 có thể trả về phòng đó nếu không có lịch chặn khác. Nếu giao phòng ngày 05/11, lễ tân kiểm tra thêm tình trạng trả và dọn phòng thực tế.

## Chính sách tiền cọc và thời hạn

| Tình huống | Cách xử lý |
|---|---|
| Đơn ngày thường được miễn cọc | Ở tối đa hai đêm **hoặc** đặt trước ngày đến một đến hai ngày theo lịch khách sạn |
| Đơn ngày thường cần cọc | Thu **30% tổng giá phòng của tất cả các đêm đã báo cho khách** |
| Đơn có đêm thuộc dịp lễ | Bắt buộc cọc **80% tổng giá phòng của tất cả các đêm đã báo cho khách**, kể cả đơn ngắn hoặc đặt sát ngày |
| Khách đến, sử dụng phòng bình thường | Cấn số cọc đã thu vào số tiền phải thanh toán |
| Khách hủy đơn ngày thường trước check-in từ 48 giờ trở lên | Hoàn toàn bộ cọc đã thu |
| Khách hủy đơn ngày thường trước check-in từ 24 giờ đến dưới 48 giờ | Hoàn một nửa cọc đã thu |
| Khách hủy đơn ngày thường khi còn dưới 24 giờ | Ghi nhận hủy và giải phóng lịch. Giữ toàn bộ cọc đã thu. |
| Khách đổi đơn ngày thường | Yêu cầu trước check-in ít nhất 24 giờ. Chỉ cập nhật khi có phòng phù hợp, khách xác nhận phương án mới và khoản cọc đã được đối soát. Nếu phương án mới chưa được xác nhận, giữ lịch đã đặt. |
| Khách yêu cầu đổi phòng vào dịp lễ | Đổi khi có phòng phù hợp và khách xác nhận lại. Nếu khách hủy vì lý do của mình hoặc quyết định không đến khi không có phòng phù hợp để đổi theo yêu cầu, giữ toàn bộ cọc. |
| Khách sạn không giao được phòng đã đặt | Ưu tiên đề xuất phòng cùng hạng và xin xác nhận. Hai bên phải thống nhất nếu đổi hạng. Nếu khách đồng ý nâng hạng do lỗi khách sạn, giữ giá đã chốt. Nếu không có phương án khách chấp nhận, hoàn toàn bộ cọc kể cả ngày lễ. Vào dịp lễ, ghi nhận và hỗ trợ voucher hoặc phương án bồi thường được duyệt khi lỗi thuộc khách sạn. |
| Khách trả sớm | Đơn tính theo đêm tính các đêm đã sử dụng. Cấn cọc vào số phải trả và giữ phần cọc dư. Gói đã trả trước giữ giá gói. Giải phóng lịch phòng còn lại. |

Tiền cọc ghi theo đơn và lần nhận tiền. Khi xử lý cọc, ghi số đã cấn, đã hoàn hoặc giữ lại cùng lý do. Tổng các phần đã xử lý không vượt số thực nhận. Cấn tiền cọc vào hóa đơn là sử dụng tiền đã thu để giảm công nợ. Báo cáo tiền thực thu và hoàn tiền dựa trên giao dịch tiền, còn voucher ghi theo phương án bồi thường đã duyệt.

## Danh sách use case

| Mã | Tác nhân chính | Kết quả mong đợi |
|---|---|---|
| UC01 | Khách hàng | Tìm theo ngày và hạng, nhận danh sách hạng có phòng phù hợp và giá tham khảo |
| UC02 | Khách hàng | Gửi một hoặc nhiều đơn trong cùng lượt, mỗi đơn có mã và trạng thái chờ xếp riêng |
| UC03 | Khách hàng | Xem yêu cầu và lịch sử đặt của mình |
| UC04 | Khách hàng | Hủy yêu cầu hoặc đơn đủ điều kiện, giải phóng lịch nếu đã xếp |
| UC05 | Lễ tân | Xem hàng chờ, chọn phòng đúng hạng và giữ phòng tạm cho cả kỳ trong 30 phút |
| UC06 | Lễ tân | Xác nhận đặt khi khách đã đồng ý và đáp ứng điều kiện cọc, rồi ghi ngày giờ nhận phòng đã thông báo |
| UC07 | Lễ tân | Nhận phòng trực tiếp hoặc từ xa và mở chặng lưu trú |
| UC08 | Lễ tân | Chuyển phòng trong cùng đơn, chốt chặng và hóa đơn cũ rồi mở chặng và hóa đơn mới |
| UC09 | Lễ tân | Chốt chặng cuối của đơn, hoàn tất trả phòng khi đơn hết công nợ và giao việc dọn phòng |
| UC10 | Nhân viên khách sạn | Nhận và hoàn thành công việc dọn phòng theo phân quyền |
| UC11 | Nhân viên khách sạn | Ghi sự cố, cập nhật việc bảo trì và thời hạn chặn lịch theo phương án xử lý |
| UC12 | Nhân viên khách sạn | Nhập và xuất vật tư, ghi lý do và chứng từ liên quan |
| UC13 | Nhân viên khách sạn | Ghi dịch vụ, đồ ăn, thức uống hoặc vật tư tính phí vào đúng chặng phòng |
| UC14 | Thu ngân | Xem bảng kê, hóa đơn từng phòng và số còn phải thu |
| UC15 | Thu ngân | Thu riêng hoặc thu chung cho các hóa đơn của nhiều đơn trong cùng lượt, đối soát cọc từng đơn |
| UC16 | Thu ngân | Phát hành và tra cứu hóa đơn tổng theo lần thu |
| UC17 | Quản lý | Quản lý hạng phòng, phòng, giá và danh mục dịch vụ |
| UC18 | Quản lý | Phân công nhiệm vụ nhân viên theo nhóm công việc |
| UC19 | Quản lý | Xem công suất, doanh thu đã thu và mức sử dụng vật tư |
| UC20 | Quản lý | Tra cứu nhật ký đổi trạng thái, chốt hóa đơn và thu tiền |
| UC21 | Khách hàng | Xác nhận phòng được đề xuất hoặc yêu cầu sửa ngày, hạng hoặc phòng trước khi đến |
| UC22 | Thu ngân | Ghi nhận, hoàn, cấn trừ hoặc ghi giữ cọc theo kết quả của đơn |
| UC23 | Lễ tân | Ghi lịch sử liên hệ, xử lý đến muộn và hủy vì khách không đến |
| UC24 | Lễ tân | Đề xuất phòng thay thế trước khi giao và ghi xác nhận của khách |
| UC25 | Lễ tân | Xử lý gia hạn hoặc trả sớm, cập nhật lịch và các chặng tính tiền |
| UC26 | Quản lý | Quyết định phương án xử lý sự cố và duyệt voucher hoặc bồi thường khi lỗi thuộc khách sạn |
| UC27 | Quản lý | Điều chỉnh khoản ghi sai hoặc giao quyền điều chỉnh cho trưởng bộ phận, có thông tin kiểm toán |

## Quy tắc nghiệp vụ

| Mã | Quy tắc | Chủ trì |
|---|---|---|
| BR01 | Ngày đi phải sau ngày đến. Lịch đêm dùng khoảng nửa mở, ngày đi có thể bằng ngày đến của lượt sau. | TV1–2 |
| BR02 | Yêu cầu chờ xếp phòng chưa giữ chỗ. Lượt giữ tạm chặn phòng cho kỳ đã chọn đến hạn 30 phút, tới khi hủy hoặc tới khi chuyển thành lịch đặt chính thức. Từ thời điểm hết hạn, lượt giữ không còn chặn lịch. | TV1–2 |
| BR03 | Khi giữ hoặc xác nhận, phòng phải phù hợp với hạng đã được khách chấp nhận và còn chỗ cho toàn kỳ. Khi xác nhận phải kiểm tra lại lịch và chuyển chính lượt giữ của đơn thành lịch đặt trong cùng giao dịch. | TV2 |
| BR04 | Mọi thao tác làm đổi lịch phòng dùng cùng cơ chế giao dịch. Hai phiên tranh cùng phòng và kỳ chỉ một phiên giữ thành công. Trong hàng chờ, lễ tân có thể ưu tiên đơn ở lâu hơn trước khi giữ phòng và báo kết quả cho khách. | TV2–3 |
| BR05 | Chỉ nhận phòng cho đơn đã xác nhận, có phòng sẵn sàng và phù hợp điều kiện nhận. | TV2–3 |
| BR06 | Mỗi đơn có tối đa một chặng đang mở. Chặng nối tiếp thuộc cùng đơn và có thời điểm bàn giao hợp lệ. Các đơn khác nhau trong cùng lượt có thể có chặng đang mở đồng thời. | TV2 |
| BR07 | Khi chuyển, phòng mới phải khác phòng cũ, sẵn sàng và trống phần lịch còn lại. Việc chuyển giữ nguyên mã đơn và tiền cọc, chỉ đổi phòng theo chặng. Nếu một bước lỗi, giữ nguyên chặng cũ, lịch và hóa đơn. | TV2–4 |
| BR08 | Trong một đơn, mỗi đêm chỉ được tính cho một chặng. Bản đầu chuyển phòng trong giờ ban ngày trước giờ nhận phòng tiêu chuẩn và tính đêm ngày chuyển cho phòng mới. Nếu khách thuê hai phòng bằng hai đơn, mỗi đơn có tiền phòng riêng cho cùng đêm. | TV2–4 |
| BR09 | Đơn giá phòng và dịch vụ dùng mức đã chốt cho chặng hoặc tại thời điểm ghi nhận tương ứng. Sửa giá danh mục chỉ ảnh hưởng nghiệp vụ phát sinh sau đó. | TV3–5 |
| BR10 | Trả phòng hoặc chuyển phòng tạo công việc dọn phòng cũ. Phòng phải hoàn thành dọn và không bị bảo trì để nhận khách tiếp theo. | TV2–3 |
| BR11 | Bảo trì chặn phòng trong khoảng hiệu lực. Nếu đụng lượt giữ đang hiệu lực hoặc lịch đã xác nhận, báo lễ tân xử lý lượt giữ hoặc đơn bị ảnh hưởng. | TV2–3 |
| BR12 | Nhập, xuất vật tư phải có số lượng dương và căn cứ. Xuất trong giao dịch, số lượng tồn sau xuất phải từ 0 trở lên. | TV3 |
| BR13 | Chỉ dịch vụ hoặc vật tư có đánh dấu tính phí và đã xác nhận mới xuất hiện trên hóa đơn. Vật tư nội bộ vẫn có chứng từ kho. | TV3–4 |
| BR14 | Phí dịch vụ, đồ ăn, thức uống và vật tư tính phí thuộc chặng của phòng đã sử dụng. Mỗi phát sinh được đưa vào hóa đơn một lần. | TV3–4 |
| BR15 | Mỗi chặng có tối đa một hóa đơn phòng. Hóa đơn nháp có thể cập nhật. CSDL bảo vệ các dòng tiền của hóa đơn đã chốt khỏi sửa trực tiếp. | TV4 |
| BR16 | Khoản thu dương và có thể phân bổ cho hóa đơn của nhiều đơn cùng khách, cùng lượt. Tổng phân bổ tiền thu bằng khoản thu và không vượt nợ từng hóa đơn sau cấn cọc. Lần gửi lại cùng mã giao dịch không thu lặp. | TV4 |
| BR17 | Hóa đơn tổng thể hiện các hóa đơn được thanh toán, số cọc cấn theo từng đơn và số tiền thu thêm. Tiền đã thu chỉ tính một lần trong báo cáo, kể cả khi hóa đơn phòng được trả qua nhiều lần thu. | TV4–5 |
| BR18 | Khách chỉ đọc, yêu cầu đổi hoặc hủy đơn của mình trước khi nhận phòng. Khi đóng đơn, áp dụng chính sách cọc tương ứng và giải phóng lịch hoặc lượt giữ còn lại. Khách đã nhận phòng đi theo luồng trả sớm. | TV1–2–4 |
| BR19 | Nhân viên thực hiện công việc theo quyền được giao. Các thao tác nhạy cảm lưu người, thời điểm và thông tin thay đổi cần kiểm toán. | TV3–5 |
| BR20 | Truy vấn tìm phòng tính từ lịch đặt, lượt giữ chưa hết hạn và lịch bảo trì trong SQL Server. Sau khi ghi và commit thay đổi ảnh hưởng lịch hoặc khi một lượt giữ hết hạn, lần tìm phòng tiếp theo phản ánh trạng thái mới. | TV1–2–5 |
| BR21 | Lễ tân xác nhận ngay khi có xác nhận của khách và đạt mức cọc đã báo theo chính sách. Đơn miễn cọc chỉ cần xác nhận của khách và kiểm tra lại lịch. Lưu ngày giờ nhận phòng được thông báo. | TV1–2–4 |
| BR22 | Mức cọc tính trên tổng giá phòng đã báo của cả kỳ. Ngày thường thu 30% khi không thuộc diện miễn cọc. Kỳ có đêm lễ thu 80% và áp dụng chính sách lễ. | TV2–4–5 |
| BR23 | Phần đã hoàn, cấn trừ và giữ lại được ghi riêng theo khoản cọc của từng đơn. Tổng các phần không vượt tiền đã nhận. Cọc giảm công nợ của chính đơn đó. Khi trả chung, hóa đơn tổng thể hiện từng khoản cọc được cấn mà không phát sinh lần thu mới. | TV4–5 |
| BR24 | Ngày thường, hoàn đủ cọc nếu hủy trước ít nhất 48 giờ, hoàn nửa nếu còn từ 24 đến dưới 48 giờ và giữ toàn bộ nếu còn dưới 24 giờ. Yêu cầu đổi lịch phải trước check-in ít nhất 24 giờ và khách xác nhận lại. | TV1–2–4 |
| BR25 | Ngày lễ, khách chỉ được hỗ trợ đổi phòng theo nhu cầu nếu còn phòng phù hợp và khách xác nhận lại. Nếu khách chủ động hủy hoặc quyết định không đến, giữ toàn bộ cọc. Trường hợp lỗi khách sạn áp dụng BR29. | TV1–2–4 |
| BR26 | Tính đến muộn từ giờ nhận phòng chuẩn của ngày đến. Nếu sau 6 giờ vẫn không liên lạc được, lễ tân ghi no-show, giải phóng lịch và giữ cọc đã thu. Nếu liên lạc được và khách báo đến muộn, ghi giờ hẹn trong giới hạn 12 giờ từ giờ chuẩn. Nếu khách chưa nhận phòng khi hết 12 giờ, xử lý no-show. | TV2–4 |
| BR27 | Check-in từ xa chỉ thực hiện khi khách đồng ý. Ghi giờ thực hiện và mở chặng lưu trú như nhận trực tiếp. Đơn đã check-in từ xa được tính phí bình thường và không thuộc diện no-show. | TV2–4 |
| BR28 | Nếu tiền cọc đến khi lượt giữ đã hết hạn, kiểm tra lại khả dụng trước khi xác nhận. Nếu phòng không còn, đề xuất phòng khác để khách đồng ý hoặc hoàn khoản đã nhận. Khoản cọc đến trễ không làm sống lại lượt giữ đã hết hạn. | TV2–4 |
| BR29 | Nếu khách sạn không giao được phòng, ưu tiên phòng cùng hạng. Khách phải xác nhận phương án thay thế, kể cả khi cùng hạng. Nâng hạng do lỗi khách sạn giữ nguyên giá đã chốt. Nếu không có phương án được chấp nhận, hoàn toàn bộ cọc. Ngày lễ ghi nhận thêm voucher hoặc bồi thường do quản lý duyệt khi lỗi thuộc khách sạn. | TV2–4–5 |
| BR30 | Gia hạn kiểm tra khả dụng của phần kỳ mới trước khi ghi. Kỳ gia hạn có chặng tính tiền và hóa đơn riêng, kể cả khi tiếp tục ở cùng phòng. Giữ nguyên kỳ đã đặt nếu gia hạn không thành công. | TV2–4 |
| BR31 | Trả sớm giải phóng phần lịch còn lại. Đơn thường tính các đêm đã sử dụng và giữ phần cọc còn dư sau cấn trừ. Gói đã trả trước giữ nguyên giá gói. | TV2–4 |
| BR32 | Lễ tân chỉ hoàn tất trả phòng sau khi chốt chi phí và số còn phải thu của đơn đang trả bằng 0. Việc hoàn tất đóng chặng cuối và tạo việc dọn cho phòng đó. Các đơn khác trong cùng lượt xử lý theo công nợ và thời điểm trả riêng. | TV2–3–4 |
| BR33 | Chỉ quản lý hoặc trưởng bộ phận được giao quyền được điều chỉnh khoản ghi sai. Với hóa đơn đã chốt, ghi điều chỉnh có lý do và người duyệt để giữ được số liệu gốc và lịch sử. | TV3–4–5 |
| BR34 | Một lượt có thể nhóm nhiều đơn cùng khách với các kỳ chồng hoặc nối tiếp trong cùng đợt lưu trú. Mỗi đơn giữ lịch, cọc, trạng thái và các chặng riêng. Khi một đơn bị hủy hoặc no-show, các đơn khác tiếp tục theo lịch riêng. | TV1–2–4 |
| BR35 | Đơn đã đặt chặn lịch cho kỳ đã xác nhận. Phòng chuyển sang đang sử dụng từ lúc check-in trực tiếp hoặc từ xa và kết thúc khi khách chuyển hoặc trả phòng. Lễ tân kiểm tra tình trạng sử dụng, dọn phòng và bảo trì trước khi giao phòng. | TV2–3 |
| BR36 | Vận hành ghi nhận sự cố. Lễ tân liên hệ khách và ghi xác nhận nếu cần đổi phòng. Quản lý xử lý sự cố và duyệt bồi thường. Nhật ký phải chỉ ra ai làm từng thao tác. | TV2–3–5 |

## Tình huống dùng để đối chiếu khi vẽ ERD

Các tình huống dưới đây mô tả dữ liệu và kết quả mong đợi để chốt quy tắc trước khi thiết kế.

| Ca | Đầu vào | Kết quả |
|---|---|---|
| AC01 · Tranh lượt giữ phòng | Hạng Deluxe, từ 1 đến 3 tháng 12. Hai lễ tân thử giữ cùng phòng trong hai phiên SQL song song. | Một lượt giữ thành công. Yêu cầu còn lại vẫn chờ xếp và lễ tân được báo xung đột trước khi thông báo phòng cho khách. |
| AC02 · Biên ngày và bảo trì | Phòng có đơn [1, 3) và bảo trì [4, 5). | [3, 4) hợp lệ, [2, 4) và [3, 5) xung đột. |
| AC03 · Chuyển phòng | Khách ở A, lễ tân chuyển sang B vào ban ngày 2 tháng 12. | A chốt đêm 1 tháng 12, B chịu đêm 2 tháng 12, dữ liệu chuyển cùng lúc với hai hóa đơn phòng. |
| AC04 · Hoàn tác khi chuyển | Tạo lỗi giả lập ở bước mở hóa đơn B hoặc có phiên khác chiếm B. | Chặng A và hóa đơn A giữ nguyên trạng trước khi chuyển. |
| AC05 · Kho và dịch vụ | Xuất một vật tư dọn phòng và giao một dịch vụ tính phí. | Cả hai có nghiệp vụ tương ứng. Bảng kê phòng chỉ có dịch vụ tính phí. |
| AC06 · Thu nhiều hóa đơn | Hai hóa đơn 1.200.000 và 900.000 đồng. Thu 1.500.000 lần đầu rồi thu 600.000 lần sau. | Hai lần thu có chứng từ tổng tương ứng. Nợ cuối bằng 0, tổng tiền thu 2.100.000, gửi lại mã lần đầu không tạo khoản thu mới. |
| AC07 · Tra cứu sau khi xác nhận và hủy | Một hạng còn đúng một phòng phù hợp. Lễ tân xác nhận đặt phòng đó, sau đó hủy đơn hợp lệ. | Sau khi xác nhận, truy vấn trả về hết phòng cho kỳ đó. Sau khi hủy, truy vấn hiển thị có phòng trở lại nếu không còn lịch chặn khác. |
| AC08 · Hết hạn giữ | Lượt giữ bắt đầu lúc 10:00. Khách đồng ý nhưng đến 10:30 chưa đủ cọc. | Phòng khả dụng trở lại từ 10:30 nếu không có lịch chặn khác. Cọc đến sau hạn phải qua bước kiểm tra và xử lý lại theo BR28. |
| AC09 · Mức cọc | Đơn đủ điều kiện miễn cọc. Đơn ngày thường không miễn có giá 3.000.000 đồng. Đơn cùng giá có đêm lễ. | Mức cọc lần lượt là 0, 900.000 và 2.400.000 đồng. |
| AC10 · Mốc hủy ngày thường | Ba đơn cùng đã cọc 900.000 đồng. Khách hủy lần lượt vào đúng 48 giờ, đúng 24 giờ và còn 23 giờ 59 phút trước check-in. | Hoàn lần lượt 900.000, 450.000 và 0 đồng. Lịch được giải phóng khi đơn đóng. |
| AC11 · Khách đến muộn | Giờ nhận chuẩn 14:00. Một đơn không liên lạc được đến 20:00. Một đơn có liên hệ và hẹn đến lúc 01:00. Một khách đồng ý nhận từ xa. | Đơn đầu đóng theo no-show. Đơn thứ hai ghi giờ hẹn và được giữ đến tối đa 02:00 hôm sau. Đơn thứ ba mở chặng lúc nhận từ xa. |
| AC12 · Phòng hỏng dịp lễ | Phòng đã đặt bị hỏng. Khách sạn đề xuất hạng cao hơn, giữ giá cũ, nhưng khách không đồng ý. | Không đổi phòng khi chưa có xác nhận. Hoàn toàn bộ cọc và ghi voucher hoặc bồi thường được duyệt. |
| AC13 · Gia hạn cùng phòng | Khách ở phòng A từ 03/11 đến 05/11 và được duyệt ở tiếp tới 07/11. | Chặng thứ hai bắt đầu ngày 05/11, có hóa đơn riêng. Hai hóa đơn cùng lượt được thanh toán chung nếu khách chọn. |
| AC14 · Trả sớm và cọc dư | Đơn tính theo đêm. Đến lúc trả sớm, phí cho kỳ đã sử dụng là 600.000 đồng, cọc còn 800.000 đồng. | Cấn 600.000 đồng, giữ 200.000 đồng và giải phóng phần lịch còn lại. Đủ điều kiện check-out nếu không còn công nợ khác. |
| AC15 · Kiểm tra công nợ khi trả phòng | Đơn đang trả còn nợ 100.000 đồng sau cấn cọc. Thu ngân ghi khoản thu hợp lệ đủ 100.000 đồng. | Lần đầu chưa được hoàn tất check-out cho đơn đó. Sau khi ghi thu, đơn hết nợ nên lễ tân có thể hoàn tất trả phòng. |
| AC16 · Hai phòng cùng kỳ | Một khách có hai đơn A và B từ 03/11 đến 05/11. Cả hai đã xác nhận. A no-show, B check-in. | Chỉ A bị hủy và xử lý cọc. B vẫn có lịch riêng và mở chặng sử dụng. Với kỳ bắt đầu 06/11, hệ thống tiếp tục xét các lượt giữ, đơn khác và bảo trì. |
| AC17 · Chuyển một trong hai phòng | Khách đang ở A và B cùng lượt. Phòng A hỏng và khách đồng ý chuyển A sang C. | Vận hành ghi sự cố. Lễ tân giữ nguyên đơn và cọc của A, chốt chặng A rồi mở chặng C. Đơn, chặng và cọc của B giữ nguyên. Quản lý lưu phương án xử lý và duyệt bồi thường nếu áp dụng. |
| AC18 · Trả phòng khác giờ | A hết công nợ. B còn nợ và vẫn đang ở. | A có thể check-out và được giao dọn. B chỉ check-out khi công nợ của B về 0. |
| AC19 · Gộp thanh toán hai phòng | Hai đơn cùng lượt có hóa đơn 1.200.000 và 900.000 đồng. Cọc được cấn trên mỗi đơn lần lượt là 300.000 và 200.000 đồng. | Hóa đơn tổng ghi chi phí 2.100.000 đồng, cấn cọc 500.000 đồng và thu thêm 1.600.000 đồng. Công nợ hai đơn về 0 sau khi ghi đủ phần thu thêm. |

Giờ chuẩn dùng trong đặc tả là 14:00 nhận phòng và 12:00 trả phòng theo Asia/Ho_Chi_Minh. Khoảng 03/11–05/11 gồm hai đêm 03 và 04/11. Khi thiết kế, nhóm ghi rõ nguồn lịch ngày lễ, điều kiện áp dụng giá đã chốt và quy tắc làm tròn tiền VND.
