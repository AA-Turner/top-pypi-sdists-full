from enum import Enum


class VenueTypeEnum(str, Enum):
    BOOK = "book"
    CONFERENCE = "conference"
    JOURNAL = "journal"
    OTHER = "other"
    PREPRINT = "preprint"
    REPORT = "report"
    THESIS = "thesis"

    def __str__(self) -> str:
        return str(self.value)
