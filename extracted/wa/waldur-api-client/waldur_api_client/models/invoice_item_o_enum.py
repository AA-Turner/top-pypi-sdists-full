from enum import Enum


class InvoiceItemOEnum(str, Enum):
    NAME = "name"
    PROJECT_NAME = "project_name"
    PROVIDER_NAME = "provider_name"
    RESOURCE_NAME = "resource_name"
    VALUE_1 = "-project_name"
    VALUE_3 = "-resource_name"
    VALUE_5 = "-provider_name"
    VALUE_7 = "-name"

    def __str__(self) -> str:
        return str(self.value)
