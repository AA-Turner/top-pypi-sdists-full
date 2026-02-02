"""
Test suite for version detection and User-Agent header generation
"""
import pytest
import sys
from pathlib import Path


def test_package_version_import():
    """Test that the package version can be imported correctly"""
    import chunkr_ai
    
    # Version should be a string and not "unknown"
    assert isinstance(chunkr_ai.__version__, str)
    assert chunkr_ai.__version__ != "unknown"
    # Version should be a valid semver format
    import re
    assert re.match(r"^\d+\.\d+\.\d+", chunkr_ai.__version__), f"Invalid version format: {chunkr_ai.__version__}"


def test_auth_headers_contain_correct_version():
    """Test that the HeadersMixin generates correct User-Agent with version"""
    import chunkr_ai
    from chunkr_ai.api.auth import HeadersMixin
    
    class TestClient(HeadersMixin):
        def __init__(self):
            self._api_key = "test-key"
    
    client = TestClient()
    headers = client._headers()
    
    # Check headers exist
    assert "User-Agent" in headers
    assert "Authorization" in headers
    
    # Check User-Agent format
    user_agent = headers["User-Agent"]
    expected_version = chunkr_ai.__version__
    assert f"chunkr-ai/{expected_version}" in user_agent
    assert "Python/" in user_agent
    
    # Verify it's not the wrong version (0.1.0 was the bug)
    assert "chunkr-ai/0.1.0" not in user_agent


def test_version_consistency():
    """Test that all version sources are consistent"""
    import chunkr_ai
    from chunkr_ai.api.auth import HeadersMixin
    
    # Get version from main package
    package_version = chunkr_ai.__version__
    
    # Get version from auth headers
    class TestClient(HeadersMixin):
        def __init__(self):
            self._api_key = "test-key"
    
    client = TestClient()
    headers = client._headers()
    user_agent = headers["User-Agent"]
    
    # Extract version from User-Agent
    import re
    version_match = re.search(r"chunkr-ai/(\d+\.\d+\.\d+)", user_agent)
    assert version_match is not None
    auth_version = version_match.group(1)
    
    # Versions should match
    assert package_version == auth_version


def test_pyproject_toml_version():
    """Test that pyproject.toml version matches package version"""
    import chunkr_ai
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    
    # Find pyproject.toml relative to test file
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject_path.exists(), f"pyproject.toml not found at {pyproject_path}"
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    pyproject_version = data["project"]["version"]
    package_version = chunkr_ai.__version__
    
    # Both should match and be valid
    assert pyproject_version == package_version
    import re
    assert re.match(r"^\d+\.\d+\.\d+", pyproject_version), f"Invalid version format: {pyproject_version}"


if __name__ == "__main__":
    # Run tests directly if called as script
    pytest.main([__file__, "-v"])