/* 콕태그 추억 저장소 (미리보기용)
 * 사용자가 올린 사진·영상을 이 브라우저의 IndexedDB에 저장합니다.
 * 실제 서비스에서는 이 부분을 서버(예: Firebase Storage, Supabase)로 바꾸면
 * 다른 사람 휴대폰에서도 같은 추억이 보입니다.
 */
(function (root) {
  "use strict";
  const DB = "kok-memories", STORE = "items";
  let dbp = null;
  function open() {
    if (dbp) return dbp;
    dbp = new Promise((res, rej) => {
      try {
        const r = indexedDB.open(DB, 1);
        r.onupgradeneeded = () => { const s = r.result.createObjectStore(STORE, { keyPath: "id" }); s.createIndex("pet", "pet"); };
        r.onsuccess = () => res(r.result);
        r.onerror = () => rej(r.error);
      } catch (e) { rej(e); }
    });
    return dbp;
  }
  async function tx(mode, fn) {
    const db = await open();
    return new Promise((res, rej) => {
      const t = db.transaction(STORE, mode);
      const out = fn(t.objectStore(STORE));
      t.oncomplete = () => res(out && out.result !== undefined ? out.result : out);
      t.onerror = () => rej(t.error);
    });
  }
  const KokStore = {
    async list(pet) {
      try {
        const rows = await tx("readonly", (s) => s.index("pet").getAll(pet));
        return (rows || []).sort((a, b) => (b.date || "").localeCompare(a.date || "") || b.created - a.created);
      } catch (_) { return []; }
    },
    async add(pet, file, caption, date) {
      const item = {
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
        pet, caption: caption || "", date: date || new Date().toISOString().slice(0, 10),
        type: file.type.startsWith("video") ? "video" : "photo",
        blob: file, created: Date.now(),
      };
      await tx("readwrite", (s) => s.put(item));
      return item;
    },
    async remove(id) { await tx("readwrite", (s) => s.delete(id)); },
    likes(pet) { try { return Number(localStorage.getItem("kok-like-" + pet) || 0); } catch (_) { return 0; } },
    like(pet) { const n = KokStore.likes(pet) + 1; try { localStorage.setItem("kok-like-" + pet, String(n)); } catch (_) {} return n; },
  };
  root.KokStore = KokStore;
})(window);
