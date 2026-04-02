import datetime
import json

import click
import jwt

from app.src.application.services.auth_service import AuthService
from app.src.infrastructure.repositories.git_oauth_repository import GitOAuthRepository
from app.src.infrastructure.repositories.mpds_oauth_repository import (
    MPDSOAuthRepository,
)
from app.src.presentation.cli import cli
from app.src.presentation.utils import TokenManager, async_command


@cli.group()
def auth():
    """Authentication commands"""
    pass


@auth.command()
@click.option("--redirect", help="Redirect URL")
def github(redirect):
    """GitHub authentication"""
    git_repo = GitOAuthRepository()
    url = git_repo.generate_auth_url(redirect)
    click.echo("GitHub Auth URL:")
    click.echo(url)


@auth.command()
@click.option("--redirect", help="Redirect URL")
def mpds(redirect):
    """MPDS authentication"""
    mpds_repo = MPDSOAuthRepository()
    url = mpds_repo.generate_auth_url(redirect)
    click.echo("MPDS Auth URL:")
    click.echo(url)


@auth.command()
@click.argument("jwt_token")
@async_command
async def set_token(jwt_token):
    """Set JWT token directly"""
    try:
        auth_service = AuthService()
        auth_service._current_token = jwt_token
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
        user_id = int(payload.get("sub", 0))

        is_authenticated = await auth_service.is_authenticated(jwt_token)
        if not is_authenticated:
            click.echo("wrong access token")
            return

        token_data = {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user_id": user_id,
            "expires_in": 604800,
            "payload": payload,
        }
        TokenManager.save_token(token_data)
        click.echo("Token saved")
        click.echo(json.dumps({"user_id": user_id, "token_type": "bearer"}, indent=2))
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@auth.command()
def info():
    """Show token information"""
    token_data = TokenManager.get_token_info()
    if token_data:
        click.echo("Token Information:")
        click.echo(json.dumps(token_data, indent=2, default=str))
    else:
        click.echo("No token found")


@auth.command()
def decode():
    """Decode JWT token"""
    token = TokenManager.get_token()
    if not token:
        click.echo("No token found")
        return
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        click.echo("JWT Payload:")
        click.echo(json.dumps(payload, indent=2))
        user_id = payload.get("sub")
        if user_id:
            click.echo(f"\nUser ID: {user_id}")
        exp = payload.get("exp")
        if exp:
            exp_time = datetime.datetime.fromtimestamp(exp)
            click.echo(f"Expires: {exp_time}")
    except Exception as e:
        click.echo(f"Error decoding token: {str(e)}")


@auth.command()
def logout():
    """Logout (clear token)"""
    if TokenManager.clear_token():
        click.echo("Logged out")
    else:
        click.echo("Logout failed")
