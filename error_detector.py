"""
error_detector.py — Detector lỗi OCR/Regex/MathJax cho đề thi Toán Cá Chép
=============================================================================
Dùng:
    python error_detector.py <file.md>              # Scan Markdown trước khi build
    python error_detector.py <file.md> --fix        # Scan + tự động sửa các lỗi fixable
    python error_detector.py <thư_mục_đề>           # Scan MD + HTML trong 1 đề
    python error_detector.py <file.html>            # Scan HTML output sau khi build

Output:
    ❌ ERROR  PA001 @ dòng 42: 'Chọn C' thiếu '## ' prefix
              → "Chọn C."
              → Auto-fixable: chạy với --fix để sửa

Exit code: 0 = sạch | 1 = có lỗi | 2 = file không tìm thấy
"""

import re
import sys
import json
import argparse
from dataclasses import dataclass, field
from pathlib import Path

# ─── Cấu trúc Finding ────────────────────────────────────────────────────────

@dataclass
class Finding:
    rule_id: str
    line_no: int        # 0 = không xác định dòng cụ thể
    matched: str        # Đoạn text khớp rule
    context: str = ""   # Dòng/đoạn context xung quanh
    auto_fixed: bool = False


# ─── Helper ──────────────────────────────────────────────────────────────────

def _find_matches(text: str, pattern: re.Pattern) -> list[tuple[int, str, str]]:
    """Trả về [(line_no, matched, context)] cho tất cả khớp của pattern."""
    results = []
    for m in pattern.finditer(text):
        line_no = text[:m.start()].count('\n') + 1
        # Context = dòng chứa match, cắt ngắn 80 ký tự
        line_start = text.rfind('\n', 0, m.start()) + 1
        line_end = text.find('\n', m.end())
        ctx = text[line_start: line_end if line_end > 0 else m.end() + 40].strip()[:80]
        results.append((line_no, m.group(0), ctx))
    return results


# ─── Detection rules (Markdown) ──────────────────────────────────────────────

_PAT_MJ001 = re.compile(r'\\lim\s*_\{')
_PAT_MJ002 = re.compile(r'\^\{\s*\\dfrac')
_PAT_GC001 = re.compile(r'^H[iì]nh\s*\d+\s*$', re.MULTILINE)
_PAT_GC002 = re.compile(r'^(##\s*Lời giải)\.\s*$', re.MULTILINE)
_PAT_PA001 = re.compile(r'^(?!##\s)Chọn\s+([A-Da-d])\b', re.MULTILINE)
_PAT_PA003 = re.compile(r'^##\s*Trả lời\s*:', re.MULTILINE | re.IGNORECASE)
_PAT_PA004 = re.compile(r'\\mathbf\{(\d+(?:\s+\d+)+)\}', re.IGNORECASE)


def _detect_pa002(text: str) -> list[Finding]:
    """PA002: Câu hỏi Phần I/III không có '## Lời giải' separator."""
    findings = []
    # Tách từng khối Câu
    for m in re.finditer(r'^Câu\s+(\d+)\s*[:\.]', text, re.MULTILINE):
        # Lấy block từ "Câu X:" đến "Câu X+1:" tiếp theo (hoặc hết file)
        block_start = m.start()
        next_cau = re.search(r'^Câu\s+\d+\s*[:\.]', text[m.end():], re.MULTILINE)
        block_end = m.end() + next_cau.start() if next_cau else len(text)
        block = text[block_start:block_end]

        has_separator = bool(re.search(r'##\s*(?:Lời giải|Đáp án)', block, re.IGNORECASE))
        if not has_separator:
            line_no = text[:block_start].count('\n') + 1
            findings.append(Finding(
                "PA002", line_no,
                matched=m.group(0).strip(),
                context=f"Câu {m.group(1)} không có '## Lời giải'"
            ))
    return findings


def detect_md(text: str, fix: bool = False) -> tuple[str, list[Finding]]:
    """Scan Markdown, trả về (text đã sửa hoặc gốc, danh sách findings)."""
    findings: list[Finding] = []

    # MJ001 — \lim_{ thiếu \limits
    for line_no, matched, ctx in _find_matches(text, _PAT_MJ001):
        findings.append(Finding("MJ001", line_no, matched, ctx))
    if fix and any(f.rule_id == "MJ001" for f in findings):
        text = re.sub(r'\\lim(\s*)_\{', r'\\lim\\limits_{', text)
        for f in findings:
            if f.rule_id == "MJ001":
                f.auto_fixed = True

    # MJ002 — ^{\dfrac trong mũ
    for line_no, matched, ctx in _find_matches(text, _PAT_MJ002):
        findings.append(Finding("MJ002", line_no, matched, ctx))
    if fix and any(f.rule_id == "MJ002" for f in findings):
        text = re.sub(r'\^\{\s*\\dfrac', r'^{\\frac', text)
        for f in findings:
            if f.rule_id == "MJ002":
                f.auto_fixed = True

    # GC001 — Orphan "Hình X"
    for line_no, matched, ctx in _find_matches(text, _PAT_GC001):
        findings.append(Finding("GC001", line_no, matched.strip(), ctx))
    if fix and any(f.rule_id == "GC001" for f in findings):
        text = _PAT_GC001.sub('', text)
        for f in findings:
            if f.rule_id == "GC001":
                f.auto_fixed = True

    # GC002 — "## Lời giải." có dấu chấm thừa
    for line_no, matched, ctx in _find_matches(text, _PAT_GC002):
        findings.append(Finding("GC002", line_no, matched.strip(), ctx))
    if fix and any(f.rule_id == "GC002" for f in findings):
        text = _PAT_GC002.sub(r'\1', text)
        for f in findings:
            if f.rule_id == "GC002":
                f.auto_fixed = True

    # PA001 — "Chọn X" thiếu "## "
    for line_no, matched, ctx in _find_matches(text, _PAT_PA001):
        findings.append(Finding("PA001", line_no, matched.strip(), ctx))
    if fix and any(f.rule_id == "PA001" for f in findings):
        text = re.sub(r'^(?!##\s)(Chọn\s+[A-Da-d]\b)', r'## \1', text, flags=re.MULTILINE)
        for f in findings:
            if f.rule_id == "PA001":
                f.auto_fixed = True

    # PA002 — Câu hỏi thiếu ## Lời giải (không auto-fix)
    findings.extend(_detect_pa002(text))

    # PA003 — "## Trả lời:" thay vì "## Đáp án:"
    for line_no, matched, ctx in _find_matches(text, _PAT_PA003):
        findings.append(Finding("PA003", line_no, matched.strip(), ctx))
    if fix and any(f.rule_id == "PA003" for f in findings):
        text = re.sub(r'^##\s*Trả lời\s*:', '## Đáp án:', text, flags=re.MULTILINE | re.IGNORECASE)
        for f in findings:
            if f.rule_id == "PA003":
                f.auto_fixed = True

    # PA004 — LaTeX số có khoảng trắng: \mathbf{4 8 0 4}
    for line_no, matched, ctx in _find_matches(text, _PAT_PA004):
        findings.append(Finding("PA004", line_no, matched, ctx))
    # PA004 không auto-fix vì ngữ cảnh phức tạp (có thể cần sửa cả dòng Đáp án)

    return text, findings


# ─── Detection rules (HTML) ──────────────────────────────────────────────────

_PAT_IM001 = re.compile(r'cdn\.mathpix\.com/[^\s"\']+')


def detect_html(text: str) -> list[Finding]:
    """Scan HTML output, trả về danh sách findings."""
    findings: list[Finding] = []

    # IM001 — cdn.mathpix.com còn sót trong HTML
    for line_no, matched, ctx in _find_matches(text, _PAT_IM001):
        findings.append(Finding("IM001", line_no, matched[:60], ctx))

    return findings


# ─── Report ──────────────────────────────────────────────────────────────────

_SEVERITY_LABEL = {
    "error":   "❌ ERROR ",
    "warning": "⚠️  WARN  ",
    "info":    "ℹ️  INFO  ",
}


def print_report(findings: list[Finding], library: dict, fix_mode: bool) -> int:
    """In báo cáo, trả về số lỗi ERROR chưa được sửa."""
    if not findings:
        print("  ✅ Không phát hiện lỗi.")
        return 0

    counts = {"error": 0, "warning": 0, "info": 0}
    unfixed_errors = 0

    for f in sorted(findings, key=lambda x: x.line_no):
        meta = library.get(f.rule_id, {})
        severity = meta.get("severity", "warning")
        counts[severity] += 1

        label = _SEVERITY_LABEL.get(severity, "⚠️  WARN  ")
        fixed_tag = " [ĐÃ SỬA ✓]" if f.auto_fixed else ""
        line_tag = f" @ dòng {f.line_no}" if f.line_no else ""

        print(f"  {label} {f.rule_id}{line_tag}{fixed_tag}")
        desc = meta.get("description", f.matched)
        print(f"            {desc}")
        if f.context and f.context != desc:
            snippet = f.context[:70]
            print(f"            → \"{snippet}\"")

        if not f.auto_fixed:
            if meta.get("auto_fixable"):
                print(f"            → Auto-fixable: chạy với --fix để tự động sửa")
            else:
                action = meta.get("suggested_action", "Sửa thủ công file Markdown")
                print(f"            → {action}")
            if severity == "error":
                unfixed_errors += 1
        print()

    total = sum(counts.values())
    print(f"  📊 {total} phát hiện: {counts['error']} lỗi | {counts['warning']} cảnh báo | {counts['info']} thông tin")
    if not fix_mode:
        fixable = sum(1 for f in findings if library.get(f.rule_id, {}).get("auto_fixable") and not f.auto_fixed)
        if fixable:
            print(f"  💡 {fixable} mục có thể tự động sửa — chạy lại với --fix")

    return unfixed_errors


# ─── Main ────────────────────────────────────────────────────────────────────

def load_library(path: Path) -> dict:
    if path.exists():
        with open(path, encoding='utf-8') as f:
            entries = json.load(f)
        return {e['id']: e for e in entries}
    return {}


def scan_exam_dir(exam_path: Path, library: dict, fix: bool) -> int:
    """Scan toàn bộ thư mục đề: MD trong 02_Process* + HTML trong 03_Outputs."""
    total_unfixed_errors = 0

    # MD files
    md_files = []
    for sub in ("02_Process", "02_Processing"):
        md_files.extend((exam_path / sub).glob("*_normalized.md"))

    for md_file in md_files:
        print(f"\n  📄 Scan Markdown: {md_file.name}")
        print("  " + "─" * 56)
        text = md_file.read_text(encoding='utf-8')
        fixed_text, findings = detect_md(text, fix=fix)
        total_unfixed_errors += print_report(findings, library, fix_mode=fix)

        if fix and fixed_text != text:
            md_file.write_text(fixed_text, encoding='utf-8')
            print(f"  💾 Đã lưu: {md_file.name}")

    # HTML output
    html_dir = exam_path / "03_Outputs"
    if html_dir.exists():
        for html_file in html_dir.glob("*_Unified.html"):
            print(f"\n  🌐 Scan HTML: {html_file.name}")
            print("  " + "─" * 56)
            text = html_file.read_text(encoding='utf-8', errors='replace')
            findings = detect_html(text)
            total_unfixed_errors += print_report(findings, library, fix_mode=False)

    return total_unfixed_errors


def main():
    parser = argparse.ArgumentParser(
        description="Detector lỗi OCR/Regex/MathJax cho đề thi Toán Cá Chép",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ví dụ:
  python error_detector.py 20260511_De_11_HKII_07
  python error_detector.py 20260511_De_11_HKII_07/02_Process/HKII_07_normalized.md --fix
  python error_detector.py 20260511_De_11_HKII_07/03_Outputs/De_11_HKII_07_Unified.html"""
    )
    parser.add_argument("target", help="Thư mục đề thi, file .md, hoặc file .html")
    parser.add_argument("--fix", action="store_true",
                        help="Tự động sửa các lỗi auto-fixable và lưu file")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    target = Path(args.target)
    # Hỗ trợ path tương đối từ thư mục Test_Web
    if not target.exists():
        alt = Path(__file__).parent / args.target
        if alt.exists():
            target = alt

    if not target.exists():
        print(f"❌ Không tìm thấy: {args.target}")
        sys.exit(2)

    script_dir = Path(__file__).parent
    library = load_library(script_dir / "error_library.json")

    print("=" * 60)
    print("  🔍 ERROR DETECTOR — TOÁN CÁ CHÉP")
    print("=" * 60)
    print(f"  Target  : {target}")
    print(f"  Mode    : {'FIX' if args.fix else 'SCAN ONLY'}")
    print(f"  Library : {len(library)} rules loaded")

    total_unfixed_errors = 0

    if target.is_dir():
        total_unfixed_errors = scan_exam_dir(target, library, fix=args.fix)
    elif target.suffix.lower() == ".md":
        print(f"\n  📄 Scan Markdown: {target.name}")
        print("  " + "─" * 56)
        text = target.read_text(encoding='utf-8')
        fixed_text, findings = detect_md(text, fix=args.fix)
        total_unfixed_errors += print_report(findings, library, fix_mode=args.fix)
        if args.fix and fixed_text != text:
            target.write_text(fixed_text, encoding='utf-8')
            print(f"  💾 Đã lưu: {target.name}")
    elif target.suffix.lower() in (".html", ".htm"):
        print(f"\n  🌐 Scan HTML: {target.name}")
        print("  " + "─" * 56)
        text = target.read_text(encoding='utf-8', errors='replace')
        findings = detect_html(text)
        total_unfixed_errors += print_report(findings, library, fix_mode=False)
    else:
        print(f"❌ File không được hỗ trợ: {target.suffix} (cần .md hoặc .html)")
        sys.exit(2)

    print()
    print("=" * 60)
    if total_unfixed_errors == 0:
        print("  ✅ PASS — Không có lỗi nghiêm trọng chưa sửa.")
    else:
        print(f"  ❌ FAIL — {total_unfixed_errors} lỗi ERROR cần xử lý thủ công.")
    print("=" * 60)

    sys.exit(1 if total_unfixed_errors > 0 else 0)


if __name__ == "__main__":
    main()
