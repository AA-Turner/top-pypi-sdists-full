"""
cvc.core.models — Pydantic schemas for the Cognitive Version Control Merkle DAG.

Every cognitive commit is a node in a content-addressed Merkle DAG.  The SHA-256
hash of each node is derived from:
    hash = SHA-256( parent_hash || serialized_content_blob || metadata_json )

This guarantees cryptographic immutability: altering any ancestor invalidates
every descendant hash, making tampering immediately detectable.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import uuid
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, computed_field


# ---------------------------------------------------------------------------
# Cross-platform directory helpers
# ---------------------------------------------------------------------------

def get_global_config_dir() -> Path:
    """
    Return the user-level config directory for CVC, created if needed.

    - Windows:  %LOCALAPPDATA%\\cvc  (e.g. C:\\Users\\X\\AppData\\Local\\cvc)
    - macOS:    ~/Library/Application Support/cvc
    - Linux:    $XDG_CONFIG_HOME/cvc  (default ~/.config/cvc)
    """
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    d = base / "cvc"
    d.mkdir(parents=True, exist_ok=True)
    return d


def discover_cvc_root(start: Path | None = None) -> Path | None:
    """
    Walk up from *start* (default: CWD) looking for a ``.cvc/`` directory,
    similar to how Git walks up to find ``.git/``.

    Returns the **project root** (parent of ``.cvc/``), or ``None``.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        candidate = current / ".cvc"
        if candidate.is_dir():
            return current
        parent = current.parent
        if parent == current:
            break  # Reached filesystem root
        current = parent
    return None


class GlobalConfig(BaseModel):
    """
    User-level defaults stored in the global config directory.
    Saved as ``config.json`` so new projects inherit the user's preferred
    provider, model, and agent identity.

    API keys are stored per-provider so the user only needs to enter them
    once via ``cvc setup``.  Environment variables always take precedence.
    """
    provider: str = "passthrough"  # Safe default: no internal LLM until user runs setup
    model: str = "claude-opus-4-6"
    agent_id: str = "sofia"
    api_keys: dict[str, str] = {}
    # Google Cloud Vertex AI — extra fields beyond the API key
    vertex_project_id: str = ""
    vertex_location: str = "us-central1"

    # ── Agent execution budgets (parity with upstream, user-configurable) ──
    # Override via env (CVC_MAX_ITERATIONS, CVC_AGENT_TIMEOUT, …) or dashboard.
    # 0 = use built-in default (80 / 40 / 900s / 300s).
    max_iterations: int = 0                # 0 → default 80 (normal models)
    max_iterations_expensive: int = 0      # 0 → default 40 (Opus/expensive)
    agent_timeout: float = 0.0             # 0 → default 900s total per turn
    tool_timeout: float = 0.0              # 0 → default 300s per tool call

    @classmethod
    def load(cls) -> "GlobalConfig":
        """Load from disk, returning defaults if the file doesn't exist."""
        path = get_global_config_dir() / "config.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                # Canonicalize provider aliases — "copilot" is a friendly alias for
                # "github" (the GitHub Copilot provider). All internal code keys on
                # "github", but the user / setup wizard / env auto-detect path may
                # write "copilot". Normalize on load to prevent split-brain auth.
                if data.get("provider") == "copilot":
                    data["provider"] = "github"
                # Same for api_keys keying.
                api_keys = data.get("api_keys") or {}
                if "copilot" in api_keys and "github" not in api_keys:
                    api_keys["github"] = api_keys.pop("copilot")
                    data["api_keys"] = api_keys
                return cls(**data)
            except Exception as e:
                import sys
                print(f"Warning: Failed to parse global config '{path}': {e}", file=sys.stderr)
                return cls()
        return cls()

    def save(self) -> Path:
        """Persist to disk. Returns the file path."""
        path = get_global_config_dir() / "config.json"
        path.write_text(
            json.dumps(self.model_dump(), indent=2),
            encoding="utf-8",
        )
        return path


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class CommitType(StrEnum):
    """Classification of cognitive commits."""
    CHECKPOINT = "checkpoint"       # Manual or auto save-point
    ANALYSIS = "analysis"           # Agent completed an analysis phase
    GENERATION = "generation"       # Agent produced code / output
    ROLLBACK = "rollback"           # Commit created on rollback restoration
    MERGE = "merge"                 # Result of a semantic merge
    ANCHOR = "anchor"               # Full anchor state (no delta)
    THOUGHT_STEP = "thought_step"   # Micro-rollback: single thought or internal reasoning
    TOOL_CALL = "tool_call"         # Micro-rollback: execution of a tool
    DISTILLATION = "distillation"   # Context distillation checkpoint
    COGNOME_EPOCH = "cognome_epoch" # COGNOME training epoch checkpoint


class BranchStatus(StrEnum):
    ACTIVE = "active"
    MERGED = "merged"
    ARCHIVED = "archived"


# ---------------------------------------------------------------------------
# Content Blob — the raw cognitive payload
# ---------------------------------------------------------------------------

class ContextMessage(BaseModel):
    """A single message in the agent's context window."""
    role: str                       # system | user | assistant | tool
    content: str
    name: str | None = None
    tool_call_id: str | None = None
    timestamp: float = Field(default_factory=time.time)


class ContentBlob(BaseModel):
    """
    The serialized cognitive state at the moment of a commit.

    Contains the full conversation context, tool outputs, file provenance,
    bash command history, and the agent's internal reasoning trace.

    This is the heart of *Cognitive* Version Control — every interaction
    the agent had with the codebase is captured here, not just chat messages.
    """
    messages: list[ContextMessage] = Field(default_factory=list)
    reasoning_trace: str = ""
    tool_outputs: dict[str, Any] = Field(default_factory=dict)        # "{turn}:{tool}:{idx}" → full result
    source_files: dict[str, str] = Field(default_factory=dict)        # path → SHA-256 (files READ)
    files_written: dict[str, str] = Field(default_factory=dict)       # path → SHA-256 (files CREATED/MODIFIED)
    bash_commands: list[dict[str, Any]] = Field(default_factory=list)  # [{command, exit_code, output, ts}]
    query_history: list[dict[str, Any]] = Field(default_factory=list)  # [{role, content, timestamp}]
    token_count: int = 0
    distilled_summary: str | None = None                              # Compressed context summary
    semantic_id: str | None = None                                    # UUID linking to ChromaDB vector embedding
    engram_preamble: str | None = None                                # COGNOME-compiled preamble injected for this turn

    def canonical_bytes(self) -> bytes:
        """Deterministic serialisation for hashing (sorted keys, no whitespace)."""
        return json.dumps(
            self.model_dump(),
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")


# ---------------------------------------------------------------------------
# Commit Metadata
# ---------------------------------------------------------------------------

class CommitMetadata(BaseModel):
    """Immutable metadata attached to every cognitive commit."""
    timestamp: float = Field(default_factory=time.time)
    agent_id: str = "sofia"
    mode: str | None = None                 # Which service created this: "mcp", "proxy", or "cli"
    git_commit_sha: str | None = None      # The linked codebase commit
    provider: str | None = None             # e.g. "anthropic", "openai"
    model: str | None = None                # e.g. "claude-sonnet-4-20250514"
    cache_id: str | None = None             # Provider-side cache handle
    tags: list[str] = Field(default_factory=list)
    # Cognitive context — actual LLM usage tracked per commit
    session_id: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cost_usd: float = 0.0
    turn_count: int = 0
    distilled_ratio: float = 0.0            # Ratio of token compression if distillation was used

    # ── Hive Mind fields (Phase 2) ────────────────────────────────────────
    squad: str | None = None                # Squad/team this commit belongs to (e.g. "aegis")
    target_agent_id: str | None = None      # Who this commit is addressed to
    rank: str | None = None                 # Agent's hierarchical level (e.g. "specialist", "captain")
    action_type: str | None = None          # Hive action: DIRECTIVE, TASK_ASSIGNMENT, RESULT, etc.

    # ── COGNOME fields ────────────────────────────────────────────────────
    engram_hash: str | None = None          # SHA-256 of the Engram preamble injected for this turn
    cognome_version: str | None = None      # CAS key of the active COGNOME at commit time
    cognome_compression: float = 0.0        # Compression ratio achieved by COGNOME

    # ── Soul-Layer fields ────────────────────────────────────────────────
    #
    # These fields extend the cognitive commit to carry soul-layer
    # metadata — the emotional context of this specific commit and
    # the preservation flag for digital parents.
    #
    # preservation_mode: when True, this commit was captured at
    # maximum fidelity because the user has enabled preservation
    # mode (terminal illness, advanced age, or explicit request).
    # These commits get the highest retention priority and are
    # never pruned or delta-compressed. They are the raw material
    # for the eventual digital parents instantiation.
    #
    # emotional_mood: the user's observed mood during this turn.
    # Captured passively from tone, not from explicit statements.
    # Builds the emotional arc of the relationship over time.
    #
    # emotional_intensity: 0.0 (neutral) to 1.0 (overwhelming).
    # Helps the soul weight which memories matter most.
    #
    # life_event: if this commit captured a significant life event
    # (breakthrough, setback, milestone), a short description goes
    # here. Most commits will have this as None — only the moments
    # that matter get tagged.
    preservation_mode: bool = False
    emotional_mood: str | None = None       # frustrated|excited|focused|tired|curious|proud|anxious|neutral
    emotional_intensity: float = 0.0
    life_event: str | None = None           # Short description if this commit is a life milestone

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.model_dump(),
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")


# ---------------------------------------------------------------------------
# The Cognitive Commit — a Merkle DAG Node
# ---------------------------------------------------------------------------

class CognitiveCommit(BaseModel):
    """
    A single node in the Merkle DAG.

    The ``commit_hash`` is computed as:
        SHA-256( parent_hash || content_blob.canonical_bytes() || metadata.canonical_bytes() )

    For merge commits, ``parent_hashes`` contains ≥ 2 parents.
    """
    commit_hash: str = ""                   # Populated by compute_hash()
    parent_hashes: list[str] = Field(default_factory=list)
    commit_type: CommitType = CommitType.CHECKPOINT
    message: str = ""
    content_blob: ContentBlob = Field(default_factory=ContentBlob)
    metadata: CommitMetadata = Field(default_factory=CommitMetadata)

    # Delta compression fields
    is_delta: bool = False
    anchor_hash: str | None = None          # The full anchor this delta is relative to
    delta_bytes: bytes | None = None        # VCDIFF-encoded delta (stored in CAS, not in index)

    def compute_hash(self) -> str:
        """Derive the SHA-256 Merkle hash from content + parents + metadata."""
        h = hashlib.sha256()
        for ph in sorted(self.parent_hashes):
            h.update(ph.encode("utf-8"))
        h.update(self.content_blob.canonical_bytes())
        h.update(self.metadata.canonical_bytes())
        self.commit_hash = h.hexdigest()
        return self.commit_hash

    @computed_field  # type: ignore[prop-decorator]
    @property
    def short_hash(self) -> str:
        return self.commit_hash[:12] if self.commit_hash else ""


# ---------------------------------------------------------------------------
# Branch Pointer
# ---------------------------------------------------------------------------

class BranchPointer(BaseModel):
    """A named pointer to the tip of a commit chain (analogous to a Git ref)."""
    name: str
    head_hash: str                          # Points to the latest CognitiveCommit
    status: BranchStatus = BranchStatus.ACTIVE
    created_at: float = Field(default_factory=time.time)
    description: str = ""
    parent_branch: str | None = None        # For tracking branch lineage


# ---------------------------------------------------------------------------
# Request / Response models for the Cognitive Proxy API
# ---------------------------------------------------------------------------

class CVCCommitRequest(BaseModel):
    """Payload for the cvc_commit tool."""
    message: str = ""
    commit_type: CommitType = CommitType.CHECKPOINT
    tags: list[str] = Field(default_factory=list)
    context_extras: dict[str, Any] = Field(default_factory=dict)  # Injected by agent layer


class CVCBranchRequest(BaseModel):
    """Payload for the cvc_branch tool."""
    name: str
    source_commit: str | None = None        # Defaults to current HEAD
    description: str = ""


class CVCMergeRequest(BaseModel):
    """Payload for the cvc_merge tool."""
    source_branch: str
    target_branch: str = "main"


class CVCRestoreRequest(BaseModel):
    """Payload for the cvc_restore (time-travel) tool."""
    commit_hash: str                        # Full or short hash


class CVCOperationResponse(BaseModel):
    """Unified response envelope for all CVC operations."""
    success: bool
    operation: str
    commit_hash: str | None = None
    branch: str | None = None
    message: str = ""
    detail: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Proxy pass-through models (OpenAI-compatible chat schema)
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str
    content: str | list[dict[str, Any]] | None = None
    name: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[dict[str, Any]] | None = None


class ChatCompletionRequest(BaseModel):
    """Subset of the OpenAI chat-completion request used by the proxy."""
    model: str = "claude-opus-4-6"
    messages: list[ChatMessage] = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False
    tools: list[dict[str, Any]] | None = None
    tool_choice: str | dict[str, Any] | None = None
    # CVC extension fields (ignored by upstream providers)
    cvc_branch: str | None = None
    cvc_auto_commit: bool = True


class ChatCompletionChoice(BaseModel):
    index: int = 0
    message: ChatMessage
    finish_reason: str = "stop"


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex[:24]}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str = ""
    choices: list[ChatCompletionChoice] = Field(default_factory=list)
    usage: UsageInfo = Field(default_factory=UsageInfo)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class CVCConfig(BaseModel):
    """Runtime configuration for the CVC system."""
    cvc_root: Path = Path(".cvc")
    db_path: Path = Path(".cvc/cvc.db")
    objects_dir: Path = Path(".cvc/objects")
    branches_dir: Path = Path(".cvc/branches")
    default_branch: str = "main"
    anchor_interval: int = 10               # Full snapshot every N commits
    agent_id: str = "sofia"
    mode: str = "cli"                       # Which service is running: "mcp", "proxy", or "cli"

    # Provider — supports: anthropic, openai, google, ollama, github, copilot, passthrough
    provider: str = "passthrough"
    upstream_base_url: str = ""  # empty = determined at request time
    model: str = "claude-opus-4-6"
    api_key: str = ""

    # Proxy
    proxy_host: str = "127.0.0.1"
    proxy_port: int = 13421

    # Vector store — Tier 3 is REQUIRED (ChromaDB is a core dependency)
    vector_enabled: bool = True  # Always True — Tier 3 is non-optional
    chroma_persist_dir: Path = Path(".cvc/chroma")

    # Tier 4 — PageIndex (LLM-powered document RAG, CLI agent only)
    pageindex_dir: Path = Path(".cvc/pageindex")

    # COGNOME — learned context compilation
    cognome_enabled: bool = True
    cognome_budget_tokens: int = 1200       # Default token budget for compiled Engrams
    cognome_auto_inject: bool = True        # Auto-inject Engram before upstream LLM calls
    cognome_l2_enabled: bool = True         # L2: semantic re-rank of selected noemata
    cognome_l3_enabled: bool = True         # L3: extractive compression of budget overflow
    cognome_l3_overflow_fraction: float = 0.15  # Fraction of budget reserved for L3 summary

    def ensure_dirs(self) -> None:
        """Create all required directories (including vector store and PageIndex)."""
        for d in (self.cvc_root, self.objects_dir, self.branches_dir, self.chroma_persist_dir, self.pageindex_dir):
            d.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _resolve_vector_enabled() -> bool:
        """Tier 3 (ChromaDB) is always enabled — it is a core dependency.

        The CVC_VECTOR_ENABLED env var is no longer honoured.
        Only Tier 4 (PageIndex) is optional.
        """
        return True

    @classmethod
    def for_project(cls, project_root: Path | None = None, **overrides: Any) -> "CVCConfig":
        """
        Build a config anchored to a specific project directory.

        Resolution order (highest priority first):
          1. Explicit ``overrides`` keyword arguments
          2. Environment variables (CVC_PROVIDER, CVC_MODEL, …)
          3. Global config (~/.config/cvc/config.json)
          4. Built-in defaults

        If *project_root* is ``None``, :func:`discover_cvc_root` is used to
        walk up from CWD.  If still not found, CWD is used.
        """
        # Discover project root
        if project_root is None:
            project_root = discover_cvc_root()
        if project_root is None:
            project_root = Path.cwd()

        root = project_root / ".cvc"

        # Global config as base defaults
        gc = GlobalConfig.load()

        # Provider resolution
        from cvc.adapters import PROVIDER_DEFAULTS  # Lazy to avoid circular import

        provider = overrides.pop("provider", None) or os.getenv("CVC_PROVIDER", gc.provider)
        defaults = PROVIDER_DEFAULTS.get(provider, {})

        # API key — resolution: env var → global config → empty
        api_key_env_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "github": "GITHUB_TOKEN",
            "copilot": "COPILOT_GITHUB_TOKEN",
            "ollama": "",
            "lmstudio": "",
            "passthrough": "",  # no key needed; AI tool's own key is forwarded
        }
        api_key_env = api_key_env_map.get(provider, "")
        api_key = os.getenv(api_key_env, "") if api_key_env else ""
        if not api_key:
            api_key = gc.api_keys.get(provider, "")

        # Upstream URL
        upstream_url_map = {
            "anthropic": "https://api.anthropic.com",
            "openai": "https://api.openai.com",
            "google": "https://generativelanguage.googleapis.com",
            "github": "https://models.inference.ai.azure.com",
            "copilot": "https://api.githubcopilot.com",
            "ollama": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            "passthrough": "",  # determined at request time from client headers
        }

        return cls(
            cvc_root=root,
            db_path=root / "cvc.db",
            objects_dir=root / "objects",
            branches_dir=root / "branches",
            default_branch=os.getenv("CVC_DEFAULT_BRANCH", "main"),
            anchor_interval=int(os.getenv("CVC_ANCHOR_INTERVAL", "10")),
            agent_id=overrides.pop("agent_id", None) or os.getenv("CVC_AGENT_ID", gc.agent_id),
            provider=provider,
            upstream_base_url=os.getenv(
                "CVC_UPSTREAM_URL",
                upstream_url_map.get(provider, "https://api.anthropic.com"),
            ),
            model=overrides.pop("model", None) or os.getenv(
                "CVC_MODEL",
                defaults.get("model", gc.model),
            ),
            api_key=api_key,
            proxy_host=os.getenv("CVC_HOST", "127.0.0.1"),
            proxy_port=int(os.getenv("CVC_PORT", "13421")),
            vector_enabled=True,  # Tier 3 is always enabled
            chroma_persist_dir=root / "chroma",
            pageindex_dir=root / "pageindex",
            **overrides,
        )


# ---------------------------------------------------------------------------
# Agent Template — for creating custom agents via dashboard / CLI
# ---------------------------------------------------------------------------

class AgentTemplate(BaseModel):
    """
    Reusable agent configuration template.

    Used by the Agent Creator system — users define agent blueprints that
    can be instantiated as live agents in the Hive Mind.  Templates are
    stored as JSON files in ``.cvc/agent_templates/``.
    """
    id: str = Field(default_factory=lambda: f"agent-{uuid.uuid4().hex[:8]}")
    name: str = "Custom Agent"
    description: str = ""
    system_prompt: str = ""
    # Tool access
    tools_allow: list[str] = Field(default_factory=list)
    tools_deny: list[str] = Field(default_factory=list)
    tool_tier: str = "coding"  # "read_only" | "coding" | "research" | "orchestration"
    # LLM configuration (overrides, empty = inherit default)
    model_override: str = ""
    provider_override: str = ""
    # Execution limits
    max_turns: int = 20
    # Hive Mind placement
    rank: str = "specialist"
    squad: str = ""
    # Capabilities & skills
    capabilities: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    # Behavior
    auto_respond: bool = False
    auto_share_to_hive: bool = True
    # Metadata
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    created_by: str = "user"
    is_builtin: bool = False


class HiveMemoryEntry(BaseModel):
    """
    A single entry in the Hive Mind shared memory.

    Hive Memory is the shared cognitive space where agents contribute
    findings, decisions, tasks, and alerts.  Agents never communicate
    directly — they read/write to this shared memory.
    """
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    agent_id: str = ""
    content: str = ""
    category: str = "general"  # "decisions" | "findings" | "tasks" | "alerts" | "general"
    tags: list[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)
    commit_hash: str = ""  # Link to the CVC commit backing this entry
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Settings Schema — JSON Schema for dynamic form rendering
# ---------------------------------------------------------------------------

SETTINGS_SCHEMA: dict[str, Any] = {
    "sections": [
        {
            "id": "provider",
            "title": "Provider & Model",
            "icon": "🤖",
            "fields": [
                {
                    "key": "provider", "type": "select", "label": "LLM Provider",
                    "options": ["anthropic", "openai", "google", "ollama", "lmstudio"],
                    "level": "global",
                },
                {
                    "key": "model", "type": "model_select", "label": "Model",
                    "depends_on": "provider", "level": "global",
                },
                {
                    "key": "custom_model", "type": "text", "label": "Custom Model Name",
                    "placeholder": "e.g. my-fine-tuned-model", "level": "global",
                },
                {
                    "key": "api_key", "type": "password", "label": "API Key",
                    "placeholder": "Enter API key for selected provider", "level": "global",
                },
                {
                    "key": "base_url_override", "type": "text",
                    "label": "Base URL Override",
                    "placeholder": "https://api.example.com",
                    "level": "global",
                },
                {
                    "key": "ollama_host", "type": "text", "label": "Ollama Host",
                    "placeholder": "http://localhost:11434", "level": "global",
                    "visible_when": {"provider": "ollama"},
                },
                {
                    "key": "lmstudio_host", "type": "text", "label": "LM Studio Host",
                    "placeholder": "http://localhost:1234", "level": "global",
                    "visible_when": {"provider": "lmstudio"},
                },
            ],
        },
        {
            "id": "agent",
            "title": "Agent Identity & Behavior",
            "icon": "🧠",
            "fields": [
                {
                    "key": "agent_id", "type": "text", "label": "Agent ID",
                    "placeholder": "sofia", "level": "global",
                },
                {
                    "key": "default_branch", "type": "text",
                    "label": "Default Branch", "placeholder": "main", "level": "project",
                },
                {
                    "key": "trust_mode", "type": "radio", "label": "Trust Mode",
                    "options": [
                        {"value": "strict", "label": "Strict", "desc": "Ask permission for everything"},
                        {"value": "smart", "label": "Smart", "desc": "Auto-approve safe tools, ask for writes"},
                        {"value": "yolo", "label": "YOLO", "desc": "Approve everything automatically"},
                    ],
                    "level": "local",
                },
                {
                    "key": "plan_display", "type": "radio", "label": "Plan Display Mode",
                    "options": [
                        {"value": "plan-approve", "label": "Approve", "desc": "Show plan and wait for approval"},
                        {"value": "plan-auto", "label": "Auto", "desc": "Show plan and auto-execute"},
                        {"value": "plan-quiet", "label": "Quiet", "desc": "Execute without showing plan"},
                    ],
                    "level": "local",
                },
                {
                    "key": "auto_memory_enabled", "type": "toggle", "label": "Auto Memory",
                    "description": "Automatically save conversation memory between sessions",
                    "level": "local",
                },
                {
                    "key": "always_thinking_enabled", "type": "toggle",
                    "label": "Always Thinking",
                    "description": "Force model reasoning/thinking phase on every turn",
                    "level": "local",
                },
                {
                    "key": "thinking_level", "type": "select", "label": "Thinking Level",
                    "options": ["off", "minimal", "low", "medium", "high", "adaptive"],
                    "description": "Control depth of model reasoning",
                    "level": "local",
                },
                {
                    "key": "output_style", "type": "select", "label": "Output Style",
                    "options": ["default", "explanatory", "learning", "concise", "verbose"],
                    "description": "How the agent formats responses",
                    "level": "local",
                },
                {
                    "key": "fast_mode", "type": "toggle", "label": "Fast Mode",
                    "description": "Use cheapest model for sub-agents",
                    "level": "local",
                },
                {
                    "key": "max_iterations", "type": "number",
                    "label": "Max Agent Iterations",
                    "description": "How many tool-use turns the main agent can run before it must produce a final reply. Upstream default 90 (commonly raised to 180+). Set 0 to use CVC default (80).",
                    "placeholder": "0 (default 80) — try 120-180 for long audits",
                    "level": "global",
                },
                {
                    "key": "max_iterations_expensive", "type": "number",
                    "label": "Max Iterations (Expensive Models)",
                    "description": "Iteration cap when running Opus or other expensive models. Set 0 to use CVC default (40).",
                    "placeholder": "0 (default 40) — try 60-80 for deep audits",
                    "level": "global",
                },
                {
                    "key": "agent_timeout", "type": "number",
                    "label": "Agent Turn Timeout (seconds)",
                    "description": "Total budget per chat turn across all iterations + tools. Set 0 to use CVC default (900s / 15 min).",
                    "placeholder": "0 (default 900) — e.g. 1800 for 30 min",
                    "level": "global",
                },
                {
                    "key": "tool_timeout", "type": "number",
                    "label": "Per-Tool Timeout (seconds)",
                    "description": "Hard timeout on any single tool call. Set 0 to use CVC default (300s / 5 min).",
                    "placeholder": "0 (default 300)",
                    "level": "global",
                },
            ],
        },
        {
            "id": "permissions",
            "title": "Permissions & Security",
            "icon": "🔒",
            "fields": [
                {
                    "key": "permissions.allow", "type": "tag_list",
                    "label": "Allow Rules",
                    "description": "Tool patterns that are automatically approved",
                    "placeholder": "e.g. Bash(npm run *), Read", "level": "project",
                },
                {
                    "key": "permissions.deny", "type": "tag_list",
                    "label": "Deny Rules",
                    "description": "Tool patterns that are always blocked",
                    "placeholder": "e.g. Bash(rm -rf *)", "level": "project",
                },
                {
                    "key": "permissions.ask", "type": "tag_list",
                    "label": "Ask Rules",
                    "description": "Tool patterns that require user confirmation",
                    "placeholder": "e.g. Edit, WebFetch", "level": "project",
                },
                {
                    "key": "trusted_commands", "type": "tag_list",
                    "label": "Trusted Commands",
                    "description": "Shell commands auto-approved without asking",
                    "level": "local",
                },
                {
                    "key": "blocked_commands", "type": "tag_list",
                    "label": "Blocked Commands",
                    "description": "Shell commands always rejected",
                    "level": "local",
                },
                {
                    "key": "sandbox_enabled", "type": "toggle", "label": "Sandbox Mode",
                    "description": "Run tools in isolated sandbox environment",
                    "level": "local",
                },
            ],
        },
        {
            "id": "hooks",
            "title": "Hooks & Lifecycle",
            "icon": "🪝",
            "fields": [
                {
                    "key": "hooks", "type": "hook_editor",
                    "label": "Hooks",
                    "description": "Lifecycle event handlers (PreToolUse, PostToolUse, SessionStart, etc.)",
                    "hook_events": [
                        "PreToolUse", "PostToolUse", "SessionStart", "SessionEnd",
                        "Stop", "UserPromptSubmit", "PreCompact",
                        "CwdChanged", "FileChanged", "TaskCreated",
                        "Notification", "SubagentStop",
                    ],
                    "level": "project",
                },
            ],
        },
        {
            "id": "env",
            "title": "Environment Variables",
            "icon": "🌐",
            "fields": [
                {
                    "key": "env", "type": "key_value",
                    "label": "Environment Variables",
                    "description": "Key-value pairs injected into agent sessions",
                    "level": "project",
                },
            ],
        },
        {
            "id": "plugins",
            "title": "Plugins & Extensions",
            "icon": "🧩",
            "fields": [
                {
                    "key": "enabled_plugins", "type": "plugin_toggles",
                    "label": "Enabled Plugins",
                    "description": "Toggle plugins on/off",
                    "level": "project",
                },
            ],
        },
        {
            "id": "network",
            "title": "Proxy & Network",
            "icon": "📡",
            "fields": [
                {
                    "key": "proxy_host", "type": "text", "label": "Proxy Host",
                    "placeholder": "127.0.0.1", "level": "global",
                },
                {
                    "key": "proxy_port", "type": "number", "label": "Proxy Port",
                    "placeholder": "19333", "level": "global",
                },
                {
                    "key": "gateway_host", "type": "text", "label": "Gateway Host",
                    "placeholder": "127.0.0.1", "level": "global",
                },
                {
                    "key": "gateway_port", "type": "number", "label": "Gateway Port",
                    "placeholder": "13421", "level": "global",
                },
                {
                    "key": "mcp_host", "type": "text", "label": "MCP Server Host",
                    "placeholder": "127.0.0.1", "level": "global",
                },
                {
                    "key": "mcp_port", "type": "number", "label": "MCP Server Port",
                    "placeholder": "8001", "level": "global",
                },
            ],
        },
        {
            "id": "context",
            "title": "Context & Memory",
            "icon": "💾",
            "fields": [
                {
                    "key": "auto_compact_threshold", "type": "slider",
                    "label": "Auto-Compact Threshold",
                    "description": "Compress context when % of window is full",
                    "min": 50, "max": 100, "step": 5, "level": "local",
                },
                {
                    "key": "context_pruning", "type": "select",
                    "label": "Context Pruning Strategy",
                    "options": ["cache-ttl", "soft-trim", "hard-clear", "none"],
                    "description": "How to manage context when it exceeds limits",
                    "level": "local",
                },
                {
                    "key": "anchor_interval", "type": "number",
                    "label": "Anchor Interval",
                    "description": "Full snapshot every N commits",
                    "placeholder": "10", "level": "project",
                },
                {
                    "key": "compaction_keep", "type": "number",
                    "label": "Compaction Keep Count",
                    "description": "Number of recent commits to keep during compaction",
                    "placeholder": "5", "level": "local",
                },
                {
                    "key": "compaction_ratio", "type": "slider",
                    "label": "Target Compression Ratio",
                    "min": 0.1, "max": 0.9, "step": 0.1, "level": "local",
                },
                {
                    "key": "session_reset_policy", "type": "select",
                    "label": "Session Reset Policy",
                    "options": ["manual", "daily", "idle-30m", "idle-1h", "idle-4h"],
                    "description": "When to automatically reset session context",
                    "level": "local",
                },
            ],
        },
        {
            "id": "advanced",
            "title": "Advanced / Developer",
            "icon": "⚙️",
            "fields": [
                {
                    "key": "debug_logging", "type": "toggle",
                    "label": "Debug Logging",
                    "description": "Enable verbose debug output",
                    "level": "local",
                },
                {
                    "key": "time_machine", "type": "toggle",
                    "label": "Time Machine",
                    "description": "Auto-commit on every tool execution",
                    "level": "local",
                },
                {
                    "key": "human_delay_ms", "type": "number",
                    "label": "Human Delay (ms)",
                    "description": "Simulate natural typing delay between responses",
                    "placeholder": "0", "level": "local",
                },
                {
                    "key": "stream_coalescing", "type": "select",
                    "label": "Stream Coalescing",
                    "options": ["paragraph", "newline", "sentence", "none"],
                    "description": "How streaming output is batched before display",
                    "level": "local",
                },
                {
                    "key": "max_agent_turns", "type": "number",
                    "label": "Max Agent Turns",
                    "description": "Maximum tool-use iterations per agent turn",
                    "placeholder": "50", "level": "local",
                },
            ],
        },
    ],
}
