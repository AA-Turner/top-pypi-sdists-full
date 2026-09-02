"""
InnoDay-backed implementation of blastoff's ``VersionStore``.

This is the DB/API backend that makes InnoDay the "version backbone" for a
project: instead of blastoff reading/writing version state from a local
``org-versions.json`` / ``.innoday/project.yml`` file, an
``InnoDayVersionStore`` reads the current version from the project's
``Release`` rows and records a completed release as a new ``Release`` row.

Backend choice -- API-backed (approach b in the PF-369 design)
--------------------------------------------------------------
The store talks to the InnoDay **HTTP API** via the same ``InnoDayAPIClient``
the CLI's ``innoday releases create/list`` commands already use, rather than a
direct SQLModel ``Session``. Reasons:

* The proxy commands (``innoday release`` / ``innoday hotfix``) run
  **client-side**, from a developer's workspace, resolving org/project from
  ``.innoday/project.yml`` -- exactly like ``innoday releases create``. There
  is no DB session available client-side, and there is no ``ReleaseService``
  layer to reuse (releases are handled inline in ``src/routers/releases.py``).
* Reusing ``InnoDayAPIClient`` mirrors the existing, tested release-record
  path (create-or-update via 409 -> PATCH), so recording is idempotent for
  free and works against local/dev/prod APIs identically.

The GitHub org and the topic list that blastoff needs are **resolved from
InnoDay** by the proxy (``/onboarding/resolve``, the same answer ``innoday init``
uses) and passed in. They used to come from a hand-maintained ``release_configs``
block in ``.innoday/project.yml`` -- one answer stored twice, with nothing keeping
the copies in step.

Semver math reuses ``blastoff.version_manager.SemanticVersion`` so the
next-version computation matches blastoff's own bump logic exactly.
"""

import asyncio
import logging
import threading
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from blastoff.stores import VersionStore
from blastoff.version_manager import OrgConfig, SemanticVersion

logger = logging.getLogger(__name__)

# Version blastoff should target for a project that has never been released.
# Kept intentionally simple (see PF-369 design "bootstrap"): the first release
# of a project starts the v0.1.0 milestone series.
BOOTSTRAP_VERSION = "v0.1.0"


class _StoreLoop:
    """One event loop for every async call this module makes, on one thread.

    ``VersionStore`` is a synchronous interface and ``InnoDayAPIClient`` is
    async, so the bridge has to run coroutines from a sync stack. The obvious
    bridge -- ``asyncio.run`` per call -- is wrong here, and wrong in a way that
    stayed hidden for a long time: it creates a loop, runs the coroutine, and
    **closes** the loop. The client's ``httpx.AsyncClient`` keeps its connection
    pool across calls, so the second call reuses a connection whose transport
    belongs to the first call's dead loop:

        File "httpcore/_async/http11.py", in _response_closed
        File "asyncio/selector_events.py", in close
            self._loop.call_soon(self._call_connection_lost, None)
        RuntimeError: Event loop is closed

    ...raised from inside a *request*, not from teardown, which is why it reads
    like a shutdown problem and is not one.

    Nothing hit it while ``load_org_config`` made exactly one request. It began
    failing when the pipeline work added a second (the IN_PROGRESS lookup beside
    the released one), which is the first time two requests ran in one command.

    A single long-lived loop on a daemon thread fixes it for good: every request
    and the client's own ``close`` see the same loop, so the pool stays valid.
    """

    _lock = threading.Lock()
    _loop: Optional[asyncio.AbstractEventLoop] = None

    @classmethod
    def run(cls, coro):
        with cls._lock:
            if cls._loop is None or cls._loop.is_closed():
                cls._loop = asyncio.new_event_loop()
                threading.Thread(
                    target=cls._loop.run_forever,
                    name="innoday-store-loop",
                    daemon=True,
                ).start()
            loop = cls._loop
        return asyncio.run_coroutine_threadsafe(coro, loop).result()


def _run_sync(coro):
    """Run an async coroutine to completion from a synchronous context.

    Always on :class:`_StoreLoop`, never on the caller's loop and never on a
    throwaway one -- see that class for why the per-call ``asyncio.run`` this
    replaced could not work once more than one request happened per command.
    """
    return _StoreLoop.run(coro)


def close_on_store_loop(coro) -> None:
    """Await a client's ``close()`` on the same loop its requests ran on.

    Exported for the CLI proxy's teardown. Closing an ``httpx.AsyncClient`` from
    a different loop than the one that opened its connections raises the same
    "Event loop is closed" this module exists to avoid.
    """
    _StoreLoop.run(coro)


class InnoDayVersionStore(VersionStore):
    """Read/record blastoff version state against the InnoDay releases API.

    Parameters
    ----------
    api_client:
        A constructed ``InnoDayAPIClient`` (carries auth/org headers).
    org_id:
        InnoDay organization UUID (used in the ``/organizations/{org_id}/...``
        API path).
    project_id:
        InnoDay project UUID -- required, since a ``Release`` belongs to a
        project and version strings are unique per project.
    github_org:
        The GitHub organization blastoff tags repos in (project.yml
        ``release_config.organization``). Surfaced as ``OrgConfig.organization``.
    topics:
        The GitHub topic used to select the project's repos (project.yml
        resolved from InnoDay). A **list** -- a project's repositories are found
        by its own alias plus any extra topics configured for it, and passing
        only the first is how a repository lands in a project but not in that
        project's release. Surfaced as ``OrgConfig.topics``.
    prerelease:
        Optional prerelease channel ("alpha"/"beta"/"rc") from project.yml,
        carried through onto the ``OrgConfig`` for parity with the file store.
    """

    def __init__(
        self,
        api_client,
        org_id: str,
        project_id: str,
        github_org: str,
        topics,
        prerelease: Optional[str] = None,
    ):
        self._api = api_client
        self._org_id = org_id
        self._project_id = project_id
        self._github_org = github_org
        # Accepts a list, or a comma-separated string from an older caller.
        self._topics = (
            list(topics)
            if isinstance(topics, (list, tuple))
            else [t.strip() for t in str(topics or "").split(",") if t.strip()]
        )
        self._prerelease = prerelease

    # ------------------------------------------------------------------ #
    # VersionStore interface
    # ------------------------------------------------------------------ #

    def load_org_config(self, alias: str) -> OrgConfig:
        """Build an ``OrgConfig`` for ``alias`` from the project's Release rows.

        ``next_version`` -- the tag blastoff is about to push to every repo -- is
        **the project's IN_PROGRESS release**, slot 1 of its two-slot pipeline.
        That row is what the dashboard and the Releases tab call the next launch,
        so the page and the command now name the same version by construction.

        They did not before, and the divergence was silent. This method derived
        the tag from ``max(released).bump_minor()`` while reading *only*
        ``status="released"`` rows -- the upcoming ones were invisible to it. A
        project that had shipped v1.8.0 and carried a planned v2.0.0 (opened by
        board sync from a version label) showed v2.0.0 on screen and tagged
        v1.9.0, then left v2.0.0 dangling because nothing revisited it.

        The old derivation survives as the fallback for a project whose pipeline
        has not been established yet -- one that has released rows but nothing
        upcoming. A project with nothing at all still bootstraps to
        :data:`BOOTSTRAP_VERSION`, which is the value ``ensure_pipeline`` opens
        slot 1 with, so the two agree there too.

        Raises ``FileNotFoundError`` only when the project genuinely cannot be
        resolved (no org/project id) -- matching the interface contract that a
        missing config surfaces as ``FileNotFoundError``.
        """
        if not self._org_id or not self._project_id:
            raise FileNotFoundError(
                f"Cannot resolve InnoDay project for alias '{alias}': "
                "org_id/project_id not set (run inside a project workspace "
                "with a valid .innoday/project.yml)."
            )

        max_released, max_released_at = self._max_released()
        last_released_version = max_released
        in_progress = self._in_progress_version()

        if in_progress is not None:
            next_version = in_progress
            logger.info(
                "InnoDayVersionStore alias=%s project_id=%s cutting %s "
                "(the project's in-progress release)",
                alias,
                self._project_id,
                in_progress,
            )
        elif max_released is None:
            next_version = BOOTSTRAP_VERSION
            logger.info(
                "InnoDayVersionStore bootstrapping alias=%s project_id=%s -- "
                "no released versions found, starting at %s",
                alias,
                self._project_id,
                BOOTSTRAP_VERSION,
            )
        else:
            next_version = (
                SemanticVersion.from_string(max_released).bump_minor().to_string()
            )
            logger.info(
                "InnoDayVersionStore alias=%s project_id=%s has no in-progress "
                "release; falling back to a minor bump of %s -> %s",
                alias,
                self._project_id,
                max_released,
                next_version,
            )

        return OrgConfig(
            alias=alias,
            organization=self._github_org,
            topics=self._topics,
            next_version=next_version,
            prerelease=self._prerelease,
            # When the last release *happened*, which is what bounds blastoff's
            # changelog window. This was hardcoded None, and blastoff read no
            # other boundary, so `list_merged_pull_requests_since(None)` returned
            # every merged PR the org had ever had and the release reported the
            # whole history as its contents.
            #
            # Supplying it fixes that only for a project that has actually
            # shipped through InnoDay -- `released_at` exists on a released row
            # and nowhere else. On 2026-08-11 that was PF alone. For every other
            # project blastoff's own fallback (the previous release tag's commit
            # date, read from GitHub) is what bounds the window, which is why
            # that fallback is not redundant with this line.
            last_released=max_released_at,
            last_released_version=last_released_version,
        )

    def save_org_config(self, org: OrgConfig) -> None:
        """No-op for the InnoDay backend.

        Unlike the file backend, InnoDay does not persist ``next_version`` as
        stored state: the authoritative next version is *derived* from the
        project's ``Release`` rows every time ``load_org_config`` runs (max
        released -> minor bump). There is therefore nothing to write back here
        -- the release itself is recorded via :meth:`record_release`, and the
        next call to ``load_org_config`` recomputes ``next_version`` from that
        new row. No file is ever touched.
        """
        logger.debug(
            "InnoDayVersionStore.save_org_config is a no-op "
            "(next_version is derived from Release rows, not stored)."
        )

    def record_release(
        self,
        org: OrgConfig,
        version: str,
        released_at: Optional[str] = None,
        summary: Optional[str] = None,
        changelog: Optional[List] = None,
    ) -> None:
        """Record ``version`` as a released ``Release`` row via the API.

        Idempotent: uses the same create-or-update (409 -> PATCH) semantics as
        ``innoday releases create --if-exists update``, so re-running a release
        that already recorded its version updates the existing row rather than
        failing.

        ``changelog`` arrives as blastoff's list-of-``{repo, prs}`` shape;
        InnoDay's ``Release.changelog`` column is a dict, so we wrap it as
        ``{"repos": [...]}`` -- the contract InnoDay's release router / CLI
        already expect for a structured per-repo inventory.
        """
        released_iso = released_at or datetime.now(timezone.utc).isoformat()

        body = {
            "version": version,
            "project_id": self._project_id,
            "status": "released",
            "released_at": released_iso,
        }
        if summary is not None:
            body["summary"] = summary
        if changelog is not None:
            body["changelog"] = self._wrap_changelog(changelog)

        _run_sync(self._create_or_update_release(body))
        logger.info(
            "InnoDayVersionStore recorded release version=%s project_id=%s org_id=%s",
            version,
            self._project_id,
            self._org_id,
        )

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _wrap_changelog(changelog: List) -> dict:
        """Wrap blastoff's list changelog into InnoDay's dict column shape."""
        return {"repos": changelog}

    def _in_progress_version(self) -> Optional[str]:
        """The version in slot 1, or ``None`` if the project has no pipeline yet.

        ``reconcile_statuses`` guarantees at most one IN_PROGRESS row per project,
        but this takes the highest by semver rather than trusting that: this runs
        client-side against whatever the API returns, and picking arbitrarily from
        two rows would make the tag depend on row order.
        """
        # The literal, matching `_max_released_version`'s "released": this module
        # runs client-side against the HTTP API and deliberately does not import
        # InnoDay's domain models. The API parses it against `ReleaseStatus` by
        # *value*, which is lowercase with an underscore.
        releases = _run_sync(self._list_releases(status="in_progress"))

        best: Optional[SemanticVersion] = None
        best_str: Optional[str] = None
        for row in releases:
            version = row.get("version")
            if not version:
                continue
            try:
                parsed = SemanticVersion.from_string(version)
            except ValueError:
                # A non-semver row cannot be bumped or compared, but it is a
                # deliberate tag someone chose -- cutting it is correct, and it
                # only loses to a semver row that outranks it.
                if best is None and best_str is None:
                    best_str = version
                continue
            if best is None or self._is_greater(parsed, best):
                best = parsed
                best_str = version
        return best_str

    def ticket_picture(self, version: str) -> Optional[Tuple[int, int]]:
        """``(planned, unfinished)`` for one version, or ``None`` if unknowable.

        **The half of the dry run blastoff structurally cannot provide.** The
        engine never queries tickets -- it works from GitHub merge dates -- so a
        dry run could say what pull requests were in a release and nothing at all
        about the work planned into it. The counts are already on every release
        row the API returns (``ticket_count`` / ``open_ticket_count``), so this
        costs one request the caller was going to make anyway.

        ``None``, not ``(0, 0)``, when the row cannot be found or the API refuses:
        "we could not ask" and "nothing is planned in" are different answers and
        printing the second for the first would be the dry run lying quietly.
        """
        try:
            releases = _run_sync(self._list_releases())
        except Exception:  # noqa: BLE001 -- informational only, never blocks
            return None
        for row in releases:
            if row.get("version") != version:
                continue
            total = row.get("ticket_count")
            open_ = row.get("open_ticket_count")
            if total is None or open_ is None:
                return None
            return int(total), int(open_)
        return None

    def _max_released(self) -> Tuple[Optional[str], Optional[str]]:
        """The highest (by semver) ``status=released`` version and when it shipped.

        Returns ``(version, released_at)``, both None when there are no valid
        released versions. Versions that don't parse as semver are skipped
        (defensive -- the column is a free-form string).

        The timestamp travels with the version because they answer one question
        between them: the version is the base blastoff bumps and compares tags
        against, and ``released_at`` bounds the changelog window. Reading them
        separately would mean two passes over the same rows and the standing risk
        of pairing a version with a different row's timestamp.

        ``released_at`` may be None on a row -- it is nullable, and a release
        recorded outside blastoff need not carry one -- so callers must treat the
        timestamp as optional even when the version is present.
        """
        releases = _run_sync(self._list_releases(status="released"))

        best: Optional[SemanticVersion] = None
        best_str: Optional[str] = None
        best_at: Optional[str] = None
        for r in releases:
            version = r.get("version")
            if not version:
                continue
            try:
                sv = SemanticVersion.from_string(version)
            except ValueError:
                logger.debug(
                    "Skipping unparseable release version '%s' for project_id=%s",
                    version,
                    self._project_id,
                )
                continue
            if best is None or self._is_greater(sv, best):
                best = sv
                best_str = version
                best_at = r.get("released_at")
        return best_str, best_at

    def _max_released_version(self) -> Optional[str]:
        """The highest ``status=released`` version. See :meth:`_max_released`."""
        return self._max_released()[0]

    @staticmethod
    def _is_greater(a: SemanticVersion, b: SemanticVersion) -> bool:
        """True if semver ``a`` > ``b`` (comparing on major/minor/patch only).

        Prerelease ordering is intentionally ignored for "max released" -- a
        released row is a stable version; this keeps the comparison simple and
        matches blastoff treating released versions as stable bases.
        """
        return (a.major, a.minor, a.patch) > (b.major, b.minor, b.patch)

    async def _list_releases(self, status: Optional[str] = None) -> List[dict]:
        """GET the project's releases, optionally filtered by status."""
        params = {"project_id": self._project_id}
        if status:
            params["status"] = status
        response = await self._api.get(
            f"/organizations/{self._org_id}/releases", params=params
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to list releases: HTTP {response.status_code} -- "
                f"{getattr(response, 'text', '')}"
            )
        return response.json()

    async def _create_or_update_release(self, body: dict) -> None:
        """POST a new release, PATCHing the existing one on a 409 conflict."""
        response = await self._api.post(
            f"/organizations/{self._org_id}/releases", json=body
        )

        if response.status_code in (200, 201):
            return

        if response.status_code == 409:
            # Already recorded -- update it in place (idempotent re-run).
            version = body["version"]
            lookup = await self._api.get(
                f"/organizations/{self._org_id}/releases/by-version/{version}",
                params={"project_id": self._project_id},
            )
            if lookup.status_code != 200:
                raise RuntimeError(
                    f"Release '{version}' exists but could not be looked up for "
                    f"update: HTTP {lookup.status_code}"
                )
            release_id = lookup.json()["id"]
            update_body = {k: v for k, v in body.items() if k != "project_id"}
            patch = await self._api.patch(
                f"/organizations/{self._org_id}/releases/{release_id}",
                json=update_body,
            )
            if patch.status_code != 200:
                raise RuntimeError(
                    f"Failed to update existing release '{version}': "
                    f"HTTP {patch.status_code} -- {getattr(patch, 'text', '')}"
                )
            return

        raise RuntimeError(
            f"Failed to record release: HTTP {response.status_code} -- "
            f"{getattr(response, 'text', '')}"
        )
