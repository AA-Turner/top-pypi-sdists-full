import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import nx_slash_menu
from nx_slash_menu import SECTIONS, SLASH_COMMANDS, filter_commands


class _TTYStringIO(io.StringIO):
    def fileno(self):
        return 1


class TestSlashMenu(unittest.TestCase):
    def test_sections_only_include_top_level_commands_section(self):
        titles = [section["title"] for section in SECTIONS]
        self.assertEqual(titles, ["COMMANDS"])

    def test_flat_commands_are_built_from_sections(self):
        flattened = [
            command["cmd"]
            for section in SECTIONS
            for command in section["commands"]
        ]
        self.assertEqual([command["cmd"] for command in SLASH_COMMANDS], flattened)

    def test_filter_empty_returns_all(self):
        results = filter_commands("")
        self.assertEqual(len(results), len(SLASH_COMMANDS))

    def test_filter_by_command_name(self):
        results = filter_commands("/integrations")
        self.assertTrue(any(result["cmd"] == "/integrations" for result in results))

    def test_filter_by_description(self):
        results = filter_commands("Browse")
        self.assertTrue(any(result["cmd"] == "/skills" for result in results))

    def test_filter_case_insensitive(self):
        results = filter_commands("INTEGRATIONS")
        self.assertTrue(any(result["cmd"] == "/integrations" for result in results))

    def test_top_level_commands_match_expected_public_menu(self):
        commands = [command["cmd"] for command in SECTIONS[0]["commands"]]
        self.assertEqual(
            commands,
            [
                "/help",
                "/mode",
                "/effort",
                "/crew",
                "/go",
                "/brain",
                "/supply",
                "/takeoff",
                "/skills",
                "/create",
                "/integrations",
                "/connected",
                "/publish",
                "/channels",
                "/message",
                "/save",
                "/resume",
                "/logout",
            ],
        )
        # /worlds is intentionally demoted out of the top-level menu — it lives in the
        # /help footer now, reachable as a typed command but not a primary action.
        self.assertNotIn("/worlds", commands)
        self.assertNotIn("/world", commands)
        # /login is demoted the same way, and for a sharper reason: you are already signed in
        # whenever you can read this menu, so listing "sign in" was offering a no-op as a primary
        # action. It remains a TYPED command for the one case it exists for — a session that
        # expired mid-REPL — which test_resume_sessions.py pins so the repair path cannot be
        # deleted along with the menu entry.
        self.assertNotIn("/login", commands)

    def test_palette_finds_every_help_command(self):
        # POSTURE, not a second hand-maintained list: EVERY command /help lists must be reachable in the palette
        # (never "No matches" for a real command). This is the guard for the drift that hid /worlds + 18 others —
        # filter_commands pulls the full registry from nx_cli.HELP_GROUPS at runtime, so the two can't diverge.
        import nx_cli
        help_cmds = {cmd for _h, cmds in nx_cli.HELP_GROUPS for cmd, _d in cmds}
        help_cmds.add("/worlds")  # the /help WORLDS footer — a real, dispatchable command
        for cmd in sorted(help_cmds):
            hits = [c["cmd"] for c in filter_commands(cmd)]
            self.assertIn(cmd, hits, f"palette shows 'No matches' for {cmd} — it drifted out of /help sync")

    def test_message_channel_picker_registry(self):
        # /message opens run_message_menu, which must offer EVERY report-back channel the module supports.
        # This used to pin a literal four while nx_message.CHANNELS held five, so `sms` was configurable
        # only by typing the command — unreachable from any picker, and a dead row in the /channels hub.
        # Derived now, so the picker cannot fall behind the module again.
        import nx_message
        keys = [c["key"] for c in nx_slash_menu.MESSAGE_CHANNELS]
        self.assertEqual(sorted(keys), sorted(nx_message.CHANNELS))
        self.assertEqual(keys[0], "telegram", "telegram stays first — it is the default report-back")
        self.assertTrue(callable(nx_slash_menu.run_message_menu))
        names = [c["name"] for c in nx_slash_menu.MESSAGE_CHANNELS]
        self.assertEqual(len(names), len(set(names)), f"duplicate display name: {names}")
        # "Text" is BANNED as a display name: /channels lists SMS and iMessage side by side, so one word
        # naming whichever was nearest sent operators picking "Text" to the wrong channel.
        self.assertNotIn("Text", names)
        self.assertIn("iMessage", names)
        self.assertIn("SMS", names)

    def test_slash_input_opens_message_picker_on_message_result(self):
        with mock.patch.object(nx_slash_menu, "_read_input_bar", return_value=("", "/")):
            with mock.patch.object(nx_slash_menu, "_run_prompt_toolkit_menu", return_value="/message"):
                with mock.patch.object(nx_slash_menu, "run_message_menu", return_value="telegram") as picker:
                    result = nx_slash_menu.slash_input()
        self.assertEqual(result, "__message__telegram")
        picker.assert_called_once()

    def test_sensitive_and_connect_commands_are_not_advertised(self):
        commands = [command["cmd"] for command in SLASH_COMMANDS]
        self.assertNotIn("/keys", commands)
        self.assertNotIn("/vpn", commands)
        self.assertFalse(any(command == "/connect" or command.startswith("/connect ") for command in commands))

    def test_slash_input_opens_prompt_toolkit_menu_when_slash_trigger(self):
        # slash_input reads via _read_input_bar, which surfaces a "/" trigger on an empty buffer.
        with mock.patch.object(nx_slash_menu, "_read_input_bar", return_value=("", "/")):
            with mock.patch.object(
                nx_slash_menu, "_run_prompt_toolkit_menu", return_value="/help"
            ) as prompt_menu:
                result = nx_slash_menu.slash_input()

        self.assertEqual(result, "/help")
        prompt_menu.assert_called_once_with("cowork")

    def test_slash_input_returns_empty_when_prompt_toolkit_fails(self):
        with mock.patch.object(nx_slash_menu, "_read_input_bar", return_value=("", "/")):
            with mock.patch.object(
                nx_slash_menu, "_run_prompt_toolkit_menu", side_effect=RuntimeError("boom")
            ):
                result = nx_slash_menu.slash_input(world="finance")

        self.assertEqual(result, "")

    def test_slash_input_dollar_trigger_composes_skill_in_place(self):
        # $ opens the skills picker, then REOPENS the input bar with the picked "$skill "
        # prefilled so the operator can compose (chain skills / add a query) before Enter.
        # side_effect: first read yields the $ trigger; the reopened read yields the final line.
        with mock.patch.object(
            nx_slash_menu, "_read_input_bar",
            side_effect=[("", "$"), ("$cold_outreach draft it", None)],
        ) as read_bar:
            with mock.patch.object(
                nx_slash_menu, "run_skills_menu", return_value="$cold_outreach"
            ) as skills_menu:
                result = nx_slash_menu.slash_input()

        self.assertEqual(result, "$cold_outreach draft it")
        skills_menu.assert_called_once_with("cowork")
        # the reopened bar was seeded with the picked skill (prefill is the 4th positional arg)
        self.assertEqual(read_bar.call_count, 2)
        self.assertIn("$cold_outreach", read_bar.call_args.args[3])

    def test_active_skills_appear_in_the_status_footer(self):
        # The footer under the input carries the full world · Mode label, cwd + skills.
        footer = nx_slash_menu._footer_text("cowork", "", ["$cold_outreach"])
        self.assertIn("nx", footer)
        self.assertIn("cowork · Partner", footer)   # full words, not the old cryptic "C·P"
        self.assertIn("$cold_outreach", footer)

    def test_world_menu_render_no_raw_ansi_and_scrolls(self):
        # Issue 1: the active-world dot must be a styled fragment, never raw ANSI escapes
        # embedded in the (style, text) tuple — prompt_toolkit renders those literally
        # ("^[[38;2;200;164;74m●^[[0m" leak). Issue 2: the render must scroll-window so the
        # SELECTED row stays visible even when it's near the bottom on a short pane.
        rows = nx_slash_menu._world_menu_rows()
        world_idx = [i for i, r in enumerate(rows) if r["type"] == "world"]
        last = world_idx[-1]  # the bottom-most world (AGENT group)
        lines = nx_slash_menu._world_menu_lines(rows, cur="cowork", selected=last, limit=8)
        joined_text = "".join(text for _style, text in lines)
        self.assertNotIn("\033", joined_text)   # no raw escape bytes anywhere
        self.assertNotIn("[38;2", joined_text)  # nor the visible remnant of one
        # the selected bottom world is on screen (viewport followed the cursor)
        self.assertIn(rows[last]["name"], joined_text)
        # NOTE: whether the ACTIVE world's dot is visible here depends on the scroll window —
        # when the viewport follows the cursor to the bottom, the active world (cowork, near the
        # top) can scroll off, so we don't assert its dot here. The dot-renders-as-a-gold-fragment
        # guarantee is covered directly by test_world_menu_active_dot_is_gold_fragment below.

    def test_world_menu_active_dot_is_gold_fragment(self):
        rows = nx_slash_menu._world_menu_rows()
        # select a NON-active row so the active dot isn't merged into the selected-row style
        lines = nx_slash_menu._world_menu_lines(rows, cur="cowork", selected=999, limit=100)
        dot_frags = [(s, t) for s, t in lines if t == "● "]
        self.assertTrue(dot_frags, "there should be one active dot fragment")
        self.assertEqual(dot_frags[0][0], "class:gold")   # gold, and a real fragment

    def test_slash_input_skills_result_from_slash_menu_composes_in_place(self):
        # / → /skills picks a skill, then REOPENS the bar with "$skill " prefilled (compose in
        # place — same as the $ trigger). side_effect terminates the reopen with the final line.
        with mock.patch.object(
            nx_slash_menu, "_read_input_bar",
            side_effect=[("", "/"), ("$brain what did we decide", None)],
        ) as read_bar:
            with mock.patch.object(
                nx_slash_menu, "_run_prompt_toolkit_menu", return_value="/skills"
            ) as slash_menu:
                with mock.patch.object(
                    nx_slash_menu, "run_skills_menu", return_value="$brain"
                ) as skills_menu:
                    result = nx_slash_menu.slash_input()

        self.assertEqual(result, "$brain what did we decide")
        slash_menu.assert_called_once_with("cowork")
        skills_menu.assert_called_once_with("cowork")
        self.assertEqual(read_bar.call_count, 2)
        self.assertIn("$brain", read_bar.call_args.args[3])

    def test_slash_input_reads_regular_text_without_menu(self):
        with mock.patch.object(nx_slash_menu, "_read_input_bar", return_value=("hello", None)):
            result = nx_slash_menu.slash_input()

        self.assertEqual(result, "hello")

    def test_read_first_char_uses_non_tty_fallback(self):
        with mock.patch.object(nx_slash_menu.sys.stdin, "fileno", return_value=0):
            with mock.patch.object(nx_slash_menu.os, "isatty", return_value=False):
                with mock.patch.object(nx_slash_menu.sys.stdin, "read", return_value="/"):
                    result = nx_slash_menu._read_first_char()

        self.assertEqual(result, "/")

    def test_rendered_menu_does_not_show_overflow_count_line(self):
        display_items = [
            {"type": "cmd", "cmd": f"/cmd-{index}", "desc": f"Description {index}"}
            for index in range(25)
        ]
        state = {"selected": 0, "filter": ""}

        rendered = nx_slash_menu._build_menu_text(display_items, state)
        text = "".join(fragment for _, fragment in rendered)

        self.assertNotIn("35 more", text)
        self.assertNotIn("... ", text)
        self.assertIn("type to filter", text)

    def test_rendered_menu_uses_desc_style_for_non_selected_descriptions(self):
        display_items = [
            {"type": "cmd", "cmd": "/help", "desc": "Show all commands"},
            {"type": "cmd", "cmd": "/skills", "desc": "Browse NX skills"},
        ]
        state = {"selected": 0, "filter": ""}

        rendered = nx_slash_menu._build_menu_text(display_items, state)

        self.assertIn(("class:dim", "    /skills                       "), rendered)
        self.assertIn(("class:desc", "Browse NX skills\n"), rendered)

    def test_rendered_menu_defaults_selection_to_first_command_after_header(self):
        display_items = nx_slash_menu._build_display_items("")
        state = {"selected": 0, "filter": ""}

        rendered = nx_slash_menu._build_menu_text(display_items, state)

        self.assertEqual(state["selected"], 1)
        self.assertIn(("class:selected", "  ❯ /help                         Show all commands\n"), rendered)

    def test_rendered_menu_uses_selected_style_token_for_selected_row(self):
        display_items = [
            {"type": "cmd", "cmd": "/help", "desc": "Show all commands"},
            {"type": "cmd", "cmd": "/skills", "desc": "Browse NX skills"},
        ]
        state = {"selected": 0, "filter": ""}

        rendered = nx_slash_menu._build_menu_text(display_items, state)

        self.assertIn(("class:selected", "  ❯ /help                         Show all commands\n"), rendered)
        self.assertNotIn(("class:current", "  ❯ /help                         Show all commands\n"), rendered)

    def test_build_integrations_menu_items_prioritize_active_world(self):
        registry = {
            "github": {
                "worlds": ["code", "product"],
                "description": "Repos, PRs, issues - 26 tools",
                "tools_count": 26,
            },
            "slack": {
                "worlds": ["cowork", "ops"],
                "description": "Messages, channels, search",
                "tools_count": 30,
            },
            "stripe": {
                "worlds": ["finance", "sales"],
                "description": "Billing, payments, subscriptions",
                "tools_count": 100,
            },
        }

        items = nx_slash_menu._build_integrations_menu_items(registry, active_world="cowork")
        headers = [item["title"] for item in items if item["type"] == "header"]

        # The menu now shows the FULL connectable catalog (so you can connect anything), grouped by category
        # with the ACTIVE world's category prioritized to the front — that prioritization is the contract here.
        self.assertEqual(headers[0], "COWORK", "active world's category must lead")
        for w in ("CODE", "FINANCE"):
            self.assertIn(w, headers)
        # and a different active world leads with its own category (proves it's real prioritization, not order luck)
        alt = [i["title"] for i in nx_slash_menu._build_integrations_menu_items(registry, active_world="finance")
               if i["type"] == "header"]
        self.assertEqual(alt[0], "FINANCE")

    def test_every_item_reachable_on_short_terminal(self):
        # Regression: a fixed 20-row window overflowed short panes; the bottom
        # got clipped and items between Airtable→Notion were unreachable. Every
        # selectable row must be visible when selected, even at a tiny limit.
        import nx_mcp_oauth as _M
        from nx_slash_menu import (_build_integrations_menu_items,
                                   _build_integrations_menu_text)
        items = _build_integrations_menu_items(_M.menu_registry(), active_world="sales")
        int_idx = [i for i, it in enumerate(items) if it.get("type") == "integration"]
        self.assertGreater(len(int_idx), 30)
        for sel in int_idx:
            rendered = _build_integrations_menu_text(
                items, {"selected": sel, "filter": ""},
                total_integrations=len(items), total_tools=0, limit=10)
            txt = "".join(t for _, t in rendered)
            self.assertIn(items[sel]["name"][:22], txt,
                          f"{items[sel]['name']} hidden when selected (limit=10)")

    def test_build_integrations_menu_text_uses_desc_style_and_footer(self):
        display_items = [
            {"type": "header", "title": "COWORK"},
            {
                "type": "integration",
                "name": "slack",
                "tools": 30,
                "desc": "Messages, channels, search",
            },
            {
                "type": "integration",
                "name": "notion",
                "tools": 12,
                "desc": "Docs, tasks, wiki",
            },
        ]
        state = {"selected": 1, "filter": ""}

        rendered = nx_slash_menu._build_integrations_menu_text(display_items, state, total_integrations=2, total_tools=42)
        text = "".join(fragment for _, fragment in rendered)

        self.assertIn("INTEGRATIONS", text)
        self.assertIn("2 integrations", text)
        self.assertIn("42 tools", text)
        self.assertIn(("class:dim", "    notion                    12 tools   "), rendered)
        self.assertIn(("class:desc", "Docs, tasks, wiki\n"), rendered)

    def test_build_integrations_menu_text_uses_foreground_only_style_token_for_selected_row(self):
        display_items = [
            {"type": "header", "title": "COWORK"},
            {
                "type": "integration",
                "name": "slack",
                "tools": 30,
                "desc": "Messages, channels, search",
            },
        ]
        state = {"selected": 1, "filter": ""}

        rendered = nx_slash_menu._build_integrations_menu_text(display_items, state, total_integrations=1, total_tools=30)

        self.assertIn(("class:current", "  ❯ slack                     30 tools   Messages, channels, search\n"), rendered)
        self.assertNotIn(("class:selected", "  ❯ slack                     30 tools   Messages, channels, search\n"), rendered)

    def test_run_integrations_menu_uses_full_screen_application(self):
        registry = {
            "slack": {
                "worlds": ["cowork"],
                "description": "Messages, channels, search",
                "tools_count": 30,
            }
        }
        app_instance = mock.Mock()
        app_instance.run.return_value = "slack"

        with mock.patch("prompt_toolkit.application.Application", return_value=app_instance) as application:
            result = nx_slash_menu.run_integrations_menu(registry, active_world="cowork")

        self.assertEqual(result, "slack")
        self.assertEqual(application.call_args.kwargs["full_screen"], True)
        self.assertEqual(application.call_args.kwargs["mouse_support"], True)


if __name__ == "__main__":
    unittest.main()
