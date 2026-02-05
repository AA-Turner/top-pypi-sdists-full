"""
CSSL Service Manager - Data models for runtime discovery, API nodes, and watches.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class RuntimeInfo:
    """Represents a discovered runtime instance."""
    id: str                             # Unique ID: f"{pid}_{create_time}"
    pid: int                            # OS process ID
    name: str                           # Process name
    language: str = "Python"            # "Python" | "CSSL" | "Python/CSSL"
    status: str = "discovered"          # discovered | attached | scanning | dead
    host: str = "localhost"             # Hostname or IP
    port: Optional[int] = None         # IPC port (None = not attached)
    memory_mb: float = 0.0             # Memory usage in MB
    cpu_pct: float = 0.0               # CPU usage percentage
    uptime: float = 0.0                # Seconds since process start
    cmdline: str = ""                  # Full command line
    marker_file: Optional[str] = None  # Path to .shareobj marker
    api_data: Optional[Dict] = None    # Scanned API (None = not scanned)
    create_time: float = 0.0           # Process creation timestamp
    last_seen: float = field(default_factory=time.time)

    @property
    def api_scanned(self) -> bool:
        return self.api_data is not None

    @property
    def is_alive(self) -> bool:
        return self.status not in ("dead", "disconnected")

    @property
    def display_name(self) -> str:
        if self.name:
            return f"{self.name} (PID {self.pid})"
        return f"PID {self.pid}"

    @property
    def uptime_str(self) -> str:
        s = int(self.uptime)
        if s < 60:
            return f"{s}s"
        elif s < 3600:
            return f"{s // 60}m {s % 60}s"
        else:
            h = s // 3600
            m = (s % 3600) // 60
            return f"{h}h {m}m"

    @property
    def memory_str(self) -> str:
        if self.memory_mb >= 1024:
            return f"{self.memory_mb / 1024:.1f} GB"
        return f"{self.memory_mb:.1f} MB"


@dataclass
class APINode:
    """Represents a node in the API tree (function, class, variable, module)."""
    name: str
    kind: str                          # "function" | "class" | "variable" | "module" | "method" | "builtin"
    signature: str = ""                # e.g. "print(value) -> void"
    docstring: str = ""                # Documentation string
    value_repr: str = ""               # repr(value) for variables
    type_name: str = ""                # Type name string
    address: str = ""                  # Hex memory address
    parent: str = ""                   # Parent namespace/class
    children: List['APINode'] = field(default_factory=list)
    is_expanded: bool = False

    @property
    def display_text(self) -> str:
        if self.kind == "function" or self.kind == "method" or self.kind == "builtin":
            return self.signature or f"{self.name}()"
        elif self.kind == "variable":
            return f"{self.name} = {self.value_repr}" if self.value_repr else self.name
        return self.name

    @property
    def icon_prefix(self) -> str:
        icons = {
            "function": "f",
            "method": "m",
            "builtin": "B",
            "class": "C",
            "variable": "v",
            "module": "M",
        }
        return icons.get(self.kind, "?")


@dataclass
class WatchVariable:
    """A variable being watched for changes."""
    name: str                          # Variable name or path
    runtime_id: str                    # Which runtime it belongs to
    last_value: str = ""               # Last known repr(value)
    last_type: str = ""                # Last known type
    update_count: int = 0              # How many times value changed
    last_update: float = field(default_factory=time.time)
    history: List[str] = field(default_factory=list)  # Last N values
    max_history: int = 50

    def update(self, new_value: str, new_type: str = ""):
        """Update with new value, track changes."""
        if new_value != self.last_value:
            self.update_count += 1
            if len(self.history) >= self.max_history:
                self.history.pop(0)
            self.history.append(self.last_value)
            self.last_value = new_value
            self.last_type = new_type
            self.last_update = time.time()
            return True  # Changed
        return False


@dataclass
class LogEntry:
    """A log entry for the output panel."""
    timestamp: float = field(default_factory=time.time)
    level: str = "info"                # info | warn | error | debug | success
    source: str = ""                   # Component that generated it
    message: str = ""

    @property
    def time_str(self) -> str:
        t = time.localtime(self.timestamp)
        return time.strftime("%H:%M:%S", t)


@dataclass
class Preferences:
    """User preferences, saved to JSON."""
    scan_interval: int = 30            # Auto-scan interval in seconds
    auto_scan: bool = True             # Enable auto-scan
    ipc_port_start: int = 45000        # IPC port range start
    ipc_port_end: int = 45100          # IPC port range end
    watch_interval: int = 1000         # Watch poll interval in ms
    max_history: int = 100             # Max command history entries
    font_size: int = 10                # Font size
    show_dead_processes: bool = False  # Show dead processes in list
    confirm_kill: bool = True          # Confirm before killing process
    log_ipc: bool = False              # Log IPC messages

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d: dict) -> 'Preferences':
        prefs = cls()
        for k, v in d.items():
            if hasattr(prefs, k):
                setattr(prefs, k, v)
        return prefs
