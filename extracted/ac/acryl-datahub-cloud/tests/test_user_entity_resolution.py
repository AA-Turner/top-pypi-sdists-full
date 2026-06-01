"""Unit tests for the user-entity-resolution ingestion source."""

from typing import Optional, cast
from unittest.mock import MagicMock

import pytest

from acryl_datahub_cloud.user_entity_resolution.source import (
    UserEntityResolutionSource,
    UserEntityResolutionSourceConfig,
    _UserRecord,
)
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.graph.client import DataHubGraph
from datahub.metadata.schema_classes import (
    AuditStampClass,
    CorpUserInfoClass,
    CorpUserStatusClass,
    SiblingsClass,
)

_AUTH_URN = "urn:li:corpuser:User@example.com"
_GHOST_URN = "urn:li:corpuser:user@example.com"
_OTHER_URN = "urn:li:corpuser:other@example.com"

_TWO_DAYS_MS = 2 * 24 * 60 * 60 * 1000


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_graph() -> MagicMock:
    return MagicMock(spec=DataHubGraph)


@pytest.fixture
def source(mock_graph: MagicMock) -> UserEntityResolutionSource:
    ctx = MagicMock(spec=PipelineContext)
    ctx.require_graph.return_value = mock_graph
    src = UserEntityResolutionSource(UserEntityResolutionSourceConfig(), ctx)
    src.graph = cast(DataHubGraph, mock_graph)
    return src


# ---------------------------------------------------------------------------
# _derive_email_key
# ---------------------------------------------------------------------------


def test_derive_email_key_from_corp_user_info() -> None:
    info = CorpUserInfoClass(active=True, email="User@Example.COM")
    key = UserEntityResolutionSource._derive_email_key(_AUTH_URN, info)
    assert key == "user@example.com"


def test_derive_email_key_falls_back_to_urn() -> None:
    key = UserEntityResolutionSource._derive_email_key(_AUTH_URN, None)
    assert key == "user@example.com"


def test_derive_email_key_returns_none_for_non_email_urn() -> None:
    key = UserEntityResolutionSource._derive_email_key("urn:li:corpuser:datahub", None)
    assert key is None


def test_derive_email_key_prefers_info_email_over_urn() -> None:
    # URN says 'alias', corpUserInfo says the real email.
    info = CorpUserInfoClass(active=True, email="real.email@example.com")
    key = UserEntityResolutionSource._derive_email_key("urn:li:corpuser:alias", info)
    assert key == "real.email@example.com"


# ---------------------------------------------------------------------------
# _group_by_email
# ---------------------------------------------------------------------------


def test_group_by_email_single_group() -> None:
    records = [
        _UserRecord(urn=_AUTH_URN, email_key="user@example.com"),
        _UserRecord(urn=_GHOST_URN, email_key="user@example.com"),
    ]
    groups = UserEntityResolutionSource._group_by_email(records)
    assert list(groups.keys()) == ["user@example.com"]
    assert len(groups["user@example.com"]) == 2


def test_group_by_email_ignores_singletons() -> None:
    records = [
        _UserRecord(urn=_AUTH_URN, email_key="user@example.com"),
        _UserRecord(urn=_OTHER_URN, email_key="other@example.com"),
    ]
    groups = UserEntityResolutionSource._group_by_email(records)
    assert groups == {}


def test_group_by_email_n_way_group() -> None:
    third_urn = "urn:li:corpuser:USER@example.com"
    records = [
        _UserRecord(urn=_AUTH_URN, email_key="user@example.com"),
        _UserRecord(urn=_GHOST_URN, email_key="user@example.com"),
        _UserRecord(urn=third_urn, email_key="user@example.com"),
    ]
    groups = UserEntityResolutionSource._group_by_email(records)
    assert len(groups["user@example.com"]) == 3


# ---------------------------------------------------------------------------
# _pick_authoritative
# ---------------------------------------------------------------------------


def test_pick_authoritative_clear_winner() -> None:
    auth = _UserRecord(
        urn=_AUTH_URN, email_key="user@example.com", status_time=_TWO_DAYS_MS
    )
    ghost = _UserRecord(urn=_GHOST_URN, email_key="user@example.com", status_time=0)
    result, reason = UserEntityResolutionSource._pick_authoritative([auth, ghost])
    assert result is auth
    assert reason is None


def test_pick_authoritative_no_status_defers() -> None:
    auth = _UserRecord(urn=_AUTH_URN, email_key="user@example.com", status_time=None)
    ghost = _UserRecord(urn=_GHOST_URN, email_key="user@example.com", status_time=None)
    result, reason = UserEntityResolutionSource._pick_authoritative([auth, ghost])
    assert result is None
    assert reason is not None
    assert "no corpUserStatus" in reason


def test_pick_authoritative_partial_status_picks_the_one_with_status() -> None:
    # Ghost has no status; auth has one — auth should win.
    auth = _UserRecord(
        urn=_AUTH_URN, email_key="user@example.com", status_time=1_000_000
    )
    ghost = _UserRecord(urn=_GHOST_URN, email_key="user@example.com", status_time=None)
    result, reason = UserEntityResolutionSource._pick_authoritative([auth, ghost])
    assert result is auth
    assert reason is None


def test_pick_authoritative_tier2_corp_user_info_wins() -> None:
    # Neither has a login event; only auth has corpUserInfo — it should win.
    auth = _UserRecord(
        urn=_AUTH_URN, email_key="user@example.com", has_corp_user_info=True
    )
    ghost = _UserRecord(
        urn=_GHOST_URN, email_key="user@example.com", has_corp_user_info=False
    )
    result, reason = UserEntityResolutionSource._pick_authoritative([auth, ghost])
    assert result is auth
    assert reason is None


def test_pick_authoritative_tier2_both_have_info_defers() -> None:
    auth = _UserRecord(
        urn=_AUTH_URN, email_key="user@example.com", has_corp_user_info=True
    )
    ghost = _UserRecord(
        urn=_GHOST_URN, email_key="user@example.com", has_corp_user_info=True
    )
    result, reason = UserEntityResolutionSource._pick_authoritative([auth, ghost])
    assert result is None
    assert reason is not None


def test_pick_authoritative_close_timestamps_picks_most_recent() -> None:
    # Even timestamps minutes apart resolve — most recent login wins.
    t = 1_000_000_000
    sso = _UserRecord(urn=_AUTH_URN, email_key="user@example.com", status_time=t)
    ghost = _UserRecord(
        urn=_GHOST_URN, email_key="user@example.com", status_time=t - 100
    )
    result, reason = UserEntityResolutionSource._pick_authoritative([sso, ghost])
    assert result is sso
    assert reason is None


# ---------------------------------------------------------------------------
# get_workunits — MCP emission
# ---------------------------------------------------------------------------


def _make_aspects(
    email: str,
    status_time: Optional[int],
    siblings: Optional[SiblingsClass] = None,
) -> dict:
    info = CorpUserInfoClass(active=True, email=email)
    aspects: dict = {"corpUserInfo": info, "corpUserStatus": None, "siblings": siblings}
    if status_time is not None:
        aspects["corpUserStatus"] = CorpUserStatusClass(
            status="ACTIVE",
            lastModified=AuditStampClass(
                time=status_time, actor="urn:li:corpuser:datahub"
            ),
        )
    return aspects


def _to_entity_aspects(aspects_dict: dict) -> dict:
    """Convert _make_aspects() output to get_entities() format: {name: (aspect, None) | None}."""
    return {k: (v, None) if v is not None else None for k, v in aspects_dict.items()}


def _setup_get_entities(mock_graph: MagicMock, urn_aspects: list) -> None:
    """Wire mock_graph.get_entities to return the given (urn, aspects_dict) mapping.

    Accepts multiple calls — each call returns the full dict so batching works.
    The side_effect returns the subset of the map matching the requested URNs.
    """
    full_map = {urn: _to_entity_aspects(aspects) for urn, aspects in urn_aspects}

    def _get_entities(entity_name, urns, aspects=None, **kwargs):
        return {u: full_map[u] for u in urns if u in full_map}

    mock_graph.get_entities.side_effect = _get_entities


def test_get_workunits_emits_siblings_for_resolved_group(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (_AUTH_URN, _make_aspects("user@example.com", status_time=_TWO_DAYS_MS)),
            (_GHOST_URN, _make_aspects("user@example.com", status_time=0)),
        ],
    )

    workunits = list(source.get_workunits())
    assert len(workunits) == 2  # one SiblingsClass per URN

    mcps = [cast(MetadataChangeProposalWrapper, wu.metadata) for wu in workunits]
    aspects = [cast(SiblingsClass, mcp.aspect) for mcp in mcps]
    assert all(isinstance(a, SiblingsClass) for a in aspects)

    primary_aspects = [a for a in aspects if a.primary]
    ghost_aspects = [a for a in aspects if not a.primary]
    assert len(primary_aspects) == 1
    assert len(ghost_aspects) == 1

    # Primary (auth URN) lists ghost as sibling.
    assert primary_aspects[0].siblings == [_GHOST_URN]
    # Ghost lists auth URN as sibling.
    assert ghost_aspects[0].siblings == [_AUTH_URN]

    assert source.report.sibling_groups_resolved == 1
    assert source.report.siblings_aspects_emitted == 2


def test_get_workunits_resolves_via_corp_user_info(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    # Neither URN has logged in; only auth has corpUserInfo → Tier 2 resolves it.
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (_AUTH_URN, _make_aspects("user@example.com", status_time=None)),
            (
                _GHOST_URN,
                {"corpUserInfo": None, "corpUserStatus": None, "siblings": None},
            ),
        ],
    )

    workunits = list(source.get_workunits())
    assert len(workunits) == 2
    assert source.report.sibling_groups_resolved == 1
    assert source.report.sibling_groups_deferred == 0

    mcps2 = [cast(MetadataChangeProposalWrapper, wu.metadata) for wu in workunits]
    primary_aspects = [m.aspect for m in mcps2 if cast(SiblingsClass, m.aspect).primary]
    assert len(primary_aspects) == 1
    assert [m.entityUrn for m in mcps2 if cast(SiblingsClass, m.aspect).primary] == [
        _AUTH_URN
    ]


def test_get_workunits_defers_when_no_status(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (_AUTH_URN, _make_aspects("user@example.com", status_time=None)),
            (_GHOST_URN, _make_aspects("user@example.com", status_time=None)),
        ],
    )

    workunits = list(source.get_workunits())
    assert workunits == []
    assert source.report.sibling_groups_deferred == 1
    assert source.report.sibling_groups_resolved == 0


def test_get_workunits_dry_run_emits_nothing(
    mock_graph: MagicMock,
) -> None:
    ctx = MagicMock(spec=PipelineContext)
    ctx.require_graph.return_value = mock_graph
    source = UserEntityResolutionSource(
        UserEntityResolutionSourceConfig(dry_run=True), ctx
    )
    source.graph = cast(DataHubGraph, mock_graph)

    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (_AUTH_URN, _make_aspects("user@example.com", status_time=_TWO_DAYS_MS)),
            (_GHOST_URN, _make_aspects("user@example.com", status_time=0)),
        ],
    )

    workunits = list(source.get_workunits())
    assert workunits == []
    assert source.report.sibling_groups_resolved == 1
    assert source.report.siblings_aspects_emitted == 0


def test_get_workunits_skips_non_email_users(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    system_urn = "urn:li:corpuser:datahub"
    mock_graph.get_urns_by_filter.return_value = [system_urn, _AUTH_URN]
    _setup_get_entities(
        mock_graph,
        [
            (
                system_urn,
                {
                    "corpUserInfo": CorpUserInfoClass(active=True),
                    "corpUserStatus": None,
                    "siblings": None,
                },
            ),
            (_AUTH_URN, _make_aspects("user@example.com", status_time=1_000)),
        ],
    )

    workunits = list(source.get_workunits())
    assert workunits == []
    assert source.report.users_without_email == 1
    assert source.report.sibling_groups_found == 0


def test_get_workunits_skips_unchanged_siblings(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    # Both URNs already carry the correct Siblings aspects — no writes expected.
    existing_auth = SiblingsClass(siblings=[_GHOST_URN], primary=True)
    existing_ghost = SiblingsClass(siblings=[_AUTH_URN], primary=False)
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (
                _AUTH_URN,
                _make_aspects("user@example.com", _TWO_DAYS_MS, siblings=existing_auth),
            ),
            (_GHOST_URN, _make_aspects("user@example.com", 0, siblings=existing_ghost)),
        ],
    )

    workunits = list(source.get_workunits())
    assert workunits == []
    assert source.report.siblings_aspects_emitted == 0
    assert source.report.siblings_aspects_skipped == 2
    assert source.report.sibling_groups_resolved == 1


def test_get_workunits_emits_when_primary_flips(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    # Previous run picked ghost as primary; now auth has a newer timestamp — must re-emit.
    stale_auth = SiblingsClass(siblings=[_GHOST_URN], primary=False)
    stale_ghost = SiblingsClass(siblings=[_AUTH_URN], primary=True)
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN]
    _setup_get_entities(
        mock_graph,
        [
            (
                _AUTH_URN,
                _make_aspects("user@example.com", _TWO_DAYS_MS, siblings=stale_auth),
            ),
            (_GHOST_URN, _make_aspects("user@example.com", 0, siblings=stale_ghost)),
        ],
    )

    workunits = list(source.get_workunits())
    assert len(workunits) == 2
    assert source.report.siblings_aspects_emitted == 2
    assert source.report.siblings_aspects_skipped == 0


def test_get_workunits_n_way_group(
    source: UserEntityResolutionSource, mock_graph: MagicMock
) -> None:
    third_urn = "urn:li:corpuser:USER@example.com"
    mock_graph.get_urns_by_filter.return_value = [_AUTH_URN, _GHOST_URN, third_urn]
    _setup_get_entities(
        mock_graph,
        [
            (_AUTH_URN, _make_aspects("user@example.com", status_time=_TWO_DAYS_MS)),
            (_GHOST_URN, _make_aspects("user@example.com", status_time=0)),
            (third_urn, _make_aspects("user@example.com", status_time=1_000)),
        ],
    )

    workunits = list(source.get_workunits())
    # One SiblingsClass per URN in the group.
    assert len(workunits) == 3
    assert source.report.siblings_aspects_emitted == 3

    mcps = [cast(MetadataChangeProposalWrapper, wu.metadata) for wu in workunits]
    primary_mcps = [m for m in mcps if cast(SiblingsClass, m.aspect).primary]
    assert len(primary_mcps) == 1
    assert primary_mcps[0].entityUrn == _AUTH_URN
    # Primary lists both ghosts.
    assert set(cast(SiblingsClass, primary_mcps[0].aspect).siblings) == {
        _GHOST_URN,
        third_urn,
    }
