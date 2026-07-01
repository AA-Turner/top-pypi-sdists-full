"""CVC CLI — `cvc providers` and `cvc credentials` subcommands.

Surfaces Phase-1 Category-1 plumbing (provider registry + CredentialPool +
FallbackChain) on the command line, mirroring the dashboard's REST surface.

Wired into the main CLI via ``main.add_command(providers_group)`` and
``main.add_command(credentials_group)`` from cvc/cli.py.
"""
from __future__ import annotations

import json

import click

from cvc.providers import all_profiles, get_provider


# ─── Helpers ─────────────────────────────────────────────────────────────


def _mask_token(token: str) -> str:
    if not token:
        return ""
    if len(token) <= 10:
        return "•" * len(token)
    return f"{'•' * 6}{token[-6:]}"


def _print_table(rows: list[list[str]], headers: list[str]) -> None:
    if not rows:
        click.echo("(none)")
        return
    cols = list(zip(*([headers] + rows)))
    widths = [max(len(c) for c in col) for col in cols]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    click.echo(fmt.format(*headers))
    click.echo("  ".join("─" * w for w in widths))
    for r in rows:
        click.echo(fmt.format(*r))


# ─── `cvc providers` ─────────────────────────────────────────────────────


@click.group("providers")
def providers_group() -> None:
    """Inspect declarative provider profiles (registry + capabilities)."""


@providers_group.command("list")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON")
def providers_list(as_json: bool) -> None:
    """List all registered providers and their capabilities."""
    profiles = all_profiles()
    if as_json:
        click.echo(json.dumps([_profile_dict(p) for p in profiles], indent=2))
        return
    rows = [
        [
            p.name,
            p.api_mode,
            p.auth_type,
            "✓" if p.supports_tools else "·",
            "✓" if p.supports_streaming else "·",
            "✓" if p.supports_reasoning else "·",
            str(len(p.fallback_models)),
        ]
        for p in profiles
    ]
    _print_table(
        rows,
        ["NAME", "API_MODE", "AUTH", "TOOLS", "STREAM", "REASON", "FALLBACKS"],
    )


@providers_group.command("show")
@click.argument("name")
def providers_show(name: str) -> None:
    """Show full details for a single provider."""
    profile = get_provider(name)
    if not profile:
        raise click.ClickException(f"unknown provider: {name}")
    click.echo(json.dumps(_profile_dict(profile), indent=2))


def _profile_dict(p) -> dict:
    return {
        "name": p.name,
        "aliases": list(p.aliases or []),
        "env_vars": list(p.env_vars or []),
        "base_url": p.base_url,
        "auth_type": p.auth_type,
        "api_mode": p.api_mode,
        "fallback_models": list(p.fallback_models or []),
        "fixed_temperature": p.fixed_temperature,
        "default_max_tokens": p.default_max_tokens,
        "supports_streaming": p.supports_streaming,
        "supports_tools": p.supports_tools,
        "supports_reasoning": p.supports_reasoning,
        "supports_prompt_cache": p.supports_prompt_cache,
    }


# ─── `cvc credentials` ───────────────────────────────────────────────────


@click.group("credentials")
def credentials_group() -> None:
    """Manage the CredentialPool — multi-key rotation across providers."""


@credentials_group.command("list")
@click.option("--provider", "-p", default=None, help="Filter by provider")
@click.option("--json", "as_json", is_flag=True)
def credentials_list(provider: str | None, as_json: bool) -> None:
    """List stored credentials (tokens are masked)."""
    from cvc.agent.credential_pool import CredentialPool

    pool = CredentialPool.get_instance()
    creds = pool.list(provider)
    if as_json:
        click.echo(
            json.dumps(
                [
                    {
                        "id": c.id,
                        "provider": c.provider,
                        "label": c.label,
                        "auth_type": c.auth_type,
                        "source": c.source,
                        "priority": c.priority,
                        "access_token_masked": _mask_token(c.access_token),
                        "base_url": c.base_url,
                        "last_status": c.last_status,
                        "request_count": c.request_count,
                    }
                    for c in creds
                ],
                indent=2,
            )
        )
        return
    rows = [
        [
            c.provider,
            c.id,
            c.label[:24],
            c.auth_type,
            c.last_status,
            str(c.request_count),
            _mask_token(c.access_token),
        ]
        for c in creds
    ]
    _print_table(
        rows, ["PROVIDER", "ID", "LABEL", "AUTH", "STATUS", "USES", "TOKEN"]
    )


@credentials_group.command("add")
@click.option("--provider", required=True)
@click.option("--label", required=True, help="Human-readable name")
@click.option("--token", required=True, help="API key / OAuth access token")
@click.option("--auth-type", default="api_key", show_default=True,
              type=click.Choice(["api_key", "oauth", "pat"]))
@click.option("--base-url", default=None)
def credentials_add(
    provider: str, label: str, token: str, auth_type: str, base_url: str | None
) -> None:
    """Add a new credential to the pool."""
    import uuid

    from cvc.agent.credential_pool import (
        SOURCE_USER,
        CredentialPool,
        PooledCredential,
    )

    cred = PooledCredential(
        provider=provider,
        id=uuid.uuid4().hex[:12],
        label=label,
        auth_type=auth_type,
        source=SOURCE_USER,
        access_token=token,
        base_url=base_url,
    )
    CredentialPool.get_instance().add(cred)
    click.secho(f"✓ added {provider}/{label} (id={cred.id})", fg="green")


@credentials_group.command("remove")
@click.argument("provider")
@click.argument("credential_id")
def credentials_remove(provider: str, credential_id: str) -> None:
    """Remove a credential from the pool."""
    from cvc.agent.credential_pool import CredentialPool

    ok = CredentialPool.get_instance().remove(provider, credential_id)
    if not ok:
        raise click.ClickException("credential not found")
    click.secho(f"✓ removed {provider}/{credential_id}", fg="green")


@credentials_group.command("reset")
@click.argument("provider")
@click.argument("credential_id")
def credentials_reset(provider: str, credential_id: str) -> None:
    """Manually clear an exhausted/error state on a credential."""
    from cvc.agent.credential_pool import CredentialPool

    pool = CredentialPool.get_instance()
    cred = pool.get(provider, credential_id)
    if not cred:
        raise click.ClickException("credential not found")
    pool.reset(cred)
    click.secho(f"✓ reset {provider}/{credential_id}", fg="green")


@credentials_group.command("stats")
def credentials_stats() -> None:
    """Show pool stats (totals, exhausted counts per provider)."""
    from cvc.agent.credential_pool import CredentialPool

    click.echo(json.dumps(CredentialPool.get_instance().stats(), indent=2))
