from __future__ import annotations

import asyncio
import os
import time

import httpx
from dotenv import load_dotenv
from matrx_utils import vcprint

load_dotenv()

# ── Client-side rate limiting (CONFIG, not env) ──────────────────────────────
# Pioneer's hosted GLiNER2 gateway enforces 200 requests / 60s. A large NER
# fan-out (a few-thousand-chunk PDF) bursts well past that, and because each
# 429'd call then RETRIES, the retry storm keeps the endpoint pinned over its
# budget — the request rate never drains and ~everything 429s in a loop.
#
# A Semaphore (concurrency) is the WRONG primitive: it bounds in-flight calls,
# not calls-per-minute. The correct fix is a process-wide async TOKEN BUCKET
# that refills at the provider's documented rate; EVERY call (first attempt and
# every retry) acquires a token before going out, so the steady-state request
# rate can never exceed the limit no matter how big the fan-out is.
#
# This is config — it changes behavior, so it lives here as a CAPS constant and
# a change is a code push (never an env var: a per-environment rate limit that
# silently differs between servers is exactly the failure mode we forbid).
#
# THE BURST BOUND (the bug fixed 2026-06-10). A token bucket grants at most
# ``capacity + rate × T`` tokens in any window of length T — the initial full
# bucket PLUS everything refilled during the window. The provider's limit is a
# 200-requests / 60s window, so to never exceed it we need:
#
#       BURST + (PER_MINUTE/60) × 60  ≤  200
#       BURST + PER_MINUTE           ≤  200
#
# The old config set BURST = PER_MINUTE = 180 → worst case 180 + 180 = 360/min,
# nearly DOUBLE the ceiling. At run start the bucket dumped its full 180-token
# burst immediately (the 8-way NER fan-out drained it in ~20s), kept refilling
# at 3/s, crossed 200 around ~30s, and then every call 429'd until the window
# rolled — exactly the retry-storm this bucket was meant to prevent.
#
# Correct shape: a SMALL burst so a fan-out can't front-load the window, plus a
# steady rate a touch under the ceiling for headroom against clock skew and the
# provider's own window accounting. 170 + 10 = 180 worst-case/min, a safe 20
# under 200.
FASTINO_RATE_LIMIT_PER_MINUTE: float = 170.0
# Max tokens that can accrue. MUST stay small — see the burst bound above. This
# is NOT "one window"; capacity is the front-loadable burst, and BURST +
# PER_MINUTE must remain ≤ the provider's per-minute ceiling.
FASTINO_RATE_LIMIT_BURST: float = 10.0

# Fastino's GLiNER2 models are served through Pioneer's hosted, OpenAI-compatible
# gateway (POST {base}/v1/chat/completions, Bearer auth). Despite the chat-shaped
# transport it is NOT a chat model: the request carries a `schema` (entity labels)
# and the assistant message content is a JSON string of typed spans. We call the
# HTTP API directly so we never ship the gliner2 SDK (it drags in torch).
DEFAULT_BASE_URL = "https://api.pioneer.ai"
COMPLETIONS_PATH = "v1/chat/completions"


def get_fastino_base_url() -> str:
    return (
        os.environ.get("PIONEER_API_BASE_URL")
        or os.environ.get("GLINER2_API_BASE_URL")
        or DEFAULT_BASE_URL
    ).rstrip("/")


def gliner2_url() -> str:
    return f"{get_fastino_base_url()}/{COMPLETIONS_PATH}"


def resolve_fastino_api_key() -> str:
    from matrx_ai.providers.keys import resolve_api_key

    key = resolve_api_key("PIONEER_API_KEY", "FASTINO_API_KEY")
    if not key:
        raise RuntimeError(
            "Fastino/GLiNER2 extraction requires PIONEER_API_KEY (or FASTINO_API_KEY) "
            "in the environment. Get one at https://pioneer.ai."
        )
    return key


def fastino_auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {resolve_fastino_api_key()}",
        "Content-Type": "application/json",
    }


# Per-request timeout (seconds) for the GLiNER2 endpoint. Pioneer's hosted
# gateway can cold-start a model on the first call of a session (10–30 s);
# raised 30→60 s after the 2026-06-03 incident (~9/171 chunks timed out on
# cold-start). A code-reviewed constant, not an env var. (Was MATRX_AI_FASTINO_TIMEOUT.)
FASTINO_TIMEOUT_SECONDS: float = 60.0


def _default_fastino_timeout() -> float:
    return FASTINO_TIMEOUT_SECONDS


def build_fastino_client(*, timeout: float | None = None) -> httpx.AsyncClient:
    """A fresh async client. Auth headers + URL are applied per-request (in
    FastinoExtraction), so this client is loop-safe and reusable — callers may
    pass one in to pool connections across a fan-out, or let each call open its
    own via ``async with``.

    ``timeout`` defaults to :func:`_default_fastino_timeout` when not supplied
    (the env-tunable per-call cap)."""
    effective_timeout = timeout if timeout is not None else _default_fastino_timeout()
    return httpx.AsyncClient(timeout=httpx.Timeout(effective_timeout, connect=10.0), verify=True)


class _AsyncTokenBucket:
    """A simple monotonic-clock token bucket for rate-limiting outbound calls.

    Tokens refill continuously at ``rate_per_sec`` up to ``capacity``. ``acquire``
    waits (cooperatively, releasing the event loop) until a token is available,
    then consumes one. A single ``asyncio.Lock`` serialises the refill+consume so
    concurrent fan-out callers share ONE budget. Loop-safe: the lock is created
    lazily on first use so the bucket can be a module-level singleton constructed
    before any event loop exists."""

    def __init__(self, rate_per_sec: float, capacity: float) -> None:
        self._rate = max(rate_per_sec, 0.0001)
        self._capacity = max(capacity, 1.0)
        self._tokens = self._capacity
        self._updated = time.monotonic()
        self._lock: asyncio.Lock | None = None
        self._warned = False

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._updated
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
            self._updated = now

    async def acquire(self) -> None:
        if self._lock is None:
            self._lock = asyncio.Lock()
        async with self._lock:
            while True:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                deficit = 1.0 - self._tokens
                wait_s = deficit / self._rate
                if not self._warned:
                    self._warned = True
                    vcprint(
                        f"⏳ Fastino rate limiter ACTIVE — throttling outbound "
                        f"GLiNER2 calls to {self._rate * 60:.0f}/min so the fan-out "
                        f"stops tripping the provider's 429. Queued ~{wait_s:.1f}s.",
                        color="yellow",
                        verbose=True,
                    )
                await asyncio.sleep(wait_s)


# Process-wide singleton: one shared budget across every Fastino caller and
# every retry, so the aggregate request rate is bounded no matter the fan-out.
_RATE_LIMITER = _AsyncTokenBucket(
    rate_per_sec=FASTINO_RATE_LIMIT_PER_MINUTE / 60.0,
    capacity=FASTINO_RATE_LIMIT_BURST,
)


async def acquire_fastino_slot() -> None:
    """Block (cooperatively) until the shared rate limiter grants a token.

    Called once before EACH outbound GLiNER2 request — including retries — so a
    retry storm can never push the aggregate rate over the provider's ceiling."""
    await _RATE_LIMITER.acquire()
