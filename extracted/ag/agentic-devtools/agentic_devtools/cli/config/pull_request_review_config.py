"""Nested ``pullRequestReview`` configuration for the v2 PR review restructure.

Stored under the ``"pullRequestReview"`` key in ``.agdt/config/project.json``
(read/written via :mod:`agentic_devtools.cli.config.project_config`).  This
module defines the typed, camelCase, nested config schema and a **tolerant**
loader: missing keys and wrong-typed values fall back to documented defaults
rather than raising, so a partially-edited or absent config never breaks the
review workflow.

This is additive (Phase P0): nothing consumes the config yet.  Review *policy*
(rubber-duck model layers, triage depth/budgets, subagent timeout/retries) lives
here; the model *inventory* (``availableModels``) is a separate top-level key.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentic_devtools.cli.config.project_config import load_project_config

# ── Defaults (plan §7 for the schema; §15.8 for the triage cost-budget fields) ──

_DEFAULT_MAIN_AGENT: tuple[str, ...] = ("gpt-5.3-codex", "gemini-3.1-pro-preview")
_DEFAULT_SUBAGENT: tuple[str, ...] = ("gpt-5.3-codex", "gemini-3.1-pro-preview")

_DEFAULT_DEEP_GLOBS: tuple[str, ...] = ("**/auth/**", "**/*.sql", "**/migrations/**")
_DEFAULT_LIGHT_GLOBS: tuple[str, ...] = ("**/*.md", "**/*.lock", "**/__snapshots__/**")


def _scalar(data: dict[str, Any], key: str, default: Any, typ: type | tuple[type, ...]) -> Any:
    """Return ``data[key]`` when present and of type *typ*, else *default*."""
    value = data.get(key, default)
    if typ is int and isinstance(value, bool):
        return default
    return value if isinstance(value, typ) else default


def _list_or_default(value: Any, default: tuple[str, ...]) -> list[str]:
    """Return a sanitized list when *value* is a list, else a list of *default*.

    Non-string or blank entries are dropped.
    """
    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]
    return list(default)


@dataclass
class RubberDuckConfig:
    """Rubber-duck (second-opinion) model layers.

    Attributes:
        enabled: Master switch for rubber-duck critiques.
        mainAgent: Candidate models the orchestrator may use to critique its own
            (pr-synthesis / triage / consolidation) work.
        subagent: Candidate models used to critique a per-file reviewer's draft.
    """

    enabled: bool = True
    mainAgent: list[str] = field(default_factory=lambda: list(_DEFAULT_MAIN_AGENT))
    subagent: list[str] = field(default_factory=lambda: list(_DEFAULT_SUBAGENT))

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible, camelCase dictionary."""
        return {
            "enabled": self.enabled,
            "mainAgent": list(self.mainAgent),
            "subagent": list(self.subagent),
        }

    @classmethod
    def from_dict(cls, data: Any) -> RubberDuckConfig:
        """Build from a dict tolerantly; non-dict input yields all defaults."""
        if not isinstance(data, dict):
            return cls()
        return cls(
            enabled=_scalar(data, "enabled", True, bool),
            mainAgent=_list_or_default(data.get("mainAgent"), _DEFAULT_MAIN_AGENT),
            subagent=_list_or_default(data.get("subagent"), _DEFAULT_SUBAGENT),
        )


@dataclass
class TriageConfig:
    """Per-file review-depth triage policy and cost guardrails.

    Attributes:
        enabled: Master switch for triage (when off, ``defaultDepth`` applies to all).
        defaultDepth: Depth used when no glob/heuristic forces a decision
            (``"light"`` or ``"deep"``).
        deepGlobs: Globs that force ``deep`` review (e.g. auth, SQL, migrations).
        lightGlobs: Globs that force ``light`` review (e.g. docs, lockfiles, snapshots).
        minDiffLinesForDeep: Changed-line threshold that pushes a file to ``deep``.
        maxDeepModelCalls: Cap on total deep-path model calls (author + ducks).
        maxDeepTotalChangedLines: Cap on total changed lines across deep files.
        maxReviewMinutes: Soft wall-clock budget for the whole review.
    """

    enabled: bool = True
    defaultDepth: str = "deep"
    deepGlobs: list[str] = field(default_factory=lambda: list(_DEFAULT_DEEP_GLOBS))
    lightGlobs: list[str] = field(default_factory=lambda: list(_DEFAULT_LIGHT_GLOBS))
    minDiffLinesForDeep: int = 20
    maxDeepModelCalls: int = 90
    maxDeepTotalChangedLines: int = 5000
    maxReviewMinutes: int = 60

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible, camelCase dictionary."""
        return {
            "enabled": self.enabled,
            "defaultDepth": self.defaultDepth,
            "deepGlobs": list(self.deepGlobs),
            "lightGlobs": list(self.lightGlobs),
            "minDiffLinesForDeep": self.minDiffLinesForDeep,
            "maxDeepModelCalls": self.maxDeepModelCalls,
            "maxDeepTotalChangedLines": self.maxDeepTotalChangedLines,
            "maxReviewMinutes": self.maxReviewMinutes,
        }

    @classmethod
    def from_dict(cls, data: Any) -> TriageConfig:
        """Build from a dict tolerantly; non-dict input yields all defaults."""
        if not isinstance(data, dict):
            return cls()

        default_depth = _scalar(data, "defaultDepth", "deep", str)
        if default_depth not in {"deep", "light"}:
            default_depth = "deep"

        return cls(
            enabled=_scalar(data, "enabled", True, bool),
            defaultDepth=default_depth,
            deepGlobs=_list_or_default(data.get("deepGlobs"), _DEFAULT_DEEP_GLOBS),
            lightGlobs=_list_or_default(data.get("lightGlobs"), _DEFAULT_LIGHT_GLOBS),
            minDiffLinesForDeep=_scalar(data, "minDiffLinesForDeep", 20, int),
            maxDeepModelCalls=_scalar(data, "maxDeepModelCalls", 90, int),
            maxDeepTotalChangedLines=_scalar(data, "maxDeepTotalChangedLines", 5000, int),
            maxReviewMinutes=_scalar(data, "maxReviewMinutes", 60, int),
        )


@dataclass
class PullRequestReviewConfig:
    """Top-level ``pullRequestReview`` config block.

    Attributes:
        rubberDuck: Rubber-duck model-layer policy.
        triage: Per-file review-depth policy and budgets.
        subagentTimeoutSeconds: Advisory per-subagent timeout (seconds).
        subagentMaxRetries: Re-spawn attempts before orchestrator takeover.
    """

    rubberDuck: RubberDuckConfig = field(default_factory=RubberDuckConfig)
    triage: TriageConfig = field(default_factory=TriageConfig)
    subagentTimeoutSeconds: int = 600
    subagentMaxRetries: int = 2

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible, nested camelCase dictionary."""
        return {
            "rubberDuck": self.rubberDuck.to_dict(),
            "triage": self.triage.to_dict(),
            "subagentTimeoutSeconds": self.subagentTimeoutSeconds,
            "subagentMaxRetries": self.subagentMaxRetries,
        }

    @classmethod
    def from_dict(cls, data: Any) -> PullRequestReviewConfig:
        """Build from a dict tolerantly; non-dict input yields all defaults."""
        if not isinstance(data, dict):
            return cls()
        return cls(
            rubberDuck=RubberDuckConfig.from_dict(data.get("rubberDuck")),
            triage=TriageConfig.from_dict(data.get("triage")),
            subagentTimeoutSeconds=_scalar(data, "subagentTimeoutSeconds", 600, int),
            subagentMaxRetries=_scalar(data, "subagentMaxRetries", 2, int),
        )


def load_pull_request_review_config(*, git_root: Path | None = None) -> PullRequestReviewConfig:
    """Load the ``pullRequestReview`` config block from ``project.json``.

    Returns a fully-defaulted :class:`PullRequestReviewConfig` when the file or
    the ``"pullRequestReview"`` key is absent or malformed (tolerant; never raises).

    Args:
        git_root: Optional repo root; when omitted it is auto-detected.
    """
    config = load_project_config(git_root=git_root)
    raw = config.get("pullRequestReview")
    if not isinstance(raw, dict):
        return PullRequestReviewConfig()
    return PullRequestReviewConfig.from_dict(raw)
