from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class ListCollaborationsItemType(Enums.KnownString):
    CONNECTION = "connection"
    CONNECTION_SCHEMA = "connection_schema"
    ENTITY_SCHEMA = "entity_schema"
    ENZYME_LIST = "enzyme_list"
    FEATURE_LIBRARY = "feature_library"
    FOLDER = "folder"
    LEGACY_ASSEMBLY = "legacy_assembly"
    LEGACY_WORKFLOW_TEMPLATE = "legacy_workflow_template"
    PROJECT = "project"
    REGISTRY = "registry"
    RESULT_SCHEMA = "result_schema"
    RUN_SCHEMA = "run_schema"
    SAVED_SEARCH = "saved_search"
    SCHEMA_INTERFACE = "schema_interface"
    TEMPLATE_COLLECTION = "template_collection"
    WORKLIST = "worklist"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "ListCollaborationsItemType":
        if not isinstance(val, str):
            raise ValueError(f"Value of ListCollaborationsItemType must be a string (encountered: {val})")
        newcls = Enum("ListCollaborationsItemType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(ListCollaborationsItemType, getattr(newcls, "_UNKNOWN"))
