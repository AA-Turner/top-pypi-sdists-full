"""SearchQuery — query OpenSearch/Elasticsearch into a pandas DataFrame.

Usage example:

.. code-block:: yaml

    SearchQuery:
      credentials:
        host: opensearch.example.com
        port: 9200
        username: admin
        password: secret
        backend: opensearch
      index: my-index-*
      query: >
        {"query": {"range": {"@timestamp": {"gte": "{start}", "lte": "{end}"}}}}
      pagination: scroll
      size: 5000
      include_metadata: false
"""
from __future__ import annotations

import json
from typing import Any, Optional
from collections.abc import Callable

import pandas

from ..exceptions import ComponentError
from ..interfaces.flow import FlowComponent
from ..interfaces.search import SearchInterface


class SearchQuery(SearchInterface, FlowComponent):
    """SearchQuery

    Query an OpenSearch or Elasticsearch index and return a pandas DataFrame.
    Drives full-result pagination via scroll (default) or search_after (PIT-based).
    Supports {start}/{end} mask variables in index and query for date-range tasks.

    :widths: auto

    | credentials     | Yes | Connection dict: host, port, username, password, backend, use_ssl, verify_certs. |
    | index           | Yes | Index name or pattern to search (e.g. logs-*). Supports {start}/{end} masks. |
    | query           | Yes | JSON DSL query body (string or dict). Supports {start}/{end} mask variables. |
    | pagination      | No  | Pagination mode: scroll (default, works everywhere) or search_after. search_after uses PIT on ES>=7.12/OpenSearch; on ES 7.10 it needs a deterministic 'sort' (unique tiebreaker) in the query or it raises ComponentError. |
    | size            | No  | Number of documents per page (default 5000). |
    | scroll          | No  | Scroll/PIT keep-alive TTL string (default 2m). |
    | max_documents   | No  | Cap total documents returned. None means no cap. |
    | include_metadata | No | Add _id, _index, and _score columns to the result DataFrame (default False). |

    :consumes: none
    :produces: dataframe

    Example:

    ```yaml
    SearchQuery:
      credentials:
        host: opensearch.example.com
        port: 9200
        username: admin
        password: secret
        backend: opensearch
      index: my-index-*
      query: >
        {"query": {"range": {"@timestamp": {"gte": "{start}", "lte": "{end}"}}}}
      pagination: scroll
      size: 5000
      include_metadata: false
    ```
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: Any = None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise, declaring config attributes before forwarding kwargs.

        Args:
            loop: Unused; accepted for API parity with other components.
            job: Optional job callable.
            stat: Optional stat callable.
            **kwargs: Component configuration, including ``credentials``,
                ``index``, ``query``, ``pagination``, ``size``, ``scroll``,
                ``max_documents``, and ``include_metadata``.
        """
        self.index: str = kwargs.pop("index", "")
        self.query: Any = kwargs.pop("query", {})
        self.pagination: str = kwargs.pop("pagination", "scroll")
        self.size: int = int(kwargs.pop("size", 5000))
        self.scroll: str = str(kwargs.pop("scroll", "2m"))
        self.max_documents: Optional[int] = kwargs.pop("max_documents", None)
        self.include_metadata: bool = bool(kwargs.pop("include_metadata", False))
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs: Any) -> bool:
        """Resolve credentials, substitute mask variables, open the client.

        Calls ``processing_credentials()``, applies ``{start}``/``{end}``
        substitution to ``index`` and ``query``, validates required config,
        then opens the search client.

        Args:
            **kwargs: Forwarded to ``super().start()``.

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: When ``index`` or ``query`` is missing, the query
                string is not valid JSON, or the backend is invalid.
        """
        await super().start(**kwargs)
        self.processing_credentials()

        if isinstance(self.index, str) and "{" in self.index:
            self.index = self.mask_replacement(self.index)
        if isinstance(self.query, str) and "{" in self.query:
            self.query = self.mask_replacement(self.query)

        if isinstance(self.query, str):
            try:
                self.query = json.loads(self.query)
            except json.JSONDecodeError as exc:
                raise ComponentError(
                    f"SearchQuery: 'query' is not valid JSON — {exc}"
                ) from exc

        if not self.index:
            raise ComponentError("SearchQuery: 'index' is required.")
        if not self.query:
            raise ComponentError("SearchQuery: 'query' is required.")

        await self.open_search_client()
        return True

    async def run(self) -> pandas.DataFrame:
        """Execute the search and return a DataFrame of results.

        Calls ``paginate()`` with the configured mode/size/scroll, then
        flattens the ``_source`` fields into a DataFrame.  When
        ``include_metadata=True``, ``_id``, ``_index``, and ``_score``
        (when present) are prepended as columns.

        Returns:
            ``pandas.DataFrame`` with one row per document.  An empty
            DataFrame is returned (without raising) when there are no hits.

        Raises:
            ComponentError: On connection or query failure.
        """
        self.logger.info(
            "SearchQuery: querying index=%r via %s (backend=%s)",
            self.index,
            self.pagination,
            self.backend,
        )
        max_docs = int(self.max_documents) if self.max_documents is not None else None
        hits = await self.paginate(
            self.index,
            self.query,
            mode=self.pagination,
            size=self.size,
            scroll=self.scroll,
            max_documents=max_docs,
            raw_hits=self.include_metadata,
        )

        if not hits:
            self.logger.warning(
                "SearchQuery: no documents returned from index=%r", self.index
            )
            df = pandas.DataFrame()
        elif self.include_metadata:
            records: list[dict] = []
            for h in hits:
                row: dict = {
                    "_id": h.get("_id", ""),
                    "_index": h.get("_index", ""),
                }
                if h.get("_score") is not None:
                    row["_score"] = h["_score"]
                row.update(h.get("_source", {}))
                records.append(row)
            df = pandas.DataFrame(records)
        else:
            df = pandas.DataFrame(hits)

        self.logger.info(
            "SearchQuery: result shape %s",
            df.shape if not df.empty else "(0, 0)",
        )
        self._result = df
        return df

    async def close(self) -> None:
        """Close the search client, releasing any scroll or PIT context."""
        await self.close_search_client()
