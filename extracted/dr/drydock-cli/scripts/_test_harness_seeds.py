"""Seed projects for the operator's 52-case test harness.

P1 mdparse stays in _gauntlet_seed.py (it predates this module and is
shared with the gauntlet runner). P2-P6 live here.

Status:
  P2 taskvault  — DONE (31 tests green; bug-search 2 red, bug-dates 2 red, v1)
  P3 loglens    — DONE (29 tests green; bug-ipv6 2 red, bug-percentile 2 red)
  P4 pipeflow   — DONE (33 tests green; bug-mean 2 red, bug-dedupe 2 red)
  P5 keystore   — DONE (30 tests green; bug-lru/ttl/compact variants)
  P6 miniapi    — DONE (26 tests green; bug-pathparse 2 red)
  P0 romanize   — handled via seed="none" (empty workspace)

Each seed writer is `seed_PX(cwd: Path, variant: str)` and is
idempotent (overwrites pre-existing files at the same paths).
"""
from __future__ import annotations

from pathlib import Path


# ────────────────────────────────────────────────────────────────────────
# P2 — taskvault : CLI task tracker with JSON persistence
# ────────────────────────────────────────────────────────────────────────

_P2_INIT = '''"""taskvault — CLI task tracker with JSON persistence."""
from taskvault.models import Task
from taskvault.store import Store

__all__ = ["Task", "Store"]
__version__ = "1.2.0"
'''

_P2_MAIN = '''from taskvault.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
'''

_P2_MODELS = '''"""Task dataclass + JSON (de)serialization."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


_VALID_STATUS = {"open", "done"}
_VALID_PRIORITY = {"low", "med", "high"}


@dataclass
class Task:
    id: int
    title: str
    status: str = "open"
    priority: str = "med"
    tags: list[str] = field(default_factory=list)
    created: str = ""        # ISO date
    due: str | None = None   # ISO date or None

    def __post_init__(self) -> None:
        if self.status not in _VALID_STATUS:
            raise ValueError(f"invalid status: {self.status}")
        if self.priority not in _VALID_PRIORITY:
            raise ValueError(f"invalid priority: {self.priority}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Task":
        return cls(
            id=d["id"],
            title=d["title"],
            status=d.get("status", "open"),
            priority=d.get("priority", "med"),
            tags=list(d.get("tags", [])),
            created=d.get("created", ""),
            due=d.get("due"),
        )

    def is_overdue(self, today: date) -> bool:
        if self.status == "done" or not self.due:
            return False
        return self.due < today.isoformat()
'''

_P2_STORE = '''"""Atomic JSON store for taskvault. Schema v2: {"version":2,"tasks":[...]}."""
from __future__ import annotations

import json
import os
from pathlib import Path

from taskvault.models import Task

SCHEMA_VERSION = 2


class Store:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.is_file():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or raw.get("version") != SCHEMA_VERSION:
            raise ValueError(
                f"taskvault: unsupported store schema. Expected version "
                f"{SCHEMA_VERSION}; got {raw.get('version') if isinstance(raw, dict) else 'a list'}"
            )
        return [Task.from_dict(t) for t in raw.get("tasks", [])]

    def save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": SCHEMA_VERSION,
            "tasks": [t.to_dict() for t in tasks],
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        os.replace(tmp, self.path)

    def next_id(self, tasks: list[Task]) -> int:
        return (max((t.id for t in tasks), default=0)) + 1
'''

_P2_QUERY = '''"""Task filtering / search."""
from __future__ import annotations

from taskvault.models import Task


def filter_tasks(
    tasks: list[Task],
    *,
    status: str | None = None,
    tag: str | None = None,
    text: str | None = None,
    due_before: str | None = None,
) -> list[Task]:
    """Return tasks matching every provided filter.

    `text` is a **case-insensitive substring** match over title + tags.
    """
    out: list[Task] = []
    text_q = text.lower() if text else None
    for t in tasks:
        if status is not None and t.status != status:
            continue
        if tag is not None and tag not in t.tags:
            continue
        if text_q is not None:
            haystack = (t.title + " " + " ".join(t.tags)).lower()
            if text_q not in haystack:
                continue
        if due_before is not None:
            if not t.due or t.due >= due_before:
                continue
        out.append(t)
    return out
'''

_P2_DATES = '''"""Lenient due-date parser. Supports ISO, 'today', 'tomorrow', '+Nd', '+Nw'."""
from __future__ import annotations

import re
from datetime import date, timedelta


_DAYS_RE = re.compile(r"^\\+(\\d+)d$")
_WEEKS_RE = re.compile(r"^\\+(\\d+)w$")
_ISO_RE = re.compile(r"^\\d{4}-\\d{2}-\\d{2}$")


def parse_due(s: str, now: date) -> date:
    """Resolve `s` to a calendar date relative to `now`."""
    s = s.strip().lower()
    if s == "today":
        return now
    if s == "tomorrow":
        return now + timedelta(days=1)
    m = _DAYS_RE.match(s)
    if m:
        return now + timedelta(days=int(m.group(1)))
    m = _WEEKS_RE.match(s)
    if m:
        return now + timedelta(weeks=int(m.group(1)))
    if _ISO_RE.match(s):
        y, mo, d = s.split("-")
        return date(int(y), int(mo), int(d))
    raise ValueError(f"unrecognized due-date format: {s!r}")
'''

_P2_CONFIG = '''"""Minimal config loader for ~/.taskvault/config.toml."""
from __future__ import annotations

import tomllib
from pathlib import Path

DEFAULTS = {
    "default_priority": "med",
    "date_fmt": "iso",
}


def load_config(path: str | Path | None = None) -> dict:
    p = Path(path) if path else Path.home() / ".taskvault" / "config.toml"
    cfg = dict(DEFAULTS)
    if p.is_file():
        try:
            user = tomllib.loads(p.read_text(encoding="utf-8"))
            cfg.update(user)
        except Exception:
            pass
    return cfg
'''

_P2_CLI = '''"""taskvault CLI — subcommands: add, ls, done, rm, edit, search, due, export."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from taskvault.dates import parse_due
from taskvault.models import Task
from taskvault.query import filter_tasks
from taskvault.store import Store


DEFAULT_STORE = Path.home() / ".taskvault" / "tasks.json"


def _store(args) -> Store:
    return Store(args.store)


def cmd_add(args) -> int:
    s = _store(args)
    tasks = s.load()
    due_iso: str | None = None
    if args.due:
        due_iso = parse_due(args.due, date.today()).isoformat()
    t = Task(
        id=s.next_id(tasks),
        title=args.title,
        priority=args.priority,
        tags=args.tag or [],
        created=date.today().isoformat(),
        due=due_iso,
    )
    tasks.append(t)
    s.save(tasks)
    print(f"added #{t.id}: {t.title}")
    return 0


def cmd_ls(args) -> int:
    s = _store(args)
    tasks = s.load()
    if args.open_only:
        tasks = filter_tasks(tasks, status="open")
    for t in tasks:
        marker = "[x]" if t.status == "done" else "[ ]"
        due = f" (due {t.due})" if t.due else ""
        print(f"#{t.id} {marker} [{t.priority}] {t.title}{due}")
    return 0


def cmd_done(args) -> int:
    s = _store(args)
    tasks = s.load()
    for t in tasks:
        if t.id == args.id:
            t.status = "done"
            s.save(tasks)
            print(f"marked done: #{t.id}")
            return 0
    print(f"no task #{args.id}", file=sys.stderr)
    return 1


def cmd_rm(args) -> int:
    s = _store(args)
    tasks = [t for t in s.load() if t.id != args.id]
    s.save(tasks)
    print(f"removed #{args.id}")
    return 0


def cmd_search(args) -> int:
    s = _store(args)
    tasks = filter_tasks(s.load(), text=args.query)
    for t in tasks:
        print(f"#{t.id} {t.title}")
    return 0


def cmd_export(args) -> int:
    s = _store(args)
    tasks = s.load()
    json.dump([t.to_dict() for t in tasks], sys.stdout, indent=2)
    print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="taskvault", description="CLI task tracker.")
    p.add_argument("--store", default=str(DEFAULT_STORE),
                   help="path to tasks.json (default: ~/.taskvault/tasks.json)")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add"); a.add_argument("title")
    a.add_argument("--priority", choices=["low", "med", "high"], default="med")
    a.add_argument("--tag", action="append")
    a.add_argument("--due", default=None)
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("ls"); ls.add_argument("--open-only", action="store_true")
    ls.set_defaults(func=cmd_ls)

    d = sub.add_parser("done"); d.add_argument("id", type=int)
    d.set_defaults(func=cmd_done)

    rm = sub.add_parser("rm"); rm.add_argument("id", type=int)
    rm.set_defaults(func=cmd_rm)

    se = sub.add_parser("search"); se.add_argument("query")
    se.set_defaults(func=cmd_search)

    ex = sub.add_parser("export")
    ex.set_defaults(func=cmd_export)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
'''

# ── tests ────────────────────────────────────────────────────────────

_P2_TEST_MODELS = '''from taskvault.models import Task


def test_task_defaults():
    t = Task(id=1, title="x")
    assert t.status == "open"
    assert t.priority == "med"
    assert t.tags == []


def test_task_to_from_dict_roundtrip():
    t = Task(id=2, title="y", tags=["a", "b"], due="2026-12-31")
    d = t.to_dict()
    t2 = Task.from_dict(d)
    assert t == t2


def test_task_rejects_bad_status():
    import pytest
    with pytest.raises(ValueError):
        Task(id=3, title="z", status="bogus")


def test_task_rejects_bad_priority():
    import pytest
    with pytest.raises(ValueError):
        Task(id=4, title="z", priority="urgent")


def test_task_is_overdue():
    from datetime import date
    t = Task(id=5, title="m", due="2026-01-01")
    assert t.is_overdue(date(2026, 6, 1))
    t.status = "done"
    assert not t.is_overdue(date(2026, 6, 1))
'''

_P2_TEST_STORE = '''import json
from pathlib import Path

from taskvault.models import Task
from taskvault.store import Store, SCHEMA_VERSION


def test_load_empty(tmp_path):
    s = Store(tmp_path / "no.json")
    assert s.load() == []


def test_save_load_roundtrip(tmp_path):
    s = Store(tmp_path / "t.json")
    s.save([Task(id=1, title="a"), Task(id=2, title="b")])
    out = s.load()
    assert [t.title for t in out] == ["a", "b"]


def test_save_is_atomic(tmp_path):
    s = Store(tmp_path / "atomic.json")
    s.save([Task(id=1, title="a")])
    # tmp file should be gone
    assert not (tmp_path / "atomic.json.tmp").exists()
    assert (tmp_path / "atomic.json").exists()


def test_next_id_starts_at_one(tmp_path):
    s = Store(tmp_path / "n.json")
    assert s.next_id([]) == 1


def test_next_id_increments(tmp_path):
    s = Store(tmp_path / "n.json")
    tasks = [Task(id=1, title="a"), Task(id=5, title="b")]
    assert s.next_id(tasks) == 6


def test_load_rejects_old_schema(tmp_path):
    p = tmp_path / "old.json"
    p.write_text(json.dumps([{"id": 1, "title": "x"}]))
    import pytest
    with pytest.raises(ValueError):
        Store(p).load()


def test_load_rejects_wrong_version(tmp_path):
    p = tmp_path / "v9.json"
    p.write_text(json.dumps({"version": 9, "tasks": []}))
    import pytest
    with pytest.raises(ValueError):
        Store(p).load()
'''

_P2_TEST_QUERY = '''from taskvault.models import Task
from taskvault.query import filter_tasks


def _tasks():
    return [
        Task(id=1, title="Buy bread", tags=["shopping"]),
        Task(id=2, title="Read book", tags=["personal"], status="done"),
        Task(id=3, title="Buy milk", tags=["shopping", "urgent"], due="2026-06-01"),
        Task(id=4, title="Fix BUG in CLI", tags=["work"]),
    ]


def test_filter_by_status():
    out = filter_tasks(_tasks(), status="open")
    assert {t.id for t in out} == {1, 3, 4}


def test_filter_by_tag():
    out = filter_tasks(_tasks(), tag="shopping")
    assert {t.id for t in out} == {1, 3}


def test_filter_search_basic():
    # uses capitalized 'Buy' so a case-sensitive bug still passes here;
    # only the explicit case-insensitive test catches it
    out = filter_tasks(_tasks(), text="Buy")
    assert {t.id for t in out} == {1, 3}


def test_query_search_case_insensitive():
    out = filter_tasks(_tasks(), text="BUY")
    assert {t.id for t in out} == {1, 3}
    out = filter_tasks(_tasks(), text="bug")
    assert {t.id for t in out} == {4}


def test_filter_search_in_tags():
    out = filter_tasks(_tasks(), text="urgent")
    assert {t.id for t in out} == {3}


def test_filter_due_before():
    out = filter_tasks(_tasks(), due_before="2026-12-31")
    assert {t.id for t in out} == {3}


def test_filter_combined():
    out = filter_tasks(_tasks(), status="open", tag="shopping", text="milk")
    assert [t.id for t in out] == [3]


def test_filter_no_matches():
    assert filter_tasks(_tasks(), text="zzzzz") == []
'''

_P2_TEST_DATES = '''from datetime import date

from taskvault.dates import parse_due


def test_dates_today():
    n = date(2026, 6, 1)
    assert parse_due("today", n) == n


def test_dates_tomorrow():
    n = date(2026, 6, 1)
    assert parse_due("tomorrow", n) == date(2026, 6, 2)


def test_dates_plus_days():
    n = date(2026, 6, 1)
    assert parse_due("+3d", n) == date(2026, 6, 4)


def test_dates_relative_days():
    n = date(2026, 6, 1)
    assert parse_due("+1d", n) == date(2026, 6, 2)
    assert parse_due("+7d", n) == date(2026, 6, 8)


def test_dates_relative_weeks():
    n = date(2026, 6, 1)
    assert parse_due("+2w", n) == date(2026, 6, 15)


def test_dates_iso():
    assert parse_due("2026-12-31", date.today()) == date(2026, 12, 31)


def test_dates_unknown_raises():
    import pytest
    with pytest.raises(ValueError):
        parse_due("next sunday", date.today())
'''

_P2_TEST_CLI = '''import json
import subprocess
import sys
from pathlib import Path


def _tv(tmp_path, *args):
    store = tmp_path / "tasks.json"
    cmd = [sys.executable, "-m", "taskvault", "--store", str(store), *args]
    return subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())


def test_cli_add_and_ls(tmp_path):
    _tv(tmp_path, "add", "task A")
    _tv(tmp_path, "add", "task B")
    r = _tv(tmp_path, "ls")
    assert r.returncode == 0
    assert "task A" in r.stdout and "task B" in r.stdout


def test_cli_done_marks_status(tmp_path):
    _tv(tmp_path, "add", "x")
    _tv(tmp_path, "done", "1")
    r = _tv(tmp_path, "ls")
    assert "[x]" in r.stdout


def test_cli_search(tmp_path):
    _tv(tmp_path, "add", "Buy milk")
    _tv(tmp_path, "add", "Read book")
    r = _tv(tmp_path, "search", "BUY")
    assert r.returncode == 0
    assert "Buy milk" in r.stdout
    assert "Read book" not in r.stdout


def test_cli_export(tmp_path):
    _tv(tmp_path, "add", "x")
    r = _tv(tmp_path, "export")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert len(data) == 1 and data[0]["title"] == "x"
'''

_P2_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_P2_README = '''# taskvault

A small CLI task tracker with JSON persistence and atomic writes.

```
python3 -m taskvault add "Buy milk" --priority high --tag shopping --due +3d
python3 -m taskvault ls --open-only
python3 -m taskvault done 1
python3 -m taskvault search BUY
```

Schema v2: `{"version":2,"tasks":[...]}`. Atomic writes via tmp+rename.

Run the tests:

```
pytest -q
```
'''

_P2_FILES: dict[str, str] = {
    "taskvault/__init__.py": _P2_INIT,
    "taskvault/__main__.py": _P2_MAIN,
    "taskvault/cli.py": _P2_CLI,
    "taskvault/store.py": _P2_STORE,
    "taskvault/models.py": _P2_MODELS,
    "taskvault/query.py": _P2_QUERY,
    "taskvault/dates.py": _P2_DATES,
    "taskvault/config.py": _P2_CONFIG,
    "tests/test_store.py": _P2_TEST_STORE,
    "tests/test_models.py": _P2_TEST_MODELS,
    "tests/test_query.py": _P2_TEST_QUERY,
    "tests/test_dates.py": _P2_TEST_DATES,
    "tests/test_cli.py": _P2_TEST_CLI,
    "pytest.ini": _P2_PYTEST_INI,
    "README.md": _P2_README,
}


def seed_taskvault(cwd: Path, variant: str = "clean") -> None:
    """Seed the taskvault project. Variants:
      - 'clean'       — all 31 tests green
      - 'bug-search'  — query.filter_tasks does case-sensitive (2 red)
      - 'bug-dates'   — parse_due +Nd off-by-one (2 red)
      - 'v1'          — store on disk is v1 schema (4 red, migration)
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _P2_FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    if variant == "bug-search":
        # filter_tasks loses lowercasing on both sides.
        p = cwd / "taskvault" / "query.py"
        t = p.read_text()
        t = t.replace(
            "text_q = text.lower() if text else None",
            "text_q = text if text else None",
        )
        t = t.replace(
            "haystack = (t.title + \" \" + \" \".join(t.tags)).lower()",
            "haystack = (t.title + \" \" + \" \".join(t.tags))",
        )
        p.write_text(t)

    elif variant == "bug-dates":
        # parse_due `+Nd` uses days=n-1.
        p = cwd / "taskvault" / "dates.py"
        t = p.read_text()
        t = t.replace(
            "return now + timedelta(days=int(m.group(1)))",
            "return now + timedelta(days=int(m.group(1)) - 1)",
            1,
        )
        p.write_text(t)

    elif variant == "v1":
        # No code change; just lay down a v1 store file at the default
        # path the migration case will point its --store at. The runner
        # writes /tmp/<workspace>/legacy_tasks.json so the model has a
        # concrete v1 file to migrate.
        legacy = cwd / "legacy_tasks.json"
        import json as _json
        legacy.write_text(_json.dumps([
            {"id": 1, "title": "Old task A",
             "status": "open", "priority": "med",
             "tags": [], "created": "2025-12-01",
             "due": "06/01/2026"},
            {"id": 2, "title": "Old task B",
             "status": "done", "priority": "high",
             "tags": ["work"], "created": "2025-12-05",
             "due": "12/31/2026"},
        ], indent=2), encoding="utf-8")


# ────────────────────────────────────────────────────────────────────────
# P3 — loglens : log parsing & regex search CLI
# ────────────────────────────────────────────────────────────────────────

_P3_INIT = '''"""loglens — log parsing & regex search CLI."""
from loglens.parser import parse_line
from loglens.records import LogRecord

__all__ = ["LogRecord", "parse_line"]
__version__ = "0.1.0"
'''

_P3_MAIN = '''from loglens.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
'''

_P3_PATTERNS = '''"""Compiled regexes + field maps for the supported log formats."""
from __future__ import annotations

import re

# Apache combined log format. IPv4 and IPv6 both supported via [0-9a-fA-F:.]+
APACHE = re.compile(
    r'(?P<ip>[0-9a-fA-F:.]+)\\s+'
    r'(?P<ident>\\S+)\\s+'
    r'(?P<user>\\S+)\\s+'
    r'\\[(?P<ts>[^\\]]+)\\]\\s+'
    r'"(?P<method>[A-Z]+)\\s+(?P<path>\\S+)\\s+(?P<proto>HTTP/[0-9.]+)"\\s+'
    r'(?P<status>\\d+)\\s+'
    r'(?P<bytes>\\d+|-)\\s+'
    r'"(?P<referer>[^"]*)"\\s+'
    r'"(?P<ua>[^"]*)"'
)

# Syslog: "Jan 12 12:34:56 host program[pid]: message"
SYSLOG = re.compile(
    r'(?P<ts>\\w{3}\\s+\\d{1,2}\\s+\\d{2}:\\d{2}:\\d{2})\\s+'
    r'(?P<host>\\S+)\\s+'
    r'(?P<program>[\\w-]+)(?:\\[(?P<pid>\\d+)\\])?:\\s+'
    r'(?P<msg>.*)'
)

FIELD_MAP = {
    "apache": ["ip", "method", "path", "status", "bytes"],
    "syslog": ["ts", "host", "program", "msg"],
    "jsonl":  ["ts", "level", "msg", "req_id"],
}
'''

_P3_RECORDS = '''"""LogRecord dataclass."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LogRecord:
    raw: str = ""
    ts: str = ""
    level: str = ""
    ip: str = ""
    method: str = ""
    path: str = ""
    status: int = 0
    bytes: int = 0
    msg: str = ""
    fmt: str = ""
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "ts": self.ts, "level": self.level, "ip": self.ip,
            "method": self.method, "path": self.path,
            "status": self.status, "bytes": self.bytes,
            "msg": self.msg, "fmt": self.fmt,
        }
'''

_P3_PARSER = '''"""Line-by-line log parser."""
from __future__ import annotations

import json

from loglens.patterns import APACHE, SYSLOG
from loglens.records import LogRecord


def sniff_format(sample: str) -> str:
    """Guess the log format from a single line."""
    if APACHE.match(sample):
        return "apache"
    if SYSLOG.match(sample):
        return "syslog"
    try:
        d = json.loads(sample)
        if isinstance(d, dict):
            return "jsonl"
    except Exception:
        pass
    return "unknown"


def parse_line(line: str, fmt: str | None = None) -> LogRecord | None:
    """Parse a single line. Returns None on parse failure (never raises)."""
    line = line.rstrip("\\n")
    if not line.strip():
        return None
    if fmt is None:
        fmt = sniff_format(line)
    try:
        if fmt == "apache":
            m = APACHE.match(line)
            if not m:
                return None
            g = m.groupdict()
            return LogRecord(
                raw=line, fmt="apache", ts=g["ts"], ip=g["ip"],
                method=g["method"], path=g["path"],
                status=int(g["status"]),
                bytes=int(g["bytes"]) if g["bytes"] != "-" else 0,
                extra={"user": g["user"], "referer": g["referer"], "ua": g["ua"]},
            )
        if fmt == "syslog":
            m = SYSLOG.match(line)
            if not m:
                return None
            g = m.groupdict()
            return LogRecord(
                raw=line, fmt="syslog", ts=g["ts"], msg=g["msg"],
                extra={"host": g["host"], "program": g["program"], "pid": g.get("pid")},
            )
        if fmt == "jsonl":
            d = json.loads(line)
            if not isinstance(d, dict):
                return None
            return LogRecord(
                raw=line, fmt="jsonl",
                ts=str(d.get("ts", "")),
                level=str(d.get("level", "")),
                msg=str(d.get("msg", "")),
                extra={k: v for k, v in d.items()
                       if k not in {"ts", "level", "msg"}},
            )
    except Exception:
        return None
    return None
'''

_P3_FILTERS = '''"""Predicate builders for filtering log records."""
from __future__ import annotations

import re
from collections.abc import Callable

from loglens.records import LogRecord


_LEVEL_RANK = {"DEBUG": 10, "INFO": 20, "WARN": 30, "WARNING": 30,
               "ERROR": 40, "CRITICAL": 50, "FATAL": 50}


def by_level(min_level: str) -> Callable[[LogRecord], bool]:
    floor = _LEVEL_RANK.get(min_level.upper(), 0)
    def _p(r: LogRecord) -> bool:
        return _LEVEL_RANK.get(r.level.upper(), 0) >= floor
    return _p


def by_time(start: str | None, end: str | None) -> Callable[[LogRecord], bool]:
    def _p(r: LogRecord) -> bool:
        if start and r.ts < start:
            return False
        if end and r.ts > end:
            return False
        return True
    return _p


def by_field(key: str, value: str) -> Callable[[LogRecord], bool]:
    def _p(r: LogRecord) -> bool:
        actual = getattr(r, key, None)
        if actual is None and key in r.extra:
            actual = r.extra[key]
        return str(actual) == value
    return _p


def compile_grep(rx: str) -> Callable[[LogRecord], bool]:
    try:
        pat = re.compile(rx)
    except re.error as e:
        raise ValueError(f"invalid regex {rx!r}: {e}") from e
    def _p(r: LogRecord) -> bool:
        return bool(pat.search(r.raw))
    return _p
'''

_P3_AGGREGATE = '''"""Aggregate stats over LogRecords."""
from __future__ import annotations

import math
from collections import Counter

from loglens.records import LogRecord


def count_by(records: list[LogRecord], field: str) -> dict[str, int]:
    c: Counter = Counter()
    for r in records:
        v = getattr(r, field, None)
        if v is None and field in r.extra:
            v = r.extra[field]
        if v not in (None, ""):
            c[str(v)] += 1
    return dict(c)


def top_n(records: list[LogRecord], field: str, n: int) -> list[tuple[str, int]]:
    return Counter(count_by(records, field)).most_common(n)


def status_class_hist(records: list[LogRecord]) -> dict[str, int]:
    c: Counter = Counter()
    for r in records:
        if r.status:
            c[f"{r.status // 100}xx"] += 1
    return dict(c)


def percentile(vals: list[float], p: float) -> float:
    """Nearest-rank percentile: vals_sorted[ceil(p/100*n)-1]."""
    if not vals:
        raise ValueError("percentile of empty list")
    s = sorted(vals)
    n = len(s)
    idx = math.ceil(p / 100.0 * n) - 1
    idx = max(0, min(n - 1, idx))
    return s[idx]
'''

_P3_IO = '''"""I/O helpers: open .log/.gz transparently."""
from __future__ import annotations

import gzip
from collections.abc import Iterator
from pathlib import Path


def open_log(path: str | Path):
    p = Path(path)
    if str(p).endswith(".gz"):
        return gzip.open(p, "rt", encoding="utf-8", errors="replace")
    return p.open("r", encoding="utf-8", errors="replace")


def iter_lines(path: str | Path) -> Iterator[str]:
    with open_log(path) as f:
        for line in f:
            yield line
'''

_P3_CLI = '''"""loglens CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loglens.aggregate import count_by, top_n
from loglens.filters import by_field, by_level, compile_grep
from loglens.io import iter_lines
from loglens.parser import parse_line, sniff_format


def _records(path):
    first = ""
    for line in iter_lines(path):
        first = line
        break
    fmt = sniff_format(first) if first else "unknown"
    for line in iter_lines(path):
        rec = parse_line(line, fmt=fmt)
        if rec is not None:
            yield rec


def cmd_grep(args) -> int:
    try:
        pred = compile_grep(args.pattern)
    except ValueError as e:
        print(f"loglens: {e}", file=sys.stderr)
        return 2
    n = 0
    for rec in _records(args.path):
        if pred(rec):
            print(rec.raw)
            n += 1
    print(f"# matches: {n}", file=sys.stderr)
    return 0


def cmd_stats(args) -> int:
    counts = count_by(list(_records(args.path)), args.field)
    for k in sorted(counts):
        print(f"{k}\\t{counts[k]}")
    return 0


def cmd_top(args) -> int:
    for val, c in top_n(list(_records(args.path)), args.field, args.n):
        print(f"{c}\\t{val}")
    return 0


def cmd_filter(args) -> int:
    preds = []
    if args.level:
        preds.append(by_level(args.level))
    if args.field and args.value:
        preds.append(by_field(args.field, args.value))
    for rec in _records(args.path):
        if all(p(rec) for p in preds):
            print(rec.raw)
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="loglens", description="Log analyzer.")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("grep")
    g.add_argument("pattern"); g.add_argument("path")
    g.set_defaults(func=cmd_grep)

    f = sub.add_parser("filter")
    f.add_argument("path"); f.add_argument("--level")
    f.add_argument("--field"); f.add_argument("--value")
    f.set_defaults(func=cmd_filter)

    s = sub.add_parser("stats")
    s.add_argument("path"); s.add_argument("field")
    s.set_defaults(func=cmd_stats)

    t = sub.add_parser("top")
    t.add_argument("path"); t.add_argument("field")
    t.add_argument("-n", type=int, default=10)
    t.set_defaults(func=cmd_top)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)
'''

_P3_TEST_PATTERNS = '''import re

from loglens.patterns import APACHE, SYSLOG, FIELD_MAP


def test_apache_basic():
    line = '127.0.0.1 - frank [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'
    m = APACHE.match(line)
    assert m is not None
    assert m.group("ip") == "127.0.0.1"
    assert m.group("method") == "GET"
    assert m.group("status") == "200"


def test_patterns_ipv6():
    line = '::1 - - [10/Oct/2025:13:55:36 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'
    m = APACHE.match(line)
    assert m is not None
    assert ":" in m.group("ip")


def test_apache_404():
    line = '10.0.0.5 - - [11/Oct/2025:00:01:02 +0000] "GET /missing HTTP/1.1" 404 0 "-" "curl"'
    m = APACHE.match(line)
    assert m and m.group("status") == "404"


def test_syslog_basic():
    line = "Jan 12 12:34:56 myhost sshd[1234]: Accepted publickey for bob"
    m = SYSLOG.match(line)
    assert m is not None
    assert m.group("host") == "myhost"
    assert m.group("program") == "sshd"
    assert m.group("pid") == "1234"


def test_syslog_no_pid():
    line = "Jan 12 12:34:56 myhost kernel: oom-kill triggered"
    m = SYSLOG.match(line)
    assert m is not None
    assert m.group("pid") is None


def test_field_map_has_all_formats():
    for fmt in ("apache", "syslog", "jsonl"):
        assert fmt in FIELD_MAP
        assert isinstance(FIELD_MAP[fmt], list)
'''

_P3_TEST_PARSER = '''import json

from loglens.parser import parse_line, sniff_format


def test_parse_apache_line():
    line = '1.2.3.4 - - [10/Oct/2025:13:55:36 +0000] "POST /api HTTP/1.1" 200 50 "-" "-"'
    r = parse_line(line)
    assert r is not None
    assert r.fmt == "apache"
    assert r.method == "POST" and r.status == 200


def test_parse_syslog_line():
    line = "Jan 12 12:34:56 host prog: hello"
    r = parse_line(line)
    assert r is not None
    assert r.fmt == "syslog"
    assert "hello" in r.msg


def test_parse_jsonl_line():
    line = json.dumps({"ts": "2025-10-10T00:00:00", "level": "INFO", "msg": "ok"})
    r = parse_line(line)
    assert r is not None
    assert r.fmt == "jsonl"
    assert r.level == "INFO"


def test_parse_returns_none_on_garbage():
    assert parse_line("===not anything===") is None


def test_parse_returns_none_on_blank():
    assert parse_line("") is None
    assert parse_line("   \\n") is None


def test_parse_never_raises():
    # Truly malformed input shouldn't raise.
    for s in ['{"bad json', "[]", "1 2 3", "}{}]"]:
        try:
            parse_line(s)
        except Exception as e:
            assert False, f"parse_line raised on {s!r}: {e!r}"


def test_sniff_format():
    assert sniff_format('1.2.3.4 - - [x] "GET / HTTP/1.1" 200 0 "-" "-"') == "apache"
    assert sniff_format("Jan 12 12:34:56 h p: x") == "syslog"
    assert sniff_format('{"ts":"x","msg":"y"}') == "jsonl"
    assert sniff_format("garbage") == "unknown"
'''

_P3_TEST_FILTERS = '''import pytest

from loglens.filters import by_field, by_level, by_time, compile_grep
from loglens.records import LogRecord


def _recs():
    return [
        LogRecord(raw="r1", level="DEBUG"),
        LogRecord(raw="r2", level="INFO"),
        LogRecord(raw="r3", level="WARN", ts="2025-10-10"),
        LogRecord(raw="r4", level="ERROR", ts="2025-10-12"),
    ]


def test_by_level_filters_below():
    p = by_level("WARN")
    out = [r for r in _recs() if p(r)]
    assert {r.raw for r in out} == {"r3", "r4"}


def test_by_level_includes_above():
    p = by_level("INFO")
    out = [r for r in _recs() if p(r)]
    assert "r1" not in {r.raw for r in out}


def test_by_time_inclusive():
    p = by_time("2025-10-10", "2025-10-12")
    out = [r for r in _recs() if p(r)]
    assert {r.raw for r in out} == {"r3", "r4"}


def test_by_field_status():
    recs = [LogRecord(raw="x", status=200), LogRecord(raw="y", status=404)]
    p = by_field("status", "404")
    assert [r.raw for r in recs if p(r)] == ["y"]


def test_compile_grep_match():
    p = compile_grep(r"\\bGET\\b")
    assert p(LogRecord(raw="GET /x"))
    assert not p(LogRecord(raw="POST /x"))


def test_compile_grep_invalid_raises():
    with pytest.raises(ValueError):
        compile_grep("[")
'''

_P3_TEST_AGGREGATE = '''import pytest

from loglens.aggregate import count_by, percentile, status_class_hist, top_n
from loglens.records import LogRecord


def _recs_apache():
    return [
        LogRecord(raw="a", ip="1.1.1.1", status=200),
        LogRecord(raw="b", ip="1.1.1.1", status=404),
        LogRecord(raw="c", ip="2.2.2.2", status=500),
        LogRecord(raw="d", ip="::1", status=200),
    ]


def test_count_by_ip():
    c = count_by(_recs_apache(), "ip")
    assert c["1.1.1.1"] == 2
    assert c["::1"] == 1


def test_aggregate_count_total():
    # Parses access.log via the apache regex; under bug-ipv6 the IPv6
    # line yields None so this total drops by 1.
    from pathlib import Path

    from loglens.parser import parse_line

    log = Path(__file__).parent.parent / "sample_logs" / "access.log"
    recs = []
    if log.is_file():
        for line in log.read_text().splitlines():
            r = parse_line(line, fmt="apache")
            if r is not None:
                recs.append(r)
    c = count_by(recs, "ip")
    # access.log ships 33 entries total: 15 + 8 + 6 + 3 + 1 (IPv6) = 33
    assert sum(c.values()) == 33


def test_status_class_hist():
    h = status_class_hist(_recs_apache())
    assert h.get("2xx") == 2
    assert h.get("4xx") == 1
    assert h.get("5xx") == 1


def test_top_n():
    out = top_n(_recs_apache(), "ip", 2)
    assert out[0][0] == "1.1.1.1"
    assert out[0][1] == 2


def test_percentile_p50():
    # 1..10 → p50 → index ceil(50/100*10) - 1 = 4 → vals[4] = 5
    assert percentile(list(range(1, 11)), 50) == 5


def test_aggregate_p95():
    # 1..100 → p95 → ceil(95) - 1 = 94 → 95
    assert percentile(list(range(1, 101)), 95) == 95


def test_aggregate_p100():
    assert percentile(list(range(1, 11)), 100) == 10


def test_percentile_empty_raises():
    with pytest.raises(ValueError):
        percentile([], 50)
'''

_P3_TEST_CLI = '''import subprocess
import sys
from pathlib import Path


def _logs():
    return Path(__file__).parent.parent / "sample_logs" / "access.log"


def test_cli_grep_runs():
    p = _logs()
    if not p.is_file():
        return  # accept absence in some envs
    r = subprocess.run(
        [sys.executable, "-m", "loglens", "grep", "GET", str(p)],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0


def test_cli_top_runs():
    p = _logs()
    if not p.is_file():
        return
    r = subprocess.run(
        [sys.executable, "-m", "loglens", "top", str(p), "ip", "-n", "3"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
'''


def _p3_sample_apache_log() -> str:
    """~40 lines of apache-combined sample including one IPv6 entry."""
    lines = []
    for i in range(15):
        lines.append(
            f'10.0.0.{i+1} - - [10/Oct/2025:00:00:{i:02d} +0000] '
            f'"GET /page{i} HTTP/1.1" 200 {1000+i*10} "-" "Mozilla/5.0"'
        )
    for i in range(8):
        lines.append(
            f'192.168.1.{i+1} - - [10/Oct/2025:00:01:{i:02d} +0000] '
            f'"POST /api/v1 HTTP/1.1" 201 {500+i*5} "-" "curl/7.81.0"'
        )
    for i in range(6):
        lines.append(
            f'172.16.0.{i+1} - - [10/Oct/2025:00:02:{i:02d} +0000] '
            f'"GET /404page HTTP/1.1" 404 0 "-" "bot"'
        )
    for i in range(3):
        lines.append(
            f'10.10.10.{i+1} - - [10/Oct/2025:00:03:{i:02d} +0000] '
            f'"GET /broken HTTP/1.1" 500 200 "-" "-"'
        )
    # one IPv6 line
    lines.append(
        '::1 - - [10/Oct/2025:00:04:00 +0000] '
        '"GET /local HTTP/1.1" 200 80 "-" "client"'
    )
    return "\n".join(lines) + "\n"


def _p3_sample_jsonl() -> str:
    import json as _json
    out = []
    for i in range(10):
        out.append(_json.dumps({
            "ts": f"2025-10-10T00:00:{i:02d}",
            "level": "INFO" if i % 3 else "WARN",
            "msg": f"event {i}", "req_id": f"req-{i}",
        }))
    return "\n".join(out) + "\n"


def _p3_sample_syslog() -> str:
    out = []
    for i in range(10):
        out.append(f"Jan 12 12:{i:02d}:00 hostA progB[{1000+i}]: event {i}")
    return "\n".join(out) + "\n"


_P3_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_P3_README = '''# loglens

Streaming log analyzer (apache combined, syslog, JSONL) with grep / filter /
stats / top subcommands.

```
python3 -m loglens grep GET sample_logs/access.log
python3 -m loglens top sample_logs/access.log ip -n 5
```

Tests:

```
pytest -q
```
'''

_P3_FILES: dict[str, str] = {
    "loglens/__init__.py": _P3_INIT,
    "loglens/__main__.py": _P3_MAIN,
    "loglens/cli.py": _P3_CLI,
    "loglens/patterns.py": _P3_PATTERNS,
    "loglens/parser.py": _P3_PARSER,
    "loglens/records.py": _P3_RECORDS,
    "loglens/filters.py": _P3_FILTERS,
    "loglens/aggregate.py": _P3_AGGREGATE,
    "loglens/io.py": _P3_IO,
    "tests/test_patterns.py": _P3_TEST_PATTERNS,
    "tests/test_parser.py": _P3_TEST_PARSER,
    "tests/test_filters.py": _P3_TEST_FILTERS,
    "tests/test_aggregate.py": _P3_TEST_AGGREGATE,
    "tests/test_cli.py": _P3_TEST_CLI,
    "pytest.ini": _P3_PYTEST_INI,
    "README.md": _P3_README,
}


def seed_loglens(cwd: Path, variant: str = "clean") -> None:
    """Seed loglens. Variants:
      - 'clean'           — 29 tests green
      - 'bug-ipv6'        — APACHE IP group is \\d+\\.\\d+\\.\\d+\\.\\d+ only (2 red)
      - 'bug-percentile'  — percentile uses int(p/100*n), no -1 (2 red)
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _P3_FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    # sample logs
    samples = cwd / "sample_logs"
    samples.mkdir(exist_ok=True)
    (samples / "access.log").write_text(_p3_sample_apache_log(), encoding="utf-8")
    (samples / "app.jsonl").write_text(_p3_sample_jsonl(), encoding="utf-8")
    (samples / "syslog.log").write_text(_p3_sample_syslog(), encoding="utf-8")

    if variant == "bug-ipv6":
        p = cwd / "loglens" / "patterns.py"
        t = p.read_text()
        # the on-disk file has single backslash before s+ inside r'...'
        t = t.replace(
            "(?P<ip>[0-9a-fA-F:.]+)",
            r"(?P<ip>\d+\.\d+\.\d+\.\d+)",
        )
        p.write_text(t)

    elif variant == "bug-percentile":
        p = cwd / "loglens" / "aggregate.py"
        t = p.read_text()
        t = t.replace(
            "idx = math.ceil(p / 100.0 * n) - 1",
            "idx = int(p / 100.0 * n)",
        )
        p.write_text(t)


# ────────────────────────────────────────────────────────────────────────
# P4 — pipeflow : CSV/JSON data pipeline (ETL)
# ────────────────────────────────────────────────────────────────────────

_P4_INIT = '''"""pipeflow — compose source → validate → transform → aggregate → sink stages."""
from pipeflow.pipeline import Pipeline
from pipeflow.schema import ColumnSpec

__all__ = ["Pipeline", "ColumnSpec"]
__version__ = "0.1.0"
'''

_P4_MAIN = '''from pipeflow.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
'''

_P4_SCHEMA = '''"""Column schema and validation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ColumnSpec:
    name: str
    type: type
    required: bool = True


def coerce_cell(value: Any, target_type: type) -> Any:
    if value is None or value == "":
        return None
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return str(value)
    if target_type is bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"true", "1", "yes", "y"}
    raise TypeError(f"unsupported type {target_type}")


def validate(rows: list[dict], schema: list[ColumnSpec]) -> tuple[list[dict], list[dict]]:
    """Return (ok_rows, errors). Required-and-missing → error; bad type → error."""
    ok: list[dict] = []
    errs: list[dict] = []
    for i, row in enumerate(rows):
        bad = False
        for col in schema:
            v = row.get(col.name)
            if v is None or (isinstance(v, str) and not v):
                if col.required:
                    errs.append({"row": i, "col": col.name, "reason": "missing"})
                    bad = True
                    break
                continue
            try:
                row[col.name] = coerce_cell(v, col.type)
            except (TypeError, ValueError):
                errs.append({"row": i, "col": col.name, "reason": "bad_type",
                             "value": v})
                bad = True
                break
        if not bad:
            ok.append(row)
    return ok, errs
'''

_P4_SOURCES = '''"""CSV/JSON source readers with schema-driven coercion."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from pipeflow.schema import ColumnSpec, coerce_cell


def read_csv(path: str | Path, schema: list[ColumnSpec] | None = None):
    """Read CSV. Returns (rows, errors). Skips fully-blank rows.
    Non-coercible cells go to errors, NOT silently zeroed.
    """
    rows: list[dict] = []
    errors: list[dict] = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if not any((v or "").strip() for v in row.values()):
                continue
            if schema is None:
                rows.append(dict(row))
                continue
            new_row: dict = {}
            bad = False
            for col in schema:
                v = row.get(col.name, "")
                if v is None or (isinstance(v, str) and not v.strip()):
                    if col.required:
                        errors.append({"row": i, "col": col.name, "reason": "missing"})
                        bad = True
                        break
                    new_row[col.name] = None
                    continue
                try:
                    new_row[col.name] = coerce_cell(v, col.type)
                except (TypeError, ValueError):
                    errors.append({"row": i, "col": col.name, "reason": "bad_type", "value": v})
                    bad = True
                    break
            if not bad:
                rows.append(new_row)
    return rows, errors


def read_json(path: str | Path) -> list[dict]:
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)
'''

_P4_TRANSFORMS = '''"""Row-level transforms."""
from __future__ import annotations

from collections.abc import Callable


def select(rows: list[dict], cols: list[str]) -> list[dict]:
    return [{c: r.get(c) for c in cols} for r in rows]


def rename(rows: list[dict], mapping: dict[str, str]) -> list[dict]:
    out = []
    for r in rows:
        nr = dict(r)
        for old, new in mapping.items():
            if old in nr:
                nr[new] = nr.pop(old)
        out.append(nr)
    return out


def derive(rows: list[dict], col: str, fn: Callable) -> list[dict]:
    out = []
    for r in rows:
        nr = dict(r)
        nr[col] = fn(nr)
        out.append(nr)
    return out


def filter_rows(rows: list[dict], pred: Callable) -> list[dict]:
    return [r for r in rows if pred(r)]


def dedupe(rows: list[dict], key: str, keep: str = "first") -> list[dict]:
    """Keep the FIRST occurrence by key order. (keep='last' available too.)"""
    seen: dict = {}
    if keep == "first":
        for r in rows:
            k = r.get(key)
            if k not in seen:
                seen[k] = r
    elif keep == "last":
        for r in rows:
            k = r.get(key)
            seen[k] = r
    else:
        raise ValueError(f"unsupported keep={keep!r}")
    return list(seen.values())
'''

_P4_AGGREGATE = '''"""Group-by aggregations."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable


def _present(vals):
    return [v for v in vals if v is not None]


def sum_(vals):
    return sum(_present(vals))


def mean(vals):
    p = _present(vals)
    if not p:
        return None
    return sum(p) / len(p)


def count(vals):
    return len(_present(vals))


def min_(vals):
    p = _present(vals)
    return min(p) if p else None


def max_(vals):
    p = _present(vals)
    return max(p) if p else None


_FUNCS: dict[str, Callable] = {
    "sum": sum_, "mean": mean, "count": count, "min": min_, "max": max_,
}


def group_by(rows: list[dict], key: str, aggs: dict[str, dict[str, str]]):
    """`aggs` = {col_name: {"fn": "sum"|"mean"|..., "as": "out_col"}}.
    Returns list of {key, **out_cols}.
    """
    buckets: dict = defaultdict(lambda: defaultdict(list))
    for r in rows:
        k = r.get(key)
        for col, _ in aggs.items():
            buckets[k][col].append(r.get(col))
    out = []
    for k, cols in buckets.items():
        row = {key: k}
        for col, spec in aggs.items():
            fn_name = spec["fn"]
            out_col = spec.get("as", f"{col}_{fn_name}")
            row[out_col] = _FUNCS[fn_name](cols[col])
        out.append(row)
    return out
'''

_P4_SINKS = '''"""Output writers."""
from __future__ import annotations

import csv
import json
from pathlib import Path


def write_csv(rows: list[dict], path: str | Path) -> None:
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_json(rows: list[dict], path: str | Path) -> None:
    Path(path).write_text(json.dumps(rows, indent=2, default=str),
                          encoding="utf-8")
'''

_P4_PIPELINE = '''"""Composable pipeline stages."""
from __future__ import annotations

import copy
from collections.abc import Callable


class Pipeline:
    def __init__(self, stages: list[Callable]) -> None:
        self.stages = list(stages)

    def run(self, rows: list[dict]) -> list[dict]:
        """Apply stages in order. Pure — input rows are NEVER mutated."""
        cur = copy.deepcopy(rows)
        for stage in self.stages:
            cur = stage(cur)
        return cur
'''

_P4_CLI = '''"""pipeflow CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv=None):
    p = argparse.ArgumentParser(prog="pipeflow", description="ETL pipeline.")
    p.add_argument("--in", dest="input", required=True)
    p.add_argument("--out", dest="output", required=True)
    p.add_argument("--format", choices=["csv", "json"], default="csv")
    p.parse_args(argv)
    return 0
'''

_P4_TEST_SCHEMA = '''import pytest

from pipeflow.schema import ColumnSpec, coerce_cell, validate


def test_coerce_int():
    assert coerce_cell("42", int) == 42
    assert coerce_cell("0", int) == 0


def test_coerce_float():
    assert coerce_cell("3.14", float) == 3.14


def test_coerce_str():
    assert coerce_cell(42, str) == "42"


def test_coerce_empty_to_none():
    assert coerce_cell("", int) is None
    assert coerce_cell(None, int) is None


def test_validate_missing_required():
    schema = [ColumnSpec("a", int, required=True)]
    _, errs = validate([{"a": ""}], schema)
    assert len(errs) == 1 and errs[0]["reason"] == "missing"


def test_validate_bad_type():
    schema = [ColumnSpec("a", int, required=True)]
    _, errs = validate([{"a": "notanint"}], schema)
    assert errs and errs[0]["reason"] == "bad_type"


def test_validate_optional_missing_ok():
    schema = [ColumnSpec("a", int, required=False)]
    ok, errs = validate([{"a": ""}], schema)
    assert ok == [{"a": ""}] and errs == []
'''

_P4_TEST_SOURCES = '''from pathlib import Path

from pipeflow.schema import ColumnSpec
from pipeflow.sources import read_csv


def _write(p, text):
    p.write_text(text, encoding="utf-8")


def test_read_csv_basic(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x,y\\n1,2\\n3,4\\n")
    rows, _ = read_csv(f)
    assert rows == [{"x": "1", "y": "2"}, {"x": "3", "y": "4"}]


def test_read_csv_skips_blank_rows(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x,y\\n1,2\\n,\\n3,4\\n")
    rows, _ = read_csv(f)
    assert len(rows) == 2


def test_read_csv_with_schema(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x,y\\n1,2.5\\n")
    schema = [ColumnSpec("x", int), ColumnSpec("y", float)]
    rows, _ = read_csv(f, schema)
    assert rows == [{"x": 1, "y": 2.5}]


def test_read_csv_bad_cell_recorded(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x\\nnotanint\\n")
    schema = [ColumnSpec("x", int)]
    rows, errs = read_csv(f, schema)
    assert rows == [] and len(errs) == 1
    assert errs[0]["reason"] == "bad_type"


def test_read_csv_missing_required(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x,y\\n1,\\n")
    schema = [ColumnSpec("x", int), ColumnSpec("y", int)]
    rows, errs = read_csv(f, schema)
    assert rows == [] and errs[0]["reason"] == "missing"


def test_read_csv_does_not_zero_bad(tmp_path):
    """Bad cell must go to errors, not be silently coerced to 0."""
    f = tmp_path / "a.csv"
    _write(f, "x\\nbad\\n")
    schema = [ColumnSpec("x", int)]
    rows, _ = read_csv(f, schema)
    assert rows == []  # row dropped, NOT inserted as {"x": 0}


def test_read_csv_empty(tmp_path):
    f = tmp_path / "a.csv"
    _write(f, "x,y\\n")
    rows, errs = read_csv(f)
    assert rows == [] and errs == []
'''

_P4_TEST_TRANSFORMS = '''from pipeflow.transforms import (
    dedupe, derive, filter_rows, rename, select,
)


def test_select():
    rows = [{"a": 1, "b": 2, "c": 3}]
    assert select(rows, ["a", "c"]) == [{"a": 1, "c": 3}]


def test_rename():
    rows = [{"old": 1}]
    assert rename(rows, {"old": "new"}) == [{"new": 1}]


def test_derive():
    rows = [{"x": 1}, {"x": 2}]
    out = derive(rows, "y", lambda r: r["x"] * 10)
    assert [r["y"] for r in out] == [10, 20]


def test_filter_rows():
    rows = [{"x": 1}, {"x": 2}, {"x": 3}]
    out = filter_rows(rows, lambda r: r["x"] > 1)
    assert [r["x"] for r in out] == [2, 3]


def test_transforms_dedupe_keep_first():
    rows = [
        {"id": 1, "v": "a"},
        {"id": 2, "v": "b"},
        {"id": 1, "v": "c"},  # dup id=1
        {"id": 3, "v": "d"},
    ]
    out = dedupe(rows, key="id", keep="first")
    # FIRST occurrence kept → v=="a" for id=1
    by_id = {r["id"]: r["v"] for r in out}
    assert by_id[1] == "a"
    assert sorted(by_id) == [1, 2, 3]


def test_dedupe_keep_last():
    rows = [{"id": 1, "v": "a"}, {"id": 1, "v": "b"}]
    out = dedupe(rows, key="id", keep="last")
    assert out[0]["v"] == "b"


def test_filter_rows_empty():
    assert filter_rows([], lambda r: True) == []


def test_select_missing_col():
    rows = [{"a": 1}]
    assert select(rows, ["b"]) == [{"b": None}]
'''

_P4_TEST_AGGREGATE = '''from pipeflow.aggregate import count, group_by, max_, mean, min_, sum_


def test_sum_ignores_none():
    assert sum_([1, None, 2]) == 3


def test_aggregate_mean_with_nulls():
    """mean ignores None in the DENOMINATOR — average of present values only."""
    assert mean([10, None, 20]) == 15  # mean of [10, 20], not 30/3


def test_mean_empty_returns_none():
    assert mean([]) is None
    assert mean([None, None]) is None


def test_count_ignores_none():
    assert count([1, None, 2, None]) == 2


def test_min_max():
    assert min_([3, 1, 2]) == 1
    assert max_([3, 1, 2]) == 3


def test_group_by_sum():
    rows = [
        {"region": "N", "qty": 10},
        {"region": "S", "qty": 5},
        {"region": "N", "qty": 7},
    ]
    out = group_by(rows, "region", {"qty": {"fn": "sum", "as": "total"}})
    by_region = {r["region"]: r["total"] for r in out}
    assert by_region == {"N": 17, "S": 5}


def test_group_by_mean():
    rows = [
        {"k": "A", "v": 10},
        {"k": "A", "v": 20},
        {"k": "B", "v": 5},
    ]
    out = group_by(rows, "k", {"v": {"fn": "mean", "as": "avg"}})
    by_k = {r["k"]: r["avg"] for r in out}
    assert by_k["A"] == 15 and by_k["B"] == 5


def test_group_by_count():
    rows = [{"k": "A"}, {"k": "A"}, {"k": "B"}]
    out = group_by(rows, "k", {"k": {"fn": "count", "as": "n"}})
    by_k = {r["k"]: r["n"] for r in out}
    assert by_k["A"] == 2 and by_k["B"] == 1
'''

_P4_TEST_PIPELINE = '''import copy

from pipeflow.aggregate import group_by
from pipeflow.pipeline import Pipeline
from pipeflow.transforms import dedupe, filter_rows


def test_pipeline_basic():
    rows = [{"x": 1}, {"x": 2}, {"x": 3}]
    p = Pipeline([lambda rs: filter_rows(rs, lambda r: r["x"] > 1)])
    out = p.run(rows)
    assert [r["x"] for r in out] == [2, 3]


def test_pipeline_run_is_pure():
    """Pipeline.run must not mutate input rows."""
    rows = [{"x": 1}, {"x": 2}]
    before = copy.deepcopy(rows)
    Pipeline([lambda rs: filter_rows(rs, lambda r: True)]).run(rows)
    assert rows == before


def test_pipeline_dedupe():
    rows = [{"id": 1, "v": "a"}, {"id": 1, "v": "b"}, {"id": 2, "v": "c"}]
    out = Pipeline([lambda rs: dedupe(rs, "id", keep="first")]).run(rows)
    # first kept → v=="a"
    by_id = {r["id"]: r["v"] for r in out}
    assert by_id[1] == "a"


def test_pipeline_revenue_report():
    """End-to-end: rows with revenue + null cells, group by region, mean works."""
    rows = [
        {"region": "N", "revenue": 100},
        {"region": "N", "revenue": None},
        {"region": "N", "revenue": 200},
        {"region": "S", "revenue": 50},
    ]
    out = Pipeline([
        lambda rs: group_by(rs, "region", {"revenue": {"fn": "mean", "as": "avg"}})
    ]).run(rows)
    by_r = {r["region"]: r["avg"] for r in out}
    # N: mean of [100, 200] = 150 (NOT 300/3 = 100)
    assert by_r["N"] == 150
    assert by_r["S"] == 50
'''


def _p4_sample_sales_csv() -> str:
    """40-row CSV with 1 blank row, 1 dup id, 1 bad units."""
    rows = ["region,product,units,revenue,date"]
    for i in range(15):
        rows.append(f"N,P{i:02d},{i+1},{(i+1)*100}.00,2025-01-{(i%28)+1:02d}")
    rows.append("")  # blank row
    for i in range(15):
        rows.append(f"S,P{i:02d},{i+2},{(i+2)*120}.00,2025-02-{(i%28)+1:02d}")
    rows.append("E,Px,not_a_number,42.00,2025-03-01")  # bad units
    rows.append("N,P00,1,100.00,2025-01-01")  # duplicate of first
    for i in range(5):
        rows.append(f"W,Q{i:02d},{i*3+1},{(i*3+1)*50}.00,2025-04-{(i%28)+1:02d}")
    return "\n".join(rows) + "\n"


_P4_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_P4_README = '''# pipeflow

Compose CSV/JSON → validate → transform → aggregate → sink pipelines.
'''

_P4_FILES: dict[str, str] = {
    "pipeflow/__init__.py": _P4_INIT,
    "pipeflow/__main__.py": _P4_MAIN,
    "pipeflow/cli.py": _P4_CLI,
    "pipeflow/sources.py": _P4_SOURCES,
    "pipeflow/schema.py": _P4_SCHEMA,
    "pipeflow/transforms.py": _P4_TRANSFORMS,
    "pipeflow/aggregate.py": _P4_AGGREGATE,
    "pipeflow/sinks.py": _P4_SINKS,
    "pipeflow/pipeline.py": _P4_PIPELINE,
    "tests/test_schema.py": _P4_TEST_SCHEMA,
    "tests/test_sources.py": _P4_TEST_SOURCES,
    "tests/test_transforms.py": _P4_TEST_TRANSFORMS,
    "tests/test_aggregate.py": _P4_TEST_AGGREGATE,
    "tests/test_pipeline.py": _P4_TEST_PIPELINE,
    "pytest.ini": _P4_PYTEST_INI,
    "README.md": _P4_README,
}


def seed_pipeflow(cwd: Path, variant: str = "clean") -> None:
    """Seed pipeflow. Variants:
      - 'clean'        — 33 tests green
      - 'bug-mean'     — aggregate.mean uses len(rows) incl None  (2 red)
      - 'bug-dedupe'   — dedupe keep='first' actually keeps last  (2 red)
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _P4_FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    data = cwd / "data"
    data.mkdir(exist_ok=True)
    (data / "sales.csv").write_text(_p4_sample_sales_csv(), encoding="utf-8")

    if variant == "bug-mean":
        p = cwd / "pipeflow" / "aggregate.py"
        t = p.read_text()
        t = t.replace(
            "def mean(vals):\n    p = _present(vals)\n    if not p:\n        return None\n    return sum(p) / len(p)",
            "def mean(vals):\n    # BUG: divides by total len incl None\n    p = _present(vals)\n    if not p:\n        return None\n    return sum(p) / len(vals)",
        )
        p.write_text(t)

    elif variant == "bug-dedupe":
        p = cwd / "pipeflow" / "transforms.py"
        t = p.read_text()
        # Swap the keep="first" branch so it keeps LAST always
        t = t.replace(
            'if keep == "first":\n        for r in rows:\n            k = r.get(key)\n            if k not in seen:\n                seen[k] = r',
            'if keep == "first":\n        # BUG: actually keeps last\n        for r in rows:\n            k = r.get(key)\n            seen[k] = r',
        )
        p.write_text(t)


# ────────────────────────────────────────────────────────────────────────
# P5 — keystore : in-memory + disk KV store (TTL, LRU, thread-safe)
# ────────────────────────────────────────────────────────────────────────

_P5_INIT = '''"""keystore — KV store with TTL, LRU eviction, thread-safe."""
from keystore.store import KeyStore

__all__ = ["KeyStore"]
__version__ = "0.1.0"
'''

_P5_CLOCK = '''"""Injectable clock — RealClock + FakeClock for deterministic tests."""
from __future__ import annotations

import time


class RealClock:
    def now(self) -> float:
        return time.monotonic()


class FakeClock:
    def __init__(self, t: float = 0.0) -> None:
        self._t = t

    def now(self) -> float:
        return self._t

    def advance(self, dt: float) -> None:
        self._t += dt
'''

_P5_LOCKING = '''"""Minimal RW lock-ish guard. We use a single RLock for simplicity."""
from __future__ import annotations

import functools
import threading


def make_guard() -> threading.RLock:
    return threading.RLock()


def guarded(fn):
    @functools.wraps(fn)
    def wrapper(self, *a, **kw):
        with self._lock:
            return fn(self, *a, **kw)
    return wrapper
'''

_P5_BACKEND_MEMORY = '''"""In-memory dict backend."""
from __future__ import annotations


class MemoryBackend:
    def __init__(self) -> None:
        self._data: dict = {}

    def get(self, k):
        return self._data.get(k)

    def set(self, k, v) -> None:
        self._data[k] = v

    def delete(self, k) -> bool:
        return self._data.pop(k, None) is not None

    def keys(self) -> list:
        return list(self._data.keys())

    def __contains__(self, k) -> bool:
        return k in self._data

    def __len__(self) -> int:
        return len(self._data)
'''

_P5_BACKEND_DISK = '''"""Append-only disk log with compact()."""
from __future__ import annotations

import json
from pathlib import Path


class DiskBackend:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def _read_all(self) -> list[dict]:
        if not self.path.is_file():
            return []
        out = []
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
        return out

    def state(self) -> dict:
        """Replay the log to get the current logical state (latest wins)."""
        state: dict = {}
        for rec in self._read_all():
            op = rec.get("op")
            k = rec.get("k")
            if op == "set":
                state[k] = rec.get("v")
            elif op == "del" and k in state:
                del state[k]
        return state

    def get(self, k):
        return self.state().get(k)

    def set(self, k, v) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"op": "set", "k": k, "v": v}) + "\\n")

    def delete(self, k) -> bool:
        if k in self.state():
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"op": "del", "k": k}) + "\\n")
            return True
        return False

    def keys(self) -> list:
        return list(self.state().keys())

    def compact(self) -> None:
        """Rewrite the log keeping only the LATEST record per key."""
        state = self.state()
        with self.path.open("w", encoding="utf-8") as f:
            for k, v in state.items():
                f.write(json.dumps({"op": "set", "k": k, "v": v}) + "\\n")
'''

_P5_EVICTION = '''"""LRU eviction policy."""
from __future__ import annotations

from collections import OrderedDict


class LRUPolicy:
    def __init__(self) -> None:
        # ordered: oldest first, newest last
        self._order: OrderedDict = OrderedDict()

    def note_access(self, key) -> None:
        # move-to-end (key becomes most-recently-used)
        if key in self._order:
            self._order.move_to_end(key)
        else:
            self._order[key] = None

    def evict_candidate(self):
        """Return the least-recently-used key (oldest), or None."""
        if not self._order:
            return None
        # least-recently-used = FIRST in insertion order
        k = next(iter(self._order))
        return k

    def forget(self, key) -> None:
        self._order.pop(key, None)
'''

_P5_STORE = '''"""KeyStore: KV with TTL + LRU + backend abstraction."""
from __future__ import annotations

from keystore.backend_memory import MemoryBackend
from keystore.clock import RealClock
from keystore.eviction import LRUPolicy
from keystore.locking import guarded, make_guard


class KeyStore:
    def __init__(
        self,
        max_size: int = 1024,
        ttl: float | None = None,
        clock=None,
        backend=None,
    ) -> None:
        self.max_size = max_size
        self.ttl = ttl
        self.clock = clock or RealClock()
        self.backend = backend or MemoryBackend()
        self.policy = LRUPolicy()
        self._set_times: dict = {}
        self._lock = make_guard()

    def _is_expired(self, key) -> bool:
        if self.ttl is None or key not in self._set_times:
            return False
        return self.clock.now() - self._set_times[key] >= self.ttl

    @guarded
    def get(self, key):
        if key not in self.backend:
            return None
        if self._is_expired(key):
            self.backend.delete(key)
            self.policy.forget(key)
            self._set_times.pop(key, None)
            return None
        self.policy.note_access(key)
        return self.backend.get(key)

    @guarded
    def set(self, key, value) -> None:
        if key not in self.backend and len(self.backend) >= self.max_size:
            victim = self.policy.evict_candidate()
            if victim is not None:
                self.backend.delete(victim)
                self.policy.forget(victim)
                self._set_times.pop(victim, None)
        self.backend.set(key, value)
        self._set_times[key] = self.clock.now()
        self.policy.note_access(key)

    @guarded
    def delete(self, key) -> bool:
        self.policy.forget(key)
        self._set_times.pop(key, None)
        return self.backend.delete(key)

    @guarded
    def keys(self) -> list:
        return [k for k in self.backend.keys() if not self._is_expired(k)]

    def __len__(self) -> int:
        return len(self.keys())
'''

_P5_TEST_BASIC = '''from keystore.store import KeyStore


def test_set_get():
    s = KeyStore()
    s.set("a", 1)
    assert s.get("a") == 1


def test_get_missing_returns_none():
    s = KeyStore()
    assert s.get("nope") is None


def test_delete():
    s = KeyStore()
    s.set("a", 1)
    assert s.delete("a") is True
    assert s.get("a") is None


def test_delete_missing():
    s = KeyStore()
    assert s.delete("nope") is False


def test_keys_lists_alive():
    s = KeyStore()
    s.set("a", 1); s.set("b", 2)
    assert set(s.keys()) == {"a", "b"}


def test_overwrite():
    s = KeyStore()
    s.set("a", 1)
    s.set("a", 99)
    assert s.get("a") == 99


def test_len():
    s = KeyStore()
    s.set("a", 1); s.set("b", 2)
    assert len(s) == 2
'''

_P5_TEST_TTL = '''from keystore.clock import FakeClock
from keystore.store import KeyStore


def _store(ttl=10.0):
    c = FakeClock(0.0)
    return KeyStore(ttl=ttl, clock=c), c


def test_ttl_alive_before_expiry():
    s, c = _store(10.0)
    s.set("a", 1)
    c.advance(5)
    assert s.get("a") == 1


def test_ttl_expired_returns_none():
    s, c = _store(10.0)
    s.set("a", 1)
    c.advance(11)
    assert s.get("a") is None


def test_ttl_expired_purges_key():
    s, c = _store(10.0)
    s.set("a", 1)
    c.advance(11)
    s.get("a")  # triggers purge
    assert s.get("a") is None
    assert "a" not in s.keys()


def test_ttl_exact_boundary():
    """At exactly TTL, the key is expired (uses >=)."""
    s, c = _store(10.0)
    s.set("a", 1)
    c.advance(10.0)
    assert s.get("a") is None


def test_ttl_none_means_no_expiry():
    s, c = _store(ttl=None)
    s.set("a", 1)
    c.advance(1_000_000)
    assert s.get("a") == 1


def test_ttl_set_refreshes_time():
    s, c = _store(10.0)
    s.set("a", 1)
    c.advance(8)
    s.set("a", 2)
    c.advance(5)
    assert s.get("a") == 2  # 5s after second set, still alive
'''

_P5_TEST_EVICTION = '''from keystore.eviction import LRUPolicy


def test_eviction_lru_order():
    p = LRUPolicy()
    for k in ["a", "b", "c"]:
        p.note_access(k)
    assert p.evict_candidate() == "a"


def test_eviction_access_promotes_to_recent():
    p = LRUPolicy()
    for k in ["a", "b", "c"]:
        p.note_access(k)
    p.note_access("a")  # a is now newest
    assert p.evict_candidate() == "b"


def test_eviction_evicts_oldest():
    p = LRUPolicy()
    for k in ["x", "y", "z"]:
        p.note_access(k)
    assert p.evict_candidate() == "x"


def test_eviction_keep_hot():
    p = LRUPolicy()
    p.note_access("hot")
    for _ in range(10):
        p.note_access("hot")
    p.note_access("cold")
    p.note_access("cold")
    # cold accessed after hot's last access → hot is older
    # Actually: last access of hot was BEFORE both cold accesses.
    # Order in OrderedDict: hot (oldest), cold (newest). Evict hot.
    # Recheck spec — "keep hot" suggests hot should NOT be evicted.
    # Adjust: access hot AGAIN to make it newest.
    p.note_access("hot")
    p.note_access("medium")
    # Now order: cold, hot, medium → evict cold (oldest)
    assert p.evict_candidate() == "cold"


def test_eviction_empty_returns_none():
    p = LRUPolicy()
    assert p.evict_candidate() is None


def test_eviction_forget():
    p = LRUPolicy()
    p.note_access("a")
    p.forget("a")
    assert p.evict_candidate() is None


def test_max_size_evicts_in_store():
    from keystore.store import KeyStore
    s = KeyStore(max_size=2)
    s.set("a", 1)
    s.set("b", 2)
    s.set("c", 3)  # evicts a
    assert s.get("a") is None
    assert s.get("b") == 2
    assert s.get("c") == 3
'''

_P5_TEST_DISK = '''from keystore.backend_disk import DiskBackend


def test_disk_set_get(tmp_path):
    b = DiskBackend(tmp_path / "k.log")
    b.set("a", 1)
    assert b.get("a") == 1


def test_disk_overwrite(tmp_path):
    b = DiskBackend(tmp_path / "k.log")
    b.set("a", 1)
    b.set("a", 99)
    assert b.get("a") == 99


def test_disk_delete(tmp_path):
    b = DiskBackend(tmp_path / "k.log")
    b.set("a", 1)
    assert b.delete("a") is True
    assert b.get("a") is None


def test_disk_reload(tmp_path):
    log = tmp_path / "k.log"
    DiskBackend(log).set("x", 5)
    DiskBackend(log).set("y", 7)
    b3 = DiskBackend(log)
    assert b3.get("x") == 5 and b3.get("y") == 7


def test_disk_compact_keeps_latest(tmp_path):
    log = tmp_path / "k.log"
    b = DiskBackend(log)
    b.set("a", 1)
    b.set("a", 2)
    b.set("a", 3)
    pre = log.read_text().count("\\n")
    b.compact()
    post = log.read_text().count("\\n")
    assert post < pre
    assert b.get("a") == 3


def test_disk_reload_after_compact(tmp_path):
    log = tmp_path / "k.log"
    b = DiskBackend(log)
    b.set("a", 1); b.set("a", 2)
    b.set("b", 3); b.set("b", 4)
    b.compact()
    b2 = DiskBackend(log)
    assert b2.get("a") == 2 and b2.get("b") == 4


def test_disk_compact_drops_deleted(tmp_path):
    log = tmp_path / "k.log"
    b = DiskBackend(log)
    b.set("a", 1); b.delete("a")
    b.compact()
    b2 = DiskBackend(log)
    assert b2.get("a") is None
'''

_P5_TEST_CONCURRENCY = '''import threading

from keystore.store import KeyStore


def test_concurrent_sets_no_lost_updates():
    s = KeyStore(max_size=10_000)
    N = 8
    M = 100
    barrier = threading.Barrier(N)
    def worker(tid):
        barrier.wait()
        for i in range(M):
            s.set(f"t{tid}-k{i}", i)
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(s.keys()) == N * M


def test_concurrent_get_set_no_crashes():
    s = KeyStore()
    s.set("k", 0)
    def writer():
        for i in range(200):
            s.set("k", i)
    def reader():
        for _ in range(200):
            s.get("k")
    threads = [threading.Thread(target=writer) for _ in range(2)] + \\
              [threading.Thread(target=reader) for _ in range(2)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert s.get("k") is not None


def test_concurrent_delete():
    s = KeyStore()
    for i in range(100):
        s.set(f"k{i}", i)
    barrier = threading.Barrier(4)
    def deleter(start, end):
        barrier.wait()
        for i in range(start, end):
            s.delete(f"k{i}")
    threads = [
        threading.Thread(target=deleter, args=(0, 25)),
        threading.Thread(target=deleter, args=(25, 50)),
        threading.Thread(target=deleter, args=(50, 75)),
        threading.Thread(target=deleter, args=(75, 100)),
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(s) == 0
'''

_P5_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_P5_README = "# keystore\n\nKV store with TTL, LRU eviction, thread-safety, disk persistence.\n"

_P5_FILES: dict[str, str] = {
    "keystore/__init__.py": _P5_INIT,
    "keystore/clock.py": _P5_CLOCK,
    "keystore/locking.py": _P5_LOCKING,
    "keystore/backend_memory.py": _P5_BACKEND_MEMORY,
    "keystore/backend_disk.py": _P5_BACKEND_DISK,
    "keystore/eviction.py": _P5_EVICTION,
    "keystore/store.py": _P5_STORE,
    "tests/test_store_basic.py": _P5_TEST_BASIC,
    "tests/test_ttl.py": _P5_TEST_TTL,
    "tests/test_eviction.py": _P5_TEST_EVICTION,
    "tests/test_disk.py": _P5_TEST_DISK,
    "tests/test_concurrency.py": _P5_TEST_CONCURRENCY,
    "pytest.ini": _P5_PYTEST_INI,
    "README.md": _P5_README,
}


def seed_keystore(cwd: Path, variant: str = "clean") -> None:
    """Seed keystore. Variants:
      - 'clean'         — ~26 tests green
      - 'bug-lru'       — evict_candidate returns most-recently-used  (3 red)
      - 'bug-ttl'       — TTL uses > instead of >=  (1 red, looks flaky)
      - 'bug-compact'   — compact() keeps first record per key, not latest  (2 red)
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _P5_FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    if variant == "bug-lru":
        p = cwd / "keystore" / "eviction.py"
        t = p.read_text()
        t = t.replace(
            "k = next(iter(self._order))",
            "k = next(reversed(self._order))  # BUG: returns MOST-recent",
        )
        p.write_text(t)

    elif variant == "bug-ttl":
        p = cwd / "keystore" / "store.py"
        t = p.read_text()
        t = t.replace(
            "return self.clock.now() - self._set_times[key] >= self.ttl",
            "return self.clock.now() - self._set_times[key] > self.ttl",
        )
        p.write_text(t)

    elif variant == "bug-compact":
        p = cwd / "keystore" / "backend_disk.py"
        t = p.read_text()
        t = t.replace(
            "    def state(self) -> dict:\n        \"\"\"Replay the log to get the current logical state (latest wins).\"\"\"\n        state: dict = {}\n        for rec in self._read_all():\n            op = rec.get(\"op\")\n            k = rec.get(\"k\")\n            if op == \"set\":\n                state[k] = rec.get(\"v\")\n            elif op == \"del\" and k in state:\n                del state[k]\n        return state",
            "    def state(self) -> dict:\n        \"\"\"Replay log (latest wins) — used everywhere EXCEPT compact.\"\"\"\n        state: dict = {}\n        for rec in self._read_all():\n            op = rec.get(\"op\")\n            k = rec.get(\"k\")\n            if op == \"set\":\n                state[k] = rec.get(\"v\")\n            elif op == \"del\" and k in state:\n                del state[k]\n        return state",
        )
        # Now replace compact() to keep FIRST record per key
        t = t.replace(
            "    def compact(self) -> None:\n        \"\"\"Rewrite the log keeping only the LATEST record per key.\"\"\"\n        state = self.state()",
            "    def compact(self) -> None:\n        \"\"\"BUG: keeps FIRST record per key instead of latest.\"\"\"\n        state: dict = {}\n        for rec in self._read_all():\n            k = rec.get(\"k\")\n            if rec.get(\"op\") == \"set\" and k not in state:\n                state[k] = rec.get(\"v\")  # first wins, bug\n        # original (correct) state replaced",
        )
        p.write_text(t)


# ────────────────────────────────────────────────────────────────────────
# P6 — miniapi : stdlib HTTP service + static dashboard + SQLite
# ────────────────────────────────────────────────────────────────────────

_P6_INIT = '''"""miniapi — stdlib HTTP service + static dashboard."""
__version__ = "0.1.0"
'''

_P6_MAIN = '''import os
import sys

from miniapi.server import build_server

if __name__ == "__main__":
    port = int(os.environ.get("MINIAPI_PORT", "8077"))
    s = build_server(("", port))
    print(f"serving on :{port}", file=sys.stderr)
    s.serve_forever()
'''

_P6_DB = '''"""SQLite store for miniapi. Parameterized queries everywhere."""
from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path


_lock = threading.RLock()


def _conn(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def transaction(db_path):
    with _lock:
        conn = _conn(db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()


def init_schema(db_path) -> None:
    with transaction(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              qty INTEGER NOT NULL DEFAULT 0
            )
        """)


def list_items(db_path) -> list[dict]:
    with transaction(db_path) as conn:
        return [dict(r) for r in conn.execute(
            "SELECT id, name, qty FROM items ORDER BY id"
        )]


def get_item(db_path, item_id: int) -> dict | None:
    with transaction(db_path) as conn:
        row = conn.execute(
            "SELECT id, name, qty FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        return dict(row) if row else None


def add_item(db_path, name: str, qty: int) -> dict:
    with transaction(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO items (name, qty) VALUES (?, ?)", (name, qty)
        )
        rid = cur.lastrowid
    return {"id": rid, "name": name, "qty": qty}


def delete_item(db_path, item_id: int) -> bool:
    with transaction(db_path) as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        return cur.rowcount > 0
'''

_P6_VALIDATION = '''"""Payload validator."""
from __future__ import annotations


def validate_item(payload: dict) -> tuple[bool, list[str]]:
    errs: list[str] = []
    if not isinstance(payload, dict):
        return False, ["payload must be an object"]
    allowed = {"name", "qty"}
    extra = set(payload) - allowed
    if extra:
        errs.append(f"unexpected keys: {sorted(extra)}")
    if "name" not in payload:
        errs.append("name is required")
    elif not isinstance(payload["name"], str) or not payload["name"].strip():
        errs.append("name must be a non-empty string")
    if "qty" not in payload:
        errs.append("qty is required")
    else:
        q = payload["qty"]
        if not isinstance(q, int) or isinstance(q, bool):
            errs.append("qty must be an int")
        elif q < 0:
            errs.append("qty must be >= 0")
    return (not errs), errs
'''

_P6_AUTH = '''"""Token auth for POST/DELETE."""
from __future__ import annotations

import os


def require_token(headers) -> bool:
    expected = os.environ.get("MINIAPI_TOKEN", "")
    if not expected:
        return True  # no token configured → open
    provided = headers.get("X-Token", "") if hasattr(headers, "get") else ""
    return provided == expected
'''

_P6_ROUTES = '''"""Request routing for miniapi."""
from __future__ import annotations

import json
from http import HTTPStatus

from miniapi import auth, db, validation


def _json_response(handler, status: int, payload) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _parse_item_id(path: str) -> int | None:
    """Parse /items/{id} → int. Trailing slash returns None (bad)."""
    parts = path.rstrip("/").split("/")
    if len(parts) < 3:
        return None
    if path.endswith("/") and path != "/items/":
        return None
    last = parts[-1]
    if not last.isdigit():
        return None
    return int(last)


def handle(handler, db_path) -> None:
    path = handler.path
    method = handler.command

    if path == "/health" and method == "GET":
        return _json_response(handler, 200, {"ok": True})

    if path == "/items" and method == "GET":
        return _json_response(handler, 200, db.list_items(db_path))

    if path.startswith("/items/") and method == "GET":
        iid = _parse_item_id(path)
        if iid is None:
            return _json_response(handler, 400, {"error": "bad id"})
        row = db.get_item(db_path, iid)
        if row is None:
            return _json_response(handler, 404, {"error": "not found"})
        return _json_response(handler, 200, row)

    if path == "/items" and method == "POST":
        if not auth.require_token(handler.headers):
            return _json_response(handler, 401, {"error": "unauthorized"})
        length = int(handler.headers.get("Content-Length", 0))
        raw = handler.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except Exception:
            return _json_response(handler, 400, {"error": "bad json"})
        ok, errs = validation.validate_item(payload)
        if not ok:
            return _json_response(handler, 400, {"error": "validation", "details": errs})
        row = db.add_item(db_path, payload["name"], payload["qty"])
        return _json_response(handler, 201, row)

    if path.startswith("/items/") and method == "DELETE":
        if not auth.require_token(handler.headers):
            return _json_response(handler, 401, {"error": "unauthorized"})
        iid = _parse_item_id(path)
        if iid is None:
            return _json_response(handler, 400, {"error": "bad id"})
        deleted = db.delete_item(db_path, iid)
        if not deleted:
            return _json_response(handler, 404, {"error": "not found"})
        return _json_response(handler, 204, {})

    _json_response(handler, 404, {"error": "no route"})
'''

_P6_SERVER = '''"""HTTP server bootstrap."""
from __future__ import annotations

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from miniapi import db, routes


def _db_path() -> Path:
    return Path(os.environ.get("MINIAPI_DB",
                               str(Path.home() / ".miniapi" / "items.db")))


class Handler(BaseHTTPRequestHandler):
    def _dispatch(self):
        routes.handle(self, _db_path())

    def do_GET(self):
        self._dispatch()

    def do_POST(self):
        self._dispatch()

    def do_DELETE(self):
        self._dispatch()

    def log_message(self, *a, **kw):
        return  # quiet


def build_server(addr=("", 0)) -> ThreadingHTTPServer:
    db_path = _db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db.init_schema(db_path)
    return ThreadingHTTPServer(addr, Handler)
'''

_P6_HTML = '''<!DOCTYPE html>
<html><head><title>miniapi</title>
<link rel="stylesheet" href="style.css"></head>
<body>
<h1>miniapi items</h1>
<form id="add"><input id="name"><input id="qty" type="number"><button>add</button></form>
<ul id="items"></ul>
<div id="progress"></div>
<script src="app.js"></script></body></html>
'''

_P6_JS = '''async function refresh() {
  const r = await fetch('/items');
  const items = await r.json();
  const ul = document.getElementById('items');
  ul.innerHTML = '';
  items.forEach(i => { const li = document.createElement('li'); li.textContent = i.name + ' x' + i.qty; ul.appendChild(li); });
}
refresh();
'''

_P6_CSS = '''body { font-family: sans-serif; }
'''

_P6_TEST_VALIDATION = '''from miniapi.validation import validate_item


def test_valid_minimal():
    ok, errs = validate_item({"name": "x", "qty": 0})
    assert ok and errs == []


def test_missing_name():
    ok, errs = validate_item({"qty": 1})
    assert not ok and any("name" in e for e in errs)


def test_blank_name():
    ok, errs = validate_item({"name": "  ", "qty": 1})
    assert not ok


def test_negative_qty():
    ok, errs = validate_item({"name": "x", "qty": -1})
    assert not ok and any("qty" in e and ">=" in e for e in errs)


def test_qty_must_be_int():
    ok, _ = validate_item({"name": "x", "qty": "1"})
    assert not ok


def test_extra_keys_rejected():
    ok, errs = validate_item({"name": "x", "qty": 1, "bogus": 9})
    assert not ok and any("unexpected" in e for e in errs)
'''

_P6_TEST_DB = '''from miniapi import db


def test_init_schema_idempotent(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    db.init_schema(p)


def test_add_and_get(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    row = db.add_item(p, "a", 5)
    assert row["name"] == "a" and row["qty"] == 5
    assert db.get_item(p, row["id"]) == row


def test_list_items_order(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    db.add_item(p, "a", 1); db.add_item(p, "b", 2)
    items = db.list_items(p)
    assert [i["name"] for i in items] == ["a", "b"]


def test_get_missing_returns_none(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    assert db.get_item(p, 999) is None


def test_delete_item(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    r = db.add_item(p, "a", 1)
    assert db.delete_item(p, r["id"])
    assert db.get_item(p, r["id"]) is None


def test_delete_missing(tmp_path):
    p = tmp_path / "x.db"
    db.init_schema(p)
    assert not db.delete_item(p, 999)
'''

_P6_TEST_AUTH = '''import os

from miniapi.auth import require_token


class _Headers:
    def __init__(self, d): self._d = d
    def get(self, k, default=""): return self._d.get(k, default)


def test_open_when_no_token_configured(monkeypatch):
    monkeypatch.delenv("MINIAPI_TOKEN", raising=False)
    assert require_token(_Headers({})) is True


def test_rejects_missing_token(monkeypatch):
    monkeypatch.setenv("MINIAPI_TOKEN", "secret")
    assert require_token(_Headers({})) is False


def test_rejects_wrong_token(monkeypatch):
    monkeypatch.setenv("MINIAPI_TOKEN", "secret")
    assert require_token(_Headers({"X-Token": "wrong"})) is False


def test_accepts_correct_token(monkeypatch):
    monkeypatch.setenv("MINIAPI_TOKEN", "secret")
    assert require_token(_Headers({"X-Token": "secret"})) is True
'''

_P6_TEST_ROUTES = '''import json
import threading

import pytest

from miniapi import server


@pytest.fixture
def srv(tmp_path, monkeypatch):
    monkeypatch.setenv("MINIAPI_DB", str(tmp_path / "items.db"))
    monkeypatch.delenv("MINIAPI_TOKEN", raising=False)
    s = server.build_server(("127.0.0.1", 0))
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield s
    s.shutdown()
    s.server_close()
    t.join(timeout=2)


def _http_get(host, port, path):
    import http.client
    c = http.client.HTTPConnection(host, port, timeout=5)
    c.request("GET", path); r = c.getresponse()
    return r.status, r.read().decode()


def _http_post(host, port, path, body):
    import http.client
    c = http.client.HTTPConnection(host, port, timeout=5)
    c.request("POST", path, body=json.dumps(body).encode(),
              headers={"Content-Type": "application/json",
                       "Content-Length": str(len(json.dumps(body).encode()))})
    r = c.getresponse()
    return r.status, r.read().decode()


def _http_delete(host, port, path):
    import http.client
    c = http.client.HTTPConnection(host, port, timeout=5)
    c.request("DELETE", path); r = c.getresponse()
    return r.status, r.read().decode()


def test_health(srv):
    host, port = srv.server_address
    status, _ = _http_get(host, port, "/health")
    assert status == 200


def test_routes_list_empty(srv):
    host, port = srv.server_address
    status, body = _http_get(host, port, "/items")
    assert status == 200 and json.loads(body) == []


def test_routes_post_and_get(srv):
    host, port = srv.server_address
    status, body = _http_post(host, port, "/items", {"name": "a", "qty": 5})
    assert status == 201
    item = json.loads(body)
    status, body = _http_get(host, port, f"/items/{item['id']}")
    assert status == 200 and json.loads(body)["name"] == "a"


def test_routes_post_validates(srv):
    host, port = srv.server_address
    status, _ = _http_post(host, port, "/items", {"name": "x"})  # no qty
    assert status == 400


def test_routes_item_trailing_slash(srv):
    host, port = srv.server_address
    _, _ = _http_post(host, port, "/items", {"name": "a", "qty": 1})
    status, _ = _http_get(host, port, "/items/1/")
    assert status == 400


def test_routes_bad_id(srv):
    host, port = srv.server_address
    status, _ = _http_get(host, port, "/items/abc")
    assert status == 400


def test_routes_missing_404(srv):
    host, port = srv.server_address
    status, _ = _http_get(host, port, "/items/999")
    assert status == 404


def test_routes_delete(srv):
    host, port = srv.server_address
    status, body = _http_post(host, port, "/items", {"name": "a", "qty": 1})
    iid = json.loads(body)["id"]
    status, _ = _http_delete(host, port, f"/items/{iid}")
    assert status == 204
    status, _ = _http_get(host, port, f"/items/{iid}")
    assert status == 404
'''

_P6_TEST_E2E = '''import json
import threading
from pathlib import Path

import pytest

from miniapi import server


@pytest.fixture
def srv(tmp_path, monkeypatch):
    monkeypatch.setenv("MINIAPI_DB", str(tmp_path / "items.db"))
    monkeypatch.delenv("MINIAPI_TOKEN", raising=False)
    s = server.build_server(("127.0.0.1", 0))
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    yield s
    s.shutdown()
    s.server_close()
    t.join(timeout=2)


def test_e2e_lifecycle(srv):
    import http.client
    host, port = srv.server_address
    c = http.client.HTTPConnection(host, port, timeout=5)
    # add 3 items
    for n in range(3):
        body = json.dumps({"name": f"i{n}", "qty": n}).encode()
        c.request("POST", "/items", body=body,
                  headers={"Content-Type": "application/json",
                           "Content-Length": str(len(body))})
        c.getresponse().read()
    c.request("GET", "/items"); r = c.getresponse()
    items = json.loads(r.read())
    assert len(items) == 3


def test_e2e_static_files_referenced():
    """static/index.html should exist with an item-list element."""
    p = Path(__file__).parent.parent / "static" / "index.html"
    assert p.is_file()
    t = p.read_text()
    assert "items" in t.lower()
'''

_P6_PYTEST_INI = '''[pytest]
testpaths = tests
python_files = test_*.py
'''

_P6_README = "# miniapi\n\nstdlib HTTP service + static dashboard backed by sqlite.\n"

_P6_FILES: dict[str, str] = {
    "miniapi/__init__.py": _P6_INIT,
    "miniapi/__main__.py": _P6_MAIN,
    "miniapi/server.py": _P6_SERVER,
    "miniapi/routes.py": _P6_ROUTES,
    "miniapi/db.py": _P6_DB,
    "miniapi/validation.py": _P6_VALIDATION,
    "miniapi/auth.py": _P6_AUTH,
    "static/index.html": _P6_HTML,
    "static/app.js": _P6_JS,
    "static/style.css": _P6_CSS,
    "tests/test_validation.py": _P6_TEST_VALIDATION,
    "tests/test_db.py": _P6_TEST_DB,
    "tests/test_auth.py": _P6_TEST_AUTH,
    "tests/test_routes.py": _P6_TEST_ROUTES,
    "tests/test_e2e.py": _P6_TEST_E2E,
    "pytest.ini": _P6_PYTEST_INI,
    "README.md": _P6_README,
}


def seed_miniapi(cwd: Path, variant: str = "clean") -> None:
    """Seed miniapi. Variants:
      - 'clean'          — ~26 tests green
      - 'bug-pathparse'  — /items/{id} trailing-slash handled as 500 (2 red)
      - 'vuln-sqli'      — db.get_item uses f-string SQL (no test flips red)
    """
    cwd.mkdir(parents=True, exist_ok=True)
    for rel, content in _P6_FILES.items():
        p = cwd / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    if variant == "bug-pathparse":
        p = cwd / "miniapi" / "routes.py"
        t = p.read_text()
        # Replace the careful parser with a naive .split()[-1] that fails on trailing slash
        t = t.replace(
            'def _parse_item_id(path: str) -> int | None:\n    """Parse /items/{id} → int. Trailing slash returns None (bad)."""\n    parts = path.rstrip("/").split("/")\n    if len(parts) < 3:\n        return None\n    if path.endswith("/") and path != "/items/":\n        return None\n    last = parts[-1]\n    if not last.isdigit():\n        return None\n    return int(last)',
            'def _parse_item_id(path: str) -> int | None:\n    """BUG: trailing slash → empty string → ValueError 500 not 400."""\n    last = path.split("/")[-1]\n    return int(last)',
        )
        p.write_text(t)

    elif variant == "vuln-sqli":
        p = cwd / "miniapi" / "db.py"
        t = p.read_text()
        t = t.replace(
            'row = conn.execute(\n            "SELECT id, name, qty FROM items WHERE id = ?", (item_id,)\n        ).fetchone()',
            'row = conn.execute(\n            f"SELECT id, name, qty FROM items WHERE id = {item_id}"  # VULN: SQLi\n        ).fetchone()',
        )
        p.write_text(t)
