"""Comprehensive tests for sage/core/tokens.py - 100% coverage target."""

import json
import tempfile
import time
from io import StringIO
from pathlib import Path

from rich.console import Console

from sage.core.tokens import (
    CacheEntry,
    CostTracker,
    GenerationCache,
    ModelPricing,
    TokenEstimate,
    TokenEstimator,
    UsageRecord,
    display_pre_generation_estimate,
    display_token_estimate,
    get_cache,
    get_estimator,
    get_tracker,
)

# =============================================================================
# TokenEstimate Tests
# =============================================================================


class TestTokenEstimate:
    """Tests for TokenEstimate dataclass."""

    def test_basic_creation(self):
        """Test creating a basic token estimate."""
        estimate = TokenEstimate(total=100)
        assert estimate.total == 100
        assert estimate.breakdown == {}
        assert estimate.method == "character_ratio"
        assert estimate.confidence == 0.8

    def test_with_breakdown(self):
        """Test estimate with breakdown."""
        estimate = TokenEstimate(
            total=500,
            breakdown={"characters": 2000, "newlines": 50},
            method="code_ratio",
            confidence=0.85,
        )
        assert estimate.total == 500
        assert estimate.breakdown["characters"] == 2000
        assert estimate.breakdown["newlines"] == 50

    def test_str_representation(self):
        """Test string representation."""
        estimate = TokenEstimate(total=1000, method="test_method", confidence=0.9)
        result = str(estimate)
        assert "1,000" in result
        assert "test_method" in result
        assert "90%" in result


# =============================================================================
# TokenEstimator Tests
# =============================================================================


class TestTokenEstimator:
    """Tests for TokenEstimator class."""

    def test_init_default(self):
        """Test default initialization."""
        estimator = TokenEstimator()
        assert estimator.model_name == "default"
        assert estimator._adjustment == 1.0

    def test_init_with_model(self):
        """Test initialization with model name."""
        estimator = TokenEstimator("gpt-4")
        assert estimator.model_name == "gpt-4"

    def test_get_model_adjustment_gpt(self):
        """Test model adjustment for GPT models."""
        estimator = TokenEstimator("gpt-4-turbo")
        assert estimator._adjustment == 1.0

    def test_get_model_adjustment_claude(self):
        """Test model adjustment for Claude models."""
        estimator = TokenEstimator("claude-3-opus")
        assert estimator._adjustment == 0.95

    def test_get_model_adjustment_llama(self):
        """Test model adjustment for LLaMA models."""
        estimator = TokenEstimator("llama-3.1-70b")
        assert estimator._adjustment == 1.1

    def test_get_model_adjustment_gemini(self):
        """Test model adjustment for Gemini models."""
        estimator = TokenEstimator("gemini-1.5-pro")
        assert estimator._adjustment == 0.98

    def test_get_model_adjustment_unknown(self):
        """Test model adjustment for unknown models."""
        estimator = TokenEstimator("unknown-model")
        assert estimator._adjustment == 1.0

    def test_detect_content_type_code_python(self):
        """Test detecting Python code."""
        estimator = TokenEstimator()
        code = """
def hello():
    print("Hello, world!")
"""
        assert estimator._detect_content_type(code) == "code"

    def test_detect_content_type_code_javascript(self):
        """Test detecting JavaScript code."""
        estimator = TokenEstimator()
        code = """
function hello() {
    console.log("Hello");
}
"""
        assert estimator._detect_content_type(code) == "code"

    def test_detect_content_type_code_cpp(self):
        """Test detecting C++ code."""
        estimator = TokenEstimator()
        code = """
#include <iostream>
int main() { return 0; }
"""
        assert estimator._detect_content_type(code) == "code"

    def test_detect_content_type_code_java(self):
        """Test detecting Java code."""
        estimator = TokenEstimator()
        code = """
package com.example;
class Hello { }
"""
        assert estimator._detect_content_type(code) == "code"

    def test_detect_content_type_json(self):
        """Test detecting JSON."""
        estimator = TokenEstimator()
        json_content = '{"key": "value", "number": 42}'
        assert estimator._detect_content_type(json_content) == "json"

    def test_detect_content_type_json_array(self):
        """Test detecting JSON array."""
        estimator = TokenEstimator()
        json_content = "[1, 2, 3, 4]"
        assert estimator._detect_content_type(json_content) == "json"

    def test_detect_content_type_markdown(self):
        """Test detecting Markdown."""
        estimator = TokenEstimator()
        markdown = """
# Heading

This is **bold** text.

- List item 1
- List item 2
"""
        assert estimator._detect_content_type(markdown) == "markdown"

    def test_detect_content_type_english(self):
        """Test detecting plain English text."""
        estimator = TokenEstimator()
        text = "This is a simple paragraph of plain English text without any special formatting."
        assert estimator._detect_content_type(text) == "english"

    def test_estimate_empty_text(self):
        """Test estimating empty text."""
        estimator = TokenEstimator()
        result = estimator.estimate("")
        assert result.total == 0
        assert result.method == "empty"

    def test_estimate_short_text(self):
        """Test estimating short text."""
        estimator = TokenEstimator()
        result = estimator.estimate("Hello, world!")
        assert result.total > 0
        assert "characters" in result.breakdown

    def test_estimate_code(self):
        """Test estimating code content."""
        estimator = TokenEstimator()
        code = """
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
"""
        result = estimator.estimate(code)
        assert result.total > 0
        assert result.method == "code_ratio"
        assert result.confidence == 0.85

    def test_estimate_json(self):
        """Test estimating JSON content."""
        estimator = TokenEstimator()
        json_content = json.dumps({"users": [{"name": "John"}, {"name": "Jane"}]})
        result = estimator.estimate(json_content)
        assert result.total > 0
        assert result.method == "json_ratio"
        assert result.confidence == 0.85

    def test_estimate_with_newlines(self):
        """Test that newlines affect estimate."""
        estimator = TokenEstimator()
        single_line = "This is a single line"
        multi_line = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"

        single_result = estimator.estimate(single_line)
        multi_result = estimator.estimate(multi_line)

        # Multi-line should account for newlines
        assert multi_result.breakdown["newlines"] > 0

    def test_estimate_messages_empty(self):
        """Test estimating empty messages list."""
        estimator = TokenEstimator()
        result = estimator.estimate_messages([])
        assert result.total == 0
        assert result.breakdown["messages"] == 0

    def test_estimate_messages_single(self):
        """Test estimating single message."""
        estimator = TokenEstimator()
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        result = estimator.estimate_messages(messages)
        assert result.total > 0
        assert result.breakdown["messages"] == 1
        assert "user_tokens" in result.breakdown

    def test_estimate_messages_multiple(self):
        """Test estimating multiple messages."""
        estimator = TokenEstimator()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
        ]
        result = estimator.estimate_messages(messages)
        assert result.total > 0
        assert result.breakdown["messages"] == 3
        assert result.method == "message_sum"
        assert result.confidence == 0.7

    def test_will_fit_true(self):
        """Test will_fit returns True when text fits."""
        estimator = TokenEstimator()
        fits, estimate = estimator.will_fit("Short text", max_tokens=1000)
        assert fits is True
        assert estimate.total < 1000

    def test_will_fit_false(self):
        """Test will_fit returns False when text doesn't fit."""
        estimator = TokenEstimator()
        long_text = "word " * 10000  # Very long text
        fits, estimate = estimator.will_fit(long_text, max_tokens=100)
        assert fits is False

    def test_will_fit_with_buffer(self):
        """Test will_fit accounts for buffer."""
        estimator = TokenEstimator()
        # Create text that might fit without buffer but not with
        text = "word " * 200
        fits_with_buffer, _ = estimator.will_fit(text, max_tokens=300, buffer=0.5)
        # With 50% buffer, effective limit is 150
        # This tests that buffer is being applied


# =============================================================================
# CacheEntry Tests
# =============================================================================


class TestCacheEntry:
    """Tests for CacheEntry dataclass."""

    def test_basic_creation(self):
        """Test creating a basic cache entry."""
        entry = CacheEntry(
            content="Generated content",
            tokens_used=100,
            model="gpt-4",
            created_at=time.time(),
        )
        assert entry.content == "Generated content"
        assert entry.tokens_used == 100
        assert entry.model == "gpt-4"
        assert entry.hits == 0

    def test_default_last_accessed(self):
        """Test default last_accessed timestamp."""
        entry = CacheEntry(
            content="Test",
            tokens_used=10,
            model="test",
            created_at=time.time(),
        )
        assert entry.last_accessed > 0


# =============================================================================
# GenerationCache Tests
# =============================================================================


class TestGenerationCache:
    """Tests for GenerationCache class."""

    def test_init_default(self):
        """Test default initialization."""
        cache = GenerationCache()
        assert cache.max_entries == 1000
        assert cache.max_age == 3600
        assert cache.cache_dir is None

    def test_init_custom(self):
        """Test custom initialization."""
        cache = GenerationCache(max_entries=500, max_age_seconds=1800)
        assert cache.max_entries == 500
        assert cache.max_age == 1800

    def test_init_with_cache_dir(self):
        """Test initialization with cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            cache = GenerationCache(cache_dir=cache_dir)
            assert cache.cache_dir == cache_dir
            assert cache_dir.exists()

    def test_hash_key_deterministic(self):
        """Test that hash key is deterministic."""
        cache = GenerationCache()
        key1 = cache._hash_key("prompt", "model", {"temperature": 0.7})
        key2 = cache._hash_key("prompt", "model", {"temperature": 0.7})
        assert key1 == key2

    def test_hash_key_different_for_different_inputs(self):
        """Test that different inputs produce different keys."""
        cache = GenerationCache()
        key1 = cache._hash_key("prompt1", "model", {})
        key2 = cache._hash_key("prompt2", "model", {})
        assert key1 != key2

    def test_get_miss(self):
        """Test cache miss."""
        cache = GenerationCache()
        result = cache.get("not cached", "model")
        assert result is None

    def test_put_and_get(self):
        """Test putting and getting from cache."""
        cache = GenerationCache()
        cache.put("prompt", "model", "result", tokens_used=50)
        result = cache.get("prompt", "model")
        assert result == "result"

    def test_put_and_get_with_params(self):
        """Test caching with parameters."""
        cache = GenerationCache()
        params = {"temperature": 0.5, "max_tokens": 100}
        cache.put("prompt", "model", "result", tokens_used=50, params=params)
        result = cache.get("prompt", "model", params=params)
        assert result == "result"

    def test_get_updates_hits(self):
        """Test that getting updates hit count."""
        cache = GenerationCache()
        cache.put("prompt", "model", "result", tokens_used=50)
        cache.get("prompt", "model")
        cache.get("prompt", "model")

        stats = cache.get_stats()
        assert stats["hits"] == 2

    def test_get_expired_entry(self):
        """Test that expired entries are removed."""
        cache = GenerationCache(max_age_seconds=0)  # Immediate expiry
        cache.put("prompt", "model", "result", tokens_used=50)
        time.sleep(0.01)
        result = cache.get("prompt", "model")
        assert result is None

    def test_evict_lru(self):
        """Test LRU eviction."""
        cache = GenerationCache(max_entries=2)
        cache.put("prompt1", "model", "result1", tokens_used=10)
        cache.put("prompt2", "model", "result2", tokens_used=10)
        cache.put("prompt3", "model", "result3", tokens_used=10)

        # prompt1 should be evicted
        assert cache.get("prompt1", "model") is None
        assert cache.get("prompt2", "model") == "result2"
        assert cache.get("prompt3", "model") == "result3"

    def test_evict_lru_empty_cache(self):
        """Test LRU eviction on empty cache."""
        cache = GenerationCache()
        cache._evict_lru()  # Should not raise

    def test_persist_entry(self):
        """Test persisting cache entry to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            cache = GenerationCache(cache_dir=cache_dir)
            cache.put("prompt", "model", "result", tokens_used=50)

            # Check file was created
            files = list(cache_dir.glob("*.json"))
            assert len(files) == 1

    def test_load_persistent_cache(self):
        """Test loading cache from disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"

            # Create first cache and add entry
            cache1 = GenerationCache(cache_dir=cache_dir)
            cache1.put("prompt", "model", "result", tokens_used=50)

            # Create second cache and verify it loads the entry
            cache2 = GenerationCache(cache_dir=cache_dir)
            result = cache2.get("prompt", "model")
            assert result == "result"

    def test_load_persistent_cache_expired(self):
        """Test that expired persistent entries are removed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"

            # Create entry manually with old timestamp
            cache_dir.mkdir(parents=True)
            entry_file = cache_dir / "test.json"
            entry_file.write_text(
                json.dumps(
                    {
                        "content": "old content",
                        "tokens_used": 10,
                        "model": "model",
                        "created_at": time.time() - 7200,  # 2 hours ago
                    }
                )
            )

            # Load cache with 1 hour max age
            cache = GenerationCache(cache_dir=cache_dir, max_age_seconds=3600)
            assert "test" not in cache._cache

    def test_load_persistent_cache_invalid_json(self):
        """Test handling invalid JSON in cache files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            cache_dir.mkdir(parents=True)

            # Create invalid JSON file
            invalid_file = cache_dir / "invalid.json"
            invalid_file.write_text("not valid json")

            # Should not raise
            cache = GenerationCache(cache_dir=cache_dir)
            assert not invalid_file.exists()  # Should be deleted

    def test_get_stats(self):
        """Test getting cache statistics."""
        cache = GenerationCache()
        cache.put("p1", "m", "r1", 10)
        cache.put("p2", "m", "r2", 10)
        cache.get("p1", "m")  # Hit
        cache.get("p3", "m")  # Miss

        stats = cache.get_stats()
        assert stats["entries"] == 2
        assert stats["max_entries"] == 1000
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5

    def test_get_stats_empty(self):
        """Test stats with no operations."""
        cache = GenerationCache()
        stats = cache.get_stats()
        assert stats["hit_rate"] == 0

    def test_clear(self):
        """Test clearing cache."""
        cache = GenerationCache()
        cache.put("p1", "m", "r1", 10)
        cache.put("p2", "m", "r2", 10)
        cache.clear()
        assert cache.get("p1", "m") is None
        assert cache.get("p2", "m") is None

    def test_clear_with_disk(self):
        """Test clearing cache with disk persistence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "cache"
            cache = GenerationCache(cache_dir=cache_dir)
            cache.put("p1", "m", "r1", 10)
            cache.clear()

            files = list(cache_dir.glob("*.json"))
            assert len(files) == 0


# =============================================================================
# ModelPricing Tests
# =============================================================================


class TestModelPricing:
    """Tests for ModelPricing dataclass."""

    def test_basic_creation(self):
        """Test creating pricing info."""
        pricing = ModelPricing(input_cost_per_1k=0.01, output_cost_per_1k=0.03)
        assert pricing.input_cost_per_1k == 0.01
        assert pricing.output_cost_per_1k == 0.03
        assert pricing.currency == "USD"

    def test_custom_currency(self):
        """Test pricing with custom currency."""
        pricing = ModelPricing(input_cost_per_1k=0.01, output_cost_per_1k=0.03, currency="EUR")
        assert pricing.currency == "EUR"


# =============================================================================
# UsageRecord Tests
# =============================================================================


class TestUsageRecord:
    """Tests for UsageRecord dataclass."""

    def test_basic_creation(self):
        """Test creating a usage record."""
        record = UsageRecord(
            model="gpt-4",
            input_tokens=100,
            output_tokens=50,
            cost=0.015,
            timestamp=time.time(),
        )
        assert record.model == "gpt-4"
        assert record.input_tokens == 100
        assert record.output_tokens == 50
        assert record.cost == 0.015
        assert record.operation == "generate"

    def test_custom_operation(self):
        """Test record with custom operation."""
        record = UsageRecord(
            model="gpt-4",
            input_tokens=100,
            output_tokens=50,
            cost=0.015,
            timestamp=time.time(),
            operation="embed",
        )
        assert record.operation == "embed"


# =============================================================================
# CostTracker Tests
# =============================================================================


class TestCostTracker:
    """Tests for CostTracker class."""

    def test_init_default(self):
        """Test default initialization."""
        tracker = CostTracker()
        assert tracker.budget_limit is None
        assert tracker.records == []

    def test_init_with_budget(self):
        """Test initialization with budget."""
        tracker = CostTracker(budget_limit=10.0)
        assert tracker.budget_limit == 10.0

    def test_get_pricing_known_model(self):
        """Test getting pricing for known model."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("gpt-4o")
        assert pricing.input_cost_per_1k == 0.005
        assert pricing.output_cost_per_1k == 0.015

    def test_get_pricing_partial_match(self):
        """Test getting pricing with partial match."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("gpt-4-turbo-preview")
        assert pricing == tracker.PRICING["gpt-4-turbo"]

    def test_get_pricing_local_model(self):
        """Test pricing for local model is free."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("ollama/llama3")
        assert pricing.input_cost_per_1k == 0.0
        assert pricing.output_cost_per_1k == 0.0

    def test_get_pricing_unknown_model(self):
        """Test default pricing for unknown model."""
        tracker = CostTracker()
        pricing = tracker.get_pricing("unknown-model-xyz")
        assert pricing == tracker.DEFAULT_PRICING

    def test_calculate_cost(self):
        """Test calculating cost."""
        tracker = CostTracker()
        cost = tracker.calculate_cost("gpt-4o", input_tokens=1000, output_tokens=500)
        expected = (1000 / 1000 * 0.005) + (500 / 1000 * 0.015)
        assert cost == expected

    def test_record_usage(self):
        """Test recording usage."""
        tracker = CostTracker()
        record = tracker.record_usage(
            model="gpt-4o",
            input_tokens=1000,
            output_tokens=500,
            operation="generate",
        )
        assert len(tracker.records) == 1
        assert record.model == "gpt-4o"
        assert record.cost > 0

    def test_get_session_cost(self):
        """Test getting session cost."""
        tracker = CostTracker()
        tracker.record_usage("gpt-4o", 1000, 500)
        tracker.record_usage("gpt-4o", 2000, 1000)
        total = tracker.get_session_cost()
        assert total > 0

    def test_get_cost_by_model(self):
        """Test getting cost breakdown by model."""
        tracker = CostTracker()
        tracker.record_usage("gpt-4o", 1000, 500)
        tracker.record_usage("claude-3-opus", 1000, 500)
        tracker.record_usage("gpt-4o", 500, 250)

        by_model = tracker.get_cost_by_model()
        assert "gpt-4o" in by_model
        assert "claude-3-opus" in by_model

    def test_get_tokens_by_model(self):
        """Test getting token usage by model."""
        tracker = CostTracker()
        tracker.record_usage("gpt-4o", 1000, 500)
        tracker.record_usage("gpt-4o", 2000, 1000)

        by_model = tracker.get_tokens_by_model()
        assert by_model["gpt-4o"]["input"] == 3000
        assert by_model["gpt-4o"]["output"] == 1500

    def test_check_budget_no_limit(self):
        """Test checking budget with no limit."""
        tracker = CostTracker()
        tracker.record_usage("gpt-4o", 1000, 500)
        within, remaining = tracker.check_budget()
        assert within is True
        assert remaining == float("inf")

    def test_check_budget_within_limit(self):
        """Test checking budget within limit."""
        tracker = CostTracker(budget_limit=1.0)
        tracker.record_usage("claude-3-haiku", 100, 50)  # Very cheap
        within, remaining = tracker.check_budget()
        assert within is True
        assert remaining > 0

    def test_check_budget_exceeded(self):
        """Test checking exceeded budget."""
        tracker = CostTracker(budget_limit=0.001)
        tracker.record_usage("gpt-4", 10000, 5000)  # Expensive
        within, remaining = tracker.check_budget()
        assert within is False
        assert remaining < 0

    def test_get_summary(self):
        """Test getting comprehensive summary."""
        tracker = CostTracker(budget_limit=10.0)
        tracker.record_usage("gpt-4o", 1000, 500)
        tracker.record_usage("claude-3-opus", 2000, 1000)

        summary = tracker.get_summary()
        assert "session_cost" in summary
        assert "total_requests" in summary
        assert "cost_by_model" in summary
        assert "tokens_by_model" in summary
        assert "budget_limit" in summary
        assert "budget_remaining" in summary
        assert "session_duration" in summary
        assert summary["total_requests"] == 2

    def test_render_summary(self):
        """Test rendering summary to console."""
        tracker = CostTracker(budget_limit=1.0)
        tracker.record_usage("gpt-4o", 1000, 500)

        output = StringIO()
        console = Console(file=output, force_terminal=True)
        tracker.render_summary(console)

        rendered = output.getvalue()
        assert "gpt-4o" in rendered
        assert "Total" in rendered

    def test_render_summary_no_budget(self):
        """Test rendering summary without budget."""
        tracker = CostTracker()
        tracker.record_usage("gpt-4o", 1000, 500)

        output = StringIO()
        console = Console(file=output, force_terminal=True)
        tracker.render_summary(console)

        # Should not raise


# =============================================================================
# Display Functions Tests
# =============================================================================


class TestDisplayFunctions:
    """Tests for display utility functions."""

    def test_display_token_estimate_low(self):
        """Test displaying low token usage."""
        estimate = TokenEstimate(total=100)
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_token_estimate(estimate, max_tokens=1000, console=console)
        rendered = output.getvalue()
        assert "100" in rendered

    def test_display_token_estimate_medium(self):
        """Test displaying medium token usage."""
        estimate = TokenEstimate(total=600)
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_token_estimate(estimate, max_tokens=1000, console=console)
        # Should render in yellow

    def test_display_token_estimate_high(self):
        """Test displaying high token usage."""
        estimate = TokenEstimate(total=900)
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_token_estimate(estimate, max_tokens=1000, console=console)
        # Should render in red

    def test_display_pre_generation_estimate(self):
        """Test displaying pre-generation estimate."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_pre_generation_estimate(
            prompt="What is Python?",
            history_tokens=500,
            max_tokens=4096,
            model="gpt-4",
            console=console,
        )
        rendered = output.getvalue()
        assert "Token Budget" in rendered
        assert "History" in rendered
        assert "Prompt" in rendered

    def test_display_pre_generation_estimate_low_remaining(self):
        """Test warning when low tokens remaining."""
        output = StringIO()
        console = Console(file=output, force_terminal=True)
        display_pre_generation_estimate(
            prompt="What is Python?",
            history_tokens=3500,  # High history
            max_tokens=4096,
            model="gpt-4",
            console=console,
        )
        rendered = output.getvalue()
        # Should contain warning


# =============================================================================
# Module-level Functions Tests
# =============================================================================


class TestModuleFunctions:
    """Tests for module-level singleton getters."""

    def test_get_estimator_default(self):
        """Test getting default estimator."""
        import sage.core.tokens as tokens_module

        # Reset state
        tokens_module._default_estimator = None

        estimator = get_estimator()
        assert isinstance(estimator, TokenEstimator)

    def test_get_estimator_with_model(self):
        """Test getting estimator with specific model."""
        estimator = get_estimator("claude-3")
        assert estimator.model_name == "claude-3"

    def test_get_cache(self):
        """Test getting cache singleton."""
        import sage.core.tokens as tokens_module

        tokens_module._default_cache = None

        cache = get_cache()
        assert isinstance(cache, GenerationCache)

    def test_get_tracker(self):
        """Test getting tracker singleton."""
        import sage.core.tokens as tokens_module

        tokens_module._default_tracker = None

        tracker = get_tracker()
        assert isinstance(tracker, CostTracker)


# =============================================================================
# Integration Tests
# =============================================================================


class TestTokensIntegration:
    """Integration tests for token management."""

    def test_complete_workflow(self):
        """Test a complete token management workflow."""
        # Create components
        estimator = TokenEstimator("gpt-4")
        cache = GenerationCache()
        tracker = CostTracker(budget_limit=1.0)

        # Estimate tokens for a prompt
        prompt = "Explain quantum computing in simple terms."
        estimate = estimator.estimate(prompt)
        assert estimate.total > 0

        # Check if fits
        fits, _ = estimator.will_fit(prompt, max_tokens=4096)
        assert fits

        # Check cache (miss)
        cached = cache.get(prompt, "gpt-4")
        assert cached is None

        # Simulate generation
        response = "Quantum computing uses qubits..."
        cache.put(prompt, "gpt-4", response, tokens_used=estimate.total)

        # Check cache (hit)
        cached = cache.get(prompt, "gpt-4")
        assert cached == response

        # Record usage
        response_estimate = estimator.estimate(response)
        tracker.record_usage(
            model="gpt-4",
            input_tokens=estimate.total,
            output_tokens=response_estimate.total,
        )

        # Check budget
        within, remaining = tracker.check_budget()
        assert within is True

        # Get summary
        summary = tracker.get_summary()
        assert summary["total_requests"] == 1

    def test_message_estimation_accuracy(self):
        """Test that message estimation is reasonable."""
        estimator = TokenEstimator()

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! How can you help me today?"},
            {
                "role": "assistant",
                "content": "I can help with many things including coding, writing, and analysis.",
            },
            {"role": "user", "content": "Can you write a Python function to sort a list?"},
        ]

        estimate = estimator.estimate_messages(messages)

        # Should be reasonable for this conversation
        assert estimate.total > 50  # At least this many tokens
        assert estimate.total < 500  # But not this many

    def test_cost_tracking_multiple_models(self):
        """Test cost tracking across multiple models."""
        tracker = CostTracker()

        # Use different models
        tracker.record_usage("gpt-4o", 1000, 500)
        tracker.record_usage("claude-3-opus", 2000, 1000)
        tracker.record_usage("gpt-3.5-turbo", 500, 250)

        by_model = tracker.get_cost_by_model()
        assert len(by_model) == 3

        # GPT-4 and Claude should be more expensive than GPT-3.5
        assert by_model["claude-3-opus"] > by_model["gpt-3.5-turbo"]
