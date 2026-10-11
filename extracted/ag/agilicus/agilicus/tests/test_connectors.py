"""Regression tests for connectors.replace_agent (IAF-2370).

`update-agent-connector` must modify only the fields explicitly passed and
preserve unrelated fields.  In particular, repointing a connector's
``connection_uri`` must not clear
``spec.connector_cloud_routing.point_of_presence_tags``.

The connectors returned by the API client are deserialized with
``_check_type`` disabled, so the fakes here are built the same way; that is
what let the old ``connector.spec.cloud_routing`` typo store a spurious key
instead of raising.
"""

from unittest.mock import MagicMock, patch

import pytest

import agilicus

from agilicus import connectors
from agilicus import main as main_module

CONNECTOR_ID = "a" * 22
ORG_ID = "org-1"
OLD_URI = "wss://old.example/.agilicus-agent/control"
NEW_URI = "wss://new.example/.agilicus-agent/control"


class _FakeConnectorsApi:
    def __init__(self, connector):
        self._connector = connector
        self.replaced = None

    def get_agent_connector(self, connector_id, **kwargs):
        return self._connector

    def replace_agent_connector(self, connector_id, agent_connector=None, **kwargs):
        self.replaced = agent_connector
        return agent_connector


class _FakeApiClient:
    def __init__(self, connector):
        self.connectors_api = _FakeConnectorsApi(connector)


def _make_connector(tags=None, routing_present=True, service_account_required=None):
    """Build an AgentConnector in the shape the API client hands back."""
    spec = agilicus.AgentConnectorSpec(
        name="conn-1",
        org_id=ORG_ID,
        connection_uri=OLD_URI,
        service_account_required=service_account_required,
        _check_type=False,
    )
    if routing_present:
        spec.connector_cloud_routing = agilicus.ConnectorCloudRouting(
            point_of_presence_tags=[
                agilicus.FeatureTagName(t, _check_type=False) for t in (tags or [])
            ],
            _check_type=False,
        )
    return agilicus.AgentConnector(spec=spec, _check_type=False)


def _run_replace_agent(connector, **kwargs):
    """Call replace_agent with a fake apiclient and return the PUT object."""
    fake = _FakeApiClient(connector)
    ctx = MagicMock()
    with patch("agilicus.connectors.context.get_token", return_value="token"), patch(
        "agilicus.connectors.context.get_apiclient", return_value=fake
    ):
        connectors.replace_agent(ctx, CONNECTOR_ID, org_id=ORG_ID, **kwargs)
    return fake.connectors_api.replaced


def _tags_of(connector):
    spec = connector.spec.to_dict()
    return spec["connector_cloud_routing"]["point_of_presence_tags"]


# ---------------------------------------------------------------------------
# (i) omitted flag: preserve existing tags, add no spurious key
# ---------------------------------------------------------------------------
def test_replace_agent_omitted_tags_preserves_existing():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        connection_uri=NEW_URI,
        point_of_presence_tag=(),
    )

    assert replaced.spec.connection_uri == NEW_URI
    assert _tags_of(replaced) == ["ca-1"]
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_none_tags_preserves_existing():
    connector = _make_connector(tags=["smoke"])

    replaced = _run_replace_agent(
        connector,
        connection_uri=NEW_URI,
        point_of_presence_tag=None,
    )

    assert replaced.spec.connection_uri == NEW_URI
    assert _tags_of(replaced) == ["smoke"]
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_empty_list_tags_preserves_existing():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        connection_uri=NEW_URI,
        point_of_presence_tag=[],
    )

    assert _tags_of(replaced) == ["ca-1"]
    assert "cloud_routing" not in replaced.spec.to_dict()


# ---------------------------------------------------------------------------
# (ii) explicit tags: set/create connector_cloud_routing
# ---------------------------------------------------------------------------
def test_replace_agent_explicit_tags_creates_routing():
    connector = _make_connector(routing_present=False)

    replaced = _run_replace_agent(
        connector,
        point_of_presence_tag=("smoke",),
    )

    assert _tags_of(replaced) == ["smoke"]
    assert "connector_cloud_routing" in replaced.spec.to_dict()
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_explicit_tags_sets_existing_routing():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        point_of_presence_tag=("smoke",),
    )

    assert _tags_of(replaced) == ["smoke"]
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_multiple_tags_replaces_exactly():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        point_of_presence_tag=("a", "b"),
    )

    assert _tags_of(replaced) == ["a", "b"]
    assert "cloud_routing" not in replaced.spec.to_dict()


# ---------------------------------------------------------------------------
# (iii) explicit clear
# ---------------------------------------------------------------------------
def test_replace_agent_clear_tags_sets_empty_list():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        clear_point_of_presence_tags=True,
    )

    assert _tags_of(replaced) == []
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_clear_tags_on_connector_without_routing():
    connector = _make_connector(routing_present=False)

    replaced = _run_replace_agent(
        connector,
        clear_point_of_presence_tags=True,
    )

    assert _tags_of(replaced) == []
    assert "cloud_routing" not in replaced.spec.to_dict()


def test_replace_agent_clear_wins_over_explicit_tags():
    connector = _make_connector(tags=["ca-1"])

    replaced = _run_replace_agent(
        connector,
        point_of_presence_tag=("smoke",),
        clear_point_of_presence_tags=True,
    )

    assert _tags_of(replaced) == []
    assert "cloud_routing" not in replaced.spec.to_dict()


# ---------------------------------------------------------------------------
# (iv) CLI boundary: an omitted --point-of-presence-tag is never "clear"
# ---------------------------------------------------------------------------
def test_cli_omitted_pop_tag_normalises_to_empty_tuple():
    captured = {}

    def fake_replace_agent(ctx, connector_id, **kwargs):
        captured.update(kwargs)
        result = MagicMock()
        result.to_dict.return_value = {}
        return result

    from click.testing import CliRunner

    with patch.object(
        main_module.connectors, "replace_agent", side_effect=fake_replace_agent
    ), patch.object(main_module, "output_entry"):
        result = CliRunner().invoke(
            main_module.update_agent_connector,
            [CONNECTOR_ID, "--connection-uri", NEW_URI, "--org-id", ORG_ID],
        )

    assert result.exit_code == 0, result.output
    assert captured["connection_uri"] == NEW_URI
    assert captured["point_of_presence_tag"] == ()
    assert captured["clear_point_of_presence_tags"] is False


def test_cli_explicit_pop_tag_is_passed_through():
    captured = {}

    def fake_replace_agent(ctx, connector_id, **kwargs):
        captured.update(kwargs)
        result = MagicMock()
        result.to_dict.return_value = {}
        return result

    from click.testing import CliRunner

    with patch.object(
        main_module.connectors, "replace_agent", side_effect=fake_replace_agent
    ), patch.object(main_module, "output_entry"):
        result = CliRunner().invoke(
            main_module.update_agent_connector,
            [CONNECTOR_ID, "--point-of-presence-tag", "smoke", "--org-id", ORG_ID],
        )

    assert result.exit_code == 0, result.output
    assert captured["point_of_presence_tag"] == ("smoke",)


# ---------------------------------------------------------------------------
# (v) service_account_required: omitted is "preserve", not "true"
# ---------------------------------------------------------------------------
def test_replace_agent_omitted_service_account_required_preserves_false():
    connector = _make_connector(service_account_required=False)

    replaced = _run_replace_agent(connector, connection_uri=NEW_URI)

    assert replaced.spec.connection_uri == NEW_URI
    assert replaced.spec.service_account_required is False


def test_replace_agent_omitted_service_account_required_preserves_true():
    connector = _make_connector(service_account_required=True)

    replaced = _run_replace_agent(connector, connection_uri=NEW_URI)

    assert replaced.spec.service_account_required is True


def test_replace_agent_explicit_service_account_required():
    connector = _make_connector(service_account_required=False)

    replaced = _run_replace_agent(connector, service_account_required=True)

    assert replaced.spec.service_account_required is True


def test_replace_agent_explicit_service_account_not_required():
    connector = _make_connector(service_account_required=True)

    replaced = _run_replace_agent(connector, service_account_required=False)

    assert replaced.spec.service_account_required is False


# ---------------------------------------------------------------------------
# (vi) CLI boundary: an omitted --service-account-required is never "true"
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "flags,expected",
    [
        ([], None),
        (["--service-account-required"], True),
        (["--service-account-not-required"], False),
    ],
)
def test_cli_service_account_required_is_tristate(flags, expected):
    captured = {}

    def fake_replace_agent(ctx, connector_id, **kwargs):
        captured.update(kwargs)
        result = MagicMock()
        result.to_dict.return_value = {}
        return result

    from click.testing import CliRunner

    with patch.object(
        main_module.connectors, "replace_agent", side_effect=fake_replace_agent
    ), patch.object(main_module, "output_entry"):
        result = CliRunner().invoke(
            main_module.update_agent_connector,
            [CONNECTOR_ID, "--connection-uri", NEW_URI, "--org-id", ORG_ID] + flags,
        )

    assert result.exit_code == 0, result.output
    assert captured["service_account_required"] is expected
