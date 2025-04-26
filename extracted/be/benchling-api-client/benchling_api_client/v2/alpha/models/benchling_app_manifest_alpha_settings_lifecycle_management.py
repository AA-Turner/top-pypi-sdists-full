from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BenchlingAppManifestAlphaSettingsLifecycleManagement(Enums.KnownString):
    AUTOMATIC = "automatic"
    MANUAL = "manual"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BenchlingAppManifestAlphaSettingsLifecycleManagement":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BenchlingAppManifestAlphaSettingsLifecycleManagement must be a string (encountered: {val})"
            )
        newcls = Enum("BenchlingAppManifestAlphaSettingsLifecycleManagement", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BenchlingAppManifestAlphaSettingsLifecycleManagement, getattr(newcls, "_UNKNOWN"))
