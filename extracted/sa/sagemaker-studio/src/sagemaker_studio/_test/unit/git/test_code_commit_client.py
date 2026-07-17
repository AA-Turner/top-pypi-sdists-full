import unittest
from unittest.mock import Mock, patch

from sagemaker_studio.git.git_code_commit_client import GitCodeCommitClient


class TestGitCodeCommitClient(unittest.TestCase):
    def setUp(self):
        self.mock_datazone_api = Mock()
        self.mock_project_api = Mock()
        self.git_code_commit_client = GitCodeCommitClient(
            datazone_api=self.mock_datazone_api,
            project_api=self.mock_project_api,
            domain_identifier="dzd_bx2a2afyvn2hlc",
            project_identifier="449et7665a6p3k",
        )

    @patch.object(GitCodeCommitClient, "_get_client")
    def test_get_clone_url(self, mock_get_client):
        mock_code_commit_client = Mock()
        mock_get_client.return_value = mock_code_commit_client
        mock_code_commit_client.get_repository.return_value = {
            "repositoryMetadata": {
                "cloneUrlHttp": "https://git-codecommit.us-west-2.amazonaws.com/v1/repos/sagemaker-studio-61p1t7s1b4n40g-dev"
            }
        }
        result = self.git_code_commit_client.get_clone_url("sagemaker-studio-61p1t7s1b4n40g-dev")
        self.assertEqual(
            result,
            {
                "cloneUrl": "https://git-codecommit.us-west-2.amazonaws.com/v1/repos/sagemaker-studio-61p1t7s1b4n40g-dev"
            },
        )
        mock_code_commit_client.get_repository.assert_called_once_with(
            repositoryName="sagemaker-studio-61p1t7s1b4n40g-dev"
        )

    def test_get_client_uses_connection_credentials(self):
        """Test that _get_client uses IAM connection credentials instead of environment credentials."""
        self.mock_project_api.get_project_default_environment.return_value = {
            "awsAccountId": "1234567890",
            "awsAccountRegion": "us-west-2",
            "domainId": "dzd_bx2a2afyvn2hlc",
            "id": "environment_123",
        }

        expected_creds = {
            "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "secretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "sessionToken": "FwoGZXIvYXdzEBY...",
            "expiration": "2026-07-06T23:00:00Z",
        }

        self.mock_datazone_api.list_connections.return_value = {
            "items": [{"connectionId": "conn-123", "name": "default.iam"}]
        }

        self.mock_datazone_api.get_connection.return_value = {
            "connectionId": "conn-123",
            "name": "default.iam",
            "type": "IAM",
            "connectionCredentials": expected_creds,
        }

        with patch("sagemaker_studio.git.git_code_commit_client.Session") as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session
            mock_client = Mock()
            mock_session.client.return_value = mock_client

            result = self.git_code_commit_client._get_client()

            mock_session.client.assert_called_once_with(
                service_name="codecommit",
                region_name="us-west-2",
                aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
                aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                aws_session_token="FwoGZXIvYXdzEBY...",
            )
            self.assertEqual(result, mock_client)

        # Verify get_environment_credentials was NOT called
        self.mock_datazone_api.get_environment_credentials.assert_not_called()

    def test_get_client_raises_when_identifiers_none(self):
        """Test that _get_client raises ValueError when identifiers are None."""
        client = GitCodeCommitClient(
            datazone_api=self.mock_datazone_api,
            project_api=self.mock_project_api,
            domain_identifier=None,
            project_identifier=None,
        )
        with self.assertRaises(ValueError) as context:
            client._get_client()
        self.assertEqual(str(context.exception), "Domain and project identifiers cannot be None")
