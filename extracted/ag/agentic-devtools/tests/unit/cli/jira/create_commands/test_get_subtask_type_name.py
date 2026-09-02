"""Tests for get_subtask_type_name helper."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.jira import create_commands


class TestGetSubtaskTypeName:
    """Tests for the get_subtask_type_name helper function."""

    def test_get_subtask_type_name_prefers_state_override(self):
        """Test helper returns the configured state override before any lookup."""
        with (
            patch.object(
                create_commands,
                "get_jira_value",
                side_effect=lambda key, required=False: {"subtask_type": "Unteraufgabe"}.get(key),
            ),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            assert create_commands.get_subtask_type_name() == "Unteraufgabe"

        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_uses_legacy_state_override(self):
        """Test helper accepts the legacy jira.subtask_issue_type override."""
        with (
            patch.object(
                create_commands,
                "get_jira_value",
                side_effect=lambda key, required=False: {"subtask_issue_type": "Teilaufgabe"}.get(key),
            ),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            assert create_commands.get_subtask_type_name() == "Teilaufgabe"

        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_prefers_env_override(self):
        """Test helper returns the configured environment override before any lookup."""
        with (
            patch.dict("os.environ", {"JIRA_SUBTASK_TYPE": "Teilaufgabe"}, clear=False),
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            assert create_commands.get_subtask_type_name() == "Teilaufgabe"

        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_uses_project_metadata_before_network_lookup(self):
        """Test helper returns the cached project-config subtask name before network lookup."""
        with (
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch("agentic_devtools.cli.config.project_config.get_issue_types_metadata") as mock_metadata,
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            mock_metadata.return_value = {
                "issue_types": [
                    {"name": "Task", "is_subtask": False},
                    {"name": "Teilaufgabe", "is_subtask": True},
                ]
            }

            assert create_commands.get_subtask_type_name(project_key="PROJ") == "Teilaufgabe"

        mock_metadata.assert_called_once_with("PROJ")
        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_skips_invalid_project_metadata_entries(self):
        """Test helper skips invalid cached entries and keeps searching for a valid subtask type."""
        with (
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch("agentic_devtools.cli.config.project_config.get_issue_types_metadata") as mock_metadata,
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            mock_metadata.return_value = {
                "issue_types": [
                    "not-a-dict",
                    {"name": "   ", "is_subtask": True},
                    {"name": "Unteraufgabe", "is_subtask": True},
                ]
            }

            assert create_commands.get_subtask_type_name(project_key="PROJ") == "Unteraufgabe"

        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_falls_back_when_cached_metadata_is_invalid(self, capsys):
        """Test helper falls back when cached project metadata is unusable and config build fails."""
        with (
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch(
                "agentic_devtools.cli.config.project_config.get_issue_types_metadata",
                return_value={"issue_types": "bad"},
            ),
            patch.object(create_commands, "_build_jira_config", side_effect=ValueError("missing config")),
        ):
            assert create_commands.get_subtask_type_name(project_key="PROJ") == "Sub-task"

        captured = capsys.readouterr()
        assert "Warning: Could not build Jira config for subtask type discovery" in captured.err

    def test_get_subtask_type_name_uses_provided_config_when_cached_metadata_has_no_match(self):
        """Test helper uses the provided config when cached metadata has no matching subtask type."""
        mock_requests = MagicMock()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = [{"name": "Unteraufgabe", "subtask": True}]
        mock_requests.get.return_value = response
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with (
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch(
                "agentic_devtools.cli.config.project_config.get_issue_types_metadata",
                return_value={"issue_types": [{"name": "Task", "is_subtask": False}]},
            ),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            assert create_commands.get_subtask_type_name(config=config, project_key="PROJ") == "Unteraufgabe"

        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_returns_discovered_type(self):
        """Test helper returns the Jira-discovered subtask issue type name."""
        mock_requests = MagicMock()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = [
            {"name": "Task", "subtask": False},
            {"name": "Unteraufgabe", "subtask": True},
        ]
        mock_requests.get.return_value = response
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with patch.object(create_commands, "_build_jira_config", return_value=config):
            assert create_commands.get_subtask_type_name() == "Unteraufgabe"

    def test_get_subtask_type_name_warns_and_falls_back_when_request_fails(self, capsys):
        """Test helper warns and falls back when the issue-type lookup fails."""
        mock_requests = MagicMock()
        mock_requests.get.side_effect = RuntimeError("boom")
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with patch.object(create_commands, "_build_jira_config", return_value=config):
            assert create_commands.get_subtask_type_name() == "Sub-task"

        captured = capsys.readouterr()
        assert "Warning: Could not discover the Jira subtask issue type" in captured.err

    def test_get_subtask_type_name_falls_back_when_payload_is_invalid(self):
        """Test helper falls back when the issue-type payload cannot be parsed."""
        mock_requests = MagicMock()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("bad json")
        mock_requests.get.return_value = response
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with patch.object(create_commands, "_build_jira_config", return_value=config):
            assert create_commands.get_subtask_type_name() == "Sub-task"

    def test_get_subtask_type_name_falls_back_when_no_subtask_type_matches(self):
        """Test helper falls back when no issue type in the payload is marked as a subtask."""
        mock_requests = MagicMock()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = ["not-a-dict", {"name": "Task", "subtask": False}]
        mock_requests.get.return_value = response
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with patch.object(create_commands, "_build_jira_config", return_value=config):
            assert create_commands.get_subtask_type_name() == "Sub-task"

    def test_get_subtask_type_name_falls_back_when_subtask_name_is_blank(self):
        """Test helper falls back when a matching subtask type has a blank name."""
        mock_requests = MagicMock()
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = [{"name": "   ", "subtask": True}]
        mock_requests.get.return_value = response
        config = create_commands.JiraConfig(
            base_url="https://jira.example.com",
            headers={},
            ssl_verify=False,
            requests_module=mock_requests,
        )

        with patch.object(create_commands, "_build_jira_config", return_value=config):
            assert create_commands.get_subtask_type_name() == "Sub-task"

    def test_get_subtask_type_name_skips_network_when_not_allowed(self):
        """Test helper returns fallback without hitting the network when network_allowed=False."""
        with (
            patch.object(create_commands, "get_jira_value", return_value=None),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            result = create_commands.get_subtask_type_name(network_allowed=False)

        assert result == "Sub-task"
        mock_build_jira_config.assert_not_called()

    def test_get_subtask_type_name_returns_state_override_without_network_when_not_allowed(self):
        """Test helper returns configured state override even when network_allowed=False."""
        with (
            patch.object(
                create_commands,
                "get_jira_value",
                side_effect=lambda key, required=False: {"subtask_type": "Unteraufgabe"}.get(key),
            ),
            patch.object(create_commands, "_build_jira_config") as mock_build_jira_config,
        ):
            result = create_commands.get_subtask_type_name(network_allowed=False)

        assert result == "Unteraufgabe"
        mock_build_jira_config.assert_not_called()
