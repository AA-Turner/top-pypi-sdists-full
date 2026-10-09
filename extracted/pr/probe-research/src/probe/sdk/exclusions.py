"""`.probe.config` as this process sees it.

`probe_config` is the stdlib matcher every surface carries; this is the SDK and
CLI side of it: which agent session this process belongs to (its environment),
where that session started, and whether the researcher set the files above
that folder aside for it (`probe session parent ignore`). Every answer here is
session-aware and never raises.

The capture paths (code, outputs, reads) ask on every file they walk and every
read they record, so they pass `hot=True`: the session view and each folder's
stat may be up to `HOT_TTL_S` old there. So do `--from-manifest` rows (one
command, many rows). Other refusals (`probe` CLI writes, `probe.init()`,
`log_artifact`) read fresh.
"""

from __future__ import annotations

import os
import sys
import time

from . import probe_config as pc

HOT_TTL_S = 1.0

_view_at = -1.0e9
_view: tuple[frozenset, bool] = (frozenset(), False)


def _session_view(fresh: bool) -> tuple[frozenset, bool]:
    """(folders set aside, retired defaults count) for this process's session:
    inside an agent session the researcher's `ignore` answer sets aside exactly
    the files it was about, and retired folder defaults still apply; with no
    session (a terminal, a training node) every file applies and they do not."""
    global _view_at, _view
    now = time.monotonic()
    if not fresh and now - _view_at < HOT_TTL_S:
        return _view
    skip: frozenset = frozenset()
    legacy = False
    try:
        from . import agent_session, session_marker

        sid = agent_session.session_id_from_env()
        if sid and session_marker.valid_session_id(sid):
            legacy = True
            _start, skip = pc.session_view(session_marker.sessions_dir(), sid)
    except Exception:  # noqa: BLE001 - a check never breaks the caller
        skip, legacy = frozenset(), False
    _view_at, _view = now, (skip, legacy)
    return _view


def excluded(
    path: str | os.PathLike, *, is_dir: bool | None = None, cwd: str | None = None, hot: bool = False,
    resolve: bool = True,
) -> pc.Verdict:
    """Is `path` excluded, as this process's session sees it?"""
    skip, legacy = _session_view(fresh=not hot)
    return pc.check(
        path, is_dir=is_dir, cwd=cwd, skip=skip, legacy=legacy, ttl=HOT_TTL_S if hot else 0.0, resolve=resolve
    )


def cwd_excluded(folder: str | os.PathLike | None = None) -> pc.Verdict:
    """Is work run in `folder` (default: the working directory) excluded?"""
    skip, legacy = _session_view(fresh=True)
    try:
        here = os.fspath(folder) if folder is not None else os.getcwd()
    except OSError:
        return pc.NOT_EXCLUDED
    return pc.check_cwd(here, skip=skip, legacy=legacy)


def run_excluded() -> tuple[str, pc.Verdict] | None:
    """For `probe.init()`: (the path, its verdict) when the working directory or
    the running script is excluded, else None."""
    verdict = cwd_excluded()
    if verdict.excluded:
        try:
            return os.getcwd(), verdict
        except OSError:
            return ".", verdict
    script = sys.argv[0] if sys.argv else ""
    if script and script not in ("-c", "-m", "-") and os.path.isfile(script):
        verdict = excluded(script, is_dir=False)
        if verdict.excluded:
            return os.path.abspath(script), verdict
    return None


def say(template: str, path: str | os.PathLike, verdict: pc.Verdict) -> str:
    """One of `probe_config`'s messages, filled in."""
    return template.format(path=pc.shown(path), source=_source(verdict))


def _source(verdict: pc.Verdict) -> str:
    rule = verdict.rule
    if rule is None:
        return pc.CONFIG_NAME
    where = pc.shown(rule.source)
    return f"{where}:{rule.line} ({rule.pattern})" if rule.line else f"{where} ({rule.pattern})"


def source(verdict: pc.Verdict) -> str:
    """`~/code/.probe.config:1 (/*)`: where a verdict came from, as messages show it."""
    return _source(verdict)


def warn(message: str) -> None:
    try:
        print(message, file=sys.stderr)
    except Exception:  # noqa: BLE001
        pass
