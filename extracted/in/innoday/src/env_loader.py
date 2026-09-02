"""
Environment-aware dotenv loader.

Loads the right .env file based on the ENVIRONMENT variable:
  local  → .env.local  (local Supabase, default for dev machines)
  dev    → .env.dev    (shared Supabase cloud dev project)
  production → no file (vars injected directly by the platform)

ENVIRONMENT must always be set explicitly. The only exception is local
development: if unset and .env.local exists, we default to local with a
visible warning.

``get_environment()`` at the bottom is the read side of the same variable --
the one resolver any endpoint reporting "which environment am I?" must use.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


class EnvironmentNotSetError(RuntimeError):
    """Raised when ENVIRONMENT is unset and no local dev fallback is available."""


def load_env(root: Path = None) -> str:
    """Load the appropriate .env file. Returns the path that was loaded."""
    root = root or Path(__file__).parent.parent

    candidates = {
        "local": root / ".env.local",
        "dev": root / ".env.dev",
        "development": root / ".env.dev",
    }

    raw_env = os.environ.get("ENVIRONMENT")

    if raw_env is None:
        local_env_path = candidates["local"]
        if local_env_path.exists():
            print(
                "WARNING: ENVIRONMENT not set — defaulting to 'local'. "
                "Set ENVIRONMENT explicitly to suppress this warning.",
                file=sys.stderr,
            )
            load_dotenv(dotenv_path=local_env_path, override=False)
            return str(local_env_path)
        raise EnvironmentNotSetError(
            "ENVIRONMENT must be set to 'local', 'dev', or 'production'. "
            "Cannot start with ambiguous environment."
        )

    env = raw_env.lower()
    if env not in ("local", "dev", "development", "production"):
        raise EnvironmentNotSetError(
            f"ENVIRONMENT must be set to 'local', 'dev', or 'production' (got '{raw_env}'). "
            "Cannot start with ambiguous environment."
        )

    # production intentionally has no .env file — vars are injected by the platform
    path = candidates.get(env)
    if path is not None and path.exists():
        load_dotenv(dotenv_path=path, override=False)
        return str(path)

    return "(none — environment variables injected by platform)"


def get_environment() -> str:
    """Which environment this process is running as, for reporting to callers.

    The single resolver behind both ``/health`` and ``/api/v1/public/status``
    (#619). ``/health`` used to compute its own answer as
    ``"development" if DEBUG else "production"`` -- that reports *"is DEBUG
    off"* under the name ``environment``, and it is how the dev deployment
    serving ``www.inno.day`` reported ``production`` while
    ``/api/v1/public/status``, seconds later in the same process, reported
    ``dev``. Anyone trusting the first endpoint believed they were looking at
    prod.

    Lives here because this module already owns what ``ENVIRONMENT`` means:
    it is the value ``load_env`` validates and dispatches the dotenv choice
    on. Unlike ``load_env`` this does not validate -- reporting must never be
    able to fail a request -- so whatever is set is returned verbatim, and
    ``production`` is the fallback (matching what ``/public/status``, the
    endpoint that was already right, has always defaulted to).
    """
    return os.environ.get("ENVIRONMENT", "").strip() or "production"
