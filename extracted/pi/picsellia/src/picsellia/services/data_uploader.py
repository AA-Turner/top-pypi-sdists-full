import logging
import os
from pathlib import Path
from typing import Any
from uuid import UUID

from orjson import orjson
from PIL import Image

from picsellia.exceptions import UploadError
from picsellia.exif import read_image_metadata
from picsellia.sdk.connection import Connection
from picsellia.sdk.datasource import DataSource
from picsellia.services.error_manager import ErrorManager
from picsellia.types.enums import DataType, ObjectDataType
from picsellia.utils import filter_payload

ALLOWED_IMAGE_CONTENT_TYPES = (
    "image/jpeg",
    "image/bmp",
    "image/gif",
    "image/png",
    "image/tiff",
)

logger = logging.getLogger("picsellia")


class DataUploader:
    def __init__(
        self,
        connection: Connection,
        datalake_id: UUID,
        connector_id: UUID | None,
        computed_tag_ids: list[UUID],
        source: DataSource | None,
        fill_metadata: bool,
        upload_dir: str | None,
        error_manager: ErrorManager | None,
    ):
        self.connection = connection
        self.connector_id = connector_id
        self.datalake_id = datalake_id
        self.error_manager = error_manager
        self.fill_metadata = fill_metadata
        self.computed_tags_ids = computed_tag_ids
        self.source = source
        self.upload_dir = upload_dir

    def upload(self, items: tuple[str | Path, dict | None, dict | None]):
        path, metadatum, custom_metadatum = items
        try:
            filename = os.path.basename(path)
            object_name = self.connection.generate_data_object_name(
                filename, ObjectDataType.DATA, self.connector_id, self.upload_dir
            )
            _, _, content_type = self.connection.upload_file(
                object_name, path, connector_id=self.connector_id
            )
            payload = self._prepare_payload(
                filename, object_name, path, content_type, metadatum, custom_metadatum
            )
            return self.connection.post(
                f"/api/datalake/{self.datalake_id}/datas",
                data=orjson.dumps(payload),
            )
        except Exception as e:
            message = f"Could not upload path '{path}'"
            logger.error(message, exc_info=e)
            if self.error_manager:
                self.error_manager.append(
                    UploadError(message=message, path=path, parent=e)
                )
            return None

    def _prepare_payload(
        self,
        filename: str,
        object_name: str,
        path: str,
        content_type: str,
        metadatum: dict,
        custom_metadatum: dict | None,
    ):
        meta = None
        metadata = filter_payload(metadatum) if metadatum else None

        if content_type in ALLOWED_IMAGE_CONTENT_TYPES:
            data_type = DataType.IMAGE
            exif_data = self.prepare_metadata_from_image(
                path, metadatum, self.fill_metadata
            )
            if exif_data:
                meta = {"width": exif_data.width, "height": exif_data.height}
                metadata = exif_data.metadata
        elif content_type.startswith("video/"):
            data_type = DataType.VIDEO
        else:
            data_type = DataType.IMAGE
            logger.info(
                f"SDK cannot open {path} because its content type {content_type} is not openable here. "
                f"We will still upload your data and try handle it in our backend services."
            )

        payload: dict[str, Any] = {
            "type": data_type,
            "filename": filename,
            "object_name": object_name,
            "content_type": content_type,
            "tags": self.computed_tags_ids,
            "data_source_id": self.source.id if self.source else None,
        }
        if meta:
            payload["meta"] = meta
        if metadata:
            payload["metadata"] = metadata
        if custom_metadatum:
            payload["custom_metadata"] = custom_metadatum
        return payload

    @staticmethod
    def prepare_metadata_from_image(path: str, metadatum: dict, fill_metadata: bool):
        try:
            # Try opening with Pillow to read exif metadata, width and height
            with Image.open(path) as image:
                return read_image_metadata(image, metadatum, fill_metadata)
        except Exception:
            logger.error(
                f"{path} could not be opened with Pillow, Picsellia will try to compute size of this image later."
            )
            return None
