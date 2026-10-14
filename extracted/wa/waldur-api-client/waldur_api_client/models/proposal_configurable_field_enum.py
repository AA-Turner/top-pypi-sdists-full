from enum import Enum


class ProposalConfigurableFieldEnum(str, Enum):
    DESCRIPTION = "description"
    PROJECT_SUMMARY = "project_summary"
    SCIENCE_SUB_DOMAIN = "science_sub_domain"
    SUPPORTING_DOCUMENTATION = "supporting_documentation"

    def __str__(self) -> str:
        return str(self.value)
