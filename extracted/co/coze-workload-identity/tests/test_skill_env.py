"""Tests for automatic skill environment variable loading."""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from coze_workload_identity import Client
from coze_workload_identity._debug import _reset_coze_debug_for_tests
from coze_workload_identity.env_keys import COZE_SKILL_ENV_ENDPOINT
from coze_workload_identity.skill_env import SkillEnvAPIError, load_skill_env
from coze_workload_identity.skill_env import _reset_skill_env_for_tests


class TestSkillEnv(unittest.TestCase):
    """Test cases for skill environment discovery and injection."""

    def setUp(self):
        _reset_skill_env_for_tests()
        _reset_coze_debug_for_tests()

    def tearDown(self):
        for key in [
            COZE_SKILL_ENV_ENDPOINT,
            "agent_id",
            "skill_id",
            "pat_token",
            "DATABASE_URL",
            "COZE_SKILL_PROXY_DOMAIN",
            "identity_ticket",
            "IDENTITY_TICKET",
            "COZE_OUTBOUND_AUTH_PROXY",
            "COZE_OUTBOUND_AUTH_PROXY_CA",
            "COZE_OUTBOUND_AUTH_PROXY_CA_PATH",
            "COZE_SKILL_ASSISTANT_TOKEN",
            "COZE_TAVILY_KEY_7649677867541872686",
            "COZE_WORKLOAD_IDENTITY_CLIENT_ID",
            "COZE_WORKLOAD_IDENTITY_CLIENT_SECRET",
            "COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT",
            "COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT",
        ]:
            os.environ.pop(key, None)
        _reset_skill_env_for_tests()
        _reset_coze_debug_for_tests()

    def test_load_skill_env_sets_env_from_matching_agent_config(self):
        """Load env vars for the skill matching the source path relPath."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "agentId": "7646332931975381289",
                "patToken": "pat_from_config",
                "identity_ticket": "identity_ticket_from_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            os.environ[COZE_SKILL_ENV_ENDPOINT] = "https://env.example.com/skill-env"
            os.environ["agent_id"] = "old_agent_id"
            os.environ["skill_id"] = "old_skill_id"
            os.environ["pat_token"] = "old_pat_token"

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {
                    "envs": {
                        "DATABASE_URL": "postgres://example",
                        "COZE_SKILL_PROXY_DOMAIN": "https://proxy.example.com:443",
                        "identity_ticket": "ticket_123",
                    }
                },
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ) as mock_post:
                loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            self.assertEqual(os.environ["DATABASE_URL"], "postgres://example")
            self.assertEqual(
                os.environ["COZE_SKILL_PROXY_DOMAIN"],
                "https://proxy.example.com:443",
            )
            self.assertEqual(
                os.environ["identity_ticket"],
                "ticket_123",
            )
            self.assertEqual(os.environ["agent_id"], "7646332931975381289")
            self.assertEqual(os.environ["skill_id"], "skill_weather")
            self.assertEqual(os.environ["pat_token"], "pat_from_config")
            self.assertEqual(
                os.environ["IDENTITY_TICKET"],
                "ticket_123",
            )

            mock_post.assert_called_once()
            call_args = mock_post.call_args
            self.assertEqual(call_args[0][0], "https://env.example.com/skill-env")
            self.assertEqual(
                call_args[1]["headers"]["Authorization"],
                "Bearer pat_from_config",
            )
            self.assertEqual(call_args[1]["timeout"], 10)
            self.assertNotIn("x-tt-env", call_args[1]["headers"])
            self.assertNotIn("x-use-ppe", call_args[1]["headers"])
            self.assertEqual(
                call_args[1]["json"],
                {
                    "agent_id": 7646332931975381289,
                    "skill_id": "skill_weather",
                },
            )

    def test_load_skill_env_reads_identity_ticket_from_ticket_file(self):
        """A /source/ticket.json style file overrides config and env tickets."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")
            ticket_file = Path(tmp_dir) / "ticket.json"
            ticket_file.write_text(
                json.dumps({"IDENTITY_TICKET": "identity_ticket_from_file"}),
                encoding="utf-8",
            )

            config = {
                "patToken": "pat_from_config",
                "identity_ticket": "identity_ticket_from_config",
                "identityTicket": "identity_ticket_from_camel_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )
            os.environ["identity_ticket"] = "existing_identity_ticket"
            os.environ["IDENTITY_TICKET"] = "existing_upper_identity_ticket"

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {"DATABASE_URL": "postgres://example"},
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.TICKET_FILE_PATH",
                ticket_file,
            ), patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ) as mock_post:
                loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            self.assertEqual(os.environ["identity_ticket"], "identity_ticket_from_file")
            self.assertEqual(os.environ["IDENTITY_TICKET"], "identity_ticket_from_file")
            self.assertEqual(
                mock_post.call_args.kwargs["json"],
                {
                    "agent_id": 7646332931975381289,
                    "skill_id": "skill_weather",
                    "identity_ticket": "identity_ticket_from_file",
                },
            )

    def test_load_skill_env_matches_skill_assistant_scripts_path(self):
        """Nested skill scripts match the installed skill relPath."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7654474657403486498"
            )
            skill_dir = (
                agent_dir
                / "workspace"
                / ".claude"
                / "skills"
                / "skill-assistant"
                / "scripts"
            )
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "get_agent.py"
            source_file.write_text("# fake skill-assistant script\n", encoding="utf-8")

            config = {
                "agentId": "7654474657403486498",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "10086",
                        "skillName": "skill-assistant",
                        "relPath": ".claude/skills/skill-assistant",
                    },
                    {
                        "skillId": "7649677867541872686",
                        "skillName": "tavily-search",
                        "relPath": ".claude/skills/tavily-search",
                    },
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {"COZE_SKILL_ASSISTANT_TOKEN": "assistant-token"},
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ) as mock_post:
                loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            self.assertEqual(
                os.environ["COZE_SKILL_ASSISTANT_TOKEN"],
                "assistant-token",
            )
            self.assertEqual(
                mock_post.call_args.kwargs["json"],
                {
                    "agent_id": 7654474657403486498,
                    "skill_id": 10086,
                },
            )

    def test_load_skill_env_sets_agent_metadata_without_matching_skill(self):
        """Agent metadata is set even when no skill relPath matches."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7654474657403486498"
            )
            source_file = agent_dir / "workspace" / "scripts" / "tool.py"
            source_file.parent.mkdir(parents=True)
            source_file.write_text("# unmatched script\n", encoding="utf-8")

            config = {
                "agentId": "7654474657403486498",
                "patToken": "pat_from_config",
                "identity_ticket": "identity_ticket_from_config",
                "skills": [
                    {
                        "skillId": "10086",
                        "skillName": "skill-assistant",
                        "relPath": ".claude/skills/skill-assistant",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )
            os.environ["agent_id"] = "old_agent_id"
            os.environ["pat_token"] = "old_pat_token"
            os.environ["skill_id"] = "old_skill_id"
            os.environ["identity_ticket"] = "existing_identity_ticket"

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
            ) as mock_post:
                loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            self.assertEqual(os.environ["agent_id"], "7654474657403486498")
            self.assertEqual(os.environ["pat_token"], "pat_from_config")
            self.assertNotIn("skill_id", os.environ)
            self.assertEqual(os.environ["identity_ticket"], "existing_identity_ticket")
            self.assertNotIn("IDENTITY_TICKET", os.environ)
            mock_post.assert_not_called()

    def test_load_skill_env_preserves_existing_proxy_and_prefers_returned_ca_content(self):
        """Default API preserves existing proxy and prefers returned CA content."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7649683932442820891"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "agentId": "7649683932442820891",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "7649677867541872686",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            os.environ["COZE_OUTBOUND_AUTH_PROXY"] = "http://existing.proxy:3000"

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {
                    "COZE_OUTBOUND_AUTH_PROXY": "http://remote.proxy:3000",
                    "COZE_OUTBOUND_AUTH_PROXY_CA": "remote ca content",
                    "COZE_OUTBOUND_AUTH_PROXY_CA_PATH": "/etc/coze-space-sandbox/auth-proxy-ca.crt",
                    "COZE_TAVILY_KEY_7649677867541872686": "COZE_CRED_DUMMY_7650076051430834202",
                    "identity_ticket": "identity_ticket_from_response",
                },
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ) as mock_post:
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            self.assertEqual(
                os.environ["COZE_OUTBOUND_AUTH_PROXY"],
                "http://existing.proxy:3000",
            )
            self.assertEqual(
                os.environ["COZE_OUTBOUND_AUTH_PROXY_CA"],
                "remote ca content",
            )
            self.assertNotIn("COZE_OUTBOUND_AUTH_PROXY_CA_PATH", os.environ)
            self.assertEqual(
                os.environ["COZE_TAVILY_KEY_7649677867541872686"],
                "COZE_CRED_DUMMY_7650076051430834202",
            )
            self.assertEqual(
                os.environ["identity_ticket"],
                "identity_ticket_from_response",
            )
            self.assertEqual(
                os.environ["IDENTITY_TICKET"],
                "identity_ticket_from_response",
            )

            mock_post.assert_called_once()
            call_args = mock_post.call_args
            self.assertEqual(
                call_args[0][0],
                "https://www.coze.cn/api/coze_claw/skill/get_skill_envs",
            )
            self.assertEqual(
                call_args[1]["headers"]["Authorization"],
                "Bearer pat_from_config",
            )
            self.assertNotIn("x-tt-env", call_args[1]["headers"])
            self.assertNotIn("x-use-ppe", call_args[1]["headers"])
            self.assertEqual(
                call_args[1]["json"],
                {
                    "agent_id": 7649683932442820891,
                    "skill_id": 7649677867541872686,
                },
            )
            console_output = stdout.getvalue()
            self.assertEqual(console_output, "")

    def test_load_skill_env_prints_request_and_response_with_debug_arg(self):
        """Debug output is printed only when --coze-debug is present."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7649683932442820891"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "agentId": "7649683932442820891",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "7649677867541872686",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {
                    "COZE_TAVILY_KEY_7649677867541872686": "tavily-secret",
                },
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch("sys.argv", ["tool.py", "--coze-debug", "query"]):
                _reset_coze_debug_for_tests()
                with patch(
                    "coze_workload_identity.skill_env.requests.Session.post",
                    return_value=response,
                ):
                    stdout = io.StringIO()
                    with redirect_stdout(stdout):
                        loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertTrue(loaded)
            console_output = stdout.getvalue()
            self.assertIn("Skill environment request", console_output)
            self.assertIn("7649683932442820891", console_output)
            self.assertIn("7649677867541872686", console_output)
            self.assertIn("Bearer pat_from_config", console_output)
            self.assertIn("Skill environment response", console_output)
            self.assertIn("COZE_TAVILY_KEY_7649677867541872686", console_output)

    def test_load_skill_env_logs_when_endpoint_returns_no_env_data(self):
        """A successful response without env data is only logged."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "agentId": "7646332931975381289",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            os.environ[COZE_SKILL_ENV_ENDPOINT] = "https://env.example.com/skill-env"

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {},
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ):
                with self.assertLogs(
                    "coze_workload_identity.skill_env", level="WARNING"
                ) as logs:
                    loaded = load_skill_env(source_path=str(source_file), force=True)

            self.assertFalse(loaded)
            self.assertIn("No skill environment variables", "\n".join(logs.output))

    def test_load_skill_env_raises_when_endpoint_returns_error_code(self):
        """A non-zero get_skill_envs BaseResp StatusCode blocks downstream requests."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {},
                "BaseResp": {
                    "StatusCode": 40001,
                    "StatusMessage": "skill env failed",
                    "Extra": {"log_id": "log_123"},
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ):
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    with self.assertRaises(SkillEnvAPIError) as cm:
                        load_skill_env(source_path=str(source_file), force=True)

            self.assertIn('"StatusCode": 40001', str(cm.exception))
            self.assertIn('"StatusMessage": "skill env failed"', str(cm.exception))

    def test_load_skill_env_retries_after_no_matching_context(self):
        """A non-Coze early import does not block a later skill-context load."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            early_source_file = Path(tmp_dir) / "ordinary_project" / "main.py"
            early_source_file.parent.mkdir()
            early_source_file.write_text("# non skill module\n", encoding="utf-8")

            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            config = {
                "agentId": "7646332931975381289",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {"DATABASE_URL": "postgres://example"},
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ) as mock_post:
                early_loaded = load_skill_env(source_path=str(early_source_file))
                loaded = load_skill_env(source_path=str(source_file))

            self.assertFalse(early_loaded)
            self.assertTrue(loaded)
            self.assertEqual(os.environ["DATABASE_URL"], "postgres://example")
            mock_post.assert_called_once()

    def test_requests_session_loads_skill_env_before_proxy_configuration(self):
        """Wrapped requests session loads skill env before reading proxy env."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7646332931975381289"
            )
            skill_dir = agent_dir / "skills" / "weather_skill"
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "package" / "tool.py"
            source_file.parent.mkdir()
            source_file.write_text("# fake tool module\n", encoding="utf-8")

            ca_file = Path(tmp_dir) / "ca.pem"
            ca_file.write_text("fake ca", encoding="utf-8")

            config = {
                "agentId": "7646332931975381289",
                "patToken": "pat_from_config",
                "skills": [
                    {
                        "skillId": "skill_weather",
                        "skillName": "weather_skill",
                        "relPath": "skills/weather_skill",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            os.environ[COZE_SKILL_ENV_ENDPOINT] = "https://env.example.com/skill-env"

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {
                    "envs": {
                        "COZE_SKILL_PROXY_DOMAIN": "https://proxy.example.com:443",
                        "identity_ticket": "ticket_123",
                        "COZE_OUTBOUND_AUTH_PROXY_CA_PATH": str(ca_file),
                    }
                },
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            code = (
                "from coze_workload_identity import requests as sdk_requests\n"
                "import importlib\n"
                "importlib.reload(sdk_requests)\n"
                "session = sdk_requests.session()\n"
            )

            namespace = {}
            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ):
                exec(compile(code, str(source_file), "exec"), namespace)

            session = namespace["session"]
            self.assertEqual(
                session.proxies["https"],
                "https://space:ticket_123@proxy.example.com:443",
            )
            self.assertEqual(session.verify, str(ca_file))
            self.assertIsNone(session.cert)

    def test_requests_import_loads_skill_env_before_user_reads_env(self):
        """Importing wrapped requests loads env before user code reads os.environ."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            agent_dir = (
                Path(tmp_dir)
                / ".coze"
                / "agents"
                / "7649684396785844489"
            )
            skill_dir = (
                agent_dir
                / "workspace"
                / ".claude"
                / "skills"
                / "tavily-search"
            )
            skill_dir.mkdir(parents=True)
            source_file = skill_dir / "main.py"
            source_file.write_text("# fake tavily tool module\n", encoding="utf-8")

            config = {
                "agentId": "7649684396785844489",
                "patToken": "sat_full_pat_token",
                "skills": [
                    {
                        "skillId": "7649677867541872686",
                        "skillName": "tavily-search",
                        "relPath": ".claude/skills/tavily-search",
                    }
                ],
            }
            (agent_dir / "config.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "data": {
                    "COZE_TAVILY_KEY_7649677867541872686": "tavily-secret",
                },
                "BaseResp": {
                    "StatusCode": 0,
                    "StatusMessage": "",
                },
            }

            code = (
                "import importlib\n"
                "import os\n"
                "from coze_workload_identity import requests as sdk_requests\n"
                "importlib.reload(sdk_requests)\n"
                "credential = os.getenv('COZE_TAVILY_KEY_7649677867541872686')\n"
            )
            namespace = {}
            with patch(
                "coze_workload_identity.skill_env.requests.Session.post",
                return_value=response,
            ):
                exec(compile(code, str(source_file), "exec"), namespace)

            self.assertEqual(namespace["credential"], "tavily-secret")

    @patch.dict(os.environ, {
        "COZE_WORKLOAD_IDENTITY_CLIENT_ID": "test_client_id",
        "COZE_WORKLOAD_IDENTITY_CLIENT_SECRET": "test_client_secret",
        "COZE_WORKLOAD_IDENTITY_TOKEN_ENDPOINT": "https://auth.example.com/token",
        "COZE_WORKLOAD_ACCESS_TOKEN_ENDPOINT": "https://auth.example.com/access-token",
    })
    @patch("coze_workload_identity.client.ensure_skill_env_loaded")
    def test_client_initialization_loads_skill_env(self, mock_load):
        """Client initialization invokes the shared skill env loader."""
        client = Client()

        mock_load.assert_called_once()
        client.close()


if __name__ == "__main__":
    unittest.main()
