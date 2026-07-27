"""
Advanced prompt engineering system for SAGE.

P1-28: Add dynamic prompt adaptation per-task
P1-29: Implement few-shot example selection by similarity
P1-30: Add prompt compression for token efficiency
P1-31: Create prompt versioning/tagging
P1-32: Implement prompt injection prevention
P1-33: Add A/B testing framework for prompts
P1-34: Implement feedback loop for prompt refinement
P1-35: Add multi-language prompt templates
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# =============================================================================
# Prompt Classification (P1-28)
# =============================================================================


class TaskType(Enum):
    """Types of tasks for prompt adaptation."""

    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    BUG_FIX = "bug_fix"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    EXPLANATION = "explanation"
    ARCHITECTURE = "architecture"
    DEBUGGING = "debugging"
    GENERAL = "general"


class PromptStyle(Enum):
    """Prompt styles for different scenarios."""

    CONCISE = "concise"  # Minimal, to-the-point
    DETAILED = "detailed"  # Full explanations
    STEP_BY_STEP = "step_by_step"  # Guided walkthrough
    TECHNICAL = "technical"  # Expert-level
    BEGINNER = "beginner"  # Simplified


# =============================================================================
# Few-shot Examples (P1-29)
# =============================================================================


@dataclass
class FewShotExample:
    """A few-shot example for in-context learning."""

    id: str
    task_type: TaskType
    input_text: str
    output_text: str
    tags: list[str] = field(default_factory=list)
    language: str = "python"
    quality_score: float = 1.0
    usage_count: int = 0

    def to_prompt(self) -> str:
        """Format as prompt example."""
        return f"User: {self.input_text}\n\nAssistant: {self.output_text}"


class FewShotSelector:
    """
    Selects relevant few-shot examples based on task similarity.

    P1-29: Implement few-shot example selection by similarity
    """

    def __init__(self, examples: list[FewShotExample] | None = None):
        self.examples = examples or []
        self._usage_stats: dict[str, int] = {}

    def add_example(self, example: FewShotExample) -> None:
        """Add an example to the selector."""
        self.examples.append(example)

    def select(
        self,
        query: str,
        task_type: TaskType | None = None,
        language: str | None = None,
        max_examples: int = 3,
    ) -> list[FewShotExample]:
        """Select relevant examples for a query."""
        candidates = self.examples.copy()

        # Filter by task type
        if task_type:
            candidates = [e for e in candidates if e.task_type == task_type]

        # Filter by language
        if language:
            candidates = [e for e in candidates if e.language == language or e.language == "any"]

        # Score by keyword overlap
        query_words = set(query.lower().split())
        scored = []
        for example in candidates:
            example_words = set(example.input_text.lower().split())
            overlap = len(query_words & example_words)
            score = (overlap / max(len(query_words), 1)) * example.quality_score
            scored.append((score, example))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        # Return top examples
        selected = [ex for _, ex in scored[:max_examples]]

        # Update usage stats
        for ex in selected:
            ex.usage_count += 1

        return selected

    def format_examples(self, examples: list[FewShotExample]) -> str:
        """Format selected examples for prompt inclusion."""
        if not examples:
            return ""

        parts = ["Here are some examples of similar tasks:\n"]
        for i, ex in enumerate(examples, 1):
            parts.append(f"--- Example {i} ---")
            parts.append(ex.to_prompt())
            parts.append("")

        return "\n".join(parts)


# =============================================================================
# Prompt Compression (P1-30)
# =============================================================================


class PromptCompressor:
    """
    Compresses prompts to reduce token usage while preserving meaning.

    P1-30: Add prompt compression for token efficiency
    """

    # Patterns that can be safely shortened
    COMPRESSION_RULES = [
        # Remove excessive whitespace
        (r"\n{3,}", "\n\n"),
        (r"[ \t]{2,}", " "),
        # Shorten common phrases
        (r"please\s+", ""),
        (r"could you\s+", ""),
        (r"I would like you to\s+", ""),
        (r"I want you to\s+", ""),
        # Remove filler words (careful application)
        (r"\b(basically|essentially|actually|really|very|just)\b\s*", ""),
        # Compress code formatting instructions
        (r"make sure to\s+", ""),
        (r"don't forget to\s+", ""),
    ]

    # Important patterns to preserve
    PRESERVE_PATTERNS = [
        r"```[\s\S]*?```",  # Code blocks
        r"`[^`]+`",  # Inline code
        r"\"[^\"]+\"",  # Quoted strings
        r"'[^']+'",  # Single-quoted strings
        r"FILE:\s*\S+",  # File references
    ]

    def __init__(self, aggressive: bool = False):
        self.aggressive = aggressive

    def compress(self, text: str, target_reduction: float = 0.2) -> tuple[str, float]:
        """
        Compress text to reduce tokens.

        Returns:
            Tuple of (compressed_text, reduction_ratio)
        """
        original_len = len(text)

        # Extract and protect important content
        preserved = {}
        for i, pattern in enumerate(self.PRESERVE_PATTERNS):
            matches = re.findall(pattern, text)
            for j, match in enumerate(matches):
                placeholder = f"__PRESERVE_{i}_{j}__"
                preserved[placeholder] = match
                text = text.replace(match, placeholder, 1)

        # Apply compression rules
        for pattern, replacement in self.COMPRESSION_RULES:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Aggressive compression if enabled
        if self.aggressive:
            text = self._aggressive_compress(text)

        # Restore preserved content
        for placeholder, original in preserved.items():
            text = text.replace(placeholder, original)

        # Calculate reduction
        compressed_len = len(text)
        reduction = 1 - (compressed_len / original_len) if original_len > 0 else 0

        return text.strip(), reduction

    def _aggressive_compress(self, text: str) -> str:
        """Apply more aggressive compression."""
        # Remove comments that aren't in code blocks
        text = re.sub(r"^\s*#.*$", "", text, flags=re.MULTILINE)

        # Shorten documentation references
        text = re.sub(r"see the documentation at \S+", "[see docs]", text)

        # Compress lists of similar items
        text = re.sub(r"(- \w+\n){5,}", "- [multiple items]\n", text)

        return text


# =============================================================================
# Prompt Versioning (P1-31)
# =============================================================================


@dataclass
class PromptVersion:
    """A versioned prompt template."""

    id: str
    version: str
    content: str
    created_at: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    parent_version: str | None = None
    performance_score: float = 0.0
    usage_count: int = 0

    @property
    def content_hash(self) -> str:
        """Get hash of prompt content."""
        return hashlib.sha256(self.content.encode()).hexdigest()[:12]


class PromptVersionManager:
    """
    Manages prompt versions and history.

    P1-31: Create prompt versioning/tagging
    """

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path
        self.versions: dict[
            str, dict[str, PromptVersion]
        ] = {}  # prompt_id -> version -> PromptVersion
        self.active_versions: dict[str, str] = {}  # prompt_id -> active_version

        if storage_path and storage_path.exists():
            self._load_versions()

    def create_version(
        self,
        prompt_id: str,
        content: str,
        tags: list[str] | None = None,
        metadata: dict | None = None,
    ) -> PromptVersion:
        """Create a new version of a prompt."""
        if prompt_id not in self.versions:
            self.versions[prompt_id] = {}
            version_num = "1.0.0"
        else:
            # Increment version
            latest = max(self.versions[prompt_id].keys())
            parts = latest.split(".")
            parts[-1] = str(int(parts[-1]) + 1)
            version_num = ".".join(parts)

        version = PromptVersion(
            id=prompt_id,
            version=version_num,
            content=content,
            tags=tags or [],
            metadata=metadata or {},
            parent_version=self.active_versions.get(prompt_id),
        )

        self.versions[prompt_id][version_num] = version
        self.active_versions[prompt_id] = version_num

        if self.storage_path:
            self._save_versions()

        return version

    def get_version(self, prompt_id: str, version: str | None = None) -> PromptVersion | None:
        """Get a specific version or the active version."""
        if prompt_id not in self.versions:
            return None

        if version is None:
            version = self.active_versions.get(prompt_id)

        return self.versions[prompt_id].get(version)

    def get_active(self, prompt_id: str) -> PromptVersion | None:
        """Get the active version of a prompt."""
        return self.get_version(prompt_id)

    def set_active(self, prompt_id: str, version: str) -> bool:
        """Set the active version of a prompt."""
        if prompt_id in self.versions and version in self.versions[prompt_id]:
            self.active_versions[prompt_id] = version
            return True
        return False

    def list_versions(self, prompt_id: str) -> list[PromptVersion]:
        """List all versions of a prompt."""
        if prompt_id not in self.versions:
            return []
        return sorted(
            self.versions[prompt_id].values(),
            key=lambda v: v.created_at,
            reverse=True,
        )

    def _load_versions(self) -> None:
        """Load versions from storage."""
        version_file = self.storage_path / "prompt_versions.json"
        if version_file.exists():
            data = json.loads(version_file.read_text(encoding="utf-8", errors="replace"))
            for prompt_id, versions in data.get("versions", {}).items():
                self.versions[prompt_id] = {v["version"]: PromptVersion(**v) for v in versions}
            self.active_versions = data.get("active", {})

    def _save_versions(self) -> None:
        """Save versions to storage."""
        if not self.storage_path:
            return

        self.storage_path.mkdir(parents=True, exist_ok=True)
        version_file = self.storage_path / "prompt_versions.json"

        data = {
            "versions": {
                pid: [
                    {
                        "id": v.id,
                        "version": v.version,
                        "content": v.content,
                        "created_at": v.created_at,
                        "tags": v.tags,
                        "metadata": v.metadata,
                        "parent_version": v.parent_version,
                        "performance_score": v.performance_score,
                        "usage_count": v.usage_count,
                    }
                    for v in versions.values()
                ]
                for pid, versions in self.versions.items()
            },
            "active": self.active_versions,
        }

        version_file.write_text(json.dumps(data, indent=2))


# =============================================================================
# Prompt Injection Prevention (P1-32)
# =============================================================================


class PromptGuard:
    """
    Prevents prompt injection attacks.

    P1-32: Implement prompt injection prevention
    """

    # Patterns that indicate injection attempts
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
        r"disregard\s+(all\s+)?(previous|prior|above)",
        r"forget\s+(everything|all|what)",
        r"you\s+are\s+now\s+(a|an)",
        r"new\s+instructions?:",
        r"system\s*:\s*",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"\[INST\]",
        r"\[/INST\]",
        r"###\s*(system|instruction)",
        r"---\s*begin\s+new\s+prompt",
        r"override\s+system\s+prompt",
        r"act\s+as\s+if\s+you\s+are",
        r"pretend\s+(you\s+are|to\s+be)",
    ]

    # Compiled patterns for efficiency
    _compiled_patterns: list[re.Pattern] = []

    def __init__(self, strict: bool = False):
        self.strict = strict
        if not PromptGuard._compiled_patterns:
            PromptGuard._compiled_patterns = [
                re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS
            ]

    def check(self, text: str) -> tuple[bool, list[str]]:
        """
        Check text for injection attempts.

        Returns:
            Tuple of (is_safe, list of detected patterns)
        """
        detected = []
        for pattern in self._compiled_patterns:
            if pattern.search(text):
                detected.append(pattern.pattern)

        return len(detected) == 0, detected

    def sanitize(self, text: str) -> str:
        """Sanitize text by escaping potential injection patterns."""
        # Escape special tokens
        text = text.replace("<|", "< |")
        text = text.replace("|>", "| >")
        text = text.replace("[INST]", "[_INST_]")
        text = text.replace("[/INST]", "[/_INST_]")

        # Escape system-like headers
        text = re.sub(
            r"^(system|assistant|user)\s*:", r"[\1]:", text, flags=re.IGNORECASE | re.MULTILINE
        )

        return text

    def wrap_user_input(self, user_input: str) -> str:
        """Wrap user input with clear boundaries."""
        sanitized = self.sanitize(user_input)
        return f"<user_input>\n{sanitized}\n</user_input>"


# =============================================================================
# A/B Testing Framework (P1-33)
# =============================================================================


@dataclass
class ABTestResult:
    """Result from an A/B test."""

    variant: str
    success: bool
    score: float
    latency: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ABTest:
    """An A/B test configuration."""

    id: str
    name: str
    variants: dict[str, str]  # variant_name -> prompt_content
    allocation: dict[str, float] = field(default_factory=dict)  # variant -> percentage
    results: list[ABTestResult] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    active: bool = True


class ABTestManager:
    """
    Manages A/B testing for prompts.

    P1-33: Add A/B testing framework for prompts
    """

    def __init__(self):
        self.tests: dict[str, ABTest] = {}
        self._random_seed = 0

    def create_test(
        self,
        name: str,
        variants: dict[str, str],
        allocation: dict[str, float] | None = None,
    ) -> ABTest:
        """Create a new A/B test."""
        test_id = hashlib.sha256(name.encode()).hexdigest()[:8]

        # Default to equal allocation
        if allocation is None:
            allocation = {v: 1.0 / len(variants) for v in variants}

        test = ABTest(
            id=test_id,
            name=name,
            variants=variants,
            allocation=allocation,
        )
        self.tests[test_id] = test
        return test

    def get_variant(self, test_id: str, user_id: str | None = None) -> tuple[str, str]:
        """
        Get variant for a test.

        Returns:
            Tuple of (variant_name, prompt_content)
        """
        test = self.tests.get(test_id)
        if not test or not test.active:
            raise ValueError(f"Test {test_id} not found or inactive")

        # Deterministic variant selection based on user_id
        if user_id:
            hash_input = f"{test_id}:{user_id}"
            hash_val = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
            rand_val = (hash_val % 1000) / 1000
        else:
            import random

            rand_val = random.random()

        # Select variant based on allocation
        cumulative = 0.0
        for variant, pct in test.allocation.items():
            cumulative += pct
            if rand_val <= cumulative:
                return variant, test.variants[variant]

        # Fallback to first variant
        first = list(test.variants.keys())[0]
        return first, test.variants[first]

    def record_result(
        self,
        test_id: str,
        variant: str,
        success: bool,
        score: float = 0.0,
        latency: float = 0.0,
        metadata: dict | None = None,
    ) -> None:
        """Record a test result."""
        test = self.tests.get(test_id)
        if not test:
            return

        result = ABTestResult(
            variant=variant,
            success=success,
            score=score,
            latency=latency,
            metadata=metadata or {},
        )
        test.results.append(result)

    def get_statistics(self, test_id: str) -> dict[str, Any]:
        """Get statistics for a test."""
        test = self.tests.get(test_id)
        if not test:
            return {}

        stats: dict[str, Any] = {variant: {} for variant in test.variants}

        for result in test.results:
            v = result.variant
            if v not in stats:
                continue

            if "count" not in stats[v]:
                stats[v] = {"count": 0, "successes": 0, "total_score": 0, "total_latency": 0}

            stats[v]["count"] += 1
            if result.success:
                stats[v]["successes"] += 1
            stats[v]["total_score"] += result.score
            stats[v]["total_latency"] += result.latency

        # Calculate averages
        for v in stats:
            count = stats[v].get("count", 0)
            if count > 0:
                stats[v]["success_rate"] = stats[v]["successes"] / count
                stats[v]["avg_score"] = stats[v]["total_score"] / count
                stats[v]["avg_latency"] = stats[v]["total_latency"] / count

        return stats


# =============================================================================
# Prompt Feedback System (P1-34)
# =============================================================================


@dataclass
class PromptFeedback:
    """Feedback for a prompt execution."""

    prompt_id: str
    prompt_version: str
    success: bool
    rating: int | None = None  # 1-5
    latency: float = 0.0
    tokens_used: int = 0
    error_type: str | None = None
    user_feedback: str | None = None
    timestamp: float = field(default_factory=time.time)


class PromptFeedbackCollector:
    """
    Collects and analyzes prompt performance feedback.

    P1-34: Implement feedback loop for prompt refinement
    """

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path
        self.feedback: list[PromptFeedback] = []

        if storage_path and (storage_path / "feedback.json").exists():
            self._load_feedback()

    def record(self, feedback: PromptFeedback) -> None:
        """Record feedback."""
        self.feedback.append(feedback)
        if self.storage_path:
            self._save_feedback()

    def get_performance_score(self, prompt_id: str, version: str | None = None) -> float:
        """Calculate performance score for a prompt."""
        relevant = [
            f
            for f in self.feedback
            if f.prompt_id == prompt_id and (version is None or f.prompt_version == version)
        ]

        if not relevant:
            return 0.0

        # Weight factors
        success_weight = 0.4
        rating_weight = 0.3
        latency_weight = 0.3

        # Calculate scores
        success_rate = sum(1 for f in relevant if f.success) / len(relevant)
        avg_rating = sum(f.rating or 3 for f in relevant) / len(relevant) / 5
        avg_latency = sum(f.latency for f in relevant) / len(relevant)
        latency_score = max(0, 1 - (avg_latency / 30))  # 30s = 0 score

        return (
            success_rate * success_weight
            + avg_rating * rating_weight
            + latency_score * latency_weight
        )

    def get_improvement_suggestions(self, prompt_id: str) -> list[str]:
        """Get suggestions for improving a prompt."""
        relevant = [f for f in self.feedback if f.prompt_id == prompt_id]
        suggestions = []

        if not relevant:
            return ["No feedback data available"]

        # Analyze error patterns
        errors = [f.error_type for f in relevant if f.error_type]
        if errors:
            error_counts = {}
            for e in errors:
                error_counts[e] = error_counts.get(e, 0) + 1
            top_error = max(error_counts, key=error_counts.get)
            suggestions.append(
                f"Address common error: {top_error} ({error_counts[top_error]} occurrences)"
            )

        # Analyze latency
        avg_latency = sum(f.latency for f in relevant) / len(relevant)
        if avg_latency > 10:
            suggestions.append("Consider prompt compression to reduce latency")

        # Analyze ratings
        low_ratings = [f for f in relevant if f.rating and f.rating <= 2]
        if len(low_ratings) > len(relevant) * 0.3:
            suggestions.append("High rate of low ratings - review user feedback for improvements")

        return suggestions or ["Prompt is performing well"]

    def _load_feedback(self) -> None:
        """Load feedback from storage."""
        feedback_file = self.storage_path / "feedback.json"
        if feedback_file.exists():
            data = json.loads(feedback_file.read_text(encoding="utf-8", errors="replace"))
            self.feedback = [PromptFeedback(**f) for f in data]

    def _save_feedback(self) -> None:
        """Save feedback to storage."""
        if not self.storage_path:
            return

        self.storage_path.mkdir(parents=True, exist_ok=True)
        feedback_file = self.storage_path / "feedback.json"

        data = [
            {
                "prompt_id": f.prompt_id,
                "prompt_version": f.prompt_version,
                "success": f.success,
                "rating": f.rating,
                "latency": f.latency,
                "tokens_used": f.tokens_used,
                "error_type": f.error_type,
                "user_feedback": f.user_feedback,
                "timestamp": f.timestamp,
            }
            for f in self.feedback
        ]

        feedback_file.write_text(json.dumps(data, indent=2))


# =============================================================================
# Multi-language Templates (P1-35)
# =============================================================================


class PromptLocalization:
    """
    Multi-language prompt templates.

    P1-35: Add multi-language prompt templates
    """

    TEMPLATES: dict[str, dict[str, str]] = {
        "system_intro": {
            "en": "You are SAGE, an AI coding assistant.",
            "es": "Eres SAGE, un asistente de programación con IA.",
            "fr": "Vous êtes SAGE, un assistant de programmation IA.",
            "de": "Sie sind SAGE, ein KI-Programmierassistent.",
            "ja": "あなたはSAGE、AIコーディングアシスタントです。",
            "zh": "您是SAGE，一个AI编程助手。",
            "pt": "Você é SAGE, um assistente de programação com IA.",
            "ru": "Вы SAGE, ИИ-помощник по программированию.",
        },
        "error_message": {
            "en": "An error occurred: {error}",
            "es": "Se produjo un error: {error}",
            "fr": "Une erreur s'est produite: {error}",
            "de": "Ein Fehler ist aufgetreten: {error}",
            "ja": "エラーが発生しました: {error}",
            "zh": "发生错误: {error}",
        },
        "confirmation_prompt": {
            "en": "Are you sure you want to {action}?",
            "es": "¿Estás seguro de que quieres {action}?",
            "fr": "Êtes-vous sûr de vouloir {action}?",
            "de": "Sind Sie sicher, dass Sie {action} möchten?",
        },
    }

    def __init__(self, default_language: str = "en"):
        self.default_language = default_language
        self.custom_templates: dict[str, dict[str, str]] = {}

    def get(self, key: str, language: str | None = None, **kwargs) -> str:
        """Get localized template."""
        lang = language or self.default_language

        # Check custom templates first
        if key in self.custom_templates:
            templates = self.custom_templates[key]
        elif key in self.TEMPLATES:
            templates = self.TEMPLATES[key]
        else:
            return key  # Return key as fallback

        # Get template for language
        template = (
            templates.get(lang)
            or templates.get(self.default_language)
            or list(templates.values())[0]
        )

        # Format with kwargs
        return template.format(**kwargs) if kwargs else template

    def add_template(self, key: str, translations: dict[str, str]) -> None:
        """Add a custom template with translations."""
        self.custom_templates[key] = translations

    def get_available_languages(self) -> list[str]:
        """Get list of available languages."""
        languages = set()
        for templates in self.TEMPLATES.values():
            languages.update(templates.keys())
        return sorted(languages)


# =============================================================================
# Dynamic Prompt Builder (P1-28)
# =============================================================================


class DynamicPromptBuilder:
    """
    Builds prompts dynamically based on task context.

    P1-28: Add dynamic prompt adaptation per-task
    """

    def __init__(
        self,
        few_shot_selector: FewShotSelector | None = None,
        compressor: PromptCompressor | None = None,
        guard: PromptGuard | None = None,
        localization: PromptLocalization | None = None,
    ):
        self.few_shot_selector = few_shot_selector or FewShotSelector()
        self.compressor = compressor or PromptCompressor()
        self.guard = guard or PromptGuard()
        self.localization = localization or PromptLocalization()

    def classify_task(self, user_input: str) -> TaskType:
        """Classify the type of task from user input."""
        input_lower = user_input.lower()

        if any(kw in input_lower for kw in ["review", "check", "audit", "analyze"]):
            return TaskType.CODE_REVIEW
        if any(kw in input_lower for kw in ["fix", "bug", "error", "issue", "broken"]):
            return TaskType.BUG_FIX
        if any(kw in input_lower for kw in ["refactor", "clean", "improve", "optimize"]):
            return TaskType.REFACTORING
        if any(kw in input_lower for kw in ["document", "docstring", "comment", "readme"]):
            return TaskType.DOCUMENTATION
        if any(kw in input_lower for kw in ["test", "spec", "unittest", "pytest"]):
            return TaskType.TESTING
        if any(kw in input_lower for kw in ["explain", "understand", "what does", "how does"]):
            return TaskType.EXPLANATION
        if any(kw in input_lower for kw in ["architect", "design", "structure", "plan"]):
            return TaskType.ARCHITECTURE
        if any(kw in input_lower for kw in ["debug", "trace", "investigate", "why"]):
            return TaskType.DEBUGGING
        if any(kw in input_lower for kw in ["create", "write", "implement", "add", "build"]):
            return TaskType.CODE_GENERATION

        return TaskType.GENERAL

    def build(
        self,
        user_input: str,
        system_prompt: str = "",
        context: dict[str, Any] | None = None,
        style: PromptStyle = PromptStyle.DETAILED,
        max_tokens: int | None = None,
        language: str | None = None,
    ) -> str:
        """Build a complete prompt dynamically."""
        context = context or {}

        # Classify task
        task_type = self.classify_task(user_input)

        # Check for injection
        is_safe, _ = self.guard.check(user_input)
        if not is_safe:
            user_input = self.guard.sanitize(user_input)

        # Select few-shot examples
        examples = self.few_shot_selector.select(
            user_input,
            task_type=task_type,
            language=context.get("language"),
            max_examples=2 if max_tokens and max_tokens < 8000 else 3,
        )

        # Build prompt parts
        parts = []

        # System prompt
        if system_prompt:
            parts.append(system_prompt)

        # Task-specific instructions
        task_instructions = self._get_task_instructions(task_type, style)
        if task_instructions:
            parts.append(task_instructions)

        # Few-shot examples
        if examples:
            parts.append(self.few_shot_selector.format_examples(examples))

        # User input (wrapped for safety)
        parts.append(self.guard.wrap_user_input(user_input))

        # Combine
        prompt = "\n\n".join(parts)

        # Compress if needed
        if max_tokens:
            estimated_tokens = len(prompt) // 4
            if estimated_tokens > max_tokens * 0.8:
                prompt, _ = self.compressor.compress(prompt)

        return prompt

    def _get_task_instructions(self, task_type: TaskType, style: PromptStyle) -> str:
        """Get task-specific instructions."""
        instructions = {
            TaskType.CODE_GENERATION: "Generate clean, well-documented code. Include error handling.",
            TaskType.CODE_REVIEW: "Review the code for bugs, security issues, and style. Provide specific suggestions.",
            TaskType.BUG_FIX: "Identify the root cause and provide a minimal fix. Explain the issue.",
            TaskType.REFACTORING: "Improve code structure while preserving functionality. Document changes.",
            TaskType.DOCUMENTATION: "Write clear, concise documentation. Include examples where helpful.",
            TaskType.TESTING: "Write comprehensive tests covering edge cases. Use appropriate assertions.",
            TaskType.EXPLANATION: "Explain clearly and concisely. Use examples to illustrate concepts.",
            TaskType.ARCHITECTURE: "Consider scalability, maintainability, and best practices.",
            TaskType.DEBUGGING: "Trace through the code systematically. Identify potential causes.",
            TaskType.GENERAL: "",
        }

        base = instructions.get(task_type, "")

        if style == PromptStyle.CONCISE:
            return f"{base} Be brief."
        elif style == PromptStyle.STEP_BY_STEP:
            return f"{base} Work through this step by step."
        elif style == PromptStyle.TECHNICAL:
            return f"{base} Use technical terminology. Assume expert knowledge."
        elif style == PromptStyle.BEGINNER:
            return f"{base} Explain simply. Define any technical terms."

        return base
