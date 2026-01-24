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
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import click
import requests
from click import Context

from tinybird.tb.config import DEFAULT_API_HOST
from tinybird.tb.modules.common import ask_for_region_interactively, get_region_from_host, get_regions
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILoginException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.telemetry import is_ci_environment

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
                                authenticate_with_tokens(data, cli_config)
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
            authenticate_with_tokens(data, cli_config)
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
        elif wb.open(url):
            return True
    except webbrowser.Error:
        pass  # keep going

    # 2. Inside WSL, prefer `wslview` if the user has it (wslu package).
    if _running_in_wsl() and shutil.which("wslview"):
        try:
            subprocess.Popen(["wslview", url])
            return True
        except Exception:
            # wslview not found, continue to next fallback
            pass

    # 3. Secondary WSL fallback use Windows **start** through cmd.exe.
    #    Empty "" argument is required so long URLs are not treated as a window title.
    if _running_in_wsl():
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", "", url])
            return True
        except Exception:
            # cmd.exe not found, continue to next fallback
            pass

    # 4. Unix last-ditch fallback xdg-open (most minimal container images have it)
    if shutil.which("xdg-open"):
        try:
            subprocess.Popen(["xdg-open", url])
            return True
        except Exception:
            # xdg-open not found, continue to next fallback
            pass

    # 5. If everything failed, let the caller know.
    return False


def create_one_time_code():
    """Create a random one-time code for the authentication process in the format of A2C4-D2G4 (only uppercase letters and digits)"""
    seperator = "-"
    full_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    parts = [full_code[:4], full_code[4:]]
    return seperator.join(parts), full_code


def check_current_folder_in_sessions(ctx: Context) -> None:
    """
    Check if the current folder is tracked in the sessions file before running a command.

    If the current folder is not in sessions.txt:
    - If no sessions exist or file doesn't exist: silently add it (first usage is fine)
    - If other folders exist: warn the user they're running from an untracked folder

    Args:
        provider: The provider name (e.g., 'gcp', 'aws')
        region: The region name
        workspace_name: The workspace name
        current_folder: The current working directory
    """
    try:
        env = ctx.ensure_object(dict)["env"]
        if env != "cloud" or ctx.invoked_subcommand == "login" or is_ci_environment():
            return

        current_folder = os.getcwd()
        cli_config = CLIConfig.get_project_config()
        regions = get_regions(cli_config)
        host = cli_config.get_host()
        if not host:
            return

        region = get_region_from_host(host, regions)

        if not region:
            return

        provider = region.get("provider", "unknown")
        region_name = region.get("name", "unknown")
        current_folder = os.getcwd()
        home_dir = Path.home()
        workspace_name = cli_config.get("name", "unknown")
        sessions_dir = home_dir / ".tinybird" / provider / region_name / workspace_name
        sessions_file = sessions_dir / "sessions.txt"

        # Normalize the current folder path
        current_folder = os.path.abspath(current_folder)

        # Read existing sessions
        existing_sessions: dict[str, str] = {}  # folder -> timestamp
        if sessions_file.exists():
            try:
                with open(sessions_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            # Format: <folder_path>\t<timestamp>
                            parts = line.split("\t")
                            if len(parts) >= 2 and parts[0]:
                                existing_sessions[parts[0]] = parts[1]
            except Exception:
                # If we can't read the file, just continue silently
                return

        # Check if current folder is already tracked
        if current_folder in existing_sessions:
            # Already tracked, update the timestamp
            try:
                existing_sessions[current_folder] = datetime.now().isoformat()
                sessions_dir.mkdir(parents=True, exist_ok=True)
                with open(sessions_file, "w") as f:
                    f.writelines(f"{folder}\t{timestamp}\n" for folder, timestamp in existing_sessions.items())
            except Exception:
                # Silently fail, don't block the command
                pass
            return

        # Current folder is not tracked
        if not existing_sessions:
            # No previous sessions, this is the first time - silently add it
            try:
                sessions_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().isoformat()
                with open(sessions_file, "a") as f:
                    f.write(f"{current_folder}\t{timestamp}\n")
            except Exception:
                # Silently fail, don't block the command
                pass
        else:
            # Other folders exist, warn the user
            click.echo("")
            click.echo(FeedbackManager.warning(message="Running command from an untracked folder"))
            click.echo(FeedbackManager.gray(message="Current folder: ") + FeedbackManager.info(message=current_folder))
            tracked_folders = ", ".join(existing_sessions.keys())
            click.echo(
                FeedbackManager.gray(message="Tracked folders: ") + FeedbackManager.info(message=tracked_folders)
            )
            confirmed = click.confirm(
                FeedbackManager.highlight(message="» Are you sure you want to continue?"),
                default=True,
            )

            if not confirmed:
                raise TrackFolderCancelled("Command cancelled by user.")

            # Add current folder to the tracked list
            try:
                timestamp = datetime.now().isoformat()
                with open(sessions_file, "a") as f:
                    f.write(f"{current_folder}\t{timestamp}\n")
            except Exception:
                # Silently fail, don't block the command
                pass

    except TrackFolderCancelled:
        raise
    except Exception:
        # Don't block execution if folder check fails
        pass


class TrackFolderCancelled(Exception):
    """Exception raised when the user cancels the folder tracking"""

    pass


def check_and_warn_folder_change(cli_config: CLIConfig) -> None:
    """
    Check if the user is logging in from a folder that hasn't been tracked before.

    Reads from ~/.tinybird/<provider>/<region>/<workspace_name>/sessions.txt to track
    folder usage history. If the current folder is not in the list of tracked folders
    and there are existing sessions, prompts the user to confirm.

    Behavior:
        - If no sessions exist: Silently add current folder
        - If current folder is already tracked: Update timestamp and continue
        - If current folder is not tracked but other folders are: Show warning and ask for confirmation

    Raises:
        TrackFolderCancelled: If user declines the folder change confirmation
    """
    if is_ci_environment():
        return

    host = cli_config.get_host()
    workspace_name = cli_config.get("name", None)
    if not host or not workspace_name:
        return

    regions = get_regions(cli_config)
    region = get_region_from_host(host, regions)

    if not region:
        return

    provider = region.get("provider", "unknown")
    region_name = region.get("name", "unknown")

    current_folder = os.getcwd()

    home_dir = Path.home()
    sessions_dir = home_dir / ".tinybird" / provider / region_name / workspace_name
    sessions_file = sessions_dir / "sessions.txt"

    # Normalize the current folder path
    current_folder = os.path.abspath(current_folder)

    # Read existing sessions if the file exists
    existing_sessions: dict[str, str] = {}  # folder -> timestamp
    if sessions_file.exists():
        try:
            with open(sessions_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        # Format: <folder_path>\t<timestamp>
                        parts = line.split("\t")
                        if len(parts) >= 2 and parts[0]:
                            existing_sessions[parts[0]] = parts[1]
        except Exception as e:
            # If we can't read the file, just continue without warning
            click.echo(FeedbackManager.warning(message=f"Warning: Could not read sessions file: {e}"))

    # If current folder is already tracked, update timestamp and return
    if current_folder in existing_sessions:
        try:
            existing_sessions[current_folder] = datetime.now().isoformat()
            sessions_dir.mkdir(parents=True, exist_ok=True)
            with open(sessions_file, "w") as f:
                f.writelines(f"{folder}\t{timestamp}\n" for folder, timestamp in existing_sessions.items())
        except Exception as e:
            click.echo(FeedbackManager.warning(message=f"Warning: Could not update sessions file: {e}"))
        return

    # If there are existing tracked folders but current folder is not tracked, warn the user
    if existing_sessions:
        click.echo("")
        click.echo(
            FeedbackManager.warning(message="Login from a different folder than previous sessions has been detected.")
        )
        click.echo(FeedbackManager.gray(message="Current folder: ") + FeedbackManager.info(message=current_folder))
        tracked_folders = ", ".join(existing_sessions.keys())
        click.echo(FeedbackManager.gray(message="Tracked folders: ") + FeedbackManager.info(message=tracked_folders))

        # Ask for confirmation
        confirmed = click.confirm(
            FeedbackManager.highlight(message="» Are you sure you want to continue?"),
            default=True,
        )

        if not confirmed:
            raise TrackFolderCancelled("Login cancelled by user.")

        # User accepted, show pull suggestion
        click.echo(
            FeedbackManager.warning(
                message="Remember to run `tb --cloud pull` to have your latest resources available."
            )
        )

    # Record the current session
    try:
        # Create the directory if it doesn't exist
        sessions_dir.mkdir(parents=True, exist_ok=True)

        # Add current folder to sessions and update timestamp
        timestamp = datetime.now().isoformat()
        existing_sessions[current_folder] = timestamp

        # Write all sessions to file
        with open(sessions_file, "w") as f:
            f.writelines(f"{folder}\t{ts}\n" for folder, ts in existing_sessions.items())
    except Exception as e:
        # If we can't write the file, just warn but don't block the login
        click.echo(FeedbackManager.warning(message=f"Warning: Could not update sessions file: {e}"))


def authenticate_with_tokens(data: Dict[str, Any], cli_config: CLIConfig):
    cli_config.set_token(data.get("workspace_token", ""))
    host = data.get("api_host", "")

    if not host:
        raise Exception("API host not found in the authentication response")

    cli_config.set_token_for_host(data.get("workspace_token", ""), host)
    cli_config.set_user_token(data.get("user_token", ""))
    cli_config.set_host(host)
    ws = cli_config.get_client(token=data.get("workspace_token", ""), host=host).workspace_info(version="v1")
    for k in ("id", "name", "user_email", "user_id", "scope"):
        if k in ws:
            cli_config[k] = ws[k]

    auth_info: Dict[str, Any] = cli_config.get_user_client().check_auth_login()
    if not auth_info.get("is_valid", False):
        raise Exception(FeedbackManager.error_auth_login_not_valid(host=cli_config.get_host()))

    if not auth_info.get("is_user", False):
        raise Exception(FeedbackManager.error_auth_login_not_user(host=cli_config.get_host()))

    # Check for folder change before persisting config
    check_and_warn_folder_change(cli_config)

    path = os.path.join(os.getcwd(), ".tinyb")
    cli_config.persist_to_file(override_with_path=path)

    click.echo(FeedbackManager.gray(message="\nWorkspace: ") + FeedbackManager.info(message=ws["name"]))
    click.echo(FeedbackManager.gray(message="User: ") + FeedbackManager.info(message=ws["user_email"]))
    click.echo(FeedbackManager.gray(message="Host: ") + FeedbackManager.info(message=host))
    click.echo(FeedbackManager.success(message="\n✓ Authentication successful!"))
