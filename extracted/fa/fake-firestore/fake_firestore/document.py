from __future__ import annotations

import operator
from copy import deepcopy
from functools import reduce
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional

from fake_firestore import AlreadyExists, NotFound
from fake_firestore._helpers import (
    Document,
    Store,
    Timestamp,
    delete_by_path,
    get_by_path,
    set_by_path,
)
from fake_firestore._transformations import apply_transformations

if TYPE_CHECKING:
    from fake_firestore.collection import FakeCollectionReference


class FakeDocumentSnapshot:
    def __init__(self, reference: FakeDocumentReference, data: Document | None) -> None:
        self.reference = reference
        self._doc = deepcopy(data) if data is not None else None

    @property
    def id(self) -> str:
        return self.reference.id

    @property
    def exists(self) -> bool:
        return self._doc is not None

    def to_dict(self) -> Document | None:
        return self._doc

    @property
    def create_time(self) -> Timestamp:
        timestamp = Timestamp.from_now()
        return timestamp

    @property
    def update_time(self) -> Timestamp:
        return self.create_time

    @property
    def read_time(self) -> Timestamp:
        timestamp = Timestamp.from_now()
        return timestamp

    def get(self, field_path: str) -> Any:
        if not self.exists or self._doc is None:
            return None
        return reduce(operator.getitem, field_path.split("."), self._doc)

    def _get_by_field_path(self, field_path: str) -> Any:
        try:
            return self.get(field_path)
        except KeyError:
            return None


class FakeDocumentReference:
    def __init__(
        self,
        data: Store,
        path: List[str],
        parent: FakeCollectionReference,
        written_docs: set[tuple[str, ...]] | None = None,
        _collection_factory: Callable[..., FakeCollectionReference] | None = None,
    ) -> None:
        self._data = data
        self._path = path
        self.parent = parent
        self._written_docs: set[tuple[str, ...]] = (
            written_docs if written_docs is not None else set()
        )
        self._collection_factory = _collection_factory

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FakeDocumentReference):
            return NotImplemented
        return self._path == other._path

    def __hash__(self) -> int:
        return hash(tuple(self._path))

    @property
    def id(self) -> str:
        return self._path[-1]

    @property
    def path(self) -> str:
        return "/".join(self._path)

    def get(
        self,
        field_paths: Optional[Iterable[str]] = None,
        transaction: Any = None,
        retry: Any = None,
        timeout: Optional[float] = None,
    ) -> FakeDocumentSnapshot:
        if tuple(self._path) not in self._written_docs:
            return FakeDocumentSnapshot(self, None)
        try:
            data = get_by_path(self._data, self._path)
        except KeyError:
            data = {}
        if field_paths is not None:
            data = {k: v for k, v in data.items() if k in field_paths}
        return FakeDocumentSnapshot(self, data)

    def create(self, data: Dict[str, Any], timeout: Optional[float] = None) -> None:
        """Create a new document with the given data.

        Raises AlreadyExists if the document already exists.
        """
        if tuple(self._path) in self._written_docs:
            raise AlreadyExists(f"Document already exists: {self._path}")  # type: ignore[no-untyped-call]
        set_by_path(self._data, self._path, deepcopy(data))
        self._written_docs.add(tuple(self._path))

    def delete(self, timeout: Optional[float] = None) -> None:
        delete_by_path(self._data, self._path)
        self._written_docs.discard(tuple(self._path))

    def set(
        self, data: Dict[str, Any], merge: bool = False, timeout: Optional[float] = None
    ) -> None:
        if merge:
            try:
                self.update(deepcopy(data))
            except NotFound:
                self.set(data)
        else:
            data = deepcopy(data)
            document: Dict[str, Any] = {}
            apply_transformations(document, data)
            set_by_path(self._data, self._path, document)
            self._written_docs.add(tuple(self._path))

    def update(self, data: Dict[str, Any], timeout: Optional[float] = None) -> None:
        if tuple(self._path) not in self._written_docs:
            raise NotFound("No document to update: {}".format(self._path))  # type: ignore[no-untyped-call]
        document = get_by_path(self._data, self._path)

        apply_transformations(document, deepcopy(data))

    def collection(self, name: str) -> FakeCollectionReference:
        assert self._collection_factory is not None
        new_path = self._path + [name]
        return self._collection_factory(
            self._data, new_path, parent=self, written_docs=self._written_docs
        )

    def collections(self, timeout: Optional[float] = None) -> List[FakeCollectionReference]:
        assert self._collection_factory is not None
        try:
            node = get_by_path(self._data, self._path)
        except (KeyError, TypeError):
            return []
        if not isinstance(node, dict):
            return []
        result = []
        for key, value in node.items():
            if isinstance(value, dict):
                child_path = self._path + [key]
                # Only include if any written doc exists under this path
                if any(wp[: len(child_path)] == tuple(child_path) for wp in self._written_docs):
                    result.append(
                        self._collection_factory(
                            self._data, child_path, parent=self, written_docs=self._written_docs
                        )
                    )
        return result


# Backward compatibility aliases
DocumentSnapshot = FakeDocumentSnapshot
DocumentReference = FakeDocumentReference
