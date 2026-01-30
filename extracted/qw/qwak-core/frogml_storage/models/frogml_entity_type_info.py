from enum import Enum

from typing_extensions import Self

from frogml_storage.constants import (
    BODY_PART_DATASET_MANIFEST_STREAM,
    BODY_PART_MODEL_MANIFEST_STREAM,
    DATASET_METADATA_FILE_NAME,
    DATASET_UI_DIRECTORY,
    MODEL_METADATA_FILE_NAME,
    MODEL_UI_DIRECTORY,
    ROOT_FROGML_DATASET_UI_DIRECTORY,
    ROOT_FROGML_MODEL_UI_DIRECTORY,
)


# noinspection PyEnum
class FrogMLEntityTypeInfo(Enum):
    MODEL = (
        MODEL_UI_DIRECTORY,
        ROOT_FROGML_MODEL_UI_DIRECTORY,
        MODEL_METADATA_FILE_NAME,
        BODY_PART_MODEL_MANIFEST_STREAM,
    )
    DATASET = (
        DATASET_UI_DIRECTORY,
        ROOT_FROGML_DATASET_UI_DIRECTORY,
        DATASET_METADATA_FILE_NAME,
        BODY_PART_DATASET_MANIFEST_STREAM,
    )

    def __init__(
        self: Self,
        entity_type: str,
        folder_name: str,
        metadata_file_name: str,
        body_part_stream: str,
    ):
        self.entity_type: str = entity_type
        self.folder_name: str = folder_name
        self.metadata_file_name: str = metadata_file_name
        self.body_part_stream: str = body_part_stream

    @classmethod
    def from_string(cls, entity_type_string: str) -> "FrogMLEntityTypeInfo":
        for entity_type in cls:
            if entity_type.entity_type.lower() == entity_type_string.lower():
                return entity_type

        raise ValueError(f"No enum constant found for entityType: {entity_type_string}")
