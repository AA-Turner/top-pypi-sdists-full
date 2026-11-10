"""How Probe stops one Miles try on the engines (W30 spike M1, M2): each `/generate` request of a running try carries
the request id `probe:{process}:{attempt}:{n}` (Miles sends none, `generate_endpoint_utils.py:102-108`), and a cancel or
retry is `POST {engine}/abort_request {"rid": "probe:{process}:{attempt}:", "prefix": true}` to every engine behind
Miles' router (as Miles' own abort, `inference_rollout_train.py:28-44`). SGLang then ends those requests with
`finish_reason: abort`."""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .rollout import Rollout

log = logging.getLogger(__name__)

#: The try running in this asyncio task (set by `ProbeGenerate`, read by the stamped `post` and the session wrap).
CURRENT: ContextVar[Rollout | None] = ContextVar("probe_miles_rollout", default=None)
#: An abort is sent again this often while a stopped try's request still runs (it may not have reached the engine).
ABORT_REPEAT_S = 0.5
ABORT_TRIES = 20
ENGINE_TIMEOUT_S = 5.0
#: Miles' router's engine list is read again after this long (an engine may be replaced).
ENGINES_TTL_S = 10.0
#: Miles' `post` defaults (`http_utils.py:436`, `_post` `:218-256`): tries and the wait between them.
MILES_MAX_RETRIES = 60
MILES_RETRY_SLEEP_S = 1.0


def to_engine_urls(urls: list[str]) -> list[str]:
    """Each engine once: the `@<rank>` suffix dp-aware routing adds is dropped (`http_utils.py:130-139`)."""
    found: list[str] = []
    for url in urls:
        base, sep, rank = str(url).rpartition("@")
        if sep and rank.isdigit():
            url = base
        if url not in found:
            found.append(url)
    return found


class EngineAborter:
    """Aborts a try's requests on every engine behind Miles' router. Blocking (a thread, never the rollout's loop)."""

    def __init__(self) -> None:
        self._engines: dict[str, tuple[float, list[str]]] = {}
        self._lock = threading.Lock()

    def abort(self, router: str, prefix: str) -> int:
        """Engines that answered. Never raises: an engine that cannot be reached is logged."""
        import httpx

        from probe.foundation.tls.tls import ssl_context

        answered = 0
        try:
            engines = self._get_engines(router)
        except Exception as exc:  # noqa: BLE001 -- the next repeat tries again
            log.debug("probe: Miles' router %s gave no engine list: %s", router, exc)
            return 0
        with httpx.Client(timeout=ENGINE_TIMEOUT_S, verify=ssl_context()) as client:
            for engine in engines:
                try:
                    client.post(f"{engine}/abort_request", json={"rid": prefix, "prefix": True}).raise_for_status()
                    answered += 1
                except Exception as exc:  # noqa: BLE001 -- one engine down never stops the others' aborts
                    log.debug("probe: engine %s did not take the abort of %s: %s", engine, prefix, exc)
        return answered

    def _get_engines(self, router: str) -> list[str]:
        import httpx

        from probe.foundation.tls.tls import ssl_context

        with self._lock:
            cached = self._engines.get(router)
        if cached is not None and time.monotonic() - cached[0] < ENGINES_TTL_S:
            return cached[1]
        answer = httpx.get(f"{router}/workers", timeout=ENGINE_TIMEOUT_S, verify=ssl_context())
        answer.raise_for_status()
        engines = to_engine_urls([worker["url"] for worker in answer.json().get("workers") or ()])
        with self._lock:
            self._engines[router] = (time.monotonic(), engines)
        return engines


class RidStamp:
    """Miles' `http_utils.post`, with the running try's request id on each `/generate` it sends, and an abort of that
    request when a command stops the try. Generate functions bind `post` by name (`single_turn.py:12`,
    `multi_turn.py:22`), so `stamp(generate)` repoints the one their module holds."""

    def __init__(self, aborter: EngineAborter, on_request: Callable[[Rollout], None],
                 on_reply: Callable[[Rollout, Any], None]) -> None:  # fmt: skip
        self._aborter = aborter
        self._on_request = on_request
        self._on_reply = on_reply
        self._original: Callable[..., Awaitable[Any]] | None = None
        self.post = self._make_post()

    @property
    def is_installed(self) -> bool:
        return self._original is not None

    def install(self, module: Any) -> None:
        """Wrap `module.post` (`miles.utils.http_utils`): Miles' own `post` underneath, an earlier stamp's unwrapped."""
        current = _unwrap(getattr(module, "post", None))
        if callable(current):
            self._original = current
            self.post.__probe_original__ = current  # type: ignore[attr-defined]
            module.post = self.post

    def stamp(self, generate: Any) -> bool:
        """Make ``generate``'s module-global `post` the stamped one; True when its requests carry the id."""
        if self._original is None:
            try:
                import miles.utils.http_utils as http_utils
            except ImportError:
                return False
            self.install(http_utils)
        namespace = find_globals(generate)
        if namespace is None:
            return False
        bound = namespace.get("post")
        if bound is not self.post and callable(bound) and _unwrap(bound) is self._original:
            namespace["post"] = self.post
        return namespace.get("post") is self.post or namespace.get("http_utils") is not None

    def _make_post(self) -> Callable[..., Awaitable[Any]]:
        async def post(url, payload, max_retries=MILES_MAX_RETRIES, action="post", headers=None):
            original = self._original
            rollout = CURRENT.get()
            if (rollout is None or rollout.is_agent or not isinstance(payload, dict) or "rid" in payload
                    or not str(url).endswith("/generate")):  # fmt: skip
                return await original(url, payload, max_retries, action=action, headers=headers)
            _call_quietly(self._on_request, rollout)
            output = await self._post_with_rids(rollout, url, payload, max_retries, action, headers)
            _call_quietly(self._on_reply, rollout, output)
            return output

        post.__probe_wrapped__ = True  # type: ignore[attr-defined]
        return post

    async def _post_with_rids(self, rollout: Rollout, url: str, payload: dict, max_retries: int, action: str,
                              headers: Any) -> Any:  # fmt: skip
        """Miles' retries (`_post`, `http_utils.py:218-256`: any error but a 4xx other than 408 / 429, 1 s apart, up to
        ``max_retries``), each send with a new request id: SGLang refuses an id it still runs ("Duplicate request ID",
        `tokenizer_manager.py:4100-4103`), and a dropped connection leaves the first send running there."""
        import httpx

        for attempt in range(1, max(int(max_retries or 1), 1) + 1):
            stamped = {**payload, "rid": rollout.take_rid()}
            try:
                return await self._send(rollout, self._original(url, stamped, 1, action=action, headers=headers))
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if (400 <= status < 500 and status not in (408, 429)) or attempt >= max_retries:
                    raise
            except Exception:
                if attempt >= max_retries:
                    raise
            await asyncio.sleep(MILES_RETRY_SLEEP_S)
        raise RuntimeError("unreachable: the last send raises")

    async def _send(self, rollout: Rollout, call: Awaitable[Any]) -> Any:
        """The request, aborted on the engines once its try is asked to stop (again while it still runs: an abort can
        land before the engine has the request). Cancelling this cancels the request, as a plain call would."""
        task = asyncio.ensure_future(call)
        waiter = asyncio.ensure_future(rollout.stopping.wait())
        try:
            await asyncio.wait({task, waiter}, return_when=asyncio.FIRST_COMPLETED)
            tries = 0
            while not task.done() and rollout.router and tries < ABORT_TRIES:
                tries += 1
                await asyncio.to_thread(self._aborter.abort, rollout.router, rollout.rid_prefix)
                await asyncio.wait({task}, timeout=ABORT_REPEAT_S)
            return await task
        finally:
            waiter.cancel()
            if not task.done():
                task.cancel()


def _unwrap(post: Any) -> Any:
    """Miles' own `post` under any stamp a process installed before (`__probe_original__`)."""
    while callable(post) and getattr(post, "__probe_original__", None) is not None:
        post = post.__probe_original__
    return post


def find_globals(generate: Any) -> dict | None:
    """The module namespace a generate function runs in: a function's, a Miles legacy adapter's (`.fn`), or a class
    instance's `__call__`."""
    for candidate in (generate, getattr(generate, "fn", None), getattr(type(generate), "__call__", None)):
        namespace = getattr(candidate, "__globals__", None)
        if isinstance(namespace, dict):
            return namespace
    return None


def _call_quietly(call: Callable[..., Any], *args: Any) -> None:
    try:
        call(*args)
    except Exception as exc:  # noqa: BLE001 -- progress is never worth a request
        log.debug("probe: a Miles request note failed: %s", exc)
