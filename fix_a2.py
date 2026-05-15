import sys

f = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\A2_denha.html'

with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

content = content.replace("""    iconStyle: 'orange'
  }
  {
    id: 'PHIEU_LD01',""", """    iconStyle: 'orange'
  }
];

/* ========== PHIẾU CONFIG (Không bị Robot ghi đè) ========== */
const PHIEUS = [
  {
    id: 'PHIEU_LD01',""")

old_duplicate = """    iconStyle: 'blue'
  },
  {
    id: 'LD02',
    file: null,
    hasPassword: true,
    title: 'Cấp Tốc - Đề 02',
    loai: 've_nha',
    buoi: 2,
    questions: 22,
    duration: 0,
    icon: '02',
    iconStyle: 'blue'
  }
];"""

new_ending = """    iconStyle: 'blue'
  }
];"""

content = content.replace(old_duplicate, new_ending)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(content)
print('Fixed A2_denha.html')
