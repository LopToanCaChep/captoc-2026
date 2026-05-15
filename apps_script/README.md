# Apps Script Mirror — List_Captoc_Web

Folder này chứa source code Google Apps Script (`.gs` / `.js`) được pull về local bằng `clasp`.

## Setup lần đầu

1. **Tìm Script ID**:
   - Mở Google Apps Script project tại [script.google.com](https://script.google.com)
   - Vào ⚙️ Project Settings → IDs → Copy **Script ID**

2. **Tạo `.clasp.json`** trong folder này:
   ```json
   {"scriptId": "PASTE_SCRIPT_ID_HERE", "rootDir": "."}
   ```

3. **Login clasp** (chỉ cần 1 lần):
   ```bash
   npx @google/clasp login
   ```

4. **Pull source**:
   ```bash
   # Từ root CaChep_Ecosystem:
   .\pull_apps_script.ps1 -Hub captoc
   ```

## Quy trình cập nhật

- **Pull**: `.\pull_apps_script.ps1` (từ root) → lấy code mới nhất từ Google
- **Push**: Nếu sửa local, dùng `npx @google/clasp push` trong folder này
- **Lưu ý**: Luôn **pull trước** khi sửa để tránh ghi đè code trên Google
