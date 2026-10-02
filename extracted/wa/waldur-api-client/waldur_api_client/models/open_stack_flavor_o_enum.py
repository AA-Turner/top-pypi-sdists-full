from enum import Enum


class OpenStackFlavorOEnum(str, Enum):
    CORES = "cores"
    DISK = "disk"
    RAM = "ram"
    VALUE_0 = "-cores"
    VALUE_1 = "-disk"
    VALUE_2 = "-ram"

    def __str__(self) -> str:
        return str(self.value)
