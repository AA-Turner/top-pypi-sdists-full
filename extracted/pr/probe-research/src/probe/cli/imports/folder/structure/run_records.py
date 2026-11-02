"""read a run's record from its folder's files: run candidates, results, config, status."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from probe.foundation.compat.compat import StrEnum, tomllib
#: `metadata.backfill.schema` on those runs.
RUN_SCHEMA = "1"

#: Per run, so one result file with a thousand fields cannot become a
#: thousand-key summary. Kept in sorted key order; the count dropped is recorded.
MAX_METRICS = 200
MAX_CONFIG = 200
#: Files larger than this are not parsed (a result table is not a result file).
MAX_PARSE_BYTES = 5 * 1024 * 1024
MAX_CONFIG_TEXT = 1_000
#: Provenance kept on the run: which files the values were read from.
MAX_SOURCES = 50


class Ended(StrEnum):
    """The terminal statuses a read run can end in (the API's `RunStatus`)."""

    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    #: Nothing in the folder says how it ended. Never `completed`.
    UNKNOWN = "untracked"


# -- which files say what ------------------------------------------------------

_RESULT_JSON = re.compile(
    r"\A(reward|outcome|.*result.*|metrics.*|summary.*|eval.*)\.json\Z", re.I)
_LONE_NUMBER = re.compile(r"\A(reward|score)\.txt\Z", re.I)
_CONFIG = re.compile(
    r"\A(.*\.toml|config.*\.(json|ya?ml)|args.*\.json|h?params.*\.(json|ya?ml|toml))\Z", re.I)
#: Explicit status fields, in the order they are read.
STATUS_FIELDS = ("status", "outcome", "success", "passed", "exit_code")
_DONE = {"completed", "complete", "success", "succeeded", "successful", "passed", "pass",
         "ok", "done", "finished"}
_FAILED = {"failed", "failure", "fail", "error", "errored", "crashed", "timeout", "timed_out"}
_CANCELED = {"canceled", "cancelled", "aborted", "killed", "interrupted"}


def is_result_file(name: str) -> bool:
    return bool(_RESULT_JSON.match(name) or _LONE_NUMBER.match(name))


def is_config_file(name: str) -> bool:
    return bool(_CONFIG.match(name))


_MANIFEST = re.compile(r"\A.*manifest.*\.json\Z", re.I)
_LOG = re.compile(r"\A.*\.log\Z", re.I)


def run_candidates(paths) -> list[str]:
    """Folders that look like one run's output: a config or manifest AND a
    result file or a log, directly inside. A hint shown to the classifier,
    which keeps or drops each; code never makes a run from it. The import's
    root is never one (the whole folder is not a run by shape alone)."""
    seen: dict[str, set[str]] = {}
    for rel in paths:
        directory, _, name = rel.rpartition("/")
        if not directory:
            continue
        if is_config_file(name) or _MANIFEST.match(name):
            seen.setdefault(directory, set()).add("config")
        if is_result_file(name) or _LOG.match(name):
            seen.setdefault(directory, set()).add("output")
    return sorted(folder for folder, kinds in seen.items() if len(kinds) == 2)


@dataclass
class RunRecord:
    """Everything a run is created with, read from its folder."""

    name: str
    started_at: str | None
    ended_at: str | None
    status: Ended
    config: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    #: `metadata.backfill`: where it came from and which files said what.
    provenance: dict = field(default_factory=dict)
    #: metric key -> the ISO mtime of the file its value was read from: the
    #: point's `wall_clock` (`metric_points`). Not in the digest.
    clocks: dict = field(default_factory=dict)

    def digest(self) -> str:
        return hashlib.sha256(json.dumps(
            [self.name, self.started_at, self.ended_at, self.status.value,
             self.config, self.metrics, self.provenance],
            sort_keys=True, default=str).encode()).hexdigest()


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _number(value) -> float | int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _scalar(value):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value if (not isinstance(value, float) or math.isfinite(value)) else None
    if isinstance(value, str):
        return value[:MAX_CONFIG_TEXT]
    return _SKIP


_SKIP = object()


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_PARSE_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _json_object(path: Path) -> dict | None:
    text = _read_text(path)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except (ValueError, RecursionError):
        return None
    return data if isinstance(data, dict) else None


def _lone_number(path: Path) -> float | int | None:
    text = _read_text(path)
    if text is None:
        return None
    token = text.strip()
    if not token or len(token.split()) != 1:
        return None
    try:
        value = int(token)
    except ValueError:
        try:
            value = float(token)
        except ValueError:
            return None
    return _number(value)


_YAML_KEY = re.compile(r"\A([A-Za-z_][\w.-]*)\s*:\s*(.*?)\s*\Z")


def _yaml_top(text: str) -> dict:
    """Top-level `key: scalar` lines of a YAML file, and nothing else.

    No YAML library ships with the CLI, and the rule only wants top-level
    scalars, which are one line each. A nested block, a list, an anchor or a
    multi-line string is skipped rather than half-read.
    """
    out: dict = {}
    for line in text.splitlines():
        if not line or line[0] in " \t#-" or line.startswith("---"):
            continue
        match = _YAML_KEY.match(line)
        if not match:
            continue
        key, raw = match.groups()
        if raw[:1] in ("\"", "'"):
            # A quoted value ends at its closing quote; a ` #` inside it is text.
            close = raw.find(raw[0], 1)
            rest = raw[close + 1:].strip() if close > 0 else "?"
            if not rest or rest.startswith("#"):
                out[key] = raw[1:close]
            continue
        raw = re.split(r"(?:^|\s)#", raw, maxsplit=1)[0].strip()
        if not raw or raw[0] in "[{|>&*!":
            continue
        lowered = raw.lower()
        if lowered in ("true", "false"):
            out[key] = lowered == "true"
        elif lowered in ("null", "~"):
            out[key] = None
        else:
            try:
                out[key] = int(raw)
            except ValueError:
                try:
                    value = float(raw)
                    out[key] = value if math.isfinite(value) else raw
                except ValueError:
                    out[key] = raw
    return out


def _config_values(path: Path) -> dict | None:
    name = path.name.lower()
    text = _read_text(path)
    if text is None:
        return None
    if name.endswith(".toml"):
        try:
            data = tomllib.loads(text)
        except (tomllib.TOMLDecodeError, ValueError, RecursionError):
            return None
    elif name.endswith(".json"):
        try:
            data = json.loads(text)
        except (ValueError, RecursionError):
            return None
        if not isinstance(data, dict):
            return None
    else:
        data = _yaml_top(text)
    out = {}
    for key, value in data.items():
        scalar = _scalar(value)
        if scalar is not _SKIP:
            out[str(key)] = scalar
    return out


def _status_of(values: list) -> Ended | None:
    """One explicit field's verdict, or None when it says nothing usable."""
    is_found: set[Ended] = set()
    for field_name, value in values:
        verdict = None
        if field_name in ("success", "passed"):
            if isinstance(value, bool):
                verdict = Ended.COMPLETED if value else Ended.FAILED
        elif field_name == "exit_code":
            if isinstance(value, int) and not isinstance(value, bool):
                verdict = Ended.COMPLETED if value == 0 else Ended.FAILED
        elif isinstance(value, str):
            word = value.strip().lower()
            verdict = (Ended.COMPLETED if word in _DONE else Ended.FAILED if word in _FAILED
                       else Ended.CANCELED if word in _CANCELED else None)
        if verdict is not None:
            is_found.add(verdict)
    # Two fields that disagree say nothing certain: no status is claimed.
    return is_found.pop() if len(is_found) == 1 else None


def _keyed(entries: list[tuple[str, str, str, object]]) -> dict:
    """`(directory, file, field, value)` -> `{key: value}`, keys traceable.

    `field` at the run's top level, `<dir>/field` below it. Two files that
    would give one key both get their file's name instead, so no number
    silently replaces another.
    """
    by_key: dict[str, list] = {}
    for directory, filename, name, value in entries:
        key = f"{directory}/{name}" if directory else name
        by_key.setdefault(key, []).append((directory, filename, name, value))
    out: dict = {}
    for key, rows in by_key.items():
        if len(rows) == 1:
            out[key] = rows[0][3]
            continue
        for directory, filename, name, value in rows:
            qualified = f"{directory}/{filename}" if directory else filename
            out[qualified if filename.rsplit(".", 1)[0] == name else f"{qualified}:{name}"] = value
    return out


def read_run(root: Path, under: str, files: list[str], *, times: bool = True) -> RunRecord:
    """A run's record from the files of its folder (paths relative to `root`).

    `files` are the files the import holds for the run (left-out ones are not
    among them). Times are their mtimes; config and metrics are read from the
    file kinds named in the module docs, at any depth, keyed by where they sit.
    The status is read only from files directly in the run's folder: a trial's
    outcome three levels down is that trial's, not the run's. With `times`
    False (the folder was copied, so every mtime is the copy's) no time is
    claimed.
    """
    mtimes: list[float] = []
    metric_rows: list = []
    config_rows: list = []
    status_fields: list = []
    sources = {"metrics": [], "config": [], "status": []}
    prefix = under + "/" if under else ""
    for rel in sorted(files):
        path = root / rel
        try:
            mtimes.append(path.stat().st_mtime)
        except OSError:
            continue
        inner = rel[len(prefix):] if rel.startswith(prefix) else rel
        directory, _, filename = inner.rpartition("/")
        if _LONE_NUMBER.match(filename):
            value = _lone_number(path)
            if value is not None:
                metric_rows.append((directory, filename, filename.rsplit(".", 1)[0],
                                    (value, mtimes[-1])))
                sources["metrics"].append(rel)
        elif _RESULT_JSON.match(filename):
            data = _json_object(path)
            if data is not None:
                is_found = False
                for key, value in data.items():
                    number = _number(value)
                    if number is not None and str(key) not in ("exit_code",):
                        metric_rows.append((directory, filename, str(key), (number, mtimes[-1])))
                        is_found = True
                if not directory:
                    picked = [(f, data[f]) for f in STATUS_FIELDS if f in data]
                    if picked:
                        status_fields.extend(picked)
                        sources["status"].append(rel)
                if is_found:
                    sources["metrics"].append(rel)
        if _CONFIG.match(filename):
            values = _config_values(path)
            if values:
                for key, value in values.items():
                    config_rows.append((directory, filename, key, value))
                sources["config"].append(rel)
    timed = _keyed(metric_rows)
    config = _keyed(config_rows)
    dropped = {}
    if len(timed) > MAX_METRICS:
        dropped["metrics"] = len(timed) - MAX_METRICS
        timed = dict(sorted(timed.items())[:MAX_METRICS])
    metrics = {key: value for key, (value, _) in timed.items()}
    clocks = {key: _iso(stamp) for key, (_, stamp) in timed.items()}
    if len(config) > MAX_CONFIG:
        dropped["config"] = len(config) - MAX_CONFIG
        config = dict(sorted(config.items())[:MAX_CONFIG])
    status = _status_of(status_fields) or Ended.UNKNOWN
    provenance = {
        "schema": RUN_SCHEMA,
        "relative_path": under,
        "files": len(files),
        # Unknown when every file of the import was written inside one window,
        # as a copy leaves them (`Evidence.mtime_uninformative`): a copy's time
        # is not the run's.
        "times": "file mtimes" if times else "unknown: every file has one copy-like mtime",
        "read_from": {k: v[:MAX_SOURCES] for k, v in sources.items() if v},
    }
    if dropped:
        provenance["dropped"] = dropped
    return RunRecord(
        name=(under.rsplit("/", 1)[-1] or "run")[:200],
        started_at=_iso(min(mtimes)) if mtimes and times else None,
        ended_at=_iso(max(mtimes)) if mtimes and times else None,
        status=status, config=config, metrics=metrics, provenance=provenance, clocks=clocks,
    )
