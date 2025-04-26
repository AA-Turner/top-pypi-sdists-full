from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BenchlingAppManifestFeatureCanvasLocations(Enums.KnownString):
    ENTRY = "ENTRY"
    ENTRY_TEMPLATE = "ENTRY_TEMPLATE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BenchlingAppManifestFeatureCanvasLocations":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BenchlingAppManifestFeatureCanvasLocations must be a string (encountered: {val})"
            )
        newcls = Enum("BenchlingAppManifestFeatureCanvasLocations", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BenchlingAppManifestFeatureCanvasLocations, getattr(newcls, "_UNKNOWN"))
