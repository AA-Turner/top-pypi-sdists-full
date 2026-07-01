from enum import Enum

class EmailInbox_status(str, Enum):
    Active = "active",
    Deleted = "deleted",

