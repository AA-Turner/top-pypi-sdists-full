# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ApplicationNodeSchemaRegistryRecord",
    "NodeSchema",
    "NodeSchemaConfiguration",
    "NodeSchemaConfigurationNumberConfigurationFieldSchema",
    "NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules",
    "NodeSchemaConfigurationStringConfigurationFieldSchema",
    "NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules",
    "NodeSchemaConfigurationBoolConfigurationFieldSchema",
    "NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules",
    "NodeSchemaInputs",
    "NodeSchemaOutputs",
]


class NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules(BaseModel):
    max_value: int

    min_value: int

    required: bool


class NodeSchemaConfigurationNumberConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationNumberConfigurationFieldSchemaValidationRules

    default: Optional[float] = None

    is_advanced_configuration: Optional[bool] = None

    is_float: Optional[bool] = None

    type: Optional[Literal["NUMBER"]] = None


class NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules(BaseModel):
    required: bool

    regex_pattern: Optional[str] = None


class NodeSchemaConfigurationStringConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationStringConfigurationFieldSchemaValidationRules

    default: Optional[bool] = None

    is_advanced_configuration: Optional[bool] = None

    type: Optional[Literal["TEXT"]] = None


class NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules(BaseModel):
    required: bool


class NodeSchemaConfigurationBoolConfigurationFieldSchema(BaseModel):
    docs: str

    label: str

    validation_rules: NodeSchemaConfigurationBoolConfigurationFieldSchemaValidationRules

    default: Optional[bool] = None

    is_advanced_configuration: Optional[bool] = None

    type: Optional[Literal["BOOL"]] = None


NodeSchemaConfiguration: TypeAlias = Union[
    NodeSchemaConfigurationNumberConfigurationFieldSchema,
    NodeSchemaConfigurationStringConfigurationFieldSchema,
    NodeSchemaConfigurationBoolConfigurationFieldSchema,
]


class NodeSchemaInputs(BaseModel):
    docs: str

    label: str

    name: str

    required: bool

    type: Literal[
        "TEXT",
        "STRING_ARRAY",
        "NUMBER",
        "BOOL",
        "CHUNK_ARRAY",
        "DOCUMENT_ARRAY",
        "KNOWLEDGE_BASE_ID",
        "KNOWLEDGE_BASE_ID_ARRAY",
        "COMPLETION_MODEL_ID",
    ]
    """
    Represents the possible types of values for an application configuration, inputs
    and outputs.

    The available types are:

    - TEXT: Represents a single line of text.
    - STRING_ARRAY: Represents an array of strings.
    - NUMBER: Represents a numeric value.
    - BOOL: Represents a boolean value.
    - CHUNK_ARRAY: Represents an array of chunks.
    - DOCUMENT_ARRAY: Represents an array of documents.
    - KNOWLEDGE_BASE_ID: Represents the ID of a knowledge base.
    - KNOWLEDGE_BASE_ID_ARRAY: Represents an array of knowledge base IDs.
    - COMPLETION_MODEL_ID: Represents the ID of a completion model.
    """

    is_hidden: Optional[bool] = None


class NodeSchemaOutputs(BaseModel):
    docs: str

    label: str

    name: str

    type: Literal[
        "TEXT",
        "STRING_ARRAY",
        "NUMBER",
        "BOOL",
        "CHUNK_ARRAY",
        "DOCUMENT_ARRAY",
        "KNOWLEDGE_BASE_ID",
        "KNOWLEDGE_BASE_ID_ARRAY",
        "COMPLETION_MODEL_ID",
    ]
    """
    Represents the possible types of values for an application configuration, inputs
    and outputs.

    The available types are:

    - TEXT: Represents a single line of text.
    - STRING_ARRAY: Represents an array of strings.
    - NUMBER: Represents a numeric value.
    - BOOL: Represents a boolean value.
    - CHUNK_ARRAY: Represents an array of chunks.
    - DOCUMENT_ARRAY: Represents an array of documents.
    - KNOWLEDGE_BASE_ID: Represents the ID of a knowledge base.
    - KNOWLEDGE_BASE_ID_ARRAY: Represents an array of knowledge base IDs.
    - COMPLETION_MODEL_ID: Represents the ID of a completion model.
    """


class NodeSchema(BaseModel):
    configuration: Dict[str, NodeSchemaConfiguration]

    inputs: Dict[str, NodeSchemaInputs]

    outputs: Dict[str, NodeSchemaOutputs]


class ApplicationNodeSchemaRegistryRecord(BaseModel):
    id: str

    name: str

    node_schema: NodeSchema = FieldInfo(alias="nodeSchema")

    tags: List[Literal["INPUT_NODE", "OUTPUT_NODE", "RAG_NODE"]]

    type: Literal[
        "TEXT_INPUT_NODE",
        "TEXT_OUTPUT_NODE",
        "KNOWLEDGE_BASE_INPUT_NODE",
        "KNOWLEDGE_BASE_NODE",
        "MULTI_KNOWLEDGE_BASE_INPUT_NODE",
        "MULTI_KNOWLEDGE_BASE_NODE",
        "RERANKER_NODE",
        "PROMPT_ENGINEERING_NODE",
        "COMPLETION_MODEL_INPUT_NODE",
        "COMPLETION_MODEL_NODE",
        "EXTERNAL_ENDPOINT_NODE",
        "DOCUMENT_INPUT_NODE",
        "MAP_REDUCE_NODE",
        "DOCUMENT_SEARCH_NODE",
        "DOCUMENT_PROMPT_NODE",
    ]

    version: Literal["OFFLINE", "V0", "AGENTS_SERVICE"]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    AGENTS_SERVICE: Application schema references egp_services definition. OFFLINE:
    Application schema for applications that do not run on SGP directly.
    """
