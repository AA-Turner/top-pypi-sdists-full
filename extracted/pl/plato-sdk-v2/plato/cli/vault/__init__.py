"""Plato vault CLI - inspect logins and bake snapshots through the login console."""

from plato.cli.vault.main import vault_app
from plato.cli.vault.persona import persona_app

vault_app.add_typer(persona_app, name="persona")

__all__ = ["vault_app"]
