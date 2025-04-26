from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AppConfigItemGenericUpdateType(Enums.KnownString):
    CONTAINER_SCHEMA = "container_schema"
    ENTITY_SCHEMA = "entity_schema"
    PLATE_SCHEMA = "plate_schema"
    LOCATION_SCHEMA = "location_schema"
    BOX_SCHEMA = "box_schema"
    RUN_SCHEMA = "run_schema"
    RESULT_SCHEMA = "result_schema"
    LEGACY_REQUEST_SCHEMA = "legacy_request_schema"
    ENTRY_SCHEMA = "entry_schema"
    WORKFLOW_TASK_SCHEMA = "workflow_task_schema"
    DROPDOWN = "dropdown"
    DROPDOWN_OPTION = "dropdown_option"
    FIELD = "field"
    TEXT = "text"
    DATE = "date"
    DATETIME = "datetime"
    SECURE_TEXT = "secure_text"
    JSON = "json"
    REGISTRY = "registry"
    FOLDER = "folder"
    ENTRY = "entry"
    WORKLIST = "worklist"
    PROJECT = "project"
    WORKFLOW_TASK_STATUS = "workflow_task_status"
    DNA_SEQUENCE = "dna_sequence"
    DNA_OLIGO = "dna_oligo"
    AA_SEQUENCE = "aa_sequence"
    CUSTOM_ENTITY = "custom_entity"
    MIXTURE = "mixture"
    MOLECULE = "molecule"
    RNA_OLIGO = "rna_oligo"
    RNA_SEQUENCE = "rna_sequence"
    BOX = "box"
    CONTAINER = "container"
    LOCATION = "location"
    PLATE = "plate"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AppConfigItemGenericUpdateType":
        if not isinstance(val, str):
            raise ValueError(f"Value of AppConfigItemGenericUpdateType must be a string (encountered: {val})")
        newcls = Enum("AppConfigItemGenericUpdateType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AppConfigItemGenericUpdateType, getattr(newcls, "_UNKNOWN"))
