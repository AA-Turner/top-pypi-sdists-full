"""Plato vault CLI - inspect logins and bake snapshots through the login console."""

from plato.cli.vault.app import app_app
from plato.cli.vault.mail import mail_app
from plato.cli.vault.main import vault_app
from plato.cli.vault.persona import persona_app
from plato.cli.vault.personas import free, personas_app
from plato.cli.vault.totp import totp_app

vault_app.add_typer(persona_app, name="persona")
vault_app.add_typer(personas_app, name="personas")
vault_app.command("free")(free)
vault_app.add_typer(app_app, name="app")
vault_app.add_typer(totp_app, name="totp")
vault_app.add_typer(mail_app, name="mail")

__all__ = ["vault_app"]
