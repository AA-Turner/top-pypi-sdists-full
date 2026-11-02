"""🚨 The organization-exemption matcher is the blast radius — attack it here.

``organization_exempt_paths`` are PREFIXES; ``organization_exempt_routes`` are
EXACT routes composed by a host from its own route table (aidream:
``Depends(organization_free)``). A bug in either direction is a data-isolation
bug, not an inconvenience: an entry that over-matches silently turns a
tenant-scoped route organization-free, and the caller never learns that the
organization it named was not required after all.

Two real incidents are pinned here:

* a bare ``startswith`` made ``/health`` exempt ``/healthcare/patients`` — an
  exemption list that widens itself silently is worse than none, because it
  reads as narrow;
* composing route paths into the PREFIX list made ``/mandates/coverage``
  exempt the organization-scoped ``/mandates/coverage/states`` it shares a stem
  with (2026-09-12, caught in composition testing before it shipped) — which is
  why exact routes are a separate list rather than a string heuristic.

Every case below asserts a NEGATIVE as hard as a positive.
"""

from __future__ import annotations

import pytest
from matrx_connect.middleware.auth import (
    compile_organization_exempt_pattern,
    is_organization_exempt_path,
)


PREFIXES = ("/health", "/auth", "/admin", "/legal/admin")
ROUTES = (
    "/mandates/{mandate_key}/references",
    "/mandates/coverage",
    "/surfaces/{client_name}/{surface_name}/manifest",
    "/scheduling/scanner-status",
    "/api/mandates/coverage",
)


def _exempt(path: str) -> bool:
    return is_organization_exempt_path(path, PREFIXES, ROUTES)


# ── prefixes stay prefixes, at a SEGMENT boundary ──────────────────────────


@pytest.mark.parametrize(
    "path",
    ["/health", "/health/version", "/admin", "/admin/system-errors", "/legal/admin/overview"],
)
def test_prefix_entries_match_the_prefix_and_below(path: str) -> None:
    assert _exempt(path)


@pytest.mark.parametrize(
    "path",
    [
        "/healthcare/patients",  # the original incident
        "/administration/anything",
        "/legal/admin-tools",
        "/legal/employees",
        "/authenticate",
    ],
)
def test_prefix_entries_never_match_across_a_segment_boundary(path: str) -> None:
    assert not _exempt(path)


# ── exact routes are EXACT — the cases that would be data-isolation bugs ───


def test_parameter_route_matches_exactly_one_shape() -> None:
    assert _exempt("/mandates/abc/references")
    assert _exempt("/mandates/some-long_key.v2/references")


@pytest.mark.parametrize(
    "path",
    [
        "/mandates/abc/references/extra",  # not a prefix — nothing may follow
        "/mandates/abc",  # the stem is not exempt
        "/mandates",  # the shared prefix is NEVER exempt
        "/mandatesX/abc/references",  # literal text is escaped
        "/mandates/abc/def/references",  # a parameter is ONE segment
        "/mandates//references",  # a parameter is NON-EMPTY
        "/xx/mandates/abc/references",  # anchored at the start
        "/mandates/abc/provenance",  # an org-scoped sibling under the same stem
        "/mandates/abc/binding",
    ],
)
def test_parameter_route_never_over_matches(path: str) -> None:
    assert not _exempt(path)


def test_a_parameterless_route_entry_is_still_exact_not_a_prefix() -> None:
    """The 2026-09-12 near-miss: ``/mandates/coverage`` is super-admin and
    organization-blind; ``/mandates/coverage/states`` is authenticated-only and
    verifies organization membership in the endpoint. If a route entry acquired
    prefix semantics, exempting the first would exempt the second."""
    assert _exempt("/mandates/coverage")
    assert not _exempt("/mandates/coverage/states")
    assert not _exempt("/mandates/coverage/anything/else")


def test_multi_parameter_route_is_segment_bounded_in_every_slot() -> None:
    assert _exempt("/surfaces/matrx-user/chat/manifest")
    assert not _exempt("/surfaces/matrx-user/manifest")
    assert not _exempt("/surfaces/matrx-user/chat/deep/manifest")
    assert not _exempt("/surfaces/matrx-user/chat/manifest/raw")


def test_the_api_twin_is_its_own_entry_and_not_inferred() -> None:
    """Auth runs before the ``/api`` prefix rewrite, so a host composes both
    forms. A bare form must not exempt the ``/api`` one by itself."""
    assert _exempt("/api/mandates/coverage")
    assert not _exempt("/api/mandates/abc/references")
    assert not _exempt("/api/scheduling/scanner-status")


# ── the two lists never leak into each other ───────────────────────────────


def test_a_route_entry_never_acquires_prefix_semantics() -> None:
    """Only the ``_paths`` list is prefix-matched. Passing the same string as a
    route and as a prefix must give different answers for a child path."""
    assert not is_organization_exempt_path(
        "/scheduling/scanner-status/detail", (), ("/scheduling/scanner-status",)
    )
    assert is_organization_exempt_path(
        "/scheduling/scanner-status/detail", ("/scheduling/scanner-status",), ()
    )


def test_a_prefix_entry_is_never_pattern_compiled() -> None:
    """A ``{...}`` accidentally left in the PREFIX list is inert literal text,
    not a wildcard — it must not match a real parameter value."""
    assert not is_organization_exempt_path("/mandates/abc/references", ("/mandates/{k}/references",), ())


def test_empty_lists_exempt_nothing() -> None:
    assert not is_organization_exempt_path("/health", (), ())
    assert not is_organization_exempt_path("/anything", ("",), ())


def test_trailing_slash_on_an_entry_is_ignored() -> None:
    assert is_organization_exempt_path("/mandates/coverage", (), ("/mandates/coverage/",))
    assert not is_organization_exempt_path("/mandates/coverage/states", (), ("/mandates/coverage/",))


def test_an_uncompilable_entry_raises_instead_of_degrading_to_a_prefix() -> None:
    with pytest.raises(ValueError):
        compile_organization_exempt_pattern("/mandates/{unclosed/references")
