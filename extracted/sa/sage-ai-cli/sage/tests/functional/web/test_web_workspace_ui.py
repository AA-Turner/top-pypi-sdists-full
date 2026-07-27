import pytest

def test_web_workspace_ui_renders():
    """
    Test the workspace UI structure and data loading in the web platform.
    Verifies that the workspace UI properly initializes and fetches the correct state 
    without depending on browser mocks.
    """
    from sage.tests.functional.harnesses.web_client import WebClient
    
    client = WebClient()
    user = client.create_user("test_workspace_user@example.com", "password123")
    session = client.login(user.email, user.password)
    
    # 1. Create a mock workspace project directly on backend
    workspace_id = client.create_workspace(session, "test_project")
    
    # 2. Emulate the UI load sequence
    workspace_data = client.get_workspace(session, workspace_id)
    assert workspace_data.name == "test_project"
    
    # 3. Add a file to workspace
    client.add_file_to_workspace(session, workspace_id, "main.py", "print('hello')")
    files = client.list_workspace_files(session, workspace_id)
    assert "main.py" in [f.name for f in files]
    
    client.logout(session)
    client.delete_user(user.email)
