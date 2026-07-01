import time
import webbrowser
import httpx
from typing import Optional, Dict, Tuple
from rich.console import Console

console = Console()

CLIENT_ID = "Iv1.b507a08c87ecfe98"
SCOPE = "read:user"

def perform_device_flow() -> Optional[str]:
    """Perform GitHub OAuth Device flow and return the OAuth token."""
    # Step 1: POST https://github.com/login/device/code
    try:
        response = httpx.post(
            "https://github.com/login/device/code",
            data={"client_id": CLIENT_ID, "scope": SCOPE},
            headers={"Accept": "application/json"},
            timeout=10.0
        )
        response.raise_for_status()
    except Exception as e:
        console.print(f"[bold red]Failed to initiate device flow:[/bold red] {e}")
        return None
        
    data = response.json()
    device_code = data.get("device_code")
    user_code = data.get("user_code")
    verification_uri = data.get("verification_uri")
    interval = data.get("interval", 5)
    
    console.print(f"\n[bold green]1.[/bold green] Opening browser: [bold underline blue]{verification_uri}[/bold underline blue]")
    console.print(f"[bold green]2.[/bold green] Enter this code: [bold yellow]{user_code}[/bold yellow]\n")
    webbrowser.open(verification_uri)
    console.print("Waiting for authentication... (Press Ctrl+C to cancel)")
    
    # Step 3: Poll https://github.com/login/oauth/access_token
    while True:
        try:
            poll_response = httpx.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                },
                headers={"Accept": "application/json"},
                timeout=10.0
            )
            poll_response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code >= 500:
                console.print(f"[dim]GitHub server error ({e.response.status_code}). Retrying...[/dim]")
                time.sleep(interval)
                continue
            else:
                console.print(f"\n[bold red]Authentication failed with HTTP {e.response.status_code}:[/bold red] {e}")
                return None
        except httpx.RequestError as e:
            console.print(f"\n[bold red]Network error while polling:[/bold red] {e}")
            return None
            
        poll_data = poll_response.json()
        if "access_token" in poll_data:
            console.print("\n[bold green]Successfully authenticated with GitHub Copilot![/bold green]")
            return poll_data["access_token"]
            
        error = poll_data.get("error")
        if error == "authorization_pending":
            time.sleep(interval)
        elif error == "slow_down":
            interval += 5
            time.sleep(interval)
        elif error == "expired_token":
            console.print("[bold red]Device code expired. Please try again.[/bold red]")
            return None
        else:
            console.print(f"[bold red]Authentication failed:[/bold red] {error}")
            return None

def fetch_copilot_token(github_oauth_token: str) -> Optional[Dict]:
    """Fetch the Copilot session token using the GitHub OAuth token."""
    try:
        response = httpx.get(
            "https://api.github.com/copilot_internal/v2/token",
            headers={
                "Authorization": f"Bearer {github_oauth_token}",
                "Accept": "application/json",
                "editor-version": "vscode/1.93.0",
                "editor-plugin-version": "copilot-chat/0.20.0"
            },
            timeout=10.0
        )
        if response.status_code == 401:
            return None # Token expired or invalid
        response.raise_for_status()
        return response.json()
    except Exception as e:
        console.print(f"[dim]Failed to fetch Copilot token: {e}[/dim]")
        return None
