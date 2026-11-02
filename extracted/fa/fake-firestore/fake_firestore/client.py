from __future__ import annotations

from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Union

from fake_firestore.collection import FakeCollectionReference
from fake_firestore.document import FakeDocumentReference, FakeDocumentSnapshot
from fake_firestore.query import FakeCollectionGroup
from fake_firestore.transaction import FakeTransaction, FakeWriteBatch


class FakeFirestoreClient:
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        written_docs: Optional[set[tuple[str, ...]]] = None,
    ) -> None:
        self._data: Dict[str, Any] = data if data is not None else {}
        self._written_docs: set[tuple[str, ...]] = (
            written_docs if written_docs is not None else set()
        )

    def _ensure_path(
        self, path: List[str]
    ) -> Union[FakeFirestoreClient, FakeCollectionReference, FakeDocumentReference]:
        current_position: Union[
            FakeFirestoreClient, FakeCollectionReference, FakeDocumentReference
        ] = self

        for el in path[:-1]:
            if isinstance(current_position, (FakeFirestoreClient, FakeDocumentReference)):
                current_position = current_position.collection(el)
            else:
                current_position = current_position.document(el)

        return current_position

    def document(self, path: str) -> FakeDocumentReference:
        path_parts = path.split("/")

        if len(path_parts) % 2 != 0:
            raise Exception("Cannot create document at path {}".format(path_parts))
        current_position = self._ensure_path(path_parts)

        if isinstance(current_position, FakeCollectionReference):
            return current_position.document(path_parts[-1])
        raise Exception("Invalid path")  # pragma: no cover

    def collection(self, path: str) -> FakeCollectionReference:
        path_parts = path.split("/")

        if len(path_parts) % 2 != 1:
            raise Exception("Cannot create collection at path {}".format(path_parts))

        name = path_parts[-1]
        if len(path_parts) > 1:
            current_position = self._ensure_path(path_parts)
            if isinstance(current_position, (FakeFirestoreClient, FakeDocumentReference)):
                return current_position.collection(name)
            raise Exception("Invalid path")  # pragma: no cover
        else:
            if name not in self._data:
                self._data[name] = {}
            return FakeCollectionReference(self._data, [name], written_docs=self._written_docs)

    def collections(self, timeout: Optional[float] = None) -> Sequence[FakeCollectionReference]:
        return [
            FakeCollectionReference(self._data, [collection_name], written_docs=self._written_docs)
            for collection_name in self._data
        ]

    def reset(self) -> None:
        self._data.clear()
        self._written_docs.clear()

    def _find_collections_by_name(
        self,
        data: Dict[str, Any],
        name: str,
        current_path: List[str],
        is_collection_level: bool = True,
    ) -> List[List[str]]:
        """Recursively find all collection paths with the given name."""
        paths: List[List[str]] = []

        for key, value in data.items():
            if is_collection_level:
                # At collection level
                new_path = current_path + [key]
                if key == name:
                    paths.append(new_path)
                # Recurse into documents
                if isinstance(value, dict):
                    paths.extend(self._find_collections_by_name(value, name, new_path, False))
            else:
                # At document level - recurse into subcollections
                if isinstance(value, dict):
                    new_path = current_path + [key]
                    paths.extend(self._find_collections_by_name(value, name, new_path, True))

        return paths

    def collection_group(self, collection_id: str) -> FakeCollectionGroup:
        """Query across all collections with the given name."""
        if "/" in collection_id:
            raise ValueError(
                f"Invalid collection_id '{collection_id}'. " "Collection IDs must not contain '/'."
            )
        paths = self._find_collections_by_name(self._data, collection_id, [])
        collections = [
            FakeCollectionReference(self._data, path, written_docs=self._written_docs)
            for path in paths
        ]
        return FakeCollectionGroup(collections)

    def get_all(
        self,
        references: Iterable[FakeDocumentReference],
        field_paths: Optional[Any] = None,
        transaction: Optional[Any] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[FakeDocumentSnapshot]:
        for doc_ref in set(references):
            yield doc_ref.get()

    def transaction(self, **kwargs: Any) -> FakeTransaction:
        return FakeTransaction(self, **kwargs)

    def batch(self) -> FakeWriteBatch:
        return FakeWriteBatch(self)


# Backward compatibility alias
MockFirestore = FakeFirestoreClient
