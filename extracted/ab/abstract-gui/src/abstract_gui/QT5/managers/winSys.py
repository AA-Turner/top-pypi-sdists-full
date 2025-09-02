import shlex, shutil
import subprocess as sp
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Mon:
    name: str; x: int; y: int; w: int; h: int

@dataclass(frozen=True)
class Win:
    wid: str        # 0x… hex
    pid: int
    x: int; y: int; w: int; h: int
    title: str
    desktop: int
class SystemIndex:
    _rx_mon = re.compile(r"^(\S+)\s+connected\s+(\d+)x(\d+)\+(\d+)\+(\d+)")
    # wmctrl -l -p -G line: 0xID DESK PID X Y W H HOST TITLE…
    _rx_win = re.compile(r"^(0x[0-9a-fA-F]+)\s+(-?\d+)\s+(\d+)\s+(-?\d+)\s+(-?\d+)\s+(\d+)\s+(\d+)\s+\S+\s+(.*)$")

    def __init__(self):
        self.mons: list[Mon] = []
        self.wins: list[Win] = []

    @staticmethod
    def run(cmd: list[str]) -> str:
        try:
            return sp.run(cmd, check=True, capture_output=True, text=True).stdout
        except sp.CalledProcessError:
            return ""

    def refresh(self):
        # monitors
        self.mons.clear()
        out = self.run(["xrandr", "--query"])
        for line in out.splitlines():
            m = self._rx_mon.match(line)
            if m:
                name, w, h, x, y = m.groups()
                self.mons.append(Mon(name, int(x), int(y), int(w), int(h)))
        # windows
        self.wins.clear()
        out = self.run(["wmctrl", "-l", "-p", "-G"])
        for line in out.splitlines():
            m = self._rx_win.match(line)
            if not m: 
                continue
            wid, desk, pid, x, y, w, h, title = m.groups()
            self.wins.append(Win(wid, int(pid), int(x), int(y), int(w), int(h), title, int(desk)))

    def monitor_of(self, x: int, y: int) -> str:
        for m in self.mons:
            if m.x <= x < m.x + m.w and m.y <= y < m.y + m.h:
                return m.name
        return "Unknown"
