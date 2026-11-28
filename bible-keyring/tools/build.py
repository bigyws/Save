"""365일 말씀 데이터 만들기.
공개 성경 데이터(scrollmapper/bible_databases: KorRV, KJV, JapKougo, ChiUn)에서
refs.py의 구절을 뽑아 data/verses-365.json, data/verses-365.csv 를 만듭니다.
사용: python3 build.py <성경 JSON 폴더>
"""
import json, sys, re, csv, os
from opencc import OpenCC
from refs import MONTHS, SPECIALS
import datetime

CODES = "Gen Exo Lev Num Deu Jos Jdg Rut 1Sa 2Sa 1Ki 2Ki 1Ch 2Ch Ezr Neh Est Job Psa Pro Ecc Sng Isa Jer Lam Eze Dan Hos Joe Amo Oba Jon Mic Nah Hab Zep Hag Zec Mal Mat Mar Luk Joh Act Rom 1Co 2Co Gal Eph Phi Col 1Th 2Th 1Ti 2Ti Tit Phm Heb Jas 1Pe 2Pe 1Jo 2Jo 3Jo Jud Rev".split()
KO = "창세기 출애굽기 레위기 민수기 신명기 여호수아 사사기 룻기 사무엘상 사무엘하 열왕기상 열왕기하 역대상 역대하 에스라 느헤미야 에스더 욥기 시편 잠언 전도서 아가 이사야 예레미야 예레미야애가 에스겔 다니엘 호세아 요엘 아모스 오바댜 요나 미가 나훔 하박국 스바냐 학개 스가랴 말라기 마태복음 마가복음 누가복음 요한복음 사도행전 로마서 고린도전서 고린도후서 갈라디아서 에베소서 빌립보서 골로새서 데살로니가전서 데살로니가후서 디모데전서 디모데후서 디도서 빌레몬서 히브리서 야고보서 베드로전서 베드로후서 요한일서 요한이서 요한삼서 유다서 요한계시록".split()
EN = ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth","1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther","Job","Psalm","Proverbs","Ecclesiastes","Song of Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians","1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon","Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]
JA = "創世記 出エジプト記 レビ記 民数記 申命記 ヨシュア記 士師記 ルツ記 サムエル記上 サムエル記下 列王紀上 列王紀下 歴代志上 歴代志下 エズラ記 ネヘミヤ記 エステル記 ヨブ記 詩篇 箴言 伝道の書 雅歌 イザヤ書 エレミヤ書 哀歌 エゼキエル書 ダニエル書 ホセア書 ヨエル書 アモス書 オバデヤ書 ヨナ書 ミカ書 ナホム書 ハバクク書 ゼパニヤ書 ハガイ書 ゼカリヤ書 マラキ書 マタイによる福音書 マルコによる福音書 ルカによる福音書 ヨハネによる福音書 使徒行伝 ローマ人への手紙 コリント人への第一の手紙 コリント人への第二の手紙 ガラテヤ人への手紙 エペソ人への手紙 ピリピ人への手紙 コロサイ人への手紙 テサロニケ人への第一の手紙 テサロニケ人への第二の手紙 テモテへの第一の手紙 テモテへの第二の手紙 テトスへの手紙 ピレモンへの手紙 ヘブル人への手紙 ヤコブの手紙 ペテロの第一の手紙 ペテロの第二の手紙 ヨハネの第一の手紙 ヨハネの第二の手紙 ヨハネの第三の手紙 ユダの手紙 ヨハネの黙示録".split()
ZH = "创世记 出埃及记 利未记 民数记 申命记 约书亚记 士师记 路得记 撒母耳记上 撒母耳记下 列王纪上 列王纪下 历代志上 历代志下 以斯拉记 尼希米记 以斯帖记 约伯记 诗篇 箴言 传道书 雅歌 以赛亚书 耶利米书 耶利米哀歌 以西结书 但以理书 何西阿书 约珥书 阿摩司书 俄巴底亚书 约拿书 弥迦书 那鸿书 哈巴谷书 西番雅书 哈该书 撒迦利亚书 玛拉基书 马太福音 马可福音 路加福音 约翰福音 使徒行传 罗马书 哥林多前书 哥林多后书 加拉太书 以弗所书 腓立比书 歌罗西书 帖撒罗尼迦前书 帖撒罗尼迦后书 提摩太前书 提摩太后书 提多书 腓利门书 希伯来书 雅各书 彼得前书 彼得后书 约翰一书 约翰二书 约翰三书 犹大书 启示录".split()
assert len(KO)==len(EN)==len(JA)==len(ZH)==66

# 시편 표제(제목)가 1절 앞에 붙어 있는 경우 직접 정리한 1절 본문
PSALM_V1 = json.load(open(os.path.join(os.path.dirname(__file__), "psalm_v1.json"), encoding="utf-8"))

t2s = OpenCC("t2s")
src = sys.argv[1]
B = {n: json.load(open(os.path.join(src, n + ".json"), encoding="utf-8"))["books"] for n in ["KorRV", "KJV", "JapKougo", "ChiUn"]}
# 일본어: scrollmapper JapKougo 에 빈 절이 있어 metastable-void/ja-colloquial (CC0) 을 함께 씀
JA2 = json.load(open(os.path.join(src, "JaColloquial.json"), encoding="utf-8"))["books"]
def _jnorm(s): return re.sub(r"[\s、，,]", "", s)

def _find(books, bi, c, v):
    for x in books[bi]["chapters"][c - 1]["verses"]:
        if x["verse"] == v:
            return x["text"].strip()
    return ""

def verse(n, bi, c, v):
    t = _find(B[n], bi, c, v)
    if n == "JapKougo":
        t2 = _find(JA2, bi, c, v)
        if not t or _jnorm(t) != _jnorm(t2):
            # 시 구절 줄바꿈(공백)을 쉼표로 바꿈
            t = re.sub(r"(?<=[^。、」』？！―])\s+(?=\S)", "、", t2.strip())
            t = re.sub(r"\s+", "", t)
    if not t:
        raise KeyError((n, bi, c, v))
    return t

PAIRS = [("「", "」"), ("『", "』"), ("“", "”"), ("‘", "’")]
def balance(t):
    """절 단위로 끊으면서 짝이 맞지 않게 된 따옴표만 지웁니다."""
    for o, c in PAIRS:
        stack, drop = [], set()
        for i, ch in enumerate(t):
            if ch == o: stack.append(i)
            elif ch == c:
                if stack: stack.pop()
                else: drop.add(i)
        drop |= set(stack)
        t = "".join(ch for i, ch in enumerate(t) if i not in drop)
    return t

def clean(n, t):
    t = re.sub(r"\s+", " ", t).strip()
    if n == "JapKougo":
        t = t.rstrip("〔").strip()
        t = re.sub(r"^\([^)]*\)、?", "", t)  # 시편 제목 (都もうでの歌) 제거
    if n in ("JapKougo", "ChiUn"):
        t = balance(t)
    if n == "ChiUn":
        t = t.replace(" ", "").replace("　", "")
        t = re.sub(r"（[^）]*）", "", t)
        t = t2s.convert(t)
        t = t.replace("「", "“").replace("」", "”").replace("『", "‘").replace("』", "’")
    if n == "KJV":
        t = t.replace("¶", "").strip()
    return t

def get(n, bi, c, vs):
    out = []
    for v in vs:
        key = f"{n}:{c}:{v}"
        if CODES[bi] == "Psa" and v == 1 and key in PSALM_V1:
            raw = clean(n, verse(n, bi, c, v))
            assert raw.endswith(PSALM_V1[key]), key  # 원문에서 제목만 뺀 것인지 확인
            out.append(PSALM_V1[key]); continue
        out.append(clean(n, verse(n, bi, c, v)))
    sep = "" if n in ("JapKougo", "ChiUn") else " "
    return sep.join(out)

def parse(ref):
    code, cv = ref.split(" ")
    c, v = cv.split(":")
    if "-" in v:
        a, b = map(int, v.split("-")); vs = list(range(a, b + 1))
    else:
        vs = [int(v)]
    return CODES.index(code), int(c), vs, v

def entry(ref):
    bi, c, vs, vlabel = parse(ref)
    return {"ref_code": ref,
            "ref_ko": f"{KO[bi]} {c}:{vlabel}", "ref_en": f"{EN[bi]} {c}:{vlabel}",
            "ref_ja": f"{JA[bi]} {c}:{vlabel}", "ref_zh": f"{ZH[bi]} {c}:{vlabel}",
            "ko": get("KorRV", bi, c, vs), "en": get("KJV", bi, c, vs),
            "ja": get("JapKougo", bi, c, vs), "zh": get("ChiUn", bi, c, vs)}

rows = []; day = 0
for month, theme, s in MONTHS:
    for ref in [x.strip() for x in s.split(";")]:
        day += 1
        dt = datetime.date(2027, 1, 1) + datetime.timedelta(days=day - 1)  # 평년 기준 날짜
        bi, c, vs, vlabel = parse(ref)
        rows.append({
            "day": day, "date": dt.strftime("%m-%d"), "date_ko": f"{dt.month}월 {dt.day}일",
            "month": month, "theme": theme, "ref_code": ref,
            "ref_ko": f"{KO[bi]} {c}:{vlabel}", "ref_en": f"{EN[bi]} {c}:{vlabel}",
            "ref_ja": f"{JA[bi]} {c}:{vlabel}", "ref_zh": f"{ZH[bi]} {c}:{vlabel}",
            "ko": get("KorRV", bi, c, vs), "en": get("KJV", bi, c, vs),
            "ja": get("JapKougo", bi, c, vs), "zh": get("ChiUn", bi, c, vs),
        })

from motifs import motif_for
for r in rows:
    r["motif"] = motif_for(r)

specials = []
for key, name, when, ref in SPECIALS:
    e = {"key": key, "name": name, "when": when, "month": None, "theme": name}
    e.update(entry(ref)); e["motif"] = motif_for({**e, "month": "1월"})
    specials.append(e)
SPECIAL_MOTIF = {"welcome": "두 손 모아 축복", "easter": "부활의 아침", "harvest": "보리 추수 들판", "thanksgiving": "추수하는 들판", "leap": "모래시계와 계절"}
for e in specials: e["motif"] = SPECIAL_MOTIF[e["key"]]

def easter(y):
    """그레고리력 부활절 (서방 교회) 날짜 계산"""
    a = y % 19; b, c = divmod(y, 100); d, e = divmod(b, 4); f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i, k = divmod(c, 4); l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451; month = (h + l - 7 * m + 114) // 31; day = (h + l - 7 * m + 114) % 31 + 1
    return datetime.date(y, month, day)

def nth_sunday(y, month, n):
    d = datetime.date(y, month, 1); d += datetime.timedelta(days=(6 - d.weekday()) % 7)
    return d + datetime.timedelta(weeks=n - 1)

calendar = {"note": "교회 절기 날짜. 교회에서 다른 날로 지키면 이 값만 바꾸면 됩니다.",
            "years": {str(y): {"easter": easter(y).isoformat(), "harvest": nth_sunday(y, 7, 1).isoformat(),
                                "thanksgiving": nth_sunday(y, 11, 3).isoformat()} for y in range(2026, 2036)}}

out = os.path.join(os.path.dirname(__file__), "..", "data")
meta = {"title": "말씀 키링 365", "versions": {"ko": "개역한글 (1961)", "en": "King James Version", "ja": "口語訳 (1955)", "zh": "和合本 (简体)"},
        "source": "scrollmapper/bible_databases (KorRV, KJV, JapKougo, ChiUn)", "count": len(rows)}
json.dump(calendar, open(os.path.join(out, "calendar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"meta": meta, "verses": rows, "specials": specials}, open(os.path.join(out, "verses-365.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cols = ["day", "date_ko", "month", "theme", "ref_ko", "ko", "motif", "ref_en", "en", "ref_ja", "ja", "ref_zh", "zh"]
with open(os.path.join(out, "verses-365.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print("wrote", len(rows))
