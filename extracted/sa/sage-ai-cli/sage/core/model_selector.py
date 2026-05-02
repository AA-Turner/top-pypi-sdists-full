"""Automatic model selection based on task type and requirements.

This module provides intelligent model selection that automatically
chooses the best model for a given task based on:
- Task type (coding, reasoning, chat, vision, embedding)
- Input complexity and length
- Required capabilities
- Available models and their strengths
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sage.providers.base import ModelInfo


class TaskType(Enum):
    """Types of tasks for model selection."""

    CODING = auto()  # Code generation, debugging, refactoring
    REASONING = auto()  # Complex reasoning, math, logic
    CHAT = auto()  # General conversation
    VISION = auto()  # Image understanding
    EMBEDDING = auto()  # Text embeddings
    SUMMARIZATION = auto()  # Text summarization
    TRANSLATION = auto()  # Language translation
    ANALYSIS = auto()  # Code/data analysis
    CREATIVE = auto()  # Creative writing


@dataclass
class TaskAnalysis:
    """Analysis of a task for model selection."""

    task_type: TaskType
    complexity: float  # 0.0 to 1.0
    requires_large_context: bool
    requires_code_execution: bool
    requires_vision: bool
    estimated_tokens: int
    confidence: float  # 0.0 to 1.0


class ModelSelector:
    """Selects the best model for a given task.

    Uses heuristics and task analysis to choose the most appropriate
    model from available options.
    """

    # Patterns for detecting task types
    CODING_PATTERNS = [
        r"\b(code|function|class|method|implement|debug|fix|refactor)\b",
        r"\b(python|javascript|typescript|rust|go|java|c\+\+)\b",
        r"\b(api|endpoint|database|sql|query)\b",
        r"\b(test|unittest|pytest|jest)\b",
        r"```\w*\n",  # Code blocks
    ]

    REASONING_PATTERNS = [
        r"\b(solve|calculate|prove|derive|analyze)\b",
        r"\b(math|equation|formula|theorem)\b",
        r"\b(logic|reasoning|deduce|infer)\b",
        r"\b(step.by.step|chain.of.thought)\b",
    ]

    VISION_PATTERNS = [
        r"\b(image|picture|photo|screenshot|diagram)\b",
        r"\b(see|look|visual|show)\b",
        r"\.(png|jpg|jpeg|gif|webp|svg)\b",
    ]

    CREATIVE_PATTERNS = [
        r"\b(write|story|poem|creative|essay)\b",
        r"\b(imagine|fiction|narrative)\b",
    ]

    # Model capability scores (model_pattern -> {capability: score})
    MODEL_CAPABILITIES: dict[str, dict[str, float]] = {
        # Coding-focused models
        r"(coder|code|starcoder|codellama|deepseek-coder|devstral)": {
            "coding": 1.0,
            "reasoning": 0.7,
            "chat": 0.5,
        },
        # Reasoning-focused models
        r"(qwq|r1|reasoning|think|o1|phi-4-reasoning)": {
            "reasoning": 1.0,
            "coding": 0.8,
            "chat": 0.6,
        },
        # Large general models
        r"(70b|72b|405b|110b|120b)": {
            "reasoning": 0.95,
            "coding": 0.9,
            "chat": 0.95,
            "creative": 0.9,
        },
        # Vision models
        r"(vision|llava|moondream|minicpm-v|bakllava)": {
            "vision": 1.0,
            "chat": 0.7,
        },
        # Embedding models
        r"(embed|bge|nomic|mxbai)": {
            "embedding": 1.0,
        },
        # Small/fast models
        r"(0\.5b|1b|2b|3b|mini|tiny|smol)": {
            "speed": 1.0,
            "chat": 0.6,
            "coding": 0.5,
        },
        # Medium balanced models
        r"(7b|8b|9b)": {
            "chat": 0.8,
            "coding": 0.75,
            "reasoning": 0.7,
            "speed": 0.7,
        },
    }

    def __init__(self, available_models: list[ModelInfo] | None = None):
        """Initialize the model selector.

        Args:
            available_models: List of available models. If None, will be
                populated when select() is called.
        """
        self.available_models = available_models or []
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns for efficiency."""
        self._compiled_patterns["coding"] = [
            re.compile(p, re.IGNORECASE) for p in self.CODING_PATTERNS
        ]
        self._compiled_patterns["reasoning"] = [
            re.compile(p, re.IGNORECASE) for p in self.REASONING_PATTERNS
        ]
        self._compiled_patterns["vision"] = [
            re.compile(p, re.IGNORECASE) for p in self.VISION_PATTERNS
        ]
        self._compiled_patterns["creative"] = [
            re.compile(p, re.IGNORECASE) for p in self.CREATIVE_PATTERNS
        ]

    def analyze_task(self, prompt: str, context: str = "") -> TaskAnalysis:
        """Analyze a task to determine its type and requirements.

        Args:
            prompt: The user's prompt/request.
            context: Additional context (previous messages, file content).

        Returns:
            TaskAnalysis with detected task type and requirements.
        """
        full_text = f"{prompt} {context}".lower()

        # Count pattern matches for each type
        scores: dict[str, int] = {
            "coding": 0,
            "reasoning": 0,
            "vision": 0,
            "creative": 0,
        }

        for task_type, patterns in self._compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(full_text)
                scores[task_type] += len(matches)

        # Determine primary task type
        max_score = max(scores.values()) if scores.values() else 0
        if max_score == 0:
            task_type = TaskType.CHAT
            confidence = 0.5
        elif scores["coding"] == max_score:
            task_type = TaskType.CODING
            confidence = min(0.9, 0.5 + scores["coding"] * 0.1)
        elif scores["reasoning"] == max_score:
            task_type = TaskType.REASONING
            confidence = min(0.9, 0.5 + scores["reasoning"] * 0.1)
        elif scores["vision"] == max_score:
            task_type = TaskType.VISION
            confidence = min(0.9, 0.5 + scores["vision"] * 0.1)
        elif scores["creative"] == max_score:
            task_type = TaskType.CREATIVE
            confidence = min(0.9, 0.5 + scores["creative"] * 0.1)
        else:
            task_type = TaskType.CHAT
            confidence = 0.6

        # Estimate complexity based on length and vocabulary
        word_count = len(full_text.split())
        complexity = min(1.0, word_count / 500)

        # Check for large context requirements
        requires_large_context = len(full_text) > 10000

        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(full_text) // 4

        return TaskAnalysis(
            task_type=task_type,
            complexity=complexity,
            requires_large_context=requires_large_context,
            requires_code_execution="run" in full_text or "execute" in full_text,
            requires_vision=scores["vision"] > 0,
            estimated_tokens=estimated_tokens,
            confidence=confidence,
        )

    def get_model_score(
        self,
        model: ModelInfo,
        task: TaskAnalysis,
    ) -> float:
        """Calculate a score for how well a model fits a task.

        Args:
            model: The model to evaluate.
            task: The analyzed task requirements.

        Returns:
            Score from 0.0 to 1.0 indicating model suitability.
        """
        model_id = model.id.lower()
        base_score = 0.5

        # Check model capabilities against task type
        task_capability_map = {
            TaskType.CODING: "coding",
            TaskType.REASONING: "reasoning",
            TaskType.CHAT: "chat",
            TaskType.VISION: "vision",
            TaskType.EMBEDDING: "embedding",
            TaskType.CREATIVE: "creative",
        }
        required_capability = task_capability_map.get(task.task_type, "chat")

        for pattern, capabilities in self.MODEL_CAPABILITIES.items():
            if re.search(pattern, model_id, re.IGNORECASE):
                capability_score = capabilities.get(required_capability, 0.5)
                base_score = max(base_score, capability_score)

        # Adjust for complexity - prefer larger models for complex tasks
        if task.complexity > 0.7:
            if re.search(r"(70b|72b|405b|110b)", model_id, re.IGNORECASE):
                base_score += 0.2
            elif re.search(r"(32b|34b|35b)", model_id, re.IGNORECASE):
                base_score += 0.1

        # Penalize if vision required but model doesn't support it
        if task.requires_vision:
            if not re.search(r"(vision|llava|moondream|vl)", model_id, re.IGNORECASE):
                base_score *= 0.3

        # Cap score at 1.0
        return min(1.0, base_score)

    def select(
        self,
        prompt: str,
        context: str = "",
        available_models: list[ModelInfo] | None = None,
        prefer_fast: bool = False,
        prefer_local: bool = False,
    ) -> tuple[ModelInfo | None, TaskAnalysis]:
        """Select the best model for a task.

        Args:
            prompt: The user's prompt/request.
            context: Additional context.
            available_models: Override available models.
            prefer_fast: Prefer faster/smaller models.
            prefer_local: Prefer local models over API.

        Returns:
            Tuple of (best model, task analysis). Model may be None if
            no suitable models are available.
        """
        models = available_models or self.available_models
        if not models:
            return None, self.analyze_task(prompt, context)

        task = self.analyze_task(prompt, context)

        # Score all models
        scored_models: list[tuple[ModelInfo, float]] = []
        for model in models:
            score = self.get_model_score(model, task)

            # Adjust for preferences
            if prefer_fast:
                if re.search(r"(mini|tiny|small|0\.5b|1b|2b|3b)", model.id, re.IGNORECASE):
                    score += 0.3

            if prefer_local:
                # Local models typically don't have cloud provider prefix
                if ":" not in model.id or model.id.startswith("llama_cpp:"):
                    score += 0.2

            scored_models.append((model, score))

        # Sort by score descending
        scored_models.sort(key=lambda x: x[1], reverse=True)

        if scored_models:
            return scored_models[0][0], task
        return None, task

    def get_recommendations(
        self,
        task: TaskAnalysis,
        available_models: list[ModelInfo] | None = None,
        limit: int = 3,
    ) -> list[tuple[ModelInfo, float, str]]:
        """Get model recommendations with explanations.

        Args:
            task: The analyzed task.
            available_models: Override available models.
            limit: Maximum recommendations to return.

        Returns:
            List of (model, score, explanation) tuples.
        """
        models = available_models or self.available_models
        if not models:
            return []

        recommendations: list[tuple[ModelInfo, float, str]] = []

        for model in models:
            score = self.get_model_score(model, task)

            # Generate explanation
            reasons = []
            model_id = model.id.lower()

            if task.task_type == TaskType.CODING:
                if re.search(r"(coder|code)", model_id):
                    reasons.append("optimized for code generation")
            elif task.task_type == TaskType.REASONING:
                if re.search(r"(qwq|r1|reasoning)", model_id):
                    reasons.append("strong reasoning capabilities")
            elif task.task_type == TaskType.VISION:
                if re.search(r"(vision|llava|vl)", model_id):
                    reasons.append("supports image understanding")

            if re.search(r"(70b|72b)", model_id):
                reasons.append("high-capacity model")
            elif re.search(r"(7b|8b)", model_id):
                reasons.append("balanced performance")

            explanation = ", ".join(reasons) if reasons else "general purpose"
            recommendations.append((model, score, explanation))

        # Sort by score and limit
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:limit]


def auto_select_model(
    prompt: str,
    available_models: list[ModelInfo],
    context: str = "",
) -> str | None:
    """Convenience function to auto-select a model ID.

    Args:
        prompt: The user's prompt.
        available_models: List of available models.
        context: Additional context.

    Returns:
        The selected model ID, or None if no suitable model found.
    """
    selector = ModelSelector(available_models)
    model, _ = selector.select(prompt, context)
    return model.id if model else None
