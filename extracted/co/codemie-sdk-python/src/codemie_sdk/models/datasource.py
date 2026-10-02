import re
from datetime import datetime
from enum import Enum
from typing import Tuple

from pydantic import BaseModel, Field, model_validator, ConfigDict, field_validator

from .common import TokensUsage, User


class CodeDataSourceType(str, Enum):
    CODE = "code"
    SUMMARY = "summary"
    CHUNK_SUMMARY = "chunk-summary"


class DataSourceType(str, Enum):
    CODE = "code"
    CONFLUENCE = "knowledge_base_confluence"
    JIRA = "knowledge_base_jira"
    FILE = "knowledge_base_file"
    XRAY = "knowledge_base_xray"
    GOOGLE = "llm_routing_google"
    GIT_FAQ = "knowledge_base_git_faq"
    PROVIDER = "provider"
    SUMMARY = "summary"
    CHUNK_SUMMARY = "chunk-summary"
    JSON = "knowledge_base_json"
    BEDROCK = "knowledge_base_bedrock"
    PLATFORM = "platform_marketplace_assistant"
    AZURE_DEVOPS_WIKI = "knowledge_base_azure_devops_wiki"
    AZURE_DEVOPS_WORK_ITEM = "knowledge_base_azure_devops_work_item"
    SHAREPOINT = "knowledge_base_sharepoint"
    XWIKI = "knowledge_base_xwiki"


class DataSourceStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    FETCHING = "fetching"
    IN_PROGRESS = "in_progress"


class DataSourceProcessingInfo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    total_documents_count: int | None = Field(None, alias="total_documents")
    skipped_documents_count: int | None = Field(None, alias="skipped_documents")
    total_size_kb: float | None = None
    average_file_size_bytes: float | None = None
    unique_extensions: list[str] | None = None
    filtered_documents: int | list | None = None
    processed_documents_count: int | None = Field(None, alias="documents_count_key")


class ElasticsearchStatsResponse(BaseModel):
    """Response model for Elasticsearch index statistics."""

    model_config = ConfigDict(extra="ignore")

    index_name: str = Field(..., description="Name of the index in Elasticsearch")
    size_in_bytes: int = Field(..., ge=0, description="Size of the index in bytes")


# Base request models
class Confluence(BaseModel):
    """Model for Confluence-specific response fields"""

    cql: str | None = None
    include_restricted_content: bool | None = None
    include_archived_content: bool | None = None
    include_attachments: bool | None = None
    include_comments: bool | None = None
    keep_markdown_format: bool | None = None
    keep_newlines: bool | None = None
    max_pages: int | None = None
    pages_per_request: int | None = None

    model_config = ConfigDict(extra="ignore")


class Jira(BaseModel):
    """Model for Jira-specific response fields"""

    jql: str | None = None
    custom_fields: list[str] | None = None

    model_config = ConfigDict(extra="ignore")


class Google(BaseModel):
    """Model for Google-specific response fields"""

    google_doc: str = Field(None, alias="googleDoc")

    model_config = ConfigDict(extra="ignore")


class File(BaseModel):
    """Model for File-specific response fields"""

    files: list[Tuple[str, bytes, str]] | None = None  # (filename, content, mime_type)

    model_config = ConfigDict(extra="ignore")


class AzureDevOpsWiki(BaseModel):
    """Model for Azure DevOps Wiki-specific response fields"""

    wiki_query: str | None = None
    organization: str | None = None
    project: str | None = None
    wiki_name: str | None = None

    model_config = ConfigDict(extra="ignore")


class AzureDevOpsWorkItem(BaseModel):
    """Model for Azure DevOps Work Item-specific response fields"""

    wiql_query: str | None = None
    organization: str | None = None
    project: str | None = None

    model_config = ConfigDict(extra="ignore")


class XWiki(BaseModel):
    """Model for xWiki-specific response fields"""

    space: str | None = None
    wiki: str | None = None

    model_config = ConfigDict(extra="ignore")


class Code(BaseModel):
    """Model for code repository datasource creation"""

    link: str | None = Field(..., min_length=1, max_length=1000)
    branch: str | None = Field(..., min_length=1, max_length=1000)
    index_type: CodeDataSourceType | None = Field(None, alias="indexType")
    files_filter: str | None = Field(default="", alias="filesFilter")
    embeddings_model: str | None = Field(None, alias="embeddingsModel")
    summarization_model: str | None = Field(None, alias="summarizationModel")
    prompt: str | None = None
    docs_generation: bool = Field(False, alias="docsGeneration")


class GitFaq(BaseModel):
    """Model for the Git FAQ (knowledge_base_git_faq) datasource creation"""

    link: str | None = Field(..., min_length=1, max_length=1000)
    branch: str | None = Field(..., min_length=1, max_length=1000)
    files_filter: str | None = Field(None)
    embedding_model: str | None = Field(None)


class BaseDataSourceRequest(BaseModel):
    """Base model for all datasource creation requests"""

    name: str = Field(
        ...,
        description="Name must contain only lowercase letters and underscores.",
        max_length=50,
    )
    project_name: str
    description: str = Field(..., max_length=100)
    shared_with_project: bool = Field(False, alias="project_space_visible")
    setting_id: str | None = Field(None)
    type: DataSourceType
    cron_expression: str | None = Field(None)
    timezone: str | None = Field(None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @classmethod
    def required_fields(cls) -> list[str]:
        return []

    @field_validator("name")
    def validate_name_field(cls, value):
        if not re.fullmatch(r"^[a-z][a-z_-]*$", value):
            raise ValueError(
                "Name must contain only lowercase letters and underscores, and cannot begin with '_' or '-'."
            )
        return value

    @model_validator(mode="before")
    def pre_init_validator(cls, values):
        # Ensure that at least one of the fields is not None
        if cls.required_fields() and not any(
            values.get(field) for field in cls.required_fields()
        ):
            raise ValueError(
                f"At least one of the following fields must be set: {', '.join(cls.required_fields())}"
            )
        return values


class CodeDataSourceRequest(BaseDataSourceRequest, Code):
    # Override to comply with keys in json
    project_space_visible: bool = Field(False, alias="projectSpaceVisible")
    setting_id: str | None = Field(None, alias="settingId")

    def __init__(self, **data):
        super().__init__(type=DataSourceType.CODE, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["link", "embeddings_model", "branch", "index_type"]


class GitFaqDataSourceRequest(BaseDataSourceRequest, GitFaq):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.GIT_FAQ, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["link", "branch"]


class JiraDataSourceRequest(BaseDataSourceRequest, Jira):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.JIRA, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["jql"]


class ConfluenceDataSourceRequest(BaseDataSourceRequest, Confluence):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.CONFLUENCE, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["cql"]


class GoogleDataSourceRequest(BaseDataSourceRequest, Google):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.GOOGLE, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["google_doc"]


class FileDataSourceRequest(BaseDataSourceRequest):
    """Model for File datasource creation requests"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.FILE, **data)


class AzureDevOpsWikiDataSourceRequest(BaseDataSourceRequest, AzureDevOpsWiki):
    """Model for Azure DevOps Wiki datasource creation requests"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.AZURE_DEVOPS_WIKI, **data)


class AzureDevOpsWorkItemDataSourceRequest(BaseDataSourceRequest, AzureDevOpsWorkItem):
    """Model for Azure DevOps Work Item datasource creation requests"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.AZURE_DEVOPS_WORK_ITEM, **data)


class XWikiDataSourceRequest(BaseDataSourceRequest, XWiki):
    """Model for xWiki datasource creation requests"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.XWIKI, **data)

    @classmethod
    def required_fields(cls) -> list[str]:
        return ["space"]


class BaseUpdateDataSourceRequest(BaseDataSourceRequest):
    """Mixin update-specific reindex fields"""

    full_reindex: bool | None = Field(None)
    skip_reindex: bool | None = Field(None)
    resume_indexing: bool | None = Field(None)
    incremental_reindex: bool | None = Field(None)

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @model_validator(mode="after")
    def validate_reindex_options(self) -> "BaseUpdateDataSourceRequest":
        ds_type = self.type

        if ds_type == DataSourceType.CONFLUENCE:
            if self.incremental_reindex:
                raise ValueError(
                    "Confluence data sources only support full_reindex and resume_indexing"
                )

        elif ds_type == DataSourceType.JIRA:
            if self.resume_indexing:
                raise ValueError(
                    "Jira data sources only support full_reindex and incremental_reindex"
                )

        elif ds_type == DataSourceType.CODE:
            if self.incremental_reindex:
                raise ValueError("Code data sources do not support incremental_reindex")

        elif ds_type == DataSourceType.GOOGLE:
            if self.resume_indexing or self.incremental_reindex:
                raise ValueError("Google data sources only support full_reindex")

        return self


class UpdateGitFaqDataSourceRequest(BaseUpdateDataSourceRequest):
    """Model for Git FAQ datasource updates; source fields require full_reindex=True"""

    link: str | None = Field(None)
    branch: str | None = Field(None)
    files_filter: str | None = Field(None)
    setting_id: str | None = Field(None)

    def __init__(self, **data):
        super().__init__(type=DataSourceType.GIT_FAQ, **data)


class UpdateCodeDataSourceRequest(BaseUpdateDataSourceRequest, Code):
    """Model for code repository datasource updates"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.CODE, **data)


class UpdateConfluenceDataSourceRequest(BaseUpdateDataSourceRequest, Confluence):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.CONFLUENCE, **data)


class UpdateJiraDataSourceRequest(BaseUpdateDataSourceRequest, Jira):
    def __init__(self, **data):
        super().__init__(type=DataSourceType.JIRA, **data)


class UpdateGoogleDataSourceRequest(BaseUpdateDataSourceRequest):
    """Model for Google docs datasource updates"""

    google_doc: str | None = Field(None, alias="googleDoc")

    def __init__(self, **data):
        super().__init__(type=DataSourceType.GOOGLE, **data)


class UpdateFileDataSourceRequest(BaseUpdateDataSourceRequest):
    """Model for File datasource updates"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.FILE, **data)


class UpdateAzureDevOpsWikiDataSourceRequest(
    BaseUpdateDataSourceRequest, AzureDevOpsWiki
):
    """Model for Azure DevOps Wiki datasource updates"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.AZURE_DEVOPS_WIKI, **data)


class UpdateAzureDevOpsWorkItemDataSourceRequest(
    BaseUpdateDataSourceRequest, AzureDevOpsWorkItem
):
    """Model for Azure DevOps Work Item datasource updates"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.AZURE_DEVOPS_WORK_ITEM, **data)


class UpdateXWikiDataSourceRequest(BaseUpdateDataSourceRequest, XWiki):
    """Model for xWiki datasource updates"""

    def __init__(self, **data):
        super().__init__(type=DataSourceType.XWIKI, **data)


class CodeAnalysisDataSourceRequest(BaseModel):
    """Model for provider-based datasource creation requests"""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = Field(..., description="Datasource name")
    description: str | None = Field(None, description="Datasource description")
    project_name: str = Field(..., description="Project name")
    project_space_visible: bool = Field(False, alias="projectSpaceVisible")
    branch: str | None = Field(None, description="Git branch")
    api_url: str = Field(..., description="Repository URL")
    access_token: str = Field(..., description="Access token for repository")
    analyzer: str | None = Field(
        None, description="Code analyzer type (e.g., Java, Python)"
    )
    datasource_root: str = Field("/", description="Root directory to analyze")


class CodeExplorationDataSourceRequest(BaseModel):
    """Model for CodeExplorationToolkit datasource creation requests"""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = Field(..., description="Datasource name")
    description: str | None = Field(None, description="Datasource description")
    project_name: str = Field(..., description="Project name")
    project_space_visible: bool = Field(False, alias="projectSpaceVisible")
    code_analysis_datasource_ids: list[str] = Field(
        ...,
        alias="code_analysis_datasource_ids",
        description="List of CodeAnalysisToolkit datasource IDs",
    )


class DataSource(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    def __getitem__(self, key):
        return getattr(self, key)

    id: str
    project_name: str
    name: str = Field(None, alias="repo_name")
    description: str | None = Field(None)
    type: DataSourceType = Field(None, alias="index_type")
    embeddings_model: str | None = Field(None)
    status: DataSourceStatus
    setting_id: str | None = Field(None)
    created_date: datetime = Field(None, alias="date")
    created_by: User
    shared_with_project: bool = Field(None, alias="project_space_visible")
    update_date: datetime
    error_message: str | None = Field(None, alias="text")
    user_abilities: list[str]
    processing_info: DataSourceProcessingInfo | None = Field(None)
    processed_documents: list[str] | None = Field(None, alias="processed_files")
    tokens_usage: TokensUsage | None = Field(None)
    # Code specific fields
    code: Code | None = None
    git_faq: GitFaq | None = None
    # Jira specific fields
    jira: Jira | None = None
    # Confluence specific fields
    confluence: Confluence | None = None
    # Google doc specific fields
    google_doc_link: str | None = None
    # Azure DevOps Wiki specific fields
    azure_devops_wiki: AzureDevOpsWiki | None = None
    # Azure DevOps Work Item specific fields
    azure_devops_work_item: AzureDevOpsWorkItem | None = None
    # xWiki specific fields
    xwiki: XWiki | None = None

    @model_validator(mode="before")
    def before_init(cls, values):
        if values.get("error"):
            values["status"] = DataSourceStatus.FAILED
        elif values.get("completed"):
            values["status"] = DataSourceStatus.COMPLETED
        elif values.get("is_fetching"):
            values["status"] = DataSourceStatus.FETCHING
        else:
            values["status"] = DataSourceStatus.IN_PROGRESS

        if values.get("index_type") in [
            DataSourceType.CONFLUENCE,
            DataSourceType.JIRA,
            DataSourceType.GOOGLE,
            DataSourceType.AZURE_DEVOPS_WIKI,
            DataSourceType.AZURE_DEVOPS_WORK_ITEM,
            DataSourceType.XWIKI,
        ]:
            complete_state = values.get("complete_state", 0)
            if complete_state is not None:
                values["processing_info"] = {"documents_count_key": complete_state}
        elif values.get("index_type") == DataSourceType.GIT_FAQ:
            values["git_faq"] = {
                "link": values.get("link"),
                "branch": values.get("branch"),
                "files_filter": values.get("files_filter"),
                "setting_id": values.get("setting_id"),
            }
        elif values.get("index_type") == DataSourceType.CODE:
            values["code"] = {
                "link": values.get("link"),
                "branch": values.get("branch"),
                "files_filter": values.get("files_filter"),
                "summarization_prompt": values.get("prompt"),
                "summarization_model": values.get("summarization_model"),
                "summarization_docs_generation": values.get("docs_generation"),
                "embeddings_model": values.get("embeddings_model"),
            }
        return values
