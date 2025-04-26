import json
from datetime import datetime, timezone
from unittest import TestCase

import responses
from click.testing import CliRunner

from montecarlodata.secrets.commands import (
    create_secret,
    delete_secret,
    get_secret,
    list_secrets,
)
from montecarlodata.tools import format_date, format_datetime
from tests.test_common_user import _SAMPLE_CONFIG


class SecretsTest(TestCase):
    @responses.activate
    def test_create_secret(self):
        expires_at = datetime.now(tz=timezone.utc).isoformat()
        created_at = datetime.now(tz=timezone.utc).isoformat()
        updated_at = datetime.now(tz=timezone.utc).isoformat()
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "createAccountSecret": {
                        "secret": {
                            "name": "a-secret",
                            "scope": "global",
                            "description": "a description",
                            "expiresAt": expires_at,
                            "createdBy": "test-user_1",
                            "createdAt": created_at,
                            "updatedBy": "test-user_2",
                            "lastUpdate": updated_at,
                        },
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            create_secret,
            obj={"config": ctx},
            args=["--name", "a-secret"],
            input="secret_value",
        )

        self.assertEqual(result.output, "Secret value: \nCreated secret: 'a-secret'.\n")
        self.assertEqual(
            json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
            {
                "description": None,
                "expiresAt": None,
                "name": "a-secret",
                "scope": "global",
                "value": "secret_value",
            },
        )

    @responses.activate
    def test_get_secret_reveal(self):
        expires_at = datetime.now(timezone.utc).isoformat()
        created_at = datetime.now(timezone.utc).isoformat()
        updated_at = datetime.now(timezone.utc).isoformat()
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "getAccountSecret": {
                        "name": "a-secret",
                        "scope": "global",
                        "description": "a description",
                        "expiresAt": expires_at,
                        "createdBy": "test-user_1",
                        "createdAt": created_at,
                        "updatedBy": "test-user_2",
                        "lastUpdate": updated_at,
                        "value": "secret value",
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            get_secret,
            obj={"config": ctx},
            args=["--name", "a-secret", "--reveal"],
        )

        self.assertEqual(result.output, "secret value\n")
        self.assertEqual(
            json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
            {"name": "a-secret", "reveal": True},
        )

        @responses.activate
        def test_get_secret_no_reveal(self):
            expires_at = datetime.now(timezone.utc).isoformat()
            created_at = datetime.now(timezone.utc).isoformat()
            updated_at = datetime.now(timezone.utc).isoformat()
            responses.post(
                _SAMPLE_CONFIG.mcd_api_endpoint,
                json={
                    "data": {
                        "getAccountSecret": {
                            "name": "a-secret",
                            "scope": "global",
                            "description": "a description",
                            "expiresAt": expires_at,
                            "createdBy": "test-user_1",
                            "createdAt": created_at,
                            "updatedBy": "test-user_2",
                            "lastUpdate": updated_at,
                        },
                    }
                },
            )

            ctx = _SAMPLE_CONFIG
            runner = CliRunner()
            result = runner.invoke(
                get_secret,
                obj={"config": ctx},
                args=["--name", "a-secret"],
            )

            self.assertEqual(
                result.output,
                "Name: a-secret\n"
                "Scope: global\n"
                "Description: a description\n"
                f"Expires at: {format_date(expires_at)}\n"
                "Created by: test-user_1\n"
                f"Created at: {format_datetime(created_at)}\n"
                "Last updated by: test-user_2\n"
                f"Last updated at: {format_datetime(created_at)}\n",
            )
            self.assertEqual(
                json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
                {"name": "a-secret", "reveal": False},
            )

    @responses.activate
    def test_list_secrets(self):
        expires_at = datetime.now(timezone.utc).isoformat()
        created_at = datetime.now(timezone.utc).isoformat()
        updated_at = datetime.now(timezone.utc).isoformat()
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "getAccountSecrets": [
                        {
                            "name": "a-secret",
                            "scope": "global",
                            "description": "a description",
                            "expiresAt": expires_at,
                            "createdBy": "test-user_1",
                            "createdAt": created_at,
                            "updatedBy": "test-user_2",
                            "lastUpdate": updated_at,
                        }
                    ],
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            list_secrets,
            obj={"config": ctx},
        )

        self.assertEqual(
            result.output,
            "╒══════════╤═════════╤═══════════════╤══════════════╤══════════════╤═════════════════════╤═══════════════════╤═════════════════════╕\n"
            "│ Name     │ Scope   │ Description   │ Expires at   │ Created by   │ Created at          │ Last updated by   │ Last updated at     │\n"
            "╞══════════╪═════════╪═══════════════╪══════════════╪══════════════╪═════════════════════╪═══════════════════╪═════════════════════╡\n"
            f"│ a-secret │ global  │ a description │ {format_date(expires_at)}   │ test-user_1  │ {format_datetime(created_at)} │ test-user_2       │ {format_datetime(created_at)} │\n"
            "╘══════════╧═════════╧═══════════════╧══════════════╧══════════════╧═════════════════════╧═══════════════════╧═════════════════════╛\n",
        )
        self.assertEqual(
            json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
            None,
        )

    @responses.activate
    def test_delete_secret(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "deleteAccountSecret": {
                        "deleted": True,
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(delete_secret, obj={"config": ctx}, args=["--name", "a-secret"])

        self.assertEqual(result.output, "Deleted secret: 'a-secret'.\n")
        self.assertEqual(
            json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
            {"name": "a-secret"},
        )

    @responses.activate
    def test_delete_secret_not_found(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "deleteAccountSecret": {
                        "deleted": False,
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(delete_secret, obj={"config": ctx}, args=["--name", "a-secret"])

        self.assertEqual(result.output, "Secret 'a-secret' was not found.\n")
        self.assertEqual(
            json.loads(responses.calls[0].request.body.decode("utf8"))["variables"],
            {"name": "a-secret"},
        )
