import sys
import re

file_path = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the updates for each question
updates = {
    1: {
        'answer': 'A',
        'sol': r'''<b>Lời giải:</b><br/>
Phương trình đường tròn \((C)\) có dạng tổng quát là \((x - a)^2 + (y - b)^2 = R^2\), với \(I(a;b)\) là tâm và \(R\) là bán kính.<br/>
Đối chiếu với phương trình đề bài cho: \((x+2)^2 + (y-3)^2 = 5\), ta có thể viết lại thành \((x - (-2))^2 + (y - 3)^2 = (\sqrt{5})^2\).<br/>
Từ đó ta suy ra: \(\begin{cases} a = -2 \\ b = 3 \\ R = \sqrt{5} \end{cases}\).<br/>
Vậy đường tròn \((C)\) có tâm \(I(-2; 3)\) và bán kính \(R = \sqrt{5}\).
<br/><b>→ Đáp án A.</b>'''
    },
    2: {
        'answer': 'C',
        'sol': r'''<b>Lời giải:</b><br/>
Tập xác định của hàm số là \(D = \mathbb{R} \setminus \{-c\}\).<br/>
Quan sát đồ thị hàm số, ta thấy:<br/>
- Đồ thị có đường tiệm cận đứng là \(x = 2\). Do đó, nghiệm của mẫu số \(x + c = 0\) phải là \(x = 2 \Rightarrow 2 + c = 0 \Leftrightarrow c = -2\).<br/>
- Đồ thị có đường tiệm cận ngang là \(y = 1\). Mặt khác, từ hàm số \(y = \dfrac{ax+2}{x+c}\), ta tính được tiệm cận ngang \(y = \dfrac{a}{1} = a\). Suy ra \(a = 1\).<br/>
Vậy ta có \(a = 1, c = -2\). Giá trị biểu thức \(P = 2a - c = 2(1) - (-2) = 4\).
<br/><b>→ Đáp án C.</b>'''
    },
    3: {
        'answer': 'C',
        'sol': r'''<b>Lời giải:</b><br/>
Áp dụng quy tắc hình hộp cho hình hộp \(ABCD.A'B'C'D'\), ta có: Véctơ đường chéo xuất phát từ một đỉnh bằng tổng ba véctơ cạnh xuất phát từ đỉnh đó.<br/>
Do đó, khi xét tại đỉnh \(D\), đường chéo không gian là đoạn \(DB'\). Tổng ba véctơ cạnh xuất phát từ \(D\) là \(\overrightarrow{DA}\), \(\overrightarrow{DC}\) và \(\overrightarrow{DD'}\).<br/>
Suy ra hệ thức đúng là: \(\overrightarrow{DB'} = \overrightarrow{DA} + \overrightarrow{DC} + \overrightarrow{DD'}\).
<br/><b>→ Đáp án C.</b>'''
    },
    4: {
        'answer': 'D',
        'sol': r'''<b>Lời giải:</b><br/>
Giả sử điểm \(M\) có tọa độ \(M(x; y; z)\).<br/>
- Hình chiếu vuông góc của \(M\) lên mặt phẳng \((Oxy)\) (mặt phẳng có phương trình \(z=0\)) là điểm \(M_1(x; y; 0)\). Theo đề bài \(M_1(-2; 3; 0)\), suy ra \(x = -2\) và \(y = 3\).<br/>
- Hình chiếu vuông góc của \(M\) lên mặt phẳng \((Oxz)\) (mặt phẳng có phương trình \(y=0\)) là điểm \(M_2(x; 0; z)\). Theo đề bài \(M_2(-2; 0; 5)\), suy ra \(z = 5\).<br/>
Kết hợp lại, ta được tọa độ điểm \(M\) là \(M(-2; 3; 5)\).
<br/><b>→ Đáp án D.</b>'''
    },
    5: {
        'answer': 'B',
        'sol': r'''<b>Lời giải:</b><br/>
Áp dụng công thức tính cosin góc giữa hai véctơ \(\vec{a}\) và \(\vec{b}\):<br/>
\(\cos (\vec{a}, \vec{b}) = \dfrac{\vec{a} \cdot \vec{b}}{|\vec{a}| \cdot |\vec{b}|} = \dfrac{x_1x_2 + y_1y_2 + z_1z_2}{\sqrt{x_1^2 + y_1^2 + z_1^2} \cdot \sqrt{x_2^2 + y_2^2 + z_2^2}}\)<br/>
\(\Rightarrow \cos (\vec{a}, \vec{b}) = \dfrac{1 \cdot (-2) + (-2) \cdot 1 + 1 \cdot 1}{\sqrt{1^2 + (-2)^2 + 1^2} \cdot \sqrt{(-2)^2 + 1^2 + 1^2}}\)<br/>
\(\Rightarrow \cos (\vec{a}, \vec{b}) = \dfrac{-2 - 2 + 1}{\sqrt{6} \cdot \sqrt{6}} = \dfrac{-3}{6} = -\dfrac{1}{2}\).<br/>
Vì \(\cos (\vec{a}, \vec{b}) = -\dfrac{1}{2}\) nên góc \((\vec{a}, \vec{b}) = 120^\circ\).
<br/><b>→ Đáp án B.</b>'''
    },
    6: {
        'answer': 'C',
        'sol': r'''<b>Lời giải:</b><br/>
Gọi độ dài cạnh hình vuông nhỏ bị cắt ở bốn góc là \(x \text{ (cm)}\), với điều kiện \(0 < x < 20\).<br/>
Khi gấp tấm bìa lại, ta được một hình hộp chữ nhật không nắp có:<br/>
- Kích thước đáy là hình vuông cạnh: \(40 - 2x \text{ (cm)}\).<br/>
- Chiều cao của hình hộp là: \(x \text{ (cm)}\).<br/>
Thể tích của khối hộp là: \(V(x) = (40 - 2x)^2 \cdot x = 4x^3 - 160x^2 + 1600x\).<br/>
Xét hàm số \(V(x)\) trên khoảng \((0; 20)\), ta có đạo hàm:<br/>
\(V'(x) = 12x^2 - 320x + 1600\).<br/>
Cho \(V'(x) = 0 \Leftrightarrow \left[\begin{array}{l} x = 20 \text{ (loại vì không thỏa mãn } 0<x<20) \\ x = \dfrac{20}{3} \text{ (thỏa mãn)} \end{array}\right.\)<br/>
Lập bảng biến thiên, ta thấy hàm số đạt giá trị lớn nhất tại \(x = \dfrac{20}{3}\).<br/>
Vậy để thể tích hộp lớn nhất thì độ dài cạnh hình vuông bị cắt là \(\dfrac{20}{3} \text{ (cm)}\).
<br/><b>→ Đáp án C.</b>'''
    },
    7: {
        'answer': 'D',
        'sol': r'''<b>Lời giải:</b><br/>
Ta xét từng phương án:<br/>
- Phương án A: Hàm số mũ \(y = \left(\dfrac{2026}{2025}\right)^x\) có cơ số \(a = \dfrac{2026}{2025} > 1\) nên đồng biến trên toàn \(\mathbb{R}\).<br/>
- Phương án B: Hàm số lôgarit \(y = \log_{\frac{1}{2}} x\) có cơ số \(a = \dfrac{1}{2} < 1\) nên nghịch biến, nhưng tập xác định chỉ là \((0; +\infty)\) chứ không phải trên \(\mathbb{R}\).<br/>
- Phương án C: Hàm số phân thức \(y = \dfrac{2x-1}{x-1}\) có tập xác định \(D = \mathbb{R} \setminus \{1\}\), hàm số bị gián đoạn tại \(x=1\) nên không thể nghịch biến trên \(\mathbb{R}\).<br/>
- Phương án D: Hàm số \(y = e^{-x} = \left(\dfrac{1}{e}\right)^x\) là hàm số mũ có tập xác định \(D = \mathbb{R}\). Cơ số \(a = \dfrac{1}{e} < 1\) nên hàm số nghịch biến trên \(\mathbb{R}\).<br/>
Vậy hàm số \(y=e^{-x}\) thỏa mãn yêu cầu bài toán.
<br/><b>→ Đáp án D.</b>'''
    },
    8: {
        'answer': 'A',
        'sol': r'''<b>Lời giải:</b><br/>
Dựa vào đồ thị hàm số \(y=f(x)\) đã cho, ta xác định các điểm cực trị như sau:<br/>
- Đồ thị có một điểm "đỉnh đồi" (chuyển từ đồng biến sang nghịch biến) tại vị trí có hoành độ \(x=0\), tung độ \(y=3\). Điểm này gọi là điểm cực đại.<br/>
- Đồ thị có một điểm "vực sâu" (chuyển từ nghịch biến sang đồng biến) tại vị trí có hoành độ \(x=2\), tung độ \(y=-1\). Điểm này gọi là điểm cực tiểu.<br/>
Đề bài hỏi "Điểm cực đại của hàm số" (tức là giá trị \(x\) của điểm cực đại), do đó ta có \(x=0\).<br/>
*(Lưu ý: Nếu đề hỏi "Giá trị cực đại của hàm số" thì mới khoanh \(y=3\), còn "Điểm cực đại của đồ thị hàm số" thì phải có cả tọa độ \(M(0;3)\)).*
<br/><b>→ Đáp án A.</b>'''
    },
    9: {
        'answer': 'A',
        'sol': r'''<b>Lời giải:</b><br/>
Từ bảng thống kê, ta thấy:<br/>
- Nhóm số liệu đầu tiên là \([40; 45)\), có đầu mút trái \(a_{min} = 40\).<br/>
- Nhóm số liệu cuối cùng là \([65; 70)\), có đầu mút phải \(a_{max} = 70\).<br/>
Khoảng biến thiên của mẫu số liệu ghép nhóm được tính bằng hiệu số giữa đầu mút phải của nhóm cuối cùng và đầu mút trái của nhóm đầu tiên.<br/>
Do đó, \(R = a_{max} - a_{min} = 70 - 40 = 30\).
<br/><b>→ Đáp án A.</b>'''
    },
    10: {
        'answer': 'D',
        'sol': r'''<b>Lời giải:</b><br/>
Tập xác định của hàm số phân thức là \(D = \mathbb{R} \setminus \{1\}\).<br/>
Để tìm tiệm cận đứng, ta xét giới hạn của hàm số khi \(x\) tiến về nghiệm của mẫu số (\(x=1\)):<br/>
Ta có \(\lim\limits_{x \rightarrow 1^{+}} y = \lim\limits_{x \rightarrow 1^{+}} \dfrac{2x+3}{x-1} = +\infty\) (vì tử số \(2(1)+3 = 5 > 0\) và mẫu số \(x-1\) mang dấu dương khi \(x \rightarrow 1^{+}\)).<br/>
Theo định nghĩa, do tồn tại ít nhất một giới hạn một bên bằng vô cực nên đường thẳng \(x = 1\) chính là đường tiệm cận đứng của đồ thị hàm số.
<br/><b>→ Đáp án D.</b>'''
    }
}

# The slides for questions 1 to 10 correspond to CÂU 1 to CÂU 10 in PHẦN I
for q_num, data in updates.items():
    # Find the block for this question
    # We look for <div class="q-badge">CÂU X</div>
    pattern = rf'(<div class="card" data-answer=")[A-D](">.*?<div class="q-badge">CÂU {q_num}</div>.*?)<div class="sol-inner" style="white-space: pre-wrap;">.*?</div></div>'
    
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        # replace data-answer
        new_block = match.group(1) + data['answer'] + match.group(2) + f'<div class="sol-inner" style="white-space: pre-wrap;">\n{data["sol"]}\n</div></div>'
        content = content[:match.start()] + new_block + content[match.end():]
    else:
        print(f"Failed to find block for Question {q_num}")

# Now update the hardcoded JS array: const p1Ans = ['A', 'C', 'C', 'B', 'D', 'B', 'C', 'C', 'C', 'A', 'B', 'C'];
# We want it to be: const p1Ans = ['A', 'C', 'C', 'D', 'B', 'C', 'D', 'A', 'A', 'D', 'B', 'C'];
old_js_arr = "const p1Ans = ['A', 'C', 'C', 'B', 'D', 'B', 'C', 'C', 'C', 'A', 'B', 'C'];"
new_js_arr = "const p1Ans = ['A', 'C', 'C', 'D', 'B', 'C', 'D', 'A', 'A', 'D', 'B', 'C'];"
if old_js_arr in content:
    content = content.replace(old_js_arr, new_js_arr)
else:
    print("Failed to find JS p1Ans array")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updates applied to CT_02.html successfully.")
