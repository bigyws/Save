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
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMid slice">
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
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMid slice">
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
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMid slice">
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


// 그림을 따로 그리지 않은 주제는 월별 색과 날마다 다른 풍경으로 그립니다.
const PALETTES = {
  "1월":  {sky:["#FCE3C8","#F4B79C"], hills:["#CDBBD9","#A08EC0","#6F6295"], sun:"#FFF4E2"},
  "2월":  {sky:["#FBDCD6","#F2B2AE"], hills:["#E8AAA5","#C98088","#9C5D6D"], sun:"#FFF1EC"},
  "3월":  {sky:["#E1EEF5","#B5D2E5"], hills:["#ADC9A3","#82A97E","#5A825F"], sun:"#FFFBEA"},
  "4월":  {sky:["#FFF1D6","#FFD39A"], hills:["#C2E1AA","#8EC37C","#5F9B58"], sun:"#FFF8E4"},
  "5월":  {sky:["#E8F4EA","#C2E1C8"], hills:["#A2D2A3","#72B17B","#4D8D5B"], sun:"#FFFBEB"},
  "6월":  {sky:["#DFEFF7","#ADD2EA"], hills:["#9EC3DB","#709FC2","#4C79A1"], sun:"#FFFDF2"},
  "7월":  {sky:["#E4F5F2","#B4E0D9"], hills:["#92D0B9","#60AF96","#3F8C77"], sun:"#FFFBEA"},
  "8월":  {sky:["#2E4A7B","#F1C8A2"], hills:["#A9B4D6","#7287BC","#3E5288"], sun:"#FFF4DA"},
  "9월":  {sky:["#F5EDDD","#E8D2AC"], hills:["#CFB68C","#AA8D63","#806845"], sun:"#FFF9EC"},
  "10월": {sky:["#F9E3C6","#EDB17C"], hills:["#DA935B","#B76F3D","#8A4F2B"], sun:"#FFF3DF"},
  "11월": {sky:["#FCE8C2","#F1C076"], hills:["#E4B75D","#C99741","#9C7431"], sun:"#FFF6DE"},
  "12월": {sky:["#0E1A3A","#3B5487"], hills:["#1C2D58","#16244A","#0E1833"], sun:"#FBEFCF", night:true},
};
const SPECIAL_MONTH = {welcome:"1월", easter:"4월", harvest:"7월", thanksgiving:"11월", leap:"3월"};
function rng(seed){ let s = seed * 9301 + 49297; return () => ((s = (s * 9301 + 49297) % 233280) / 233280); }
function hill(y, amp, r){
  const a = y + (r()-.5)*amp, b = y + (r()-.5)*amp*1.6, c = y + (r()-.5)*amp;
  return `M0 ${a}C90 ${b} 170 ${c} 250 ${b+10}S330 ${a-6} 360 ${c}V500H0Z`;
}
function emblem(motif, P){
  if (motif === "십자가 언덕") return `<g transform="translate(180 168)" fill="#2B2A33" opacity=".85"><rect x="-4" y="-52" width="8" height="70" rx="2"/><rect x="-22" y="-36" width="44" height="7" rx="2"/></g>`;
  if (motif.startsWith("성탄")) return `<g transform="translate(250 92)" fill="#FFF3C4"><path d="M0-22L5-5L22 0L5 5L0 22L-5 5L-22 0L-5-5Z"/><circle r="40" fill="#FFF3C4" opacity=".12"/></g>`;
  if (motif === "부활의 아침") return `<g fill="#FFF6DD" opacity=".22"><path d="M180 240L80 0H120Z"/><path d="M180 240L165 0H200Z"/><path d="M180 240L250 0H290Z"/></g>`;
  if (motif === "맞잡은 두 손" || motif === "두 손 모아 축복") return `<path d="M180 150c-14-16-40-6-40 14c0 18 22 30 40 44c18-14 40-26 40-44c0-20-26-30-40-14z" fill="#fff" opacity=".55"/>`;
  return "";
}
function artGeneric(p, card){
  const P = PALETTES[card.month] || PALETTES[SPECIAL_MONTH[card.key]] || PALETTES["1월"];
  const r = rng(card.day || (card.key ? card.key.length * 37 : 7));
  const sx = 70 + r()*220, sy = 70 + r()*80;
  const stars = P.night ? Array.from({length:16},()=>`<circle cx="${(r()*360).toFixed(0)}" cy="${(r()*200).toFixed(0)}" r="${(0.8+r()*1.2).toFixed(1)}" fill="#FFF6DD" opacity="${(.5+r()*.5).toFixed(2)}"/>`).join("") : "";
  const birds = P.night ? "" : Array.from({length:2+Math.floor(r()*3)},()=>{const x=30+r()*280,y=40+r()*90,w=5+r()*5;return `<path d="M${x.toFixed(0)} ${y.toFixed(0)}q${w} -${w} ${w*2} 0q${w} -${w} ${w*2} 0" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="1.8" stroke-linecap="round"/>`}).join("");
  return `<svg class="bg" viewBox="0 0 360 500" preserveAspectRatio="xMidYMid slice"><defs>
    <linearGradient id="${p}sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${P.sky[0]}"/><stop offset="1" stop-color="${P.sky[1]}"/></linearGradient>
    <radialGradient id="${p}sg"><stop offset="0" stop-color="${P.sun}" stop-opacity=".9"/><stop offset="1" stop-color="${P.sun}" stop-opacity="0"/></radialGradient></defs>
    <rect width="360" height="500" fill="url(#${p}sk)"/>${stars}
    <circle cx="${sx}" cy="${sy}" r="110" fill="url(#${p}sg)"/><circle cx="${sx}" cy="${sy}" r="${P.night?22:34}" fill="${P.sun}"/>
    ${birds}${emblem(card.motif || "", P)}
    <path d="${hill(225,40,r)}" fill="${P.hills[0]}"/><path d="${hill(275,46,r)}" fill="${P.hills[1]}"/><path d="${hill(330,40,r)}" fill="${P.hills[2]}"/>
    <path d="M0 410C120 390 240 420 360 396V500H0Z" fill="#000" opacity=".18"/></svg>`;
}
function artFor(card, prefix){
  const p = prefix || ("a" + Math.random().toString(36).slice(2, 7));
  if (card.motif === "양과 초장") return artShepherd(p);
  if (card.motif === "독수리와 산") return artEagle(p);
  if (card.motif === "등불과 밤길") return artLantern(p);
  return artGeneric(p, card);
}
root.MalsseumArt = { artFor };
})(this);
