/* 콕태그 샘플 데이터
 * 키링 하나 = 반려동물 한 마리 = 아래 항목 하나입니다.
 * NFC 태그에는 memory.html?pet=<아이디> 주소를 씁니다. (예: memory.html?pet=choco)
 * 실제 고객 사진을 넣을 때는 photos 항목에 scene 대신 src: "photos/choco/01.jpg" 처럼 파일 경로를 적습니다.
 */
(function (root) {
  "use strict";
  const KOK = {
    brand: "콕태그",
    shop: {
      products: [
        { id: "dog", kind: "dog", name: "강아지 추억 키링", price: 19900, desc: "아크릴 양면 인쇄 + NFC 칩 내장" },
        { id: "cat", kind: "cat", name: "고양이 추억 키링", price: 19900, desc: "아크릴 양면 인쇄 + NFC 칩 내장" },
      ],
      plans: [
        { id: "basic", name: "기본", add: 0, desc: "사진 30장, 영상 3개" },
        { id: "plus", name: "플러스", add: 10000, desc: "사진·영상 무제한, 1년간 무료 수정" },
      ],
      engrave: 3000,
      shipping: 3000,
      freeShippingOver: 40000,
    },
    pets: {
      choco: {
        kind: "dog",
        name: "초코",
        nameEn: "CHOCO",
        breed: "말티푸",
        birthday: "2019-04-12",
        together: "2019-06-01",
        owner: "초코 누나",
        message: "초코야, 우리 집에 와줘서 고마워. 산책 갈 때마다 꼬리 흔드는 네 모습이 제일 좋아.",
        photos: [
          { scene: "park", date: "2024-05-03", caption: "한강 공원 첫 소풍" },
          { scene: "birthday", date: "2024-04-12", caption: "다섯 번째 생일 파티" },
          { scene: "beach", date: "2023-08-15", caption: "처음 본 바다" },
          { scene: "snack", date: "2024-01-20", caption: "간식 앞에서 윙크" },
          { scene: "nap", date: "2023-12-24", caption: "크리스마스 이브 낮잠" },
          { scene: "home", date: "2019-06-01", caption: "우리 집에 온 첫날" },
        ],
        videos: [
          { scene: "park", date: "2024-05-03", title: "공 물어오기 성공", duration: "0:24" },
          { scene: "birthday", date: "2024-04-12", title: "생일 케이크 앞에서", duration: "0:41" },
        ],
        timeline: [
          { date: "2019-06-01", title: "우리 가족이 된 날", text: "손바닥만 한 초코가 박스 안에서 낑낑거리며 왔어요.", scene: "home" },
          { date: "2020-03-10", title: "앉아! 성공", text: "간식 하나에 앉아, 손, 엎드려까지 한 번에 배웠어요.", scene: "snack" },
          { date: "2023-08-15", title: "첫 바다 여행", text: "파도가 올 때마다 도망가다가 결국 물에 첨벙.", scene: "beach" },
          { date: "2024-04-12", title: "다섯 살 생일", text: "고깔모자는 3초 만에 벗겨졌지만 케이크는 다 먹었어요.", scene: "birthday" },
        ],
      },
      nabi: {
        kind: "cat",
        name: "나비",
        nameEn: "NABI",
        breed: "코리안 숏헤어 (치즈)",
        birthday: "2020-09-02",
        together: "2020-11-14",
        owner: "나비 집사",
        message: "창가에서 햇볕 쬐는 나비를 보면 하루가 따뜻해져. 오래오래 같이 살자.",
        photos: [
          { scene: "nap", date: "2024-02-11", caption: "이불 위 꿀잠" },
          { scene: "snack", date: "2024-03-08", caption: "생선 간식 발견" },
          { scene: "home", date: "2020-11-14", caption: "처음 우리 집에 온 날" },
          { scene: "birthday", date: "2023-09-02", caption: "세 번째 생일" },
          { scene: "park", date: "2024-04-20", caption: "베란다 정원 산책" },
          { scene: "beach", date: "2023-07-30", caption: "여름 휴가 사진 속 나비" },
        ],
        videos: [
          { scene: "home", date: "2024-03-01", title: "꾹꾹이 하는 나비", duration: "0:18" },
          { scene: "nap", date: "2024-02-11", title: "골골송 들어보세요", duration: "0:35" },
        ],
        timeline: [
          { date: "2020-11-14", title: "길에서 만난 인연", text: "비 오는 날 아파트 화단에서 만나 가족이 되었어요.", scene: "home" },
          { date: "2021-05-05", title: "첫 캣타워", text: "캣타워보다 상자를 더 좋아한다는 걸 알게 된 날.", scene: "park" },
          { date: "2023-09-02", title: "세 살 생일", text: "츄르 케이크에 촛불 대신 깃털 장난감을 꽂았어요.", scene: "birthday" },
          { date: "2024-02-11", title: "겨울잠 시즌", text: "전기장판 위가 나비의 겨울 지정석이 되었어요.", scene: "nap" },
        ],
      },
    },
  };
  if (typeof module !== "undefined" && module.exports) module.exports = KOK;
  else root.KOK = KOK;
})(typeof window !== "undefined" ? window : globalThis);
