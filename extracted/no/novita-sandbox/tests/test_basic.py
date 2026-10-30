"""
Basic tests for Novita Agent Sandbox SDK.
"""

from importlib.metadata import version

from novita_sandbox import __version__


def test_version_matches_installed_distribution():
    """Expose the version of the distribution that the caller installed."""
    assert __version__ == version("novita-sandbox")
