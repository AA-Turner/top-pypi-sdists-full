# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `airbyte_ops_mcp.connector_secrets` (ported from airbyte-python-cdk)."""

from __future__ import annotations

from contextlib import ExitStack
from unittest.mock import MagicMock, call, patch

import pytest
from cyclopts.exceptions import CycloptsError
from google.api_core.exceptions import (
    AlreadyExists,
    GoogleAPICallError,
    NotFound,
    RetryError,
)

from airbyte_ops_mcp.cli._base import app
from airbyte_ops_mcp.connector_secrets import (
    ConnectorSecretAlreadyExistsError,
    ConnectorSecretConnectorMismatchError,
    ConnectorSecretFilenameConflictError,
    ConnectorSecretNotFoundError,
    ConnectorSecretVersionDisableError,
    ConnectorSecretWithNoValidVersionsError,
    InvalidConnectorSecretFilenameError,
    InvalidConnectorSecretNameError,
    InvalidConnectorSecretPayloadError,
    create_secret,
    get_gsm_writer_client,
    update_secret,
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


class TestCreateSecret:
    def test_create_secret_success(self) -> None:
        client = MagicMock()
        client.list_secrets.return_value = []
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        client.create_secret.return_value = secret
        version = MagicMock()
        version.name = f"{secret.name}/versions/1"
        client.add_secret_version.return_value = version

        value = '{ "token": "hidden-payload" }\n'
        result = create_secret(
            "source-miro",
            value,
            secret_name="SECRET_SOURCE-MIRO__CREDS",
            gcp_project_id="test-project",
            client=client,
        )

        client.create_secret.assert_called_once_with(
            request={
                "parent": "projects/test-project",
                "secret_id": "SECRET_SOURCE-MIRO__CREDS",
                "secret": {
                    "replication": {"automatic": {}},
                    "labels": {"connector": "source-miro"},
                },
            }
        )
        client.add_secret_version.assert_called_once_with(
            request={
                "parent": secret.name,
                "payload": {"data": value.encode("utf-8")},
            }
        )
        assert result == version.name

    def test_create_secret_with_filename_label(self) -> None:
        client = MagicMock()
        client.list_secrets.return_value = []
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__OAUTH"
        client.create_secret.return_value = secret
        version = MagicMock()
        version.name = f"{secret.name}/versions/1"
        client.add_secret_version.return_value = version

        result = create_secret(
            "source-miro",
            '{"token":"hidden"}',
            secret_name="SECRET_SOURCE-MIRO__OAUTH",
            filename="oauth_config",
            gcp_project_id="test-project",
            client=client,
        )

        assert client.create_secret.call_args.kwargs["request"]["secret"]["labels"] == {
            "connector": "source-miro",
            "filename": "oauth_config",
        }
        assert result == version.name

    @pytest.mark.parametrize(
        "secret_name",
        [
            "SECRET_WRONG__CREDS",
            "secret_source-miro__CREDS",
            "SECRET_SOURCE-MIRO",
            "SECRET_SOURCE-OTHER__CREDS",
        ],
    )
    def test_create_secret_rejects_invalid_name(self, secret_name: str) -> None:
        client = MagicMock()

        with pytest.raises(InvalidConnectorSecretNameError) as exc_info:
            create_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name=secret_name,
                client=client,
            )

        assert "SECRET_SOURCE-MIRO__[A-Z0-9_]+" in str(exc_info.value)
        assert "SECRET_SOURCE-MIRO__CREDS" in str(exc_info.value)
        client.create_secret.assert_not_called()

    @pytest.mark.parametrize(
        ("value", "is_valid_json"),
        [
            ('{"token":"payload-must-not-appear"', False),
            ('["payload-must-not-appear"]', True),
            ("{}", True),
            ('{"token": NaN}', False),
            ('{"a": Infinity}', False),
        ],
    )
    def test_create_secret_rejects_invalid_payload(
        self, value: str, is_valid_json: bool
    ) -> None:
        client = MagicMock()
        with pytest.raises(InvalidConnectorSecretPayloadError) as exc_info:
            create_secret(
                "source-miro",
                value,
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                client=client,
            )

        assert value not in str(exc_info.value)
        assert exc_info.value.is_valid_json is is_valid_json
        client.create_secret.assert_not_called()

    @pytest.mark.parametrize("filename", ["Bad", "has.dot", "", "a" * 64])
    def test_create_secret_rejects_invalid_filename(self, filename: str) -> None:
        client = MagicMock()
        with pytest.raises(InvalidConnectorSecretFilenameError):
            create_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                filename=filename,
                client=client,
            )

        client.create_secret.assert_not_called()

    @pytest.mark.parametrize(
        ("filename", "existing_labels"),
        [(None, {}), ("oauth_config", {"filename": "oauth_config"})],
    )
    def test_create_secret_rejects_filename_conflict(
        self, filename: str | None, existing_labels: dict[str, str]
    ) -> None:
        client = MagicMock()
        existing_secret = MagicMock()
        existing_secret.name = "projects/test-project/secrets/EXISTING_SECRET"
        existing_secret.labels = existing_labels
        client.list_secrets.return_value = [existing_secret]

        with pytest.raises(ConnectorSecretFilenameConflictError) as exc_info:
            create_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                filename=filename,
                gcp_project_id="test-project",
                client=client,
            )

        assert "EXISTING_SECRET" in str(exc_info.value)
        assert "different `--filename`" in str(exc_info.value)
        client.create_secret.assert_not_called()

    def test_create_secret_maps_already_exists(self) -> None:
        client = MagicMock()
        client.list_secrets.return_value = []
        client.create_secret.side_effect = AlreadyExists("exists")

        with pytest.raises(ConnectorSecretAlreadyExistsError):
            create_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                client=client,
            )

        client.add_secret_version.assert_not_called()


class TestUpdateSecret:
    def test_update_secret_disables_previous_versions_after_add(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-miro"}
        client.get_secret.return_value = secret
        old_versions = [MagicMock(), MagicMock()]
        old_versions[0].name = f"{secret.name}/versions/1"
        old_versions[1].name = f"{secret.name}/versions/2"
        client.list_secret_versions.return_value = old_versions
        version = MagicMock()
        version.name = f"{secret.name}/versions/3"
        client.add_secret_version.return_value = version
        value = '{"token":"new-hidden-payload"}'

        result = update_secret(
            "source-miro",
            value,
            secret_name="SECRET_SOURCE-MIRO__CREDS",
            gcp_project_id="test-project",
            client=client,
        )

        client.get_secret.assert_called_once_with(name=secret.name)
        client.add_secret_version.assert_called_once_with(
            request={
                "parent": secret.name,
                "payload": {"data": value.encode("utf-8")},
            }
        )
        assert client.mock_calls == [
            call.get_secret(name=secret.name),
            call.list_secret_versions(
                request={"parent": secret.name, "filter": "state:ENABLED"}
            ),
            call.add_secret_version(
                request={
                    "parent": secret.name,
                    "payload": {"data": value.encode("utf-8")},
                }
            ),
            call.disable_secret_version(request={"name": old_versions[0].name}),
            call.disable_secret_version(request={"name": old_versions[1].name}),
        ]
        client.destroy_secret_version.assert_not_called()
        client.delete_secret.assert_not_called()
        assert result == version.name

    def test_update_secret_add_failure_does_not_disable_versions(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-miro"}
        client.get_secret.return_value = secret
        old_version = MagicMock()
        old_version.name = f"{secret.name}/versions/1"
        client.list_secret_versions.return_value = [old_version]
        client.add_secret_version.side_effect = GoogleAPICallError("add failed")

        with pytest.raises(GoogleAPICallError):
            update_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                gcp_project_id="test-project",
                client=client,
            )

        client.disable_secret_version.assert_not_called()

    def test_update_secret_continues_after_disable_failure(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-miro"}
        client.get_secret.return_value = secret
        old_versions = [MagicMock(), MagicMock(), MagicMock()]
        for index, old_version in enumerate(old_versions, start=1):
            old_version.name = f"{secret.name}/versions/{index}"
        client.list_secret_versions.return_value = old_versions
        new_version = MagicMock()
        new_version.name = f"{secret.name}/versions/4"
        client.add_secret_version.return_value = new_version
        client.disable_secret_version.side_effect = [
            None,
            GoogleAPICallError("disable failed"),
            None,
        ]
        value = '{"token":"disable-failure-payload"}'

        with pytest.raises(ConnectorSecretVersionDisableError) as exc_info:
            update_secret(
                "source-miro",
                value,
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                gcp_project_id="test-project",
                client=client,
            )

        error = exc_info.value
        assert error.secret_name == "SECRET_SOURCE-MIRO__CREDS"
        assert error.new_version_name == new_version.name
        assert error.failed_version_names == [old_versions[1].name]
        assert "was added and is now the latest" in str(error)
        assert old_versions[1].name in str(error)
        assert value not in str(error)
        assert client.disable_secret_version.call_args_list == [
            call(request={"name": old_version.name}) for old_version in old_versions
        ]

    def test_update_secret_continues_after_retry_error(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-miro"}
        client.get_secret.return_value = secret
        old_versions = [MagicMock(), MagicMock()]
        for index, old_version in enumerate(old_versions, start=1):
            old_version.name = f"{secret.name}/versions/{index}"
        client.list_secret_versions.return_value = old_versions
        new_version = MagicMock()
        new_version.name = f"{secret.name}/versions/3"
        client.add_secret_version.return_value = new_version
        client.disable_secret_version.side_effect = [
            RetryError("exhausted", cause=None),
            None,
        ]

        with pytest.raises(ConnectorSecretVersionDisableError) as exc_info:
            update_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                gcp_project_id="test-project",
                client=client,
            )

        assert exc_info.value.failed_version_names == [old_versions[0].name]
        assert exc_info.value.new_version_name == new_version.name
        assert client.disable_secret_version.call_args_list == [
            call(request={"name": old_version.name}) for old_version in old_versions
        ]

    def test_update_secret_never_disables_new_version(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-miro"}
        client.get_secret.return_value = secret
        version = MagicMock()
        version.name = f"{secret.name}/versions/2"
        client.list_secret_versions.return_value = [version]
        client.add_secret_version.return_value = version

        result = update_secret(
            "source-miro",
            '{"token":"hidden"}',
            secret_name="SECRET_SOURCE-MIRO__CREDS",
            gcp_project_id="test-project",
            client=client,
        )

        assert result == version.name
        client.disable_secret_version.assert_not_called()

    def test_update_secret_maps_not_found(self) -> None:
        client = MagicMock()
        client.get_secret.side_effect = NotFound("missing")

        with pytest.raises(ConnectorSecretNotFoundError):
            update_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                client=client,
            )

        client.add_secret_version.assert_not_called()

    def test_update_secret_rejects_connector_label_mismatch(self) -> None:
        client = MagicMock()
        secret = MagicMock()
        secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS"
        secret.labels = {"connector": "source-other"}
        client.get_secret.return_value = secret

        with pytest.raises(ConnectorSecretConnectorMismatchError) as exc_info:
            update_secret(
                "source-miro",
                '{"token":"hidden"}',
                secret_name="SECRET_SOURCE-MIRO__CREDS",
                gcp_project_id="test-project",
                client=client,
            )

        assert "source-other" in str(exc_info.value)
        client.add_secret_version.assert_not_called()


def test_writer_client_uses_writer_credentials(monkeypatch) -> None:
    monkeypatch.setenv("GCP_GSM_WRITER_CREDENTIALS", '{"type":"writer"}')
    monkeypatch.setenv("GCP_GSM_CREDENTIALS", '{"type":"read-only"}')
    with patch(
        "airbyte_ops_mcp.connector_secrets.gsm.secretmanager.SecretManagerServiceClient.from_service_account_info"
    ) as from_service_account_info:
        client = get_gsm_writer_client()

    from_service_account_info.assert_called_once_with({"type": "writer"})
    assert "read-only" not in str(from_service_account_info.call_args)
    assert client == from_service_account_info.return_value


def _invoke_secrets_command(tokens: list[str]) -> None:
    try:
        app(tokens=tokens, exit_on_error=False)
    except SystemExit as exc:
        if exc.code not in (0, None):
            raise


def test_create_command_uses_default_config_path_and_hides_payload(
    tmp_path, capsys
) -> None:
    secrets_dir = tmp_path / "secrets"
    secrets_dir.mkdir()
    config_file = secrets_dir / "config.json"
    payload = '{"token":"cli-payload-must-not-appear"}'
    config_file.write_text(payload)

    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory",
                return_value=("source-miro", tmp_path),
            )
        )
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        create_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.create_secret",
                return_value="projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS/versions/3",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "create",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__CREDS",
            ]
        )

    create_secret_mock.assert_called_once()
    assert create_secret_mock.call_args.kwargs["value"] == payload
    captured = capsys.readouterr()
    assert captured.out == ""
    assert payload not in captured.err
    assert "SECRET_SOURCE-MIRO__CREDS version 3" in captured.err


def test_create_command_uses_config_file_with_bare_connector(tmp_path, capsys) -> None:
    config_file = tmp_path / "custom.json"
    payload = '{"token":"custom-cli-payload-must-not-appear"}'
    config_file.write_text(payload)

    with ExitStack() as stack:
        resolve_connector = stack.enter_context(
            patch("airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory")
        )
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        create_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.create_secret",
                return_value="projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS/versions/4",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "create",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__CREDS",
                "--config-file",
                str(config_file),
            ]
        )

    resolve_connector.assert_not_called()
    assert create_secret_mock.call_args.kwargs["connector_name"] == "source-miro"
    assert create_secret_mock.call_args.kwargs["value"] == payload
    captured = capsys.readouterr()
    assert captured.out == ""
    assert payload not in captured.err


def test_create_command_resolves_existing_directory_with_config_file(
    tmp_path, monkeypatch
) -> None:
    config_file = tmp_path / "custom.json"
    config_file.write_text('{"token":"directory-argument"}')
    monkeypatch.chdir(tmp_path)

    with ExitStack() as stack:
        resolve_connector = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory",
                return_value=("source-miro", tmp_path),
            )
        )
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        create_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.create_secret",
                return_value="projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS/versions/7",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "create",
                ".",
                "--secret-name",
                "SECRET_SOURCE-MIRO__CREDS",
                "--config-file",
                str(config_file),
            ]
        )

    resolve_connector.assert_called_once_with(".")
    assert create_secret_mock.call_args.kwargs["connector_name"] == "source-miro"


def test_create_command_preserves_crlf_config_file_bytes(tmp_path) -> None:
    config_file = tmp_path / "custom.json"
    payload_bytes = b'{\r\n  "token":\r\n  "preserved"\r\n}'
    config_file.write_bytes(payload_bytes)

    with ExitStack() as stack:
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        create_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.create_secret",
                return_value="projects/test-project/secrets/SECRET_SOURCE-MIRO__CREDS/versions/8",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "create",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__CREDS",
                "--config-file",
                str(config_file),
            ]
        )

    assert create_secret_mock.call_args.kwargs["value"] == payload_bytes.decode("utf-8")


def test_create_command_rejects_non_utf8_config_file_without_byte_details(
    tmp_path,
) -> None:
    config_file = tmp_path / "invalid.json"
    config_file.write_bytes(b"\xff")

    with pytest.raises(ValueError) as exc_info:
        _invoke_secrets_command(
            [
                "secrets",
                "create",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__CREDS",
                "--config-file",
                str(config_file),
            ]
        )

    assert str(exc_info.value) == f"Config file is not valid UTF-8: {config_file}"


def test_update_command_uses_secret_filename_and_hides_payload(
    tmp_path, capsys
) -> None:
    secrets_dir = tmp_path / "secrets"
    secrets_dir.mkdir()
    config_file = secrets_dir / "oauth_config.json"
    payload = '{"token":"update-cli-payload-must-not-appear"}'
    config_file.write_text(payload)
    secret = MagicMock()
    secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__OAUTH"
    secret.labels = {"connector": "source-miro", "filename": "oauth_config"}

    with ExitStack() as stack:
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory",
                return_value=("source-miro", tmp_path),
            )
        )
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.get_connector_secret",
                return_value=secret,
            )
        )
        update_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.update_secret",
                return_value=f"{secret.name}/versions/5",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "update",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__OAUTH",
            ]
        )

    assert update_secret_mock.call_args.kwargs["value"] == payload
    captured = capsys.readouterr()
    assert captured.out == ""
    assert payload not in captured.err
    assert "SECRET_SOURCE-MIRO__OAUTH version 5" in captured.err


def test_update_command_uses_config_file_with_bare_connector(tmp_path, capsys) -> None:
    config_file = tmp_path / "override.json"
    payload = '{"token":"update-override-payload-must-not-appear"}'
    config_file.write_text(payload)
    secret = MagicMock()
    secret.name = "projects/test-project/secrets/SECRET_SOURCE-MIRO__OAUTH"
    secret.labels = {"connector": "source-miro", "filename": "oauth_config"}

    with ExitStack() as stack:
        resolve_connector = stack.enter_context(
            patch("airbyte_ops_mcp.cli.secrets.resolve_connector_name_and_directory")
        )
        stack.enter_context(patch("airbyte_ops_mcp.cli.secrets.get_gsm_writer_client"))
        stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.get_connector_secret",
                return_value=secret,
            )
        )
        update_secret_mock = stack.enter_context(
            patch(
                "airbyte_ops_mcp.cli.secrets.update_secret",
                return_value=f"{secret.name}/versions/6",
            )
        )
        _invoke_secrets_command(
            [
                "secrets",
                "update",
                "source-miro",
                "--secret-name",
                "SECRET_SOURCE-MIRO__OAUTH",
                "--config-file",
                str(config_file),
            ]
        )

    resolve_connector.assert_not_called()
    assert update_secret_mock.call_args.kwargs["connector_name"] == "source-miro"
    assert update_secret_mock.call_args.kwargs["value"] == payload
    captured = capsys.readouterr()
    assert captured.out == ""
    assert payload not in captured.err
