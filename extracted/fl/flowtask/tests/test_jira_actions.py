import pytest
from unittest.mock import patch, MagicMock
from jira import JIRAError
from resources.jira import JiraActions

# Mocks para los datos de prueba
SERVER = "https://fake-jira-server.com"
EMAIL = "test@example.com"
TOKEN = "fake_token"

@pytest.fixture
def jira_actions():
    """Fixture para inicializar una instancia de JiraActions"""
    return JiraActions(SERVER, EMAIL, TOKEN)

def test_create_issue_success(jira_actions):
    """Prueba para crear un issue exitosamente"""
    with patch.object(jira_actions.jira, 'create_issue') as mock_create_issue:
        mock_create_issue.return_value = MagicMock(key='TEST-123')
        issue = jira_actions.create_issue("TEST", "Issue Summary", "Issue Description")
        assert issue.key == 'TEST-123'
        mock_create_issue.assert_called_once_with(fields={
            'project': {'key': 'TEST'},
            'summary': 'Issue Summary',
            'description': 'Issue Description',
            'issuetype': {'name': 'Bug'}
        })

def test_create_issue_validation_error(jira_actions):
    """Prueba para capturar error de validación al crear un issue"""
    with patch.object(jira_actions.jira, 'create_issue', side_effect=JIRAError(status_code=400)) as mock_create_issue:
        with pytest.raises(ValueError, match="Validation error while Creating an issue"):
            jira_actions.create_issue("TEST", "Issue Summary", "Issue Description")
        mock_create_issue.assert_called_once()

def test_add_comment_success(jira_actions):
    """Prueba para agregar un comentario exitosamente"""
    with patch.object(jira_actions.jira, 'add_comment') as mock_add_comment:
        mock_add_comment.return_value = "Comment added"
        result = jira_actions.add_comment("TEST-123", "This is a comment")
        assert result == "Comment added"
        mock_add_comment.assert_called_once_with(jira_actions.jira.issue("TEST-123"), "This is a comment")

def test_transition_issue_success(jira_actions):
    """Prueba para realizar una transición exitosa"""
    with patch.object(jira_actions.jira, 'transitions') as mock_transitions, \
         patch.object(jira_actions.jira, 'transition_issue') as mock_transition_issue:
        
        mock_transitions.return_value = [{'id': '1', 'name': 'Start Progress'}, {'id': '2', 'name': 'Close Issue'}]
        issue = MagicMock(key='TEST-123')
        with patch.object(jira_actions.jira, 'issue', return_value=issue):
            result = jira_actions.transition_issue("TEST-123", "Start Progress", "Transition comment")
            assert result == issue
            mock_transition_issue.assert_called_once_with("TEST-123", '1', comment="Transition comment")

def test_add_worklog_invalid_time_format(jira_actions):
    """Prueba para capturar error de formato de tiempo inválido en worklog"""
    with pytest.raises(ValueError, match="Invalid time format"):
        jira_actions.add_worklog("TEST-123", "invalid_time_format", "Worklog comment")

def test_handle_jira_error(jira_actions):
    """Prueba para el manejo de errores personalizados"""
    error = JIRAError(status_code=403)
    with pytest.raises(PermissionError, match="Insufficient permissions to Creating an issue"):
        jira_actions.handle_jira_error(error, "Creating an issue")
