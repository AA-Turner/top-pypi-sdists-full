from pathlib import Path
import json
import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class Credential:
    """OAuth credential data structure"""

    access_token: str
    token_type: str = "Bearer"
    refresh_token: Optional[str] = None
    expiry: Optional[str] = None
    org_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert credential to dictionary for OAuth session"""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "refresh_token": self.refresh_token,
            "expires_at": self.expiry,
            "org_id": self.org_id,
        }


def get_credential_path() -> Path:
    """Get the path to the credential file"""
    # TODO: Update this for Windows; currently, Path.home() works only on Linux and macOS.
    return Path.home() / ".config" / "orby" / "credential.json"


def get_credential() -> Optional[Credential]:
    """Load credential from file"""
    # default load from credential file
    credential = get_credential_from_file()
    # if credential is None:
    #     # if not found, load from environment variables
    #     credential = get_credential_from_env()
    return credential


# get credentials from local file
def get_credential_from_file() -> Optional[Credential]:
    """Load credential from file"""
    credential_path = get_credential_path()
    if not credential_path.exists():
        return None
    try:
        with open(credential_path, "r") as f:
            data = json.load(f)
        credential = Credential(**data)
        if credential.access_token is None or credential.refresh_token is None:
            return None
        return credential
    except Exception:
        logger.exception("Failed to load credential from file")
        return None


# get credentials from environment variables
def get_credential_from_env() -> Optional[Credential]:
    """Load credential from environment variables"""
    refresh_token = os.getenv("REFRESH_TOKEN")
    if refresh_token is None:
        logger.error("REFRESH_TOKEN is not set")
        return None
    org_id = os.getenv("ORBY_ORG_ID")
    if org_id is None:
        logger.error("ORBY_ORG_ID is not set")
        return None

    return Credential(access_token="", refresh_token=refresh_token, org_id=org_id)


def save_credential(credential: Credential) -> Path:
    """Save credential to file"""
    credential_path = get_credential_path()

    # Create directory if it doesn't exist
    credential_path.parent.mkdir(parents=True, exist_ok=True)

    # Save credential
    with open(credential_path, "w") as f:
        json.dump(asdict(credential), f, indent=2)

    # Set secure permissions (owner only)
    credential_path.chmod(0o600)
    print(f"Credential saved to {credential_path}")
    return credential_path


def clear_credential() -> bool:
    """Clear saved credential"""
    credential_path = get_credential_path()

    if credential_path.exists():
        credential_path.unlink()
        return True
    return False
