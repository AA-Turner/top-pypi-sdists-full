"""Resolve SQLite database file paths from URLs and settings."""
from pathlib import Path
from urllib.parse import unquote, urlparse


def _normalize_sqlite_path(raw: str) -> Path:
    """Turn a URL path segment into a filesystem path (Windows-safe)."""
    if not raw:
        raise ValueError("SQLite URL has no database path")

    # sqlite:////tmp/... (legacy) → /tmp/...
    if raw.startswith("//") and not (len(raw) >= 4 and raw[3] == ":"):
        raw = "/" + raw.lstrip("/")

    # /C:/Users/... or /C:/Users/... from sqlite:///C:/...
    if len(raw) >= 3 and raw[0] == "/" and raw[2] == ":":
        raw = raw[1:]

    # sqlite:///ingest.db → single relative filename
    if raw.startswith("/") and not (len(raw) > 2 and raw[2] == ":"):
        name = raw.lstrip("/")
        if name and "/" not in name and "\\" not in name:
            return Path.cwd() / name

    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def sqlite_path_from_url(url: str) -> Path:
    """Return filesystem path for ``sqlite:///…`` (relative paths are under cwd)."""
    parsed = urlparse(str(url))
    if parsed.scheme != "sqlite":
        raise ValueError(f"Not a SQLite URL: {url!r}")

    raw = unquote(parsed.path or "")
    if parsed.netloc:
        raw = f"{parsed.netloc}{raw}"
    return _normalize_sqlite_path(raw)


def default_sqlite_url(filename: str) -> str:
    path = Path(filename)
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    # file:///… avoids sqlite:////absolute on Unix (urlparse → //tmp/…).
    return path.as_uri().replace("file:", "sqlite:", 1)
