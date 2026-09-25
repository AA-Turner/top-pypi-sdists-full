"""Canonical paths for the browser pages the API links people to.

The pages themselves are **not served here**. They live in innoday-ui (a
separate Next.js app) at ``APP_URL`` -- today https://www.havilandsoftware.com.
This app is the API, under ``/api/v1``. Its old server-rendered ``/ui`` was
removed; ``src/api/app.py`` now 301s any ``/ui`` address to the same path on
``APP_URL``, so bookmarks and already-delivered emails keep working.

The API still needs these paths because it builds links a person will open in
a browser: the device-flow ``verification_uri``, the invite email link, and the
Supabase ``redirect_to`` built by ``users.py``, ``bootstrap.py`` and
``scripts/backfill_supabase_identities.py``. innoday-ui serves each at exactly
the path named here. They are constants because a drifted path is not a
visible failure: it is an invite email that silently lands on a 404 (#414).

``LEGACY_REDIRECTS`` maps the pre-``/ui`` paths to their ``/ui`` form. Those
were baked into invite emails already delivered and into Supabase's redirect
allowlist, so they must keep working.
"""

import os

UI_PREFIX = "/ui"

AUTH_CALLBACK_PATH = f"{UI_PREFIX}/auth/callback"
INVITE_ACCEPT_PATH = f"{UI_PREFIX}/invite/accept"
DEVICE_PATH = f"{UI_PREFIX}/device"


def app_url() -> str:
    """Where innoday-ui -- the web pages -- is reached. Not the API's address.

    The API and the pages are different apps on different hosts: the CLI talks
    to the API (``www.inno.day``), and a person's browser is sent here.
    """
    return os.getenv("APP_URL", "http://localhost:3000").rstrip("/")


# Where the pages lived before the /ui prefix. Still routed, as 301s.
LEGACY_AUTH_CALLBACK_PATH = "/auth/callback"
LEGACY_INVITE_ACCEPT_PATH = "/invite/accept"
LEGACY_DEVICE_PATH = "/device"

LEGACY_REDIRECTS = {
    LEGACY_AUTH_CALLBACK_PATH: AUTH_CALLBACK_PATH,
    LEGACY_INVITE_ACCEPT_PATH: INVITE_ACCEPT_PATH,
    LEGACY_DEVICE_PATH: DEVICE_PATH,
}
