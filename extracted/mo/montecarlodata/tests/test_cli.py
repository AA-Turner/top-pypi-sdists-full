import configparser
import os
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner

from montecarlodata.cli import AUTH_TYPE_API_KEY, AUTH_TYPE_OAUTH, configure

# A valid mcd_token is exactly 56 chars (ConfigManager.write enforces it).
_VALID_TOKEN = "x" * 56


class ConfigureTest(TestCase):
    def setUp(self) -> None:
        self._runner = CliRunner()

    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_oauth_flag(self, config_manager_mock: Mock):
        result = self._runner.invoke(
            configure,
            [
                "--oauth",
                "--mcd-oauth-client-id",
                "cid",
                "--mcd-oauth-client-secret",
                "sec",
                "--mcd-instance-id",
                "us1",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_called_once_with(
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
        )

    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_oauth_invalid_instance_id_flag(self, config_manager_mock: Mock):
        result = self._runner.invoke(
            configure,
            [
                "--oauth",
                "--mcd-oauth-client-id",
                "cid",
                "--mcd-oauth-client-secret",
                "sec",
                "--mcd-instance-id",
                "not a valid id!",
            ],
        )
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid instance id", result.output)
        config_manager_mock.return_value.write.assert_not_called()

    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_oauth_reprompts_on_invalid_instance_id(self, config_manager_mock: Mock):
        # Invalid instance id at the prompt re-prompts; a valid one then succeeds.
        result = self._runner.invoke(
            configure,
            ["--oauth", "--mcd-oauth-client-id", "cid", "--mcd-oauth-client-secret", "sec"],
            input="bad id!\nus1\n",
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Invalid instance id", result.output)
        config_manager_mock.return_value.write.assert_called_once_with(
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
        )

    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_api_key_flag(self, config_manager_mock: Mock):
        result = self._runner.invoke(
            configure,
            ["--api-key", "--mcd-id", "id", "--mcd-token", "tok"],
        )
        self.assertEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_called_once_with(mcd_id="id", mcd_token="tok")

    @patch("montecarlodata.cli.questionary")
    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_prompts_for_auth_type_oauth(
        self, config_manager_mock: Mock, questionary_mock: Mock
    ):
        # No auth flag -> arrow-key picker; choose oauth, then provide oauth details.
        questionary_mock.select.return_value.ask.return_value = AUTH_TYPE_OAUTH
        result = self._runner.invoke(configure, input="cid\nsec\nus1\n")
        self.assertEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_called_once_with(
            mcd_oauth_client_id="cid",
            mcd_oauth_client_secret="sec",
            mcd_instance_id="us1",
        )

    @patch("montecarlodata.cli.questionary")
    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_prompts_for_auth_type_api_key(
        self, config_manager_mock: Mock, questionary_mock: Mock
    ):
        # Picker returns api-key, then prompts for key/secret.
        questionary_mock.select.return_value.ask.return_value = AUTH_TYPE_API_KEY
        result = self._runner.invoke(configure, input="id\ntok\n")
        self.assertEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_called_once_with(mcd_id="id", mcd_token="tok")

    @patch("montecarlodata.cli.questionary")
    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_aborts_when_auth_type_cancelled(
        self, config_manager_mock: Mock, questionary_mock: Mock
    ):
        # Cancelling the picker (Ctrl-C) returns None -> abort without writing.
        questionary_mock.select.return_value.ask.return_value = None
        result = self._runner.invoke(configure)
        self.assertNotEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_not_called()

    @patch("montecarlodata.cli.ConfigManager")
    def test_configure_oauth_and_api_key_mutually_exclusive(self, config_manager_mock: Mock):
        result = self._runner.invoke(configure, ["--oauth", "--api-key"])
        self.assertNotEqual(result.exit_code, 0)
        config_manager_mock.return_value.write.assert_not_called()

    def test_reconfigure_oauth_to_api_key_clears_stale_oauth_creds(self):
        # Real config round-trip: switching an existing OAuth profile to API key must drop the
        # stale OAuth credentials (otherwise OAuth wins in Config.read and the new key is ignored).
        with tempfile.TemporaryDirectory() as tmp:
            first = self._runner.invoke(
                configure,
                [
                    "--config-path",
                    tmp,
                    "--oauth",
                    "--mcd-oauth-client-id",
                    "cid",
                    "--mcd-oauth-client-secret",
                    "sec",
                    "--mcd-instance-id",
                    "us1",
                ],
            )
            self.assertEqual(first.exit_code, 0, first.output)
            second = self._runner.invoke(
                configure,
                [
                    "--config-path",
                    tmp,
                    "--api-key",
                    "--mcd-id",
                    "the-id",
                    "--mcd-token",
                    _VALID_TOKEN,
                ],
            )
            self.assertEqual(second.exit_code, 0, second.output)

            cfg = configparser.ConfigParser()
            cfg.read(os.path.join(tmp, "profiles.ini"))
            section = cfg["default"]
            self.assertEqual(section.get("mcd_id"), "the-id")
            self.assertEqual(section.get("mcd_token"), _VALID_TOKEN)
            self.assertNotIn("mcd_oauth_client_id", section)
            self.assertNotIn("mcd_oauth_client_secret", section)
            self.assertNotIn("mcd_instance_id", section)

    def test_reconfigure_api_key_to_oauth_clears_stale_token(self):
        # The reverse: switching an API-key profile to OAuth must not leave the live token behind.
        with tempfile.TemporaryDirectory() as tmp:
            first = self._runner.invoke(
                configure,
                ["--config-path", tmp, "--api-key", "--mcd-id", "id", "--mcd-token", _VALID_TOKEN],
            )
            self.assertEqual(first.exit_code, 0, first.output)
            second = self._runner.invoke(
                configure,
                [
                    "--config-path",
                    tmp,
                    "--oauth",
                    "--mcd-oauth-client-id",
                    "cid",
                    "--mcd-oauth-client-secret",
                    "sec",
                    "--mcd-instance-id",
                    "us1",
                ],
            )
            self.assertEqual(second.exit_code, 0, second.output)

            cfg = configparser.ConfigParser()
            cfg.read(os.path.join(tmp, "profiles.ini"))
            section = cfg["default"]
            self.assertEqual(section.get("mcd_oauth_client_id"), "cid")
            self.assertNotIn("mcd_id", section)
            self.assertNotIn("mcd_token", section)
