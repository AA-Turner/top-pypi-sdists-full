import abc
from typing import Generic, TypeVar
from uuid import UUID

from picsellia.sdk.asset import Asset, MultiAsset
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data, MultiData
from picsellia.sdk.multi_object import MultiObject
from picsellia.sdk.polygon import Polygon
from picsellia.sdk.rectangle import Rectangle
from picsellia.services.lister.asset_lister import AssetFilter, AssetLister
from picsellia.services.lister.data_lister import DataFilter, DataLister

TItem = TypeVar("TItem", bound=Dao)


class VisualSearchService(abc.ABC, Generic[TItem]):
    def __init__(self, connection: Connection):
        self.connection = connection

    def query_visual_search(self, query: str, limit: int) -> MultiObject[TItem]:
        r = self.connection.get(
            self.build_url_query(),
            params={"visual_search_query": query, "visual_search_limit": limit},
        ).json()
        result = {}
        data_scores = {}
        for point in r["points"]:
            data_scores[point["id"]] = point["score"]
            result[point["id"]] = None

        items = self.list_items_from_ids(list(data_scores.keys()))
        for item in items:
            item._score = data_scores[str(item.id)]
            result[str(item.id)] = item

        ordered_data = [item for item in result.values() if item]
        return self.build_multi_object(ordered_data)

    def list_embeddings(
        self,
        limit: int,
        with_vector: bool,
        with_payload: bool,
        has_error: bool | None,
    ) -> list[dict]:
        points = []
        offset = None
        while len(points) < limit:
            r = self.connection.get(
                self.build_url_list(),
                params={
                    "with_vector": with_vector,
                    "with_payload": with_payload,
                    "has_error": has_error,
                    "limit": min(limit, 100),
                    "offset": offset,
                    **self.get_additional_scroll_params(),
                },
            ).json()
            points.extend(r["points"])
            offset = r["next_page_offset"]
            if offset is None:
                break

        return points

    @abc.abstractmethod
    def build_url_query(self) -> str:
        pass

    @abc.abstractmethod
    def build_url_list(self) -> str:
        pass

    @abc.abstractmethod
    def list_items_from_ids(self, ids: list[str]) -> list[Data]:
        pass

    @abc.abstractmethod
    def build_multi_object(self, items: list[TItem]) -> MultiObject[TItem]:
        pass

    @staticmethod
    def get_additional_scroll_params() -> dict:
        return {}


class DatalakeVisualSearchService(VisualSearchService[Data]):
    def __init__(self, connection: Connection, datalake_id: UUID):
        super().__init__(connection)
        self.datalake_id = datalake_id

    def build_url_query(self) -> str:
        return f"/api/datalake/{self.datalake_id}/datas/ids/visual-search"

    def build_url_list(self) -> str:
        return f"/api/visual-search/datalake/{self.datalake_id}/points/scroll"

    def list_items_from_ids(self, ids: list[str]) -> list[Data]:
        return DataLister(self.connection, self.datalake_id).list_items(
            filters=DataFilter.model_validate({"ids": ids})
        )

    def build_multi_object(self, items: list[Data]) -> MultiData:
        return MultiData(self.connection, datalake_id=self.datalake_id, items=items)


class DatasetVersionVisualSearchService(VisualSearchService[Asset]):
    def __init__(self, connection: Connection, dataset_version_id: UUID):
        super().__init__(connection)
        self.dataset_version_id = dataset_version_id

    def build_url_query(self) -> str:
        return f"/api/dataset/version/{self.dataset_version_id}/datas/ids/visual-search"

    def build_url_list(self) -> str:
        return f"/api/visual-search/dataset-version/{self.dataset_version_id}/points/scroll"

    def list_items_from_ids(self, ids: list[str]) -> list[Asset]:
        return AssetLister(self.connection, self.dataset_version_id).list_items(
            filters=AssetFilter.model_validate({"ids": ids})
        )

    def build_multi_object(self, items: list[Asset]) -> MultiAsset:
        return MultiAsset(self.connection, self.dataset_version_id, items=items)


class RectangleVisualSearchService(VisualSearchService[Rectangle]):
    def __init__(self, connection: Connection, dataset_version_id: UUID):
        super().__init__(connection)
        self.dataset_version_id = dataset_version_id

    def build_url_query(self) -> str:
        raise NotImplementedError()

    def list_items_from_ids(self, ids: list[str]) -> list[Rectangle]:
        raise NotImplementedError()

    def build_multi_object(self, items: list[Rectangle]) -> MultiObject[Rectangle]:
        raise NotImplementedError()

    def build_url_list(self) -> str:
        return f"/api/dataset/version/{self.dataset_version_id}/embeddings/shapes"

    @staticmethod
    def get_additional_scroll_params() -> dict:
        return {"shape_type": "rectangle"}


class PolygonVisualSearchService(VisualSearchService[Polygon]):
    def __init__(self, connection: Connection, dataset_version_id: UUID):
        super().__init__(connection)
        self.dataset_version_id = dataset_version_id

    def build_url_query(self) -> str:
        raise NotImplementedError()

    def list_items_from_ids(self, ids: list[str]) -> list[Polygon]:
        raise NotImplementedError()

    def build_multi_object(self, items: list[Polygon]) -> MultiObject[Polygon]:
        raise NotImplementedError()

    def build_url_list(self) -> str:
        return f"/api/dataset/version/{self.dataset_version_id}/embeddings/shapes"

    @staticmethod
    def get_additional_scroll_params() -> dict:
        return {"shape_type": "polygon"}
