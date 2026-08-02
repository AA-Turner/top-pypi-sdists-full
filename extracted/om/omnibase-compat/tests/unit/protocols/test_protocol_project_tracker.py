# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import json
import unittest.mock

import pytest

from omnibase_compat.adapters.adapter_project_tracker_linear import (
    AdapterProjectTrackerLinear,
)
from omnibase_compat.models.model_project_tracker import (
    ModelIssueStatus,
    ModelLabel,
    ModelTeam,
)
from omnibase_compat.protocols.protocol_project_tracker import ProtocolProjectTracker


def _mock_urlopen(response_body: dict[str, object]) -> unittest.mock.MagicMock:
    cm = unittest.mock.MagicMock()
    cm.read.return_value = json.dumps(response_body).encode()
    cm.__enter__ = unittest.mock.MagicMock(return_value=cm)
    cm.__exit__ = unittest.mock.MagicMock(return_value=False)
    return cm


_TEAMS_RESPONSE: dict[str, object] = {
    "data": {
        "teams": {
            "nodes": [
                {"id": "t1", "name": "Engineering", "key": "ENG"},
                {"id": "t2", "name": "Product", "key": "PROD"},
            ]
        }
    }
}

_LABELS_RESPONSE: dict[str, object] = {
    "data": {
        "issueLabels": {
            "nodes": [
                {"id": "l1", "name": "bug", "color": "#ff0000", "team": {"id": "t1"}},
                {"id": "l2", "name": "feature", "color": "#00ff00", "team": {"id": "t1"}},
            ]
        }
    }
}

_STATUSES_RESPONSE: dict[str, object] = {
    "data": {
        "workflowStates": {
            "nodes": [
                {"id": "s1", "name": "Backlog", "type": "unstarted", "team": {"id": "t1"}},
                {"id": "s2", "name": "In Progress", "type": "started", "team": {"id": "t1"}},
                {"id": "s3", "name": "Done", "type": "completed", "team": {"id": "t1"}},
            ]
        }
    }
}


@pytest.mark.unit
def test_is_instance_of_protocol() -> None:
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    assert isinstance(adapter, ProtocolProjectTracker)


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_teams(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen(_TEAMS_RESPONSE)
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    teams = adapter.list_teams()
    assert teams == [
        ModelTeam(id="t1", name="Engineering", key="ENG"),
        ModelTeam(id="t2", name="Product", key="PROD"),
    ]
    assert len(teams) == 2


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_teams_sends_auth_header(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen(_TEAMS_RESPONSE)
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    adapter.list_teams()
    req: unittest.mock.MagicMock = mock_open.call_args[0][0]
    assert req.headers["Authorization"] == "lin_api_testkey"


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_issue_labels(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen(_LABELS_RESPONSE)
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    labels = adapter.list_issue_labels("ENG")
    assert labels == [
        ModelLabel(id="l1", name="bug", color="#ff0000", team_id="t1"),
        ModelLabel(id="l2", name="feature", color="#00ff00", team_id="t1"),
    ]


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_issue_labels_sends_team_filter(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen(_LABELS_RESPONSE)
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    adapter.list_issue_labels("ENG")
    req: unittest.mock.MagicMock = mock_open.call_args[0][0]
    body = json.loads(req.data)
    assert body["variables"]["filter"]["team"]["key"]["eq"] == "ENG"


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_issue_statuses(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen(_STATUSES_RESPONSE)
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    statuses = adapter.list_issue_statuses("ENG")
    assert statuses == [
        ModelIssueStatus(id="s1", name="Backlog", type="unstarted", team_id="t1"),
        ModelIssueStatus(id="s2", name="In Progress", type="started", team_id="t1"),
        ModelIssueStatus(id="s3", name="Done", type="completed", team_id="t1"),
    ]


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_teams_empty(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen({"data": {"teams": {"nodes": []}}})
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    assert adapter.list_teams() == []


@pytest.mark.unit
@unittest.mock.patch(
    "omnibase_compat.adapters.adapter_project_tracker_linear.urllib.request.urlopen"
)
def test_list_teams_error_response(mock_open: unittest.mock.MagicMock) -> None:
    mock_open.return_value = _mock_urlopen({"errors": [{"message": "bad"}]})
    adapter = AdapterProjectTrackerLinear(api_key="lin_api_testkey")
    with pytest.raises(ValueError, match="Unexpected Linear response"):
        adapter.list_teams()


@pytest.mark.unit
def test_protocol_has_expected_methods() -> None:
    methods = {"list_teams", "list_issue_labels", "list_issue_statuses"}
    for method in methods:
        assert hasattr(ProtocolProjectTracker, method), f"Missing method: {method}"


@pytest.mark.unit
def test_custom_base_url() -> None:
    adapter = AdapterProjectTrackerLinear(api_key="key", base_url="http://localhost:8080")
    assert adapter._base_url == "http://localhost:8080"


@pytest.mark.unit
def test_models_frozen() -> None:
    team = ModelTeam(id="t1", name="Eng", key="ENG")
    with pytest.raises(ValueError):
        team.name = "changed"  # type: ignore[misc]

    label = ModelLabel(id="l1", name="bug", color="#f00", team_id="t1")
    with pytest.raises(ValueError):
        label.name = "changed"  # type: ignore[misc]

    status = ModelIssueStatus(id="s1", name="Backlog", type="unstarted", team_id="t1")
    with pytest.raises(ValueError):
        status.name = "changed"  # type: ignore[misc]
