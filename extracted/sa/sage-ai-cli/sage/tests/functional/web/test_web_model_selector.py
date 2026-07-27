import pytest

def test_web_model_selector():
    """
    Test the model selector component in the web platform.
    Verifies that changing the model successfully updates the user's active session model
    without relying on local storage mocks.
    """
    from sage.tests.functional.harnesses.web_client import WebClient
    
    client = WebClient()
    user = client.create_user("test_model_user@example.com", "password123")
    session = client.login(user.email, user.password)
    
    # Check default model
    current_model = client.get_active_model(session)
    assert current_model == "cloud:qwen3-coder"
    
    # Select new model
    client.set_active_model(session, "local:gemma-4")
    new_model = client.get_active_model(session)
    assert new_model == "local:gemma-4"
    
    client.logout(session)
    client.delete_user(user.email)
