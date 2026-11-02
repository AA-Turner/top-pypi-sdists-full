"""TrackingMarker: settle a coding-agent session's tracking on its first research write."""

from __future__ import annotations

from probe.sdk import session_marker


#: Route families whose create/change requests ARE recording research: the writes the
#: tracking auto-mark mirrors (`_auto_mark_tracking`). Nested routes (artifacts, notes,
#: uploads) sit under these prefixes. Kept in step with the CLI vocabulary in
#: plugins/probe-research/hooks/tracking_guard.py::WRITE_GROUPS (that names COMMANDS for
#: the warn layer, this URL families for the auto-mark); both lean the same way: a miss
#: costs silence (no mark), never a false mark. Machine plumbing (/v1/tokens, auth,
#: capabilities, workspaces) is deliberately absent.
_RESEARCH_PATH_PREFIXES = (
    "/v1/projects",
    "/v1/experiments",
    "/v1/runs",
    "/v1/artifacts",
    "/ingest/",
)

#: Methods that only read. Everything else on a research path is a write.
_READ_METHODS = ("GET", "HEAD", "OPTIONS")

#: Cap on remembered sessions so a long-lived transport (the hosted MCP serves many
#: callers through one) cannot grow a set forever. Forgetting is safe: the session is
#: re-checked on its next write (one stat) and still cannot overwrite a decision.
_TRACKING_MEMO_CAP = 512


def _is_research_path(path: str) -> bool:
    """Whether this path is a research route, matched on SEGMENT boundaries: a bare prefix
    would read `/v1/projects-search` as `/v1/projects` and a search-shaped POST under a
    look-alike name would flip tracking. The prefix must be the whole path or be followed
    by `/` or `?`.
    """
    for prefix in _RESEARCH_PATH_PREFIXES:
        if not path.startswith(prefix):
            continue
        rest = path[len(prefix) :]
        if not rest or rest[0] in "/?" or prefix.endswith("/"):
            return True
    return False


class TrackingMarkerMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    def _auto_mark_tracking(self, method: str, path: str, session_id: str | None) -> None:
        """After a coding-agent session's first successful research write, settle its tracking signal at
        the cwd's default (never `on` by itself), so local surfaces agree with the backend. Never for
        reads, non-research routes, an env override or an explicit decision; only a settled session is
        remembered. Fail-soft: never breaks the write it rides on."""
        if not session_id or session_id in self._tracking_marked:
            return
        if method.upper() in _READ_METHODS:
            return
        if not _is_research_path(path):
            return
        try:
            # Normal path: SessionStart already settled it. Read before resolving any
            # default so a later folder edit adds no ancestor I/O to every write.
            if session_marker.tracking_signal(session_id) is not None:
                settled = True
            elif session_marker.tracking_env_override() is not None:
                settled = True  # held by the env for this process's lifetime
            elif session_marker.set_tracking_if_absent(
                session_id, session_marker.resolve_tracking_default(None)[0]
            ):
                settled = True  # this call decided it
            else:
                # False is ambiguous: a decision exists, or the write failed.
                settled = session_marker.tracking_signal(session_id) is not None
        except Exception:  # noqa: BLE001 - by the fail-soft contract above
            return
        if not settled:
            return
        if len(self._tracking_marked) >= _TRACKING_MEMO_CAP:
            self._tracking_marked.clear()
        self._tracking_marked.add(session_id)
