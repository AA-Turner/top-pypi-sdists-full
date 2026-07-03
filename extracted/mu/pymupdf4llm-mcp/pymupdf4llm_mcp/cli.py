import importlib.metadata
from typing import Annotated

import typer

from pymupdf4llm_mcp.app import mcp

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if not value:
        return
    typer.echo(importlib.metadata.version("pymupdf4llm-mcp"))
    raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show package version and exit.", callback=_version_callback, is_eager=True),
    ] = False,
):
    del version


@app.command()
def stdio():
    mcp.run(transport="stdio")


@app.command()
def sse(
    host: str = "localhost",
    port: int = 3000,
):
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport="sse")


if __name__ == "__main__":
    app(["stdio"])
