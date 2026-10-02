from enum import Enum


class RESTRICTEDOFFERINGVISIBILITYMODEEnum(str, Enum):
    HIDE_INACCESSIBLE = "hide_inaccessible"
    REQUIRE_MEMBERSHIP = "require_membership"
    SHOW_ALL = "show_all"
    SHOW_RESTRICTED_DISABLED = "show_restricted_disabled"

    def __str__(self) -> str:
        return str(self.value)
