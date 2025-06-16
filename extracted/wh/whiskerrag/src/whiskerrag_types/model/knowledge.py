from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Union
from uuid import UUID, uuid4

from pydantic import (
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from whiskerrag_types.model.knowledge_source import (
    KnowledgeSourceConfig,
    KnowledgeSourceEnum,
    TextSourceConfig,
)
from whiskerrag_types.model.splitter import KnowledgeSplitConfig
from whiskerrag_types.model.timeStampedModel import TimeStampedModel
from whiskerrag_types.model.utils import MetadataSerializer, calculate_sha256


class KnowledgeTypeEnum(str, Enum):
    """
    mime type of the knowledge. The type is used to determine how to process the knowledge and
    is also used to determine the type of the knowledge resource.
    different types of knowledge will be processed differently and have different load、split configurations.
    For example, text will be processed by splitter, while code will be processed by language parser.
    """

    TEXT = "text"
    IMAGE = "image"
    MARKDOWN = "markdown"
    LATEX = "latex"
    JSON = "json"
    DOCX = "docx"
    PDF = "pdf"
    QA = "qa"
    YUQUEDOC = "yuquedoc"
    YUQUE_BOOK = "yuque_book"
    GITHUB_REPO = "github_repo"
    # Code types， same as the language types
    CPP = "cpp"
    GO = "go"
    JAVA = "java"
    KOTLIN = "kotlin"
    JS = "js"
    TS = "ts"
    PHP = "php"
    PROTO = "proto"
    PYTHON = "python"
    RST = "rst"
    RUBY = "ruby"
    RUST = "rust"
    SCALA = "scala"
    SWIFT = "swift"
    HTML = "html"
    SOL = "sol"
    CSHARP = "csharp"
    COBOL = "cobol"
    C = "c"
    LUA = "lua"
    PERL = "perl"
    HASKELL = "haskell"
    ELIXIR = "elixir"
    POWERSHELL = "powershell"


class EmbeddingModelEnum(str, Enum):
    OPENAI = "openai"
    # lightweight
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    all_mpnet_base_v2 = "sentence-transformers/all-mpnet-base-v2"
    # multi languge
    PARAPHRASE_MULTILINGUAL_MINILM_L12_V2 = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    # chinese
    TEXT2VEC_BASE_CHINESE = "shibing624/text2vec-base-chinese"


class Knowledge(TimeStampedModel):
    knowledge_id: str = Field(
        default_factory=lambda: str(uuid4()), description="knowledge id"
    )
    space_id: str = Field(
        ...,
        description="the space of knowledge, example: petercat bot id, github repo name",
    )
    tenant_id: str = Field(..., description="tenant id")
    knowledge_type: KnowledgeTypeEnum = Field(
        KnowledgeTypeEnum.TEXT, description="type of knowledge resource"
    )
    knowledge_name: str = Field(
        ..., max_length=255, description="name of the knowledge resource"
    )
    source_type: KnowledgeSourceEnum = Field(
        KnowledgeSourceEnum.USER_INPUT_TEXT, description="source type"
    )
    source_config: KnowledgeSourceConfig = Field(
        ...,
        description="source config of the knowledge",
    )
    embedding_model_name: Union[EmbeddingModelEnum, str] = Field(
        EmbeddingModelEnum.OPENAI,
        description="name of the embedding model. you can set any other model if target embedding service registered",
    )
    split_config: KnowledgeSplitConfig = Field(
        ...,
        description="configuration for splitting the knowledge",
    )
    file_sha: Optional[str] = Field(None, description="SHA of the file")
    file_size: Optional[int] = Field(None, description="size of the file")
    metadata: dict = Field({}, description="additional metadata, user can update it")
    retrieval_count: int = Field(default=0, description="count of the retrieval")
    parent_id: Optional[str] = Field(None, description="parent knowledge id")
    enabled: bool = Field(True, description="is knowledge enabled")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if (
            self.source_type == KnowledgeSourceEnum.USER_INPUT_TEXT
            and isinstance(self.source_config, TextSourceConfig)
            and self.source_config.text is not None
            and self.file_sha is None
        ):
            self.file_sha = calculate_sha256(self.source_config.text)
            self.file_size = len(self.source_config.text.encode("utf-8"))

    def update(self, **kwargs: Dict[str, Any]) -> "Knowledge":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        return self

    @field_validator("enabled", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)

    @model_validator(mode="before")
    def pre_process_data(cls, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
        if isinstance(data, dict) and not data.get("knowledge_id"):
            data["knowledge_id"] = str(uuid4())

        if "metadata" not in data:
            data["metadata"] = {}

        if "knowledge_type" in data:
            knowledge_type = data["knowledge_type"]
            if isinstance(knowledge_type, KnowledgeTypeEnum):
                knowledge_type_str = knowledge_type.value
            else:
                knowledge_type_str = str(knowledge_type)
            data["metadata"]["_knowledge_type"] = knowledge_type_str

        if "_reference_url" not in data.get("metadata", {}):
            data["metadata"]["_reference_url"] = ""

        return data

    @field_serializer("metadata")
    def serialize_metadata(self, metadata: dict) -> dict:
        metadata = dict(metadata or {})
        knowledge_type = getattr(self, "knowledge_type", None)
        if knowledge_type:
            metadata["_knowledge_type"] = (
                knowledge_type.value
                if isinstance(knowledge_type, KnowledgeTypeEnum)
                else str(knowledge_type)
            )
        metadata.setdefault("_reference_url", "")
        sorted_metadata = MetadataSerializer.deep_sort_dict(metadata)
        return sorted_metadata if isinstance(sorted_metadata, dict) else {}

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
