from __future__ import annotations

from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import select

from .provider import StorageProvider


class PostgresStorageProvider(StorageProvider):
    def __init__(
        self,
        engine: AsyncEngine,
        model: type,
        *,
        id_field: str = "id",
        tg_id_field: str = "tg_id",
        wallet_field: str = "wallet_address",
        sub_field: str = "sub",
        tg_id_transform: Callable[[Any], Any] | None = None,
        model_to_dict: Callable[[Any], dict] | None = None,
    ):
        self.engine = engine
        self.model = model
        self.id_field = id_field
        self.tg_id_field = tg_id_field
        self.wallet_field = wallet_field
        self.sub_field = sub_field
        self.tg_id_transform = tg_id_transform
        self.model_to_dict = model_to_dict

    def _normalize_tg_id(self, tg_id: Any) -> Any:
        if self.tg_id_transform is None:
            return tg_id
        return self.tg_id_transform(tg_id)

    def _build_sub_from_tg_id(self, tg_id: Any) -> str:
        return f"tg:{tg_id}"

    def _filter_known_fields(self, data: dict) -> dict:
        return {key: value for key, value in data.items() if hasattr(self.model, key)}

    def _coerce_user_data(self, user_data: dict) -> dict:
        processed = dict(user_data)
        if self.tg_id_field in processed and processed[self.tg_id_field] is not None:
            raw_tg_id = processed[self.tg_id_field]
            if self.sub_field and not processed.get(self.sub_field):
                processed[self.sub_field] = self._build_sub_from_tg_id(raw_tg_id)
            processed[self.tg_id_field] = self._normalize_tg_id(raw_tg_id)
        return self._filter_known_fields(processed)

    def _model_to_dict(self, instance: Any) -> dict:
        if self.model_to_dict is not None:
            return self.model_to_dict(instance)
        if hasattr(instance, "dict"):
            return instance.dict()
        raise TypeError("model_to_dict is required for this model")

    async def retrieve_user(self, search_query: dict) -> dict:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = dict(search_query)
            raw_tg_id = query.get(self.tg_id_field)
            if (
                raw_tg_id is not None
                and self.sub_field
                and self.sub_field not in query
                and hasattr(self.model, self.sub_field)
            ):
                statement = select(self.model).where(
                    getattr(self.model, self.sub_field) == self._build_sub_from_tg_id(raw_tg_id)
                )
                result = await session.execute(statement)
                user = result.scalars().first()
                if user:
                    return self._model_to_dict(user)

            if raw_tg_id is not None:
                query[self.tg_id_field] = self._normalize_tg_id(raw_tg_id)

            filtered = self._filter_known_fields(query)
            if not filtered:
                return {}

            statement = select(self.model).where(
                *(getattr(self.model, key) == value for key, value in filtered.items())
            )
            result = await session.execute(statement)
            user = result.scalars().first()
            return self._model_to_dict(user) if user else {}

    async def update_user(self, id: str, update_data: dict) -> tuple[int, str | None]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            statement = select(self.model).where(getattr(self.model, self.id_field) == id)
            result = await session.execute(statement)
            user = result.scalars().first()
            if not user:
                return 0, "User not found"

            processed = self._coerce_user_data(update_data)
            for key, value in processed.items():
                setattr(user, key, value)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return 1, None

    async def insert_user(self, user_data: dict) -> int:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            processed = self._coerce_user_data(user_data)
            user = self.model(**processed)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return getattr(user, self.id_field)

    async def delete_user(self, id: int) -> tuple[int, str | None]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            statement = select(self.model).where(getattr(self.model, self.id_field) == int(id))
            result = await session.execute(statement)
            user = result.scalars().first()
            if not user:
                return 0, "User not found"
            await session.delete(user)
            await session.commit()
            return 1, None

    async def merge_accounts(
        self, from_account_id: int, to_account_id: int
    ) -> tuple[int, str | None]:
        _ = (from_account_id, to_account_id)
        return 0, "merge_accounts is not implemented for this storage provider"
