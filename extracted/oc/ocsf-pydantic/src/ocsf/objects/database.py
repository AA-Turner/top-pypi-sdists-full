from datetime import datetime
from enum import Enum

from .data_classification import DataClassification

from ._entity import Entity

from .group import Group


class DatabaseTypeId(Enum):
    """
    The normalized identifier of the database type.
    """
    Unknown: int = 0
    Relational: int = 1
    Network: int = 2
    Object_Oriented: int = 3
    Centralized: int = 4
    Operational: int = 5
    Nosql: int = 6
    Other: int = 99

class Database(Entity, DataClassification):
    """
    The database object is used for databases which are typically datastore services
    that contain an organized collection of structured and unstructured data or a
    types of data.
    """

    type_id: DatabaseTypeId # The normalized identifier of the database type.

    # Recommended:
    type: str | None = None # The database type.

    # Optional:
    created_time: datetime | None = None # The time when the database was known to have been created.
    modified_time: datetime | None = None # The most recent time when any changes, updates, or
                                          # modifications were made within the database.
    desc: str | None = None # The description of the database.
    size: int | None = None # The size of the database in bytes.
    groups: list[Group] | None = None # The group names to which the database belongs.
    name: str | None = None # The database name, ordinarily as assigned by a database administrator.
    uid: str | None = None # The unique identifier of the database.
