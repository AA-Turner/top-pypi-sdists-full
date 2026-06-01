import logging
from uuid import UUID

import orjson
from beartype import beartype

import picsellia.exceptions as exceptions
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.data import Data
from picsellia.sdk.downloadable import Downloadable
from picsellia.sdk.label import Label
from picsellia.sdk.multi_object import MultiObject
from picsellia.types.enums import DataType
from picsellia.types.schemas import PredictedAssetSchema

logger = logging.getLogger("picsellia")


class PredictedAsset(Dao, Downloadable):
    def __init__(self, connexion: Connection, deployment_id: UUID, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)

        self._deployment_id = deployment_id

    @property
    def deployment_id(self) -> UUID:
        """UUID of (Deployment) where this (PredictedAsset) is"""
        return self._deployment_id

    @property
    def data_id(self) -> UUID:
        """UUID of (Data) of this (PredictedAsset)"""
        return self._data_id

    @property
    def oracle_prediction_id(self) -> UUID:
        """Oracle prediction if of this predicted asset"""
        return self._oracle_prediction_id

    @property
    def object_name(self) -> str:
        """Object name of this (PredictedAsset)"""
        return self._object_name

    @property
    def filename(self) -> str:
        """Filename of this (PredictedAsset)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If true, this (Asset) file is considered large"""
        return True

    @property
    def type(self) -> DataType:
        """Type of this (PredictedAsset)"""
        return self._type

    @property
    def width(self) -> int:
        """Width of this (PredictedAsset)."""
        return self._width

    @property
    def height(self) -> int:
        """Height of this (PredictedAsset)."""
        return self._height

    @property
    def metadata(self) -> dict | None:
        """Metadata of this Data. Can be None"""
        return self._metadata

    def __str__(self):
        return f"{Colors.BLUE}PredictedAsset '{self.filename}' ({self.type}) {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> PredictedAssetSchema:
        schema = PredictedAssetSchema(**data)
        self._data_id = schema.data.id
        self._oracle_prediction_id = schema.oracle_prediction_id

        # Downloadable properties
        self._object_name = schema.data.object_name
        self._filename = schema.data.filename
        self._url = schema.data.url
        self._metadata = schema.data.metadata

        self._type = schema.data.type
        self._height = schema.data.meta.height
        self._width = schema.data.meta.width

        self._champion_prediction = None
        self._shadow_prediction = None
        self._review = None
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/predicted/asset/{self.id}").json()
        self.refresh(r)
        self._load_predictions(r["predictions"], r["reviews"])
        return r

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this Asset by calling platform.

        Returns:
            A url as str of this Asset.
        """
        r = self.connection.get(f"/api/data/{self.data_id}/presigned-url")
        self._url = r.json()["presigned_url"]
        return self._url

    @exception_handler
    @beartype
    def get_data(self):
        """Retrieve data of this asset

            ```python
            data = asset.get_data()
            assert data.id == asset.data_id
            assert data.filename == asset.filename
            ```

        Returns:
            A (Data) object
        """
        r = self.connection.get(f"/api/data/{self.data_id}").json()
        return Data(self.connection, UUID(r["datalake_id"]), r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this predicted asset from its deployment

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this predicted asset

        Examples:
            ```python
            one_asset.delete()
            ```
        """
        self.connection.delete(f"/api/predicted/asset/{self.id}")
        logger.info(f"{self} removed from deployment")

    @exception_handler
    @beartype
    def add_review(
        self,
        rectangles: list[tuple[int, int, int, int, Label]] | None = None,
        polygons: list[tuple[list[list[int]], Label]] | None = None,
        classifications: list[Label] | None = None,
        lines: list[tuple[list[list[int]], Label]] | None = None,
        points: list[tuple[list[int], Label]] | None = None,
    ):
        """Add a review to your predicted-asset.
           It will then be used along the prediction for the monitoring.

        :warning: **DANGER ZONE**: You will not be able to change it afterward and
            the monitoring metrics will not be able to be computed again with another review.

        This method allowed string as label names, it's not longer the case

        Examples:
            ```python
            labels = deployment.list_labels()
            one_annotation.overwrite(rectangles=[(10, 20, 30, 40, labels[0]), (50, 60, 20, 30, labels[1])])
            ```

        Arguments:
            rectangles (list[tuple[int, int, int, int, Label]], optional): List of rectangles of this review. Defaults to None.
            polygons (list[tuple[list[list[int]], Label]], optional): List of polygons of this review. Defaults to None.
            classifications (list[Label], optional): List of classifications of this review. Defaults to None.
            lines (list[tuple[list[list[int]], Label]], optional): List of lines of this review. Defaults to None.
            points (list[tuple[list[int], Label]], optional): List of points of this review. Defaults to None.
        """
        payload = {}
        if rectangles:
            payload["rectangles"] = [
                {
                    "x": rectangle[0],
                    "y": rectangle[1],
                    "w": rectangle[2],
                    "h": rectangle[3],
                    "label_id": rectangle[4].id,
                }
                for rectangle in rectangles
            ]

        if polygons:
            payload["polygons"] = [
                {"polygon": polygon[0], "label_id": polygon[1].id}
                for polygon in polygons
            ]
        if classifications:
            payload["classifications"] = [
                {"label_id": classification.id} for classification in classifications
            ]
        if lines:
            payload["lines"] = [
                {"line": line[0], "label_id": line[1].id} for line in lines
            ]
        if points:
            payload["points"] = [
                {"point": point[0], "label_id": point[1].id} for point in points
            ]
        r = self.connection.post(
            f"/api/predicted/asset/{self.id}/reviews", data=orjson.dumps(payload)
        ).json()
        logger.info(f"{self} has been reviewed.")
        return r

    @exception_handler
    @beartype
    def get_champion_prediction(self) -> dict:
        """This will return a dict with data representing champion prediction of this asset"""
        if self._champion_prediction:
            return self._champion_prediction

        data = self.sync()
        self._load_predictions(data["predictions"], data["reviews"])
        return self._champion_prediction

    @exception_handler
    @beartype
    def get_shadow_prediction(self) -> dict | None:
        """This will return a dict with data representing shadow prediction of this asset"""
        if self._shadow_prediction:
            return self._shadow_prediction

        data = self.sync()
        self._load_predictions(data["predictions"], data["reviews"])
        return self._shadow_prediction

    @exception_handler
    @beartype
    def get_review(self) -> dict | None:
        """This will return a dict with data representing the last review created on this asset"""
        if self._review:
            return self._review

        data = self.sync()
        self._load_predictions(data["predictions"], data["reviews"])
        return self._review

    def _load_predictions(
        self, predictions: list[dict] | None, reviews: list[dict] | None
    ) -> None:
        if predictions:
            for prediction in predictions:
                if prediction["is_shadow"]:
                    self._shadow_prediction = prediction
                else:
                    self._champion_prediction = prediction

        if reviews:
            self._review = reviews[-1]


class MultiPredictedAsset(MultiObject[PredictedAsset]):
    @beartype
    def __init__(
        self,
        connexion: Connection,
        deployment_id: UUID,
        items: list[PredictedAsset],
    ):
        MultiObject.__init__(self, connexion, items)
        self.deployment_id = deployment_id

    def __str__(self) -> str:
        return f"{Colors.GREEN}MultiPredictedAsset for deployment {self.deployment_id} {Colors.ENDC}, size: {len(self)}"

    def __getitem__(self, key) -> "PredictedAsset | MultiPredictedAsset":
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            assets = [self.items[i] for i in indices]
            return MultiPredictedAsset(self.connection, self.deployment_id, assets)
        return self.items[key]

    @beartype
    def __add__(self, other) -> "MultiPredictedAsset":
        self.assert_same_connection(other)
        items = self.items.copy()
        if isinstance(other, MultiPredictedAsset):
            items.extend(other.items.copy())
        elif isinstance(other, PredictedAsset):
            items.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return MultiPredictedAsset(self.connection, self.deployment_id, items)

    @beartype
    def __iadd__(self, other) -> "MultiPredictedAsset":
        self.assert_same_connection(other)

        if isinstance(other, MultiPredictedAsset):
            self.extend(other.items.copy())
        elif isinstance(other, PredictedAsset):
            self.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

        return self
