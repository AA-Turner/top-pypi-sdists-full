#
# Copyright 2023-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot.enums import enum_to_list, PineconeCloud, VectorDatabaseMetadataCombinationStrategy
from datarobot.models.api_object import APIObject
from datarobot.models.custom_model_version import CustomModelVersion
from datarobot.models.deployment import Deployment
from datarobot.models.genai.custom_model_embedding_validation import CustomModelEmbeddingValidation
from datarobot.models.genai.custom_model_validation import (
    get_entity_id,
    NonChatAwareCustomModelValidation,
)
from datarobot.models.genai.playground import Playground
from datarobot.models.use_cases.use_case import UseCase
from datarobot.models.use_cases.utils import get_use_case_id, resolve_use_cases, UseCaseLike
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution

chunking_parameters_trafaret = t.Dict(
    {
        t.Key("embedding_model", optional=True, default=None): str,
        t.Key("embedding_validation_id", optional=True, default=None): str,
        t.Key("chunking_method", optional=True, default=None): t.Or(str, t.Null),
        t.Key("chunk_size", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("chunk_overlap_percentage", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("separators", optional=True, default=None): t.Or(t.List(t.String), t.Null),
        t.Key("custom_chunking", default=False): t.Bool,
    }
).ignore_extra("*")

embedding_model_trafaret = t.Dict(
    {
        t.Key("embedding_model"): str,
        t.Key("description"): str,
        t.Key("max_sequence_length"): int,
        t.Key("languages"): str,
    }
).ignore_extra("*")

supported_custom_model_embedding_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
    }
).ignore_extra("*")

supported_embeddings_trafaret = t.Dict(
    {
        t.Key("embedding_models"): t.List(embedding_model_trafaret),
        t.Key("default_embedding_model"): t.String,
        t.Key("custom_model_embedding_validations"): t.List(
            supported_custom_model_embedding_trafaret
        ),
    }
).ignore_extra("*")

text_chunking_parameter_fields_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("type"): t.String,
        t.Key("description"): t.String,
        t.Key("default"): t.Or(t.Int, t.List(t.String(allow_blank=True))),
        t.Key("min", optional=True): t.Or(t.Int, t.Null),
        t.Key("max", optional=True): t.Or(t.Int, t.Null),
    }
).ignore_extra("*")

text_chunking_method_trafaret = t.Dict(
    {
        t.Key("chunking_method"): t.Or(t.String, t.Null),
        t.Key("chunking_parameters"): t.List(text_chunking_parameter_fields_trafaret),
        t.Key("description"): t.String,
    }
).ignore_extra("*")

text_chunking_config_trafaret = t.Dict(
    {
        t.Key("embedding_model"): t.String,
        t.Key("methods"): t.List(text_chunking_method_trafaret),
        t.Key("default_method"): t.String,
    }
).ignore_extra("*")

supported_text_chunkings_trafaret = t.Dict(
    {
        t.Key("text_chunking_configs"): t.List(text_chunking_config_trafaret),
    }
).ignore_extra("*")

nested_supported_retrieval_setting_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("type"): t.Or(t.String, t.List(t.String)),
        t.Key("description"): t.String,
        t.Key("title"): t.String,
        t.Key("default", optional=True, default=None): t.Or(t.String, t.Int, t.Bool, t.Null),
        t.Key("minimum", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("maximum", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("enum", optional=True, default=None): t.Or(t.List(t.String), t.Null),
        t.Key("settings", optional=True, default=None): t.Null,
        t.Key("group_id", optional=True, default=None): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

supported_retrieval_setting_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("type"): t.Or(t.String, t.List(t.String)),
        t.Key("description"): t.String,
        t.Key("title"): t.String,
        t.Key("default", optional=True, default=None): t.Or(t.String, t.Int, t.Bool, t.Null),
        t.Key("minimum", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("maximum", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("enum", optional=True, default=None): t.Or(t.List(t.String), t.Null),
        t.Key("settings", optional=True, default=None): t.Or(
            t.List(nested_supported_retrieval_setting_trafaret), t.Null
        ),
        t.Key("group_id", optional=True, default=None): t.Or(t.String, t.Null),
    }
).ignore_extra("*")

supported_retrieval_settings_trafaret = t.Dict(
    {
        t.Key("settings"): t.List(supported_retrieval_setting_trafaret),
    }
).ignore_extra("*")


vector_database_dataset_export_job_trafaret = t.Dict(
    {
        t.Key("job_id"): t.String,
        t.Key("vector_database_id"): t.String,
        t.Key("export_dataset_id"): t.String,
    }
).ignore_extra("*")

PineconeConnection = t.Dict(
    {
        t.Key("type"): t.Atom("pinecone"),
        t.Key("cloud"): t.Enum(*enum_to_list(PineconeCloud)),
        t.Key("region"): t.String,
        t.Key("credential_id"): t.String,
    }
).allow_extra("*")

ElasticsearchConnection = t.Dict(
    {
        t.Key("type"): t.Atom("elasticsearch"),
        t.Key("url", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("cloud_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("credential_id"): t.String(),
    }
).allow_extra("*")

AnyExternalVectorDatabaseConnection = t.Dict({t.Key("type"): t.String}).allow_extra("*")

ExternalVectorDatabaseConnection = t.Or(
    PineconeConnection,
    ElasticsearchConnection,
    AnyExternalVectorDatabaseConnection,
)

vector_database_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("size"): t.Int,
        t.Key("use_case_id"): t.String,
        t.Key("dataset_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("embedding_model", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("chunking_method", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("chunk_size", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("chunk_overlap_percentage", optional=True, default=None): t.Or(t.Int, t.Null),
        t.Key("chunks_count"): t.Int,
        t.Key("custom_chunking", default=False): t.Bool,
        t.Key("separators", optional=True, default=None): t.Or(
            t.List(t.String(allow_blank=True)), t.Null
        ),
        t.Key("creation_date"): t.String,
        t.Key("creation_user_id"): t.String,
        t.Key("organization_id"): t.String,
        t.Key("tenant_id"): t.String,
        t.Key("last_update_date"): t.String,
        t.Key("execution_status"): t.String,
        t.Key("playgrounds_count"): t.Int,
        t.Key("dataset_name"): t.String(allow_blank=True),
        t.Key("user_name"): t.String(allow_blank=True),
        t.Key("source"): t.String,
        t.Key("validation_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("error_message", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("embedding_validation_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("is_separator_regex"): t.Bool,
        t.Key("parent_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("family_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("metadata_columns", optional=True, default=None): t.Or(t.Null, t.List(t.String)),
        t.Key("added_dataset_ids", optional=True, default=None): t.Or(t.Null, t.List(t.String)),
        t.Key("added_dataset_names", optional=True, default=None): t.Or(t.Null, t.List(t.String)),
        t.Key("version", optional=True, default=None): t.Or(t.Null, t.Int),
        t.Key("external_vector_database_connection", optional=True, default=None): t.Or(
            t.Null, ExternalVectorDatabaseConnection
        ),
        t.Key("metadata_dataset_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("metadata_dataset_name", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("metadata_combination_strategy", optional=True, default=None): t.Or(
            t.Null, t.Enum(*enum_to_list(VectorDatabaseMetadataCombinationStrategy))
        ),
        t.Key("added_metadata_dataset_pairs", optional=True, default=None): t.Or(
            t.Null,
            t.List(
                t.Dict(
                    {
                        t.Key("dataset_id"): t.String,
                        t.Key("dataset_name"): t.String,
                        t.Key("metadata_dataset_id"): t.String,
                        t.Key("metadata_dataset_name"): t.String,
                    }
                )
            ),
        ),
    }
).ignore_extra("*")


class ChunkingParameters(APIObject):
    """
    Parameters defining how documents are split and embedded.

    Attributes
    ----------
    embedding_model : Optional[str]
        Name of the text embedding model.
        Currently supported options are listed in VectorDatabaseEmbeddingModel
        but the values can differ with different platform versions.
    chunking_method : str
        Name of the method to split dataset documents.
        Currently supported options are listed in VectorDatabaseChunkingMethod
        but the values can differ with different platform versions.
    chunk_size : int
        Size of each text chunk in number of tokens.
    chunk_overlap_percentage : int
        Overlap percentage between chunks.
    separators : list[str]
        Strings used to split documents into text chunks.
    embedding_validation : Optional[CustomModelEmbeddingValidation, SupportedCustomModelEmbedding, str]
        ID or object for custom embedding validation.
    custom_chunking : bool
        Determines if the chunking is custom. With custom chunking,
        dataset rows are not split into chunks automatically;
        instead, the user provides the chunks.
    """

    _converter = chunking_parameters_trafaret

    def __init__(
        self,
        embedding_model: Optional[str],
        chunking_method: Union[str, None],
        chunk_size: Union[int, None],
        chunk_overlap_percentage: Union[int, None],
        separators: Union[List[str], None],
        custom_chunking: bool = False,
        embedding_validation: Optional[
            Union[CustomModelEmbeddingValidation, SupportedCustomModelEmbedding, str]
        ] = None,
    ):
        self.embedding_model = embedding_model
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.chunk_overlap_percentage = chunk_overlap_percentage
        self.separators = separators
        self.embedding_validation_id = self._get_embedding_validation_id(embedding_validation)
        self.custom_chunking = custom_chunking

    @staticmethod
    def _get_embedding_validation_id(
        embedding_validation: Optional[
            Union[CustomModelEmbeddingValidation, SupportedCustomModelEmbedding, str]
        ] = None,
    ) -> Union[str, None]:
        """Get ID of custom embedding validation from supported objects"""
        if isinstance(
            embedding_validation, (CustomModelEmbeddingValidation, SupportedCustomModelEmbedding)
        ):
            return embedding_validation.id
        return embedding_validation


class EmbeddingModel(APIObject):
    """
    A single model for embedding text.

    Attributes
    ----------
    embedding_model : str
        Name of the text embedding model.
        Currently supported options are listed in VectorDatabaseEmbeddingModel
        but the values can differ with different platform versions.
    description : str
        Description of the embedding model.
    max_sequence_length : int
        The model's maximum number of processable input tokens.
    languages : str
        Languages supported by the model.
        Currently supported options are listed in VectorDatabaseDatasetLanguages
        but the values can differ with different platform versions.
    """

    _converter = embedding_model_trafaret

    def __init__(
        self,
        embedding_model: str,
        description: str,
        max_sequence_length: int,
        languages: List[str],
    ):
        self.embedding_model = embedding_model
        self.description = description
        self.max_sequence_length = max_sequence_length
        self.languages = languages


class SupportedCustomModelEmbedding(APIObject):
    """
    All supported custom embedding models for the use case.

    Attributes
    ----------
    id : str
        ID of the custom model embedding validation.
    name : str
        The name of the custom model embedding validation.
    """

    _converter = supported_custom_model_embedding_trafaret

    def __init__(
        self,
        id: str,
        name: str,
    ):
        self.id = id
        self.name = name


class SupportedEmbeddings(APIObject):
    """
    All supported embedding models including the recommended default model.

    Attributes
    ----------
    embedding_models : list[EmbeddingModel]
        All supported embedding models.
    default_embedding_model : str
        Name of the default recommended text embedding model.
        Currently supported options are listed in VectorDatabaseEmbeddingModel
        but the values can differ with different platform versions.
    custom_model_embedding_validations : List[str]
        External embedding models that have been validated
    """

    _converter = supported_embeddings_trafaret

    def __init__(
        self,
        embedding_models: List[Dict[str, Any]],
        default_embedding_model: str,
        custom_model_embedding_validations: List[Dict[str, Any]],
    ):
        self.embedding_models = [
            EmbeddingModel.from_server_data(model) for model in embedding_models
        ]
        self.default_embedding_model = default_embedding_model
        self.custom_model_embedding_validations = [
            SupportedCustomModelEmbedding.from_server_data(validation)
            for validation in custom_model_embedding_validations
        ]


class TextChunkingParameterFields(APIObject):
    """
    Text chunking parameter fields.

    Attributes
    ----------
    name : str
        Parameter name.
    type : str
        Parameter type.
        Currently supported options are listed in VectorDatabaseChunkingParameterType
        but the values can differ with different platform versions.
    description : str
        Parameter description.
    default : int or list[str]
        Parameter default value.
    min : Optional[int]
        Parameter minimum value.
    max : Optional[int]
        Parameter maximum value.
    """

    _converter = text_chunking_parameter_fields_trafaret

    def __init__(
        self,
        name: str,
        type: str,
        description: str,
        default: Union[int, List[str]],
        min: Optional[int] = None,
        max: Optional[int] = None,
    ):
        self.name = name
        self.type = type
        self.description = description
        self.default = default
        self.min = min
        self.max = max


class TextChunkingMethod(APIObject):
    """
    A single text chunking method.

    Attributes
    ----------
    chunking_method : str
        Name of the method to split dataset documents.
        Currently supported options are listed in VectorDatabaseChunkingMethod
        but the values can differ with different platform versions.
    chunking_parameters : list[TextChunkingParameterFields]
        All chunking parameters including ranges and defaults.
    description : str
        Description of the chunking method.
    """

    _converter = text_chunking_method_trafaret

    def __init__(
        self,
        chunking_method: Union[str, None],
        chunking_parameters: List[Dict[str, Any]],
        description: str,
    ):
        self.chunking_method = chunking_method
        self.chunking_parameters = [
            TextChunkingParameterFields.from_server_data(parameter)
            for parameter in chunking_parameters
        ]
        self.description = description


class TextChunkingConfig(APIObject):
    """
    A single text chunking configurations.

    Attributes
    ----------
    embedding_model : str
        Name of the text embedding model.
        Currently supported options are listed in VectorDatabaseEmbeddingModel
        but the values can differ with different platform versions.
    methods : list[TextChunkingMethod]
        All text chunking methods and their supported parameters.
    default_method : str
        The default text chunking method name.
        Currently supported options are listed in VectorDatabaseChunkingMethod
        but the values can differ with different platform versions.
    """

    _converter = text_chunking_config_trafaret

    def __init__(
        self,
        embedding_model: str,
        methods: List[Dict[str, Any]],
        default_method: str,
    ):
        self.embedding_model = embedding_model
        self.methods = [TextChunkingMethod.from_server_data(method) for method in methods]
        self.default_method = default_method


class SupportedTextChunkings(APIObject):
    """
    Supported text chunking configurations which includes a set of
    recommended chunking parameters for each supported embedding model.

    Attributes
    ----------
    text_chunking_configs
        All supported text chunking configurations.
    """

    _converter = supported_text_chunkings_trafaret

    def __init__(self, text_chunking_configs: List[Dict[str, Any]]):
        self.text_chunking_configs = [
            TextChunkingConfig.from_server_data(config) for config in text_chunking_configs
        ]


class SupportedRetrievalSetting(APIObject):
    """
    A single supported retrieval setting.

    Attributes
    ----------
    name: str
        The name of the setting.
    type: str or list[str]
        The type of the setting.
    description: str
        The description of the setting.
    title: str
        The title of the setting.
    default: str, int, bool, or None
        The default value of the setting.
    minimum: int or None
        The minimum value of the setting.
    maximum: int or None
        The maximum value of the setting.
    enum: list[str] or None
        The enum values of the setting.
    settings: list[SupportedRetrievalSetting] or None
        The supported retriever settings.
    group_id: str or None
        The group ID of the setting.
    """

    _converter = supported_retrieval_setting_trafaret

    def __init__(
        self,
        name: str,
        type: Union[str, List[str]],
        description: str,
        title: str,
        default: Union[str, int, bool, None],
        minimum: Union[int, None],
        maximum: Union[int, None],
        enum: Union[List[str], None],
        settings: Union[List[Union[Dict[str, Any], List[Dict[str, Any]]]], None],
        group_id: Union[str, None],
    ):
        self.name = name
        self.type = type
        self.description = description
        self.title = title
        self.default = default
        self.minimum = minimum
        self.maximum = maximum
        self.enum = enum
        self.settings = (
            [SupportedRetrievalSetting.from_server_data(setting) for setting in settings]
            if settings
            else None
        )
        self.group_id = group_id


class SupportedRetrievalSettings(APIObject):
    """
    Supported retrieval settings.

    Attributes
    ----------
    settings : list[dict]
        The supported retriever settings.
    """

    _converter = supported_retrieval_settings_trafaret

    def __init__(
        self,
        settings: List[Union[Dict[str, Any], List[Dict[str, Any]]]],
    ):
        self.settings = [
            SupportedRetrievalSetting.from_server_data(setting) for setting in settings
        ]


class VectorDatabaseDatasetExportJob(APIObject):
    """
    Response for the vector database dataset export job.

    Attributes
    ----------
    job_id : str
        ID of the export job.
    vector_database_id : str
        ID of the vector database.
    export_dataset_id : str
        ID of the exported dataset.
    """

    _converter = vector_database_dataset_export_job_trafaret

    def __init__(
        self,
        job_id: str,
        vector_database_id: str,
        export_dataset_id: str,
    ):
        self.job_id = job_id
        self.vector_database_id = vector_database_id
        self.export_dataset_id = export_dataset_id


class VectorDatabase(APIObject):
    """
    Metadata for a DataRobot vector database accessible to the user.

    Attributes
    ----------
    id : str
        Vector database ID.
    name : str
        Vector database name.
    size : int
        Size of the vector database assets in bytes.
    use_case_id : str
        Linked use case ID.
    dataset_id : str
        ID of the dataset used for creation.
    embedding_model : str
        Name of the text embedding model.
        Currently supported options are listed in VectorDatabaseEmbeddingModel
        but the values can differ with different platform versions.
    chunking_method : str or None
        Name of the method to split dataset documents.
        Currently supported options are listed in VectorDatabaseChunkingMethod
        but the values can differ with different platform versions.
    chunk_size : int or None
        Size of each text chunk in number of tokens.
    chunk_overlap_percentage : int or None
        Overlap percentage between chunks.
    chunks_count : int
        Total number of text chunks.
    custom_chunking : bool
        Determines if the chunking is custom. With custom chunking,
        dataset rows are not split into chunks automatically;
        instead, the user provides the chunks.
    separators : list[string] or None
        Separators for document splitting.
    creation_date : str
        Date when the database was created.
    creation_user_id : str
        The ID of the creating user.
    organization_id : str
        The creating user's organization ID.
    tenant_id : str
        The creating user's tenant ID.
    last_update_date : str
        Last update date for the database.
    execution_status : str
        Database execution status.
        Currently supported options are listed in VectorDatabaseExecutionStatus
        but the values can differ with different platform versions.
    playgrounds_count : int
        Number of using playgrounds.
    dataset_name : str
        Name of the used dataset.
    user_name : str
        Name of the creating user.
    source : str
        Source of the vector database.
        Currently supported options are listed in VectorDatabaseSource
        but the values can differ with different platform versions.
    validation_id : Optional[str]
        ID of custom model vector database validation.
        Only filled for external vector databases.
    error_message : Optional[str]
        Additional information for errored vector database.
    embedding_validation_id : Optional[str]
        ID of the custom embedding validation, if any.
    is_separator_regex : bool
        Whether the separators should be treated as regular expressions.
    external_vector_database_connection : Optional[dict]
        Parameters defining the external vector database connection to use.
    metadata_dataset_id: Optional[str]
        The ID of the dataset used to add additional metadata to the vector database.
    metadata_dataset_name: Optional[str]
        The name of the dataset used to add additional metadata to the vector database.
    metadata_combination_strategy: Optional[VectorDatabaseMetadataCombinationStrategy]
        The strategy used to combine metadata when there is duplication between the dataset and
        the metadata dataset.
    added_metadata_dataset_pairs: Optional[List[Dict[str, str]]
        Pairs of dataset_id and metadata_dataset_id that have been added to the vector database.
    """

    _path = "api/v2/genai/vectorDatabases"

    _converter = vector_database_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        size: int,
        use_case_id: str,
        dataset_id: Optional[str],
        embedding_model: Optional[str],
        chunking_method: Union[Optional[str], None],
        chunk_size: Union[int, None],
        chunk_overlap_percentage: Union[int, None],
        chunks_count: int,
        custom_chunking: bool,
        separators: Union[List[str], None],
        creation_date: str,
        creation_user_id: str,
        organization_id: str,
        tenant_id: str,
        last_update_date: str,
        execution_status: str,
        playgrounds_count: int,
        dataset_name: str,
        user_name: str,
        source: str,
        validation_id: Optional[str],
        error_message: Optional[str],
        is_separator_regex: bool,
        embedding_validation_id: Optional[str],
        # VDB_PERFORMANCE fields
        parent_id: Optional[str],
        family_id: Optional[str],
        metadata_columns: Optional[List[str]],
        added_dataset_ids: Optional[List[str]],
        added_dataset_names: Optional[List[str]],
        version: int,
        external_vector_database_connection: Optional[Dict[str, Any]],
        metadata_dataset_id: Optional[str],
        metadata_dataset_name: Optional[str],
        metadata_combination_strategy: Optional[VectorDatabaseMetadataCombinationStrategy],
        added_metadata_dataset_pairs: Optional[List[Dict[str, str]]],
    ):
        self.id = id
        self.name = name
        self.size = size
        self.use_case_id = use_case_id
        self.dataset_id = dataset_id
        self.embedding_model = embedding_model
        self.chunking_method = chunking_method
        self.chunk_size = chunk_size
        self.chunk_overlap_percentage = chunk_overlap_percentage
        self.chunks_count = chunks_count
        self.separators = separators
        self.creation_date = creation_date
        self.creation_user_id = creation_user_id
        self.organization_id = organization_id
        self.tenant_id = tenant_id
        self.last_update_date = last_update_date
        self.execution_status = execution_status
        self.playgrounds_count = playgrounds_count
        self.dataset_name = dataset_name
        self.user_name = user_name
        self.source = source
        self.validation_id = validation_id
        self.error_message = error_message
        self.is_separator_regex = is_separator_regex
        self.embedding_validation_id = embedding_validation_id
        self.custom_chunking = custom_chunking
        self.parent_id = parent_id
        self.family_id = family_id
        self.metadata_columns = metadata_columns
        self.added_dataset_ids = added_dataset_ids
        self.added_dataset_names = added_dataset_names
        self.version = version
        self.external_vector_database_connection = external_vector_database_connection
        self.metadata_dataset_id = metadata_dataset_id
        self.metadata_dataset_name = metadata_dataset_name
        self.metadata_combination_strategy = metadata_combination_strategy
        self.added_metadata_dataset_pairs = added_metadata_dataset_pairs

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name}, "
            f"execution_status={self.execution_status})"
        )

    @classmethod
    def get_supported_embeddings(
        cls,
        dataset_id: Optional[str] = None,
        use_case: Optional[Union[UseCase, str]] = None,
    ) -> SupportedEmbeddings:
        """Get all supported and the recommended embedding models.

        Parameters
        ----------
        dataset_id : Optional[str]
            ID of a dataset for which the recommended model is returned
            based on the detected language of that dataset.
        use_case : Optional[UseCase, str]
            May be Use Case ID or the Use Case entity.

        Returns
        -------
        supported_embeddings : SupportedEmbeddings
            The supported embedding models.
        """
        params = {
            "dataset_id": dataset_id,
            "use_case_id": get_use_case_id(use_case, is_required=False),
        }
        url = f"{cls._client.domain}/{cls._path}/supportedEmbeddings/"
        r_data = cls._client.get(url, params=params)
        return SupportedEmbeddings.from_server_data(r_data.json())

    def submit_export_dataset_job(
        self,
    ) -> VectorDatabaseDatasetExportJob:
        """Submit the vector database dataset export job.

        Returns
        -------
        result : VectorDatabaseDatasetExportJob
            The result of the vector database dataset export job containing the exported dataset id.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/datasetExportJobs/"
        r_data = self._client.post(url)
        return VectorDatabaseDatasetExportJob.from_server_data(r_data.json())

    @classmethod
    def get_supported_retrieval_settings(cls) -> SupportedRetrievalSettings:
        """Get supported retrieval settings.

        Returns
        -------
        supported_retrieval_settings : SupportedRetrievalSettings
            The supported retriever settings.
        """
        url = f"{cls._client.domain}/{cls._path}/supportedRetrievalSettings/"
        r_data = cls._client.get(url)
        return SupportedRetrievalSettings.from_server_data(r_data.json())

    @classmethod
    def create(
        cls,
        dataset_id: str,
        chunking_parameters: Optional[ChunkingParameters] = None,
        use_case: Optional[Union[UseCase, str]] = None,
        name: Optional[str] = None,
        parent_vector_database_id: Optional[str] = None,
        update_llm_blueprints: Optional[bool] = None,
        update_deployments: Optional[bool] = None,
        external_vector_database_connection: Optional[Dict[str, Any]] = None,
        metadata_dataset_id: Optional[str] = None,
        metadata_combination_strategy: Optional[VectorDatabaseMetadataCombinationStrategy] = None,
    ) -> VectorDatabase:
        """
        Create a new vector database.

        Parameters
        ----------
        dataset_id : str
            ID of the dataset used for creation.
        chunking_parameters : ChunkingParameters
            Parameters defining how documents are split and embedded.
        use_case : Optional[Union[UseCase, str]], optional
            Use case to link to the created vector database.
        name : Optional[str]
            Vector database name, by default None
            which leads to the default name 'Vector Database for <dataset name>'.
        parent_vector_database_id : Optional[str]
            ID of the parent vector database to base the update on.
        update_llm_blueprints : Optional[bool]
            Whether to update LLM blueprints related to the parent vector database.
        update_deployments : Optional[bool]
            Whether to update deployments related to the parent vector database.
        external_vector_database_connection: Optional[dict]
            Parameters defining the external vector database connection to use.
        metadata_dataset_id : Optional[str]
            The ID of the dataset used to provide additional metadata.
        metadata_combination_strategy : Optional[VectorDatabaseMetadataCombinationStrategy]
            Strategy used to combine the metadata columns if there are duplicates between the
            dataset and the metadata dataset.

        Returns
        -------
        vector database : VectorDatabase
            The created vector database with execution status 'new'.
        """
        payload = {
            "name": name,
            "dataset_id": dataset_id,
            "use_case_id": get_use_case_id(use_case, is_required=True),
            "chunking_parameters": chunking_parameters,
            "parent_vector_database_id": parent_vector_database_id,
            "update_llm_blueprints": update_llm_blueprints,
            "update_deployments": update_deployments,
            "metadata_dataset_id": metadata_dataset_id,
            "metadata_combination_strategy": metadata_combination_strategy,
        }
        if external_vector_database_connection:
            payload["external_vector_database_connection"] = ExternalVectorDatabaseConnection(
                external_vector_database_connection
            )
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.post(url, data=payload)
        return cls.from_server_data(r_data.json())

    @classmethod
    def create_from_custom_model(
        cls,
        name: str,
        use_case: Optional[Union[UseCase, str]] = None,
        validation_id: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        deployment_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> VectorDatabase:
        """
        Create a new vector database from validated custom model deployment.

        Parameters
        ----------
        name : str
            Vector database name.
        use_case : Optional[Union[UseCase, str]], optional
            Use case to link to the created vector database.
        validation_id : Optional[str]
            ID of CustomModelVectorDatabaseValidation for the deployment.
            Alternatively, you can specify ALL the following fields.
        prompt_column_name : Optional[str]
            The column name the deployed model expect as the input.
        target_column_name : Optional[str]
            The target name deployed model will output.
        deployment_id : Optional[str]
            ID of the deployment.
        model_id : Optional[str]
            ID of the underlying deployment model.
            Can be found from the API as Deployment.model["id"].

        Returns
        -------
        vector database : VectorDatabase
            The created vector database.
        """
        payload: Dict[str, Any] = {
            "use_case_id": get_use_case_id(use_case, is_required=True),
            "name": name,
        }
        if validation_id:
            payload["validation_id"] = validation_id
        else:
            assert all([prompt_column_name, target_column_name, deployment_id, model_id]), (
                "Either validation_id or all of prompt_column_name, target_column_name, "
                "deployment_id, model_id fields should be specified"
            )
            payload.update(
                {
                    "prompt_column_name": prompt_column_name,
                    "target_column_name": target_column_name,
                    "deployment_id": deployment_id,
                    "model_id": model_id,
                }
            )
        url = f"{cls._client.domain}/{cls._path}/fromCustomModelDeployment/"
        r_data = cls._client.post(url, data=payload)
        return cls.from_server_data(r_data.json())

    @classmethod
    def get(cls, vector_database_id: str) -> VectorDatabase:
        """
        Retrieve a single vector database.

        Parameters
        ----------
        vector_database_id : str
            The ID of the vector database you want to retrieve.

        Returns
        -------
        vector database : VectorDatabase
            The requested vector database.
        """
        url = f"{cls._client.domain}/{cls._path}/{vector_database_id}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())

    @classmethod
    def list(
        cls,
        use_case: Optional[UseCaseLike] = None,
        playground: Optional[Union[Playground, str]] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        completed_only: Optional[bool] = None,
    ) -> List[VectorDatabase]:
        """
        List all vector databases associated with a specific use case available to the user.

        Parameters
        ----------
        use_case : Optional[UseCaseLike], optional
            The returned vector databases are filtered to those associated with a specific Use Case
            or Cases if specified or can be inferred from the Context.
            Accepts either the entity or the ID.
        playground : Optional[Union[Playground, str]], optional
            The returned vector databases are filtered to those associated with a specific playground
            if it is specified. Accepts either the entity or the ID.
        search : Optional[str]
            String for filtering vector databases.
            Vector databases that contain the string in name will be returned.
            If not specified, all vector databases will be returned.
        sort : Optional[str]
            Property to sort vector databases by.
            Prefix the attribute name with a dash to sort in descending order,
            e.g. sort='-creationDate'.
            Currently supported options are listed in ListVectorDatabasesSortQueryParams
            but the values can differ with different platform versions.
            By default, the sort parameter is None which will result in
            vector databases being returned in order of creation time descending.
        completed_only : Optional[bool]
            A filter to retrieve only vector databases that have been successfully created.
            By default, all vector databases regardless of execution status are retrieved.

        Returns
        -------
        vectorbases : list[VectorDatabase]
            A list of vector databases available to the user.
        """
        params = {
            "search": search,
            "sort": sort,
            "completed_only": completed_only,
            "playground_id": get_entity_id(playground) if playground else None,
        }

        params = resolve_use_cases(use_cases=use_case, params=params, use_case_key="use_case_id")

        url = f"{cls._client.domain}/{cls._path}/"
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def update(
        self, name: Optional[str] = None, credential_id: Optional[str] = None
    ) -> VectorDatabase:
        """
        Update the vector database.

        Parameters
        ----------
        name : Optional[str]
            The new name for the vector database.
        credential_id : Optional[str]
            The new credential id to access the connected vector database.

        Returns
        -------
        vector database : VectorDatabase
            The updated vector database.
        """
        payload = {"name": name, "credential_id": credential_id}
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        r_data = self._client.patch(url, data=payload)
        return self.from_server_data(r_data.json())

    def update_connected(
        self,
        dataset_id: str,
        metadata_dataset_id: Optional[str] = None,
        metadata_combination_strategy: Optional[str] = None,
    ) -> VectorDatabase:
        """
        Update a connected vector database.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset to add to the vector database.
        metadata_dataset_id : Optional[str]
            The ID of the dataset used to provide additional metadata.
        metadata_combination_strategy : Optional[VectorDatabaseMetadataCombinationStrategy]
            The strategy used to combine the metadata columns if there are duplicates between the
            dataset and the metadata dataset.

        Returns
        -------
        vector database : VectorDatabase
            The updated vector database.
        """
        payload = {
            "dataset_id": dataset_id,
            "metadata_dataset_id": metadata_dataset_id,
            "metadata_combination_strategy": metadata_combination_strategy,
        }
        url = f"{self._client.domain}/{self._path}/{self.id}/externalVectorDatabaseDocuments/"
        r_data = self._client.patch(url, data=payload)
        return self.from_server_data(r_data.json())

    def delete(self) -> None:
        """
        Delete the vector database.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)

    @classmethod
    def get_supported_text_chunkings(cls) -> SupportedTextChunkings:
        """Get all supported text chunking configurations which includes
        a set of recommended chunking parameters for each supported embedding model.

        Returns
        -------
        supported_text_chunkings : SupportedTextChunkings
            The supported text chunking configurations.
        """
        url = f"{cls._client.domain}/{cls._path}/supportedTextChunkings/"
        r_data = cls._client.get(url)
        return SupportedTextChunkings.from_server_data(r_data.json())

    def download_text_and_embeddings_asset(
        self, file_path: Optional[str] = None, part: Optional[int] = None
    ) -> None:
        """Download a parquet file with text chunks and corresponding embeddings created
        by a vector database.

        Parameters
        ----------
        file_path : Optional[str]
            File path to save the asset. By default, it saves in the current directory
            autogenerated by server name.
        part : Optional[int]
            Part of the text chunks to download. Connected vector databases have a
            part for each dataset that is added.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/textAndEmbeddings/"
        query_params = {}
        if part:
            query_params["part"] = part
        response = self._client.get(url, stream=True, params=query_params)
        if not file_path:
            file_path = response.headers["Content-Disposition"].split("=")[-1].strip('"')
        with open(str(file_path), mode="wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                f.write(chunk)

    def send_to_custom_model_workshop(
        self,
        maximum_memory: Optional[int] = None,
        resource_bundle_id: Optional[str] = None,
        replicas: Optional[int] = None,
        network_egress_policy: Optional[str] = None,
    ) -> CustomModelVersion:
        """
        Create a new CustomModelVersion for this vector database.

        Parameters
        ----------
        maximum_memory: Optional[int]
            The maximum memory that will be allocated to this custom model.
        resource_bundle_id: Optional[str]
            The ID of a datarobot.models.resource_bundle.ResourceBundle that will be used by this
            custom model.
        replicas: Optional[int]
            A fixed number of replicas that will be deployed for this custom model.
        network_egress_policy: Optional[str]
            Determines whether the given custom model is isolated, or can access the public network.
            Values: [`datarobot.NETWORK_EGRESS_POLICY.NONE`,
            `datarobot.NETWORK_EGRESS_POLICY.PUBLIC`].
        """

        requested_resources: dict[str, Any] = {}
        if maximum_memory is not None:
            requested_resources["maximum_memory"] = maximum_memory
        if resource_bundle_id is not None:
            requested_resources["resource_bundle_id"] = resource_bundle_id
        if replicas is not None:
            requested_resources["replicas"] = replicas
        if network_egress_policy is not None:
            requested_resources["network_egress_policy"] = network_egress_policy

        payload_data: dict[str, Any] = (
            {"resources": requested_resources} if requested_resources else {}
        )

        url = f"{self._client.domain}/{self._path}/{self.id}/customModelVersions/"

        response_data = self._client.post(url, data=payload_data)
        location = wait_for_async_resolution(self._client, response_data.headers["Location"])
        return CustomModelVersion.from_location(location)

    def deploy(
        self,
        default_prediction_server_id: Optional[str] = None,
        prediction_environment_id: Optional[str] = None,
        credential_id: Optional[str] = None,
        maximum_memory: Optional[int] = None,
        resource_bundle_id: Optional[str] = None,
        replicas: Optional[int] = None,
        network_egress_policy: Optional[str] = None,
    ) -> Deployment:
        """
        Create a new Custom Model for this vector database and deploy it on a new Deployment.

        Parameters
        ----------
        default_prediction_server_id: Optional[str]
            An identifier of a prediction server to be used as the default prediction server.
            When working with prediction environments, the default prediction server ID should not
            be provided.
        prediction_environment_id: Optional[str]
            An identifier of a prediction environment to be used for model deployment.
        credential_id: Optional[str]:
            The ID of credentials to access a connected vector database. This is only needed for vector
            databases with an external source when the user does not have access to the credentials
            associated with this vector database.
        maximum_memory: Optional[int]
            The maximum memory that will be allocated to the new custom model.
        resource_bundle_id: Optional[str]
            The ID of a datarobot.models.resource_bundle.ResourceBundle that will be used by the new
            custom model.
        replicas: Optional[int]
            A fixed number of replicas that will be deployed for this custom model.
        network_egress_policy: Optional[str]
            Determines whether the given custom model is isolated, or can access the public network.
            Values: [`datarobot.NETWORK_EGRESS_POLICY.NONE`,
            `datarobot.NETWORK_EGRESS_POLICY.PUBLIC`].
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/deployments/"

        requested_resources: dict[str, Any] = {}
        if maximum_memory is not None:
            requested_resources["maximum_memory"] = maximum_memory
        if resource_bundle_id is not None:
            requested_resources["resource_bundle_id"] = resource_bundle_id
        if replicas is not None:
            requested_resources["replicas"] = replicas
        if network_egress_policy is not None:
            requested_resources["network_egress_policy"] = network_egress_policy

        payload_data: dict[str, Any] = (
            {"resources": requested_resources} if requested_resources else {}
        )

        if default_prediction_server_id:
            payload_data["default_prediction_server_id"] = default_prediction_server_id
        if prediction_environment_id:
            payload_data["prediction_environment_id"] = prediction_environment_id
        if credential_id:
            payload_data["credential_id"] = credential_id

        response_data = self._client.post(url, data={})
        location = wait_for_async_resolution(self._client, response_data.headers["Location"])
        return Deployment.from_location(location)


class CustomModelVectorDatabaseValidation(NonChatAwareCustomModelValidation):
    """
    Validation record checking the ability of the deployment to serve as a vector database.

    Attributes
    ----------
    id : str
        The ID of the validation.
    prompt_column_name : str
        The column name the deployed model expect as the input.
    target_column_name : str
        The target name deployed model will output.
    deployment_id : str
        ID of the deployment.
    model_id : str
        ID of the underlying deployment model.
        Can be found from the API as Deployment.model["id"].
    validation_status : str
        Can be TESTING, FAILED and PASSED. Only PASSED allowed for use.
    deployment_access_data : dict, optional
        The data that will be used for accessing the deployment prediction server.
        This field is only available for deployments that pass validation.
        Dict fields are as follows:
        - prediction_api_url - The URL for the deployment prediction server.
        - datarobot_key - The first of two auth headers for the prediction server.
        - authorization_header - The second of two auth headers for the prediction server.
        - input_type - The input type the model expects, either JSON or CSV.
        - model_type - The target type of the deployed custom model.
    tenant_id : str
        The creating user's tenant ID.
    name : str
        The display name of the validated custom model.
    creation_date : str
        The creation date of the validation (ISO 8601 formatted).
    user_id : str
        The ID of the creating user.
    error_message : Optional[str]
        Additional information for the errored validation.
    deployment_name : Optional[str]
        The name of the validated deployment.
    user_name : Optional[str]
        The name of the creating user.
    use_case_id : Optional[str]
        The ID of the Use Case associated with the validation.
    """

    _path = "api/v2/genai/customModelVectorDatabaseValidations"
