import os
import json
import time
import requests
import typer
import jwt
from prompt_toolkit import prompt

CONFIG_FILE = os.path.expanduser("~/.intctl_token")

# Keycloak config
KEYCLOAK_BASE = "https://cloak.intellithing.tech"
REALM = "intellithing_main"
CLIENT_ID = "cli"

AUTH_DEVICE_URL = f"{KEYCLOAK_BASE}/realms/{REALM}/protocol/openid-connect/auth/device"
TOKEN_URL = f"{KEYCLOAK_BASE}/realms/{REALM}/protocol/openid-connect/token"
USERINFO_URL = f"{KEYCLOAK_BASE}/realms/{REALM}/protocol/openid-connect/userinfo"

login_app = typer.Typer(help="Authenticate CLI with Keycloak")


def save_login_data(data: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


def load_login_data():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None


def clear_login_data():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        
def refresh_token_flow():
    data = load_login_data()
    if not data or "refresh_token" not in data:
        typer.echo("❌ No refresh token found. Please run 'intctl login'.")
        raise typer.Exit(1)

    res = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": data["refresh_token"],
            "client_id": CLIENT_ID
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if res.status_code == 200:
        token_data = res.json()
        data["access_token"] = token_data["access_token"]
        data["refresh_token"] = token_data.get("refresh_token", data["refresh_token"])  # some setups rotate refresh tokens
        save_login_data(data)
        typer.echo("🔁 Token refreshed successfully.")
        return data["access_token"]
    else:
        typer.echo(f"❌ Token refresh failed: {res.text}")
        clear_login_data()
        raise typer.Exit(1)

def get_valid_access_token() -> str:
    data = load_login_data()
    if not data:
        typer.echo("❌ Not logged in. Please run 'intctl login'.")
        raise typer.Exit(1)

    try:
        token_payload = jwt.decode(data["access_token"], options={"verify_signature": False})
        exp = token_payload["exp"]
        now = int(time.time())

        # Refresh if the token expires in less than 60 seconds
        if exp - now < 60:
            return refresh_token_flow()
        return data["access_token"]

    except Exception as e:
        typer.echo(f"⚠️ Failed to decode access token: {e}")
        return refresh_token_flow()


@login_app.command()
def login():
    """Login via browser and select an organization."""
    typer.echo("🔐 Starting login...")
    org = prompt("Enter your organization ID or name: ").strip()
    if not org:
        typer.echo("❌ Organization is required.")
        raise typer.Exit(1)

    # Step 1: Device Code Flow
    res = requests.post(
        AUTH_DEVICE_URL,
        data={
            "client_id": CLIENT_ID,
            "scope": "openid offline_access",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res.raise_for_status()
    device_data = res.json()

    typer.echo(f"\n🔗 Visit this URL in your browser to log in:")
    typer.echo(f"   {device_data['verification_uri_complete']}\n")

    # Step 2: Poll for token
    interval = device_data.get("interval", 5)
    for _ in range(device_data["expires_in"] // interval):
        time.sleep(interval)
        token_res = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_data["device_code"],
                "client_id": CLIENT_ID,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if token_res.status_code == 200:
            token_data = token_res.json()
            access_token = token_data["access_token"]
            refresh_token = token_data["refresh_token"]

            # Fetch user info
            userinfo_res = requests.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo = userinfo_res.json()
            username = userinfo.get("preferred_username", "unknown")

            save_login_data({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "username": username,
                "org": org,
            })

            typer.echo(f"✅ Logged in as {username} under org '{org}'.")
            return

        elif token_res.status_code == 400 and token_res.json().get("error") == "authorization_pending":
            continue
        else:
            typer.echo(f"❌ Error: {token_res.text}")
            raise typer.Exit(1)

    typer.echo("❌ Login timed out.")
    raise typer.Exit(1)


@login_app.command()
def logout():
    """Clear saved login and organization info."""
    clear_login_data()
    typer.echo("👋 Logged out successfully.")


@login_app.command()
def whoami():
    """Show current user and organization."""
    data = load_login_data()
    if not data:
        typer.echo("❌ Not logged in.")
        raise typer.Exit(1)

    typer.echo(f"👤 User: {data['username']}")
    typer.echo(f"🏢 Org:  {data['org']}")
