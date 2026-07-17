import unittest
from unittest.mock import Mock

from botocore.exceptions import ClientError

from sagemaker_studio.credentials import CredentialsVendingService
from sagemaker_studio.exceptions import AWSClientException


class TestCredentialsVendingService(unittest.TestCase):

    def setUp(self):
        self.mock_datazone_api = Mock()
        self.mock_project_api = Mock()
        self.credentials_service = CredentialsVendingService(
            self.mock_datazone_api, self.mock_project_api
        )

    def test_get_domain_execution_role_credential_in_space_validation_exception(self):
        error_response = {"Error": {"Code": "ValidationException", "Message": "Invalid parameters"}}
        self.mock_datazone_api.get_domain_execution_role_credentials.side_effect = ClientError(
            error_response, "GetDomainExecutionRoleCredentialInSpace"  # type: ignore
        )
        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_domain_execution_role_credential_in_space("invalid-domain")
        self.assertEqual(
            "Invalid value for `domain_identifier`, must match regular expression `^dzd[-_][a-zA-Z0-9_-]{1,36}$`",
            str(context.exception),
        )

    def test_get_domain_execution_role_credentials_in_space_access_denied_exception(self):
        error_response = {
            "Error": {
                "Code": "AccessDeniedException",
                "Message": "Failed to find the user profile name info",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.get_domain_execution_role_credentials.side_effect = ClientError(
            error_response, "GetDomainExecutionRoleCredentialInSpace"  # type: ignore
        )
        with self.assertRaises(AWSClientException) as context:
            self.credentials_service.get_domain_execution_role_credential_in_space("dzd_domain123")
            self.assertTrue("AccessDeniedException" in str(context.exception))

    def test_get_domain_execution_role_credentials_in_space_validation_exception(self):
        error_response = {
            "Error": {
                "Code": "ValidationException",
                "Message": "ValidationException",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.get_domain_execution_role_credentials.side_effect = ClientError(
            error_response, "GetDomainExecutionRoleCredentialInSpace"  # type: ignore
        )
        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_domain_execution_role_credential_in_space("dzd_domain123")
            self.assertTrue("Invalid input parameters" in str(context.exception))

    def test_get_project_default_iam_connection_credentials_express_mode(self):
        """Test getting credentials via default.iam connection (EXPRESS mode)."""
        expected_creds = {
            "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "secretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "sessionToken": "FwoGZXIvYXdzEBY...",
            "expiration": "2026-07-06T23:00:00Z",
        }

        # Express mode: default.iam exists (single list_connections call)
        self.mock_datazone_api.list_connections.return_value = {
            "items": [{"connectionId": "conn-123", "name": "default.iam"}]
        }

        self.mock_datazone_api.get_connection.return_value = {
            "connectionId": "conn-123",
            "name": "default.iam",
            "type": "IAM",
            "connectionCredentials": expected_creds,
        }

        result = self.credentials_service.get_project_default_iam_connection_credentials(
            "domain_123", "project_123"
        )
        assert result == expected_creds
        self.mock_datazone_api.list_connections.assert_called_once_with(
            domainIdentifier="domain_123",
            projectIdentifier="project_123",
            type="IAM",
            name="default.iam",
        )
        self.mock_datazone_api.get_connection.assert_called_once_with(
            domainIdentifier="domain_123",
            identifier="conn-123",
            withSecret=True,
        )

    def test_get_project_default_iam_connection_credentials_standard_mode(self):
        """Test getting credentials via project.iam connection (STANDARD mode)."""
        expected_creds = {
            "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "secretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "sessionToken": "FwoGZXIvYXdzEBY...",
            "expiration": "2026-07-06T23:00:00Z",
        }

        # Standard mode: default.iam does NOT exist, falls back to project.iam
        self.mock_datazone_api.list_connections.side_effect = [
            # First call: check default.iam -> empty
            {"items": []},
            # Second call: check project.iam -> found
            {"items": [{"connectionId": "conn-456", "name": "project.iam"}]},
        ]

        self.mock_datazone_api.get_connection.return_value = {
            "connectionId": "conn-456",
            "name": "project.iam",
            "type": "IAM",
            "connectionCredentials": expected_creds,
        }

        result = self.credentials_service.get_project_default_iam_connection_credentials(
            "domain_123", "project_123"
        )
        assert result == expected_creds
        self.mock_datazone_api.get_connection.assert_called_once_with(
            domainIdentifier="domain_123",
            identifier="conn-456",
            withSecret=True,
        )

    def test_get_project_default_iam_connection_credentials_no_connection_found(self):
        """Test error when no IAM connection exists."""
        # Neither default.iam nor project.iam exist
        self.mock_datazone_api.list_connections.side_effect = [
            {"items": []},  # default.iam not found
            {"items": []},  # project.iam not found
        ]

        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_project_default_iam_connection_credentials(
                "domain_123", "project_123"
            )
        self.assertIn("No default IAM connection found", str(context.exception))

    def test_get_project_default_iam_connection_credentials_no_credentials_in_response(self):
        """Test error when GetConnection returns no connectionCredentials."""
        self.mock_datazone_api.list_connections.return_value = {
            "items": [{"connectionId": "conn-123", "name": "default.iam"}]
        }

        self.mock_datazone_api.get_connection.return_value = {
            "connectionId": "conn-123",
            "name": "default.iam",
            "type": "IAM",
            # No connectionCredentials key
        }

        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_project_default_iam_connection_credentials(
                "domain_123", "project_123"
            )
        self.assertIn("No credentials returned", str(context.exception))

    def test_get_project_default_iam_connection_credentials_validation_exception(self):
        """Test ValidationException raises ValueError."""
        error_response = {
            "Error": {
                "Code": "ValidationException",
                "Message": "ValidationException",
            },
        }
        self.mock_datazone_api.list_connections.side_effect = ClientError(
            error_response, "ListConnections"  # type: ignore
        )

        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_project_default_iam_connection_credentials(
                "domain_123", "project_123"
            )
        self.assertIn("Invalid input parameters", str(context.exception))

    def test_get_project_default_iam_connection_credentials_other_exception(self):
        """Test non-ValidationException ClientError raises ValueError with proper message."""
        error_response = {
            "Error": {
                "Code": "AccessDeniedException",
                "Message": "Access denied",
            },
        }
        self.mock_datazone_api.list_connections.side_effect = ClientError(
            error_response, "ListConnections"  # type: ignore
        )

        with self.assertRaises(ValueError) as context:
            self.credentials_service.get_project_default_iam_connection_credentials(
                "domain_123", "project_123"
            )
        self.assertIn("Unable to get IAM connection credentials", str(context.exception))

    def test_get_project_default_environment_credentials_delegates_to_connection(self):
        """Test that the deprecated method delegates to the new connection method."""
        expected_creds = {
            "accessKeyId": "123",
            "secretAccessKey": "456",
            "sessionToken": "789",
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

        result = self.credentials_service.get_project_default_environment_credentials(
            "domain_123", "project_123"
        )
        assert result == expected_creds
