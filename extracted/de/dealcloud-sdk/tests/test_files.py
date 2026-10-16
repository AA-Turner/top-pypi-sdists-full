"""Tests for DealCloudFiles class and file module (LocalStorage, ExportResult)."""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dealcloud_sdk.constants import field_types
from dealcloud_sdk.files.dealcloud_files import (
    DealCloudFiles,
    ExportResult,
    LocalStorage,
)


class TestDealCloudFilesInit:
    """Tests for DealCloudFiles initialization."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_files_url(self, mock_client_class):
        """Test that init sets files URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._files_url == "https://test.dealcloud.com/api/rest/v4/data/entryfiles"


class TestDealCloudFilesDownloadFile:
    """Tests for download_file method."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_file_returns_bytes(self, mock_client_class):
        """Test download_file returns bytes when no output_path (uses client.download_file)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def write_to_buffer(url, destination, **kwargs):
            destination.write(b"file content")

        mock_client.download_file.side_effect = write_to_buffer
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = files.download_file(123, "Logo")

        assert result == b"file content"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_file_saves_to_path(self, mock_client_class, tmp_path):
        """Test download_file saves to output_path (client.download_file writes to path)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def write_to_path(url, destination, **kwargs):
            __import__("pathlib").Path(destination).write_bytes(b"saved content")

        mock_client.download_file.side_effect = write_to_path
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        output_path = tmp_path / "downloaded.png"
        result = files.download_file(123, "Logo", output_path=str(output_path))

        assert result == str(output_path)
        assert output_path.exists()
        assert output_path.read_bytes() == b"saved content"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_file_creates_parent_dirs(self, mock_client_class, tmp_path):
        """Test download_file creates parent directories (client.download_file)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}

        def write_to_path(url, destination, **kwargs):
            p = __import__("pathlib").Path(destination)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"content")

        mock_client.download_file.side_effect = write_to_path
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        output_path = tmp_path / "subdir" / "nested" / "file.png"
        files.download_file(123, "Logo", output_path=str(output_path))

        assert output_path.exists()


class TestDealCloudFilesDownloadAttachmentMetadata:
    """Tests for download_attachment_metadata method (uses rows/query by entryId)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_attachment_metadata(self, mock_client_class):
        """Test download_attachment_metadata returns metadata from rows/query response."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "rows": [
                {
                    "Logo": {
                        "fileName": "logo.png",
                        "fileSize": 1024,
                        "contentType": "image/png",
                        "uploadDate": "2024-01-15T10:30:00Z",
                    }
                }
            ]
        }
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = files.download_attachment_metadata("Company", 123, "Logo")

        assert result["fileName"] == "logo.png"
        assert result["fileSize"] == 1024
        assert result["contentType"] == "image/png"
        # POST was called with query endpoint and body with entryId query
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "/rows/query/Company" in call_args[0][0] or "Company" in str(call_args)
        body = call_args[1]["json"]
        assert "query" in body and "123" in body["query"]
        assert body.get("limit") == 1
        assert body.get("wrapIntoArrays") is True


class TestDealCloudFilesDeleteFile:
    """Tests for delete_file method."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_file_success(self, mock_client_class):
        """Test delete_file returns True on success."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = files.delete_file(123, "Logo")

        assert result is True
        mock_client.delete.assert_called_once()


class TestDealCloudFilesGetContentType:
    """Tests for _get_content_type helper."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_pdf(self, mock_client_class):
        """Test PDF content type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._get_content_type(".pdf") == "application/pdf"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_xlsx(self, mock_client_class):
        """Test Excel content type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._get_content_type(".xlsx") == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_png(self, mock_client_class):
        """Test PNG content type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._get_content_type(".png") == "image/png"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_unknown(self, mock_client_class):
        """Test unknown extension returns octet-stream."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._get_content_type(".xyz") == "application/octet-stream"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_case_insensitive(self, mock_client_class):
        """Test content type lookup is case insensitive."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert files._get_content_type(".PDF") == "application/pdf"
        assert files._get_content_type(".PNG") == "image/png"


class TestLocalStorage:
    """Tests for LocalStorage backend."""

    def test_write_creates_file_and_parent_dirs(self, tmp_path):
        storage = LocalStorage(tmp_path)
        path = storage.write("subdir/nested/file.png", b"image content", "image/png")
        assert path == str(tmp_path / "subdir" / "nested" / "file.png")
        assert (tmp_path / "subdir" / "nested" / "file.png").read_bytes() == b"image content"

    def test_exists_true_after_write(self, tmp_path):
        storage = LocalStorage(tmp_path)
        storage.write("test.txt", b"hello", "text/plain")
        assert storage.exists("test.txt") is True

    def test_exists_false_for_missing(self, tmp_path):
        storage = LocalStorage(tmp_path)
        assert storage.exists("nonexistent.txt") is False

    def test_open_write_streams_bytes(self, tmp_path):
        storage = LocalStorage(tmp_path)
        with storage.open_write("streamed.bin", content_type="application/octet-stream") as buf:
            buf.write(b"abc")
        assert (tmp_path / "streamed.bin").read_bytes() == b"abc"
        assert storage.exists("streamed.bin") is True


class TestExportResult:
    """Tests for ExportResult dataclass."""

    def test_success_rate_zero_total(self):
        r = ExportResult(total_files=0)
        assert r.success_rate == 100.0

    def test_success_rate_partial(self):
        r = ExportResult(total_files=10, exported=8, failed=2)
        assert r.success_rate == 80.0

    def test_has_errors_true(self):
        r = ExportResult(errors=[{"file": "a", "error": "fail"}])
        assert r.has_errors is True

    def test_has_errors_false(self):
        r = ExportResult(errors=[])
        assert r.has_errors is False


class TestDealCloudFilesGetContentTypePublic:
    """Tests for public get_content_type and get_extension."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_with_dot(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        assert files.get_content_type(".pdf") == "application/pdf"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_content_type_without_dot(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        assert files.get_content_type("xlsx") == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_extension(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(site_url="test.dealcloud.com", client_id="x", client_secret="y")
        assert files.get_extension("application/pdf") == ".pdf"
        assert files.get_extension("image/jpeg") == ".jpg"
        assert files.get_extension("unknown/type") == ""


class TestDealCloudFilesFilesUrl:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_files_url_property(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert files.files_url.endswith("/entryfiles")


class TestDealCloudFilesAliases:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_download_attachment_delegates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "download_file", return_value=b"x") as m:
            out = files.download_attachment(1, "Logo")
        assert out == b"x"
        m.assert_called_once_with(entry_id=1, field_id="Logo", output_path=None, progress_callback=None)

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_delete_attachment_delegates(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "delete_file", return_value=True) as m:
            assert files.delete_attachment(9, "Doc") is True
        m.assert_called_once_with(entry_id=9, field_id="Doc")


class TestDownloadAttachmentMetadataBranches:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_empty_rows_returns_empty_dict(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"rows": []}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert files.download_attachment_metadata("Company", 1, "Logo") == {}

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_snake_case_metadata_normalized(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "rows": [
                {
                    "Logo": {
                        "file_name": "x.png",
                        "file_size": 10,
                        "content_type": "image/png",
                        "upload_date": "2020-01-01",
                    }
                }
            ]
        }
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        meta = files.download_attachment_metadata("Company", 1, "Logo")
        assert meta["fileName"] == "x.png"
        assert meta["fileSize"] == 10
        assert meta["contentType"] == "image/png"
        assert meta["uploadDate"] == "2020-01-01"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_non_dict_field_returns_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"rows": [{"Logo": "not-a-dict"}]}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert files.download_attachment_metadata("Company", 1, "Logo") == {}


class TestUploadAttachment:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_success(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b'[{"rowId": 42}]'
        mock_resp.json.return_value = [{"rowId": 42}]
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client

        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)

        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            result = files.upload_attachment(
                "Attachment",
                b"hello",
                "note.pdf",
            )
        assert result["entry_id"] == 42
        assert result["document_field_id"] == 2
        mock_client.post_raw.assert_called_once()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_requires_title_and_document_fields(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[]):
            with pytest.raises(ValueError, match="Title and Document"):
                files.upload_attachment("Attachment", b"x", "f.pdf")

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_requires_field_ids(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=None, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            with pytest.raises(ValueError, match="must have id"):
                files.upload_attachment("Attachment", b"x", "f.pdf")

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_non_list_json_returns_response_payload(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b'{"error":"x"}'
        mock_resp.json.return_value = {"error": "x"}
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            result = files.upload_attachment("Attachment", b"x", "f.txt")
        assert result["entry_id"] is None
        assert result["document_field_id"] == 2
        assert result["response"] == {"error": "x"}

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_list_without_row_id(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[{}]"
        mock_resp.json.return_value = [{}]
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            result = files.upload_attachment("Attachment", b"x", "f.txt")
        assert result["entry_id"] is None
        assert result["document_field_id"] == 2

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_uses_explicit_content_type(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            files.upload_attachment(
                "Attachment",
                b"x",
                "report.pdf",
                content_type="application/octet-stream",
            )
        model = json.loads(mock_client.post_raw.call_args[1]["data"]["model"])
        assert model["binaryStoreRequests"][0]["contentType"] == "application/octet-stream"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_infers_content_type_from_extension(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            files.upload_attachment("Attachment", b"x", "report.pdf")
        call_kw = mock_client.post_raw.call_args[1]
        model = json.loads(call_kw["data"]["model"])
        binary = model["binaryStoreRequests"][0]
        assert binary["contentType"] == "application/pdf"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_targets_existing_row(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.put_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        logo = SimpleNamespace(apiName="Logo", id=77, fieldType=field_types.IMAGE)
        name_f = SimpleNamespace(apiName="Name", id=1, fieldType=1)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[name_f, logo]):
            result = files.upload_file_to_entry_field(
                "Company",
                555,
                "Logo",
                b"bytes",
                "shot.png",
                content_type="image/jpeg",
            )
        assert result["entry_id"] == 555
        assert result["field_id"] == 77
        call_kw = mock_client.put_raw.call_args[1]
        model = json.loads(call_kw["data"]["model"])
        bsr = model["binaryStoreRequests"][0]
        assert bsr["entryId"] == 555
        assert bsr["fieldId"] == 77
        assert bsr["contentType"] == "image/jpeg"
        mock_client.post_raw.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_raises_on_row_error_in_200_body(self, mock_client_class):
        from dealcloud_sdk.utils.process_response_errors import DealCloudValidationError

        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        body = [{"entryId": 555, "fieldId": 77, "error": {"code": 5002, "description": "bad"}}]
        mock_resp = MagicMock()
        mock_resp.content = b"x"
        mock_resp.json.return_value = body
        mock_client.put_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        logo = SimpleNamespace(apiName="Logo", id=77, fieldType=field_types.IMAGE)
        files = DealCloudFiles(site_url="test.dealcloud.com", client_id="123", client_secret="secret")
        with patch.object(files, "get_fields", return_value=[logo]):
            with pytest.raises(DealCloudValidationError) as exc:
                files.upload_file_to_entry_field("Company", 555, "Logo", b"b", "a.png")
        assert exc.value.row_errors[0]["EntryId"] == 555

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_by_numeric_field_id(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.put_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        logo = SimpleNamespace(apiName="Logo", id=77, fieldType=field_types.IMAGE)
        name_f = SimpleNamespace(apiName="Name", id=1, fieldType=1)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[name_f, logo]):
            result = files.upload_file_to_entry_field(
                "Company",
                555,
                77,
                b"bytes",
                "shot.png",
            )
        assert result["field_id"] == 77
        call_kw = mock_client.put_raw.call_args[1]
        model = json.loads(call_kw["data"]["model"])
        assert model["binaryStoreRequests"][0]["fieldId"] == 77

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_unknown_numeric_id_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[]):
            with pytest.raises(ValueError, match="No field id 999"):
                files.upload_file_to_entry_field(
                    "Company", 1, 999, b"x", "n.png"
                )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_infers_content_type_when_empty_string(
        self, mock_client_class
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.put_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        logo = SimpleNamespace(apiName="Logo", id=77, fieldType=field_types.IMAGE)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[logo]):
            files.upload_file_to_entry_field(
                "Company", 1, "Logo", b"x", "doc.pdf", content_type=""
            )
        model = json.loads(mock_client.put_raw.call_args[1]["data"]["model"])
        assert model["binaryStoreRequests"][0]["contentType"] == "application/pdf"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_attachment_custom_title(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = []
        mock_client.post_raw.return_value = mock_resp
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[title_f, doc_f]):
            files.upload_attachment(
                "Attachment",
                b"x",
                "f.pdf",
                title="Custom Title",
            )
        model = json.loads(mock_client.post_raw.call_args[1]["data"]["model"])
        assert model["storeRequests"][0]["value"] == "Custom Title"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_string_field_without_id_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        logo = SimpleNamespace(apiName="Logo", id=None, fieldType=field_types.IMAGE)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[logo]):
            with pytest.raises(ValueError, match="No field 'Logo' on object"):
                files.upload_file_to_entry_field(
                    "Company", 1, "Logo", b"x", "n.png"
                )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_unknown_string_name_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[]):
            with pytest.raises(ValueError, match=r"No field 'Missing' on object"):
                files.upload_file_to_entry_field(
                    "Company", 1, "Missing", b"x", "n.png"
                )

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_rejects_non_file_field(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        txt = SimpleNamespace(apiName="Note", id=3, fieldType=field_types.TEXT)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with patch.object(files, "get_fields", return_value=[txt]):
            with pytest.raises(ValueError, match="IMAGE or BINARY"):
                files.upload_file_to_entry_field(
                    "Company", 1, "Note", b"x", "n.txt"
                )

    def _attachment_ref_files(self, mock_client_class, cv_field, post_body):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_resp = MagicMock()
        mock_resp.content = b"[]"
        mock_resp.json.return_value = post_body
        mock_client.post_raw.return_value = mock_resp
        mock_client.put.return_value = [{"rowId": 9}]
        mock_client_class.return_value = mock_client
        title_f = SimpleNamespace(apiName="Title", id=1, fieldType=1)
        doc_f = SimpleNamespace(apiName="Document", id=2, fieldType=field_types.BINARY)
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        return mock_client, files, [cv_field, title_f, doc_f]

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_attachment_reference_two_step(self, mock_client_class):
        cv = SimpleNamespace(
            apiName="CV", name="CV", id=55, fieldType=field_types.REFERENCE, isAttachment=True
        )
        mock_client, files, fields = self._attachment_ref_files(
            mock_client_class, cv, [{"rowId": 9}]
        )
        with patch.object(files, "get_fields", return_value=fields), patch.object(
            files, "get_attachment_object_id", return_value="Attachment"
        ):
            result = files.upload_file_to_entry_field("Contact", 555, "CV", b"pdf", "cv.pdf")
        mock_client.put_raw.assert_not_called()
        assert mock_client.post_raw.call_count == 1
        assert mock_client.post_raw.call_args[0][0].endswith("/Attachment")
        put_args, put_kw = mock_client.put.call_args
        assert put_args[0].endswith("/Contact")
        assert put_kw["json"] == {
            "storeRequests": [{"entryId": 555, "fieldId": 55, "value": 9}]
        }
        assert result["field_id"] == 55
        assert result["attachment_entry_id"] == 9
        assert result["attachment_document_field_id"] == 2

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_resolves_display_name(self, mock_client_class):
        cv = SimpleNamespace(
            apiName="CurriculumVitae",
            name="CV",
            id=55,
            fieldType=field_types.REFERENCE,
            isAttachment=True,
        )
        mock_client, files, fields = self._attachment_ref_files(
            mock_client_class, cv, [{"rowId": 9}]
        )
        with patch.object(files, "get_fields", return_value=fields), patch.object(
            files, "get_attachment_object_id", return_value="Attachment"
        ):
            result = files.upload_file_to_entry_field("Contact", 555, "CV", b"pdf", "cv.pdf")
        assert result["field_id"] == 55

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_reference_not_attachment_raises(self, mock_client_class):
        ref = SimpleNamespace(
            apiName="Company", name="Company", id=55, fieldType=field_types.REFERENCE,
            isAttachment=False,
        )
        mock_client, files, fields = self._attachment_ref_files(mock_client_class, ref, [])
        with patch.object(files, "get_fields", return_value=fields):
            with pytest.raises(ValueError, match="attachment REFERENCE"):
                files.upload_file_to_entry_field("Contact", 1, "Company", b"x", "n.pdf")
        mock_client.post_raw.assert_not_called()
        mock_client.put.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_upload_file_to_entry_field_attachment_reference_no_row_id_raises(
        self, mock_client_class
    ):
        cv = SimpleNamespace(
            apiName="CV", name="CV", id=55, fieldType=field_types.REFERENCE, isAttachment=True
        )
        mock_client, files, fields = self._attachment_ref_files(mock_client_class, cv, [{}])
        with patch.object(files, "get_fields", return_value=fields), patch.object(
            files, "get_attachment_object_id", return_value="Attachment"
        ):
            with pytest.raises(ValueError, match="no row id"):
                files.upload_file_to_entry_field("Contact", 1, "CV", b"x", "cv.pdf")
        mock_client.put.assert_not_called()


class TestFindFileFields:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_single_object_image(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        co = SimpleNamespace(apiName="Company", id=10)
        pic = SimpleNamespace(apiName="Logo", fieldType=field_types.IMAGE, id=20)
        with (
            patch.object(files, "get_objects", return_value=[co]),
            patch.object(files, "get_fields", return_value=[pic]),
        ):
            found = files.find_file_fields("Company", field_type="image")
        assert len(found) == 1
        assert found[0]["object_name"] == "Company"
        assert found[0]["field"] is pic

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_all_merges_image_and_binary(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        co = SimpleNamespace(apiName="Company", id=10)
        img = SimpleNamespace(apiName="Logo", fieldType=field_types.IMAGE, id=1)
        doc = SimpleNamespace(apiName="Doc", fieldType=field_types.BINARY, id=2)
        with (
            patch.object(files, "get_objects", return_value=[co]),
            patch.object(files, "get_fields", return_value=[img, doc]),
        ):
            found = files.find_file_fields("Company", field_type="all")
        assert len(found) == 2

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_all_objects_no_matching_field_type(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        o1 = SimpleNamespace(apiName="NoteObj", id=5)
        txt = SimpleNamespace(apiName="Body", fieldType=field_types.TEXT, id=1)
        with (
            patch.object(files, "get_objects", return_value=[o1]),
            patch.object(files, "get_fields", return_value=[txt]),
        ):
            assert files._find_file_fields(None, field_types.IMAGE) == []

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_attachment_fields_all_objects_no_attachment_refs(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        o1 = SimpleNamespace(apiName="Co", id=1)
        ref = SimpleNamespace(
            apiName="Parent",
            fieldType=field_types.REFERENCE,
            id=2,
            isAttachment=False,
        )
        with (
            patch.object(files, "get_objects", return_value=[o1]),
            patch.object(files, "get_fields", return_value=[ref]),
        ):
            assert files._find_attachment_fields(None) == []

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_binary_type(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        co = SimpleNamespace(apiName="Deal", id=10)
        doc = SimpleNamespace(apiName="Contract", fieldType=field_types.BINARY, id=3)
        with (
            patch.object(files, "get_objects", return_value=[co]),
            patch.object(files, "get_fields", return_value=[doc]),
        ):
            found = files.find_file_fields("Deal", field_type="binary")
        assert len(found) == 1
        assert found[0]["field"] is doc

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_invalid_type_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(ValueError, match="field_type"):
            files.find_file_fields(field_type="video")

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_attachment_fields_single_object_no_matches(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        co = SimpleNamespace(apiName="Deal", id=5)
        plain = SimpleNamespace(
            apiName="Parent",
            fieldType=field_types.REFERENCE,
            id=2,
            isAttachment=False,
        )
        with (
            patch.object(files, "get_objects", return_value=[co]),
            patch.object(files, "get_fields", return_value=[plain]),
        ):
            assert files._find_attachment_fields("Deal") == []

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_attachment_fields_reference_with_flag(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        co = SimpleNamespace(apiName="Deal", id=5)
        att = SimpleNamespace(
            apiName="Files",
            fieldType=field_types.REFERENCE,
            id=99,
            isAttachment=True,
        )
        with (
            patch.object(files, "get_objects", return_value=[co]),
            patch.object(files, "get_fields", return_value=[att]),
        ):
            found = files.find_attachment_fields("Deal")
        assert len(found) == 1
        assert found[0]["field"] is att


class TestFilesApiRefactor:
    """Tests for Files API refactoring."""

    def test_files_api_uses_client_methods(self):
        """Verify Files API uses RestClient methods instead of direct access."""
        import inspect

        from dealcloud_sdk.files.dealcloud_files import DealCloudFiles

        source = inspect.getsource(DealCloudFiles)

        # Should NOT contain direct client access patterns
        assert "._client._client" not in source
        assert "_get_auth_headers_sync" not in source

        # Should use proper client methods (download_file for GET-style file retrieval, post/post_raw, delete)
        assert "_client.download_file" in source or "_client.get_raw" in source or "_client.get(" in source
        assert "_client.post_raw" in source or "_client.post(" in source
        assert "_client.put_raw" in source


