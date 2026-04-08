import importlib


def get_plato_version() -> str:
    """Get the installed plato SDK version."""
    try:
        return importlib.metadata.version("plato-sdk-v2")
    except Exception:
        return "unknown"
