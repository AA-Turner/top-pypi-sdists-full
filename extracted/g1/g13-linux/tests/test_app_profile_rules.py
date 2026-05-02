"""Tests for AppProfileRulesManager and related classes."""

import json
from unittest.mock import patch


class TestAppProfileRule:
    """Tests for AppProfileRule dataclass."""

    def test_rule_creation(self):
        """Test creating a rule."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="EVE Online",
            pattern="EVE -",
            match_type="window_name",
            profile_name="eve_online",
            enabled=True,
        )

        assert rule.name == "EVE Online"
        assert rule.pattern == "EVE -"
        assert rule.match_type == "window_name"
        assert rule.profile_name == "eve_online"
        assert rule.enabled is True

    def test_rule_matches_window_name(self):
        """Test matching against window name."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="EVE",
            pattern="EVE -",
            match_type="window_name",
            profile_name="eve",
        )

        assert rule.matches("EVE - Tranquility", "eve") is True
        assert rule.matches("Firefox", "firefox") is False

    def test_rule_matches_wm_class(self):
        """Test matching against WM_CLASS."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Firefox",
            pattern="firefox",
            match_type="wm_class",
            profile_name="browser",
        )

        assert rule.matches("Some Page", "firefox") is True
        assert rule.matches("firefox", "chromium") is False

    def test_rule_matches_both(self):
        """Test matching against both name and class."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Code",
            pattern="code",
            match_type="both",
            profile_name="coding",
        )

        assert rule.matches("Visual Studio Code", "electron") is True
        assert rule.matches("Other App", "code") is True
        assert rule.matches("Other", "electron") is False

    def test_rule_matches_case_insensitive(self):
        """Test case-insensitive matching."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Firefox",
            pattern="FIREFOX",
            match_type="wm_class",
            profile_name="browser",
        )

        assert rule.matches("Page", "firefox") is True
        assert rule.matches("Page", "Firefox") is True

    def test_rule_disabled_no_match(self):
        """Test disabled rule doesn't match."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Disabled",
            pattern=".*",
            match_type="window_name",
            profile_name="any",
            enabled=False,
        )

        assert rule.matches("Anything", "anything") is False

    def test_rule_invalid_regex_no_match(self):
        """Test invalid regex doesn't match."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Bad Regex",
            pattern="[invalid",
            match_type="window_name",
            profile_name="any",
        )

        assert rule.matches("anything", "anything") is False

    def test_rule_unknown_match_type(self):
        """Test unknown match_type doesn't match."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Unknown",
            pattern="test",
            match_type="unknown",
            profile_name="any",
        )

        assert rule.matches("test", "test") is False

    def test_rule_to_dict(self):
        """Test converting rule to dict."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule(
            name="Test",
            pattern="test",
            match_type="window_name",
            profile_name="profile1",
            enabled=False,
        )

        d = rule.to_dict()
        assert d["name"] == "Test"
        assert d["pattern"] == "test"
        assert d["match_type"] == "window_name"
        assert d["profile_name"] == "profile1"
        assert d["enabled"] is False

    def test_rule_from_dict(self):
        """Test creating rule from dict."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        data = {
            "name": "Test",
            "pattern": "test",
            "match_type": "wm_class",
            "profile_name": "profile1",
            "enabled": True,
        }

        rule = AppProfileRule.from_dict(data)
        assert rule.name == "Test"
        assert rule.pattern == "test"
        assert rule.match_type == "wm_class"
        assert rule.profile_name == "profile1"
        assert rule.enabled is True

    def test_rule_from_dict_defaults(self):
        """Test creating rule from dict with missing fields."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule

        rule = AppProfileRule.from_dict({})

        assert rule.name == "Unnamed Rule"
        assert rule.pattern == ""
        assert rule.match_type == "window_name"
        assert rule.profile_name == ""
        assert rule.enabled is True


class TestAppProfileConfig:
    """Tests for AppProfileConfig dataclass."""

    def test_config_creation_empty(self):
        """Test creating empty config."""
        from g13_linux.gui.models.app_profile_rules import AppProfileConfig

        config = AppProfileConfig()

        assert config.rules == []
        assert config.default_profile is None
        assert config.enabled is True

    def test_config_to_dict(self):
        """Test converting config to dict."""
        from g13_linux.gui.models.app_profile_rules import AppProfileConfig, AppProfileRule

        config = AppProfileConfig(
            rules=[AppProfileRule("Test", "test", "window_name", "profile1")],
            default_profile="default",
            enabled=False,
        )

        d = config.to_dict()
        assert len(d["rules"]) == 1
        assert d["default_profile"] == "default"
        assert d["enabled"] is False

    def test_config_from_dict(self):
        """Test creating config from dict."""
        from g13_linux.gui.models.app_profile_rules import AppProfileConfig

        data = {
            "rules": [
                {
                    "name": "Test",
                    "pattern": "test",
                    "match_type": "window_name",
                    "profile_name": "p1",
                }
            ],
            "default_profile": "default",
            "enabled": True,
        }

        config = AppProfileConfig.from_dict(data)
        assert len(config.rules) == 1
        assert config.rules[0].name == "Test"
        assert config.default_profile == "default"
        assert config.enabled is True


class TestAppProfileRulesManager:
    """Tests for AppProfileRulesManager."""

    def test_manager_init_no_file(self, qapp, tmp_path):
        """Test manager with no config file."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        assert manager.rules == []
        assert manager.default_profile is None
        assert manager.enabled is True

    def test_manager_load_existing_config(self, qapp, tmp_path):
        """Test loading existing config file."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        config_path.write_text(
            json.dumps(
                {
                    "rules": [
                        {
                            "name": "Test",
                            "pattern": "test",
                            "match_type": "window_name",
                            "profile_name": "p1",
                        }
                    ],
                    "default_profile": "default",
                    "enabled": False,
                }
            )
        )

        manager = AppProfileRulesManager(config_path=config_path)

        assert len(manager.rules) == 1
        assert manager.default_profile == "default"
        assert manager.enabled is False

    def test_manager_load_invalid_json(self, qapp, tmp_path):
        """Test loading invalid JSON config."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        config_path.write_text("invalid json {{{")

        manager = AppProfileRulesManager(config_path=config_path)

        assert manager.rules == []
        assert manager.enabled is True

    def test_manager_save(self, qapp, tmp_path):
        """Test saving config to file."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        rule = AppProfileRule("Test", "test", "window_name", "profile1")
        manager.add_rule(rule)

        # Verify file was saved
        assert config_path.exists()
        data = json.loads(config_path.read_text())
        assert len(data["rules"]) == 1

    def test_manager_enabled_property(self, qapp, tmp_path):
        """Test enabled property setter."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.enabled = False

        assert manager.enabled is False
        assert len(changes) == 1

    def test_manager_default_profile_property(self, qapp, tmp_path):
        """Test default_profile property setter."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.default_profile = "new_default"

        assert manager.default_profile == "new_default"
        assert len(changes) == 1

    def test_manager_match_first_rule_wins(self, qapp, tmp_path):
        """Test that first matching rule wins."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("Firefox", "firefox", "wm_class", "browser1"))
        manager.add_rule(AppProfileRule("Firefox2", "firefox", "wm_class", "browser2"))

        result = manager.match("Firefox", "firefox")
        assert result == "browser1"

    def test_manager_match_default_profile(self, qapp, tmp_path):
        """Test that default profile is used when no match."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)
        manager.default_profile = "default_profile"

        result = manager.match("Unknown", "unknown")
        assert result == "default_profile"

    def test_manager_match_no_default(self, qapp, tmp_path):
        """Test that None is returned when no match and no default."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        result = manager.match("Unknown", "unknown")
        assert result is None

    def test_manager_match_disabled(self, qapp, tmp_path):
        """Test that match returns None when disabled."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)
        manager.enabled = False
        manager.add_rule(AppProfileRule("Any", ".*", "window_name", "any"))

        result = manager.match("Anything", "anything")
        assert result is None

    def test_manager_on_window_changed_emits_signal(self, qapp, tmp_path):
        """Test on_window_changed emits profile_switch_requested."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)
        manager.add_rule(AppProfileRule("EVE", "EVE", "window_name", "eve_profile"))

        switches = []
        manager.profile_switch_requested.connect(lambda p: switches.append(p))

        manager.on_window_changed("123", "EVE - Tranquility", "eve")

        assert len(switches) == 1
        assert switches[0] == "eve_profile"

    def test_manager_on_window_changed_no_double_emit(self, qapp, tmp_path):
        """Test on_window_changed doesn't emit twice for same profile."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)
        manager.add_rule(AppProfileRule("EVE", "EVE", "window_name", "eve_profile"))

        switches = []
        manager.profile_switch_requested.connect(lambda p: switches.append(p))

        manager.on_window_changed("123", "EVE - Tranquility", "eve")
        manager.on_window_changed("456", "EVE - Jita", "eve")  # Different window, same profile

        assert len(switches) == 1

    def test_manager_on_window_changed_no_match(self, qapp, tmp_path):
        """Test on_window_changed with no matching rule."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        switches = []
        manager.profile_switch_requested.connect(lambda p: switches.append(p))

        manager.on_window_changed("123", "Unknown", "unknown")

        assert len(switches) == 0

    def test_manager_add_rule_at_index(self, qapp, tmp_path):
        """Test adding rule at specific index."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))
        manager.add_rule(AppProfileRule("Third", "3", "window_name", "p3"))
        manager.add_rule(AppProfileRule("Second", "2", "window_name", "p2"), index=1)

        assert manager.rules[0].name == "First"
        assert manager.rules[1].name == "Second"
        assert manager.rules[2].name == "Third"

    def test_manager_remove_rule(self, qapp, tmp_path):
        """Test removing a rule."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))
        manager.add_rule(AppProfileRule("Second", "2", "window_name", "p2"))

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.remove_rule(0)

        assert len(manager.rules) == 1
        assert manager.rules[0].name == "Second"
        assert len(changes) == 1

    def test_manager_remove_rule_invalid_index(self, qapp, tmp_path):
        """Test removing rule with invalid index."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.remove_rule(99)  # Invalid index

        assert len(changes) == 0

    def test_manager_update_rule(self, qapp, tmp_path):
        """Test updating a rule."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("Old", "old", "window_name", "old_p"))

        new_rule = AppProfileRule("New", "new", "wm_class", "new_p")
        manager.update_rule(0, new_rule)

        assert manager.rules[0].name == "New"
        assert manager.rules[0].pattern == "new"

    def test_manager_update_rule_invalid_index(self, qapp, tmp_path):
        """Test updating rule with invalid index."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        new_rule = AppProfileRule("New", "new", "wm_class", "new_p")

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.update_rule(99, new_rule)  # Invalid index

        assert len(changes) == 0

    def test_manager_move_rule(self, qapp, tmp_path):
        """Test moving a rule."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))
        manager.add_rule(AppProfileRule("Second", "2", "window_name", "p2"))
        manager.add_rule(AppProfileRule("Third", "3", "window_name", "p3"))

        manager.move_rule(0, 2)

        assert manager.rules[0].name == "Second"
        assert manager.rules[1].name == "Third"
        assert manager.rules[2].name == "First"

    def test_manager_move_rule_invalid_index(self, qapp, tmp_path):
        """Test moving rule with invalid index."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule, AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        manager = AppProfileRulesManager(config_path=config_path)

        manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))

        changes = []
        manager.rules_changed.connect(lambda: changes.append(True))

        manager.move_rule(0, 99)  # Invalid destination

        assert len(changes) == 0

    def test_manager_save_error_handling(self, qapp, tmp_path):
        """Test save handles errors gracefully."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        # Use a path that can't be written to
        config_path = tmp_path / "nonexistent_dir" / "subdir" / "app_profiles.json"

        manager = AppProfileRulesManager(config_path=config_path)

        # Mock open to raise an error
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            # Should not raise
            manager.save()
