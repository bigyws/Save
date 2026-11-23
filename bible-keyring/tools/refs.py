# 365일 말씀 목록: 월별 주제와 구절 위치 (개역한글 기준 장절)
MONTHS = [
 ("1월", "새 출발 · 소망", "Lam 3:22-23; Isa 43:19; 2Co 5:17; Jer 29:11; Phi 3:13-14; Psa 37:5; Pro 16:9; Jos 1:9; Psa 90:12; Pro 3:5-6; Rom 15:13; Psa 39:7; Psa 62:5; Jer 17:7; Psa 121:1-2; Psa 118:24; Mic 7:7; Isa 60:1; Rom 8:28; Eph 3:20; Psa 71:5; Lam 3:25; Psa 130:5; Heb 6:19; 1Pe 1:3; Rom 5:5; Psa 27:14; Deu 31:8; Psa 31:24; Psa 146:5; Psa 5:3"),
 ("2월", "사랑", "Joh 3:16; 1Jo 4:8; 1Jo 4:19; 1Co 13:4; 1Co 13:13; Rom 5:8; Rom 8:38-39; Joh 15:13; Joh 13:34; Jer 31:3; Zep 3:17; 1Jo 4:18; 1Jo 3:18; 1Pe 4:8; Col 3:14; Eph 3:18; Rom 13:10; Gal 5:13; 1Jo 4:10; Isa 54:10; Psa 103:13; Isa 49:15; Mat 22:37; Mat 22:39; Luk 6:31; 1Co 16:14; Pro 10:12; Rom 12:10"),
 ("3월", "믿음", "Heb 11:1; Heb 11:6; Rom 10:17; Mar 9:23; Mar 11:24; Gal 2:20; Eph 2:8; Rom 1:17; 2Co 5:7; Jas 2:17; Mat 17:20; Joh 20:29; Joh 14:1; Rom 10:10; 1Jo 5:4; Hab 2:4; Luk 1:37; Psa 56:3; Isa 26:4; Heb 12:2; 1Pe 1:8; Act 16:31; Mar 5:36; Mat 21:22; Psa 9:10; Pro 30:5; Heb 10:23; 2Ti 4:7; Jas 1:6; Gen 15:6; Joh 1:12"),
 ("4월", "부활 · 새 생명", "Joh 11:25; Col 3:4; 1Co 15:20; 1Co 15:55; 1Co 15:57; Rom 6:4; Joh 10:10; Joh 14:6; Joh 14:19; Isa 53:5; Rom 6:23; 1Pe 2:24; Gal 6:14; Joh 12:24; Joh 19:30; Luk 24:32; Rev 21:5; Rev 1:18; Phi 3:10; Col 3:1; Rom 8:11; 1Pe 1:23; Joh 5:24; Eze 36:26; Tit 3:5; Isa 53:6; Joh 1:29; Rom 5:1; Joh 6:35; Joh 15:5"),
 ("5월", "가정 · 이웃", "Jos 24:15; Psa 127:1; Psa 127:3; Psa 128:3; Pro 22:6; Exo 20:12; Eph 6:1; Eph 6:4; Col 3:20; Eph 5:25; Gen 2:24; Ecc 4:12; Pro 17:17; Pro 17:6; Pro 31:30; Pro 31:28; Psa 133:1; Act 2:46; Rut 1:16; Deu 6:7; Pro 15:1; Pro 16:24; Col 3:13; Eph 4:32; Eph 4:3; Rom 12:15; Gal 6:2; Phi 2:4; Mat 5:9; Isa 66:13; Psa 103:17"),
 ("6월", "평안 · 위로", "Joh 14:27; Phi 4:6-7; Isa 26:3; Mat 11:28; Mat 11:29; Psa 23:1; Psa 23:4; Psa 4:8; Psa 46:1; Psa 46:10; Psa 34:18; Psa 147:3; 2Co 1:4; 1Pe 5:7; Psa 55:22; Joh 16:33; Isa 41:13; Psa 94:19; Psa 91:2; Psa 91:4; Mat 6:34; Mat 5:4; Rev 21:4; Psa 30:5; Psa 42:11; Isa 40:11; Isa 43:2; Psa 29:11; Col 3:15; 2Th 3:16"),
 ("7월", "은혜 · 쉼", "2Co 12:9; Eph 1:7; Joh 1:16; Tit 2:11; Heb 4:16; Psa 84:11; Psa 103:2; Psa 103:5; Isa 55:1; Psa 63:3; Psa 84:10; Psa 27:4; Psa 16:11; Psa 36:9; Psa 1:3; Jer 17:8; Psa 42:1; Joh 4:14; Joh 7:38; Psa 65:11; Isa 30:15; Exo 33:14; Mar 6:31; Psa 62:1; Psa 116:7; Psa 127:2; Psa 37:7; Isa 32:18; Mat 6:26; Mat 6:28; Luk 12:7"),
 ("8월", "힘 · 용기", "Isa 40:31; Phi 4:13; Isa 40:29; Psa 18:2; Psa 27:1; Psa 28:7; Neh 8:10; Deu 31:6; 2Ti 1:7; Isa 41:10; Jos 1:5; Psa 73:26; Psa 84:5; Eph 6:10; 2Ch 20:15; Exo 14:14; Rom 8:31; Rom 8:37; 1Co 16:13; Psa 138:3; Zec 4:6; 2Co 4:16; 2Co 4:8; Isa 12:2; Psa 59:16; Psa 62:7; Psa 118:6; Heb 13:6; 1Jo 4:4; Deu 33:27; Gal 6:9"),
 ("9월", "말씀 · 지혜", "Psa 119:105; Psa 119:103; Psa 119:11; Psa 1:2; 2Ti 3:16; Heb 4:12; Isa 40:8; Mat 4:4; Joh 1:1; Jos 1:8; Psa 19:7; Psa 19:10; Jas 1:5; Pro 9:10; Pro 1:7; Pro 2:6; Pro 4:23; Pro 3:13; Pro 16:3; Col 3:16; Mat 7:24; Luk 11:28; Jas 1:22; Isa 55:11; Psa 119:130; Psa 119:18; Mat 24:35; Joh 8:32; Rom 12:2; Ecc 12:1"),
 ("10월", "기도 · 인도", "Jer 33:3; Mat 7:7; 1Th 5:17; Jas 5:16; Mat 6:6; Mat 18:20; Joh 14:14; Joh 15:7; 1Jo 5:14; Rom 8:26; Psa 145:18; Psa 50:15; Isa 65:24; Mat 26:41; Luk 18:1; Col 4:2; Eph 6:18; Psa 32:8; Isa 30:21; Psa 37:23; Psa 25:4; Psa 48:14; Isa 58:11; Psa 143:8; Psa 139:10; Exo 13:21; Isa 42:16; Joh 10:27; Psa 73:24; Psa 31:3; Psa 51:10"),
 ("11월", "감사 · 찬양", "1Th 5:18; Psa 136:1; Psa 100:4; Psa 100:5; Psa 103:1; Psa 150:6; Psa 95:2; Psa 50:23; Col 3:17; Eph 5:20; Phi 4:4; Psa 34:1; Psa 9:1; Hab 3:18; Psa 126:5; Psa 126:3; Psa 107:8; Gen 8:22; 2Co 9:15; 2Co 9:7; Psa 116:12; Psa 145:3; Psa 147:1; Psa 104:33; Psa 96:1; Psa 30:11; Psa 113:3; Rev 4:11; Psa 85:12; Deu 8:10"),
 ("12월", "성탄 · 빛", "Isa 9:2; Joh 1:5; Joh 8:12; Mat 5:14; Mat 5:16; 1Jo 1:5; 1Jo 1:7; Eph 5:8; Psa 18:28; 2Co 4:6; Isa 9:6; Gal 4:4; 1Jo 4:9; 2Co 8:9; Phi 2:7; Joh 1:14; Mat 1:21; Luk 1:46-47; Rev 3:20; Rev 22:20; Luk 2:7; Mic 5:2; Mat 1:23; Luk 2:10; Luk 2:11; Luk 2:14; Mat 2:10; Luk 2:19; Heb 13:8; Psa 121:8; 1Sa 7:12"),
]

# 특별 카드: 날짜가 해마다 바뀌는 절기, 윤년, 첫 만남
SPECIALS = [
 ("welcome", "첫 만남", "키링을 처음 댄 날 한 번", "Num 6:24-26"),
 ("easter", "부활절", "부활절 주일 (해마다 바뀜)", "Mat 28:6"),
 ("harvest", "맥추감사절", "7월 첫째 주일 (교회마다 다를 수 있음)", "Exo 23:16"),
 ("thanksgiving", "추수감사절", "11월 셋째 주일 (교회마다 다를 수 있음)", "Psa 67:6"),
 ("leap", "윤년 2월 29일", "4년에 한 번", "Ecc 3:1"),
]
