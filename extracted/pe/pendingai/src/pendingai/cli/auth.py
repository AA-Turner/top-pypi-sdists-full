#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typer import Exit, Typer

from pendingai.auth import SessionInfo
from pendingai.auth.session import AuthSession
from pendingai.cli.console import Console
from pendingai.cli.context import PendingAiContext
from pendingai.cli.utils import catch_exception
from pendingai.utils.logger import Logger

logger = Logger().get_logger()
cout = Console()
app = Typer(
    name="auth",
    help="Manage an authenticated session with the Pending AI platform.",
    short_help="Authenticate with the Pending AI platform.",
    no_args_is_help=True,
)


# region command: login ------------------------------------------------


@app.command("login", help="Login to a Pending AI account.")
@catch_exception()
def _login(ctx: PendingAiContext):
    ctx.obj["client"].authentication.login()
    info: SessionInfo | None = ctx.obj["client"].session.info
    cout.print("[green]✓ Authentication complete.")
    if info:
        cout.print(f"[green]✓ Logged in user account: [bold]{info.user_email}")
        cout.print(f"[green]✓ Logged in organization: [bold]{info.user_org_name}")


# region command: logout -----------------------------------------------


@app.command("logout", help="Logout of a Pending AI account.")
@catch_exception()
def _logout(ctx: PendingAiContext):
    info: SessionInfo | None = ctx.obj["client"].session.info
    if info:
        ctx.obj["client"].authentication.logout()
        cout.print(f"[success]✓ Logged out [b underline]{info.user_email}[/].")
    else:
        cout.print("[warn]! Already logged out.")


# region command: refresh ----------------------------------------------


@app.command("refresh", help="Refresh an authenticated session.")
@catch_exception()
def _refresh(ctx: PendingAiContext):
    info: SessionInfo | None = ctx.obj["client"].session.info
    if not info:
        cout.print("[warn]! No logged in user, use [code]pendingai auth login[/].")
        raise Exit(1)
    ctx.obj["client"].authentication.refresh()
    cout.print("[green]✓ Authentication complete.")
    if info:
        cout.print(f"[green]✓ Logged in as user: [bold]{info.user_email}")
        cout.print(f"[green]✓ Logged in to team: [bold]{info.user_org_name}")


# region command: status -----------------------------------------------


@app.command("status", help="Show active session information.")
@catch_exception()
def _status(ctx: PendingAiContext):
    session: AuthSession = ctx.obj["client"].session
    if not session.info:
        cout.print("[warn]! No logged in user, use [code]pendingai auth login[/].")
        raise Exit(1)
    elif session.token and session.token.is_expired():
        cout.print("[warn]! Access has expired, use [code]pendingai auth refresh[/].")
        raise Exit(1)

    if session.info.remaining.days >= 1:
        cout.print("[success]✓ Session is active: Over 1 day remaining")
    elif session.info.remaining.total_seconds() < 60:
        cout.print("[warn]! Session is closing soon: Less than 1 minute remaining")
    else:
        time_left: str = str(session.info.remaining).split(".")[0]
        cout.print(f"[success]✓ Session is active: [not b]{time_left} remaining")
    cout.print(f"- Session user account: [b underline]{session.info.user_email}")
    cout.print(f"- Session organization: [b]{session.info.user_org_name}")


# region command: token ------------------------------------------------


@app.command("token", help="Get the access token of the current session.")
@catch_exception()
def _token(ctx: PendingAiContext):
    if not ctx.obj["client"].session.token:
        cout.print("[warn]! No logged in user, use [code]pendingai auth login[/].")
        raise Exit(1)
    elif ctx.obj["client"].session.token.is_expired():
        cout.print("[warn]! Access token expired; use [code]pendingai auth refresh[/].")
        raise Exit(1)
    assert ctx.obj["client"].session.info
    email: str = ctx.obj["client"].session.info.user_email
    cout.print(f"[success]✓ Access token for [b underline]{email}[/].")
    cout.print(f"\b{ctx.obj['client'].session.token.access_token}", soft_wrap=True)
