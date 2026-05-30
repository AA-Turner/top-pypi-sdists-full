import json
from unittest import TestCase
from unittest.mock import Mock, patch

import click
from pycarlo.core import Client

from montecarlodata.agents.agent import AgentService
from montecarlodata.agents.fields import (
    AWS,
    AWS_ASSUMABLE_ROLE,
    AZURE,
    AZURE_BLOB,
    AZURE_FUNCTION_APP_KEY,
    AZURE_FUNCTION_SERVICE_PRINCIPAL,
    AZURE_STORAGE_ACCOUNT_KEYS,
    AZURE_STORAGE_SERVICE_PRINCIPAL,
    DATA_STORE_AGENT,
    REMOTE_AGENT,
    S3,
)
from montecarlodata.common.user import UserService
from tests.helpers import capture_function
from tests.test_common_user import _SAMPLE_CONFIG


class AgentServiceTest(TestCase):
    def setUp(self) -> None:
        self._mc_client = Mock(spec=Client)
        self._user_service = Mock(spec=UserService)
        self._service = AgentService(
            config=_SAMPLE_CONFIG,
            mc_client=self._mc_client,
            command_name="test",
            user_service=self._user_service,
        )

    # ------------------------------------------------------------------
    # _ensure_aws_external_id
    # ------------------------------------------------------------------

    def test_ensure_aws_external_id_uses_existing_value(self):
        response = Mock()
        response.get_agent_aws_external_id.external_id = "existing-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service._ensure_aws_external_id,
            {"agent_id": "abc-123", "agent_type": REMOTE_AGENT},
        )

        self.assertIsNone(out.exception)
        # No mint should have been called: only the get query went out.
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("existing-id", captured)
        self.assertIn("Existing ExternalId preserved", captured)
        # Remote-agent next-steps point the user at register-aws-agent --agent-id.
        self.assertIn("register-aws-agent --agent-id abc-123", captured)
        self.assertIn("--lambda-arn", captured)

    def test_ensure_aws_external_id_mints_when_missing(self):
        response = Mock()
        response.get_agent_aws_external_id = None  # not generated yet
        response.generate_agent_aws_external_id.result.external_id = "minted-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service._ensure_aws_external_id,
            {"agent_id": "abc-123", "agent_type": REMOTE_AGENT},
        )

        self.assertIsNone(out.exception)
        # Two GraphQL operations: the get, then the generate.
        self.assertEqual(2, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("ExternalId generated", captured)
        self.assertIn("minted-id", captured)

    def test_ensure_aws_external_id_data_store_message(self):
        # Data-store next-steps should point at register-s3-store with --bucket-name.
        response = Mock()
        response.get_agent_aws_external_id = None
        response.generate_agent_aws_external_id.result.external_id = "minted-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service._ensure_aws_external_id,
            {"agent_id": "abc-123", "agent_type": "DATA_STORE_AGENT"},
        )

        self.assertIsNone(out.exception)
        captured = out.std_out.getvalue()
        self.assertIn("register-s3-store --agent-id abc-123", captured)
        self.assertIn("--bucket-name", captured)

    # ------------------------------------------------------------------
    # set_agent_enabled
    # ------------------------------------------------------------------

    def test_set_agent_enabled_dry_run_success_does_not_change_state(self):
        response = Mock()
        response.update_agent_enabled.validation_result.success = True
        response.update_agent_enabled.validation_result.errors = None
        response.update_agent_enabled.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.set_agent_enabled,
            {"agent_id": "abc-123", "enabled": True, "dry_run": True},
        )

        self.assertIsNone(out.exception)
        captured = out.std_out.getvalue()
        self.assertIn("Dry run completed successfully", captured)
        self.assertIn("would be enabled", captured)

    def test_set_agent_enabled_dry_run_failure_aborts(self):
        response = Mock()
        response.update_agent_enabled.validation_result.success = False
        response.update_agent_enabled.validation_result.errors = None
        response.update_agent_enabled.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.set_agent_enabled,
            {"agent_id": "abc-123", "enabled": True, "dry_run": True},
        )

        self.assertIsInstance(out.exception, click.exceptions.Abort)

    def test_set_agent_enabled_disable_echoes_disabled(self):
        response = Mock()
        response.update_agent_enabled.validation_result = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.set_agent_enabled,
            {"agent_id": "abc-123", "enabled": False},
        )

        self.assertIsNone(out.exception)
        self.assertIn("disabled", out.std_out.getvalue())

    # ------------------------------------------------------------------
    # rotate_aws_external_id
    # ------------------------------------------------------------------

    def test_rotate_aws_external_id_no_prompt_mints_and_displays(self):
        response = Mock()
        response.generate_agent_aws_external_id.result.external_id = "rotated-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service.rotate_aws_external_id,
            {"agent_id": "abc-123", "no_prompt": True},
        )

        self.assertIsNone(out.exception)
        captured = out.std_out.getvalue()
        self.assertIn("ExternalId rotated", captured)
        self.assertIn("rotated-id", captured)

    def test_rotate_aws_external_id_aborts_when_user_declines_prompt(self):
        # No mc_client response needed: the abort happens before any GraphQL call.
        with self.assertRaises(click.exceptions.Abort):
            with click.Context(click.Command("test")):
                # Simulate user typing "n" at the click.confirm prompt.
                with self._patch_stdin("n\n"):
                    self._service.rotate_aws_external_id(agent_id="abc-123", no_prompt=False)
        self._mc_client.assert_not_called()

    @staticmethod
    def _patch_stdin(text: str):
        import io
        import sys
        from contextlib import contextmanager

        @contextmanager
        def _ctx():
            saved = sys.stdin
            sys.stdin = io.StringIO(text)
            try:
                yield
            finally:
                sys.stdin = saved

        return _ctx()

    # ------------------------------------------------------------------
    # create_agent (AWS path triggers external_id flow)
    # ------------------------------------------------------------------

    def test_create_aws_agent_triggers_external_id_flow(self):
        response = Mock()
        response.create_or_update_agent.agent_id = "abc-123"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        # Get returns null on the first call, generate produces the value.
        response.get_agent_aws_external_id = None
        response.generate_agent_aws_external_id.result.external_id = "minted-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": REMOTE_AGENT,
                "platform": AWS,
                "storage": S3,
                "auth_type": AWS_ASSUMABLE_ROLE,
                "endpoint": "arn:aws:lambda:us-east-1:012345678901:function:agent",
                "assumable_role": "arn:aws:iam::012345678901:role/agent-invoker",
            },
        )

        self.assertIsNone(out.exception)
        # Three calls: create_or_update_agent, get_agent_aws_external_id, generate.
        self.assertEqual(3, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("minted-id", captured)

        # Confirm the mutation was called without external_id in credentials.
        first_call = self._mc_client.call_args_list[0]
        # The Mutation object has a get_field_args helper but to keep this test
        # simple we just verify we never sent an external_id key in the JSON
        # by re-inspecting kwargs passed through to create_or_update_agent.
        # We did this indirectly: the create_agent code path no longer reads
        # external_id from kwargs, so the JSON we'd build cannot include one.
        # Sanity check the input mutation didn't carry an external_id literal.
        sent = str(first_call)
        self.assertNotIn("external_id", sent)

    def test_create_aws_stub_without_role_or_endpoint_runs_external_id_flow(self):
        # First registration without --assumable-role / --lambda-arn: register
        # the stub on the backend, then auto-mint and display the ExternalId.
        response = Mock()
        response.create_or_update_agent.agent_id = "abc-123"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        response.get_agent_aws_external_id = None
        response.generate_agent_aws_external_id.result.external_id = "minted-id"
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": REMOTE_AGENT,
                "platform": AWS,
                "storage": S3,
                "auth_type": AWS_ASSUMABLE_ROLE,
                "endpoint": None,
                # No --assumable-role on first call.
            },
        )

        self.assertIsNone(out.exception)
        self.assertEqual(3, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("minted-id", captured)
        # The mutation argument carried no credentials at all.
        first_call_str = str(self._mc_client.call_args_list[0])
        self.assertNotIn("aws_assumable_role", first_call_str)
        self.assertNotIn("external_id", first_call_str)

    def test_complete_aws_stub_does_not_repeat_external_id_display(self):
        # Second call (--agent-id + role + endpoint): the backend will
        # auto-enable; the CLI just confirms the update without showing the
        # ExternalId again (it was shown on the first registration).
        response = Mock()
        response.create_or_update_agent.agent_id = "abc-123"
        response.create_or_update_agent.auto_enabled = True
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": REMOTE_AGENT,
                "platform": AWS,
                "storage": S3,
                "auth_type": AWS_ASSUMABLE_ROLE,
                "endpoint": "arn:aws:lambda:us-east-1:012345678901:function:agent",
                "assumable_role": "arn:aws:iam::012345678901:role/agent-invoker",
                "agent_id": "abc-123",
            },
        )

        self.assertIsNone(out.exception)
        # Just one mutation call: no get / generate on follow-up registrations.
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        # auto_enabled=True surfaces the "updated and enabled" message instead
        # of the plain "registered" wording.
        self.assertIn("Agent updated and enabled", captured)
        self.assertNotIn("Existing ExternalId", captured)
        self.assertNotIn("ExternalId generated", captured)

    def test_complete_aws_stub_when_auto_enabled_is_false(self):
        # If the update doesn't bring the agent into a fully configured state
        # (e.g. role supplied without endpoint), the backend won't auto-enable
        # and the CLI should fall back to the neutral "registered" message.
        response = Mock()
        response.create_or_update_agent.agent_id = "abc-123"
        response.create_or_update_agent.auto_enabled = False
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": REMOTE_AGENT,
                "platform": AWS,
                "storage": S3,
                "auth_type": AWS_ASSUMABLE_ROLE,
                "endpoint": None,
                "assumable_role": "arn:aws:iam::012345678901:role/agent-invoker",
                "agent_id": "abc-123",
            },
        )

        self.assertIsNone(out.exception)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertNotIn("Agent updated and enabled", captured)

    # ------------------------------------------------------------------
    # create_agent (Azure paths)
    # ------------------------------------------------------------------

    def test_create_azure_blob_store_connection_string(self):
        response = Mock()
        response.create_or_update_agent.agent_id = "azure-cs-123"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": DATA_STORE_AGENT,
                "platform": AZURE,
                "storage": AZURE_BLOB,
                "auth_type": AZURE_STORAGE_ACCOUNT_KEYS,
                "endpoint": "my-container",
                "connection_string": "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key",
            },
        )

        self.assertIsNone(out.exception)
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("azure-cs-123", captured)

        # Verify credentials contain azure_connection_string
        call_args = str(self._mc_client.call_args_list[0])
        self.assertIn("azure_connection_string", call_args)

    def test_create_azure_blob_store_service_principal(self):
        response = Mock()
        response.create_or_update_agent.agent_id = "azure-sp-123"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        # Capture the credentials JSON that create_agent serialises.
        captured_creds = {}
        original_dumps = json.dumps

        def intercept_dumps(obj, **kwargs):
            if isinstance(obj, dict) and "tenant_id" in obj:
                captured_creds.update(obj)
            return original_dumps(obj, **kwargs)

        with patch("montecarlodata.agents.agent.json.dumps", side_effect=intercept_dumps):
            out = capture_function(
                self._service.create_agent,
                {
                    "agent_type": DATA_STORE_AGENT,
                    "platform": AZURE,
                    "storage": AZURE_BLOB,
                    "auth_type": AZURE_STORAGE_SERVICE_PRINCIPAL,
                    "endpoint": "my-container",
                    "tenant_id": "tenant-abc",
                    "client_id": "client-def",
                    "client_secret": "secret-ghi",
                    "account_url": "mystorageaccount",
                },
            )

        self.assertIsNone(out.exception)
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("azure-sp-123", captured)

        # Verify credentials contain all SP fields
        self.assertEqual(captured_creds["tenant_id"], "tenant-abc")
        self.assertEqual(captured_creds["client_id"], "client-def")
        self.assertEqual(captured_creds["client_secret"], "secret-ghi")
        self.assertEqual(captured_creds["account_url"], "mystorageaccount")

    def test_create_azure_agent_app_key(self):
        response = Mock()
        response.create_or_update_agent.agent_id = "azure-ak-123"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        out = capture_function(
            self._service.create_agent,
            {
                "agent_type": REMOTE_AGENT,
                "platform": AZURE,
                "storage": AZURE_BLOB,
                "auth_type": AZURE_FUNCTION_APP_KEY,
                "endpoint": "https://my-func.azurewebsites.net/api/agent",
                "app_key": "my-app-key",
            },
        )

        self.assertIsNone(out.exception)
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("azure-ak-123", captured)

        call_args = str(self._mc_client.call_args_list[0])
        self.assertIn("app_key", call_args)

    def test_create_azure_agent_service_principal(self):
        response = Mock()
        response.create_or_update_agent.agent_id = "azure-sp-456"
        response.create_or_update_agent.validation_result.success = True
        response.create_or_update_agent.validation_result.errors = None
        response.create_or_update_agent.validation_result.warnings = None
        self._mc_client.return_value = response

        captured_creds = {}
        original_dumps = json.dumps

        def intercept_dumps(obj, **kwargs):
            if isinstance(obj, dict) and "audience" in obj:
                captured_creds.update(obj)
            return original_dumps(obj, **kwargs)

        with patch("montecarlodata.agents.agent.json.dumps", side_effect=intercept_dumps):
            out = capture_function(
                self._service.create_agent,
                {
                    "agent_type": REMOTE_AGENT,
                    "platform": AZURE,
                    "storage": AZURE_BLOB,
                    "auth_type": AZURE_FUNCTION_SERVICE_PRINCIPAL,
                    "endpoint": "https://my-func.azurewebsites.net/api/agent",
                    "sp_tenant_id": "tenant-abc",
                    "sp_client_id": "client-def",
                    "sp_client_secret": "secret-ghi",
                    "sp_audience": "api://my-func-audience",
                },
            )

        self.assertIsNone(out.exception)
        self.assertEqual(1, self._mc_client.call_count)
        captured = out.std_out.getvalue()
        self.assertIn("Agent successfully registered", captured)
        self.assertIn("azure-sp-456", captured)

        self.assertEqual(captured_creds["tenant_id"], "tenant-abc")
        self.assertEqual(captured_creds["client_id"], "client-def")
        self.assertEqual(captured_creds["client_secret"], "secret-ghi")
        self.assertEqual(captured_creds["audience"], "api://my-func-audience")
