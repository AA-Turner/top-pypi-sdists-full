"""the local report ledger: consent gate, one-per-window dedupe stamps, kept 0600 copies, last sent."""

from __future__ import annotations

import contextlib
import json
import os
import time
import uuid
from collections.abc import Iterable, Mapping
from pathlib import Path
DEDUPE_WINDOW_S = 6 * 3600
KEEP_REPORTS = 5


# ---------------------------------------------------------------------------
# Consent and dedupe (automatic reports)
# ---------------------------------------------------------------------------


def disabled(env: Mapping[str, str]) -> str | None:
    """Why an automatic report may not be sent for this consenting environment."""
    from probe.analytics import report_policy

    return report_policy.staff_reports_disabled(env, base_url())


def _stamp_path(family: str, scope_key: str, at: float) -> Path:
    window = int(at // DEDUPE_WINDOW_S)
    tag = f"{family}-{scope_key}".replace(":", "~").replace("/", "_")
    return reports_dir() / "stamps" / f"report-{tag}-{window}.stamp"


def release(family: str, scope_key: str, *, now: float) -> None:
    """Give back the window `claim` took at `now`: its send did not land and a
    retry (the Probe service tries a report it did not land again) may. Never raises."""
    with contextlib.suppress(OSError):
        _stamp_path(family, scope_key, now).unlink()


def claim(family: str, scope_key: str, *, now: float | None = None) -> bool:
    """The one report of `family` for `scope_key` (a session or "machine") in
    this `DEDUPE_WINDOW_S` window, claimed atomically: True for the caller that
    created the window's stamp, False for every other."""
    at = time.time() if now is None else now
    window = int(at // DEDUPE_WINDOW_S)
    path = _stamp_path(family, scope_key, at)
    folder = path.parent
    folder.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return False
    os.close(fd)
    _prune_stamps(folder, window)
    return True


def _prune_stamps(folder: Path, window: int) -> None:
    for stamp in folder.glob("report-*.stamp"):
        try:
            if int(stamp.stem.rsplit("-", 1)[1]) < window - 1:
                stamp.unlink()
        except (ValueError, IndexError, OSError):
            continue


# ---------------------------------------------------------------------------
# Local copies
# ---------------------------------------------------------------------------


def _write_private(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def newest_first(paths: Iterable[Path]) -> list[Path]:
    """`paths`, the newest modified first (a tie: the later name first). One deleted since it was
    listed (an agent pruning its sessions, another report pruning its copies) is left out: it
    costs only itself, never the caller's whole listing."""
    dated = []
    for path in paths:
        try:
            dated.append((path.stat().st_mtime, path.name, path))
        except OSError:
            continue
    dated.sort(key=lambda row: row[:2], reverse=True)
    return [row[2] for row in dated]


def keep_copy(body: dict, outcome: dict, path: Path | None = None) -> Path:
    """Write (or rewrite) this report's local copy, 0600, and keep only the
    newest `KEEP_REPORTS`."""
    folder = reports_dir()
    if path is None:
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        unique = uuid.uuid4().hex[:8]  # two reports in one second keep two copies
        path = folder / f"report-{stamp}-{unique}-{body.get('family', 'report').replace(':', '~')}.json"
    _write_private(path, json.dumps({"at": int(time.time()), "outcome": outcome, "body": body}, indent=1,
                                    ensure_ascii=False) + "\n")
    copies = newest_first(folder.glob("report-*.json"))
    for old in copies[KEEP_REPORTS:]:
        with contextlib.suppress(OSError):
            old.unlink()
    return path


def last_sent() -> tuple[float, str] | None:
    """When the newest report that reached the Probe team was sent, and its id."""
    best: tuple[float, str] | None = None
    try:
        copies = list(reports_dir().glob("report-*.json"))
    except OSError:
        return None
    for path in copies:
        data = read_json(path)
        outcome = data.get("outcome") if isinstance(data, dict) else None
        if isinstance(outcome, dict) and outcome.get("id") and isinstance(data.get("at"), (int, float)):
            if best is None or data["at"] > best[0]:
                best = (float(data["at"]), str(outcome["id"]))
    return best
from probe.shared.reports.logs import read_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import base_url, reports_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
