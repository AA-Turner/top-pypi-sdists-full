
from datetime import datetime
from enum import Enum

from .data_classification import DataClassification

from .group import Group
from ._entity import Entity
from .file import File


class DatabucketTypeId(Enum):
    """
    The normalized identifier of the databucket type.
    """
    Unknown: int = 0
    S3: int = 1
    Azure_Blob: int = 2
    GCP_Bucket: int = 3
    Other: int = 99

class Databucket(Entity, DataClassification):
    """
    The databucket object is a basic container that holds data, typically organized
    through the use of data partitions.
    """

    type_id: DatabucketTypeId # The normalized identifier of the databucket type.

    # Recommended:
    type: str | None = None # The databucket type.

    # Optional:
    created_time: datetime | None = None # The time when the databucket was known to have been created.
    modified_time: datetime | None = None # The most recent time when any changes, updates, or
                                          # modifications were made within the databucket.
    desc: str | None = None # The description of the databucket.
    size: int | None = None # The size of the databucket in bytes.
    file: File | None = None # A file within a databucket.
    groups: list[Group] | None = None # The group names to which the databucket belongs.
    name: str | None = None # The databucket name.
    uid: str | None = None # The unique identifier of the databucket.
