"""Tests for the typed contract-error family (TRK-M1-02 A7).

TrackerContractError is the new common base for "the payload violates the
tracker's contract" failures (as opposed to transport/auth/not-found
failures, which stay under ConnectorRequestError). DiscoveryContractError
is re-parented under it without any change to its own attributes or
raise sites (still a SpecKittyTrackerError via MRO, so every existing
isinstance(exc, SpecKittyTrackerError) check in
tests/test_discovery_contract_errors.py keeps passing unchanged).

IssuePayloadContractError and DecisionReferenceContractError are new
TrackerContractError subclasses; their production raise sites belong to
TRK-M1-03 (mapping/policy/sync engine). This file only pins the type
shape and provides a reference raise-site per TRK-M1-01 draft §5's
TRK-M1-02 row ("tests N19-N22 and the contract rows of N1/N3 (error
types exist and are raised by a reference raise-site)").

ScopeViolationError is a new, separate SpecKittyTrackerError subclass
(not a TrackerContractError — a scope violation is not a payload-contract
violation); its production raise site is host territory (TRK-M1-04/05,
TRK-M1-06 N7).
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker.errors import (
    DecisionReferenceContractError,
    DiscoveryContractError,
    IssuePayloadContractError,
    ScopeViolationError,
    SpecKittyTrackerError,
    TrackerContractError,
)


def test_tracker_contract_error_is_a_spec_kitty_tracker_error() -> None:
    exc = TrackerContractError(
        "bad payload",
        provider="beads",
        kind="issue",
        field_path="status",
        reason="BD-003",
    )
    assert isinstance(exc, SpecKittyTrackerError)
    assert exc.provider == "beads"
    assert exc.kind == "issue"
    assert exc.field_path == "status"
    assert exc.reason == "BD-003"


def test_tracker_contract_error_attrs_default_to_none() -> None:
    exc = TrackerContractError("bad payload")
    assert exc.provider is None
    assert exc.kind is None
    assert exc.field_path is None
    assert exc.reason is None


def test_discovery_contract_error_is_reparented_under_tracker_contract_error() -> None:
    exc = DiscoveryContractError(
        "bad discovery data",
        provider="linear",
        kind="workspace",
        field_path="provider_context",
        reason="WS-006",
    )
    # Backward compatibility: every pre-existing isinstance check against
    # SpecKittyTrackerError (tests/test_discovery_contract_errors.py) still
    # holds, because TrackerContractError -> SpecKittyTrackerError.
    assert isinstance(exc, TrackerContractError)
    assert isinstance(exc, SpecKittyTrackerError)
    assert exc.reason == "WS-006"


@pytest.mark.parametrize(
    "error_cls",
    [IssuePayloadContractError, DecisionReferenceContractError],
)
def test_new_contract_error_subclasses_are_tracker_contract_errors(
    error_cls: type[TrackerContractError],
) -> None:
    exc = error_cls("malformed", kind="patch", field_path="severity", reason="PK-001")
    assert isinstance(exc, TrackerContractError)
    assert isinstance(exc, SpecKittyTrackerError)
    assert exc.kind == "patch"
    assert exc.field_path == "severity"
    assert exc.reason == "PK-001"


def test_scope_violation_error_is_spec_kitty_tracker_error_not_contract_error() -> None:
    exc = ScopeViolationError(
        "cross-scope access",
        expected_scope="repoA",
        actual_scope="repoB",
    )
    assert isinstance(exc, SpecKittyTrackerError)
    assert not isinstance(exc, TrackerContractError)
    assert exc.expected_scope == "repoA"
    assert exc.actual_scope == "repoB"


def test_issue_payload_contract_error_reference_raise_site_unknown_patch_key() -> None:
    """Reference raise-site for N1 (unknown patch key -> PK-001).

    This demonstrates the error's shape via a minimal, local validator. The
    production wiring of this rule into every connector/engine egress path
    is TRK-M1-03 A6; this is not that wiring.
    """

    def _reject_unknown_patch_keys(patch: dict[str, object], allowed: frozenset[str]) -> None:
        for key in patch:
            if key not in allowed:
                raise IssuePayloadContractError(
                    f"unexpected patch key: {key}",
                    kind="patch",
                    field_path=key,
                    reason="PK-001",
                )

    with pytest.raises(IssuePayloadContractError) as exc_info:
        _reject_unknown_patch_keys({"severity": 1}, frozenset({"title", "body"}))

    exc = exc_info.value
    assert exc.kind == "patch"
    assert exc.field_path == "severity"
    assert exc.reason == "PK-001"


def test_issue_payload_contract_error_reference_raise_site_malformed_json() -> None:
    """Reference raise-site for N3 (malformed Beads JSON -> BD-000).

    Demonstrates the error's shape for the "parser sees invalid JSON" case.
    Production wiring into BeadsConnector._parse_json is TRK-M1-03 A8; this
    is not that wiring.
    """
    import json

    def _parse_strict(text: str) -> object:
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise IssuePayloadContractError(
                f"invalid JSON payload: {exc}",
                kind="issue",
                field_path=None,
                reason="BD-000",
            ) from exc

    with pytest.raises(IssuePayloadContractError) as exc_info:
        _parse_strict("{not json")

    assert exc_info.value.reason == "BD-000"
    assert exc_info.value.kind == "issue"
