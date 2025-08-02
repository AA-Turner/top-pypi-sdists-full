import typer
from va.store.orby.orby_client import get_orby_client

app = typer.Typer(help="Auth related commands")


@app.command("login")
def login(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force new login even if already authenticated"
    ),
):
    """Log in to Orby with the OAuth2 flow"""
    client = get_orby_client()

    if client.login(force=force):
        typer.echo("✅ Login successful!")
    else:
        typer.echo("❌ Login failed")
        raise typer.Exit(1)
