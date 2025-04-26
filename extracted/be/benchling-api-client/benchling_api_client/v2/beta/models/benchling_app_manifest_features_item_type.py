from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BenchlingAppManifestFeaturesItemType(Enums.KnownString):
    APP_HOMEPAGE = "APP_HOMEPAGE"
    ASSAY_RUN = "ASSAY_RUN"
    CANVAS = "CANVAS"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BenchlingAppManifestFeaturesItemType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BenchlingAppManifestFeaturesItemType must be a string (encountered: {val})"
            )
        newcls = Enum("BenchlingAppManifestFeaturesItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BenchlingAppManifestFeaturesItemType, getattr(newcls, "_UNKNOWN"))
