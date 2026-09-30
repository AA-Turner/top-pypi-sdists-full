"""Client-owned retry for automind's ``page_not_ready`` (HTTP 409) answer.

The VQE does **not** retry internally. When the vision model reports an active
loader, ``auteur-automind`` returns ``{"error": "page_not_ready", ...}``
(``app/services/vqe_service.py``) and the heal route maps it to **409** with an
explicit contract (``app/api/endpoints/healer.py``)::

    # 409 is pragmatic (outside tenacity's 5xx retry set) — client
    # owns the retry loop; do NOT switch this to a 5xx.

409 is therefore deliberately absent from ``_http.TRANSIENT_HTTP_STATUS_CODES``:
retrying inside the transport layer would re-POST the *same stale screenshot*
and could never observe a settled page. The retry has to wrap the screenshot
capture — which is what :func:`retry_on_page_not_ready` does.

Port of the V2 source
(``_is_page_not_ready_response`` + the ``Heal.vision_query`` loop): 3 POSTs,
3s between them, a fresh screenshot and a fresh ``request_id`` every attempt.
"""
from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Callable

_log = logging.getLogger(__name__)

#: Body discriminator automind sets when the VQE saw an active loader.
PAGE_NOT_READY_ERROR = "page_not_ready"
#: Status automind pairs with it (picked to sit outside the transport retry set).
PAGE_NOT_READY_STATUS = 409
#: Total POSTs per vision call (V2 parity).
MAX_ATTEMPTS = 3
#: Delay between attempts. The final attempt is not followed by a sleep.
SLEEP_SECONDS = 3


def new_request_id() -> str:
    """Fresh per-attempt id so every retry lands in its own automind VQE debug
    folder (``{org_id}/vqe/{request_id}``) instead of overwriting the last one.
    """
    return uuid.uuid4().hex[:16]


def is_page_not_ready_response(response: Any) -> bool:
    """True when automind answered 409 AND ``body.error == "page_not_ready"``.

    Both halves are required — a 409 carrying any other body is not a loader
    signal and must not burn a retry.
    """
    if response is None or getattr(response, "status_code", None) != PAGE_NOT_READY_STATUS:
        return False
    try:
        body = response.json() if hasattr(response, "json") else {}
    except Exception:  # noqa: BLE001 — a non-JSON 409 is not a loader signal
        return False
    return isinstance(body, dict) and body.get("error") == PAGE_NOT_READY_ERROR


def page_not_ready_message(prefix: str, body: Any) -> str:
    """Terminal message for an exhausted budget, preserving loader diagnostics.

    Keeps the literal ``page_not_ready`` substring: auteur's
    ``selenium_test_agent/llm/code_generation.py`` routes on
    ``"page_not_ready" in str(e)`` to surface PAGE_NOT_READY_AFTER_RETRIES
    rather than a generic action failure.
    """
    loader_reason = body.get("loader_reason", "") if isinstance(body, dict) else ""
    attempts = body.get("attempts", "") if isinstance(body, dict) else ""
    return (
        f"{prefix}: {PAGE_NOT_READY_ERROR} "
        f"(loader_reason={loader_reason!r}, attempts={attempts}, "
        f"client_attempts={MAX_ATTEMPTS})"
    )


def retry_on_page_not_ready(attempt_fn: Callable[[], Any], *, label: str = "vision") -> Any:
    """Run ``attempt_fn()`` until it stops answering 409 ``page_not_ready``.

    ``attempt_fn`` MUST re-capture the screenshot on every call — retrying above
    the transport layer is only useful because attempt N+1 observes a fresh
    page.

    Returns the last response, which may still be a 409 when the budget is
    exhausted; the caller raises from the parsed body so the loader diagnostics
    survive into the step error.
    """
    response = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = attempt_fn()
        if not is_page_not_ready_response(response):
            return response
        if attempt < MAX_ATTEMPTS:
            _log.info(
                "%s :: page_not_ready (attempt %d/%d), waiting %ds and retrying "
                "with a fresh screenshot",
                label, attempt, MAX_ATTEMPTS, SLEEP_SECONDS,
            )
            time.sleep(SLEEP_SECONDS)
    _log.warning(
        "%s :: page_not_ready after %d attempts — giving up", label, MAX_ATTEMPTS
    )
    return response
