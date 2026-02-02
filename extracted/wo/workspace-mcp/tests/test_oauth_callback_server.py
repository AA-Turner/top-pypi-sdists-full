import sys


def test_get_oauth_redirect_uri_prioritizes_env_var(monkeypatch):
    """
    Test that get_oauth_redirect_uri prioritizes the GOOGLE_OAUTH_REDIRECT_URI
    environment variable over the constructed URI.
    """
    # Set the environment variable before importing
    expected_uri = "https://my-custom-redirect.uri/callback"
    monkeypatch.setenv("GOOGLE_OAUTH_REDIRECT_URI", expected_uri)

    # Remove module from cache if already imported
    if "core.config" in sys.modules:
        del sys.modules["core.config"]

    # Import after setting env var
    from core.config import get_oauth_redirect_uri

    # Call the function
    redirect_uri = get_oauth_redirect_uri()

    # Assert that the environment variable's value is returned
    assert redirect_uri == expected_uri


def test_get_oauth_redirect_uri_constructs_uri_when_env_var_is_missing(monkeypatch):
    """
    Test that get_oauth_redirect_uri constructs the URI from WORKSPACE_MCP_BASE_URI
    and WORKSPACE_MCP_PORT when the GOOGLE_OAUTH_REDIRECT_URI environment variable is not set.
    """
    # Ensure the environment variable is not set and set the base URI and port
    monkeypatch.delenv("GOOGLE_OAUTH_REDIRECT_URI", raising=False)
    monkeypatch.setenv("WORKSPACE_MCP_BASE_URI", "http://localhost-test")
    monkeypatch.setenv("WORKSPACE_MCP_PORT", "9999")

    # Remove module from cache if already imported
    if "core.config" in sys.modules:
        del sys.modules["core.config"]

    # Import after setting env vars
    from core.config import get_oauth_redirect_uri

    # Call the function
    redirect_uri = get_oauth_redirect_uri()

    # Assert that the URI is constructed as expected
    expected_uri = "http://localhost-test:9999/oauth2callback"
    assert redirect_uri == expected_uri
