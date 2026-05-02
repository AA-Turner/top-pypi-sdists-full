import time
import webbrowser

import click
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

from .. import terminal
from ..channel import Channel, ServiceClient
from ..clients.capsule import ConfirmLoginRequest, RequestLoginRequest
from ..config import (
    DEFAULT_CONTEXT_NAME,
    ConfigContext,
    get_settings,
    load_config,
    save_config,
)

POLL_INTERVAL_S = 2
POLL_TIMEOUT_S = 300


@click.command()
@click.option("--host", default=None, help="Gateway host")
@click.option("--port", default=None, type=int, help="Gateway gRPC port")
@click.option("--http-port", default=None, type=int, help="Gateway HTTP port (defaults to --port)")
def login(host: str | None, port: int | None, http_port: int | None):
    """Authenticate with Capsule via browser.

    Set CAPSULE_GATEWAY_URL=localhost:1980 to target a local dev server.
    """
    settings = get_settings()
    gateway_host = host or settings.gateway_host
    gateway_port = port or settings.gateway_port
    gateway_http_port = http_port

    channel = Channel(addr=f"{gateway_host}:{gateway_port}", token=None)

    with ServiceClient.with_channel(channel) as client:
        res = client.capsule.request_login(RequestLoginRequest())
        if not res.ok:
            terminal.error(f"Login failed: {res.err_msg}")
            raise SystemExit(1)

        login_url = res.login_url
        terminal.header("Opening browser to authenticate...")
        terminal.info(f"{login_url}\n")

        if not webbrowser.open(login_url):
            terminal.warn("Could not open browser. Open the URL above manually.")

        confirm = _poll_with_spinner(client, res.login_id)

    context = ConfigContext(
        token=confirm.token,
        gateway_host=gateway_host,
        gateway_port=gateway_port,
        gateway_http_port=gateway_http_port,
    )

    contexts = load_config()
    contexts[DEFAULT_CONTEXT_NAME] = context
    save_config(contexts)

    terminal.success(f"\nAuthenticated! Workspace: {confirm.workspace_id}")


def _poll_with_spinner(client: ServiceClient, login_id: str):
    console = Console()
    deadline = time.time() + POLL_TIMEOUT_S

    with Live(
        Spinner("dots", text="Waiting for authentication in the browser..."),
        console=console,
        transient=True,
    ):
        while time.time() < deadline:
            time.sleep(POLL_INTERVAL_S)

            res = client.capsule.confirm_login(ConfirmLoginRequest(login_id=login_id))
            if res.ok:
                return res

            if res.err_msg not in ("pending",):
                terminal.error(f"Login failed: {res.err_msg}")
                raise SystemExit(1)

    terminal.error("Login timed out. Please try again.")
    raise SystemExit(1)
