"""Hosted-vs-local tracker mode taxonomy.

This module is the SDK-side surface added by mission
``tracker-readiness-alignment-01KS7PZ7`` (Workstream 5 of
``Priivacy-ai/spec-kitty#1091``, tracking issue
``Priivacy-ai/spec-kitty-tracker#18``).

Background
----------

Before this module existed the only place that classified providers as
"SaaS-backed" vs "local/native" was the *consumer's* configuration —
``specify_cli.tracker.config`` in the CLI repo carries two literal
``frozenset`` constants (``SAAS_PROVIDERS`` / ``LOCAL_PROVIDERS``).  That
arrangement coupled the CLI to a hand-maintained list and made it
difficult for any other consumer (a downstream SDK, a deployed-dev
canary, the dashboard renderer) to ask the SDK "is this provider hosted
or local?" without re-encoding the same enumeration.

What this module exposes
------------------------

- :class:`TrackerMode`: a two-value :class:`enum.StrEnum` (``HOSTED`` /
  ``LOCAL``).  No third bucket — every supported provider is exactly one
  of the two for the lifetime of this contract.  Adding a new mode is a
  spec-level change and requires bumping the consumer compatibility
  expectation.
- :data:`HOSTED_PROVIDERS` / :data:`LOCAL_PROVIDERS`: ``frozenset[str]``
  of normalized provider slugs.  Single source of truth.  Consumers MAY
  re-export, but MUST NOT shadow with a divergent set.
- :func:`provider_mode`: lookup helper returning the mode for a given
  provider slug.  Raises ``ValueError`` for unknown slugs so the caller
  is forced to handle the unrecognized case explicitly (no silent
  default).
- :func:`is_hosted_provider` / :func:`is_local_provider`: convenience
  booleans for callers that don't want to import the enum.

Operating rules honoured
------------------------

- **No SaaS state mutation.** This module is pure metadata.
- **No new pip deps.** Stdlib only.
- **No event producers introduced.** No canonical-producer surface
  touched.
- **No protocol changes to existing connectors.** The taxonomy is
  additive; existing imports from :mod:`spec_kitty_tracker` are
  unaffected.
- **Read-only API.** The frozensets are immutable; the function helpers
  are pure.

Consumer guidance (CLI side)
----------------------------

The Spec Kitty CLI's `specify_cli.tracker.config` module retains its own
``SAAS_PROVIDERS`` / ``LOCAL_PROVIDERS`` constants for backward
compatibility with its existing call sites; over time those should be
replaced with `provider_mode()` calls into this module so the SDK is the
single source of truth.  Doing so is **out of scope** for this mission —
the mission's task is to *make* the SDK-side surface available so the
CLI side can migrate to it incrementally.
"""

from __future__ import annotations

from enum import StrEnum


class TrackerMode(StrEnum):
    """Operating mode for a tracker provider.

    Two values, by design:

    - ``HOSTED`` — provider is routed through the Spec Kitty SaaS
      control plane via Nango proxy transport.  Requires hosted auth
      (``spec-kitty auth login``).  CLI behaviour: register the command
      only when ``is_saas_sync_enabled()``; route auth failures through
      the shared readiness language.
    - ``LOCAL`` — provider is driven by a direct connector with local
      credentials.  No hosted auth, no readiness probe.  Works fully
      offline.

    Adding a third member is a **specification-level change** (it would
    leak through every consumer's exhaustive ``match`` statement); make
    sure the rollout plan covers each consumer before doing so.
    """

    HOSTED = "hosted"
    LOCAL = "local"


# ---------------------------------------------------------------------------
# Provider slug taxonomy (single source of truth)
# ---------------------------------------------------------------------------
#
# Slugs MUST be lower-case.  Consumers normalize external input with
# ``str.lower().strip()`` before lookup; ``provider_mode`` does this
# defensively as well.

HOSTED_PROVIDERS: frozenset[str] = frozenset({"linear", "jira", "github", "gitlab"})
"""SaaS-hosted providers routed through the Spec Kitty SaaS control plane."""

LOCAL_PROVIDERS: frozenset[str] = frozenset({"beads", "fp"})
"""Local-only providers driven by direct connectors with no hosted auth."""

ALL_KNOWN_PROVIDERS: frozenset[str] = HOSTED_PROVIDERS | LOCAL_PROVIDERS
"""Union of every slug this SDK currently classifies."""


def provider_mode(provider: str) -> TrackerMode:
    """Return the :class:`TrackerMode` for *provider*.

    The lookup is case-insensitive and surrounding whitespace is
    stripped before classification.  Unknown providers raise
    :class:`ValueError` — the caller MUST handle the unrecognized case
    explicitly rather than relying on a silent default.

    Args:
        provider: Provider slug, e.g. ``"linear"``, ``"github"``,
            ``"beads"``, ``"fp"``.  Case-insensitive; whitespace is
            stripped.

    Returns:
        ``TrackerMode.HOSTED`` for providers in
        :data:`HOSTED_PROVIDERS`; ``TrackerMode.LOCAL`` for providers in
        :data:`LOCAL_PROVIDERS`.

    Raises:
        ValueError: If *provider* is empty after normalization or is not
            present in :data:`ALL_KNOWN_PROVIDERS`.
    """
    if not isinstance(provider, str):
        raise ValueError(f"provider must be a string, got {type(provider).__name__}")

    normalized = provider.strip().lower()
    if not normalized:
        raise ValueError("provider slug must not be empty")

    if normalized in HOSTED_PROVIDERS:
        return TrackerMode.HOSTED
    if normalized in LOCAL_PROVIDERS:
        return TrackerMode.LOCAL

    raise ValueError(
        f"unknown tracker provider: {provider!r}. Known providers: {sorted(ALL_KNOWN_PROVIDERS)}"
    )


def is_hosted_provider(provider: str) -> bool:
    """Return ``True`` iff *provider* is a hosted SaaS-backed provider.

    Convenience wrapper around :func:`provider_mode` for callers that
    don't want to import :class:`TrackerMode`.  Unknown providers raise
    :class:`ValueError` (same as :func:`provider_mode`) — there is no
    silent ``False`` fallback because that would mask configuration
    drift.
    """
    return provider_mode(provider) is TrackerMode.HOSTED


def is_local_provider(provider: str) -> bool:
    """Return ``True`` iff *provider* is a local-only provider.

    See :func:`is_hosted_provider` for rationale on the no-fallback
    behaviour for unknown providers.
    """
    return provider_mode(provider) is TrackerMode.LOCAL
