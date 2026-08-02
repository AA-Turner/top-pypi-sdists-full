"""Resource managers for the high-level Mixpeek client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mixpeek._client.client import Mixpeek


class _Resource:
    """Base resource with access to the parent client's HTTP helper."""

    # Body keys that are legitimate API fields for this resource and must NOT
    # be re-routed to the X-Namespace header (e.g. namespaces.create's
    # namespace_id recovery override).
    _NS_BODY_FIELDS: tuple[str, ...] = ()

    def __init__(self, client: Mixpeek) -> None:
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Any | None = None,
        namespace: str | None = None,
    ) -> Any:
        # The API scopes every request by the X-Namespace header; resource
        # methods fold extra kwargs into the JSON body, where a per-call
        # namespace_id=/namespace= would be silently ignored by the server.
        # Route those to the header instead of dropping them.
        if isinstance(body, dict):
            for key in ("namespace_id", "namespace"):
                if key in body and key not in self._NS_BODY_FIELDS:
                    value = body.pop(key)
                    if namespace is None and value is not None:
                        namespace = value
        return self._client._request(method, path, body=body, namespace=namespace)


class NamespaceDocuments(_Resource):
    """Manage documents within a namespace (BYOV / standalone)."""

    def upsert(
        self,
        *,
        namespace_id: str,
        documents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"documents": documents, **kwargs}
        return self._request(
            "POST", f"/namespaces/{namespace_id}/documents/upsert", body=body
        )


class Namespaces(_Resource):
    """Manage namespaces (Qdrant collections)."""

    # namespace_id is a real body field on the namespaces API (create's
    # recovery/migration override), not a scoping shorthand.
    _NS_BODY_FIELDS = ("namespace_id",)

    def __init__(self, client: Mixpeek) -> None:
        super().__init__(client)
        self.documents = NamespaceDocuments(client)

    def list(self) -> list[dict[str, Any]]:
        return self._request("GET", "/namespaces")

    def get(self, namespace_id: str) -> dict[str, Any]:
        return self._request("GET", f"/namespaces/{namespace_id}")

    def create(
        self,
        *,
        namespace_id: str | None = None,
        mode: str | None = None,
        vector_configs: list[dict[str, Any]] | None = None,
        name: str | None = None,
        feature_extractors: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a namespace.

        ``mode`` is inferred when omitted so the obvious call works:
        passing ``feature_extractors`` (or just ``name``) creates a **managed**
        namespace; passing ``vector_configs`` creates a **standalone** (BYO
        vectors) namespace. Pass ``mode=`` explicitly to override.
        """
        if mode is None:
            if vector_configs is not None:
                mode = "standalone"
            elif feature_extractors is not None or name is not None:
                mode = "managed"
            else:
                mode = "standalone"

        if mode == "standalone":
            body: dict[str, Any] = {**kwargs}
            resolved = body.pop("namespace_name", None) or name or namespace_id
            if namespace_id is not None:
                body["namespace_id"] = namespace_id
            if resolved is not None:
                body["namespace_name"] = resolved
            if vector_configs is not None:
                body["vector_configs"] = vector_configs
            return self._request("POST", "/namespaces/standalone", body=body)

        body = {**kwargs}
        # The managed-namespace API field is `namespace_name` (required). Accept
        # name=, namespace_name= (via kwargs), or namespace_id as the source so
        # the documented client.namespaces.create(name=...) path actually works.
        resolved_name = body.pop("namespace_name", None) or name or namespace_id
        if resolved_name is not None:
            body["namespace_name"] = resolved_name
        if namespace_id is not None:
            body["namespace_id"] = namespace_id
        if feature_extractors is not None:
            body["feature_extractors"] = feature_extractors
        return self._request("POST", "/namespaces", body=body)

    def delete(self, namespace_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/namespaces/{namespace_id}")

    def clone(
        self,
        namespace_id: str,
        body: dict[str, Any] | None = None,
        *,
        namespace_name: str | None = None,
        name: str | None = None,
        include_resources: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Clone an entire namespace (collections + retrievers, vectors copied —
        no reprocessing) into a new isolated environment.

        The new name is required — supply it as ``namespace_name=`` (``name=``
        also accepted) or inside a ``body`` dict. ``include_resources`` selects
        which resource types to copy (defaults to collections + retrievers)::

            client.namespaces.clone(ns_id, namespace_name="staging")
            client.namespaces.clone(ns_id, {"namespace_name": "staging",
                "include_resources": {"collections": True, "retrievers": True}})
        """
        merged: dict[str, Any] = {**(body or {}), **kwargs}
        if include_resources is not None:
            merged["include_resources"] = include_resources
        resolved = namespace_name or name or merged.pop("namespace_name", None)
        if not resolved:
            raise ValueError("namespace_name is required to clone a namespace")
        return self._request(
            "POST",
            f"/namespaces/{namespace_id}/clone",
            body={"namespace_name": resolved, **merged},
        )

    def promote(
        self,
        namespace_id: str,
        *,
        vector_mappings: list[dict[str, Any]] | None = None,
        add_vectors: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Promote a standalone (BYO-vectors) namespace to managed mode.

        Existing vectors/documents are preserved. ``vector_mappings`` maps
        existing indexes to inference services (auto-embed queries);
        ``add_vectors`` creates new managed indexes.
        """
        body: dict[str, Any] = {**kwargs}
        if vector_mappings is not None:
            body["vector_mappings"] = vector_mappings
        if add_vectors is not None:
            body["add_vectors"] = add_vectors
        return self._request(
            "POST", f"/namespaces/{namespace_id}/promote", body=body or None
        )


class Buckets(_Resource):
    """Manage buckets and object uploads."""

    def list(self) -> list[dict[str, Any]]:
        return self._request("POST", "/buckets/list")

    def get(self, bucket_id: str) -> dict[str, Any]:
        return self._request("GET", f"/buckets/{bucket_id}")

    def create(
        self,
        *,
        bucket_name: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a bucket.

        The API field is ``bucket_name``; ``name=`` is accepted as an alias so
        the documented ``client.buckets.create(name=...)`` path works. A
        ``bucket_schema`` (object structure) is required by the API — pass it as
        a keyword.
        """
        resolved = bucket_name or name or kwargs.pop("bucket_name", None)
        if not resolved:
            raise ValueError("bucket_name is required")
        return self._request(
            "POST", "/buckets", body={"bucket_name": resolved, **kwargs}
        )

    def delete(self, bucket_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/buckets/{bucket_id}")

    def upload(
        self,
        bucket_id: str,
        *,
        url: str | None = None,
        data: Any | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if url is not None:
            body["blob"] = {"url": url}
        elif data is not None:
            body["blob"] = {"data": data}
        if metadata is not None:
            body["metadata"] = metadata
        return self._request("POST", f"/buckets/{bucket_id}/objects", body=body)

    def list_objects(
        self,
        bucket_id: str,
        *,
        cursor: str | None = None,
        page_size: int = 100,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"page_size": page_size}
        if cursor is not None:
            body["cursor"] = cursor
        return self._request("POST", f"/buckets/{bucket_id}/objects/list", body=body)


class Collections(_Resource):
    """Manage collections (processing pipelines)."""

    def list(self) -> list[dict[str, Any]]:
        return self._request("POST", "/collections/list")

    def get(self, collection_id: str) -> dict[str, Any]:
        return self._request("GET", f"/collections/{collection_id}")

    def create(
        self,
        *,
        collection_name: str | None = None,
        name: str | None = None,
        feature_extractor: dict[str, Any] | None = None,
        source: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a collection.

        The API field is ``collection_name``; ``name=`` is accepted as an alias
        so the documented ``client.collections.create(name=...)`` path works.
        """
        resolved = collection_name or name or kwargs.pop("collection_name", None)
        if not resolved:
            raise ValueError("collection_name is required")
        body: dict[str, Any] = {"collection_name": resolved, **kwargs}
        if feature_extractor is not None:
            body["feature_extractor"] = feature_extractor
        if source is not None:
            body["source"] = source
        return self._request("POST", "/collections", body=body)

    def delete(self, collection_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/collections/{collection_id}")

    def trigger(self, collection_id: str, **kwargs: Any) -> dict[str, Any]:
        return self._request(
            "POST", f"/collections/{collection_id}/trigger", body=kwargs or None
        )

    def update(
        self,
        collection_id: str,
        updates: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update collection metadata (PATCH).

        Pass the fields to change either as a positional/keyword ``updates`` dict
        or as flat keyword arguments (the two are merged). All of these work::

            client.collections.update(cid, {"description": "new desc"})
            client.collections.update(cid, description="new desc")
            client.collections.update(cid, updates={"metadata": {"team": "rec"}})
        """
        body: dict[str, Any] = {**(updates or {}), **kwargs}
        if not body:
            raise ValueError(
                "update() needs at least one field to change "
                "(pass a dict of fields or keyword args)."
            )
        return self._request("PATCH", f"/collections/{collection_id}", body=body)

    def clone(
        self,
        collection_id: str,
        body: dict[str, Any] | None = None,
        *,
        collection_name: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Clone a collection into a new one, optionally overriding fields.

        The new name is required — supply it as ``collection_name=`` (``name=``
        also accepted), or inside a ``body`` dict. Overrides (e.g.
        ``feature_extractor``) may be passed in ``body`` or as flat kwargs::

            client.collections.clone(cid, collection_name="copy")
            client.collections.clone(cid, {"collection_name": "copy",
                                           "feature_extractor": {...}})
        """
        merged: dict[str, Any] = {**(body or {}), **kwargs}
        resolved = collection_name or name or merged.pop("collection_name", None)
        if not resolved:
            raise ValueError("collection_name is required to clone a collection")
        return self._request(
            "POST",
            f"/collections/{collection_id}/clone",
            body={"collection_name": resolved, **merged},
        )


class Retrievers(_Resource):
    """Manage and execute retrievers."""

    def list(self) -> list[dict[str, Any]]:
        return self._request("POST", "/retrievers/list")

    def get(self, retriever_id: str) -> dict[str, Any]:
        return self._request("GET", f"/retrievers/{retriever_id}")

    def create(
        self,
        *,
        retriever_name: str | None = None,
        name: str | None = None,
        stages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        # The API field is `retriever_name`. Accept the legacy `name=` kwarg as
        # an alias so older call sites keep working.
        resolved_name = retriever_name or name
        if not resolved_name:
            raise ValueError("retriever_name is required")
        return self._request(
            "POST",
            "/retrievers",
            body={"retriever_name": resolved_name, "stages": stages, **kwargs},
        )

    def update(
        self,
        retriever_id: str,
        *,
        stages: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {**kwargs}
        if stages is not None:
            body["stages"] = stages
        return self._request("PATCH", f"/retrievers/{retriever_id}", body=body)

    def delete(self, retriever_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"/retrievers/{retriever_id}")

    def execute(
        self,
        retriever_id: str,
        *,
        inputs: dict[str, Any],
        settings: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"inputs": inputs, **kwargs}
        if settings is not None:
            body["settings"] = settings
        return self._request("POST", f"/retrievers/{retriever_id}/execute", body=body)

    def run(
        self,
        retriever_id: str,
        *,
        inputs: dict[str, Any],
        settings: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Alias for :meth:`execute` — run a retriever against one query."""
        return self.execute(retriever_id, inputs=inputs, settings=settings, **kwargs)

    def execute_batch(
        self,
        retriever_id: str,
        *,
        queries: list[dict[str, Any]],
        settings: dict[str, Any] | None = None,
        concurrency: int | None = None,
        return_presigned_urls: bool | None = None,
        return_vectors: bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute a retriever against many queries in one call (1-50 queries).

        Each query is ``{"inputs": {...}, "filters": {...}?}``. As a convenience,
        a bare inputs dict (no ``"inputs"`` key) is wrapped automatically, so both
        of these work::

            client.retrievers.execute_batch(rid, queries=[{"query": "a"}, {"query": "b"}])
            client.retrievers.execute_batch(rid, queries=[{"inputs": {"query": "a"}}])
        """
        norm: list[dict[str, Any]] = []
        for q in queries:
            if isinstance(q, dict) and "inputs" in q:
                norm.append(q)
            else:
                norm.append({"inputs": q})
        body: dict[str, Any] = {"queries": norm, **kwargs}
        if settings is not None:
            body["settings"] = settings
        if concurrency is not None:
            body["concurrency"] = concurrency
        if return_presigned_urls is not None:
            body["return_presigned_urls"] = return_presigned_urls
        if return_vectors is not None:
            body["return_vectors"] = return_vectors
        return self._request(
            "POST", f"/retrievers/{retriever_id}/execute/batch", body=body
        )

    def clone(
        self,
        retriever_id: str,
        body: dict[str, Any] | None = None,
        *,
        retriever_name: str | None = None,
        name: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Clone a retriever into a new one, optionally overriding fields.

        The new name is required — supply it as ``retriever_name=`` (``name=``
        also accepted) or inside a ``body`` dict. Any other field (``stages``,
        ``input_schema``, ``description``, ...) overrides the source; omit to copy
        from source. All of these work::

            client.retrievers.clone(rid, retriever_name="variant")
            client.retrievers.clone(rid, {"retriever_name": "variant",
                                          "stages": [...]})
        """
        merged: dict[str, Any] = {**(body or {}), **kwargs}
        resolved = retriever_name or name or merged.pop("retriever_name", None)
        if not resolved:
            raise ValueError("retriever_name is required to clone a retriever")
        return self._request(
            "POST",
            f"/retrievers/{retriever_id}/clone",
            body={"retriever_name": resolved, **merged},
        )

    def publish(
        self,
        retriever_id: str,
        *,
        display_name: str | None = None,
        public_name: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Publish a retriever to a public, shareable URL (mxp.co/r/{public_name})."""
        body: dict[str, Any] = {**kwargs}
        if display_name is not None:
            body["display_name"] = display_name
        if public_name is not None:
            body["public_name"] = public_name
        return self._request(
            "POST", f"/retrievers/{retriever_id}/publish", body=body or None
        )

    def run_evaluation(
        self,
        retriever_id: str,
        *,
        dataset_name: str | None = None,
        dataset_id: str | None = None,
        evaluation_config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Start an evaluation of this retriever against a ground-truth dataset.

        The dataset may be named via ``dataset_name=`` (``dataset_id=`` is also
        accepted — both map to the API's ``dataset_name`` field, which resolves
        by name or id). Convenience alias for :meth:`Evaluations.run`.
        """
        resolved = dataset_name or dataset_id
        if not resolved:
            raise ValueError("dataset_name (or dataset_id) is required")
        body: dict[str, Any] = {"dataset_name": resolved, **kwargs}
        if evaluation_config is not None:
            body["evaluation_config"] = evaluation_config
        return self._request(
            "POST", f"/retrievers/{retriever_id}/evaluations", body=body
        )

    def create_interaction(
        self,
        *,
        feature_id: str | None = None,
        document_id: str | None = None,
        interaction_type: list[str],
        position: int = 0,
        retriever_id: str | None = None,
        execution_id: str | None = None,
        feature_uri: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        occurred_at: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Record a user interaction (click, purchase, feedback, ...).

        Args:
            occurred_at: When the interaction actually happened (ISO 8601).
                Omit for live interactions — the server stamps "now". Supply it
                ONLY to BACKFILL historical interactions (e.g. migrating existing
                click logs) so learned-fusion temporal decay weights them by their
                true age. A future value is clamped to now; backfilled events
                bypass the real-time session cache.
        """
        resolved_feature_id = feature_id or document_id
        if not resolved_feature_id:
            raise ValueError(
                "Either feature_id or document_id is required. "
                "Execute responses use 'document_id'; the interactions API "
                "expects 'feature_id' — both refer to the same entity."
            )
        body: dict[str, Any] = {
            "feature_id": resolved_feature_id,
            "interaction_type": interaction_type,
            "position": position,
            **kwargs,
        }
        for key, val in [
            ("retriever_id", retriever_id),
            ("execution_id", execution_id),
            ("feature_uri", feature_uri),
            ("user_id", user_id),
            ("session_id", session_id),
            ("occurred_at", occurred_at),
        ]:
            if val is not None:
                body[key] = val
        return self._request("POST", "/retrievers/interactions", body=body)

    def create_interaction_from_result(
        self,
        result: dict[str, Any],
        *,
        position: int,
        interaction_type: list[str] | None = None,
        retriever_id: str | None = None,
        feature_uri: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        occurred_at: str | None = None,
    ) -> dict[str, Any]:
        """Create an interaction from a retriever execution result.

        Extracts feature_id, execution_id, retriever_id, and feature_uri
        from the execution response so callers don't need to do it manually.

        Args:
            result: The full response dict from ``retrievers.execute()``.
            position: 0-indexed position of the clicked/interacted result.
            interaction_type: e.g. ``["click"]``, ``["purchase"]``.
            retriever_id: Override the retriever_id (auto-detected from
                the execute response if omitted).
            feature_uri: Override the feature_uri (auto-detected from
                ``learned_fusion_context`` if omitted).
            user_id: The user who performed the interaction.
            session_id: Current session identifier.
            occurred_at: ISO 8601 timestamp for historical backfill.
        """
        if interaction_type is None:
            interaction_type = ["click"]

        docs = result.get("results", result.get("documents", []))
        if position >= len(docs):
            raise IndexError(
                f"position {position} out of range (got {len(docs)} results)"
            )
        doc = docs[position]
        feature_id = (
            doc.get("feature_id") or doc.get("document_id") or doc.get("id", "")
        )
        if not feature_id:
            raise ValueError("Could not extract feature_id from result")

        if feature_uri is None:
            lfc = result.get("learned_fusion_context") or {}
            uris = lfc.get("feature_uris", [])
            if uris:
                feature_uri = uris[0]

        if retriever_id is None:
            retriever_id = result.get("retriever_id")
        if not retriever_id:
            import warnings

            warnings.warn(
                "Execute response is missing 'retriever_id'. The interaction "
                "will be created without a retriever link and won't appear in "
                "list_interactions, get_user_weights, or get_stats. Pass "
                "retriever_id explicitly or upgrade your API version.",
                stacklevel=2,
            )

        return self.create_interaction(
            feature_id=feature_id,
            interaction_type=interaction_type,
            position=position,
            retriever_id=retriever_id,
            execution_id=result.get("execution_id"),
            feature_uri=feature_uri,
            user_id=user_id,
            session_id=session_id,
            document_score=doc.get("score"),
            occurred_at=occurred_at,
        )

    def backfill_interactions(
        self, interactions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Bulk-record historical interactions in one call (1-1000).

        For migrating an existing click/purchase history into Mixpeek: set each
        interaction's ``occurred_at`` (ISO 8601) to its true timestamp so
        learned-fusion temporal decay weights it by real age. Send large
        histories in chunks of ≤ 1000. Returns ``{created, failed, errors}``.

        Example:
            client.retrievers.backfill_interactions([
                {"feature_id": "d1", "interaction_type": ["purchase"],
                 "retriever_id": "ret_...",
                 "user_id": "u1", "feature_uri": "mixpeek://...",
                 "occurred_at": "2026-01-15T10:30:00Z"},
                ...
            ])
        """
        missing = [i for i, ix in enumerate(interactions) if not ix.get("retriever_id")]
        if missing:
            import warnings

            warnings.warn(
                f"{len(missing)} interaction(s) are missing 'retriever_id' "
                f"(indices: {missing[:5]}{'...' if len(missing) > 5 else ''}). "
                "These will be created but won't appear in list_interactions, "
                "get_user_weights, or get_stats for any retriever.",
                stacklevel=2,
            )
        return self._request(
            "POST",
            "/retrievers/interactions/batch",
            body={"interactions": interactions},
        )

    # -- Learned Fusion Control ------------------------------------------------

    def enable_learned_fusion(self, retriever_id: str) -> dict[str, Any]:
        """Enable learned fusion for a retriever."""
        return self._request(
            "POST", f"/retrievers/{retriever_id}/learned-fusion/enable"
        )

    def disable_learned_fusion(self, retriever_id: str) -> dict[str, Any]:
        """Disable learned fusion for a retriever (kill switch)."""
        return self._request(
            "POST", f"/retrievers/{retriever_id}/learned-fusion/disable"
        )

    def set_rollout(self, retriever_id: str, *, rollout_pct: float) -> dict[str, Any]:
        """Set the learned fusion traffic-split percentage (0-100)."""
        return self._request(
            "POST",
            f"/retrievers/{retriever_id}/learned-fusion/rollout",
            body={"rollout_pct": rollout_pct},
        )

    def opt_out_user(self, retriever_id: str, *, user_id: str) -> dict[str, Any]:
        """Opt a user out of learned fusion personalization."""
        return self._request(
            "POST",
            f"/retrievers/{retriever_id}/learned-fusion/opt-out/{user_id}",
        )

    def opt_in_user(self, retriever_id: str, *, user_id: str) -> dict[str, Any]:
        """Opt a user back into learned fusion personalization."""
        return self._request(
            "POST",
            f"/retrievers/{retriever_id}/learned-fusion/opt-in/{user_id}",
        )

    def reset_user(self, retriever_id: str, *, user_id: str) -> dict[str, Any]:
        """Reset a user's learned fusion state."""
        return self._request(
            "DELETE",
            f"/retrievers/{retriever_id}/learned-fusion/user/{user_id}",
        )

    # -- Learned Fusion Read ---------------------------------------------------

    def get_weights(self, retriever_id: str) -> dict[str, Any]:
        """Get global learned fusion weight distribution."""
        return self._request(
            "GET", f"/retrievers/{retriever_id}/learned-fusion/weights"
        )

    def get_user_weights(self, retriever_id: str, *, user_id: str) -> dict[str, Any]:
        """Get per-user learned fusion weights."""
        return self._request(
            "GET",
            f"/retrievers/{retriever_id}/learned-fusion/weights/{user_id}",
        )

    def get_stats(self, retriever_id: str) -> dict[str, Any]:
        """Get aggregate learned fusion statistics."""
        return self._request("GET", f"/retrievers/{retriever_id}/learned-fusion/stats")

    def get_activity(self, retriever_id: str) -> dict[str, Any]:
        """Get recent learned fusion activity events."""
        return self._request(
            "GET", f"/retrievers/{retriever_id}/learned-fusion/activity"
        )

    # -- Interaction Management ------------------------------------------------

    def list_interactions(
        self,
        retriever_id: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, Any]:
        """List interactions for a retriever with pagination."""
        return self._request(
            "POST",
            f"/retrievers/interactions/list?page={page}&page_size={page_size}",
            body={"retriever_id": retriever_id},
        )

    def get_interaction(self, interaction_id: str) -> dict[str, Any]:
        """Get a specific interaction by ID."""
        return self._request("GET", f"/retrievers/interactions/{interaction_id}")

    def delete_interaction(self, interaction_id: str) -> dict[str, Any]:
        """Delete a specific interaction."""
        return self._request("DELETE", f"/retrievers/interactions/{interaction_id}")


class Documents(_Resource):
    """Query and manage documents."""

    def list(
        self,
        collection_id: str,
        *,
        cursor: str | None = None,
        page_size: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"page_size": page_size, **kwargs}
        if cursor is not None:
            body["cursor"] = cursor
        return self._request(
            "POST", f"/collections/{collection_id}/documents/list", body=body
        )

    def get(self, collection_id: str, document_id: str) -> dict[str, Any]:
        return self._request(
            "GET", f"/collections/{collection_id}/documents/{document_id}"
        )

    def delete(self, collection_id: str, document_id: str) -> dict[str, Any]:
        return self._request(
            "DELETE", f"/collections/{collection_id}/documents/{document_id}"
        )

    def update(
        self,
        collection_id: str,
        document_id: str,
        *,
        update_data: dict[str, Any],
    ) -> dict[str, Any]:
        return self._request(
            "PATCH",
            f"/collections/{collection_id}/documents/{document_id}",
            body=update_data,
        )

    def batch_update(
        self,
        collection_id: str,
        *,
        updates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/collections/{collection_id}/documents/batch",
            body={"updates": updates},
        )

    def search(
        self,
        *,
        collection_ids: list[str] | None = None,
        query: str | None = None,
        page_size: int = 10,
        **kwargs: Any,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"page_size": page_size, **kwargs}
        if collection_ids is not None:
            body["collection_ids"] = collection_ids
        if query is not None:
            body["query"] = query
        return self._request("POST", "/documents/search", body=body)


class Evaluations(_Resource):
    """Create ground-truth datasets and evaluate retrievers against them.

    Datasets are namespace-scoped; running/listing evaluations is retriever-scoped.
    Example::

        ds = client.evaluations.create_dataset(
            dataset_name="rec_gt",
            queries=[{"query_id": "q1", "query_input": {"query": "running shoes"},
                      "relevant_documents": ["doc_1", "doc_2"]}],
        )
        run = client.evaluations.run(retriever_id, dataset_name="rec_gt")
        client.evaluations.get(retriever_id, run["evaluation_id"])
    """

    # -- Datasets --------------------------------------------------------------

    def create_dataset(
        self,
        *,
        dataset_name: str,
        queries: list[dict[str, Any]],
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a ground-truth dataset.

        Each query is ``{"query_id", "query_input": {...}, "relevant_documents":
        [...], "relevance_scores"?: {doc_id: int}}``.
        """
        body: dict[str, Any] = {
            "dataset_name": dataset_name,
            "queries": queries,
            **kwargs,
        }
        if description is not None:
            body["description"] = description
        if metadata is not None:
            body["metadata"] = metadata
        return self._request("POST", "/retrievers/evaluations/datasets", body=body)

    def list_datasets(self, *, page: int = 1, page_size: int = 20) -> dict[str, Any]:
        """List ground-truth datasets in the namespace (paginated)."""
        return self._request(
            "GET",
            f"/retrievers/evaluations/datasets?page={page}&page_size={page_size}",
        )

    def get_dataset(self, dataset_identifier: str) -> dict[str, Any]:
        """Get a ground-truth dataset by ID or name."""
        return self._request(
            "GET", f"/retrievers/evaluations/datasets/{dataset_identifier}"
        )

    def generate_from_interactions(
        self,
        retriever_id: str,
        *,
        dataset_name: str | None = None,
        min_interactions: int | None = None,
        lookback_days: int | None = None,
        positive_interaction_types: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Auto-build a ground-truth dataset from recorded interactions."""
        body: dict[str, Any] = {**kwargs}
        for key, val in [
            ("dataset_name", dataset_name),
            ("min_interactions", min_interactions),
            ("lookback_days", lookback_days),
            ("positive_interaction_types", positive_interaction_types),
        ]:
            if val is not None:
                body[key] = val
        return self._request(
            "POST",
            f"/retrievers/{retriever_id}/evaluations/generate-from-interactions",
            body=body or None,
        )

    # -- Evaluations -----------------------------------------------------------

    def run(
        self,
        retriever_id: str,
        *,
        dataset_name: str | None = None,
        dataset_id: str | None = None,
        evaluation_config: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Start an evaluation of a retriever against a dataset.

        Identify the dataset with ``dataset_name=`` (``dataset_id=`` also
        accepted). ``evaluation_config`` may set
        ``{"k_values": [...], "metrics": [...]}``.
        """
        resolved = dataset_name or dataset_id
        if not resolved:
            raise ValueError("dataset_name (or dataset_id) is required")
        body: dict[str, Any] = {"dataset_name": resolved, **kwargs}
        if evaluation_config is not None:
            body["evaluation_config"] = evaluation_config
        return self._request(
            "POST", f"/retrievers/{retriever_id}/evaluations", body=body
        )

    def list(self, retriever_id: str) -> dict[str, Any]:
        """List evaluations for a retriever."""
        return self._request("GET", f"/retrievers/{retriever_id}/evaluations")

    def get(self, retriever_id: str, evaluation_id: str) -> dict[str, Any]:
        """Get a single evaluation record (status, metrics, per-query results)."""
        return self._request(
            "GET", f"/retrievers/{retriever_id}/evaluations/{evaluation_id}"
        )


class Tasks(_Resource):
    """Poll and manage async background tasks (e.g. namespace clones, batches)."""

    def get(self, task_id: str) -> dict[str, Any]:
        """Get a task's status and result (poll this for async clone/batch jobs)."""
        return self._request("GET", f"/tasks/{task_id}")

    def list(self, **kwargs: Any) -> dict[str, Any]:
        """List tasks (optionally filtered via keyword args)."""
        return self._request("POST", "/tasks/list", body=kwargs or None)

    def delete(self, task_id: str) -> dict[str, Any]:
        """Kill / cancel a running task."""
        return self._request("DELETE", f"/tasks/{task_id}")
