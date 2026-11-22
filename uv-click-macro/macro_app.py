# -*- coding: utf-8 -*-
"""
UV 인쇄기 클릭 자동화 (클릭 매크로)

- 단계(클릭 위치, 대기, 키 입력, 글자 입력)를 순서대로 등록해 두고
  [시작]을 누르면 그대로 실행합니다.
- 작업별로 여러 개를 저장해 두고 골라서 쓸 수 있습니다.
- 클릭 녹화: 직접 한 번 클릭해 보면 위치와 간격이 단계로 기록됩니다.

단축키 (다른 프로그램이 앞에 있어도 동작)
  F4  : 클릭 녹화 시작 / 다시 누르면 녹화 끝 (녹화 중엔 창이 내려감)
  F8  : 지금 마우스가 있는 위치를 '클릭' 단계로 추가
  F12 : 단계에 END 표시 / 다시 누르면 END 해제 (단계 번호는 추가되지 않음)
  F9  : 시작
  F10 : 정지 (녹화 중이면 녹화 종료)
  ESC : 실행 중일 때 정지
  비상정지: 마우스를 화면 왼쪽 위 구석으로 확 밀면 즉시 멈춥니다.
"""
import ctypes
import json
import os
import queue
import re
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# 윈도우 화면 배율(125%, 150%)에서도 좌표가 어긋나지 않도록 설정
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

import pyautogui
import pyperclip
from pynput import keyboard, mouse

pyautogui.FAILSAFE = True   # 마우스를 왼쪽 위 구석으로 → 비상정지
pyautogui.PAUSE = 0.03

VERSION = "v.23"
CREDIT = f"made by. 양원식 {VERSION}"
APP_TITLE = f"UV 인쇄 클릭 자동화 [{CREDIT}]"
COMPANY = "신신기획"

# 업그레이드 내역 (최신이 위) — 프로그램 맨 위 [made by. ...] 를 누르면 보입니다
CHANGELOG = [
    ("v.23", "11/22", "시작 확인 창은 총 수량이 납품수량의 95% 이상일 때만 표시"),
    ("v.22", "11/22", "납품수량 입력 (채우면 총 소재 수량 빨간색), F9 시작 전 확인 창"),
    ("v.21", "11/21", "위쪽 버튼 줄 오른쪽 끝을 목록 오른쪽 끝에 맞춤"),
    ("v.20", "11/21", "위쪽 새 작업·저장·다른 이름·삭제 버튼 넓게, 버튼 이름 '녹화 F4'"),
    ("v.19", "11/21", "녹화 단축키 F4 로 변경, 버전 표시와 업그레이드 내역 보기 추가"),
    ("v.18", "11/21", "오른쪽 버튼 한 줄 배치, 창 가로 폭 줄이기"),
    ("v.17", "11/21", "컴팩트 화면 적용, 녹화 단축키 F3"),
    ("v.16", "11/21", "녹화 단축키 F7 (한 번 누르면 녹화, 다시 누르면 끝)"),
    ("v.15", "11/21", "컴팩트 화면, 후대기 기본 0.2초"),
    ("v.14", "11/21", "총 소재 수량 ＋1장 / －1장 버튼"),
    ("v.13", "11/20", "F12 는 번호 추가 없이 END 만 켜기/끄기"),
    ("v.12", "11/20", "F12 같은 위치에서 다시 누르면 END 해제"),
    ("v.11", "11/20", "F12 로 END 표시"),
    ("v.10", "11/20", "메모에 END 가 없으면 카운트 안 함"),
    ("v.9", "11/20", "[made by. 양원식] 표시"),
    ("v.8", "11/20", "SHINSHIN 로고, SS 아이콘"),
    ("v.7", "11/20", "맨 위 제목줄 추가"),
    ("v.6", "11/20", "계산식 문구 숨기기, 소리 알림 삭제"),
    ("v.5", "11/20", "카운터 단위 '판' → '번'"),
    ("v.4", "11/20", "END 메모로 카운트, 한 번에 소재 수량, 계산기 삭제"),
    ("v.3", "11/19", "생산 카운터, 일시정지(F11), 계산기 추가"),
    ("v.2", "11/19", "Python 없이 실행되는 exe 파일"),
    ("v.1", "11/19", "실행 파일 이름 정리 (압축 풀 때 글자 깨짐 방지)"),
    ("v.0", "11/19", "처음 만듦: 위치 찍기(F8), 클릭 녹화, 작업 저장, 시작/정지"),
]
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_DIR = os.path.join(BASE_DIR, "macros")
# exe 안에 같이 묶인 파일 위치 (로고 등)
BUNDLE_DIR = getattr(sys, "_MEIPASS", BASE_DIR)


def find_logo(height):
    """로고 파일 찾기: exe 옆에 logo.png 가 있으면 그것을, 없으면 내장된 로고 중
    원하는 높이에 가장 가까운 것을 사용"""
    for name in ("logo.png", "logo.gif"):
        path = os.path.join(BASE_DIR, name)
        if os.path.isfile(path):
            return path, True
    best = None
    for d in (os.path.join(BUNDLE_DIR, "assets"), os.path.join(BASE_DIR, "assets")):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            m = re.fullmatch(r"logo_(\d+)\.png", f)
            if m:
                h = int(m.group(1))
                score = (h > height, abs(h - height))   # 넘치지 않는 것 우선
                if best is None or score < best[0]:
                    best = (score, os.path.join(d, f))
        if best:
            return best[1], False
    return None, False


def find_icon():
    for d in (os.path.join(BUNDLE_DIR, "assets"), os.path.join(BASE_DIR, "assets")):
        path = os.path.join(d, "icon_64.png")
        if os.path.isfile(path):
            return path
    return None


SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

STEP_TYPES = {
    "click": "클릭",
    "double": "더블클릭",
    "right": "오른쪽클릭",
    "move": "마우스이동",
    "wait": "대기",
    "key": "키 입력",
    "text": "글자 입력",
}
TYPE_BY_LABEL = {v: k for k, v in STEP_TYPES.items()}
POSITION_TYPES = ("click", "double", "right", "move")


def new_step(kind="click", x=0, y=0, value="", delay=0.2, memo=""):
    return {"type": kind, "x": int(x), "y": int(y), "value": value,
            "delay": float(delay), "memo": memo}


def safe_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', "_", name).strip()
    return name or "이름없음"


def list_macros():
    os.makedirs(MACRO_DIR, exist_ok=True)
    names = [f[:-5] for f in os.listdir(MACRO_DIR) if f.lower().endswith(".json")]
    return sorted(names)


def load_macro(name):
    with open(os.path.join(MACRO_DIR, name + ".json"), encoding="utf-8") as f:
        data = json.load(f)
    steps = [new_step(s.get("type", "click"), s.get("x", 0), s.get("y", 0),
                      s.get("value", ""), s.get("delay", 0.5), s.get("memo", ""))
             for s in data.get("steps", [])]
    return {"name": name, "repeat": int(data.get("repeat", 1)),
            "start_wait": float(data.get("start_wait", 2)),
            "per_plate": max(1, int(data.get("per_plate", 1))),
            "steps": steps}


def save_macro(macro):
    os.makedirs(MACRO_DIR, exist_ok=True)
    path = os.path.join(MACRO_DIR, safe_filename(macro["name"]) + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"repeat": macro["repeat"], "start_wait": macro["start_wait"],
                   "per_plate": macro.get("per_plate", 1),
                   "steps": macro["steps"]}, f, ensure_ascii=False, indent=2)


def load_settings():
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def is_end(step):
    """메모가 END 인 단계 → 한 번이 끝난 것으로 보고 카운터 +1"""
    return step.get("memo", "").strip().upper() == "END"


class StepDialog(tk.Toplevel):
    """단계 추가/수정 창"""

    def __init__(self, master, step, title="단계 편집"):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.result = None
        self.step = dict(step)

        pad = {"padx": 6, "pady": 4}
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="동작").grid(row=0, column=0, sticky="w", **pad)
        self.kind = tk.StringVar(value=STEP_TYPES[self.step["type"]])
        cb = ttk.Combobox(frm, textvariable=self.kind, state="readonly",
                          values=list(STEP_TYPES.values()), width=14)
        cb.grid(row=0, column=1, columnspan=2, sticky="w", **pad)
        cb.bind("<<ComboboxSelected>>", lambda e: self._refresh())

        ttk.Label(frm, text="X / Y 좌표").grid(row=1, column=0, sticky="w", **pad)
        self.x = tk.StringVar(value=str(self.step["x"]))
        self.y = tk.StringVar(value=str(self.step["y"]))
        self.ex = ttk.Entry(frm, textvariable=self.x, width=7)
        self.ey = ttk.Entry(frm, textvariable=self.y, width=7)
        self.ex.grid(row=1, column=1, sticky="w", **pad)
        self.ey.grid(row=1, column=2, sticky="w", **pad)
        self.pick_btn = ttk.Button(frm, text="3초 뒤 마우스 위치 가져오기",
                                   command=self._pick)
        self.pick_btn.grid(row=2, column=1, columnspan=2, sticky="w", **pad)

        self.value_label = ttk.Label(frm, text="값")
        self.value_label.grid(row=3, column=0, sticky="w", **pad)
        self.value = tk.StringVar(value=self.step["value"])
        self.ev = ttk.Entry(frm, textvariable=self.value, width=28)
        self.ev.grid(row=3, column=1, columnspan=2, sticky="w", **pad)
        self.hint = ttk.Label(frm, text="", foreground="#666")
        self.hint.grid(row=4, column=1, columnspan=2, sticky="w", padx=6)

        ttk.Label(frm, text="실행 후 대기(초)").grid(row=5, column=0, sticky="w", **pad)
        self.delay = tk.StringVar(value=str(self.step["delay"]))
        ttk.Entry(frm, textvariable=self.delay, width=7).grid(
            row=5, column=1, sticky="w", **pad)

        ttk.Label(frm, text="메모").grid(row=6, column=0, sticky="w", **pad)
        self.memo = tk.StringVar(value=self.step["memo"])
        ttk.Entry(frm, textvariable=self.memo, width=28).grid(
            row=6, column=1, columnspan=2, sticky="w", **pad)
        ttk.Label(frm, text="※ 메모에 END 라고 적으면 이 단계에서 카운터 +1번 (F12 로 켜고 끄기)",
                  foreground="#b00020").grid(row=7, column=1, columnspan=2, sticky="w", padx=6)

        btns = ttk.Frame(frm)
        btns.grid(row=8, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(btns, text="확인", command=self._ok).pack(side="left", padx=4)
        ttk.Button(btns, text="취소", command=self.destroy).pack(side="left", padx=4)

        self._refresh()
        self.bind("<Return>", lambda e: self._ok())
        self.bind("<Escape>", lambda e: self.destroy())
        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def _refresh(self):
        kind = TYPE_BY_LABEL[self.kind.get()]
        pos = kind in POSITION_TYPES
        for w in (self.ex, self.ey, self.pick_btn):
            w.state(["!disabled"] if pos else ["disabled"])
        if kind == "key":
            self.ev.state(["!disabled"])
            self.value_label.config(text="키")
            self.hint.config(text="예: enter, tab, esc, f5, ctrl+s, alt+f4")
        elif kind == "text":
            self.ev.state(["!disabled"])
            self.value_label.config(text="입력할 글자")
            self.hint.config(text="한글도 가능 (붙여넣기 방식)")
        else:
            self.ev.state(["disabled"])
            self.value_label.config(text="값")
            self.hint.config(text="")

    def _pick(self):
        self.pick_btn.config(text="마우스를 대상 위에 올려두세요… 3")

        def tick(n):
            if n == 0:
                x, y = pyautogui.position()
                self.x.set(str(x))
                self.y.set(str(y))
                self.pick_btn.config(text="3초 뒤 마우스 위치 가져오기")
                self.lift()
                return
            self.pick_btn.config(text=f"마우스를 대상 위에 올려두세요… {n}")
            self.after(1000, tick, n - 1)

        tick(3)

    def _ok(self):
        try:
            kind = TYPE_BY_LABEL[self.kind.get()]
            delay = float(self.delay.get() or 0)
            x = int(float(self.x.get() or 0))
            y = int(float(self.y.get() or 0))
        except ValueError:
            messagebox.showerror(APP_TITLE, "좌표와 대기시간은 숫자로 입력해 주세요.", parent=self)
            return
        if kind in ("key", "text") and not self.value.get().strip():
            messagebox.showerror(APP_TITLE, "값을 입력해 주세요.", parent=self)
            return
        if delay < 0:
            delay = 0
        self.result = new_step(kind, x, y, self.value.get(), delay, self.memo.get())
        self.destroy()


class StartConfirm(tk.Toplevel):
    """납품수량 95% 이상일 때 F9 / 시작 누르면 먼저 뜨는 확인 창"""

    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.result = False
        self.title("시작 확인")
        self.resizable(False, False)
        self.transient(app.root)
        self.attributes("-topmost", True)
        m = app.macro
        n = app._per_plate()
        frm = tk.Frame(self, bg="#ffffff", padx=18, pady=12)
        frm.pack(fill="both", expand=True)
        tk.Label(frm, text="⚠ 자동 클릭을 시작할까요?", bg="#ffffff", fg="#b00020",
                 font=("맑은 고딕", 13, "bold")).pack(anchor="w")
        pct = int(app._total() * 100 / app.target) if app.target else 0
        tk.Label(frm, text=f"납품수량의 {pct}% 를 채웠습니다. 남은 수량을 확인하세요.", bg="#ffffff", fg="#555",
                 font=("맑은 고딕", 9)).pack(anchor="w", pady=(2, 8))
        info = tk.Frame(frm, bg="#f4f6fa", padx=12, pady=8)
        info.pack(fill="x")
        rows = [("작업", m["name"] or "(저장 안 됨)"),
                ("반복", f'{m["repeat"]}회  (한 번에 소재 {n}장)'),
                ("이번에 추가", f'{m["repeat"] * n:,}장' if any(is_end(s) for s in m["steps"])
                 else "END 없음 — 세지 않음"),
                ("총 소재 수량", f"{app._total():,}장")]
        if app.target:
            left = max(0, app.target - app._total())
            rows.append(("납품수량", f"{app.target:,}장  (남은 수량 {left:,}장)"))
        for r, (k, v) in enumerate(rows):
            tk.Label(info, text=k, bg="#f4f6fa", fg="#666", font=("맑은 고딕", 9)).grid(
                row=r, column=0, sticky="w", padx=(0, 14), pady=1)
            tk.Label(info, text=v, bg="#f4f6fa", fg="#111", font=("맑은 고딕", 9, "bold")).grid(
                row=r, column=1, sticky="w", pady=1)
        if app._target_reached():
            tk.Label(frm, text="※ 이미 납품수량을 채웠습니다!", bg="#ffffff", fg="#d0002a",
                     font=("맑은 고딕", 10, "bold")).pack(anchor="w", pady=(8, 0))
        btns = tk.Frame(frm, bg="#ffffff")
        btns.pack(fill="x", pady=(12, 0))
        ttk.Button(btns, text="▶ 시작 (Enter / F9)", style="Start.TButton",
                   command=self.ok).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(btns, text="취소 (Esc)", style="Stop.TButton",
                   command=self.cancel).pack(side="left", expand=True, fill="x", padx=(4, 0))
        self.bind("<Return>", lambda e: self.ok())
        self.bind("<Escape>", lambda e: self.cancel())
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.update_idletasks()
        # 프로그램 창 가운데에 띄우기
        x = app.root.winfo_rootx() + (app.root.winfo_width() - self.winfo_width()) // 2
        y = app.root.winfo_rooty() + (app.root.winfo_height() - self.winfo_height()) // 3
        self.geometry(f"+{max(0, x)}+{max(0, y)}")
        try:
            self.bell()
        except tk.TclError:
            pass
        self.grab_set()
        self.focus_force()

    def ok(self):
        self.result = True
        self.destroy()

    def cancel(self):
        self.result = False
        self.destroy()


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        scale = max(1.0, self.root.winfo_fpixels("1i") / 96.0)
        w = min(int(560 * scale), self.root.winfo_screenwidth() - 40)
        h = min(int(620 * scale), self.root.winfo_screenheight() - 80)
        self.root.geometry(f"{w}x{h}")
        self.root.minsize(min(int(520 * scale), w), min(int(520 * scale), h))

        self.events = queue.Queue()      # 다른 스레드 → 화면 업데이트
        self.stop_event = threading.Event()
        self.running = False
        self.recording = False
        self.dirty = False
        self.rec_last_time = None
        self.mouse_listener = None
        self.sending_keys = False
        self.pause_event = threading.Event()
        self.settings = load_settings()
        self.count = int(self.settings.get("count", 0))
        self.extra = int(self.settings.get("extra", 0))
        self.target = int(self.settings.get("target", 0))  # 납품수량 (0 = 안 정함)
        self._confirm_dlg = None   # 총 장수 직접 조정분 (＋/－장)
        self.count_paused = False

        self.macro = {"name": "", "repeat": 1, "start_wait": 2.0, "per_plate": 1, "steps": []}

        self._build_ui()
        self._start_hotkeys()
        self._refresh_macro_list()

        last = self.settings.get("last_macro")
        if last and last in list_macros():
            self._open_macro(last)
        elif list_macros():
            self._open_macro(list_macros()[0])
        else:
            self._new_macro(ask=False)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.after(50, self._poll_events)

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("vista" if sys.platform == "win32" else "clam")
        except tk.TclError:
            pass
        style.configure("Start.TButton", font=("맑은 고딕", 10, "bold"), padding=(4, 3))
        style.configure("Stop.TButton", font=("맑은 고딕", 10, "bold"), padding=(4, 3))
        style.configure("Side.TButton", font=("맑은 고딕", 9), padding=(2, 1))
        style.configure("Treeview", rowheight=20, font=("맑은 고딕", 9))
        style.configure("Treeview.Heading", font=("맑은 고딕", 9, "bold"))

        # 맨 위: 회사 로고 + 프로그램 이름
        self._build_header()

        # 상단: 작업(매크로) 선택
        # 가운데: 위쪽 작업 줄 + 단계 목록 + 오른쪽 버튼 (같은 칸에 맞춰 줄 맞춤)
        # 아래쪽 영역을 먼저 배치해야 창이 작아도 잘리지 않음
        self._build_bottom()

        mid = ttk.Frame(self.root, padding=(8, 4, 8, 0))
        mid.pack(fill="both", expand=True)
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(1, weight=1)

        # 위쪽 작업 줄: 목록(스크롤바 포함)과 오른쪽 끝을 맞춤
        top = ttk.Frame(mid)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 4))
        ttk.Label(top, text="작업").pack(side="left")
        self.macro_var = tk.StringVar()
        self.macro_combo = ttk.Combobox(top, textvariable=self.macro_var,
                                        state="readonly", width=12)
        self.macro_combo.pack(side="left", padx=4)
        self.macro_combo.bind("<<ComboboxSelected>>",
                              lambda e: self._switch_macro(self.macro_var.get()))
        for i, (text, cmd) in enumerate((("새 작업", self._new_macro), ("저장", self._save),
                                         ("다른 이름", self._save_as), ("삭제", self._delete_macro))):
            ttk.Button(top, text=text, command=cmd, style="Side.TButton", width=7).pack(
                side="left", padx=(1, 0 if i == 3 else 1), fill="x", expand=True)
        self.topmost = tk.BooleanVar(value=self.settings.get("topmost", True))
        ttk.Checkbutton(mid, text="항상 위", variable=self.topmost,
                        command=self._apply_topmost).grid(row=0, column=2, sticky="e",
                                                          padx=(6, 0), pady=(0, 4))
        self._apply_topmost()

        cols = ("no", "type", "x", "y", "value", "delay", "memo")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", selectmode="extended")
        heads = {"no": ("#", 24), "type": ("동작", 58), "x": ("X", 38), "y": ("Y", 38),
                 "value": ("키/글자", 58), "delay": ("후대기", 50), "memo": ("메모", 70)}
        for c in cols:
            text, w = heads[c]
            self.tree.heading(c, text=text)
            self.tree.column(c, width=w, anchor="center" if c != "memo" else "w",
                             stretch=(c == "memo"))
        self.tree.tag_configure("end", background="#ffe1e1", foreground="#b00020")
        self.tree.tag_configure("current", background="#ffe58a")
        sb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.bind("<Double-1>", lambda e: self._edit_step())
        self.tree.bind("<Delete>", lambda e: self._delete_steps())

        side = ttk.Frame(mid, padding=(6, 0, 0, 0))
        self.tree.grid(row=1, column=0, sticky="nsew")
        sb.grid(row=1, column=1, sticky="ns")
        side.grid(row=1, column=2, sticky="ns")
        side_btns = (
            ("위치 추가 F8", self._add_current_position),
            ("END F12", self._toggle_end_here),
            ("직접 추가", self._add_step),
            ("대기 추가", lambda: self._insert_step(new_step("wait", delay=1.0, memo="기다리기"))),
            ("수정", self._edit_step),
            ("복사", self._duplicate_steps),
            ("▲ 위로", lambda: self._move_steps(-1)),
            ("▼ 아래로", lambda: self._move_steps(1)),
            ("삭제", self._delete_steps),
            ("위치 확인", self._show_position),
        )
        for r, (text, cmd) in enumerate(side_btns):
            ttk.Button(side, text=text, command=cmd, style="Side.TButton", width=11).grid(
                row=r, column=0, sticky="ew", pady=1)
        ttk.Separator(side).grid(row=len(side_btns), column=0, sticky="ew", pady=3)
        self.rec_btn = ttk.Button(side, text="● 녹화 F4", command=self._toggle_record,
                                  style="Side.TButton", width=11)
        self.rec_btn.grid(row=len(side_btns) + 1, column=0, sticky="ew")


    def _build_header(self):
        BG = "#ffffff"
        head = tk.Frame(self.root, bg=BG, padx=8, pady=3)
        head.pack(fill="x")
        tk.Frame(self.root, height=2, bg="#1a4fa0").pack(fill="x")
        self.logo_img = None
        scale = max(1.0, self.root.winfo_fpixels("1i") / 96.0)
        target = int(20 * scale)                  # 로고 높이 (화면 배율에 맞춤)
        path, custom = find_logo(target)
        if path:
            try:
                img = tk.PhotoImage(file=path)
                if custom:                        # 직접 넣은 logo.png 가 크면 줄이기
                    factor = max(1, -(-img.height() // int(56 * scale)))
                    if factor > 1:
                        img = img.subsample(factor, factor)
                self.logo_img = img
                tk.Label(head, image=img, bg=BG).pack(side="left", padx=(0, 10))
                tk.Frame(head, width=2, bg="#cccccc").pack(side="left", fill="y",
                                                           padx=(0, 10), pady=3)
            except tk.TclError:
                self.logo_img = None
        icon = find_icon()
        if icon:
            try:
                self.icon_img = tk.PhotoImage(file=icon)
                self.root.iconphoto(True, self.icon_img)   # 제목줄/작업표시줄 아이콘
            except tk.TclError:
                pass
        if self.logo_img is None:
            tk.Label(head, text=COMPANY, bg=BG, fg="#1a4fa0",
                     font=("맑은 고딕", 13, "bold")).pack(side="left", padx=(0, 10))
        tk.Label(head, text="UV 인쇄 클릭 자동화", bg=BG, fg="#222",
                 font=("맑은 고딕", 12, "bold")).pack(side="left")
        credit = tk.Label(head, text=f"[{CREDIT}]", bg=BG, fg="#777", cursor="hand2",
                          font=("맑은 고딕", 8, "bold"))
        credit.pack(side="left", padx=(6, 0), pady=(3, 0))
        credit.bind("<Button-1>", lambda e: self._show_changelog())
        credit.bind("<Enter>", lambda e: credit.config(fg="#1a4fa0"))
        credit.bind("<Leave>", lambda e: credit.config(fg="#777"))

    def _show_changelog(self):
        """업그레이드 내역 창"""
        win = tk.Toplevel(self.root)
        win.title(f"업그레이드 내역 — {VERSION}")
        win.transient(self.root)
        win.resizable(False, True)
        frm = ttk.Frame(win, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=f"UV 인쇄 클릭 자동화  {CREDIT}",
                  font=("맑은 고딕", 10, "bold")).pack(anchor="w", pady=(0, 6))
        box = ttk.Frame(frm)
        box.pack(fill="both", expand=True)
        txt = tk.Text(box, width=64, height=16, font=("맑은 고딕", 9), relief="flat",
                      bg="#fafafa", padx=8, pady=6, wrap="word", spacing1=2, spacing3=2)
        sb = ttk.Scrollbar(box, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        txt.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")
        txt.tag_configure("ver", foreground="#1a4fa0", font=("맑은 고딕", 9, "bold"))
        txt.tag_configure("now", foreground="#b00020", font=("맑은 고딕", 9, "bold"))
        txt.tag_configure("date", foreground="#888")
        for i, (ver, date, note) in enumerate(CHANGELOG):
            txt.insert("end", f"{ver:<6}", "now" if i == 0 else "ver")
            txt.insert("end", f" {date}  ", "date")
            txt.insert("end", note + ("  ← 지금 버전" if i == 0 else "") + "\n")
        txt.configure(state="disabled")
        ttk.Button(frm, text="닫기", command=win.destroy).pack(pady=(6, 0))
        win.bind("<Escape>", lambda e: win.destroy())
        win.attributes("-topmost", bool(self.topmost.get()))
        win.focus_set()

    def _build_bottom(self):
        style = ttk.Style()
        style.configure("Pause.TButton", font=("맑은 고딕", 10, "bold"), padding=(4, 3))
        style.configure("Cnt.TButton", font=("맑은 고딕", 9, "bold"), padding=(2, 2))

        # 맨 아래 상태줄
        self.status = tk.StringVar(value="준비")
        self.status_bar = ttk.Label(self.root, textvariable=self.status, relief="sunken",
                                    anchor="w", padding=(6, 1))
        self.status_bar.pack(fill="x", side="bottom")

        # 생산 카운터
        self.tools = ttk.Frame(self.root, padding=(8, 0, 8, 4))
        self.tools.pack(fill="x", side="bottom")
        self._build_counter(self.tools)

        # 실행 버튼 줄
        run = ttk.Frame(self.root, padding=(8, 3, 8, 4))
        run.pack(fill="x", side="bottom")
        self.start_btn = ttk.Button(run, text="▶ 시작 (F9)", style="Start.TButton",
                                    command=self.start)
        self.pause_btn = ttk.Button(run, text="일시정지 (F11)", style="Pause.TButton",
                                    command=self.toggle_pause)
        self.stop_btn = ttk.Button(run, text="■ 정지 (F10)", style="Stop.TButton",
                                   command=self.stop)
        for i, b in enumerate((self.start_btn, self.pause_btn, self.stop_btn)):
            b.grid(row=0, column=i, sticky="ew", padx=4)
            run.columnconfigure(i, weight=1, uniform="run")
        self.pause_btn.state(["disabled"])

        # 실행 옵션 줄
        opt = ttk.Frame(self.root, padding=(8, 4, 8, 0))
        opt.pack(fill="x", side="bottom")
        self.show_tools = tk.BooleanVar(value=self.settings.get("show_tools", True))
        ttk.Checkbutton(opt, text="카운터", variable=self.show_tools,
                        command=self._apply_show_tools).pack(side="right")
        ttk.Label(opt, text="반복").pack(side="left")
        self.repeat_var = tk.StringVar(value="1")
        ttk.Spinbox(opt, from_=1, to=9999, textvariable=self.repeat_var, width=5,
                    command=self._mark_dirty).pack(side="left", padx=(3, 10))
        ttk.Label(opt, text="시작대기(초)").pack(side="left")
        self.start_wait_var = tk.StringVar(value="2")
        ttk.Spinbox(opt, from_=0, to=30, increment=1, textvariable=self.start_wait_var,
                    width=3, command=self._mark_dirty).pack(side="left", padx=(3, 10))
        self.speed_var = tk.StringVar(value=self.settings.get("speed", "보통"))
        ttk.Label(opt, text="이동").pack(side="left")
        ttk.Combobox(opt, textvariable=self.speed_var, state="readonly", width=5,
                     values=["빠름", "보통", "느림"]).pack(side="left", padx=3)
        self._apply_show_tools()

    def _apply_show_tools(self):
        if self.show_tools.get():
            # 상태줄 바로 위에 다시 붙이기
            self.tools.pack(fill="x", side="bottom", after=self.status_bar)
        else:
            self.tools.pack_forget()
        self.settings["show_tools"] = bool(self.show_tools.get())

    # ------------------------------------------------------------ 카운터
    def _build_counter(self, parent):
        box = ttk.LabelFrame(parent, text=" 생산 카운터 ", padding=(6, 2, 6, 4))
        box.pack(fill="both", expand=True)

        # 검은 화면: 번 수 / 총 수량
        BG, FG, FG2 = "#10261c", "#4dff9a", "#b9f5d0"
        panel = tk.Frame(box, bg=BG, padx=10, pady=2)
        panel.pack(fill="x")
        self.count_widgets = []
        for col, (title, attr) in enumerate((("완료 횟수", "plates_var"),
                                             ("총 소재 수량", "total_var"))):
            cell = tk.Frame(panel, bg=BG)
            cell.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 20, 0))
            panel.columnconfigure(col, weight=1, uniform="cnt")
            tlbl = tk.Label(cell, text=title, bg=BG, fg=FG2, font=("맑은 고딕", 8), justify="left")
            tlbl.pack(side="left", anchor="n", pady=(4, 0))
            if attr == "total_var":
                self.total_title = tlbl
            var = tk.StringVar()
            setattr(self, attr, var)
            lbl = tk.Label(cell, textvariable=var, bg=BG, fg=FG, anchor="e",
                           font=("맑은 고딕", 20, "bold"))
            lbl.pack(side="right", fill="x", expand=True)
            self.count_widgets.append(lbl)

        # 한 번 소재 수량 + 세는 방법 안내
        row1 = ttk.Frame(box)
        row1.pack(fill="x", pady=(3, 2))
        ttk.Label(row1, text="한 번에 소재", font=("맑은 고딕", 9, "bold")).pack(side="left")
        self.per_plate_var = tk.StringVar(value="1")
        ttk.Spinbox(row1, from_=1, to=9999, textvariable=self.per_plate_var, width=6,
                    font=("맑은 고딕", 10, "bold"), justify="center",
                    command=self._per_plate_changed).pack(side="left", padx=6)
        ttk.Label(row1, text="장", font=("맑은 고딕", 9, "bold")).pack(side="left")
        self.per_plate_var.trace_add("write", lambda *a: self._per_plate_changed())
        ttk.Label(row1, text="납품수량", font=("맑은 고딕", 9, "bold")).pack(side="left", padx=(14, 0))
        self.target_var = tk.StringVar(value=str(self.target) if self.target else "")
        ttk.Spinbox(row1, from_=0, to=999999, textvariable=self.target_var, width=7,
                    font=("맑은 고딕", 10, "bold"), justify="center",
                    command=self._target_changed).pack(side="left", padx=6)
        ttk.Label(row1, text="장", font=("맑은 고딕", 9, "bold")).pack(side="left")
        self.target_var.trace_add("write", lambda *a: self._target_changed())
        self.count_state = ttk.Label(row1, text="", foreground="#1b7a3d", font=("맑은 고딕", 8))
        self.count_state.pack(side="right")

        # 버튼
        row2 = ttk.Frame(box)
        row2.pack(fill="x")
        self.count_pause_btn = ttk.Button(row2, text="일시정지", style="Cnt.TButton",
                                          command=self._toggle_count_pause)
        btns = (ttk.Button(row2, text="＋1번", style="Cnt.TButton",
                           command=lambda: self._add_count(1, manual=True)),
                ttk.Button(row2, text="－1번", style="Cnt.TButton",
                           command=lambda: self._add_count(-1, manual=True)),
                ttk.Button(row2, text="＋1장", style="Cnt.TButton",
                           command=lambda: self._add_extra(1)),
                ttk.Button(row2, text="－1장", style="Cnt.TButton",
                           command=lambda: self._add_extra(-1)),
                self.count_pause_btn,
                ttk.Button(row2, text="↺ 리셋", style="Cnt.TButton", command=self._reset_count))
        for col, b in enumerate(btns):
            b.grid(row=0, column=col, sticky="ew", padx=2)
            row2.columnconfigure(col, weight=1, uniform="cntb")
        self._update_count_display()

    def _set_per_plate(self, n):
        self._loading = True
        try:
            self.per_plate_var.set(str(n))
        finally:
            self._loading = False
        self._update_count_display()

    def _per_plate(self):
        try:
            return max(1, int(float(self.per_plate_var.get())))
        except (ValueError, tk.TclError):
            return 1

    def _per_plate_changed(self):
        if getattr(self, "_loading", False):
            return
        n = self._per_plate()
        if self.macro.get("per_plate") != n:
            self.macro["per_plate"] = n
            self._mark_dirty()
        self._update_count_display()

    def _target_changed(self):
        try:
            t = max(0, int(float(self.target_var.get() or 0)))
        except (ValueError, tk.TclError):
            t = 0
        if t != self.target:
            self.target = t
            self.settings["target"] = t
            save_settings(self.settings)
        self._update_count_display()

    def _near_target(self):
        """납품수량의 95% 이상 채웠는지 (시작 확인 창을 띄울 때)"""
        return self.target > 0 and self._total() >= self.target * 0.95

    def _target_reached(self):
        return self.target > 0 and self._total() >= self.target

    def _update_count_display(self):
        self.plates_var.set(f"{self.count:,} 번")
        self.total_var.set(f"{self._total():,} 장")
        self.total_title.config(text="총 소재 수량" + (f"\n납품 {self.target:,}장" if self.target else ""))
        self._apply_count_colors()
        self._update_count_rule()

    def _apply_count_colors(self):
        base = "#ffc94d" if self.count_paused else "#4dff9a"
        self.count_widgets[0].config(fg=base)
        # 납품수량을 채우면 총 소재 수량을 빨간색으로
        self.count_widgets[1].config(fg="#ff4d4d" if self._target_reached() else base)

    def _total(self):
        return max(0, self.count * self._per_plate() + self.extra)

    def _add_extra(self, n):
        """총 소재 수량만 ＋/－ (불량·추가분 등)"""
        base = self.count * self._per_plate()
        self.extra = max(-base, self.extra + n)      # 총 장수가 0 밑으로 안 내려가게
        self.settings["extra"] = self.extra
        save_settings(self.settings)
        self._update_count_display()

    def _update_count_rule(self):
        if self.count_paused:
            text, color = "일시정지 — 자동으로 세지 않음", "#b36b00"
        elif self._target_reached():
            text, color = "■ 납품수량 완료!", "#d0002a"
        elif any(is_end(s) for s in self.macro["steps"]):
            text, color = "▶ END 단계 실행 시 +1번", "#1b7a3d"
        else:
            text, color = "※ END 없음 — 세지 않음 (F12 로 END 표시)", "#b00020"
        self.count_state.config(text=text, foreground=color)

    def _add_count(self, n, manual=False):
        if self.count_paused and not manual:
            return
        self.count = max(0, self.count + n)
        self.settings["count"] = self.count
        save_settings(self.settings)
        self._update_count_display()

    def _toggle_count_pause(self):
        self.count_paused = not self.count_paused
        self.count_pause_btn.config(text="▶ 다시 세기" if self.count_paused else "일시정지")
        self._apply_count_colors()
        self._update_count_rule()

    def _reset_count(self):
        if (self.count or self.extra) and not messagebox.askyesno(
                APP_TITLE, f"카운터 {self.count}번 ({self._total()}장)을 0으로 되돌릴까요?"):
            return
        self.count = 0
        self.extra = 0
        self.settings["count"] = 0
        self.settings["extra"] = 0
        save_settings(self.settings)
        self._update_count_display()

    def _apply_topmost(self):
        self.root.attributes("-topmost", bool(self.topmost.get()))

    # ------------------------------------------------------------ 목록 표시
    def _refresh_tree(self, select=None):
        self.tree.delete(*self.tree.get_children())
        for i, s in enumerate(self.macro["steps"]):
            pos = s["type"] in POSITION_TYPES
            self.tree.insert("", "end", iid=str(i), values=(
                i + 1, STEP_TYPES.get(s["type"], s["type"]),
                s["x"] if pos else "", s["y"] if pos else "",
                s["value"] if s["type"] in ("key", "text") else "",
                f'{s["delay"]:g}', s["memo"]), tags=self._row_tags(i))
        if select:
            ids = [str(i) for i in select if 0 <= i < len(self.macro["steps"])]
            if ids:
                self.tree.selection_set(ids)
                self.tree.see(ids[-1])
        self._update_title()
        if hasattr(self, "count_state"):
            self._update_count_rule()

    def _row_tags(self, i):
        steps = self.macro["steps"]
        return ("end",) if 0 <= i < len(steps) and is_end(steps[i]) else ()

    def _update_title(self):
        name = self.macro["name"] or "(저장 안 됨)"
        self.root.title(f'{APP_TITLE} - {name}{" *" if self.dirty else ""}')

    def _mark_dirty(self, *_):
        self.dirty = True
        self._update_title()

    def _selected(self):
        return sorted(int(i) for i in self.tree.selection())

    def _insert_step(self, step):
        sel = self._selected()
        idx = sel[-1] + 1 if sel else len(self.macro["steps"])
        self.macro["steps"].insert(idx, step)
        self._mark_dirty()
        self._refresh_tree(select=[idx])

    # ------------------------------------------------------------ 단계 편집
    def _add_current_position(self):
        """F8: 지금 마우스 위치를 클릭 단계로 추가"""
        if self.running or self.recording:
            return
        x, y = pyautogui.position()
        self._insert_step(new_step("click", x, y))
        self.status.set(f"클릭 위치 추가: ({x}, {y})  — 메모를 적어두면 나중에 알아보기 쉽습니다.")

    def _toggle_end_here(self):
        """F12: 그 위치에 END 표시 / 같은 위치에서 다시 누르면 END 없애기"""
        if self.running:
            return
        steps = self.macro["steps"]
        if self.recording:
            # 녹화 중에는 방금 녹화한 클릭의 END 를 켜고 끄기
            if steps:
                last = steps[-1]
                last["memo"] = "" if is_end(last) else "END"
                self._mark_dirty()
                self._refresh_tree(select=[len(steps) - 1])
                self.status.set("녹화 중… 방금 클릭을 END 로 표시했습니다. 끝나면 F4" if is_end(last)
                                else "녹화 중… 방금 클릭의 END 를 없앴습니다. 끝나면 F4")
            return
        if not steps:
            self.status.set("단계가 없습니다. 먼저 F8 로 클릭 위치를 추가하세요.")
            return
        # 어느 단계에 END 를 붙일지: ① 마우스 근처 단계 ② 목록에서 선택한 단계 ③ 마지막 단계
        x, y = pyautogui.position()
        near = [i for i, st in enumerate(steps)
                if st["type"] in POSITION_TYPES and abs(st["x"] - x) <= 20 and abs(st["y"] - y) <= 20]
        sel = self._selected()
        if near:
            pick = [i for i in sel if i in near]
            i = pick[0] if pick else near[-1]
        elif sel:
            i = sel[0]
        else:
            i = len(steps) - 1
        st = steps[i]
        if is_end(st):
            st["memo"] = ""
            self.status.set(f"{i + 1}번 단계의 END 를 없앴습니다.")
        else:
            st["memo"] = "END"
            self.status.set(f"{i + 1}번 단계를 END 로 표시 — 실행되면 카운터 +1번 (F12 다시 누르면 해제)")
        self._mark_dirty()
        self._refresh_tree(select=[i])

    def _add_step(self):
        x, y = pyautogui.position()
        dlg = StepDialog(self.root, new_step("click", x, y), "단계 추가")
        self.root.wait_window(dlg)
        if dlg.result:
            self._insert_step(dlg.result)

    def _edit_step(self):
        sel = self._selected()
        if not sel:
            return
        i = sel[0]
        dlg = StepDialog(self.root, self.macro["steps"][i], f"{i + 1}번 단계 수정")
        self.root.wait_window(dlg)
        if dlg.result:
            self.macro["steps"][i] = dlg.result
            self._mark_dirty()
            self._refresh_tree(select=[i])

    def _duplicate_steps(self):
        sel = self._selected()
        if not sel:
            return
        copies = [dict(self.macro["steps"][i]) for i in sel]
        at = sel[-1] + 1
        self.macro["steps"][at:at] = copies
        self._mark_dirty()
        self._refresh_tree(select=list(range(at, at + len(copies))))

    def _delete_steps(self):
        sel = self._selected()
        if not sel:
            return
        for i in reversed(sel):
            del self.macro["steps"][i]
        self._mark_dirty()
        self._refresh_tree(select=[min(sel[0], len(self.macro["steps"]) - 1)])

    def _move_steps(self, d):
        sel = self._selected()
        steps = self.macro["steps"]
        if not sel or (d < 0 and sel[0] == 0) or (d > 0 and sel[-1] == len(steps) - 1):
            return
        order = sel if d < 0 else list(reversed(sel))
        for i in order:
            steps[i], steps[i + d] = steps[i + d], steps[i]
        self._mark_dirty()
        self._refresh_tree(select=[i + d for i in sel])

    def _show_position(self):
        """선택한 단계 위치로 마우스만 옮겨서 맞는지 확인 (클릭 안 함)"""
        sel = self._selected()
        if not sel:
            return
        s = self.macro["steps"][sel[0]]
        if s["type"] not in POSITION_TYPES:
            return
        pyautogui.moveTo(s["x"], s["y"], duration=0.3)
        self.status.set(f'{sel[0] + 1}번 위치로 마우스를 옮겼습니다 (클릭은 안 함).')

    # ------------------------------------------------------------ 작업 파일
    def _refresh_macro_list(self):
        self.macro_combo["values"] = list_macros()
        self.macro_var.set(self.macro["name"])

    def _confirm_discard(self):
        if not self.dirty:
            return True
        ans = messagebox.askyesnocancel(APP_TITLE, "바뀐 내용을 저장할까요?")
        if ans is None:
            return False
        if ans:
            return self._save()
        return True

    def _open_macro(self, name):
        try:
            self.macro = load_macro(name)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"불러오기 실패: {e}")
            return
        self.repeat_var.set(str(self.macro["repeat"]))
        self.start_wait_var.set(f'{self.macro["start_wait"]:g}')
        self._set_per_plate(self.macro["per_plate"])
        self.dirty = False
        self._refresh_macro_list()
        self._refresh_tree()
        self.settings["last_macro"] = name
        self.status.set(f'"{name}" 불러옴 — 단계 {len(self.macro["steps"])}개')

    def _switch_macro(self, name):
        if name == self.macro["name"]:
            return
        if not self._confirm_discard():
            self.macro_var.set(self.macro["name"])
            return
        self._open_macro(name)

    def _new_macro(self, ask=True):
        if ask and not self._confirm_discard():
            return
        name = ""
        if ask:
            name = simpledialog.askstring(APP_TITLE, "새 작업 이름 (예: 머그컵 인쇄, 폰케이스 A)",
                                          parent=self.root)
            if name is None:
                return
            name = safe_filename(name)
        self.macro = {"name": name, "repeat": 1, "start_wait": 2.0, "per_plate": 1, "steps": []}
        self.repeat_var.set("1")
        self.start_wait_var.set("2")
        self._set_per_plate(1)
        self.dirty = bool(name)
        self._refresh_macro_list()
        self._refresh_tree()
        self.status.set("인쇄 프로그램에서 누를 곳에 마우스를 올리고 F8을 누르세요. 또는 F4 로 클릭 녹화.")

    def _collect_options(self):
        self.macro["per_plate"] = self._per_plate()
        try:
            self.macro["repeat"] = max(1, int(float(self.repeat_var.get())))
        except ValueError:
            self.macro["repeat"] = 1
        try:
            self.macro["start_wait"] = max(0.0, float(self.start_wait_var.get()))
        except ValueError:
            self.macro["start_wait"] = 2.0

    def _save(self):
        if not self.macro["name"]:
            return self._save_as()
        self._collect_options()
        try:
            save_macro(self.macro)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"저장 실패: {e}")
            return False
        self.dirty = False
        self._refresh_macro_list()
        self._update_title()
        self.settings["last_macro"] = self.macro["name"]
        self.status.set(f'"{self.macro["name"]}" 저장됨')
        return True

    def _save_as(self):
        name = simpledialog.askstring(APP_TITLE, "저장할 작업 이름", parent=self.root,
                                      initialvalue=self.macro["name"])
        if not name:
            return False
        name = safe_filename(name)
        if name in list_macros() and name != self.macro["name"]:
            if not messagebox.askyesno(APP_TITLE, f'"{name}"이(가) 이미 있습니다. 덮어쓸까요?'):
                return False
        self.macro["name"] = name
        return self._save()

    def _delete_macro(self):
        name = self.macro["name"]
        if not name or name not in list_macros():
            return
        if not messagebox.askyesno(APP_TITLE, f'"{name}" 작업을 삭제할까요?'):
            return
        os.remove(os.path.join(MACRO_DIR, name + ".json"))
        rest = list_macros()
        self.dirty = False
        if rest:
            self._open_macro(rest[0])
        else:
            self._new_macro(ask=False)

    # ------------------------------------------------------------ 단축키
    def _start_hotkeys(self):
        def on_press(key):
            if self.sending_keys:   # 매크로가 직접 누른 키는 무시
                return
            if key == keyboard.Key.f8:
                self.events.put(("hotkey", "add"))
            elif key == keyboard.Key.f12:
                self.events.put(("hotkey", "add_end"))
            elif key == keyboard.Key.f9:
                self.events.put(("hotkey", "start"))
            elif key == keyboard.Key.f4:
                self.events.put(("hotkey", "record"))
            elif key == keyboard.Key.f10:
                self.events.put(("hotkey", "stop"))
            elif key in (keyboard.Key.f11, keyboard.Key.pause):
                self.events.put(("hotkey", "pause"))
            elif key == keyboard.Key.esc and self.running:
                self.stop_event.set()
                self.events.put(("hotkey", "stop"))

        self.kb_listener = keyboard.Listener(on_press=on_press)
        self.kb_listener.daemon = True
        self.kb_listener.start()

    def _poll_events(self):
        try:
            while True:
                ev, arg = self.events.get_nowait()
                if ev == "hotkey":
                    if arg == "add":
                        self._add_current_position()
                    elif arg == "record":
                        self._toggle_record()
                    elif arg == "add_end":
                        self._toggle_end_here()
                    elif arg == "start":
                        self.start()
                    elif arg == "pause":
                        self.toggle_pause()
                    elif arg == "stop":
                        if self.recording:
                            self._toggle_record()
                        else:
                            self.stop()
                elif ev == "status":
                    self.status.set(arg)
                elif ev == "highlight":
                    for iid in self.tree.tag_has("current"):
                        self.tree.item(iid, tags=self._row_tags(int(iid)))
                    if arg is not None and self.tree.exists(str(arg)):
                        self.tree.item(str(arg), tags=("current",))
                        self.tree.see(str(arg))
                elif ev == "count":
                    self._add_count(arg)
                elif ev == "done":
                    self._run_finished(arg)
                elif ev == "rec_click":
                    self._record_click(*arg)
        except queue.Empty:
            pass
        self.root.after(30, self._poll_events)

    # ------------------------------------------------------------ 녹화
    def _toggle_record(self):
        if self.running:
            return
        if not self.recording:
            self.recording = True
            self.rec_last_time = None
            self.rec_btn.config(text="■ 녹화 끝 F4")
            self.status.set("녹화 중… 평소처럼 클릭하세요 (목록 끝에 이어서 추가). 끝나면 F4.")
            self.root.iconify()   # 창을 내려서 클릭에 방해되지 않게

            def on_click(x, y, button, pressed):
                if pressed and self.recording:
                    self.events.put(("rec_click", (int(x), int(y), button.name, time.time())))

            self.mouse_listener = mouse.Listener(on_click=on_click)
            self.mouse_listener.daemon = True
            self.mouse_listener.start()
        else:
            self.recording = False
            if self.mouse_listener:
                self.mouse_listener.stop()
                self.mouse_listener = None
            self.rec_btn.config(text="● 녹화 F4")
            self.root.deiconify()
            self.root.lift()
            self.status.set("녹화 끝. 대기시간은 실제 간격대로 들어갔으니 필요하면 수정하세요.")

    def _record_click(self, x, y, button, t):
        if not self.recording:
            return
        steps = self.macro["steps"]
        kind = "right" if button == "right" else "click"
        if self.rec_last_time is not None and steps:
            gap = t - self.rec_last_time
            prev = steps[-1]
            # 같은 자리를 빠르게 두 번 → 더블클릭으로 합침
            if (kind == "click" and prev["type"] == "click" and gap < 0.4
                    and abs(prev["x"] - x) <= 4 and abs(prev["y"] - y) <= 4):
                prev["type"] = "double"
                self.rec_last_time = t
                self._mark_dirty()
                self._refresh_tree(select=[len(steps) - 1])
                return
            prev["delay"] = round(max(0.2, gap), 1)
        steps.append(new_step(kind, x, y))
        self.rec_last_time = t
        self._mark_dirty()
        self._refresh_tree(select=[len(steps) - 1])
        self.status.set(f"녹화 중… {len(steps)}번째 클릭 ({x}, {y})  — 끝나면 F4")

    # ------------------------------------------------------------ 실행
    def start(self):
        if self.running or self.recording:
            return
        if self._confirm_dlg is not None:      # 확인 창이 떠 있을 때 F9 한 번 더 → 시작
            self._confirm_dlg.ok()
            return
        if not self.macro["steps"]:
            messagebox.showinfo(APP_TITLE, "등록된 단계가 없습니다.")
            return
        self._collect_options()
        if self._near_target():
            # 납품수량의 95% 이상 채웠을 때만 확인 창
            dlg = StartConfirm(self)
            self._confirm_dlg = dlg
            self.root.wait_window(dlg)
            self._confirm_dlg = None
            if not dlg.result:
                self.status.set("시작을 취소했습니다.")
                return
        self._begin_run()

    def _begin_run(self):
        self.running = True
        self.stop_event.clear()
        self.pause_event.clear()
        self.start_btn.state(["disabled"])
        self.pause_btn.state(["!disabled"])
        self.pause_btn.config(text="일시정지 (F11)")
        move = {"빠름": 0.05, "보통": 0.2, "느림": 0.5}.get(self.speed_var.get(), 0.2)
        self.settings["speed"] = self.speed_var.get()
        steps = [dict(s) for s in self.macro["steps"]]
        threading.Thread(target=self._run, daemon=True,
                         args=(steps, self.macro["repeat"], self.macro["start_wait"], move)
                         ).start()

    def stop(self):
        if self.running:
            self.stop_event.set()
            self.pause_event.clear()
            self.status.set("정지하는 중…")

    def toggle_pause(self):
        if not self.running:
            return
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_btn.config(text="일시정지 (F11)")
            self.status.set("다시 시작합니다…")
        else:
            self.pause_event.set()
            self.pause_btn.config(text="▶ 계속 (F11)")
            self.status.set("일시정지 중 — [▶ 계속] 또는 F11 을 누르면 이어서 진행합니다.")

    def _sleep(self, sec):
        """정지/일시정지를 확인하면서 기다리기 (일시정지 동안은 시간이 멈춤)"""
        end = time.monotonic() + sec
        while True:
            if self.stop_event.is_set():
                raise InterruptedError
            if self.pause_event.is_set():
                t0 = time.monotonic()
                while self.pause_event.is_set() and not self.stop_event.is_set():
                    self.stop_event.wait(0.1)
                end += time.monotonic() - t0
                continue
            remain = end - time.monotonic()
            if remain <= 0:
                return
            self.stop_event.wait(min(remain, 0.1))

    def _run(self, steps, repeat, start_wait, move):
        put = self.events.put
        reason = "완료"
        try:
            left = start_wait
            while left > 0:
                put(("status", f"{left:.0f}초 뒤 시작합니다… (정지: F10 / ESC)"))
                self._sleep(min(1.0, left))
                left -= 1.0
            for r in range(repeat):
                for i, s in enumerate(steps):
                    self._sleep(0)          # 일시정지/정지 확인
                    put(("highlight", i))
                    put(("status", f"[{r + 1}/{repeat}회] {i + 1}/{len(steps)}단계: "
                                   f'{STEP_TYPES.get(s["type"])} {s["memo"]}'))
                    self._do_step(s, move)
                    if is_end(s):
                        put(("count", 1))   # 메모가 END → 한 번 끝, 카운터 +1
                    if s["delay"] > 0:
                        self._sleep(s["delay"])
        except InterruptedError:
            reason = "정지됨"
        except pyautogui.FailSafeException:
            reason = "비상정지 (마우스가 화면 구석으로 이동)"
        except Exception as e:
            reason = f"오류: {e}"
        put(("highlight", None))
        put(("done", reason))

    def _do_step(self, s, move):
        kind = s["type"]
        if kind in POSITION_TYPES:
            pyautogui.moveTo(s["x"], s["y"], duration=move)
            if kind == "click":
                pyautogui.click()
            elif kind == "double":
                pyautogui.doubleClick()
            elif kind == "right":
                pyautogui.rightClick()
        elif kind == "key":
            self.sending_keys = True
            try:
                self._press_keys(s["value"])
            finally:
                time.sleep(0.05)
                self.sending_keys = False
        elif kind == "text":
            pyperclip.copy(s["value"])
            time.sleep(0.05)
            pyautogui.hotkey("ctrl", "v")
        # "wait" 는 delay 만 사용

    @staticmethod
    def _press_keys(value):
        keys = [k.strip().lower() for k in value.split("+") if k.strip()]
        alias = {"esc": "escape", "control": "ctrl", "엔터": "enter", "del": "delete"}
        keys = [alias.get(k, k) for k in keys]
        if len(keys) == 1:
            pyautogui.press(keys[0])
        elif keys:
            pyautogui.hotkey(*keys)

    def _run_finished(self, reason):
        self.running = False
        self.pause_event.clear()
        self.start_btn.state(["!disabled"])
        self.pause_btn.state(["disabled"])
        self.pause_btn.config(text="일시정지 (F11)")
        self.status.set(f"{reason}  ({time.strftime('%H:%M:%S')})")

    def _on_close(self):
        if self.running:
            self.stop_event.set()
        if not self._confirm_discard():
            return
        self.settings["topmost"] = bool(self.topmost.get())
        self.settings["speed"] = self.speed_var.get()
        if self.macro["name"]:
            self.settings["last_macro"] = self.macro["name"]
        save_settings(self.settings)
        self.root.destroy()


def main():
    root = tk.Tk()
    MacroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
