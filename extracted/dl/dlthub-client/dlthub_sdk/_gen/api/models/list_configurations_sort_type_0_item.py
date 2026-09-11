from enum import Enum


class ListConfigurationsSortType0Item(str, Enum):
    DATE_ADDED = "date_added"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
