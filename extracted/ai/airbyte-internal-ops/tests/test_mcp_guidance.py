import pytest
from airbyte import constants
from airbyte.exceptions import AirbyteNoCloudCredentialsError

from airbyte_ops_mcp.mcp import connector_qa


@pytest.mark.parametrize("hosted", [True, False])
def test_shared_hosted_mcp_mode(
    hosted: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(constants, "_HOSTED_MCP_MODE_ENABLED", hosted)
    error = AirbyteNoCloudCredentialsError(_allow_bearer=False)
    if hosted:
        assert error.guidance == (
            "Provide client credentials via the `X-Airbyte-Cloud-Client-Id` and "
            "`X-Airbyte-Cloud-Client-Secret` headers."
        )
    else:
        assert error.guidance == (
            "Provide both `client_id` and `client_secret`, as arguments or via the "
            "`AIRBYTE_CLOUD_CLIENT_ID` and `AIRBYTE_CLOUD_CLIENT_SECRET` environment "
            "variables."
        )


def test_connector_qa_missing_credentials_uses_shared_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(constants, "_HOSTED_MCP_MODE_ENABLED", False)
    monkeypatch.setattr(connector_qa, "resolve_cloud_client_id", lambda: None)
    monkeypatch.setattr(connector_qa, "resolve_cloud_client_secret", lambda: None)

    with pytest.raises(AirbyteNoCloudCredentialsError) as exc_info:
        connector_qa.validate_connection_workspace("connection-id", "workspace-id")

    assert exc_info.value.guidance == (
        "Provide both `client_id` and `client_secret`, as arguments or via the "
        "`AIRBYTE_CLOUD_CLIENT_ID` and `AIRBYTE_CLOUD_CLIENT_SECRET` environment "
        "variables."
    )
