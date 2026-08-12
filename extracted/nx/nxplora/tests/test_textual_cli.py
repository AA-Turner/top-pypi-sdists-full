import contextlib
import importlib
import importlib.util
import io
import logging
import os
from pathlib import Path
import re
import sys
import tempfile
import types
import unittest
from unittest import mock

import chat_ui
import nx_cli
import nx_data
import nx_rag
import nx_slash_menu
import nx_storage
import welcome
import nx_terminal
from textual.widgets import Input, Static


class _TTYStringIO(io.StringIO):
    def fileno(self):
        return 1


def _fake_nvidia_env():
    return {
        "NVIDIA_KEY_1": "key-1",
        "NVIDIA_KEY_2": "key-2",
        "NVIDIA_KEY_3": "key-3",
        "NVIDIA_KEY_4": "key-4",
        "NVIDIA_KEY_5": "key-5",
        "NVIDIA_KEY_6": "key-6",
    }


def _reload_module(name):
    sys.modules.pop(name, None)
    return importlib.import_module(name)


class RunWelcomeTests(unittest.TestCase):
    def test_run_welcome_debug_output_includes_runtime_details(self):
        fake_welcome = types.ModuleType("welcome")

        class BrokenWelcome:
            def __init__(self, cfg=None):
                raise RuntimeError("boom")

        fake_welcome.NXWelcome = BrokenWelcome

        stderr = io.StringIO()
        with mock.patch.dict(sys.modules, {"welcome": fake_welcome}):
            with mock.patch.dict(os.environ, {"NX_DEBUG_WELCOME": "1"}, clear=False):
                with mock.patch.object(nx_cli, "show_welcome"):
                    with contextlib.redirect_stderr(stderr):
                        choice = nx_cli.run_welcome(cfg={"account": "demo@nexplora.ai"})

        self.assertIsNone(choice)
        output = stderr.getvalue()
        self.assertIn("RuntimeError: boom", output)
        self.assertIn(sys.executable, output)
        self.assertIn("textual=", output)

    def test_run_welcome_runs_textual_inline(self):
        captured = {}
        fake_welcome = types.ModuleType("welcome")

        class FakeWelcome:
            def __init__(self, cfg=None):
                self.choice = "oauth"

            def run(self, **kwargs):
                captured["run"] = kwargs

        fake_welcome.NXWelcome = FakeWelcome

        with mock.patch.object(nx_cli, "_load_sibling_module", return_value=fake_welcome):
            choice = nx_cli.run_welcome(cfg={"account": "demo@nexplora.ai"})

        self.assertEqual(choice, "oauth")
        self.assertEqual(captured["run"], {"inline": True})


class ObfuscationTests(unittest.TestCase):
    def test_sensitive_constants_are_obfuscated_in_runtime_modules(self):
        nx_obfuscate = _reload_module("nx_obfuscate")

        # DeepInfra catalog IDs (case-sensitive). Used when DeepInfra resolves.
        self.assertEqual(nx_obfuscate.M["kimi"], "moonshotai/Kimi-K2.6")
        self.assertEqual(nx_obfuscate.M["dsv4pro"], "deepseek-ai/DeepSeek-V4-Pro")
        self.assertEqual(nx_obfuscate.M["dsv4flash"], "deepseek-ai/DeepSeek-V4-Flash")
        self.assertEqual(nx_obfuscate.M["glm52"], "zai-org/GLM-5.2")
        self.assertEqual(nx_obfuscate.M["kimi_code"], "moonshotai/Kimi-K2.7-Code")
        self.assertEqual(nx_obfuscate.M["llama8b"], "meta-llama/Meta-Llama-3.1-8B-Instruct")
        self.assertEqual(nx_obfuscate.M["nemotron"], "nvidia/llama-3.3-nemotron-super-49b-v1")

        # Fireworks catalog IDs (p-notation, verified live 2026-06-22).
        self.assertEqual(nx_obfuscate.FW["fast"], "accounts/fireworks/models/deepseek-v4-flash")
        self.assertEqual(nx_obfuscate.FW["pro"], "accounts/fireworks/models/deepseek-v4-pro")
        self.assertEqual(nx_obfuscate.FW["kimi_code"], "accounts/fireworks/models/kimi-k2p7-code")
        self.assertEqual(nx_obfuscate.FW["kimi"], "accounts/fireworks/models/kimi-k2p6")
        self.assertEqual(nx_obfuscate.FW["glm"], "accounts/fireworks/models/glm-5p2")

        self.assertEqual(nx_obfuscate.URLS["nvidia"], "https://integrate.api.nvidia.com/v1")
        self.assertEqual(nx_obfuscate.URLS["deepinfra"], "https://api.deepinfra.com/v1/openai")
        self.assertEqual(nx_obfuscate.SB["nx_url"], "https://tiyoncvmleryjmoftdya.supabase.co")
        self.assertEqual(nx_obfuscate.HUB["default"], "http://localhost:37373")
        self.assertEqual(nx_obfuscate.AUTH["base"], "https://api.nexplora.ai")
        # ── COMPARED AGAINST setup.py, NOT THE INSTALLED PACKAGE ──────────────────────────────
        # This asserted ID["version"] == nx_cli.VERSION, and nx_cli.VERSION is the version of the
        # INSTALLED nxplora wheel. Those are equal only when the machine happens to have the
        # current release installed — never true on a dev box mid-release, so the assertion could
        # not hold where it runs. It had drifted forty releases (0.15.221 vs 0.15.261) unnoticed
        # inside a suite whose collection was broken, which is how a guard stops guarding.
        #
        # setup.py is the actual source of truth the bundled literal must track, it is present
        # wherever these tests run, and comparing to it holds in dev AND in a release.
        setup_py = (Path(__file__).resolve().parents[1] / "setup.py").read_text(encoding="utf-8")
        declared = re.search(r'version="([^"]+)"', setup_py)
        self.assertIsNotNone(declared, "setup.py must declare a version")
        self.assertEqual(
            nx_obfuscate.ID["version"],
            declared.group(1),
            "the bundled fallback version must track setup.py — bump both together",
        )

        root = Path(__file__).resolve().parents[1]
        targets = [
            root / "nx_cli.py",
            root / "nx_routing.py",
            root / "nx_storage.py",
            root / "nx_data.py",
            root / "nx_mcp_hub.py",
            root / "nx_mcp_manager.py",
            root / "nx_key_pool.py",
        ]
        forbidden_literals = [
            # DeepInfra catalog IDs
            "moonshotai/Kimi-K2.6",
            "deepseek-ai/DeepSeek-V4-Pro",
            "deepseek-ai/DeepSeek-V4-Flash",
            "zai-org/GLM-5.2",
            "moonshotai/Kimi-K2.7-Code",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "nvidia/llama-3.3-nemotron-super-49b-v1",
            # Fireworks catalog IDs
            "accounts/fireworks/models/deepseek-v4-flash",
            "accounts/fireworks/models/deepseek-v4-pro",
            "accounts/fireworks/models/kimi-k2p7-code",
            "accounts/fireworks/models/kimi-k2p6",
            "accounts/fireworks/models/glm-5p2",
            # Provider base URLs + Keychain names
            "https://integrate.api.nvidia.com/v1",
            "https://api.deepinfra.com/v1/openai",
            "https://api.fireworks.ai/inference/v1",
            "https://tiyoncvmleryjmoftdya.supabase.co",
            "http://localhost:37373",
            "https://ravitemer.github.io/mcp-registry/registry.json",
            "https://api.nexplora.ai",
            "nvidia-key-",
            "deepinfra-key",
            "fireworks-key",
        ]

        for path in targets:
            source = path.read_text(encoding="utf-8")
            for literal in forbidden_literals:
                with self.subTest(path=path.name, literal=literal):
                    self.assertNotIn(literal, source)


class ReplTests(unittest.TestCase):
    def setUp(self):
        # Hermeticity: force the soft daily-quota gate open for every REPL test.
        # It reads ~/.nx/usage.json and silently `continue`s the turn at the
        # cap — without this, these tests pass or fail based on real local
        # usage state (e.g. after a day of heavy CLI use the counter hits the
        # cap and every REPL turn is skipped). Quota behaviour is covered by
        # dedicated quota tests.
        _qp = mock.patch.object(nx_cli, "_quota_check_and_warn", return_value=True)
        _qp.start()
        self.addCleanup(_qp.stop)

    def _run_repl(self, inputs, cfg=None):
        stdout = io.StringIO()
        with mock.patch.object(nx_cli, "slash_input", side_effect=inputs) as mock_input:
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    # Hermeticity: the soft daily-quota gate reads ~/.nx/usage.json
                    # and `continue`s the turn when the cap is hit. Without this
                    # mock the REPL tests pass/fail based on real local usage
                    # state. Force the gate open so the loop always processes the
                    # input. (Quota behaviour itself is covered separately.)
                    with mock.patch.object(nx_cli, "_quota_check_and_warn", return_value=True):
                        with contextlib.redirect_stdout(stdout):
                            nx_cli.run_nx_repl(cfg or {"account": "demo@nexplora.ai"})
        return stdout.getvalue(), mock_input

    def test_repl_prints_header_and_uses_world_prompt(self):
        output, mock_input = self._run_repl(["/exit"])
        self.assertIn("NX", output)
        # Email is masked on-screen now; full address must not appear.
        self.assertIn("d…@nexplora.ai", output)
        self.assertNotIn("demo@nexplora.ai", output)
        # `active_effort` joined this call when the effort selector shipped (nx_cli.py:21885).
        # The assertion is exact on purpose — it is how a silently-dropped prompt field gets
        # caught — so it moves WITH the signature rather than being loosened to a subset check.
        self.assertEqual(mock_input.call_args_list[0].kwargs, {"world": "cowork", "active_skills": [], "active_mode": "", "active_effort": ""})

    def test_repl_logs_route_errors_before_streaming(self):
        stdout = io.StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(nx_cli, "slash_input", side_effect=["hello", "/exit"]):
                with mock.patch.object(nx_cli, "init_readline"):
                    with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                        with mock.patch.object(nx_cli, "resolve_route_result", side_effect=RuntimeError("route exploded")):
                            with mock.patch.object(nx_cli.Path, "home", return_value=Path(tmpdir)):
                                with contextlib.redirect_stdout(stdout):
                                    nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

            debug_path = Path(tmpdir) / ".nx" / "logs" / "debug.log"
            debug_text = debug_path.read_text(encoding="utf-8") if debug_path.exists() else ""

        output = stdout.getvalue()
        self.assertIn("Something went wrong. If this persists contact support.", output)
        self.assertIn("=== ROUTE ERROR ===", debug_text)
        self.assertIn("RuntimeError: route exploded", debug_text)

    def test_repl_handles_help_and_exit_commands(self):
        output, _ = self._run_repl(["/help", "/exit"])
        # Header line is "NX — commands" (lower-case) in the current layout.
        self.assertIn("commands", output)
        self.assertIn("/exit", output)
        self.assertIn("world", output)
        self.assertIn("/audit", output)
        self.assertIn("/install", output)
        self.assertIn("/auth", output)
        self.assertIn("/integrations", output)
        self.assertIn("/tools", output)
        # The integrations entry surfaces with its current one-line description.
        self.assertIn("Browse & connect integrations", output)
        self.assertNotIn("/connect  connect a live MCP service for this user", output)
        # /keys and /vpn are surfaced in the ACCOUNT group of the current help.
        self.assertIn("/keys", output)
        self.assertIn("/vpn", output)

    def test_repl_world_command_without_args_lists_worlds(self):
        # Bare "/world" (no name) invokes the interactive grouped picker
        # (nx_slash_menu.run_world_menu) — same pattern as /integrations's
        # run_integrations_menu. Mock it directly rather than expecting plain
        # text output; the real interactive UI is covered by nx_slash_menu's
        # own tests.
        with mock.patch("nx_slash_menu.run_world_menu", return_value="finance") as picker:
            output, mock_input = self._run_repl(["/world", "/exit"])
        picker.assert_called_once()
        self.assertEqual(mock_input.call_args_list[1].kwargs["world"], "finance")

    def test_repl_world_command_switches_world(self):
        output, mock_input = self._run_repl(["/world finance", "/world", "/exit"])
        self.assertEqual(mock_input.call_args_list[1].kwargs, {"world": "finance", "active_skills": [], "active_mode": "", "active_effort": ""})

    def test_repl_activates_skill_and_applies_it_to_next_turn_only(self):
        cfg = {"account": "demo@nexplora.ai"}
        captured_messages = []

        def fake_stream_chat(messages, cfg, api_key=None, model=None, provider=None, extra_body=None, secondary_model="", tools=None):
            del cfg, api_key, model, provider, extra_body
            captured_messages.append(messages)
            yield "Hello from NX"

        route_result = types.SimpleNamespace(
            world="cowork",
            model="deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct",
            voice="PEER",
            provider="deepinfra",
            api_key="test-key",
            extra_body={},
        )

        stdout = io.StringIO()
        with mock.patch.object(nx_cli, "slash_input", side_effect=["$cold_outreach", "Draft a sequence", "Second turn", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli, "stream_chat", new=fake_stream_chat):
                        with mock.patch.object(nx_cli, "resolve_route_result", return_value=route_result):
                            with contextlib.redirect_stdout(stdout):
                                nx_cli.run_nx_repl(cfg)

        self.assertEqual(cfg["_active_skill"], "cold outreach")
        self.assertEqual(cfg["_active_skills_display"], [])
        self.assertEqual(len(captured_messages), 2)
        # 0.3.91+ uses per-skill overlays — the activation marker is the skill
        # name in the system prompt, not a generic "activated the X skill" line.
        self.assertIn("'cold outreach' skill", captured_messages[0][0]["content"])
        self.assertNotIn("'cold outreach' skill", captured_messages[1][0]["content"])

    def test_repl_keyboard_interrupt_cancels_line_not_session(self):
        # A single Ctrl-C at the prompt cancels the CURRENT line and re-prompts (standard REPL UX,
        # like python/bash) — it does NOT quit the session; an explicit /exit does. So the loop
        # keeps going after the interrupt and exits cleanly on the follow-up /exit.
        output, _ = self._run_repl([KeyboardInterrupt(), "/exit"])
        self.assertIn("NX", output)

    def test_repl_does_not_initialize_rag_before_first_message(self):
        with mock.patch.object(nx_cli, "init_rag") as init_rag:
            self._run_repl(["/exit"])

        init_rag.assert_not_called()

    def test_repl_initializes_rag_on_first_message(self):
        fake_rag = mock.Mock()
        fake_rag.query.return_value = []

        def fake_stream_chat(messages, cfg, api_key=None, model=None, provider=None, extra_body=None, secondary_model="", tools=None):
            del messages, cfg, api_key, model, provider, extra_body
            yield "Hello from NX"

        with mock.patch.object(nx_cli, "init_rag", return_value=fake_rag) as init_rag:
            with mock.patch.object(nx_cli, "stream_chat", new=fake_stream_chat):
                with mock.patch.object(
                    nx_cli,
                    "resolve_route_result",
                    return_value=types.SimpleNamespace(
                        world="cowork",
                        model="deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct",
                        voice="PEER",
                        provider="deepinfra",
                        api_key="test-key",
                        extra_body={},
                    ),
                ):
                    self._run_repl(["hello", "/exit"], cfg={"account": "demo@nexplora.ai", "user_id": "user-1"})

        # init_rag now also receives the session JWT so the RAG Supabase client
        # is RLS-scoped (no service-role bypass). cfg has no token here → "".
        init_rag.assert_called_once_with("user-1", world="cowork", user_jwt="")

    def test_repl_saves_user_and_assistant_messages(self):
        saved = []

        def fake_stream_chat(messages, cfg, api_key=None, model=None, provider=None, extra_body=None, secondary_model="", tools=None):
            del api_key, model, provider, extra_body
            cfg["_last_model_used"] = "deepseek-ai/deepseek-r1"
            cfg["_last_provider"] = "deepinfra"
            yield "Hello from NX"

        def fake_save_message(*args, **kwargs):
            saved.append(kwargs)

        stdout = io.StringIO()
        with mock.patch.object(nx_cli, "slash_input", side_effect=["hello", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli, "save_config"):
                        with mock.patch.object(nx_cli, "stream_chat", new=fake_stream_chat):
                            with mock.patch.object(
                                nx_cli,
                                "resolve_route_result",
                                return_value=types.SimpleNamespace(
                                    world="cowork",
                                    model="deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct",
                                    voice="PEER",
                                    provider="deepinfra",
                                    api_key="test-key",
                                    extra_body={},
                                ),
                            ):
                                with mock.patch.object(nx_cli, "_data_client", return_value=object()):
                                    with mock.patch.object(nx_cli.nx_data, "upsert_user", return_value="user-1"):
                                        with mock.patch.object(nx_cli.nx_data, "create_session", return_value="session-1"):
                                            with mock.patch.object(nx_cli.nx_data, "save_message", side_effect=fake_save_message):
                                                with mock.patch.object(nx_cli.nx_data, "end_session"):
                                                    with contextlib.redirect_stdout(stdout):
                                                        nx_cli.run_nx_repl(
                                                            {
                                                                "account": "demo@nexplora.ai",
                                                                "model": "deepseek-ai/deepseek-r1",
                                                            }
                                                        )

        self.assertEqual(len(saved), 2)
        self.assertEqual(saved[0]["role"], "user")
        self.assertEqual(saved[1]["role"], "assistant")
        self.assertEqual(saved[0]["world"], "cowork")
        self.assertEqual(saved[1]["world"], "cowork")
        self.assertEqual(saved[0]["model"], "deepinfra/meta-llama/Meta-Llama-3.1-70B-Instruct")
        self.assertEqual(saved[1]["model"], "deepseek-ai/deepseek-r1")
        self.assertEqual(saved[0]["provider"], "deepinfra")
        self.assertEqual(saved[1]["provider"], "deepinfra")

    def test_repl_connect_command_adds_server_and_reports_tool_count(self):
        stdout = io.StringIO()
        tool_responses = [
            [],
            [
                {"server": "github", "name": "search_repositories"},
                {"server": "github", "name": "create_or_update_file"},
            ],
        ]

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/connect github ghp_test_123", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli.time, "sleep"):
                        with mock.patch("nx_mcp_manager.start_user_hub", return_value={"status": "ready", "hub_alive": True}):
                            with mock.patch(
                                "nx_mcp_manager.add_server_for_user",
                                return_value={"success": True, "status": "connected", "tools_count": 2},
                            ):
                                with mock.patch(
                                    "nx_mcp_manager.get_user_tools",
                                    side_effect=tool_responses,
                                ):
                                    with contextlib.redirect_stdout(stdout):
                                        nx_cli.run_nx_repl(
                                            {
                                                "account": "demo@nexplora.ai",
                                                "nx_user_id": "user-1",
                                                "user_id": "user-1",
                                            }
                                        )

        output = stdout.getvalue()
        self.assertIn("Connecting github", output)
        self.assertIn("github connected", output)
        self.assertIn("2 tools available", output)

    def test_repl_integrations_connect_routes_to_connect_handler(self):
        stdout = io.StringIO()
        tool_responses = [
            [],
            [
                {"server": "github", "name": "search_repositories"},
                {"server": "github", "name": "create_or_update_file"},
            ],
        ]

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/integrations connect github ghp_test_123", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli.time, "sleep"):
                        with mock.patch("nx_mcp_manager.start_user_hub", return_value={"status": "ready", "hub_alive": True}):
                            with mock.patch(
                                "nx_mcp_manager.add_server_for_user",
                                return_value={"success": True, "status": "connected", "tools_count": 2},
                            ):
                                with mock.patch(
                                    "nx_mcp_manager.get_user_tools",
                                    side_effect=tool_responses,
                                ):
                                    with contextlib.redirect_stdout(stdout):
                                        nx_cli.run_nx_repl(
                                            {
                                                "account": "demo@nexplora.ai",
                                                "nx_user_id": "user-1",
                                                "user_id": "user-1",
                                            }
                                        )

        output = stdout.getvalue()
        self.assertIn("Connecting github", output)
        self.assertIn("github connected", output)
        self.assertIn("2 tools available", output)

    def test_repl_integrations_uses_interactive_menu_selection_to_connect(self):
        # /integrations → pick klaviyo → confirm → the generic remote-MCP connect runs.
        # klaviyo is an OAuth ("sign in") server, so the connect routes through
        # nx_mcp_oauth.connect (browser flow) — mocked here to succeed offline. (The old
        # nx_mcp_manager.add_server_for_user hub path was replaced by nx_mcp_oauth.)
        stdout = io.StringIO()
        with mock.patch.object(nx_cli, "slash_input", side_effect=["/integrations", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli.time, "sleep"):
                        with mock.patch("nx_slash_menu.run_integrations_menu", return_value="klaviyo") as picker:
                            with mock.patch("builtins.input", return_value="y") as confirm:
                                with mock.patch(
                                    "nx_mcp_oauth.connect",
                                    return_value={"ok": True, "name": "Klaviyo", "mode": "oauth"},
                                ) as connect:
                                    with contextlib.redirect_stdout(stdout):
                                        nx_cli.run_nx_repl(
                                            {
                                                "account": "demo@nexplora.ai",
                                                "nx_user_id": "user-1",
                                                "user_id": "user-1",
                                                "world": "cowork",
                                            }
                                        )

        output = stdout.getvalue()
        picker.assert_called_once()
        confirm.assert_called_once()
        connect.assert_called_once()
        self.assertIn("Connecting Klaviyo", output)
        self.assertIn("Klaviyo connected", output)

    def test_repl_integrations_requires_confirmation_before_connect(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/integrations", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch("nx_slash_menu.run_integrations_menu", return_value="tavily") as picker:
                        with mock.patch("builtins.input", return_value="n") as confirm:
                            with mock.patch("getpass.getpass") as prompt:
                                with mock.patch("nx_mcp_manager.add_server_for_user") as add_server:
                                    with contextlib.redirect_stdout(stdout):
                                        nx_cli.run_nx_repl(
                                            {
                                                "account": "demo@nexplora.ai",
                                                "nx_user_id": "user-1",
                                                "user_id": "user-1",
                                                "world": "cowork",
                                            }
                                        )

        output = stdout.getvalue()
        picker.assert_called_once()
        prompt.assert_not_called()
        add_server.assert_not_called()
        self.assertIn("tavily", output)
        self.assertIn("Connect?", confirm.call_args[0][0])

    def test_repl_connect_prompts_for_api_key_when_missing(self):
        stdout = io.StringIO()
        tool_responses = [[{"server": "github", "name": "search_repositories"}]]

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/connect github", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli.time, "sleep"):
                        with mock.patch("nx_mcp_manager.start_user_hub", return_value={"status": "ready", "hub_alive": True}):
                            with mock.patch("getpass.getpass", return_value="ghp_prompted_123") as prompt:
                                with mock.patch(
                                    "nx_mcp_manager.add_server_for_user",
                                    return_value={"success": True, "status": "connected", "tools_count": 1},
                                ) as add_server:
                                    with mock.patch(
                                        "nx_mcp_manager.get_user_tools",
                                        side_effect=tool_responses,
                                    ):
                                        with contextlib.redirect_stdout(stdout):
                                            nx_cli.run_nx_repl(
                                                {
                                                    "account": "demo@nexplora.ai",
                                                    "nx_user_id": "user-1",
                                                    "user_id": "user-1",
                                                }
                                            )

        prompt.assert_called_once()
        visible_prompt = nx_cli.strip_ansi(prompt.call_args[0][0]).lower()
        self.assertIn("github", visible_prompt)
        self.assertIn("credential", visible_prompt)
        self.assertNotIn("github_personal_access_token", visible_prompt)
        self.assertEqual(
            add_server.call_args.kwargs["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"],
            "ghp_prompted_123",
        )

    def test_repl_connect_oauth_opens_browser_and_prompts_for_token(self):
        stdout = io.StringIO()
        tool_responses = [[{"server": "slack", "name": "post_message"}]]

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/connect slack", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli.time, "sleep"):
                        with mock.patch("nx_mcp_manager.start_user_hub", return_value={"status": "ready", "hub_alive": True}):
                            with mock.patch("webbrowser.open") as open_browser:
                                with mock.patch("getpass.getpass", return_value="xoxb-token") as prompt:
                                    with mock.patch(
                                        "nx_mcp_manager.add_server_for_user",
                                        return_value={"success": True, "status": "connected", "tools_count": 1},
                                    ) as add_server:
                                        with mock.patch(
                                            "nx_mcp_manager.get_user_tools",
                                            side_effect=tool_responses,
                                        ):
                                            with contextlib.redirect_stdout(stdout):
                                                nx_cli.run_nx_repl(
                                                    {
                                                        "account": "demo@nexplora.ai",
                                                        "nx_user_id": "user-1",
                                                        "user_id": "user-1",
                                                    }
                                                )

        open_browser.assert_called_once()
        self.assertIn("slack", open_browser.call_args[0][0])
        visible_prompt = nx_cli.strip_ansi(prompt.call_args[0][0]).lower()
        self.assertIn("slack", visible_prompt)
        self.assertIn("token", visible_prompt)
        self.assertEqual(
            add_server.call_args.kwargs["env"]["SLACK_BOT_TOKEN"],
            "xoxb-token",
        )

    def test_repl_integrations_returns_without_connect_when_picker_cancels(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/integrations", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch("nx_slash_menu.run_integrations_menu", return_value=None):
                        with mock.patch("nx_mcp_manager.add_server_for_user") as add_server:
                            with contextlib.redirect_stdout(stdout):
                                nx_cli.run_nx_repl({"account": "demo@nexplora.ai", "world": "cowork"})

        output = stdout.getvalue()
        add_server.assert_not_called()
        self.assertNotIn("Connecting", output)

    def test_repl_install_next_step_hides_env_var_name(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/install tavily", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(
                        nx_cli,
                        "install_mcp",
                        return_value={
                            "success": True,
                            "status": "installed_needs_auth",
                            "env_key": "TAVILY_API_KEY",
                        },
                    ):
                        with contextlib.redirect_stdout(stdout):
                            nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

        output = stdout.getvalue()
        self.assertIn("Next: /auth tavily", output)
        self.assertNotIn("TAVILY_API_KEY", output)

    def test_repl_catches_unexpected_exceptions_without_exposing_details(self):
        stdout = io.StringIO()

        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch.object(nx_cli, "slash_input", side_effect=["/connect github", "/exit"]):
                with mock.patch.object(nx_cli, "init_readline"):
                    with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                        with mock.patch.object(nx_cli, "_connect_service", side_effect=RuntimeError("NVIDIA_KEY_1 exploded")):
                            with mock.patch.object(nx_cli.Path, "home", return_value=Path(tmpdir)):
                                with contextlib.redirect_stdout(stdout):
                                    nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

            output = stdout.getvalue()
            log_path = Path(tmpdir) / ".nx" / "logs" / "error.log"
            log_exists = log_path.exists()
            log_text = log_path.read_text() if log_exists else ""

        self.assertIn("Something went wrong. If this persists contact support.", output)
        self.assertNotIn("NVIDIA_KEY_1", output)
        self.assertTrue(log_exists)
        self.assertIn("RuntimeError: NVIDIA_KEY_1 exploded", log_text)

    def test_repl_skills_opens_skills_picker(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/skills", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_slash_menu, "run_skills_menu", return_value="$cold_outreach") as skills_menu:
                        with contextlib.redirect_stdout(stdout):
                            nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

        output = stdout.getvalue()
        skills_menu.assert_called_once_with("cowork")
        self.assertNotIn("cold outreach activated", output)


class DataLoggerTests(unittest.TestCase):
    def test_log_message_defaults_world_and_provider(self):
        cfg = {
            "session_id": "session-1",
            "user_id": "user-1",
            "model": "deepseek-ai/deepseek-r1",
        }

        with mock.patch.object(nx_cli, "_data_client", return_value=object()):
            with mock.patch.object(nx_cli.nx_data, "save_message") as save_message:
                logger = nx_cli._DataLogger(cfg)
                logger.log_message("user", "hello")

        save_message.assert_called_once()
        kwargs = save_message.call_args.kwargs
        self.assertEqual(kwargs["world"], "cowork")
        self.assertEqual(kwargs["model"], "deepseek-ai/deepseek-r1")
        self.assertEqual(kwargs["provider"], "deepinfra")

    def test_ensure_user_uses_nx_user_id_without_upsert(self):
        cfg = {
            "account": "demo@nexplora.ai",
            "nx_user_id": "nx-user-1",
            "nx_token": "nx-token-1",
        }

        with mock.patch.object(nx_cli, "_data_client", return_value=object()):
            with mock.patch.object(nx_cli.nx_data, "upsert_user") as upsert_user:
                with mock.patch.object(nx_cli, "save_config"):
                    logger = nx_cli._DataLogger(cfg)
                    user_id = logger.ensure_user()

        self.assertEqual(user_id, "nx-user-1")
        self.assertEqual(cfg["user_id"], "nx-user-1")
        upsert_user.assert_not_called()


class StreamChatTests(unittest.TestCase):
    def test_stream_chat_caches_response_model_and_provider(self):
        cfg = {"token": "token-1", "model": "requested-model"}

        response = mock.Mock()
        response.status_code = 200
        response.headers = {"content-type": "text/event-stream"}
        response.iter_lines.return_value = [
            b'data: {"model":"deepseek-ai/deepseek-r1","provider":"deepinfra","choices":[{"delta":{"content":"Hello"}}]}',
            b"data: [DONE]",
        ]

        with mock.patch.object(nx_cli.requests, "post", return_value=response):
            chunks = list(nx_cli.stream_chat([{"role": "user", "content": "hi"}], cfg))

        self.assertEqual(chunks, ["Hello"])
        self.assertEqual(cfg["_last_model_used"], "deepseek-ai/deepseek-r1")
        self.assertEqual(cfg["_last_provider"], "deepinfra")

    def test_stream_chat_uses_provider_base_url_and_extra_body(self):
        cfg = {
            "token": "token-1",
            "model": "requested-model",
            "_last_provider": "nvidia",
            "_last_model_used": "moonshotai/kimi-k2.6",
            "_last_route_extra_body": {"chat_template_kwargs": {"thinking": True}},
        }

        response = mock.Mock()
        response.status_code = 200
        response.headers = {"content-type": "text/event-stream"}
        response.iter_lines.return_value = [
            b'data: {"choices":[{"delta":{"content":"ok"}}]}',
            b"data: [DONE]",
        ]

        # ── THE KEY POOL IS EMPTIED, AND THAT IS THE WHOLE FIX ────────────────────────────────
        # This test asserted the gateway was used and had been failing. It looked like a routing
        # regression; it is not. git shows the gateway attempt has been appended to pool_attempts
        # (i.e. LAST, after every pool key) since 394367fc3 — the commit that removed its `if False`
        # and enabled it at all — which predates this test by a month. The ordering never changed.
        #
        # What the test was really depending on was an EMPTY key pool: with no pool keys, the
        # gateway is the only attempt and therefore also the first. On any machine or build where
        # the pool yields keys, NVIDIA is tried first and the assertion fails. So it passed or failed
        # according to ambient pool contents, not according to anything about routing.
        #
        # Emptying the pool explicitly makes the real claim testable and deterministic: given a
        # session token and nothing else to try, the request goes to the Nexplora gateway with the
        # session JWT — not to a provider endpoint. The gateway-vs-pool PRIORITY is a separate,
        # deliberate product decision that lives in stream_chat and is not this test's subject.
        empty_pool = mock.Mock()
        empty_pool.iter_slots.return_value = []
        with mock.patch.object(nx_cli, "get_pool", return_value=empty_pool):
            with mock.patch.object(nx_cli.requests, "post", return_value=response) as post:
                list(nx_cli.stream_chat([{"role": "user", "content": "hi"}], cfg))

        # The Nexplora GATEWAY (CHAT_URL) proxies provider routing and accepts the session JWT
        # directly — posts go there, not to the provider's /chat/completions endpoint.
        self.assertEqual(post.call_args.args[0], nx_cli.CHAT_URL)
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "moonshotai/kimi-k2.6")
        # Provider params merge at the TOP LEVEL, never nested under "extra_body"
        # — the raw endpoint 400s on a literal "extra_body" field (see _post()'s
        # comment in nx_cli.py). Assert the flattened shape, not the nested one.
        self.assertEqual(payload["chat_template_kwargs"], {"thinking": True})
        self.assertEqual(payload["max_tokens"], 4096)
        self.assertTrue(payload["stream"])

    def test_stream_chat_uses_explicit_api_key_override(self):
        cfg = {"token": "token-1", "model": "requested-model"}

        response = mock.Mock()
        response.status_code = 200
        response.headers = {"content-type": "text/event-stream"}
        response.iter_lines.return_value = [
            b'data: {"choices":[{"delta":{"content":"ok"}}]}',
            b"data: [DONE]",
        ]

        with mock.patch.object(nx_cli.requests, "post", return_value=response) as post:
            list(nx_cli.stream_chat([{"role": "user", "content": "hi"}], cfg, api_key="override-key"))

        headers = post.call_args.kwargs["headers"]
        self.assertEqual(headers["Authorization"], "Bearer override-key")

    def test_stream_chat_prefers_explicit_route_args_over_cfg_state(self):
        cfg = {
            "token": "token-1",
            "model": "cfg-model",
            "_last_provider": "deepinfra",
            "_last_model_used": "cfg-last-model",
            "_last_route_extra_body": {"cfg": True},
        }

        response = mock.Mock()
        response.status_code = 200
        response.headers = {"content-type": "text/event-stream"}
        response.iter_lines.return_value = [
            b'data: {"choices":[{"delta":{"content":"ok"}}]}',
            b"data: [DONE]",
        ]

        with mock.patch.object(nx_cli.requests, "post", return_value=response) as post:
            list(
                nx_cli.stream_chat(
                    [{"role": "user", "content": "hi"}],
                    cfg,
                    api_key="route-key",
                    model="route-model",
                    provider="nvidia",
                    extra_body={"route": True},
                )
            )

        self.assertEqual(post.call_args.args[0], nx_cli.PROVIDER_BASE_URLS["nvidia"] + "/chat/completions")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["model"], "route-model")
        # Flattened at the top level — see the comment on the sibling assertion
        # above for why "extra_body" is never a literal nested key.
        self.assertEqual(payload["route"], True)


class ReadlineTests(unittest.TestCase):
    def test_init_readline_registers_safe_history_writer(self):
        callback = None

        def fake_register(fn):
            nonlocal callback
            callback = fn

        with mock.patch.object(nx_cli, "HAVE_READLINE", True):
            with mock.patch.object(nx_cli, "ensure_dirs"):
                with mock.patch.object(nx_cli.readline, "read_history_file"):
                    with mock.patch.object(nx_cli.atexit, "register", side_effect=fake_register):
                        nx_cli.init_readline()

        self.assertIsNotNone(callback)
        with mock.patch.object(nx_cli.readline, "write_history_file", side_effect=PermissionError("blocked")):
            callback()


class NXSessionExchangeTests(unittest.TestCase):
    def test_exchange_for_nx_session_persists_session_tokens(self):
        cfg = {"token": "nexplora-jwt"}
        httpx = types.ModuleType("httpx")
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            "nx_access_token": "nx-access",
            "nx_refresh_token": "nx-refresh",
            "nx_user_id": "nx-user-1",
        }
        httpx.post = mock.Mock(return_value=response)

        with mock.patch.dict(sys.modules, {"httpx": httpx}):
            with mock.patch.object(nx_cli, "save_config") as save_config:
                data = nx_cli.exchange_for_nx_session("nexplora-jwt", cfg)

        self.assertEqual(data["nx_access_token"], "nx-access")
        self.assertEqual(cfg["nx_token"], "nx-access")
        self.assertEqual(cfg["nx_refresh_token"], "nx-refresh")
        self.assertEqual(cfg["nx_user_id"], "nx-user-1")
        save_config.assert_called_once_with(cfg)


class NXDataClientTests(unittest.TestCase):
    def test_init_client_authenticates_postgrest_with_user_jwt(self):
        client = mock.Mock()
        client.postgrest = mock.Mock()

        with mock.patch.object(nx_data, "_HAS_SUPABASE", True):
            with mock.patch.object(nx_data, "SUPABASE_URL", "https://example.supabase.co"):
                with mock.patch.object(nx_data, "SUPABASE_ANON_KEY", "anon-key"):
                    with mock.patch.object(nx_data, "create_client", return_value=client) as create_client:
                        result = nx_data.init_client(user_jwt="nx-jwt")

        self.assertIs(result, client)
        create_client.assert_called_once_with("https://example.supabase.co", "anon-key")
        client.postgrest.auth.assert_called_once_with("nx-jwt")


class StorageHelpersTests(unittest.TestCase):
    def test_append_storage_message_records_expected_shape(self):
        messages = []

        msg = nx_cli.append_storage_message(
            messages=messages,
            role="assistant",
            content="Hello from NX",
            world="cowork",
            model_used="deepseek-ai/deepseek-r1",
        )

        self.assertEqual(messages, [msg])
        self.assertEqual(msg["role"], "assistant")
        self.assertEqual(msg["content"], "Hello from NX")
        self.assertEqual(msg["world"], "cowork")
        self.assertEqual(msg["model_used"], "deepseek-ai/deepseek-r1")
        self.assertEqual(msg["trainable"], True)
        self.assertIn("timestamp", msg)

    def test_append_storage_message_uses_timezone_utc_when_datetime_utc_is_missing(self):
        messages = []
        fake_datetime = types.SimpleNamespace(
            datetime=__import__("datetime").datetime,
            timezone=__import__("datetime").timezone,
        )

        with mock.patch.object(nx_cli, "datetime", fake_datetime):
            msg = nx_cli.append_storage_message(
                messages=messages,
                role="assistant",
                content="Hello from NX",
                world="cowork",
                model_used="deepseek-ai/deepseek-r1",
            )

        self.assertEqual(messages, [msg])
        self.assertTrue(msg["timestamp"].endswith("+00:00"))

    def test_storage_timestamp_helpers_use_timezone_utc_when_datetime_utc_is_missing(self):
        fake_datetime = types.SimpleNamespace(
            datetime=__import__("datetime").datetime,
            timezone=__import__("datetime").timezone,
        )

        with mock.patch.object(nx_storage, "_dt", fake_datetime):
            self.assertRegex(nx_storage._timestamp(), r"^\d{8}-\d{6}$")
            self.assertTrue(nx_storage._utc_iso().endswith("+00:00"))

    def test_handle_storage_save_command_uses_last_response(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_cli, "save_artifact", return_value={"path": "docs/brief.txt", "url": "https://example.com/brief.txt"}) as save_artifact:
            with contextlib.redirect_stdout(stdout):
                nx_cli.handle_storage_save_command(
                    args="brief.txt",
                    user_id="user-1",
                    user_jwt="jwt-1",
                    last_response="final answer",
                    current_world="cowork",
                )

        save_artifact.assert_called_once_with(
            user_id="user-1",
            user_jwt="jwt-1",
            content="final answer",
            filename="brief",
            extension="txt",
        )
        self.assertIn("Saved", stdout.getvalue())


class RoutingTests(unittest.TestCase):
    def _import_module(self, name):
        spec = importlib.util.find_spec(name)
        self.assertIsNotNone(spec, f"Expected module {name} to exist")
        if name == "nx_routing":
            sys.modules.pop("nx_key_pool", None)
        return _reload_module(name)

    def test_route_returns_expected_tier_and_default_voice_for_each_world(self):
        # The per-world TIER + default VOICE come from WORLD_CONFIG (the promise of this test).
        # PROVIDER is resolved dynamically: code-family worlds route to the DeepInfra/Qwen-Coder
        # registry, the rest to Fireworks — so we assert the resolved model + reasoning match the
        # RESOLVED provider's tier registry (TIERS_BY_PROVIDER), never a hardcoded provider. The probe is a
        # short CODING phrase ("fix the bug") with no escalation keywords: code worlds stay code (it's coding),
        # flash worlds stay flash (no escalation), frontier/agentic worlds keep their config tier. A casual
        # (non-coding) probe would downgrade code worlds to flash — covered separately.
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test_key"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

            # Expected tier + default_voice DERIVED from the source of truth (WORLD_CONFIG) so this
            # can never re-rot when a world's config changes.
            expected = {}
            for _world in (
                "strategy", "finance", "legal", "compliance", "research", "product",
                "people", "cowork", "ops", "support", "hr", "onboarding", "sales",
                "marketing", "growth", "code", "nx-code", "devops", "nx-1", "agents",
            ):
                _cfg = nx_routing.WORLD_CONFIG[_world]
                expected[_world] = (_cfg["tier"], _cfg["default_voice"])

            for world, (tier, voice) in expected.items():
                with self.subTest(world=world):
                    result = nx_routing.route(world=world, user_input="fix the bug", user_id="user-1")
                    self.assertEqual(result.world, world)
                    self.assertEqual(result.tier, tier)      # the promise of this test: per-world tier…
                    self.assertEqual(result.voice, voice)    # …and default voice, both from WORLD_CONFIG.
                    # A concrete model is resolved (specific model choices are covered by the dedicated
                    # per-world model tests, e.g. test_route_code_world_picks_qwen_coder).
                    self.assertTrue(result.model)

    def test_voice_shift_triggers_fire_and_locked_worlds_do_not_shift(self):
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=False):
            nx_routing = self._import_module("nx_routing")

            # Canonical modes (MODE_POSTURES): PARTNER · AUTOPILOT · STUDY · REFINE.
            # A learning/"how does" intent shifts to STUDY.
            self.assertEqual(
                nx_routing.detect_voice_shift("How does this work?", "AUTOPILOT", "support"),
                "STUDY",
            )
            # No trigger → the world default passes through unchanged.
            self.assertEqual(
                nx_routing.detect_voice_shift("Should I do this?", "PARTNER", "cowork"),
                "PARTNER",
            )
            self.assertEqual(
                nx_routing.detect_voice_shift("Let's brainstorm an idea", "STUDY", "research"),
                "STUDY",
            )
            # An execution intent ("ship it") shifts to AUTOPILOT.
            self.assertEqual(
                nx_routing.detect_voice_shift("We should just ship it later", "PARTNER", "strategy"),
                "AUTOPILOT",
            )
            # Locked worlds never shift: ops is pinned to AUTOPILOT.
            self.assertEqual(
                nx_routing.detect_voice_shift("How does this work?", "AUTOPILOT", "ops"),
                "AUTOPILOT",
            )
            # Locked worlds never shift: legal is pinned to PARTNER.
            self.assertEqual(
                nx_routing.detect_voice_shift("Explain this", "PARTNER", "legal"),
                "PARTNER",
            )

    def test_mode_override_takes_precedence_over_auto_detection(self):
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=False):
            nx_routing = self._import_module("nx_routing")

            # Auto-detection of "how does this work?" would shift to STUDY, but an
            # explicit mode override wins. "refine" normalizes to the canonical
            # REFINE posture (distinct from the auto-detected STUDY), proving the
            # override takes precedence.
            result = nx_routing.route(
                world="support",
                user_input="how does this work?",
                user_id="user-1",
                override_voice="refine",
            )

            self.assertEqual(result.voice, "REFINE")

    def test_route_returns_valid_api_key_and_slot_index(self):
        # NVIDIA pool is now tertiary fallback — only used when Fireworks +
        # DeepInfra keys are both absent. Test that the pool still works in
        # that case.
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=True):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="hello", user_id="user-42")

        self.assertIn(result.api_key, _fake_nvidia_env().values())
        self.assertGreaterEqual(result.slot_index, 0)
        self.assertLess(result.slot_index, 6)
        self.assertEqual(result.provider, "nvidia")
        # Every tier now carries an EXPLICIT max_tokens generation ceiling (was {} before) — assert
        # the ceiling is present + positive rather than a brittle literal.
        self.assertIn("max_tokens", result.extra_body)
        self.assertGreater(result.extra_body["max_tokens"], 0)

    def test_route_uses_fireworks_when_env_key_present(self):
        # Primary provider 0.3.96+. Flash-tier cowork → V4-Flash on Fireworks.
        with mock.patch.dict(os.environ, {"FIREWORKS_API_KEY": "fw_test"}, clear=True):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="hello", user_id="user-42")

        self.assertEqual(result.provider, "fireworks")
        self.assertEqual(result.tier, "flash")
        self.assertEqual(result.model, "accounts/fireworks/models/deepseek-v4-flash")
        self.assertEqual(result.api_key, "fw_test")
        self.assertEqual(result.slot_index, -1)
        self.assertEqual(result.reasoning_effort, "low")

    def test_route_falls_back_to_deepinfra_when_no_fireworks_key(self):
        # No Fireworks key → DeepInfra is the next resolved provider, with
        # DeepInfra catalog IDs (different namespace than Fireworks).
        with mock.patch.dict(os.environ, {"DEEPINFRA_API_KEY": "di_test"}, clear=True):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="hello", user_id="user-42")

        self.assertEqual(result.provider, "deepinfra")
        self.assertEqual(result.model, "deepseek-ai/DeepSeek-V4-Flash")
        self.assertEqual(result.api_key, "di_test")

    def test_route_falls_back_to_nvidia_when_no_fireworks_or_deepinfra(self):
        # Both modern keys absent → NVIDIA NIM pool is the tertiary fallback.
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=True):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="hello", user_id="user-42")

        self.assertEqual(result.provider, "nvidia")
        self.assertIn(result.api_key, _fake_nvidia_env().values())
        self.assertGreaterEqual(result.slot_index, 0)

    def test_route_code_world_picks_kimi_meantime(self):
        # Meantime (Qwen 3.8 Max not released yet): the code tier routes to Kimi 2.6/7 on the secondary provider.
        # A short/"light" input picks Kimi K2.6 at medium reasoning; heavier inputs use the coding-specialized
        # Kimi K2.7-Code. The moment the DashScope Qwen key is set, coding flips to Qwen 3.8 Max (native override).
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                # A CODING turn stays on the code tier; a casual "hello" would downgrade to flash (see the
                # dedicated casual-downgrade test), so this asserts code-tier routing with a real coding input.
                result = nx_routing.route(world="code", user_input="fix the bug", user_id="user-42")

        self.assertEqual(result.world, "code")
        self.assertEqual(result.tier, "code")
        self.assertEqual(result.model, nx_routing.MR["peer"])   # Kimi K2.6 (meantime light-coding lane)
        self.assertEqual(result.reasoning_effort, "medium")

    def test_route_casual_chat_in_code_world_downgrades_to_flash(self):
        # Casual chat / talk (no coding) on the code page → flash tier (cheap), never the code tier.
        # Only ACTUAL coding (incl. audit) stays on the code tier. (User: "casual chat is flash even in the code page".)
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")
                casual = nx_routing.route(world="code", user_input="hey how's your day going", user_id="u1")
                audit = nx_routing.route(world="code", user_input="audit this module for bugs", user_id="u1")
        self.assertEqual(casual.tier, "flash")   # casual talk → flash
        self.assertEqual(audit.tier, "code")     # audit coding → code (→ Qwen when keyed)

    def test_route_escalates_flash_to_frontier_on_keyword(self):
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="please analyze Q3 revenue", user_id="user-1")

        self.assertEqual(result.tier, "frontier")
        self.assertEqual(result.model, "accounts/fireworks/models/deepseek-v4-pro")

    def test_route_does_not_escalate_on_keyword_substring(self):
        # "plant" must not trigger "plan" — word-boundary regex.
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="water the plant", user_id="user-1")

        self.assertEqual(result.tier, "flash")

    def test_route_escalates_flash_to_frontier_on_length(self):
        # A LONG, content-rich input escalates. (Length escalation is gated on
        # lexical diversity now, so repetition padding like "a"*601 does NOT
        # escalate — that's covered by the next test.)
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        long_diverse = " ".join(f"topic{i}detail" for i in range(80))  # 80 unique, >500 chars
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input=long_diverse, user_id="user-1")

        self.assertEqual(result.tier, "frontier")

    def test_route_does_not_escalate_on_repetition_padding(self):
        # Length from repeated tokens is low-signal — must NOT escalate.
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="and " * 200, user_id="user-1")

        self.assertEqual(result.tier, "flash")

    def test_route_council_prefix_overrides_world_tier(self):
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(world="cowork", user_input="$council should we hire", user_id="user-1")

        self.assertEqual(result.tier, "council")

    def test_route_audio_parts_route_to_glm(self):
        # audio_parts → GLM-5.2 on Fireworks (the only multimodal-audio model).
        env = {**_fake_nvidia_env(), "FIREWORKS_API_KEY": "fw_test"}
        with mock.patch.dict(os.environ, env, clear=False):
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                nx_routing = self._import_module("nx_routing")

                result = nx_routing.route(
                    world="cowork",
                    user_input="describe this audio",
                    user_id="user-1",
                    audio_parts=[{"type": "input_audio", "input_audio": {"data": "...", "format": "mp3"}}],
                )

        self.assertEqual(result.model, "accounts/fireworks/models/glm-5p2")
        self.assertEqual(result.tier, "frontier")

    def test_council_models_are_all_on_fireworks(self):
        # Council should use the three Fireworks-format model IDs.
        nx_obfuscate = self._import_module("nx_obfuscate")
        nx_council = _reload_module("nx_council")
        self.assertEqual(len(nx_council.COUNCIL_MODELS), 3)
        for m in nx_council.COUNCIL_MODELS:
            self.assertTrue(m.startswith("accounts/fireworks/models/"),
                            f"council model {m} is not on Fireworks")
        # All three should be distinct.
        self.assertEqual(len(set(nx_council.COUNCIL_MODELS)), 3)
        # Synthesis runs on V4-Pro (strongest reasoner), NOT Kimi — Kimi is the
        # Operator voice and using it biased synthesis toward Operator framing.
        self.assertEqual(nx_council.SYNTHESIS_MODEL, nx_obfuscate.FW["pro"])
        # Synthesis must be a Fireworks model too.
        self.assertTrue(nx_council.SYNTHESIS_MODEL.startswith("accounts/fireworks/models/"))


class KeyPoolTests(unittest.TestCase):
    def test_key_pool_initializes_with_6_keys_from_env(self):
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=False):
            nx_key_pool = _reload_module("nx_key_pool")

            pool = nx_key_pool.get_pool()

        self.assertEqual(len(pool.status()), 6)

    def test_key_pool_loads_from_keychain_when_env_is_empty(self):
        def fake_run(command, capture_output, text, timeout):
            slot = command[-2]
            stdout = "key-1\n" if slot == "nvidia-key-1" else ""
            return types.SimpleNamespace(returncode=0 if stdout else 1, stdout=stdout)

        with mock.patch.dict(os.environ, {}, clear=True):
            nx_key_pool = _reload_module("nx_key_pool")
            with mock.patch("subprocess.run", side_effect=fake_run):
                pool = nx_key_pool.get_pool()

        self.assertEqual(len(pool.status()), 1)
        self.assertEqual(pool.get_key("user-1"), ("key-1", 0))

    def test_key_pool_returns_empty_pool_when_no_keys_exist(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            nx_key_pool = _reload_module("nx_key_pool")
            with mock.patch("subprocess.run", return_value=types.SimpleNamespace(returncode=1, stdout="")):
                pool = nx_key_pool.get_pool()

        self.assertEqual(pool.get_key("user-1"), ("", -1))
        self.assertEqual(pool.status(), [])

    def test_different_user_ids_get_distributed_across_slots(self):
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=False):
            nx_key_pool = _reload_module("nx_key_pool")

            _, slot_a = nx_key_pool.get_pool().get_key("user-a")
            _, slot_b = nx_key_pool.get_pool().get_key("user-b")

        self.assertNotEqual(slot_a, slot_b)

    def test_record_failure_locks_slot_after_3_failures(self):
        with mock.patch.dict(os.environ, _fake_nvidia_env(), clear=False):
            nx_key_pool = _reload_module("nx_key_pool")
            pool = nx_key_pool.get_pool()
            _, slot_index = pool.get_key("user-a")

            pool.record_failure(slot_index)
            pool.record_failure(slot_index)
            pool.record_failure(slot_index)

        self.assertTrue(pool.status()[slot_index]["locked"])


class PromptBuilderTests(unittest.TestCase):
    def _import_module(self, name):
        spec = importlib.util.find_spec(name)
        self.assertIsNotNone(spec, f"Expected module {name} to exist")
        return importlib.import_module(name)

    def test_build_system_prompt_assembles_for_all_voices(self):
        nx_prompts = self._import_module("nx_prompts")

        # Canonical modes only (MODE_POSTURES) — the retired voices
        # PEER/ADVISOR/CHALLENGER/TEACHER/OPERATOR fold into these via
        # normalize_mode and no longer have their own gate entries.
        for voice in nx_prompts.MODE_POSTURES:
            with self.subTest(voice=voice):
                prompt = nx_prompts.build_system_prompt(
                    world="cowork",
                    voice=voice,
                    rag_context="Retrieved facts",
                )
                self.assertIn("You are NX. Built by Nexplora.", prompt)
                self.assertIn(f"Current world: {'COWORK'}", prompt)
                self.assertIn(nx_prompts.NX_VOICE_GATES[voice].strip(), prompt)
                self.assertIn(nx_prompts.RESPONSE_FORMAT.strip(), prompt)
                self.assertIn("Retrieved facts", prompt)

    def test_build_system_prompt_includes_guardrails_seeds_and_extended_world_context(self):
        nx_prompts = self._import_module("nx_prompts")

        prompt = nx_prompts.build_system_prompt(
            world="devops",
            voice="OPERATOR",
            rag_context="RAG CONTEXT",
        )

        self.assertIn(nx_prompts.NX_GUARDRAILS.strip(), prompt)
        self.assertIn(nx_prompts.NX_SEEDS.strip(), prompt)
        self.assertIn("Current world: DEVOPS", prompt)
        self.assertIn(nx_prompts.NX_WORLD_CONTEXT["devops"], prompt)
        self.assertIn("RAG CONTEXT", prompt)

    def test_prompt_sources_do_not_include_bold_markdown(self):
        nx_prompts = self._import_module("nx_prompts")

        self.assertNotIn("**", nx_prompts.NX_IDENTITY)
        for voice, gate in nx_prompts.NX_VOICE_GATES.items():
            with self.subTest(voice=voice):
                self.assertNotIn("**", gate)


class ReplModeCommandTests(unittest.TestCase):
    def setUp(self):
        # Force the soft daily-quota gate open (see ReplTests.setUp).
        _qp = mock.patch.object(nx_cli, "_quota_check_and_warn", return_value=True)
        _qp.start()
        self.addCleanup(_qp.stop)

    def test_repl_mode_command_updates_override_and_routes_with_it(self):
        self.assertTrue(hasattr(nx_cli, "route"), "Expected nx_cli.route to be wired into the REPL")

        calls = []

        def fake_route(world, user_input, user_id, override_voice=None, prefer_primary_provider=False,
                       effort_override=None, audio_parts=None):
            calls.append(
                {
                    "world": world,
                    "user_input": user_input,
                    "user_id": user_id,
                    "override_voice": override_voice,
                    "prefer_primary_provider": prefer_primary_provider,
                    "effort_override": effort_override,
                }
            )
            return types.SimpleNamespace(
                world=world,
                tier="execution",
                model="test-model",
                voice=override_voice or "AUTOPILOT",
                provider="deepinfra",
                api_key="test-key",
                slot_index=1,
                extra_body={},
            )

        stdout = io.StringIO()
        # /mode study selects the canonical STUDY posture; it is displayed
        # title-cased ("Study") and stored as the "STUDY" override that the next
        # turn routes with. (The retired "teacher" alias folds to the same
        # STUDY posture via normalize_mode.)
        with mock.patch.object(nx_cli, "slash_input", side_effect=["/mode study", "how does this work?", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli, "stream_chat", return_value=iter(["done"])):
                        with mock.patch.object(nx_cli, "route", side_effect=fake_route):
                            with contextlib.redirect_stdout(stdout):
                                nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

        self.assertIn("mode", stdout.getvalue())
        self.assertIn("Study", stdout.getvalue())
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["override_voice"], "STUDY")
        self.assertEqual(calls[0]["user_id"], "demo@nexplora.ai")

    def test_repl_keys_and_vpn_commands_do_not_crash_when_vpn_unavailable(self):
        stdout = io.StringIO()
        fake_pool = mock.Mock()
        fake_pool.status.return_value = [{"slot": 1, "requests_this_minute": 0, "failures": 0, "locked": False}]
        fake_rotator = mock.Mock()
        fake_rotator.status.return_value = {"available": False, "reason": "protonvpn-cli not installed"}

        with mock.patch.object(nx_cli, "slash_input", side_effect=["/keys", "/vpn", "/exit"]):
            with mock.patch.object(nx_cli, "init_readline"):
                with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                    with mock.patch.object(nx_cli, "get_pool", return_value=fake_pool):
                        with mock.patch.object(nx_cli, "get_rotator", return_value=fake_rotator):
                            with contextlib.redirect_stdout(stdout):
                                nx_cli.run_nx_repl({"account": "demo@nexplora.ai"})

        output = stdout.getvalue()
        self.assertIn("key 1", output)
        self.assertIn("protonvpn-cli not installed", output)


class ExecutionModeTests(unittest.TestCase):
    def test_is_execution_task_distinguishes_code_requests_from_chat(self):
        nx_executor = _reload_module("nx_executor")

        self.assertFalse(nx_executor.is_execution_task("create file app.py", "cowork"))
        self.assertTrue(nx_executor.is_execution_task("build and deploy this", "nx-code"))
        self.assertTrue(nx_executor.is_execution_task("implement auth flow", "code"))
        self.assertFalse(nx_executor.is_execution_task("hello there", "nx-code"))
        self.assertFalse(nx_executor.is_execution_task("whattup nx", "code"))
        self.assertFalse(nx_executor.is_execution_task("what do you think about pricing?", "cowork"))
        self.assertFalse(nx_executor.is_execution_task("run this pricing idea by me", "finance"))

    def test_stream_file_write_prints_colored_diff(self):
        nx_executor = _reload_module("nx_executor")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            nx_executor.stream_file_write(
                "app.py",
                "new line\nkeep line\n",
                original="old line\nkeep line\n",
            )

        output = stdout.getvalue()
        self.assertIn("  ✦ app.py", output)
        self.assertIn("\033[31m-old line\033[0m", output)
        self.assertIn("\033[32m+new line\033[0m", output)

    def test_stream_command_prints_command_output_and_success(self):
        nx_executor = _reload_module("nx_executor")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = nx_executor.stream_command("printf 'hello\\nworld\\n'")

        output = stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("$ printf 'hello\\nworld\\n'", output)
        self.assertIn("  hello", output)
        self.assertIn("  world", output)
        self.assertIn("\033[32m✓ done\033[0m", output)


class RunChatTests(unittest.TestCase):
    def test_run_chat_runs_textual_inline(self):
        captured = {}
        fake_chat = types.ModuleType("chat_ui")
        fake_logger = mock.Mock()

        class FakeChatApp:
            def __init__(self, **kwargs):
                captured["init"] = kwargs

            def run(self, **kwargs):
                captured["run"] = kwargs

        fake_chat.NXChatApp = FakeChatApp

        with mock.patch.object(nx_cli, "_load_sibling_module", return_value=fake_chat):
            with mock.patch.object(nx_cli, "_DataLogger", return_value=fake_logger):
                with mock.patch.object(nx_cli, "_init_storage_state", return_value={}):
                    with mock.patch.object(nx_cli, "init_rag", return_value=None):
                        with mock.patch.object(nx_cli, "load_system_prompt", return_value="system prompt"):
                            with mock.patch.object(nx_cli, "_flush_storage_session"):
                                nx_cli.run_chat({"account": "demo@nexplora.ai"})

        self.assertEqual(captured["run"], {"inline": True})


class NXTerminalTests(unittest.TestCase):
    def _stream_render(self, full_text, chunk=3):
        """Stream full_text through the live renderer in tiny chunks (splitting
        tags across boundaries) and return the ANSI-stripped on-screen output."""
        import re as _re
        nx_terminal._current_stream = None
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            nx_terminal.print_nx_start()
            for i in range(0, len(full_text), chunk):
                nx_terminal.print_nx_chunk(full_text[i:i + chunk])
            nx_terminal.print_nx_end()
        return _re.sub(r"\x1b\[[0-9;]*m", "", buf.getvalue())

    def test_stream_renders_tool_calls_as_clean_lines_no_raw_tags(self):
        # Tags split across 3-char chunks — the exact condition that used to leak
        # raw <nx:...> / ```nx-run syntax onto the screen.
        full = (
            "Let me check that first.\n\n"
            '<nx:read_file path="docs/README.md"/>\n'
            "```nx-run\nfind /Users/x/Nx -type f -name '*.mp4' 2>/dev/null | head\n```\n"
            "No video in the repo. Where is it?"
        )
        out = self._stream_render(full)
        # No raw tool syntax may reach the user.
        self.assertNotIn("<nx:", out)
        self.assertNotIn("nx-run", out)
        self.assertNotIn("```", out)
        # Clean, scannable action line for read_file (run_command / ```nx-run blocks are
        # stripped from the prose stream — the executor prints their own "Ran …" block).
        self.assertIn("Read", out)
        self.assertIn("README.md", out)
        # Prose on both sides survives.
        self.assertIn("Let me check that first.", out)
        self.assertIn("Where is it?", out)

    def test_stream_does_not_dump_long_commands(self):
        # A run_command tag + its (possibly huge) payload must NEVER reach the prose stream —
        # the raw tag is stripped and the executor prints its own "Ran …" block instead.
        long_cmd = "echo " + "a" * 300
        out = self._stream_render(f'<nx:run_command cmd="{long_cmd}"/>')
        self.assertNotIn("<nx:run_command", out)
        self.assertNotIn("a" * 200, out)  # the long command body is never dumped

    def test_welcome_is_responsive_no_overflow_when_narrow(self):
        # Regression for the "ai slop" narrow-pane render: every line must fit
        # the terminal width (no wrap), and the eyebrow must not be letter-spaced
        # when narrow (that wrapped mid-word as "SYST/EM").
        import re as _re
        for w in (48, 56, 64):
            stdout = io.StringIO()
            with mock.patch.object(nx_terminal, "_w", return_value=w):
                with contextlib.redirect_stdout(stdout):
                    nx_terminal.print_welcome("v@gmail.com", "0.5.6", "strategy")
            plain = _re.sub(r"\x1b\[[0-9;]*m", "", stdout.getvalue())
            for line in plain.split("\n"):
                self.assertLessEqual(len(line), w, f"line overflows {w} cols: {line!r}")
            self.assertIn("NEXPLORA", plain)                    # plain eyebrow when narrow
            self.assertNotIn("N E X P L O R A", plain)          # not letter-spaced when narrow

    def test_stream_strips_markdown_emphasis_for_prose(self):
        # Visual guard: NX defaults to prose — stray markdown bold/headers that
        # render as literal junk in a terminal must be stripped.
        out = self._stream_render("**FREELANCE AGREEMENT**\n## Section 1\nClean text here.")
        self.assertNotIn("**", out)
        self.assertNotIn("## ", out)
        self.assertIn("FREELANCE AGREEMENT", out)
        self.assertIn("Section 1", out)
        self.assertIn("Clean text here.", out)

    def test_visual_guard_no_dark_tones_no_box_chars(self):
        # A rendered turn must use no near-invisible tones and no box-drawing
        # chars in prose (those were the regressions that shipped).
        out_raw = io.StringIO()
        import re as _re
        nx_terminal._current_stream = None
        with contextlib.redirect_stdout(out_raw):
            nx_terminal.print_nx_start()
            nx_terminal.print_nx_chunk("On it — here's the plan.")
            nx_terminal.print_nx_end()
        raw = out_raw.getvalue()
        for dark in ("38;2;68;65;48", "38;2;38;36;22", "38;2;120;98;44", "38;2;100;78;28"):
            self.assertNotIn(dark, raw, f"dark tone {dark} resurfaced")

    def test_thinking_indicator_no_flood_on_non_tty(self):
        # Regression: on a non-TTY stdout (no carriage-return overwrite), the
        # working spinner must print ONE static line, never a redraw-loop flood
        # ("500 Working" on screen). It also must use a readable tone, not the
        # old dark 120;98;44.
        import time as _t
        stdout = io.StringIO()  # .isatty() is False
        with contextlib.redirect_stdout(stdout):
            stopper = nx_terminal.print_nx_thinking()
            _t.sleep(0.4)
            stopper.set()
        out = stdout.getvalue()
        # The non-tty branch prints ONE static "working…" line, then a throttled beat only
        # every 15s — so in this short window it appears exactly once (no redraw-loop flood).
        self.assertEqual(out.count("working…"), 1, "spinner flooded on non-tty")
        self.assertNotIn("38;2;120;98;44", out)  # not the old dark tone

    def test_print_welcome_matches_target_sections_without_legacy_copy(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_terminal, "clear_screen"):
            with contextlib.redirect_stdout(stdout):
                nx_terminal.print_welcome("demo@nexplora.ai", "0.3.23", "cowork")

        output = stdout.getvalue()
        # Gold NX chip (background) — the brand lockup.
        self.assertIn("\033[48;2;200;164;74m", output)
        self.assertIn("NX", output)
        # Email is masked on-screen as of 0.3.91.
        self.assertIn("d…@nexplora.ai", output)
        self.assertNotIn("demo@nexplora.ai", output)
        # Minimal lockup — tracked NEXPLORA eyebrow + START/LIVE columns, no more
        # "TIPS" / "WHAT'S LIVE" headers and no fabricated copy.
        self.assertIn("N E X P L O R A", output)     # tracked NEXPLORA eyebrow (wide)
        self.assertIn("L I V E", output)             # tracked eyebrow label
        self.assertNotIn("WHAT'S AVAILABLE", output)
        self.assertNotIn("1,000+", output)
        self.assertIn("Nexplora model layer", output)
        self.assertIn("ready", output)               # live status heartbeat
        # Commands surfaced in the new layout. (The welcome START column lists
        # /mode, not a world command — worlds are switched via /worlds elsewhere.)
        for cmd in ("/help", "/mode", "/model", "/council", "/integrations", "/skills"):
            with self.subTest(cmd=cmd):
                self.assertIn(cmd, output)

    def test_print_welcome_uses_foreground_only_sections_without_box_drawing_chars(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_terminal, "_w", return_value=96):
            with contextlib.redirect_stdout(stdout):
                nx_terminal.print_welcome("demo@nexplora.ai", "0.3.50", "cowork")

        output = stdout.getvalue()
        self.assertIn("\033[48;2;200;164;74m", output)   # gold NX chip
        self.assertIn("\033[38;2;172;166;148m", output)  # readable dim tone
        # Minimal lockup: the NEXPLORA eyebrow + the live "ready" heartbeat, no fabricated
        # marketing counts (no "1,000+", "21 worlds", etc.).
        self.assertIn("N E X P L O R A", output)
        self.assertIn("ready", output)
        self.assertNotIn("1,000+", output)
        self.assertNotIn("21 worlds", output)
        self.assertNotIn("21 operations", output)
        self.assertNotIn("7,800", output)
        # Concentric hairline frame (foreground rule, not box-drawing chars).
        self.assertIn("─" * 80, output)
        for ch in "╭╮╰╯│":
            with self.subTest(ch=ch):
                self.assertNotIn(ch, output)

    def test_slash_input_uses_clean_prompt_line_without_footer(self):
        stdout = _TTYStringIO()
        with mock.patch.object(nx_slash_menu.os, "isatty", return_value=True):
            with mock.patch.object(nx_slash_menu.os, "get_terminal_size", return_value=os.terminal_size((120, 30))):
                with mock.patch.object(nx_terminal, "_w", return_value=96):
                    with mock.patch.object(nx_slash_menu, "_read_first_char", return_value="\n"):
                        with mock.patch.object(nx_slash_menu.sys, "stdout", stdout):
                            # EOF is patched rather than relying on the ambient stdin. On a non-TTY
                            # stdin slash_input reads through input(), and under pytest that is
                            # DontReadFromInput, which raises OSError("reading from stdin while
                            # output is captured") — a harness artifact, not a product failure. The
                            # documented EOF sentinel is what this test is actually about, so it is
                            # now stated explicitly instead of inherited from however the runner
                            # happens to leave stdin.
                            def _eof_input(prompt=""):
                                # Real input(prompt) EMITS the prompt and then hits EOF. A bare
                                # side_effect=EOFError skips the emit, which silently empties the
                                # captured output and would make the "›" assertion below vacuous.
                                stdout.write(prompt)
                                raise EOFError

                            with mock.patch("builtins.input", _eof_input):
                                result = nx_slash_menu.slash_input("cowork")

        # On a non-TTY stdin the input bar reads via plain input() and returns
        # "/exit" on EOF (its documented EOF/^C sentinel).
        self.assertEqual(result, "/exit")
        output = stdout.getvalue()
        # The clean "›" prompt line — no full-width footer rule beneath it.
        self.assertNotIn("─" * 96, output)
        self.assertIn("›", output)

    def test_stream_nx_response_flushes_left_with_single_prefix(self):
        stdout = io.StringIO()

        with mock.patch.object(nx_terminal.time, "sleep") as sleep:
            with contextlib.redirect_stdout(stdout):
                nx_terminal.stream_nx_response("hello from nx")

        output = stdout.getvalue()
        self.assertTrue(output.startswith(f"  {nx_terminal.NX_SYMBOL}  {nx_terminal.WHITE}hello"))
        self.assertIn("from", output)
        self.assertIn("nx", output)
        self.assertEqual(sleep.call_count, 2)

    def test_get_input_returns_exit_on_keyboard_interrupt(self):
        with mock.patch("builtins.input", side_effect=KeyboardInterrupt):
            value = nx_terminal.get_input("cowork", "auto")

        self.assertEqual(value, "/exit")


class MainEntrypointTests(unittest.TestCase):
    def test_main_defaults_to_raw_repl_without_ui_flag(self):
        with mock.patch.object(nx_cli, "load_config", return_value={"token": "token-1", "account": "demo@nexplora.ai", "_setup_complete": True}):
            with mock.patch.object(nx_cli, "run_nx_repl") as run_nx_repl:
                with mock.patch.object(nx_cli, "run_chat") as run_chat:
                    with mock.patch.object(sys, "argv", ["nx"]):
                        nx_cli.main()

        run_nx_repl.assert_called_once()
        run_chat.assert_not_called()

    def test_main_ui_flag_launches_textual_chat(self):
        with mock.patch.object(nx_cli, "load_config", return_value={"token": "token-1", "account": "demo@nexplora.ai", "_setup_complete": True}):
            with mock.patch.object(nx_cli, "run_chat") as run_chat:
                with mock.patch.object(nx_cli, "run_nx_repl") as run_nx_repl:
                    with mock.patch.object(sys, "argv", ["nx", "--ui"]):
                        nx_cli.main()

        run_chat.assert_called_once()
        run_nx_repl.assert_not_called()

    def test_main_resets_launch_world_to_cowork(self):
        cfg = {"account": "demo@nexplora.ai", "token": "token-1", "world": "code", "_setup_complete": True}

        with mock.patch.object(nx_cli, "load_config", return_value=cfg):
            with mock.patch.object(nx_cli, "run_nx_repl") as run_nx_repl:
                with mock.patch.object(sys, "argv", ["nx"]):
                    nx_cli.main()

        run_nx_repl.assert_called_once()
        launched_cfg = run_nx_repl.call_args.args[0]
        self.assertEqual(launched_cfg["world"], "cowork")


class VPNRotatorTests(unittest.TestCase):
    def test_vpn_module_gracefully_reports_missing_protonvpn_cli(self):
        nx_vpn = _reload_module("nx_vpn")

        with mock.patch.object(nx_vpn.VPNRotator, "_check_available", return_value=False):
            rotator = nx_vpn.VPNRotator()

        self.assertEqual(rotator.status(), {"available": False, "reason": "protonvpn-cli not installed"})

    def test_flush_storage_session_saves_log_and_exports_training_candidates(self):
        state = {
            "cfg": {"user_id": "user-1", "world": "cowork", "session_id": "session-1"},
            "messages": [
                {
                    "role": "user",
                    "content": "hello",
                    "world": "cowork",
                    "model_used": "deepseek-ai/deepseek-r1",
                    "trainable": True,
                    "timestamp": "2026-06-13T00:00:00",
                }
            ],
        }

        with mock.patch.object(nx_cli, "save_session_log", return_value={"path": "sessions/session-1.json"}) as save_session_log:
            with mock.patch.object(nx_cli, "export_training_candidates", return_value={"pairs_exported": 1}) as export_training_candidates:
                nx_cli._flush_storage_session(state)

        save_session_log.assert_called_once()
        export_training_candidates.assert_called_once()
        self.assertTrue(state["flushed"])


class RagHelpersTests(unittest.TestCase):
    def test_init_rag_returns_none_when_module_unavailable(self):
        with mock.patch.object(nx_cli, "_rag_available", False):
            rag = nx_cli.init_rag("user-1", world="cowork")
        self.assertIsNone(rag)

    def test_build_rag_system_prompt_returns_base_when_no_results(self):
        rag = mock.Mock()
        rag.query.return_value = []

        prompt = nx_cli.build_rag_system_prompt(
            base_system_prompt="base prompt",
            rag=rag,
            query="pricing",
            world="cowork",
        )

        self.assertEqual(prompt, "base prompt")

    def test_ingest_helpers_are_noops_without_rag(self):
        nx_cli.ingest_user_message(None, "hello", "cowork")
        nx_cli.ingest_after_response(None, "answer", "cowork", "deepseek-ai/deepseek-r1")

    def test_flush_rag_on_exit_is_noop_without_rag(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            nx_cli.flush_rag_on_exit(None, [])
        self.assertEqual(stdout.getvalue(), "")


class NXRagTests(unittest.TestCase):
    def _make_rag(self):
        with mock.patch.object(nx_rag.nx_data, "init_client", return_value=None):
            with mock.patch.object(nx_rag.NXRag, "_init_ranker", return_value=None):
                rag = nx_rag.NXRag(user_id="user-1", world="cowork", rerank=False)
        rag._allow_model_download = False
        return rag

    def test_reranker_is_not_initialized_during_construction(self):
        with mock.patch.object(nx_rag.nx_data, "init_client", return_value=None):
            with mock.patch.object(nx_rag, "_load_flashrank_deps", return_value=(mock.Mock(), mock.Mock())) as load_flashrank:
                rag = nx_rag.NXRag(user_id="user-1", world="cowork", rerank=True)

        self.assertIsNone(rag._ranker)
        load_flashrank.assert_not_called()

    def test_embedding_uses_sentence_transformer_when_available(self):
        rag = self._make_rag()
        rag._embedder = mock.Mock()
        rag._embedder.encode.return_value = [0.1, 0.2, 0.3]

        embedding = rag._embedding("pricing strategy")

        self.assertEqual(embedding, [0.1, 0.2, 0.3])

    def test_embedding_falls_back_to_hash_if_embedder_encode_fails(self):
        rag = self._make_rag()
        rag._embedder = mock.Mock()
        rag._embedder.encode.side_effect = RuntimeError("boom")

        embedding = rag._embedding("pricing strategy")

        self.assertEqual(len(embedding), 384)
        self.assertAlmostEqual(sum(value * value for value in embedding), 1.0, places=5)

    def test_ingest_tracks_documents_in_local_index(self):
        rag = self._make_rag()
        rag._embed_text = mock.Mock(side_effect=[[1.0, 0.0], [0.0, 1.0]])

        self.assertTrue(rag.ingest("enterprise pricing playbook"))
        self.assertTrue(rag.ingest("hiring and onboarding guide"))

        self.assertEqual([doc["content"] for doc in rag._local_docs], [
            "enterprise pricing playbook",
            "hiring and onboarding guide",
        ])

    def test_query_uses_local_index_when_remote_search_is_empty(self):
        rag = self._make_rag()
        rag._embed_text = mock.Mock(
            side_effect=[
                [1.0, 0.0],
                [0.0, 1.0],
                [1.0, 0.0],
            ]
        )

        rag.ingest("enterprise pricing playbook")
        rag.ingest("hiring and onboarding guide")
        results = rag.query("pricing", world_filter="cowork")

        self.assertEqual(results[0]["content"], "enterprise pricing playbook")
        self.assertGreaterEqual(results[0]["similarity"], results[1]["similarity"])


class NXChatAppTests(unittest.IsolatedAsyncioTestCase):
    def _make_app(self):
        def stream_chat(messages, cfg):
            yield "Hello from NX"

        return chat_ui.NXChatApp(
            cfg={"account": "demo@nexplora.ai", "_version": "0.3.0"},
            stream_chat=stream_chat,
            save_session=lambda messages: "/tmp/session.json",
            clear_config=lambda: None,
            load_system_prompt=lambda: "system prompt",
            help_lines=("/help  show commands", "/logout  sign out"),
            on_save_command=None,
        )

    async def test_chat_app_renders_branded_welcome_panel_and_input(self):
        app = self._make_app()

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            app.query_one("#panel", Static)
            left = app.query_one("#left", Static).render()
            app.query_one("#right", Static)
            app.query_one("#stars", Static)
            app.query_one("#meta", Static)
            app.query_one("#output")
            prompt = app.query_one("#prompt", Input)

            self.assertIn("Welcome back", left.plain)
            self.assertIn("d…@nexplora.ai", left.plain)
            self.assertNotIn("demo@nexplora.ai", left.plain)
            self.assertEqual(prompt.placeholder, "Ask NX anything")

    async def test_chat_app_starts_with_empty_output(self):
        app = self._make_app()

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            output = app.query_one("#output")
            self.assertEqual(len(output.children), 0)
            self.assertEqual(app.query_one("#status", Static).render().plain, "")

    async def test_chat_app_keeps_header_animation_running(self):
        app = self._make_app()

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            before_right = app.query_one("#right", Static).render().plain
            before_stars = app.query_one("#stars", Static).render().plain

            for _ in range(140):
                app._tick()

            await pilot.pause()

            after_right = app.query_one("#right", Static).render().plain
            after_stars = app.query_one("#stars", Static).render().plain

            self.assertNotEqual(before_right, after_right)
            self.assertNotEqual(before_stars, after_stars)

    async def test_chat_app_save_command_uses_injected_callback(self):
        calls = []

        def stream_chat(messages, cfg):
            yield "Hello from NX"

        def on_save_command(args, last_response, current_world):
            calls.append((args, last_response, current_world))
            return {"path": "docs/brief.md"}

        app = chat_ui.NXChatApp(
            cfg={"account": "demo@nexplora.ai", "_version": "0.3.0", "world": "cowork"},
            stream_chat=stream_chat,
            save_session=lambda messages: "/tmp/session.json",
            clear_config=lambda: None,
            load_system_prompt=lambda: "system prompt",
            help_lines=("/help  show commands", "/logout  sign out"),
            on_save_command=on_save_command,
        )

        app._last_assistant_text = "Stored reply"
        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()
            app._handle_command("/save brief.md")
            await pilot.pause()

        self.assertEqual(calls, [("brief.md", "Stored reply", "cowork")])

    async def test_chat_app_world_command_updates_world_and_header(self):
        app = self._make_app()

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            prompt = app.query_one("#prompt", Input)
            app.on_input_submitted(Input.Submitted(input=prompt, value="/world finance"))
            await pilot.pause()

            self.assertEqual(app._world, "finance")
            self.assertEqual(app.cfg.get("world"), "finance")
            meta = app.query_one("#meta", Static).render().plain
            self.assertIn("World      finance", meta)

            output = app.query_one("#output")
            self.assertIn("world set to finance", output.children[-1].render().plain)

    async def test_chat_app_world_command_without_args_shows_list(self):
        app = self._make_app()

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            prompt = app.query_one("#prompt", Input)
            app.on_input_submitted(Input.Submitted(input=prompt, value="/world"))
            await pilot.pause()

            output = app.query_one("#output")
            self.assertIn("Available worlds", output.children[-1].render().plain)

    async def test_chat_app_keeps_assistant_response_visible_after_stream_finishes(self):
        def stream_chat(messages, cfg):
            yield "Hello"
            yield " from NX"

        app = chat_ui.NXChatApp(
            cfg={"account": "demo@nexplora.ai", "_version": "0.3.0"},
            stream_chat=stream_chat,
            save_session=lambda messages: "/tmp/session.json",
            clear_config=lambda: None,
            load_system_prompt=lambda: "system prompt",
            help_lines=("/help  show commands", "/logout  sign out"),
            on_save_command=None,
        )

        async with app.run_test(size=(100, 40)) as pilot:
            await pilot.pause()

            prompt = app.query_one("#prompt", Input)
            submit_event = Input.Submitted(input=prompt, value="Ship it")
            app.on_input_submitted(submit_event)

            await pilot.pause()
            await pilot.pause()

            output = app.query_one("#output")
            self.assertEqual(len(output.children), 2)

            assistant_block = output.children[1]
            self.assertEqual(assistant_block.render().plain, "✦\nHello from NX")
            self.assertEqual(app._last_assistant_text, "Hello from NX")
            self.assertEqual(app.query_one("#status", Static).render().plain, "")

            await pilot.pause()
            self.assertIs(output.children[1], assistant_block)
            self.assertEqual(assistant_block.render().plain, "✦\nHello from NX")


class ChatFormattingTests(unittest.TestCase):
    def test_render_message_formats_clean_user_layout(self):
        block = chat_ui._render_message("user", "What are we building with NX?")

        self.assertEqual(block.plain, "you\nWhat are we building with NX?")

    def test_render_message_keeps_multiline_assistant_text_flush_left(self):
        block = chat_ui._render_message("assistant", "Line one\nLine two")

        self.assertEqual(block.plain, "✦\nLine one\nLine two")


class LoggingSuppressionTests(unittest.TestCase):
    def test_chat_ui_suppresses_noisy_loggers(self):
        for name in ("httpx", "sentence_transformers", "transformers", "torch", "supabase"):
            logging.getLogger(name).setLevel(logging.INFO)

        chat_ui._suppress_noisy_logs()

        for name in ("httpx", "sentence_transformers", "transformers", "torch", "supabase"):
            self.assertEqual(logging.getLogger(name).level, logging.WARNING)

    def test_nx_cli_suppresses_noisy_loggers(self):
        for name in (
            "httpx",
            "huggingface_hub",
            "huggingface_hub.utils._http",
            "sentence_transformers",
            "transformers",
            "torch",
            "supabase",
        ):
            logging.getLogger(name).setLevel(logging.INFO)

        nx_cli._suppress_noisy_logs()

        for name in ("httpx", "supabase"):
            self.assertEqual(logging.getLogger(name).level, logging.WARNING)
        for name in ("huggingface_hub", "huggingface_hub.utils._http", "sentence_transformers", "transformers", "torch"):
            self.assertEqual(logging.getLogger(name).level, logging.ERROR)


class TextualLayoutAndBindingTests(unittest.TestCase):
    @staticmethod
    def _binding_pairs(bindings):
        pairs = set()
        for binding in bindings:
            if hasattr(binding, "key") and hasattr(binding, "action"):
                pairs.add((binding.key, binding.action))
            else:
                key, action, *_ = binding
                pairs.add((key, action))
        return pairs

    def test_chat_css_uses_full_width_layout(self):
        self.assertIn("Screen {\n        background: #050505;\n        color: #c8a44a;", chat_ui.NXChatApp.CSS)
        self.assertNotIn("align:", chat_ui.NXChatApp.CSS)
        self.assertIn("#panel {\n        width: 100%;", chat_ui.NXChatApp.CSS)
        self.assertIn("#inner {\n        layout: horizontal;\n        height: 16;\n        width: 100%;", chat_ui.NXChatApp.CSS)
        self.assertIn("#left {\n        width: 28;", chat_ui.NXChatApp.CSS)
        self.assertIn("#shell {\n        width: 100%;\n        height: 1fr;\n        padding: 0;", chat_ui.NXChatApp.CSS)

    def test_welcome_css_uses_full_width_layout(self):
        self.assertNotIn("align:", welcome.NXWelcome.CSS)
        self.assertIn("#panel {\n        width: 100%;", welcome.NXWelcome.CSS)
        self.assertIn("#left {\n        width: 28;", welcome.NXWelcome.CSS)

    def test_chat_and_welcome_define_ctrl_c_and_ctrl_q_quit_bindings(self):
        chat_bindings = self._binding_pairs(chat_ui.NXChatApp.BINDINGS)
        welcome_bindings = self._binding_pairs(welcome.NXWelcome.BINDINGS)

        self.assertIn(("ctrl+c", "quit"), chat_bindings)
        self.assertIn(("ctrl+q", "quit"), chat_bindings)
        self.assertIn(("ctrl+c", "quit"), welcome_bindings)
        self.assertIn(("ctrl+q", "quit"), welcome_bindings)


if __name__ == "__main__":
    unittest.main()
