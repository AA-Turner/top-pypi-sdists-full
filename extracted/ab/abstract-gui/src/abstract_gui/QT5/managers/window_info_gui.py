#!/usr/bin/env python3
"""Window Manager GUI – *no‑duplicate* file opener
==================================================
Cross‑platform PyQt5 utility that keeps one window per file.

Key features
------------
* **Live search** + type filter (Browser / Editor / Terminal / Other).
* **Select‑All by type**, bulk *Close Selected* — with *saved‑only* option.
* **Move / Minimize / Maximize** actions.
* **Open File…** – *never* spawns a duplicate:
  • if a window already contains that file’s *basename* in its title, it simply
    activates that window.
  • otherwise launches the file with the default app (Linux: `xdg-open`).
  • after open/activate, the window list refreshes.

Built for Linux/X11 (requires **wmctrl** + **xdotool**). Swap shell commands
for Windows/macOS as noted in comments.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from abstract_utilities import is_number
# -----------------------------------------------------------------------------
#  helper heuristics -----------------------------------------------------------
# -----------------------------------------------------------------------------

def classify_type(title: str) -> str:
    t = title.lower()
    if any(b in t for b in ("chrome", "firefox", "edge", "safari")):
        return "Browser"
    if any(e in t for e in ("code", "sublime", "pycharm", "notepad", "vim")):
        return "Editor"
    if any(term in t for term in ("terminal", "xterm", "cmd", "powershell")):
        return "Terminal"
    return "Other"


def looks_unsaved(title: str) -> bool:
    return (
        any(mark in title for mark in ("*", "●", "•"))
        or title.lower().startswith("untitled")
    )




    
# -----------------------------------------------------------------------------
#  main application ------------------------------------------------------------
# -----------------------------------------------------------------------------


class WindowManagerApp(QMainWindow):
    COLS = ["Window ID", "Title", "PID", "Monitor", "Type"]

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Window Manager")
        self.resize(980, 640)
        self.monitors: List[Tuple[str, int, int, int, int]] = []
        self.windows: List[Tuple[str, str, str, str, str]] = []  # incl. type
        self._build_ui()
        self.refresh()

    # ---------------- shell helpers ----------------
    def run_command(self, cmd: str) -> str:
        """Run *cmd* in a shell and return stdout (or "" on failure)."""
        try:
            out = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True
            ).stdout.strip()
            return out
        except subprocess.CalledProcessError as exc:
            self.statusBar().showMessage(f"Error: {exc}", 5000)
            return ""

    # ---------------- xrandr / wmctrl parsing ----------------
    def get_monitors(self) -> List[Tuple[str, int, int, int, int]]:
        self.monitors = []
        out = self.run_command("xrandr --query | grep ' connected'")
        for line in out.splitlines():
            m = re.match(r"(\S+)\s+connected\s+(\d+)x(\d+)\+(\d+)\+(\d+)", line)
            if m:
                name, w, h, x, y = m.groups()
                self.monitors.append((name, int(x), int(y), int(w), int(h)))
        return self.monitors
    
    def get_windows(self) -> List[Tuple[str, str, str, str, str]]:
        """Return [(id, pid, title, monitor, type), …]"""
        self.windows.clear()
        mons = self.get_monitors()
        out = self.run_command("wmctrl -l -p -G")
        
        for line in out.splitlines():
            parts = line.split()
            if len(parts) < 8:
                continue
            win_id, desktop, pid, x, y, w, h= parts[:7]
            title = " ".join(parts[8:])
            x, y = int(x), int(y)
            monitor = "Unknown"
            for name, mx, my, mw, mh in mons:
                if mx <= x < mx + mw and my <= y < my + mh:
                    monitor = name
                    break
            win_type = classify_type(title)
            self.windows.append((win_id, pid, title, monitor, win_type))
        return self.windows

    # ---------------- UI ------------------------------------------------------
    def _build_ui(self) -> None:
        central = QWidget(self)
        self.setCentralWidget(central)
        outer = QVBoxLayout(central)

        # filter row
        filt = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search titles…")
        self.search_edit.textChanged.connect(self.update_table)
        filt.addWidget(self.search_edit)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["All", "Browser", "Editor", "Terminal", "Other"])
        self.type_combo.currentIndexChanged.connect(self.update_table)
        filt.addWidget(self.type_combo)

        sel_type_btn = QPushButton("Select‑All (type)")
        sel_type_btn.clicked.connect(self.select_all_by_type)
        filt.addWidget(sel_type_btn)

        open_btn = QPushButton("Open File…")
        open_btn.clicked.connect(self.open_file)
        filt.addWidget(open_btn)

        outer.addLayout(filt)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.itemDoubleClicked.connect(self.activate_window)
        outer.addWidget(self.table, stretch=1)

        # control panel
        ctrl = QHBoxLayout()
        self.monitor_combo = QComboBox(); ctrl.addWidget(self.monitor_combo)

        mv_btn = QPushButton("Move to Monitor"); mv_btn.clicked.connect(self.move_window); ctrl.addWidget(mv_btn)
        mn_btn = QPushButton("Minimize"); mn_btn.clicked.connect(lambda: self.control_window("minimize")); ctrl.addWidget(mn_btn)
        mx_btn = QPushButton("Maximize"); mx_btn.clicked.connect(lambda: self.control_window("maximize")); ctrl.addWidget(mx_btn)
        cls_all_btn = QPushButton("Close Selected (all)"); cls_all_btn.clicked.connect(lambda: self.close_selected(True)); ctrl.addWidget(cls_all_btn)
        cls_saved_btn = QPushButton("Close Selected (saved)"); cls_saved_btn.clicked.connect(lambda: self.close_selected(False)); ctrl.addWidget(cls_saved_btn)
        rf_btn = QPushButton("Refresh"); rf_btn.clicked.connect(self.refresh); ctrl.addWidget(rf_btn)

        outer.addLayout(ctrl)
        self.setStatusBar(QStatusBar())

    # ---------------- table helpers ----------------
    def update_table(self) -> None:
        search = self.search_edit.text().lower()
        t_req = self.type_combo.currentText()
        rows = [w for w in self.windows if (not search or search in w[2].lower()) and (t_req == "All" or w[4] == t_req)]
        self.table.setRowCount(len(rows))
        for r, data in enumerate(rows):
            for c, val in enumerate(data):
                item = QTableWidgetItem(val)
                item.setData(Qt.UserRole, data)
                if c == 1 and looks_unsaved(val):
                    item.setForeground(Qt.red)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()

    def update_monitor_dropdown(self) -> None:
        self.monitor_combo.clear()
        self.monitor_combo.addItems([m[0] for m in self.monitors])

    # ---------------- core actions ----------------
    def refresh(self) -> None:
        self.get_windows()
        self.update_table()
        self.update_monitor_dropdown()
        self.statusBar().showMessage("Refreshed", 2500)

    def _selected_rows(self) -> List[Tuple[str, str, str, str, str]]:
        sel = []
        for idx in self.table.selectionModel().selectedRows():
            data = self.table.item(idx.row(), 0).data(Qt.UserRole)
            if data:
                sel.append(data)
        return sel

    def select_all_by_type(self) -> None:
        t_req = self.type_combo.currentText()
        if t_req == "All":
            self.table.selectAll(); return
        self.table.clearSelection()
        for r in range(self.table.rowCount()):
            if self.table.item(r, 4).text() == t_req:
                self.table.selectRow(r)

    def move_window(self) -> None:
        sel = self._selected_rows();
        if not sel:
            return
        tgt = self.monitor_combo.currentText()
        for win_id, *_ in sel:
            for name, x, y, *_ in self.monitors:
                if name == tgt:
                    self.run_command(f"wmctrl -i -r {win_id} -e 0,{x},{y},-1,-1")
        self.refresh()

    def control_window(self, act: str) -> None:
        sel = self._selected_rows();
        if not sel:
            return
        for win_id, *_ in sel:
            if act == "minimize":
                self.run_command(f"xdotool windowminimize {win_id}")
            elif act == "maximize":
                self.run_command(f"wmctrl -i -r {win_id} -b add,maximized_vert,maximized_horz")
        self.refresh()

    def close_selected(self, include_unsaved: bool) -> None:
        sel = self._selected_rows();
        if not sel:
            return
        skip, to_close = [], []
        for data in sel:
            win_id, _, title, *_ = data
            if looks_unsaved(title) and not include_unsaved:
                skip.append(title); continue
            to_close.append((win_id, title))
        if not to_close:
            QMessageBox.information(self, "Nothing to close", "No saved windows selected."); return
        if any(looks_unsaved(t) for _, t in to_close):
            if QMessageBox.question(self, "Unsaved?", "Some look unsaved – close anyway?", QMessageBox.Yes | QMessageBox.No) != QMessageBox.Yes:
                return
        for win_id, _ in to_close:
            self.run_command(f"xdotool windowclose {win_id}")
        msg = f"Closed {len(to_close)} window(s)" + (" (skipped unsaved)" if skip else "")
        self.statusBar().showMessage(msg, 4000)
        self.refresh()

    def activate_window(self, item) -> None:
        data = item.data(Qt.UserRole)
        if data:
            self.run_command(f"xdotool windowactivate {data[0]}")

    # ---------------- smart file opener ----------------
    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open file")
        if not path:
            return
        base = os.path.basename(path).lower()
        self.refresh()  # ensure latest list
        for win_id, pid, title, *_ in self.windows:
            if base in title.lower():
                # bring to front
                self.run_command(f"xdotool windowactivate {win_id}")
                self.statusBar().showMessage(f"Activated existing window for {base}", 3000)
                return
        # not found – open new
        self.run_command(f"xdg-open '{path}' &")  # async launch
        # give the app a moment to create its window, then refresh
        time.sleep(1.5)
        self.refresh()
        self.statusBar().showMessage(f"Opened {base}", 3000)


   
# -----------------------------------------------------------------------------
#  run ------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def parse_window_info(line):
    parts = line.split()
    window_js = {}
    keys = ['win_id', 'desktop', 'pid', 'x', 'y', 'w', 'h', 'extra']
    last_key=keys[0]
    for i,part in enumerate(parts):
        if last_key != "extra":
            last_key = keys[i]
            
        if last_key == "extra":
            found = False
            if last_key not in window_js:
                window_js[last_key] = []
            if window_js.get('location') == None:
                if os.path.exists(part):
                    found = True
                    window_js['location']=part
                    basename = os.path.basename(part)
                    window_js['basename'] = basename
                    if window_js.get('name') == None and window_js.get('extra'):
                        extra = window_js.get('extra')
                        name= ' '.join(extra)
                        window_js['name'] = name
                        window_js['extra'] = []
            if found == False:
                window_js[last_key].append(part)
        else:
          window_js[last_key]=part 
    x = window_js.get('x')
    y = window_js.get('y')
    if is_number(x) and is_number(y):
        window_js["monitor"] = get_monitor(x,y)
  
    return window_js
def get_window_mgr():
    app = QApplication(sys.argv)
    window_mgr = WindowManagerApp()
    return window_mgr
def get_window_info():
    window_mgr = get_window_mgr()
    return window_mgr.run_command("wmctrl -l -p -G")
def get_active_pid(win_id):
    window_mgr = get_window_mgr()
    return window_mgr.run_command(f"xdotool windowactivate {win_id}")
def get_monitors():
    window_mgr = get_window_mgr()
    return window_mgr.get_monitors()
def both_exist(path,winbase):
    if path and winbase:
        path = str(path)
        winbase = str(winbase)
        if os.path.exists(path) and os.path.exists(winbase):
            return True
    return False
def resolve_path_file(path,winbase=None,winpath=None):
    if winpath ==None and winbase==None:
        return False
    if winpath ==None and winbase:
        basename = os.path.basename(path).lower()
        winbase = winbase.lower()
        return basenam == winbase
    if winpath and winbase ==None:
        winbase = os.path.basename(winpath).lower()
    if not both_exist(winpath,path):
        return False
         
    basename = os.path.basename(path)
    if winbase.lower() == basename.lower():
        return True
    if os.path.isdir(winpath):
        if [base.lower() for base in os.listdir(winpath) if base and base == basename.lower()]:
            return True
    return False

def verify_file(line,filepath):
    window_js = parse_window_info(line)
    base = os.path.basename(file_path).lower()
    winpath = window_js.get('location')
    name = window_js.get('name')
    winbase = window_js.get('basename',name)
    
    if resolve_path_file(filepath,winbase=winbase,winpath=winpath):
        return window_js
def get_win_id_from_path(filepath):
    window_info = get_window_info()
    
    for line in window_info.split('\n'):
        window_js = verify_file(line,filepath)
        if window_js:
            return window_js
def get_monitor(x,y):
    mons = get_monitors()
    x, y = int(x), int(y)
    monitor = "Unknown"
    for name, mx, my, mw, mh in mons:
        if mx <= x < mx + mw and my <= y < my + mh:
            monitor = name
            break

    return monitor
def parse_window_infos():
    out = get_window_info()
    pieces = out.splitlines()
    for i,line in enumerate(pieces):
        try:
            window_js = parse_window_info(line)
            pieces.append(window_js)
        except Exception as e:
            print(f"{e}")
    return pieces
def get_file_attrib(file_path):
    window_info = get_window_info()
    lines = window_info.split('\n')
    get_win_id_from_path(file_path)
