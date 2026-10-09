"""Client-owned retry for automind's ``page_not_ready`` (HTTP 409) answer.

The VQE does **not** retry internally. When the vision model reports an active
loader, ``auteur-automind`` returns ``{"error": "page_not_ready", ...}``
(``app/services/vqe_service.py``) and the heal route maps it to **409** with an
explicit contract (``app/api/endpoints/healer.py``)::

    # 409 is pragmatic (outside tenacity's 5xx retry set) — client
    # owns the retry loop; do NOT switch this to a 5xx.

Retrying inside the HTTP layer would re-POST the *same stale screenshot* and
could never observe a settled page, so the budget has to wrap the screenshot
capture — which is what :func:`retry_on_page_not_ready` does.

Port of the V2 source
(``_is_page_not_ready_response`` + the ``Heal.vision_query`` loop): 3 POSTs,
3s between them, a fresh screenshot and a fresh ``request_id`` every attempt.
Async twin of ``testmu_selenium/_helpers/_page_ready.py``.
"""
from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any, Awaitable, Callable, Optional

_log = logging.getLogger("testmu.page_ready")

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


def is_page_not_ready_body(body: Any) -> bool:
    """True when a parsed heal response carries the loader signal.

    The status check lives in the HTTP layer (``_post_v3_vision``), which
    returns the 409 body verbatim instead of raising so this discriminator can
    run over the parsed dict.
    """
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


async def retry_on_page_not_ready(
    attempt_fn: Callable[[], Awaitable[Any]],
    *,
    label: str = "vision",
) -> Optional[Any]:
    """Await ``attempt_fn()`` until it stops answering ``page_not_ready``.

    ``attempt_fn`` MUST re-capture the screenshot on every call — retrying above
    the transport layer is only useful because attempt N+1 observes a fresh
    page.

    Returns the last parsed body, which may still carry the loader error when
    the budget is exhausted; the caller raises from it so ``loader_reason``
    survives into the step error.
    """
    result = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        result = await attempt_fn()
        if not is_page_not_ready_body(result):
            return result
        if attempt < MAX_ATTEMPTS:
            _log.info(
                "%s :: page_not_ready (attempt %d/%d), waiting %ds and retrying "
                "with a fresh screenshot",
                label, attempt, MAX_ATTEMPTS, SLEEP_SECONDS,
            )
            await asyncio.sleep(SLEEP_SECONDS)
    _log.warning(
        "%s :: page_not_ready after %d attempts — giving up", label, MAX_ATTEMPTS
    )
    return result
