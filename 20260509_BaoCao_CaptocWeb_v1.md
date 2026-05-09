# 📋 Báo Cáo Phiên Làm Việc — Cấp Tốc 2026
> **Thời gian**: 09/05/2026 (04:39 → 09:44)
> **Dự án**: `List_Captoc_Web` — Nền tảng Luyện Đề Cấp Tốc 2026

---

## 1. Kết quả đạt được

### ✅ Phase 4: Dashboard Admin — Hoàn tất
- Tạo `dashboard.html` với đăng nhập SHA-256 (MK: `0806`)
- Thống kê: lượt nộp, TB điểm, TB từng phần, phần yếu nhất
- Bảng điểm toàn bộ HS, color-coded, filter theo buổi/đề/loại
- Cảnh báo: HS dưới 5đ, P.III = 0đ
- Profile chi tiết từng HS

### ✅ Đề LD01 — Live!
- Tí tạo đề ở Test_Web (nhà máy) → copy HTML sang `List_Captoc_Web`
- Tô inject: Modal nhập **mã CT** + POST Google Sheets + ẩn lời giải
- Robot sync → hash MK → push GitHub → Live!
- **URL**: `https://loptoancachep.github.io/captoc-2026/`
- **MK đề**: `ld01`

### ✅ Nâng cấp UI (theo review bạn Tí)
| Fix | Mô tả |
|---|---|
| **Bypass security** | Chỉ cho bypass khi `file://` protocol, production luôn hiện sai MK |
| **Hero upgrade** | Thêm dotted pattern + 🐟 mờ góc phải + badge "🔥 KHOÁ 2026" |
| **Hover effect** | Học từ Chuyên Đề Web: icon đổi vàng, nâng 4px, transition 0.3s |
| **Arrow icon** | Swap `arrow_1.png` ↔ `arrow.png` khi hover |
| **Focus-visible** | Thêm outline xanh cho tất cả interactive elements (a11y) |
| **maxlength** | Lookup input: 4 → 6 (hỗ trợ CT100+) |
| **Empty states** | Tra cứu có icon ⚠️ và 🐟, center layout |

---

## 2. Quy trình vận hành đã chốt

### Tạo đề mới (phân công)

| Bước | Ai | Công việc |
|---|---|---|
| **1** | **Tí** | Tạo đề ở Test_Web (nhà máy) → file `*_Unified.html` |
| **2** | **Tí** | Copy file HTML vào `List_Captoc_Web/01_Inputs/` |
| **3** | **Tô** | Inject: mã CT + POST Sheets + ẩn/hiện giải + đặt MK |
| **4** | **Tô** | Cập nhật CSV → chạy Robot → push lên web |

### Quy tắc đáp án

| Loại đề | Sau nộp bài | Biến kỹ thuật |
|---|---|---|
| **🏫 Trên lớp** (lẻ) | Chỉ điểm + đúng/sai, **KHÔNG lời giải** | `SHOW_SOLUTION = false` |
| **🏠 Về nhà** (chẵn) | Điểm + **lời giải chi tiết** | `SHOW_SOLUTION = true` |

---

## 3. Thông tin kỹ thuật

### Biến JS inject vào file đề

```javascript
const SCRIPT_URL = '...Apps Script endpoint...';
const EXAM_ID = 'LD01';       // Mã đề
const EXAM_LOAI = 'tren_lop'; // tren_lop | ve_nha
const EXAM_BUOI = 1;          // Buổi học
const SHOW_SOLUTION = false;  // Ẩn/hiện lời giải
```

### POST data gửi về Sheets

```json
{
  "maHS": "CT01",
  "tenDe": "LD01",
  "loaiDe": "tren_lop",
  "buoi": 1,
  "diemPhan1": 2.5,
  "diemPhan2": 3.0,
  "diemPhan3": 1.5,
  "tongDiem": 7.0,
  "thoiGianLam": "52:30",
  "soCauDung": 18,
  "tongSoCau": 22
}
```

### Cấu trúc thư mục

```
List_Captoc_Web/
├── 01_Inputs/               ← File đề gốc từ Test_Web
├── 01_Kho_De_Goc/           ← Source of Truth (Robot đọc)
├── Pic/                     ← Logo + Arrow icons
├── de/                      ← Output BUILD tự sinh (KHÔNG SỬA TAY)
├── index.html               ← Hub (filter + BXH + Tra cứu)
├── dashboard.html           ← Dashboard admin (MK: 0806)
├── quan_ly_de_thi.csv       ← Metadata + mật khẩu
├── sync_playlist.ps1        ← Robot Auto-Discovery + Build + Push
├── Sync_Len_Web.bat         ← Nút 1-click cho Tí
└── PROJECT_CONTEXT.md       ← Tài liệu gốc (đọc trước tiên)
```

---

## 4. Trạng thái hệ thống

| Component | Trạng thái | URL / Vị trí |
|---|---|---|
| **Hub** | ✅ Live | `loptoancachep.github.io/captoc-2026/` |
| **Dashboard** | ✅ Live (MK: 0806) | `/captoc-2026/dashboard.html` |
| **LD01** | ✅ Live (MK: ld01) | Mã hóa SHA-256 trong `/de/` |
| **Apps Script** | ✅ Active | Endpoint POST + GET |
| **Google Sheet** | ✅ Ready | Tab KetQua + DanhSach |

---

## 5. Backlog (từ review)

| # | Vấn đề | Ưu tiên | Trạng thái |
|---|---|---|---|
| 2 | API endpoint lộ → thêm origin check ở Apps Script | 🟡 | Chưa làm |
| 7 | Hover giật trên iPad (hover ảo) | 🟢 | Monitor |
| 8 | BXH/filter thiếu phân tách thị giác | 🟢 | Backlog |
| 9 | Filter sticky khi cuộn | 🟢 | Backlog |
| 11 | Loader cá 🐟 chưa hiển thị (dead code) | 🟢 | Backlog |

---

## 6. Ghi chú cho Tô (phiên sau)

> **Đọc file này + `PROJECT_CONTEXT.md` trước khi làm bất kỳ thay đổi nào.**

- **Khi Tí gửi file đề mới**: Xem bước 3 mục 2 — inject 5 biến JS + đổi modal nhập tên → nhập mã CT.
- **Khi sửa giao diện Hub**: Tham khảo `List_Chuyende_Web/index.html` để giữ consistency.
- **Khi cần debug**: Endpoint Apps Script = dòng `const API_URL` trong `index.html`.
- **KHÔNG BAO GIỜ**: Sửa file trong `de/`, Robot sẽ ghi đè.
