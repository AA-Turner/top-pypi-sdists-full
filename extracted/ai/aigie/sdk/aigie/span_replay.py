"""
Span Replay for re-running LLM calls with different parameters.

Provides the ability to capture LLM call parameters, replay them with
modifications, and compare outputs for debugging and optimization.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ReplayStatus(Enum):
    """Status of a replay attempt."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ComparisonResult(Enum):
    """Result of comparing two outputs."""

    IDENTICAL = "identical"
    SIMILAR = "similar"
    DIFFERENT = "different"
    ERROR = "error"


@dataclass
class CapturedSpan:
    """A captured LLM span that can be replayed."""

    id: str
    trace_id: str
    name: str

    # Model configuration
    model: str
    provider: str

    # Input
    messages: list[dict[str, Any]]
    system_prompt: str | None = None

    # Parameters
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] = field(default_factory=list)
    extra_params: dict[str, Any] = field(default_factory=dict)

    # Original output
    output: str | None = None
    output_tokens: int = 0
    input_tokens: int = 0

    # Timing
    latency_ms: float = 0.0
    captured_at: datetime = field(default_factory=datetime.utcnow)

    # Metadata
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_hash(self) -> str:
        """Get a hash of the input parameters."""
        content = json.dumps(
            {
                "messages": self.messages,
                "system_prompt": self.system_prompt,
                "model": self.model,
            },
            sort_keys=True,
        )
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "trace_id": self.trace_id,
            "name": self.name,
            "model": self.model,
            "provider": self.provider,
            "messages": self.messages,
            "system_prompt": self.system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stop_sequences": self.stop_sequences,
            "extra_params": self.extra_params,
            "output": self.output,
            "output_tokens": self.output_tokens,
            "input_tokens": self.input_tokens,
            "latency_ms": self.latency_ms,
            "captured_at": self.captured_at.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
            "hash": self.get_hash(),
        }


@dataclass
class ReplayResult:
    """Result of replaying a span."""

    id: str
    span_id: str
    status: ReplayStatus

    # Modified parameters
    modified_params: dict[str, Any]

    # New output
    output: str | None = None
    output_tokens: int = 0
    input_tokens: int = 0

    # Timing
    latency_ms: float = 0.0
    replayed_at: datetime = field(default_factory=datetime.utcnow)

    # Comparison with original
    comparison: ComparisonResult | None = None
    similarity_score: float | None = None
    differences: list[str] = field(default_factory=list)

    # Error info
    error: str | None = None
    error_type: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "span_id": self.span_id,
            "status": self.status.value,
            "modified_params": self.modified_params,
            "output": self.output,
            "output_tokens": self.output_tokens,
            "input_tokens": self.input_tokens,
            "latency_ms": self.latency_ms,
            "replayed_at": self.replayed_at.isoformat(),
            "comparison": self.comparison.value if self.comparison else None,
            "similarity_score": self.similarity_score,
            "differences": self.differences,
            "error": self.error,
            "error_type": self.error_type,
        }


@dataclass
class ReplayExperiment:
    """A set of replays comparing different configurations."""

    id: str
    name: str
    description: str | None
    span_id: str
    original_span: CapturedSpan

    # Variations to test
    variations: list[dict[str, Any]] = field(default_factory=list)

    # Results
    results: list[ReplayResult] = field(default_factory=list)

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    created_by: str | None = None

    def get_summary(self) -> dict[str, Any]:
        """Get summary statistics for the experiment."""
        if not self.results:
            return {"num_variations": len(self.variations), "completed": 0}

        successful = [r for r in self.results if r.status == ReplayStatus.SUCCESS]

        return {
            "id": self.id,
            "name": self.name,
            "num_variations": len(self.variations),
            "completed": len(self.results),
            "successful": len(successful),
            "avg_latency_ms": sum(r.latency_ms for r in successful) / len(successful)
            if successful
            else 0,
            "avg_similarity": sum(r.similarity_score or 0 for r in successful) / len(successful)
            if successful
            else 0,
            "identical_count": sum(
                1 for r in successful if r.comparison == ComparisonResult.IDENTICAL
            ),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "span_id": self.span_id,
            "original_span": self.original_span.to_dict(),
            "variations": self.variations,
            "results": [r.to_dict() for r in self.results],
            "summary": self.get_summary(),
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_by": self.created_by,
        }


class SpanReplay:
    """
    System for capturing and replaying LLM spans.

    Usage:
        replay = SpanReplay(client)

        # Capture a span from a trace
        span = await replay.capture_from_trace(trace_id="trace_123", span_name="llm_call")

        # Replay with different temperature
        result = await replay.replay(
            span_id=span.id,
            temperature=0.0,  # Make deterministic
        )

        # Compare outputs
        comparison = replay.compare_outputs(span.output, result.output)

        # Run an experiment with multiple variations
        experiment = await replay.run_experiment(
            span_id=span.id,
            name="Temperature sweep",
            variations=[
                {"temperature": 0.0},
                {"temperature": 0.5},
                {"temperature": 1.0},
            ]
        )
    """

    def __init__(self, client: Any | None = None):
        self._client = client
        self._captured_spans: dict[str, CapturedSpan] = {}
        self._replay_results: list[ReplayResult] = []
        self._experiments: dict[str, ReplayExperiment] = {}

        # Model handlers for replay
        self._model_handlers: dict[str, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default model handlers for replay."""

        async def openai_handler(
            messages: list[dict],
            model: str,
            **params,
        ) -> dict[str, Any]:
            # Placeholder - would use actual OpenAI client
            return {
                "content": f"[OpenAI {model} replay response]",
                "input_tokens": 100,
                "output_tokens": 50,
            }

        async def anthropic_handler(
            messages: list[dict],
            model: str,
            **params,
        ) -> dict[str, Any]:
            # Placeholder - would use actual Anthropic client
            return {
                "content": f"[Anthropic {model} replay response]",
                "input_tokens": 100,
                "output_tokens": 50,
            }

        self._model_handlers["openai"] = openai_handler
        self._model_handlers["anthropic"] = anthropic_handler

    def register_model_handler(
        self,
        provider: str,
        handler: Callable,
    ):
        """Register a custom model handler for replay."""
        self._model_handlers[provider] = handler

    # =========================================================================
    # Span Capture
    # =========================================================================

    def capture(
        self,
        name: str,
        model: str,
        provider: str,
        messages: list[dict[str, Any]],
        output: str,
        trace_id: str | None = None,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: float = 0.0,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        **extra_params,
    ) -> CapturedSpan:
        """Capture a span for later replay."""
        span = CapturedSpan(
            id=str(uuid4()),
            trace_id=trace_id or str(uuid4()),
            name=name,
            model=model,
            provider=provider,
            messages=messages,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            output=output,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            tags=tags or [],
            metadata=metadata or {},
            extra_params=extra_params,
        )

        self._captured_spans[span.id] = span
        return span

    async def capture_from_trace(
        self,
        trace_id: str,
        span_name: str | None = None,
        span_type: str = "generation",
    ) -> CapturedSpan | None:
        """Capture a span from an existing trace."""
        # In production, would fetch from the client's API
        # For now, return a placeholder
        if self._client:
            # Would call: trace = await self._client.api.trace.get(trace_id)
            # Then find the span and capture it
            pass

        return None

    def get_span(self, span_id: str) -> CapturedSpan | None:
        """Get a captured span by ID."""
        return self._captured_spans.get(span_id)

    def list_spans(
        self,
        model: str | None = None,
        provider: str | None = None,
        tags: list[str] | None = None,
        limit: int = 100,
    ) -> list[CapturedSpan]:
        """List captured spans with optional filtering."""
        spans = list(self._captured_spans.values())

        if model:
            spans = [s for s in spans if s.model == model]

        if provider:
            spans = [s for s in spans if s.provider == provider]

        if tags:
            spans = [s for s in spans if any(t in s.tags for t in tags)]

        return sorted(spans, key=lambda s: s.captured_at, reverse=True)[:limit]

    def delete_span(self, span_id: str) -> bool:
        """Delete a captured span."""
        if span_id in self._captured_spans:
            del self._captured_spans[span_id]
            return True
        return False

    # =========================================================================
    # Replay Execution
    # =========================================================================

    async def replay(
        self,
        span_id: str,
        model: str | None = None,
        provider: str | None = None,
        messages: list[dict] | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        timeout_seconds: int = 60,
        compare_output: bool = True,
        **extra_params,
    ) -> ReplayResult:
        """
        Replay a captured span with optional parameter modifications.

        Args:
            span_id: ID of the captured span to replay
            model: Override the model
            provider: Override the provider
            messages: Override the messages
            system_prompt: Override the system prompt
            temperature: Override temperature
            max_tokens: Override max tokens
            top_p: Override top_p
            timeout_seconds: Timeout for the replay
            compare_output: Whether to compare with original output
            **extra_params: Additional parameters to override

        Returns:
            ReplayResult with the new output and comparison
        """
        span = self._captured_spans.get(span_id)
        if not span:
            return ReplayResult(
                id=str(uuid4()),
                span_id=span_id,
                status=ReplayStatus.FAILURE,
                modified_params={},
                error="Span not found",
                error_type="NotFoundError",
            )

        # Build modified parameters
        modified = {}
        if model is not None:
            modified["model"] = model
        if provider is not None:
            modified["provider"] = provider
        if messages is not None:
            modified["messages"] = messages
        if system_prompt is not None:
            modified["system_prompt"] = system_prompt
        if temperature is not None:
            modified["temperature"] = temperature
        if max_tokens is not None:
            modified["max_tokens"] = max_tokens
        if top_p is not None:
            modified["top_p"] = top_p
        modified.update(extra_params)

        # Merge with original parameters
        replay_params = {
            "model": modified.get("model", span.model),
            "provider": modified.get("provider", span.provider),
            "messages": modified.get("messages", span.messages),
            "system_prompt": modified.get("system_prompt", span.system_prompt),
            "temperature": modified.get("temperature", span.temperature),
            "max_tokens": modified.get("max_tokens", span.max_tokens),
            "top_p": modified.get("top_p", span.top_p),
        }

        # Execute replay
        result_id = str(uuid4())
        start_time = time.time()

        try:
            handler = self._model_handlers.get(replay_params["provider"])
            if not handler:
                raise ValueError(f"No handler for provider: {replay_params['provider']}")

            # Build messages with system prompt
            messages_to_send = []
            if replay_params["system_prompt"]:
                messages_to_send.append(
                    {
                        "role": "system",
                        "content": replay_params["system_prompt"],
                    }
                )
            messages_to_send.extend(replay_params["messages"])

            # Call the model handler with timeout
            response = await asyncio.wait_for(
                handler(
                    messages=messages_to_send,
                    model=replay_params["model"],
                    temperature=replay_params["temperature"],
                    max_tokens=replay_params["max_tokens"],
                    top_p=replay_params["top_p"],
                ),
                timeout=timeout_seconds,
            )

            latency_ms = (time.time() - start_time) * 1000

            result = ReplayResult(
                id=result_id,
                span_id=span_id,
                status=ReplayStatus.SUCCESS,
                modified_params=modified,
                output=response.get("content"),
                output_tokens=response.get("output_tokens", 0),
                input_tokens=response.get("input_tokens", 0),
                latency_ms=latency_ms,
            )

            # Compare with original if requested
            if compare_output and span.output and result.output:
                comparison, score, diffs = self._compare_outputs(
                    span.output,
                    result.output,
                )
                result.comparison = comparison
                result.similarity_score = score
                result.differences = diffs

        except asyncio.TimeoutError:
            result = ReplayResult(
                id=result_id,
                span_id=span_id,
                status=ReplayStatus.TIMEOUT,
                modified_params=modified,
                error=f"Replay timed out after {timeout_seconds}s",
                error_type="TimeoutError",
                latency_ms=(time.time() - start_time) * 1000,
            )
        except Exception as e:
            result = ReplayResult(
                id=result_id,
                span_id=span_id,
                status=ReplayStatus.FAILURE,
                modified_params=modified,
                error=str(e),
                error_type=type(e).__name__,
                latency_ms=(time.time() - start_time) * 1000,
            )

        self._replay_results.append(result)
        return result

    async def replay_batch(
        self,
        span_id: str,
        variations: list[dict[str, Any]],
        parallel: bool = True,
    ) -> list[ReplayResult]:
        """Replay a span with multiple parameter variations."""
        if parallel:
            tasks = [self.replay(span_id=span_id, **variation) for variation in variations]
            return await asyncio.gather(*tasks)
        results = []
        for variation in variations:
            result = await self.replay(span_id=span_id, **variation)
            results.append(result)
        return results

    # =========================================================================
    # Output Comparison
    # =========================================================================

    def _compare_outputs(
        self,
        original: str,
        replayed: str,
    ) -> tuple[ComparisonResult, float, list[str]]:
        """Compare two outputs and return comparison result, similarity score, and differences."""
        if original == replayed:
            return ComparisonResult.IDENTICAL, 1.0, []

        # Calculate similarity using simple ratio
        # In production, could use more sophisticated methods
        from difflib import SequenceMatcher, unified_diff

        similarity = SequenceMatcher(None, original, replayed).ratio()

        # Get differences
        original_lines = original.splitlines()
        replayed_lines = replayed.splitlines()
        diff = list(
            unified_diff(
                original_lines,
                replayed_lines,
                fromfile="original",
                tofile="replayed",
                lineterm="",
            )
        )

        if similarity > 0.9:
            return ComparisonResult.SIMILAR, similarity, diff
        return ComparisonResult.DIFFERENT, similarity, diff

    def compare_outputs(
        self,
        output_a: str,
        output_b: str,
    ) -> dict[str, Any]:
        """Compare two outputs and return detailed comparison."""
        comparison, similarity, diffs = self._compare_outputs(output_a, output_b)

        return {
            "comparison": comparison.value,
            "similarity_score": similarity,
            "identical": comparison == ComparisonResult.IDENTICAL,
            "differences": diffs,
            "length_a": len(output_a),
            "length_b": len(output_b),
            "length_diff": len(output_b) - len(output_a),
        }

    # =========================================================================
    # Experiments
    # =========================================================================

    async def run_experiment(
        self,
        span_id: str,
        name: str,
        variations: list[dict[str, Any]],
        description: str | None = None,
        parallel: bool = True,
        created_by: str | None = None,
    ) -> ReplayExperiment:
        """
        Run a replay experiment with multiple variations.

        Args:
            span_id: ID of the span to replay
            name: Name of the experiment
            variations: List of parameter variations to test
            description: Optional description
            parallel: Whether to run variations in parallel
            created_by: User who created the experiment

        Returns:
            ReplayExperiment with all results
        """
        span = self._captured_spans.get(span_id)
        if not span:
            raise ValueError(f"Span {span_id} not found")

        experiment = ReplayExperiment(
            id=str(uuid4()),
            name=name,
            description=description,
            span_id=span_id,
            original_span=span,
            variations=variations,
            created_by=created_by,
        )

        # Run all variations
        results = await self.replay_batch(span_id, variations, parallel=parallel)
        experiment.results = results
        experiment.completed_at = datetime.utcnow()

        self._experiments[experiment.id] = experiment
        return experiment

    async def run_temperature_sweep(
        self,
        span_id: str,
        temperatures: list[float] | None = None,
        name: str = "Temperature Sweep",
    ) -> ReplayExperiment:
        """Run an experiment sweeping through different temperatures."""
        if temperatures is None:
            temperatures = [0.0, 0.3, 0.5, 0.7, 1.0]

        variations = [{"temperature": t} for t in temperatures]
        return await self.run_experiment(
            span_id=span_id,
            name=name,
            variations=variations,
            description=f"Temperature sweep: {temperatures}",
        )

    async def run_model_comparison(
        self,
        span_id: str,
        models: list[tuple[str, str]],  # List of (provider, model) tuples
        name: str = "Model Comparison",
    ) -> ReplayExperiment:
        """Run an experiment comparing different models."""
        variations = [{"provider": provider, "model": model} for provider, model in models]
        return await self.run_experiment(
            span_id=span_id,
            name=name,
            variations=variations,
            description=f"Model comparison: {models}",
        )

    def get_experiment(self, experiment_id: str) -> ReplayExperiment | None:
        """Get an experiment by ID."""
        return self._experiments.get(experiment_id)

    def list_experiments(
        self,
        span_id: str | None = None,
        limit: int = 100,
    ) -> list[ReplayExperiment]:
        """List experiments with optional filtering."""
        experiments = list(self._experiments.values())

        if span_id:
            experiments = [e for e in experiments if e.span_id == span_id]

        return sorted(experiments, key=lambda e: e.created_at, reverse=True)[:limit]

    # =========================================================================
    # Results Analysis
    # =========================================================================

    def get_replay_results(
        self,
        span_id: str | None = None,
        status: ReplayStatus | None = None,
        limit: int = 100,
    ) -> list[ReplayResult]:
        """Get replay results with optional filtering."""
        results = self._replay_results

        if span_id:
            results = [r for r in results if r.span_id == span_id]

        if status:
            results = [r for r in results if r.status == status]

        return results[-limit:]

    def get_best_result(
        self,
        span_id: str,
        metric: str = "latency_ms",
        minimize: bool = True,
    ) -> ReplayResult | None:
        """Get the best replay result for a span based on a metric."""
        results = [
            r
            for r in self._replay_results
            if r.span_id == span_id and r.status == ReplayStatus.SUCCESS
        ]

        if not results:
            return None

        if metric == "latency_ms":
            def key(r):
                return r.latency_ms
        elif metric == "similarity_score":
            def key(r):
                return r.similarity_score or 0
            minimize = False  # Higher is better
        elif metric == "output_tokens":
            def key(r):
                return r.output_tokens
        else:
            return results[0]

        return min(results, key=key) if minimize else max(results, key=key)

    def export_results(
        self,
        span_id: str | None = None,
        format: str = "json",
    ) -> str:
        """Export replay results to a format."""
        results = self.get_replay_results(span_id=span_id)
        data = [r.to_dict() for r in results]

        if format == "json":
            return json.dumps(data, indent=2)
        if format == "jsonl":
            return "\n".join(json.dumps(d) for d in data)
        raise ValueError(f"Unsupported format: {format}")


# Convenience function
def create_span_replay(client: Any | None = None) -> SpanReplay:
    """Create a new span replay instance."""
    return SpanReplay(client)
