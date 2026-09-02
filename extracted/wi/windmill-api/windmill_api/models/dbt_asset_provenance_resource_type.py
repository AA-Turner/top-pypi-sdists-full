from enum import Enum


class DbtAssetProvenanceResourceType(str, Enum):
    MODEL = "model"
    SEED = "seed"
    SNAPSHOT = "snapshot"
    SOURCE = "source"

    def __str__(self) -> str:
        return str(self.value)
