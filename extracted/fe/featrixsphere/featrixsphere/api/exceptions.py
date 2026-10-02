#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Exceptions for FeatrixSphere API client.
"""


class FeatrixAuthenticationError(Exception):
    """Raised when the server returns 401 Unauthorized.

    This means the API key is missing, invalid, or expired.
    Set your API key in ~/.featrix or the FEATRIX_API_KEY environment variable.
    """

    def __init__(self, message: str = None, status_code: int = 401):
        if message is None:
            message = (
                "Authentication required. "
                "Set your API key in ~/.featrix (as api_key=sk_live_...) "
                "or the FEATRIX_API_KEY environment variable."
            )
        self.status_code = status_code
        super().__init__(message)


class FeatrixPredictionError(Exception):
    """Raised when a prediction request fails on the server.

    Contains the server's error detail (e.g., model integrity check failure,
    missing model, version mismatch) so the customer sees an actionable message
    instead of a raw HTTP 500.
    """

    def __init__(self, message: str, status_code: int = 500):
        self.status_code = status_code
        super().__init__(message)


class ModelNotLoadingError(Exception):
    """Raised when ``get_load_status`` is called for a model the server isn't
    tracking. Either the model was never asked to load, or the load entry has
    been evicted from the server's in-memory state.
    """

    def __init__(self, model_id: str = None, message: str = None):
        self.model_id = model_id
        if message is None:
            message = f"Server is not tracking a load for model {model_id!r}"
        super().__init__(message)


class LoadTimeoutError(Exception):
    """Raised by ``wait_until_loaded`` when ``timeout_s`` elapses before the
    load reaches ``phase='done'``.
    """

    def __init__(self, model_id: str = None, last_status=None, timeout_s: float = None):
        self.model_id = model_id
        self.last_status = last_status
        self.timeout_s = timeout_s
        super().__init__(
            f"Timed out after {timeout_s:.0f}s waiting for {model_id!r} to load; "
            f"last phase={getattr(last_status, 'phase', '?')}"
        )


class LoadFailedError(Exception):
    """Raised by ``wait_until_loaded`` (and surfaced from ``get_load_status``
    when phase=='failed') when the server reports the load failed.
    """

    def __init__(self, model_id: str = None, status=None):
        self.model_id = model_id
        self.status = status
        err = getattr(status, 'error', None) or "unknown error"
        super().__init__(f"Load failed for {model_id!r}: {err}")


class TrainingStatusUnavailableError(RuntimeError):
    """Raised by ``wait_for_training`` when the client cannot determine
    whether training succeeded, failed, or is still running.

    This is deliberately NOT the same signal as a confirmed training
    failure: it means polling broke down (repeated connection errors, or a
    'failed' status reading that was never confirmed by a follow-up poll),
    not that the server reported a terminal failure. Automation that
    relaunches training on a caught exception should catch this separately
    from a genuine failure and NOT relaunch — the job may still be running
    server-side, and relaunching blind creates duplicate training jobs that
    compete for the same compute node.

    Subclasses RuntimeError for backward compatibility with existing
    ``except RuntimeError`` callers; check ``isinstance(e,
    TrainingStatusUnavailableError)`` to distinguish "can't tell" from a
    confirmed failure.
    """

    def __init__(self, session_id: str = None, message: str = None):
        self.session_id = session_id
        if message is None:
            message = (
                f"Could not determine training status for session {session_id!r}. "
                f"The job may still be running — check status independently before "
                f"retrying or relaunching."
            )
        super().__init__(message)


class SessionNotFoundError(RuntimeError):
    """Raised by ``wait_for_training`` when the server has confirmed this
    session does not exist on any compute node (a 404 on session-status
    lookup).

    Unlike ``TrainingStatusUnavailableError`` ("can't tell"), this is a
    confirmed, terminal signal: the session is gone and polling again will
    not change that. Automation must NOT retry this call in a loop — that
    exact pattern (catch, retry ``wait_for_training()`` again, forever) is
    what let one customer's script poll a permanently-absent session
    continuously for 5+ days (~18,000 requests) with nothing on either side
    to stop it. See
    docs/internal/plans/2026-07-job-system-reliability-consolidated-plan.md
    Part 1, "zombie client, no circuit breaker either side".

    Subclasses RuntimeError for backward compatibility with existing
    ``except RuntimeError`` callers; check ``isinstance(e,
    SessionNotFoundError)`` to distinguish "confirmed gone" from either a
    confirmed failure or an unconfirmed "can't tell."
    """

    def __init__(self, session_id: str = None, message: str = None):
        self.session_id = session_id
        if message is None:
            message = (
                f"Session {session_id!r} was not found on any compute node. "
                f"This is a confirmed, permanent result — do not retry this call."
            )
        super().__init__(message)
