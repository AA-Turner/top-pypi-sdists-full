"""Google OAuth authorization for the GeoCIF dashboard.

Controls access via an email allowlist loaded from either:
  - GEOCIF_ALLOWED_USERS env var (comma-separated emails)
  - users.txt in this directory (one email per line, # comments)

If neither exists, all authenticated Google users are allowed.

Required env vars for OAuth (set before `panel serve`):
  PANEL_OAUTH_KEY      — Google OAuth client ID
  PANEL_OAUTH_SECRET   — Google OAuth client secret
  PANEL_COOKIE_SECRET  — random secret for session cookies
"""

import os
from pathlib import Path


def load_allowed_users() -> set[str]:
    """Load allowed emails from env var or users.txt."""
    env = os.environ.get("GEOCIF_ALLOWED_USERS", "")
    if env:
        return {e.strip().lower() for e in env.split(",") if e.strip()}

    users_file = Path(__file__).parent / "users.txt"
    if users_file.exists():
        return {
            line.strip().lower()
            for line in users_file.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        }

    return set()


ALLOWED_USERS = load_allowed_users()


def authorize(user_info: dict) -> bool:
    """Panel authorize_callback — return True if user's email is allowed.

    Used with: pn.config.authorize_callback = authorize
    """
    if not ALLOWED_USERS:
        return True  # no allowlist → all authenticated users OK
    email = (user_info.get("email") or "").lower()
    return email in ALLOWED_USERS
