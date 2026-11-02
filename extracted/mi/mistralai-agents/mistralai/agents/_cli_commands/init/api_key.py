"""The project's `.env`: the Mistral API key the agent calls the API with. `.gitignore` keeps it out of git."""

from __future__ import annotations

import os
import webbrowser
from pathlib import Path

# Opens the create-key dialog of the Studio API keys page.
STUDIO_API_KEYS_URL = "https://console.mistral.ai/api-keys/new"
ENV_FILE = ".env"
ENV_VARIABLE = "MISTRAL_API_KEY"


def checked(api_key: str) -> str:
    """The key, stripped. A key with whitespace inside would not survive as one `.env` line."""
    stripped = api_key.strip()
    if not stripped or any(character.isspace() for character in stripped):
        raise ValueError("An API key is one word, with no spaces. Paste it again.")
    return stripped


def open_studio() -> bool:
    """Open the Studio page that creates a key, and say whether a browser opened it."""
    try:
        return webbrowser.open(STUDIO_API_KEYS_URL)
    except webbrowser.Error:
        return False


def write_env(folder: Path, api_key: str) -> None:
    """Write `.env` with the key, or with an empty value to fill in when `api_key` is empty.

    Readable by the user only, since it holds a secret. O_EXCL refuses any path already there, such as a
    link to another file, rather than write the key through it.
    """
    descriptor = os.open(folder / ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as env:
        env.write(f"{ENV_VARIABLE}={api_key}\n")
