"""Open a URL in the user's browser without ever hiding it from the terminal.

Every interactive auth flow needs the same thing, and getting it wrong strands
the user: a tab that opened behind another window looks exactly like a tab that
never opened, and an accidentally closed tab leaves the flow waiting on a
callback with no way to reach the page again. So the URL is always printed —
before the attempt, and regardless of whether it succeeds.
"""

import webbrowser

import typer


def open_and_announce(url: str, *, what: str) -> bool:
    """Print ``url`` (labelled by ``what``), then try to open a browser on it.

    Returns whether a browser was launched — callers generally don't need it,
    since the printed URL is the fallback either way.

    Output goes to **stderr** so a command whose stdout carries a value (a
    resolved token, a JSON payload) stays parseable while its guidance is still
    visible.
    """
    typer.echo("", err=True)
    typer.secho(f"  🔗 {what}", fg=typer.colors.YELLOW, err=True)
    typer.secho("     Open this URL if no browser opens, or if you close the tab by mistake:", err=True)
    typer.secho(f"     {url}", fg=typer.colors.CYAN, err=True)
    typer.echo("", err=True)

    try:
        opened = webbrowser.open(url)
    except Exception:  # noqa: BLE001 - any backend failure means "not opened"
        opened = False

    if not opened:
        typer.secho(
            "  ⚠ No browser could be launched automatically — use the URL above.",
            fg=typer.colors.YELLOW,
            err=True,
        )
    return opened


def announce_delegated_flow(command: str, *, what: str, recovery: str = "") -> None:
    """Warn that a third-party CLI is about to take over and may open a browser.

    Some auth flows are not ours to drive: ``glab auth login`` mints and opens its
    own URL, so we cannot print it. What we can do is say — before handing over
    the terminal — which command is taking it, that a browser may appear, and how
    to resume if it goes wrong. Without that, a browser tab opening mid-install
    looks like it came from nowhere.

    ``recovery`` is the command to run by hand if the flow fails or the tab gets
    closed; it defaults to ``command`` itself.
    """
    typer.echo("", err=True)
    typer.secho(f"  🔗 {what}", fg=typer.colors.YELLOW, err=True)
    typer.secho(f"     `{command}` takes over the terminal and may open a browser.", err=True)
    typer.secho("     Follow its instructions below.", err=True)
    typer.secho(f"     If it fails or you close the tab, run: {recovery or command}", err=True)
    typer.echo("", err=True)
