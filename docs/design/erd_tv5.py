"""Sinh ERD phan Quan ly (TV5) dang SVG, ky hieu chan qua (crow's foot)."""
import sys
from xml.sax.saxutils import escape

W, H = 2280, 1440
HEAD, ROW, PAD = 40, 26, 14
BOXW = 310
NAVY, GREY = "#1b3a5c", "#7d8a99"
LINE = "#2b3440"
FONT = "DejaVu Sans, sans-serif"

C = [60, 520, 980, 1440, 1900]
R1, R2, R3 = 110, 480, 910

# (ten, x, y, loai: core/edge, [(khoa, cot)])
E = {
    "DIP_LE": (C[0], R1, "core", [
        ("PK", "ma_dip_le"), ("", "ten_dip_le"), ("", "tu_ngay"),
        ("", "den_ngay"), ("", "ty_le_coc"), ("", "ghi_chu")]),
    "BANG_GIA_HANG": (C[1], R1, "core", [
        ("PK", "ma_bang_gia"), ("FK", "ma_hang"), ("FK", "ma_dip_le"),
        ("", "hieu_luc_tu"), ("", "hieu_luc_den"), ("", "gia_moi_dem")]),
    "HANG_PHONG": (C[2], R1, "core", [
        ("PK", "ma_hang"), ("UK", "ten_hang"), ("", "gia_niem_yet"),
        ("", "suc_chua_toi_da"), ("", "trang_thai")]),
    "PHONG": (C[3], R1, "core", [
        ("PK", "ma_phong"), ("FK", "ma_hang"), ("UK", "so_phong"), ("", "tang")]),
    "DICH_VU (TV3/TV5)": (C[4], R1, "core", [
        ("PK", "ma_dich_vu"), ("", "ten_dich_vu"), ("", "don_vi_tinh"),
        ("", "tinh_phi"), ("", "don_gia_hien_hanh")]),
    "VAI_TRO": (C[0], R2, "core", [
        ("PK", "ma_vai_tro"), ("UK", "ten_vai_tro"), ("", "nhom_cong_viec"),
        ("UK", "ten_role_sql"), ("", "mo_ta")]),
    "PHAN_CONG": (C[1], R2, "core", [
        ("PK", "ma_phan_cong"), ("FK", "ma_nhan_vien"), ("FK", "ma_vai_tro"),
        ("FK", "ma_nguoi_giao"), ("", "tu_ngay"), ("", "den_ngay"),
        ("", "quyen_dieu_chinh")]),
    "NHAN_VIEN": (C[2], R2, "core", [
        ("PK", "ma_nhan_vien"), ("FK", "ma_quan_ly"), ("", "ho_ten"),
        ("UK", "so_dien_thoai"), ("UK", "sql_login"), ("", "trang_thai")]),
    "DIEU_CHINH_HOA_DON": (C[3], R2, "core", [
        ("PK", "ma_dieu_chinh"), ("FK", "ma_hoa_don_phong"), ("FK", "ma_nguoi_lap"),
        ("FK", "ma_nguoi_duyet"), ("", "so_tien_dieu_chinh"), ("", "ly_do"),
        ("", "thoi_diem_lap"), ("", "thoi_diem_duyet"), ("", "trang_thai")]),
    "NHAT_KY_KIEM_TOAN": (C[4], R2, "core", [
        ("PK", "ma_nhat_ky"), ("FK", "ma_nhan_vien"), ("", "sql_login"),
        ("", "ten_bang"), ("", "ma_ban_ghi"), ("", "thao_tac"),
        ("", "gia_tri_cu"), ("", "gia_tri_moi"), ("", "thoi_diem")]),
    "SU_CO (TV3)": (C[0], R3, "edge", [
        ("PK", "ma_su_co"), ("FK", "ma_phong"), ("FK", "ma_chang"),
        ("FK", "ma_nhan_vien"), ("", "mo_ta"), ("", "trang_thai")]),
    "QUYET_DINH_SU_CO": (C[1], R3, "core", [
        ("PK", "ma_quyet_dinh"), ("FK,UK", "ma_su_co"), ("FK", "ma_quan_ly"),
        ("", "phuong_an"), ("", "noi_dung"), ("", "thoi_diem_quyet_dinh")]),
    "BOI_THUONG": (C[2], R3, "core", [
        ("PK", "ma_boi_thuong"), ("FK", "ma_don"), ("FK", "ma_quyet_dinh"),
        ("FK", "ma_nguoi_duyet"), ("", "hinh_thuc"), ("", "gia_tri"),
        ("", "ly_do"), ("", "thoi_diem_duyet"), ("", "trang_thai")]),
    "DON_DAT_PHONG (TV2)": (C[3], R3, "edge", [
        ("PK", "ma_don"), ("FK", "ma_luot"), ("FK", "ma_hang"),
        ("FK", "ma_phong_du_kien"), ("", "trang_thai_don")]),
    "HOA_DON_PHONG (TV4)": (C[4], R3, "edge", [
        ("PK", "ma_hoa_don_phong"), ("FK,UK", "ma_chang"), ("FK", "ma_don"),
        ("", "tong_tien"), ("", "con_no")]),
}


def box(name):
    x, y, _, cols = E[name]
    return x, y, BOXW, HEAD + ROW * len(cols) + PAD


def row_y(name, i):
    """Toa do y giua dong thuoc tinh thu i."""
    x, y, _, _ = E[name]
    return y + HEAD + 8 + ROW * i + ROW / 2


out = []
a = out.append


def text(x, y, s, size=15, weight="normal", fill="#222", anchor="start", style=""):
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
      f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {style}>{escape(s)}</text>')


def draw_entity(name):
    x, y, kind, cols = E[name]
    _, _, w, h = box(name)
    core = kind == "core"
    hfill = NAVY if core else GREY
    bfill = "#ffffff" if core else "#e9ecef"
    dash = '' if core else 'stroke-dasharray="7 5"'
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{bfill}" '
      f'stroke="{hfill}" stroke-width="2" {dash}/>')
    a(f'<path d="M{x} {y+HEAD} V{y+7} Q{x} {y} {x+7} {y} H{x+w-7} Q{x+w} {y} {x+w} {y+7} '
      f'V{y+HEAD} Z" fill="{hfill}"/>')
    text(x + w / 2, y + 27, name, 17, "bold", "#fff", "middle")
    kx = x + 70
    a(f'<line x1="{kx}" y1="{y+HEAD}" x2="{kx}" y2="{y+h}" stroke="#9aa5b1" stroke-width="1"/>')
    for i, (k, c) in enumerate(cols):
        cy = row_y(name, i) + 5
        if k:
            text(x + 35, cy, k, 13, "bold", "#222", "middle")
        text(kx + 14, cy, c, 16, "bold" if k == "PK" else "normal")


def end_marker(x, y, dx, dy, card, label_side=1):
    """(x,y) tren canh thuc the; (dx,dy) huong di ra ngoai thuc the."""
    mn, mx = card.split(",")
    px, py = -dy, dx  # vuong goc

    def P(d, s=0):
        return x + dx * d + px * s, y + dy * d + py * s

    def seg(p, q):
        a(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" '
          f'stroke="{LINE}" stroke-width="2"/>')

    if mx == "N":
        seg(P(0, 9), P(16)); seg(P(0, -9), P(16)); seg(P(0), P(16))
        outer = 24
    else:
        seg(P(9, 7), P(9, -7))
        outer = 18
    if mn == "1":
        seg(P(outer, 7), P(outer, -7))
    else:
        cx, cy = P(outer + 5)
        a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="#fff" stroke="{LINE}" stroke-width="2"/>')
    # nhan luc luong
    if dy == 0:  # duong ngang: nhan nam duoi duong
        lx, ly = x + dx * 36, y + 18
    else:  # duong doc: nhan nam ben phai (label_side=-1: ben trai)
        lx, ly = x + 22 * label_side, y + dy * 36
    text(lx, ly + 5, card, 14, "normal", "#333", "middle")


def rel(points, card_a, card_b, label, lpos, side_a=1, side_b=1):
    """points: polyline; diem dau thuoc thuc the A, diem cuoi thuoc thuc the B."""
    d = "M" + " L".join(f"{p[0]} {p[1]}" for p in points)
    a(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2"/>')

    def unit(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        n = (dx * dx + dy * dy) ** 0.5
        return dx / n, dy / n

    end_marker(*points[0], *unit(points[0], points[1]), card_a, side_a)
    end_marker(*points[-1], *unit(points[-1], points[-2]), card_b, side_b)
    text(lpos[0], lpos[1], label, 14, "normal", "#333", "middle")


def right(n): x, y, w, h = box(n); return x + w
def left(n): return box(n)[0]
def top(n): return box(n)[1]
def bottom(n): x, y, w, h = box(n); return y + h


a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(60, 62, "SƠ ĐỒ ERD - PHẦN QUẢN LÝ (TV5)", 36, "bold", "#2b3440")

# ---- Danh muc: dip le, bang gia, hang, phong ----
y = row_y("DIP_LE", 0)
rel([(right("DIP_LE"), y), (left("BANG_GIA_HANG"), y)], "0,1", "0,N", "ap_dung_dip_le",
    ((right("DIP_LE") + left("BANG_GIA_HANG")) / 2, y - 10), -1, -1)
rel([(right("BANG_GIA_HANG"), y), (left("HANG_PHONG"), y)], "0,N", "1,1", "co_bang_gia",
    ((right("BANG_GIA_HANG") + left("HANG_PHONG")) / 2, y - 10), -1, -1)
rel([(right("HANG_PHONG"), y), (left("PHONG"), y)], "1,1", "0,N", "gom_cac_phong",
    ((right("HANG_PHONG") + left("PHONG")) / 2, y - 10), -1, -1)

# ---- Nhan su ----
y1 = row_y("VAI_TRO", 0)
rel([(right("VAI_TRO"), y1), (left("PHAN_CONG"), y1)], "1,1", "0,N", "thuoc_vai_tro",
    ((right("VAI_TRO") + left("PHAN_CONG")) / 2, y1 - 10), -1, -1)
yb = row_y("PHAN_CONG", 1)
rel([(left("NHAN_VIEN"), yb), (right("PHAN_CONG"), yb)], "1,1", "0,N", "duoc_phan_cong",
    ((right("PHAN_CONG") + left("NHAN_VIEN")) / 2, yb - 10), -1, -1)
yc = row_y("PHAN_CONG", 3)
rel([(left("NHAN_VIEN"), yc), (right("PHAN_CONG"), yc)], "1,1", "0,N", "giao_viec",
    ((right("PHAN_CONG") + left("NHAN_VIEN")) / 2, yc - 10), -1, -1)

# de quy: quan ly truc tiep
nx = left("NHAN_VIEN")
rel([(nx + 60, top("NHAN_VIEN")), (nx + 60, top("NHAN_VIEN") - 55),
     (nx + 190, top("NHAN_VIEN") - 55), (nx + 190, top("NHAN_VIEN"))],
    "0,1", "0,N", "quan_ly_truc_tiep", (nx + 125, top("NHAN_VIEN") - 63), -1, 1)

# nhan vien -> dieu chinh (lap, duyet)
yd = row_y("DIEU_CHINH_HOA_DON", 1)
rel([(right("NHAN_VIEN"), yd), (left("DIEU_CHINH_HOA_DON"), yd)], "1,1", "0,N", "lap_dieu_chinh",
    ((right("NHAN_VIEN") + left("DIEU_CHINH_HOA_DON")) / 2, yd - 10), -1, -1)
ye = row_y("DIEU_CHINH_HOA_DON", 4)
rel([(right("NHAN_VIEN"), ye), (left("DIEU_CHINH_HOA_DON"), ye)], "0,1", "0,N", "duyet_dieu_chinh",
    ((right("NHAN_VIEN") + left("DIEU_CHINH_HOA_DON")) / 2, ye - 10), 1, 1)

# nhan vien -> nhat ky (di vong phia tren)
ntop = top("NHAN_VIEN")
kx = left("NHAT_KY_KIEM_TOAN") + BOXW / 2
rel([(nx + 290, ntop), (nx + 290, ntop - 30), (kx, ntop - 30), (kx, top("NHAT_KY_KIEM_TOAN"))],
    "0,1", "0,N", "thuc_hien_thao_tac", ((left("DIEU_CHINH_HOA_DON") + right("DIEU_CHINH_HOA_DON")) / 2, ntop - 38), 1, 1)

# hoa don phong -> dieu chinh
hx = left("HOA_DON_PHONG (TV4)") + BOXW / 2
dx_ = left("DIEU_CHINH_HOA_DON") + BOXW / 2
mid = (bottom("DIEU_CHINH_HOA_DON") + top("HOA_DON_PHONG (TV4)")) / 2 + 20
rel([(hx, top("HOA_DON_PHONG (TV4)")), (hx, mid), (dx_, mid), (dx_, bottom("DIEU_CHINH_HOA_DON"))],
    "1,1", "0,N", "dieu_chinh_hoa_don", ((hx + dx_) / 2, mid - 10), 1, 1)

# ---- Su co va boi thuong ----
ys = row_y("SU_CO (TV3)", 0)
rel([(right("SU_CO (TV3)"), ys), (left("QUYET_DINH_SU_CO"), ys)], "1,1", "0,1", "duoc_xu_ly",
    ((right("SU_CO (TV3)") + left("QUYET_DINH_SU_CO")) / 2, ys - 10), -1, -1)
rel([(right("QUYET_DINH_SU_CO"), ys), (left("BOI_THUONG"), ys)], "0,1", "0,N", "kem_boi_thuong",
    ((right("QUYET_DINH_SU_CO") + left("BOI_THUONG")) / 2, ys - 10), -1, -1)
yt = row_y("BOI_THUONG", 1)
rel([(left("DON_DAT_PHONG (TV2)"), yt), (right("BOI_THUONG"), yt)], "1,1", "0,N", "boi_thuong_don",
    ((right("BOI_THUONG") + left("DON_DAT_PHONG (TV2)")) / 2, yt - 10), -1, -1)

nb = bottom("NHAN_VIEN")
qx = left("QUYET_DINH_SU_CO") + BOXW / 2
rel([(nx + 60, nb), (nx + 60, nb + 75), (qx, nb + 75), (qx, top("QUYET_DINH_SU_CO"))],
    "1,1", "0,N", "ra_quyet_dinh", ((nx + 60 + qx) / 2, nb + 67), 1, 1)
rel([(nx + 230, nb), (nx + 230, top("BOI_THUONG"))], "1,1", "0,N", "duyet_boi_thuong",
    (nx + 300, (nb + top("BOI_THUONG")) / 2 + 5), 1, 1)

for n in E:
    draw_entity(n)

# ---- Chu thich ----
ly = 1245
a(f'<rect x="60" y="{ly}" width="46" height="24" fill="#fff" stroke="{NAVY}" stroke-width="2"/>')
text(120, ly + 18, "Thực thể lõi TV5 (Quản lý)", 17)
a(f'<rect x="60" y="{ly+36}" width="46" height="24" fill="#e9ecef" stroke="{GREY}" '
  f'stroke-width="2" stroke-dasharray="6 4"/>')
text(120, ly + 54, "Thực thể ranh giới (TV2, TV3, TV4)", 17)

notes = [
    "Ghi chú: BANG_GIA_HANG dùng khoảng hiệu lực nửa mở [hieu_luc_tu, hieu_luc_den); ma_dip_le NULL là giá ngày thường. Sửa giá chỉ áp dụng cho nghiệp vụ phát sinh sau (BR09).",
    "PHAN_CONG nối NHAN_VIEN – VAI_TRO (n–n) theo thời gian; quyen_dieu_chinh đánh dấu trưởng bộ phận được giao quyền điều chỉnh (BR33). NHAN_VIEN.ma_quan_ly là quan hệ đệ quy (CTE đệ quy).",
    "NHAT_KY_KIEM_TOAN ghi bằng trigger audit; ten_bang + ma_ban_ghi trỏ đa hình nên không đặt FK. Báo cáo công suất, doanh thu, vật tư (UC19) suy ra bằng view/function, không lưu bảng riêng.",
    "Quan hệ HANG_PHONG/PHONG với DON_DAT_PHONG, LUOT_GIU_PHONG, CHANG_LUU_TRU, SU_CO, VAN_HANH_PHONG đã thể hiện ở ERD TV2, TV3; tên và cột chưa chốt là đề xuất thiết kế.",
]
for i, s in enumerate(notes):
    text(60, 1342 + i * 26, s, 15, "normal", "#555")

a("</svg>")
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out))
