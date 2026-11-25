// 말씀 카드 배경 그림 (SVG). 구절의 그림 주제와 월에 따라 그립니다.
(function (root) {
function sheep(x,y,s,flip){
  const k = flip?-s:s;
  return `<g transform="translate(${x},${y}) scale(${k},${s})">
    <ellipse cx="2" cy="24" rx="24" ry="4" fill="#2f5a34" opacity=".18"/>
    <g fill="#4a3f38"><rect x="-13" y="8" width="3.4" height="14" rx="1.7"/><rect x="-5" y="9" width="3.4" height="14" rx="1.7"/><rect x="6" y="9" width="3.4" height="14" rx="1.7"/><rect x="13" y="8" width="3.4" height="14" rx="1.7"/></g>
    <g fill="#FFFBF2"><circle cx="-13" cy="1" r="10"/><circle cx="-2" cy="-6" r="12"/><circle cx="11" cy="-3" r="11"/><circle cx="-6" cy="7" r="10"/><circle cx="8" cy="7" r="10"/><circle cx="17" cy="4" r="8"/></g>
    <g fill="#EDE5D4" opacity=".8"><circle cx="-8" cy="10" r="6"/><circle cx="6" cy="11" r="6"/></g>
    <ellipse cx="25" cy="-1" rx="7.5" ry="9.5" transform="rotate(22 25 -1)" fill="#4a3f38"/>
    <ellipse cx="19" cy="-8" rx="5" ry="2.6" transform="rotate(-25 19 -8)" fill="#4a3f38"/>
    <circle cx="27.5" cy="-3" r="1.2" fill="#fff"/>
  </g>`;
}
function artShepherd(p){
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMin slice">
  <defs>
    <linearGradient id="${p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6E3C4"/><stop offset=".55" stop-color="#FAD7AE"/><stop offset="1" stop-color="#F6C7A0"/></linearGradient>
    <radialGradient id="${p}sun"><stop offset="0" stop-color="#FFF7E2"/><stop offset=".35" stop-color="#FFF1D2" stop-opacity=".9"/><stop offset="1" stop-color="#FFE7C4" stop-opacity="0"/></radialGradient>
    <linearGradient id="${p}h1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C5D9A6"/><stop offset="1" stop-color="#A9C98E"/></linearGradient>
    <linearGradient id="${p}h2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#97C384"/><stop offset="1" stop-color="#7DB06F"/></linearGradient>
    <linearGradient id="${p}h3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6FAA69"/><stop offset="1" stop-color="#4F8C55"/></linearGradient>
  </defs>
  <rect width="360" height="500" fill="url(#${p}sky)"/>
  <circle cx="246" cy="128" r="120" fill="url(#${p}sun)"/>
  <circle cx="246" cy="128" r="38" fill="#FFF6E0"/>
  <g fill="none" stroke="#9C7A62" stroke-width="2" stroke-linecap="round" opacity=".7">
    <path d="M64 92q7-7 14 0q7-7 14 0"/><path d="M104 70q5-5 10 0q5-5 10 0"/><path d="M86 118q4-4 8 0q4-4 8 0"/></g>
  <g fill="#FFFFFF" opacity=".75"><ellipse cx="80" cy="160" rx="46" ry="11"/><ellipse cx="104" cy="152" rx="26" ry="11"/><ellipse cx="300" cy="200" rx="40" ry="8"/></g>
  <path d="M0 218C70 186 140 196 210 212S320 196 360 204V500H0Z" fill="url(#${p}h1)"/>
  <path d="M0 262C80 232 170 262 250 246S330 228 360 238V500H0Z" fill="url(#${p}h2)"/>
  <g transform="translate(296 222)"><rect x="-3" y="0" width="6" height="26" rx="2" fill="#7A5A40"/><circle cx="0" cy="-10" r="17" fill="#5E9A5F"/><circle cx="-12" cy="-2" r="12" fill="#5E9A5F"/><circle cx="12" cy="-1" r="12" fill="#548E56"/></g>
  <path d="M0 312C100 284 200 322 360 292V500H0Z" fill="url(#${p}h3)"/>
  <path d="M30 500C90 420 160 350 220 300" stroke="#E8D5A8" stroke-width="16" fill="none" opacity=".45" stroke-linecap="round"/>
  ${sheep(92,250,.9,false)}
  ${sheep(165,268,1.05,true)}
  ${sheep(250,276,.8,false)}
  ${sheep(58,300,1.25,false)}
  <path d="M310 410L304 300q-2-22 14-24q16-1 16 16" fill="none" stroke="#6B4C34" stroke-width="5" stroke-linecap="round"/>
  <g fill="#FFF3D6"><circle cx="40" cy="360" r="3"/><circle cx="120" cy="340" r="2.5"/><circle cx="210" cy="352" r="3"/><circle cx="280" cy="330" r="2.5"/><circle cx="330" cy="356" r="3"/></g>
  <g fill="#F4A9A0"><circle cx="70" cy="380" r="3"/><circle cx="170" cy="372" r="2.5"/><circle cx="255" cy="368" r="3"/></g>
  <path d="M0 400C120 380 240 410 360 386V500H0Z" fill="#457F4B"/>
  </svg>`;
}
function artEagle(p){
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMin slice">
  <defs>
    <linearGradient id="${p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2C4777"/><stop offset=".45" stop-color="#6D8CC0"/><stop offset=".72" stop-color="#C9B8C8"/><stop offset="1" stop-color="#F3C9A2"/></linearGradient>
    <radialGradient id="${p}sun" cx=".5" cy=".5"><stop offset="0" stop-color="#FFF4DA"/><stop offset=".3" stop-color="#FFE3B8" stop-opacity=".8"/><stop offset="1" stop-color="#FFD8A8" stop-opacity="0"/></radialGradient>
    <linearGradient id="${p}m3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E5288"/><stop offset="1" stop-color="#26355F"/></linearGradient>
  </defs>
  <rect width="360" height="500" fill="url(#${p}sky)"/>
  <circle cx="180" cy="300" r="170" fill="url(#${p}sun)"/>
  <g fill="#FFF3DA" opacity=".12"><path d="M180 300L60 0H110Z"/><path d="M180 300L170 0H215Z"/><path d="M180 300L290 0H340Z"/></g>
  <g fill="#fff"><circle cx="40" cy="40" r="1.2" opacity=".7"/><circle cx="300" cy="30" r="1.4" opacity=".6"/><circle cx="330" cy="80" r="1" opacity=".5"/><circle cx="70" cy="90" r="1" opacity=".5"/></g>
  <path d="M0 270L50 210L84 236L140 168L190 226L232 190L290 240L330 206L360 226V500H0Z" fill="#A9B4D6"/>
  <path d="M140 168L124 188L136 186L146 196L156 184L164 190Z" fill="#F4F1EE"/>
  <path d="M232 190L220 204L232 202L240 210L248 202Z" fill="#F4F1EE"/>
  <path d="M0 312L70 236L110 270L170 212L230 280L290 230L360 290V500H0Z" fill="#7287BC"/>
  <path d="M70 236L54 256L68 252L76 262L88 250Z" fill="#E9ECF4"/>
  <path d="M170 212L152 234L166 230L174 242L184 230L192 236Z" fill="#E9ECF4"/>
  <path d="M290 230L274 248L288 246L296 254L308 244Z" fill="#E9ECF4"/>
  <g fill="#FFFFFF" opacity=".55"><ellipse cx="90" cy="300" rx="70" ry="12"/><ellipse cx="270" cy="314" rx="80" ry="12"/><ellipse cx="190" cy="326" rx="60" ry="9"/></g>
  <path d="M0 360L60 300L120 346L200 280L270 340L320 306L360 330V500H0Z" fill="url(#${p}m3)"/>
  <path d="M0 430C90 400 220 420 360 396V500H0Z" fill="#1C2748"/>
  <g transform="translate(176 118) rotate(-6)" fill="#1E2840">
    <path d="M0 -4C-18 -14 -40 -30 -66 -36L-96 -44L-86 -35L-106 -35L-91 -27L-110 -23L-90 -17L-104 -10L-80 -8C-56 -4 -28 4 -9 10L-7 22L0 32L7 22L9 10C28 4 56 -4 80 -8L104 -10L90 -17L110 -23L91 -27L106 -35L86 -35L96 -44L66 -36C40 -30 18 -14 0 -4Z"/>
    <path d="M-8 22L-12 40L0 34L12 40L8 22Z"/>
    <circle cx="0" cy="-8" r="6.5" fill="#F5F0E6"/>
    <path d="M-2 -4L0 4L3 -3Z" fill="#E2A33F"/>
  </g>
  <g fill="none" stroke="#1E2840" stroke-width="1.6" stroke-linecap="round" opacity=".55"><path d="M70 196q5-5 10 0q5-5 10 0"/><path d="M276 150q4-4 8 0q4-4 8 0"/></g>
  </svg>`;
}
function artLantern(p){
  const stars=[[30,40],[70,22],[118,58],[160,30],[210,64],[300,40],[330,90],[50,110],[250,24],[280,120],[20,170],[340,170],[96,150],[190,110]];
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMin slice">
  <defs>
    <linearGradient id="${p}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1A3A"/><stop offset=".6" stop-color="#22386A"/><stop offset="1" stop-color="#3B5487"/></linearGradient>
    <radialGradient id="${p}glow"><stop offset="0" stop-color="#FFE1A0" stop-opacity=".95"/><stop offset=".25" stop-color="#FFC966" stop-opacity=".55"/><stop offset="1" stop-color="#FFB547" stop-opacity="0"/></radialGradient>
    <linearGradient id="${p}path" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C6A46A" stop-opacity=".35"/><stop offset=".55" stop-color="#E9C987"/><stop offset="1" stop-color="#B98F52"/></linearGradient>
    <mask id="${p}moon"><rect width="360" height="500" fill="#fff"/><circle cx="84" cy="70" r="22" fill="#000"/></mask>
  </defs>
  <rect width="360" height="500" fill="url(#${p}sky)"/>
  ${stars.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="${i%3?1.1:1.8}" fill="#FFF6DD" opacity="${i%2?.6:.95}"/>`).join('')}
  <circle cx="72" cy="78" r="24" fill="#FBEFCF" mask="url(#${p}moon)"/>
  <path d="M0 236C70 206 130 220 190 228S300 206 360 216V500H0Z" fill="#1C2D58"/>
  <path d="M0 270C90 246 170 266 240 256S330 244 360 250V500H0Z" fill="#16244A"/>
  <g fill="#0F1A38"><path d="M30 262l12-40l12 40z"/><path d="M48 264l9-30l9 30z"/><path d="M318 252l11-38l11 38z"/></g>
  <path d="M176 246C168 270 150 290 160 320C172 360 120 400 70 500H300C240 420 230 370 214 330C200 296 196 270 190 246Z" fill="url(#${p}path)"/>
  <circle cx="232" cy="236" r="130" fill="url(#${p}glow)"/>
  <ellipse cx="222" cy="352" rx="70" ry="16" fill="#FFD98C" opacity=".35"/>
  <rect x="229" y="246" width="6" height="110" rx="2" fill="#2A2F45"/>
  <path d="M232 246h22v8" stroke="#2A2F45" stroke-width="4" fill="none" stroke-linecap="round"/>
  <g transform="translate(254 256)">
    <path d="M-6 0h12l2 5h-16z" fill="#2A2F45"/>
    <rect x="-11" y="5" width="22" height="30" rx="4" fill="#FFE7A8" stroke="#2A2F45" stroke-width="3"/>
    <path d="M0 13c4 5 4 10 0 14c-4-4-4-9 0-14z" fill="#FF9E3D"/>
    <path d="M-13 35h26l-3 5h-20z" fill="#2A2F45"/>
  </g>
  <g fill="#FFE39A"><circle cx="150" cy="300" r="2"/><circle cx="300" cy="280" r="1.8"/><circle cx="110" cy="250" r="1.5"/><circle cx="320" cy="330" r="2.2" opacity=".7"/></g>
  <path d="M0 400C70 390 120 420 150 500H0Z" fill="#0E1833"/>
  <path d="M360 390C300 392 260 430 250 500H360Z" fill="#0E1833"/>
  </svg>`;
}


// 그림을 따로 그리지 않은 주제: 풍경(언덕·산·물가·들판) × 시간(낮·새벽·노을·밤) × 주제 소재를 날마다 바꿔 그립니다.
const PALETTES = {
  "1월":  {sky:["#FCE3C8","#F4B79C"], hills:["#CDBBD9","#A08EC0","#6F6295"], sun:"#FFF4E2"},
  "2월":  {sky:["#FBDCD6","#F2B2AE"], hills:["#E8AAA5","#C98088","#9C5D6D"], sun:"#FFF1EC"},
  "3월":  {sky:["#E1EEF5","#B5D2E5"], hills:["#ADC9A3","#82A97E","#5A825F"], sun:"#FFFBEA"},
  "4월":  {sky:["#FFF1D6","#FFD39A"], hills:["#C2E1AA","#8EC37C","#5F9B58"], sun:"#FFF8E4"},
  "5월":  {sky:["#E8F4EA","#C2E1C8"], hills:["#A2D2A3","#72B17B","#4D8D5B"], sun:"#FFFBEB"},
  "6월":  {sky:["#DFEFF7","#ADD2EA"], hills:["#9EC3DB","#709FC2","#4C79A1"], sun:"#FFFDF2"},
  "7월":  {sky:["#E4F5F2","#B4E0D9"], hills:["#92D0B9","#60AF96","#3F8C77"], sun:"#FFFBEA"},
  "8월":  {sky:["#BFD3EE","#F1C8A2"], hills:["#A9B4D6","#7287BC","#3E5288"], sun:"#FFF4DA"},
  "9월":  {sky:["#F5EDDD","#E8D2AC"], hills:["#CFB68C","#AA8D63","#806845"], sun:"#FFF9EC"},
  "10월": {sky:["#F9E3C6","#EDB17C"], hills:["#DA935B","#B76F3D","#8A4F2B"], sun:"#FFF3DF"},
  "11월": {sky:["#FCE8C2","#F1C076"], hills:["#E4B75D","#C99741","#9C7431"], sun:"#FFF6DE"},
  "12월": {sky:["#DCE6F2","#B9CBE3"], hills:["#9DB3CF","#6F8BB1","#4A6690"], sun:"#FFF8E8"},
};
const SPECIAL_MONTH = {welcome:"1월", easter:"4월", harvest:"7월", thanksgiving:"11월", leap:"3월"};
const TIMES = {
  dawn:   {sky:["#F4CFE0","#FCE6C6"], tint:"#B48BB8", k:.35, sun:"#FFF0DA"},
  sunset: {sky:["#F5A77E","#F8D9A6"], tint:"#A65E4B", k:.38, sun:"#FFE0A8"},
  night:  {sky:["#0F1C3E","#34507F"], tint:"#18264A", k:.72, sun:"#FBEFCF", night:true},
};
const TIME_ORDER = ["day","dawn","day","sunset","day","night"];
const SCENES = ["hills","mountains","water","field"];
// 주제 → 풍경, 시간, 소재
const MOTIF = {
  "수금과 찬양":{obj:"lyre"}, "펼친 성경":{obj:"book"}, "기도하는 손":{obj:"pray"},
  "맞잡은 두 손":{obj:"heart"}, "두 손 모아 축복":{obj:"heart", time:"dawn"},
  "성탄의 별과 마구간":{obj:"stable", time:"night", scene:"hills"}, "부활의 아침":{obj:"tomb", time:"dawn", scene:"hills"},
  "십자가 언덕":{obj:"cross", scene:"hills"}, "포도나무":{obj:"grapes", scene:"hills"},
  "추수하는 들판":{obj:"wheat", scene:"field"}, "보리 추수 들판":{obj:"wheat", scene:"field"},
  "시냇가의 나무":{obj:"tree", scene:"water"}, "샘물과 시냇물":{obj:"stream", scene:"field"},
  "하늘의 새":{obj:"birds"}, "들꽃":{obj:"flowers", scene:"hills"}, "어미새의 날개":{obj:"wings"},
  "반석과 요새":{obj:"castle", scene:"mountains"}, "방패":{obj:"shield"}, "구름기둥과 불기둥":{obj:"pillar", scene:"field"},
  "바다와 배":{obj:"boat", scene:"water"}, "떡과 잔":{obj:"bread"}, "별이 빛나는 밤":{obj:"", time:"night"},
  "산 위의 마을":{obj:"village", scene:"hills"}, "빛줄기":{obj:"rays"}, "문을 두드리는 손":{obj:"house", scene:"hills"},
  "집과 가족":{obj:"house", scene:"hills"}, "감사의 식탁":{obj:"basket"}, "해돋이":{obj:"rays", time:"dawn"},
  "길과 이정표":{obj:"path", scene:"field"}, "산":{obj:"", scene:"mountains"}, "잔잔한 호수":{obj:"", scene:"water"},
  "겨자씨와 산":{obj:"sprout", scene:"mountains"}, "모래시계와 계절":{obj:"hourglass"},
};
function rng(seed){ let s = (seed * 7919 + 104729) % 233280; return () => ((s = (s * 9301 + 49297) % 233280) / 233280); }
function mix(a, b, t){ const p = (h) => [1,3,5].map((i) => parseInt(h.slice(i, i + 2), 16)); const x = p(a), y = p(b);
  return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, "0")).join(""); }
function hill(y, amp, r){
  const a = y + (r()-.5)*amp, b = y + (r()-.5)*amp*1.6, c = y + (r()-.5)*amp;
  return `M0 ${a.toFixed(0)}C90 ${b.toFixed(0)} 170 ${c.toFixed(0)} 250 ${(b+10).toFixed(0)}S330 ${(a-6).toFixed(0)} 360 ${c.toFixed(0)}V500H0Z`;
}
const W = "#FFFFFF";
function emblem(svg, night){ return `<g transform="translate(0 -22)" opacity="${night ? .9 : .92}" style="filter:drop-shadow(0 2px 6px rgba(0,0,0,.18))">${svg}</g>`; }
const OBJ = {
  lyre: (c) => emblem(`<g transform="translate(180 128)" fill="none" stroke="${W}" stroke-linecap="round"><path d="M-24 34C-42-6-32-40-12-48M24 34C42-6 32-40 12-48" stroke-width="7"/><path d="M-30 34H30" stroke-width="8"/><path d="M-27-18H27" stroke-width="5"/><path d="M-12-18V34M-4-18V34M4-18V34M12-18V34" stroke-width="2"/></g>
    <g fill="${W}"><circle cx="252" cy="96" r="6"/><rect x="256" y="70" width="2.5" height="26"/><circle cx="110" cy="84" r="5"/><rect x="113.5" y="62" width="2.2" height="22"/></g>`, c.night),
  book: (c) => emblem(`<g transform="translate(180 128)"><path d="M0-4C-18-16-42-16-56-9V34C-42 27-18 27 0 38Z" fill="${W}"/><path d="M0-4C18-16 42-16 56-9V34C42 27 18 27 0 38Z" fill="${W}" opacity=".88"/>
    <g stroke="${c.ink}" stroke-width="2" opacity=".35"><path d="M-46 4C-34 0-20 0-8 6M-46 14C-34 10-20 10-8 16M8 6C20 0 34 0 46 4M8 16C20 10 34 10 46 14"/></g></g>`, c.night),
  pray: (c) => emblem(`<g transform="translate(180 132)" fill="${W}"><path d="M-2 44V-34C-2-46-15-48-18-36L-26 18-38 44Z"/><path d="M2 44V-34C2-46 15-48 18-36L26 18 38 44Z" opacity=".9"/></g>`, c.night),
  heart: (c) => emblem(`<path d="M180 150c-16-18-46-7-46 16 0 20 25 34 46 50 21-16 46-30 46-50 0-23-30-34-46-16z" fill="${W}"/>`, c.night),
  wings: (c) => emblem(`<g transform="translate(180 140)" fill="${W}"><path d="M-6 10C-30-20-70-30-96-26L-80-16-98-10-78-2-92 6-70 10C-44 14-22 18-6 24Z"/><path d="M6 10C30-20 70-30 96-26L80-16 98-10 78-2 92 6 70 10C44 14 22 18 6 24Z"/></g>`, c.night),
  shield: (c) => emblem(`<g transform="translate(180 130)"><path d="M0-46L40-32V0C40 26 20 42 0 50C-20 42-40 26-40 0V-32Z" fill="${W}"/><path d="M0-26V30M-18-4H18" stroke="${c.ink}" stroke-width="6" stroke-linecap="round" opacity=".45"/></g>`, c.night),
  bread: (c) => emblem(`<g transform="translate(180 136)" fill="${W}"><ellipse cx="-30" cy="22" rx="34" ry="16"/><path d="M-50 18q10-8 20 0M-34 14q10-8 20 0" stroke="${c.ink}" stroke-width="2.5" fill="none" opacity=".3"/>
    <path d="M20-30H56C56-6 48 6 38 8V30H50V36H26V30H38V8C28 6 20-6 20-30Z"/></g>`, c.night),
  basket: (c) => emblem(`<g transform="translate(180 140)"><circle cx="-18" cy="-6" r="14" fill="#F2A65A"/><circle cx="8" cy="-12" r="15" fill="#E8574F"/><circle cx="28" cy="-2" r="12" fill="#B5CF5A"/><circle cx="-2" cy="2" r="11" fill="#8E5BA8"/>
    <path d="M-44 0H44L34 36H-34Z" fill="${W}"/><path d="M-38 12H38M-35 24H35" stroke="${c.ink}" stroke-width="2" opacity=".3"/></g>`, c.night),
  hourglass: (c) => emblem(`<g transform="translate(180 130)"><path d="M-26-42H26M-26 42H26" stroke="${W}" stroke-width="7" stroke-linecap="round"/><path d="M-20-38C-20-10 0-6 0 0S-20 10-20 38H20C20 10 0 6 0 0S20-10 20-38Z" fill="${W}" opacity=".85"/><path d="M-12 36C-10 24 10 24 12 36Z" fill="${c.accent}"/></g>`, c.night),
  rays: (c) => `<g fill="${c.sun}" opacity=".22"><path d="M${c.sx} ${c.sy}L40 0H90Z"/><path d="M${c.sx} ${c.sy}L150 0H200Z"/><path d="M${c.sx} ${c.sy}L260 0H310Z"/><path d="M${c.sx} ${c.sy}L360 40V90Z"/></g>`,
  birds: (c) => Array.from({length:8}, (_, i) => { const x = 40 + i*38 + (c.r()-.5)*20, y = 60 + (c.r())*110, w = 5 + c.r()*6;
    return `<path d="M${x.toFixed(0)} ${y.toFixed(0)}q${w.toFixed(1)} -${w.toFixed(1)} ${(w*2).toFixed(1)} 0q${w.toFixed(1)} -${w.toFixed(1)} ${(w*2).toFixed(1)} 0" fill="none" stroke="${c.night ? "#FFF6DD" : "#2B2A33"}" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"/>`; }).join(""),
  pillar: (c) => `<g fill="${W}" opacity=".85">${Array.from({length:7}, (_, i) => `<ellipse cx="${(250 + Math.sin(i)*8).toFixed(0)}" cy="${250 - i*26}" rx="${26 - i*1.2}" ry="16"/>`).join("")}</g><ellipse cx="250" cy="250" rx="60" ry="10" fill="${W}" opacity=".25"/>`,
  cross: (c) => `<g transform="translate(250 232)" fill="${c.ink}"><rect x="-5" y="-70" width="10" height="84" rx="2"/><rect x="-28" y="-50" width="56" height="9" rx="2"/></g><g transform="translate(205 240)" fill="${c.ink}" opacity=".7"><rect x="-3" y="-40" width="6" height="48"/><rect x="-16" y="-28" width="32" height="6"/></g><g transform="translate(295 240)" fill="${c.ink}" opacity=".7"><rect x="-3" y="-40" width="6" height="48"/><rect x="-16" y="-28" width="32" height="6"/></g>`,
  star: (c) => `<g transform="translate(250 84)" fill="#FFF3C4"><path d="M0-24L5-5L24 0L5 5L0 24L-5 5L-24 0L-5-5Z"/><circle r="46" opacity=".14"/></g>`,
  stable: (c) => `<g transform="translate(160 236)"><path d="M-40 0L0-30L40 0V30H-40Z" fill="${c.ink}"/><path d="M-46 2L0-34L46 2" stroke="${c.ink}" stroke-width="6" fill="none"/><rect x="-12" y="6" width="24" height="24" fill="#FFD98A"/><circle cx="0" cy="18" r="30" fill="#FFD98A" opacity=".18"/></g>`,
  tomb: (c) => `<g transform="translate(200 240)"><path d="M-70 30C-70-26 70-26 70 30Z" fill="${mix(c.ink, "#A89D8A", .5)}"/><ellipse cx="-6" cy="8" rx="20" ry="24" fill="#3A3328"/><circle cx="46" cy="14" r="22" fill="${mix(c.ink, "#C2B8A3", .55)}"/></g>`,
  grapes: (c) => `<g transform="translate(276 210)"><path d="M-80-30C-40-60 20-50 40-20" stroke="#5E7A3A" stroke-width="5" fill="none"/><path d="M-30-46c10-16 34-14 36 4-14 8-28 8-36-4z" fill="#6E9A45"/><path d="M14-40c14-10 30-2 28 14-14 4-24 0-28-14z" fill="#5E8A3C"/>
    ${[[0,0],[12,0],[24,0],[6,11],[18,11],[30,11],[12,22],[24,22],[18,33]].map(([x,y]) => `<circle cx="${x-6}" cy="${y-18}" r="7" fill="#6B3F7A"/>`).join("")}</g>`,
  wheat: (c) => Array.from({length:9}, (_, i) => { const x = 20 + i*40 + (c.r()-.5)*14, h = 70 + c.r()*30, y0 = 330;
    return `<g stroke="#C9922F" fill="#E3B24F"><path d="M${x.toFixed(0)} ${y0}V${(y0-h).toFixed(0)}" stroke-width="2.5"/>${[0,1,2,3,4].map((k) => `<ellipse cx="${(x-5).toFixed(0)}" cy="${(y0-h+8+k*9).toFixed(0)}" rx="4" ry="7" transform="rotate(-25 ${(x-5).toFixed(0)} ${(y0-h+8+k*9).toFixed(0)})"/><ellipse cx="${(x+5).toFixed(0)}" cy="${(y0-h+8+k*9).toFixed(0)}" rx="4" ry="7" transform="rotate(25 ${(x+5).toFixed(0)} ${(y0-h+8+k*9).toFixed(0)})"/>`).join("")}</g>`; }).join(""),
  tree: (c) => `<g transform="translate(108 232)"><rect x="-5" y="-6" width="10" height="34" rx="3" fill="#6E5038"/><circle cx="0" cy="-30" r="30" fill="${mix(c.hills[1], "#3E7A45", .5)}"/><circle cx="-24" cy="-14" r="20" fill="${mix(c.hills[1], "#3E7A45", .6)}"/><circle cx="24" cy="-12" r="20" fill="${mix(c.hills[1], "#2F6A3A", .6)}"/></g>`,
  stream: (c) => `<path d="M175 246C170 280 120 300 150 340S90 420 60 500H170C190 430 230 400 210 350S200 280 186 246Z" fill="${mix(c.sky[0], "#9FD0EA", .6)}" opacity=".9"/><path d="M180 270q-14 20 0 40M150 360q-20 30-10 60" stroke="#fff" stroke-width="2" opacity=".5" fill="none"/>`,
  flowers: (c) => Array.from({length:16}, () => { const x = c.r()*360, y = 290 + c.r()*60, col = ["#F4A3B4","#FFE07A","#FFFFFF","#C9A7E8"][Math.floor(c.r()*4)];
    return `<path d="M${x.toFixed(0)} ${(y+10).toFixed(0)}v-12" stroke="#4E8B4A" stroke-width="2"/><circle cx="${x.toFixed(0)}" cy="${(y-3).toFixed(0)}" r="${(4+c.r()*3).toFixed(1)}" fill="${col}"/><circle cx="${x.toFixed(0)}" cy="${(y-3).toFixed(0)}" r="1.6" fill="#E8A13A"/>`; }).join(""),
  castle: (c) => `<g transform="translate(206 168)" fill="${c.ink}"><rect x="-40" y="0" width="80" height="44"/><rect x="-52" y="-22" width="22" height="66"/><rect x="30" y="-22" width="22" height="66"/><rect x="-10" y="-30" width="20" height="30"/>
    ${[-52,-41,30,41].map((x) => `<rect x="${x}" y="-30" width="7" height="9"/>`).join("")}<path d="M0-30V-48L14-42 0-36" /><rect x="-8" y="22" width="16" height="22" rx="8" fill="${c.sky[1]}" opacity=".7"/></g>`,
  boat: (c) => `<g transform="translate(150 286)"><path d="M-46 0H46L32 18H-32Z" fill="${c.ink}"/><rect x="-2" y="-62" width="4" height="62" fill="${c.ink}"/><path d="M2-58L40-6H2Z" fill="${W}" opacity=".92"/><path d="M-2-52L-30-8H-2Z" fill="${W}" opacity=".8"/></g>`,
  village: (c) => [[150,214,1],[186,206,1.2],[222,214,1],[258,222,.9]].map(([x,y,s]) => `<g transform="translate(${x} ${y}) scale(${s})" fill="${c.ink}"><path d="M-14 0L0-14L14 0V16H-14Z"/><rect x="-4" y="4" width="8" height="8" fill="#FFD98A"/></g>`).join(""),
  house: (c) => `<g transform="translate(236 232)"><rect x="-34" y="-8" width="68" height="44" fill="${mix(c.ink, "#ffffff", .25)}"/><path d="M-44-6L0-40L44-6Z" fill="${c.ink}"/><rect x="18" y="-40" width="10" height="20" fill="${c.ink}"/>
    <rect x="-10" y="10" width="20" height="26" fill="#7A4E2E"/><circle cx="6" cy="24" r="2" fill="#FFD98A"/><rect x="-28" y="2" width="12" height="12" fill="#FFD98A"/><rect x="16" y="2" width="12" height="12" fill="#FFD98A"/></g>`,
  path: (c) => `<path d="M176 248C170 262 150 276 168 300C190 330 120 380 80 500H260C230 420 236 360 214 320C196 290 196 266 188 248Z" fill="${mix(c.hills[0], "#F3E2B8", .65)}"/>
    <g transform="translate(250 262)" fill="#6E5038"><rect x="-3" y="-44" width="6" height="56"/><path d="M3-40H36L44-34 36-28H3Z"/><path d="M-3-24H-34L-42-18-34-12H-3Z"/></g>`,
  sprout: (c) => `<g transform="translate(180 300)"><circle r="40" fill="#FFF6D8" opacity=".25"/><path d="M0 20V-14" stroke="#4E8B4A" stroke-width="4"/><path d="M0-6C-4-24-24-26-30-18-22-8-8-6 0-6Z" fill="#7CC36A"/><path d="M0-12C4-30 24-32 30-24 22-14 8-12 0-12Z" fill="#6AB35A"/></g>`,
};
function scenery(scene, c, p){
  const H = c.hills, r = c.r;
  if (scene === "mountains") {
    const peaks = Array.from({length:5}, (_, i) => [i*90 - 20 + r()*30, 150 + r()*60]);
    const range = `M0 260${peaks.map(([x,y]) => `L${x.toFixed(0)} ${y.toFixed(0)}L${(x+45).toFixed(0)} ${(y+50+r()*20).toFixed(0)}`).join("")}L360 240V500H0Z`;
    const snow = c.night ? "" : peaks.map(([x,y]) => `<path d="M${x.toFixed(0)} ${y.toFixed(0)}l-12 18 8-2 4 6 6-8 8 4z" fill="#FBF8F4" opacity=".9"/>`).join("");
    return `<path d="${range}" fill="${H[0]}"/>${snow}<path d="${hill(285,50,r)}" fill="${H[1]}"/><path d="${hill(340,36,r)}" fill="${H[2]}"/>`;
  }
  if (scene === "water") {
    return `<path d="M0 236C60 222 120 228 180 238S300 226 360 232V256H0Z" fill="${H[1]}"/>
      <rect y="252" width="360" height="248" fill="url(#${p}wt)"/>
      <rect x="${(c.sx-14).toFixed(0)}" y="256" width="28" height="140" fill="${c.sun}" opacity=".28"/>
      ${Array.from({length:10}, () => { const x = r()*320, y = 270 + r()*120, w = 20 + r()*40; return `<path d="M${x.toFixed(0)} ${y.toFixed(0)}h${w.toFixed(0)}" stroke="#fff" stroke-opacity=".35" stroke-width="2" stroke-linecap="round"/>`; }).join("")}
      <path d="M0 430C100 410 220 440 360 420V500H0Z" fill="${H[2]}"/>`;
  }
  if (scene === "field") {
    return `<path d="M0 240C120 232 240 236 360 240V500H0Z" fill="${H[0]}"/>
      <path d="M0 262C120 252 240 258 360 262V500H0Z" fill="${H[1]}"/>
      ${Array.from({length:7}, (_, i) => `<path d="M180 252L${(i*60 - 20).toFixed(0)} 500" stroke="${H[2]}" stroke-opacity=".35" stroke-width="3"/>`).join("")}
      <path d="M0 360C120 350 240 362 360 352V500H0Z" fill="${H[2]}" opacity=".7"/>`;
  }
  return `<path d="${hill(225,40,r)}" fill="${H[0]}"/><path d="${hill(275,46,r)}" fill="${H[1]}"/><path d="${hill(330,40,r)}" fill="${H[2]}"/>`;
}
// 땅 위에 놓이는 소재: 풍경과 함께 위로 올려서 말씀 글씨에 가리지 않게 합니다.
const GROUND = ["cross","stable","tomb","grapes","wheat","tree","stream","flowers","castle","boat","village","house","path","sprout","pillar"];
const LIFT = 70;
// 이미 그려 둔 그림(양 떼, 등불)의 풍경을 위로 올립니다. 하늘 배경 사각형 뒤의 모든 것을 dy만큼 올리고 아래를 채웁니다.
function lift(svg, dy, fill, base){
  const at = svg.indexOf('<path d="M0 '), end = svg.lastIndexOf("</svg>");
  if (at < 0) return svg;
  return svg.slice(0, at) + `<g class="land" data-base="${base}" transform="translate(0 -${dy})">` + svg.slice(at, end) + `</g><rect class="landfill" y="${500 - dy - 2}" width="360" height="${dy + 2}" fill="${fill}"/>` + svg.slice(end);
}
function artGeneric(p, card){
  const base = PALETTES[card.month] || PALETTES[SPECIAL_MONTH[card.key]] || PALETTES["1월"];
  const seed = card.day || (card.key ? card.key.length * 37 + 400 : 7);
  const r = rng(seed);
  const m = MOTIF[card.motif] || {obj:""};
  const timeKey = m.time || (card.month === "12월" && seed % 2 ? "night" : TIME_ORDER[(seed * 5) % 6]);
  const T = TIMES[timeKey];
  const sky = T ? T.sky : base.sky;
  const hills = T ? base.hills.map((h) => mix(h, T.tint, T.k)) : base.hills;
  const night = !!(T && T.night);
  const scene = m.scene || SCENES[seed % 4];
  const sx = 60 + r()*240, sy = 64 + r()*70;
  const c = {r, sky, hills, night, sun: T ? T.sun : base.sun, sx, sy, ink: mix(hills[2], "#1C1C24", .45), accent: hills[1]};
  const stars = night ? Array.from({length:24}, () => `<circle cx="${(r()*360).toFixed(0)}" cy="${(r()*210).toFixed(0)}" r="${(0.7+r()*1.3).toFixed(1)}" fill="#FFF6DD" opacity="${(.45+r()*.55).toFixed(2)}"/>`).join("") : "";
  const sun = night
    ? `<circle cx="${sx.toFixed(0)}" cy="${sy.toFixed(0)}" r="20" fill="${c.sun}"/><circle cx="${(sx+9).toFixed(0)}" cy="${(sy-6).toFixed(0)}" r="18" fill="${sky[0]}"/>`
    : `<circle cx="${sx.toFixed(0)}" cy="${sy.toFixed(0)}" r="110" fill="url(#${p}sg)"/><circle cx="${sx.toFixed(0)}" cy="${sy.toFixed(0)}" r="${timeKey === "sunset" ? 40 : 32}" fill="${c.sun}"/>`;
  const clouds = night || scene === "water" && r() < .5 ? "" : Array.from({length:1 + Math.floor(r()*2)}, () => { const x = 30 + r()*260, y = 50 + r()*110;
    return `<g fill="#fff" opacity=".7"><ellipse cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" rx="38" ry="10"/><ellipse cx="${(x+18).toFixed(0)}" cy="${(y-7).toFixed(0)}" rx="22" ry="11"/></g>`; }).join("");
  const obj = m.obj && OBJ[m.obj] ? OBJ[m.obj](c) : "";
  const ground = GROUND.includes(m.obj);
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMin slice"><defs>
    <linearGradient id="${p}sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${sky[0]}"/><stop offset="1" stop-color="${sky[1]}"/></linearGradient>
    <linearGradient id="${p}wt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${mix(sky[1], hills[0], .3)}"/><stop offset="1" stop-color="${mix(hills[2], sky[0], .2)}"/></linearGradient>
    <radialGradient id="${p}sg"><stop offset="0" stop-color="${c.sun}" stop-opacity=".9"/><stop offset="1" stop-color="${c.sun}" stop-opacity="0"/></radialGradient></defs>
    <rect width="360" height="500" fill="url(#${p}sk)"/>${stars}${sun}${clouds}
    <g class="land" data-base="300" transform="translate(0 -${LIFT})">${scenery(scene, c, p)}${ground ? obj : ""}</g>
    <rect class="landfill" y="${500 - LIFT - 2}" width="360" height="${LIFT + 2}" fill="${hills[2]}"/>${ground ? "" : obj}${m.obj === "stable" ? OBJ.star(c) : ""}
    <path d="M0 420C120 400 240 430 360 406V500H0Z" fill="#000" opacity=".16"/></svg>`;
}
function artFor(card, prefix){
  const p = prefix || ("a" + Math.random().toString(36).slice(2, 7));
  if (card.motif === "양과 초장") return lift(artShepherd(p), 55, "#457F4B", 320);
  if (card.motif === "독수리와 산") return artEagle(p);
  if (card.motif === "등불과 밤길") return lift(artLantern(p), 40, "#0E1833", 330);
  return artGeneric(p, card);
}
// 카드 크기를 보고, 땅 위 소재가 말씀 글씨 바로 위에 오도록 풍경을 올립니다.
function fitLand(card){
  if (!card) return;
  const svg = card.querySelector("svg.bg"); if (!svg) return;
  const land = svg.querySelector(".land"), fill = svg.querySelector(".landfill"); if (!land) return;
  const cw = card.clientWidth, ch = card.clientHeight; if (!cw || !ch) return;
  const s = Math.max(cw / 360, ch / 500);
  const vt = card.querySelector(".vtext");
  const clearPx = vt ? vt.offsetTop - 10 : ch * .62;
  const base = Number(land.getAttribute("data-base")) || 300;
  const dy = Math.max(30, Math.min(175, base - clearPx / s));
  land.setAttribute("transform", `translate(0 -${dy.toFixed(0)})`);
  if (fill) { fill.setAttribute("y", (500 - dy - 2).toFixed(0)); fill.setAttribute("height", (dy + 2).toFixed(0)); }
}
root.MalsseumArt = { artFor, fitLand };
})(this);
