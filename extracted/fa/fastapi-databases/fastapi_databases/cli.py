#!/usr/bin/env python3
import typer

from alembic.config import Config
from alembic import command

alembic_cfg = Config("./alembic.ini")

app = typer.Typer()


@app.command()
def init():
    """Initialize db"""

    typer.echo(typer.style("initialzing database migration files", fg="green"))

    command.init(alembic_cfg, "alembic", template="generic", package=True)
    return


@app.command()
def makemigrations():
    """make db migrations"""

    command.revision(alembic_cfg, autogenerate=True)
    return


@app.command()
def migrate():
    """migrate db"""

    command.upgrade(alembic_cfg, "head")
    return


if __name__ == "__main__":
    app()
