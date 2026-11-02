"""tbot health monitoring, lifecycle management, and on-demand kube cert generation.

tbot runs as an ECS sidecar container and generates short-lived credentials
via the Teleport Machine ID protocol (IAM join method).

Outputs:
  - identity at {data_dir}/identity/ (for tsh commands)
  - on-demand kubernetes certs via tbot oneshot (per profile+cluster)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

TBOT_DATA_DIR = Path(os.environ.get("TBOT_DATA_DIR", "/tbot-data"))
TELEPORT_PROXY = os.environ.get("TELEPORT_PROXY", "edgescaleai.teleport.sh:443")
TBOT_JOIN_TOKEN = os.environ.get("TBOT_JOIN_TOKEN", "cube-mcp-bot-iam")
KUBE_CERT_TTL = os.environ.get("KUBE_CERT_TTL", "24h")
KUBE_CACHE_TTL = int(os.environ.get("KUBE_CACHE_TTL_SECONDS", "82800"))  # 23h
APP_TYPE_CACHE_TTL = int(os.environ.get("APP_TYPE_CACHE_TTL_SECONDS", "3600"))
# App LABELS decide who may reach an app (browser_proxy/authz.py), so they get their own,
# much shorter clock: an app type never changes, but its audience does on every
# expose/unexpose. `forget_app` clears the entry on the task that made the change; this
# TTL bounds how long any OTHER task (prod runs two) serves the old audience.
APP_LABEL_CACHE_TTL = int(os.environ.get("APP_LABEL_CACHE_TTL_SECONDS", "60"))
# That TTL puts the app refresh (`tsh apps ls`, up to 30s) on the browser-proxy authz path
# once a minute per active app, so it is single-flighted like the kube listing below: one
# shell-out per profile at a time, a waiter that queued behind a refresh reuses it rather
# than re-running it, the wait is bounded, and a failure is remembered briefly so a bad
# `tsh` is one process per window rather than one per proxied request. Authorization
# still fails closed while it cannot look; this bounds the cost, not the answer.
# Longer than `_fetch_app_types`' own 30s ceiling: a waiter that gave up first would deny
# (authz fails closed) on a refresh that was still going to answer.
APP_REFRESH_LOCK_ACQUIRE_TIMEOUT = 35.0
APP_REFRESH_FAILURE_TTL = 5.0
# The identity whose `tsh apps ls` lists EVERY app: the unscoped `cube-mcp-bot` role
# (`app_labels: '*': '*'`). `get_app_company` reads labels off it for authorization, and
# `list_apps` hands its whole listing to the console's fleet Apps page, which then filters
# by `can_see`. Never a caller's own identity: `get_identity_path` falls back to the
# shared, unscoped identity when a profile has no per-role output, so a scoped listing
# is not a boundary (docs/console-spec.md §4.22, finding 4).
FLEET_LISTING_PROFILE = "admin"
KUBE_CLUSTER_LIST_CACHE_TTL = int(
    os.environ.get("KUBE_CLUSTER_LIST_CACHE_TTL_SECONDS", "60")
)

# How long a FAILED fleet listing is remembered. Much shorter than the success TTL
# and it exists for a different reason: to stop a convoy, not to save work.
#
# Nothing was cached on failure originally, so that a `tsh` blip could not pin
# "unavailable" for a whole minute. But the re-check inside the single-flight lock
# then never short-circuits a failing read: during a proxy outage every queued waiter
# re-enters the 30s shell-out WHILE HOLDING THE LOCK, so K concurrent cube-page loads
# serialize into 30*K seconds and each timeout leaks another `tsh`. A short negative
# entry bounds that at one shell-out per window while still recovering in seconds.
KUBE_CLUSTER_LIST_FAILURE_TTL = int(
    os.environ.get("KUBE_CLUSTER_LIST_FAILURE_TTL_SECONDS", "10")
)

# Longest a caller waits for the single-flight lock before giving up and reporting
# "could not look". Mirrors `console/cache.py::_ACQUIRE_TIMEOUT_SECONDS` and exists for
# the same convoy reason: an unbounded queue behind a 30s subprocess is unbounded tail
# latency on an endpoint every cube-page load hits.
KUBE_CLUSTER_LOCK_ACQUIRE_TIMEOUT = 20.0

# How long a Teleport kube_server heartbeat stays valid after the agent last
# announced itself. This is TELEPORT'S constant, not a measurement of ours, and it is
# the entire time constant of anything built on cluster PRESENCE: an agent that stops
# reporting keeps appearing in `tsh kube ls` until its heartbeat expires.
#
# Verified against the live fleet (2026-09-03) by reading `metadata.expires` off
# `tctl get kube_server` for all 56 registered clusters: every one expired between
# 804s and 887s in the future, i.e. a 900s TTL with announce intervals well inside
# it. `tsh kube ls` itself carries NO timestamp — name and labels only — which is why
# this bound has to be stated rather than measured on the read path.
TELEPORT_HEARTBEAT_TTL_SECONDS = int(
    os.environ.get("TELEPORT_HEARTBEAT_TTL_SECONDS", "900")
)

# Profile names that don't match a Teleport role directly
PROFILE_ROLE_MAP: dict[str, str] = {
    "admin": "cube-mcp-bot",
    "esaiadmin": "cube-mcp-bot",
}

# Dedicated Teleport role for minting App Service join tokens (the `expose`
# pathway). tbot writes a role-scoped identity at
# identity-roles/<TOKEN_MINTER_PROFILE>/; the directory name matches the role
# name so that cert carries ONLY token:create (least privilege).
TOKEN_MINTER_PROFILE = "cube-mcp-token-minter"
APP_TOKEN_TTL = os.environ.get("APP_TOKEN_TTL", "1h")


class TbotManager:
    """Monitor tbot sidecar health and credential availability."""

    def __init__(self, data_dir: Path = TBOT_DATA_DIR) -> None:
        self.data_dir = data_dir
        self.identity_dir = data_dir / "identity"
        self.identity_path = self.identity_dir / "identity"
        self.proxy = TELEPORT_PROXY
        self._kube_cache: dict[tuple[str, str], tuple[str, float]] = {}
        # Per (profile, cluster): one tbot oneshot at a time. Concurrent misses for one key
        # rewrote the same tbot.yaml while another tbot was reading it (review of PR 363,
        # where the AI tab's GPU read made three concurrent misses routine). Each lock is
        # kept with the loop it was made under, so a lock from a dead loop is replaced.
        self._kube_locks: dict[tuple[str, str], tuple[asyncio.AbstractEventLoop, asyncio.Lock]] = {}
        self._app_type_cache: dict[str, tuple[str, float]] = {}
        self._app_label_cache: dict[str, tuple[dict, float]] = {}
        # Per profile (a bounded set): the refresh lock, when a refresh last SUCCEEDED,
        # and until when a failed one is not retried. See APP_REFRESH_LOCK_ACQUIRE_TIMEOUT.
        self._app_refresh_locks: dict[str, asyncio.Lock] = {}
        self._app_refreshed_at: dict[str, float] = {}
        self._app_refresh_failed_until: dict[str, float] = {}
        # The whole listing from the last FLEET_LISTING_PROFILE refresh, for the console's
        # fleet Apps page: `(apps, expiry)`. Only that identity's listing is complete; a
        # scoped profile's refresh would store a partial fleet as if it were the whole.
        self._app_listing: tuple[list[dict], float] | None = None
        # ONE slot, deliberately not keyed by profile — `list_kube_clusters_detailed`
        # takes no profile (see its docstring). Fleet-wide and cheap to share: one
        # `tsh kube ls` answers for every cube, unlike the per-cube inventory lookup.
        # `(clusters, read_ok, expiry)`; a failed read is cached too, briefly.
        self._kube_cluster_cache: tuple[dict[str, dict], bool, float] | None = None
        self._kube_cluster_lock: asyncio.Lock | None = None

    @property
    def is_ready(self) -> bool:
        """Check if tbot has generated a valid identity file."""
        return self.identity_path.exists() and self.identity_path.stat().st_size > 0

    async def wait_ready(self, timeout: float = 60) -> bool:
        """Wait for tbot to generate credentials. Returns True if ready."""
        elapsed = 0.0
        interval = 2.0
        while elapsed < timeout:
            if self.is_ready:
                logger.info("tbot identity ready at %s", self.identity_path)
                return True
            await asyncio.sleep(interval)
            elapsed += interval
        logger.warning("tbot credentials not ready after %.0fs", timeout)
        return False

    def get_identity_path(self, profile: str = "admin") -> Path:
        """Return the identity file path for a given profile.

        Tries per-role identity first, falls back to the shared identity.
        """
        role_identity = self.data_dir / "identity-roles" / profile / "identity"
        if role_identity.exists() and role_identity.stat().st_size > 0:
            return role_identity
        return self.identity_path

    def token_minter_identity_path(self) -> Path:
        """Return the fixed path to the token-minter identity.

        Unlike get_identity_path(), this does NOT fall back to the shared
        identity — a missing minter identity must fail loudly (caller raises)
        rather than silently minting with an over-privileged cert.
        """
        return self.data_dir / "identity-roles" / TOKEN_MINTER_PROFILE / "identity"

    def tsh_base_args(self, profile: str = "admin") -> list[str]:
        """Return base tsh args for identity-based auth, scoped to a role."""
        return [
            "tsh",
            "--proxy", self.proxy,
            "-i", str(self.get_identity_path(profile)),
            "--insecure",
        ]

    def tctl_base_args(self) -> list[str]:
        """Return base tctl args authorized by the token-minter identity.

        Mirrors tsh_base_args but uses the fixed token-minter identity (never
        the shared fallback) and `--auth-server` (tctl talks to the auth API,
        which Teleport Cloud routes via the proxy address).
        """
        return [
            "tctl",
            "--auth-server", self.proxy,
            "-i", str(self.token_minter_identity_path()),
            "--insecure",
        ]

    def tsh_env(self) -> dict[str, str]:
        """Return minimal environment for running tsh."""
        return {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": "/tmp",
        }

    def tbot_env(self) -> dict[str, str]:
        """Return environment for running tbot oneshot.

        Includes AWS credential chain vars needed for IAM join method.
        """
        env = {
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": "/tmp",
        }
        # Pass through AWS credential chain for ECS task role (IAM join)
        for key in ("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",
                     "AWS_CONTAINER_CREDENTIALS_FULL_URI",
                     "AWS_CONTAINER_AUTHORIZATION_TOKEN",
                     "AWS_DEFAULT_REGION", "AWS_REGION",
                     "ECS_CONTAINER_METADATA_URI_V4"):
            val = os.environ.get(key)
            if val:
                env[key] = val
        return env

    async def _run_kube_ls(self, profile: str = "admin") -> list[dict]:
        """`tsh kube ls --format=json`, parsed. RAISES on any failure.

        The raising sibling of `list_kube_clusters_tsh`, which swallows every error
        to `[]`. Both spellings are needed and the difference is not stylistic: a
        caller that only lists cubes for a human can degrade to "none found", but a
        caller that draws a CONCLUSION from a cube's absence cannot — "Teleport does
        not list this cluster" and "we could not ask Teleport" are different facts,
        and collapsing them would render a working cube as disconnected every time
        `tsh` hiccupped. Same three-outcome discipline as
        `console/reads.py::_exposed_apps_read`.

        Each element is Teleport's own shape: `kube_cluster_name`, `labels`,
        `selected`, `scope`. There is **no timestamp in it** — see
        `TELEPORT_HEARTBEAT_TTL_SECONDS` for what presence in this list does and does
        not bound.
        """
        cmd = self.tsh_base_args(profile) + ["kube", "ls", "--format=json"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.tsh_env(),
            )
        except FileNotFoundError as e:
            raise RuntimeError("tsh not found in container") from e
        except OSError as e:
            # PermissionError (tsh present but not executable), or a fork failure
            # under PID/memory pressure. Normalized rather than allowed to escape:
            # every caller of this method treats RuntimeError as "could not look",
            # and an OSError reaching the console route is a 500 on a decoration
            # endpoint that is documented never to 5xx.
            raise RuntimeError(f"could not start tsh: {type(e).__name__}") from e

        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        except asyncio.TimeoutError as e:
            # `wait_for` cancels the WAIT, never the child. Without this the process
            # is orphaned — and on an endpoint every cube-page load hits, that leaks
            # one `tsh` per timeout for as long as the outage lasts.
            proc.kill()
            try:
                await proc.wait()
            except Exception:
                pass
            raise RuntimeError("tsh kube ls timed out") from e

        if proc.returncode != 0:
            raise RuntimeError(
                f"tsh kube ls failed: {stderr.decode(errors='replace').strip()[-500:]}"
            )
        try:
            # `errors="replace"`, like stderr above: non-UTF-8 output is a malformed
            # answer, not a crash, and a UnicodeDecodeError here escaped as a 500.
            parsed = json.loads(stdout.decode(errors="replace"))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"could not parse tsh kube ls output: {e}") from e
        if not isinstance(parsed, list):
            raise RuntimeError("tsh kube ls did not return a list")
        return [c for c in parsed if isinstance(c, dict)]

    async def list_kube_clusters_tsh(self, profile: str = "admin") -> list[str]:
        """Dynamically discover kube clusters via tsh kube ls.

        Degrades to `[]` on every failure — keep it that way for `cube_list`, and use
        `list_kube_clusters_detailed` anywhere absence has to stay distinguishable
        from a failed read.
        """
        try:
            return [
                name
                for c in await self._run_kube_ls(profile)
                if (name := c.get("kube_cluster_name"))
            ]
        except RuntimeError as e:
            logger.warning("tsh kube ls unavailable: %s", e)
            return []

    def _cluster_lock(self) -> asyncio.Lock:
        """The single-flight lock, replacing one bound to a dead event loop.

        `asyncio.Lock` binds to a loop lazily — only on the *contended* `acquire`
        path — so a lock contended under one loop raises `RuntimeError: ... bound to a
        different event loop` if it is later contended under another. Since nothing
        replaced it, that wedged this method with a permanent failure for the process
        lifetime. Not reachable under ECS (one loop per task) but reachable under
        `uvicorn --reload`, any future worker-thread loop, and in tests.

        Same recovery `console/cache.py::_lock_for` performs, for the same reason:
        recovering beats failing, and it costs one attribute check.
        """
        lock = self._kube_cluster_lock
        if lock is not None:
            bound = getattr(lock, "_get_loop", None)
            try:
                if bound is not None and lock.locked():
                    bound()  # raises RuntimeError if bound to another loop
                return lock
            except RuntimeError:
                logger.warning(
                    "teleport cluster lock was bound to a dead event loop; replacing"
                )
        self._kube_cluster_lock = asyncio.Lock()
        return self._kube_cluster_lock

    async def list_kube_clusters_detailed(self) -> tuple[dict[str, dict], bool]:
        """Live kube clusters as `name -> labels`, plus whether the read SUCCEEDED.

        `({}, True)` is "Teleport listed nothing"; `({}, False)` is "we could not
        ask". The boolean is the whole point — see `_run_kube_ls`.

        **Takes no `profile`, deliberately, and that is a safety property rather than
        an omission.** The listing is always read on the unscoped identity. A
        per-profile `tsh kube ls` is scoped by the Teleport role's
        `kubernetes_labels: {cube: [...]}`, but that scoping is only as good as the
        `cube` label — which just 18 of 56 live clusters advertise, since it needs
        teleport-agent module >= 0.5.0 (`docs/rbac-architecture.md`, and
        `scripts/provision-access.py::check_cube_labels`, which warns about exactly
        this). A scoped identity therefore UNDER-REPORTS arbitrarily, which for any
        consumer deciding connected/disconnected renders enrolled cubes as
        disconnected.
        
        Every other Teleport-backed tool here threads the caller's profile
        (`cube_list`, `cube_status`, `kubectl_exec`, `app_list` all do), so a caller
        following that convention would get a plausible-looking wrong answer. The
        parameter is absent so that mistake is unreachable rather than merely
        documented. Authorization belongs to the CALLER: this is a fleet membership
        test, and whoever calls it must already have decided which cubes the requester
        may be told about.

        **Fleet-wide and cached, because one call answers for every cube.** The
        opposite shape from the inventory join, where a lookup is per cube and so the
        cube list refuses to join at all: here the marginal cost of a second cube is
        zero. Single-flighted, with a bounded acquire so a hung shell-out cannot build
        an unbounded queue, and a short negative entry so a convoy cannot re-run it —
        see `KUBE_CLUSTER_LIST_FAILURE_TTL` and
        `KUBE_CLUSTER_LOCK_ACQUIRE_TIMEOUT`.
        """
        cached = self._live_clusters()
        if cached is not None:
            return cached

        lock = self._cluster_lock()
        try:
            await asyncio.wait_for(
                lock.acquire(), timeout=KUBE_CLUSTER_LOCK_ACQUIRE_TIMEOUT
            )
        except asyncio.TimeoutError:
            # Someone else is already shelling out and is taking too long. Reporting
            # "could not look" beats queueing behind them: the caller renders an
            # honest unknown now instead of blocking a browser request indefinitely.
            logger.warning(
                "teleport cluster listing: waited %.0fs for the single-flight lock; "
                "reporting unavailable rather than queueing",
                KUBE_CLUSTER_LOCK_ACQUIRE_TIMEOUT,
            )
            return {}, False

        try:
            # Re-check: a waiter that queued behind the holder must not re-run it.
            cached = self._live_clusters()
            if cached is not None:
                return cached
            try:
                rows = await self._run_kube_ls()
            except Exception as e:
                # Deliberately `Exception`, not `RuntimeError`. `_run_kube_ls`
                # normalizes what it anticipates, but anything it did not — and this
                # is a subprocess path — must still become "could not look" rather
                # than a 500 on a decoration endpoint.
                logger.warning(
                    "teleport kube cluster listing unavailable: %s",
                    e if isinstance(e, RuntimeError) else type(e).__name__,
                )
                self._kube_cluster_cache = (
                    {}, False, time.monotonic() + KUBE_CLUSTER_LIST_FAILURE_TTL,
                )
                return {}, False
            clusters = {
                name: (c.get("labels") or {})
                for c in rows
                if (name := c.get("kube_cluster_name"))
            }
            self._kube_cluster_cache = (
                clusters, True, time.monotonic() + KUBE_CLUSTER_LIST_CACHE_TTL,
            )
            return self._copy_clusters(clusters), True
        finally:
            lock.release()

    def _live_clusters(self) -> tuple[dict[str, dict], bool] | None:
        """The unexpired cache entry, or None. Monotonic clock, like `console/cache.py`:
        a wall-clock jump must not extend an entry's validity."""
        entry = self._kube_cluster_cache
        if entry is None:
            return None
        clusters, ok, expiry = entry
        if expiry <= time.monotonic():
            self._kube_cluster_cache = None
            return None
        return self._copy_clusters(clusters), ok

    @staticmethod
    def _copy_clusters(clusters: dict[str, dict]) -> dict[str, dict]:
        """A defensive copy of the cached listing.

        The cache is process-lifetime and shared by every request, so handing out the
        stored object would let one consumer's mutation poison the fleet view for
        everyone until the TTL expired. Cheap at fleet scale (~56 small dicts) and
        only on a hit.
        """
        return {name: dict(labels) for name, labels in clusters.items()}

    async def get_kube_kubeconfig(self, cluster: str, profile: str = "admin") -> tuple[str, str]:
        """Get a kubeconfig path for a kube cluster, using cache when possible.

        Runs tbot in oneshot mode to generate a kubernetes (v1) output with
        role-scoped certs. Results are cached per (profile, cluster) for ~23h.

        Returns (kubeconfig_path, error_message). On success error is empty.
        """
        cache_key = (profile, cluster)
        hit = self._cached_kubeconfig(cache_key)
        if hit:
            return hit, ""
        loop = asyncio.get_running_loop()
        entry = self._kube_locks.get(cache_key)
        if entry is None or entry[0] is not loop:
            entry = (loop, asyncio.Lock())
            self._kube_locks[cache_key] = entry
        async with entry[1]:
            # A caller that queued behind a generation uses its result.
            hit = self._cached_kubeconfig(cache_key)
            if hit:
                return hit, ""
            return await self._generate_kubeconfig(cluster, profile)

    def _cached_kubeconfig(self, cache_key: tuple[str, str]) -> str:
        cached = self._kube_cache.get(cache_key)
        if cached:
            kc_path, expiry = cached
            if time.time() < expiry and Path(kc_path).exists():
                return kc_path
            self._kube_cache.pop(cache_key, None)
        return ""

    async def _generate_kubeconfig(self, cluster: str, profile: str) -> tuple[str, str]:
        cache_key = (profile, cluster)
        dest_dir = f"/tmp/tbot-kube/{profile}/{cluster}"
        os.makedirs(f"{dest_dir}/id", exist_ok=True)
        os.makedirs(f"{dest_dir}/kube", exist_ok=True)

        config = {
            "version": "v2",
            "proxy_server": self.proxy,
            "onboarding": {"join_method": "iam", "token": TBOT_JOIN_TOKEN},
            "storage": {"type": "memory"},
            "oneshot": True,
            "certificate_ttl": KUBE_CERT_TTL,
            "outputs": [
                {
                    "type": "identity",
                    "destination": {"type": "directory", "path": f"{dest_dir}/id"},
                },
                {
                    "type": "kubernetes",
                    "roles": [PROFILE_ROLE_MAP.get(profile, profile)],
                    "kubernetes_cluster": cluster,
                    "destination": {"type": "directory", "path": f"{dest_dir}/kube"},
                },
            ],
        }

        cfg_path = f"{dest_dir}/tbot.yaml"
        with open(cfg_path, "w") as f:
            yaml.dump(config, f)

        cmd = [
            "tbot", "start", "-c", cfg_path,
            f"--proxy-server={self.proxy}",
            f"--certificate-ttl={KUBE_CERT_TTL}",
        ]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.tbot_env(),
            )
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        except asyncio.TimeoutError:
            return "", "tbot oneshot timed out"
        except FileNotFoundError:
            return "", "tbot not found in container"

        if proc.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            if "not found" in err.lower():
                return "", f"cluster '{cluster}' not found or not accessible for profile '{profile}'"
            return "", err[-500:]

        kc_path = f"{dest_dir}/kube/kubeconfig.yaml"
        if not Path(kc_path).exists():
            return "", "tbot oneshot did not generate kubeconfig"

        self._kube_cache[cache_key] = (kc_path, time.time() + KUBE_CACHE_TTL)
        logger.info("Generated kube creds for %s/%s (cached %ds)", profile, cluster, KUBE_CACHE_TTL)
        return kc_path, ""

    async def get_app_type(self, app_name: str, profile: str = "admin") -> str:
        """Return app type ("TCP" or "HTTP") for an app, using a TTL cache.

        On cache miss, fetches all apps via ``tsh apps ls`` and batch-populates
        the cache to avoid N+1 calls.  Falls back to ``"HTTP"`` on any error.
        """
        cached = self._app_type_cache.get(app_name)
        if cached:
            app_type, expiry = cached
            if time.time() < expiry:
                return app_type
            self._app_type_cache.pop(app_name, None)

        if not self.is_ready:
            logger.debug("tbot not ready, defaulting app type to HTTP for %s", app_name)
            return "HTTP"

        try:
            await self._refresh_apps(profile)
        except Exception as e:
            logger.warning("Failed to fetch app types: %s", e)
            return "HTTP"

        cached = self._app_type_cache.get(app_name)
        if cached:
            return cached[0]

        logger.debug("App %s not found in tsh apps ls, defaulting to HTTP", app_name)
        return "HTTP"

    async def get_app_company(self, app_name: str, profile: str = "admin") -> str | None:
        """Return the app's `company` Teleport label, or None if unknown.

        Defaults to the ``admin`` identity's visibility (which lists every
        app -- the ``cube-mcp-bot`` role's ``app_labels`` are ``'*':'*'``) so
        this reflects the app's REAL label regardless of the *caller's* own
        scope. That matters: it's the ground truth an authz check (§4.3)
        compares the caller's profile-mapped company against, not a view the
        caller itself is trusted to report.

        Cached for ``APP_LABEL_CACHE_TTL`` (60s), not the hour app TYPES get:
        once apps carry several companies, changing an app's audience is a routine
        expose/unexpose, and this is the lookup authorization compares against.
        `forget_app` drops an entry immediately on the task that changed it.
        """
        cached = self._app_label_cache.get(app_name)
        if cached:
            labels, expiry = cached
            if time.time() < expiry:
                return labels.get("company")
            self._app_label_cache.pop(app_name, None)

        if not self.is_ready:
            logger.debug("tbot not ready, cannot resolve company label for %s", app_name)
            return None

        try:
            await self._refresh_apps(profile)
        except Exception as e:
            logger.warning("Failed to fetch app labels: %s", e)
            return None

        cached = self._app_label_cache.get(app_name)
        return cached[0].get("company") if cached else None

    async def _refresh_apps(self, profile: str) -> None:
        """`_fetch_app_types`, single-flighted per profile. Raises when it cannot look;
        both callers already turn that into "unknown"."""
        if self._app_refresh_failed_until.get(profile, 0.0) > time.monotonic():
            raise RuntimeError("tsh apps ls failed moments ago; not retrying yet")
        queued_at = time.monotonic()
        lock = self._app_refresh_locks.setdefault(profile, asyncio.Lock())
        try:
            await asyncio.wait_for(lock.acquire(), timeout=APP_REFRESH_LOCK_ACQUIRE_TIMEOUT)
        except asyncio.TimeoutError:
            raise RuntimeError("tsh apps ls is already running and has not finished") from None
        try:
            if self._app_refreshed_at.get(profile, 0.0) >= queued_at:
                return  # refreshed while we waited: reuse it rather than shelling out again
            try:
                await self._fetch_app_types(profile)
            except Exception:
                self._app_refresh_failed_until[profile] = time.monotonic() + APP_REFRESH_FAILURE_TTL
                raise
            self._app_refreshed_at[profile] = time.monotonic()
        finally:
            lock.release()

    async def _fetch_app_types(self, profile: str = "admin") -> None:
        """Run ``tsh apps ls --format=json`` and batch-populate the type +
        label caches (one call feeds both -- see ``get_app_type``/``get_app_company``)."""
        cmd = self.tsh_base_args(profile) + ["apps", "ls", "--format=json"]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self.tsh_env(),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)

        if proc.returncode != 0:
            raise RuntimeError(f"tsh apps ls failed: {stderr.decode()}")

        apps = json.loads(stdout.decode())
        expiry = time.time() + APP_TYPE_CACHE_TTL
        label_expiry = time.time() + APP_LABEL_CACHE_TTL
        listing: list[dict] = []
        for app in apps:
            name = app.get("metadata", {}).get("name", "")
            uri = app.get("spec", {}).get("uri", "")
            app_type = "TCP" if uri.startswith("tcp://") else "HTTP"
            self._app_type_cache[name] = (app_type, expiry)
            labels = app.get("metadata", {}).get("labels") or {}
            self._app_label_cache[name] = (labels, label_expiry)
            if name:
                listing.append({"name": name, "uri": uri, "labels": dict(labels)})
        if profile == FLEET_LISTING_PROFILE:
            self._app_listing = (listing, label_expiry)

    async def list_apps(self) -> list[dict] | None:
        """Every app in the Teleport tenant -> `[{name, uri, labels}]`, or None if unknown.

        The listing `get_app_company` authorizes against (the unscoped identity's
        `tsh apps ls`), on the same 60s clock and through the same single-flighted
        refresh, so the console's fleet Apps page cannot list an app the browser proxy
        would refuse or omit one it would open. It is the WHOLE fleet: the caller
        filters it with `app_companies(profile).can_see`, and nothing here knows who is
        asking.

        None, never `[]`, when it cannot look (tbot not ready, `tsh` failed or timed
        out): an empty list is a real answer, and "no apps" must not stand in for
        "could not read them". Returns copies, so a caller cannot edit the snapshot.
        """
        snapshot = self._app_listing
        if snapshot is None or time.time() >= snapshot[1]:
            if not self.is_ready:
                return None
            try:
                await self._refresh_apps(FLEET_LISTING_PROFILE)
            except Exception as e:
                logger.warning("Failed to list apps (%s)", type(e).__name__)
                return None
            snapshot = self._app_listing
            if snapshot is None:
                return None
        return [{**a, "labels": dict(a["labels"])} for a in snapshot[0]]

    def forget_app(self, app_name: str) -> None:
        """Drop an app's cached labels after this process changed its audience.

        Also expires the fleet listing, so the next `list_apps` on this task re-lists
        rather than serving the pre-change entry for up to a minute. Teleport itself
        reflects the change only once the cube's app service has rolled out.
        """
        self._app_label_cache.pop(app_name, None)
        self._app_listing = None

    async def mint_app_token(self, ttl: str = APP_TOKEN_TTL, timeout: float = 30.0) -> str:
        """Mint a short-lived App Service join token via the minter identity.

        Returns the provision-token string (consumed when the app-service agent
        joins, then dead). Raises RuntimeError on any failure — a missing minter
        identity, a tctl/RBAC error, or unparseable output — so the caller never
        proceeds with an empty token.
        """
        identity = self.token_minter_identity_path()
        if not (identity.exists() and identity.stat().st_size > 0):
            raise RuntimeError(
                f"token-minter identity not available at {identity} — is the "
                "cube-mcp-token-minter role granted to the bot and tbot redeployed?"
            )

        cmd = self.tctl_base_args() + [
            "tokens", "add", "--type=app", f"--ttl={ttl}", "--format=json",
        ]
        proc = None
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=self.tsh_env(),
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError as e:
            # `wait_for` cancels the wait, not the process: kill it rather than orphan a
            # `tctl` (and a live token it may still print) per timed-out expose.
            if proc is not None and proc.returncode is None:
                proc.kill()
            raise RuntimeError("tctl tokens add timed out") from e
        except FileNotFoundError as e:
            raise RuntimeError("tctl not found in container") from e

        if proc.returncode != 0:
            raise RuntimeError(
                f"tctl tokens add failed: {stderr.decode(errors='replace').strip()[-500:]}"
            )

        try:
            payload = json.loads(stdout.decode())
        except json.JSONDecodeError as e:
            raise RuntimeError(f"could not parse tctl tokens add output: {e}") from e

        token = payload.get("token") or payload.get("metadata", {}).get("name")
        if not token:
            raise RuntimeError(f"tctl tokens add returned no token: {payload}")
        return token

    def status(self) -> dict:
        """Return tbot status info for health checks."""
        return {
            "data_dir": str(self.data_dir),
            "ready": self.is_ready,
            "identity": self.is_ready,
        }


# Module-level singleton
tbot = TbotManager()
