from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class FileUploadUiBlockType(Enums.KnownString):
    FILE_UPLOAD = "FILE_UPLOAD"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "FileUploadUiBlockType":
        if not isinstance(val, str):
            raise ValueError(f"Value of FileUploadUiBlockType must be a string (encountered: {val})")
        newcls = Enum("FileUploadUiBlockType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(FileUploadUiBlockType, getattr(newcls, "_UNKNOWN"))
