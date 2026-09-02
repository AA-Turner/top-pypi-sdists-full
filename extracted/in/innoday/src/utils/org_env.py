"""
Org environment loader.

Reads env/orgs/<alias> and exposes a clean, board-type-agnostic config.
Used by the CLI and agent to load org credentials without hard-coding
JIRA_*, LINEAR_*, TRELLO_* var names.

The org identifier is the org **alias** (globally unique). The env file is
named for it (env/orgs/<alias>) and stamps ``ORG_ALIAS=`` inside. There is no
``ORG_SLUG`` fallback — ``slug`` is fully retired.
"""

from pathlib import Path
from typing import Optional


class OrgEnv:
    """Board-agnostic org configuration loaded from env/orgs/<alias>."""

    def __init__(
        self,
        alias: str,
        org_name: Optional[str] = None,
        github_org: Optional[str] = None,
        github_topic: Optional[str] = None,
        board_type: Optional[str] = None,
        board_url: Optional[str] = None,
        board_api_token: Optional[str] = None,
        board_api_email: Optional[str] = None,
    ):
        self.alias = alias
        self.org_name = org_name
        self.github_org = github_org
        self.github_topic = github_topic
        self.board_type = board_type
        self.board_url = board_url
        self.board_api_token = board_api_token
        self.board_api_email = board_api_email

    @property
    def integration_token(self) -> Optional[str]:
        """
        Returns the value to use as X-Integration-Token header.

        Jira:   "email:token" (Basic Auth format the API expects)
        Others: raw token
        """
        if not self.board_api_token:
            return None
        if self.board_type == "jira" and self.board_api_email:
            return f"{self.board_api_email}:{self.board_api_token}"
        return self.board_api_token

    def __repr__(self) -> str:
        token_set = "set" if self.board_api_token else "not set"
        return (
            f"OrgEnv(alias={self.alias!r}, board_type={self.board_type!r}, "
            f"github_org={self.github_org!r}, token={token_set})"
        )


def _default_orgs_dir() -> Path:
    """Return env/orgs/ relative to the project root."""
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "pyproject.toml").exists():
            return parent / "env" / "orgs"
    return Path.cwd() / "env" / "orgs"


def load_org_env(alias: str, orgs_dir: Optional[Path] = None) -> Optional["OrgEnv"]:
    """
    Load org config from env/orgs/<alias>.

    Returns None if the file doesn't exist (org not configured locally).
    Does NOT raise — callers decide whether a missing file is an error.

    Args:
        alias: org alias, e.g. "acme"
        orgs_dir: directory containing org files; defaults to env/orgs/
    """
    if orgs_dir is None:
        orgs_dir = _default_orgs_dir()

    env_file = orgs_dir / alias
    if not env_file.exists():
        return None

    values: dict[str, str] = {}
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        values[key.strip()] = val.strip()

    return OrgEnv(
        # The org alias — from ORG_ALIAS, or the filename (which IS the alias).
        # No ORG_SLUG fallback; slug is retired.
        alias=values.get("ORG_ALIAS") or alias,
        org_name=values.get("ORG_NAME") or None,
        github_org=values.get("GITHUB_ORG") or None,
        github_topic=values.get("GITHUB_TOPIC") or None,
        board_type=values.get("BOARD_TYPE") or None,
        board_url=values.get("BOARD_URL") or None,
        board_api_token=values.get("BOARD_API_TOKEN") or None,
        board_api_email=values.get("BOARD_API_EMAIL") or None,
    )


def load_org_env_required(alias: str, orgs_dir: Optional[Path] = None) -> "OrgEnv":
    """Same as load_org_env but raises ValueError if the file is missing."""
    org = load_org_env(alias, orgs_dir)
    if org is None:
        raise ValueError(
            f"No org env file found for '{alias}'.\n"
            f"Create it: cp env/orgs/example env/orgs/{alias}\n"
            f"Then fill in BOARD_TYPE, BOARD_URL, BOARD_API_TOKEN, etc."
        )
    return org
