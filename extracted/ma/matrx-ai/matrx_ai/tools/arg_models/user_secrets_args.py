"""Argument models for the user_secrets tool family."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from matrx_ai.tools.declared import ToolArgs

# Mirrors the enum advertised by the tool_def.parameters DB row (the source of
# truth). Keep these in sync — the drift gate flags a one-sided enum constraint.
SecretCategory = Literal[
    "anthropic",
    "aws",
    "custom",
    "github",
    "google",
    "linear",
    "notion",
    "openai",
    "slack",
    "stripe",
    "supabase",
    "vercel",
]


class UserSecretSetArgs(ToolArgs):
    """Add or rotate a single secret on the user's account.

    Example:
        ``user_secret_set(key="GITHUB_TOKEN", value="ghp_…",
                          category="github",
                          description="Personal access token for build agent")``

    Behavior is idempotent (upsert): re-running with the same key overwrites
    the value without creating a duplicate row. After the call, the secret
    is immediately available to every new sandbox the user creates and to
    any tool that reads from the user-secrets vault."""

    key: str = Field(
        ...,
        description=(
            "Environment-variable name to store the secret under. Must be a "
            "valid identifier: letters, digits, and underscores; cannot "
            "start with a digit. Convention: SCREAMING_SNAKE_CASE."
        ),
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z_][A-Za-z0-9_]*$",
    )
    value: str = Field(
        ...,
        description="The raw secret value. Stored Fernet-encrypted at rest.",
        max_length=32768,
    )
    description: str | None = Field(
        default=None,
        description="Free-text note about what this secret is for.",
        max_length=512,
    )
    category: SecretCategory | None = Field(
        default=None,
        description=(
            "Provider category, used for grouping in the UI. One of: "
            "github, openai, anthropic, google, aws, stripe, supabase, "
            "vercel, linear, notion, slack, custom. Defaults to 'custom'."
        ),
    )
    inject_into_sandbox: bool = Field(
        default=True,
        description=(
            "When true, this secret will be exposed as an environment "
            "variable in every new sandbox the user creates. Turn off only "
            "for secrets that should be readable by the user but not by "
            "anything running inside the sandbox."
        ),
    )


__all__ = ["UserSecretSetArgs"]
