"""`cvc auth ...` — unified auth namespace (mirrors the upstream auth).

This is a thin façade that re-exposes the existing provider-specific auth
commands under a common `cvc auth login <provider>` / `cvc auth logout
<provider>` / `cvc auth status` interface.  No business logic lives here —
each subcommand delegates to the canonical implementation in the relevant
`cli_<provider>.py` module so there's exactly one source of truth.

Usage:
    cvc auth login copilot       # browser OAuth device flow
    cvc auth status              # show all configured providers
    cvc auth logout copilot      # remove all Copilot credentials
"""
from __future__ import annotations

import click


@click.group(name="auth")
def auth_group() -> None:
    """Manage authentication for LLM providers."""


# ── login ───────────────────────────────────────────────────────────────
@auth_group.group("login")
def auth_login() -> None:
    """Log in to an LLM provider."""


@auth_login.command("copilot")
def auth_login_copilot() -> None:
    """Browser OAuth device flow for GitHub Copilot (free tier)."""
    from cvc.cli_copilot import copilot_login
    ctx = click.get_current_context()
    ctx.invoke(copilot_login)


# ── logout ──────────────────────────────────────────────────────────────
@auth_group.group("logout")
def auth_logout() -> None:
    """Remove credentials for an LLM provider."""


@auth_logout.command("copilot")
@click.option("--id", "cred_id", default=None, help="Credential ID to remove (omit + use --all to wipe).")
@click.option("--all", "remove_all", is_flag=True, help="Remove ALL Copilot credentials.")
def auth_logout_copilot(cred_id: str | None, remove_all: bool) -> None:
    """Remove GitHub Copilot credentials."""
    from cvc.cli_copilot import copilot_logout
    ctx = click.get_current_context()
    ctx.invoke(copilot_logout, cred_id=cred_id, remove_all=remove_all)


# ── status ──────────────────────────────────────────────────────────────
@auth_group.command("status")
def auth_status() -> None:
    """Show authentication status across all providers."""
    from cvc.cli_copilot import copilot_status
    ctx = click.get_current_context()
    ctx.invoke(copilot_status)


__all__ = ["auth_group"]
