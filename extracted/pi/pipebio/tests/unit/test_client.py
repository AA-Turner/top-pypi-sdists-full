import os

import pytest
from unittest.mock import patch, MagicMock
from pipebio.pipebio_client import DOWNLOAD_READ_TIMEOUT_SECONDS, PipebioClient
from pipebio.models.export_format import ExportFormat
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


class TestDownloadExportOutput:
    """Tests for download_export_output, which needs no live credentials."""

    @staticmethod
    def _client():
        with patch('requests_toolbelt.sessions.BaseUrlSession') as mock_session_class, \
             patch.dict('os.environ', {'PIPEBIO_MANUAL_AUTH': 'true'}, clear=True):
            mock_session_class.return_value = MagicMock()
            return PipebioClient(url='https://test-api.pipebio.com')

    @staticmethod
    def _mock_urlopen(bodies, read_sizes=None):
        """Build a urlopen mock returning each body in turn, as a context manager.

        read() is a real implementation over the body rather than a fixed
        side_effect list, so the recorded sizes reflect how the client actually
        consumes the response. Pass read_sizes to capture every requested size
        (None meaning "read the whole body").
        """
        def _open(url, timeout=None):
            body = bodies.pop(0)
            position = 0

            def _read(size=None):
                nonlocal position
                if read_sizes is not None:
                    read_sizes.append(size)
                end = len(body) if size is None or size < 0 else position + size
                chunk = body[position:end]
                position += len(chunk)
                return chunk

            response = MagicMock()
            response.headers.get.return_value = str(len(body))
            response.read.side_effect = _read
            response.__enter__.return_value = response
            response.__exit__.return_value = False
            return response
        return _open

    def test_download_is_streamed_in_bounded_chunks(self, tmp_path):
        """The headline fix: the body must never be read into memory at once.

        Asserted directly, because a mock whose read() ignores its size argument
        is satisfied by file.write(response.read()) just as happily as by a
        chunked loop.
        """
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}
        body = b'x' * (1024 * 1024 * 2 + 17)
        read_sizes = []

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([body], read_sizes=read_sizes)):
            client.download_export_output(
                'job-1',
                destination_folder=str(tmp_path),
                destination_filename='export.tsv',
            )

        assert (tmp_path / 'export.tsv').read_bytes() == body
        # Every read is capped at the 1MiB copy buffer: no unparameterised read,
        # and nothing large enough to hold the whole body.
        assert read_sizes, 'read() was never called'
        assert set(read_sizes) == {1024 * 1024}
        assert len(read_sizes) > 1

    def test_multiple_links_write_distinct_files(self, tmp_path):
        """Regression: N output links used to overwrite a single destination."""
        client = self._client()
        job = {
            "status": "COMPLETE",
            "outputLinks": [{"url": "https://one"}, {"url": "https://two"}],
        }

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'first', b'second'])):
            outputs = client.download_export_output(
                'job-1',
                destination_folder=str(tmp_path),
                destination_filename='export.tsv',
            )

        assert outputs == [
            str(tmp_path / 'export_1.tsv'),
            str(tmp_path / 'export_2.tsv'),
        ]
        assert (tmp_path / 'export_1.tsv').read_bytes() == b'first'
        assert (tmp_path / 'export_2.tsv').read_bytes() == b'second'

    def test_single_link_keeps_filename_unindexed(self, tmp_path):
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'only'])):
            outputs = client.download_export_output(
                'job-1',
                destination_folder=str(tmp_path),
                destination_filename='export.tsv',
            )

        assert outputs == [str(tmp_path / 'export.tsv')]
        assert (tmp_path / 'export.tsv').read_bytes() == b'only'

    def test_compound_extension_is_preserved(self, tmp_path):
        client = self._client()
        job = {
            "status": "COMPLETE",
            "outputLinks": [{"url": "https://one"}, {"url": "https://two"}],
        }

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'a', b'b'])):
            outputs = client.download_export_output(
                'job-1',
                destination_folder=str(tmp_path),
                destination_filename='export.tsv.gz',
            )

        assert [os.path.basename(path) for path in outputs] == [
            'export_1.tsv.gz',
            'export_2.tsv.gz',
        ]

    def test_filename_defaults_to_job_file_name(self, tmp_path):
        client = self._client()
        job = {
            "status": "COMPLETE",
            "params": {"fileName": "from-job.tsv"},
            "outputLinks": [{"url": "https://one"}],
        }

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'x'])):
            outputs = client.download_export_output(
                'job-1', destination_folder=str(tmp_path)
            )

        assert outputs == [str(tmp_path / 'from-job.tsv')]

    def test_failed_job_raises(self, tmp_path):
        client = self._client()
        job = {"status": "FAILED", "messages": ["out of memory"], "outputLinks": []}

        with patch.object(client.jobs, 'poll_job', return_value=job):
            with pytest.raises(Exception, match="did not complete"):
                client.download_export_output(
                    'job-1',
                    destination_folder=str(tmp_path),
                    destination_filename='export.tsv',
                )

    def test_no_output_links_raises(self, tmp_path):
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": []}

        with patch.object(client.jobs, 'poll_job', return_value=job):
            with pytest.raises(Exception, match="no output links"):
                client.download_export_output(
                    'job-1',
                    destination_folder=str(tmp_path),
                    destination_filename='export.tsv',
                )

    def test_interrupted_download_leaves_no_file(self, tmp_path):
        """A mid-stream failure must not leave a partial file at the final path."""
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}

        def _open(url, timeout=None):
            response = MagicMock()
            response.headers.get.return_value = '100'
            response.read.side_effect = [b'partial', IOError('connection reset')]
            response.__enter__.return_value = response
            response.__exit__.return_value = False
            return response

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen', side_effect=_open):
            with pytest.raises(IOError):
                client.download_export_output(
                    'job-1',
                    destination_folder=str(tmp_path),
                    destination_filename='export.tsv',
                )

        assert list(tmp_path.iterdir()) == []

    def test_short_download_raises_and_cleans_up(self, tmp_path):
        """Content-Length mismatch must not be reported as a complete export."""
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}

        def _open(url, timeout=None):
            response = MagicMock()
            response.headers.get.return_value = '999'
            response.read.side_effect = [b'short', b'']
            response.__enter__.return_value = response
            response.__exit__.return_value = False
            return response

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen', side_effect=_open):
            with pytest.raises(Exception, match="Incomplete download"):
                client.download_export_output(
                    'job-1',
                    destination_folder=str(tmp_path),
                    destination_filename='export.tsv',
                )

        assert list(tmp_path.iterdir()) == []

    def test_download_passes_a_read_timeout(self, tmp_path):
        """Without a timeout, a stalled connection hangs the caller forever."""
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}
        opener = MagicMock(side_effect=self._mock_urlopen([b'x']))

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen', opener):
            client.download_export_output(
                'job-1',
                destination_folder=str(tmp_path),
                destination_filename='export.tsv',
            )

        assert opener.call_args.kwargs['timeout'] == DOWNLOAD_READ_TIMEOUT_SECONDS

    def test_destination_folder_defaults_to_cwd(self, tmp_path, monkeypatch):
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}
        monkeypatch.chdir(tmp_path)

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'x'])):
            outputs = client.download_export_output(
                'job-1', destination_filename='export.tsv'
            )

        assert outputs == [os.path.join(os.getcwd(), 'export.tsv')]
        assert (tmp_path / 'export.tsv').read_bytes() == b'x'

    def test_missing_destination_folder_is_created(self, tmp_path):
        client = self._client()
        job = {"status": "COMPLETE", "outputLinks": [{"url": "https://one"}]}
        nested = tmp_path / 'does' / 'not' / 'exist'

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen',
                   side_effect=self._mock_urlopen([b'x'])):
            outputs = client.download_export_output(
                'job-1',
                destination_folder=str(nested),
                destination_filename='export.tsv',
            )

        assert outputs == [str(nested / 'export.tsv')]

    def test_partial_multi_link_failure_names_completed_files(self, tmp_path):
        """The caller gets no return value, so the error must name what is on disk."""
        client = self._client()
        job = {
            "status": "COMPLETE",
            "outputLinks": [{"url": "https://one"}, {"url": "https://two"}],
        }

        def _open(url, timeout=None):
            response = MagicMock()
            response.__enter__.return_value = response
            response.__exit__.return_value = False
            if url == "https://two":
                response.headers.get.return_value = '100'
                response.read.side_effect = IOError('connection reset')
            else:
                response.headers.get.return_value = '5'
                response.read.side_effect = [b'first', b'']
            return response

        with patch.object(client.jobs, 'poll_job', return_value=job), \
             patch('pipebio.pipebio_client.urlopen', side_effect=_open):
            with pytest.raises(Exception, match="already downloaded"):
                client.download_export_output(
                    'job-1',
                    destination_folder=str(tmp_path),
                    destination_filename='export.tsv',
                )

        # The first file persists; only the failed file's .part is cleaned up.
        assert [path.name for path in sorted(tmp_path.iterdir())] == ['export_1.tsv']

    def test_printed_resume_snippet_parses_for_windows_paths(self, capsys):
        """The printed resume line must be copy-pasteable Python.

        A Windows path interpolated into a double-quoted literal is a
        SyntaxError: destination_folder="C:\\Users\\..." is a truncated \\U escape.
        """
        import ast

        client = self._client()
        client.user = {"org": {"id": "org-1"}}
        windows_folder = r"C:\Users\alice\exports"

        with patch.object(client.entities, "get",
                          return_value={"name": "export.tsv", "ownerId": "owner-1"}), \
             patch.object(client.jobs, "create", return_value="job-1"), \
             patch.object(client, "download_export_output", return_value=[]), \
             patch("pipebio.pipebio_client.os.makedirs"):
            client.export(
                entity_id="entity-1",
                format=ExportFormat.CSV,
                destination_folder=windows_folder,
            )

        snippet = [line.strip() for line in capsys.readouterr().out.splitlines()
                   if "download_export_output(" in line][0]

        # Raises SyntaxError if the path was interpolated unescaped.
        parsed = ast.parse(snippet).body[0].value
        keywords = {kw.arg: ast.literal_eval(kw.value) for kw in parsed.keywords}
        assert keywords["destination_folder"] == windows_folder
        assert ast.literal_eval(parsed.args[0]) == "job-1"
