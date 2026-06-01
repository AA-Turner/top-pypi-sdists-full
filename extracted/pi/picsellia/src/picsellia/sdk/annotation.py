import logging
from typing import Any
from uuid import UUID

import orjson
from beartype import beartype

import picsellia.pxl_multithreading as mlt
from picsellia import exceptions
from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.classification import Classification
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.label import Label
from picsellia.sdk.line import Line
from picsellia.sdk.multi_object import MultiObject
from picsellia.sdk.point import Point
from picsellia.sdk.polygon import Polygon
from picsellia.sdk.rectangle import Rectangle
from picsellia.sdk.worker import Worker
from picsellia.types.enums import AnnotationStatus
from picsellia.types.schemas import AnnotationSchema
from picsellia.utils import chunk_list

logger = logging.getLogger("picsellia")


class Annotation(Dao):
    def __init__(
        self,
        connexion: Connection,
        dataset_version_id: UUID,
        asset_id: UUID,
        data: dict,
    ) -> None:
        Dao.__init__(self, connexion, data)
        self._dataset_version_id = dataset_version_id
        self._asset_id = asset_id

    @property
    def asset_id(self) -> UUID:
        """UUID of the (Asset) holding this (Annotation)"""
        return self._asset_id

    @property
    def dataset_version_id(self) -> UUID:
        """UUID of (DatasetVersion) holding this (Annotation)"""
        return self._dataset_version_id

    @property
    def duration(self) -> float:
        """Duration time of this (Annotation)"""
        return self._duration

    @property
    def status(self) -> AnnotationStatus:
        """Status of this (Annotation)"""
        return self._status

    @property
    def attributes(self) -> dict[str, Any] | None:
        """Attributes of this (Annotation)"""
        return self._attributes

    def __str__(self):
        return f"{Colors.BLUE}Annotation on asset {self.asset_id} {Colors.ENDC} (id: {self.id})"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/annotation/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> AnnotationSchema:
        schema = AnnotationSchema(**data)
        self._duration = schema.duration
        self._status = schema.status
        self._attributes = schema.attributes
        return schema

    @exception_handler
    @beartype
    def update(
        self,
        worker: Worker | None = None,
        duration: float | int | None = None,
        status: AnnotationStatus | str | None = None,
    ) -> None:
        """Update this annotation with a new worker, a new duration or a new status.

        Worker parameter is deprecated and cannot be used anymore. It will be removed in 6.27

        Examples:
            ```python
            one_annotation.update(status=AnnotationStatus.ACCEPTED)
            ```
        Arguments:
            duration (float, optional): Duration of this annotation. Defaults to None.
            status (AnnotationStatus, optional): Status of this annotation. Defaults to None.
        """
        payload = {}
        if duration:
            payload["duration"] = float(duration)

        if worker:
            logger.warning("worker is deprecated and should not be used anymore.")

        if status:
            payload["status"] = AnnotationStatus.validate(status)

        r = self.connection.patch(
            f"/api/annotation/{self.id}", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this annotation from the platform.
        All annotations shapes will be deleted!
        This is a very dangerous move.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            one_annotation.delete()
            ```
        """
        self.connection.delete(f"/api/annotation/{self.id}")
        logger.info(f"{self} deleted from platform.")

    @exception_handler
    @beartype
    def overwrite(
        self,
        rectangles: list[tuple[int, int, int, int, Label]] | None = None,
        polygons: list[tuple[list[list[int]], Label]] | None = None,
        classifications: list[Label] | None = None,
        lines: list[tuple[list[list[int]], Label]] | None = None,
        points: list[tuple[list[int], Label]] | None = None,
        duration: float | int = 0.0,
    ) -> None:
        """Overwrite content of this annotation with a new duration and new shapes

        This method can be called on asset that are not synced in a campaign.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
            one_annotation.overwrite(rectangles=[(10, 20, 30, 40, label_cat), (50, 60, 20, 30, label_dog)])
            ```

        Arguments:
            rectangles (list[tuple[int, int, int, int, Label]], optional): List of rectangles to overwrite. Defaults to None.
            polygons (list[tuple[list[list[int]], Label]], optional): List of polygons to overwrite. Defaults to None.
            classifications (list[Label], optional): List of classifications to overwrite. Defaults to None.
            lines (list[tuple[list[list[int]], Label]], optional): List of lines to overwrite. Defaults to None.
            points (list[tuple[list[int], int, Label]], optional): List of points to overwrite. Defaults to None.
            duration (float or int, optional): Duration of this annotation. Defaults to 0.0.
        """
        payload: dict[str, Any] = {"duration": duration}
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
        if lines:
            payload["lines"] = [
                {"line": line[0], "label_id": line[1].id} for line in lines
            ]
        if points:
            payload["points"] = [
                {"point": point[0], "label_id": point[1].id} for point in points
            ]
        if classifications:
            payload["classifications"] = [
                {"label_id": classification.id} for classification in classifications
            ]

        r = self.connection.post(
            f"/api/annotation/{self.id}/save", data=orjson.dumps(payload)
        ).json()
        self.refresh(r)
        logger.info(
            f"{self} is now saved with a new content. Old shapes already retrieved are not consistent anymore."
        )

    @exception_handler
    @beartype
    def list_rectangles(self) -> list[Rectangle]:
        """Retrieve all rectangles of this annotation

        Examples:
            ```python
            rects = one_annotation.list_rectangles()
            ```

        Returns:
            List of (Rectangle) objects.
        """
        r = self.connection.get(f"/api/annotation/{self.id}/rectangles").json()
        return [
            Rectangle(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_rectangle(
        self, x: int, y: int, w: int, h: int, label: Label
    ) -> Rectangle:
        """Create a rectangle into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            rect = one_annotation.create_rectangle(420, 69, 100, 10, label_car)
            ```

        Arguments:
            x (int): x coordinate of the rectangle.
            y (int): y coordinate of the rectangle.
            w (int): width of the rectangle.
            h (int): height of the rectangle.
            label (Label): Label of the rectangle.

        Returns:
            A (Rectangle) object.
        """
        return self.create_multiple_rectangles([(x, y, w, h, label)])[0]

    @exception_handler
    @beartype
    def create_multiple_rectangles(
        self, rectangles: list[tuple[int, int, int, int, Label]]
    ) -> list[Rectangle]:
        """Create some rectangles into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            rects = one_annotation.create_multiple_rectangles([(420, 69, 100, 10, label_car), (123, 456, 20, 20, label_person)])
            ```

        Arguments:
            rectangles (list[tuple[int, int, int, int, Label]]): List of rectangles to create.

        Returns:
            List of (Rectangle) objects.
        """
        assert len(rectangles) > 0, "Please give at least one rectangle"
        payload = []
        for rectangle in rectangles:
            payload.append(
                {
                    "x": rectangle[0],
                    "y": rectangle[1],
                    "w": rectangle[2],
                    "h": rectangle[3],
                    "label_id": rectangle[4].id,
                }
            )
        payload = {"rectangles": payload}
        r = self.connection.post(
            f"/api/annotation/{self.id}/bulk-rectangles", data=orjson.dumps(payload)
        ).json()
        return [
            Rectangle(self.connection, self.dataset_version_id, self.id, item)
            for item in r["rectangles"]
        ]

    @exception_handler
    @beartype
    def list_polygons(self) -> list[Polygon]:
        """Retrieve all polygons of this annotation

        Examples:
            ```python
            polys = one_annotation.list_polygons()
            ```

        Returns:
            List of (Polygon) objects.
        """
        r = self.connection.get(f"/api/annotation/{self.id}/polygons").json()
        return [
            Polygon(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_polygon(self, coords: list[list[int]], label: Label) -> Polygon:
        """Create a polygon into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            poly = one_annotation.create_polygon([[0, 0], [0, 1], [1, 1], [0, 0]], label_car)
            ```

        Arguments:
            coords (list[list[int]]): List of coordinates of the polygon.
            label (Label): Label of the polygon.

        Returns:
            A (Polygon) object.
        """
        return self.create_multiple_polygons([(coords, label)])[0]

    @exception_handler
    @beartype
    def create_multiple_polygons(
        self, polygons: list[tuple[list[list[int]], Label]]
    ) -> list[Polygon]:
        """Create some polygons into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            polys = one_annotation.create_multiple_polygons([([[0, 0], [0, 1], [1, 1], [0, 0]] label_car), ([[0, 2], [0, 3], [1, 2], [0, 2]] label_person)])
            ```

        Arguments:
            polygons (list[tuple[list[list[int]], Label]]): List of polygons to create.

        Returns:
            List of (Polygon) objects.
        """
        assert len(polygons) > 0, "Please give at least one polygon"
        payload = []
        for polygon in polygons:
            payload.append({"polygon": polygon[0], "label_id": polygon[1].id})
        payload = {"polygons": payload}
        r = self.connection.post(
            f"/api/annotation/{self.id}/bulk-polygons", data=orjson.dumps(payload)
        ).json()
        return [
            Polygon(self.connection, self.dataset_version_id, self.id, item)
            for item in r["polygons"]
        ]

    @exception_handler
    @beartype
    def list_lines(self) -> list[Line]:
        """Retrieve all lines of this annotation

        Examples:
            ```python
            lines = one_annotation.list_lines()
            ```

        Returns:
            List of (Line) objects.
        """
        r = self.connection.get(f"/api/annotation/{self.id}/lines").json()
        return [
            Line(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_line(self, coords: list[list[int]], label: Label) -> Line:
        """Create a line into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            line = one_annotation.create_line([[0, 0], [0, 1], [1, 1], [0, 0]], label_car)
            ```

        Arguments:
            coords (list[list[int]]): List of coordinates of the line.
            label (Label): Label of the line.

        Returns:
            A (Line) object.
        """
        return self.create_multiple_lines([(coords, label)])[0]

    @exception_handler
    @beartype
    def create_multiple_lines(
        self, lines: list[tuple[list[list[int]], Label]]
    ) -> list[Line]:
        """Create some lines into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            lines = one_annotation.create_multiple_lines([([[0, 0], [0, 1], [1, 1]] label_car), ([[0, 2], [0, 3], [1, 2]] label_person)])
            ```

        Arguments:
            lines (list[tuple[list[list[int]], Label]]): List of lines to create.

        Returns:
            List of (Line) objects.
        """
        assert len(lines) > 0, "Please give at least one line"
        payload = []
        for line in lines:
            payload.append({"line": line[0], "label_id": line[1].id})
        payload = {"lines": payload}
        r = self.connection.post(
            f"/api/annotation/{self.id}/bulk-lines", data=orjson.dumps(payload)
        ).json()
        return [
            Line(self.connection, self.dataset_version_id, self.id, item)
            for item in r["lines"]
        ]

    @exception_handler
    @beartype
    def list_points(self) -> list[Point]:
        """Retrieve all points of this annotation

        Examples:
            ```python
            points = one_annotation.list_points()
            ```

        Returns:
            List of (Point) objects.
        """
        r = self.connection.get(f"/api/annotation/{self.id}/points").json()
        return [
            Point(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_point(self, coords: list[int], label: Label) -> Point:
        """Create a point into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            poly = one_annotation.create_point([0, 0], label_car)
            ```

        Arguments:
            coords (list[int]): List of coordinates of the point.
            label (Label): Label of the point.

        Returns:
            A (Point) object.
        """
        return self.create_multiple_points([(coords, label)])[0]

    @exception_handler
    @beartype
    def create_multiple_points(
        self, points: list[tuple[list[int], Label]]
    ) -> list[Point]:
        """Create some points into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            polys = one_annotation.create_multiple_points([([0, 0], label_car), ([0, 2], label_person)])
            ```

        Arguments:
            points (list[tuple[list[int], Label]]): List of points to create.

        Returns:
            List of (Point) objects.
        """
        assert len(points) > 0, "Please give at least one point"
        payload = []
        for point in points:
            payload.append({"point": point[0], "label_id": point[1].id})
        payload = {"points": payload}
        r = self.connection.post(
            f"/api/annotation/{self.id}/bulk-points", data=orjson.dumps(payload)
        ).json()
        return [
            Point(self.connection, self.dataset_version_id, self.id, item)
            for item in r["points"]
        ]

    @exception_handler
    @beartype
    def list_classifications(self) -> list[Classification]:
        """Retrieve all classifications of this annotation

        Examples:
            ```python
            classifications = one_annotation.list_classifications()
            ```

        Returns:
            List of (Classification) objects.
        """
        r = self.connection.get(f"/api/annotation/{self.id}/classifications").json()
        return [
            Classification(self.connection, self.dataset_version_id, self.id, item)
            for item in r["items"]
        ]

    @exception_handler
    @beartype
    def create_classification(self, label: Label) -> Classification:
        """Create a classification into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            classifications = one_annotation.create_classification(label_car)
            ```

        Arguments:
            label (Label): Label of the classification.

        Returns:
            A (Classification) object.
        """
        return self.create_multiple_classifications([label])[0]

    @exception_handler
    @beartype
    def create_multiple_classifications(
        self, classifications: list[Label]
    ) -> list[Classification]:
        """Create some classifications into this annotation.

        This method can be called on asset that are not synced in a campaign.

        Examples:
            ```python
            polys = one_annotation.create_multiple_classifications([label_car, label_person])
            ```

        Arguments:
            classifications (list[Label]): List of classifications to create.

        Returns:
            List of (Classification) objects.
        """
        assert len(classifications) > 0, "Please give at least one polygon"
        payload = []
        for classification in classifications:
            payload.append({"label_id": classification.id})
        payload = {"classifications": payload}
        r = self.connection.post(
            f"/api/annotation/{self.id}/bulk-classifications",
            data=orjson.dumps(payload),
        ).json()
        return [
            Classification(self.connection, self.dataset_version_id, self.id, item)
            for item in r["classifications"]
        ]


class MultiAnnotation(MultiObject[Annotation]):
    @beartype
    def __init__(
        self, connexion: Connection, dataset_version_id: UUID, items: list[Annotation]
    ):
        MultiObject.__init__(self, connexion, items)
        self._dataset_version_id = dataset_version_id

    @property
    def dataset_version_id(self) -> UUID:
        return self._dataset_version_id

    def __str__(self) -> str:
        return f"{Colors.GREEN}MultiAnnotation for dataset version {self.dataset_version_id}{Colors.ENDC}  size: {len(self)}"

    def __getitem__(self, key) -> "Annotation | MultiAnnotation":
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            annotations = [self.items[i] for i in indices]
            return MultiAnnotation(
                self.connection, self.dataset_version_id, annotations
            )
        return self.items[key]

    @beartype
    def __add__(self, other) -> "MultiAnnotation":
        self.assert_same_connection(other)
        items = self.items.copy()
        self._add_other_items_to_items(other, items)
        return MultiAnnotation(self.connection, self.dataset_version_id, items)

    @beartype
    def __iadd__(self, other) -> "MultiAnnotation":
        self.assert_same_connection(other)
        self._add_other_items_to_items(other, self.items)
        return self

    def _add_other_items_to_items(self, other, items) -> None:
        if isinstance(other, MultiAnnotation):
            if other.dataset_version_id != self.dataset_version_id:
                raise exceptions.BadRequestError(
                    "These annotations does not come from the same dataset"
                )
            items.extend(other.items.copy())
        elif isinstance(other, Annotation):
            if other.dataset_version_id != self.dataset_version_id:
                raise exceptions.BadRequestError(
                    "This annotation does not come from the same dataset"
                )
            items.append(other)
        else:
            raise exceptions.BadRequestError("You can't add these two objects")

    def copy(self) -> "MultiAnnotation":
        return MultiAnnotation(
            self.connection, self.dataset_version_id, self.items.copy()
        )

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete these annotations and their shape

        This method cannot be called on dataset with a campaign.

        :warning: **DANGER ZONE**: Be very careful here!

        Remove these annotations

        Examples:
            ```python
            some_annotations = dataset_version.list_annotations()[:10]
            some_annotations.delete()
            ```
        """
        payload = {"asset_ids": ["__all__"], "annotation_ids": self.ids}
        self.connection.delete(
            f"/api/dataset/version/{self.dataset_version_id}/annotations",
            data=orjson.dumps(payload),
        )
        logger.info(f"{len(self.items)} annotations deleted.")

    @exception_handler
    @beartype
    def load(
        self,
        chunk_size: int = 100,
        max_workers: int | None = None,
        skip_error: bool = False,
    ) -> dict:
        """Load these annotation by retrieving shapes with labels, asset_id and worker_id

        Examples:
            ```python
            annotations = foo_dataset_version.list_annotations()
            annotations_dict = annotations.load()
            ```
        Arguments:
            chunk_size (int, optional): Size of chunk of annotations to load by request. Defaults to 100.
            max_workers (int, optional): Number of max workers used to load annotations. Defaults to os.cpu_count() + 4.
            skip_error (bool, optional): skip error of a chunk and return partial annotations. Default to False

        Returns:
            Dict of annotations by asset_id
        """

        return MultiAnnotation.load_annotations_from_ids(
            self.connection,
            self.dataset_version_id,
            self.ids,
            chunk_size,
            max_workers,
            skip_error,
        )

    @staticmethod
    def load_annotations_from_ids(
        connection: Connection,
        dataset_version_id: UUID,
        ids: list[UUID],
        chunk_size: int,
        max_workers: int | None = None,
        skip_error: bool = False,
    ) -> dict:
        if chunk_size < 1 or chunk_size > 10000:
            raise exceptions.BadRequestError(
                "Impossible to load less than 1 or more than 10000 annotations by chunk. Please give another chunk_size"
            )
        elif chunk_size > 1000:
            chunk_size = 1000
            logger.warning(
                "Please lower annotation loading chuck size, limit will be enforced to 1000 in a future version."
            )

        def load_some_annotations(list_index: tuple):
            r = connection.xget(
                f"/api/dataset/version/{dataset_version_id}/annotations",
                data=orjson.dumps(list_index[0]),
            )
            return r.json()

        list_chunked = chunk_list(ids, chunk_size)

        results: dict[int, list[dict]] = mlt.do_mlt_function(
            list_chunked,
            load_some_annotations,
            lambda item: item[1],
            max_workers=max_workers,
        )

        assets: dict[str, list] = {}
        for key, chunk_annotation in results.items():
            if chunk_annotation is None:
                if skip_error:
                    logging.error(
                        f"Something wrong happened while loading annotations with chunk {key}."
                    )
                    logging.error(
                        "This dataset may not be ready for loading annotations (check its type). Skipping chunk."
                    )
                    continue
                else:
                    raise exceptions.BadRequestError(
                        f"Something wrong happened while loading annotations with chunk {key}."
                        "This dataset may not be ready for loading annotations (check its type)."
                    )

            for annotation in chunk_annotation:
                asset_id = annotation.pop("asset_id")
                if asset_id not in assets:
                    assets[asset_id] = []
                assets[asset_id].append(annotation)

        return assets
