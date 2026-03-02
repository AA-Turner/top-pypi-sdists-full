"""EmDash Core - FastAPI server for code intelligence."""

from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

try:
    __version__ = version("emdash-ai")
except PackageNotFoundError:
    # Dev mode: read from pyproject.toml
    try:
        import tomllib
        _pyproject = Path(__file__).resolve().parent.parent.parent.parent / "pyproject.toml"
        if _pyproject.exists():
            __version__ = tomllib.loads(_pyproject.read_text())["project"]["version"]
        else:
            __version__ = "0.0.0-dev"
    except Exception:
        __version__ = "0.0.0-dev"
