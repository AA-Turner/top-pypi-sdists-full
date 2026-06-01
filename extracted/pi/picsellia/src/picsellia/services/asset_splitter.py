import logging
from uuid import UUID

from picsellia.sdk.asset import Asset
from picsellia.sdk.connection import Connection
from picsellia.services.splitter import Splitter

logger = logging.getLogger("picsellia")


class AssetSplitter(Splitter):
    @staticmethod
    def convert_items_to_assets(
        connection: Connection,
        dataset_version_id: UUID,
        items: list,
        label_names: dict[str, str],
    ) -> tuple[list[Asset], dict[str, int]]:
        assets = []
        label_repartition = {}
        for item in items:
            # TODO: Get asset from worker or status
            annotation = item["annotations"][0]
            asset = Asset(connection, dataset_version_id=dataset_version_id, data=item)

            assets.append(asset)

            # Retrieve all label_ids of this asset annotation
            label_ids = AssetSplitter._find_label_ids_from_annotation(annotation)

            # Add it to label ref count
            AssetSplitter._update_label_repartition(
                label_repartition, label_ids, label_names
            )
        return assets, label_repartition

    @staticmethod
    def _find_label_ids_from_annotation(annotation: dict):
        return [
            shape["label_id"]
            for shape_type in [
                "rectangles",
                "classifications",
                "points",
                "polygons",
                "lines",
                "keypoints",
            ]
            for shape in annotation[shape_type]
        ]

    @staticmethod
    def _update_label_repartition(
        label_repartition: dict[str, int],
        label_ids: list[str],
        label_names: dict[str, str],
    ):
        for label_id in label_ids:
            try:
                label_name = label_names[label_id]
                if label_name not in label_repartition:
                    label_repartition[label_name] = 1
                else:
                    label_repartition[label_name] += 1
            except KeyError:  # pragma: no cover
                logger.warning(f"A shape has an unknown label ({label_id}).")
