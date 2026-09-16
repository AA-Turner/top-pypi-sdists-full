# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the LaunchDarkly flag organization-targeting module and tools."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from airbyte_ops_mcp.approval_resolution import (
    ApprovalResolutionError,
    resolve_admin_email_from_approval,
)
from airbyte_ops_mcp.cloud_admin import launchdarkly_flags as ld
from airbyte_ops_mcp.cloud_admin.launchdarkly_flags import (
    get_flag as real_get_flag,
)
from airbyte_ops_mcp.mcp import feature_flags
from airbyte_ops_mcp.tier_cache import OrgTierResult

_FLAG = {
    "key": "adp.external-cloud-orgs.enabled",
    "name": "ADP External Cloud Orgs",
    "kind": "boolean",
    "tags": ["ops-mcp"],
    "variations": [
        {"_id": "var-on", "value": True, "name": "Enabled"},
        {"_id": "var-off", "value": False, "name": "Disabled"},
    ],
    "environments": {
        "production": {
            "on": True,
            "contextTargets": [
                {
                    "contextKind": "organization",
                    "variation": 0,
                    "values": ["org-a"],
                },
                {
                    "contextKind": "user",
                    "variation": 0,
                    "values": ["user-x"],
                },
                {
                    "contextKind": "organization",
                    "variation": 1,
                    "values": ["org-b"],
                },
            ],
        }
    },
}


def _ok_response(payload: dict | None = None, status_code: int = 200) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = payload if payload is not None else {}
    response.text = str(payload)
    return response


@pytest.fixture(autouse=True)
def _ld_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAUNCHDARKLY_API_TOKEN", "test-token")


@pytest.mark.unit
def test_missing_token_raises_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Missing `LAUNCHDARKLY_API_TOKEN` produces a clear configuration error."""
    monkeypatch.delenv("LAUNCHDARKLY_API_TOKEN", raising=False)
    with pytest.raises(ld.LaunchDarklyAPIError, match="LAUNCHDARKLY_API_TOKEN"):
        ld.get_flag("some-flag")


@pytest.mark.unit
def test_get_flag_404_raises_not_found() -> None:
    """A 404 response raises `LaunchDarklyAPIError` mentioning 'not found'."""
    with patch.object(
        ld.requests, "get", return_value=_ok_response({}, 404)
    ), pytest.raises(ld.LaunchDarklyAPIError, match="not found"):
        ld.get_flag("missing-flag")


@pytest.mark.unit
def test_patch_org_targets_semantic_patch_body() -> None:
    """PATCH sends one semantic-patch instruction with the required comment."""
    patch_mock = MagicMock(return_value=_ok_response({}))
    with patch.object(ld.requests, "patch", patch_mock):
        ld.patch_org_targets(
            "flag-1",
            action="add",
            variation_id="var-on",
            organization_id="org-1",
            comment="[ops-mcp] add organization org-1",
        )

    _, kwargs = patch_mock.call_args
    assert (
        kwargs["headers"]["Content-Type"]
        == "application/json; domain-model=launchdarkly.semanticpatch"
    )
    body = kwargs["json"]
    assert body["environmentKey"] == "production"
    assert body["comment"]
    assert body["instructions"] == [
        {
            "kind": "addTargets",
            "contextKind": "organization",
            "variationId": "var-on",
            "values": ["org-1"],
        }
    ]


@pytest.mark.unit
def test_patch_org_targets_remove_kind() -> None:
    """`action='remove'` emits a `removeTargets` instruction."""
    patch_mock = MagicMock(return_value=_ok_response({}))
    with patch.object(ld.requests, "patch", patch_mock):
        ld.patch_org_targets(
            "flag-1",
            action="remove",
            variation_id="var-on",
            organization_id="org-1",
            comment="c",
        )
    instruction = patch_mock.call_args.kwargs["json"]["instructions"][0]
    assert instruction["kind"] == "removeTargets"


@pytest.mark.unit
def test_patch_org_targets_non_2xx_raises() -> None:
    """Non-2xx PATCH responses raise with status and body."""
    with patch.object(
        ld.requests, "patch", return_value=_ok_response({}, 400)
    ), pytest.raises(ld.LaunchDarklyAPIError, match="400"):
        ld.patch_org_targets(
            "flag-1",
            action="add",
            variation_id="v",
            organization_id="o",
            comment="c",
        )


@pytest.mark.unit
def test_resolve_variation_boolean_default_picks_true() -> None:
    """A boolean flag with no selector resolves to the `True` variation."""
    index, variation_id = ld.resolve_variation(_FLAG, None)
    assert (index, variation_id) == (0, "var-on")


@pytest.mark.unit
def test_resolve_variation_name_case_insensitive() -> None:
    """Variation names match case-insensitively."""
    assert ld.resolve_variation(_FLAG, "disabled") == (1, "var-off")


@pytest.mark.unit
def test_resolve_variation_value_string_match() -> None:
    """`str(value)` matching makes 'false' select the off variation."""
    assert ld.resolve_variation(_FLAG, "false") == (1, "var-off")


@pytest.mark.unit
def test_resolve_variation_multivariate_requires_selection() -> None:
    """Multivariate flags without a selector raise, listing variation names."""
    flag = dict(_FLAG, kind="multivariate")
    with pytest.raises(ld.LaunchDarklyAPIError, match=r"Enabled.*Disabled"):
        ld.resolve_variation(flag, None)


@pytest.mark.unit
def test_resolve_variation_unknown_raises() -> None:
    """An unknown selector raises, listing available variations."""
    with pytest.raises(ld.LaunchDarklyAPIError, match="Unknown variation"):
        ld.resolve_variation(_FLAG, "nope")


@pytest.mark.unit
def test_get_org_targets_filters_by_kind_and_variation() -> None:
    """Only `organization` contextTargets on the given variation are returned."""
    assert ld.get_org_targets(_FLAG, 0) == ["org-a"]
    assert ld.get_org_targets(_FLAG, 1) == ["org-b"]


@pytest.mark.unit
def test_flag_is_ops_targetable() -> None:
    """The eligibility check is the `ops-mcp` tag."""
    assert ld.flag_is_ops_targetable(_FLAG)
    assert not ld.flag_is_ops_targetable(dict(_FLAG, tags=[]))


def _org_row() -> dict:
    return {
        "organization_id": "org-1",
        "organization_name": "Org One",
        "email": "admin@one.example",
        "tombstone": False,
        "is_agentic": False,
    }


def _mock_tool_deps(monkeypatch: pytest.MonkeyPatch, flag: dict) -> MagicMock:
    """Patch the module-level dependencies of `update_launchdarkly_feature_flag_targeting`."""
    monkeypatch.setattr(feature_flags, "require_internal_admin_flag_only", lambda: None)
    monkeypatch.setattr(
        feature_flags,
        "resolve_admin_email_from_approval",
        lambda **_: "admin@airbyte.io",
    )
    monkeypatch.setattr(
        feature_flags,
        "query_organization_agentic_flags",
        lambda ids: [_org_row()],
    )
    monkeypatch.setattr(
        feature_flags,
        "get_org_tier",
        lambda **_: OrgTierResult(
            organization_id="org-1", customer_tier="TIER_2", is_in_cache=True
        ),
    )
    get_flag_mock = MagicMock(return_value=flag)
    patch_mock = MagicMock()
    monkeypatch.setattr(ld, "get_flag", get_flag_mock)
    monkeypatch.setattr(ld, "patch_org_targets", patch_mock)
    return patch_mock


@pytest.mark.unit
def test_update_rejects_untagged_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    """An untagged flag is rejected before any PATCH."""
    patch_mock = _mock_tool_deps(monkeypatch, dict(_FLAG, tags=[]))
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "ops-mcp" in result.message
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_noop_when_already_targeted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Adding an already-targeted org returns success without a PATCH."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-a",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert result.success
    assert "already" in result.message
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_approval_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """An approval-resolution failure returns `success=False`, no PATCH."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(
        feature_flags,
        "resolve_admin_email_from_approval",
        MagicMock(side_effect=ApprovalResolutionError("approval missing")),
    )
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "approval missing" in result.message
    patch_mock.assert_not_called()


def _flag(key: str, name: str, tags: list[str] | None = None) -> dict:
    """Build a minimal LaunchDarkly flag dict."""
    return {
        "key": key,
        "name": name,
        "kind": "boolean",
        "tags": tags or [],
        "variations": [{"_id": "v1", "value": True, "name": "On"}],
        "environments": {"production": {"on": True, "contextTargets": []}},
    }


@pytest.mark.unit
def test_list_flags_applies_flag_contains_and_marks_addressable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`list_launchdarkly_feature_flags` filters by key/name substring."""
    flags = [
        _flag("adp.external-cloud-orgs.enabled", "ADP Orgs", ["ops-mcp"]),
        _flag("adp.other", "Other ADP Flag"),
        _flag("unrelated", "Unrelated"),
    ]
    monkeypatch.setattr(feature_flags, "list_flags", lambda tag=None: flags)

    result = feature_flags.list_launchdarkly_feature_flags(
        flag_contains="ADP", ctx=MagicMock()
    )

    assert [f.flag_key for f in result.flags] == [
        "adp.external-cloud-orgs.enabled",
        "adp.other",
    ]
    assert result.flags[0].ops_mcp_addressable
    assert not result.flags[1].ops_mcp_addressable
    assert result.total_returned == 2
    assert not result.truncated


@pytest.mark.unit
def test_list_flags_passes_tag_and_honors_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`tag` is passed through to the API and results truncate to `limit`."""
    list_mock = MagicMock(
        return_value=[_flag(f"flag-{i}", f"Flag {i}") for i in range(3)]
    )
    monkeypatch.setattr(feature_flags, "list_flags", list_mock)

    result = feature_flags.list_launchdarkly_feature_flags(
        tag="ops-mcp", limit=2, ctx=MagicMock()
    )

    list_mock.assert_called_once_with(tag="ops-mcp")
    assert result.total_returned == 2
    assert result.truncated
    assert len(result.flags) == 2


@pytest.mark.unit
def test_list_flags_no_filters(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without filters all flags are returned untruncated."""
    monkeypatch.setattr(
        feature_flags, "list_flags", MagicMock(return_value=[_flag("f", "F")])
    )
    result = feature_flags.list_launchdarkly_feature_flags(ctx=MagicMock())
    assert result.total_returned == 1
    assert not result.truncated


@pytest.mark.unit
def test_variation_id_of_falls_back_to_id() -> None:
    """`variation_id_of` reads `_id` first and falls back to `id`."""
    assert ld.variation_id_of({"_id": "a", "id": "b"}) == "a"
    assert ld.variation_id_of({"id": "b"}) == "b"
    flag = dict(_FLAG)
    flag["variations"] = [{"id": "legacy-id", "value": True, "name": "On"}]
    assert ld.resolve_variation(flag, None) == (0, "legacy-id")


@pytest.mark.unit
def test_update_returns_failure_on_request_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A `requests` transport error becomes `success=False`, not an exception."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(ld, "get_flag", real_get_flag)
    monkeypatch.setattr(
        ld.requests,
        "get",
        MagicMock(side_effect=requests.ConnectionError("conn refused")),
    )
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_rejects_non_slack_approval_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unrecognized `approval_comment_url` domain fails without a PATCH."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(
        feature_flags,
        "resolve_admin_email_from_approval",
        resolve_admin_email_from_approval,
    )
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://example.com/not-an-approval",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "Unrecognized approval URL domain" in result.message
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_reverify_failure_reports_expected_targets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed post-write re-read still reports the expected target list."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(
        ld,
        "get_flag",
        MagicMock(side_effect=[_FLAG, _FLAG, ld.LaunchDarklyAPIError("boom")]),
    )
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert result.success
    assert result.new_targets == ["org-a", "org-1"]
    assert any("Post-write verification read failed" in w for w in result.warnings)
    patch_mock.assert_called_once()


@pytest.mark.unit
def test_update_add_unconfirmed_when_reread_lacks_org(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A successful add whose re-read still lacks the org is reported unconfirmed."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(ld, "get_flag", MagicMock(side_effect=[_FLAG, _FLAG, _FLAG]))
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "unconfirmed" in result.message
    assert result.new_targets == ["org-a"]
    patch_mock.assert_called_once()


@pytest.mark.unit
def test_update_remove_implicit_variation_locates_org(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remove without `variation` targets the variation the org is currently on."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    after = {
        **_FLAG,
        "environments": {"production": {"on": True, "contextTargets": []}},
    }
    monkeypatch.setattr(ld, "get_flag", MagicMock(side_effect=[_FLAG, _FLAG, after]))
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-b",
        "remove",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert result.success
    assert result.variation_name == "Disabled"
    assert patch_mock.call_args.kwargs["variation_id"] == "var-off"
    assert patch_mock.call_args.kwargs["action"] == "remove"


@pytest.mark.unit
def test_update_remove_implicit_variation_ambiguous(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remove without `variation` fails when the org is on multiple variations."""
    both = {
        **_FLAG,
        "environments": {
            "production": {
                "on": True,
                "contextTargets": [
                    {
                        "contextKind": "organization",
                        "variation": 0,
                        "values": ["org-1"],
                    },
                    {
                        "contextKind": "organization",
                        "variation": 1,
                        "values": ["org-1"],
                    },
                ],
            }
        },
    }
    patch_mock = _mock_tool_deps(monkeypatch, both)
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "remove",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "multiple variations" in result.message
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_remove_implicit_untargeted_multivariate_noop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Remove without `variation` on an untargeted multivariate flag is a no-op."""
    multivariate = {
        **_FLAG,
        "kind": "multivariate",
        "variations": [
            {"_id": "var-a", "value": "a", "name": "A"},
            {"_id": "var-b", "value": "b", "name": "B"},
            {"_id": "var-c", "value": "c", "name": "C"},
        ],
        "environments": {
            "production": {"on": True, "contextTargets": []},
        },
    }
    patch_mock = _mock_tool_deps(monkeypatch, multivariate)
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "remove",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert result.success
    assert "nothing to remove" in result.message
    assert result.previous_targets == []
    assert result.new_targets == []
    patch_mock.assert_not_called()


@pytest.mark.unit
def test_update_normalizes_organization_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Uppercase or padded organization IDs are normalized before any LD call."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    after = {
        **_FLAG,
        "environments": {
            "production": {
                "on": True,
                "contextTargets": [
                    {
                        "contextKind": "organization",
                        "variation": 0,
                        "values": ["org-a", "org-1"],
                    },
                ],
            }
        },
    }
    monkeypatch.setattr(ld, "get_flag", MagicMock(side_effect=[_FLAG, _FLAG, after]))
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "  ORG-1 ",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert result.success
    assert result.organization_id == "org-1"
    assert patch_mock.call_args.kwargs["organization_id"] == "org-1"


@pytest.mark.unit
def test_update_remove_implicit_unconfirmed_when_org_moves_variation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Implicit remove is unconfirmed if the re-read shows the org on another variation."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    moved = {
        **_FLAG,
        "environments": {
            "production": {
                "on": True,
                "contextTargets": [
                    {
                        "contextKind": "organization",
                        "variation": 0,
                        "values": ["org-b"],
                    },
                ],
            }
        },
    }
    monkeypatch.setattr(ld, "get_flag", MagicMock(side_effect=[_FLAG, _FLAG, moved]))
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-b",
        "remove",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "unconfirmed" in result.message
    assert result.new_targets == []
    patch_mock.assert_called_once()


@pytest.mark.unit
def test_flag_key_is_url_encoded() -> None:
    """Flag keys with URL-special characters are percent-encoded in requests."""
    get_mock = MagicMock(return_value=_ok_response({}))
    with patch.object(ld.requests, "get", get_mock):
        ld.get_flag("a/b?c")
    assert "a%2Fb%3Fc" in get_mock.call_args.args[0]


@pytest.mark.unit
def test_update_rejects_when_flag_loses_tag_before_patch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A flag that drops the `ops-mcp` tag before the write is rejected."""
    patch_mock = _mock_tool_deps(monkeypatch, _FLAG)
    monkeypatch.setattr(
        ld,
        "get_flag",
        MagicMock(side_effect=[_FLAG, dict(_FLAG, tags=[])]),
    )
    result = feature_flags.update_launchdarkly_feature_flag_targeting(
        "flag-1",
        "org-1",
        "add",
        "https://airbytehq.slack.com/archives/C1/p1",
        organization_name="Org One",
        ctx=MagicMock(),
    )
    assert not result.success
    assert "ops-mcp" in result.message
    patch_mock.assert_not_called()
