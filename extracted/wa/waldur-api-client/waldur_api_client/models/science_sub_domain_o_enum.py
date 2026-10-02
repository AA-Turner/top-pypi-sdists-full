from enum import Enum


class ScienceSubDomainOEnum(str, Enum):
    CODE = "code"
    DOMAIN_NAME = "domain_name"
    NAME = "name"
    PROJECTS_COUNT = "projects_count"
    VALUE_0 = "-code"
    VALUE_1 = "-domain_name"
    VALUE_2 = "-name"
    VALUE_3 = "-projects_count"

    def __str__(self) -> str:
        return str(self.value)
