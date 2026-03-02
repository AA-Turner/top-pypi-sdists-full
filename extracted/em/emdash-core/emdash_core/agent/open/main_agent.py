"""Open Agent - Self-evolving personal assistant with OpenClaw-style memory.

This module provides the OpenAgent, a minimal, self-evolving, user-driven
personal assistant that writes itself based on user needs rather than
having heavy predefined opinions.

Features:
- Long-term Memory: MEMORY.md (curated, durable facts)
- Short-term Memory: Daily markdown logs (rolling working memory)
- Pre-compaction memory flush (OpenClaw-style)
- Full-text search via SQLite FTS5 index or QMD backend
- User identity stored in .emdash/rules/USER.md
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING, Union
from pathlib import Path

from ..base import BaseAgent
from ..compaction_strategy import LLMSummaryStrategy
from ..events import AgentEventEmitter
from ..providers.factory import DEFAULT_MODEL
from .toolkit import OpenToolkit
from .capabilities import CapabilityRegistry
from .prompts import OPEN_BOOTSTRAP_PROMPT, build_open_system_prompt
from .memory import HierarchicalMemory
from .memory_tools import MemoryToolSet
from .memory_store import MemoryStore
from .memory_index import MemoryIndex
from .memory_qmd import QmdIndex, QmdConfig

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default scaffolding templates — created on first run if missing
# ---------------------------------------------------------------------------

_DEFAULT_RULES_DIR = Path(__file__).parent / "defaults"

_SCAFFOLDING_FILENAMES: tuple[str, ...] = (
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "BOOTSTRAP.md",
)

_BASE_RULE_FILENAMES: tuple[str, ...] = (
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
)


def _load_default_scaffolding_files() -> dict[str, str]:
    """Load bundled default scaffolding templates from markdown files."""
    templates: dict[str, str] = {}
    for filename in _SCAFFOLDING_FILENAMES:
        template_path = _DEFAULT_RULES_DIR / filename
        try:
            templates[filename] = template_path.read_text(encoding="utf-8")
        except OSError:
            logger.warning("Default scaffolding template missing: %s", template_path)
    return templates


class OpenAgent(BaseAgent):
    """Self-evolving personal assistant with OpenClaw-style memory.

    Memory model (OpenClaw):
    - Markdown files on disk are the source of truth
    - MEMORY.md — long-term curated facts and preferences
    - memory/YYYY-MM-DD.md — daily rolling logs (short-term)
    - SQLite FTS5 index for search
    - Pre-compaction flush to prevent memory loss

    Key characteristics:
    - Minimal bootstrap prompt (<100 tokens base)
    - Learns user preferences over time
    - Discovers and adds capabilities dynamically
    - User-driven evolution (not opinionated)
    - Self-modifying through learning tools
    """

    # Agent identity
    name = "Open Assistant"
    agent_type = "open"
    description = "A minimal, self-evolving personal assistant that learns from you"

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = 100,
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
        repo_root: Optional[Path] = None,
        capability_registry: Optional[CapabilityRegistry] = None,
        hierarchical_memory: Optional[HierarchicalMemory] = None,
    ):
        """Initialize the Open Agent.

        Args:
            model: LLM model to use
            emitter: Event emitter for streaming output
            max_iterations: Maximum tool iterations per run
            verbose: Enable verbose logging
            enable_thinking: Enable extended thinking
            session_id: Session ID for isolation
            repo_root: Repository root path
            capability_registry: Optional pre-configured CapabilityRegistry
            hierarchical_memory: Optional pre-configured HierarchicalMemory
        """
        # Store fields before calling super() since _get_toolkit() needs them
        self._session_id = session_id
        self._capability_registry = capability_registry
        self._hierarchical_memory = hierarchical_memory
        self._repo_root = repo_root or Path.cwd()
        self._memory_tools: Optional[MemoryToolSet] = None

        # OpenClaw memory system — initialised in _get_toolkit()
        self._memory_store: Optional[MemoryStore] = None
        self._memory_index: Optional[Union[MemoryIndex, QmdIndex]] = None

        # Call parent init (which calls _get_toolkit())
        super().__init__(
            model=model,
            emitter=emitter,
            max_iterations=max_iterations,
            verbose=verbose,
            enable_thinking=enable_thinking,
            session_id=session_id,
        )

        # Wire pre-compaction memory flush into the compaction strategy.
        # When context approaches the compaction threshold, the strategy
        # calls our hook to persist important facts before summarisation
        # destroys message detail (OpenClaw-style memory flush).
        if isinstance(self._compaction_strategy, LLMSummaryStrategy):
            self._compaction_strategy.set_pre_compact_hook(
                self._flush_memory_before_compaction
            )

    def _get_toolkit(self) -> "BaseToolkit":
        """Return the Open Toolkit with learning and memory capabilities."""
        # Initialize managers if not provided
        if self._capability_registry is None:
            self._capability_registry = CapabilityRegistry(
                emdash_dir=self._repo_root / ".emdash",
            )

        if self._hierarchical_memory is None:
            self._hierarchical_memory = HierarchicalMemory(
                session_id=self._session_id or "default",
                emdash_dir=self._repo_root / ".emdash",
            )

        # Create legacy memory tools wrapper (backward compat)
        self._memory_tools = MemoryToolSet(self._hierarchical_memory)

        # ----- OpenClaw memory system -----
        workspace = self._repo_root / ".emdash"
        self._memory_store = MemoryStore(workspace_dir=workspace)

        # Select index backend from config
        sqlite_index = MemoryIndex(
            db_path=workspace / "memory" / "index.sqlite",
            workspace_dir=workspace,
        )

        try:
            from ...core.config import get_config
            memory_cfg = get_config().memory
        except Exception:
            memory_cfg = None

        # Apply config-driven bootstrap limits (OpenClaw defaults)
        if memory_cfg:
            self.BOOTSTRAP_MAX_CHARS = memory_cfg.bootstrap_max_chars
            self.BOOTSTRAP_TOTAL_MAX_CHARS = memory_cfg.bootstrap_total_max_chars

        if memory_cfg and memory_cfg.backend == "qmd":
            qmd_config = QmdConfig(
                max_results=memory_cfg.max_results,
                timeout_ms=memory_cfg.timeout_ms,
                max_snippet_chars=memory_cfg.qmd_max_snippet_chars,
                embedding_model=memory_cfg.qmd_embedding_model,
                vector_weight=memory_cfg.qmd_vector_weight,
            )
            self._memory_index = QmdIndex(
                bm25=sqlite_index,
                workspace_dir=workspace,
                config=qmd_config,
            )
            logger.info("Memory backend: QMD hybrid (BM25 + vector)")
        else:
            self._memory_index = sqlite_index
            logger.info("Memory backend: SQLite FTS5")

        # Initial index sync (fast — only indexes what's on disk)
        try:
            self._memory_index.sync_now("boot")
        except Exception as exc:
            logger.warning("Memory index boot sync failed: %s", exc)

        # Ensure scaffolding files exist for first-run users
        self._ensure_default_scaffolding()

        # Create toolkit with all capabilities
        return OpenToolkit(
            repo_root=self._repo_root,
            capability_registry=self._capability_registry,
            hierarchical_memory=self._hierarchical_memory,
            memory_tools=self._memory_tools,
            memory_store=self._memory_store,
            memory_index=self._memory_index,
        )

    def _ensure_default_scaffolding(self) -> None:
        """Create default SOUL/IDENTITY/USER/BOOTSTRAP files if they don't exist.

        Non-destructive: existing files are never overwritten.
        Also migrates files found at the repo root into .emdash/rules/.
        """
        scaffolding_files = _load_default_scaffolding_files()
        rules_dir = self._repo_root / ".emdash" / "rules"
        try:
            rules_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            logger.debug("Could not create rules directory: %s", rules_dir)
            return

        for filename in _SCAFFOLDING_FILENAMES:
            dest = rules_dir / filename
            if dest.exists():
                continue

            # Migrate from repo root if the file exists there
            root_file = self._repo_root / filename
            if root_file.exists():
                try:
                    dest.write_text(root_file.read_text(encoding="utf-8"), encoding="utf-8")
                    root_file.unlink()
                    logger.info("Migrated %s from repo root to %s", filename, dest)
                    continue
                except OSError:
                    logger.debug("Could not migrate %s", root_file)

            # Otherwise create the default template
            content = scaffolding_files.get(filename)
            if content is None:
                logger.debug("No bundled default scaffolding template for %s", filename)
                continue
            try:
                dest.write_text(content, encoding="utf-8")
                logger.info("Created default scaffolding file: %s", dest)
            except OSError:
                logger.debug("Could not write scaffolding file: %s", dest)

    # ------------------------------------------------------------------
    # System prompt with OpenClaw memory injection
    # ------------------------------------------------------------------

    # OpenClaw bootstrap file limits
    BOOTSTRAP_MAX_CHARS = 20_000       # Per-file truncation (OpenClaw default)
    BOOTSTRAP_TOTAL_MAX_CHARS = 150_000  # Total across all bootstrap files

    def _build_system_prompt(self) -> str:
        """Build a dynamic system prompt with OpenClaw memory injection.

        Matches OpenClaw's system prompt assembly:

        1. Rule/bootstrap files (SOUL.md, USER.md, IDENTITY.md, BOOTSTRAP.md)
           — prepended under "Project Context", truncated per-file and total
        2. Base prompt (bootstrap or onboarding)
        3. MEMORY.md (long-term curated memory) — if present
        4. Capabilities, tools, guidance sections
        5. Environment section

        Daily logs are **not** injected — they are accessed on-demand
        via ``memory_search`` / ``memory_get`` tools.
        """
        # Ensure toolkit is created
        if not hasattr(self, 'toolkit') or self.toolkit is None:
            return OPEN_BOOTSTRAP_PROMPT

        # Resolve USER.md path for onboarding detection
        user_md_path = None
        for base in [self._repo_root / ".emdash" / "rules", Path.home() / ".emdash" / "rules"]:
            candidate = base / "USER.md"
            if candidate.exists():
                user_md_path = candidate
                break

        prompt = build_open_system_prompt(
            capability_registry=self._capability_registry,
            hierarchical_memory=self._hierarchical_memory,
            toolkit=self.toolkit,
            user_md_path=user_md_path,
            memory_store=self._memory_store,
        )

        # Load bootstrap/persona files: project-level first, user-level fallback.
        # Matches OpenClaw: files are trimmed and prepended under "Project Context"
        # so the model sees identity and profile context without explicit reads.
        # Per-file limit: BOOTSTRAP_MAX_CHARS (default 20,000)
        # Total limit:    BOOTSTRAP_TOTAL_MAX_CHARS (default 150,000)
        total_injected = 0
        for filename in self._get_rule_files_for_prompt():
            content = ""
            for base in [self._repo_root / ".emdash" / "rules", Path.home() / ".emdash" / "rules"]:
                path = base / filename
                if path.exists():
                    try:
                        content = path.read_text().strip()
                        if content:
                            logger.info("Loaded rules file: %s", path)
                            break
                    except Exception:
                        logger.debug("Failed to read rules file: %s", path)

            if not content:
                logger.debug("Rules file not found or empty: %s", filename)
                continue

            # Per-file truncation (OpenClaw: bootstrapMaxChars)
            if len(content) > self.BOOTSTRAP_MAX_CHARS:
                content = content[:self.BOOTSTRAP_MAX_CHARS] + "\n\n... (truncated)"
                logger.info("Truncated %s to %d chars", filename, self.BOOTSTRAP_MAX_CHARS)

            # Total budget check (OpenClaw: bootstrapTotalMaxChars)
            if total_injected + len(content) > self.BOOTSTRAP_TOTAL_MAX_CHARS:
                logger.warning(
                    "Bootstrap total limit reached (%d chars), skipping %s",
                    self.BOOTSTRAP_TOTAL_MAX_CHARS, filename,
                )
                break

            # Annotate so the agent knows which file this content came from
            annotated = f"<!-- source: .emdash/rules/{filename} -->\n{content}"
            prompt = annotated + "\n\n" + prompt
            total_injected += len(content)

        # Append runtime environment context (remote machine + active channel)
        prompt += "\n\n" + self._build_environment_section()

        return prompt

    def _should_include_bootstrap_rule(self) -> bool:
        """Return whether BOOTSTRAP.md should be included in prompt assembly.

        BOOTSTRAP.md is first-run guidance only. Keep it scoped to the
        very first interaction before USER.md has been filled in.
        """
        return not self._user_md_has_content()

    def _user_md_has_content(self) -> bool:
        """Check if USER.md has been filled in beyond the template."""
        for base in [self._repo_root / ".emdash" / "rules", Path.home() / ".emdash" / "rules"]:
            path = base / "USER.md"
            if path.exists():
                try:
                    content = path.read_text()
                    # Check if the Name field has been filled in
                    for line in content.splitlines():
                        if line.startswith("- **Name:**") and line.strip() != "- **Name:**":
                            return True
                except Exception:
                    pass
        return False

    def _get_rule_files_for_prompt(self) -> tuple[str, ...]:
        """Select rule files to prepend to the system prompt."""
        if self._should_include_bootstrap_rule():
            return _BASE_RULE_FILENAMES + ("BOOTSTRAP.md",)
        return _BASE_RULE_FILENAMES

    def _build_environment_section(self) -> str:
        """Build a section describing the runtime environment.

        Tells the agent it lives on a remote machine and how the user
        is interacting (via which channel).
        """
        try:
            from ...channels.router import get_channel_router
            router = get_channel_router()
            if router and router.primary:
                channel_name = router.primary.name
            else:
                channel_name = "CLI"
        except Exception:
            channel_name = "CLI"

        return (
            "## Environment\n\n"
            "IMPORTANT: You live on a remote machine, NOT on the user's local computer. "
            "You have full access to this machine's terminal, filesystem, and network. "
            f"The user is interacting with you via **{channel_name}**. "
            "Keep this in mind when referencing files, paths, or system resources — "
            "everything you see and do happens on the remote machine."
        )

    def _get_available_subagents(self) -> dict[str, str]:
        """Return available sub-agent types."""
        return {
            "explore": "Read-only exploration of codebase",
            "plan": "Deep analysis and architecture planning",
            "research": "Web research and information gathering",
            "coder": "Code implementation (when file changes needed)",
        }

    # ------------------------------------------------------------------
    # Pre-run and post-run hooks
    # ------------------------------------------------------------------

    def _pre_run(self, query: str, **kwargs) -> None:
        """Hook called before running the agent.

        Adds memory-enhanced context:
        - Capability detection
        - Channel message ingestion
        - Daily log entry for current interaction
        """
        # Check for pending channel messages
        try:
            from ...channels.stored import StoredChannel
            stored = StoredChannel(self._repo_root / ".emdash")
            pending = stored.get_and_clear()
            if pending and self._memory_store:
                self._memory_store.append_daily(
                    f"Pending channel notifications:\n{pending}",
                    heading="Channel notifications",
                )
                self._memory_index.mark_dirty(
                    f"memory/{datetime.now().strftime('%Y-%m-%d')}.md"
                )
        except Exception:
            pass  # Channel system not available

        # Record this interaction in today's daily log
        if self._memory_store:
            self._memory_store.append_daily(
                f"User query: {query[:500]}",
                heading="Session interaction",
            )
            self._memory_index.mark_dirty(
                f"memory/{datetime.now().strftime('%Y-%m-%d')}.md"
            )

        # Check for capability matches
        if self._capability_registry:
            matching_caps = self._capability_registry.find_matching(query)
            if matching_caps:
                self._capability_registry.record_usage(matching_caps[0].name)

        # Rebuild system prompt with current memory context
        self.system_prompt = self._build_system_prompt()

    def run(self, query: str, **kwargs):
        """Run the agent with memory-enhanced context.

        Overrides parent to add pre-run memory setup.
        """
        # Set up memory context before running
        self._pre_run(query, **kwargs)

        # Run parent implementation synchronously
        return super().run(query, **kwargs)

    def _on_run_complete(self, response: str) -> None:
        """Hook called when a run completes successfully."""
        super()._on_run_complete(response)

    # ------------------------------------------------------------------
    # Pre-compaction memory flush (OpenClaw-style)
    # ------------------------------------------------------------------

    def _flush_memory_before_compaction(
        self,
        messages: list[dict],
        emitter: Optional[AgentEventEmitter] = None,
    ) -> None:
        """Persist important facts before compaction destroys message detail.

        Called by :class:`LLMSummaryStrategy` at the soft threshold (before
        the hard compaction threshold). Uses the LLM to extract key facts
        from the conversation and writes them to the daily markdown log
        via :class:`MemoryStore`. Also writes durable facts to MEMORY.md.

        Implements the OpenClaw pre-compaction memory flush mechanism.
        """
        if not self._memory_store:
            return

        if emitter:
            emitter.emit_thinking("Saving important context before compaction...")

        # Build a lightweight summary of messages for the extraction prompt.
        # Skip the first message (original query) and recent messages (they
        # survive compaction) — focus on the "middle" that will be lost.
        KEEP_RECENT = 6
        if len(messages) <= KEEP_RECENT + 2:
            return  # Too few messages to worry about

        middle_msgs = messages[1:-KEEP_RECENT]
        if not middle_msgs:
            return

        conversation_text = self._format_messages_for_flush(middle_msgs)

        # Ask the LLM to extract durable facts
        prompt = (
            "You are a memory extraction specialist. The conversation below "
            "is about to be compressed and most detail will be lost.\n\n"
            "Produce TWO sections:\n\n"
            "## Daily (working context)\n"
            "Ongoing tasks, recent decisions, things in progress.\n\n"
            "## Durable (long-term facts)\n"
            "User preferences, stable decisions, project facts, "
            "anything the user explicitly asked to remember.\n\n"
            "Use concise Markdown bullet points. "
            "If a section has nothing, write NOTHING_TO_SAVE.\n\n"
            "---\n\n"
            f"{conversation_text}"
        )

        try:
            from ..providers import get_provider
            from ..providers.factory import _get_default_model_name

            model_name = _get_default_model_name()
            provider = get_provider(model_name)

            response = provider.chat(
                messages=[{"role": "user", "content": prompt}],
                system="Extract durable memories. Be concise — bullet points only.",
            )

            extracted = (response.content or "").strip()

            if not extracted or extracted == "NOTHING_TO_SAVE":
                logger.debug("Memory flush: nothing worth saving")
                return

            # Parse sections
            daily_section, durable_section = self._parse_flush_sections(extracted)

            # 1. Write daily context to today's log
            if daily_section:
                log_path = self._memory_store.append_daily(
                    daily_section,
                    heading="Pre-compaction memory flush",
                )
                today = datetime.now().strftime("%Y-%m-%d")
                self._memory_index.mark_dirty(f"memory/{today}.md")
                logger.info("Memory flush: wrote daily context to %s", log_path)

            # 2. Write durable facts to MEMORY.md
            if durable_section:
                self._memory_store.append_long_term(
                    durable_section,
                    heading="Pre-compaction memory flush",
                )
                self._memory_index.mark_dirty("MEMORY.md")
                logger.info("Memory flush: wrote durable facts to MEMORY.md")

            if emitter:
                emitter.emit_thinking("Memory flush complete — important context saved.")

        except Exception as exc:
            logger.warning("Memory flush failed (non-fatal): %s", exc)

    @staticmethod
    def _parse_flush_sections(text: str) -> tuple[str, str]:
        """Parse the LLM flush output into daily and durable sections.

        Returns:
            Tuple of (daily_text, durable_text). Either may be empty.
        """
        daily = ""
        durable = ""

        current_section = ""
        current_lines: list[str] = []

        for line in text.splitlines():
            stripped = line.strip().lower()
            if stripped.startswith("## daily") or stripped.startswith("## working"):
                if current_section == "durable" and current_lines:
                    durable = "\n".join(current_lines).strip()
                current_section = "daily"
                current_lines = []
            elif stripped.startswith("## durable") or stripped.startswith("## long"):
                if current_section == "daily" and current_lines:
                    daily = "\n".join(current_lines).strip()
                current_section = "durable"
                current_lines = []
            else:
                if "NOTHING_TO_SAVE" not in line:
                    current_lines.append(line)

        # Flush remaining
        if current_section == "daily" and current_lines:
            daily = "\n".join(current_lines).strip()
        elif current_section == "durable" and current_lines:
            durable = "\n".join(current_lines).strip()
        elif not current_section and current_lines:
            # No sections found — treat everything as daily
            daily = "\n".join(current_lines).strip()

        return daily, durable

    @staticmethod
    def _format_messages_for_flush(messages: list[dict], max_chars: int = 12000) -> str:
        """Format messages into a compact text block for the flush LLM call."""
        parts: list[str] = []
        total = 0
        for msg in messages:
            role = msg.get("role", "?")
            content = msg.get("content", "")
            if isinstance(content, list):
                content = " ".join(
                    p.get("text", "") for p in content if isinstance(p, dict)
                )
            # Truncate individual messages
            if len(content) > 2000:
                content = content[:2000] + "…"
            part = f"[{role.upper()}] {content}"
            if total + len(part) > max_chars:
                parts.append("[...truncated...]")
                break
            parts.append(part)
            total += len(part)
        return "\n\n".join(parts)

    # ------------------------------------------------------------------
    # Public memory interface (backward-compatible)
    # ------------------------------------------------------------------

    def remember(
        self,
        content: str,
        layer: str = "long_term",
        importance: float = 0.5,
        context: str = "general",
        tags: Optional[list] = None,
    ) -> dict:
        """Store something in memory.

        Args:
            content: Information to remember
            layer: Which layer ("long_term", "short_term")
            importance: Importance score (0.0-1.0)
            context: Category
            tags: Optional tags

        Returns:
            Result dict
        """
        # Use OpenClaw MemoryStore if available
        if self._memory_store:
            if layer == "long_term":
                self._memory_store.append_long_term(content)
                self._memory_index.mark_dirty("MEMORY.md")
                return {"success": True, "location": "MEMORY.md"}
            else:
                path = self._memory_store.append_daily(content)
                rel = str(path.relative_to(self._memory_store.workspace_dir))
                self._memory_index.mark_dirty(rel)
                return {"success": True, "location": rel}

        # Fallback to legacy system
        if self._memory_tools:
            return self._memory_tools.remember(
                content=content,
                layer=layer,
                importance=importance,
                context=context,
                tags=tags,
            )
        return {"success": False, "error": "Memory not initialized"}

    def recall(
        self,
        query: str,
        layers: Optional[list] = None,
        context: Optional[str] = None,
        top_k: int = 5,
    ) -> dict:
        """Search memory.

        Args:
            query: Search query
            layers: Which layers to search
            context: Filter by context
            top_k: Max results

        Returns:
            Matching memories
        """
        # Use OpenClaw MemoryIndex if available
        if self._memory_index:
            from dataclasses import asdict
            hits = self._memory_index.search(query, limit=top_k)
            return {
                "success": True,
                "results": [asdict(h) for h in hits],
                "count": len(hits),
            }

        # Fallback to legacy system
        if self._memory_tools:
            return self._memory_tools.recall(
                query=query,
                layers=layers,
                context=context,
                top_k=top_k,
            )
        return {"success": False, "error": "Memory not initialized"}

    def show_memory_stats(self) -> dict:
        """Get memory statistics."""
        stats: dict = {}
        if self._memory_store:
            stats["daily_logs"] = self._memory_store.list_daily_logs()[:5]
            stats["has_memory_md"] = self._memory_store.memory_md_path.exists()
        if self._memory_tools:
            stats.update(self._memory_tools.get_memory_stats())
        return stats if stats else {"success": False, "error": "Memory not initialized"}

    def export_memory(self) -> dict:
        """Export all memory layers."""
        if self._hierarchical_memory:
            return {
                "success": True,
                "memory": self._hierarchical_memory.export_all(),
            }
        return {"success": False, "error": "Memory not initialized"}

    def reset(self) -> None:
        """Reset capabilities and memory to initial state."""
        if self._capability_registry:
            self._capability_registry.reset()
        if self._hierarchical_memory:
            self._hierarchical_memory.reset()

        self.system_prompt = self._build_system_prompt()

    # Capabilities Interface

    def list_capabilities(self) -> list:
        """List all learned capabilities."""
        caps = []
        if self._capability_registry:
            caps.extend([
                {
                    "name": c.name,
                    "description": c.description,
                    "usage_count": c.usage_count,
                    "enabled": c.enabled,
                    "type": "capability",
                }
                for c in self._capability_registry.list_all()
            ])
        return caps

    def suggest_capability(self, message: str) -> Optional[dict]:
        """Suggest creating a new capability based on message."""
        if self._capability_registry:
            history = []
            return self._capability_registry.suggest_new(message, history)
        return None
