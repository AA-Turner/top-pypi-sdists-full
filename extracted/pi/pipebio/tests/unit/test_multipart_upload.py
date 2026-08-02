import math
from unittest.mock import MagicMock, patch, mock_open

import pytest
import requests

from pipebio.multipart_upload import (
    CHUNK_SIZE,
    MULTIPART_THRESHOLD,
    MAX_RETRIES,
    _is_retryable,
    _post_with_retries,
    upload_multipart_aws,
    _abort_multipart_upload,
    _upload_part_aws,
)


class TestIsRetryable:
    def test_connection_error_is_retryable(self):
        e = requests.exceptions.ConnectionError()
        assert _is_retryable(e) is True

    def test_timeout_is_retryable(self):
        e = requests.exceptions.Timeout()
        assert _is_retryable(e) is True

    def test_5xx_http_error_is_retryable(self):
        response = MagicMock()
        response.status_code = 503
        e = requests.exceptions.HTTPError(response=response)
        assert _is_retryable(e) is True

    def test_429_http_error_is_retryable(self):
        response = MagicMock()
        response.status_code = 429
        e = requests.exceptions.HTTPError(response=response)
        assert _is_retryable(e) is True

    def test_400_http_error_is_not_retryable(self):
        response = MagicMock()
        response.status_code = 400
        e = requests.exceptions.HTTPError(response=response)
        assert _is_retryable(e) is False

    def test_403_http_error_is_not_retryable(self):
        response = MagicMock()
        response.status_code = 403
        e = requests.exceptions.HTTPError(response=response)
        assert _is_retryable(e) is False

    def test_404_http_error_is_not_retryable(self):
        response = MagicMock()
        response.status_code = 404
        e = requests.exceptions.HTTPError(response=response)
        assert _is_retryable(e) is False


class TestPostWithRetries:
    def test_returns_on_first_success(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 200
        session.post.return_value = response

        with patch("pipebio.multipart_upload.Util.raise_detailed_error"):
            result = _post_with_retries(session, "/test", {"key": "value"})

        assert result == response
        assert session.post.call_count == 1

    def test_retries_on_connection_error(self):
        session = MagicMock()
        response = MagicMock()
        response.status_code = 200
        session.post.side_effect = [
            requests.exceptions.ConnectionError(),
            response,
        ]

        with patch("pipebio.multipart_upload.Util.raise_detailed_error"), \
             patch("pipebio.multipart_upload.time.sleep"):
            result = _post_with_retries(session, "/test", {})

        assert result == response
        assert session.post.call_count == 2

    def test_raises_immediately_on_400(self):
        session = MagicMock()
        bad_response = MagicMock()
        bad_response.status_code = 400
        http_error = requests.exceptions.HTTPError(response=bad_response)

        with patch("pipebio.multipart_upload.Util.raise_detailed_error", side_effect=http_error):
            with pytest.raises(requests.exceptions.HTTPError):
                _post_with_retries(session, "/test", {})

        assert session.post.call_count == 1


class TestUploadMultipartAws:
    def test_zero_byte_file_raises(self):
        session = MagicMock()
        with patch("os.path.getsize", return_value=0):
            with pytest.raises(ValueError, match="zero-byte"):
                upload_multipart_aws(
                    session=session,
                    absolute_file_location="/fake/file.fastq",
                    file_name="file.fastq",
                    parent_id="folder-1",
                    project_id="project-1",
                    organization_id="org-1",
                )

    def test_happy_path_assembles_parts_and_completes(self):
        session = MagicMock()
        file_size = CHUNK_SIZE + 100
        file_content = b"x" * file_size

        create_response = MagicMock()
        create_response.status_code = 200
        create_response.json.return_value = {
            "job": {"id": "job-123"},
            "multipartUploadId": "upload-abc",
        }

        complete_response = MagicMock()
        complete_response.status_code = 200
        complete_response.json.return_value = {}

        session.post.side_effect = [
            create_response,
            MagicMock(status_code=200, json=MagicMock(return_value={"url": "https://s3/part1", "headers": {}})),
            MagicMock(status_code=200, json=MagicMock(return_value={"url": "https://s3/part2", "headers": {}})),
            complete_response,
        ]

        put_response = MagicMock()
        put_response.status_code = 200
        put_response.headers = {"ETag": '"abc123"'}
        put_response.raise_for_status = MagicMock()

        with patch("os.path.getsize", return_value=file_size), \
             patch("builtins.open", mock_open(read_data=file_content)), \
             patch("pipebio.multipart_upload.Util.raise_detailed_error"), \
             patch("pipebio.multipart_upload.requests.put", return_value=put_response), \
             patch("pipebio.multipart_upload._print_progress"):
            result = upload_multipart_aws(
                session=session,
                absolute_file_location="/fake/file.fastq",
                file_name="file.fastq",
                parent_id="folder-1",
                project_id="project-1",
                organization_id="org-1",
            )

        assert result == {"id": "job-123"}
        assert session.post.call_count == 4

    def test_abort_called_on_upload_failure(self):
        session = MagicMock()
        file_size = CHUNK_SIZE + 100

        create_response = MagicMock()
        create_response.status_code = 200
        create_response.json.return_value = {
            "job": {"id": "job-123"},
            "multipartUploadId": "upload-abc",
        }

        presigned_response = MagicMock()
        presigned_response.status_code = 200
        presigned_response.json.return_value = {"url": "https://s3/part1", "headers": {}}

        session.post.side_effect = [
            create_response,
            *[presigned_response] * MAX_RETRIES,
        ]

        put_response = MagicMock()
        put_response.status_code = 500
        put_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=MagicMock(status_code=500)
        )

        with patch("os.path.getsize", return_value=file_size), \
             patch("builtins.open", mock_open(read_data=b"x" * file_size)), \
             patch("pipebio.multipart_upload.Util.raise_detailed_error"), \
             patch("pipebio.multipart_upload.requests.put", return_value=put_response), \
             patch("pipebio.multipart_upload._print_progress"), \
             patch("pipebio.multipart_upload.time.sleep"):
            with pytest.raises(Exception, match="Failed to upload part 1"):
                upload_multipart_aws(
                    session=session,
                    absolute_file_location="/fake/file.fastq",
                    file_name="file.fastq",
                    parent_id="folder-1",
                    project_id="project-1",
                    organization_id="org-1",
                )

        session.delete.assert_called_once()
        abort_call = session.delete.call_args
        assert abort_call[0][0] == "multipart-upload/job-123"
        assert abort_call[1]["json"]["uploadId"] == "upload-abc"

    def test_on_progress_callback_invoked(self):
        session = MagicMock()
        file_size = 100
        file_content = b"x" * file_size

        create_response = MagicMock()
        create_response.status_code = 200
        create_response.json.return_value = {
            "job": {"id": "job-123"},
            "multipartUploadId": "upload-abc",
        }

        presigned_response = MagicMock()
        presigned_response.status_code = 200
        presigned_response.json.return_value = {"url": "https://s3/part1", "headers": {}}

        complete_response = MagicMock()
        complete_response.status_code = 200
        complete_response.json.return_value = {}

        session.post.side_effect = [create_response, presigned_response, complete_response]

        put_response = MagicMock()
        put_response.status_code = 200
        put_response.headers = {"ETag": '"etag1"'}
        put_response.raise_for_status = MagicMock()

        progress_calls = []

        with patch("os.path.getsize", return_value=file_size), \
             patch("builtins.open", mock_open(read_data=file_content)), \
             patch("pipebio.multipart_upload.Util.raise_detailed_error"), \
             patch("pipebio.multipart_upload.requests.put", return_value=put_response), \
             patch("pipebio.multipart_upload._print_progress"):
            upload_multipart_aws(
                session=session,
                absolute_file_location="/fake/file.fastq",
                file_name="file.fastq",
                parent_id="folder-1",
                project_id="project-1",
                organization_id="org-1",
                on_progress=lambda uploaded, total: progress_calls.append((uploaded, total)),
            )

        assert len(progress_calls) == 1
        assert progress_calls[0] == (file_size, file_size)


class TestUploadPartAws:
    def test_retries_on_timeout_then_succeeds(self):
        session = MagicMock()
        presigned_response = MagicMock()
        presigned_response.status_code = 200
        presigned_response.json.return_value = {"url": "https://s3/part", "headers": {}}
        session.post.return_value = presigned_response

        put_ok = MagicMock()
        put_ok.status_code = 200
        put_ok.headers = {"ETag": '"etag-abc"'}
        put_ok.raise_for_status = MagicMock()

        with patch("pipebio.multipart_upload.Util.raise_detailed_error"), \
             patch("pipebio.multipart_upload.requests.put") as mock_put, \
             patch("pipebio.multipart_upload.time.sleep"):
            mock_put.side_effect = [requests.exceptions.Timeout(), put_ok]
            result = _upload_part_aws(session, "upload-1", "job-1", 1, b"data")

        assert result == "etag-abc"
        assert mock_put.call_count == 2


class TestAbortMultipartUpload:
    def test_calls_server_delete_endpoint(self):
        session = MagicMock()
        session.delete.return_value = MagicMock(status_code=204)

        _abort_multipart_upload(session, "upload-abc", "job-123")

        session.delete.assert_called_once_with(
            "multipart-upload/job-123",
            json={"uploadId": "upload-abc"},
        )

    def test_gracefully_handles_server_error(self, capsys):
        session = MagicMock()
        session.delete.side_effect = Exception("Server not deployed")

        _abort_multipart_upload(session, "upload-abc", "job-123")

        captured = capsys.readouterr()
        assert "abandoned" in captured.out
        assert "cleaned up automatically" in captured.out
