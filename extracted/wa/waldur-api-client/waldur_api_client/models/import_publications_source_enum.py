from enum import Enum


class ImportPublicationsSourceEnum(str, Enum):
    DOI = "doi"
    ORCID = "orcid"

    def __str__(self) -> str:
        return str(self.value)
