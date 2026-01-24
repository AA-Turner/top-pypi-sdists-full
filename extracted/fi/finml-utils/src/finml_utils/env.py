import os
import warnings
from pathlib import Path

from dotenv import load_dotenv


def get_env(key: str) -> str | None:
    try:
        # Try to load .env file with explicit path
        env_file = Path.cwd() / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Fallback to automatic discovery
            load_dotenv()
        return os.environ.get(key)
    except:  # noqa
        warnings.warn(f"Couldn't load {key}")  # noqa
        return None
