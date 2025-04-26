from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BenchlingAppManifestAlphaFeaturesItemType(Enums.KnownString):
    APP_HOMEPAGE = "APP_HOMEPAGE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BenchlingAppManifestAlphaFeaturesItemType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BenchlingAppManifestAlphaFeaturesItemType must be a string (encountered: {val})"
            )
        newcls = Enum("BenchlingAppManifestAlphaFeaturesItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BenchlingAppManifestAlphaFeaturesItemType, getattr(newcls, "_UNKNOWN"))
