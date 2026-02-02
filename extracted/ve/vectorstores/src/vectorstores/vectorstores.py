from __future__ import annotations

import datetime
import logging
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
)
from uuid import uuid4
import numpy as np
import weaviate  # type: ignore
from vectorstores.base import VectorStore

logger = logging.getLogger(__name__)


def _default_schema(index_name: str) -> Dict:
    return {
        "class": index_name,
        "properties": [
            {
                "name": "text",
                "dataType": ["text"],
            }
        ],
    }


def _default_score_normalizer(val: float) -> float:
    # prevent overflow
    # use 709 because that's the largest exponent that doesn't overflow
    # use -709 because that's the smallest exponent that doesn't underflow
    val = np.clip(val, -709, 709)
    return 1 - 1 / (1 + np.exp(val))


def _json_serializable(value: Any) -> Any:
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return value


@dataclass
class Vector:
    """
    Schema for rows sent to or returned from the vector store.
    """

    text: Optional[str] = None
    uuid: Optional[str] = None
    vector: Any = None  # NumPy array of embedding values
    metadata: Dict[str, Any] = field(default_factory=dict)


class WeaviateVectorStore(VectorStore):
    """Weaviate vector store.

    To use, you should have the `weaviate-client` python package installed.

    Example:
        ```python
        import weaviate
        from langchain_community.vectorstores import Weaviate

        client = weaviate.Client(url=os.environ["WEAVIATE_URL"], ...)
        weaviate = Weaviate(client, index_name, text_key)
        ```
    """

    def __init__(
        self,
        client: weaviate.WeaviateClient,
        index_name: Optional[str],
        text_key: str,
        relevance_score_fn: Optional[
            Callable[[float], float]
        ] = _default_score_normalizer,
        use_multi_tenancy: bool = False,
    ):
        """Initialize with Weaviate client."""
        self._client = client
        self._index_name = index_name or f"LangChain_{uuid4().hex}"
        self._text_key = text_key
        self.relevance_score_fn = relevance_score_fn

        schema = _default_schema(self._index_name)
        schema["MultiTenancyConfig"] = {"enabled": use_multi_tenancy}

        # check whether the index already exists
        if not client.collections.exists(self._index_name):
            client.collections.create_from_dict(schema)

        # store collection for convenience
        # this does not actually send a request to weaviate
        self._collection = client.collections.get(self._index_name)

        # store this setting so we don't have to send a request to weaviate
        # every time we want to do a CRUD operation
        self._multi_tenancy_enabled = self._collection.config.get(
            simple=False
        ).multi_tenancy_config.enabled

    def add_vector(
        self,
        vectors: Iterable[Vector],  # added vector compatibility
        metadatas: Optional[List[dict]] = None,
        tenant: Optional[str] = None,
        ids: Optional[Any] = None,  # added this for later search
        **kwargs: Any,
    ) -> List[str]:
        """Upload vectors with metadata (properties) to Weaviate."""
        from weaviate.util import generate_uuid5  # type: ignore

        if tenant and not self._does_tenant_exist(tenant):
            logger.info(
                f"Tenant {tenant} does not exist in index {self._index_name}. "
                "Creating tenant."
            )
            tenant_objs = [weaviate.classes.tenants.Tenant(name=tenant)]
            self._collection.tenants.create(tenants=tenant_objs)

        ids = []

        with self._client.batch.dynamic() as batch:
            for i, vector_obj in enumerate(vectors):
                text_val = getattr(vector_obj, "text", None)
                data_properties: Dict[str, Any] = {}
                if text_val is not None:
                    data_properties[self._text_key] = text_val
                if metadatas is not None:
                    for key, val in metadatas[i].items():
                        data_properties[key] = _json_serializable(val)
                # Allow for ids (consistent w/ other methods)
                # # Or uuids (backwards compatible w/ existing arg)
                # If the UUID of one of the objects already exists
                # then the existing object will be replaced by the new object.
                _id = generate_uuid5(vector_obj)
                if "uuids" in kwargs:
                    _id = kwargs["uuids"][i]
                elif "ids" in kwargs:
                    _id = kwargs["ids"][i]

                batch.add_object(
                    collection=self._index_name,
                    properties=data_properties,
                    uuid=_id,
                    vector=vector_obj.vector,
                    tenant=tenant,
                )
                ids.append(_id)

        failed_objs = self._client.batch.failed_objects
        for obj in failed_objs:
            err_message = (
                f"Failed to add object: {obj.original_uuid}\nReason: {obj.message}"
            )
            logger.error(err_message)
        return ids

    def delete(
        self,
        ids: Optional[List[str]] = None,
        tenant: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Delete by vector IDs.

        Args:
            ids: List of ids to delete.
            tenant: The tenant name.
        """

        if ids is None:
            raise ValueError("No ids provided to delete.")

        id_filter = weaviate.classes.query.Filter.by_id().contains_any(ids)

        with self._tenant_context(tenant) as collection:
            collection.data.delete_many(where=id_filter)

    def _does_tenant_exist(self, tenant: str) -> bool:
        """Check if tenant exists in Weaviate."""
        assert self._multi_tenancy_enabled, (
            "Cannot check for tenant existence when multi-tenancy is not enabled"
        )
        tenants = self._collection.tenants.get()

        return tenant in tenants

    @contextmanager
    def _tenant_context(
        self, tenant: Optional[str] = None
    ) -> Generator[weaviate.collections.Collection, None, None]:
        """Context manager for handling tenants.

        Args:
            tenant: The tenant name.
        """

        if tenant is not None and not self._multi_tenancy_enabled:
            raise ValueError(
                "Cannot use tenant context when multi-tenancy is not enabled"
            )

        if tenant is None and self._multi_tenancy_enabled:
            raise ValueError("Must use tenant context when multi-tenancy is enabled")

        try:
            yield self._collection.with_tenant(tenant)
        finally:
            pass

    def similarity_search(
        self,
        vector: Optional[Sequence[float]],
        k: int = 4,
        tenant: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Vector]:
        """
        Perform a nearest-neighbor search using a provided embedding vector.

        Parameters:
            vector: Embedding to search against.
            k: Number of neighbors to return.
            tenant: Optional Weaviate tenant name.
            **kwargs: Extra keyword arguments forwarded to `collection.query.near_vector`.

        Returns:
            List of `Vector` objects for the top `k` hits.
        """
        return_uuids = kwargs.pop("return_uuids", False)

        with self._tenant_context(tenant) as collection:
            try:
                include_vector = kwargs.pop("include_vector", True)
                # Weaviate client expects the payload under the `near_vector` keyword.
                result = collection.query.near_vector(
                    near_vector=vector,
                    limit=k,
                    include_vector=include_vector,
                    **kwargs,
                )  # type: ignore[operator]
            except weaviate.exceptions.WeaviateQueryException as e:
                raise ValueError(f"Error during query: {e}")

        docs: List[Vector] = []
        for obj in result.objects:
            # Merge Weaviate properties and decoded metadata payload.
            merged_metadata: Dict[str, Any] = {}
            for key, value in obj.properties.items():
                if key == self._text_key:
                    continue
                if key == "metadata" and isinstance(value, str):
                    try:
                        merged_metadata.update(json.loads(value))
                    except json.JSONDecodeError:
                        merged_metadata[key] = value
                else:
                    merged_metadata[key] = value

            if obj.vector and "default" in obj.vector:
                merged_metadata["vector"] = obj.vector

            if return_uuids:
                merged_metadata["uuid"] = str(obj.uuid)

            vector_payload = merged_metadata.pop("vector", None)
            # Prefer UUID we added to metadata; fall back to object's UUID if available.
            doc_uuid = merged_metadata.get("uuid")

            doc = Vector(
                text=obj.properties.get(self._text_key),
                uuid=doc_uuid,
                vector=vector_payload,
                metadata=merged_metadata,
            )
            docs.append(doc)

        return docs
