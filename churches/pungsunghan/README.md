# 풍성한교회 말씀 키링

`bible-keyring-original/`(원본)을 복사해서 로고와 교회 이름만 바꾼 풍성한교회용입니다.

- 주소: https://bigyws.github.io/Save/churches/pungsunghan/
- NFC 키링용 주소: https://bigyws.github.io/Save/churches/pungsunghan/?tag=1
- 로고: `img/logo.png` (밝은 화면), `img/logo-dark.png` (어두운 화면, 글씨를 밝게), `img/emblem.png` (첫 만남 카드), `img/icon-180.png` (홈 화면 아이콘)
- `index.html`은 `app.html` 앞뒤에 문서 머리말(아이콘 포함)을 붙인 것입니다. app.html을 고치면 index.html도 같이 고칩니다.

## 교회 소식 (설정 화면 아래)

관리자 모드가 꺼져 있을 때 설정 화면 아래에 보이고, 관리자 모드에서는 숨겨집니다.
- 예배 시간 안내: `app.html` / `index.html` 의 `<table class="sched">` 안 줄을 고칩니다.
- 대표 전화: 031-796-6776 (화면 오른쪽 위 전화 버튼, 교회소식의 찾아오시는 길)
- 찾아오시는 길: 주소(경기도 하남시 덕풍북로6번길 9-13), 구글 지도("풍성한교회 + 주소" 장소 검색), 네이버 지도·카카오맵("하남시 풍성한교회" 검색)

## NFC 키링

- 키링에 넣을 주소: `https://bigyws.github.io/Save/churches/pungsunghan/?tag=1`
- 시안: `keyring/keyring-designs.png` (A 원형 50mm, B 카드형 40×60mm), 원본 `keyring/designs.html`
- 칩: NTAG213 (주소 길이 약 55자, 용량 충분)
- 주의: 키링을 나눠 준 뒤에는 저장소 이름(Save)과 폴더 이름(churches/pungsunghan)을 바꾸면 안 됩니다. 바꾸면 키링이 열리지 않습니다.
