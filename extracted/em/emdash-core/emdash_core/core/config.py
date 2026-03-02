"""Configuration management for EmDash."""

import logging
import os
import shutil
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


def _migrate_claude_to_emdash(claude_dir: Path, emdash_dir: Path) -> None:
    """Copy missing files/dirs from a .claude directory into .emdash.

    Only adds files that don't already exist in the target — never
    overwrites. Runs recursively so subdirectories (commands/, etc.)
    are handled too.
    """
    if not claude_dir.is_dir():
        return

    for src in claude_dir.rglob("*"):
        if not src.is_file():
            continue
        relative = src.relative_to(claude_dir)
        dest = emdash_dir / relative
        if dest.exists():
            continue
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            logger.debug("Migrated %s → %s", src, dest)
        except OSError as exc:
            logger.debug("Failed to migrate %s: %s", src, exc)


def migrate_from_claude() -> None:
    """Migrate missing config files from .claude to .emdash.

    Checks both project-level (./.claude → ./.emdash) and
    user-level (~/.claude → ~/.emdash). Existing .emdash files
    are never overwritten.
    """
    # Project-level
    project_claude = Path.cwd() / ".claude"
    project_emdash = Path.cwd() / ".emdash"
    _migrate_claude_to_emdash(project_claude, project_emdash)

    # User-level
    home_claude = Path.home() / ".claude"
    home_emdash = Path.home() / ".emdash"
    _migrate_claude_to_emdash(home_claude, home_emdash)


def get_config_dir() -> Path:
    """Get the emdash config directory (~/.emdash)."""
    return Path.home() / ".emdash"


def get_user_config_path() -> Path:
    """Get the user config file path (~/.emdash/.env)."""
    return get_config_dir() / ".env"


def get_local_env_path() -> Path:
    """Get the .env file path in the current working directory."""
    return Path.cwd() / ".env"


def load_env_files() -> None:
    """Load environment variables from config files.

    Load order (later files override earlier):
    1. ~/.emdash/.env (user-level defaults)
    2. .emdash/.env in cwd (project-level overrides)
    3. .env in cwd (project-level overrides, legacy)
    """
    # Load user-level config first (lower priority)
    user_env = get_user_config_path()
    if user_env.exists():
        load_dotenv(user_env, override=False)

    # Load project-level .emdash/.env (medium priority)
    project_env = Path.cwd() / ".emdash" / ".env"
    if project_env.exists():
        load_dotenv(project_env, override=True)

    # Load local .env from current working directory (highest priority, legacy)
    local_env = get_local_env_path()
    if local_env.exists():
        load_dotenv(local_env, override=True)


# Migrate missing files from .claude before loading config
migrate_from_claude()

# Load environment variables from config files
load_env_files()


class KuzuConfig(BaseModel):
    """Kuzu embedded database configuration."""

    database_path: str = Field(default=".emdash/index/kuzu_db")
    read_only: bool = Field(default=False)

    @classmethod
    def from_env(cls) -> "KuzuConfig":
        """Load configuration from environment variables."""
        return cls(
            database_path=os.getenv("KUZU_DATABASE_PATH", ".emdash/index/kuzu_db"),
            read_only=os.getenv("KUZU_READ_ONLY", "false").lower() == "true",
        )


class IngestionConfig(BaseModel):
    """Configuration for repository ingestion."""

    max_workers: int = Field(default=4, ge=1, le=16)
    batch_size: int = Field(default=1000, ge=100, le=10000)
    git_depth: Optional[int] = Field(default=None)
    ast_only: bool = Field(default=False, description="Skip Layer B (git) and Layer C (analytics)")
    ignore_patterns: list[str] = Field(
        default_factory=lambda: [
            "__pycache__",
            "*.pyc",
            "*.pyo",
            ".git",
            ".venv",
            "venv",
            "env",
            "node_modules",
            ".tox",
            ".pytest_cache",
            "*.egg-info",
            # Build outputs - minified files slow down indexing significantly
            "dist",
            "build",
            ".next",
            ".nuxt",
            ".output",
            "_astro",
            "*.min.js",
            "*.min.css",
            "*.bundle.js",
            "*.chunk.js",
            # Other common excludes
            "coverage",
            ".nyc_output",
            "*.map",
        ]
    )

    @classmethod
    def from_env(cls) -> "IngestionConfig":
        """Load configuration from environment variables."""
        git_depth = os.getenv("GIT_DEPTH")
        return cls(
            max_workers=int(os.getenv("MAX_WORKERS", "4")),
            batch_size=int(os.getenv("BATCH_SIZE", "1000")),
            git_depth=int(git_depth) if git_depth else None,
            ast_only=os.getenv("AST_ONLY", "false").lower() == "true",
        )


class AnalyticsConfig(BaseModel):
    """Configuration for graph analytics."""

    pagerank_iterations: int = Field(default=20, ge=5, le=100)
    pagerank_damping: float = Field(default=0.85, ge=0.0, le=1.0)
    clustering_algorithm: str = Field(default="louvain")

    @classmethod
    def from_env(cls) -> "AnalyticsConfig":
        """Load configuration from environment variables."""
        return cls(
            pagerank_iterations=int(os.getenv("PAGERANK_ITERATIONS", "20")),
            pagerank_damping=float(os.getenv("PAGERANK_DAMPING", "0.85")),
            clustering_algorithm=os.getenv("CLUSTERING_ALGORITHM", "louvain"),
        )


class GitHubConfig(BaseModel):
    """Configuration for GitHub API access."""

    token: Optional[str] = Field(default=None)

    @classmethod
    def from_env(cls) -> "GitHubConfig":
        """Load configuration from environment variables."""
        return cls(token=os.getenv("GITHUB_TOKEN"))

    @property
    def is_available(self) -> bool:
        """Check if GitHub token is configured."""
        return self.token is not None and len(self.token) > 0


class OpenAIConfig(BaseModel):
    """Configuration for OpenAI API (embeddings and chat)."""

    api_key: Optional[str] = Field(default=None)
    model: str = Field(default="text-embedding-3-small")
    dimensions: int = Field(default=1536)
    batch_size: int = Field(default=100, ge=1, le=2000)

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        """Load configuration from environment variables."""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            dimensions=int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS", "1536")),
            batch_size=int(os.getenv("OPENAI_BATCH_SIZE", "100")),
        )

    @property
    def is_available(self) -> bool:
        """Check if OpenAI API key is configured."""
        return self.api_key is not None and len(self.api_key) > 0


class AnthropicConfig(BaseModel):
    """Configuration for Anthropic API (chat)."""

    api_key: Optional[str] = Field(default=None)

    @classmethod
    def from_env(cls) -> "AnthropicConfig":
        """Load configuration from environment variables."""
        return cls(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    @property
    def is_available(self) -> bool:
        """Check if Anthropic API key is configured."""
        return self.api_key is not None and len(self.api_key) > 0


class FireworksConfig(BaseModel):
    """Configuration for Fireworks AI API (embeddings)."""

    api_key: Optional[str] = Field(default=None)
    batch_size: int = Field(default=100, ge=1, le=500)

    @classmethod
    def from_env(cls) -> "FireworksConfig":
        """Load configuration from environment variables."""
        return cls(
            api_key=os.getenv("FIREWORKS_API_KEY"),
            batch_size=int(os.getenv("FIREWORKS_BATCH_SIZE", "100")),
        )

    @property
    def is_available(self) -> bool:
        """Check if Fireworks API key is configured."""
        return self.api_key is not None and len(self.api_key) > 0


class ContextConfig(BaseModel):
    """Configuration for session context providers."""

    providers: list[str] = Field(
        default_factory=lambda: ["touched_areas"],
        description="Comma-separated list of context provider names",
    )
    min_score: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Minimum score threshold to include context items",
    )
    decay_factor: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Factor to multiply existing scores on new touch",
    )
    neighbor_depth: int = Field(
        default=2,
        ge=1,
        le=5,
        description="Number of hops for AST neighbor traversal",
    )
    max_items: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of context items to include",
    )
    enabled: bool = Field(
        default=True,
        description="Whether session context is enabled",
    )

    @classmethod
    def from_env(cls) -> "ContextConfig":
        """Load configuration from environment variables."""
        providers_str = os.getenv("CONTEXT_PROVIDERS", "touched_areas,explored_areas")
        return cls(
            providers=[p.strip() for p in providers_str.split(",") if p.strip()],
            min_score=float(os.getenv("CONTEXT_MIN_SCORE", "0.5")),
            decay_factor=float(os.getenv("CONTEXT_DECAY_FACTOR", "0.8")),
            neighbor_depth=int(os.getenv("CONTEXT_NEIGHBOR_DEPTH", "2")),
            max_items=int(os.getenv("CONTEXT_MAX_ITEMS", "50")),
            enabled=os.getenv("CONTEXT_ENABLED", "true").lower() == "true",
        )


class AgentConfig(BaseModel):
    """Configuration for agent behavior."""

    max_context_messages: int = Field(
        default=25,
        ge=5,
        le=100,
        description="Maximum number of previous messages to send to LLM (excludes system prompt)",
    )

    max_iterations: int = Field(
        default=100,
        ge=10,
        le=200,
        description="Maximum tool call iterations before stopping",
    )

    tool_max_output_tokens: int = Field(
        default=25000,
        ge=1000,
        le=100000,
        description="Maximum tokens for tool output (estimated at ~4 chars/token)",
    )

    tool_parallel_workers: int = Field(
        default=6,
        ge=1,
        le=16,
        description="Maximum parallel workers for concurrent tool execution",
    )

    context_compact_threshold: float = Field(
        default=0.8,
        ge=0.5,
        le=0.95,
        description="Trigger context compaction at this % of model's context limit",
    )

    context_compact_target: float = Field(
        default=0.5,
        ge=0.3,
        le=0.7,
        description="Target context size after compaction (% of model's limit)",
    )

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Load configuration from environment variables."""
        return cls(
            max_context_messages=int(os.getenv("EMDASH_MAX_CONTEXT_MESSAGES", "25")),
            max_iterations=int(os.getenv("EMDASH_MAX_ITERATIONS", "100")),
            tool_max_output_tokens=int(os.getenv("EMDASH_TOOL_MAX_OUTPUT", "25000")),
            tool_parallel_workers=int(os.getenv("EMDASH_TOOL_PARALLEL_WORKERS", "6")),
            context_compact_threshold=float(os.getenv("EMDASH_CONTEXT_COMPACT_THRESHOLD", "0.8")),
            context_compact_target=float(os.getenv("EMDASH_CONTEXT_COMPACT_TARGET", "0.5")),
        )


class MCPConfig(BaseModel):
    """Configuration for MCP (Model Context Protocol) servers."""

    github_token: Optional[str] = Field(default=None)
    github_repo: Optional[str] = Field(default=None)  # Format: "owner/repo"
    server_mode: str = Field(default="local")  # "local" | "docker"
    toolsets: list[str] = Field(
        default_factory=lambda: ["repos", "pull_requests", "issues", "code_security"]
    )
    binary_path: str = Field(default="github-mcp-server")
    read_only: bool = Field(default=True)
    timeout: int = Field(default=30)

    @staticmethod
    def _get_gh_cli_token() -> Optional[str]:
        """Get GitHub token from gh CLI if available (supports browser auth)."""
        import subprocess
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return None

    @staticmethod
    def _get_repo_from_git() -> Optional[str]:
        """Auto-detect owner/repo from git remote origin URL."""
        import subprocess
        import re
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                url = result.stdout.strip()
                # Handle SSH: git@github.com:owner/repo.git
                ssh_match = re.search(r"git@github\.com[:/](.+?)/(.+?)(?:\.git)?$", url)
                if ssh_match:
                    return f"{ssh_match.group(1)}/{ssh_match.group(2)}"
                # Handle HTTPS: https://github.com/owner/repo.git
                https_match = re.search(r"github\.com/(.+?)/(.+?)(?:\.git)?$", url)
                if https_match:
                    return f"{https_match.group(1)}/{https_match.group(2)}"
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return None

    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Load configuration from environment variables.

        Token priority:
        1. GITHUB_TOKEN env var
        2. GITHUB_PERSONAL_ACCESS_TOKEN env var
        3. gh CLI auth token (supports browser auth for private repos)
        """
        toolsets_str = os.getenv("MCP_TOOLSETS", "repos,pull_requests,issues,code_security")

        # Try env vars first, then fall back to gh CLI
        github_token = (
            os.getenv("GITHUB_TOKEN") or
            os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN") or
            MCPConfig._get_gh_cli_token()
        )

        # Auto-detect repo from git remote if not set in env
        github_repo = os.getenv("GITHUB_REPO") or MCPConfig._get_repo_from_git()

        return cls(
            github_token=github_token,
            github_repo=github_repo,
            server_mode=os.getenv("MCP_SERVER_MODE", "local"),
            toolsets=toolsets_str.split(",") if toolsets_str else [],
            binary_path=os.getenv("MCP_BINARY_PATH", "github-mcp-server"),
            read_only=os.getenv("MCP_READ_ONLY", "true").lower() == "true",
            timeout=int(os.getenv("MCP_TIMEOUT", "30")),
        )

    @property
    def is_available(self) -> bool:
        """Check if MCP is properly configured."""
        return self.github_token is not None and len(self.github_token) > 0

    @property
    def repo_owner(self) -> Optional[str]:
        """Get the owner from github_repo (e.g., 'wix-private' from 'wix-private/picasso')."""
        if self.github_repo and "/" in self.github_repo:
            return self.github_repo.split("/")[0]
        return None

    @property
    def repo_name(self) -> Optional[str]:
        """Get the repo name from github_repo (e.g., 'picasso' from 'wix-private/picasso')."""
        if self.github_repo and "/" in self.github_repo:
            return self.github_repo.split("/")[1]
        return None


class MemoryConfig(BaseModel):
    """Configuration for the OpenClaw-style memory system.

    Controls the markdown-on-disk memory system used by the Open Agent.
    """

    enabled: bool = Field(default=True, description="Enable the memory system")
    long_term_file: str = Field(default="MEMORY.md", description="Long-term memory filename")
    daily_dir: str = Field(default="memory", description="Daily logs directory name")

    backend: str = Field(default="qmd", description="Index backend: 'sqlite' or 'qmd'")

    # Bootstrap / injection limits (matching OpenClaw defaults)
    bootstrap_max_chars: int = Field(
        default=20_000, ge=1000, le=100_000,
        description="Max chars per bootstrap file injected into system prompt",
    )
    bootstrap_total_max_chars: int = Field(
        default=150_000, ge=5000, le=500_000,
        description="Max total chars for all bootstrap files combined",
    )

    # Search / indexing
    chunk_tokens: int = Field(default=400, ge=100, le=2000, description="Target chunk size in tokens")
    overlap_tokens: int = Field(default=80, ge=0, le=500, description="Overlap between chunks in tokens")
    max_results: int = Field(default=5, ge=1, le=20, description="Max search results to return")
    timeout_ms: int = Field(default=3000, ge=500, le=10000, description="Search timeout in milliseconds")

    # QMD hybrid search settings
    qmd_max_snippet_chars: int = Field(default=700, ge=100, le=2000, description="Max snippet size for QMD results")
    qmd_embedding_model: Optional[str] = Field(
        default=None,
        description="Embedding model for QMD vector search (e.g. 'openai:text-embedding-3-small'). None = auto-select.",
    )
    qmd_vector_weight: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Weight balance: 0.0 = BM25 only, 1.0 = vector only, 0.5 = equal",
    )

    # Compaction flush
    flush_enabled: bool = Field(default=True, description="Enable pre-compaction memory flush")
    flush_soft_threshold_tokens: int = Field(default=4000, ge=1000, le=20000)

    @classmethod
    def from_env(cls, json_overrides: dict | None = None) -> "MemoryConfig":
        """Load from env vars with optional JSON config overrides."""
        base = json_overrides or {}
        qmd_section = base.get("qmd", {}) if isinstance(base.get("qmd"), dict) else {}

        return cls(
            enabled=base.get("enabled", os.getenv("EMDASH_MEMORY_ENABLED", "true").lower() == "true"),
            long_term_file=base.get("long_term_file", os.getenv("EMDASH_MEMORY_LT_FILE", "MEMORY.md")),
            daily_dir=base.get("daily_dir", os.getenv("EMDASH_MEMORY_DAILY_DIR", "memory")),
            backend=base.get("backend", os.getenv("EMDASH_MEMORY_BACKEND", "qmd")),
            bootstrap_max_chars=base.get("bootstrap_max_chars", int(os.getenv("EMDASH_BOOTSTRAP_MAX_CHARS", "20000"))),
            bootstrap_total_max_chars=base.get("bootstrap_total_max_chars", int(os.getenv("EMDASH_BOOTSTRAP_TOTAL_MAX_CHARS", "150000"))),
            chunk_tokens=base.get("chunk_tokens", int(os.getenv("EMDASH_MEMORY_CHUNK_TOKENS", "400"))),
            overlap_tokens=base.get("overlap_tokens", int(os.getenv("EMDASH_MEMORY_OVERLAP_TOKENS", "80"))),
            max_results=base.get("max_results", int(os.getenv("EMDASH_MEMORY_MAX_RESULTS", "5"))),
            timeout_ms=base.get("timeout_ms", int(os.getenv("EMDASH_MEMORY_TIMEOUT_MS", "3000"))),
            qmd_max_snippet_chars=qmd_section.get("max_snippet_chars", int(os.getenv("EMDASH_QMD_MAX_SNIPPET", "700"))),
            qmd_embedding_model=qmd_section.get("embedding_model", os.getenv("EMDASH_QMD_EMBEDDING_MODEL")),
            qmd_vector_weight=float(qmd_section.get("vector_weight", os.getenv("EMDASH_QMD_VECTOR_WEIGHT", "0.5"))),
            flush_enabled=base.get("flush_enabled", os.getenv("EMDASH_MEMORY_FLUSH_ENABLED", "true").lower() == "true"),
        )


class ExperimentalConfig(BaseModel):
    """Feature flags for experimental features.

    Loaded from emdash.config.json "experimental" section, with
    environment variable overrides. Env vars take precedence.

    Example emdash.config.json:
        {
            "experimental": {
                "agent_teams": true,
                "tasks_v2": true
            }
        }
    """

    agent_teams: bool = Field(
        default=False,
        description="Enable Agent Teams — multi-agent orchestration with shared tasks and messaging",
    )
    tasks_v2: bool = Field(
        default=True,
        description="Enable Tasks v2 — file-based task coordination with atomic claiming",
    )

    @classmethod
    def from_env(cls, json_overrides: dict | None = None) -> "ExperimentalConfig":
        """Load from env vars with optional JSON config overrides.

        Priority (highest wins):
            1. Environment variables (EMDASH_EXPERIMENTAL_AGENT_TEAMS, EMDASH_TASKS_V2)
            2. emdash.config.json "experimental" section
            3. Feature defaults
        """
        base = json_overrides or {}

        def _resolve_bool(env_var: str, json_key: str, default: bool = False) -> bool:
            env_val = os.environ.get(env_var, "").lower()
            if env_val in ("1", "true", "yes"):
                return True
            if env_val in ("0", "false", "no"):
                return False
            # Fall back to JSON config
            json_val = base.get(json_key)
            if isinstance(json_val, bool):
                return json_val
            return default

        return cls(
            agent_teams=_resolve_bool("EMDASH_EXPERIMENTAL_AGENT_TEAMS", "agent_teams"),
            tasks_v2=_resolve_bool("EMDASH_TASKS_V2", "tasks_v2", default=True),
        )


class EmDashConfig(BaseModel):
    """Main configuration for EmDash."""

    kuzu: KuzuConfig = Field(default_factory=KuzuConfig)
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig)
    analytics: AnalyticsConfig = Field(default_factory=AnalyticsConfig)
    github: GitHubConfig = Field(default_factory=GitHubConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    fireworks: FireworksConfig = Field(default_factory=FireworksConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    context: ContextConfig = Field(default_factory=ContextConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    experimental: ExperimentalConfig = Field(default_factory=ExperimentalConfig)
    log_level: str = Field(default="WARNING")

    @classmethod
    def from_env(cls) -> "EmDashConfig":
        """Load full configuration from environment variables and config files."""
        # Load JSON config for experimental flags and memory settings
        json_experimental = _load_json_config_section("experimental")
        json_memory = _load_json_config_section("memory")

        return cls(
            kuzu=KuzuConfig.from_env(),
            ingestion=IngestionConfig.from_env(),
            analytics=AnalyticsConfig.from_env(),
            github=GitHubConfig.from_env(),
            openai=OpenAIConfig.from_env(),
            anthropic=AnthropicConfig.from_env(),
            fireworks=FireworksConfig.from_env(),
            mcp=MCPConfig.from_env(),
            context=ContextConfig.from_env(),
            agent=AgentConfig.from_env(),
            memory=MemoryConfig.from_env(json_memory),
            experimental=ExperimentalConfig.from_env(json_experimental),
            log_level=os.getenv("LOG_LEVEL", "WARNING"),
        )

    def validate_kuzu(self) -> None:
        """Validate Kuzu configuration."""
        if not self.kuzu.database_path:
            raise ConfigurationError("Kuzu database path is required")


def _load_json_config_section(section: str) -> dict | None:
    """Load a section from emdash.config.json if it exists.

    Searches in order:
        1. EMDASH_CONFIG_PATH env var (explicit override)
        2. ./emdash.config.json (project root)
        3. ./.emdash/config.json (project .emdash dir)

    Returns the section dict, or None if not found.
    """
    import json

    env_path = os.getenv("EMDASH_CONFIG_PATH")
    candidates = (
        [Path(env_path)] if env_path else [
            Path.cwd() / "emdash.config.json",
            Path.cwd() / ".emdash" / "config.json",
        ]
    )

    for path in candidates:
        if path.is_file():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict) and section in raw:
                    val = raw[section]
                    return val if isinstance(val, dict) else None
            except (json.JSONDecodeError, OSError):
                pass

    return None


# Global configuration instance
_config: Optional[EmDashConfig] = None


def get_config() -> EmDashConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = EmDashConfig.from_env()
    return _config


def set_config(config: EmDashConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config


def _find_json_config_path() -> Path:
    """Find or create the JSON config file path.

    Returns the first existing config file, or creates emdash.config.json
    in the current directory if none exists.
    """
    env_path = os.getenv("EMDASH_CONFIG_PATH")
    if env_path:
        return Path(env_path)

    candidates = [
        Path.cwd() / "emdash.config.json",
        Path.cwd() / ".emdash" / "config.json",
    ]

    for path in candidates:
        if path.is_file():
            return path

    # Default: create emdash.config.json in project root
    return candidates[0]


def enable_experimental(feature: str) -> None:
    """Enable an experimental feature in emdash.config.json and reload config.

    Writes the setting to the JSON config file so it persists across
    sessions. Also updates the in-memory config immediately.

    Args:
        feature: Feature key (e.g., "agent_teams", "tasks_v2").
    """
    import json

    path = _find_json_config_path()

    # Load existing config or start fresh
    if path.is_file():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raw = {}
    else:
        raw = {}

    # Set the experimental flag
    if "experimental" not in raw or not isinstance(raw["experimental"], dict):
        raw["experimental"] = {}
    raw["experimental"][feature] = True

    # Write back
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")

    # Reset cached config so next get_config() picks up the change
    global _config
    _config = None
