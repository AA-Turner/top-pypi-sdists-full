from enum import Enum


class DesignObjectType(Enum):
    DATA_TYPE = "Data Type"
    DECISION = "Decision"
    EXPRESSION_RULE = "Expression Rule"
    INTEGRATION = "Integration"
    INTERFACE = "Interface"
    RECORD_TYPE = "Record Type"
    SITE = "Site"
    WEB_API = "Web API"
    TRANSLATION_SET = "Translation Set"


class DesignObject:
    """
    Class representing an Design Object
    """

    def __init__(self, name: str, opaque_id: str):
        self.name = name
        self.opaque_id = opaque_id

    def __str__(self) -> str:
        return f"DesignObject(name={self.name}, opaque_id={self.opaque_id})"

    def __repr__(self) -> str:
        return self.__str__()
