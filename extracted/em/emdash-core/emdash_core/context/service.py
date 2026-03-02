"""Context service - facade over providers and session management."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from .models import ContextItem
from .reranker import rerank_context_items
from .registry import ContextProviderRegistry
from .session import SessionContextManager
from ..graph.connection import KuzuConnection, get_connection
from ..utils.logger import log


class ContextService:
    """High-level service for managing session context.

    Provides a unified interface for:
    - Detecting modified files (via git diff)
    - Extracting context from providers
    - Managing session persistence
    - Formatting context for LLM prompts
    """

    def __init__(self, connection: Optional[KuzuConnection] = None, repo_root: Optional[str] = None):
        """Initialize context service.

        Args:
            connection: Kuzu database connection (uses global if not provided)
            repo_root: Repository root path for git operations
        """
        self.connection = connection or get_connection()
        self.repo_root = repo_root or os.getcwd()
        self.session_manager = SessionContextManager(self.connection)
        self._providers: Optional[list[str]] = None
        self._min_score = float(os.getenv("CONTEXT_MIN_SCORE", "0.5"))
        self._max_items = int(os.getenv("CONTEXT_MAX_ITEMS", "50"))

    @property
    def providers(self) -> list[str]:
        """Get list of enabled provider names from config."""
        if self._providers is None:
            env_val = os.getenv("CONTEXT_PROVIDERS", "touched_areas,explored_areas")
            self._providers = [p.strip() for p in env_val.split(",") if p.strip()]
        return self._providers

    def detect_modified_files(self) -> list[str]:
        """Detect files modified since last commit.

        Uses git diff to find modified files.

        Returns:
            List of modified file paths (absolute)
        """
        try:
            # Get unstaged changes
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=10,
            )

            files = []
            if result.returncode == 0 and result.stdout.strip():
                files.extend(result.stdout.strip().split("\n"))

            # Also get staged changes
            result_staged = subprocess.run(
                ["git", "diff", "--name-only", "--cached"],
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=10,
            )

            if result_staged.returncode == 0 and result_staged.stdout.strip():
                files.extend(result_staged.stdout.strip().split("\n"))

            # Convert to absolute paths and deduplicate
            abs_files = []
            seen = set()
            for f in files:
                if f and f not in seen:
                    seen.add(f)
                    abs_path = os.path.join(self.repo_root, f)
                    if os.path.exists(abs_path):
                        abs_files.append(abs_path)

            return abs_files

        except subprocess.TimeoutExpired:
            log.warning("Git diff timed out")
            return []
        except FileNotFoundError:
            log.warning("Git not found")
            return []
        except Exception as e:
            log.warning(f"Failed to detect modified files: {e}")
            return []

    def update_context(
        self,
        terminal_id: str,
        modified_files: Optional[list[str]] = None,
        exploration_steps: Optional[list] = None,
    ):
        """Update session context after changes.

        Args:
            terminal_id: Terminal session identifier
            modified_files: List of modified files (auto-detected if not provided)
            exploration_steps: List of ExplorationStep objects from AgentSession
        """
        if modified_files is None:
            modified_files = self.detect_modified_files()

        # Get or create session
        session = self.session_manager.get_or_create_session(terminal_id)

        # Extract context from all enabled providers
        all_items = []
        for provider_name in self.providers:
            try:
                # Import providers to ensure registration
                from .providers import explored_areas, touched_areas  # noqa: F401

                provider = ContextProviderRegistry.get_provider(provider_name, self.connection)

                # Different providers need different inputs
                if provider_name == "touched_areas" and modified_files:
                    items = provider.extract_context(modified_files)
                elif provider_name == "explored_areas" and exploration_steps:
                    items = provider.extract_context(exploration_steps)
                else:
                    # Skip provider if no relevant input
                    log.debug(f"Skipping provider '{provider_name}' - no relevant input")
                    continue

                all_items.extend(items)
                log.debug(f"Provider '{provider_name}' extracted {len(items)} items")
            except Exception as e:
                log.warning(f"Provider '{provider_name}' failed: {e}")

        # Add items to session
        if all_items:
            self.session_manager.add_context_items(session.session_id, all_items)
        else:
            log.debug("No context items extracted from any provider")

    def get_context_prompt(self, terminal_id: str, query: Optional[str] = None) -> str:
        """Get formatted context for LLM system prompt.

        Args:
            terminal_id: Terminal session identifier
            query: Optional query to re-rank context by relevance

        Returns:
            Formatted context string for system prompt
        """
        session = self.session_manager.get_or_create_session(terminal_id)
        items = self.session_manager.get_context(session.session_id, self._min_score)

        if not items:
            return ""

        # Re-rank by query relevance if query provided
        if query:
            items = rerank_context_items(items, query, top_k=self._max_items)
        else:
            # Limit number of items without re-ranking
            items = items[: self._max_items]

        # Deduplicate by file_path + qualified_name to avoid repetition
        seen_keys = set()
        unique_items = []
        for item in items:
            # Create unique key from file path and qualified name
            key = (item.file_path or "", item.qualified_name)
            if key not in seen_keys:
                seen_keys.add(key)
                unique_items.append(item)
        items = unique_items

        # Format as markdown
        lines = [
            "## Session Context",
            "",
            "The following code entities were recently modified or are related to recent changes:",
            "",
        ]

        for item in items:
            score_indicator = "***" if item.score > 0.8 else "**" if item.score > 0.5 else "*"
            lines.append(f"### {score_indicator}{item.entity_type}: {item.qualified_name}{score_indicator}")

            if item.file_path:
                # Show relative path if possible
                try:
                    rel_path = os.path.relpath(item.file_path, self.repo_root)
                    lines.append(f"- File: `{rel_path}`")
                except ValueError:
                    lines.append(f"- File: `{item.file_path}`")

            if item.description:
                # Truncate long descriptions
                desc = item.description.strip()
                if len(desc) > 200:
                    desc = desc[:197] + "..."
                lines.append(f"- Description: {desc}")

            if item.neighbors:
                neighbor_str = ", ".join(f"`{n}`" for n in item.neighbors[:5])
                if len(item.neighbors) > 5:
                    neighbor_str += f" (+{len(item.neighbors) - 5} more)"
                lines.append(f"- Related: {neighbor_str}")

            lines.append("")

        return "\n".join(lines)

    def get_context_items(self, terminal_id: str) -> list[ContextItem]:
        """Get raw context items for a session.

        Args:
            terminal_id: Terminal session identifier

        Returns:
            List of context items
        """
        session = self.session_manager.get_or_create_session(terminal_id)
        return self.session_manager.get_context(session.session_id, self._min_score)

    def clear_context(self, terminal_id: str):
        """Clear all context for a session.

        Args:
            terminal_id: Terminal session identifier
        """
        session = self.session_manager.get_or_create_session(terminal_id)
        self.session_manager.clear_session(session.session_id)

    @staticmethod
    def get_terminal_id() -> str:
        """Get or generate terminal ID.

        Uses EMDASH_TERMINAL_ID env var or generates a new one.

        Returns:
            Terminal ID string
        """
        import uuid

        terminal_id = os.getenv("EMDASH_TERMINAL_ID")
        if not terminal_id:
            terminal_id = str(uuid.uuid4())
            os.environ["EMDASH_TERMINAL_ID"] = terminal_id
        return terminal_id
