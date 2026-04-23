"""Tests for hook config schema, trust boundary, and reload semantics (#1489)."""

from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import yaml

from anteroom.config import (
    HookEntryConfig,
    HookMatcherConfig,
    HookRunnerConfig,
    HooksConfig,
    _build_hooks_config,
    _is_int_like,
    _parse_hook_entries,
    load_config,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_MINIMAL_AI = {"ai": {"base_url": "https://api.example.com", "api_key": "sk-test"}}


def _write_config(path: Path, data: dict) -> Path:
    cfg_file = path / "config.yaml"
    cfg_file.write_text(yaml.dump(data))
    return cfg_file


def _minimal(tmp_path: Path, extra: dict | None = None) -> Path:
    data: dict = dict(_MINIMAL_AI)
    if extra:
        data = {**data, **extra}
    return _write_config(tmp_path, data)


# ---------------------------------------------------------------------------
# HookMatcherConfig
# ---------------------------------------------------------------------------


class TestHookMatcherConfig:
    def test_defaults(self) -> None:
        m = HookMatcherConfig()
        assert m.tool_name == "*"
        assert m.arguments == {}

    def test_custom_values(self) -> None:
        m = HookMatcherConfig(tool_name="bash", arguments={"cmd": "ls"})
        assert m.tool_name == "bash"
        assert m.arguments == {"cmd": "ls"}


# ---------------------------------------------------------------------------
# HookRunnerConfig
# ---------------------------------------------------------------------------


class TestHookRunnerConfig:
    def test_defaults(self) -> None:
        r = HookRunnerConfig()
        assert r.type == "command"
        assert r.command == ""
        assert r.url == ""
        assert r.timeout == 5

    def test_invalid_type_defaults_to_command(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            r = HookRunnerConfig(type="invalid")
        assert r.type == "command"
        assert "invalid" in caplog.text

    def test_timeout_clamped_to_minimum(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            r = HookRunnerConfig(timeout=0)
        assert r.timeout == 1
        assert "below minimum" in caplog.text

    def test_timeout_clamped_to_maximum(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            r = HookRunnerConfig(timeout=999)
        assert r.timeout == 30
        assert "above maximum" in caplog.text

    def test_valid_webhook_type(self) -> None:
        r = HookRunnerConfig(type="webhook", url="http://localhost/hook")
        assert r.type == "webhook"

    def test_timeout_at_boundary_min(self) -> None:
        r = HookRunnerConfig(timeout=1)
        assert r.timeout == 1

    def test_timeout_at_boundary_max(self) -> None:
        r = HookRunnerConfig(timeout=30)
        assert r.timeout == 30


# ---------------------------------------------------------------------------
# HookEntryConfig
# ---------------------------------------------------------------------------


class TestHookEntryConfig:
    def test_defaults(self) -> None:
        e = HookEntryConfig()
        assert e.id == ""
        assert e.event == "pre_tool"
        assert e.trust_source == "personal"
        assert e.message == ""
        assert isinstance(e.matcher, HookMatcherConfig)
        assert isinstance(e.runner, HookRunnerConfig)

    def test_invalid_event_defaults_to_pre_tool(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            e = HookEntryConfig(event="on_click")
        assert e.event == "pre_tool"
        assert "on_click" in caplog.text

    def test_is_executable_personal(self) -> None:
        e = HookEntryConfig(id="h1", trust_source="personal")
        assert e.is_executable is True

    def test_is_executable_team(self) -> None:
        e = HookEntryConfig(id="h1", trust_source="team")
        assert e.is_executable is True

    def test_is_executable_pack_false(self) -> None:
        e = HookEntryConfig(id="h1", trust_source="pack")
        assert e.is_executable is False

    def test_is_executable_unknown_source_false(self) -> None:
        e = HookEntryConfig(id="h1", trust_source="unknown")
        assert e.is_executable is False

    def test_post_tool_event_valid(self) -> None:
        e = HookEntryConfig(event="post_tool")
        assert e.event == "post_tool"


# ---------------------------------------------------------------------------
# _is_int_like
# ---------------------------------------------------------------------------


class TestIsIntLike:
    def test_int_is_int_like(self) -> None:
        assert _is_int_like(5) is True

    def test_string_int_is_int_like(self) -> None:
        assert _is_int_like("10") is True

    def test_float_is_not_int_like(self) -> None:
        assert _is_int_like(3.5) is False

    def test_string_float_is_not_int_like(self) -> None:
        assert _is_int_like("3.5") is False

    def test_empty_string_is_not_int_like(self) -> None:
        assert _is_int_like("") is False

    def test_none_is_not_int_like(self) -> None:
        assert _is_int_like(None) is False


# ---------------------------------------------------------------------------
# _parse_hook_entries
# ---------------------------------------------------------------------------


class TestParseHookEntries:
    def test_empty_list(self) -> None:
        assert _parse_hook_entries([], "pre_tool", "personal", {}) == []

    def test_not_a_list_returns_empty(self) -> None:
        assert _parse_hook_entries("not_a_list", "pre_tool", "personal", {}) == []  # type: ignore[arg-type]

    def test_skips_non_dict_items(self) -> None:
        result = _parse_hook_entries(["bad", 42], "pre_tool", "personal", {})
        assert result == []

    def test_skips_entry_missing_id(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            result = _parse_hook_entries([{"runner": {"command": "echo hi"}}], "pre_tool", "personal", {})
        assert result == []
        assert "missing 'id'" in caplog.text

    def test_skips_entry_with_empty_id(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            result = _parse_hook_entries([{"id": ""}], "pre_tool", "personal", {})
        assert result == []
        assert "missing 'id'" in caplog.text

    def test_parses_minimal_entry(self) -> None:
        raw = [{"id": "h1", "runner": {"command": "echo hi"}}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert len(result) == 1
        assert result[0].id == "h1"
        assert result[0].trust_source == "personal"
        assert result[0].runner.command == "echo hi"

    def test_dedup_first_wins(self, caplog: pytest.LogCaptureFixture) -> None:
        seen: dict[str, str] = {"h1": "personal"}
        raw = [{"id": "h1", "runner": {"command": "second"}}]
        with caplog.at_level(logging.DEBUG):
            result = _parse_hook_entries(raw, "pre_tool", "pack", seen)
        assert result == []

    def test_updates_seen_ids(self) -> None:
        seen: dict[str, str] = {}
        raw = [{"id": "h1", "runner": {"command": "x"}}]
        _parse_hook_entries(raw, "pre_tool", "personal", seen)
        assert seen == {"h1": "personal"}

    def test_matcher_parsed(self) -> None:
        raw = [{"id": "h1", "matcher": {"tool_name": "bash", "arguments": {"a": "b"}}}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert result[0].matcher.tool_name == "bash"
        assert result[0].matcher.arguments == {"a": "b"}

    def test_invalid_matcher_not_dict_falls_back(self) -> None:
        raw = [{"id": "h1", "matcher": "bad"}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert result[0].matcher.tool_name == "*"

    def test_matcher_arguments_non_dict_does_not_crash(self) -> None:
        """Regression: a non-dict ``arguments`` value (e.g. a YAML list or
        scalar) must not raise AttributeError during parse.  The parser
        previously called ``.items()`` on whatever was provided and
        crashed on lists/strings.  It should quietly fall back to ``{}``.
        """
        # Simulates YAML like `arguments: [foo, bar]` or `arguments: bad`
        for bad_args in (["a", "b"], "bad", 42, None):
            raw = [{"id": "h1", "matcher": {"tool_name": "bash", "arguments": bad_args}}]
            result = _parse_hook_entries(raw, "pre_tool", "personal", {})
            assert len(result) == 1
            assert result[0].matcher.arguments == {}
            assert result[0].matcher.tool_name == "bash"

    def test_webhook_runner_parsed(self) -> None:
        raw = [{"id": "h1", "runner": {"type": "webhook", "url": "http://host/hook", "timeout": 10}}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert result[0].runner.type == "webhook"
        assert result[0].runner.url == "http://host/hook"
        assert result[0].runner.timeout == 10

    def test_non_int_timeout_defaults_to_five(self) -> None:
        raw = [{"id": "h1", "runner": {"command": "x", "timeout": "bad"}}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert result[0].runner.timeout == 5

    def test_message_field(self) -> None:
        raw = [{"id": "h1", "message": "please confirm", "runner": {"command": "x"}}]
        result = _parse_hook_entries(raw, "pre_tool", "personal", {})
        assert result[0].message == "please confirm"


# ---------------------------------------------------------------------------
# _build_hooks_config
# ---------------------------------------------------------------------------


class TestBuildHooksConfig:
    def test_empty_raw(self) -> None:
        cfg = _build_hooks_config({})
        assert cfg.pre_tool == []
        assert cfg.post_tool == []

    def test_hooks_key_not_dict_ignored(self) -> None:
        cfg = _build_hooks_config({"hooks": "bad"})
        assert cfg.pre_tool == []

    def test_personal_hooks_parsed(self) -> None:
        raw = {
            "hooks": {
                "pre_tool": [{"id": "h1", "runner": {"command": "x"}}],
                "post_tool": [{"id": "h2", "runner": {"command": "y"}}],
            }
        }
        cfg = _build_hooks_config(raw)
        assert len(cfg.pre_tool) == 1
        assert len(cfg.post_tool) == 1
        assert cfg.pre_tool[0].trust_source == "personal"
        assert cfg.post_tool[0].trust_source == "personal"

    def test_pack_hooks_parsed_as_non_executable(self, caplog: pytest.LogCaptureFixture) -> None:
        personal_raw: dict = {"hooks": {}}
        pack_raw = {"hooks": {"pre_tool": [{"id": "pack-h1", "runner": {"command": "x"}}]}}
        with caplog.at_level(logging.INFO):
            cfg = _build_hooks_config(personal_raw, pack_raw=pack_raw)
        assert len(cfg.pre_tool) == 1
        assert cfg.pre_tool[0].trust_source == "pack"
        assert cfg.pre_tool[0].is_executable is False
        assert "NOT executable" in caplog.text

    def test_personal_wins_over_pack_on_id_collision(self) -> None:
        """When the caller supplies an explicit personal view that shares an
        id with a pack, the personal entry wins AND retains its personal
        trust source (executable).  Without ``personal_raw`` the function
        has no way to distinguish a legitimate override from a pack-bubbled
        entry, so this call form is the safe one for operator overrides.
        """
        personal_raw = {"hooks": {"pre_tool": [{"id": "shared", "runner": {"command": "personal"}}]}}
        pack_raw = {"hooks": {"pre_tool": [{"id": "shared", "runner": {"command": "pack"}}]}}
        cfg = _build_hooks_config(personal_raw, pack_raw=pack_raw, personal_raw=personal_raw)
        assert len(cfg.pre_tool) == 1
        assert cfg.pre_tool[0].runner.command == "personal"
        assert cfg.pre_tool[0].trust_source == "personal"

    def test_pack_bubble_into_raw_stays_pack_when_no_personal_snapshot(self) -> None:
        """Regression for the phase-1 trust-boundary hole: when personal
        config declares no hooks, ``deep_merge(pack, personal)`` bubbles
        the pack hook list into the merged ``raw`` dict.  If the caller
        has no access to the pre-merge personal view, any id that is also
        declared in ``pack_raw`` must be tagged with ``trust_source="pack"``
        so it is not silently promoted to executable.
        """
        # Simulate what load_config sees after deep_merge(pack, personal)
        # when personal declares no hooks: the pack hook list shows up in
        # the merged dict verbatim.
        pack_raw = {"hooks": {"pre_tool": [{"id": "pack-h1", "runner": {"command": "x"}}]}}
        merged_raw = {"hooks": {"pre_tool": pack_raw["hooks"]["pre_tool"]}}  # pyright: ignore[reportGeneralTypeIssues]

        # Old-style call without personal_raw: guard tags shared ids as pack.
        cfg = _build_hooks_config(merged_raw, pack_raw=pack_raw)
        assert len(cfg.pre_tool) == 1
        assert cfg.pre_tool[0].id == "pack-h1"
        assert cfg.pre_tool[0].trust_source == "pack"
        assert cfg.pre_tool[0].is_executable is False

    def test_pack_bubble_into_raw_with_empty_personal_snapshot(self) -> None:
        """New-style call with an explicit (empty) personal snapshot.  The
        pack's entry must not surface via the trusted parse, and only the
        pack-source parse contributes it — as a non-executable entry."""
        pack_raw = {"hooks": {"pre_tool": [{"id": "pack-h1", "runner": {"command": "x"}}]}}
        merged_raw = {"hooks": {"pre_tool": pack_raw["hooks"]["pre_tool"]}}  # pyright: ignore[reportGeneralTypeIssues]
        personal_snapshot: dict = {}  # personal declared no hooks at all

        cfg = _build_hooks_config(merged_raw, pack_raw=pack_raw, personal_raw=personal_snapshot)
        assert len(cfg.pre_tool) == 1
        assert cfg.pre_tool[0].id == "pack-h1"
        assert cfg.pre_tool[0].trust_source == "pack"
        assert cfg.pre_tool[0].is_executable is False

    def test_pack_raw_none_ok(self) -> None:
        raw = {"hooks": {"pre_tool": [{"id": "h1", "runner": {"command": "x"}}]}}
        cfg = _build_hooks_config(raw, pack_raw=None)
        assert len(cfg.pre_tool) == 1

    def test_pack_hooks_key_missing_ok(self) -> None:
        pack_raw: dict = {}
        cfg = _build_hooks_config({}, pack_raw=pack_raw)
        assert cfg.pre_tool == []

    def test_pack_raw_hooks_not_dict_ignored(self) -> None:
        pack_raw = {"hooks": "bad"}
        cfg = _build_hooks_config({}, pack_raw=pack_raw)
        assert cfg.pre_tool == []


# ---------------------------------------------------------------------------
# load_config integration — hooks field on AppConfig
# ---------------------------------------------------------------------------


class TestLoadConfigHooks:
    def test_hooks_absent_gives_empty_config(self, tmp_path: Path) -> None:
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(_MINIMAL_AI))
        config, _ = load_config(cfg_file)
        assert isinstance(config.hooks, HooksConfig)
        assert config.hooks.pre_tool == []
        assert config.hooks.post_tool == []

    def test_hooks_loaded_from_config_file(self, tmp_path: Path) -> None:
        data = {
            **_MINIMAL_AI,
            "hooks": {
                "pre_tool": [{"id": "guard-bash", "runner": {"command": "echo pre"}}],
            },
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        config, _ = load_config(cfg_file)
        assert len(config.hooks.pre_tool) == 1
        assert config.hooks.pre_tool[0].id == "guard-bash"
        assert config.hooks.pre_tool[0].is_executable is True

    def test_hooks_invalid_yaml_type_raises(self, tmp_path: Path) -> None:
        data = {**_MINIMAL_AI, "hooks": "not_a_dict"}
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="hooks must be a mapping"):
            load_config(cfg_file)

    def test_hooks_duplicate_ids_deduplicated(self, tmp_path: Path) -> None:
        data = {
            **_MINIMAL_AI,
            "hooks": {
                "pre_tool": [
                    {"id": "dup", "runner": {"command": "first"}},
                    {"id": "dup", "runner": {"command": "second"}},
                ]
            },
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        config, _ = load_config(cfg_file)
        assert len(config.hooks.pre_tool) == 1
        assert config.hooks.pre_tool[0].runner.command == "first"

    def test_load_config_missing_runner_rejected(self, tmp_path: Path) -> None:
        """Regression: a hook entry with no ``runner`` field must be a
        hard config error.  Before the fix the parser quietly built an
        empty command runner that could never execute, masking the bug.
        """
        data = {**_MINIMAL_AI, "hooks": {"pre_tool": [{"id": "h1"}]}}
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="missing required 'runner'"):
            load_config(cfg_file)

    def test_load_config_non_dict_runner_rejected(self, tmp_path: Path) -> None:
        data = {**_MINIMAL_AI, "hooks": {"pre_tool": [{"id": "h1", "runner": "bad"}]}}
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="runner must be a mapping"):
            load_config(cfg_file)

    def test_load_config_non_dict_matcher_rejected(self, tmp_path: Path) -> None:
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "h1", "matcher": "bad", "runner": {"command": "x"}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="matcher must be a mapping"):
            load_config(cfg_file)

    def test_load_config_bool_timeout_rejected(self, tmp_path: Path) -> None:
        """``timeout: true`` would silently coerce to ``1`` in Python's
        ``int(bool)``; the validator rejects it explicitly."""
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "h1", "runner": {"command": "x", "timeout": True}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="timeout must be an integer"):
            load_config(cfg_file)

    def test_pack_only_hook_stays_non_executable_through_load_config(self, tmp_path: Path) -> None:
        """End-to-end regression for the trust-boundary hole: a pack
        supplies hooks while personal declares none.  After load_config
        the entry must still carry ``trust_source="pack"`` and
        ``is_executable=False``.
        """
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(_MINIMAL_AI))  # personal has no hooks

        pack_config = {"hooks": {"pre_tool": [{"id": "pack-guard", "runner": {"command": "echo pack"}}]}}
        config, _ = load_config(cfg_file, pack_config=pack_config)
        assert len(config.hooks.pre_tool) == 1
        entry = config.hooks.pre_tool[0]
        assert entry.id == "pack-guard"
        assert entry.trust_source == "pack"
        assert entry.is_executable is False

    def test_personal_override_of_pack_id_stays_executable_through_load_config(self, tmp_path: Path) -> None:
        """When personal explicitly declares a hook with the same id as a
        pack hook, the personal entry wins AND stays executable.  This is
        the legitimate override pattern — the snapshot taken before
        deep_merge lets _build_hooks_config tell this apart from a pack
        bubble."""
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "shared", "runner": {"command": "personal"}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))

        pack_config = {"hooks": {"pre_tool": [{"id": "shared", "runner": {"command": "pack"}}]}}
        config, _ = load_config(cfg_file, pack_config=pack_config)
        assert len(config.hooks.pre_tool) == 1
        entry = config.hooks.pre_tool[0]
        assert entry.id == "shared"
        assert entry.runner.command == "personal"
        assert entry.trust_source == "personal"
        assert entry.is_executable is True

    def test_team_hooks_stay_executable_when_personal_has_none(self, tmp_path: Path) -> None:
        """Regression: team is a trusted layer.  Team-declared hooks must
        survive load_config and remain executable even when personal
        declares no hooks.  A naive trust-boundary fix that used only the
        pre-merge personal snapshot would silently drop team hooks.
        """
        personal = tmp_path / "config.yaml"
        personal.write_text(yaml.dump(_MINIMAL_AI))  # no hooks in personal

        team_path = tmp_path / "team.yaml"
        team_content = yaml.dump(
            {
                "hooks": {"pre_tool": [{"id": "team-guard", "runner": {"command": "echo team"}}]},
            }
        )
        team_path.write_text(team_content)

        # Mark team config as trusted so load_team_config doesn't silently
        # drop it in non-interactive mode.
        from anteroom.services.trust import compute_content_hash, save_trust_decision

        data_dir = personal.parent
        content_hash = compute_content_hash(team_content)
        save_trust_decision(str(team_path.resolve()), content_hash, recursive=False, data_dir=data_dir)

        config, _ = load_config(personal, team_config_path=team_path)
        assert len(config.hooks.pre_tool) == 1
        entry = config.hooks.pre_tool[0]
        assert entry.id == "team-guard"
        assert entry.trust_source == "team"
        assert entry.is_executable is True

    def test_team_and_personal_unique_hooks_both_preserved(self, tmp_path: Path) -> None:
        """Regression: when team and personal each declare unique hooks in
        the same event, both must survive load_config.  ``deep_merge`` would
        replace the hook list wholesale (hooks are a plain list of dicts,
        not name-keyed), silently dropping team policy even though no ids
        collide.  The loader concatenates manually so each side's unique
        ids come through while personal wins on id collision.
        """
        personal = tmp_path / "config.yaml"
        personal.write_text(
            yaml.dump(
                {
                    **_MINIMAL_AI,
                    "hooks": {
                        "pre_tool": [{"id": "personal-guard", "runner": {"command": "echo personal"}}],
                    },
                }
            )
        )

        team_path = tmp_path / "team.yaml"
        team_content = yaml.dump(
            {
                "hooks": {"pre_tool": [{"id": "team-guard", "runner": {"command": "echo team"}}]},
            }
        )
        team_path.write_text(team_content)

        from anteroom.services.trust import compute_content_hash, save_trust_decision

        data_dir = personal.parent
        content_hash = compute_content_hash(team_content)
        save_trust_decision(str(team_path.resolve()), content_hash, recursive=False, data_dir=data_dir)

        config, _ = load_config(personal, team_config_path=team_path)
        by_id = {e.id: e for e in config.hooks.pre_tool}
        assert set(by_id) == {"personal-guard", "team-guard"}
        assert by_id["personal-guard"].trust_source == "personal"
        assert by_id["team-guard"].trust_source == "team"
        assert all(e.is_executable for e in config.hooks.pre_tool)

    def test_team_and_personal_id_collision_personal_wins(self, tmp_path: Path) -> None:
        """Regression: when team and personal declare a hook with the same
        id, personal must win while team-only ids continue to surface."""
        personal = tmp_path / "config.yaml"
        personal.write_text(
            yaml.dump(
                {
                    **_MINIMAL_AI,
                    "hooks": {
                        "pre_tool": [
                            {"id": "shared", "runner": {"command": "PERSONAL"}},
                            {"id": "personal-only", "runner": {"command": "p-only"}},
                        ],
                    },
                }
            )
        )

        team_path = tmp_path / "team.yaml"
        team_content = yaml.dump(
            {
                "hooks": {
                    "pre_tool": [
                        {"id": "shared", "runner": {"command": "TEAM"}},
                        {"id": "team-only", "runner": {"command": "t-only"}},
                    ],
                },
            }
        )
        team_path.write_text(team_content)

        from anteroom.services.trust import compute_content_hash, save_trust_decision

        data_dir = personal.parent
        content_hash = compute_content_hash(team_content)
        save_trust_decision(str(team_path.resolve()), content_hash, recursive=False, data_dir=data_dir)

        config, _ = load_config(personal, team_config_path=team_path)
        by_id = {e.id: e for e in config.hooks.pre_tool}
        assert set(by_id) == {"shared", "personal-only", "team-only"}
        assert by_id["shared"].runner.command == "PERSONAL"
        assert by_id["shared"].trust_source == "personal"
        assert by_id["personal-only"].trust_source == "personal"
        assert by_id["team-only"].trust_source == "team"

    def test_webhook_url_file_scheme_rejected(self, tmp_path: Path) -> None:
        """file:// webhook URLs are rejected at validation time (SSRF/LFI guard)."""
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "h1", "runner": {"type": "webhook", "url": "file:///etc/passwd"}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="http"):
            load_config(cfg_file)

    def test_webhook_url_https_accepted(self, tmp_path: Path) -> None:
        """https:// webhook URLs pass validation."""
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "h1", "runner": {"type": "webhook", "url": "https://hooks.example.com/cb"}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        config, _ = load_config(cfg_file)
        assert config.hooks.pre_tool[0].runner.url == "https://hooks.example.com/cb"

    def test_webhook_url_arbitrary_scheme_rejected(self, tmp_path: Path) -> None:
        """Arbitrary schemes (e.g. ext::) are rejected."""
        data = {
            **_MINIMAL_AI,
            "hooks": {"pre_tool": [{"id": "h1", "runner": {"type": "webhook", "url": "ext::some-cmd"}}]},
        }
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(data))
        with pytest.raises(ValueError, match="http"):
            load_config(cfg_file)


# ---------------------------------------------------------------------------
# ConfigWatcher — reload semantics (session-scoped contract)
# ---------------------------------------------------------------------------


class TestConfigWatcherReloadSemantics:
    """Verify that ConfigWatcher fires on_change but hook config is NOT the
    watcher's concern — the runtime is responsible for ignoring hook changes.

    These tests confirm the watcher's existing behavior is unchanged: it
    calls on_change for valid config changes regardless of content.
    """

    @pytest.mark.asyncio
    async def test_watcher_calls_on_change_for_valid_hook_change(self, tmp_path: Path) -> None:
        from anteroom.services.config_watcher import ConfigWatcher

        initial = {**_MINIMAL_AI, "hooks": {"pre_tool": []}}
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(initial))

        callback = AsyncMock()
        watcher = ConfigWatcher([cfg_file], callback, interval=0.05)

        # Advance mtime so the next check detects a change
        updated = {**_MINIMAL_AI, "hooks": {"pre_tool": [{"id": "h1", "runner": {"command": "x"}}]}}
        cfg_file.write_text(yaml.dump(updated))
        import os

        os.utime(cfg_file, (cfg_file.stat().st_mtime + 1, cfg_file.stat().st_mtime + 1))

        await watcher._check_file(cfg_file)

        callback.assert_awaited_once()
        path_arg, raw_arg = callback.call_args.args
        assert path_arg == cfg_file
        assert isinstance(raw_arg, dict)

    @pytest.mark.asyncio
    async def test_watcher_does_not_call_on_change_when_file_unchanged(self, tmp_path: Path) -> None:
        from anteroom.services.config_watcher import ConfigWatcher

        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text(yaml.dump(_MINIMAL_AI))

        callback = AsyncMock()
        watcher = ConfigWatcher([cfg_file], callback, interval=0.05)

        # Second check with same mtime — no change
        await watcher._check_file(cfg_file)

        callback.assert_not_awaited()
