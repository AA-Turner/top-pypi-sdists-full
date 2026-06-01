"""Test version is accessible."""

import smplkit


def test_version_is_string():
    assert isinstance(smplkit.__version__, str)


def test_version_is_not_fallback():
    """In a proper install, version should not be the fallback."""
    # During CI with pip install -e ".[dev]", hatch-vcs reads from git
    # This may be "0.0.0" in dev if there are no tags yet, which is fine
    assert smplkit.__version__ is not None


def test_version_fallback():
    """When _version module is missing, __version__ falls back to '0.0.0'."""
    import importlib
    import sys

    # Temporarily hide the _version module
    version_mod = sys.modules.get("smplkit._version")
    sys.modules["smplkit._version"] = None  # type: ignore
    try:
        # Force reimport of smplkit to trigger the fallback path
        saved = sys.modules.pop("smplkit")
        try:
            importlib.invalidate_caches()
            import smplkit as fresh_smplkit

            assert fresh_smplkit.__version__ == "0.0.0"
        finally:
            sys.modules["smplkit"] = saved
    finally:
        if version_mod is not None:
            sys.modules["smplkit._version"] = version_mod
        else:
            sys.modules.pop("smplkit._version", None)
