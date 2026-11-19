# -*- coding: utf-8 -*-
"""
UV 인쇄기 클릭 자동화 (클릭 매크로)

- 단계(클릭 위치, 대기, 키 입력, 글자 입력)를 순서대로 등록해 두고
  [시작]을 누르면 그대로 실행합니다.
- 작업별로 여러 개를 저장해 두고 골라서 쓸 수 있습니다.
- 클릭 녹화: 직접 한 번 클릭해 보면 위치와 간격이 단계로 기록됩니다.

단축키 (다른 프로그램이 앞에 있어도 동작)
  F8  : 지금 마우스가 있는 위치를 '클릭' 단계로 추가
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

APP_TITLE = "UV 인쇄 클릭 자동화"
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_DIR = os.path.join(BASE_DIR, "macros")
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


def new_step(kind="click", x=0, y=0, value="", delay=0.5, memo=""):
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
            "steps": steps}


def save_macro(macro):
    os.makedirs(MACRO_DIR, exist_ok=True)
    path = os.path.join(MACRO_DIR, safe_filename(macro["name"]) + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"repeat": macro["repeat"], "start_wait": macro["start_wait"],
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

        btns = ttk.Frame(frm)
        btns.grid(row=7, column=0, columnspan=3, pady=(10, 0))
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


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x580")
        self.root.minsize(820, 480)

        self.events = queue.Queue()      # 다른 스레드 → 화면 업데이트
        self.stop_event = threading.Event()
        self.running = False
        self.recording = False
        self.dirty = False
        self.rec_last_time = None
        self.mouse_listener = None
        self.sending_keys = False
        self.settings = load_settings()

        self.macro = {"name": "", "repeat": 1, "start_wait": 2.0, "steps": []}

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
        style.configure("Start.TButton", font=("맑은 고딕", 12, "bold"), padding=8)
        style.configure("Stop.TButton", font=("맑은 고딕", 12, "bold"), padding=8)
        style.configure("Treeview", rowheight=24)

        # 상단: 작업(매크로) 선택
        top = ttk.Frame(self.root, padding=(10, 8))
        top.pack(fill="x")
        ttk.Label(top, text="작업 선택").pack(side="left")
        self.macro_var = tk.StringVar()
        self.macro_combo = ttk.Combobox(top, textvariable=self.macro_var,
                                        state="readonly", width=24)
        self.macro_combo.pack(side="left", padx=6)
        self.macro_combo.bind("<<ComboboxSelected>>",
                              lambda e: self._switch_macro(self.macro_var.get()))
        ttk.Button(top, text="새 작업", command=self._new_macro).pack(side="left", padx=2)
        ttk.Button(top, text="저장", command=self._save).pack(side="left", padx=2)
        ttk.Button(top, text="다른 이름으로", command=self._save_as).pack(side="left", padx=2)
        ttk.Button(top, text="삭제", command=self._delete_macro).pack(side="left", padx=2)
        self.topmost = tk.BooleanVar(value=self.settings.get("topmost", True))
        ttk.Checkbutton(top, text="항상 위", variable=self.topmost,
                        command=self._apply_topmost).pack(side="right")
        self._apply_topmost()

        # 가운데: 단계 목록
        mid = ttk.Frame(self.root, padding=(10, 0))
        mid.pack(fill="both", expand=True)
        cols = ("no", "type", "x", "y", "value", "delay", "memo")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", selectmode="extended")
        heads = {"no": ("#", 36), "type": ("동작", 90), "x": ("X", 60), "y": ("Y", 60),
                 "value": ("키/글자", 130), "delay": ("후 대기(초)", 80), "memo": ("메모", 200)}
        for c in cols:
            text, w = heads[c]
            self.tree.heading(c, text=text)
            self.tree.column(c, width=w, anchor="center" if c != "memo" else "w",
                             stretch=(c == "memo"))
        self.tree.tag_configure("current", background="#ffe58a")
        sb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.bind("<Double-1>", lambda e: self._edit_step())
        self.tree.bind("<Delete>", lambda e: self._delete_steps())

        side = ttk.Frame(mid, padding=(8, 0, 0, 0))
        side.pack(side="right", fill="y")
        sb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        for text, cmd in (
            ("위치 추가 (F8)", self._add_current_position),
            ("단계 직접 추가", self._add_step),
            ("대기 추가", lambda: self._insert_step(new_step("wait", delay=1.0, memo="기다리기"))),
            ("수정", self._edit_step),
            ("복사", self._duplicate_steps),
            ("삭제", self._delete_steps),
            ("▲ 위로", lambda: self._move_steps(-1)),
            ("▼ 아래로", lambda: self._move_steps(1)),
            ("위치 확인", self._show_position),
        ):
            ttk.Button(side, text=text, command=cmd).pack(pady=2, fill="x", ipadx=6)
        ttk.Separator(side).pack(fill="x", pady=6)
        self.rec_btn = ttk.Button(side, text="● 클릭 녹화", command=self._toggle_record)
        self.rec_btn.pack(pady=2, fill="x", ipadx=6)

        # 하단: 실행
        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill="x")
        ttk.Label(bottom, text="반복 횟수").pack(side="left")
        self.repeat_var = tk.StringVar(value="1")
        ttk.Spinbox(bottom, from_=1, to=9999, textvariable=self.repeat_var, width=6,
                    command=self._mark_dirty).pack(side="left", padx=(4, 12))
        ttk.Label(bottom, text="시작 전 대기(초)").pack(side="left")
        self.start_wait_var = tk.StringVar(value="2")
        ttk.Spinbox(bottom, from_=0, to=30, increment=1, textvariable=self.start_wait_var,
                    width=5, command=self._mark_dirty).pack(side="left", padx=(4, 12))
        self.speed_var = tk.StringVar(value=self.settings.get("speed", "보통"))
        ttk.Label(bottom, text="마우스 이동").pack(side="left")
        ttk.Combobox(bottom, textvariable=self.speed_var, state="readonly", width=6,
                     values=["빠름", "보통", "느림"]).pack(side="left", padx=4)

        self.stop_btn = ttk.Button(bottom, text="■ 정지 (F10)", style="Stop.TButton",
                                   command=self.stop)
        self.stop_btn.pack(side="right", padx=4)
        self.start_btn = ttk.Button(bottom, text="▶ 시작 (F9)", style="Start.TButton",
                                    command=self.start)
        self.start_btn.pack(side="right", padx=4)

        self.status = tk.StringVar(value="준비")
        bar = ttk.Label(self.root, textvariable=self.status, relief="sunken",
                        anchor="w", padding=(8, 3))
        bar.pack(fill="x", side="bottom")

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
                f'{s["delay"]:g}', s["memo"]))
        if select:
            ids = [str(i) for i in select if 0 <= i < len(self.macro["steps"])]
            if ids:
                self.tree.selection_set(ids)
                self.tree.see(ids[-1])
        self._update_title()

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
        if self.running:
            return
        x, y = pyautogui.position()
        if self.recording:
            return
        self._insert_step(new_step("click", x, y, delay=0.5))
        self.status.set(f"클릭 위치 추가: ({x}, {y})  — 메모를 적어두면 나중에 알아보기 쉽습니다.")

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
        self.macro = {"name": name, "repeat": 1, "start_wait": 2.0, "steps": []}
        self.repeat_var.set("1")
        self.start_wait_var.set("2")
        self.dirty = bool(name)
        self._refresh_macro_list()
        self._refresh_tree()
        self.status.set("인쇄 프로그램에서 누를 곳에 마우스를 올리고 F8을 누르세요. 또는 [● 클릭 녹화].")

    def _collect_options(self):
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
            elif key == keyboard.Key.f9:
                self.events.put(("hotkey", "start"))
            elif key == keyboard.Key.f10:
                self.events.put(("hotkey", "stop"))
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
                    elif arg == "start":
                        self.start()
                    elif arg == "stop":
                        if self.recording:
                            self._toggle_record()
                        else:
                            self.stop()
                elif ev == "status":
                    self.status.set(arg)
                elif ev == "highlight":
                    for iid in self.tree.tag_has("current"):
                        self.tree.item(iid, tags=())
                    if arg is not None and self.tree.exists(str(arg)):
                        self.tree.item(str(arg), tags=("current",))
                        self.tree.see(str(arg))
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
            if self.macro["steps"] and not messagebox.askyesno(
                    APP_TITLE, "녹화한 클릭을 지금 목록 끝에 이어서 추가합니다. 계속할까요?"):
                return
            self.recording = True
            self.rec_last_time = None
            self.rec_btn.config(text="■ 녹화 끝 (F10)")
            self.status.set("녹화 중… 인쇄 프로그램에서 평소처럼 클릭하세요. 끝나면 F10.")
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
            self.rec_btn.config(text="● 클릭 녹화")
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
        steps.append(new_step(kind, x, y, delay=0.5))
        self.rec_last_time = t
        self._mark_dirty()
        self._refresh_tree(select=[len(steps) - 1])
        self.status.set(f"녹화 중… {len(steps)}번째 클릭 ({x}, {y})  — 끝나면 F10")

    # ------------------------------------------------------------ 실행
    def start(self):
        if self.running or self.recording:
            return
        if not self.macro["steps"]:
            messagebox.showinfo(APP_TITLE, "등록된 단계가 없습니다.")
            return
        self._collect_options()
        self.running = True
        self.stop_event.clear()
        self.start_btn.state(["disabled"])
        move = {"빠름": 0.05, "보통": 0.2, "느림": 0.5}.get(self.speed_var.get(), 0.2)
        self.settings["speed"] = self.speed_var.get()
        steps = [dict(s) for s in self.macro["steps"]]
        threading.Thread(target=self._run, daemon=True,
                         args=(steps, self.macro["repeat"], self.macro["start_wait"], move)
                         ).start()

    def stop(self):
        if self.running:
            self.stop_event.set()
            self.status.set("정지하는 중…")

    def _run(self, steps, repeat, start_wait, move):
        put = self.events.put
        reason = "완료"
        try:
            t_end = time.time() + start_wait
            while time.time() < t_end:
                put(("status", f"{t_end - time.time():.0f}초 뒤 시작합니다… (정지: F10 / ESC)"))
                if self.stop_event.wait(0.2):
                    raise InterruptedError
            for r in range(repeat):
                for i, s in enumerate(steps):
                    if self.stop_event.is_set():
                        raise InterruptedError
                    put(("highlight", i))
                    put(("status", f"[{r + 1}/{repeat}회] {i + 1}/{len(steps)}단계: "
                                   f'{STEP_TYPES.get(s["type"])} {s["memo"]}'))
                    self._do_step(s, move)
                    if s["delay"] > 0 and self.stop_event.wait(s["delay"]):
                        raise InterruptedError
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
        self.start_btn.state(["!disabled"])
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
