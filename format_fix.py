import re

f_path = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html'
with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix 0<x<20 in Câu I_6
# We know it's "0<x<20"
content = content.replace("0<x<20", "0&lt;x&lt;20")

# 2. Fix True/False format
# Match "## a) ĐÚNG" or "## b) SAI" etc.
def repl(match):
    letter = match.group(1)
    status = match.group(2)
    color = "#22c55e" if status == "ĐÚNG" else "#ef4444"
    return f'<br/><b>{letter}) <span style="color:{color}; font-weight:900">{status}</span></b><br/>'

content = re.sub(r'## ([a-d])\) (ĐÚNG|SAI)', repl, content)

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Format fixes applied successfully.")
