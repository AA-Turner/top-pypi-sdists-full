#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import pathlib
from datetime import datetime, tzinfo

import rich.theme
import typer

# local datetime tzinfo used for setting timezones for datetime objects.
TZ_LOCAL: tzinfo | None = datetime.now().astimezone().tzinfo

# app-name is required for the main command name for the typer app; also
# used for package distribution loading the installed version; package
# should be named this in 'pyproject.toml'.
APPLICATION_NAME: str = "pendingai"

# typer app directory consistent for any operating system and is then
# created if it doesn't already exist.
APPLICATION_DIRECTORY: pathlib.Path = pathlib.Path(
    typer.get_app_dir(APPLICATION_NAME, force_posix=True)
)
APPLICATION_DIRECTORY.mkdir(parents=True, exist_ok=True)

# rich consoles are used and for each a default set of styles are loaded
# to be consistent and concise for application logic; update themes for
# more control below.
RICH_CONSOLE_THEME: rich.theme.Theme = rich.theme.Theme(
    styles={
        "warn": "yellow not bold",
        "success": "green not bold",
        "fail": "red bold",
        "link": "blue bold underline",
    }
)

# console width for help text and rich console output formatting
CONSOLE_WIDTH: int = 88

# upload limit in bytes for api service requests.
FILE_SIZE_UPLOAD_LIMIT: float = 6e6

# external documentation redirect url for pending.ai docs webpages.
PENDINGAI_DOCS_REDIRECT_URL: str = "https://docs.pending.ai/"


PENDINGAI_BASE_URL: dict[str, str] = {
    "dev": "https://api.dev.pending.ai/",
    "stage": "https://api.stage.pending.ai/",
    "default": "https://api.pending.ai/",
}
PENDINGAI_AUTH_URL: dict[str, str] = {
    "dev": "https://auth.dev.pending.ai/",
    "stage": "https://auth.stage.pending.ai/",
    "default": "https://auth.pending.ai/",
}
PENDINGAI_LABS_URL: dict[str, str] = {
    "dev": "https://lab.dev.pending.ai/",
    "stage": "https://lab.stage.pending.ai/",
    "default": "https://lab.pending.ai/",
}
PENDINGAI_AUTH_CLIENTID: dict[str, str] = {
    "dev": "GM1gfvGCnokIySbVO7vjmkRy4tVx5WYm",
    "stage": "PDWKoudtiP4WZV7aQt5YZbb5xlcmN6ju",
    "default": "dH69BCxGo4MyCcMWi64ZBq2YZx3UIoh1",
}
PENDINGAI_AUTH_AUDIENCE: dict[str, str] = {
    "dev": "api.dev.pending.ai/external-api",
    "stage": "api.stage.pending.ai/external-api",
    "default": "api.pending.ai/external-api",
}
