"""
validate_csv.py — Kiểm tra schema 3 CSV Distribution của CaChep_Ecosystem

Dùng:
    python validate_csv.py list_test      # List_Test_Web/quan_ly_de_thi.csv
    python validate_csv.py list_captoc    # List_Captoc_Web/quan_ly_de_thi.csv
    python validate_csv.py list_chuyende  # List_Chuyende_Web/quan_ly_chuyen_de.csv
    python validate_csv.py all            # cả 3

Exit code: 0 = sạch, 1 = có lỗi, 2 = file không tìm thấy
"""
import sys
import csv
import re
from pathlib import Path

ROOT = Path(__file__).parent

# ═══ SCHEMA DEFINITIONS ═══

SCHEMAS = {
    "list_test": {
        "csv_path": ROOT / "List_Test_Web" / "quan_ly_de_thi.csv",
        "label": "List_Test_Web",
        "columns": [
            "ID", "Ten_De", "Lop", "Dang", "So_Cau",
            "Thoi_Gian", "File_Goc", "Trang_Thai", "Mat_Khau"
        ],
        "rules": {
            "ID":          {"required": True,  "pattern": r"^de_\d+$"},
            "Ten_De":      {"required": True},
            "Lop":         {"required": True,  "int_range": (10, 12)},
            "Dang":        {"required": True},
            "So_Cau":      {"required": True,  "int_min": 0},
            "Thoi_Gian":   {"required": True,  "int_min": 1},
            "File_Goc":    {"required": True,  "html_ext": True},
            "Trang_Thai":  {"required": True,  "domain": ["Hien", "An"]},
            "Mat_Khau":    {"required": False},
        },
        "unique": ["ID", "File_Goc"],
    },
    "list_captoc": {
        "csv_path": ROOT / "List_Captoc_Web" / "quan_ly_de_thi.csv",
        "label": "List_Captoc_Web",
        "columns": [
            "ID", "Ten_De", "Loai", "Buoi", "So_Cau",
            "Thoi_Gian", "File_Goc", "Trang_Thai", "Mat_Khau"
        ],
        "rules": {
            "ID":          {"required": True,  "pattern": r"^LD\d+$"},
            "Ten_De":      {"required": True},
            "Loai":        {"required": True},
            "Buoi":        {"required": True,  "int_min": 1},
            "So_Cau":      {"required": True,  "int_min": 0},
            "Thoi_Gian":   {"required": True,  "int_min": 1},
            "File_Goc":    {"required": True,  "html_ext": True},
            "Trang_Thai":  {"required": True,  "domain": ["Hien", "An"]},
            "Mat_Khau":    {"required": False},
        },
        "unique": ["ID", "File_Goc"],
    },
    "list_chuyende": {
        "csv_path": ROOT / "List_Chuyende_Web" / "quan_ly_chuyen_de.csv",
        "label": "List_Chuyende_Web",
        "columns": [
            "ID_ChuyenDe", "Ten_ChuyenDe", "Mon_Hoc", "Lop",
            "So_Cau", "Mat_Khau", "Trang_Thai"
        ],
        "rules": {
            "ID_ChuyenDe":  {"required": True,  "pattern": r"^chuyende_\d+$"},
            "Ten_ChuyenDe": {"required": True},
            "Mon_Hoc":      {"required": True},
            "Lop":          {"required": True,  "int_range": (10, 12)},
            "So_Cau":       {"required": True,  "int_min": 0},
            "Mat_Khau":     {"required": False},
            "Trang_Thai":   {"required": True,  "domain": ["Hien", "An"]},
        },
        "unique": ["ID_ChuyenDe"],
    },
}


def _err(rule_id, row_num, col, msg):
    return {"rule": rule_id, "row": row_num, "col": col, "msg": msg}


def validate(schema_key: str) -> list[dict]:
    schema = SCHEMAS[schema_key]
    csv_path = schema["csv_path"]
    issues = []

    if not csv_path.exists():
        print(f"[CSV002] ❌ Không tìm thấy file: {csv_path}")
        sys.exit(2)

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        actual_cols = reader.fieldnames or []

        # CSV001 — Kiểm tra cột bắt buộc
        for col in schema["columns"]:
            if col not in actual_cols:
                issues.append(_err("CSV001", 0, col, f"Thiếu cột bắt buộc: '{col}'"))

        missing_cols = {c for c in schema["columns"] if c not in actual_cols}
        if missing_cols:
            return issues  # không validate row nếu thiếu cột

        # Đọc từng row
        seen = {col: {} for col in schema.get("unique", [])}
        for row_num, row in enumerate(reader, start=2):
            rules = schema["rules"]
            for col, col_rules in rules.items():
                val = row.get(col, "").strip()

                # CSV006 — Bắt buộc không được rỗng
                if col_rules.get("required") and val == "":
                    issues.append(_err("CSV006", row_num, col, f"Trường bắt buộc bị rỗng"))
                    continue

                if val == "":
                    continue  # optional, bỏ qua

                # CSV002 — Pattern ID
                if "pattern" in col_rules:
                    if not re.match(col_rules["pattern"], val):
                        issues.append(_err("CSV002", row_num, col,
                                          f"ID không đúng pattern '{col_rules['pattern']}': '{val}'"))

                # CSV003 — Integer range/min
                if "int_min" in col_rules or "int_range" in col_rules:
                    try:
                        n = int(val)
                    except ValueError:
                        issues.append(_err("CSV003", row_num, col,
                                          f"Phải là số nguyên, nhận được: '{val}'"))
                        continue

                    if "int_min" in col_rules and n < col_rules["int_min"]:
                        issues.append(_err("CSV003", row_num, col,
                                          f"Giá trị {n} < min {col_rules['int_min']}"))
                    if "int_range" in col_rules:
                        lo, hi = col_rules["int_range"]
                        if not (lo <= n <= hi):
                            issues.append(_err("CSV003", row_num, col,
                                              f"Giá trị {n} không trong [{lo}, {hi}]"))

                # CSV004 — Domain
                if "domain" in col_rules and val not in col_rules["domain"]:
                    issues.append(_err("CSV004", row_num, col,
                                      f"Giá trị '{val}' không thuộc {col_rules['domain']}"))

                # CSV007 — .html extension
                if col_rules.get("html_ext") and not val.lower().endswith(".html"):
                    issues.append(_err("CSV007", row_num, col,
                                      f"File_Goc phải kết thúc bằng .html: '{val}'"))

            # CSV005 — Duplicate unique
            for col in schema.get("unique", []):
                val = row.get(col, "").strip()
                if val in seen[col]:
                    issues.append(_err("CSV005", row_num, col,
                                      f"Trùng lặp '{val}' (lần đầu ở dòng {seen[col][val]})"))
                else:
                    seen[col][val] = row_num

    return issues


def print_report(label: str, issues: list[dict], csv_path: Path):
    print(f"\n{'─' * 60}")
    print(f"  📋 {label}  ({csv_path})")
    print(f"{'─' * 60}")
    if not issues:
        print("  ✅ Sạch — không có lỗi nào.")
        return
    for iss in issues:
        row_str = f"dòng {iss['row']}" if iss["row"] else "header"
        print(f"  [{iss['rule']}] {row_str} | {iss['col']}: {iss['msg']}")
    print(f"\n  ⚠️  Tổng: {len(issues)} vấn đề")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    target = sys.argv[1].lower()
    if target == "all":
        keys = list(SCHEMAS.keys())
    elif target in SCHEMAS:
        keys = [target]
    else:
        print(f"❌ Không nhận dạng được target '{target}'. Dùng: list_test | list_captoc | list_chuyende | all")
        sys.exit(2)

    total_issues = 0
    for key in keys:
        schema = SCHEMAS[key]
        issues = validate(key)
        print_report(schema["label"], issues, schema["csv_path"])
        total_issues += len(issues)

    print(f"\n{'═' * 60}")
    if total_issues == 0:
        print("  🎉 Tất cả CSV đều hợp lệ!")
        sys.exit(0)
    else:
        print(f"  ❌ Tổng cộng {total_issues} vấn đề — cần sửa trước khi sync.")
        sys.exit(1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    main()
