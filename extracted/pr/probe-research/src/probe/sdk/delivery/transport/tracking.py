"""TrackingMarker: settle a coding-agent session's tracking on its first research write."""

from __future__ import annotations


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
