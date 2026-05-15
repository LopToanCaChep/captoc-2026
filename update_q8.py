import sys
import re

# 1. Update CT_02.html
f1 = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html'
with open(f1, 'r', encoding='utf-8') as f:
    content1 = f.read()

sol_text = r'''<b>Lời giải:</b><br/>
Dựa vào đồ thị hàm số \(y=f(x)\) đã cho, ta xác định các điểm cực trị như sau:<br/>
- Đồ thị chuyển từ đồng biến sang nghịch biến (tạo thành đỉnh) tại điểm có tọa độ \((2; 3)\). Do đó, điểm cực đại của đồ thị hàm số là \(M(2; 3)\).<br/>
- Đồ thị chuyển từ nghịch biến sang đồng biến (tạo thành đáy) tại điểm có tọa độ \((0; -1)\). Do đó, điểm cực tiểu của đồ thị hàm số là \((0; -1)\).<br/>
Đề bài hỏi "Điểm cực đại của hàm số" (tức là hoành độ \(x\) của điểm cực đại), suy ra ta có \(x=2\).<br/>
*(Lưu ý: Nếu đề hỏi "Giá trị cực đại của hàm số" thì đáp án là \(y=3\), còn "Điểm cực đại của đồ thị hàm số" thì đáp án là \(M(2;3)\)).*
<br/><b>→ Đáp án B.</b>'''

pattern = r'(<div class="card" data-answer=")[A-D](">.*?<div class="q-badge">CÂU 8</div>.*?)<div class="sol-inner" style="white-space: pre-wrap;">.*?</div></div>'
match = re.search(pattern, content1, flags=re.DOTALL)
if match:
    new_block = match.group(1) + 'B' + match.group(2) + f'<div class="sol-inner" style="white-space: pre-wrap;">\n{sol_text}\n</div></div>'
    content1 = content1[:match.start()] + new_block + content1[match.end():]

old_js_arr = "const p1Ans = ['A', 'C', 'C', 'D', 'B', 'C', 'D', 'A', 'A', 'D', 'B', 'C'];"
new_js_arr = "const p1Ans = ['A', 'C', 'C', 'D', 'B', 'C', 'D', 'B', 'A', 'D', 'B', 'C'];"
content1 = content1.replace(old_js_arr, new_js_arr)

with open(f1, 'w', encoding='utf-8') as f:
    f.write(content1)

# 2. Update phieu_ld02.html
f2 = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\phieu\phieu_ld02.html'
with open(f2, 'r', encoding='utf-8') as f:
    content2 = f.read()

old_config_arr = "const ANS_P1=['A','C','C','D','B','C','D','A','A','D','B','C'];"
new_config_arr = "const ANS_P1=['A','C','C','D','B','C','D','B','A','D','B','C'];"
content2 = content2.replace(old_config_arr, new_config_arr)

with open(f2, 'w', encoding='utf-8') as f:
    f.write(content2)

print("Updates applied to CT_02.html and phieu_ld02.html successfully.")
