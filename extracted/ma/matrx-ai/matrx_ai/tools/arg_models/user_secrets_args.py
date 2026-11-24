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
            'Env-var name, e.g. GITHUB_TOKEN.'
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
        description='What the secret is for.',
        max_length=512,
    )
    category: SecretCategory | None = Field(
        default=None,
        description=(
            'Provider, for grouping in the UI.'
        ),
    )
    inject_into_sandbox: bool = Field(
        default=True,
        description=(
            'Expose as an env var in every new sandbox.'
        ),
    )


__all__ = ["UserSecretSetArgs"]
