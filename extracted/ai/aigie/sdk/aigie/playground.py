"""
Playground infrastructure for prompt testing and iteration.

Provides programmatic access to test prompts against different models,
compare outputs, and iterate on prompt engineering without deploying.
"""

from __future__ import annotations

import asyncio
import builtins
import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ModelProvider(Enum):
    """Supported model providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    COHERE = "cohere"
    MISTRAL = "mistral"
    GROQ = "groq"
    TOGETHER = "together"
    CUSTOM = "custom"


@dataclass
class ModelConfig:
    """Configuration for a model."""

    provider: ModelProvider
    model_name: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: list[str] = field(default_factory=list)
    extra_params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider.value,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "stop_sequences": self.stop_sequences,
            **self.extra_params,
        }


@dataclass
class PromptTemplate:
    """A reusable prompt template with variable substitution."""

    id: str
    name: str
    template: str
    variables: list[str] = field(default_factory=list)
    system_prompt: str | None = None
    description: str | None = None
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self, **kwargs) -> str:
        """Render the template with provided variables."""
        result = self.template
        for var in self.variables:
            placeholder = f"{{{{{var}}}}}"
            if var in kwargs:
                result = result.replace(placeholder, str(kwargs[var]))
        return result

    def get_hash(self) -> str:
        """Get a hash of the template content for versioning."""
        content = f"{self.template}|{self.system_prompt or ''}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "template": self.template,
            "variables": self.variables,
            "system_prompt": self.system_prompt,
            "description": self.description,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
            "hash": self.get_hash(),
        }


@dataclass
class PlaygroundRun:
    """Result of a single playground execution."""

    id: str
    prompt_template_id: str | None
    model_config: ModelConfig
    input_variables: dict[str, Any]
    rendered_prompt: str
    system_prompt: str | None
    output: str
    latency_ms: float
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost_usd: float | None
    created_at: datetime = field(default_factory=datetime.utcnow)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "prompt_template_id": self.prompt_template_id,
            "model_config": self.model_config.to_dict(),
            "input_variables": self.input_variables,
            "rendered_prompt": self.rendered_prompt,
            "system_prompt": self.system_prompt,
            "output": self.output,
            "latency_ms": self.latency_ms,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "tokens_total": self.tokens_total,
            "cost_usd": self.cost_usd,
            "created_at": self.created_at.isoformat(),
            "error": self.error,
            "metadata": self.metadata,
        }


@dataclass
class ComparisonResult:
    """Result of comparing multiple model outputs."""

    id: str
    runs: list[PlaygroundRun]
    prompt_template: PromptTemplate | None
    input_variables: dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    winner: str | None = None  # run_id of the winning output
    scores: dict[str, dict[str, float]] = field(default_factory=dict)  # run_id -> metric -> score
    notes: str | None = None

    def get_summary(self) -> dict[str, Any]:
        """Get a summary comparison of all runs."""
        return {
            "id": self.id,
            "num_runs": len(self.runs),
            "models_compared": [r.model_config.model_name for r in self.runs],
            "avg_latency_ms": sum(r.latency_ms for r in self.runs) / len(self.runs)
            if self.runs
            else 0,
            "total_cost_usd": sum(r.cost_usd or 0 for r in self.runs),
            "winner": self.winner,
            "created_at": self.created_at.isoformat(),
        }


class PromptRegistry:
    """Registry for managing prompt templates."""

    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}
        self._versions: dict[str, list[PromptTemplate]] = {}  # template_id -> list of versions

    def register(self, template: PromptTemplate) -> PromptTemplate:
        """Register a new prompt template."""
        self._templates[template.id] = template

        # Track version history
        if template.id not in self._versions:
            self._versions[template.id] = []
        self._versions[template.id].append(template)

        return template

    def create(
        self,
        name: str,
        template: str,
        variables: builtins.list[str] | None = None,
        system_prompt: str | None = None,
        description: str | None = None,
        tags: builtins.list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PromptTemplate:
        """Create and register a new prompt template."""
        # Auto-detect variables if not provided
        if variables is None:
            import re

            variables = list(set(re.findall(r"\{\{(\w+)\}\}", template)))

        prompt = PromptTemplate(
            id=str(uuid4()),
            name=name,
            template=template,
            variables=variables,
            system_prompt=system_prompt,
            description=description,
            tags=tags or [],
            metadata=metadata or {},
        )
        return self.register(prompt)

    def get(self, template_id: str) -> PromptTemplate | None:
        """Get a template by ID."""
        return self._templates.get(template_id)

    def get_by_name(self, name: str) -> PromptTemplate | None:
        """Get a template by name."""
        for template in self._templates.values():
            if template.name == name:
                return template
        return None

    def list(
        self,
        tags: builtins.list[str] | None = None,
        search: str | None = None,
    ) -> builtins.list[PromptTemplate]:
        """List all templates, optionally filtered."""
        templates = list(self._templates.values())

        if tags:
            templates = [t for t in templates if any(tag in t.tags for tag in tags)]

        if search:
            search_lower = search.lower()
            templates = [
                t
                for t in templates
                if search_lower in t.name.lower()
                or search_lower in (t.description or "").lower()
                or search_lower in t.template.lower()
            ]

        return templates

    def update(
        self,
        template_id: str,
        template: str | None = None,
        system_prompt: str | None = None,
        description: str | None = None,
        tags: builtins.list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PromptTemplate | None:
        """Update a template and create a new version."""
        existing = self._templates.get(template_id)
        if not existing:
            return None

        # Create new version
        new_template = PromptTemplate(
            id=existing.id,
            name=existing.name,
            template=template if template is not None else existing.template,
            variables=existing.variables,
            system_prompt=system_prompt if system_prompt is not None else existing.system_prompt,
            description=description if description is not None else existing.description,
            version=existing.version + 1,
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
            tags=tags if tags is not None else existing.tags,
            metadata=metadata if metadata is not None else existing.metadata,
        )

        # Re-detect variables if template changed
        if template is not None:
            import re

            new_template.variables = list(set(re.findall(r"\{\{(\w+)\}\}", template)))

        return self.register(new_template)

    def get_versions(self, template_id: str) -> builtins.list[PromptTemplate]:
        """Get all versions of a template."""
        return self._versions.get(template_id, [])

    def delete(self, template_id: str) -> bool:
        """Delete a template."""
        if template_id in self._templates:
            del self._templates[template_id]
            if template_id in self._versions:
                del self._versions[template_id]
            return True
        return False


class Playground:
    """
    Interactive playground for testing prompts against different models.

    Usage:
        playground = Playground(client)

        # Create a prompt template
        template = playground.prompts.create(
            name="summarizer",
            template="Summarize the following text: {{text}}",
            system_prompt="You are a helpful assistant that creates concise summaries."
        )

        # Run against a model
        result = await playground.run(
            template=template,
            model=ModelConfig(provider=ModelProvider.OPENAI, model_name="gpt-4"),
            variables={"text": "Long article here..."}
        )

        # Compare models
        comparison = await playground.compare(
            template=template,
            models=[
                ModelConfig(provider=ModelProvider.OPENAI, model_name="gpt-4"),
                ModelConfig(provider=ModelProvider.ANTHROPIC, model_name="claude-3-opus"),
            ],
            variables={"text": "Long article here..."}
        )
    """

    def __init__(self, client: Any | None = None):
        self._client = client
        self.prompts = PromptRegistry()
        self._runs: list[PlaygroundRun] = []
        self._comparisons: list[ComparisonResult] = []
        self._model_handlers: dict[ModelProvider, Callable] = {}

        # Register default handlers
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default model handlers."""
        # These are placeholder implementations
        # In production, these would use actual API clients

        async def openai_handler(config: ModelConfig, messages: list[dict]) -> dict:
            # Placeholder - would use openai client
            return {
                "content": "[OpenAI response placeholder]",
                "tokens_input": 100,
                "tokens_output": 50,
            }

        async def anthropic_handler(config: ModelConfig, messages: list[dict]) -> dict:
            # Placeholder - would use anthropic client
            return {
                "content": "[Anthropic response placeholder]",
                "tokens_input": 100,
                "tokens_output": 50,
            }

        self._model_handlers[ModelProvider.OPENAI] = openai_handler
        self._model_handlers[ModelProvider.ANTHROPIC] = anthropic_handler

    def register_model_handler(
        self,
        provider: ModelProvider,
        handler: Callable[[ModelConfig, list[dict]], dict],
    ):
        """Register a custom model handler."""
        self._model_handlers[provider] = handler

    async def run(
        self,
        template: PromptTemplate | None = None,
        prompt: str | None = None,
        model: ModelConfig | None = None,
        variables: dict[str, Any] | None = None,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PlaygroundRun:
        """
        Run a prompt against a model.

        Args:
            template: Prompt template to use
            prompt: Raw prompt string (alternative to template)
            model: Model configuration
            variables: Variables to substitute in template
            system_prompt: System prompt override
            metadata: Additional metadata

        Returns:
            PlaygroundRun with the result
        """
        if template is None and prompt is None:
            raise ValueError("Either template or prompt must be provided")

        if model is None:
            model = ModelConfig(provider=ModelProvider.OPENAI, model_name="gpt-4")

        variables = variables or {}

        # Render prompt
        if template:
            rendered_prompt = template.render(**variables)
            final_system = system_prompt or template.system_prompt
        else:
            rendered_prompt = prompt
            final_system = system_prompt

        # Build messages
        messages = []
        if final_system:
            messages.append({"role": "system", "content": final_system})
        messages.append({"role": "user", "content": rendered_prompt})

        # Execute
        start_time = time.time()
        error = None
        output = ""
        tokens_input = 0
        tokens_output = 0

        try:
            handler = self._model_handlers.get(model.provider)
            if handler:
                result = await handler(model, messages)
                output = result.get("content", "")
                tokens_input = result.get("tokens_input", 0)
                tokens_output = result.get("tokens_output", 0)
            else:
                error = f"No handler registered for provider: {model.provider.value}"
        except Exception as e:
            error = str(e)

        latency_ms = (time.time() - start_time) * 1000

        # Calculate cost (simplified)
        cost = self._estimate_cost(model, tokens_input, tokens_output)

        run = PlaygroundRun(
            id=str(uuid4()),
            prompt_template_id=template.id if template else None,
            model_config=model,
            input_variables=variables,
            rendered_prompt=rendered_prompt,
            system_prompt=final_system,
            output=output,
            latency_ms=latency_ms,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_input + tokens_output,
            cost_usd=cost,
            error=error,
            metadata=metadata or {},
        )

        self._runs.append(run)
        return run

    async def compare(
        self,
        template: PromptTemplate | None = None,
        prompt: str | None = None,
        models: list[ModelConfig] = None,
        variables: dict[str, Any] | None = None,
        system_prompt: str | None = None,
    ) -> ComparisonResult:
        """
        Compare prompt outputs across multiple models.

        Args:
            template: Prompt template to use
            prompt: Raw prompt string
            models: List of model configurations to compare
            variables: Variables to substitute
            system_prompt: System prompt override

        Returns:
            ComparisonResult with all runs
        """
        if models is None or len(models) < 2:
            raise ValueError("At least 2 models required for comparison")

        # Run all models in parallel
        tasks = [
            self.run(
                template=template,
                prompt=prompt,
                model=model,
                variables=variables,
                system_prompt=system_prompt,
            )
            for model in models
        ]

        runs = await asyncio.gather(*tasks)

        comparison = ComparisonResult(
            id=str(uuid4()),
            runs=list(runs),
            prompt_template=template,
            input_variables=variables or {},
        )

        self._comparisons.append(comparison)
        return comparison

    async def run_batch(
        self,
        template: PromptTemplate,
        model: ModelConfig,
        variable_sets: list[dict[str, Any]],
    ) -> list[PlaygroundRun]:
        """Run a template against multiple variable sets."""
        tasks = [self.run(template=template, model=model, variables=vars) for vars in variable_sets]
        return await asyncio.gather(*tasks)

    def score_run(
        self,
        run_id: str,
        scores: dict[str, float],
    ) -> bool:
        """Add scores to a run for evaluation."""
        for comparison in self._comparisons:
            for run in comparison.runs:
                if run.id == run_id:
                    comparison.scores[run_id] = scores
                    return True
        return False

    def set_winner(self, comparison_id: str, run_id: str) -> bool:
        """Set the winning run in a comparison."""
        for comparison in self._comparisons:
            if comparison.id == comparison_id:
                comparison.winner = run_id
                return True
        return False

    def get_run(self, run_id: str) -> PlaygroundRun | None:
        """Get a run by ID."""
        for run in self._runs:
            if run.id == run_id:
                return run
        return None

    def get_comparison(self, comparison_id: str) -> ComparisonResult | None:
        """Get a comparison by ID."""
        for comparison in self._comparisons:
            if comparison.id == comparison_id:
                return comparison
        return None

    def list_runs(
        self,
        template_id: str | None = None,
        model_name: str | None = None,
        limit: int = 100,
    ) -> list[PlaygroundRun]:
        """List runs with optional filters."""
        runs = self._runs

        if template_id:
            runs = [r for r in runs if r.prompt_template_id == template_id]

        if model_name:
            runs = [r for r in runs if r.model_config.model_name == model_name]

        return runs[-limit:]

    def _estimate_cost(
        self,
        model: ModelConfig,
        tokens_input: int,
        tokens_output: int,
    ) -> float | None:
        """Estimate cost based on model and token usage."""
        # Simplified pricing (would need real pricing data)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "claude-3-opus": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        }

        model_pricing = pricing.get(model.model_name)
        if model_pricing:
            return (tokens_input / 1000) * model_pricing["input"] + (
                tokens_output / 1000
            ) * model_pricing["output"]
        return None

    def export_runs(self, format: str = "json") -> str:
        """Export all runs to a format."""
        data = [run.to_dict() for run in self._runs]

        if format == "json":
            return json.dumps(data, indent=2)
        if format == "jsonl":
            return "\n".join(json.dumps(d) for d in data)
        raise ValueError(f"Unsupported format: {format}")


# Convenience function
def create_playground(client: Any | None = None) -> Playground:
    """Create a new playground instance."""
    return Playground(client)
