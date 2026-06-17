import inspect
import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from runlayer_cli.api import PluginDetail, SkillDetail
from runlayer_cli.catalog_client import CatalogConnector
from runlayer_cli.commands.catalog.kinds import (
    CONNECTOR_KIND,
    PLUGIN_KIND,
    SKILL_KIND,
)
from runlayer_cli.main import app

runner = CliRunner()


def _skill(
    name: str = "review-code",
    *,
    skill_id: str = "550e8400-e29b-41d4-a716-446655440000",
    install_name: str | None = "review-code",
) -> SkillDetail:
    return SkillDetail(
        id=skill_id,
        name=name,
        install_name=install_name,
        namespace="Org/Repo",
        description="Review code changes",
        file_count=2,
        is_public=True,
    )


def _plugin(
    name: str = "review-suite",
    *,
    plugin_id: str = "550e8400-e29b-41d4-a716-446655440001",
    install_name: str | None = "review-suite",
) -> PluginDetail:
    return PluginDetail(
        id=plugin_id,
        name=name,
        install_name=install_name,
        namespace="Org/Repo",
        description="Review plugin bundle",
        is_public=True,
        server_count=1,
        tool_count=3,
        skill_count=2,
    )


def _connector(
    name: str = "com.github/mcp",
    *,
    title: str = "GitHub",
    beta: bool = False,
) -> CatalogConnector:
    return CatalogConnector(
        name=name,
        title=title,
        description="GitHub MCP connector",
        version="1.0.0",
        status="active",
        remotes=[{"type": "streamable-http", "url": "https://example.com/mcp"}],
        meta={
            "io.modelcontextprotocol.registry/publisher-provided": {
                "runlayer": {
                    "deploymentMode": "hosted",
                    "beta": beta,
                    "oauthBrokerVendor": "github",
                }
            },
            "io.runlayer/computed": {"existing_count": 2},
        },
        mcpFingerprint="a" * 64,
        versionFingerprint="b" * 64,
    )


@contextmanager
def _catalog_patches(tmp_path: Path) -> Iterator[MagicMock]:
    """Patch catalog command deps; yield the RunlayerClient mock."""
    with (
        patch(
            "runlayer_cli.commands.catalog.commands.setup_logging",
            return_value=tmp_path / "log.txt",
        ),
        patch(
            "runlayer_cli.commands.catalog.commands.resolve_credentials",
            return_value={"host": "https://example.com", "secret": "rl_test"},
        ),
        patch("runlayer_cli.commands.catalog.commands.RunlayerClient") as client_class,
    ):
        yield client_class


def test_catalog_skills_lists_available_skills(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_skills.return_value = [_skill()]

        result = runner.invoke(
            app,
            [
                "catalog",
                "skills",
                "--query",
                "review",
                "--namespace",
                "Org/Repo",
            ],
        )

    assert result.exit_code == 0
    assert "review-code" in result.output
    assert "1 skill(s) available" in result.output
    client_class.assert_called_once_with(
        hostname="https://example.com",
        secret="rl_test",
    )
    client_class.return_value.list_skills.assert_called_once_with(
        namespace="Org/Repo",
        filter="all",
        query="review",
    )


def test_catalog_plugins_prints_json(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_plugins_detailed.return_value = [_plugin()]

        result = runner.invoke(app, ["catalog", "plugins", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload[0]["name"] == "review-suite"
    assert payload[0]["server_count"] == 1
    client_class.return_value.list_plugins_detailed.assert_called_once_with(
        namespace=None,
        filter="all",
        query=None,
    )


def test_catalog_connectors_filters_beta_by_default(tmp_path: Path) -> None:
    stable_connector = _connector()
    beta_connector = _connector("com.beta/mcp", title="Beta", beta=True)
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_catalog_connectors.return_value = [
            beta_connector,
            stable_connector,
        ]

        result = runner.invoke(app, ["catalog", "connectors"])

    assert result.exit_code == 0
    assert "GitHub" in result.output
    assert "Beta" not in result.output


def test_catalog_connectors_include_beta(tmp_path: Path) -> None:
    beta_connector = _connector("com.beta/mcp", title="Beta", beta=True)
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_catalog_connectors.return_value = [
            beta_connector
        ]

        result = runner.invoke(app, ["catalog", "connectors", "--include-beta"])

    assert result.exit_code == 0
    assert "Beta" in result.output
    assert "beta" in result.output


def test_catalog_search_groups_results(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_skills.return_value = [_skill()]
        client_class.return_value.list_plugins_detailed.return_value = [_plugin()]
        client_class.return_value.list_catalog_connectors.return_value = [_connector()]

        result = runner.invoke(app, ["catalog", "search", "github"])

    assert result.exit_code == 0
    assert "Connectors:" in result.output
    assert "Skills:" in result.output
    assert "Plugins:" in result.output
    client_class.return_value.list_skills.assert_called_once_with(
        namespace=None,
        filter="all",
        query="github",
    )
    client_class.return_value.list_plugins_detailed.assert_called_once_with(
        namespace=None,
        filter="all",
        query="github",
    )


def test_catalog_search_allows_partial_failure(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_skills.side_effect = RuntimeError(
            "skills unavailable"
        )
        client_class.return_value.list_plugins_detailed.return_value = [_plugin()]
        client_class.return_value.list_catalog_connectors.return_value = []

        result = runner.invoke(app, ["catalog", "search", "review"])

    assert result.exit_code == 0
    assert "Warning: failed to search skills: skills unavailable" in result.output
    assert "Plugins:" in result.output


def test_only_connector_kind_supports_beta() -> None:
    # Beta is a connector-only catalog concept; skills/plugins have no beta flag.
    assert CONNECTOR_KIND.supports_beta is True
    assert SKILL_KIND.supports_beta is False
    assert PLUGIN_KIND.supports_beta is False


def test_skill_plugin_listings_do_not_accept_include_beta() -> None:
    # Guard against silently swallowing --include-beta: only beta-capable kinds
    # may take the flag, so listing skills/plugins with it must be a hard error.
    assert "include_beta" not in inspect.signature(SKILL_KIND.list_items).parameters
    assert "include_beta" not in inspect.signature(PLUGIN_KIND.list_items).parameters
    assert "include_beta" in inspect.signature(CONNECTOR_KIND.list_items).parameters


def test_catalog_search_include_beta_only_affects_connectors(tmp_path: Path) -> None:
    beta_connector = _connector("com.beta/mcp", title="Review Beta", beta=True)
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_skills.return_value = [_skill()]
        client_class.return_value.list_plugins_detailed.return_value = [_plugin()]
        client_class.return_value.list_catalog_connectors.return_value = [
            beta_connector
        ]

        result = runner.invoke(app, ["catalog", "search", "review", "--include-beta"])

    assert result.exit_code == 0
    # Beta surfaces for connectors...
    assert "Review Beta" in result.output
    # ...and skills/plugins still list (flag is a no-op for them, never an error).
    assert "Skills:" in result.output
    assert "Plugins:" in result.output
    client_class.return_value.list_skills.assert_called_once_with(
        namespace=None,
        filter="all",
        query="review",
    )
    client_class.return_value.list_plugins_detailed.assert_called_once_with(
        namespace=None,
        filter="all",
        query="review",
    )


def test_catalog_info_skill_by_id(tmp_path: Path) -> None:
    skill = _skill()
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.get_skill.return_value = skill

        result = runner.invoke(
            app,
            ["catalog", "info", "skill", skill.id, "--json"],
        )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["id"] == skill.id
    client_class.return_value.get_skill.assert_called_once_with(skill.id)


def test_catalog_info_plugin_by_name(tmp_path: Path) -> None:
    plugin = _plugin()
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_plugins_detailed.return_value = [plugin]

        result = runner.invoke(
            app,
            ["catalog", "info", "plugin", "review-suite"],
        )

    assert result.exit_code == 0
    assert "name: review-suite" in result.output
    client_class.return_value.get_plugin.assert_not_called()


def test_catalog_info_connector_by_title(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_catalog_connectors.return_value = [_connector()]

        result = runner.invoke(app, ["catalog", "info", "connector", "GitHub"])

    assert result.exit_code == 0
    assert "name: com.github/mcp" in result.output
    assert "oauth_broker_vendor: github" in result.output
    # remotes are serialized to JSON at the display layer, not in ConnectorView
    assert '"type": "streamable-http"' in result.output


def test_catalog_info_connector_json_serializes_remotes(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_catalog_connectors.return_value = [_connector()]

        result = runner.invoke(
            app, ["catalog", "info", "connector", "GitHub", "--json"]
        )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["remotes"] == [
        {"type": "streamable-http", "url": "https://example.com/mcp"}
    ]


def test_catalog_info_reports_ambiguous_name(tmp_path: Path) -> None:
    with _catalog_patches(tmp_path) as client_class:
        client_class.return_value.list_skills.return_value = [
            _skill(skill_id="550e8400-e29b-41d4-a716-446655440000"),
            _skill(skill_id="550e8400-e29b-41d4-a716-446655440002"),
        ]

        result = runner.invoke(app, ["catalog", "info", "skill", "review-code"])

    assert result.exit_code == 1
    assert "Multiple skills matched 'review-code'" in result.output
