"""SDK identity shared by REST requests and WebSocket handshakes."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def _sdk_version() -> str:
    try:
        return version("runta-sdk")
    except PackageNotFoundError:
        # Source-only imports don't have installed distribution metadata.
        try:
            import tomllib
        except ModuleNotFoundError:  # Python 3.10
            import tomli as tomllib
        try:
            with (Path(__file__).resolve().parents[3] / "pyproject.toml").open(
                "rb"
            ) as source:
                value = tomllib.load(source)["project"]["version"]
            return value if isinstance(value, str) and value else "unknown"
        except (OSError, ValueError, KeyError, TypeError):
            return "unknown"


USER_AGENT = f"runta-python-sdk/{_sdk_version()}"
