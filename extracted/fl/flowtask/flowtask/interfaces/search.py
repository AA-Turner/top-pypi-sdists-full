"""Search interface for OpenSearch/Elasticsearch using asyncdb's elastic driver.

ES 7.10 note
------------
Against an ES 7.10 cluster always use ``backend="opensearch"``.
opensearch-py 3.1.0 (hard-pinned by ai-parrot) is fully compatible because
OpenSearch forked from ES 7.10.2.  The installed elasticsearch 8.15.1 client
targets ES 8 only and will fail against a 7.x cluster.

Pagination strategy (capability-aware)
--------------------------------------
* ``scroll`` (default): works on every supported cluster — ES 7.10, ES 8.x and
  OpenSearch. This is the safe, snapshot-consistent choice.
* ``search_after``: the strategy is chosen from the cluster's capabilities,
  resolved once at connect via ``client.info()``:
    - OpenSearch ≥2.4 / Elasticsearch ≥7.12 → PIT + ``_shard_doc`` tiebreaker.
    - Elasticsearch 7.10 → plain ``search_after`` (no PIT, no ``_shard_doc``);
      the query MUST carry a deterministic ``sort`` with a unique tiebreaker,
      otherwise a ``ComponentError`` is raised telling the user to add one or
      use ``scroll``.
  A user-provided ``sort`` is always honoured and never overwritten.
"""
from __future__ import annotations

from typing import Any, Optional

from navconfig.logging import logging
from asyncdb import AsyncDB
from asyncdb.exceptions import DriverError

from .client import ClientInterface
from ..exceptions import ComponentError


_VALID_BACKENDS: frozenset[str] = frozenset({"opensearch", "elasticsearch"})

# Silence the very chatty transport loggers that dump full request/response
# bodies (huge on scroll pages), so even a --debug run stays focused on the
# pagination progress. Mirrors Boto3Client's handling of boto3/urllib3.
for _noisy in (
    "opensearch", "opensearchpy", "elasticsearch",
    "elastic_transport", "urllib3", "urllib3.connectionpool",
):
    logging.getLogger(_noisy).setLevel(logging.WARNING)


class SearchInterface(ClientInterface):
    """Async client mixin for OpenSearch/Elasticsearch with full-result pagination.

    Wraps asyncdb's ``elastic`` driver for connection/auth and adds multi-page
    scroll and search_after pagination — since the driver's single
    ``query()``/``fetchall()`` only returns the first page.

    Credentials schema
    ------------------
    host        – server hostname (``https://``/``http://`` prefix stripped)
    port        – server port (default 9200)
    username    – HTTP-Basic user (mapped to ``user`` in asyncdb params)
    password    – HTTP-Basic password
    protocol    – ``http`` or ``https`` (default ``http``)
    backend     – ``opensearch`` (default) or ``elasticsearch``
    use_ssl     – enable TLS (bool, default ``False``)
    verify_certs – verify TLS certificates (bool, default ``False``)
    """

    _credentials: dict = {
        "host": str,
        "port": int,
        "username": str,
        "password": str,
        "protocol": str,
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.backend: str = kwargs.pop("backend", "opensearch")
        self.use_ssl: bool = bool(kwargs.pop("use_ssl", False))
        self.verify_certs: bool = bool(kwargs.pop("verify_certs", False))
        self._db: Optional[Any] = None
        self._active_scroll_id: Optional[str] = None
        self._active_pit_id: Optional[str] = None
        # Cluster capabilities, resolved at connect time via client.info().
        # Conservative defaults: assume the oldest target (ES 7.10) until proven
        # otherwise — no PIT, no _shard_doc tiebreaker.
        self._supports_pit: bool = False
        self._supports_shard_doc: bool = False
        self._engine_label: str = "unknown"
        # Fallback logger for standalone use (tests, scripts).
        # LogSupport sets self._logger before calling super(), so the guard
        # avoids overwriting the component-level logger when mixed in.
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger("FlowTask.Interface.Search")
        super().__init__(*args, **kwargs)

    def processing_credentials(self) -> None:
        """Resolve credentials, seed host/port, and validate backend.

        ``ClientInterface`` does not auto-call ``define_host()``, so ``self.host``
        and ``self.port`` start as ``None``.  We seed them from the credentials
        dict *before* delegating to the base resolver — otherwise the base
        resolver, seeing ``self.port is None`` as the default, blanks an int
        credential to ``None`` (navconfig ``getint()`` rejects an int key), and
        ``open()`` ends up with no port.
        """
        if self.credentials:
            if self.credentials.get("host") is not None:
                self.host = self.credentials["host"]
            if self.credentials.get("port") is not None:
                self.port = self.credentials["port"]
        super().processing_credentials()
        # Restore concrete host/port if the base resolver blanked them.
        if self.credentials:
            self.host = self.credentials.get("host") or self.host
            self.port = self.credentials.get("port") or self.port
        self.backend = (
            self.credentials.pop("backend", None) or self.backend or "opensearch"
        )
        if self.backend not in _VALID_BACKENDS:
            raise ComponentError(
                f"SearchInterface: invalid backend {self.backend!r}. "
                f"Valid choices: {sorted(_VALID_BACKENDS)}"
            )
        self.use_ssl = bool(self.credentials.pop("use_ssl", self.use_ssl))
        self.verify_certs = bool(
            self.credentials.pop("verify_certs", self.verify_certs)
        )

    async def open(
        self,
        host: str = None,
        port: int = None,
        credentials: dict = None,
        **kwargs: Any,
    ) -> "SearchInterface":
        """Open the asyncdb elastic driver and establish a connection.

        Args:
            host: Override the host from credentials.
            port: Override the port from credentials.
            credentials: Credential dict (falls back to ``self.credentials``).

        Returns:
            self

        Raises:
            ComponentError: On driver or connection failure.
        """
        creds = credentials or self.credentials or {}
        # None-safe resolution: a credential key may exist with a None value
        # (the base resolver can blank it), so chain through to a real default
        # instead of trusting dict defaults.
        raw_host = str(host or creds.get("host") or self.host or "localhost")
        # asyncdb builds DSN from protocol+host+port; strip any prefix.
        raw_host = raw_host.removeprefix("https://").removeprefix("http://")
        protocol = creds.get("protocol") or ("https" if self.use_ssl else "http")

        params: dict = {
            "host": raw_host,
            "port": int(port or creds.get("port") or self.port or 9200),
            "protocol": protocol,
            "db": creds.get("db", "default"),
            # asyncdb pops 'user' and 'password' from params in __init__
            "user": creds.get("username") or creds.get("user", ""),
            "password": creds.get("password", ""),
        }

        try:
            self._db = AsyncDB(
                "elastic",
                params=params,
                client_type=self.backend,
                use_ssl=self.use_ssl,
                verify_certs=self.verify_certs,
            )
            await self._db.connection()
            self._connection = self._db._connection
            await self._detect_capabilities(self._connection)
            self._logger.info(
                "SearchInterface: connected via %s to %s://%s:%s",
                self.backend, protocol, raw_host, params["port"],
            )
        except DriverError as exc:
            raise ComponentError(
                f"SearchInterface: connection failed — {exc}"
            ) from exc
        except Exception as exc:
            raise ComponentError(
                f"SearchInterface: unexpected error on open: {exc}"
            ) from exc

        return self

    async def open_search_client(self) -> None:
        """Open the client (explicit lifecycle alias for ``open``)."""
        await self.open(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
        )

    async def _detect_capabilities(self, client: Any) -> None:
        """Resolve cluster capabilities (PIT, ``_shard_doc``) via ``info()``.

        Sets ``self._supports_pit`` and ``self._supports_shard_doc`` so
        ``search_after`` can pick the right strategy per cluster:

        * OpenSearch ≥ 2.4 (opensearch-py): PIT via ``create_pit`` + ``_shard_doc``.
        * Elasticsearch ≥ 7.12 (elasticsearch client): PIT via
          ``open_point_in_time`` + ``_shard_doc``.
        * Elasticsearch 7.10 (reached with the opensearch-py client): NO usable
          PIT (endpoint differs) and NO ``_shard_doc`` (added in 7.12) → plain
          ``search_after`` requiring a user-provided deterministic ``sort``.

        On any detection failure, defaults stay conservative (no PIT / no
        ``_shard_doc``) so behaviour degrades safely rather than failing at
        query time.
        """
        self._supports_pit = False
        self._supports_shard_doc = False
        try:
            info = await client.info()
        except Exception as exc:  # noqa: BLE001
            self._logger.warning(
                "SearchInterface: capability detection failed (%s); "
                "assuming no PIT / no _shard_doc.", exc
            )
            return

        version = (info or {}).get("version", {}) or {}
        number = str(version.get("number", ""))
        distribution = version.get("distribution")  # "opensearch" or absent (ES)
        try:
            parts = number.split(".")
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0
        except (ValueError, IndexError):
            major = minor = 0

        if distribution == "opensearch":
            self._engine_label = f"opensearch {number}"
            self._supports_pit = (major, minor) >= (2, 4)
            self._supports_shard_doc = major >= 2
        else:
            self._engine_label = f"elasticsearch {number}"
            # ES PIT (open_point_in_time) is only reachable with the
            # elasticsearch client; against ES 7.10 we use the opensearch-py
            # client whose PIT endpoint does not exist on that engine.
            self._supports_pit = (
                self.backend == "elasticsearch" and (major, minor) >= (7, 10)
            )
            self._supports_shard_doc = (major, minor) >= (7, 12)

        self._logger.info(
            "SearchInterface: cluster %s — PIT=%s, _shard_doc=%s",
            self._engine_label, self._supports_pit, self._supports_shard_doc,
        )

    async def close(self, timeout: int = 5) -> None:
        """Close any active scroll/PIT context and the underlying connection."""
        await self.close_search_client()

    async def close_search_client(self) -> None:
        """Release any open scroll context or PIT, then close the driver."""
        client = self._connection
        if client is None:
            return

        if self._active_scroll_id:
            try:
                await self._clear_scroll(client, self._active_scroll_id)
            except Exception as exc:  # noqa: BLE001
                self._logger.warning(
                    "SearchInterface: failed to clear scroll: %s", exc
                )
            finally:
                self._active_scroll_id = None

        if self._active_pit_id:
            try:
                await self._close_pit(client, self._active_pit_id)
            except Exception as exc:  # noqa: BLE001
                self._logger.warning(
                    "SearchInterface: failed to close PIT: %s", exc
                )
            finally:
                self._active_pit_id = None

        if self._db is not None:
            try:
                await self._db.close()
            except Exception as exc:  # noqa: BLE001
                self._logger.warning(
                    "SearchInterface: error closing driver: %s", exc
                )
            finally:
                self._db = None
                self._connection = None

    # ── Pagination ────────────────────────────────────────────────────────────

    async def paginate(
        self,
        index: str,
        query: dict,
        *,
        mode: str = "scroll",
        size: int = 5000,
        scroll: str = "2m",
        max_documents: Optional[int] = None,
        raw_hits: bool = False,
    ) -> list[dict]:
        """Retrieve all matching documents using multi-page pagination.

        Args:
            index: Index name (or comma-separated indices) to search.
            query: Elasticsearch/OpenSearch JSON DSL query body.
            mode: ``"scroll"`` (default) or ``"search_after"`` (PIT-based).
            size: Number of documents per page.
            scroll: Scroll/PIT keep-alive TTL (e.g. ``"2m"``).
            max_documents: Cap total documents returned; ``None`` means no cap.
            raw_hits: When ``True``, return full hit objects (with ``_id``,
                ``_index``, ``_score``, ``_source``); when ``False`` (default)
                return only ``_source`` dicts.

        Returns:
            List of dicts from all matching documents.

        Raises:
            ComponentError: On connection or query failure.
            ValueError: For an unknown ``mode`` value.
        """
        if mode not in ("scroll", "search_after"):
            raise ValueError(
                f"Unknown pagination mode {mode!r}; "
                "choose 'scroll' or 'search_after'."
            )
        client = self._connection
        if client is None:
            raise ComponentError(
                "SearchInterface.paginate: client is not connected. "
                "Call open() or open_search_client() first."
            )
        if mode == "scroll":
            return await self._paginate_scroll(
                client, index, query, size, scroll, max_documents, raw_hits
            )
        return await self._paginate_search_after(
            client, index, query, size, scroll, max_documents, raw_hits
        )

    async def _paginate_scroll(
        self,
        client: Any,
        index: str,
        query: dict,
        size: int,
        scroll_ttl: str,
        max_documents: Optional[int],
        raw_hits: bool = False,
    ) -> list[dict]:
        docs: list[dict] = []
        scroll_id: Optional[str] = None
        page = 0

        def _extract(hit: dict) -> dict:
            return hit if raw_hits else hit.get("_source", {})

        try:
            response = await client.search(
                index=index,
                body={**query, "size": size},
                scroll=scroll_ttl,
            )
            scroll_id = response.get("_scroll_id")
            self._active_scroll_id = scroll_id
            hits = response.get("hits", {}).get("hits", [])
            page = 1
            docs.extend(_extract(h) for h in hits)
            self._logger.info(
                "SearchInterface[scroll]: page %d → %d docs (total %d)",
                page, len(hits), len(docs),
            )

            while hits:
                if max_documents is not None and len(docs) >= max_documents:
                    break
                response = await self._scroll(client, scroll_id, scroll_ttl)
                scroll_id = response.get("_scroll_id", scroll_id)
                self._active_scroll_id = scroll_id
                hits = response.get("hits", {}).get("hits", [])
                if not hits:
                    break
                page += 1
                docs.extend(_extract(h) for h in hits)
                # Progress every 10 pages (avoids flooding on big windows).
                if page % 10 == 0:
                    self._logger.info(
                        "SearchInterface[scroll]: page %d → +%d docs (total %d)",
                        page, len(hits), len(docs),
                    )

        except ComponentError:
            raise
        except Exception as exc:
            raise ComponentError(
                f"SearchInterface: scroll pagination error: {exc}"
            ) from exc
        finally:
            if scroll_id:
                try:
                    await self._clear_scroll(client, scroll_id)
                except Exception as exc:  # noqa: BLE001
                    self._logger.warning(
                        "SearchInterface: clear_scroll failed in cleanup: %s", exc
                    )
                self._active_scroll_id = None

        if max_documents is not None and len(docs) > max_documents:
            self._logger.warning(
                "SearchInterface: result truncated to %d (fetched %d)",
                max_documents,
                len(docs),
            )
            docs = docs[:max_documents]

        self._logger.info(
            "SearchInterface: scroll complete — %d documents in %d page(s)",
            len(docs), page,
        )
        return docs

    def _resolve_search_after_sort(self, query: dict) -> list:
        """Pick the sort used for ``search_after``, with a unique tiebreaker.

        Order of preference:
        1. The user's ``sort`` in the query (assumed to carry a unique
           tiebreaker) — never overwritten.
        2. ``_shard_doc`` when the cluster supports it (ES ≥7.12 / OpenSearch).
        3. Otherwise raise ``ComponentError`` — on ES 7.10 there is no automatic
           tiebreaker, so the caller MUST provide a deterministic ``sort`` (or
           use ``pagination='scroll'``).
        """
        user_sort = query.get("sort")
        if user_sort:
            return user_sort
        if self._supports_shard_doc:
            return [{"_shard_doc": "asc"}]
        raise ComponentError(
            "SearchInterface: pagination='search_after' on this cluster "
            f"({self._engine_label}) has no automatic tiebreaker (_shard_doc "
            "requires Elasticsearch >= 7.12 / OpenSearch). Provide a deterministic "
            "'sort' with a unique tiebreaker in the query, e.g. "
            '[{"@timestamp": "asc"}, {"_id": "asc"}], or use pagination=\'scroll\'.'
        )

    async def _paginate_search_after(
        self,
        client: Any,
        index: str,
        query: dict,
        size: int,
        keep_alive: str,
        max_documents: Optional[int],
        raw_hits: bool = False,
    ) -> list[dict]:
        docs: list[dict] = []
        pit_id: Optional[str] = None

        def _extract(hit: dict) -> dict:
            return hit if raw_hits else hit.get("_source", {})

        # Resolve the sort (may raise ComponentError on ES 7.10 without a sort).
        sort = self._resolve_search_after_sort(query)
        # Never mutate the caller's query dict; rebuild without its sort key.
        base_body = {k: v for k, v in query.items() if k != "sort"}
        use_pit = self._supports_pit

        try:
            if use_pit:
                pit_id = await self._open_pit(client, index, keep_alive)
                self._active_pit_id = pit_id
            search_after: Optional[list] = None

            while True:
                if max_documents is not None and len(docs) >= max_documents:
                    break

                body: dict = {**base_body, "size": size, "sort": sort}
                if search_after is not None:
                    body["search_after"] = search_after

                if use_pit:
                    response = await self._search_with_pit(
                        client, body, pit_id, keep_alive
                    )
                    pit_id = response.get("pit_id", pit_id)
                    self._active_pit_id = pit_id
                else:
                    # ES 7.10 path: plain search_after, no PIT.
                    response = await client.search(index=index, body=body)

                hits = response.get("hits", {}).get("hits", [])
                if not hits:
                    break
                docs.extend(_extract(h) for h in hits)
                next_cursor = hits[-1].get("sort")
                if next_cursor is None:
                    self._logger.warning(
                        "SearchInterface: hits lack 'sort' values; cannot advance "
                        "search_after cursor — stopping after %d docs.", len(docs)
                    )
                    break
                search_after = next_cursor

        except ComponentError:
            raise
        except Exception as exc:
            raise ComponentError(
                f"SearchInterface: search_after pagination error: {exc}"
            ) from exc
        finally:
            if pit_id:
                try:
                    await self._close_pit(client, pit_id)
                except Exception as exc:  # noqa: BLE001
                    self._logger.warning(
                        "SearchInterface: close_pit failed in cleanup: %s", exc
                    )
                self._active_pit_id = None

        if max_documents is not None and len(docs) > max_documents:
            self._logger.warning(
                "SearchInterface: result truncated to %d (fetched %d)",
                max_documents,
                len(docs),
            )
            docs = docs[:max_documents]

        self._logger.info(
            "SearchInterface: search_after complete — %d documents", len(docs)
        )
        return docs

    # ── Backend-specific helpers ───────────────────────────────────────────────

    async def _scroll(self, client: Any, scroll_id: str, scroll_ttl: str) -> dict:
        if self.backend == "opensearch":
            return await client.scroll(
                body={"scroll_id": scroll_id, "scroll": scroll_ttl}
            )
        return await client.scroll(scroll_id=scroll_id, scroll=scroll_ttl)

    async def _clear_scroll(self, client: Any, scroll_id: str) -> None:
        if self.backend == "opensearch":
            await client.clear_scroll(body={"scroll_id": [scroll_id]})
        else:
            await client.clear_scroll(scroll_id=scroll_id)

    async def _open_pit(self, client: Any, index: str, keep_alive: str) -> str:
        if self.backend == "opensearch":
            # keep_alive is a query parameter for opensearch-py
            response = await client.create_pit(
                index=index, params={"keep_alive": keep_alive}
            )
            return response.get("pit_id") or response.get("id", "")
        response = await client.open_point_in_time(
            index=index, keep_alive=keep_alive
        )
        return response.get("id", "")

    async def _close_pit(self, client: Any, pit_id: str) -> None:
        if self.backend == "opensearch":
            await client.delete_pit(body={"pit_id": [pit_id]})
        else:
            await client.close_point_in_time(id=pit_id)

    async def _search_with_pit(
        self,
        client: Any,
        body: dict,
        pit_id: str,
        keep_alive: str,
    ) -> dict:
        if self.backend == "opensearch":
            body = {**body, "pit": {"id": pit_id, "keep_alive": keep_alive}}
            return await client.search(body=body)
        return await client.search(
            body=body,
            pit={"id": pit_id, "keep_alive": keep_alive},
        )
