"""Service layer for `montecarlo agent-traces export`.

Wraps the two-call async pattern (mutation → poll status query → download
presigned URL) into a single CLI command. Mirrors the data_exports service
shape — GqlWrapper for the API calls, click for user-facing output.
"""

import os
import re
import time
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import unquote, urlparse

import click
import requests

from montecarlodata.agent_traces.queries import (
    EXPECTED_EXPORT_AGENT_TRACE,
    EXPECTED_GET_AGENT_TRACE_EXPORT,
    EXPORT_AGENT_TRACE,
    GET_AGENT_TRACE_EXPORT,
)
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.utils import GqlWrapper

# Status values returned by the server (mapped at the server's resolver
# boundary from the internal QUEUED/RUNNING/COMPLETED/FAILED enum).
# DONE_PARTIAL is terminal: the artifact is available but at least one span
# couldn't be fetched. The download still proceeds (the partial artifact has
# debug value), but the CLI exits non-zero so shell pipelines / Agent Preflight
# tooling can detect that the export is unusable as complete golden data.
_TERMINAL_STATUSES = {"DONE", "DONE_PARTIAL", "FAILED"}

# How many consecutive poll failures the CLI tolerates before giving up.
# An isolated network blip or gateway 504 shouldn't kill an export that's
# still running fine server-side — especially for slow CH-backed traces
# where polling can accumulate over minutes. Set conservatively: 5
# consecutive failures (~10s at the default 2s poll interval) is enough
# to ride out a transient hiccup but short enough to surface a real
# outage quickly.
_MAX_CONSECUTIVE_POLL_ERRORS = 5


# Pattern of an agent-trace URL's path from the Monte Carlo UI:
# /agents/<MCON>/<agent-slug>/traces/<trace_id>[?<query>]
#
# MCON itself contains '++' and ':' (e.g. "MCON++<account>++<warehouse>++table
# ++<db>:<schema>.<table>"). None of those are path separators, so the path
# segment between /agents/ and /<agent-slug>/traces/ captures the full MCON
# even when the table id contains colons or other punctuation.
#
# <agent-slug> is the URL-friendly name of the agent the trace belongs to
# (e.g. "ai-agent", "parts-procurement-agent"). Slugs are alphanumeric +
# hyphen today; we don't pin a stricter shape here because the slug is
# discarded — we only care about position. If the server ever surfaces
# underscores or dots in slugs, broaden the character class accordingly.
#
# Trace IDs are 32-char hex in real callers; the [0-9a-fA-F]+ accepts any
# hex string for robustness across future server-side changes to the
# format.
_TRACE_LINK_PATH_PATTERN = re.compile(
    r"^/agents/(MCON\+\+[^/]+)/[a-zA-Z0-9-]+/traces/([0-9a-fA-F]+)/?$"
)

# Apex domain of all Monte Carlo UI hosts (app.getmontecarlo.com,
# eu1.getmontecarlo.com, local.getmontecarlo.com, etc.). Match either the
# apex itself or a subdomain. Lightweight guardrail to give a clearer error
# when users paste a non-MC URL by accident — the real authorization
# boundary is server-side mcon/trace_id auth, not host validation.
_MC_UI_DOMAIN = "getmontecarlo.com"


def parse_trace_link(link: str) -> Tuple[str, str]:
    """Extract (mcon, trace_id) from a Monte Carlo agent-trace page URL.

    Accepts the URL shape produced by the UI's "copy link" button:

        https://<host>/agents/<MCON>/ai-agent/traces/<trace_id>[?<query>]

    Host must be ``getmontecarlo.com`` or a subdomain of it (covers
    ``app.``, ``eu1.``, ``local.``, etc.). Scheme, port, query string,
    and fragment are ignored. URL-encoded path characters (e.g. ``%2B``
    for ``+``) are decoded before matching so links copied from address
    bars in either encoded or pre-decoded form both work.

    Raises ``ValueError`` if the host or path doesn't match, with the
    offending input echoed so the user can spot a typo or wrong-page
    paste.
    """
    parsed = urlparse(link)
    hostname = (parsed.hostname or "").lower()
    if hostname != _MC_UI_DOMAIN and not hostname.endswith("." + _MC_UI_DOMAIN):
        raise ValueError(
            f"Expected a Monte Carlo trace URL (host ending in '{_MC_UI_DOMAIN}'); got {link!r}."
        )

    path = unquote(parsed.path or "")
    match = _TRACE_LINK_PATH_PATTERN.match(path)
    if not match:
        raise ValueError(
            f"Could not parse trace MCON and trace ID from {link!r}. "
            f"Expected a URL like "
            f"'https://app.getmontecarlo.com/agents/MCON++.../ai-agent/traces/<hex-id>' "
            f"(copy via the trace page's 'copy link' button in the UI)."
        )
    return match.group(1), match.group(2)


class AgentTraceExportService:
    SERVICE_NAME = "agent_trace_export_service"

    def __init__(
        self,
        config: Config,
        command_name: str,
        request_wrapper: Optional[GqlWrapper] = None,
        polling_wrapper: Optional[GqlWrapper] = None,
    ):
        self._abort_on_error = True
        self._command_name = command_name
        self._request_wrapper = request_wrapper or GqlWrapper(
            config,
            command_name=self._command_name,
        )
        # Separate wrapper for the status-poll loop. Constructed with
        # abort_on_error=False so a single transient GraphQL error (e.g.
        # a gateway 504 surfaced as `errors: [{message: "Request timed
        # out"}]`) returns to the caller instead of immediately aborting.
        # The poll loop tolerates a bounded streak of such errors and
        # aborts only if connectivity is genuinely lost. The strict
        # wrapper above stays for the one-shot mutation, where an
        # immediate abort on the first error is the right behavior.
        self._polling_wrapper = polling_wrapper or GqlWrapper(
            config,
            command_name=self._command_name,
            abort_on_error=False,
        )

    @manage_errors
    def export(
        self,
        *,
        mcon: str,
        trace_id: str,
        output: Optional[str] = None,
        timeout_seconds: int = 600,
        poll_interval_seconds: float = 2.0,
    ) -> bool:
        """Run the full export flow: dispatch, poll, download.

        Args:
            mcon: MCON of the trace table (found in the trace page URL in the UI).
            trace_id: hex trace id to export.
            output: file path to write the gzipped JSON to. Defaults to
                ./trace-<trace_id>.json.gz in the current directory.
            timeout_seconds: max wall-clock time to wait for DONE before
                returning with a "still running" message.
            poll_interval_seconds: seconds between status polls.

        Returns:
            True if the export reached DONE (full success) and the artifact
            was downloaded.
            False if either (a) the export reached DONE_PARTIAL — artifact
            still downloaded but incomplete, unusable for Agent Preflight
            golden data — or (b) the poll loop hit ``timeout_seconds``
            before reaching a terminal status. The Click command function
            translates ``False`` into a non-zero exit code (2) — ``Exit()``
            raised here would be swallowed by the ``@manage_errors``
            decorator (which catches all ``Exception`` subclasses including
            ``click.exceptions.Exit`` and re-raises as ``Abort``), see
            ``collector/commands.py:run_validations`` for the canonical
            return-then-Exit pattern.
        """
        job_id = self._request_export(mcon=mcon, trace_id=trace_id)
        click.echo(f"Started export job {job_id}")

        status_payload = self._poll_until_terminal(
            job_id=job_id,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
        )

        if status_payload is None:
            # Lost contact during polling (max consecutive errors before
            # the deadline, or deadline hit during an error streak with no
            # successful poll). The server-side job may still be running.
            click.echo(
                f"Export status unclear after {timeout_seconds}s — multiple polling "
                f"failures. Job {job_id} may still be running on the server.",
                err=True,
            )
            return False

        status = status_payload.status  # type: ignore
        if status == "FAILED":
            error = status_payload.error or "(no error message)"  # type: ignore
            complain_and_abort(f"Export failed: {error}")
        elif status not in {"DONE", "DONE_PARTIAL"}:
            # Timed out — surface the job id so the user can resume later.
            click.echo(
                f"Export still {status} after {timeout_seconds}s. "
                f"Re-run with --resume {job_id} once it completes.",
                err=True,
            )
            return False

        url = status_payload.url  # type: ignore
        if not url:
            complain_and_abort(
                f"Server returned {status} but no presigned URL — this should not happen."
            )

        output_path = self._resolve_output_path(output=output, trace_id=trace_id)
        self._download_to_path(url=url, output_path=output_path)

        if status == "DONE_PARTIAL":
            # Loud, structured warning to stderr — the partial artifact is
            # not usable as Agent Preflight golden data. Server's `error`
            # carries a stable structured summary like
            # "N span(s) dropped at single-span payload limit; M additional
            # span(s) not fetched after abort". Surface verbatim so users
            # can copy/paste into Slack / a bug report.
            partial_reason = status_payload.error or "(no detail)"  # type: ignore
            click.echo(
                "WARNING: Export completed with PARTIAL data.\n"
                f"  Reason: {partial_reason}\n"
                "  Cannot be used as Agent Preflight golden data — "
                "re-run the export to retry.\n"
                f"  Partial artifact saved to: {output_path}",
                err=True,
            )
            # Return False so the Click command emits Exit(2) at the
            # command layer; shell pipelines / Make tooling see non-zero.
            return False

        click.echo(f"Downloaded to {output_path}")
        return True

    def _request_export(self, *, mcon: str, trace_id: str) -> str:
        """Send the exportAgentTrace mutation. Returns the job_id (string UUID)."""
        response = self._request_wrapper.make_request_v2(
            query=EXPORT_AGENT_TRACE,
            operation=EXPECTED_EXPORT_AGENT_TRACE,
            service=self.SERVICE_NAME,
            variables=dict(mcon=mcon, trace_id=trace_id),
        )
        # Box wraps the response with exact-key attribute access — GraphQL
        # returns camelCase keys, so `.jobId` rather than `.job_id`. Snake-cased
        # access would silently AttributeError.
        return response.data.jobId  # type: ignore

    def _poll_until_terminal(
        self,
        *,
        job_id: str,
        timeout_seconds: int,
        poll_interval_seconds: float,
    ):
        """Poll getAgentTraceExport until the job hits a terminal status,
        the timeout is reached, or we lose contact with the server.

        Tolerates a bounded streak of consecutive poll failures (gateway
        504s, transient network errors). On a successful poll, the error
        counter resets — so a flaky connection doesn't accumulate over
        the lifetime of a long-running export. Aborts only if we exceed
        ``_MAX_CONSECUTIVE_POLL_ERRORS`` in a row.

        Returns the last successful status payload (terminal or last-
        known non-terminal on deadline hit), or ``None`` if we lost
        contact during polling — caller treats ``None`` like a timeout.
        """
        deadline = time.monotonic() + timeout_seconds
        last_status: Optional[str] = None
        last_good_payload = None
        consecutive_errors = 0
        last_error_summary: Optional[str] = None
        while True:
            payload, errors = self._poll_once(job_id=job_id)
            status = getattr(payload, "status", None) if payload else None

            if status:
                consecutive_errors = 0
                last_good_payload = payload
                if status != last_status:
                    click.echo(f"Status: {status}")
                    last_status = status
                if status in _TERMINAL_STATUSES:
                    return payload
                if time.monotonic() >= deadline:
                    return payload
            else:
                consecutive_errors += 1
                last_error_summary = self._summarize_poll_errors(errors)
                if consecutive_errors >= _MAX_CONSECUTIVE_POLL_ERRORS:
                    complain_and_abort(
                        f"Lost contact with the export service: "
                        f"{consecutive_errors} consecutive polling failures. "
                        f"Job {job_id} may still be running on the server — "
                        f"check the API endpoint and re-run once connectivity "
                        f"is restored. Last error: {last_error_summary}"
                    )
                click.echo(
                    f"Poll failed ({last_error_summary}); retrying in "
                    f"{poll_interval_seconds}s "
                    f"(consecutive errors: {consecutive_errors}/"
                    f"{_MAX_CONSECUTIVE_POLL_ERRORS})",
                    err=True,
                )
                if time.monotonic() >= deadline:
                    # Deadline hit during an error streak. If we had any
                    # successful poll earlier, return its payload so the
                    # caller can report the last-known status; otherwise
                    # signal lost-contact with None.
                    return last_good_payload
            time.sleep(poll_interval_seconds)

    def _poll_once(self, *, job_id: str):
        """Single poll. Returns (payload, errors). On transport-level
        exceptions (network, connection reset, etc.) returns
        (None, [{message: str(exc)}]) so the caller can treat all
        per-poll failures uniformly without juggling exception types."""
        try:
            response = self._polling_wrapper.make_request_v2(
                query=GET_AGENT_TRACE_EXPORT,
                operation=EXPECTED_GET_AGENT_TRACE_EXPORT,
                service=self.SERVICE_NAME,
                variables=dict(job_id=job_id),
            )
            return response.data, response.errors
        except Exception as e:
            return None, [{"message": str(e)}]

    @staticmethod
    def _summarize_poll_errors(errors) -> str:
        """Extract a short human-readable summary from a GraphQL errors
        list (or our synthesized transport-error stand-in). Falls back to
        a generic message if the shape is unexpected so we never crash
        the retry-or-abort decision on a malformed error payload."""
        if not errors:
            return "(no error detail)"
        first = errors[0]
        if isinstance(first, dict):
            return str(first.get("message") or first)
        return str(first)

    @staticmethod
    def _resolve_output_path(*, output: Optional[str], trace_id: str) -> Path:
        if output:
            return Path(output).expanduser().resolve()
        return Path.cwd() / f"trace-{trace_id}.json.gz"

    @staticmethod
    def _download_to_path(*, url: str, output_path: Path) -> None:
        """Stream the presigned URL contents to disk.

        Streamed download avoids loading the whole gzipped payload in memory —
        Phase 2 traces with warehouse spans can be tens of MB.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with requests.get(url, stream=True) as resp:
            resp.raise_for_status()
            # The server sets Content-Encoding: gzip on the S3 object so
            # the URL serves gzipped bytes. We want the bytes verbatim
            # (already gzipped) — set decode_content=False to prevent
            # requests/urllib3 from auto-inflating mid-stream.
            resp.raw.decode_content = False
            with open(output_path, "wb") as out:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        out.write(chunk)
        # Sanity: file should be non-empty.
        if output_path.stat().st_size == 0:
            complain_and_abort(f"Downloaded file is empty: {output_path}. Check server logs.")
        # Friendly note when the file isn't named .json.gz — the body IS
        # gzipped regardless, just give the user a heads-up.
        if os.path.splitext(output_path)[1] not in (".gz", ".gzip"):
            click.echo(
                f"Note: file written verbatim (gzipped). "
                f"Decompress with `gunzip -c {output_path} | jq .` to view.",
                err=True,
            )
