import re

f_path = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html'
with open(f_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace II_2
pattern2 = r'Bảng biến thiên\n\\\(x\\\):.*?\\\(-\\\infty\\\)\s*\|\s*'
replacement2 = r'Bảng biến thiên:<br/>\n<div class="img-box" style="margin-top:8px"><img src="../Pic/CT_02_II_2_BBT.png" style="max-width:100%; border-radius:8px;"/></div>\n'

# Wait, regex might be tricky. Let's use exact string replacement
text2 = r'''Bảng biến thiên
\(x\): \(-\infty\) | 1 |  | 2 | 3 | \(+\infty\) |
\(y^{\prime}\): | - | 0 | + | + | 0 | -
\(y\): \(+\infty\) |  | \({ }+\infty\) |  |  |  |
: |  |  | \(-\infty\) |  |  |'''
img2 = r'''Bảng biến thiên:<br/>
<div class="img-box" style="margin-top:8px; text-align:center;"><img src="../Pic/CT_02_II_2_BBT.png" style="max-width:100%; border-radius:8px;"/></div>'''

text3 = r'''Ta có bảng biến thiên
\(x\): 0 | 20 | \(+\infty\)
\(L^{\prime}(x)\): + | 0 | -
\(L(x)\): |  |'''
img3 = r'''Ta có bảng biến thiên:<br/>
<div class="img-box" style="margin-top:8px; text-align:center;"><img src="../Pic/CT_02_II_3_BBT.png" style="max-width:100%; border-radius:8px;"/></div>'''

content = content.replace(text2, img2)
content = content.replace(text3, img3)

with open(f_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("BBT images inserted successfully.")
