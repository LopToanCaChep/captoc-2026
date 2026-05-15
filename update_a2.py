import sys

f = r'c:\Users\huyds\OneDrive\2. PARA\1 - Projects\CaChep_Ecosystem\02_Distribution\List_Captoc_Web\A2_denha.html'

with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

target = """    icon: '📮',
    iconStyle: 'blue'
  }
];"""

replacement = """    icon: '📮',
    iconStyle: 'blue'
  },
  {
    id: 'PHIEU_LD03',
    file: 'phieu/phieu_ld03.html',
    hasPassword: false,
    title: 'Phiếu Tô - Đề 03',
    loai: 'phieu',
    buoi: 3,
    questions: 22,
    duration: 0,
    icon: '📮',
    iconStyle: 'blue'
  }
];"""

content = content.replace(target, replacement)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(content)
print('Done updating A2_denha.html')
