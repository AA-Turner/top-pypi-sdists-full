"""Host-injected tool source — tool-registry rows without the ORM.

A client host (no Postgres — matrx-local) gets its ``tool.definition`` rows
through this seam instead of the host-injected ORM base. Mirrors the
``ModelCatalog`` design (``matrx_ai.catalog.host_catalog``): a tiny Protocol,
a structural validator, and a ``get_*`` accessor the registry checks BEFORE
the ORM path.

Two ways a host gets a tool source:

1. **Explicit** — ``matrx_ai.configure(tool_source=MySource())`` where the
   object implements :class:`ToolSource` (``async list_tools() ->
   list[dict]``, rows in the ``tool.definition`` ``to_dict()`` shape).
2. **Derived (server-backed)** — when ``configure(server_url=...,
   source_app=...)`` is set and no explicit ``tool_source`` was given,
   :func:`get_tool_source` builds a :class:`ServerToolSource` that GETs
   ``{server_url}/ai-tools/app/{source_app}/all`` (the same route
   matrx-local's tool_sync verifies against), sending the current JWT from
   ``get_jwt`` when one is configured. This is the "server-backed tool
   registry fetch" the ``configure()`` docstring promises.

``ToolRegistry.load_from_database()`` checks this seam first; the ORM base
is never touched when a source is available — so a client host boots with
ZERO ``DBNotConfiguredError`` from the tool system.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from matrx_utils import vcprint

from matrx_ai._ext import get_ext, has_ext

#: The _ext registry key under which an explicit tool source is registered.
TOOL_SOURCE_KEY = "tool_source"

#: Methods a ToolSource must implement (validation + structural check).
TOOL_SOURCE_METHODS: tuple[str, ...] = ("list_tools",)


@runtime_checkable
class ToolSource(Protocol):
    """Host-implemented tool-definition source for client-host installs."""

    async def list_tools(self) -> list[dict[str, Any]]:
        """Return every active tool row (``tool.definition`` ``to_dict()`` shape)."""
        ...


def missing_tool_source_methods(candidate: Any) -> list[str]:
    """Return the ToolSource method names ``candidate`` lacks."""
    return [
        name
        for name in TOOL_SOURCE_METHODS
        if not callable(getattr(candidate, name, None))
    ]


class ToolSourceFetchError(RuntimeError):
    """A server-backed tool fetch failed (network / HTTP / payload shape)."""


class ServerToolSource:
    """Fetch this app's tool definitions from the AIDream server registry.

    GET ``{server_url}/ai-tools/app/{source_app}/all`` — a public route; the
    JWT (when a ``get_jwt`` seam is configured) is still sent so the fetch
    keeps working if the route ever gains auth. The route accepts both
    underscore and hyphen executor spellings (``matrx_local`` /
    ``matrx-local``) server-side.
    """

    def __init__(
        self,
        server_url: str,
        source_app: str,
        get_jwt: Any = None,
        *,
        # A desktop host awaits this fetch inside its boot lifespan — a
        # black-holed network must not stall app startup for long. 8s is
        # generous for one JSON GET; offline boots fall back to the host's
        # bundled catalog.
        timeout_seconds: float = 8.0,
    ) -> None:
        self._base = server_url.rstrip("/")
        self._source_app = source_app.strip()
        self._get_jwt = get_jwt
        self._timeout = timeout_seconds
        self._fetched = False
        self._rows: list[dict[str, Any]] = []
        self._executor_name = self._source_app.replace("_", "-")

    @property
    def url(self) -> str:
        from urllib.parse import quote

        return f"{self._base}/ai-tools/app/{quote(self._source_app, safe='')}/all"

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if callable(self._get_jwt):
            try:
                token = self._get_jwt()
            except Exception as exc:  # noqa: BLE001 — an expired token cache must not kill the fetch
                vcprint(
                    f"[ServerToolSource] get_jwt() raised ({exc!r}); fetching without auth",
                    color="yellow",
                )
                token = None
            import inspect

            if inspect.iscoroutine(token):
                # An async get_jwt slipped past validation — never send
                # "Bearer <coroutine ...>". Close it (silences the
                # never-awaited warning) and fetch anonymously.
                token.close()
                vcprint(
                    "[ServerToolSource] get_jwt is async (returned a coroutine) — "
                    "the seam requires a SYNC zero-arg callable. Fetching without "
                    "auth; fix the host's configure(get_jwt=...).",
                    color="red",
                )
                token = None
            if token:
                headers["Authorization"] = f"Bearer {token}"
        return headers

    async def list_tools(self) -> list[dict[str, Any]]:
        import httpx

        try:
            async with httpx.AsyncClient(
                timeout=self._timeout, follow_redirects=True
            ) as client:
                resp = await client.get(self.url, headers=self._headers())
        except httpx.HTTPError as exc:
            raise ToolSourceFetchError(
                f"tool registry fetch failed: GET {self.url} → {type(exc).__name__}: {exc}"
            ) from exc
        if resp.status_code != 200:
            raise ToolSourceFetchError(
                f"tool registry fetch failed: GET {self.url} → HTTP {resp.status_code}: "
                f"{resp.text[:500]}"
            )
        try:
            payload = resp.json()
        except ValueError as exc:
            raise ToolSourceFetchError(
                f"tool registry fetch returned non-JSON: GET {self.url}: {exc}"
            ) from exc
        tools = payload.get("tools") if isinstance(payload, dict) else None
        if not isinstance(tools, list):
            raise ToolSourceFetchError(
                f"tool registry fetch returned an unexpected shape (no 'tools' list): "
                f"GET {self.url} → keys={sorted(payload) if isinstance(payload, dict) else type(payload).__name__}"
            )
        rows = [row for row in tools if isinstance(row, dict)]
        resolved_executor = payload.get("executor_name")
        if isinstance(resolved_executor, str) and resolved_executor.strip():
            self._executor_name = resolved_executor.strip()
        self._rows = rows
        self._fetched = True
        vcprint(
            f"[ServerToolSource] fetched {len(rows)} tool definition(s) for "
            f"app '{self._source_app}' from {self._base}",
            color="green",
        )
        return rows

    async def list_bindings(self) -> list[dict[str, str]]:
        """Synthesize bindings from the executor-filtered registry response.

        The endpoint already returns only definitions joined through active
        bindings for one executor. Preserve that routing fact for client hosts
        so discovery tools and executor resolution see the same contract as
        the server-side ORM registry.
        """
        if not self._fetched:
            await self.list_tools()
        return [
            {"tool_id": str(row["id"]), "executor_name": self._executor_name}
            for row in self._rows
            if row.get("id")
        ]

    async def list_executors(self) -> list[dict[str, Any]]:
        """Expose the filtered app executor for client-side route matching."""
        if not self._fetched:
            await self.list_tools()
        return [
            {
                "name": self._executor_name,
                "parent_executor_name": None,
                "is_active": True,
            }
        ]


def get_tool_source() -> ToolSource | None:
    """Return the effective tool source, or None (→ the ORM path runs).

    Resolution order:
      1. An explicit ``configure(tool_source=...)`` seam.
      2. A derived :class:`ServerToolSource` when BOTH ``server_url`` and
         ``source_app`` are configured (client-host server-backed fetch).
      3. None — server hosts (no client seams) load through the ORM base.
    """
    if has_ext(TOOL_SOURCE_KEY):
        source = get_ext(TOOL_SOURCE_KEY)
        if source is not None:
            return source
    if has_ext("server_url") and has_ext("source_app"):
        server_url = get_ext("server_url")
        source_app = get_ext("source_app")
        if server_url and source_app:
            return ServerToolSource(
                str(server_url),
                str(source_app),
                get_ext("get_jwt") if has_ext("get_jwt") else None,
            )
    return None


__all__ = [
    "TOOL_SOURCE_KEY",
    "TOOL_SOURCE_METHODS",
    "ServerToolSource",
    "ToolSource",
    "ToolSourceFetchError",
    "get_tool_source",
    "missing_tool_source_methods",
]
