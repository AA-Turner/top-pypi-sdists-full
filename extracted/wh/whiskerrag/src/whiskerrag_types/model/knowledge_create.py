from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_serializer, model_validator

from whiskerrag_types.model.knowledge import (
    EmbeddingModelEnum,
    Knowledge,
    KnowledgeTypeEnum,
)
from whiskerrag_types.model.knowledge_source import (
    GithubRepoSourceConfig,
    KnowledgeSourceEnum,
    OpenIdSourceConfig,
    OpenUrlSourceConfig,
    S3SourceConfig,
    TextSourceConfig,
    YuqueSourceConfig,
)
from whiskerrag_types.model.splitter import (
    GeaGraphSplitConfig,
    GithubRepoParseConfig,
    ImageSplitConfig,
    JSONSplitConfig,
    MarkdownSplitConfig,
    PDFSplitConfig,
    TextSplitConfig,
    YuqueSplitConfig,
)
from whiskerrag_types.model.tenant import Tenant
from whiskerrag_types.model.utils import MetadataSerializer


class KnowledgeCreateBase(BaseModel):
    space_id: str = Field(
        ...,
        description="the space of knowledge, example: petercat bot id, github repo name",
    )
    knowledge_type: KnowledgeTypeEnum = Field(
        KnowledgeTypeEnum.TEXT, description="type of knowledge resource"
    )
    knowledge_name: str = Field(
        ..., max_length=255, description="name of the knowledge resource"
    )
    metadata: dict = Field({}, description="additional metadata, user can update it")
    source_type: KnowledgeSourceEnum = Field(..., description="source type")
    embedding_model_name: Union[EmbeddingModelEnum, str] = Field(
        EmbeddingModelEnum.OPENAI,
        description="name of the embedding model. you can set any other model if target embedding service registered",
    )
    file_sha: Optional[str] = Field(None, description="SHA of the file")
    file_size: Optional[int] = Field(None, description="size of the file")

    @field_serializer("metadata")
    def serialize_metadata(self, metadata: dict) -> Optional[dict]:
        if metadata is None:
            return None
        sorted_metadata = MetadataSerializer.deep_sort_dict(metadata)
        return sorted_metadata if isinstance(sorted_metadata, dict) else None

    @field_serializer("knowledge_type")
    def serialize_knowledge_type(
        self, knowledge_type: Union[KnowledgeTypeEnum, str]
    ) -> str:
        if isinstance(knowledge_type, KnowledgeTypeEnum):
            return knowledge_type.value
        return str(knowledge_type)

    @field_serializer("source_type")
    def serialize_source_type(
        self, source_type: Union[KnowledgeSourceEnum, str]
    ) -> str:
        if isinstance(source_type, KnowledgeSourceEnum):
            return source_type.value
        return str(source_type)

    @field_serializer("embedding_model_name")
    def serialize_embedding_model_name(
        self, embedding_model_name: Union[EmbeddingModelEnum, str]
    ) -> str:
        if isinstance(embedding_model_name, EmbeddingModelEnum):
            return embedding_model_name.value
        return str(embedding_model_name)


class TextCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.TEXT] = Field(
        KnowledgeTypeEnum.TEXT, description="type of knowledge resource"
    )
    source_config: Union[
        TextSourceConfig, OpenUrlSourceConfig, OpenIdSourceConfig, S3SourceConfig
    ] = Field(
        ...,
        description="source config of the knowledge",
    )
    split_config: TextSplitConfig = Field(
        ...,
        description="split config of the knowledge",
    )


class JSONCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.JSON] = Field(
        KnowledgeTypeEnum.JSON, description="type of knowledge resource"
    )
    source_config: Union[
        TextSourceConfig, OpenUrlSourceConfig, OpenIdSourceConfig, S3SourceConfig
    ] = Field(
        ...,
        description="source config of the knowledge",
    )
    split_config: JSONSplitConfig = Field(
        ...,
        description="split config of the knowledge",
    )


class MarkdownCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.MARKDOWN] = Field(
        KnowledgeTypeEnum.MARKDOWN, description="type of knowledge resource"
    )
    source_config: Union[
        TextSourceConfig, OpenUrlSourceConfig, OpenIdSourceConfig, S3SourceConfig
    ] = Field(
        ...,
        description="source config of the knowledge",
    )
    split_config: MarkdownSplitConfig = Field(
        ...,
        description="split config of the knowledge",
    )


class PDFCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.PDF] = Field(
        KnowledgeTypeEnum.PDF, description="type of knowledge resource"
    )
    source_config: Union[OpenUrlSourceConfig, OpenIdSourceConfig, S3SourceConfig] = (
        Field(
            ...,
            description="source config of the knowledge",
        )
    )
    split_config: PDFSplitConfig = Field(
        ...,
        description="split config of the knowledge",
    )
    file_sha: str = Field(..., description="SHA of the file")
    file_size: int = Field(..., description="Byte size of the file")


class GithubRepoCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.GITHUB_REPO] = Field(
        KnowledgeTypeEnum.GITHUB_REPO, description="type of knowledge resource"
    )
    source_config: GithubRepoSourceConfig = Field(
        ...,
        description="source config of the knowledge",
    )
    split_config: GithubRepoParseConfig = Field(
        ...,
        description="split config of the knowledge",
    )


class QACreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.QA] = Field(
        KnowledgeTypeEnum.QA, description="type of knowledge resource"
    )
    question: str = Field(..., description="question of the knowledge resource")
    answer: str = Field(..., description="answer of the knowledge resource")
    split_config: TextSplitConfig = Field(
        ...,
        description="split config of the knowledge, used to split the question into chunks",
    )
    source_type: Literal[KnowledgeSourceEnum.USER_INPUT_TEXT] = Field(
        KnowledgeSourceEnum.USER_INPUT_TEXT, description="source type"
    )
    source_config: Optional[TextSourceConfig] = Field(
        default=None,
        description="source config of the knowledge",
    )

    @model_validator(mode="after")
    def update_source_and_metadata(self) -> "QACreate":
        self.source_config = self.source_config or TextSourceConfig()
        self.source_config.text = self.question

        self.metadata = self.metadata or {}
        self.metadata["answer"] = self.answer

        return self


class ImageCreate(KnowledgeCreateBase):
    knowledge_type: Literal[KnowledgeTypeEnum.IMAGE] = Field(
        KnowledgeTypeEnum.IMAGE, description="type of knowledge resource"
    )
    source_type: Literal[KnowledgeSourceEnum.CLOUD_STORAGE_IMAGE] = Field(
        KnowledgeSourceEnum.CLOUD_STORAGE_IMAGE, description="source type"
    )
    source_config: Union[OpenUrlSourceConfig, OpenIdSourceConfig, S3SourceConfig] = (
        Field(
            ...,
            description="source config of the knowledge",
        )
    )
    split_config: Union[ImageSplitConfig]
    file_sha: str = Field(..., description="SHA of the file")
    file_size: int = Field(..., description="Byte size of the file")


class YuqueCreate(KnowledgeCreateBase):
    knowledge_type: Literal[
        KnowledgeTypeEnum.YUQUEDOC, KnowledgeTypeEnum.GITHUB_REPO
    ] = Field(
        default=KnowledgeTypeEnum.YUQUEDOC, description="type of knowledge resource"
    )
    source_type: Literal[KnowledgeSourceEnum.YUQUE] = Field(
        KnowledgeSourceEnum.YUQUE, description="source type"
    )
    source_config: YuqueSourceConfig = Field(
        ...,
        description="source config of the knowledge",
    )
    split_config: Union[GeaGraphSplitConfig, YuqueSplitConfig] = Field(
        ...,
        description="split config of the knowledge",
    )


# TODO: add more knowledge types
# EXCEL = "excel"
# PPTX = "pptx"
KnowledgeCreateUnion = Union[
    TextCreate,
    ImageCreate,
    JSONCreate,
    MarkdownCreate,
    PDFCreate,
    GithubRepoCreate,
    QACreate,
    YuqueCreate,
]


def text_create_to_knowledge(record: TextCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def image_create_to_knowledge(record: ImageCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def json_create_to_knowledge(record: JSONCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def markdown_create_to_knowledge(record: MarkdownCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def pdf_create_to_knowledge(record: PDFCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def github_repo_create_to_knowledge(
    record: GithubRepoCreate, tenant: Tenant
) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def qa_create_to_knowledge(record: QACreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


def yuque_create_to_knowledge(record: YuqueCreate, tenant: Tenant) -> Knowledge:
    return Knowledge(
        **record.model_dump(),
        tenant_id=tenant.tenant_id,
    )


KNOWLEDGE_CREATE_2_KNOWLEDGE_STRATEGY_MAP = {
    TextCreate: text_create_to_knowledge,
    ImageCreate: image_create_to_knowledge,
    JSONCreate: json_create_to_knowledge,
    MarkdownCreate: markdown_create_to_knowledge,
    PDFCreate: pdf_create_to_knowledge,
    GithubRepoCreate: github_repo_create_to_knowledge,
    QACreate: qa_create_to_knowledge,
    YuqueCreate: yuque_create_to_knowledge,
}
