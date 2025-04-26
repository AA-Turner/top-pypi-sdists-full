from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FileStatusUploadStatus(Enums.KnownString):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED_VALIDATION = "FAILED_VALIDATION"
    NOT_UPLOADED = "NOT_UPLOADED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FileStatusUploadStatus":
        if not isinstance(val, str):
            raise ValueError(f"Value of FileStatusUploadStatus must be a string (encountered: {val})")
        newcls = Enum("FileStatusUploadStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FileStatusUploadStatus, getattr(newcls, "_UNKNOWN"))
