import asyncio
import signal
import sys
import time
from typing import NoReturn

import click

from exponent.commands.common import (
    check_inside_git_repo,
    check_running_from_home_directory,
    check_ssl,
    create_chat,
    inside_ssh_session,
    redirect_to_login,
    start_client,
)
from exponent.commands.settings import use_settings
from exponent.commands.types import exponent_cli_group
from exponent.commands.utils import (
    ConnectionTracker,
    Spinner,
    launch_exponent_browser,
    print_exponent_message,
)
from exponent.core.config import Settings, SettingsProtocol
from exponent.core.remote_execution.client import (
    REMOTE_EXECUTION_CLIENT_EXIT_INFO,
    SwitchCLIChat,
    WSDisconnected,
)
from exponent.core.remote_execution.types import ChatSource
from exponent.core.remote_execution.utils import assert_unreachable
from exponent.utils.version import check_exponent_version_and_upgrade

try:
    # this is an optional dependency for python <3.11
    from async_timeout import timeout  # ty: ignore[unresolved-import]
except ImportError:  # pragma: no cover
    from asyncio import timeout


@exponent_cli_group()
def run_cli() -> None:
    """Run AI-powered chat sessions."""
    pass  # pragma: no cover


@run_cli.command()
@click.option(
    "--chat-id",
    help="ID of an existing chat session to reconnect",
    required=False,
    prompt_required=False,
    prompt="Enter the chat ID to reconnect to",
)
@click.option(
    "--prompt",
    help="Start a chat with a given prompt.",
)
@click.option(
    "--workflow-id",
    hidden=True,
    required=False,
)
@click.option(
    "--timeout-seconds",
    type=int,
    help="Number of seconds without receiving a request before shutting down",
    envvar="INDENT_TIMEOUT_SECONDS",
)
@use_settings
def run(
    settings: Settings,
    chat_id: str | None = None,
    prompt: str | None = None,
    workflow_id: str | None = None,
    timeout_seconds: int | None = None,
) -> None:
    """[default] Start or reconnect to an Indent session."""
    check_exponent_version_and_upgrade(settings)

    if not settings.api_key:
        redirect_to_login(settings)
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    check_running_from_home_directory()
    check_ssl()
    loop.run_until_complete(check_inside_git_repo(settings))

    api_key = settings.api_key
    base_url = settings.base_url
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    chat_uuid = chat_id or loop.run_until_complete(
        create_chat(api_key, base_api_url, base_ws_url, ChatSource.CLI_RUN)
    )

    if isinstance(timeout_seconds, int) and timeout_seconds <= 0:
        click.secho("Error: --timeout-seconds must be a positive integer", fg="red")
        sys.exit(1)

    if chat_uuid is None:
        sys.exit(1)

    assert chat_uuid is not None  # Narrowing for type checker after sys.exit

    if (
        (not inside_ssh_session())
        and (not workflow_id)
        # If the user specified a chat ID, they probably don't want to re-launch the chat
        and (not chat_id)
    ):
        # Open the chat in the browser
        launch_exponent_browser(settings.environment, base_url, chat_uuid)

    while True:
        result = run_chat(
            loop,
            api_key,
            chat_uuid,
            settings,
            prompt,
            workflow_id,
            timeout_seconds,
        )
        if result is None or isinstance(result, WSDisconnected):
            # NOTE: None here means that handle_connection_changes exited
            # first. We should likely have a different message for this.
            if result and result.error_message:
                click.secho(f"Error: {result.error_message}", fg="red")
                sys.exit(10)
            else:
                click.echo("Disconnected upon user request, shutting down...")
                break
        elif isinstance(result, SwitchCLIChat):
            chat_uuid = result.new_chat_uuid
            click.echo("\nSwitching chats...")
        else:
            assert_unreachable(result)  # pragma: no cover


def _cleanup_tasks(loop: asyncio.AbstractEventLoop) -> None:
    """Cancel and cleanup all tasks in the event loop."""
    for task in asyncio.all_tasks(loop):
        task.cancel()
    all_tasks = asyncio.all_tasks(loop)
    current_task = asyncio.current_task(loop)
    if current_task:
        all_tasks.discard(current_task)

    if all_tasks:
        loop.run_until_complete(asyncio.gather(*all_tasks, return_exceptions=True))


def _handle_shutdown(loop: asyncio.AbstractEventLoop, message: str) -> NoReturn:
    """Handle graceful shutdown by cancelling tasks and exiting."""
    try:
        all_tasks = asyncio.all_tasks(loop)
        if len(all_tasks) > 0:
            loop.run_until_complete(asyncio.gather(*all_tasks, return_exceptions=True))
    except Exception:
        pass
    click.secho(message, fg="yellow")
    sys.exit(130)


def run_chat(
    loop: asyncio.AbstractEventLoop,
    api_key: str,
    chat_uuid: str,
    settings: SettingsProtocol,
    prompt: str | None,
    workflow_id: str | None,
    timeout_seconds: int | None,
) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO | None:
    start_ts = time.time()
    base_url = settings.base_url
    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    print_exponent_message(base_url, chat_uuid)
    click.echo()

    connection_tracker = ConnectionTracker()

    client_fut = loop.create_task(
        start_client(
            api_key,
            base_url,
            base_api_url,
            base_ws_url,
            chat_uuid,
            prompt=prompt,
            workflow_id=workflow_id,
            connection_tracker=connection_tracker,
            timeout_seconds=timeout_seconds,
        )
    )

    conn_fut = loop.create_task(handle_connection_changes(connection_tracker, start_ts))

    # Set up signal handlers for graceful shutdown
    def signal_handler() -> None:
        click.echo("\nReceived interrupt signal, shutting down gracefully...")
        for task in asyncio.all_tasks(loop):
            task.cancel()

    try:
        loop.add_signal_handler(signal.SIGINT, signal_handler)
        loop.add_signal_handler(signal.SIGTERM, signal_handler)
        loop.add_signal_handler(signal.SIGQUIT, signal_handler)
    except NotImplementedError:
        # Signal handlers are not supported on Windows
        pass

    try:
        done, _ = loop.run_until_complete(
            asyncio.wait({client_fut, conn_fut}, return_when=asyncio.FIRST_COMPLETED)
        )

        if client_fut in done:
            return client_fut.result()
        else:
            return None
    except KeyboardInterrupt:
        click.echo("\nReceived interrupt signal, shutting down gracefully...")
        for task in asyncio.all_tasks(loop):
            task.cancel()
        _handle_shutdown(loop, "Exited due to keyboard interrupt")
    except asyncio.CancelledError:
        _handle_shutdown(loop, "Exited due to interrupt signal")
    except Exception:
        click.secho("Unexpected error:", fg="red")
        sys.exit(130)
    finally:
        _cleanup_tasks(loop)


async def handle_connection_changes(
    connection_tracker: ConnectionTracker, start_ts: float
) -> None:
    try:
        async with timeout(5):
            assert await connection_tracker.next_change()
            click.echo(ready_message(start_ts))
    except TimeoutError:
        spinner = Spinner("Connecting...")
        spinner.show()
        assert await connection_tracker.next_change()
        spinner.hide()
        click.echo(ready_message(start_ts))

    while True:
        assert not await connection_tracker.next_change()

        click.echo("Disconnected...", nl=False)
        await asyncio.sleep(1)
        spinner = Spinner("Reconnecting...")
        spinner.show()
        assert await connection_tracker.next_change()
        spinner.hide()
        click.echo("\x1b[1;32m✓ Reconnected", nl=False)
        sys.stdout.flush()
        await asyncio.sleep(1)
        click.echo("\r\x1b[0m\x1b[2K", nl=False)
        sys.stdout.flush()


def ready_message(start_ts: float) -> str:
    elapsed = round(time.time() - start_ts, 2)
    return f"\x1b[32m✓\x1b[0m Ready in {elapsed}s"
