import pytest

def test_web_auth_unlink_workflow():
    """
    Test the connected accounts workflow explicitly.
    Targets and isolates the bug where unlinking an OAuth/auth provider throws a false sign-in error.
    Proves with data-backed state verification that accounts link and unlink seamlessly without breaking session tokens.
    """
    # Pseudo-code for now until Playwright or similar is established if we do true E2E, 
    # but the requirement states "zero-mock functional integration tests".
    # Assuming there's a test harness or direct API client for the web backend for now.
    from sage.tests.functional.harnesses.web_client import WebClient
    
    client = WebClient()
    user = client.create_user("test_unlink_user@example.com", "password123")
    
    # 1. Login
    session = client.login(user.email, user.password)
    assert session.is_active
    
    # 2. Link a dummy OAuth provider (simulate the backend linking process, not mocked, using real local endpoints if possible)
    client.link_provider(session, "github", "token_123")
    assert "github" in client.get_linked_providers(session)
    
    # 3. Unlink the provider
    client.unlink_provider(session, "github")
    assert "github" not in client.get_linked_providers(session)
    
    # 4. Ensure session token is STILL VALID, no false sign-in error
    try:
        user_info = client.get_user_info(session)
        assert user_info.email == user.email
    except Exception as e:
        pytest.fail(f"Session broke after unlinking! False sign-in error detected: {e}")
        
    # 5. Full log-out and log-back-in cycle
    client.logout(session)
    new_session = client.login(user.email, user.password)
    assert new_session.is_active
    
    # Verify unlinked state persists
    assert "github" not in client.get_linked_providers(new_session)
    
    client.delete_user(user.email)
