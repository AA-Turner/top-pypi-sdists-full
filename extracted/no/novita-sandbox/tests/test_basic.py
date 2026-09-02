"""
Basic tests for Novita Agent Sandbox SDK.
"""

from novita_sandbox import __version__

def test_version():
    """Test that version is defined."""
    assert __version__ == "1.0.0"
