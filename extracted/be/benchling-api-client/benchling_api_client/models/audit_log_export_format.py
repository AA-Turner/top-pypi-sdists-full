from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AuditLogExportFormat(Enums.KnownString):
    CSV = "CSV"
    PDF = "PDF"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AuditLogExportFormat":
        if not isinstance(val, str):
            raise ValueError(f"Value of AuditLogExportFormat must be a string (encountered: {val})")
        newcls = Enum("AuditLogExportFormat", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AuditLogExportFormat, getattr(newcls, "_UNKNOWN"))
