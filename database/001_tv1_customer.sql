-- ============================================================================
-- TV1 · KHÁCH HÀNG - DDL 4 BẢNG LÕI
-- File đề xuất đặt tại: database/migrations/001_tv1_customer.sql
-- Phạm vi: UC01–UC04, UC21
-- Quy tắc: BR01, BR02, BR18, BR21, BR22, BR24, BR25, BR29, BR31, BR34
-- Lưu ý: Chạy sau 00_create_database.sql. Khối FK ranh giới sang HANG_PHONG
--        và PHONG (TV2/TV5) sẽ tự động gắn nếu các bảng đó đã tồn tại.
-- ============================================================================

USE [HotelBooking];
GO

-- 1. Bảng KHACH_HANG
CREATE TABLE dbo.KHACH_HANG (
    ma_khach       INT IDENTITY(1,1) NOT NULL,
    ho_ten         NVARCHAR(100)     NOT NULL,
    so_dien_thoai  VARCHAR(20)       NOT NULL,
    email          VARCHAR(150)      NULL,
    loai_giay_to   VARCHAR(20)       NULL,
    so_giay_to     VARCHAR(30)       NULL,
    dia_chi        NVARCHAR(255)     NULL,
    sql_login      SYSNAME           NULL,
    trang_thai     VARCHAR(20)       NOT NULL CONSTRAINT DF_KHACH_HANG_trang_thai DEFAULT ('HOAT_DONG'),
    thoi_diem_tao  DATETIME2(0)      NOT NULL CONSTRAINT DF_KHACH_HANG_thoi_diem_tao DEFAULT (SYSDATETIME()),

    CONSTRAINT PK_KHACH_HANG PRIMARY KEY CLUSTERED (ma_khach),
    CONSTRAINT UQ_KHACH_HANG_so_dien_thoai UNIQUE (so_dien_thoai),
    CONSTRAINT CK_KHACH_HANG_loai_giay_to CHECK (
        loai_giay_to IS NULL OR loai_giay_to IN ('CCCD', 'HO_CHIEU')
    ),
    CONSTRAINT CK_KHACH_HANG_giay_to_dong_bo CHECK (
        (loai_giay_to IS NULL AND so_giay_to IS NULL)
        OR (loai_giay_to IS NOT NULL AND so_giay_to IS NOT NULL)
    ),
    CONSTRAINT CK_KHACH_HANG_trang_thai CHECK (trang_thai IN ('HOAT_DONG', 'VO_HIEU'))
);
GO

CREATE UNIQUE NONCLUSTERED INDEX UX_KHACH_HANG_email
    ON dbo.KHACH_HANG (email)
    WHERE email IS NOT NULL;

CREATE UNIQUE NONCLUSTERED INDEX UX_KHACH_HANG_so_giay_to
    ON dbo.KHACH_HANG (so_giay_to)
    WHERE so_giay_to IS NOT NULL;

CREATE UNIQUE NONCLUSTERED INDEX UX_KHACH_HANG_sql_login
    ON dbo.KHACH_HANG (sql_login)
    WHERE sql_login IS NOT NULL;
GO

-- 2. Bảng LUOT_LUU_TRU (nhóm 1 hoặc nhiều đơn của cùng khách - BR34)
CREATE TABLE dbo.LUOT_LUU_TRU (
    ma_luot          INT IDENTITY(1,1) NOT NULL,
    ma_luot_hien_thi VARCHAR(20)       NOT NULL,
    ma_khach         INT               NOT NULL,
    trang_thai_luot  VARCHAR(20)       NOT NULL CONSTRAINT DF_LUOT_LUU_TRU_trang_thai DEFAULT ('DANG_MO'),
    thoi_diem_tao    DATETIME2(0)      NOT NULL CONSTRAINT DF_LUOT_LUU_TRU_thoi_diem_tao DEFAULT (SYSDATETIME()),

    CONSTRAINT PK_LUOT_LUU_TRU PRIMARY KEY CLUSTERED (ma_luot),
    CONSTRAINT UQ_LUOT_LUU_TRU_ma_hien_thi UNIQUE (ma_luot_hien_thi),
    CONSTRAINT FK_LUOT_LUU_TRU_KHACH_HANG FOREIGN KEY (ma_khach)
        REFERENCES dbo.KHACH_HANG (ma_khach)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_LUOT_LUU_TRU_trang_thai CHECK (
        trang_thai_luot IN ('DANG_MO', 'HOAN_TAT', 'DA_HUY')
    )
);
GO

-- 3. Bảng DON_DAT_PHONG (1 phòng/thời điểm, lịch và cọc riêng - BR01, BR21, BR22, BR31, BR34)
CREATE TABLE dbo.DON_DAT_PHONG (
    ma_don              INT IDENTITY(1,1) NOT NULL,
    ma_don_hien_thi     VARCHAR(20)       NOT NULL,
    ma_luot             INT               NOT NULL,
    ma_hang             INT               NOT NULL,
    ngay_den            DATE              NOT NULL,
    ngay_di             DATE              NOT NULL,
    so_khach            TINYINT           NOT NULL,
    tong_gia_bao        DECIMAL(18,0)     NOT NULL,
    la_ky_le            BIT               NOT NULL CONSTRAINT DF_DON_DAT_PHONG_la_ky_le DEFAULT (0),
    la_goi_tra_truoc    BIT               NOT NULL CONSTRAINT DF_DON_DAT_PHONG_la_goi_tra_truoc DEFAULT (0),
    coc_yeu_cau         DECIMAL(18,0)     NOT NULL CONSTRAINT DF_DON_DAT_PHONG_coc_yeu_cau DEFAULT (0),
    trang_thai          VARCHAR(25)       NOT NULL CONSTRAINT DF_DON_DAT_PHONG_trang_thai DEFAULT ('CHO_XEP_PHONG'),
    gio_nhan_thong_bao  DATETIME2(0)      NULL,
    thoi_diem_tao       DATETIME2(0)      NOT NULL CONSTRAINT DF_DON_DAT_PHONG_thoi_diem_tao DEFAULT (SYSDATETIME()),
    thoi_diem_dong      DATETIME2(0)      NULL,
    ly_do_dong          NVARCHAR(255)     NULL,

    CONSTRAINT PK_DON_DAT_PHONG PRIMARY KEY CLUSTERED (ma_don),
    CONSTRAINT UQ_DON_DAT_PHONG_ma_hien_thi UNIQUE (ma_don_hien_thi),
    CONSTRAINT FK_DON_DAT_PHONG_LUOT_LUU_TRU FOREIGN KEY (ma_luot)
        REFERENCES dbo.LUOT_LUU_TRU (ma_luot)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_DON_DAT_PHONG_ngay CHECK (ngay_di > ngay_den),
    CONSTRAINT CK_DON_DAT_PHONG_so_khach CHECK (so_khach > 0),
    CONSTRAINT CK_DON_DAT_PHONG_gia_coc CHECK (
        tong_gia_bao >= 0 AND coc_yeu_cau >= 0 AND coc_yeu_cau <= tong_gia_bao
    ),
    CONSTRAINT CK_DON_DAT_PHONG_trang_thai CHECK (
        trang_thai IN (
            'CHO_XEP_PHONG', 'CHO_KHACH_XN', 'CHO_XN_CUOI',
            'DA_XAC_NHAN', 'DANG_LUU_TRU', 'DA_TRA_PHONG',
            'DA_HUY', 'NO_SHOW', 'HET_HAN_GIU'
        )
    ),
    CONSTRAINT CK_DON_DAT_PHONG_dong_don CHECK (
        (trang_thai IN ('DA_HUY', 'NO_SHOW', 'HET_HAN_GIU') AND thoi_diem_dong IS NOT NULL)
        OR (trang_thai NOT IN ('DA_HUY', 'NO_SHOW', 'HET_HAN_GIU') AND thoi_diem_dong IS NULL)
    )
);
GO

-- 4. Bảng YEU_CAU_THAY_DOI (thực thể yếu, append-only theo (ma_don, lan_yc) - UC21, BR24, BR25, BR29)
CREATE TABLE dbo.YEU_CAU_THAY_DOI (
    ma_don              INT            NOT NULL,
    lan_yc              INT            NOT NULL,
    loai_yeu_cau        VARCHAR(25)    NOT NULL,
    ma_hang_moi         INT            NULL,
    ngay_den_moi        DATE           NULL,
    ngay_di_moi         DATE           NULL,
    ma_phong_de_xuat    INT            NULL,
    trang_thai_khach    VARCHAR(20)    NOT NULL CONSTRAINT DF_YC_THAY_DOI_tt_khach DEFAULT ('CHO_PHAN_HOI'),
    tg_khach_phan_hoi   DATETIME2(0)   NULL,
    trang_thai_ap_dung  VARCHAR(20)    NOT NULL CONSTRAINT DF_YC_THAY_DOI_tt_ap_dung DEFAULT ('CHUA_AP_DUNG'),
    tg_le_tan_ap_dung   DATETIME2(0)   NULL,
    tg_tao              DATETIME2(0)   NOT NULL CONSTRAINT DF_YC_THAY_DOI_tg_tao DEFAULT (SYSDATETIME()),
    ly_do               NVARCHAR(255)  NULL,

    CONSTRAINT PK_YEU_CAU_THAY_DOI PRIMARY KEY CLUSTERED (ma_don, lan_yc),
    CONSTRAINT FK_YC_THAY_DOI_DON_DAT_PHONG FOREIGN KEY (ma_don)
        REFERENCES dbo.DON_DAT_PHONG (ma_don)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT CK_YC_THAY_DOI_lan_yc CHECK (lan_yc >= 1),
    CONSTRAINT CK_YC_THAY_DOI_loai CHECK (
        loai_yeu_cau IN ('DE_XUAT_XEP', 'KHACH_DOI', 'THAY_PHONG_SU_CO')
    ),
    CONSTRAINT CK_YC_THAY_DOI_ngay_moi CHECK (
        (ngay_den_moi IS NULL AND ngay_di_moi IS NULL)
        OR (ngay_den_moi IS NOT NULL AND ngay_di_moi IS NOT NULL AND ngay_di_moi > ngay_den_moi)
    ),
    CONSTRAINT CK_YC_THAY_DOI_tt_khach CHECK (
        trang_thai_khach IN ('CHO_PHAN_HOI', 'DONG_Y', 'TU_CHOI', 'HET_HAN')
    ),
    CONSTRAINT CK_YC_THAY_DOI_moc_khach CHECK (
        (trang_thai_khach IN ('DONG_Y', 'TU_CHOI') AND tg_khach_phan_hoi IS NOT NULL)
        OR (trang_thai_khach IN ('CHO_PHAN_HOI', 'HET_HAN') AND tg_khach_phan_hoi IS NULL)
    ),
    CONSTRAINT CK_YC_THAY_DOI_tt_ap_dung CHECK (
        trang_thai_ap_dung IN ('CHUA_AP_DUNG', 'DA_AP_DUNG', 'DA_THAY_THE', 'HUY')
    ),
    CONSTRAINT CK_YC_THAY_DOI_moc_le_tan CHECK (
        (trang_thai_ap_dung = 'DA_AP_DUNG' AND tg_le_tan_ap_dung IS NOT NULL AND trang_thai_khach = 'DONG_Y')
        OR (trang_thai_ap_dung <> 'DA_AP_DUNG' AND tg_le_tan_ap_dung IS NULL)
    )
);
GO

-- Tự động gắn FK ranh giới nếu bảng HANG_PHONG và PHONG (TV2/TV5) đã tồn tại
IF OBJECT_ID(N'dbo.HANG_PHONG', N'U') IS NOT NULL
BEGIN
    ALTER TABLE dbo.DON_DAT_PHONG
        ADD CONSTRAINT FK_DON_DAT_PHONG_HANG_PHONG FOREIGN KEY (ma_hang)
            REFERENCES dbo.HANG_PHONG (ma_hang)
            ON DELETE NO ACTION ON UPDATE NO ACTION;

    ALTER TABLE dbo.YEU_CAU_THAY_DOI
        ADD CONSTRAINT FK_YC_THAY_DOI_HANG_MOI FOREIGN KEY (ma_hang_moi)
            REFERENCES dbo.HANG_PHONG (ma_hang)
            ON DELETE NO ACTION ON UPDATE NO ACTION;
END;

IF OBJECT_ID(N'dbo.PHONG', N'U') IS NOT NULL
BEGIN
    ALTER TABLE dbo.YEU_CAU_THAY_DOI
        ADD CONSTRAINT FK_YC_THAY_DOI_PHONG_DE_XUAT FOREIGN KEY (ma_phong_de_xuat)
            REFERENCES dbo.PHONG (ma_phong)
            ON DELETE NO ACTION ON UPDATE NO ACTION;
END;
GO
