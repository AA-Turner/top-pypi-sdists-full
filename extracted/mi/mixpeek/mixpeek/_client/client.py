"""High-level Mixpeek client — ergonomic wrapper around the generated SDK."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import urllib3


class _AttrDict(dict):
    """A dict that also supports attribute access, so SDK responses work the way
    every docs example uses them: both ``r["field"]`` AND ``r.field``.

    It remains a real ``dict`` (``==`` with a plain dict, ``.get()``, JSON-
    serializable), so this is fully backward compatible. Nested objects and the
    objects inside response lists are wrapped too (via ``json`` ``object_hook``),
    so ``resp.results[0].document_id`` works.
    """

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc


class Mixpeek:
    """One-liner client for the Mixpeek API.

    Usage::

        from mixpeek import Mixpeek

        mp = Mixpeek("sk_xxx", namespace="ns_xxx")
        results = mp.search("red car", collection="products")
    """

    DEFAULT_BASE_URL = "https://api.mixpeek.com/v1"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        namespace: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("MIXPEEK_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "An API key is required. Pass api_key= or set MIXPEEK_API_KEY."
            )
        self.namespace = namespace or os.environ.get("MIXPEEK_NAMESPACE")
        raw_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        if raw_url.endswith("/api/v1"):
            pass
        elif raw_url.endswith(("api.mixpeek.com", "api.staging.mixpeek.com")):
            raw_url = f"{raw_url}/v1"
        self.base_url = raw_url
        self.timeout = timeout
        self._http = urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=5.0, read=timeout),
            retries=urllib3.Retry(total=2, backoff_factor=0.3),
        )

        # Resource managers (lazy-style but immediate for discoverability)
        from mixpeek._client.resources import (
            Buckets,
            Collections,
            Documents,
            Evaluations,
            Namespaces,
            Retrievers,
            Tasks,
        )

        self.namespaces = Namespaces(self)
        self.buckets = Buckets(self)
        self.collections = Collections(self)
        self.retrievers = Retrievers(self)
        self.documents = Documents(self)
        self.evaluations = Evaluations(self)
        self.tasks = Tasks(self)

    # ---- Convenience shortcuts ------------------------------------------------

    def search(
        self,
        query: str | None = None,
        *,
        namespace_id: str | None = None,
        queries: list[dict[str, Any]] | None = None,
        collection: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        namespace: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if namespace_id is not None or queries is not None:
            # POST /v1/search was removed; querying is unified on retrievers for
            # both standalone (BYO vectors) and managed namespaces. Build an
            # ephemeral feature_search retriever from the provided `queries`
            # (which already carry inline vector values), execute it, and clean
            # it up. See docs.mixpeek.com/vector-store/overview.
            return self._byov_search(
                namespace_id=namespace_id or self.namespace,
                queries=queries or [],
                limit=limit,
                **kwargs,
            )

        if query is None:
            raise ValueError(
                "Either 'query' (text) or 'namespace_id'+'queries' (vector) is required."
            )
        ns = namespace or self.namespace
        stages: list[dict[str, Any]] = [
            {
                "type": "feature_search",
                "feature_extractor": {"type": "text"},
                "query": query,
                "collection_ids": [collection] if collection else [],
                "limit": limit,
            }
        ]
        if filters:
            stages.insert(
                0,
                {
                    "type": "attribute_filter",
                    "conditions": filters,
                },
            )
        body = {
            "stages": stages,
            "inputs": {"query": query},
        }
        return self._request("POST", "/retrievers/execute", body=body, namespace=ns)

    def _byov_search(
        self,
        *,
        namespace_id: str | None,
        queries: list[dict[str, Any]],
        limit: int = 10,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Run a BYO-vector search by creating + executing an ephemeral retriever.

        ``queries`` is a list of feature_search ``searches`` entries, each
        carrying an inline vector value, e.g.::

            [{"feature_uri": "sdk_8",
              "query": {"input_mode": "vector", "value": [0.1, ...]},
              "top_k": 5}]
        """
        if not queries:
            raise ValueError("queries is required for a BYO-vector search.")

        final_top_k = max((q.get("top_k", limit) for q in queries), default=limit)
        stage = {
            "stage_name": "feature_search",
            "stage_type": "filter",
            "config": {
                "stage_id": "feature_search",
                "parameters": {"searches": queries, "final_top_k": final_top_k},
            },
        }
        # Call _request directly so the namespace is sent as the X-Namespace
        # header (resource wrappers fold extra kwargs into the JSON body).
        created = self._request(
            "POST",
            "/retrievers",
            body={
                "retriever_name": f"sdk-byov-search-{uuid.uuid4().hex[:8]}",
                "stages": [stage],
                **kwargs,
            },
            namespace=namespace_id,
        )
        ret_id = created.get("retriever_id") if isinstance(created, dict) else None
        if not ret_id:
            raise MixpeekAPIError(
                500, {"detail": "retriever create returned no id", "body": created}
            )
        try:
            return self._request(
                "POST",
                f"/retrievers/{ret_id}/execute",
                body={"inputs": {}},
                namespace=namespace_id,
            )
        finally:
            try:
                self._request("DELETE", f"/retrievers/{ret_id}", namespace=namespace_id)
            except Exception:  # noqa: BLE001 — best-effort cleanup of the ephemeral retriever
                pass

    def index(
        self,
        source: str,
        *,
        collection: str | None = None,
        metadata: dict[str, Any] | None = None,
        namespace: str | None = None,
    ) -> dict[str, Any]:
        """Upload a file URL to a bucket and optionally trigger a collection.

        ``source`` can be an S3/GCS URI or any public URL.
        If ``collection`` is provided the collection is triggered after upload.
        """
        ns = namespace or self.namespace

        # Find or pick the first bucket in the namespace
        buckets = self._request("POST", "/buckets/list", namespace=ns)
        if not buckets:
            raise ValueError("No buckets found in the target namespace.")
        bucket_id = (
            buckets[0]["bucket_id"]
            if isinstance(buckets, list)
            else buckets["results"][0]["bucket_id"]
        )

        upload_body: dict[str, Any] = {"blob": {"url": source}}
        if metadata:
            upload_body["metadata"] = metadata

        result = self._request(
            "POST", f"/buckets/{bucket_id}/objects", body=upload_body, namespace=ns
        )

        if collection:
            self._request("POST", f"/collections/{collection}/trigger", namespace=ns)

        return result

    # ---- HTTP helper ----------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Any | None = None,
        namespace: str | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        ns = namespace or self.namespace
        if ns:
            headers["X-Namespace"] = ns

        encoded_body = json.dumps(body).encode("utf-8") if body is not None else None

        max_retries = 3
        for attempt in range(max_retries + 1):
            resp = self._http.request(
                method,
                url,
                body=encoded_body,
                headers=headers,
            )

            if resp.status in (429, 503) and attempt < max_retries:
                retry_after = 2.0
                try:
                    err_body = json.loads(resp.data.decode("utf-8"))
                    details = (
                        err_body.get("detail", {}).get("error", {}).get("details", {})
                    )
                    retry_after = float(details.get("retry_after_seconds", retry_after))
                except Exception:
                    pass
                import time

                time.sleep(min(retry_after, 30.0))
                continue

            break

        if resp.status >= 400:
            try:
                detail = json.loads(resp.data.decode("utf-8"))
            except Exception:
                detail = resp.data.decode("utf-8", errors="replace")
            raise MixpeekAPIError(resp.status, detail)

        if not resp.data:
            return None

        # object_hook wraps every JSON object (including nested + list elements)
        # so responses support both r["field"] and r.field, as the docs show.
        return json.loads(resp.data.decode("utf-8"), object_hook=_AttrDict)


class MixpeekAPIError(Exception):
    """Raised when the Mixpeek API returns an error response."""

    def __init__(self, status: int, detail: Any) -> None:
        self.status = status
        self.detail = detail
        self.retryable = status in (429, 503)
        self.retry_after: float | None = None
        try:
            details = detail.get("detail", {}).get("error", {}).get("details", {})
            self.retry_after = float(details.get("retry_after_seconds"))
        except Exception:
            pass
        super().__init__(f"Mixpeek API error {status}: {detail}")
