"""ESPHome Device Builder frontend (built JS bundles + index.html)."""
from pathlib import Path


def where() -> Path:
    """Return the directory containing the prebuilt frontend assets.

    The backend serves the contents of this directory as the dashboard
    UI — `index.html`, the bundled JS chunks, and any static assets
    copied in from ``public/static``.
    """
    return Path(__file__).parent
