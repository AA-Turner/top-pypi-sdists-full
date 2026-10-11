"""Unit tests for DealCloudFiles export_* methods (mocked read_data / downloads)."""

import logging
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dealcloud_sdk.constants import field_types
from dealcloud_sdk.files.dealcloud_files import DealCloudFiles, ExportResult, LocalStorage


def _image_field_info():
    fld = SimpleNamespace(apiName="Logo", id=55, fieldType=field_types.IMAGE)
    return {"object_id": 10, "object_name": "Company", "field": fld}


def _binary_field_info():
    fld = SimpleNamespace(apiName="Contract", id=66, fieldType=field_types.BINARY)
    return {"object_id": 20, "object_name": "Deal", "field": fld}


class TestExportImagesValidation:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_requires_output_or_storage(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with pytest.raises(ValueError, match="output_dir or storage"):
            files.export_images()


class TestExportImagesEmpty:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_no_fields_returns_empty_result(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with patch.object(files, "_find_file_fields", return_value=[]):
            r = files.export_images(storage=MagicMock())
        assert r.exported == 0 and r.total_files == 0


class TestExportImagesHappyPath:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_downloads_and_writes(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        storage = LocalStorage(tmp_path)
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 100, "Logo": {"fileName": "x.png"}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "image/png", "fileName": "x.png"},
            ),
            patch.object(files, "download_file", return_value=b"bytes"),
        ):
            r = files.export_images(output_dir=str(tmp_path), object_id="Company")
        assert r.exported == 1
        assert r.total_files == 1
        assert len(r.files) == 1

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_field_ids_filter(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        a = _image_field_info()
        b = {
            "object_id": 10,
            "object_name": "Company",
            "field": SimpleNamespace(apiName="Other", id=99, fieldType=field_types.IMAGE),
        }
        storage = MagicMock()
        storage.exists.return_value = False
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[a, b]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_images(storage=storage, field_ids=["Logo"])
            assert mock_read.called

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_skips_when_exists_and_no_overwrite(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        storage = MagicMock()
        storage.exists.return_value = True
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Logo": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "image/png"},
            ),
            patch.object(files, "download_file") as mock_dl,
        ):
            r = files.export_images(storage=storage, overwrite=False)
        assert r.skipped == 1
        assert r.exported == 0
        mock_dl.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_on_progress_and_inner_failure(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        prog = MagicMock()
        storage = LocalStorage(tmp_path)
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 7, "Logo": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "image/png"},
            ),
            patch.object(files, "download_file", side_effect=OSError("dl fail")),
        ):
            r = files.export_images(
                output_dir=str(tmp_path),
                on_progress=prog,
            )
        assert r.failed == 1
        assert r.errors
        # on_progress is only invoked after a successful write, not on download failure
        prog.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_read_data_outer_failure(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", side_effect=RuntimeError("read fail")),
        ):
            r = files.export_images(output_dir=str(tmp_path))
        assert r.exported == 0

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_query_only_builds_query(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_images(
                output_dir=str(tmp_path),
                object_id="Company",
                query="Active = 1",
            )
        assert mock_read.call_args[1]["query"] == "Active = 1"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_skips_entry_without_file_payload(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": None, "Logo": {"x": 1}}],
            ),
        ):
            r = files.export_images(output_dir=str(tmp_path))
        assert r.total_files == 0

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_entry_ids_only_builds_in_query(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_images(
                output_dir=str(tmp_path),
                object_id="Company",
                entry_ids=[7, 8],
            )
        q = mock_read.call_args[1]["query"].replace(" ", "")
        assert "EntryIdin(7,8)" in q

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_entry_ids_and_query_combine(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_images(
                output_dir=str(tmp_path),
                object_id="Company",
                entry_ids=[1, 2],
                query="Status = 1",
            )
            q = mock_read.call_args[1]["query"]
        compact = q.replace(" ", "")
        assert "EntryIdin(1,2)" in compact
        assert "Status=1" in compact


class TestExportDocuments:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_requires_output_or_storage(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with pytest.raises(ValueError, match="output_dir or storage"):
            files.export_documents()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_no_fields_after_field_ids_filter(self, mock_client_class, caplog, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            caplog.at_level(logging.INFO),
        ):
            files.export_documents(
                output_dir=str(tmp_path),
                field_ids=["NonexistentField"],
            )
        assert any("No binary" in r.message for r in caplog.records)

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_query_only(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_documents(
                output_dir=str(tmp_path),
                object_id="Deal",
                query="Stage = 'Open'",
            )
        assert mock_read.call_args[1]["query"] == "Stage = 'Open'"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_happy_path_uses_file_name_ext(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 5, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={
                    "contentType": "application/pdf",
                    "fileName": "deal.pdf",
                },
            ),
            patch.object(files, "download_file", return_value=b"%PDF"),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.exported == 1

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_entry_ids_only_in_query(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_documents(
                output_dir=str(tmp_path),
                object_id="Deal",
                entry_ids=[3, 4],
            )
        q = mock_read.call_args[1]["query"].replace(" ", "")
        assert "EntryIdin(3,4)" in q

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_entry_ids_and_query_combine(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_documents(
                output_dir=str(tmp_path),
                object_id="Deal",
                entry_ids=[1, 2],
                query="Status = 1",
            )
        q = mock_read.call_args[1]["query"]
        compact = q.replace(" ", "")
        assert "EntryIdin(1,2)" in compact
        assert "Status=1" in compact

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_on_progress_after_success(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        prog = MagicMock()
        storage = LocalStorage(tmp_path)
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 100, "Logo": {"fileName": "x.png"}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "image/png", "fileName": "x.png"},
            ),
            patch.object(files, "download_file", return_value=b"bytes"),
        ):
            r = files.export_images(storage=storage, on_progress=prog)
        assert r.exported == 1
        prog.assert_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_images_non_bytes_download_skips_write(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _image_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Logo": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "image/png"},
            ),
            patch.object(files, "download_file", return_value=None),
        ):
            r = files.export_images(output_dir=str(tmp_path))
        assert r.exported == 0
        assert r.total_files == 1

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_skips_when_exists(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        storage = MagicMock()
        storage.exists.return_value = True
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "application/pdf", "fileName": "a.pdf"},
            ),
            patch.object(files, "download_file") as mock_dl,
        ):
            r = files.export_documents(storage=storage, overwrite=False)
        assert r.skipped == 1
        mock_dl.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_on_progress_after_success(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        prog = MagicMock()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "application/pdf", "fileName": "doc.pdf"},
            ),
            patch.object(files, "download_file", return_value=b"%PDF"),
        ):
            r = files.export_documents(
                output_dir=str(tmp_path),
                on_progress=prog,
            )
        assert r.exported == 1
        prog.assert_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_non_bytes_download_skips_write(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "application/pdf", "fileName": "a.pdf"},
            ),
            patch.object(files, "download_file", return_value="not-bytes"),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.exported == 0
        assert r.total_files == 1

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_empty_file_name_uses_content_type_ext(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                return_value={"contentType": "application/pdf", "fileName": ""},
            ),
            patch.object(files, "download_file", return_value=b"x"),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.exported == 1

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_field_ids_filter(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        a = _binary_field_info()
        b = {
            "object_id": 20,
            "object_name": "Deal",
            "field": SimpleNamespace(apiName="Other", id=99, fieldType=field_types.BINARY),
        }
        mock_read = MagicMock(return_value=[])
        with (
            patch.object(files, "_find_file_fields", return_value=[a, b]),
            patch.object(files, "read_data", mock_read),
        ):
            files.export_documents(
                output_dir=str(tmp_path),
                field_ids=["Contract"],
            )
        assert mock_read.called

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_skips_row_without_binary_payload(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": None}],
            ),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.total_files == 0

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_inner_download_failure_records_error(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(
                files,
                "read_data",
                return_value=[{"EntryId": 1, "Contract": {"x": 1}}],
            ),
            patch.object(
                files,
                "download_attachment_metadata",
                side_effect=OSError("meta fail"),
            ),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.failed == 1
        assert r.errors

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_documents_read_data_outer_failure(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        info = _binary_field_info()
        with (
            patch.object(files, "_find_file_fields", return_value=[info]),
            patch.object(files, "read_data", side_effect=RuntimeError("boom")),
        ):
            r = files.export_documents(output_dir=str(tmp_path))
        assert r.exported == 0


class TestExportFilesCombined:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_files_requires_output_or_storage(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with pytest.raises(ValueError, match="output_dir or storage"):
            files.export_files()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_files_with_explicit_storage_skips_localstorage_ctor(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        storage = MagicMock()
        with (
            patch.object(files, "export_images", return_value=ExportResult()) as m_img,
            patch.object(files, "export_documents", return_value=ExportResult()) as m_doc,
        ):
            files.export_files(storage=storage, include_images=True, include_documents=False)
        m_img.assert_called_once()
        m_doc.assert_not_called()
        assert m_img.call_args[1]["storage"] is storage

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_files_documents_only(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with (
            patch.object(
                files,
                "export_images",
                return_value=ExportResult(),
            ) as m_img,
            patch.object(
                files,
                "export_documents",
                return_value=ExportResult(total_files=1, exported=1),
            ) as m_doc,
        ):
            r = files.export_files(
                output_dir=str(tmp_path),
                include_images=False,
                include_documents=True,
            )
        assert r.exported == 1
        m_img.assert_not_called()
        m_doc.assert_called_once()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_files_calls_images_and_documents(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with (
            patch.object(
                files,
                "export_images",
                return_value=ExportResult(total_files=1, exported=1),
            ) as m_img,
            patch.object(
                files,
                "export_documents",
                return_value=ExportResult(total_files=2, exported=2),
            ) as m_doc,
        ):
            r = files.export_files(output_dir=str(tmp_path))
        assert r.total_files == 3
        assert r.exported == 3
        m_img.assert_called_once()
        m_doc.assert_called_once()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_files_images_only(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with (
            patch.object(files, "export_images", return_value=ExportResult(exported=1)) as m_img,
            patch.object(files, "export_documents") as m_doc,
        ):
            files.export_files(
                output_dir=str(tmp_path),
                include_images=True,
                include_documents=False,
            )
        m_img.assert_called_once()
        m_doc.assert_not_called()

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_attachments_delegates(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with patch.object(files, "export_files", return_value=ExportResult()) as m:
            files.export_attachments(output_dir=str(tmp_path), object_id="X")
        m.assert_called_once()
        assert m.call_args[1]["object_id"] == "X"

    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_entry_files_forwards_to_export_files(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        with patch.object(files, "export_files", return_value=ExportResult()) as m:
            files.export_entry_files("Deal", 999, output_dir=str(tmp_path))
        kw = m.call_args[1]
        assert kw["entry_ids"] == [999]
        assert kw["object_id"] == "Deal"
        assert kw["naming"] == "{field_name}.{ext}"


class TestFindFileFieldsAllObjects:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_file_fields_warns_when_get_fields_fails_for_object(self, mock_client_class, caplog):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        o1 = SimpleNamespace(apiName="A", id=1)
        o2 = SimpleNamespace(apiName="B", id=2)
        img = SimpleNamespace(apiName="Pic", id=9, fieldType=field_types.IMAGE)

        def get_fields_side_effect(oid):
            if oid == 1:
                return [img]
            raise RuntimeError("no schema")

        with (
            patch.object(files, "get_objects", return_value=[o1, o2]),
            patch.object(files, "get_fields", side_effect=get_fields_side_effect),
            caplog.at_level(logging.WARNING),
        ):
            out = files._find_file_fields(None, field_types.IMAGE)
        assert len(out) == 1
        assert any("Could not get fields" in r.message for r in caplog.records)


class TestFindAttachmentFieldsAllObjects:
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_find_attachment_fields_warns_when_get_fields_fails(self, mock_client_class, caplog):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        files = DealCloudFiles(
            site_url="test.dealcloud.com",
            client_id="1",
            client_secret="s",
        )
        o1 = SimpleNamespace(apiName="A", id=1)
        o2 = SimpleNamespace(apiName="B", id=2)
        att = SimpleNamespace(
            apiName="Files",
            id=3,
            fieldType=field_types.REFERENCE,
            isAttachment=True,
        )

        def get_fields_side_effect(oid):
            if oid == 1:
                return [att]
            raise RuntimeError("schema down")

        with (
            patch.object(files, "get_objects", return_value=[o1, o2]),
            patch.object(files, "get_fields", side_effect=get_fields_side_effect),
            caplog.at_level(logging.WARNING),
        ):
            out = files._find_attachment_fields(None)
        assert len(out) == 1
        assert any("Could not get fields" in r.message for r in caplog.records)
