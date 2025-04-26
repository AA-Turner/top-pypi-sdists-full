from datetime import datetime
from enum import Enum
from functools import cache
from typing import cast, List, Optional, Union

from benchling_api_client.v2.beta.extensions import Enums
from benchling_api_client.v2.beta.models.base_manifest_config import BaseManifestConfig
from benchling_api_client.v2.beta.models.dropdown_dependency import DropdownDependency
from benchling_api_client.v2.beta.models.dropdown_dependency_types import DropdownDependencyTypes
from benchling_api_client.v2.beta.models.entity_schema_dependency import EntitySchemaDependency
from benchling_api_client.v2.beta.models.entity_schema_dependency_type import EntitySchemaDependencyType
from benchling_api_client.v2.beta.models.field_definitions_manifest import FieldDefinitionsManifest
from benchling_api_client.v2.beta.models.manifest_array_config import ManifestArrayConfig
from benchling_api_client.v2.beta.models.manifest_float_scalar_config import ManifestFloatScalarConfig
from benchling_api_client.v2.beta.models.manifest_integer_scalar_config import ManifestIntegerScalarConfig
from benchling_api_client.v2.beta.models.manifest_scalar_config import ManifestScalarConfig
from benchling_api_client.v2.beta.models.manifest_text_scalar_config import ManifestTextScalarConfig
from benchling_api_client.v2.beta.models.resource_dependency import ResourceDependency
from benchling_api_client.v2.beta.models.resource_dependency_types import ResourceDependencyTypes
from benchling_api_client.v2.beta.models.schema_dependency import SchemaDependency
from benchling_api_client.v2.beta.models.schema_dependency_subtypes import SchemaDependencySubtypes
from benchling_api_client.v2.beta.models.schema_dependency_types import SchemaDependencyTypes
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency_output import (
    WorkflowTaskSchemaDependencyOutput,
)
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency_type import (
    WorkflowTaskSchemaDependencyType,
)
from benchling_api_client.v2.extensions import UnknownType
from benchling_api_client.v2.stable.extensions import NotPresentError

_ArrayElementDependency = Union[
    SchemaDependency,
    EntitySchemaDependency,
    WorkflowTaskSchemaDependency,
    DropdownDependency,
    ResourceDependency,
    ManifestScalarConfig,
]


class _UnsupportedSubTypeError(Exception):
    """Error when an unsupported subtype is encountered."""

    pass


class _ScalarConfigTypes(Enums.KnownString):
    """
    Enum type copied from an earlier version of benchling-api-client, for internal use only.

    See BNCH-108704.
    """

    TEXT = "text"
    FLOAT = "float"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    SECURE_TEXT = "secure_text"
    JSON = "json"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @cache
    def of_unknown(val: str) -> "_ScalarConfigTypes":
        if not isinstance(val, str):
            raise ValueError(f"Value of _ScalarConfigTypes must be a string (encountered: {val})")
        newcls = Enum("_ScalarConfigTypes", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(_ScalarConfigTypes, newcls._UNKNOWN)


def _field_definitions_from_dependency(
    dependency: Union[
        EntitySchemaDependency,
        SchemaDependency,
        WorkflowTaskSchemaDependency,
        WorkflowTaskSchemaDependencyOutput,
    ]
) -> List[FieldDefinitionsManifest]:
    """Safely return a list of field definitions from a schema dependency or empty list."""
    try:
        if hasattr(dependency, "field_definitions"):
            return dependency.field_definitions
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def _element_definition_from_dependency(dependency: ManifestArrayConfig) -> List[_ArrayElementDependency]:
    """Safely return an element definition as a list of dependencies from an array dependency or empty list."""
    try:
        if hasattr(dependency, "element_definition"):
            return [
                _fix_element_definition_deserialization(element) for element in dependency.element_definition
            ]
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def _enum_from_dependency(
    dependency: Union[
        ManifestFloatScalarConfig,
        ManifestIntegerScalarConfig,
        ManifestTextScalarConfig,
    ]
) -> List:
    """Safely return an enum from a scalar config."""
    try:
        if hasattr(dependency, "enum"):
            return dependency.enum
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


# TODO BNCH-57036 All element definitions currently deserialize to UnknownType. Hack around this temporarily
def _fix_element_definition_deserialization(  # noqa:PLR0911
    element: Union[UnknownType, _ArrayElementDependency]
) -> _ArrayElementDependency:
    if isinstance(element, UnknownType):
        if "type" in element.value:
            element_type = element.value["type"]
            if element_type == WorkflowTaskSchemaDependencyType.WORKFLOW_TASK_SCHEMA:
                return WorkflowTaskSchemaDependency.from_dict(element.value)
            elif element_type == EntitySchemaDependencyType.ENTITY_SCHEMA:
                return EntitySchemaDependency.from_dict(element.value)
            elif element_type in [member.value for member in SchemaDependencyTypes]:
                return SchemaDependency.from_dict(element.value)
            elif element_type == DropdownDependencyTypes.DROPDOWN:
                return DropdownDependency.from_dict(element.value)
            elif element_type in [member.value for member in ResourceDependencyTypes]:
                return ResourceDependency.from_dict(element.value)
            elif element_type in [member.value for member in _ScalarConfigTypes]:
                return type(element_type).from_dict(element.value)
        raise NotImplementedError(f"No array deserialization fix for {element}")
    return element


def _workflow_task_schema_output_from_dependency(
    dependency: WorkflowTaskSchemaDependency,
) -> Optional[WorkflowTaskSchemaDependencyOutput]:
    """Safely return a workflow task schema output from a workflow task schema or None."""
    try:
        if hasattr(dependency, "output"):
            return dependency.output
    # We can't seem to handle this programmatically by checking isinstance() or output truthiness
    except NotPresentError:
        pass
    return None


def _options_from_dependency(dependency: DropdownDependency) -> List[BaseManifestConfig]:
    """Safely return a list of options from a dropdown dependency or empty list."""
    try:
        if hasattr(dependency, "options"):
            return dependency.options
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return []


def _subtype_from_entity_schema_dependency(
    dependency: EntitySchemaDependency,
) -> Optional[SchemaDependencySubtypes]:
    """Safely return an entity schema dependency's subtype, if present."""
    try:
        if hasattr(dependency, "subtype") and dependency.subtype:
            return dependency.subtype
    # We can't seem to handle this programmatically by checking isinstance() or field truthiness
    except NotPresentError:
        pass
    return None


def datetime_config_value_to_str(value: datetime) -> str:
    """Convert a datetime value to a valid string accepted by a datetime app config item."""
    return value.strftime("%Y-%m-%d %I:%M:%S %p")
