from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FileUpdateUploadStatus(Enums.KnownString):
    SUCCEEDED = "SUCCEEDED"
    FAILED_VALIDATION = "FAILED_VALIDATION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FileUpdateUploadStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of FileUpdateUploadStatus must be a string (encountered: {val})")
        newcls = Enum("FileUpdateUploadStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FileUpdateUploadStatus, getattr(newcls, "_UNKNOWN"))
