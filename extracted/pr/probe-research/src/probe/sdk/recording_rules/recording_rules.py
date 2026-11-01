"""`.probe.config` as this process sees it.

`probe_config` is the stdlib matcher every surface carries; this is the SDK/CLI side: which agent session
this process belongs to, where it started, and whether the researcher set the files above that folder aside
(`probe session parent ignore`). Every answer is session-aware and never raises.

Capture paths (code, outputs, reads) ask per file walked or read, so they pass `hot=True`: the session view
and each folder's stat may be up to `HOT_TTL_S` old (as do `--from-manifest` rows). Other refusals (`probe`
CLI writes, `probe.init()`, `log_artifact`) read fresh.
"""

from __future__ import annotations

import os
import sys
import time

from .. import probe_config as pc

HOT_TTL_S = 1.0

_view_at = -1.0e9
_view: tuple[frozenset, bool] = (frozenset(), False)


def _session_view(fresh: bool) -> tuple[frozenset, bool]:
    """(folders set aside, retired-defaults flag) for this process's session: in an agent session the
    researcher's `ignore` answer sets aside exactly the files it was about and retired folder defaults
    still apply; with no session (terminal, training node) every file applies and they do not."""
    global _view_at, _view
    now = time.monotonic()
    if not fresh and now - _view_at < HOT_TTL_S:
        return _view
    skip: frozenset = frozenset()
    legacy = False
    try:
        from .. import agent_session, session_marker

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


def checker(*, hot: bool = True, cwd: str | None = None) -> pc.Checker:
    """`excluded` for a batch of paths (snapshot, walk, manifest): same answers, each folder worked out once."""
    skip, legacy = _session_view(fresh=not hot)
    return pc.Checker(cwd=cwd, skip=skip, legacy=legacy, ttl=HOT_TTL_S if hot else 0.0)


def cwd_excluded(folder: str | os.PathLike | None = None) -> pc.Verdict:
    """Is work run in `folder` (default: the working directory) excluded?"""
    skip, legacy = _session_view(fresh=True)
    try:
        here = os.fspath(folder) if folder is not None else os.getcwd()
    except OSError:
        return pc.NOT_EXCLUDED
    return pc.check_cwd(here, skip=skip, legacy=legacy)


def run_excluded() -> tuple[str, pc.Verdict] | None:
    """For `probe.init()`: (path, verdict) when the working directory or running script is excluded, else None.
    The stricter wins (a `hash` folder running an `off` script is `off`); `identity_only` means the run opens and
    records identities only."""
    found: tuple[str, pc.Verdict] | None = None
    verdict = cwd_excluded()
    if verdict.excluded:
        try:
            found = (os.getcwd(), verdict)
        except OSError:
            found = (".", verdict)
        if verdict.hidden:
            return found
    script = sys.argv[0] if sys.argv else ""
    if script and script not in ("-c", "-m", "-") and os.path.isfile(script):
        verdict = excluded(script, is_dir=False)
        if verdict.excluded:
            mine = (os.path.abspath(script), verdict)
            if found is None:
                return mine
            worse = pc.stricter(found[1], verdict)
            if worse is found[1]:
                return found
            if worse is verdict:
                return mine
            return found[0], worse  # `read` and `hash` met: `off`
    return found


def identity_only(path: str | os.PathLike, *, is_dir: bool | None = None, hot: bool = False) -> bool:
    """Whether `path` is at `hash`: the SDK records only its identity (path, sha256/fingerprint, size, rows). Never raises."""
    try:
        return excluded(path, is_dir=is_dir, hot=hot).identity_only
    except Exception:  # noqa: BLE001 - a check never breaks the caller
        return False


def run_identity_only() -> bool:
    """Whether this process's run location (cwd or script) is at `hash`: the run records metrics, config and file
    identities but not its console log (such scripts commonly print their records). Never raises."""
    try:
        hit = run_excluded()
    except Exception:  # noqa: BLE001
        return False
    return hit is not None and hit[1].identity_only


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
