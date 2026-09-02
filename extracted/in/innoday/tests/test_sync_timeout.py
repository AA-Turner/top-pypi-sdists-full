"""A sync is not a read, and must not inherit a read's timeout.

`innoday --organization bp --project BPAI sync` failed every time with

    ✗ Error: ReadTimeout (no message)

against a 30-second default. Measured, BPAI's repo sync takes **~32 seconds** —
the worst possible margin: it always failed, always at the very end, and the
message named neither what had timed out nor that the work had nearly finished.
There was also no supported way to raise the limit: `set_api_timeout` existed
with nothing able to call it, and `config set` did not accept the key.
"""

from unittest.mock import MagicMock

from src.cli.client import InnoDayAPIClient
from src.cli.config import CLIConfig


def _config(api_timeout=30.0):
    config = MagicMock()
    config.get_api_url.return_value = "https://www.inno.day"
    config.get_api_timeout.return_value = api_timeout
    config.get_current_organization.return_value = None
    config.get_current_project_id.return_value = None
    config.get_user_id.return_value = None
    config.get_cli_token.return_value = None
    config.get_team_secret.return_value = None
    return config


class TestSyncGetsALongerBudget:
    def test_the_floor_beats_the_read_default(self):
        config = CLIConfig.__new__(CLIConfig)
        config._config = {"platform": {"api_timeout": 30.0}}
        assert config.get_api_timeout() == 30.0
        assert config.get_sync_timeout() == CLIConfig.SYNC_TIMEOUT_FLOOR

    def test_the_floor_clears_the_measured_bpai_time(self):
        """~32s measured. A floor that did not clear it by a wide margin would
        just move the cliff rather than remove it."""
        assert CLIConfig.SYNC_TIMEOUT_FLOOR > 60

    def test_a_deliberately_longer_configured_timeout_still_wins(self):
        """A floor, not a replacement — someone who configured 600s wants it
        everywhere, not everywhere except the slowest command."""
        config = CLIConfig.__new__(CLIConfig)
        config._config = {"platform": {"api_timeout": 600.0}}
        assert config.get_sync_timeout() == 600.0


class TestTheClientHonoursAnOverride:
    def test_default_uses_the_configured_timeout(self):
        client = InnoDayAPIClient(_config(api_timeout=30.0))
        assert client.api_client.timeout.read == 30.0

    def test_an_override_replaces_it(self):
        client = InnoDayAPIClient(_config(api_timeout=30.0), timeout=300.0)
        assert client.api_client.timeout.read == 300.0

    def test_an_override_of_zero_is_not_mistaken_for_absent(self):
        """`if timeout:` would fall back to the config here; `is not None` does
        not. Zero is a strange choice but it is a choice."""
        client = InnoDayAPIClient(_config(api_timeout=30.0), timeout=0)
        assert client.api_client.timeout.read == 0
