import sys

with open('phieu/phieu_ld01.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<title>Phiếu Trả Lời — LD01</title>', '<title>Phiếu Trả Lời — LD03</title>')
text = text.replace('Cấp Tốc — Đề 01 (LD01)', 'Cấp Tốc — Đề 03 (LD03)')

old_config = """const EXAM_ID='LD01', EXAM_LOAI='tren_lop', EXAM_BUOI=1;
const ANS_P1=['C','B','B','A','A','B','C','A','D','D','C','D'];
const ANS_P2={1:{a:'D',b:'S',c:'D',d:'D'},2:{a:'S',b:'D',c:'D',d:'D'},3:{a:'D',b:'S',c:'D',d:'S'},4:{a:'D',b:'D',c:'S',d:'D'}};
const ANS_P3=['11.7','0.17','90','120','9.76','9'];"""

new_config = """const EXAM_ID='LD03', EXAM_LOAI='phieu', EXAM_BUOI=3;
const ANS_P1=['A','C','B','D','D','B','C','B','A','A','A','A'];
const ANS_P2={1:{a:'S',b:'S',c:'S',d:'D'},2:{a:'D',b:'D',c:'S',d:'S'},3:{a:'D',b:'S',c:'D',d:'D'},4:{a:'S',b:'D',c:'D',d:'D'}};
const ANS_P3=['49','15','0.5','12','23','1042'];"""

text = text.replace(old_config, new_config)

with open('phieu/phieu_ld03.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done phieu_ld03')
