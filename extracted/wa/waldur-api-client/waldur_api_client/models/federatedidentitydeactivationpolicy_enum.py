from enum import Enum


class FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum(str, Enum):
    ALL_ISDS_REMOVED = "all_isds_removed"
    ANY_ISD_REMOVED = "any_isd_removed"

    def __str__(self) -> str:
        return str(self.value)
