from enum import Enum


class SoftwareVersionOEnum(str, Enum):
    CREATED = "created"
    PACKAGE_NAME = "package_name"
    RELEASE_DATE = "release_date"
    VALUE_0 = "-created"
    VALUE_1 = "-package_name"
    VALUE_2 = "-release_date"
    VALUE_3 = "-version"
    VERSION = "version"

    def __str__(self) -> str:
        return str(self.value)
