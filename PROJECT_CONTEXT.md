# PROJECT CONTEXT — PLAYLIST LUYỆN ĐỀ CẤP TỐC 2026 (TOÁN CÁ CHÉP)
Môi trường: Thư mục gốc `List_Captoc_Web` | Ngày tạo: 09/05/2026
Trạng thái: 🟡 Đang xây dựng

---

## 1. MỤC TIÊU & DEFINITION OF DONE

**Dự án này là gì?**
`List_Captoc_Web` là hệ thống **phân phối đề luyện thi** dành riêng cho lớp **Cấp Tốc THPTQG 2026**. Học sinh truy cập 1 URL → thấy danh sách đề → chọn đề → nhập mật khẩu → làm bài → nộp → xem BXH.

**Mối quan hệ trong hệ sinh thái Cá Chép:**

```text
Test_Web (Nhà máy)           List_Captoc_Web (Cửa hàng Cấp Tốc)
┌──────────────────┐         ┌──────────────────────────────────┐
│ PDF → OCR → HTML │──robot──▶│ Hub LD01-LD40 + SHA-256 + BXH   │──URL──▶ HS Cấp Tốc
│ *_Unified.html   │         │ Filter: Trên lớp / Về nhà       │
└──────────────────┘         └──────────────────────────────────┘

List_Test_Web (Ngân hàng đề năm học) ← Dự án riêng, đối tượng khác
List_Chuyende_Web (Chuyên đề Hub)    ← Dự án riêng, đối tượng khác
```

**Dự án ĐẠT CHUẨN khi:**
- [ ] Trang Hub hiển thị danh sách đề LD01→LD40 với filter Trên lớp / Về nhà.
- [ ] Tất cả đề có mật khẩu SHA-256, hoạt động mượt trên Safari iOS.
- [ ] Cấu trúc đề chuẩn THPTQG 2025: Phần I (MC) + Phần II (TF) + Phần III (SA).
- [ ] HS nộp bài → dữ liệu gửi về Google Sheets (mã CT, điểm 3 phần, thời gian).
- [ ] BXH công khai hiển thị Top 10 theo mã CT ngay trong Hub.
- [ ] Dashboard admin (cho Tí) hiển thị bảng điểm chi tiết, filter theo buổi/HS.
- [ ] Robot `sync_playlist.ps1` tự quét → copy → build → push GitHub.

---

## 2. DANH PHÁP & QUY ƯỚC

### 2.1. Tên đề thi: LD (Luyện Đề)

| Quy tắc | Giá trị |
|---|---|
| **Format** | `LD01`, `LD02`, ..., `LD40` |
| **Tổng số đề** | 40 (20 buổi × 2 đề/buổi) |
| **Lẻ = Trên lớp** | LD01, LD03, LD05, ..., LD39 (20 đề) |
| **Chẵn = Về nhà** | LD02, LD04, LD06, ..., LD40 (20 đề) |
| **Icon** | Số thứ tự (01, 02...) phong cách iOS |
| **Tag phân biệt** | 🏫 Trên lớp (xanh) · 🏠 Về nhà (cam) |

| Buổi | 🏫 Trên lớp | 🏠 Về nhà |
|---|---|---|
| Buổi 1 | LD01 | LD02 |
| Buổi 2 | LD03 | LD04 |
| Buổi 3 | LD05 | LD06 |
| ... | ... | ... |
| Buổi 20 | LD39 | LD40 |

### 2.2. Mã học sinh: CT (Cấp Tốc)

| Quy tắc | Giá trị |
|---|---|
| **Format** | `CT01`, `CT02`, ..., `CT25`, ... |
| **Mở rộng** | Thêm HS mới → thêm CT26, CT27... (không giới hạn) |
| **Phát mã** | Tí phát mã vào buổi đầu tiên |
| **Bảng mapping** | Google Sheets tab "DanhSach" (mã ↔ tên thật ↔ SĐT) |
| **Validate** | JS check format `CT` + 2 số, không giới hạn range |
| **Bảo mật** | BXH chỉ hiện mã CT, không hiện tên thật |

### 2.3. Cấu trúc đề thi — Chuẩn THPTQG 2025

| Phần | Tên | Loại câu | Số câu | Điểm |
|---|---|---|---|---|
| **I** | Trắc nghiệm nhiều lựa chọn | Multiple Choice (A/B/C/D) | 12 câu | 3.0đ (0.25đ/câu) |
| **II** | Trắc nghiệm Đúng – Sai | True/False (4 cụm × 4 ý) | 4 cụm | 4.0đ (0/0.25/0.5/1.0đ/cụm) |
| **III** | Trả lời ngắn | Short Answer (nhập đáp số) | 6 câu | 3.0đ (0.5đ/câu) |
| | **Tổng** | | **22 câu** | **10.0đ** |

### 2.4. Quy tắc đáp án

| Loại đề | Sau nộp bài | Lý do |
|---|---|---|
| **🏫 Trên lớp** (lẻ) | Chỉ hiện **điểm + câu đúng/sai**, KHÔNG hiện lời giải | Tí sửa trực tiếp tại lớp, tránh HS xao nhãng |
| **🏠 Về nhà** (chẵn) | Hiện **điểm + lời giải chi tiết** | HS tự học, cần đáp án để hiểu |

> **Kỹ thuật**: Template Unified HTML dùng biến `SHOW_SOLUTION = false` (trên lớp) / `true` (về nhà).

---

## 3. KIẾN TRÚC KỸ THUẬT

### 3.1. Cấu trúc file

```text
List_Captoc_Web/
├── 01_Kho_De_Goc/           ← Source of Truth (file đề gốc LD01-LD40)
├── Pic/                     ← Logo + Mascot (retina 2x)
│   ├── logoleft.png
│   └── logoright.png
├── de/                      ← Output BUILD tự sinh (KHÔNG SỬA TAY)
├── index.html               ← Playlist Hub (filter: Trên lớp / Về nhà + BXH)
├── dashboard.html           ← Dashboard admin (bảng điểm, biểu đồ, cần MK admin)
├── quan_ly_de_thi.csv       ← Metadata + mật khẩu (40 đề)
├── sync_playlist.ps1        ← Robot Auto-Discovery + Build + Push
├── Sync_Len_Web.bat         ← Nút 1-click cho Tí
├── PROJECT_CONTEXT.md       ← File này
└── README.md
```

### 3.2. Luồng hoạt động

```text
[Tí tạo đề ở Test_Web]
       ↓
[Click Sync_Len_Web.bat]
       ↓
[Robot quét Test_Web → phát hiện file Unified mới]
       ↓
[Copy vào 01_Kho_De_Goc/ → thêm dòng CSV → build index.html]
       ↓
[SHA-256 hash mật khẩu → đổi tên file]
       ↓
[Git push → GitHub Pages → Live!]
```

### 3.3. Luồng dữ liệu (CSDL)

```text
HS làm bài → bấm NỘP → JS tính điểm 3 phần
       ↓
POST {maHS: "CT02", tenDe: "LD05", diemP1, diemP2, diemP3, tongDiem, ...}
       ↓
Google Apps Script (Web App) → ghi 1 dòng vào Google Sheets
       ↓
Sheets Published to Web → JSON công khai
       ↓
  ┌────────────────────┐     ┌─────────────────────────┐
  │ 🏆 BXH CÔNG KHAI   │     │ 📊 DASHBOARD ADMIN      │
  │ (HS thấy)          │     │ (Chỉ Tí thấy)          │
  │ Top 10 mã CT       │     │ Bảng điểm + biểu đồ    │
  │ Ngay trong Hub     │     │ dashboard.html + MK     │
  └────────────────────┘     └─────────────────────────┘
```

### 3.4. Cách mở đề trên Mobile (Safari-safe)

Tất cả đề đều có mật khẩu → dùng kỹ thuật pre-open tab:
1. HS bấm đề → Modal nhập mật khẩu hiện ra.
2. HS bấm "MỞ ĐỀ" → `window.open('about:blank')` NGAY LẬP TỨC (sync, trong user gesture).
3. Async: tính SHA-256 → `fetch HEAD` kiểm tra file → redirect tab mới.
4. Sai mật khẩu → đóng tab, hiện lỗi.

### 3.5. Thiết kế giao diện

| Thành phần | Giá trị |
|---|---|
| **Nền trang** | `#FFFFFF` (trắng) |
| **Hero** | Nền `#003B99` (xanh đậm thương hiệu), chữ `#F7C800` (vàng) |
| **Tiêu đề Hero** | "Luyện Đề Cấp Tốc 2026" |
| **Phụ đề** | "Toán Cá Chép · Khóa Cấp Tốc THPTQG" |
| **Font display** | Unbounded (800 weight) |
| **Font body** | Manrope |
| **Filter tabs** | `Tất cả` · `🏫 Trên lớp` · `🏠 Về nhà` |
| **Tag trên lớp** | Badge xanh (#E8F4FD / #0040BE) |
| **Tag về nhà** | Badge cam (#FFF0E6 / #E24500) |
| **Logo** | `logoleft.png` — 72px, `logoright.png` — 88px float animation |
| **Mobile** | `touch-action:manipulation`, debounce 800ms |

---

## 4. QUY TẮC KỸ THUẬT

| Quy tắc | Giải thích |
|---|---|
| **Mở tab mới** | Đề thi luôn mở ở tab mới (`_blank`), KHÔNG load trong iframe |
| **File đề self-contained** | Mỗi file `.html` chạy được độc lập (CSS/JS/MathJax riêng) |
| **Mã CT validate** | JS check format `CT` + 2 số, hiện cảnh báo nếu sai |
| **Điểm 3 phần** | POST gửi riêng `diemPhan1`, `diemPhan2`, `diemPhan3` |
| **Mobile-First** | Giao diện Hub hoạt động trên 375px trở lên |
| **Encoding UTF-8** | Bắt buộc cho CSV/HTML |
| **Thư mục `de/` auto-gen** | Robot tự sinh nội dung. KHÔNG BAO GIỜ sửa tay |

**KHÔNG được làm:**
- Không nhúng nội dung đề vào `index.html`.
- Không dùng `<iframe>` (gây scroll conflict trên mobile).
- Không dùng `window.open()` sau `await` (Safari chặn).
- Không sửa file trong thư mục `de/` (Robot sẽ ghi đè).
- Không hiện tên thật HS trên BXH (chỉ hiện mã CT).

---

## 5. CƠ SỞ DỮ LIỆU

### 5.1. CSV quản lý đề (`quan_ly_de_thi.csv`)

```csv
ID,Ten_De,Loai,Buoi,So_Cau,Thoi_Gian,File_Goc,Trang_Thai,Mat_Khau
ld_01,LD01,tren_lop,1,22,90,LD01.html,Hien,captoc01
ld_02,LD02,ve_nha,1,22,0,LD02.html,Hien,btvn01
ld_03,LD03,tren_lop,2,22,90,LD03.html,Hien,captoc02
ld_04,LD04,ve_nha,2,22,0,LD04.html,Hien,btvn02
...
```

| Cột | Ý nghĩa |
|---|---|
| `ID` | Mã nội bộ: `ld_01`, `ld_02`, ... |
| `Ten_De` | Tên hiển thị: `LD01`, `LD02`, ... |
| `Loai` | `tren_lop` hoặc `ve_nha` |
| `Buoi` | Số buổi (1-20) |
| `So_Cau` | Luôn = 22 (chuẩn THPTQG) |
| `Thoi_Gian` | 90 (trên lớp) hoặc 0 (về nhà = không giới hạn) |
| `Mat_Khau` | Plaintext (local only, Robot hash trước khi push) |

### 5.2. Google Sheets — 1 file, 2 tab

> **Tất cả 40 đề ghi chung 1 tab** — 750 dòng max, rất nhẹ, dễ query tổng hợp.

**Tab "KetQua"** (Apps Script ghi tự động):

| Cột | Ví dụ | Ghi chú |
|---|---|---|
| Thời điểm | 2026-06-15 19:45:00 | Auto |
| Mã HS | CT02 | HS nhập |
| Tên đề | LD05 | Auto |
| Loại | tren_lop | Auto |
| Buổi | 3 | Auto |
| Lần | 1 | JS tự đếm |
| Điểm P.I | 2.5 | Auto |
| Điểm P.II | 3.0 | Auto |
| Điểm P.III | 2.0 | Auto |
| Tổng điểm | 7.5 | Auto |
| Câu đúng | 18/22 | Auto |
| Thời gian làm | 52:30 | Auto |
| TrangThai | hop_le | Tí đổi `da_xoa` nếu HS nhầm |

**Tab "DanhSach"** (Tí quản lý thủ công):

| Mã | Họ tên | SĐT phụ huynh |
|---|---|---|
| CT01 | Lê Minh Cường | 0901... |
| CT02 | Nguyễn Văn An | 0912... |
| ... | ... | ... |

### 5.3. Quy tắc nộp nhiều lần

| Quy tắc | Giá trị |
|---|---|
| **Mỗi lần nộp** | = 1 dòng mới (không ghi đè) |
| **Cột Lần** | JS tự đếm: CT02 nộp LD05 lần 2 → Lần = 2 |
| **BXH tính theo** | **Lần đầu tiên** (TrangThai = hop_le) |
| **Xóa lần nhầm** | Tí đổi `TrangThai` = `da_xoa` trong Sheets |
| **Soft delete** | Giữ dòng, Dashboard tự bỏ qua dòng `da_xoa` |

---

## 6. HOSTING

| Hạng mục | Giá trị |
|---|---|
| **Nền tảng** | GitHub Pages |
| **Repo** | `LopToanCaChep/captoc-2026` |
| **URL** | `https://loptoancachep.github.io/captoc-2026/` |
| **Nhúng** | Embed trong Ghost CMS qua iframe |
| **Deploy** | Tự động qua `sync_playlist.ps1` (git push → live) |

---

## 7. QUY TRÌNH VẬN HÀNH CHO TÍ

### Thêm đề mới
1. Tạo đề ở `Test_Web` → workflow `/TaoHTML_BaiThi`.
2. Click đúp `Sync_Len_Web.bat` → Robot tự xử lý → push GitHub.

### Đặt / đổi mật khẩu
1. Mở `quan_ly_de_thi.csv` → sửa cột `Mat_Khau`.
2. **Ctrl + S** (PHẢI lưu trước!!!).
3. Click đúp `Sync_Len_Web.bat`.

### Ẩn đề thi
1. `quan_ly_de_thi.csv` → đổi `Trang_Thai` thành `An`.
2. **Ctrl + S** → Click đúp `Sync_Len_Web.bat`.

### Thêm học sinh mới
1. Mở Google Sheets → tab "DanhSach" → thêm dòng `CT26, Tên HS, SĐT`.
2. Phát mã CT26 cho HS mới. Không cần sửa code.

### Xem kết quả
- **Nhanh**: Mở Hub → kéo xuống BXH (Top 10 công khai).
- **Chi tiết**: Mở `dashboard.html` → nhập mật khẩu admin.

---

## 8. TÔ ĐỌC FILE NÀY → LÀM GÌ

Nếu có request liên quan đến `List_Captoc_Web`, Tô tự kiểm tra:
1. ✅ **Tên đề = LD** — LD01→LD40, lẻ = trên lớp, chẵn = về nhà.
2. ✅ **Mã HS = CT** — CT01+, validate format, không hiện tên thật trên BXH.
3. ✅ **Mở tab mới** — Tất cả đề có mật khẩu, dùng pre-open tab (Safari-safe).
4. ✅ **Điểm 3 phần** — POST gửi riêng P.I, P.II, P.III.
5. ✅ **Nộp nhiều lần** — BXH lấy lần đầu. Xóa nhầm = soft delete (đổi TrangThai).
6. ✅ **1 tab chung** — Tất cả 40 đề ghi vào tab "KetQua", không tách tab.
7. ✅ **Mobile-First** — Mọi component test trên 375px trước.
8. ✅ **UTF-8** — Encoding bắt buộc cho CSV/HTML.
9. ✅ **Thư mục `de/` tự sinh** — Robot quản lý, không sửa tay.
10. ✅ **File đề bất biến** — Copy từ `Test_Web`, KHÔNG sửa nội dung.
