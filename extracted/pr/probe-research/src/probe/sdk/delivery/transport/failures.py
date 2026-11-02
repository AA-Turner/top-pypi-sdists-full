"""map a failed response or connection error to the SDK's typed errors, and say whether it may still have landed."""

from __future__ import annotations

import json

import httpx

from probe.sdk.settings import workspace_limit as _workspace_limit

from ... import errors


#: Answers a gateway gives IN PLACE of the app's: the request may have been
#: processed and only its response lost.
_AMBIGUOUS_STATUSES = frozenset({502, 503, 504})


def outcome_unknown(exc: BaseException) -> bool:
    """Whether a failed request may still have been PROCESSED by the server.

    A read timeout, dropped connection or protocol error after the request left, a
    deadline that cut only the response, or a 502/503/504 from in front of the app: the
    write may have landed and only the answer was lost. A connect-class failure is not
    unknown (never left), nor is any answer the app gave. Only a request safe to send
    twice (a run create with its `creation_key` on a server declaring
    `run_creation_key`, plan 2.5) may be re-sent after one."""
    if isinstance(exc, errors.DeadlineExceeded):
        return exc.sent
    if isinstance(exc, errors.TransportError):
        cause = exc.__cause__
        return isinstance(cause, httpx.HTTPError) and not isinstance(cause, _CONNECT_ERRORS)
    return isinstance(exc, errors.RosError) and exc.status in _AMBIGUOUS_STATUSES


def _presigned_put_error(resp: httpx.Response, url: str) -> errors.RosError:
    """The error for a presigned PUT's failed answer. 401/403 is the upload's own
    capability refused, not the credential (none sent): `UploadRefused` (#2073). Else as
    on any request."""
    if resp.status_code in (401, 403):
        detail = resp.text
        try:
            parsed = resp.json()
            if isinstance(parsed, dict) and parsed.get("detail") is not None:
                detail = parsed["detail"]
        except ValueError:
            pass
        message = (
            f"upload to {_blob_label(url)} refused ({resp.status_code}): "
            f"{errors._detail_message(detail)[:300]}. A presigned upload carries no "
            "credential, so this refuses the upload's signed URL, not your login; a "
            "self-hosted server must set public_base_url to its own address"
        )
        return _with_retry_after(
            errors.UploadRefused(message, status=resp.status_code, detail=detail), resp
        )
    return _with_retry_after(errors.error_for(resp.status_code, resp.text), resp)


def _is_trash_notice(resp: httpx.Response) -> bool:
    """The server's 410 for a run, group, experiment or project in its TRASH."""
    if resp.status_code != 410:
        return False
    try:
        body = resp.json()
    except (json.JSONDecodeError, ValueError):
        return False
    return isinstance(body, dict) and body.get("detail") == "in_trash"


class ErrorMappingMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    def _to_error(self, resp: httpx.Response) -> errors.RosError:
        try:
            body = resp.json()
            detail = body.get("detail")
            if body.get("code") == errors.CLIENT_TOO_OLD:
                min_version = body.get("min_version")
                min_version = min_version if isinstance(min_version, str) else None
                return errors.ClientTooOldError(
                    errors.upgrade_message(errors._detail_message(detail), min_version),
                    status=resp.status_code,
                    detail=detail,
                    min_version=min_version,
                )
            # A run, group, experiment or project in the TRASH answers 410 with a fixed token
            # plus the notice ("in the trash since ..., Probe can restore it until ...").
            # The sentence is what a person or agent needs; the token alone says nothing.
            in_trash = detail == "in_trash"
            if in_trash and isinstance(body.get("message"), str):
                detail = body["message"]
        except (json.JSONDecodeError, ValueError, AttributeError):
            detail, in_trash = resp.text, False
        error = errors.error_for(resp.status_code, detail)
        if in_trash:
            error.in_trash = True
        applied = resp.headers.get(_workspace_limit.APPLIED_HEADER)
        if applied and resp.status_code == 404:
            # The API answered under this computer's workspace limit: what was asked for may
            # exist outside it. Said, never left to read as gone (agents have filed
            # data-loss reports off a silent miss).
            error.workspace_limit_applied = applied
            _workspace_limit.annotate_not_found(
                error,
                _workspace_limit.hidden_hint(applied, getattr(self.settings, "workspace_limit", None)),
            )
        return _with_retry_after(error, resp)

from probe.sdk.delivery.transport.blobs import _blob_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.deadlines import _with_retry_after  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.transport.transport import _CONNECT_ERRORS  # noqa: E402 -- pieces need each other; the front door loads this one first
