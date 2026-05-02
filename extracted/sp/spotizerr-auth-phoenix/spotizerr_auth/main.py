import time
import logging
import pathlib
import json
import requests
import sys
import secrets
import string
import typing

# Rich library for beautiful terminal interfaces
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.rule import Rule
from rich.status import Status
from rich.text import Text

# Initialize the Rich console
console = Console()

# Define icons for consistency
class Icons:
    SPOTIFY = "🎵"
    CHECK = "✅"
    CROSS = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    ARROW = "➤"
    LOCK = "🔒"
    KEY = "🔑"
    USER = "👤"
    GEAR = "⚙️"
    DOWNLOAD = "⬇️"
    SUCCESS = "🎉"
    NETWORK = "🌐"
    CLEAN = "🧹"
    REGISTER = "👤➕"
    ADMIN = "👑"

LOG_FORMAT = "[LOG] %(asctime)s %(name)s %(levelname)s: %(message)s"

try:
    from librespot import Version
    from librespot.proto import Connect_pb2 as Connect
    from librespot.zeroconf import ZeroconfServer
except ImportError:
    console.print("[bold red]Error: librespot-spotizerr-phoenix is not installed. Please install it with pip.[/]")
    console.print("[bold red]e.g. 'pip install -r requirements.txt' or 'pip install librespot-spotizerr-phoenix'[/]")
    sys.exit(1)


def configure_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if root_logger.handlers:
        return

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(handler)


def enable_librespot_logging(level: int = logging.DEBUG) -> None:
    logger_names = [
        "Librespot:ApiClient",
        "Librespot:DealerClient",
        "Librespot:EventService",
        "Librespot:Session",
        "Librespot:TokenProvider",
        "Librespot:ZeroconfServer",
        "Librespot:MercuryClient",
        "Librespot:ChannelManager",
        "Librespot:AudioKeyManager",
        "Librespot:CdnManager",
        "Librespot:PlayableContentFeeder",
        "Librespot:DeviceStateHandler",
        "Librespot:Player:VorbisOnlyAudioQuality",
    ]

    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.propagate = True

    logging.getLogger("urllib3").setLevel(level)


def print_logging_header() -> None:
    console.print()
    console.print(Rule(f"[bold green]{Icons.INFO} Logs[/]", style="green"))
    console.print("[dim]Debug output starts here.[/]")


def print_header():
    """Print a modern header for the application using Rich Panel."""
    header = Text.from_markup(f"""
{Icons.SPOTIFY} [bold cyan]SPOTIZERR AUTHENTICATION UTILITY[/]
[dim]Configure Spotify credentials for your Spotizerr instance[/]
    """, justify="center")
    console.print(Panel(header, border_style="cyan", expand=False))

def _parse_device_type(device_type: str) -> typing.Optional[int]:
    normalized = device_type.strip().upper().replace("-", "_").replace(" ", "_")
    if normalized.isdigit():
        value = int(normalized)
        try:
            Connect.DeviceType.Name(value)
        except ValueError:
            return None
        return value
    try:
        return Connect.DeviceType.Value(normalized)
    except ValueError:
        return None

def generate_default_device_id() -> str:
    return "".join(secrets.choice("0123456789abcdef") for _ in range(40))

def device_profile_defaults(device_type_name: str) -> typing.Dict[str, str]:
    profiles = {
        "UNKNOWN": {
            "device_name": "Unknown Device",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Device",
        },
        "UNKNOWN_SPOTIFY": {
            "device_name": "Spotify Device",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Device",
        },
        "SPEAKER": {
            "device_name": "Living Room Speaker",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Speaker",
        },
        "AVR": {
            "device_name": "AV Receiver",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; AVR",
        },
        "STB": {
            "device_name": "Set-Top Box",
            "device_software_version": "Spotify 1.97.4 Android TV",
            "system_info_string": "Spotify 1.97.4; Android TV 13; STB",
        },
        "AUDIO_DONGLE": {
            "device_name": "Audio Dongle",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Dongle",
        },
        "CAST_VIDEO": {
            "device_name": "Cast Video",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Chromecast; Video",
        },
        "CAST_AUDIO": {
            "device_name": "Cast Audio",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Chromecast; Audio",
        },
        "SMARTPHONE": {
            "device_name": "iPhone",
            "device_software_version": "Spotify 9.1.14 iOS",
            "system_info_string": "Spotify 9.1.14; iOS 17.3; iPhone15,2",
        },
        "SMARTWATCH": {
            "device_name": "Smartwatch",
            "device_software_version": "Spotify 9.1.16.824 Wear OS",
            "system_info_string": "Spotify 9.1.16.824; Wear OS 4; Pixel Watch 2",
        },
        "TABLET": {
            "device_name": "iPad",
            "device_software_version": "Spotify 9.1.14 iOS",
            "system_info_string": "Spotify 9.1.14; iPadOS 17.3; iPad14,5",
        },
        "COMPUTER": {
            "device_name": "Desktop Computer",
            "device_software_version": "Spotify 1.2.81.264 Desktop",
            "system_info_string": "Spotify 1.2.81.264; Windows 11; Desktop",
        },
        "CHROMEBOOK": {
            "device_name": "Chromebook",
            "device_software_version": "Spotify 9.1.18.1484 Android",
            "system_info_string": "Spotify 9.1.18.1484; ChromeOS 120; Chromebook",
        },
        "TV": {
            "device_name": "Smart TV",
            "device_software_version": "Spotify 1.97.4 Android TV",
            "system_info_string": "Spotify 1.97.4; Android TV 13; TV",
        },
        "GAME_CONSOLE": {
            "device_name": "Game Console",
            "device_software_version": "Spotify 2024.03.11_1-5817b61 Xbox",
            "system_info_string": "Spotify 2024.03.11_1-5817b61; Xbox OS; Console",
        },
        "AUTOMOBILE": {
            "device_name": "Car Audio",
            "device_software_version": "Spotify 9.1.18.1484 Android Auto",
            "system_info_string": "Spotify 9.1.18.1484; Android Auto; Car",
        },
        "CAR_THING": {
            "device_name": "Car Thing",
            "device_software_version": "Spotify Car Thing 1.1.0",
            "system_info_string": "Spotify Car Thing 1.1.0; Linux; Car Thing",
        },
        "OBSERVER": {
            "device_name": "Observer Device",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Observer",
        },
        "HOME_THING": {
            "device_name": "Home Thing",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Home",
        },
    }

    return profiles.get(
        device_type_name,
        {
            "device_name": "Spotify Device",
            "device_software_version": "Spotify Connect 3.2.6",
            "system_info_string": "Spotify Connect 3.2.6; Linux; Device",
        },
    )

def prompt_device_overrides(preferred_locale: str) -> typing.Dict[str, typing.Any]:
    console.print(Rule(f"[bold blue]{Icons.GEAR} Device Identity Overrides[/]", style="blue"))
    console.print(
        "[dim]Press Enter to accept the default values for the selected device type.[/]"
    )

    default_device_type = "SPEAKER"
    default_device_id = generate_default_device_id()
    device_type_prompt = (
        f"[magenta]{Icons.ARROW}[/] Device type (enum name)\n"
        "[dim]Valid Enums: UNKNOWN, COMPUTER, TABLET, SMARTPHONE, SPEAKER, TV, AVR, STB, AUDIO_DONGLE, GAME_CONSOLE, CAST_VIDEO, CAST_AUDIO, AUTOMOBILE, SMARTWATCH, CHROMEBOOK, UNKNOWN_SPOTIFY, CAR_THING, OBSERVER, HOME_THING[/]"
    )
    device_type_raw = Prompt.ask(
        device_type_prompt,
        default=default_device_type,
    ).strip() or default_device_type

    parsed_device_type = _parse_device_type(device_type_raw)
    if parsed_device_type is None:
        valid_types = ", ".join(Connect.DeviceType.keys())
        console.print(
            f"❌ [bold red]Invalid device type.[/] Valid values: {valid_types}"
        )
        sys.exit(1)

    device_type_name = Connect.DeviceType.Name(parsed_device_type)
    profile_defaults = device_profile_defaults(device_type_name)

    device_name = Prompt.ask(
        f"[magenta]{Icons.ARROW}[/] Device name",
        default=profile_defaults["device_name"],
    ).strip() or profile_defaults["device_name"]
    device_id = Prompt.ask(
        f"[magenta]{Icons.ARROW}[/] Device ID (40 hex characters - default is randomly generated)",
        default=default_device_id,
    ).strip() or default_device_id
    device_software_version = Prompt.ask(
        f"[magenta]{Icons.ARROW}[/] Device software version",
        default=profile_defaults["device_software_version"],
    ).strip() or profile_defaults["device_software_version"]
    system_info_string = Prompt.ask(
        f"[magenta]{Icons.ARROW}[/] System info string",
        default=profile_defaults["system_info_string"],
    ).strip() or profile_defaults["system_info_string"]

    if len(device_id) != 40 or any(ch not in string.hexdigits for ch in device_id):
        console.print("❌ [bold red]Device ID must be 40 hex characters.[/]")
        sys.exit(1)

    if len(preferred_locale) != 2:
        console.print("❌ [bold red]Preferred locale must be a 2-letter code.[/]")
        sys.exit(1)

    return {
        "device_name": device_name,
        "device_type": parsed_device_type,
        "device_id": device_id.lower(),
        "preferred_locale": preferred_locale.lower(),
        "device_software_version": device_software_version,
        "system_info_string": system_info_string,
    }


def log_device_overrides(overrides: typing.Dict[str, typing.Any]) -> None:
    device_type_name = Connect.DeviceType.Name(overrides["device_type"])
    logging.info("Device identity overrides:")
    logging.info("- device_name: %s", overrides["device_name"])
    logging.info("- device_type: %s", device_type_name)
    logging.info("- device_id: %s", overrides["device_id"])
    logging.info("- preferred_locale: %s", overrides["preferred_locale"])
    logging.info("- device_software_version: %s", overrides["device_software_version"])
    logging.info("- system_info_string: %s", overrides["system_info_string"])


def log_http_request(
    method: str,
    url: str,
    payload: typing.Optional[typing.Dict[str, typing.Any]] = None,
    redacted_keys: typing.Optional[typing.Set[str]] = None,
) -> None:
    if payload is None:
        logging.info("HTTP %s %s", method, url)
        return

    redacted_keys = redacted_keys or set()
    safe_payload: typing.Dict[str, typing.Any] = {}
    for key, value in payload.items():
        if key in redacted_keys:
            safe_payload[key] = "<redacted>"
        elif key == "blob_content":
            try:
                safe_payload[key] = f"<credentials {len(json.dumps(value))} bytes>"
            except TypeError:
                safe_payload[key] = "<credentials>"
        else:
            safe_payload[key] = value
    logging.info("HTTP %s %s payload=%s", method, url, safe_payload)


def log_http_response(method: str, url: str, status_code: int) -> None:
    logging.info("HTTP %s %s -> %s", method, url, status_code)

def apply_version_overrides(overrides: typing.Dict[str, typing.Any]) -> None:
    device_software_version = overrides.get("device_software_version")
    system_info_string = overrides.get("system_info_string")

    if device_software_version:
        Version.version_string = staticmethod(lambda: device_software_version)
    if system_info_string:
        Version.system_info_string = staticmethod(lambda: system_info_string)

def get_spotify_session_and_wait_for_credentials(
    device_name: str,
    overrides: typing.Dict[str, typing.Any],
) -> None:
    """
    Starts the patched Zeroconf server. Because it's patched to be a daemon
    and not to log to the console, we can call it directly and cleanly.
    """
    credential_file = pathlib.Path("credentials.json")
    if credential_file.exists():
        console.print(f"⚠️ [yellow]Removing existing '{credential_file}'[/]")
        try:
            credential_file.unlink()
        except OSError as e:
            console.print(f"❌ [bold red]Could not remove existing 'credentials.json':[/] {e}")
            sys.exit(1)

    # Start the patched ZeroconfServer. It will run silently in the background.
    # No need to manage threads here anymore.
    builder = ZeroconfServer.Builder().set_device_name(device_name)
    if overrides.get("device_type") is not None:
        builder.set_device_type(overrides["device_type"])
    if overrides.get("device_id") is not None:
        builder.set_device_id(overrides["device_id"])
    if overrides.get("preferred_locale") is not None:
        builder.set_preferred_locale(overrides["preferred_locale"])
    zeroconf_server = builder.create()
    logging.info("Zeroconf server started for device '%s'", device_name)
    instructions = f"""
[bold yellow]1.[/] Open Spotify on another device.
[bold yellow]2.[/] Look for '[bold white]{device_name}[/]' in the Connect menu.
[bold yellow]3.[/] [bold]Transfer playback[/] to capture the session.
    """
    console.print(Panel(
        instructions,
        title=f"[cyan bold]{Icons.SPOTIFY} Connection Instructions[/]",
        subtitle=f"[dim]{Icons.NETWORK} Now available on your network[/]",
        border_style="cyan",
        expand=False
    ))

    with Status("Waiting for Spotify connection...", spinner="dots", console=console):
        while not (credential_file.exists() and credential_file.stat().st_size > 0):
            time.sleep(1)

    console.print(f"✅ [green]Connection successful! Credential file has been created.[/]")
    
    # We no longer need to manually close anything, the daemon will be handled
    # automatically on script exit.

# --- ALL OTHER FUNCTIONS (check_auth_status, authenticate_user, etc.) REMAIN UNCHANGED ---

def check_auth_status(base_url):
    """
    Check the authentication status of the Spotizerr instance using Rich for output.
    """
    console.print(Rule(f"[bold blue]{Icons.LOCK} Authentication Status Check[/]", style="blue"))
    
    auth_status_url = f"{base_url.rstrip('/')}/api/auth/status"
    
    log_http_request("GET", auth_status_url)
    with console.status(f"Checking [underline]{base_url}[/]...", spinner="dots"):
        try:
            response = requests.get(auth_status_url, timeout=10)
            log_http_response("GET", auth_status_url, response.status_code)
            response.raise_for_status()
            auth_data = response.json()
        except requests.exceptions.RequestException as e:
            console.print(f"❌ [bold red]Failed to check auth status:[/] {e}")
            return None

    auth_enabled = auth_data.get('auth_enabled', False)
    auth_icon = Icons.LOCK if auth_enabled else Icons.KEY
    status_style = "red" if auth_enabled else "green"
    
    console.print(f"{Icons.INFO} Authentication: [{status_style}]{auth_enabled}[/] {auth_icon}")
    
    if auth_enabled:
        authenticated = auth_data.get('authenticated', False)
        auth_status_icon = Icons.CHECK if authenticated else Icons.CROSS
        auth_status_style = "green" if authenticated else "red"
        
        console.print(f"{Icons.INFO} Currently authenticated: [{auth_status_style}]{authenticated}[/] {auth_status_icon}")
        console.print(f"{Icons.INFO} Registration enabled: [cyan]{auth_data.get('registration_enabled', False)}[/]")
        
        if auth_data.get('sso_enabled', False):
            providers = auth_data.get('sso_providers', [])
            console.print(f"{Icons.INFO} SSO providers: [cyan]{', '.join(providers)}[/]")
    else:
        console.print(f"✅ [green]Authentication disabled - admin privileges are automatic.[/]")
        
    return auth_data

def authenticate_user(base_url, auth_status):
    """
    Handle user authentication using Rich Prompt for choices.
    """
    if not auth_status.get('auth_enabled', False):
        console.print("✅ [green]Authentication disabled, proceeding...[/]")
        return None
    
    if auth_status.get('authenticated', False):
        console.print("✅ [green]Already authenticated.[/]")
        return "existing_token"

    console.print(Rule(f"[bold blue]{Icons.USER} User Authentication[/]", style="blue"))

    choices = ["Login to existing account"]
    if auth_status.get('registration_enabled', False):
        choices.append("Register new account")
    
    choice = Prompt.ask(
        "[bold white]Select authentication method[/]",
        choices=["Login", "Register"] if len(choices) > 1 else ["Login"],
        default="Login"
    )

    if choice == "Login":
        return login_user(base_url)
    elif choice == "Register":
        return register_user(base_url)
    else:
        console.print("❌ [bold red]Invalid choice.[/]")
        return None

def login_user(base_url):
    """
    Handle user login using Rich Prompt.
    """
    console.print(Rule(f"[bold blue]{Icons.KEY} User Login[/]", style="blue"))
    
    login_url = f"{base_url.rstrip('/')}/api/auth/login"
    
    username = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Username")
    password = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Password", password=True)
    
    if not username or not password:
        console.print("❌ [bold red]Username and password are required.[/]")
        return None
    
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    
    log_http_request("POST", login_url, payload, redacted_keys={"password"})
    with console.status("Authenticating user...", spinner="dots"):
        try:
            response = requests.post(login_url, headers=headers, json=payload, timeout=10)
            log_http_response("POST", login_url, response.status_code)
            response.raise_for_status()
            
            data = response.json()
            token = data.get("access_token")
            user_info = data.get("user", {})
            
            console.print(f"✅ [green]Welcome back, [bold]{user_info.get('username', 'unknown')}[/]![/]")
            
            role = user_info.get('role', 'unknown')
            role_icon = Icons.ADMIN if role == "admin" else Icons.USER
            console.print(f"{Icons.INFO} Role: [cyan]{role}[/] {role_icon}")
            
            return token
            
        except requests.exceptions.RequestException as e:
            console.print(f"❌ [bold red]Login failed:[/] {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    console.print(f"   [red]Details: {error_data.get('error', 'Unknown error')}[/]")
                except json.JSONDecodeError:
                    console.print(f"   [red]Response: {e.response.text}[/]")
            return None

def register_user(base_url):
    """
    Handle user registration using Rich Prompt.
    """
    console.print(Rule(f"[bold blue]{Icons.REGISTER} User Registration[/]", style="blue"))
    
    register_url = f"{base_url.rstrip('/')}/api/auth/register"
    
    username = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Choose username")
    email = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Email address")
    password = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Choose password", password=True)
    confirm_password = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Confirm password", password=True)
    
    if not all([username, email, password]):
        console.print("❌ [bold red]Username, email, and password are required.[/]")
        return None
    
    if password != confirm_password:
        console.print("❌ [bold red]Passwords do not match.[/]")
        return None
    
    payload = {"username": username, "email": email, "password": password}
    
    log_http_request("POST", register_url, payload, redacted_keys={"password"})
    with console.status("Creating account...", spinner="dots"):
        try:
            response = requests.post(register_url, headers={"Content-Type": "application/json"}, json=payload, timeout=10)
            log_http_response("POST", register_url, response.status_code)
            response.raise_for_status()
            
            console.print(f"{Icons.SUCCESS} [green]Account created for '[bold]{username}[/]'[/]")
            console.print(f"{Icons.INFO} Please log in with your new credentials.")
            
            return login_user(base_url)
            
        except requests.exceptions.RequestException as e:
            console.print(f"❌ [bold red]Registration failed:[/] {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    console.print(f"   [red]Details: {error_data.get('error', 'Unknown error')}[/]")
                except json.JSONDecodeError:
                    console.print(f"   [red]Response: {e.response.text}[/]")
            return None

def get_auth_headers(token):
    """Get headers with authentication token if available."""
    headers = {"Content-Type": "application/json"}
    if token and token != "existing_token":
        headers["Authorization"] = f"Bearer {token}"
    return headers

def check_and_configure_api_creds(base_url, auth_token=None):
    """
    Checks and configures Spotizerr API credentials using Rich UI components.
    """
    console.print(Rule(f"[bold blue]{Icons.GEAR} Spotify API Configuration[/]", style="blue"))
    api_config_url = f"{base_url.rstrip('/')}/api/credentials/spotify_api_config"
    headers = get_auth_headers(auth_token)

    try:
        log_http_request("GET", api_config_url)
        with console.status("Checking API credentials...", spinner="dots"):
            response = requests.get(api_config_url, headers=headers, timeout=10)
            log_http_response("GET", api_config_url, response.status_code)
            response.raise_for_status()

        data = response.json()
        if data.get("client_id") and data.get("client_secret"):
            console.print("✅ [green]Spotizerr API credentials are already configured.[/]")
            return True

        console.print("⚠️ [yellow]Spotizerr server is missing Spotify API credentials (client_id/client_secret).[/]")
        console.print(f"{Icons.INFO} Get these from: [underline]https://developer.spotify.com/dashboard[/]")
        
        if not Confirm.ask("[bold]Do you want to configure them now?[/]", default=True):
            console.print(f"{Icons.INFO} Please configure API credentials on your server before proceeding.")
            return False

        new_client_id = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Enter your Spotify [cyan]client_id[/]")
        new_client_secret = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Enter your Spotify [cyan]client_secret[/]")

        if not new_client_id or not new_client_secret:
            console.print("❌ [bold red]Both client_id and client_secret must be provided.[/]")
            return False

        payload = {"client_id": new_client_id, "client_secret": new_client_secret}
        
        log_http_request(
            "PUT",
            api_config_url,
            payload,
            redacted_keys={"client_secret"},
        )
        with console.status("Updating API credentials...", spinner="dots"):
            put_response = requests.put(api_config_url, headers=headers, json=payload, timeout=10)
            log_http_response("PUT", api_config_url, put_response.status_code)
            put_response.raise_for_status()

        console.print(f"{Icons.SUCCESS} [green]Successfully configured Spotizerr API credentials![/]")
        return True

    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Failed to communicate with Spotizerr API at {api_config_url}:[/] {e}")
        if hasattr(e, 'response') and e.response is not None:
            console.print(f"   [red]Response status: {e.response.status_code}[/]")
            try:
                error_data = e.response.json()
                console.print(f"   [red]Response body: {error_data.get('error', e.response.text)}[/]")
            except json.JSONDecodeError:
                console.print(f"   [red]Response body: {e.response.text}[/]")
        return False


def main():
    """Main function for the Spotizerr auth utility."""
    configure_logging()
    enable_librespot_logging()
    print_header()
    try:
        base_url = Prompt.ask(
            f"[magenta]{Icons.ARROW}[/] Enter the base URL of your Spotizerr instance",
            default="http://localhost:7171"
        )
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'http://' + base_url

        auth_status = check_auth_status(base_url)
        if auth_status is None:
            sys.exit(1)
            
        auth_token = authenticate_user(base_url, auth_status)

        if auth_status.get('auth_enabled', False) and auth_token is None:
            console.print("❌ [bold red]Authentication was required but failed. Exiting.[/]")
            sys.exit(1)

        if not check_and_configure_api_creds(base_url, auth_token):
            sys.exit(1)

        console.print(Rule(f"[bold blue]{Icons.USER} Account Configuration[/]", style="blue"))
        account_name = Prompt.ask(f"[magenta]{Icons.ARROW}[/] Enter a name for this Spotify account")
        if not account_name:
            console.print("❌ [bold red]Account name cannot be empty.[/]")
            sys.exit(1)

        region = Prompt.ask(
            f"[magenta]{Icons.ARROW}[/] Enter your Spotify region (e.g., US, DE, MX). This is the 2-letter country code"
        ).upper()
        if not region:
            console.print("❌ [bold red]Region cannot be empty.[/]")
            sys.exit(1)
        if len(region) != 2:
            console.print("❌ [bold red]Region must be a 2-letter country code.[/]")
            sys.exit(1)

        device_overrides = prompt_device_overrides(region.lower())
        apply_version_overrides(device_overrides)
        print_logging_header()
        log_device_overrides(device_overrides)

        console.print(Rule(f"[bold blue]{Icons.SPOTIFY} Spotify Session Capture[/]", style="blue"))
        device_name = device_overrides["device_name"]
        cred_file = pathlib.Path("credentials.json")
        if cred_file.exists():
            console.print(f"⚠️ [yellow]'{cred_file}' already exists.[/]")
            # Validate existing credentials before offering reuse
            can_reuse = False
            try:
                if cred_file.stat().st_size > 0:
                    with open(cred_file, "r") as f:
                        _existing = json.load(f)
                        can_reuse = isinstance(_existing, dict) and len(_existing) > 0
            except Exception:
                can_reuse = False
            if can_reuse:
                if Confirm.ask("Reuse existing 'credentials.json' without reconnecting to Spotify?", default=True):
                    console.print(f"{Icons.INFO} Using existing 'credentials.json'.")
                else:
                    get_spotify_session_and_wait_for_credentials(device_name, device_overrides)
            else:
                console.print("❌ [bold red]Existing 'credentials.json' is invalid or empty. You must reconnect to Spotify.[/]")
                if Confirm.ask("Connect now to create a fresh 'credentials.json'?", default=True):
                    get_spotify_session_and_wait_for_credentials(device_name, device_overrides)
                else:
                    console.print("❌ [bold red]Cannot continue without a valid 'credentials.json'. Exiting.[/]")
                    sys.exit(1)
        else:
            get_spotify_session_and_wait_for_credentials(device_name, device_overrides)
        
        if not cred_file.exists():
            console.print("❌ [bold red]Failed to obtain 'credentials.json'. Exiting.[/]")
            sys.exit(1)

        console.print(Rule(f"[bold blue]{Icons.DOWNLOAD} Uploading Credentials[/]", style="blue"))
        try:
            with open(cred_file, "r") as f:
                credentials_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            console.print(f"❌ [bold red]Could not read or parse 'credentials.json':[/] {e}")
            sys.exit(1)

        device_info = {
            "device_name": device_overrides.get("device_name"),
            "device_id": device_overrides.get("device_id"),
            "device_type": device_overrides.get("device_type"),
            "device_software_version": device_overrides.get("device_software_version"),
            "system_info_string": device_overrides.get("system_info_string"),
            "preferred_locale": device_overrides.get("preferred_locale"),
        }
        payload = {
            "region": region,
            "blob_content": credentials_data,
            "device_info": device_info,
        }
        api_url = f"{base_url.rstrip('/')}/api/credentials/spotify/{account_name}"
        headers = get_auth_headers(auth_token)

        log_http_request("POST", api_url, payload, redacted_keys={"blob_content"})
        with console.status(f"Registering account '[bold]{account_name}[/]' to Spotizerr...", spinner="dots"):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=10)
                log_http_response("POST", api_url, response.status_code)
                response.raise_for_status()
                console.print(f"{Icons.SUCCESS} [green]Successfully registered/updated Spotify account in Spotizerr![/]")
                if response.text and response.headers.get("Content-Type") == "application/json":
                    console.print(f"{Icons.INFO} Server response: {response.json()}")
            except requests.exceptions.RequestException as e:
                console.print(f"❌ [bold red]Failed to call Spotizerr API:[/] {e}")
                if hasattr(e, 'response') and e.response is not None:
                     console.print(f"   [red]Status: {e.response.status_code}[/]")
                     try:
                         error_data = e.response.json()
                         console.print(f"   [red]Details: {error_data.get('error', e.response.text)}[/]")
                     except json.JSONDecodeError:
                         console.print(f"   [red]Response body: {e.response.text}[/]")
                sys.exit(1)

        console.print(Rule(f"[bold blue]{Icons.CLEAN} Cleanup[/]", style="blue"))
        if Confirm.ask("Do you want to delete 'credentials.json' now?", default=True):
            try:
                if cred_file.exists():
                    cred_file.unlink()
                    console.print("✅ [green]'credentials.json' deleted.[/]")
            except OSError as e:
                console.print(f"❌ [bold red]Error deleting 'credentials.json':[/] {e}")
        else:
            console.print(f"{Icons.INFO} 'credentials.json' was kept for future use.")
         
        console.print(f"\n[bold green]{Icons.SUCCESS} Process completed successfully![/]")
        console.print(f"[dim]Your Spotify account '{account_name}' is now configured in Spotizerr.[/]\n")
        
    except KeyboardInterrupt:
        console.print(f"\n[yellow]{Icons.WARNING} Operation cancelled by user.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]An unexpected error occurred:[/bold red] {e}")
        console.print_exception(show_locals=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
