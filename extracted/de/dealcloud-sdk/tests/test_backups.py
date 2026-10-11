"""Tests for DealCloudBackups (four swagger operations only)."""

import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.backups.dealcloud_backups import (
    DealCloudBackups,
    _backup_rows_from_list_response,
)
from dealcloud_sdk.storage import LocalStorage


class TestDealCloudBackupsInit:
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_backups_url(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert backups._backups_url == "https://test.dealcloud.com/api/rest/v4/backups"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_backups_url_property(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        assert backups.backups_url == backups._backups_url


class TestBackupRowsFromListResponse:
    """Unit tests for _backup_rows_from_list_response normalization."""

    def test_none_returns_empty(self):
        assert _backup_rows_from_list_response(None) == []

    def test_bare_list_keeps_only_name_link(self):
        rows = [
            {"name": "a.zip", "link": "https://a", "extra": 1},
            {"name": "b.zip", "link": "https://b"},
        ]
        assert _backup_rows_from_list_response(rows) == [
            {"name": "a.zip", "link": "https://a"},
            {"name": "b.zip", "link": "https://b"},
        ]

    def test_bare_list_omits_incomplete_rows(self):
        assert _backup_rows_from_list_response(
            [{"name": "a.zip"}, {"name": "b.zip", "link": "https://b"}],
        ) == [{"name": "b.zip", "link": "https://b"}]

    def test_list_filters_non_dicts(self):
        assert _backup_rows_from_list_response(
            [{"name": "x", "link": "y"}, "skip", 3],
        ) == [{"name": "x", "link": "y"}]

    def test_dict_without_model_returns_empty(self):
        assert _backup_rows_from_list_response({"statusCode": 200}) == []

    def test_dict_with_model_list(self):
        raw = {"model": [{"name": "b.zip", "link": "https://x/y"}]}
        assert _backup_rows_from_list_response(raw) == [
            {"name": "b.zip", "link": "https://x/y"},
        ]

    def test_dict_model_list_filters_non_dicts_and_incomplete(self):
        raw = {"model": [{"name": "a"}, "bad", {"name": "c.zip", "link": "https://c"}]}
        assert _backup_rows_from_list_response(raw) == [
            {"name": "c.zip", "link": "https://c"},
        ]

    def test_dict_model_non_list_returns_empty(self):
        assert _backup_rows_from_list_response({"model": {"name": "x"}}) == []

    def test_primitive_raw_returns_empty(self):
        assert _backup_rows_from_list_response(42) == []


class TestBackupCreation:
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_request_backup_basic(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post_no_retry429.return_value = {}
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        backups.request_backup()
        assert mock_client.post_no_retry429.call_args[0][0].endswith("/request")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_request_backup_with_options(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post_no_retry429.return_value = {}
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        backups.request_backup(ids=[2013, 16088], api_names=["Company", "Contact"])
        payload = mock_client.post_no_retry429.call_args[1]["json"]
        assert payload["ids"] == [2013, 16088]
        assert payload["apiNames"] == ["Company", "Contact"]


class TestListBackups:
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_backups(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"name": "b1.zip", "link": "https://example.com/b1.zip"},
            {"name": "b2.zip", "link": "https://example.com/b2.zip"},
        ]
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = backups.list_backups()
        assert len(result) == 2
        assert result[0]["name"] == "b1.zip"
        assert result[0]["link"] == "https://example.com/b1.zip"
        assert set(result[0].keys()) == {"name", "link"}

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_backups_strips_api_result_envelope(self, mock_client_class):
        """GET /backups returns ApiResult; list_backups returns only model rows as {name, link}."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "model": [
                {"name": "a.zip", "link": "https://blob/a.zip", "extra": "ignored"},
                {"name": "b.zip", "link": "https://blob/b.zip"},
            ],
            "statusCode": 200,
            "message": "OK",
        }
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = backups.list_backups()
        assert result == [
            {"name": "a.zip", "link": "https://blob/a.zip"},
            {"name": "b.zip", "link": "https://blob/b.zip"},
        ]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_list_backups_calls_backups_url(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        backups.list_backups()
        mock_client.get.assert_called_once_with("https://test.dealcloud.com/api/rest/v4/backups")


class TestDownloadBackup:
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_uses_list_link_with_skip_auth(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        sas = "https://blob.example.net/container/b123.zip?sv=1&sig=x"
        mock_client.get.return_value = {
            "model": [{"name": "b123.zip", "link": sas}],
            "statusCode": 200,
        }

        def write_content(endpoint, destination, **kwargs):
            path = __import__("pathlib").Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"backup content")

        mock_client.download_file.side_effect = write_content
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        output_path = tmp_path / "backup.zip"
        result = backups.download_backup(str(output_path), file_name="b123.zip")

        assert output_path.exists()
        assert output_path.read_bytes() == b"backup content"
        mock_client.get.assert_called_once()
        mock_client.download_file.assert_called_once()
        call_endpoint = mock_client.download_file.call_args[0][0]
        assert call_endpoint == sas
        assert mock_client.download_file.call_args[1].get("skip_auth") is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_fallback_rest_path_when_no_link(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"model": [], "statusCode": 200}

        def write_content(endpoint, destination, **kwargs):
            path = __import__("pathlib").Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"x")

        mock_client.download_file.side_effect = write_content
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        out = tmp_path / "b.zip"
        backups.download_backup(str(out), file_name="b.zip")
        mock_client.download_file.assert_called_once()
        assert mock_client.download_file.call_args[0][0].endswith("/backups/b.zip")
        assert mock_client.download_file.call_args[1].get("skip_auth") in (None, False)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_download_link_skips_list(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.download_file.return_value = 1
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        url = "https://blob.example.net/f?sig=1"
        out = str(tmp_path / "o.zip")
        backups.download_backup(out, download_link=url)
        mock_client.get.assert_not_called()
        mock_client.download_file.assert_called_once()
        assert mock_client.download_file.call_args[0][0] == url
        assert mock_client.download_file.call_args[1]["destination"] == out
        assert mock_client.download_file.call_args[1]["skip_auth"] is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_streaming_storage_open_write(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.download_file.return_value = 3
        mock_client_class.return_value = mock_client

        storage = LocalStorage(tmp_path)
        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        url = "https://blob.example.net/f?sig=1"
        backups.download_backup(
            file_name="b.zip",
            storage=storage,
            relative_path="exports/b.zip",
            download_link=url,
        )
        mock_client.download_file.assert_called_once()
        dest = mock_client.download_file.call_args[1]["destination"]
        assert hasattr(dest, "write")
        assert (tmp_path / "exports" / "b.zip").exists()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_rejects_output_path_and_storage(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        storage = LocalStorage(tmp_path)
        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(ValueError, match="either output_path or storage"):
            backups.download_backup(
                str(tmp_path / "o.zip"),
                file_name="x.zip",
                storage=storage,
                relative_path="k.zip",
                download_link="https://blob/x",
            )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_requires_file_name_or_download_link(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(ValueError, match="file_name when download_link"):
            backups.download_backup(str(tmp_path / "o.zip"))

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_skips_rows_until_name_matches(self, mock_client_class, tmp_path):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "model": [
                {"name": "other.zip", "link": "https://blob/x"},
                {"name": "target.zip", "link": "https://blob/target?sig=1"},
            ],
        }

        def write_content(endpoint, destination, **kwargs):
            path = __import__("pathlib").Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"z")

        mock_client.download_file.side_effect = write_content
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        out = tmp_path / "t.zip"
        backups.download_backup(str(out), file_name="target.zip")
        assert mock_client.download_file.call_args[0][0] == "https://blob/target?sig=1"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_download_backup_non_http_link_falls_back_to_rest_endpoint(
        self, mock_client_class, tmp_path
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "model": [{"name": "x.zip", "link": "ftp://files/x.zip"}],
        }

        def write_content(endpoint, destination, **kwargs):
            path = __import__("pathlib").Path(destination)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"rest")

        mock_client.download_file.side_effect = write_content
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        out = tmp_path / "x.zip"
        backups.download_backup(str(out), file_name="x.zip")
        ep = mock_client.download_file.call_args[0][0]
        assert ep.endswith("/backups/x.zip")
        assert mock_client.download_file.call_args[1].get("skip_auth") is not True


class TestDeleteBackup:
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_backup(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        backups = DealCloudBackups(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = backups.delete_backup("b123.zip")
        assert result is True
        mock_client.post.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/backups/delete/b123.zip"
        )
