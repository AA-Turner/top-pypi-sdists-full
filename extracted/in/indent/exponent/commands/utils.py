import asyncio
import os
import sys
import time
import webbrowser

import click

from exponent.core.config import Environment, SettingsProtocol
from exponent.utils.version import get_installed_version


def print_editable_install_forced_prod_warning(settings: SettingsProtocol) -> None:
    click.secho(
        "Detected local editable install, but this command only works against prod.",
        fg="red",
        bold=True,
    )
    click.secho("Using prod settings:", fg="red", bold=True)
    click.secho("- base_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
    click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.get_base_api_url()}", fg=(100, 200, 255), bold=False)
    click.secho()


def print_editable_install_warning(settings: SettingsProtocol) -> None:
    click.secho(
        "Detected local editable install, using local URLs", fg="yellow", bold=True
    )
    click.secho("- base_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.base_url}", fg=(100, 200, 255), bold=False)
    click.secho("- base_api_url=", fg="yellow", bold=True, nl=False)
    click.secho(f"{settings.get_base_api_url()}", fg=(100, 200, 255), bold=False)
    click.secho()


def print_exponent_message(base_url: str, chat_uuid: str) -> None:
    version = get_installed_version()
    shell = os.environ.get("SHELL")

    click.echo()
    click.secho(f"△ Indent v{version}", fg=(180, 150, 255), bold=True)
    click.echo()
    click.echo(
        " - Link: " + click.style(f"{base_url}/chats/{chat_uuid}", fg=(100, 200, 255))
    )

    if shell is not None:
        click.echo(f" - Shell: {shell}")


def is_indent_app_installed() -> bool:
    if sys.platform == "darwin":  # macOS
        return os.path.exists("/Applications/Indent.app")

    # TODO: Add support for Windows and Linux
    return False


def launch_exponent_browser(
    environment: Environment, base_url: str, chat_uuid: str
) -> None:
    if is_indent_app_installed() and environment == Environment.production:
        url = f"exponent://chats/{chat_uuid}"
    else:
        url = f"{base_url}/chats/{chat_uuid}"
    webbrowser.open(url)


class Spinner:
    def __init__(self, text: str) -> None:
        self.text = text
        self.task: asyncio.Task[None] | None = None
        self.base_time = time.time()
        self.fg_color: tuple[int, int, int] | None = None
        self.bold = False
        self.animation_chars = "⣷⣯⣟⡿⢿⣻⣽⣾"
        self.animation_speed = 10

    def show(self) -> None:
        if self.task is not None:
            return

        async def spinner(base_time: float) -> None:
            color_start = ""
            if self.fg_color:
                if isinstance(self.fg_color, tuple) and len(self.fg_color) == 3:
                    r, g, b = self.fg_color
                    color_start = f"\x1b[38;2;{r};{g};{b}m"
                elif isinstance(self.fg_color, int):
                    color_start = f"\x1b[{30 + self.fg_color}m"

            bold_start = "\x1b[1m" if self.bold else ""
            style_start = f"{color_start}{bold_start}"
            style_end = "\x1b[0m"

            while True:
                t = time.time() - base_time
                i = round(t * self.animation_speed) % len(self.animation_chars)
                click.echo(
                    f"\r{style_start}{self.animation_chars[i]} {self.text}{style_end}",
                    nl=False,
                )
                await asyncio.sleep(0.1)

        self.task = asyncio.get_event_loop().create_task(spinner(self.base_time))

    def hide(self) -> None:
        if self.task is None:
            return

        self.task.cancel()
        self.task = None
        click.echo("\r\x1b[0m\x1b[2K", nl=False)
        sys.stdout.flush()


class ConnectionTracker:
    def __init__(self) -> None:
        self.connected = True
        self.queue: asyncio.Queue[bool] = asyncio.Queue()

    def is_connected(self) -> bool:
        while True:
            try:
                self.connected = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        return self.connected

    async def wait_for_reconnection(self) -> None:
        if not self.is_connected():
            assert await self.queue.get()
            self.connected = True

    async def set_connected(self, connected: bool) -> None:
        await self.queue.put(connected)

    async def next_change(self) -> bool:
        return await self.queue.get()


def get_short_git_commit_hash(commit_hash: str) -> str:
    return commit_hash[:8]
