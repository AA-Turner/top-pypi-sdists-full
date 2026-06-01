import abc
import logging
from functools import partial
from typing import Any, Generic, TypeVar
from uuid import UUID

from orjson import orjson
from pydantic import BaseModel, Field

from picsellia import pxl_multithreading as mlt
from picsellia.compatibility import add_data_mandatory_query_parameters
from picsellia.pxl_multithreading import do_paginate
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.utils import flatten

logger = logging.getLogger(__name__)


class BaseFilter(BaseModel):
    limit: int | None = Field(default=None, gt=0)
    offset: int | None = Field(default=None, ge=0)
    order_by: list[str] | None = None
    query: str | None = None

    def has_list_of_items(self) -> bool:
        pass


TItem = TypeVar("TItem", bound=Dao)
TFilter = TypeVar("TFilter", bound=BaseFilter)


class AbstractItemLister(abc.ABC, Generic[TItem, TFilter]):
    def __init__(self, connection: Connection):
        self.connection = connection

    def list_items(self, filters: TFilter) -> list[TItem]:
        if filters.has_list_of_items():
            return self._chunk_filter_and_fetch_items(filters)
        else:
            return self._list_items_with_pagination(filters)

    def list_ids(
        self,
        limit: int | None = None,
        offset: int | None = None,
        query: str | None = None,
    ) -> list[UUID]:
        return do_paginate(
            limit,
            offset,
            10000,
            partial(self._fetch_paginated_ids, query),
        )

    @abc.abstractmethod
    def _get_query_param_and_items_from_filters(
        self, filters: TFilter
    ) -> tuple[str, list]:
        pass

    @abc.abstractmethod
    def _get_other_params(self, filters: TFilter) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    def _get_path(self) -> str:
        pass

    @abc.abstractmethod
    def _build_item(self, data: dict) -> TItem:
        pass

    def _chunk_filter_and_fetch_items(self, filters: TFilter) -> list[TItem]:
        query_param, items = self._get_query_param_and_items_from_filters(filters)
        base_params = self._get_other_params(filters)

        paginate_fn = partial(
            self._call_xget_for_one_chunk,
            filters.query,
            filters.order_by,
            base_params,
            query_param,
        )

        return flatten(
            mlt.do_chunk_called_function(
                items,
                f=paginate_fn,
                chunk_size=1000,
            )
        )

    def _call_xget_for_one_chunk(
        self,
        query: str | None,
        order_by: list[str] | None,
        base_params: dict,
        query_param: str,
        items: list,
    ) -> list[TItem]:
        params = base_params.copy()
        if order_by:
            params["order_by"] = order_by

        payload: dict[str, Any] = {query_param: items}
        if query:
            payload["q"] = query

        return self._call_xget(params, payload)[0]

    def _call_xget(self, params: dict, payload: dict) -> tuple[list[TItem], int]:
        add_data_mandatory_query_parameters(payload)
        content = self.connection.xget(
            self._get_path(),
            params=params,
            data=orjson.dumps(payload),
        ).json()
        return self._parse_response(content)

    def _list_items_with_pagination(self, filters: TFilter) -> list[TItem]:
        base_params = self._get_other_params(filters)
        paginate_fn = partial(
            self._call_get_for_one_page, filters.query, filters.order_by, base_params
        )
        return mlt.do_paginate(filters.limit, filters.offset, None, paginate_fn)

    def _call_get_for_one_page(
        self,
        query: str | None,
        order_by: list[str] | None,
        base_params: dict[str, Any],
        limit: int,
        offset: int,
    ) -> tuple[list[TItem], int]:
        params = base_params.copy()
        params["limit"] = limit
        params["offset"] = offset
        if order_by:
            params["order_by"] = order_by
        if query:
            params["q"] = query
        return self._call_get(params)

    def _call_get(self, params: dict) -> tuple[list[TItem], int]:
        add_data_mandatory_query_parameters(params)
        content = self.connection.get(self._get_path(), params=params).json()
        return self._parse_response(content)

    def _parse_response(self, content: dict) -> tuple[list[TItem], int]:
        return (
            [self._build_item(item) for item in content["items"]],
            content["count"],
        )

    def _fetch_paginated_ids(self, query: str | None, limit: int, offset: int):
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if query:
            params["q"] = query
        path = self._get_path() + "/ids/paginated"
        r = self.connection.get(path, params=params).json()
        return r["items"], r["count"]
