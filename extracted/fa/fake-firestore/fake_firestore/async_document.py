from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional

from fake_firestore.document import FakeDocumentReference, FakeDocumentSnapshot

if TYPE_CHECKING:
    from fake_firestore.async_collection import AsyncFakeCollectionReference


class AsyncFakeDocumentReference(FakeDocumentReference):
    async def get(  # type: ignore[override]
        self,
        field_paths: Optional[Iterable[str]] = None,
        transaction: Any = None,
        retry: Any = None,
        timeout: Optional[float] = None,
    ) -> FakeDocumentSnapshot:
        return super().get(
            field_paths=field_paths, transaction=transaction, retry=retry, timeout=timeout
        )

    async def set(self, data: Dict[str, Any], merge: bool = False) -> None:  # type: ignore[override]
        if merge:
            from fake_firestore import NotFound

            try:
                await self.update(data)
            except NotFound:
                await self.set(data)
        else:
            FakeDocumentReference.set(self, data, merge=False)

    async def update(self, data: Dict[str, Any]) -> None:  # type: ignore[override]
        super().update(data)

    async def delete(self) -> None:  # type: ignore[override]
        super().delete()

    async def create(self, data: Dict[str, Any]) -> None:  # type: ignore[override]
        super().create(data)

    def collection(self, name: str) -> AsyncFakeCollectionReference:
        from fake_firestore.async_collection import AsyncFakeCollectionReference

        new_path = self._path + [name]
        return AsyncFakeCollectionReference(
            self._data, new_path, parent=self, written_docs=self._written_docs
        )

    async def collections(self) -> List[AsyncFakeCollectionReference]:  # type: ignore[override]
        from fake_firestore.async_collection import AsyncFakeCollectionReference

        assert self._collection_factory is not None
        try:
            from fake_firestore._helpers import get_by_path

            node = get_by_path(self._data, self._path)
        except (KeyError, TypeError):
            return []
        if not isinstance(node, dict):
            return []
        result: List[AsyncFakeCollectionReference] = []
        for key, value in node.items():
            if isinstance(value, dict):
                child_path = self._path + [key]
                if any(wp[: len(child_path)] == tuple(child_path) for wp in self._written_docs):
                    result.append(
                        AsyncFakeCollectionReference(
                            self._data, child_path, parent=self, written_docs=self._written_docs
                        )
                    )
        return result
