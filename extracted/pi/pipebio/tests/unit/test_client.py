import pytest
from unittest.mock import patch, MagicMock
from pipebio.pipebio_client import PipebioClient
from pipebio.models.job_type import JobType


class TestPipeBioClient:

    def test_get_user(self):
        """Test getting user information."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "orgs": [{"id": "test-org-id"}]
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPE_API_KEY': 'test-key'}):
            
            # Create a mock session instance
            mock_session = MagicMock()
            mock_session.get.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            # Create the client and test
            client = PipebioClient(url='https://test-api.pipebio.com')
            result = client.get_user()
            
            assert result["firstName"] == "Test"
            assert result["lastName"] == "User"
            assert mock_session.get.call_args_list[-1].args[0] == 'me'

    def test_upload_file(self):
        """Test file upload functionality."""
        # Create separate mock responses for each API call
        mock_aws_response = MagicMock()
        mock_aws_response.status_code = 200
        mock_aws_response.json.return_value = {"stack": "test-stack"}

        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "org": {"id": "test-org-id"}
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPE_API_KEY': 'test-key'}), \
             patch('os.path.getsize', return_value=1024):
            
            # Set up session mock with different responses for different endpoints
            mock_session = MagicMock()
            mock_session.get.side_effect = lambda url: mock_aws_response if 'debug/about' in url else mock_user_response
            mock_session_class.return_value = mock_session
            
            # Create client
            client = PipebioClient(url='https://test-api.pipebio.com')
            
            # Mock the jobs component
            with patch.object(client.jobs, 'create_signed_upload') as mock_create_upload, \
                 patch.object(client.jobs, 'upload_data_to_signed_url') as mock_upload:
                
                mock_create_upload.return_value = {
                    "data": {
                        "url": "https://test-upload-url.com",
                        "headers": {"test": "header"},
                        "job": {"id": "test-job-id"}
                    }
                }
                
                result = client.upload_file(
                    file_name="test.txt",
                    absolute_file_location="test.txt",
                    parent_id=123,
                    project_id="test-project"
                )
                
                assert result["id"] == "test-job-id"
                assert mock_create_upload.call_count == 1
                assert mock_upload.call_count == 1

    def test_client_initialization_with_api_key(self):
        """Test client initialization with PIPE_API_KEY environment variable."""
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "org": {"id": "test-org-id"},
            "id": "user-123"
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPE_API_KEY': 'test-api-key'}, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')

            # Verify user was set
            assert client.user is not None
            assert client.user["firstName"] == "Test"
            assert client.user["id"] == "user-123"

            # Verify authorization header was set
            mock_session.headers.update.assert_called()
            auth_header_call = [call for call in mock_session.headers.update.call_args_list
                               if 'Authorization' in call[0][0]][0]
            assert auth_header_call[0][0]['Authorization'] == 'Bearer test-api-key'

            # Verify user-dependent services were initialized with user
            assert client.jobs._user is not None
            assert client.organization_lists._user is not None
            assert client.workflows._user is not None

    def test_client_initialization_with_manual_auth(self):
        """Test client initialization with PIPEBIO_MANUAL_AUTH=true."""
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')

            assert client.user is None

            # Verify no authorization header was set
            auth_calls = [call for call in mock_session.headers.update.call_args_list
                         if call[0] and 'Authorization' in call[0][0]]
            assert len(auth_calls) == 0

            # Verify user-dependent services were initialized with None
            assert client.jobs._user is None
            assert client.organization_lists._user is None
            assert client.workflows._user is None

    def test_client_set_s2s_token(self):
        """Test setting S2S token after manual auth initialization."""
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "S2S",
            "lastName": "User",
            "org": {"id": "s2s-org-id"},
            "id": "s2s-user-123"
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')
            assert client.user is None

            client.internal_tools.set_s2s_token('test-s2s-token')

            # Verify user was set
            assert client.user is not None
            assert client.user["firstName"] == "S2S"
            assert client.user["id"] == "s2s-user-123"

            # Verify authorization header was updated
            auth_update_call = [call for call in mock_session.headers.update.call_args_list
                               if call[0] and 'Authorization' in call[0][0]][-1]
            assert auth_update_call[0][0]['Authorization'] == 'Bearer test-s2s-token'

            # Verify user-dependent services were re-initialized with user
            assert client.jobs._user is not None
            assert client.jobs._user["id"] == "s2s-user-123"
            assert client.organization_lists._user is not None
            assert client.organization_lists._user["id"] == "s2s-user-123"
            assert client.workflows._user is not None
            assert client.workflows._user["id"] == "s2s-user-123"

    def test_client_requires_auth_without_manual_flag(self):
        """Test that client raises exception when no auth is provided and PIPEBIO_MANUAL_AUTH is not set."""
        with patch('requests_toolbelt.sessions.BaseUrlSession'), \
             patch.dict('os.environ', {}, clear=True):

            with pytest.raises(Exception, match='PIPE_API_KEY required'):
                PipebioClient(url='https://test-api.pipebio.com')

    def test_client_token_priority_order(self):
        """Test that tokens are used in correct priority order: USER_TOKEN > BENCHLING_S2S_TOKEN > PIPE_API_KEY."""
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "Test",
            "lastName": "User",
            "org": {"id": "test-org-id"}
        }

        # Test USER_TOKEN takes precedence
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {
                 'USER_TOKEN': 'user-token',
                 'BENCHLING_S2S_TOKEN': 's2s-token',
                 'PIPE_API_KEY': 'api-key'
             }, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session_class.return_value = mock_session

            PipebioClient(url='https://test-api.pipebio.com')

            auth_call = [call for call in mock_session.headers.update.call_args_list
                        if call[0] and 'Authorization' in call[0][0]][0]
            assert auth_call[0][0]['Authorization'] == 'Bearer user-token'

        # Test BENCHLING_S2S_TOKEN takes precedence over PIPE_API_KEY
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {
                 'BENCHLING_S2S_TOKEN': 's2s-token',
                 'PIPE_API_KEY': 'api-key'
             }, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session_class.return_value = mock_session

            PipebioClient(url='https://test-api.pipebio.com')

            auth_call = [call for call in mock_session.headers.update.call_args_list
                        if call[0] and 'Authorization' in call[0][0]][0]
            assert auth_call[0][0]['Authorization'] == 'Bearer s2s-token'

        # Test PIPE_API_KEY is used when others aren't present
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
            patch.dict('os.environ', {'PIPE_API_KEY': 'api-key'}, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session_class.return_value = mock_session

            PipebioClient(url='https://test-api.pipebio.com')

            auth_call = [call for call in mock_session.headers.update.call_args_list
                        if call[0] and 'Authorization' in call[0][0]][0]
            assert auth_call[0][0]['Authorization'] == 'Bearer api-key'

    def test_methods_fail_before_s2s_auth(self):
        """Test that methods requiring user context fail gracefully before S2S authentication."""
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')

            assert client.user is None

            # Jobs.create should fail because it needs organization_id from user
            with pytest.raises(TypeError, match="'NoneType' object"):
                client.jobs.create(
                    shareable_id='test-shareable',
                    job_type=JobType.ExportJob,
                    name='test-job',
                    input_entity_ids=['entity-1']
                )

            # OrganizationLists.get_germlines should fail
            with pytest.raises(TypeError, match="'NoneType' object"):
                client.organization_lists.get_germlines()

    def test_methods_work_after_s2s_auth(self):
        """Test that methods requiring user context work after S2S authentication."""
        mock_user_response = MagicMock()
        mock_user_response.status_code = 200
        mock_user_response.json.return_value = {
            "firstName": "S2S",
            "lastName": "User",
            "org": {"id": "org-123"},
            "id": "user-123"
        }

        mock_create_response = MagicMock()
        mock_create_response.status_code = 200
        mock_create_response.json.return_value = {
            "id": "job-123",
            "status": "pending"
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session.get.return_value = mock_user_response
            mock_session.post.return_value = mock_create_response
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')
            client.internal_tools.set_s2s_token('test-s2s-token')

            # Now jobs.create should work because user is set
            job_id = client.jobs.create(
                shareable_id='test-shareable',
                job_type=JobType.ExportJob,
                name='test-job',
                input_entity_ids=['entity-1']
            )

            assert job_id == "job-123"
            # Verify the organization_id was extracted from user
            create_call = mock_session.post.call_args
            assert 'ownerId' in create_call[1]['json']
            assert create_call[1]['json']['ownerId'] == 'org-123'

    def test_methods_work_with_explicit_org_id(self):
        """Test that methods work with explicit organization_id even when user is None."""
        mock_create_response = MagicMock()
        mock_create_response.status_code = 200
        mock_create_response.json.return_value = {
            "id": "job-123",
            "status": "pending"
        }

        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session.post.return_value = mock_create_response
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')

            assert client.user is None

            # Jobs.create should work when organization_id is provided explicitly
            job_id = client.jobs.create(
                shareable_id='test-shareable',
                job_type=JobType.ExportJob,
                name='test-job',
                input_entity_ids=['entity-1'],
                owner_id='explicit-org-123'  # Explicitly provided
            )

            assert job_id == "job-123"
            # Verify the explicit organization_id was used
            create_call = mock_session.post.call_args
            assert create_call[1]['json']['ownerId'] == 'explicit-org-123'


class TestCorrelationId:

    def test_set_correlation_id_adds_header(self):
        """Test that set_correlation_id sets X-Correlation-Id on all subsequent requests."""
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):

            mock_session = MagicMock()
            mock_session.headers = {}
            mock_session_class.return_value = mock_session

            client = PipebioClient(url='https://test-api.pipebio.com')
            client.set_correlation_id('my-operation-123')

            assert mock_session.headers["X-Correlation-Id"] == "my-operation-123"
