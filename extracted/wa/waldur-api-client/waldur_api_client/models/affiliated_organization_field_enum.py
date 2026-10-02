from enum import Enum


class AffiliatedOrganizationFieldEnum(str, Enum):
    ABBREVIATION = "abbreviation"
    ADDRESS = "address"
    CODE = "code"
    COUNTRY = "country"
    CREATED = "created"
    DESCRIPTION = "description"
    EMAIL = "email"
    HOMEPAGE = "homepage"
    MODIFIED = "modified"
    NAME = "name"
    PROJECTS_COUNT = "projects_count"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
