"""Global runtime settings resolved from environment variables.

All settings can be overridden via ``PLATO_`` prefixed env vars::

    export PLATO_RUNTIME_DIR=~/.plato
    export PLATO_GATEWAY_HOST=gateway.plato.so
    export PLATO_DEFAULT_RUNTIME=apple
    export PLATO_APPLE_SERVER_URL=http://127.0.0.1:8766

The settings singleton is accessed via ``get_settings()``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class RuntimeSettings(BaseSettings):
    """Global settings for Plato runtimes."""

    model_config = {"env_prefix": "PLATO_"}

    runtime_dir: Path = Field(
        default=Path.home() / ".plato",
        description="Root directory for Plato runtime state, caches, and SSH keys.",
    )

    gateway_host: str = Field(
        default="gateway.plato.so",
        description="Plato gateway hostname for SSH proxy.",
    )

    default_runtime: str = Field(
        default="apple",
        description="Default runtime type when none is specified (apple, vm).",
    )

    api_key: str = Field(
        default="",
        description="Plato API key for VM provisioning.",
    )

    vm_image: str = Field(
        default="383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-worlds/webclone:0.3.70",
        description="Default Docker image for VM runtimes.",
    )

    agent_vm_image: str = Field(
        default="383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-agents/claude-code:3.1.15",
        description="Default Docker image for VM-backed agent runtimes (claude-code).",
    )

    gemini_agent_vm_image: str = Field(
        default="383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-agents/gemini-cli:3.1.21",
        description="Docker image for Gemini CLI agent runtimes.",
    )

    codex_vm_image: str = Field(
        default="383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-agents/codex:3.0.28",
        description="Default Docker image for Codex agent runtimes.",
    )

    apple_image: str = Field(
        default="plato-runtime-test:latest",
        description="Default OCI image for Apple container runtimes.",
    )

    apple_server_url: str = Field(
        default="",
        description="Optional base URL for a manually managed Apple container server.",
    )

    ssh_mode: str = Field(
        default="auto",
        description=(
            "How to SSH to VMs: 'gateway' (always use Plato gateway proxy), "
            "'mesh' (always use WireGuard mesh IP), "
            "'auto' (mesh if JOB_ID is set, gateway otherwise)."
        ),
    )


_settings: RuntimeSettings | None = None


def get_settings() -> RuntimeSettings:
    """Get the global runtime settings singleton."""
    global _settings
    if _settings is None:
        _settings = RuntimeSettings()
        _settings.runtime_dir.mkdir(parents=True, exist_ok=True)
    return _settings
