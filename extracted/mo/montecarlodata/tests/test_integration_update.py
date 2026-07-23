import uuid
from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

from montecarlodata.integrations.commands import update_credentials
from tests.test_common_user import _SAMPLE_CONFIG

_SAMPLE_UUID = str(uuid.uuid4())


class IntegrationsUpdateCredentialsCliTest(TestCase):
    @patch("montecarlodata.integrations.commands.ConnectionOperationsService")
    def test_sentinel_secret_is_prompted_and_substituted(self, service_class_mock):
        """A "-1" value in --changes is replaced by the masked prompt input before
        the value ever reaches the service layer."""
        update_mock = service_class_mock.return_value.update_credentials

        runner = CliRunner()
        result = runner.invoke(
            update_credentials,
            obj={"config": _SAMPLE_CONFIG},
            args=[
                "--connection-id",
                _SAMPLE_UUID,
                "--changes",
                '{"databricks_client_secret": "-1", "databricks_client_id": "public-id"}',
                "--skip-validation",
            ],
            input="entered-secret\n",
        )

        self.assertEqual(result.exit_code, 0, result.output)
        update_mock.assert_called_once()
        call_kwargs = update_mock.call_args[1]
        self.assertEqual(
            call_kwargs["changes"],
            {"databricks_client_secret": "entered-secret", "databricks_client_id": "public-id"},
        )
        self.assertFalse(call_kwargs["should_validate"])
        # The secret must never be echoed back (hidden input).
        self.assertNotIn("entered-secret", result.output)

    @patch("montecarlodata.integrations.commands.ConnectionOperationsService")
    def test_plaintext_changes_pass_through_unchanged(self, service_class_mock):
        """Without a "-1" sentinel, --changes is forwarded verbatim and no prompt occurs."""
        update_mock = service_class_mock.return_value.update_credentials

        runner = CliRunner()
        result = runner.invoke(
            update_credentials,
            obj={"config": _SAMPLE_CONFIG},
            args=[
                "--connection-id",
                _SAMPLE_UUID,
                "--changes",
                '{"user": "Apollo"}',
            ],
            input="",
        )

        self.assertEqual(result.exit_code, 0, result.output)
        update_mock.assert_called_once()
        self.assertEqual(update_mock.call_args[1]["changes"], {"user": "Apollo"})
