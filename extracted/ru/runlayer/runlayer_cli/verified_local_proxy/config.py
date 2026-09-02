"""Configuration management for verification config."""

from __future__ import annotations

from pydantic import BaseModel, Field

from runlayer_cli.verified_local_proxy.exceptions import ConfigurationError


class VerificationConfig(BaseModel):
    """Configuration for verifying a local MCP server."""

    server_id: str = Field(..., description="Server identifier")
    display_name: str = Field(..., description="Human-readable name")

    # Target connection details
    target_host: str = Field(default="127.0.0.1")
    target_port: int = Field(..., description="Port the target listens on")
    target_path: str = Field(default="/mcp", description="MCP endpoint path")

    # macOS verification requirements
    macos_authority: str | None = Field(
        default=None,
        description="Expected code signing authority on macOS (includes team ID)",
    )
    macos_root_ca: str = Field(
        default="Apple Root CA",
        description="Required root CA in certificate chain (prevents risky CA attacks)",
    )
    macos_strict_resource_check: bool = Field(
        default=False,
        description="If True, verify sealed resources (may fail for Electron apps after updates)",
    )

    # Optional: specific binary paths to verify
    expected_binary_paths: list[str] = Field(
        default_factory=list,
        description="Expected paths where the binary should be located",
    )

    # Periodic re-verification to mitigate TOCTOU attacks
    reverify_interval_seconds: int | None = Field(
        default=None,
        description="If set, re-verify process signature periodically (mitigates TOCTOU attacks)",
    )

    # Resilience settings - allow proxy to outlive target restarts
    wait_for_target: bool = Field(
        default=False,
        description="If True, wait for target to start instead of failing immediately",
    )
    wait_timeout_seconds: int | None = Field(
        default=None,
        description="Max time to wait for target (None = wait forever)",
    )
    retry_on_target_loss: bool = Field(
        default=False,
        description="If True, wait for target to restart instead of exiting when reverification fails",
    )

    @property
    def target_url(self) -> str:
        """Full URL to the target MCP server."""
        return f"http://{self.target_host}:{self.target_port}{self.target_path}"


# Hardcoded verification configs for MVP
# In the future, these will be fetched from Runlayer API
VERIFICATION_CONFIGS: dict[str, VerificationConfig] = {
    "com.figma/desktop-mcp": VerificationConfig(
        server_id="com.figma/desktop-mcp",
        display_name="Figma Desktop MCP",
        target_port=3845,
        target_path="/mcp",
        macos_authority="Developer ID Application: Figma, Inc. (T8RA8NE3B7)",
        expected_binary_paths=[
            "/Applications/Figma.app",
        ],
        reverify_interval_seconds=10,  # Re-verify every 10 seconds
        # Resilience: proxy outlives Figma restarts
        wait_for_target=True,  # Wait for Figma to start
        retry_on_target_loss=True,  # Wait for Figma to restart
    ),
    "design.paper/desktop-mcp": VerificationConfig(
        server_id="design.paper/desktop-mcp",
        display_name="Paper MCP",
        target_port=29979,
        target_path="/mcp",
        macos_authority="Developer ID Application: Stephen Haney (PA579U484X)",
        expected_binary_paths=[
            "/Applications/Paper.app",
        ],
        reverify_interval_seconds=10,
        wait_for_target=True,
        retry_on_target_loss=True,
    ),
}


def load_verification_config(server_id: str) -> VerificationConfig:
    """
    Load verification config for a server.

    For MVP, this looks up from hardcoded configs.
    In the future, this will fetch from Runlayer API.

    Args:
        server_id: Server identifier (e.g., "com.figma/desktop-mcp")

    Returns:
        VerificationConfig for the server

    Raises:
        ConfigurationError: If server_id is not found
    """
    config = VERIFICATION_CONFIGS.get(server_id)
    if config is None:
        available = ", ".join(VERIFICATION_CONFIGS.keys())
        raise ConfigurationError(
            f"Unknown server_id: {server_id}. Available servers: {available}"
        )
    return config
