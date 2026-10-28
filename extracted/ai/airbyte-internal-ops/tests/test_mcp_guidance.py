import pytest
from airbyte import constants
from airbyte.exceptions import AirbyteNoCloudCredentialsError


@pytest.mark.parametrize("hosted", [True, False])
def test_shared_hosted_mcp_mode(
    hosted: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(constants, "_HOSTED_MCP_MODE_ENABLED", hosted)
    error = AirbyteNoCloudCredentialsError(_allow_bearer=False)
    if hosted:
        assert error.guidance == (
            "Provide client credentials via the transport `Client-Id` and "
            "`Client-Secret` headers."
        )
    else:
        assert error.guidance == (
            "Provide both `client_id` and `client_secret`, as arguments or via the "
            "`AIRBYTE_CLOUD_CLIENT_ID` and `AIRBYTE_CLOUD_CLIENT_SECRET` environment "
            "variables."
        )
