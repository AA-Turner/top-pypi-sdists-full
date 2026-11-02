"""Strict permission values accepted by the Agents SDK authoring API."""

from fnmatch import fnmatchcase
from typing import Self

from pydantic import ConfigDict, model_validator

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.core import validate_permission_pattern

_GLOB_METACHARACTERS = frozenset("*?[")


class PermissionRule(harness_session.PermissionRule):
    model_config = ConfigDict(extra="forbid", frozen=True)

    @model_validator(mode="after")
    def _reject_patterns_that_cannot_match(self) -> Self:
        rule = f"PermissionRule for tools {list(self.tools)!r}"
        if not self.tools:
            raise ValueError(f"{rule}: tools is empty, so the rule matches no tool call")
        for pattern in self.tools:
            _check_pattern(rule, "tools", pattern, arguments=False)
            if "." not in pattern and _GLOB_METACHARACTERS.isdisjoint(pattern):
                raise ValueError(
                    f"{rule}: tools pattern {pattern!r} matches no tool. Rules match the stable tool ID "
                    f"'<namespace>.<name>', not the name the model sees; for an SDK tool use "
                    f"'client.{pattern}', or its own namespace if it declares one"
                )
        for field, patterns in (
            ("allowlist", self.allowlist),
            ("denylist", self.denylist),
            ("sensitive", self.sensitive),
        ):
            for pattern in patterns:
                _check_pattern(rule, field, pattern, arguments=True)
        return self


class PermissionPolicy(harness_session.PermissionPolicy):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rules: tuple[PermissionRule, ...] = ()


def _check_pattern(rule: str, field: str, pattern: str, *, arguments: bool) -> None:
    try:
        validate_permission_pattern(pattern, arguments=arguments)
    except ValueError as error:
        raise ValueError(f"{rule}: {field} pattern {pattern!r} {error}") from None


def always_denies(policy: PermissionPolicy, tool_id: str) -> bool:
    """Return whether ``policy`` denies every call to ``tool_id``, whatever its arguments.

    Mirrors the runtime: rules match the stable tool ID with glob patterns, first match wins, and
    the default applies when no rule matches. In the matching rule, a denylist hit denies, then a
    sensitive hit asks, then a non-empty allowlist allows or asks, and otherwise the rule's
    decision applies. So the rule denies every call when a denylist pattern matches any text, or
    when it has no sensitive or allowlist patterns and its decision is ``deny``.
    """

    for rule in policy.rules:
        if not any(fnmatchcase(tool_id, pattern) for pattern in rule.tools):
            continue
        if any(_matches_any_text(pattern) for pattern in rule.denylist):
            return True
        if rule.allowlist or rule.sensitive:
            return False
        return rule.decision == "deny"
    return policy.default == "deny"


def _matches_any_text(pattern: str) -> bool:
    return bool(pattern) and set(pattern) == {"*"}
