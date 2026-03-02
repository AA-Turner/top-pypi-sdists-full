from datetime import datetime

from ._entity import Entity
from .group import Group

class Table(Entity):
    """
    The table object represents a table within a structured relational database or
    datastore, which contains columns and rows of data that are able to be create,
    updated, deleted and queried.
    """

    # Optional:
    created_time: datetime | None = None # The time when the table was known to have been created.
    modified_time: datetime | None = None # The most recent time when any changes, updates, or
                                          # modifications were made within the table.
    desc: str | None = None # The description of the table.
    size: int | None = None # The size of the data table in bytes.
    groups: list[Group] | None = None # The group names to which the table belongs.
    name: str | None = None # The table name, ordinarily as assigned by a database administrator.
    uid: str | None = None # The unique identifier of the table.
