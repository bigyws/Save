"""검토용 엑셀 파일 만들기: python3 make_xlsx.py <출력 경로> [시트 이름 앞에 붙일 말]"""
import json, sys, collections, datetime, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
here = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(here, "../data/verses-365.json"), encoding="utf-8"))
CAL = json.load(open(os.path.join(here, "../data/calendar.json"), encoding="utf-8"))
out = sys.argv[1]; pre = sys.argv[2] if len(sys.argv) > 2 else ""
fill = PatternFill("solid", fgColor="F1ECE2")
def header(ws):
    for c in ws[1]: c.fill = fill; c.font = Font(bold=True)
def widths(ws, w):
    for k, v in w.items(): ws.column_dimensions[k].width = v
def wrap(ws, cols):
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(vertical="top", wrap_text=c.column_letter in cols)

wb = Workbook(); ws = wb.active; ws.title = pre + "365 말씀"
ws.append(["Day", "날짜", "월", "주제", "구절", "개역한글", "그림 주제(제안)", "검토", "메모", "English (KJV)", "日本語 (口語訳)", "中文 (和合本 简体)", "Reference", "参照", "出处"])
for r in D["verses"]:
    ws.append([r["day"], r["date_ko"], r["month"], r["theme"], r["ref_ko"], r["ko"], r["motif"], None, None, r["en"], r["ja"], r["zh"], r["ref_en"], r["ref_ja"], r["ref_zh"]])
header(ws); wrap(ws, "FJKL"); ws.freeze_panes = "F2"
widths(ws, {"A": 6, "B": 9, "C": 6, "D": 13, "E": 18, "F": 52, "G": 16, "H": 9, "I": 18, "J": 48, "K": 44, "L": 38, "M": 18, "N": 22, "O": 16})

ws = wb.create_sheet(pre + "특별 카드")
ws.append(["카드", "보여주는 날", "구절", "개역한글", "그림 주제(제안)", "검토", "메모", "English (KJV)", "日本語 (口語訳)", "中文 (和合本 简体)"])
for s in D["specials"]:
    ws.append([s["name"], s["when"], s["ref_ko"], s["ko"], s["motif"], None, None, s["en"], s["ja"], s["zh"]])
header(ws); wrap(ws, "BDHIJ"); ws.freeze_panes = "B2"
widths(ws, {"A": 14, "B": 24, "C": 16, "D": 52, "E": 16, "F": 9, "G": 18, "H": 48, "I": 44, "J": 38})

ws = wb.create_sheet(pre + "절기 날짜")
ws.append(["연도", "부활절", "맥추감사절", "추수감사절"])
for y, v in CAL["years"].items():
    ws.append([int(y)] + [datetime.date.fromisoformat(v[k]) for k in ("easter", "harvest", "thanksgiving")])
for row in ws.iter_rows(min_row=2, min_col=2):
    for c in row: c.number_format = "yyyy-mm-dd (aaa)"
header(ws); widths(ws, {"A": 8, "B": 18, "C": 18, "D": 18})

ws = wb.create_sheet(pre + "월별 주제")
ws.append(["월", "주제", "날짜", "일수"])
g = collections.OrderedDict()
for r in D["verses"]: g.setdefault((r["month"], r["theme"]), []).append(r)
for (m, t), rs in g.items(): ws.append([m, t, f'{rs[0]["date_ko"]} ~ {rs[-1]["date_ko"]}', len(rs)])
header(ws); widths(ws, {"A": 8, "B": 16, "C": 22, "D": 8})

ws = wb.create_sheet(pre + "그림 주제")
ws.append(["그림 주제(제안)", "구절 수"])
for k, v in collections.Counter(r["motif"] for r in D["verses"] + D["specials"]).most_common(): ws.append([k, v])
header(ws); widths(ws, {"A": 22, "B": 10})

ws = wb.create_sheet(pre + "안내")
for line in [
    ["말씀 키링 365 · 구절 목록 초안"], [],
    ["보여주는 방식", "매년 같은 날짜에 같은 구절이 나옵니다 (평년 365일 기준). 온 교회가 같은 날 같은 말씀을 받습니다."],
    ["특별 카드", "부활절·맥추감사절·추수감사절 주일에는 그날의 구절 대신 특별 카드가 나옵니다. 윤년 2월 29일에는 윤년 카드, 키링을 처음 댄 날에는 첫 만남 카드가 먼저 나옵니다."],
    ["절기 날짜", "부활절은 자동으로 계산됩니다. 맥추감사절은 7월 첫째 주일, 추수감사절은 11월 셋째 주일로 넣어 두었습니다. 교회에서 다른 날로 지키면 '절기 날짜' 시트에서 그 해 날짜를 고쳐 주세요."],
    ["번역본", "한국어 개역한글(1961) · English King James Version · 日本語 口語訳(1955) · 中文 和合本(简体, 번체 원문을 간체로 변환)"],
    ["본문 출처", "scrollmapper/bible_databases (KorRV, KJV, ChiUn), metastable-void/ja-colloquial (口語訳, CC0)"],
    ["본문 처리", "시편 1절 앞의 제목(예: 다윗의 시)은 뺐고, 일본어·중국어는 절로 끊으며 짝이 안 맞게 된 따옴표만 지웠습니다. 그 외 본문은 원문 그대로입니다."],
    ["그림 주제", "구절의 낱말(목자, 독수리, 등불 등)로 자동 제안한 것입니다. 바꿔도 됩니다."],
    ["검토 방법", "검토 칸에서 확정 / 교체 / 보류를 고르고, 교체할 구절이나 의견은 메모 칸에 적어 주세요."],
]: ws.append(line)
ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 110; ws["A1"].font = Font(bold=True, size=13)
wb.save(out); print(out)
