"""TrackingMarker: settle a coding-agent session's tracking on its first research write; a run create
turns an off or read auto chat on (probe auto mode)."""

from __future__ import annotations

import re
import sys

from probe.sdk import session_marker

#: A run create: `POST /v1/projects/<id>/runs` or `.../experiments/<id>/runs` (`client.runs.create`).
_RUN_CREATE_PATH = re.compile(r"^/v1/projects/[^/?]+(?:/experiments/[^/?]+)?/runs/?(?:\?.*)?$")


#: Route families whose create/change requests ARE recording research: the writes the
#: tracking auto-mark mirrors (`_auto_mark_tracking`). Nested routes (artifacts, notes,
#: uploads) sit under these prefixes. Kept in step with the CLI vocabulary in
#: plugins/probe/hooks/tracking_guard.py::WRITE_GROUPS (that names COMMANDS for
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
        """After a coding-agent session's first successful research write, settle a switch nobody
        decided from the new-chat default, so local surfaces agree with the backend. Undecided there
        means Probe's hooks never started the chat (it was open before the install), so its `on` is
        `on (inline)` (`seed_inline`), never an invented state. Never for reads, non-research routes,
        an env override or an explicit decision; only a settled session is remembered. Fail-soft:
        never breaks the write it rides on."""
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
            elif session_marker.state_env_override() is not None:
                settled = True  # held by the env for this process's lifetime
            elif session_marker.seed_inline(session_id):
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

    def _set_auto_chat_on(self, method: str, path: str, session_id: str | None, response) -> None:
        """A successful run create (its answer carries the run id) from an auto chat that is off or read:
        turn it on, stored by who records, so the run is recorded (`session_marker.set_auto_chat_on`).
        Fail-soft: never breaks the create it rides on."""
        if not session_id or method.upper() != "POST" or not _RUN_CREATE_PATH.match(path):
            return
        try:
            body = response.json()
            if not isinstance(body, dict) or not body.get("id"):
                return
            from probe.sdk import agent_session

            found = agent_session.session_agent_from_env()
            if session_marker.set_auto_chat_on(session_id, found[0] if found else None) is None:
                return
            print(session_marker.RUN_LAUNCH_ON, file=sys.stderr, flush=True)
            _send_run_launch(found[0] if found else None)
        except Exception:  # noqa: BLE001 - by the fail-soft contract above
            return


def _send_run_launch(chat_agent: str | None) -> None:
    """`session.switched` for a run create that turned an auto chat on (trigger `run_launch`)."""
    from probe import analytics

    analytics.emit_session_switched(scope="chat", state="on", chat_agent=chat_agent,
                                    control=session_marker.CONTROL_AUTO,
                                    trigger=str(analytics.SwitchTrigger.RUN_LAUNCH))
