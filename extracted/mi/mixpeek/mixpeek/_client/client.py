"""High-level Mixpeek client — ergonomic wrapper around the generated SDK."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

import urllib3

#: A retryable 429/503 is retried until the waits would pass this many
#: seconds in total: long enough for a vector-store writer to finish booting
#: (about 2 min) or a standby to take over.
RETRY_BUDGET_S = 180.0
#: One wait is never longer than this, whatever the server advises.
MAX_RETRY_WAIT_S = 30.0
#: The first wait when the server advises none; it doubles each retry.
DEFAULT_RETRY_AFTER_S = 2.0


def _error_details(payload: Any) -> list[dict]:
    """The error body's ``details`` objects: ``error.details`` (the API's
    shape) and ``detail.error.details`` (an older one)."""
    if not isinstance(payload, dict):
        return []
    found = [(payload.get("error") or {}).get("details")]
    if isinstance(payload.get("detail"), dict):
        found.append((payload["detail"].get("error") or {}).get("details"))
    return [d for d in found if isinstance(d, dict)]


def _advised_wait(resp: Any, payload: Any) -> float | None:
    """The server's advised wait in seconds: the Retry-After header, else the
    error body's ``retry_after_seconds``, else None."""
    headers = getattr(resp, "headers", None) or {}
    value = headers.get("Retry-After") if hasattr(headers, "get") else None
    candidates = [value] + [
        d.get("retry_after_seconds") for d in _error_details(payload)
    ]
    for v in candidates:
        if v is None:
            continue
        try:
            return max(0.0, float(v))
        except (TypeError, ValueError):
            continue  # e.g. an HTTP-date Retry-After: try the body
    return None


def _marked_not_retryable(payload: Any) -> bool:
    """A 429/503 whose body says ``retryable: false`` is not retried."""
    return any(d.get("retryable") is False for d in _error_details(payload))


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


def _feature_search_entry(query: dict[str, Any]) -> dict[str, Any]:
    """Accept the ``vector_name``/``vector`` spelling the vector-store docs use.

    feature_search reads ``feature_uri`` and ``query``. An entry that names its
    vector with ``vector_name`` and passes it as ``vector`` is rewritten to that
    shape; an entry already in it passes through. The caller's dict is left as is.
    """
    entry = dict(query)
    if "feature_uri" not in entry and "vector_name" in entry:
        entry["feature_uri"] = entry.pop("vector_name")
    if "query" not in entry and "vector" in entry:
        entry["query"] = {"input_mode": "vector", "value": entry.pop("vector")}
    return entry


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
            Batches,
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
        self.batches = Batches(self)

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
                filters=filters,
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
        filters: dict[str, Any] | None = None,
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
        queries = [_feature_search_entry(q) for q in queries]

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
                body={"inputs": {}, **({"filters": filters} if filters else {})},
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
        blob_property: str | None = None,
        blob_type: str | None = None,
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

        from mixpeek._client.resources import _blob_entry

        # The blob's property and type come from the bucket schema, as in
        # Buckets.upload; blob_property= and blob_type= choose them explicitly.
        upload_body: dict[str, Any] = {
            "blobs": [
                _blob_entry(
                    lambda bid: self._request("GET", f"/buckets/{bid}", namespace=ns),
                    bucket_id,
                    source,
                    blob_property=blob_property,
                    blob_type=blob_type,
                )
            ]
        }
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
        """Every ``Mixpeek`` call goes through here, including the retry
        decision: a retryable 429 or 503 is retried until the waits would pass
        ``RETRY_BUDGET_S`` (3 min) in total, long enough for a writer to boot
        or a standby to take over. Each wait is the server's Retry-After
        header, else its ``retry_after_seconds``, else a backoff from 2s that
        doubles; none is longer than ``MAX_RETRY_WAIT_S``. A 429/503 marked
        ``retryable: false`` and every other status are not retried. A write
        the API refused with a 503 stored nothing, so retrying it is safe.
        This is the one retry policy the SDK ships; callers using the
        raw generated API classes (``mixpeek.AccountApi`` etc. via
        ``ApiClient``) bypass this wrapper entirely and get none, since that
        surface is generated code this package does not hand-edit. A caller
        on the raw classes who wants the same behavior passes their own
        ``Configuration(retries=urllib3.Retry(status_forcelist=[429, 503],
        respect_retry_after_header=True))`` -- the generated client already
        threads a ``retries`` value straight to urllib3's ``PoolManager``.
        """
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

        import time

        waited = 0.0
        backoff = DEFAULT_RETRY_AFTER_S
        while True:
            resp = self._http.request(
                method,
                url,
                body=encoded_body,
                headers=headers,
            )
            if resp.status not in (429, 503):
                break
            try:
                err_body = json.loads(resp.data.decode("utf-8"))
            except Exception:
                err_body = None
            if _marked_not_retryable(err_body):
                break
            advised = _advised_wait(resp, err_body)
            wait = min(advised if advised is not None else backoff, MAX_RETRY_WAIT_S)
            if waited + wait > RETRY_BUDGET_S:
                break
            time.sleep(wait)
            waited += wait
            if advised is None:
                backoff = min(backoff * 2, MAX_RETRY_WAIT_S)

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
    """Raised when the Mixpeek API returns an error response that ``Mixpeek._request``
    did not retry away (a non-retryable status, or a 429/503 still failing when
    the retry budget ran out). ``retryable`` and ``retry_after`` are
    informational on the raised error; they do not trigger a further retry
    here."""

    def __init__(self, status: int, detail: Any) -> None:
        self.status = status
        self.detail = detail
        self.retryable = status in (429, 503)
        self.retry_after: float | None = None
        self.retry_after = _advised_wait(None, detail)
        super().__init__(f"Mixpeek API error {status}: {detail}")
