# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `airbyte_ops_mcp.connector_secrets` (ported from airbyte-python-cdk)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from cyclopts.exceptions import CycloptsError

from airbyte_ops_mcp.cli._base import app
from airbyte_ops_mcp.connector_secrets import (
    ConnectorSecretWithNoValidVersionsError,
    write_secret_file,
)


class TestWriteSecretFile:
    @pytest.fixture
    def mock_client(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_secret(self) -> MagicMock:
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/test-secret"
        return secret

    @pytest.fixture
    def mock_file_path(self, tmp_path):
        return tmp_path / "test_secret.json"

    def test_write_secret_file_with_enabled_version(
        self, mock_client, mock_secret, mock_file_path
    ) -> None:
        mock_version = MagicMock()
        mock_version.name = f"{mock_secret.name}/versions/1"
        mock_client.list_secret_versions.return_value = [mock_version]

        mock_response = MagicMock()
        mock_response.payload.data.decode.return_value = '{"key": "value"}'
        mock_client.access_secret_version.return_value = mock_response

        write_secret_file(
            secret=mock_secret,
            client=mock_client,
            file_path=mock_file_path,
            connector_name="test-connector",
            gcp_project_id="test-project",
        )

        mock_client.list_secret_versions.assert_called_once()
        assert "state:ENABLED" in str(mock_client.list_secret_versions.call_args)
        mock_client.access_secret_version.assert_called_once_with(
            name=mock_version.name
        )
        assert mock_file_path.read_text() == '{"key": "value"}'

    def test_write_secret_file_with_no_enabled_versions(
        self, mock_client, mock_secret, mock_file_path
    ) -> None:
        mock_client.list_secret_versions.return_value = []

        with pytest.raises(ConnectorSecretWithNoValidVersionsError) as excinfo:
            write_secret_file(
                secret=mock_secret,
                client=mock_client,
                file_path=mock_file_path,
                connector_name="test-connector",
                gcp_project_id="test-project",
            )

        mock_client.list_secret_versions.assert_called_once()
        assert "state:ENABLED" in str(mock_client.list_secret_versions.call_args)
        mock_client.access_secret_version.assert_not_called()
        assert not mock_file_path.exists()
        assert excinfo.value.secret_name == "test-secret"
        assert excinfo.value.connector_name == "test-connector"
        assert excinfo.value.gcp_project_id == "test-project"


@patch("airbyte_ops_mcp.cli.secrets.get_gsm_secrets_client")
@patch("airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory")
@patch("airbyte_ops_mcp.cli.secrets.get_secrets_dir")
@patch("airbyte_ops_mcp.cli.secrets.fetch_secret_handles")
class TestFetchCommand:
    """Exercise the `airbyte-ops secrets fetch` cyclopts command end-to-end."""

    def _invoke_fetch(self) -> None:
        """Dispatch `airbyte-ops secrets fetch` through the cyclopts root app.

        Cyclopts calls `sys.exit(0)` on clean return; swallow that specific
        case so tests can assert on captured output.
        """
        try:
            app(tokens=["secrets", "fetch"], exit_on_error=False)
        except SystemExit as exc:
            if exc.code not in (0, None):
                raise

    def test_fetch_with_some_failed_secrets(
        self,
        mock_fetch_secret_handles,
        mock_get_secrets_dir,
        mock_resolve,
        mock_get_client,
        tmp_path,
        capsys,
    ) -> None:
        mock_get_client.return_value = MagicMock()
        mock_resolve.return_value = ("test-connector", tmp_path)
        mock_get_secrets_dir.return_value = tmp_path / "secrets"

        secret1 = MagicMock()
        secret1.name = "projects/test-project/secrets/test-secret-1"
        secret1.labels = {}
        secret2 = MagicMock()
        secret2.name = "projects/test-project/secrets/test-secret-2"
        secret2.labels = {}
        mock_fetch_secret_handles.return_value = [secret1, secret2]

        with patch("airbyte_ops_mcp.cli.secrets.write_secret_file") as mock_write:
            mock_write.side_effect = [
                None,
                ConnectorSecretWithNoValidVersionsError(
                    connector_name="test-connector",
                    secret_name="test-secret-2",
                    gcp_project_id="test-project",
                ),
            ]

            self._invoke_fetch()

            assert mock_write.call_count == 2

        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "Failed to retrieve secret 'test-secret-2'" in combined
        assert "Failed to retrieve 1 secret(s)" in combined

    def test_fetch_with_all_failed_secrets(
        self,
        mock_fetch_secret_handles,
        mock_get_secrets_dir,
        mock_resolve,
        mock_get_client,
        tmp_path,
        capsys,
    ) -> None:
        mock_get_client.return_value = MagicMock()
        mock_resolve.return_value = ("test-connector", tmp_path)
        mock_get_secrets_dir.return_value = tmp_path / "secrets"

        secret1 = MagicMock()
        secret1.name = "projects/test-project/secrets/test-secret-1"
        secret1.labels = {}
        secret2 = MagicMock()
        secret2.name = "projects/test-project/secrets/test-secret-2"
        secret2.labels = {}
        mock_fetch_secret_handles.return_value = [secret1, secret2]

        with patch("airbyte_ops_mcp.cli.secrets.write_secret_file") as mock_write:
            mock_write.side_effect = [
                ConnectorSecretWithNoValidVersionsError(
                    connector_name="test-connector",
                    secret_name="test-secret-1",
                    gcp_project_id="test-project",
                ),
                ConnectorSecretWithNoValidVersionsError(
                    connector_name="test-connector",
                    secret_name="test-secret-2",
                    gcp_project_id="test-project",
                ),
            ]

            with pytest.raises(
                (ConnectorSecretWithNoValidVersionsError, CycloptsError)
            ):
                self._invoke_fetch()

            assert mock_write.call_count == 2

        captured = capsys.readouterr()
        combined = captured.out + captured.err
        assert "Failed to retrieve secret 'test-secret-1'" in combined
        assert "Failed to retrieve secret 'test-secret-2'" in combined
        assert "Failed to retrieve 2 secret(s)" in combined
