// 오늘 보여줄 말씀 카드를 고릅니다.
// 규칙: 매년 같은 날짜에 같은 구절(평년 365일 기준).
//  - 부활절·맥추감사절·추수감사절 주일에는 특별 카드 (날짜는 data/calendar.json)
//  - 윤년 2월 29일에는 윤년 카드, 3월 1일부터는 평년과 같은 구절
//  - 키링을 처음 댄 날에는 첫 만남 카드를 먼저 보여주고, 이어서 오늘 카드
(function (root) {
  const pad = (n) => String(n).padStart(2, "0");
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const isLeap = (y) => (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;

  // 그레고리력 부활절 (calendar.json 에 없는 해를 위한 계산)
  function easter(y) {
    const a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4;
    const f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3);
    const h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4;
    const l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
    const month = Math.floor((h + l - 7 * m + 114) / 31), day = ((h + l - 7 * m + 114) % 31) + 1;
    return `${y}-${pad(month)}-${pad(day)}`;
  }
  function nthSunday(y, month, n) {
    const d = new Date(y, month - 1, 1);
    d.setDate(1 + ((7 - d.getDay()) % 7) + 7 * (n - 1));
    return iso(d);
  }
  function feastDates(y, calendar) {
    const set = (calendar && calendar.years && calendar.years[String(y)]) || {};
    return {
      easter: set.easter || easter(y),
      harvest: set.harvest || nthSunday(y, 7, 1),
      thanksgiving: set.thanksgiving || nthSunday(y, 11, 3),
    };
  }

  // 평년 기준 Day (1~365). 윤년 2/29 는 0.
  function dayNumber(date) {
    const y = date.getFullYear();
    const start = new Date(y, 0, 1);
    let n = Math.round((new Date(y, date.getMonth(), date.getDate()) - start) / 86400000) + 1;
    if (isLeap(y)) {
      if (date.getMonth() === 1 && date.getDate() === 29) return 0;
      if (n > 59) n -= 1;
    }
    return n;
  }

  function pickCard(date, data, calendar, opts = {}) {
    const today = iso(date);
    const special = (key) => data.specials.find((s) => s.key === key);
    const f = feastDates(date.getFullYear(), calendar);
    let card;
    if (today === f.easter) card = special("easter");
    else if (today === f.harvest) card = special("harvest");
    else if (today === f.thanksgiving) card = special("thanksgiving");
    else {
      const n = dayNumber(date);
      card = n === 0 ? special("leap") : data.verses[n - 1];
    }
    const welcome = opts.firstTapEver ? special("welcome") : null;
    return { date: today, card, welcome };
  }

  const api = { pickCard, dayNumber, easter, feastDates };
  if (typeof module !== "undefined") module.exports = api; else root.MalsseumDaily = api;
})(this);
