"""A profile's APP COMPANIES, and the one predicate that decides app visibility.

An **app company** is a value of an exposed app's Teleport `company` label; a profile
may see an app when it holds one of the app's app companies (CONTEXT.md). This module is
the single answer to both halves of that sentence, shared by every surface that asks it
-- the browser app proxy (`browser_proxy/authz.py`), `expose`/`unexpose`/`list_exposed`
(`tools/expose.py`) and the console's exposed-apps read (`console/reads.py`). None of
them may re-derive it: a second copy is how one surface ends up showing an app another
refuses to open (docs/multi-company-app-access-spec.md).

**A profile holds a SET.** The first entry is its HOME app company -- what `expose`
writes when no company is named; the rest are GRANTED (the customers a partner works
for). The set's source of truth is the ``app_companies`` field of the profile's own
Secrets Manager secret (``<secrets_prefix><profile>``, the secret that already carries
its Apollo credentials). ``scripts/provision-access.py`` is the only writer, and it
writes the Teleport role's ``app_labels`` from the same value in the same plan, so the
two enforcement points -- this module and Teleport's own cert check -- cannot drift the
way the hardcoded map did (issue #275).

**Baseline and fallback.** ``settings.app_companies_source`` selects the source per
stack. ``"map"`` (the default, and prod's setting until the 2026-09-28 transition; now
the rollback, as both deployed stacks set ``"stored"``) is the BASELINE:
one app company per profile, ``PROFILE_COMPANY_MAP.get(profile, profile)``, and the
stored field is never read. ``"stored"`` reads the set; a profile with no field yet still
resolves to the map value. Because the secrets and roles are shared across stacks, this
switch is what keeps prod unchanged while dev validates, and flipping it back is the
rollback -- so the map stays until that option is deliberately retired. A secret that HAS
the field but holds something unusable resolves to ``None`` and callers deny: a
malformed grant is never widened into the fallback. Nor is an UNREADABLE secret: it
reuses the last set this process read for the profile, and denies when there is none.
Falling back to the map there would widen any profile whose stored home is narrower than
its map entry, and `list_exposed` and the console have no Teleport check behind them.

**An app's label is a set too, written comma-separated** (``company: "lear,pltr"``),
because a Teleport label holds one string per key. Roles match it with anchored
regexes -- see ``provision-access.py::role_app_company_patterns`` -- which Teleport
evaluates on every request and every new connection. `label_companies` is the parser;
nothing else may split the label.
"""

from __future__ import annotations

import logging
import os
import re
import threading
import time
from dataclasses import dataclass

from cube_cloud.teleport.tbot_manager import PROFILE_ROLE_MAP

logger = logging.getLogger(__name__)

# Default company label for unscoped admin profiles (matches the module's own default).
DEFAULT_COMPANY = os.environ.get("TELEPORT_APP_DEFAULT_COMPANY", "edgescaleai")

# The broad bot role (admin/esaiadmin resolve to it via PROFILE_ROLE_MAP) has
# app_labels '*':'*' -- it is NOT scoped to any company and sees every app.
UNSCOPED_ROLE = "cube-mcp-bot"

# An app company is a single DNS-label-shaped token: the charset every live label
# already uses, and the one thing that keeps a value safe to join with commas and to
# embed in a role regex without quoting surprises.
_NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")

# The BASELINE source of truth: what every profile resolves to when this stack's
# `app_companies_source` is "map", and what an unmigrated profile resolves to when it is
# "stored". Entries exist only where a profile's company differs from its own name; every
# other profile defaults to company == profile name. It stays while "map" remains a
# supported rollback. Do NOT add entries for new grants -- run
# `scripts/provision-access.py profile set-app-companies`, which stores the set and
# rewrites the Teleport role together. `provision-access.py` reads this literal (via
# `ast`) to seed that migration, so it must stay a plain dict literal.
PROFILE_COMPANY_MAP: dict[str, str] = {
    "edgescaleai-dev": "edgescaleai",
    "lear-sandbox": "lear-sandbox",
    "lear-dev": "lear",
    "conagra-dev": "conagra",
    "pltr-dev": "pltr",
    "pltr-sandbox": "pltr",
    "pltr-perception-dev": "pltr-perception",
    "pltr-southwire-dev": "southwire",
    "strategists": "edgescaleai",
    "esai-fde": "edgescaleai",
    "core-onboarding": "edgescaleai",
}

# How long a resolved set is reused. Browser-proxy authz runs on every proxied request,
# so this bounds Secrets Manager reads; it is also the longest a removed grant keeps
# passing THIS check (Teleport's own check sees a role change on the next connection).
CACHE_TTL_SECONDS = float(os.environ.get("CUBE_CLOUD_APP_COMPANIES_CACHE_TTL_SECONDS", "60"))


@dataclass(frozen=True)
class AppCompanies:
    """What one profile holds. ``home`` is always a member of ``held``."""

    home: str
    held: frozenset[str]
    unscoped: bool = False
    source: str = "stored"  # "stored" | "fallback" | "unscoped"

    def can_see(self, label_value: object) -> bool:
        """True iff an app whose `company` label is ``label_value`` is visible to us.

        Unscoped profiles see everything, including an app with no label at all. A
        scoped profile needs at least one app company in common with the label; an
        absent or empty label matches nobody (unknown ownership reads as foreign).
        """
        if self.unscoped:
            return True
        return bool(self.held & label_companies(label_value))


class _Unset:
    pass


_UNSET = _Unset()
# Caches the Secrets Manager read only -- (expiry, raw field). The transitional map is an
# in-process dict and is consulted fresh on every call.
_cache: dict[str, tuple[float, list[object] | None]] = {}
# The last field each profile's secret was READ with, kept past its TTL: what an unreadable
# secret resolves to. Keys are authenticated profiles, so the dict is bounded by them.
_last_read: dict[str, list[object] | None] = {}
_lock = threading.Lock()
_malformed_logged: set[str] = set()


def is_valid_name(value: object) -> bool:
    return isinstance(value, str) and bool(_NAME_RE.fullmatch(value))


def is_unscoped(profile: str) -> bool:
    return PROFILE_ROLE_MAP.get(profile, profile) == UNSCOPED_ROLE


def label_companies(label_value: object) -> frozenset[str]:
    """Parse an app's `company` label into its set of app companies.

    Comma-separated, NOT whitespace-tolerant: a token is taken exactly as written and
    kept only if it is a valid app company name, so this never admits a label the role
    regex (`^(.*,)?<name>(,.*)?$`, which Teleport full-matches) refuses. Tolerating
    `"lear, pltr"` made cube-cloud list an app to `pltr` that Teleport would not let it
    open, and `"lear "` swept by an `unexpose all=true` Teleport matched to nobody. An
    invalid token (`Groundcover`, `" pltr"`) is DROPPED: it can match no stored set,
    since every stored name is validated.
    """
    if not isinstance(label_value, str):
        return frozenset()
    return frozenset(t for t in label_value.split(",") if is_valid_name(t))


def format_label(companies: set[str] | frozenset[str]) -> str:
    """The `company` label value for a set: sorted, comma-joined. The inverse of
    `label_companies` for any set of valid names, and deterministic, so a relabel that
    changes nothing writes byte-identical config."""
    bad = sorted(c for c in companies if not is_valid_name(c))
    if bad:
        raise ValueError(f"invalid app company name(s): {bad}")
    return ",".join(sorted(companies))


def _read_stored(profile: str) -> list[object] | None | _Unset:
    """The raw ``app_companies`` field, ``None`` when absent, ``_UNSET`` when unreadable.

    Reads the same secret `auth/profiles.py::get_credentials` does; only the one
    non-secret field is kept. A test suite that never touches AWS stubs this function
    (tests/conftest.py).
    """
    from cube_cloud.auth import profiles  # local: keeps boto3 off the import path of callers' tests

    try:
        secret = profiles.read_profile_secret(profile)
    except profiles.ProfileSecretNotFound:
        return None  # no secret at all: "not migrated" (the profile has no creds anyway)
    except Exception as e:  # noqa: BLE001 -- class only; the message can quote the secret id
        # Denied, corrupt or a network failure is UNREADABLE, never "not migrated": the
        # absent branch falls back to the map, which is exactly what must not widen.
        logger.warning("app companies: could not read profile secret for %s (%s)", profile, type(e).__name__)
        return _UNSET
    if "app_companies" not in secret:
        return None
    value = secret["app_companies"]
    return value if isinstance(value, list) else [value]


def _from_stored(profile: str, raw: list[object]) -> AppCompanies | None:
    if not raw or not all(is_valid_name(n) for n in raw):
        if profile not in _malformed_logged:
            _malformed_logged.add(profile)
            logger.error(
                "app companies: profile %s has a malformed app_companies field (%d entries); "
                "denying app access until provision-access.py rewrites it", profile, len(raw),
            )
        return None
    return AppCompanies(home=str(raw[0]), held=frozenset(str(n) for n in raw), source="stored")


def _fallback(profile: str) -> AppCompanies:
    home = PROFILE_COMPANY_MAP.get(profile, profile)
    return AppCompanies(home=home, held=frozenset({home}), source="fallback")


def _stored(profile: str) -> list[object] | None | _Unset:
    """The field, cached; on a failed read, the last one read (``_UNSET`` if never)."""
    now = time.monotonic()
    with _lock:
        hit = _cache.get(profile)
    if hit and hit[0] > now:
        return hit[1]
    raw = _read_stored(profile)
    with _lock:
        if isinstance(raw, _Unset):  # never cached, so the next call retries the read
            if profile in _last_read:
                logger.warning("app companies: reusing the last set read for %s", profile)
                return _last_read[profile]
            return raw
        _cache[profile] = (now + CACHE_TTL_SECONDS, raw)
        _last_read[profile] = raw
    return raw


def reads_stored_sets() -> bool:
    """False on a stack pinned to the BASELINE (`app_companies_source` != "stored").

    Secrets and Teleport roles are shared by dev and prod; this per-stack setting is
    what lets one stack validate stored sets while the other keeps today's behaviour,
    and flipping it back is the rollback. Anything but "stored" means baseline.
    """
    from cube_cloud.config import settings

    return (settings.app_companies_source or "").strip().lower() == "stored"


def can_combine(companies: set[str] | frozenset[str]) -> bool:
    """Whether one app may carry every company in ``companies`` on this stack.

    One company is always fine. More than one needs a "stored" stack and, when
    `settings.app_companies_combinable` is not "*" (its default), every company on that
    list. Dev carried a list of test companies while roles still matched `company` EXACTLY
    (such a role stops seeing an app the moment it gains a second company); it was removed
    once they were migrated (spec Phase 5). An empty value restricts to nothing combinable.
    """
    if len(companies) <= 1:
        return True
    if not reads_stored_sets():
        return False
    allowed = combinable_companies()
    return allowed is None or set(companies) <= allowed


def combinable_companies() -> frozenset[str] | None:
    """The companies this stack lets share one app: ``None`` for any (the "*" default).

    The one reading of `settings.app_companies_combinable`, shared by `can_combine` and
    the console session, so the expose picker states the same limit the write enforces.
    """
    from cube_cloud.config import settings

    raw = (settings.app_companies_combinable or "").strip()
    return None if raw == "*" else label_companies(raw)


def app_companies(profile: str) -> AppCompanies | None:
    """Resolve what ``profile`` holds. ``None`` means deny: callers must fail closed.

    Unscoped (admin) profiles hold everything and expose under ``DEFAULT_COMPANY`` by
    default. A stored set wins; an absent field (a profile never migrated) falls back to
    the transitional map. An unreadable secret resolves to the last set read for the
    profile and denies when there is none: once sets and the map diverge, the map can be
    WIDER than what the profile holds. The request already read this same secret for its
    Apollo credentials, so a first-read failure here is a rare blip, and it is never
    cached, so the next call retries.
    """
    if is_unscoped(profile):
        return AppCompanies(home=DEFAULT_COMPANY, held=frozenset(), unscoped=True, source="unscoped")
    if not reads_stored_sets():
        return _fallback(profile)  # baseline: the stored field is not even read
    raw = _stored(profile)
    if isinstance(raw, _Unset):
        return None
    if raw is None:
        return _fallback(profile)
    return _from_stored(profile, raw)


def clear_cache() -> None:
    with _lock:
        _cache.clear()
        _last_read.clear()
        _malformed_logged.clear()
