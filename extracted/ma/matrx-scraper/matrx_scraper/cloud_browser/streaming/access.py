"""Authorization seam — the ONE access answer, re-derived at every checkpoint.

The real Browser Manager backs this with
``iam.has_access_for('browser_profile', profile_id, level)`` plus the grant-
revision digest (OPEN(grant-revision-source)). WS-4 ships a fixture resolver
with a bumpable grant revision so every revocation assertion runs with no
Browser Manager and no `browser.*` schema.

Load-bearing rule (S4 §3.2 B7): the ticket says what was ASKED FOR; the resolver
says what is TRUE. Access is re-derived from the canonical resolver at claim, at
every renewal, and NEVER from the ticket's own assertion. Access never depends on
the active organization — every check keys on the user.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Protocol

# Canonical DB enum; UI shows view/edit/full. "admin" = item-level Full, never
# organization admin (SHARE_LEVELS.md).
LEVEL_ORDER = {"viewer": 1, "editor": 2, "admin": 3}


@dataclass(frozen=True)
class AccessAnswer:
    """The resolver's verdict at one instant."""

    has_access: bool
    level: str  # "viewer" | "editor" | "admin" | "" when none
    grant_revision: int
    membership_ok: bool = True

    def meets(self, required: str) -> bool:
        if not self.has_access:
            return False
        return LEVEL_ORDER.get(self.level, 0) >= LEVEL_ORDER.get(required, 99)


class AccessResolver(Protocol):
    def resolve(self, *, user_id: str, profile_id: str) -> AccessAnswer: ...


@dataclass
class _Grant:
    level: str
    revision: int
    membership_ok: bool = True
    revoked: bool = False


class FixtureAccessResolver:
    """In-memory stand-in for ``iam.has_access_for`` + the grant-revision digest.

    Every mutation (grant/revoke/lower/expire/membership change) bumps the grant
    revision, exactly as the real digest does over (level, expires_at, source
    rows, membership state) — so B7 detects it without anyone writing an app-level
    flag. This is the fixture the standalone revocation proofs drive.
    """

    def __init__(self) -> None:
        self._grants: dict[tuple[str, str], _Grant] = {}
        self._rev = 0
        self._lock = threading.Lock()

    def _bump(self) -> int:
        self._rev += 1
        return self._rev

    def grant(self, *, user_id: str, profile_id: str, level: str) -> AccessAnswer:
        with self._lock:
            g = _Grant(level=level, revision=self._bump())
            self._grants[(user_id, profile_id)] = g
            return AccessAnswer(True, level, g.revision)

    def revoke(self, *, user_id: str, profile_id: str) -> None:
        with self._lock:
            g = self._grants.get((user_id, profile_id))
            if g:
                g.revoked = True
                g.revision = self._bump()

    def lower(self, *, user_id: str, profile_id: str, level: str) -> None:
        with self._lock:
            g = self._grants.get((user_id, profile_id))
            if g:
                g.level = level
                g.revision = self._bump()

    def drop_membership(self, *, user_id: str, profile_id: str) -> None:
        with self._lock:
            g = self._grants.get((user_id, profile_id))
            if g:
                g.membership_ok = False
                g.revision = self._bump()

    def resolve(self, *, user_id: str, profile_id: str) -> AccessAnswer:
        with self._lock:
            g = self._grants.get((user_id, profile_id))
            if g is None or g.revoked or not g.membership_ok:
                # Still report the current revision so a claim carrying a stale
                # revision is rejected rather than mistaken for "never granted".
                rev = g.revision if g else self._rev
                return AccessAnswer(
                    False,
                    "" if g is None or g.revoked else g.level,
                    rev,
                    membership_ok=(g.membership_ok if g else True),
                )
            return AccessAnswer(True, g.level, g.revision, membership_ok=True)
