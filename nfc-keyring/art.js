/* 콕태그 일러스트 모음
 * 강아지·고양이 캐릭터, 키링 앞/뒤 디자인, 샘플 사진 장면을 SVG 문자열로 만듭니다.
 * 브라우저(window.KokArt)와 Node(require) 양쪽에서 씁니다.
 */
(function (root) {
  "use strict";

  const PAL = {
    dog: { fur: "#eab57c", fur2: "#c8864a", ear: "#b9733a", muzzle: "#fff5e8", back: "#ffe1c4", backInk: "#7a4520", accent: "#ff8f6b" },
    cat: { fur: "#f7c46c", fur2: "#e2963a", ear: "#f7c46c", inner: "#f6a7b2", muzzle: "#fffaf0", back: "#d9edff", backInk: "#2c5785", accent: "#6aa8ff" },
  };
  const INK = "#3a2a20";
  const CUT = "#3a2a20";

  // ---------- 실루엣 (키링 칼선 · 테두리용) ----------
  function silhouette(kind) {
    if (kind === "cat") {
      return `<ellipse cx="150" cy="175" rx="108" ry="88"/>
        <path d="M60 140 L64 52 Q68 38 82 46 L142 98 Z"/>
        <path d="M240 140 L236 52 Q232 38 218 46 L158 98 Z"/>`;
    }
    return `<ellipse cx="150" cy="165" rx="100" ry="90"/>
      <ellipse cx="62" cy="172" rx="34" ry="62" transform="rotate(18 62 172)"/>
      <ellipse cx="238" cy="172" rx="34" ry="62" transform="rotate(-18 238 172)"/>`;
  }

  // ---------- 얼굴 ----------
  function eyes(kind, mood) {
    const y = kind === "cat" ? 160 : 158;
    const L = kind === "cat" ? 106 : 108, R = kind === "cat" ? 194 : 192;
    const open = (x) => kind === "cat"
      ? `<ellipse cx="${x}" cy="${y}" rx="13" ry="16" fill="${INK}"/><circle cx="${x + 5}" cy="${y - 6}" r="5" fill="#fff"/><circle cx="${x - 4}" cy="${y + 6}" r="2.4" fill="#fff"/>`
      : `<circle cx="${x}" cy="${y}" r="14" fill="${INK}"/><circle cx="${x + 5}" cy="${y - 6}" r="5" fill="#fff"/><circle cx="${x - 4}" cy="${y + 6}" r="2.5" fill="#fff"/>`;
    const shut = (x) => `<path d="M${x - 14} ${y} Q${x} ${y + 12} ${x + 14} ${y}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    const happy = (x) => `<path d="M${x - 14} ${y + 4} Q${x} ${y - 10} ${x + 14} ${y + 4}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    if (mood === "sleep") return shut(L) + shut(R);
    if (mood === "wink") return open(L) + happy(R);
    if (mood === "smile") return happy(L) + happy(R);
    return open(L) + open(R);
  }

  function dogFace(mood, p) {
    return `
      <ellipse cx="102" cy="150" rx="32" ry="28" fill="${p.fur2}" opacity=".55"/>
      <ellipse cx="150" cy="208" rx="54" ry="40" fill="${p.muzzle}"/>
      ${eyes("dog", mood)}
      <ellipse cx="86" cy="196" rx="15" ry="8" fill="#ff9aa8" opacity=".55"/>
      <ellipse cx="214" cy="196" rx="15" ry="8" fill="#ff9aa8" opacity=".55"/>
      ${mood === "sleep" ? "" : `<ellipse cx="150" cy="224" rx="9" ry="11" fill="#ff8fa3"/>`}
      <path d="M136 186 Q150 177 164 186 Q160 199 150 201 Q140 199 136 186 Z" fill="${INK}"/>
      <ellipse cx="146" cy="184" rx="4" ry="2" fill="#fff" opacity=".6"/>
      <path d="M150 201 V211 M150 211 Q141 222 131 214 M150 211 Q159 222 169 214" fill="none" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/>`;
  }

  function catFace(mood, p) {
    return `
      <path d="M76 118 L80 68 L124 102 Z M224 118 L220 68 L176 102 Z" fill="${p.inner}"/>
      <g stroke="${p.fur2}" stroke-width="9" stroke-linecap="round" fill="none">
        <path d="M150 92 V116"/><path d="M127 97 L132 117"/><path d="M173 97 L168 117"/>
        <path d="M46 168 L74 174"/><path d="M48 188 L76 188"/><path d="M254 168 L226 174"/><path d="M252 188 L224 188"/>
      </g>
      <ellipse cx="134" cy="202" rx="22" ry="17" fill="${p.muzzle}"/>
      <ellipse cx="166" cy="202" rx="22" ry="17" fill="${p.muzzle}"/>
      ${eyes("cat", mood)}
      <ellipse cx="84" cy="196" rx="14" ry="8" fill="#ff9aa8" opacity=".55"/>
      <ellipse cx="216" cy="196" rx="14" ry="8" fill="#ff9aa8" opacity=".55"/>
      <path d="M141 186 Q150 181 159 186 Q154 195 150 196 Q146 195 141 186 Z" fill="#f2879a"/>
      <path d="M150 196 Q143 207 134 201 M150 196 Q157 207 166 201" fill="none" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/>
      <g stroke="${INK}" stroke-width="2.2" stroke-linecap="round" opacity=".7">
        <path d="M108 202 L62 194"/><path d="M108 210 L60 214"/><path d="M192 202 L238 194"/><path d="M192 210 L240 214"/>
      </g>`;
  }

  /* 캐릭터 머리(300×300 박스). opts: mood(open|smile|wink|sleep), body, hat */
  function petArt(kind, opts) {
    opts = opts || {};
    const p = PAL[kind];
    const mood = opts.mood || "open";
    let s = "";
    if (opts.body) {
      s += kind === "cat"
        ? `<path d="M232 300 Q290 280 280 236" fill="none" stroke="${p.fur2}" stroke-width="16" stroke-linecap="round"/>
           <ellipse cx="150" cy="292" rx="88" ry="58" fill="${p.fur}"/><ellipse cx="150" cy="300" rx="44" ry="36" fill="${p.muzzle}"/>`
        : `<ellipse cx="150" cy="292" rx="84" ry="56" fill="${p.fur}"/><ellipse cx="150" cy="300" rx="42" ry="34" fill="${p.muzzle}"/>
           <ellipse cx="112" cy="336" rx="18" ry="12" fill="${p.fur}"/><ellipse cx="188" cy="336" rx="18" ry="12" fill="${p.fur}"/>`;
    }
    if (kind === "cat") {
      s += `<g fill="${p.fur}">${silhouette("cat")}</g>${catFace(mood, p)}`;
    } else {
      s += `<ellipse cx="150" cy="165" rx="100" ry="90" fill="${p.fur}"/>
        <ellipse cx="62" cy="172" rx="34" ry="62" transform="rotate(18 62 172)" fill="${p.ear}"/>
        <ellipse cx="238" cy="172" rx="34" ry="62" transform="rotate(-18 238 172)" fill="${p.ear}"/>
        <path d="M128 80 Q140 62 150 78 Q160 62 172 80" fill="${p.fur}" stroke="${p.fur}" stroke-width="6" stroke-linejoin="round"/>
        ${dogFace(mood, p)}`;
    }
    if (opts.hat) {
      const top = kind === "cat" ? 90 : 76;
      s += `<g transform="rotate(-12 150 ${top})"><path d="M118 ${top + 6} L150 ${top - 62} L182 ${top + 6} Z" fill="#7b8cff"/>
        <path d="M128 ${top - 14} L172 ${top - 14} M138 ${top - 36} L162 ${top - 36}" stroke="#ffd84d" stroke-width="7" stroke-linecap="round"/>
        <circle cx="150" cy="${top - 64}" r="11" fill="#ff7a93"/></g>`;
    }
    return s;
  }

  // ---------- 키링 디자인 ----------
  function paw(x, y, s, fill, rot) {
    return `<g transform="translate(${x} ${y}) rotate(${rot || 0}) scale(${s})" fill="${fill}">
      <ellipse cx="0" cy="6" rx="9" ry="7.5"/><circle cx="-9" cy="-5" r="3.8"/><circle cx="-3" cy="-10" r="3.8"/><circle cx="4" cy="-10" r="3.8"/><circle cx="10" cy="-5" r="3.8"/></g>`;
  }
  function nfcMark(cx, cy, color) {
    return `<g fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round">
      <rect x="${cx - 22}" y="${cy - 30}" width="44" height="60" rx="9"/>
      <path d="M${cx + 30} ${cy - 14} Q${cx + 40} ${cy} ${cx + 30} ${cy + 14}"/>
      <path d="M${cx + 40} ${cy - 24} Q${cx + 56} ${cy} ${cx + 40} ${cy + 24}"/>
      <path d="M${cx - 30} ${cy - 14} Q${cx - 40} ${cy} ${cx - 30} ${cy + 14}"/>
      <path d="M${cx - 40} ${cy - 24} Q${cx - 56} ${cy} ${cx - 40} ${cy + 24}"/></g>
      <circle cx="${cx}" cy="${cy + 18}" r="3.5" fill="${color}"/>`;
  }
  function esc(t) { return String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

  /* kind: dog|cat, side: front|back, opts: { name, guide(칩 위치 표시), id(고유 접두사) } */
  function keyringSVG(kind, side, opts) {
    opts = opts || {};
    const p = PAL[kind];
    const id = (opts.id || "kr") + "-" + kind + "-" + side;
    const loopY = kind === "cat" ? 26 : 22;
    const tabTo = kind === "cat" ? 110 : 100;
    const sil = `${silhouette(kind)}<circle cx="150" cy="${loopY}" r="22"/><rect x="136" y="${loopY}" width="28" height="${tabTo - loopY}" rx="6"/>`;
    const name = esc(opts.name || (kind === "cat" ? "NABI" : "CHOCO"));
    let art;
    if (side === "front") {
      art = petArt(kind, { mood: "open" });
    } else {
      const ink = p.backInk;
      const cy = kind === "cat" ? 178 : 168;
      art = `<g fill="${p.back}">${silhouette(kind)}</g>
        ${paw(78, cy - 40, 0.9, p.accent, -20)}${paw(226, cy - 44, 0.8, p.accent, 18)}
        ${paw(70, cy + 46, 0.7, p.accent, 10)}${paw(232, cy + 42, 0.75, p.accent, -14)}
        <g transform="translate(150 ${cy - 34}) scale(.72) translate(-150 ${-(cy - 34)})">${nfcMark(150, cy - 34, ink)}</g>
        <text x="150" y="${cy + 20}" text-anchor="middle" font-family="Jua, 'Arial Rounded MT Bold', sans-serif" font-size="23" fill="${ink}">콕! 대보세요</text>
        <text x="150" y="${cy + 48}" text-anchor="middle" font-family="Jua, 'Arial Rounded MT Bold', sans-serif" font-size="21" letter-spacing="2" fill="${p.accent}">${name}</text>
        ${kind === "cat"
          ? `<path d="M128 ${cy + 66} q10 -9 22 0 q-12 9 -22 0 z m22 0 l8 -6 v12 z" fill="${ink}" opacity=".7"/>`
          : `<path d="M134 ${cy + 64} h32 m-32 0 a4 4 0 1 1 -4 -4 m4 4 a4 4 0 1 0 -4 4 m36 -4 a4 4 0 1 0 4 -4 m-4 4 a4 4 0 1 1 4 4" stroke="${ink}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>`}`;
      if (opts.guide) {
        art += `<circle cx="150" cy="${cy}" r="62" fill="none" stroke="#e5484d" stroke-width="2" stroke-dasharray="6 5"/>
          <text x="150" y="${cy - 68}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#e5484d">NFC 칩 (지름 25mm)</text>`;
      }
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-22 -16 344 312" role="img" aria-label="${kind === "cat" ? "고양이" : "강아지"} 키링 ${side === "front" ? "앞면" : "뒷면"}">
  <defs>
    <g id="${id}-sil">${sil}</g>
    <mask id="${id}-hole"><rect x="-40" y="-40" width="400" height="400" fill="#fff"/><circle cx="150" cy="${loopY}" r="9" fill="#000"/></mask>
  </defs>
  <g mask="url(#${id}-hole)">
    <use href="#${id}-sil" fill="${CUT}" stroke="${CUT}" stroke-width="26" stroke-linejoin="round"/>
    <use href="#${id}-sil" fill="#ffffff" stroke="#ffffff" stroke-width="22" stroke-linejoin="round"/>
    ${art}
  </g>
</svg>`;
  }

  // ---------- 샘플 사진 장면 ----------
  const SCENES = {
    park: { bg: "#cfe9ff", mood: "open" },
    nap: { bg: "#2f3766", mood: "sleep" },
    birthday: { bg: "#ffd9e3", mood: "smile", hat: true },
    snack: { bg: "#fff0bf", mood: "wink" },
    beach: { bg: "#c4f0ea", mood: "smile" },
    home: { bg: "#efe3ff", mood: "open" },
  };
  function sceneProps(scene, kind) {
    switch (scene) {
      case "park": return { back: `<circle cx="330" cy="70" r="34" fill="#ffd84d"/><rect y="300" width="400" height="100" fill="#8fd16a"/>
        <path d="M0 300 Q100 285 200 300 T400 300 V310 H0Z" fill="#7cc257"/>`, front: `<circle cx="330" cy="330" r="30" fill="#ff6b6b"/><path d="M304 318 Q330 336 356 318" stroke="#fff" stroke-width="5" fill="none"/>` };
      case "nap": return { back: `<circle cx="320" cy="80" r="30" fill="#ffe9a3"/><circle cx="334" cy="72" r="28" fill="#2f3766"/>
        ${[[60, 60], [120, 40], [220, 70], [370, 150], [40, 160]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="3" fill="#fff" opacity=".8"/>`).join("")}
        <ellipse cx="200" cy="360" rx="190" ry="60" fill="#8f9bff"/>`, front: `<text x="300" y="150" font-family="Jua, sans-serif" font-size="40" fill="#fff" opacity=".9">Z</text><text x="330" y="118" font-family="Jua, sans-serif" font-size="28" fill="#fff" opacity=".7">z</text>` };
      case "birthday": return { back: [[40, 60, "#7b8cff"], [90, 120, "#ffd84d"], [330, 60, "#5bd1a8"], [360, 160, "#ff7a93"], [60, 220, "#5bd1a8"], [300, 230, "#7b8cff"]]
        .map(([x, y, c], k) => `<rect x="${x}" y="${y}" width="14" height="8" rx="2" fill="${c}" transform="rotate(${k * 37} ${x} ${y})"/>`).join(""),
        front: `<rect x="285" y="300" width="90" height="60" rx="10" fill="#fff"/><rect x="285" y="300" width="90" height="18" rx="9" fill="#ff9fb4"/><rect x="326" y="276" width="8" height="24" fill="#7b8cff"/><path d="M330 262 q6 8 0 14 q-6 -6 0 -14z" fill="#ffb02e"/>` };
      case "snack": return { back: `<circle cx="70" cy="80" r="40" fill="#ffe08a"/>`, front: kind === "cat"
        ? `<g transform="translate(300 320) rotate(-15)"><ellipse rx="44" ry="20" fill="#7fb6ff"/><path d="M40 0 L66 -18 V18Z" fill="#7fb6ff"/><circle cx="-24" cy="-4" r="4" fill="${INK}"/></g>`
        : `<g transform="translate(310 330) rotate(-20)" fill="#fff" stroke="#e6d3b3" stroke-width="3"><rect x="-38" y="-9" width="76" height="18" rx="9"/><circle cx="-40" cy="-10" r="12"/><circle cx="-40" cy="10" r="12"/><circle cx="40" cy="-10" r="12"/><circle cx="40" cy="10" r="12"/></g>` };
      case "beach": return { back: `<circle cx="80" cy="70" r="30" fill="#fff3a6"/><path d="M0 260 Q50 245 100 260 T200 260 T300 260 T400 260 V400 H0Z" fill="#5cc8e8"/>
        <path d="M0 320 Q100 300 200 320 T400 320 V400 H0Z" fill="#f6dfa8"/>`, front: `<g transform="translate(330 330)"><path d="M-30 0 A30 30 0 0 1 30 0Z" fill="#ff7a93"/><path d="M-10 0 A10 30 0 0 1 10 0Z" fill="#fff"/><rect x="-2" y="0" width="4" height="40" fill="#8a6a4a"/></g>` };
      default: return { back: `<rect x="40" y="50" width="90" height="70" rx="8" fill="#fff" opacity=".7"/><rect x="270" y="40" width="80" height="100" rx="8" fill="#fff" opacity=".7"/><rect y="320" width="400" height="80" fill="#d9c7f5"/>`,
        front: `<path d="M330 320 q-20 -26 0 -40 q20 14 0 40z" fill="#ff7a93"/>` };
    }
  }

  /* opts: { date, animate } */
  function photoSVG(kind, scene, opts) {
    opts = opts || {};
    const sc = SCENES[scene] || SCENES.home;
    const props = sceneProps(scene, kind);
    const anim = opts.animate
      ? `<style>.kk-bob{animation:kkbob 1.4s ease-in-out infinite;transform-origin:200px 360px}.kk-tilt{animation:kktilt 2.8s ease-in-out infinite;transform-origin:200px 250px}
         @keyframes kkbob{50%{transform:translateY(-14px)}}@keyframes kktilt{25%{transform:rotate(-6deg)}75%{transform:rotate(6deg)}}
         @media (prefers-reduced-motion: reduce){.kk-bob,.kk-tilt{animation:none}}</style>` : "";
    const date = opts.date ? `<text x="384" y="388" text-anchor="end" font-family="'Courier New', monospace" font-size="16" font-weight="700" fill="#ff8a3d" opacity=".9">${esc(opts.date.replace(/-/g, "."))}</text>` : "";
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice">${anim}
      <rect width="400" height="400" fill="${sc.bg}"/>${props.back}
      <g class="kk-bob"><g class="kk-tilt"><g transform="translate(60 40) scale(.94)">${petArt(kind, { mood: sc.mood, body: true, hat: sc.hat })}</g></g></g>
      ${props.front}${date}</svg>`;
  }

  const api = { PAL, petArt, keyringSVG, photoSVG, SCENES: Object.keys(SCENES) };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.KokArt = api;
})(typeof window !== "undefined" ? window : globalThis);
