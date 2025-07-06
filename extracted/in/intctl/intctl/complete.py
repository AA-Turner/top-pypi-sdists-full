# intctl/commands/complete.py

import os
import json
import typer
import requests
from intctl.config import load_config
from dotenv import load_dotenv
load_dotenv()

API_BASE_URL = os.getenv("INTELLITHING_API_BASE_URL", "http://34.39.118.103")

def _handle_api_error(response: requests.Response):
    """A helper to parse and display API errors."""
    try:
        error_detail = response.json().get("detail", response.text)
    except requests.exceptions.JSONDecodeError:
        error_detail = response.text
    
    typer.secho(f"\n❌ API Error ({response.status_code}): {error_detail}", fg=typer.colors.RED)
    raise typer.Exit(code=1)

def _get_finalization_payload() -> dict:
    """Loads config and builds the payload, performing validation."""
    cfg = load_config()
    
    required_keys = [
        "setup_uuid", "organization_name", "user_uuid", "organization_uuid",
        "workspace_uuid", "region", "secret_name", "domain"
    ]
    
    missing_keys = [key for key in required_keys if key not in cfg or not cfg[key]]
    if missing_keys:
        typer.secho("\n❌ Configuration is incomplete. Cannot complete setup.", fg=typer.colors.RED)
        typer.secho(f"   Missing required values: {', '.join(missing_keys)}", fg=typer.colors.RED)
        typer.secho("   Please run 'intctl sync' and 'intctl setup' first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    return {
        "setup_uuid": cfg["setup_uuid"],
        "organization_name": cfg["organization_name"],
        "user_uuid": cfg["user_uuid"],
        "organization_uuid": cfg["organization_uuid"],
        "workspace_uuid": cfg["workspace_uuid"],
        "region": cfg["region"],
        "secret_name": cfg["secret_name"],
        "url": f"https://{cfg['domain']}"
    }

def post_completion_data():
    """Pushes the final, complete configuration to the /finalize endpoint."""
    typer.secho(" finalizing setup with INTELLITHING...", fg=typer.colors.CYAN)
    payload = _get_finalization_payload()
    
    typer.echo("\nSending the following data to finalize setup:")
    typer.echo(json.dumps(payload, indent=2))

    if not typer.confirm("\nDo you want to proceed?"):
        raise typer.Abort()

    endpoint = f"{API_BASE_URL}/finalize"
    try:
        response = requests.post(endpoint, json=payload, timeout=30)
        if response.status_code == 200:
            domain = payload['url']
            typer.secho("\n🎉 Success! Your workspace setup has been finalized.", fg=typer.colors.GREEN, bold=True)
            typer.secho(f"   Your API gateway is now: {domain}", fg=typer.colors.GREEN)
        else:
            _handle_api_error(response)
    except requests.exceptions.RequestException as e:
        typer.secho(f"\n❌ Network Error: Could not connect to the API at {API_BASE_URL}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

def show_manual_data():
    """Displays the finalization payload for manual entry."""
    typer.secho("📋 Below is the data required for manual finalization:", fg=typer.colors.YELLOW)
    payload = _get_finalization_payload()
    typer.echo(json.dumps(payload, indent=2))