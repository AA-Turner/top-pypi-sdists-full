"""
Token estimation and management for SAGE.

P1-21: Add token estimation before inference
P1-22: Implement generation caching
P1-23: Add cost tracking per model/provider
P1-55: Token usage display before/after operations
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

# =============================================================================
# Token Estimation (P1-21)
# =============================================================================


@dataclass
class TokenEstimate:
    """Estimated token count with breakdown."""

    total: int
    breakdown: dict[str, int] = field(default_factory=dict)
    method: str = "character_ratio"
    confidence: float = 0.8

    def __str__(self) -> str:
        return f"~{self.total:,} tokens ({self.method}, {self.confidence:.0%} confidence)"


class TokenEstimator:
    """
    Estimates token counts for different content types.

    Different models have different tokenization schemes, so we use
    heuristics calibrated for common models.
    """

    # Average characters per token for different languages
    CHARS_PER_TOKEN = {
        "english": 4.0,
        "code": 3.5,  # Code tends to be denser
        "mixed": 3.8,
        "json": 3.0,  # JSON has many special tokens
        "markdown": 4.2,
    }

    # Model-specific adjustments (multipliers)
    MODEL_ADJUSTMENTS = {
        "gpt-4": 1.0,
        "gpt-3.5": 1.0,
        "claude": 0.95,  # Claude tends to be slightly more efficient
        "llama": 1.1,  # LLaMA often tokenizes less efficiently
        "gemini": 0.98,
        "default": 1.0,
    }

    # Overhead tokens per message
    MESSAGE_OVERHEAD = 4  # Role, formatting, etc.

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or "default"
        self._adjustment = self._get_model_adjustment(model_name)

    def _get_model_adjustment(self, model_name: str | None) -> float:
        """Get adjustment factor for model."""
        if not model_name:
            return 1.0

        model_lower = model_name.lower()
        for key, adj in self.MODEL_ADJUSTMENTS.items():
            if key in model_lower:
                return adj
        return 1.0

    def _detect_content_type(self, text: str) -> str:
        """Detect the type of content for better estimation."""
        # Check for code patterns
        code_patterns = [
            r"^\s*(def |class |import |from |function |const |let |var )",
            r"[{}()\[\]];",
            r"^\s*#include",
            r"^\s*package ",
        ]
        for pattern in code_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return "code"

        # Check for JSON
        if text.strip().startswith("{") or text.strip().startswith("["):
            try:
                json.loads(text)
                return "json"
            except json.JSONDecodeError:
                pass

        # Check for Markdown
        if re.search(r"^#{1,6}\s|^\*\*|^\-\s|^```", text, re.MULTILINE):
            return "markdown"

        return "english"

    def estimate(self, text: str) -> TokenEstimate:
        """Estimate token count for text."""
        if not text:
            return TokenEstimate(total=0, method="empty")

        content_type = self._detect_content_type(text)
        chars_per_token = self.CHARS_PER_TOKEN.get(content_type, 4.0)

        # Base estimate
        raw_estimate = len(text) / chars_per_token

        # Apply model adjustment
        adjusted = raw_estimate * self._adjustment

        # Add overhead for newlines (often tokenized separately)
        newline_count = text.count("\n")
        with_newlines = adjusted + (newline_count * 0.5)

        # Round up to be conservative
        total = int(with_newlines) + 1

        return TokenEstimate(
            total=total,
            breakdown={
                "characters": len(text),
                "newlines": newline_count,
                "content_type": content_type,
                "chars_per_token": chars_per_token,
            },
            method=f"{content_type}_ratio",
            confidence=0.85 if content_type in ["code", "json"] else 0.75,
        )

    def estimate_messages(self, messages: list[dict[str, str]]) -> TokenEstimate:
        """Estimate total tokens for a list of messages."""
        total = 0
        breakdown = {"messages": len(messages)}

        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "user")

            # Content tokens
            content_est = self.estimate(content)
            total += content_est.total

            # Message overhead (role, formatting)
            total += self.MESSAGE_OVERHEAD

            breakdown[f"{role}_tokens"] = breakdown.get(f"{role}_tokens", 0) + content_est.total

        return TokenEstimate(
            total=total,
            breakdown=breakdown,
            method="message_sum",
            confidence=0.7,
        )

    def will_fit(
        self, text: str, max_tokens: int, buffer: float = 0.1
    ) -> tuple[bool, TokenEstimate]:
        """Check if text will fit within token limit with buffer."""
        estimate = self.estimate(text)
        effective_limit = int(max_tokens * (1 - buffer))
        fits = estimate.total <= effective_limit
        return fits, estimate


# =============================================================================
# Generation Cache (P1-22)
# =============================================================================


@dataclass
class CacheEntry:
    """Cached generation result."""

    content: str
    tokens_used: int
    model: str
    created_at: float
    hits: int = 0
    last_accessed: float = field(default_factory=time.time)


class GenerationCache:
    """
    Cache for model generations to reduce API costs.

    Uses content-addressable storage with LRU eviction.
    """

    def __init__(
        self,
        max_entries: int = 1000,
        max_age_seconds: int = 3600,
        cache_dir: Path | None = None,
    ):
        self.max_entries = max_entries
        self.max_age = max_age_seconds
        self.cache_dir = cache_dir
        self._cache: dict[str, CacheEntry] = {}
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}

        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
            self._load_persistent_cache()

    def _hash_key(self, prompt: str, model: str, params: dict[str, Any]) -> str:
        """Create hash key for cache lookup."""
        key_data = {
            "prompt": prompt,
            "model": model,
            "temperature": params.get("temperature", 0),
            "max_tokens": params.get("max_tokens", 0),
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()[:16]

    def get(self, prompt: str, model: str, params: dict | None = None) -> str | None:
        """Get cached generation if available."""
        params = params or {}
        key = self._hash_key(prompt, model, params)

        if key in self._cache:
            entry = self._cache[key]

            # Check if expired
            if time.time() - entry.created_at > self.max_age:
                del self._cache[key]
                self._stats["evictions"] += 1
                self._stats["misses"] += 1
                return None

            # Update access stats
            entry.hits += 1
            entry.last_accessed = time.time()
            self._stats["hits"] += 1
            return entry.content

        self._stats["misses"] += 1
        return None

    def put(
        self,
        prompt: str,
        model: str,
        result: str,
        tokens_used: int,
        params: dict | None = None,
    ) -> None:
        """Cache a generation result."""
        params = params or {}
        key = self._hash_key(prompt, model, params)

        # Evict if at capacity
        if len(self._cache) >= self.max_entries:
            self._evict_lru()

        self._cache[key] = CacheEntry(
            content=result,
            tokens_used=tokens_used,
            model=model,
            created_at=time.time(),
        )

        if self.cache_dir:
            self._persist_entry(key)

    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if not self._cache:
            return

        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].last_accessed)
        del self._cache[oldest_key]
        self._stats["evictions"] += 1

    def _persist_entry(self, key: str) -> None:
        """Persist cache entry to disk."""
        if not self.cache_dir:
            return

        entry = self._cache[key]
        entry_file = self.cache_dir / f"{key}.json"
        entry_file.write_text(
            json.dumps(
                {
                    "content": entry.content,
                    "tokens_used": entry.tokens_used,
                    "model": entry.model,
                    "created_at": entry.created_at,
                }
            )
        )

    def _load_persistent_cache(self) -> None:
        """Load cache from disk."""
        if not self.cache_dir:
            return

        for entry_file in self.cache_dir.glob("*.json"):
            try:
                data = json.loads(entry_file.read_text(encoding="utf-8", errors="replace"))
                if time.time() - data["created_at"] <= self.max_age:
                    self._cache[entry_file.stem] = CacheEntry(**data)
            except (json.JSONDecodeError, KeyError):
                entry_file.unlink()  # Remove invalid cache files

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0

        return {
            "entries": len(self._cache),
            "max_entries": self.max_entries,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "evictions": self._stats["evictions"],
            "hit_rate": hit_rate,
        }

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        if self.cache_dir:
            for f in self.cache_dir.glob("*.json"):
                f.unlink()


# =============================================================================
# Cost Tracking (P1-23)
# =============================================================================


@dataclass
class ModelPricing:
    """Pricing information for a model."""

    input_cost_per_1k: float  # Cost per 1000 input tokens
    output_cost_per_1k: float  # Cost per 1000 output tokens
    currency: str = "USD"


@dataclass
class UsageRecord:
    """Record of a single API usage."""

    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    timestamp: float
    operation: str = "generate"


class CostTracker:
    """
    Tracks API usage costs per model and provider.

    Supports both known pricing and estimated costs.
    """

    # Known pricing (as of 2024)
    PRICING: dict[str, ModelPricing] = {
        # OpenAI
        "gpt-4o": ModelPricing(0.005, 0.015),
        "gpt-4-turbo": ModelPricing(0.01, 0.03),
        "gpt-4": ModelPricing(0.03, 0.06),
        "gpt-3.5-turbo": ModelPricing(0.0005, 0.0015),
        # Anthropic
        "claude-3-opus": ModelPricing(0.015, 0.075),
        "claude-3-sonnet": ModelPricing(0.003, 0.015),
        "claude-3-haiku": ModelPricing(0.00025, 0.00125),
        # Google
        "gemini-pro": ModelPricing(0.0005, 0.0015),
        "gemini-1.5-pro": ModelPricing(0.00125, 0.005),
        "gemini-1.5-flash": ModelPricing(0.000075, 0.0003),
        # Local models (free)
        "local": ModelPricing(0.0, 0.0),
        "ollama": ModelPricing(0.0, 0.0),
        "llama": ModelPricing(0.0, 0.0),
    }

    DEFAULT_PRICING = ModelPricing(0.001, 0.002)

    def __init__(self, budget_limit: float | None = None):
        self.budget_limit = budget_limit
        self.records: list[UsageRecord] = []
        self._session_start = time.time()

    def get_pricing(self, model: str) -> ModelPricing:
        """Get pricing for a model."""
        model_lower = model.lower()

        # Direct match
        if model_lower in self.PRICING:
            return self.PRICING[model_lower]

        # Partial match
        for key, pricing in self.PRICING.items():
            if key in model_lower:
                return pricing

        # Check if local model
        if any(local in model_lower for local in ["local", "ollama", "gguf", "llama.cpp"]):
            return ModelPricing(0.0, 0.0)

        return self.DEFAULT_PRICING

    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Calculate cost for a generation."""
        pricing = self.get_pricing(model)
        input_cost = (input_tokens / 1000) * pricing.input_cost_per_1k
        output_cost = (output_tokens / 1000) * pricing.output_cost_per_1k
        return input_cost + output_cost

    def record_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        operation: str = "generate",
    ) -> UsageRecord:
        """Record API usage and return the record."""
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        record = UsageRecord(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            timestamp=time.time(),
            operation=operation,
        )
        self.records.append(record)

        return record

    def get_session_cost(self) -> float:
        """Get total cost for current session."""
        return sum(r.cost for r in self.records)

    def get_cost_by_model(self) -> dict[str, float]:
        """Get cost breakdown by model."""
        by_model: dict[str, float] = {}
        for record in self.records:
            by_model[record.model] = by_model.get(record.model, 0) + record.cost
        return by_model

    def get_tokens_by_model(self) -> dict[str, dict[str, int]]:
        """Get token usage breakdown by model."""
        by_model: dict[str, dict[str, int]] = {}
        for record in self.records:
            if record.model not in by_model:
                by_model[record.model] = {"input": 0, "output": 0}
            by_model[record.model]["input"] += record.input_tokens
            by_model[record.model]["output"] += record.output_tokens
        return by_model

    def check_budget(self) -> tuple[bool, float]:
        """Check if within budget. Returns (within_budget, remaining)."""
        if self.budget_limit is None:
            return True, float("inf")

        current = self.get_session_cost()
        remaining = self.budget_limit - current
        return remaining > 0, remaining

    def get_summary(self) -> dict[str, Any]:
        """Get comprehensive usage summary."""
        return {
            "session_cost": self.get_session_cost(),
            "total_requests": len(self.records),
            "cost_by_model": self.get_cost_by_model(),
            "tokens_by_model": self.get_tokens_by_model(),
            "budget_limit": self.budget_limit,
            "budget_remaining": self.check_budget()[1] if self.budget_limit else None,
            "session_duration": time.time() - self._session_start,
        }

    def render_summary(self, console: Console | None = None) -> None:
        """Render cost summary to console."""
        if console is None:
            from sage.core.renderer import console as _default_console
            console = _default_console
        summary = self.get_summary()

        table = Table(title="Usage Summary")
        table.add_column("Model", style="cyan")
        table.add_column("Requests", justify="right")
        table.add_column("Input Tokens", justify="right")
        table.add_column("Output Tokens", justify="right")
        table.add_column("Cost", justify="right", style="green")

        by_model_tokens = summary["tokens_by_model"]
        by_model_cost = summary["cost_by_model"]

        for model in by_model_tokens:
            tokens = by_model_tokens[model]
            cost = by_model_cost.get(model, 0)
            requests = sum(1 for r in self.records if r.model == model)

            table.add_row(
                model,
                str(requests),
                f"{tokens['input']:,}",
                f"{tokens['output']:,}",
                f"${cost:.4f}",
            )

        # Total row
        total_input = sum(t["input"] for t in by_model_tokens.values())
        total_output = sum(t["output"] for t in by_model_tokens.values())
        table.add_row(
            "[bold]Total[/bold]",
            str(len(self.records)),
            f"{total_input:,}",
            f"{total_output:,}",
            f"[bold]${summary['session_cost']:.4f}[/bold]",
        )

        console.print(table)

        if summary["budget_limit"]:
            remaining = summary["budget_remaining"]
            pct_used = (summary["session_cost"] / summary["budget_limit"]) * 100
            color = "green" if pct_used < 80 else "yellow" if pct_used < 100 else "red"
            console.print(
                f"\nBudget: [bold {color}]${remaining:.4f}[/bold {color}] remaining ({pct_used:.1f}% used)"
            )


# =============================================================================
# Token Display Utilities (P0-15)
# =============================================================================


def display_token_estimate(
    estimate: TokenEstimate,
    max_tokens: int,
    console: Console | None = None,
) -> None:
    """Display token estimate with context window usage."""
    if console is None:
        from sage.core.renderer import console as _default_console
        console = _default_console

    usage_pct = (estimate.total / max_tokens) * 100
    color = "green" if usage_pct < 50 else "yellow" if usage_pct < 80 else "red"

    console.print(
        f"[dim]Tokens: ~{estimate.total:,} / {max_tokens:,} ({usage_pct:.1f}%)[/dim]", style=color
    )


def display_pre_generation_estimate(
    prompt: str,
    history_tokens: int,
    max_tokens: int,
    model: str,
    console: Console | None = None,
) -> None:
    """Display token estimate before generation."""
    if console is None:
        from sage.core.renderer import console as _default_console
        console = _default_console
    estimator = TokenEstimator(model)

    prompt_est = estimator.estimate(prompt)
    total = history_tokens + prompt_est.total

    console.print("\n[dim]─── Token Budget ───[/dim]")
    console.print(f"[dim]History: {history_tokens:,}[/dim]")
    console.print(f"[dim]Prompt:  ~{prompt_est.total:,}[/dim]")
    console.print(f"[dim]Total:   ~{total:,} / {max_tokens:,}[/dim]")

    remaining = max_tokens - total
    if remaining < 1000:
        console.print(
            f"[yellow]Warning: Only ~{remaining:,} tokens remaining for response[/yellow]"
        )


# =============================================================================
# Module-level instances
# =============================================================================

_default_estimator: TokenEstimator | None = None
_default_cache: GenerationCache | None = None
_default_tracker: CostTracker | None = None


def get_estimator(model: str | None = None) -> TokenEstimator:
    """Get token estimator instance."""
    global _default_estimator
    if _default_estimator is None or model:
        _default_estimator = TokenEstimator(model)
    return _default_estimator


def get_cache() -> GenerationCache:
    """Get generation cache instance."""
    global _default_cache
    if _default_cache is None:
        _default_cache = GenerationCache()
    return _default_cache


def get_tracker() -> CostTracker:
    """Get cost tracker instance."""
    global _default_tracker
    if _default_tracker is None:
        _default_tracker = CostTracker()
    return _default_tracker
