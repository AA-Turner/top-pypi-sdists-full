import os
import tempfile
from pathlib import Path
from typing import Callable


def env_int(env_var: str, default: int | None = None) -> Callable[[], int | None]:
    def getter() -> int | None:
        val = os.environ.get(env_var, None)
        if val is not None:
            return int(val)
        return default

    return getter


def env_str(env_var: str, default: str | None = None) -> Callable[[], str | None]:
    def getter() -> str | None:
        val = os.environ.get(env_var, default)
        return val

    return getter


def env_bool(env_var: str, default: bool | None = None) -> Callable[[], bool]:
    truthy = {"true", "t", "1", "yes", "y"}
    falsy = {"false", "f", "0", "no", "n"}

    def getter() -> bool:
        val = os.environ.get(env_var, None)
        if val is None:
            if default is not None:
                return default
        else:
            lc_val = val.lower()
            if lc_val in truthy:
                return True
            if lc_val in falsy:
                return False
        raise ValueError(
            f"env var '{env_var}' contains invalid literal for boolean: '{val}' and no default set"
        )

    return getter


def env_bool_aliased(
    env_vars: list[str], default: bool | None = None
) -> Callable[[], bool]:
    """Read the first of ``env_vars`` that is set (precedence order, highest first).

    Lets a shared, unprefixed variable (e.g. ``ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED``)
    override a service-prefixed alias (``ISTARI_CLIENT_IDENTITY_SERVICE_ENABLED``), so one
    platform value configures every client. Falls back to ``default`` when none is set.
    """
    truthy = {"true", "t", "1", "yes", "y"}
    falsy = {"false", "f", "0", "no", "n"}

    def getter() -> bool:
        for env_var in env_vars:
            val = os.environ.get(env_var, None)
            if val is not None:
                lc_val = val.lower()
                if lc_val in truthy:
                    return True
                if lc_val in falsy:
                    return False
                raise ValueError(
                    f"env var '{env_var}' contains invalid literal for boolean: '{val}'"
                )
        if default is not None:
            return default
        raise ValueError(f"none of {env_vars} is set and no default was provided")

    return getter


def env_cache_root(env_var: str) -> Callable[[], Path]:
    def getter() -> Path:
        env_val = os.environ.get(env_var, None)
        if env_val:
            dir = Path(env_val)
            if not dir.is_dir():
                raise NotADirectoryError(dir)
            return dir
        else:
            dir = Path(tempfile.mkdtemp(prefix="istari-client-cache-"))
            dir.mkdir(parents=True, exist_ok=True)
            return dir

    return getter
