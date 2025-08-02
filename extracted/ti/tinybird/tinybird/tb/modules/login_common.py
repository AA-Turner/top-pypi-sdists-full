import http.server
import os
import platform
import random
import shutil
import socketserver
import string
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import click
import requests

from tinybird.tb.config import DEFAULT_API_HOST
from tinybird.tb.modules.common import ask_for_region_interactively, get_regions
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILoginException
from tinybird.tb.modules.feedback_manager import FeedbackManager

SERVER_MAX_WAIT_TIME = 180


class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # The access_token is in the URL fragment, which is not sent to the server
        # We'll send a small HTML page that extracts the token and sends it back to the server
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            """
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background: #f5f5f5;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <script>
                const searchParams = new URLSearchParams(window.location.search);
                const code = searchParams.get('code');
                const workspace = searchParams.get('workspace');
                const region = searchParams.get('region');
                const provider = searchParams.get('provider');
                const host = "{auth_host}";
                fetch('/?code=' + code, {{method: 'POST'}})
                    .then(() => {{
                        window.location.href = host + "/" + provider + "/" + region + "/cli-login?workspace=" + workspace;
                    }});
            </script>
        </body>
        </html>
        """.format(auth_host=self.server.auth_host).encode()  # type: ignore
        )

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if "code" in query_params:
            code = query_params["code"][0]
            self.server.auth_callback(code)  # type: ignore
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(400, "Missing 'code' parameter")

        self.server.shutdown()

    def log_message(self, format, *args):
        # Suppress log messages
        return


AUTH_SERVER_PORT = 49160


class AuthServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, auth_callback, auth_host):
        self.auth_callback = auth_callback
        self.auth_host = auth_host
        super().__init__(server_address, RequestHandlerClass)


def start_server(auth_callback, auth_host):
    with AuthServer(("", AUTH_SERVER_PORT), AuthHandler, auth_callback, auth_host) as httpd:
        httpd.timeout = 30
        start_time = time.time()
        while time.time() - start_time < SERVER_MAX_WAIT_TIME:  # Run for a maximum of 180 seconds
            httpd.handle_request()


def login(
    host: Optional[str],
    auth_host: str = "https://cloud.tinybird.co",
    workspace: Optional[str] = None,
    interactive: bool = False,
    method: str = "browser",
):
    try:
        cli_config = CLIConfig.get_project_config()
        if not host and cli_config.get_token():
            host = cli_config.get_host(use_defaults_if_needed=False)
        if not host or interactive:
            if interactive:
                click.echo(FeedbackManager.highlight(message="» Select one region from the list below:"))
            else:
                click.echo(FeedbackManager.highlight(message="» No region detected, select one from the list below:"))

            regions = get_regions(cli_config)
            selected_region = ask_for_region_interactively(regions)

            # If the user cancels the selection, we'll exit
            if not selected_region:
                sys.exit(1)
            host = selected_region.get("api_host")

        if not host:
            host = DEFAULT_API_HOST

        host = host.rstrip("/")
        auth_host = auth_host.rstrip("/")

        if method == "code":
            display_code, one_time_code = create_one_time_code()
            click.echo(FeedbackManager.info(message=f"First, copy your one-time code: {display_code}"))
            click.echo(FeedbackManager.info(message="Press [Enter] to continue in the browser..."))
            input()
            click.echo(FeedbackManager.highlight(message="» Opening browser for authentication..."))
            params = {
                "apiHost": host,
                "code": one_time_code,
                "method": "code",
            }
            auth_url = f"{auth_host}/api/cli-login?{urlencode(params)}"
            open_url(auth_url)
            click.echo(
                FeedbackManager.info(message="\nIf browser does not open, please open the following URL manually:")
            )
            click.echo(FeedbackManager.info(message=auth_url))

            def poll_for_tokens():
                while True:
                    params = {
                        "apiHost": host,
                        "cliCode": one_time_code,
                        "method": "code",
                    }
                    response = requests.get(f"{auth_host}/api/cli-login?{urlencode(params)}")

                    try:
                        if response.status_code == 200:
                            data = response.json()
                            user_token = data.get("user_token", "")
                            workspace_token = data.get("workspace_token", "")
                            if user_token and workspace_token:
                                authenticate_with_tokens(data, host, cli_config)
                                break
                    except Exception:
                        pass

                    time.sleep(2)

            poll_for_tokens()
            return

        auth_event = threading.Event()
        auth_code: list[str] = []  # Using a list to store the code, as it's mutable

        def auth_callback(code):
            auth_code.append(code)
            auth_event.set()

        click.echo(FeedbackManager.highlight(message="» Opening browser for authentication..."))
        # Start the local server in a separate thread
        server_thread = threading.Thread(target=start_server, args=(auth_callback, auth_host))
        server_thread.daemon = True
        server_thread.start()

        # Open the browser to the auth page
        params = {
            "apiHost": host,
        }

        if workspace:
            params["workspace"] = workspace

        auth_url = f"{auth_host}/api/cli-login?{urlencode(params)}"
        open_url(auth_url)

        click.echo(FeedbackManager.info(message="\nIf browser does not open, please open the following URL manually:"))
        click.echo(FeedbackManager.info(message=auth_url))

        # Wait for the authentication to complete or timeout
        if auth_event.wait(timeout=SERVER_MAX_WAIT_TIME):  # Wait for up to 180 seconds
            params = {}
            params["code"] = auth_code[0]
            response = requests.get(
                f"{auth_host}/api/cli-login?{urlencode(params)}",
            )

            data = response.json()
            authenticate_with_tokens(data, host, cli_config)
        else:
            raise Exception("Authentication failed or timed out.")
    except Exception as e:
        raise CLILoginException(FeedbackManager.error(message=str(e)))


def _running_in_wsl() -> bool:
    """Return True when Python is executing inside a WSL distro."""
    # Fast positive check (modern WSL always sets at least one of these):
    if "WSL_DISTRO_NAME" in os.environ or "WSL_INTEROP" in os.environ:
        return True

    # Fall back to kernel /proc data
    release = platform.uname().release.lower()
    if "microsoft" in release:  # covers stock WSL kernels
        return True
    try:
        if "microsoft" in open("/proc/version").read().lower():
            return True
    except FileNotFoundError:
        pass
    return False


def open_url(url: str, *, new_tab: bool = False) -> bool:
    # 1. Try the standard library first on CPython ≥ 3.11 this already
    #    recognises WSL and fires up the Windows default browser for us.
    try:
        wb: Any = webbrowser.get()  # mypy: Any for Py < 3.10
        if new_tab:
            if wb.open_new_tab(url):
                return True
        else:
            if wb.open(url):
                return True
    except webbrowser.Error:
        pass  # keep going

    # 2. Inside WSL, prefer `wslview` if the user has it (wslu package).
    if _running_in_wsl() and shutil.which("wslview"):
        subprocess.Popen(["wslview", url])
        return True

    # 3. Secondary WSL fallback use Windows **start** through cmd.exe.
    #    Empty "" argument is required so long URLs are not treated as a window title.
    if _running_in_wsl():
        subprocess.Popen(["cmd.exe", "/c", "start", "", url])
        return True

    # 4. Unix last-ditch fallback xdg-open (most minimal container images have it)
    if shutil.which("xdg-open"):
        subprocess.Popen(["xdg-open", url])
        return True

    # 5. If everything failed, let the caller know.
    return False


def create_one_time_code():
    """Create a random one-time code for the authentication process in the format of A2C4-D2G4 (only uppercase letters and digits)"""
    seperator = "-"
    full_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    parts = [full_code[:4], full_code[4:]]
    return seperator.join(parts), full_code


def authenticate_with_tokens(data: Dict[str, Any], host: Optional[str], cli_config: CLIConfig):
    cli_config.set_token(data.get("workspace_token", ""))
    host = host or data.get("api_host", "")
    cli_config.set_token_for_host(data.get("workspace_token", ""), host)
    cli_config.set_user_token(data.get("user_token", ""))
    cli_config.set_host(host)
    ws = cli_config.get_client(token=data.get("workspace_token", ""), host=host).workspace_info(version="v1")
    for k in ("id", "name", "user_email", "user_id", "scope"):
        if k in ws:
            cli_config[k] = ws[k]

    path = os.path.join(os.getcwd(), ".tinyb")
    cli_config.persist_to_file(override_with_path=path)

    auth_info: Dict[str, Any] = cli_config.get_user_client().check_auth_login()
    if not auth_info.get("is_valid", False):
        raise Exception(FeedbackManager.error_auth_login_not_valid(host=cli_config.get_host()))

    if not auth_info.get("is_user", False):
        raise Exception(FeedbackManager.error_auth_login_not_user(host=cli_config.get_host()))

    click.echo(FeedbackManager.gray(message="\nWorkspace: ") + FeedbackManager.info(message=ws["name"]))
    click.echo(FeedbackManager.gray(message="User: ") + FeedbackManager.info(message=ws["user_email"]))
    click.echo(FeedbackManager.gray(message="Host: ") + FeedbackManager.info(message=host))
    click.echo(FeedbackManager.success(message="\n✓ Authentication successful!"))
