import asyncio
import logging
import os
import os.path
import platform
import ssl
import stat
import sys
import webbrowser
from collections.abc import Coroutine
from typing import Any, cast

import certifi
import click
import httpx
from dotenv import load_dotenv

from exponent.commands.utils import ConnectionTracker
from exponent.core.config import (
    SettingsProtocol,
    get_settings,
)
from exponent.core.graphql.client import GraphQLClient
from exponent.core.remote_execution.client import (
    REMOTE_EXECUTION_CLIENT_EXIT_INFO,
    RemoteExecutionClient,
)
from exponent.core.remote_execution.exceptions import (
    ExponentError,
    HandledExponentError,
)
from exponent.core.remote_execution.git import get_git_info
from exponent.core.remote_execution.session import send_exception_log
from exponent.core.remote_execution.types import ChatSource

load_dotenv()


def set_log_level() -> None:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level), stream=sys.stdout)


def redirect_to_login(settings: SettingsProtocol, cause: str = "detected") -> None:
    if inside_ssh_session():
        click.echo(f"No API Key {cause}, run 'indent login --key <API-KEY>'")
    else:
        click.echo("No API Key detected, redirecting to login...")
        webbrowser.open(f"{settings.base_url}/settings")


def inside_ssh_session() -> bool:
    return (os.environ.get("SSH_TTY") or os.environ.get("SSH_CONNECTION")) is not None


async def inside_git_repo() -> bool:
    git_info = await get_git_info(os.getcwd())

    return git_info is not None


def missing_ssl_certs() -> bool:
    if platform.system().lower() != "darwin":
        return False

    openssl_dir, openssl_cafile = os.path.split(ssl.get_default_verify_paths().openssl_cafile)

    return not os.path.exists(os.path.join(openssl_dir, openssl_cafile))


def install_ssl_certs() -> None:
    STAT_0o775 = (
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )

    openssl_dir, openssl_cafile = os.path.split(ssl.get_default_verify_paths().openssl_cafile)

    cwd = os.getcwd()
    # change working directory to the default SSL directory
    os.chdir(openssl_dir)
    relpath_to_certifi_cafile = os.path.relpath(certifi.where())

    try:
        os.remove(openssl_cafile)
    except FileNotFoundError:
        pass

    click.echo(" -- creating symlink to certifi certificate bundle")
    os.symlink(relpath_to_certifi_cafile, openssl_cafile)
    click.echo(" -- setting permissions")
    os.chmod(openssl_cafile, STAT_0o775)
    click.echo(" -- update complete")
    os.chdir(cwd)


def check_ssl() -> None:
    if missing_ssl_certs():
        click.confirm(
            "Missing root SSL certs required for python to make HTTP requests, install certifi certificates now?",
            abort=True,
            default=True,
        )

        install_ssl_certs()


async def check_inside_git_repo(settings: SettingsProtocol) -> None:
    if not settings.options.git_warning_disabled and not (await inside_git_repo()):
        click.echo(
            click.style(
                "\nWarning: Running from a folder that is not a git repository",
                fg="yellow",
                bold=True,
            )
        )
        click.echo("This is a check to make sure you are running Indent from the root of your project.")

        click.echo(f"\nCurrent directory: {click.style(os.getcwd(), fg='cyan')}")

        click.echo("\nRecommendation:")
        click.echo("  Run Indent from the root directory of your codebase.")
        click.echo("\nExample:")
        click.echo(f"  If your project is in {click.style('~/my-project', fg='cyan')}, run:")
        click.echo(f"  {click.style('cd ~/my-project && exponent run', fg='green')}")

        # Tell the user they can run exponent config --no-git-warning to disable this check
        click.echo(
            f"\nYou can run {click.style('indent config --set-git-warning-disabled', fg='green')} to disable this check."
        )

        if not click.confirm(
            click.style(
                f"\nDo you want to continue running Indent from {os.getcwd()}?",
                fg="yellow",
            ),
            default=True,
        ):
            click.echo(click.style("\nOperation aborted.", fg="red"))
            raise click.Abort()


def check_running_from_home_directory(require_confirmation: bool = True) -> bool:
    if os.path.expanduser("~") == os.getcwd():
        click.echo(
            click.style(
                "\nWarning: Running Indent from Home Directory",
                fg="yellow",
                bold=True,
            )
        )
        click.echo("Running Indent from your home directory can cause unexpected issues.")
        click.echo("\nRecommendation:")
        click.echo("  Run Indent from the root directory of your codebase.")
        click.echo("\nExample:")
        click.echo(f"  If your project is in {click.style('~/my-project', fg='cyan')}, run:")
        click.echo(f"  {click.style('cd ~/my-project && indent run', fg='green')}")

        if require_confirmation:
            if not click.confirm(
                click.style(
                    f"\nDo you want to continue running indent from {os.getcwd()}?",
                    fg="yellow",
                ),
                default=True,
            ):
                click.echo(click.style("\nOperation aborted.", fg="red"))
                raise click.Abort()
        else:
            click.echo("\n")  # Newline to separate from next command

        return True

    return False


def run_until_complete(coro: Coroutine[Any, Any, Any]) -> Any:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(coro)

    try:
        return loop.run_until_complete(task)
    except KeyboardInterrupt:
        click.echo("\nReceived interrupt signal, shutting down gracefully...")
        task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
        click.secho("Exited due to keyboard interrupt", fg="yellow")
        sys.exit(130)  # Standard exit code for SIGINT (128 + 2)
    except ExponentError as e:
        try:
            settings = get_settings()
            loop.run_until_complete(send_exception_log(e, session=None, settings=settings))
        except Exception:
            pass
        click.secho(f"Encountered error: {e}", fg="red")
        click.secho(
            "The Indent team has been notified, please try again and reach out if the problem persists.",
            fg="yellow",
        )
        sys.exit(1)
    except HandledExponentError as e:
        click.secho(str(e), fg="red")
        sys.exit(1)


async def start_chat_turn(api_key: str, base_api_url: str, base_ws_url: str, chat_uuid: str, prompt: str) -> None:
    graphql_client = GraphQLClient(api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url)

    result = await graphql_client.start_chat_turn(
        chat_uuid=chat_uuid,
        prompt=prompt,
        require_confirmation=False,
        depth_limit=20,
    )

    if result.start_chat_turn.typename__ != "Chat":
        raise HandledExponentError(
            f"Error starting chat turn: {getattr(result.start_chat_turn, 'message', 'Unknown error')}"
        )


async def run_workflow(
    base_url: str,
    client: RemoteExecutionClient,
    chat_uuid: str,
    workflow_id: str,
) -> None:
    click.secho("Running workflow...")
    workflow_data = await client.run_workflow(chat_uuid, workflow_id)
    click.secho("Workflow started.")
    if workflow_data and "workflow_run_uuid" in workflow_data:
        click.echo(
            " - Link: "
            + click.style(
                f"{base_url}/workflow/{workflow_data['workflow_run_uuid']}",
                fg=(100, 200, 255),
            )
        )


async def start_client(
    api_key: str,
    base_url: str,
    base_api_url: str,
    base_ws_url: str,
    chat_uuid: str,
    prompt: str | None = None,
    workflow_id: str | None = None,
    connection_tracker: ConnectionTracker | None = None,
    timeout_seconds: int | None = None,
) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
    async with RemoteExecutionClient.session(
        api_key=api_key,
        base_url=base_api_url,
        base_ws_url=base_ws_url,
        working_directory=os.getcwd(),
    ) as client:
        main_coro = client.run_connection(
            chat_uuid,
            connection_tracker,
            timeout_seconds,
        )
        aux_coros: list[Coroutine[Any, Any, None]] = []

        if prompt:
            # If given a prompt, we also need to send a request
            # to kick off the initial turn loop for the chat
            aux_coros.append(start_chat_turn(api_key, base_api_url, base_ws_url, chat_uuid, prompt))
        elif workflow_id:
            # Similarly, if given a workflow ID, we need to send
            # a request to kick off the workflow
            aux_coros.append(run_workflow(base_url, client, chat_uuid, workflow_id))

        client_result, *_ = await asyncio.gather(main_coro, *aux_coros)
        return cast(REMOTE_EXECUTION_CLIENT_EXIT_INFO, client_result)


# Helper functions
async def create_chat(api_key: str, base_api_url: str, base_ws_url: str, chat_source: ChatSource) -> str | None:
    try:
        async with RemoteExecutionClient.session(api_key, base_api_url, base_ws_url, os.getcwd()) as client:
            chat = await client.create_chat(chat_source)
            return chat.chat_uuid
    except (httpx.ConnectError, ExponentError) as e:
        click.secho(f"Error: {e}", fg="red")
        return None


async def set_login_complete(api_key: str, base_api_url: str, base_ws_url: str) -> None:
    graphql_client = GraphQLClient(api_key=api_key, base_api_url=base_api_url, base_ws_url=base_ws_url)
    result = await graphql_client.set_login_complete()

    data = result.set_login_complete

    if data.user_api_key != api_key:
        raise HandledExponentError("Invalid API key, login to https://indent.com to find your API key.")
