"""Core module for EmDash - models, configuration, and exceptions."""

from .config import (
    EmDashConfig,
    KuzuConfig,
    IngestionConfig,
    AnalyticsConfig,
    GitHubConfig,
    OpenAIConfig,
    AnthropicConfig,
    FireworksConfig,
    ContextConfig,
    AgentConfig,
    MCPConfig,
    get_config,
    set_config,
    get_config_dir,
    get_user_config_path,
    get_local_env_path,
    load_env_files,
)

from .exceptions import (
    EmDashException,
    ConfigurationError,
    DatabaseConnectionError,
    RepositoryError,
    ParsingError,
    GraphBuildError,
    QueryError,
    AnalyticsError,
)

from .models import (
    FileEntity,
    ClassEntity,
    FunctionEntity,
    ModuleEntity,
    ImportStatement,
    CommitEntity,
    FileModification,
    AuthorEntity,
    PullRequestEntity,
    TaskEntity,
    RepositoryEntity,
    ClusterEntity,
    CodebaseEntities,
    FileEntities,
    GitData,
)

from .review_config import (
    ReviewConfig,
    load_review_config,
)

__all__ = [
    # Config
    "EmDashConfig",
    "KuzuConfig",
    "IngestionConfig",
    "AnalyticsConfig",
    "GitHubConfig",
    "OpenAIConfig",
    "AnthropicConfig",
    "FireworksConfig",
    "ContextConfig",
    "AgentConfig",
    "MCPConfig",
    "get_config",
    "set_config",
    "get_config_dir",
    "get_user_config_path",
    "get_local_env_path",
    "load_env_files",
    # Exceptions
    "EmDashException",
    "ConfigurationError",
    "DatabaseConnectionError",
    "RepositoryError",
    "ParsingError",
    "GraphBuildError",
    "QueryError",
    "AnalyticsError",
    # Models
    "FileEntity",
    "ClassEntity",
    "FunctionEntity",
    "ModuleEntity",
    "ImportStatement",
    "CommitEntity",
    "FileModification",
    "AuthorEntity",
    "PullRequestEntity",
    "TaskEntity",
    "RepositoryEntity",
    "ClusterEntity",
    "CodebaseEntities",
    "FileEntities",
    "GitData",
    # Review config
    "ReviewConfig",
    "load_review_config",
]
