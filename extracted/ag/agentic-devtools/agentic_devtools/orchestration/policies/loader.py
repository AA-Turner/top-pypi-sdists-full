"""Policy configuration loader."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.state import _get_git_repo_root

from .config import PolicyConfig, PRReviewPolicy, SharedBudgetPolicy, WorkOnIssuePolicy
from .exceptions import PolicyValidationError

_CONFIG_RELATIVE_PATH = ".agdt/config/autonomy-policies.yml"


class PolicyLoader:
    """Loads and validates policy configuration from YAML.

    Reads from `.agdt/config/autonomy-policies.yml` relative to the git
    repository root. Missing or empty files return sensible defaults.
    Unknown keys are silently ignored for forward compatibility.
    """

    def load(self) -> PolicyConfig:
        """Load and return the resolved policy configuration.

        Returns:
            PolicyConfig with user overrides merged onto defaults.

        Raises:
            PolicyValidationError: If git root cannot be resolved or values are invalid.
        """
        git_root = _get_git_repo_root()
        if git_root is None:
            raise PolicyValidationError(
                field_path="<root>",
                invalid_value=None,
                constraint="Repository root resolution failed. Not inside a git worktree.",
            )

        config_path = Path(git_root) / _CONFIG_RELATIVE_PATH

        if not config_path.exists():
            return PolicyConfig()

        content = config_path.read_text(encoding="utf-8")
        if not content or not content.strip():
            return PolicyConfig()

        try:
            raw = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise PolicyValidationError(
                field_path="<file>",
                invalid_value=str(config_path),
                constraint=f"YAML syntax error: {e}",
            ) from e

        if raw is None or not isinstance(raw, dict):
            return PolicyConfig()

        return self._build_config(raw)

    def _build_config(self, raw: dict[str, Any]) -> PolicyConfig:
        """Build PolicyConfig from raw YAML dict, merging with defaults."""
        pr_review_raw = raw.get("pr_review", {})
        work_on_issue_raw = raw.get("work_on_issue", {})
        shared_raw = raw.get("shared", {})

        if not isinstance(pr_review_raw, dict):
            pr_review_raw = {}
        if not isinstance(work_on_issue_raw, dict):
            work_on_issue_raw = {}
        if not isinstance(shared_raw, dict):
            shared_raw = {}

        pr_review = self._build_pr_review(pr_review_raw)
        work_on_issue = self._build_work_on_issue(work_on_issue_raw)
        shared = self._build_shared(shared_raw)

        return PolicyConfig(pr_review=pr_review, work_on_issue=work_on_issue, shared=shared)

    def _build_pr_review(self, raw: dict[str, Any]) -> PRReviewPolicy:
        """Build PRReviewPolicy from raw dict."""
        approval = raw.get("approval_threshold", {})
        if not isinstance(approval, dict):
            approval = {}

        kwargs: dict[str, Any] = {}

        if "max_high_severity" in approval:
            val = approval["max_high_severity"]
            self._validate_non_negative_int("pr_review.approval_threshold.max_high_severity", val)
            kwargs["max_high_severity"] = int(val)

        if "max_medium_severity" in approval:
            val = approval["max_medium_severity"]
            self._validate_non_negative_int("pr_review.approval_threshold.max_medium_severity", val)
            kwargs["max_medium_severity"] = int(val)

        if "confidence_minimum" in raw:
            val = raw["confidence_minimum"]
            self._validate_float_range("pr_review.confidence_minimum", val, 0.0, 1.0)
            kwargs["confidence_minimum"] = float(val)

        if "escalation_triggers" in raw:
            val = raw["escalation_triggers"]
            if not isinstance(val, list) or not all(isinstance(t, str) for t in val):
                raise PolicyValidationError(
                    field_path="pr_review.escalation_triggers",
                    invalid_value=val,
                    constraint="must be a list of strings",
                )
            for trigger in val:
                if not isinstance(trigger, str) or not trigger.strip():
                    raise PolicyValidationError(
                        field_path="pr_review.escalation_triggers",
                        invalid_value=trigger,
                        constraint="each trigger must contain at least one non-whitespace character",
                    )
            kwargs["escalation_triggers"] = tuple(val)

        return PRReviewPolicy(**kwargs)

    def _build_work_on_issue(self, raw: dict[str, Any]) -> WorkOnIssuePolicy:
        """Build WorkOnIssuePolicy from raw dict."""
        kwargs: dict[str, Any] = {}

        if "retry_budget" in raw:
            val = raw["retry_budget"]
            self._validate_non_negative_int("work_on_issue.retry_budget", val)
            kwargs["retry_budget"] = int(val)

        if "blocked_after_minutes" in raw:
            val = raw["blocked_after_minutes"]
            self._validate_non_negative_int("work_on_issue.blocked_after_minutes", val)
            kwargs["blocked_after_minutes"] = int(val)

        if "coverage_threshold" in raw:
            val = raw["coverage_threshold"]
            self._validate_non_negative_int("work_on_issue.coverage_threshold", val)
            kwargs["coverage_threshold"] = int(val)

        if "node_retry_budgets" in raw:
            val = raw["node_retry_budgets"]
            if not isinstance(val, dict):
                raise PolicyValidationError(
                    field_path="work_on_issue.node_retry_budgets",
                    invalid_value=val,
                    constraint="must be a mapping of node names to non-negative integers",
                )
            budgets: dict[str, int] = {}
            for node_name, budget in val.items():
                normalized = node_name.strip() if isinstance(node_name, str) else node_name
                field_path = f"work_on_issue.node_retry_budgets.{normalized}"
                if not isinstance(node_name, str) or not normalized:
                    raise PolicyValidationError(
                        field_path=field_path,
                        invalid_value=node_name,
                        constraint="node name must be a non-empty string",
                    )
                if normalized in budgets:
                    raise PolicyValidationError(
                        field_path=field_path,
                        invalid_value=node_name,
                        constraint=(
                            f"duplicate node name after whitespace normalization: '{normalized}' already defined"
                        ),
                    )
                self._validate_non_negative_int(field_path, budget)
                budgets[normalized] = int(budget)
            kwargs["node_retry_budgets"] = budgets

        return WorkOnIssuePolicy(**kwargs)

    def _build_shared(self, raw: dict[str, Any]) -> SharedBudgetPolicy:
        """Build SharedBudgetPolicy from raw dict."""
        kwargs: dict[str, Any] = {}

        if "max_tokens" in raw:
            val = raw["max_tokens"]
            self._validate_non_negative_int("shared.max_tokens", val)
            kwargs["max_tokens"] = int(val)

        if "max_wall_clock_minutes" in raw:
            val = raw["max_wall_clock_minutes"]
            self._validate_non_negative_int("shared.max_wall_clock_minutes", val)
            kwargs["max_wall_clock_minutes"] = int(val)

        return SharedBudgetPolicy(**kwargs)

    def _validate_non_negative_int(self, field_path: str, value: Any) -> None:
        """Validate that a value is a non-negative integer."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise PolicyValidationError(
                field_path=field_path,
                invalid_value=value,
                constraint="must be a non-negative integer",
            )
        if isinstance(value, float) and not value.is_integer():
            raise PolicyValidationError(
                field_path=field_path,
                invalid_value=value,
                constraint="must be a whole number (not a decimal fraction)",
            )
        if value < 0:
            raise PolicyValidationError(
                field_path=field_path,
                invalid_value=value,
                constraint="must be non-negative (>= 0)",
            )

    def _validate_float_range(self, field_path: str, value: Any, min_val: float, max_val: float) -> None:
        """Validate that a value is a float within the given range."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise PolicyValidationError(
                field_path=field_path,
                invalid_value=value,
                constraint=f"must be a number between {min_val} and {max_val}",
            )
        fval = float(value)
        if math.isnan(fval) or fval < min_val or fval > max_val:
            raise PolicyValidationError(
                field_path=field_path,
                invalid_value=value,
                constraint=f"must be between {min_val} and {max_val} inclusive",
            )
