"""Tracks whether the API key this editor authenticates with is still accepted.

The web editor pod signs every cloud-api call with the project's 'web-editor'
API key, injected as ABSTRA_API_TOKEN at deploy time. Revoke that key while the
pod is running (deleting it in the console does exactly that) and every cloud-api
call starts answering 401: Smart Chat, tables, connectors, deploys. The pod
cannot mint a replacement, because the key *is* its only credential.

This service only notices and says so; repairing is
controllers/web_editor.repair_api_key, which asks cloud-api for a live key
against the editor session token and stores it. Noticing is what makes the repair
possible at all: flagging the rejected token is what lets get_credentials prefer
the stored one over the environment's, so the pod recovers without being
replaced.

The status rides GET /_editor/api/web-editor/, and the frontend watcher polls it
to trigger the repair. Only once that repair has failed does it fall back to the
console waiting room, which redeploys the pod with a fresh key.

A single 401 does not prove the key is dead — cloud-api also answers 401 when the
web editor session token is expired — so the first 401 triggers a probe against
/cli/api-keys/info, whose only credential is the API key. Only an explicit
401/403 there flags the key. Connection errors and 5xx leave it valid: swapping
credentials during a cloud-api blip would trade a working pod for nothing.
"""

import threading
import time
from typing import Callable, Optional

from abstra_internals.cloud_api import get_api_key_info
from abstra_internals.credentials import (
    get_credentials,
    mark_token_rejected,
    resolve_headers,
    set_credentials,
)
from abstra_internals.logger import AbstraLogger

# Floor between probes, so a burst of 401s (or a steady stream of failing
# requests) costs one round trip instead of one per request.
PROBE_INTERVAL_SECONDS = 30


def _current_header() -> Optional[str]:
    """The Api-Authorization the next request would carry, in the same shape the
    client reports back, so the two can be compared without string surgery."""
    return (resolve_headers() or {}).get("Api-Authorization")


def resolve_ambient_session_token() -> Optional[str]:
    """The editor session token available where a 401 happened.

    The request's own cookie when there is one; otherwise the copy the editor
    keeps on disk for the paths that run without a request (the tunnel already
    reads it the same way). In a worker there is only the file, so the identity is
    whoever opened the editor last — the same caveat that file already carries.
    """
    try:
        import flask

        token = flask.request.cookies.get("editor_auth")
        if token:
            return token
    except Exception:
        # No request context (background thread, worker), or no cookie.
        pass

    try:
        from abstra_internals.cloud_api import get_editor_auth_token_from_file

        return get_editor_auth_token_from_file() or None
    except Exception:
        return None


class ApiKeyStatus:
    """Process-wide, thread-safe.

    Invalid is sticky until `reset`, which the repair calls once new credentials
    are stored. Nothing else clears it: re-probing on a timer would only flap
    while the key stays revoked.
    """

    _lock = threading.Lock()
    _invalid = False
    _last_probe_at = 0.0

    # Serializes recovery, so a burst of 401s across threads costs one repair:
    # the first thread repairs and the others wait, then find fresh credentials
    # already in place and simply retry.
    _recovery_lock = threading.Lock()

    # Per-thread guard. The repair talks to cloud-api through the same client, so
    # without this its own response could start another recovery underneath us.
    _recovering = threading.local()

    # Injected at wiring time (repositories/factory) to keep this service free of
    # repository imports. Takes the session token, returns the key to store.
    _repair_fn: Optional[Callable[[str], Optional[str]]] = None

    @classmethod
    def is_valid(cls) -> bool:
        with cls._lock:
            return not cls._invalid

    @classmethod
    def configure_repair(cls, repair_fn: Callable[[str], Optional[str]]) -> None:
        cls._repair_fn = repair_fn

    @classmethod
    def recover_from_unauthorized(cls, sent_credential: Optional[str] = None) -> bool:
        """Handle a 401 from cloud-api and report whether to retry the request.

        Runs synchronously on the caller's thread: the point is that the request
        that hit the revoked key gets replayed with a live one, instead of failing
        and leaving the user to trigger the recovery by hand. Returns False when
        there is nothing to retry with, and the caller keeps its 401.

        `sent_credential` is the Api-Authorization the request went out with. It
        has to come from the caller rather than be read here: concurrent requests
        overlap, so by now the credential may already have been replaced by
        another one of them, and the only thing this request needs is a replay.
        """
        if getattr(cls._recovering, "active", False):
            return False

        cls._recovering.active = True
        try:
            with cls._recovery_lock:
                if sent_credential is not None and sent_credential != _current_header():
                    # Already replaced, by another request or while this one was in
                    # flight. Nothing to repair; just replay with what is current.
                    return True

                token_in_use = get_credentials()
                if not cls._confirm_invalid(token_in_use):
                    return False

                session_token = resolve_ambient_session_token()
                if not session_token:
                    AbstraLogger.warning(
                        "[ApiKeyStatus] API key is revoked but no editor session token "
                        "is available to replace it"
                    )
                    return False

                return cls.repair(session_token)
        except Exception as e:
            AbstraLogger.capture_exception(e)
            return False
        finally:
            cls._recovering.active = False

    @classmethod
    def repair(cls, session_token: str) -> bool:
        """Swap in a live API key, obtained against the editor session token.

        Storing the key is not enough on its own: the deployment's token would
        still win the resolution and every call would keep 401ing. So whatever was
        in use gets rejected as part of the swap — that is what actually puts the
        stored key in front. Callers that reach here without having probed first
        (the frontend-driven repair) depend on this.

        Rejecting only happens when cloud-api hands back a *different* key, so a
        repair triggered on a healthy pod is a no-op rather than a self-inflicted
        outage.
        """
        if cls._repair_fn is None:
            return False

        replaced = get_credentials()
        api_key = cls._repair_fn(session_token)
        if not api_key:
            return False

        if replaced and replaced != api_key:
            mark_token_rejected(replaced)

        set_credentials(api_key)
        cls.reset()
        AbstraLogger.warning(
            "[ApiKeyStatus] API key replaced at runtime; the editor is authenticated again"
        )
        return True

    @classmethod
    def _confirm_invalid(cls, token_in_use: Optional[str]) -> bool:
        """Whether cloud-api really refuses this token.

        A 401 is not proof on its own: routes that take a session token answer
        401 for an expired one too, and replacing the API key would not fix that.
        /cli/api-keys/info settles it, since the API key is its only credential.
        Throttled, so a stream of 401s that are not about the key (an expired
        session, say) costs one probe rather than one per request.
        """
        with cls._lock:
            if cls._invalid:
                return True
            if time.time() - cls._last_probe_at < PROBE_INTERVAL_SECONDS:
                return False
            cls._last_probe_at = time.time()

        headers = resolve_headers()
        if headers is None:
            cls._flag_invalid("no credentials available", None)
            return True

        reason = get_api_key_info(headers).get("reason")
        if reason != "INVALID_API_TOKEN":
            # Connection errors and 5xx land here too: swapping credentials during
            # a cloud-api blip would trade a working pod for nothing.
            return False

        cls._flag_invalid("cloud-api rejected the API key", token_in_use)
        return True

    @classmethod
    def _flag_invalid(cls, reason: str, token: Optional[str]) -> None:
        if token:
            mark_token_rejected(token)

        with cls._lock:
            already_invalid = cls._invalid
            cls._invalid = True

        if not already_invalid:
            AbstraLogger.warning(
                f"[ApiKeyStatus] API key is no longer valid ({reason}). "
                "The editor will ask cloud-api for a new one."
            )

    @classmethod
    def reset(cls) -> None:
        """Report healthy again after new credentials are stored, so the frontend
        stops asking for a repair.

        Deliberately does not touch which tokens are rejected: the revoked
        environment token must stay rejected, or get_credentials would prefer it
        over the one just stored and we would flap between repairing and 401ing.
        """
        with cls._lock:
            was_invalid = cls._invalid
            cls._invalid = False
            cls._probe_in_flight = False
            cls._last_probe_at = 0.0

        if was_invalid:
            AbstraLogger.warning(
                "[ApiKeyStatus] API key repaired; status is valid again"
            )
