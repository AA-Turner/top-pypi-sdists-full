import logging
import os
from collections.abc import Callable

from picsellia.sdk.asset import Asset, MultiAsset
from picsellia.types.enums import AnnotationExportKey

logger = logging.getLogger("picsellia")


class ExportKeyService:
    @staticmethod
    def get_export_key(
        use_id: bool | None, export_key: AnnotationExportKey | str | None
    ) -> AnnotationExportKey:
        """This method is used for retro-compatibility of use_id and export_key"""
        if use_id:
            logger.warning("use_id is deprecated, use export_key='ASSET_ID' instead.")
            if export_key is None:
                export_key = AnnotationExportKey.ASSET_ID
            elif export_key == AnnotationExportKey.ASSET_ID:
                logger.warning(
                    "use_id is deprecated, you don't need to give it when export_key is defined"
                )
            else:
                logger.warning("use_id will not be used because export_key is given")

        if export_key is None:
            return AnnotationExportKey.FILENAME

        return AnnotationExportKey.validate(export_key)

    @staticmethod
    def fetch_assets_from_coco_filenames(
        fetcher: Callable,
        export_key: AnnotationExportKey,
        coco_filenames: list[str],
    ) -> MultiAsset:
        if export_key == AnnotationExportKey.ASSET_ID:
            # asset ids are in filename keys of coco file, as <id>.<extension>
            asset_ids = [filename.split(".")[0] for filename in coco_filenames]
            return fetcher(ids=asset_ids)
        elif export_key == AnnotationExportKey.DATA_ID:
            data_ids = [filename.split(".")[0] for filename in coco_filenames]
            return fetcher(data_ids=data_ids)
        elif export_key == AnnotationExportKey.FILENAME:
            return fetcher(filenames=coco_filenames)
        elif export_key == AnnotationExportKey.OBJECT_NAME:
            return fetcher(object_names=coco_filenames)
        else:  # pragma: no cover
            raise NotImplementedError()

    @staticmethod
    def get_coco_filename_from_asset(
        export_key: AnnotationExportKey, asset: Asset
    ) -> str:
        if export_key == AnnotationExportKey.FILENAME:
            return asset.filename
        elif export_key == AnnotationExportKey.OBJECT_NAME:
            return asset.object_name
        elif export_key == AnnotationExportKey.ASSET_ID:
            return asset.id_with_extension
        elif export_key == AnnotationExportKey.DATA_ID:
            extension = os.path.splitext(asset.filename)[1]
            return f"{asset.data_id}{extension}"
        else:  # pragma: no cover
            raise NotImplementedError()
