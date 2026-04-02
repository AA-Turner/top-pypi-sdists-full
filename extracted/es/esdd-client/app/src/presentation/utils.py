import asyncio
import datetime
import json
from functools import wraps
from typing import Any, Dict, Optional

import click
import keyring
from keyrings.alt.file import PlaintextKeyring

KEYRING_SERVICE_NAME = "esdd-cli"
keyring.set_keyring(PlaintextKeyring())


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


class TokenManager:
    @staticmethod
    def get_token() -> Optional[str]:
        token_json = keyring.get_password(KEYRING_SERVICE_NAME, "access_token")
        if token_json:
            try:
                token_data = json.loads(token_json)
                return token_data.get("access_token")
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def save_token(token_data: Dict[str, Any]) -> None:
        token_data["created_at"] = datetime.datetime.now().isoformat()
        token_json = json.dumps(token_data)
        keyring.set_password(KEYRING_SERVICE_NAME, "access_token", token_json)

    @staticmethod
    def clear_token() -> bool:
        try:
            keyring.delete_password(KEYRING_SERVICE_NAME, "access_token")
            return True
        except keyring.errors.PasswordDeleteError:
            return False

    @staticmethod
    def get_token_info() -> Optional[Dict[str, Any]]:
        token_json = keyring.get_password(KEYRING_SERVICE_NAME, "access_token")
        if token_json:
            try:
                token_data = json.loads(token_json)
                created_at = token_data.get("created_at")
                expires_in = token_data.get("expires_in", 0)
                if created_at and expires_in:
                    created = datetime.datetime.fromisoformat(created_at)
                    expires_at = created + datetime.timedelta(seconds=expires_in)
                    now = datetime.datetime.now()
                    token_data["is_valid"] = now < expires_at
                    token_data["expires_at"] = expires_at.isoformat()
                return token_data
            except (json.JSONDecodeError, KeyError):
                return None
        return None


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not TokenManager.get_token():
            click.echo("Not authenticated. Use 'esdd auth' commands first.")
            return
        return f(*args, **kwargs)

    return wrapper
