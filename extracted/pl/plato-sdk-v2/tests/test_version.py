"""Tests for package version retrieval."""

import re


def test_plato_version_is_set():
    """Test that plato.__version__ is set and valid."""
    import plato

    assert hasattr(plato, "__version__")
    assert plato.__version__ is not None
    assert isinstance(plato.__version__, str)


def test_plato_version_is_semver():
    """Test that plato.__version__ follows semver format."""
    import plato

    # Should match X.Y.Z or X.Y.Z.devN format
    pattern = r"^\d+\.\d+\.\d+(\.dev\d+)?$"
    assert re.match(pattern, plato.__version__), f"Version {plato.__version__} doesn't match semver"


def test_plato_version_matches_metadata():
    """Test that plato.__version__ matches importlib.metadata."""
    from importlib.metadata import version

    import plato

    expected = version("plato-sdk-v2")
    assert plato.__version__ == expected
