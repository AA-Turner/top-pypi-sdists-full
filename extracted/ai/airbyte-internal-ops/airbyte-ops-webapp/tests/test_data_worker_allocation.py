"""Tests for the Data Worker Allocation page and tools."""

from __future__ import annotations

import pytest
from airbyte_ops_mcp.cloud_admin.data_worker_allocation import (
    DataWorkerAllocationAPIError,
    DataWorkerAllocationResponseError,
)
from airbyte_ops_mcp.cloud_admin.models import (
    DataplaneGroup,
    DataplaneGroupList,
    DataWorkerAllocation,
    DataWorkerAllocationList,
)

from airbyte_ops_webapp.auth import mock_session
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation import (
    _helpers as helpers,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation import (
    _mcp_tools as mcp_tools,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._mcp_tools import (
    add_capacity,
    lookup_allocations,
    remove_capacity,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation._state import (
    DataWorkerAllocationPageState,
)
from airbyte_ops_webapp.pages.platform_admin.data_worker_allocation.page import (
    data_worker_allocation,
)
from airbyte_ops_webapp.state import MOCK_ONLY_ENV_VAR, OAuthConfigState


def _sample_oauth_config() -> OAuthConfigState:
    return OAuthConfigState(
        enabled=True,
        issuer="https://issuer.example",
        client_id="client",
        redirect_uri="https://app.example/callback",
        authorization_endpoint="https://issuer.example/auth",
        token_endpoint="https://issuer.example/token",
        session_endpoint="/oauth/session",
        token_exchange_endpoint="/oauth/token",
    )


def test_page_state_contains_all_allocation_fields() -> None:
    state = DataWorkerAllocationPageState.from_env(
        oauth_config=_sample_oauth_config()
    ).to_prefab_state()

    assert state["org_loaded"] is False
    assert state["add_amount"] == ""
    assert state["result_modal_open"] is False


@pytest.fixture
def mock_authenticated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(MOCK_ONLY_ENV_VAR, "1")
    monkeypatch.setattr(mock_session, "_oauth_authenticated", True)


def test_mock_lookup_and_capacity_validation(
    mock_authenticated: None,
) -> None:
    lookup = lookup_allocations("demo-org")
    assert lookup.org_loaded is True
    assert lookup.allocations is not None

    assert add_capacity("demo-org", "abc").success is False
    assert add_capacity("demo-org", "-1").success is False
    assert add_capacity("demo-org", "2").success is True


def test_allocation_rows_carry_region_names(mock_authenticated: None) -> None:
    """Rows show a region name, not just a UUID."""
    lookup = lookup_allocations("demo-org")
    assert lookup.allocations is not None

    names = [row["dataplane_group_name"] for row in lookup.allocations["allocations"]]
    assert names == ["US", "EU"]


def test_zero_capacity_regions_are_hidden(monkeypatch) -> None:
    """Removing all capacity leaves a zero row the page should not offer."""
    allocation_list = DataWorkerAllocationList(
        organization_id="org-1",
        total_allocated_capacity=1.0,
        allocations=[
            DataWorkerAllocation(dataplane_group_id="us", allocated_capacity=1.0),
            DataWorkerAllocation(
                dataplane_group_id="us-central", allocated_capacity=0.0
            ),
        ],
    )
    monkeypatch.setattr(
        mcp_tools,
        "list_dataplane_groups",
        lambda **_: DataplaneGroupList(
            dataplane_groups=[
                DataplaneGroup(dataplane_group_id="us", name="US"),
                DataplaneGroup(dataplane_group_id="us-central", name="US-Central"),
            ]
        ),
    )

    rows = mcp_tools._named_allocation_rows(allocation_list, "org-1", "token")

    assert [row["dataplane_group_name"] for row in rows] == ["US"]


def test_hiding_zero_rows_does_not_change_the_total(monkeypatch) -> None:
    """The total comes from the API, so it still counts every region."""
    monkeypatch.setattr(
        mcp_tools, "list_dataplane_groups", lambda **_: DataplaneGroupList()
    )
    allocation_list = DataWorkerAllocationList(
        organization_id="org-1",
        total_allocated_capacity=1.0,
        allocations=[
            DataWorkerAllocation(dataplane_group_id="z", allocated_capacity=0.0)
        ],
    )

    rows = mcp_tools._named_allocation_rows(allocation_list, "org-1", "token")

    assert rows == []
    assert allocation_list.total_allocated_capacity == 1.0


def test_negative_capacity_is_still_shown(monkeypatch) -> None:
    """A negative value is a data problem, so it must stay visible."""
    monkeypatch.setattr(
        mcp_tools, "list_dataplane_groups", lambda **_: DataplaneGroupList()
    )
    allocation_list = DataWorkerAllocationList(
        organization_id="org-1",
        total_allocated_capacity=-2.0,
        allocations=[
            DataWorkerAllocation(dataplane_group_id="odd", allocated_capacity=-2.0)
        ],
    )

    rows = mcp_tools._named_allocation_rows(allocation_list, "org-1", "token")

    assert len(rows) == 1


def test_named_allocation_rows_falls_back_to_id(monkeypatch) -> None:
    """An unlisted region shows its UUID. Deleted regions hit this."""
    allocation_list = DataWorkerAllocationList(
        organization_id="org-1",
        total_allocated_capacity=5.0,
        allocations=[
            DataWorkerAllocation(dataplane_group_id="known-id", allocated_capacity=3.0),
            DataWorkerAllocation(
                dataplane_group_id="tombstoned-id", allocated_capacity=2.0
            ),
        ],
    )
    monkeypatch.setattr(
        mcp_tools,
        "list_dataplane_groups",
        lambda **_: DataplaneGroupList(
            dataplane_groups=[DataplaneGroup(dataplane_group_id="known-id", name="US")]
        ),
    )

    rows = mcp_tools._named_allocation_rows(allocation_list, "org-1", "token")

    assert rows[0]["dataplane_group_name"] == "US"
    assert rows[1]["dataplane_group_name"] == "tombstoned-id"


def test_named_allocation_rows_survives_lookup_failure(monkeypatch) -> None:
    """A failed name lookup still returns the capacity numbers."""

    def boom(**_):
        raise DataWorkerAllocationAPIError("dataplane group list unavailable")

    monkeypatch.setattr(mcp_tools, "list_dataplane_groups", boom)
    allocation_list = DataWorkerAllocationList(
        organization_id="org-1",
        total_allocated_capacity=3.0,
        allocations=[
            DataWorkerAllocation(dataplane_group_id="some-id", allocated_capacity=3.0)
        ],
    )

    rows = mcp_tools._named_allocation_rows(allocation_list, "org-1", "token")

    assert rows[0]["dataplane_group_name"] == "some-id"
    assert rows[0]["allocated_capacity"] == 3.0


def test_dataplane_group_list_parses_camel_case_wrapper() -> None:
    """The wrapper key is camelCase, so the alias has to match."""
    parsed = DataplaneGroupList.model_validate(
        {
            "dataplaneGroups": [
                {
                    "dataplane_group_id": "abc",
                    "name": "US",
                    "organization_id": "org",
                    "enabled": True,
                }
            ]
        }
    )

    assert parsed.dataplane_groups[0].name == "US"
    assert parsed.dataplane_groups[0].dataplane_group_id == "abc"


def test_dataplane_group_list_defaults_to_empty() -> None:
    """The key is optional in the response."""
    assert DataplaneGroupList.model_validate({}).dataplane_groups == []


def test_remove_capacity_validates_amount(mock_authenticated: None) -> None:
    """Removal rejects the same bad amounts as adding."""
    assert remove_capacity("demo-org", "region-1", "abc").success is False
    assert remove_capacity("demo-org", "region-1", "0").success is False
    assert remove_capacity("demo-org", "region-1", "-1").success is False
    assert remove_capacity("demo-org", "region-1", "2").success is True


@pytest.mark.parametrize("amount", ["nan", "inf", "-inf", "Infinity"])
def test_capacity_rejects_non_finite_amounts(
    mock_authenticated: None, amount: str
) -> None:
    """float() accepts these, but they are not valid JSON."""
    assert add_capacity("demo-org", amount).success is False
    assert remove_capacity("demo-org", "region-1", amount).success is False


def test_remove_capacity_requires_a_region(mock_authenticated: None) -> None:
    """Removal has to say which region, unlike adding."""
    result = remove_capacity("demo-org", "", "2")

    assert result.success is False
    assert "region" in result.message.lower()


def test_remove_capacity_sends_region_to_the_api(monkeypatch) -> None:
    """The chosen region reaches the client call."""
    seen: dict[str, object] = {}

    def fake_remove(**kwargs):
        seen.update(kwargs)
        return DataWorkerAllocationList(
            organization_id="org-1",
            total_allocated_capacity=1.0,
            allocations=[],
        )

    monkeypatch.setattr(mcp_tools, "remove_data_worker_capacity", fake_remove)
    monkeypatch.setattr(mcp_tools, "auth_available", lambda *_: True)
    monkeypatch.setattr(mcp_tools, "mock_only_enabled", lambda: False)
    monkeypatch.setattr(
        mcp_tools, "list_dataplane_groups", lambda **_: DataplaneGroupList()
    )

    result = mcp_tools.remove_capacity("org-1", "region-9", "2.5", region_name="EU")

    assert result.success is True
    assert seen["dataplane_group_id"] == "region-9"
    assert seen["amount"] == 2.5
    assert "EU" in result.message


@pytest.mark.parametrize("tool", ["add", "remove"])
def test_unreadable_response_still_reports_success(monkeypatch, tool: str) -> None:
    """A committed change must never be reported as failed."""

    def boom(**_):
        raise DataWorkerAllocationResponseError("unreadable body")

    monkeypatch.setattr(mcp_tools, "add_data_worker_capacity", boom)
    monkeypatch.setattr(mcp_tools, "remove_data_worker_capacity", boom)
    monkeypatch.setattr(mcp_tools, "auth_available", lambda *_: True)
    monkeypatch.setattr(mcp_tools, "mock_only_enabled", lambda: False)

    if tool == "add":
        result = mcp_tools.add_capacity("org-1", "2")
    else:
        result = mcp_tools.remove_capacity("org-1", "region-1", "2")

    assert result.success is True
    assert result.total_allocated_capacity is None
    assert result.stale is True
    assert "could not be read back" in result.message


def _state_keys(actions) -> list[str]:
    return [a.key for a in actions if getattr(a, "key", None)]


def test_apply_success_updates_the_overview_from_the_result() -> None:
    """The change response is authoritative, so the overview uses it."""
    keys = _state_keys(helpers.apply_success_actions())

    assert "allocations" in keys
    assert "allocations_stale" in keys
    allocations_value = next(
        a.value for a in helpers.apply_success_actions() if a.key == "allocations"
    )
    assert "Rx(" not in str(allocations_value)
    assert "$result.allocations_view" in str(allocations_value)


def test_capacity_change_result_carries_a_full_allocations_view(
    mock_authenticated: None,
) -> None:
    """The overview replacement must be built by the tool, not the client."""
    result = mcp_tools.add_capacity("org-1", "2")

    assert result.success is True
    assert result.allocations_view == {
        "organization_id": "org-1",
        "total_allocated_capacity": result.total_allocated_capacity,
        "allocations": result.allocations,
    }


def test_failed_refresh_is_visible_and_marks_state_stale() -> None:
    """A failed refresh must not leave old numbers looking current."""
    actions = helpers.refresh_fail_actions()
    keys = _state_keys(actions)

    assert "allocations_stale" in keys
    assert "tool_error" in keys
    assert any(type(a).__name__ == "ShowToast" for a in actions)
    assert keys != ["is_loading", "loading_message"]


def test_successful_lookup_clears_the_stale_flag() -> None:
    """Otherwise the warning would persist after a good refresh."""
    assert "allocations_stale" in _state_keys(helpers.lookup_success_actions())


def test_page_state_has_removal_fields() -> None:
    """The removal form needs its own state keys."""
    state = DataWorkerAllocationPageState.from_env(
        oauth_config=_sample_oauth_config()
    ).to_prefab_state()

    assert state["remove_amount"] == ""
    assert state["remove_dataplane_group_id"] == ""
    assert state["remove_dataplane_group_name"] == ""
    assert state["remove_confirm_open"] is False


def _walk(component):
    """Yield a component and everything under it."""
    yield component
    for child in getattr(component, "children", None) or []:
        yield from _walk(child)


def test_row_remove_button_records_region_and_opens_dialog() -> None:
    """A row's Remove button records its region and opens the dialog."""
    nodes = list(_walk(data_worker_allocation().view))
    keys_set_on_click = {
        action.key
        for node in nodes
        for action in (getattr(node, "on_click", None) or [])
        if getattr(action, "key", None)
    }

    assert "remove_dataplane_group_id" in keys_set_on_click
    assert "remove_dataplane_group_name" in keys_set_on_click
    assert "remove_confirm_open" in keys_set_on_click

    # No Select: the renderer won't expand a ForEach into SelectOption children.
    assert not [node for node in nodes if type(node).__name__ == "Select"]
