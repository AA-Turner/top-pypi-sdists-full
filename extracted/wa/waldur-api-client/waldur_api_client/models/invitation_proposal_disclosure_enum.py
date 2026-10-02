from enum import Enum


class InvitationProposalDisclosureEnum(str, Enum):
    FULL_DETAILS = "full_details"
    TITLES_AND_SUMMARIES = "titles_and_summaries"
    TITLES_ONLY = "titles_only"

    def __str__(self) -> str:
        return str(self.value)
