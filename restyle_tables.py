import sys

table1_html_old = """<div class="table-wrap" style="overflow-x:auto; margin: 12px 0;">
<table style="width:100%; border-collapse: collapse; text-align: center; border: 2px solid #cbd5e1;">
  <thead>
    <tr style="background:#f8fafc; font-weight:bold;">
      <td style="padding: 10px; border: 1px solid #cbd5e1;">Đường kính \\((\\mathrm{cm})\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([40 ; 45)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([45 ; 50)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([50 ; 55)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([55 ; 60)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([60 ; 65)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([65 ; 70)\\)</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight:bold; background:#f8fafc;">Tần số</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">5</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">20</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">18</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">7</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">3</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">1</td>
    </tr>
  </tbody>
</table>
</div>"""

table1_html_new = """<div class="table-wrap" style="overflow-x:auto; margin: 12px 0;">
<table style="width:100%; border-collapse: collapse; text-align: center; border: 3px solid #003B99; background: #F7C800; color: #003B99;">
  <thead>
    <tr style="font-weight:bold; border-bottom: 3px solid #003B99;">
      <td style="padding: 10px; border: 2px solid #003B99;">Đường kính \\((\\mathrm{cm})\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([40 ; 45)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([45 ; 50)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([50 ; 55)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([55 ; 60)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([60 ; 65)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([65 ; 70)\\)</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 2px solid #003B99; font-weight:bold;">Tần số</td>
      <td style="padding: 10px; border: 2px solid #003B99;">5</td>
      <td style="padding: 10px; border: 2px solid #003B99;">20</td>
      <td style="padding: 10px; border: 2px solid #003B99;">18</td>
      <td style="padding: 10px; border: 2px solid #003B99;">7</td>
      <td style="padding: 10px; border: 2px solid #003B99;">3</td>
      <td style="padding: 10px; border: 2px solid #003B99;">1</td>
    </tr>
  </tbody>
</table>
</div>"""

table2_html_old = """<div class="table-wrap" style="overflow-x:auto; margin: 12px 0;">
<table style="width:100%; border-collapse: collapse; text-align: center; border: 2px solid #cbd5e1;">
  <thead>
    <tr style="background:#f8fafc; font-weight:bold;">
      <td style="padding: 10px; border: 1px solid #cbd5e1;">Thời gian (phút)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([30 ; 50)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([50 ; 70)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([70 ; 90)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([90 ; 110)\\)</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">\\([110 ; 130)\\)</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight:bold; background:#f8fafc;">CLB Yoga</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">2</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">3</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">6</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">3</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">2</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight:bold; background:#f8fafc;">CLB Gym</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">4</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">1</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">6</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">1</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">4</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight:bold; background:#f8fafc;">Tông số</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">6</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">4</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">12</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">4</td>
      <td style="padding: 10px; border: 1px solid #cbd5e1;">6</td>
    </tr>
  </tbody>
</table>
</div>"""

table2_html_new = """<div class="table-wrap" style="overflow-x:auto; margin: 12px 0; border-radius: 8px; overflow: hidden; border: 3px solid #003B99; box-shadow: 2px 2px 0px #003B99;">
<table style="width:100%; border-collapse: collapse; text-align: center; background: #F7C800; color: #003B99;">
  <thead>
    <tr style="font-weight:bold; border-bottom: 3px solid #003B99;">
      <td style="padding: 10px; border: 2px solid #003B99;">Thời gian (phút)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([30 ; 50)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([50 ; 70)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([70 ; 90)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([90 ; 110)\\)</td>
      <td style="padding: 10px; border: 2px solid #003B99;">\\([110 ; 130)\\)</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px; border: 2px solid #003B99; font-weight:bold;">CLB Yoga</td>
      <td style="padding: 10px; border: 2px solid #003B99;">2</td>
      <td style="padding: 10px; border: 2px solid #003B99;">3</td>
      <td style="padding: 10px; border: 2px solid #003B99;">6</td>
      <td style="padding: 10px; border: 2px solid #003B99;">3</td>
      <td style="padding: 10px; border: 2px solid #003B99;">2</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 2px solid #003B99; font-weight:bold;">CLB Gym</td>
      <td style="padding: 10px; border: 2px solid #003B99;">4</td>
      <td style="padding: 10px; border: 2px solid #003B99;">1</td>
      <td style="padding: 10px; border: 2px solid #003B99;">6</td>
      <td style="padding: 10px; border: 2px solid #003B99;">1</td>
      <td style="padding: 10px; border: 2px solid #003B99;">4</td>
    </tr>
    <tr>
      <td style="padding: 10px; border: 2px solid #003B99; font-weight:bold;">Tông số</td>
      <td style="padding: 10px; border: 2px solid #003B99;">6</td>
      <td style="padding: 10px; border: 2px solid #003B99;">4</td>
      <td style="padding: 10px; border: 2px solid #003B99;">12</td>
      <td style="padding: 10px; border: 2px solid #003B99;">4</td>
      <td style="padding: 10px; border: 2px solid #003B99;">6</td>
    </tr>
  </tbody>
</table>
</div>"""

files = [
    r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\01_Kho_De_Goc\CT_02.html',
    r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\01_Factory\Test_Web\20250515_CT_02\03_Outputs\02_Unified.html'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace(table1_html_old, table1_html_new.replace('<div class="table-wrap" style="overflow-x:auto; margin: 12px 0;">\n<table style="width:100%; border-collapse: collapse; text-align: center; border: 3px solid #003B99; background: #F7C800; color: #003B99;">', '<div class="table-wrap" style="overflow-x:auto; margin: 12px 0; border-radius: 8px; overflow: hidden; border: 3px solid #003B99; box-shadow: 2px 2px 0px #003B99;">\n<table style="width:100%; border-collapse: collapse; text-align: center; background: #F7C800; color: #003B99;">'))
    content = content.replace(table2_html_old, table2_html_new)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Tables style updated!")
