"""Tests for AppProfilesWidget and RuleEditDialog."""

from unittest.mock import patch

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox


class TestRuleEditDialog:
    """Tests for RuleEditDialog."""

    def test_dialog_init_add_mode(self, qapp):
        """Test dialog initialization in add mode."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1", "profile2"])

        assert dialog.windowTitle() == "Add Rule"
        assert dialog.name_edit.text() == ""
        assert dialog.pattern_edit.text() == ""
        assert dialog.match_type_combo.currentIndex() == 0
        assert dialog.enabled_check.isChecked() is True

    def test_dialog_init_edit_mode(self, qapp):
        """Test dialog initialization in edit mode."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        rule = AppProfileRule(
            name="Test Rule",
            pattern="test.*",
            match_type="wm_class",
            profile_name="profile1",
            enabled=False,
        )

        dialog = RuleEditDialog(rule=rule, profiles=["profile1", "profile2"])

        assert dialog.windowTitle() == "Edit Rule"
        assert dialog.name_edit.text() == "Test Rule"
        assert dialog.pattern_edit.text() == "test.*"
        assert dialog.match_type_combo.currentIndex() == 1  # wm_class
        assert dialog.profile_combo.currentText() == "profile1"
        assert dialog.enabled_check.isChecked() is False

    def test_dialog_init_edit_mode_both_match_type(self, qapp):
        """Test dialog with both match type."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        rule = AppProfileRule(
            name="Test",
            pattern="test",
            match_type="both",
            profile_name="p1",
        )

        dialog = RuleEditDialog(rule=rule, profiles=["p1"])

        assert dialog.match_type_combo.currentIndex() == 2  # both

    def test_dialog_init_edit_mode_profile_not_in_list(self, qapp):
        """Test dialog when profile is not in the list."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        rule = AppProfileRule(
            name="Test",
            pattern="test",
            match_type="window_name",
            profile_name="unknown_profile",
        )

        dialog = RuleEditDialog(rule=rule, profiles=["profile1"])

        # Should set the edit text since profile not found
        assert dialog.profile_combo.currentText() == "unknown_profile"

    def test_get_rule_success(self, qapp):
        """Test getting rule from dialog."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1"])
        dialog.name_edit.setText("My Rule")
        dialog.pattern_edit.setText("my-pattern")
        dialog.match_type_combo.setCurrentIndex(1)  # wm_class
        dialog.profile_combo.setCurrentText("profile1")
        dialog.enabled_check.setChecked(False)

        rule = dialog.get_rule()

        assert rule is not None
        assert rule.name == "My Rule"
        assert rule.pattern == "my-pattern"
        assert rule.match_type == "wm_class"
        assert rule.profile_name == "profile1"
        assert rule.enabled is False

    def test_get_rule_empty_name(self, qapp):
        """Test get_rule returns None for empty name."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1"])
        dialog.name_edit.setText("")
        dialog.pattern_edit.setText("pattern")
        dialog.profile_combo.setCurrentText("profile1")

        rule = dialog.get_rule()
        assert rule is None

    def test_get_rule_empty_pattern(self, qapp):
        """Test get_rule returns None for empty pattern."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1"])
        dialog.name_edit.setText("Name")
        dialog.pattern_edit.setText("")
        dialog.profile_combo.setCurrentText("profile1")

        rule = dialog.get_rule()
        assert rule is None

    def test_get_rule_empty_profile(self, qapp):
        """Test get_rule returns None for empty profile."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=[])
        dialog.name_edit.setText("Name")
        dialog.pattern_edit.setText("pattern")
        dialog.profile_combo.setCurrentText("")

        rule = dialog.get_rule()
        assert rule is None

    def test_get_rule_whitespace_stripped(self, qapp):
        """Test get_rule strips whitespace."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1"])
        dialog.name_edit.setText("  My Rule  ")
        dialog.pattern_edit.setText("  pattern  ")
        dialog.profile_combo.setCurrentText("  profile1  ")

        rule = dialog.get_rule()

        assert rule.name == "My Rule"
        assert rule.pattern == "pattern"
        assert rule.profile_name == "profile1"

    def test_get_rule_match_type_both(self, qapp):
        """Test get_rule with 'both' match type."""
        from g13_linux.gui.views.app_profiles import RuleEditDialog

        dialog = RuleEditDialog(profiles=["profile1"])
        dialog.name_edit.setText("Name")
        dialog.pattern_edit.setText("pattern")
        dialog.match_type_combo.setCurrentIndex(2)  # both
        dialog.profile_combo.setCurrentText("profile1")

        rule = dialog.get_rule()
        assert rule.match_type == "both"


class TestAppProfilesWidget:
    """Tests for AppProfilesWidget."""

    @pytest.fixture
    def rules_manager(self, tmp_path):
        """Create a rules manager for testing."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRulesManager

        config_path = tmp_path / "app_profiles.json"
        return AppProfileRulesManager(config_path=config_path)

    def test_widget_init(self, qapp, rules_manager):
        """Test widget initialization."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["p1", "p2"])

        assert widget.rules_manager == rules_manager
        assert widget.profiles == ["p1", "p2"]
        assert widget.enabled_check is not None
        assert widget.rules_list is not None

    def test_widget_init_empty_profiles(self, qapp, rules_manager):
        """Test widget with empty profiles list."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=None)

        assert widget.profiles == []

    def test_update_status_not_available(self, qapp, rules_manager):
        """Test status when window monitoring not available."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = False
            widget = AppProfilesWidget(rules_manager)

        assert "not available" in widget.status_label.text()
        assert widget.enabled_check.isEnabled() is False

    def test_update_status_enabled(self, qapp, rules_manager):
        """Test status when enabled."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.enabled = True

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        assert "active" in widget.status_label.text()

    def test_update_status_disabled(self, qapp, rules_manager):
        """Test status when disabled."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.enabled = False

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        assert "disabled" in widget.status_label.text()

    def test_refresh_rules_list(self, qapp, rules_manager):
        """Test refreshing the rules list."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Rule1", "r1", "window_name", "p1", enabled=True))
        rules_manager.add_rule(AppProfileRule("Rule2", "r2", "window_name", "p2", enabled=False))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        assert widget.rules_list.count() == 2
        assert "Rule1" in widget.rules_list.item(0).text()
        assert "Rule2" in widget.rules_list.item(1).text()

    def test_on_enabled_toggled(self, qapp, rules_manager):
        """Test enable toggle."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        signals = []
        widget.enabled_changed.connect(lambda v: signals.append(v))

        widget._on_enabled_toggled(True)

        assert rules_manager.enabled is True
        assert len(signals) == 1
        assert signals[0] is True

    def test_on_test_clicked_success(self, qapp, rules_manager):
        """Test test button with successful window detection."""
        from g13_linux.gui.models.window_monitor import WindowInfo
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        mock_info = WindowInfo("123", "Test Window", "test-class")

        with patch(
            "g13_linux.gui.views.app_profiles.get_active_window_info", return_value=mock_info
        ):
            with patch.object(QMessageBox, "information") as mock_msg:
                widget._on_test_clicked()
                mock_msg.assert_called_once()
                call_args = mock_msg.call_args[0]
                assert "Test Window" in call_args[2]

    def test_on_test_clicked_with_match(self, qapp, rules_manager):
        """Test test button when rule matches."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.models.window_monitor import WindowInfo
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Test", "Test", "window_name", "matched_profile"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        mock_info = WindowInfo("123", "Test Window", "test-class")

        with patch(
            "g13_linux.gui.views.app_profiles.get_active_window_info", return_value=mock_info
        ):
            with patch.object(QMessageBox, "information") as mock_msg:
                widget._on_test_clicked()
                call_args = mock_msg.call_args[0]
                assert "matched_profile" in call_args[2]

    def test_on_test_clicked_failure(self, qapp, rules_manager):
        """Test test button with failed window detection."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        with patch("g13_linux.gui.views.app_profiles.get_active_window_info", return_value=None):
            with patch.object(QMessageBox, "warning") as mock_msg:
                widget._on_test_clicked()
                mock_msg.assert_called_once()

    def test_on_add_rule_accepted(self, qapp, rules_manager):
        """Test adding a rule when dialog accepted."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget, RuleEditDialog

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["p1"])

        mock_rule = AppProfileRule("New", "new", "window_name", "p1")

        with patch.object(RuleEditDialog, "exec", return_value=True):
            with patch.object(RuleEditDialog, "get_rule", return_value=mock_rule):
                widget._on_add_rule()

        assert len(rules_manager.rules) == 1
        assert rules_manager.rules[0].name == "New"

    def test_on_add_rule_rejected(self, qapp, rules_manager):
        """Test adding a rule when dialog rejected."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget, RuleEditDialog

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        with patch.object(RuleEditDialog, "exec", return_value=False):
            widget._on_add_rule()

        assert len(rules_manager.rules) == 0

    def test_on_add_rule_none_returned(self, qapp, rules_manager):
        """Test adding a rule when get_rule returns None."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget, RuleEditDialog

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        with patch.object(RuleEditDialog, "exec", return_value=True):
            with patch.object(RuleEditDialog, "get_rule", return_value=None):
                widget._on_add_rule()

        assert len(rules_manager.rules) == 0

    def test_on_edit_clicked_with_selection(self, qapp, rules_manager):
        """Test edit button with item selected."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Test", "test", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)

        with patch.object(widget, "_on_edit_rule") as mock_edit:
            widget._on_edit_clicked()
            mock_edit.assert_called_once()

    def test_on_edit_clicked_no_selection(self, qapp, rules_manager):
        """Test edit button with no item selected."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        with patch.object(widget, "_on_edit_rule") as mock_edit:
            widget._on_edit_clicked()
            mock_edit.assert_not_called()

    def test_on_edit_rule_accepted(self, qapp, rules_manager):
        """Test editing a rule when dialog accepted."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget, RuleEditDialog

        rules_manager.add_rule(AppProfileRule("Old", "old", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["p1"])

        item = widget.rules_list.item(0)
        new_rule = AppProfileRule("New", "new", "wm_class", "p1")

        with patch.object(RuleEditDialog, "exec", return_value=True):
            with patch.object(RuleEditDialog, "get_rule", return_value=new_rule):
                widget._on_edit_rule(item)

        assert rules_manager.rules[0].name == "New"

    def test_on_edit_rule_rejected(self, qapp, rules_manager):
        """Test editing a rule when dialog rejected."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget, RuleEditDialog

        rules_manager.add_rule(AppProfileRule("Old", "old", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        item = widget.rules_list.item(0)

        with patch.object(RuleEditDialog, "exec", return_value=False):
            widget._on_edit_rule(item)

        assert rules_manager.rules[0].name == "Old"

    def test_on_delete_rule_confirmed(self, qapp, rules_manager):
        """Test deleting a rule when confirmed."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("ToDelete", "del", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)

        with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Yes):
            widget._on_delete_rule()

        assert len(rules_manager.rules) == 0

    def test_on_delete_rule_cancelled(self, qapp, rules_manager):
        """Test deleting a rule when cancelled."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Keep", "keep", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)

        with patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.No):
            widget._on_delete_rule()

        assert len(rules_manager.rules) == 1

    def test_on_delete_rule_no_selection(self, qapp, rules_manager):
        """Test delete with no item selected."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        with patch.object(QMessageBox, "question") as mock_msg:
            widget._on_delete_rule()
            mock_msg.assert_not_called()

    def test_on_move_up(self, qapp, rules_manager):
        """Test moving a rule up."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))
        rules_manager.add_rule(AppProfileRule("Second", "2", "window_name", "p2"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(1)
        widget._on_move_up()

        assert rules_manager.rules[0].name == "Second"
        assert widget.rules_list.currentRow() == 0

    def test_on_move_up_first_item(self, qapp, rules_manager):
        """Test move up on first item does nothing."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)
        widget._on_move_up()

        assert rules_manager.rules[0].name == "First"

    def test_on_move_down(self, qapp, rules_manager):
        """Test moving a rule down."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("First", "1", "window_name", "p1"))
        rules_manager.add_rule(AppProfileRule("Second", "2", "window_name", "p2"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)
        widget._on_move_down()

        assert rules_manager.rules[1].name == "First"
        assert widget.rules_list.currentRow() == 1

    def test_on_move_down_last_item(self, qapp, rules_manager):
        """Test move down on last item does nothing."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Last", "1", "window_name", "p1"))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget.rules_list.setCurrentRow(0)
        widget._on_move_down()

        assert rules_manager.rules[0].name == "Last"

    def test_on_default_changed_none(self, qapp, rules_manager):
        """Test setting default profile to None."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.default_profile = "some_profile"

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        widget._on_default_changed("(None - keep current)")

        assert rules_manager.default_profile is None

    def test_on_default_changed_profile(self, qapp, rules_manager):
        """Test setting default profile to a profile."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["profile1"])

        widget._on_default_changed("profile1")

        assert rules_manager.default_profile == "profile1"

    def test_update_profiles(self, qapp, rules_manager):
        """Test updating the profiles list."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["old_profile"])

        widget.default_combo.setCurrentText("old_profile")
        widget.update_profiles(["new_profile1", "new_profile2"])

        assert widget.profiles == ["new_profile1", "new_profile2"]
        assert widget.default_combo.count() == 3  # None + 2 profiles

    def test_update_profiles_preserves_selection(self, qapp, rules_manager):
        """Test update_profiles preserves current selection if possible."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["profile1", "profile2"])

        widget.default_combo.setCurrentText("profile1")
        widget.update_profiles(["profile1", "profile3"])

        assert widget.default_combo.currentText() == "profile1"

    def test_setup_with_existing_default_profile(self, qapp, rules_manager):
        """Test widget setup when default profile already set."""
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.default_profile = "existing"

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager, profiles=["existing", "other"])

        assert widget.default_combo.currentText() == "existing"

    def test_rules_list_disabled_rule_gray(self, qapp, rules_manager):
        """Test disabled rules appear gray in list."""
        from g13_linux.gui.models.app_profile_rules import AppProfileRule
        from g13_linux.gui.views.app_profiles import AppProfilesWidget

        rules_manager.add_rule(AppProfileRule("Disabled", "d", "window_name", "p1", enabled=False))

        with patch("g13_linux.gui.views.app_profiles.WindowMonitorThread") as mock_monitor:
            mock_monitor.return_value.is_available = True
            widget = AppProfilesWidget(rules_manager)

        item = widget.rules_list.item(0)
        assert item.foreground().color() == Qt.GlobalColor.gray
