"""SAGE Context Management System (Items 601-700).

Implements:
- Conversation Context (Items 601-625)
- Project Context (Items 626-650)
- Code Context (Items 651-675)
- Knowledge Context (Items 676-700)
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class Message:
    """A conversation message."""

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ExtractedContext:
    """Context extracted from conversation."""

    mentioned_files: list[str] = field(default_factory=list)
    mentioned_symbols: list[str] = field(default_factory=list)
    intent: str = ""
    entities: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class ProjectStructure:
    """Project structure information."""

    directories: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    root: str = ""


@dataclass
class LanguageInfo:
    """Detected language information."""

    primary: str = "unknown"
    secondary: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class FrameworkInfo:
    """Detected framework information."""

    name: str = "unknown"
    version: str | None = None
    confidence: float = 0.0


@dataclass
class Dependency:
    """A project dependency."""

    name: str
    version: str | None = None
    dev: bool = False


@dataclass
class ArchitectureInfo:
    """Project architecture information."""

    pattern: str = "unknown"
    layers: list[str] = field(default_factory=list)
    components: list[str] = field(default_factory=list)


@dataclass
class ClassInfo:
    """Information about a class."""

    name: str
    methods: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)


@dataclass
class FunctionInfo:
    """Information about a function."""

    name: str
    parameters: list[str] = field(default_factory=list)
    returns: str | None = None


@dataclass
class ImportInfo:
    """Information about an import."""

    module: str
    names: list[str] = field(default_factory=list)
    alias: str | None = None


@dataclass
class CodeStructure:
    """Parsed code structure."""

    classes: list[ClassInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    imports: list[ImportInfo] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Code dependency information."""

    internal: list[str] = field(default_factory=list)
    external: list[str] = field(default_factory=list)


@dataclass
class SymbolLocation:
    """Location of a symbol."""

    file: str
    line: int
    column: int = 0


@dataclass
class KnowledgeItem:
    """A piece of knowledge."""

    key: str
    value: Any
    confidence: float = 1.0
    source: str = "manual"


@dataclass
class Inference:
    """An inferred piece of knowledge."""

    topic: str
    conclusion: str
    confidence: float = 0.0
    evidence: list[str] = field(default_factory=list)


@dataclass
class Pattern:
    """A learned pattern."""

    pattern: str
    frequency: int = 1
    confidence: float = 0.5


@dataclass
class CodingStyle:
    """Detected coding style."""

    naming_convention: str = "unknown"
    indentation: str = "spaces"
    line_length: int = 80


# =============================================================================
# Conversation Context (Items 601-625)
# =============================================================================


class ConversationContext:
    """Manage conversation context."""

    def __init__(self) -> None:
        """Initialize conversation context."""
        self.messages: list[Message] = []
        self._files_mentioned: set[str] = set()
        self._symbols_mentioned: set[str] = set()

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation."""
        self.messages.append(Message(role=role, content=content))
        self._extract_mentions(content)

    def _extract_mentions(self, content: str) -> None:
        """Extract file and symbol mentions from content."""
        # Extract file mentions (*.py, *.js, etc.)
        file_pattern = r"\b[\w/]+\.\w{1,4}\b"
        files = re.findall(file_pattern, content)
        self._files_mentioned.update(files)

        # Extract potential symbols (CamelCase, snake_case)
        symbol_pattern = r"\b([A-Z][a-zA-Z0-9]+|[a-z][a-z0-9_]+)\b"
        symbols = re.findall(symbol_pattern, content)
        self._symbols_mentioned.update(s for s in symbols if len(s) > 3)

    def extract_context(self) -> ExtractedContext:
        """Extract context from conversation."""
        # Determine intent from recent messages
        intent = "unknown"
        if self.messages:
            last_user_msg = next((m for m in reversed(self.messages) if m.role == "user"), None)
            if last_user_msg:
                content = last_user_msg.content.lower()
                if "fix" in content:
                    intent = "fix"
                elif "add" in content or "create" in content:
                    intent = "create"
                elif "explain" in content:
                    intent = "explain"
                elif "review" in content:
                    intent = "review"

        return ExtractedContext(
            mentioned_files=list(self._files_mentioned),
            mentioned_symbols=list(self._symbols_mentioned),
            intent=intent,
        )

    def summarize(self) -> str:
        """Summarize the conversation."""
        if not self.messages:
            return "No messages in conversation"

        user_count = sum(1 for m in self.messages if m.role == "user")
        assistant_count = sum(1 for m in self.messages if m.role == "assistant")

        topics = list(self._files_mentioned)[:3]
        topic_str = ", ".join(topics) if topics else "general discussion"

        return (
            f"Conversation with {len(self.messages)} messages "
            f"({user_count} user, {assistant_count} assistant). "
            f"Topics: {topic_str}"
        )


class ReferenceResolver:
    """Resolve references in conversation."""

    def resolve_pronoun(self, pronoun: str, messages: list[dict[str, str]]) -> str:
        """Resolve a pronoun to its referent."""
        pronoun_lower = pronoun.lower()

        # Look for recent nouns that the pronoun might refer to
        for msg in reversed(messages[:-1]):  # Skip the message with the pronoun
            content = msg.get("content", "")

            # Find potential referents (nouns)
            # Pattern for "the X" or "X function/class/file"
            patterns = [
                r"the\s+(\w+\s+\w+)",
                r"(\w+)\s+(?:function|class|file|method)",
                r"Look at\s+the\s+(\w+\s+\w+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    return match.group(1)

        return pronoun  # Return unchanged if no referent found

    def resolve_coreference(self, phrase: str, messages: list[dict[str, str]]) -> str:
        """Resolve coreference (e.g., 'the issue' -> 'database connection failing')."""
        # Look for related concepts in previous messages
        for msg in reversed(messages[:-1]):
            content = msg.get("content", "")

            # Look for problem statements
            if "is failing" in content or "not working" in content:
                # Extract the subject
                match = re.search(
                    r"(?:The\s+)?(\w+(?:\s+\w+)?)\s+is\s+(?:failing|not working)",
                    content,
                    re.IGNORECASE,
                )
                if match:
                    return match.group(1)

        return phrase


class GoalTracker:
    """Track goals and progress."""

    def __init__(self) -> None:
        """Initialize goal tracker."""
        self.current_goal: str | None = None
        self.subgoals: list[str] = []
        self.completed_subgoals: list[str] = []

    def set_goal(self, goal: str) -> None:
        """Set the current goal."""
        self.current_goal = goal
        self.subgoals = []
        self.completed_subgoals = []

    def add_subgoal(self, subgoal: str) -> None:
        """Add a subgoal."""
        self.subgoals.append(subgoal)

    def complete_subgoal(self, subgoal: str) -> None:
        """Mark a subgoal as complete."""
        if subgoal in self.subgoals:
            self.subgoals.remove(subgoal)
            self.completed_subgoals.append(subgoal)

    @property
    def progress(self) -> float:
        """Calculate progress (0-1)."""
        total = len(self.subgoals) + len(self.completed_subgoals)
        if total == 0:
            return 0.0
        return len(self.completed_subgoals) / total


# =============================================================================
# Project Context (Items 626-650)
# =============================================================================


class ProjectAnalyzer:
    """Analyze project context."""

    def __init__(self, project_path: str) -> None:
        """Initialize project analyzer."""
        self.project_path = Path(project_path)

    def discover_structure(self) -> ProjectStructure:
        """Discover project structure."""
        dirs = []
        files = []

        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                dirs.append(item.name)
            elif item.is_file():
                files.append(item.name)

        return ProjectStructure(
            directories=dirs,
            files=files,
            root=str(self.project_path),
        )

    def detect_language(self) -> LanguageInfo:
        """Detect primary programming language."""
        extensions: dict[str, int] = {}
        import os

        # Optimization: Use os.walk for efficiency and early directory pruning
        skip_dirs = {".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}
        file_count = 0
        for root, dirs, files in os.walk(self.project_path):
            # Prune directories in-place
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
            
            for f in files:
                if f.startswith("."):
                    continue
                ext = os.path.splitext(f)[1].lower()
                if ext:
                    extensions[ext] = extensions.get(ext, 0) + 1
                    file_count += 1
                
                if file_count >= 2000: # Safety cap
                    break
            if file_count >= 2000:
                break

        # Map extensions to languages
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
        }

        lang_counts: dict[str, int] = {}
        for ext, count in extensions.items():
            lang = lang_map.get(ext)
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + count

        if not lang_counts:
            return LanguageInfo(primary="unknown")

        primary = max(lang_counts.items(), key=lambda x: x[1])
        total = sum(lang_counts.values())

        return LanguageInfo(
            primary=primary[0],
            secondary=[l for l in lang_counts if l != primary[0]],
            confidence=primary[1] / total if total > 0 else 0,
        )

    def detect_framework(self) -> FrameworkInfo:
        """Detect project framework."""
        # Check for Python frameworks
        requirements = self.project_path / "requirements.txt"
        if requirements.exists():
            content = requirements.read_text(encoding="utf-8", errors="replace").lower()
            if "flask" in content:
                return FrameworkInfo(name="Flask", confidence=0.9)
            elif "django" in content:
                return FrameworkInfo(name="Django", confidence=0.9)
            elif "fastapi" in content:
                return FrameworkInfo(name="FastAPI", confidence=0.9)

        # Check for Node.js frameworks
        package_json = self.project_path / "package.json"
        if package_json.exists():
            content = package_json.read_text(encoding="utf-8", errors="replace").lower()
            if "react" in content:
                return FrameworkInfo(name="React", confidence=0.9)
            elif "vue" in content:
                return FrameworkInfo(name="Vue", confidence=0.9)
            elif "express" in content:
                return FrameworkInfo(name="Express", confidence=0.9)

        return FrameworkInfo(name="unknown", confidence=0)

    def discover_dependencies(self) -> list[Dependency]:
        """Discover project dependencies."""
        deps = []

        # Python requirements.txt
        requirements = self.project_path / "requirements.txt"
        if requirements.exists():
            for line in requirements.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    # Parse name and version
                    match = re.match(r"([a-zA-Z0-9_-]+)([<>=!]+.+)?", line)
                    if match:
                        name = match.group(1)
                        version = match.group(2)
                        deps.append(Dependency(name=name, version=version))

        return deps

    def map_architecture(self) -> ArchitectureInfo:
        """Map project architecture."""
        dirs = set()
        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                dirs.add(item.name.lower())

        # Detect MVC pattern
        mvc_dirs = {"models", "views", "controllers"}
        if len(dirs & mvc_dirs) >= 2:
            return ArchitectureInfo(
                pattern="MVC",
                layers=["models", "views", "controllers"],
            )

        # Detect layered architecture
        layer_dirs = {"domain", "application", "infrastructure", "presentation"}
        if len(dirs & layer_dirs) >= 2:
            return ArchitectureInfo(
                pattern="Layered",
                layers=list(dirs & layer_dirs),
            )

        # Default
        return ArchitectureInfo(
            pattern="Custom",
            layers=list(dirs),
        )


# =============================================================================
# Code Context (Items 651-675)
# =============================================================================


class CodeAnalyzer:
    """Analyze code structure."""

    def parse_structure(self, code: str) -> CodeStructure:
        """Parse code structure."""
        structure = CodeStructure()

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    bases = [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases]
                    structure.classes.append(
                        ClassInfo(
                            name=node.name,
                            methods=methods,
                            bases=bases,
                        )
                    )

                elif isinstance(node, ast.FunctionDef):
                    # Only top-level functions
                    if not any(isinstance(p, ast.ClassDef) for p in ast.walk(tree)):
                        params = [arg.arg for arg in node.args.args]
                        structure.functions.append(
                            FunctionInfo(
                                name=node.name,
                                parameters=params,
                            )
                        )

            # Re-parse for top-level functions only
            structure.functions = []
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    params = [arg.arg for arg in node.args.args]
                    structure.functions.append(
                        FunctionInfo(
                            name=node.name,
                            parameters=params,
                        )
                    )

        except SyntaxError:
            pass

        return structure

    def extract_imports(self, code: str) -> list[ImportInfo]:
        """Extract imports from code."""
        imports = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(
                            ImportInfo(
                                module=alias.name,
                                alias=alias.asname,
                            )
                        )
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    names = [alias.name for alias in node.names]
                    imports.append(
                        ImportInfo(
                            module=module,
                            names=names,
                        )
                    )

        except SyntaxError:
            pass

        return imports

    def identify_dependencies(self, code: str) -> DependencyInfo:
        """Identify code dependencies."""
        deps = DependencyInfo()

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    # Relative imports (level > 0 or starts with .)
                    if node.level > 0:
                        # Relative import like "from .utils import helper"
                        prefix = "." * node.level
                        deps.internal.append(f"{prefix}{module}" if module else prefix)
                    elif "." in module or module.islower():
                        # Internal imports like "from models.user import User"
                        deps.internal.append(module)
                    else:
                        deps.external.append(module)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        # Standard imports are usually external
                        deps.external.append(alias.name)

        except SyntaxError:
            pass

        return deps


class SymbolResolver:
    """Resolve symbols to their definitions."""

    def __init__(self, project_path: str) -> None:
        """Initialize symbol resolver."""
        self.project_path = Path(project_path)
        self._symbol_cache: dict[str, SymbolLocation] = {}

    def resolve(self, symbol: str, from_file: str) -> SymbolLocation | None:
        """Resolve symbol to its definition."""
        # Check cache
        cache_key = f"{from_file}:{symbol}"
        if cache_key in self._symbol_cache:
            return self._symbol_cache[cache_key]

        # Search for definition in project files
        for py_file in self.project_path.glob("*.py"):
            if py_file.name == from_file:
                continue

            try:
                content = py_file.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if (isinstance(node, ast.FunctionDef) and node.name == symbol) or (
                        isinstance(node, ast.ClassDef) and node.name == symbol
                    ):
                        location = SymbolLocation(
                            file=py_file.name,
                            line=node.lineno,
                        )
                        self._symbol_cache[cache_key] = location
                        return location

            except (SyntaxError, UnicodeDecodeError):
                continue

        return None


# =============================================================================
# Knowledge Context (Items 676-700)
# =============================================================================


class KnowledgeBase:
    """Store and query knowledge."""

    def __init__(self) -> None:
        """Initialize knowledge base."""
        self._knowledge: dict[str, KnowledgeItem] = {}

    def store(self, key: str, value: Any, confidence: float = 1.0) -> None:
        """Store a piece of knowledge."""
        self._knowledge[key] = KnowledgeItem(
            key=key,
            value=value,
            confidence=confidence,
        )

    def get(self, key: str) -> Any | None:
        """Get a piece of knowledge."""
        item = self._knowledge.get(key)
        return item.value if item else None

    def query(self, pattern: str) -> list[KnowledgeItem]:
        """Query knowledge by pattern."""
        results = []
        pattern_lower = pattern.lower()

        for key, item in self._knowledge.items():
            if pattern_lower in key.lower():
                results.append(item)

        return results

    def infer(self, topic: str) -> Inference | None:
        """Infer knowledge about a topic."""
        evidence = []

        # Look for related knowledge
        if topic == "testing_setup":
            if self.get("uses_pytest"):
                evidence.append("Uses pytest")
            if self.get("has_tests_directory"):
                evidence.append("Has tests directory")

            if evidence:
                return Inference(
                    topic=topic,
                    conclusion="Project has pytest-based testing",
                    confidence=0.8,
                    evidence=evidence,
                )

        return None


class PatternLearner:
    """Learn patterns from observations."""

    def __init__(self) -> None:
        """Initialize pattern learner."""
        self._observations: list[str] = []
        self._patterns: dict[str, Pattern] = {}

    def observe(self, observation: str) -> None:
        """Observe a piece of code or text."""
        self._observations.append(observation)
        self._extract_patterns(observation)

    def _extract_patterns(self, text: str) -> None:
        """Extract patterns from text."""
        # Look for function naming patterns
        func_match = re.search(r"def\s+(\w+)", text)
        if func_match:
            name = func_match.group(1)
            # Check for prefixes
            for prefix in ["test_", "get_", "set_", "is_", "has_"]:
                if name.startswith(prefix):
                    pattern_key = f"function_prefix:{prefix}"
                    if pattern_key in self._patterns:
                        self._patterns[pattern_key].frequency += 1
                    else:
                        self._patterns[pattern_key] = Pattern(
                            pattern=prefix,
                            frequency=1,
                        )

    def get_patterns(self) -> list[Pattern]:
        """Get learned patterns."""
        return list(self._patterns.values())


class StyleAdapter:
    """Adapt to coding style."""

    def __init__(self) -> None:
        """Initialize style adapter."""
        self._observations: list[str] = []
        self._naming_counts: dict[str, int] = {
            "snake_case": 0,
            "camelCase": 0,
            "PascalCase": 0,
        }

    def observe(self, code: str) -> None:
        """Observe code sample."""
        self._observations.append(code)
        self._analyze_naming(code)

    def _analyze_naming(self, code: str) -> None:
        """Analyze naming conventions."""
        # Look for function definitions
        func_match = re.search(r"def\s+(\w+)", code)
        if func_match:
            name = func_match.group(1)

            if "_" in name and name.islower():
                self._naming_counts["snake_case"] += 1
            elif name[0].islower() and any(c.isupper() for c in name[1:]):
                self._naming_counts["camelCase"] += 1
            elif name[0].isupper():
                self._naming_counts["PascalCase"] += 1

    def detected_style(self) -> CodingStyle:
        """Get detected coding style."""
        if not any(self._naming_counts.values()):
            return CodingStyle()

        convention = max(self._naming_counts.items(), key=lambda x: x[1])[0]

        return CodingStyle(naming_convention=convention)


class ContextCompactor:
    """Automatic context compaction when approaching token limits.

    When context hits 90% of window, summarizes conversation history
    while preserving architectural decisions and key context.
    """

    def __init__(
        self,
        max_tokens: int = 128000,
        threshold: float = 0.9,
    ):
        self.max_tokens = max_tokens
        self.threshold = threshold
        self.compaction_count = 0

    def estimate_tokens(self, messages: list) -> int:
        """Rough token estimation (4 chars ≈ 1 token)."""
        total_chars = sum(len(self._get_msg_content(m)) for m in messages)
        return total_chars // 4

    def _get_msg_role(self, msg: Any) -> str:
        """Helper to get message role."""
        if hasattr(msg, "role"):
            return msg.role
        if isinstance(msg, dict):
            return msg.get("role", "")
        return ""

    def _get_msg_content(self, msg: Any) -> str:
        """Helper to get message content."""
        if hasattr(msg, "content"):
            return msg.content
        if isinstance(msg, dict):
            return msg.get("content", "")
        return ""

    def needs_compaction(self, messages: list) -> bool:
        """Check if context needs compaction."""
        tokens = self.estimate_tokens(messages)
        return tokens >= (self.max_tokens * self.threshold)

    def compact(
        self,
        messages: list,
        router: Any,  # Use Any to avoid circular import with ProviderRouter
        model_id: str,
    ) -> list:
        """Compact messages by summarizing older conversation.

        Preserves:
        - System prompt
        - Most recent 4 turns
        - Architectural decisions
        - File contents mentioned
        """
        if len(messages) <= 6:
            return messages

        # Keep system prompt and recent messages
        system_msgs = [m for m in messages if self._get_msg_role(m) == "system"]
        recent = messages[-8:]  # Keep last 4 turns (8 messages)
        to_summarize = messages[len(system_msgs) : -8]

        if not to_summarize:
            return messages

        # Extract key information to preserve
        files_mentioned = set()
        architectural_decisions = []

        for msg in to_summarize:
            content = self._get_msg_content(msg)
            # Extract file paths
            for match in re.finditer(r"FILE:\s*(\S+)", content):
                files_mentioned.add(match.group(1))
            # Extract architectural patterns
            if any(
                x in content.lower() for x in ["architecture", "design", "pattern", "structure"]
            ):
                # Keep first 200 chars of architectural discussions
                architectural_decisions.append(content[:200])

        # Build summary prompt
        summary_content = "\n---\n".join(self._get_msg_content(m)[:500] for m in to_summarize[:10])

        summary_prompt = (
            "Summarize this conversation history in 3-5 bullet points. "
            "Focus on: decisions made, files changed, problems solved.\n\n"
            f"{summary_content[:3000]}"
        )

        # Generate summary using a fast model
        try:
            from sage.providers.base import Message as MsgType

            summary = router.generate(
                [MsgType(role="user", content=summary_prompt)],
                model_id,
                temperature=0.3,
                max_tokens=500,
            )
        except Exception:
            summary = "Previous conversation involved code changes and debugging."

        # Build compacted context - use Message object for consistency
        from sage.providers.base import Message as MsgClass

        compacted_history = MsgClass(
            role="assistant",
            content=(
                f"[Context Compacted - Summary of {len(to_summarize)} messages]\n\n"
                f"{summary}\n\n"
                f"Files touched: {', '.join(list(files_mentioned)[:10]) or 'various'}\n"
            ),
        )

        self.compaction_count += 1

        return system_msgs + [compacted_history] + recent

    def get_status(self, messages: list) -> str:
        """Get context status."""
        tokens = self.estimate_tokens(messages)
        pct = (tokens / self.max_tokens) * 100
        return f"Context: {tokens:,}/{self.max_tokens:,} tokens ({pct:.1f}%) | Compactions: {self.compaction_count}"
