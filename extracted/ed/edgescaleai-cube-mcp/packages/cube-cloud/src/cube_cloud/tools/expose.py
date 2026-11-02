"""expose/unexpose/list_exposed: register/remove/list a cube service as a
Teleport app (account-less).

All three are thin facades over the module tools, preconfigured for the
Teleport Multi-App Service module — one shared module installation per
environment, serving any number of apps via its `apps` variable (a JSON
array, since Apollo module variables have no native list type). `expose`
installs the module on the first app and idempotently upserts into its `apps`
list on every call after; `unexpose` removes an app (or, with `all=True`,
every app exposed to the caller's home company alone) from that list, tearing the whole module
down (unlink + uninstall its entity) automatically once no apps remain, since
the module's agent pod fails to initialize on an empty `apps` list;
`list_exposed` reads that same `apps` list without mutating it.

A scoped (non-admin) caller's company boundary is enforced everywhere here, and what
it may LEARN depends on the stack. On a "map" stack `list_exposed` never surfaces an
app outside the companies the caller holds. On a "stored" stack it lists every app on
the cube with its audience (anyone who can see a cube sees what is exposed on it and
to whom: docs/multi-company-app-access-spec.md, model item 5), but never the target,
URL, rewrite or labels of an app the caller cannot reach. On both, `unexpose` treats
such an app as indistinguishable from one that doesn't exist.

Every mutating call mints a fresh short-lived App Service join token from the
cube-mcp bot's own identity (no human Teleport account) — any `apps` change
triggers a ConfigMap update and pod rollout, so a stale/already-consumed
token would break that rejoin.

Access to an exposed app is then account-less too. The address these tools
PUBLISH is the browser app proxy's — ``https://<qualified-name>.<apex>``, built
by ``browser_proxy/resolver.py::browser_app_url`` and reachable in a browser with
the same login cube-mcp already issues. The app's Teleport ``public_addr`` is
stored in Apollo for Teleport's own routing and is deliberately never rendered:
reaching it redirects to Teleport SSO, and those accounts are being retired.
``app_proxy`` is a separate, unrestricted path to the same app: it port-forwards
ANY exposed app to a local port for whatever wants one, and is the only way into a
``tcp://`` app. The two are independent and both work at once — these responses
just don't advertise the tunnel as the follow-up to publishing, so it is named
only where there is no URL. See docs/expose-token-minter-spec.md and
docs/browser-app-proxy-spec.md.
"""

from __future__ import annotations

import ast
import asyncio
import contextvars
import functools
import json
import logging
import os
import re
import time

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common import apollo_queries as Q

# App-company resolution lives in `auth/app_companies.py`, shared with the browser
# proxy and the console. DEFAULT_COMPANY / PROFILE_COMPANY_MAP / UNSCOPED_ROLE are
# re-exported because callers and tests have long reached them through this module.
from cube_cloud.auth.app_companies import (
    DEFAULT_COMPANY,
    PROFILE_COMPANY_MAP,
    UNSCOPED_ROLE,
    app_companies,
    can_combine,
    format_label,
    is_valid_name,
    label_companies,
    reads_stored_sets,
)
from cube_cloud.browser_proxy.resolver import (
    browser_app_url_or_reason,
    is_app_label,
    is_http_app,
)
from cube_cloud.teleport.tbot_manager import PROFILE_ROLE_MAP, tbot
from cube_cloud.tools.environments import _resolve_environment

logger = logging.getLogger(__name__)

# Apollo coordinate for the Teleport Multi-App Service module. Version is
# overridable via env so it can be bumped without a code change — confirm the
# live published version with get_product_releases / list_modules before
# relying on the default. The lookup that finds an existing installation
# (modules._find_module_by_coordinate) ignores the version segment on purpose,
# so bumping this does not orphan/duplicate already-installed environments.
#
# That version-agnostic lookup is also what makes a stale default INVISIBLE on
# every cube that already has the module: `expose` finds the installation and
# upserts into it regardless of what this string says, so the version here is
# only ever read on a FIRST install. It went stale exactly that way — the fleet
# moved to 0.3.0 by hand while this stayed 0.2.0 and nothing failed, until a
# legacy cube (`cube-9likqvpd`) was migrated and would have been handed the old
# module. Terraform passes the env var on both stacks so the deployed value is
# config rather than a code literal; `test_module_coordinate_pin.py` fails CI if
# the two disagree, because a drift here is silent by construction.
TELEPORT_MULTI_APP_SERVICE_MODULE = os.environ.get(
    "TELEPORT_MULTI_APP_SERVICE_MODULE_COORDINATE",
    "module:teleport-multi-app-service-module:0.3.0",
)
# Domain apps are served under (matches the Teleport proxy host).
TELEPORT_APP_DOMAIN = os.environ.get("TELEPORT_APP_DOMAIN", "edgescaleai.teleport.sh")


def _companies_unreadable(profile: str, verb: str) -> str:
    """The refusal for a profile whose app companies resolve to None (deny)."""
    return (
        f"{verb} refused: the app companies for profile '{profile}' are unreadable; "
        "an operator must repair them with scripts/provision-access.py."
    )


def protected_module_bases(profile: str) -> frozenset[str] | None:
    """Modules a caller may change only through expose/unexpose, never the generic tools.

    For a scoped profile: the Teleport multi-app module (its `apps` variable is every
    company's app list on the cube). None for an unscoped admin, who keeps the generic
    tools as the break-glass path. Passed by `main.py` to install_module /
    update_module_variables / uninstall_module; see `modules.protected_refusal`.
    """
    from cube_cloud.auth.app_companies import is_unscoped
    from cube_cloud.tools import modules

    if is_unscoped(profile):
        return None
    return frozenset({modules.module_base_coordinate(TELEPORT_MULTI_APP_SERVICE_MODULE)})


def _resolve_company(profile: str, requested: str | None) -> tuple[str | None, str | None]:
    """Resolve the company label for an expose/unexpose call -> (company, error).

    A scoped profile writes the company it names, which must be one it HOLDS, and its
    HOME company when it names none. On a "map" stack a profile holds only its home
    company, so this is exactly the old rule there: anything else is refused. Unscoped
    admin profiles may pass `requested`, falling back to DEFAULT_COMPANY. A profile
    whose app companies cannot be resolved is refused outright -- fail closed.
    Visibility (which apps a caller may SEE) is a different question: use
    `app_companies(profile).can_see(...)`, never a comparison against this result.
    """
    companies = app_companies(profile)
    if companies is None:
        return None, _companies_unreadable(profile, "expose")
    if companies.unscoped:
        # On a "stored" stack every label is parsed as a set of app company names, so a
        # name that is not one would be dropped on read (the app would look unlabelled)
        # and `format_label` refuses to write it. A "map" stack writes it verbatim, as it
        # always has: that is the baseline.
        if requested and reads_stored_sets() and not is_valid_name(requested):
            return None, (
                f"expose refused: '{requested}' is not an app company name this stack can "
                "read (lower-case letters, digits and '-')."
            )
        return (requested or DEFAULT_COMPANY), None
    target = requested or companies.home
    if target not in companies.held:
        if len(companies.held) == 1:
            return None, (
                f"expose refused: profile '{profile}' is scoped to company '{companies.home}'; "
                f"cannot expose under company='{requested}'."
            )
        return None, (
            f"expose refused: profile '{profile}' does not hold app company '{requested}'; "
            f"it can use: {', '.join(sorted(companies.held))}."
        )
    return target, None


_DNS_LABEL_RE = re.compile(r"[^a-z0-9-]+")
MAX_LABEL_LEN = 63  # single DNS label limit (leftmost label of <name>.<domain>)


def _sanitize_label(raw: str) -> str:
    """Lower-case and reduce a string to a valid DNS-label charset.

    Collapses any run of non-[a-z0-9-] characters to a single '-' and trims
    leading/trailing '-', so a raw app_name / env name can't produce an invalid
    Teleport app name or SNI host.
    """
    return _DNS_LABEL_RE.sub("-", raw.strip().lower()).strip("-")


def _qualified_app_name(app_name: str, env_name: str) -> tuple[str | None, str | None]:
    """Build a per-env-unique Teleport app name -> (name, error).

    Returns ``<app>-<env>`` (each part sanitized to a DNS label). Refuses if
    either part is empty after sanitizing, or the result exceeds the 63-char DNS
    label limit (it becomes the leftmost label of ``<name>.<domain>``).
    """
    app = _sanitize_label(app_name)
    env = _sanitize_label(env_name)
    if not app:
        return None, f"expose refused: app_name '{app_name}' has no valid DNS characters."
    if not env:
        return None, f"expose refused: environment '{env_name}' has no valid DNS characters."
    qualified = f"{app}-{env}"
    if len(qualified) > MAX_LABEL_LEN:
        return None, (
            f"expose refused: qualified app name '{qualified}' exceeds {MAX_LABEL_LEN} "
            "chars (DNS label limit). Pass a shorter app_name or an explicit public_addr."
        )
    return qualified, None


# --- Read-your-own-write -----------------------------------------------------------
#
# Every expose/unexpose READS the module's whole `apps` list, changes it, and WRITES the
# whole list back (Apollo module updates are full-replace). Apollo applies that write
# ASYNCHRONOUSLY: the mutation answers `UpdateRequested` and a read a moment later still
# returns the old list. So two changes to one cube a few seconds apart lost the first
# one -- the second started from the stale list and wrote it back without it. Found
# live on dev 2026-09-24 (an expose followed by adding a company); it is not specific
# to that, and affected prod too (two exposes back to back).
#
# Two measures, both scoped to what one process can guarantee:
#   * `_await_own_write`: after writing, poll until Apollo shows exactly what was
#     written (settled in under 5s on cube-66odzn95), so the NEXT change starts from
#     it -- including a teardown, which waits until the module is unlinking or gone.
#     Bounded; on timeout the response says so instead of claiming it landed.
#   * `_lock_cube`: expose/unexpose on one cube run one at a time, so two concurrent
#     calls in this process cannot read the same stale list. The key is the RESOLVED
#     environment id, taken after `_resolve_environment` has authorized the caller:
#     one key per cube however it was spelled (name, RID, unique substring), a set
#     bounded by the fleet, and no contention visible on a cube the caller cannot see.
#     The wait for it is bounded too, and a caller who outwaits it is REFUSED with
#     nothing written.
#   * One BUDGET per call (`CALL_BUDGET_SECONDS`, from the moment the call starts):
#     the lock wait, the join-token mint (a `tctl` shell-out allowed 30s on its own) and
#     the own-write wait each get only what is left of it. Bounding each phase alone
#     added up to ~68s, past the ALB's 60s idle timeout (it sends no bytes while the
#     handler runs), which is a transport error for a write that may still land. The
#     budget bounds the TOOL, not the request: the console's reads around it (notably
#     `fetch_services`, a kubectl shell-out with its own 60s ceiling) are outside it.
# Two calls landing at the same moment on DIFFERENT cube-cloud tasks (prod runs two)
# can still race; that needs a cross-task lock and is not attempted here.
OWN_WRITE_WAIT_SECONDS = float(os.environ.get("EXPOSE_OWN_WRITE_WAIT_SECONDS", "15"))
OWN_WRITE_POLL_SECONDS = 1.0
CUBE_LOCK_WAIT_SECONDS = float(os.environ.get("EXPOSE_CUBE_LOCK_WAIT_SECONDS", "20"))
CALL_BUDGET_SECONDS = float(os.environ.get("EXPOSE_CALL_BUDGET_SECONDS", "45"))
# Kept back from the lock wait for what must follow it: the module read, the mint and
# the write (a few seconds each when healthy). Without it a caller that waited the whole
# budget for the lock would have none left to write.
_AFTER_LOCK_RESERVE_SECONDS = 12.0
_WRITE_RESERVE_SECONDS = 4.0
NOT_YET_VISIBLE_NOTE = (
    "  Note:    Apollo has not shown this change yet. Wait a few seconds before "
    "changing this cube's exposed apps again, or the next change may undo this one."
)
CUBE_BUSY = (
    "another change to this cube's exposed apps is still being applied, so nothing was "
    "changed. Try again in a few seconds."
)
_cube_locks: dict[str, asyncio.Lock] = {}
_held_locks: contextvars.ContextVar[list[asyncio.Lock] | None] = contextvars.ContextVar(
    "expose_held_cube_locks", default=None,
)
_call_deadline: contextvars.ContextVar[float | None] = contextvars.ContextVar(
    "expose_call_deadline", default=None,
)


def _remaining() -> float:
    """Seconds left in this call's budget (unbounded outside a wrapped call)."""
    deadline = _call_deadline.get()
    return float("inf") if deadline is None else deadline - time.monotonic()


def _serialized_per_cube(fn):
    """Start the call's budget, and release, however it ends, the cube lock it took
    with `_lock_cube`."""
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        held: list[asyncio.Lock] = []
        token = _held_locks.set(held)
        deadline_token = _call_deadline.set(time.monotonic() + CALL_BUDGET_SECONDS)
        try:
            return await fn(*args, **kwargs)
        finally:
            _call_deadline.reset(deadline_token)
            _held_locks.reset(token)
            for lock in reversed(held):
                lock.release()

    return wrapper


def _cube_lock(env_id: str) -> asyncio.Lock:
    """The lock for ``env_id``, replacing one bound to a dead event loop (as
    `console/cache.py::_lock_for` does: otherwise it would stay held forever)."""
    lock = _cube_locks.get(env_id)
    if lock is not None and lock.locked():
        try:
            lock._get_loop()
        except RuntimeError:
            lock = None
    if lock is None:
        lock = _cube_locks[env_id] = asyncio.Lock()
    return lock


async def _lock_cube(env_id: str) -> bool:
    """Hold this cube's lock for the rest of the wrapped call -> False if it stayed busy."""
    held = _held_locks.get()
    if held is None:
        raise RuntimeError("_lock_cube needs a caller wrapped in @_serialized_per_cube")
    lock = _cube_lock(env_id)
    if lock.locked():
        wait = min(CUBE_LOCK_WAIT_SECONDS, _remaining() - _AFTER_LOCK_RESERVE_SECONDS)
        try:
            if wait <= 0:
                raise asyncio.TimeoutError
            await asyncio.wait_for(lock.acquire(), timeout=wait)
        except asyncio.TimeoutError:
            logger.warning("expose: env %s stayed busy; refusing", env_id)
            return False
    else:
        await lock.acquire()
    held.append(lock)
    return True


def _mint_timeout() -> float:
    """What the join-token mint may take: its own 30s ceiling, or less of the budget."""
    return max(1.0, min(30.0, _remaining() - _WRITE_RESERVE_SECONDS))


# `ApolloProductModuleInstallationStateV2` members, verified by introspection 2026-09-24:
# InstallRequested, Installed, UpdateRequested, UninstallRequested, Uninstalled,
# Cancelled. (An earlier guess, `Unlinking`, is not one of them.) Which of them
# LIST_MODULES reports for an installation being unlinked is NOT verified -- console-spec
# §4.4b records it reporting `Installed` throughout an UPDATE -- so nothing refuses a write
# on a state. The teardown wait below only accepts these as "done"; if LIST_MODULES shows
# `Installed` until the row goes, it waits for the row to go, which is also right.
_REMOVED_STATES = ("_UninstallRequested", "_Uninstalled")


def _module_state(module: dict) -> str:
    return (module.get("state") or {}).get("__typename") or ""


def _write_failed(result: str) -> bool:
    """A module write that reported failure: nothing to wait for."""
    return (result or "").lstrip().lower().startswith(("error", "failed", "module '"))


async def _await_own_write(client: ApolloClient, env_id: str, expected: list[dict] | None) -> bool:
    """Poll until Apollo shows our write -> whether it did, in budget.

    ``expected`` is the `apps` list written; ``None`` is a TEARDOWN, which has landed once
    the module is being uninstalled or gone. A teardown the next call could not see would hand it
    the pre-removal list to write back, re-declaring the app just removed.
    """
    from cube_cloud.tools import modules

    want = None if expected is None else json.dumps(expected, sort_keys=True)
    granted = max(0.0, min(OWN_WRITE_WAIT_SECONDS, _remaining()))
    deadline = time.monotonic() + granted
    while True:
        try:
            installations = await modules._fetch_module_installations(client, env_id)
            module = modules._find_module_by_coordinate(installations, TELEPORT_MULTI_APP_SERVICE_MODULE)
            if want is None:
                if module is None or _module_state(module).endswith(_REMOVED_STATES):
                    return True
            elif module is not None:
                apps, err = _load_apps(module)
                if not err and json.dumps(apps, sort_keys=True) == want:
                    return True
        except Exception as e:  # noqa: BLE001 -- class only: ApolloError text embeds module variables
            logger.warning("expose: re-read while awaiting own write failed (%s)", type(e).__name__)
        if time.monotonic() >= deadline:
            logger.warning("expose: Apollo did not show the write on env %s within %.1fs "
                           "(of %.0fs configured; the call's budget capped it)", env_id, granted,
                           OWN_WRITE_WAIT_SECONDS)
            return False
        await asyncio.sleep(OWN_WRITE_POLL_SECONDS)


def _publishable_result(result: str) -> str:
    """The module tool's confirmation, with the `apps` blob taken out of it.

    `update_module_variables` echoes the variables it wrote, and `apps` is the
    WHOLE shared module's app list: every company's app names, their internal
    service URIs, their company labels, and their Teleport addresses. `authToken`
    is masked because it is secret-NAMED; `apps` is not, so it printed verbatim
    into a scoped caller's own successful expose — the same blob
    `_unreadable_apps` refuses to quote and `console/writes._loggable` strips, and
    it is archived whole in the S3 telemetry sink.

    Only that one line is replaced. The rest of the confirmation is kept because
    `update_module_variables` reports failures as a STRING rather than raising, so
    dropping it would turn "the write did not apply" into silence.

    No count is given. The write is a full replace, so any number here is the
    total across all tenants — a smaller disclosure than the names and URIs, but
    still one the caller has no business receiving. `list_exposed` answers the
    question properly: per company, and never another tenant's internals.
    """
    from cube_cloud.tools import modules

    return modules.redact_variable_line(
        result, "apps", "<not shown; use list_exposed>"
    )


# Schemes Teleport's app service actually implements. This IS an allowlist,
# unlike the rewrite-header validation below: the set is closed by what Teleport
# supports, not by what we are willing to permit. Without it a typo
# (`https//`, `mqtt://`, a bare host) is stored silently and surfaces much later
# as a Teleport dial failure that does not name the cause.
ALLOWED_SCHEMES = ("http://", "https://", "tcp://")

# RFC 7230 `token` — the legal characters in an HTTP field name.
_HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")

# Headers TELEPORT itself refuses to let an app rewrite. Mirrored from
# `lib/srv/app/common/header.go::ReservedHeaders` (which appends
# `httplib/reverseproxy.XHeaders`), verified against gravitational/teleport
# 2026-09-14.
#
# This is NOT the policy allowlist §4.1 argues against — it is a copy of an
# upstream constraint, and the reason to copy it is that the failure is
# CUBE-WIDE. `servicecfg.App.CheckAndSetDefaults` returns
# `trace.BadParameter("... header %q is reserved and can't be rewritten")`, which
# fails config load for the whole `teleport-app-service` agent, not just the one
# app. The module is shared by every company on the cube, so one bad header
# crashloops the agent and takes every tenant's apps down — minutes after a
# tool response that said "Exposed", on a surface nothing here watches.
#
# Refusing them converts that outage into an `expose refused:` string. Anything
# NOT on this list still goes through untouched, so the no-allowlist decision
# stands for every header Teleport will actually accept.
_RESERVED_REWRITE_HEADERS = frozenset({
    "teleport-jwt-assertion",
    "cf-access-token",
    "x-forwarded-ssl",
    "x-teleport-api-error",
    "x-teleport-api-info",
    "x-teleport-aws-assumed-role",
    "x-teleport-aws-assumed-role-authorization",
    # reverseproxy.XHeaders
    "x-forwarded-proto",
    "x-forwarded-for",
    "x-forwarded-host",
    "x-forwarded-port",
    "x-forwarded-server",
    "x-real-ip",
})
# Teleport label keys/values: alphanumerics plus a few separators. Deliberately
# permissive (`app-type` on cube-9likqvpd has to survive) but excludes whitespace
# and control characters.
_LABEL_TOKEN_RE = re.compile(r"^[A-Za-z0-9._/-]+$")

MAX_REWRITE_HEADERS = 16
MAX_REWRITE_LINE_LEN = 512
MAX_EXTRA_LABELS = 16
MAX_LABEL_TOKEN_LEN = 128


def _validate_scheme(app_uri: str) -> str | None:
    """Refuse an `app_uri` whose scheme Teleport cannot serve -> error or None."""
    if not (app_uri or "").strip().lower().startswith(ALLOWED_SCHEMES):
        return (
            f"expose refused: app_uri '{app_uri}' must start with one of "
            f"{', '.join(ALLOWED_SCHEMES)}. A wrong scheme is stored without "
            "complaint and then fails at dial time with an unrelated-looking "
            "Teleport error."
        )
    return None


def _decode_json_arg(value, name: str, expected: type):
    """Accept either a JSON STRING or an already-decoded value -> (value, error).

    MCP tool arguments carry structured values as JSON strings — the convention
    every other structured argument in `proxy_tools.py` follows
    (`update_module_variables.variables`, `install_entity.config_overrides`,
    `create_secret.secret_keys`). Declaring a native `array`/`object` in the
    schema instead looked cleaner and failed against a real client, which sent
    the value as the string `"[...]"`; validation rejected it before reaching
    any of our code.

    The already-decoded branch is not redundant: `console/writes.py` calls these
    tools in-process with real Python objects, and a console route should not
    have to serialize to JSON just so this can parse it back.
    """
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as e:
            return None, (
                f"expose refused: {name} must be valid JSON ({e}). Pass a JSON "
                f"{'array' if expected is list else 'object'} as a string, e.g. "
                + ('\'["Host: app.internal"]\'' if expected is list
                   else '\'{"app-type": "console"}\'')
            )
    if not isinstance(value, expected):
        return None, (
            f"expose refused: {name} must be a JSON "
            f"{'array' if expected is list else 'object'}."
        )
    return value, None


def _validate_rewrite_headers(headers: list) -> tuple[list[str] | None, str | None]:
    """Validate a rewrite-header list -> (headers, error).

    STRUCTURAL validation only — there is deliberately no allowlist of header
    NAMES. An allowlist would buy "no Authorization/Cookie reaches the in-cube
    app", but that is not a boundary this tool holds anywhere else: `expose`
    already accepts an arbitrary `app_uri`, so a caller who can reach it can
    already point an app at anything in the cluster. Constraining names is
    friction, and it would land on exactly the legacy configs this exists to
    migrate — several of which have not been surveyed yet.

    What IS load-bearing is the CR/LF rejection: a newline in either half would
    inject *additional* headers into the request Teleport makes upstream, which
    is a real escalation rather than a naming preference.
    """
    if not isinstance(headers, list):
        return None, (
            "expose refused: rewrite_headers must be a JSON array of "
            '"Name: value" strings, e.g. ["Host: app.internal"].'
        )
    if len(headers) > MAX_REWRITE_HEADERS:
        return None, (
            f"expose refused: at most {MAX_REWRITE_HEADERS} rewrite headers "
            f"(got {len(headers)})."
        )
    cleaned: list[str] = []
    for raw in headers:
        if not isinstance(raw, str):
            return None, (
                f"expose refused: rewrite header {raw!r} is not a string; each "
                'entry must look like "Name: value".'
            )
        line = raw.strip()
        if len(line) > MAX_REWRITE_LINE_LEN:
            return None, (
                f"expose refused: rewrite header exceeds {MAX_REWRITE_LINE_LEN} chars."
            )
        # Every control character, not just CR/LF/NUL. Teleport validates the
        # value itself and rejects the whole config on a bad one (see
        # `_RESERVED_REWRITE_HEADERS`), so a stray control byte is another
        # cube-wide crashloop rather than one broken app. CR/LF remain the
        # security-relevant pair — they inject additional headers into the
        # request Teleport makes upstream — and are named first for that reason.
        if any(ord(c) < 0x20 or ord(c) == 0x7F for c in line):
            return None, (
                "expose refused: a rewrite header may not contain control "
                "characters. A carriage return or newline would inject "
                "additional headers into the request Teleport makes to your "
                "service; any control byte makes Teleport reject the whole "
                "app-service config, which takes every app on the cube down."
            )
        name, sep, value = line.partition(":")
        if not sep:
            return None, (
                f"expose refused: rewrite header '{line}' has no ':' — each entry "
                'must look like "Name: value".'
            )
        name = name.strip()
        if not _HEADER_NAME_RE.fullmatch(name):
            return None, (
                f"expose refused: '{name}' is not a valid HTTP header name."
            )
        if name.lower() in _RESERVED_REWRITE_HEADERS:
            return None, (
                f"expose refused: '{name}' is reserved by Teleport and cannot be "
                "rewritten. Teleport rejects the whole app-service config on a "
                "reserved header, which would stop EVERY app on this cube — "
                "including other companies' — a few minutes after this call."
            )
        cleaned.append(f"{name}: {value.strip()}")
    return cleaned, None


# Labels the server owns on every app it writes. `company` is the audience (a set,
# comma-separated); `cube` is the environment the app runs on, stamped so a fleet-wide
# view can say where an app lives without parsing its name.
SERVER_LABELS = ("company", "cube")


def _validate_labels(labels: dict) -> tuple[dict[str, str] | None, str | None]:
    """Validate caller-supplied EXTRA app labels -> (labels, error).

    `company` and `cube` are dropped here rather than rejected: both are set by the
    server (`company` from `_resolve_company`, which holds the tenancy check; `cube`
    from the resolved environment), and letting a caller set either through this
    argument would route straight around that. Dropping keeps a well-meaning caller
    who echoes back a label set from `list_exposed` working, while making the
    server's values authoritative either way.
    """
    if not isinstance(labels, dict):
        return None, (
            'expose refused: labels must be a JSON object, e.g. {"app-type": "console"}.'
        )
    extra = {k: v for k, v in labels.items() if k not in SERVER_LABELS}
    if len(extra) > MAX_EXTRA_LABELS:
        return None, (
            f"expose refused: at most {MAX_EXTRA_LABELS} extra labels (got {len(extra)})."
        )
    cleaned: dict[str, str] = {}
    for key, value in extra.items():
        if not isinstance(key, str) or not isinstance(value, str):
            return None, (
                f"expose refused: label {key!r} must have a string key and value."
            )
        for part, what in ((key, "key"), (value, "value")):
            if len(part) > MAX_LABEL_TOKEN_LEN:
                return None, (
                    f"expose refused: label {what} exceeds {MAX_LABEL_TOKEN_LEN} chars."
                )
            if not _LABEL_TOKEN_RE.fullmatch(part):
                return None, (
                    f"expose refused: label {what} '{part}' may contain only "
                    "letters, digits, '.', '_', '/' and '-'."
                )
        cleaned[key] = value
    return cleaned, None


def _unreadable_tokens(label: object) -> list[str]:
    """Tokens of a `company` label that are not app company names (e.g. `Groundcover`).

    `label_companies` drops them on read, so a set computed from the label and written
    back would silently take the app away from whatever role still matches that token.
    Every write here keeps them, or refuses.
    """
    if not isinstance(label, str):
        return []
    return sorted(t for t in (p.strip() for p in label.split(",")) if t and not is_valid_name(t))


def _audience_text(apps: list[dict], name: str) -> str:
    """Who the stored entry ``name`` is visible to, as written (unreadable tokens too)."""
    label = next(((a.get("labels") or {}).get("company") for a in apps if a.get("name") == name), None)
    tokens = sorted(label_companies(label)) + _unreadable_tokens(label)
    return ", ".join(tokens) or "(no company)"


def _overwrite_refusal(
    profile: str, prior: dict | None, company: str, name: str, environment: str,
) -> str | None:
    """Why a SCOPED caller may not replace the existing entry ``prior``, or None.

    Re-exposing a name replaces that entry's target and its company label in one
    upsert. A scoped caller may do that only to an app already exposed to exactly the
    company it is writing -- its own. Two refusals, split by what the caller can see:

    * An app the caller cannot see (another company's, or unlabelled): refused with
      the name only. Naming the owner, target or address would enumerate another
      tenant, and "unexpose it first" is advice they cannot act on. Before this check
      the upsert went through and REPOINTED that company's public URL. The refusal
      does confirm that SOMETHING uses the name -- the trade the console already made
      for the same reason (`writes.NAME_TAKEN_MESSAGE`); the alternative is repointing
      a live URL. It also covers the caller's own app when its label is stray or
      empty, which only an admin can relabel, so the message says whom to ask.
    * An app the caller can see under a different company (one it was granted):
      refused with the audience stated, because replacing the label takes the app
      away from that company. That is allowed, but only as an explicit unexpose, never
      as a side effect of a re-expose.

    Unscoped admins are not refused; that is unchanged. The ``expose refused:`` prefix
    marks both as pre-write for `console/writes.py::_refused_before_writing`.
    """
    if prior is None:
        return None
    companies = app_companies(profile)
    if companies is None:  # None means DENY everywhere; here too, whatever ran first
        return _companies_unreadable(profile, "expose")
    if companies.unscoped:
        return None
    label = (prior.get("labels") or {}).get("company")
    if not companies.can_see(label):
        return (
            f"expose refused: the name '{name}' is already in use on {environment}. "
            "Choose a different app_name, or if it is yours, ask an administrator to fix "
            "its company label."
        )
    current = label_companies(label)
    if current != {company}:
        return (
            f"expose refused: '{name}' is already exposed on {environment} to "
            f"{', '.join(sorted(current))}; re-exposing it under '{company}' would take it "
            "away from them. Unexpose it first if that is intended, or choose a different "
            "app_name."
        )
    return None


def _plan_labels(
    profile: str, target: str, prior: dict | None, app_uri: str, config_changing: bool,
    name: str, environment: str, *, named: bool,
) -> tuple[frozenset[str] | None, str | None]:
    """The company set the entry will carry after this expose -> (set, refusal).

    A new app gets ``{target}``. On a "map" stack an existing name is REPLACED under
    ``target`` as it always was, guarded by `_overwrite_refusal`. On a "stored" stack an
    existing app GAINS ``target``, and three rules apply to a scoped caller:

    * **Joining needs the same target and no reconfiguration.** Exposing the same
      service under an app that already exists adds the caller's company to it, even
      when the caller could not see the app before. A join now grants MANAGEMENT as well
      as visibility (the next rule lets any company on an app reconfigure it), so a
      caller that joins another company's app may then repoint its public URL. That
      stays within what cube access already grants: any profile on a cube can rewrite the
      app-service entity's config through `update_entity_config`, every company's app
      entry included (the recorded residual in AGENTS.md), and where the cube advertises
      its `cube` Teleport label (18 of 56 clusters, module >= 0.5.0) the profile is also
      cluster-admin on it and could repoint the Service directly. The same-target
      requirement is what keeps a join from being a repoint in one step; a different
      target is refused, by name only when the app was invisible to the caller.
    * **Reconfiguring needs ONE company on the app** -- any caller that can see it.
      Changing the target, rewrite headers, extra labels or public address changes the
      app for its whole audience, but whoever is on an app manages it: a customer must
      never be blocked from its own app because a partner or EdgescaleAI is on it too
      (Wyatt, 2026-09-25). The set is kept, since a reconfigure never drops a company,
      and a caller already on the app that NAMES no company adds none, changing the app
      or merely re-running: its default (the caller's home company) would otherwise land
      on an app co-owned by a company the caller does not hold -- a partner fixing its
      customer's app would open the other owner's app to the partner's users. Naming a
      company is an explicit add. An app the caller cannot see is still refused, by name
      only.
    * **Combining is gated per stack** (`can_combine`), and every stack now takes the
      `"*"` default. Dev's list of test companies protected roles that still matched
      `company` exactly; it was removed once they were migrated (2026-09-25). An empty
      value stops all combining, the brake if it is ever needed. It gates only a set that
      grows, so an app already carrying several companies can still be reconfigured.

    Unscoped admins join and reconfigure freely, still subject to the combining gate.

    The console's expose picker PREDICTS these outcomes before the click
    (`console/web/src/CubePage.tsx::existingAppHint`). A rule added or changed here needs a
    branch there too; no test spans the two languages.
    """
    if prior is None:
        return frozenset({target}), None
    if not reads_stored_sets():
        return frozenset({target}), _overwrite_refusal(profile, prior, target, name, environment)
    companies = app_companies(profile)
    if companies is None:  # `_resolve_company` refuses first; kept fail-closed anyway
        return None, "expose refused: this profile's app companies are unreadable."
    label = (prior.get("labels") or {}).get("company")
    current = label_companies(label)
    joined = frozenset(current | {target})
    visible = companies.can_see(label)
    in_use = (
        f"expose refused: the name '{name}' is already in use on {environment}. "
        "Choose a different app_name."
    )
    if _unreadable_tokens(label):
        if not visible and not companies.unscoped:
            return None, in_use
        return None, (
            f"expose refused: '{name}' on {environment} carries a company label this stack "
            "cannot read, so its audience cannot be changed safely. An admin can re-expose "
            "it without naming a company, which keeps the label as it is."
        )
    if not current and not companies.unscoped:
        # No company on it at all is UNKNOWN ownership (read as foreign, like everywhere
        # else). A join would make the caller its SOLE company, and a later unexpose would
        # then delete an app it could never see: a takeover, not a join.
        return None, in_use
    changing = config_changing or (prior.get("uri") or "") != app_uri
    if not companies.unscoped:
        if not visible and changing:
            return None, in_use
    if visible and not named and not companies.unscoped:
        # A caller already ON the app (it holds one of its companies) that names none adds
        # none, whether it changes the app or merely re-runs: its home-company default would
        # otherwise open a co-owner's app to its users. Joining an app it is NOT on still
        # adds its home company -- that is what a join is.
        joined = frozenset(current)
    # Gate only a set that GROWS. A reconfigure of an app that is already combined adds
    # nothing and changes no role's match, so the brake (an empty allowlist) must not
    # freeze it: it stops an app gaining a company, as every description of it says.
    if joined != current and not can_combine(joined):
        if not visible:
            return None, in_use
        return None, (
            f"expose refused: '{name}' is already exposed on {environment} to "
            f"{', '.join(sorted(current))}; adding '{target}' would make one app visible "
            "to several companies, which is not enabled on this stack for these companies."
        )
    return joined, None


def _app_dict(
    name: str,
    uri: str,
    public_addr: str,
    company: str,
    rewrite_headers: list[str] | None = None,
    extra_labels: dict[str, str] | None = None,
    cube: str | None = None,
) -> dict:
    """Build one apps-array entry for the multi-app module's `apps` variable.

    `rewrite` is OMITTED entirely when there is nothing to write — never
    `None` and never `{"headers": []}`. That omission is what lets
    `_merge_app`'s dict merge preserve an existing rewrite when the caller did
    not mention one (see `expose`'s `rewrite_headers` handling), and it keeps
    the rendered app config identical to what a hand-written entry looks like.
    """
    entry = {
        "name": name,
        "uri": uri,
        "public_addr": public_addr,
        "labels": {**(extra_labels or {}), "company": company},
    }
    if cube:
        entry["labels"]["cube"] = cube
    if rewrite_headers:
        entry["rewrite"] = {"headers": list(rewrite_headers)}
    return entry


def _unreadable_apps(problem: str, raw: str) -> str:
    """Error for an unreadable `apps` variable, WITHOUT quoting it.

    The raw value is the shared module's full app list — every app on the cube,
    including other companies', with URIs and public addresses. `list_exposed` and the
    console filter those out precisely so a scoped caller never learns they exist, and
    echoing the payload here handed them over on any corruption. Its length and the
    problem are enough to act on; the value itself is visible to an admin through
    `list_modules`.
    """
    return (
        f"Error: apps variable {problem} ({len(raw)} chars). It is not quoted here "
        "because it lists every app on this cube, including other tenants'. An admin "
        "can inspect it with list_modules."
    )


def _load_apps(module: dict) -> tuple[list[dict] | None, str | None]:
    """Read+validate the `apps` variable off an *existing* module installation.

    Returns (apps, None) on success or (None, error) if the variable is
    missing, unreadable as either JSON or a Python literal, not a list, or has
    an entry without a `name`. Deliberately never self-heals a malformed value
    to `[]`: Apollo's update is a full-replace, so silently treating corrupt
    `apps` data as empty and writing back just the one app from this call would
    delete every other already-running app's route — refusing is the safe
    failure mode.

    JSON is the canonical form. A Python-repr value is *also* accepted (see the
    recovery path below) because a historical `str()` coercion bug wrote them;
    that tolerance is read-side only — every write here emits real JSON.
    """
    raw = next(
        (
            v.get("variableValue", {}).get("value")
            for v in module.get("variables", [])
            if v.get("variableName") == "apps"
        ),
        None,
    )
    display = module.get("displayName") or module.get("moduleMavenCoordinate") or "?"
    if not raw:
        return None, (
            f"Error: module '{display}' is missing its 'apps' variable — manual "
            "Apollo inspection required before expose/unexpose can proceed."
        )
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Recovery path for values corrupted by the historical `str()` coercion in
        # `modules.py` (fixed there via `_variable_string`), which wrote a Python
        # **repr** — single-quoted keys — instead of JSON. Those values are
        # unparseable as JSON but are still perfectly good literal data, and
        # refusing them bricked expose/unexpose/list_exposed on any cube whose
        # `apps` variable had been written through the generic module tool
        # (observed on cube-66odzn95).
        #
        # `ast.literal_eval` evaluates literals ONLY — no names, calls, or
        # operators — so a hostile value cannot execute anything; anything it
        # can't read still falls through to the refusal below. Recovery is
        # read-only: the next expose/unexpose re-serializes with `json.dumps`,
        # so a corrupted variable self-heals on the following write.
        try:
            parsed = ast.literal_eval(raw)
        except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
            return None, _unreadable_apps("is not valid JSON", raw)
    if not isinstance(parsed, list):
        return None, _unreadable_apps("is not a JSON list", raw)
    if not all(isinstance(a, dict) and a.get("name") for a in parsed):
        return None, _unreadable_apps("has an entry missing 'name'", raw)
    return parsed, None


def _merge_app(apps: list[dict], entry: dict, clear_rewrite: bool = False) -> list[dict]:
    """Idempotent upsert of `entry` into `apps`, matched by exact `name`.

    Replaces an existing entry with the same name in place (at the same list
    index, preserving any extra label beyond `company`); appends if no entry
    matches. A `public_addr` override that changes the effective name is, by
    design, treated as a *different* app — this never tries to guess "same app,
    new address," since guessing wrong (silently replacing) is worse than an
    extra harmless route the caller can clean up once noticed.

    The `{**existing, **entry}` merge also preserves any key this tool does not
    write, which is how a hand-injected `rewrite` block survived on
    `cube-66odzn95` through many exposes. That is now DELIBERATE and tested
    (`test_expose_rewrite.py`) rather than incidental: `_app_dict` omits
    `rewrite` when the caller passed nothing, precisely so this merge leaves an
    existing one alone.

    `clear_rewrite` is the one thing a dict merge cannot express. A caller
    passing `rewrite_headers=[]` is asking for REMOVAL, and removal has to be
    explicit — which matters more than it sounds: the first production use of
    this argument is deleting a rewrite that makes MinIO unreachable through the
    browser proxy.
    """
    for i, existing in enumerate(apps):
        if existing.get("name") == entry["name"]:
            merged_labels = {**(existing.get("labels") or {}), **entry["labels"]}
            merged = {**existing, **entry, "labels": merged_labels}
            if clear_rewrite:
                merged.pop("rewrite", None)
            apps[i] = merged
            return apps
    apps.append(entry)
    return apps


def _remove_app(apps: list[dict], name: str) -> tuple[list[dict] | None, dict | None]:
    """Remove the app matched by `name`.

    Returns (remaining_apps, removed_entry) if found (remaining_apps may be
    []), or (None, None) if `name` isn't present — the None sentinel
    distinguishes "not found" from "found and removed, zero left."
    """
    removed = next((a for a in apps if a.get("name") == name), None)
    if removed is None:
        return None, None
    return [a for a in apps if a.get("name") != name], removed


def _without_company(
    apps: list[dict], names: set[str], company: str | None,
) -> tuple[list[dict], list[str], list[str]]:
    """Take ``company`` off the named apps -> (remaining, deleted, narrowed).

    An app left with no company is DELETED; one that keeps another company stays,
    relabeled (``narrowed``). ``company=None`` deletes the named apps outright -- the
    admin path, and what every removal did before apps could carry several companies.
    """
    remaining, deleted, narrowed = [], [], []
    for a in apps:
        if a.get("name") not in names:
            remaining.append(a)
            continue
        label = (a.get("labels") or {}).get("company")
        left = label_companies(label) - ({company} if company else set())
        kept = _unreadable_tokens(label)  # never ours to drop: see `_unreadable_tokens`
        if company is None or not (left or kept):
            deleted.append(a["name"])
        else:
            narrowed.append(a["name"])
            value = ",".join(([format_label(left)] if left else []) + kept)
            remaining.append({**a, "labels": {**(a.get("labels") or {}), "company": value}})
    return remaining, deleted, narrowed


@_serialized_per_cube
async def expose(
    client: ApolloClient,
    environment: str,
    app_name: str,
    app_uri: str,
    public_addr: str | None = None,
    company: str | None = None,
    profile: str = "admin",
    rewrite_headers: list | str | None = None,
    labels: dict | str | None = None,
) -> str:
    """Expose a running in-cluster service as a Teleport app.

    Idempotent: re-running expose for the same effective app name updates that
    app's entry in place on the environment's shared Teleport multi-app-service
    module — it never installs a duplicate module or duplicates the app.

    Args:
        environment: Apollo environment / cube whose shared app-service module
            this app is added to (installed on first use).
        app_name: Base Teleport app name. Auto-qualified to ``<app_name>-<env>``
            (using the resolved environment name) so it stays unique across cubes
            in the shared Teleport tenant — that qualified name is what you pass
            to ``app_proxy`` (and to ``unexpose`` to remove it later).
        app_uri: Internal service URI, e.g.
            ``http://svc.namespace.svc.cluster.local:8080``. Point at the REAL
            service + targetPort — a wrong port surfaces as Teleport
            "context deadline exceeded".
        public_addr: Optional override for the app's **Teleport** public address —
            a Teleport-registration detail, NOT the URL this tool publishes (that
            is always the browser app proxy's ``https://<name>.<apex>``). When set
            it is used verbatim AND ``app_name`` is taken verbatim (no
            qualification), so the name must be a valid DNS label on its own; keep
            it consistent with ``<app_name>.<TELEPORT_APP_DOMAIN>`` or Teleport may
            not route. Rarely needed.
        company: The app company to expose this app TO -- who can see it. Must be
            one the caller's profile holds; defaults to its HOME company. On a
            "stored" stack, exposing an app that already exists under the same name
            and target ADDS a company to its audience (see `_plan_labels`): the named
            one, or the home one for a caller not yet on the app -- a caller already on
            it adds nothing unless it names the company. On a "map" stack it replaces
            the label, as before. Unscoped admins may name
            any company (default DEFAULT_COMPANY for a NEW app); on a "stored" stack
            an admin naming none on an existing app keeps its label verbatim.
        profile: Caller's Teleport profile — recorded for audit; the token is
            minted with the dedicated minter identity, not this profile.
        rewrite_headers: Headers the app service rewrites on requests it forwards
            upstream, as ``["Host: x", "Origin: https://x"]``. Two distinct uses:
            selecting an ingress vhost (the value must match the in-cluster
            ingress rule, and is NOT derivable from this app's own address), and
            satisfying an app that checks Origin against Host. Omit to leave any
            existing rewrite untouched; pass ``[]`` to REMOVE it. Removal is not
            hypothetical — a rewrite pinning Host/Origin to the Teleport address
            makes an app unreachable through the browser proxy.
        labels: Extra Teleport labels for this app, merged under the resolved
            ``company`` (which this cannot set — see ``_validate_labels``).
            Needed so a migrated app does not silently lose an operator-set
            label. Omit to leave existing extra labels untouched.
    """
    # Local import avoids a tools.modules <-> tools.expose import cycle.
    from cube_cloud.tools import modules

    if not tbot.is_ready:
        return "tbot credentials not ready. expose is not available yet."

    # Company first — pure in-memory, fail-closed, no network.
    # "" names no company, exactly as `_resolve_company` reads it (`requested or home`); an
    # MCP client sends "" for an omitted optional string, and treating it as named made a
    # reconfigure ADD the home company and an admin re-expose stamp DEFAULT_COMPANY.
    named_company = company or None
    # The same for the two JSON-string arguments: "" is omitted, not malformed JSON (clearing
    # a rewrite is the explicit "[]").
    rewrite_headers = None if rewrite_headers == "" else rewrite_headers
    labels = None if labels == "" else labels
    company, company_err = _resolve_company(profile, company)
    if company_err:
        return company_err

    # Then the rest of the pure, in-memory validation, all of it BEFORE any
    # Apollo/Teleport call: a malformed argument should cost nothing and must
    # never leave a half-applied write. The `expose refused:` prefix keeps
    # `console/writes._refused_before_writing` classifying these as pre-write.
    if (scheme_err := _validate_scheme(app_uri)) is not None:
        return scheme_err

    clean_headers: list[str] | None = None
    if rewrite_headers is not None:
        decoded, decode_err = _decode_json_arg(rewrite_headers, "rewrite_headers", list)
        if decode_err:
            return decode_err
        clean_headers, headers_err = _validate_rewrite_headers(decoded)
        if headers_err:
            return headers_err
        # A rewrite is an HTTP concept. Storing one on a tcp:// app would write
        # config Teleport ignores while reporting success.
        if clean_headers and not is_http_app(app_uri):
            return (
                "expose refused: rewrite_headers cannot be used with a tcp:// "
                "app — the app service rewrites HTTP headers, and a TCP app "
                "carries none."
            )

    clean_labels: dict[str, str] | None = None
    if labels is not None:
        decoded_labels, decode_err = _decode_json_arg(labels, "labels", dict)
        if decode_err:
            return decode_err
        clean_labels, labels_err = _validate_labels(decoded_labels)
        if labels_err:
            return labels_err

    # Env resolution is unconditional now (even on the public_addr-override
    # path): finding the environment's existing module installation needs
    # env_info["id"] regardless of which naming path is taken below.
    try:
        env_info = await _resolve_environment(client, environment)
    except ApolloError as e:
        return f"expose failed: {e}"
    env_name = env_info.get("name", environment)

    if public_addr:
        # Explicit override: caller owns the name<->addr coupling; no qualification.
        # The NAME is still checked as a DNS label, because it becomes the leftmost
        # label of the published browser URL and the label
        # `browser_proxy/resolver.py` resolves back to a Teleport app. Unvalidated,
        # this path stored apps that no published URL could ever reach (it also
        # skipped the 63-char limit `_qualified_app_name` enforces). The
        # "expose refused:" prefix keeps `console/writes.py::_refused_before_writing`
        # classifying this as a pre-write bail-out.
        if not is_app_label(app_name):
            return (
                f"expose refused: app_name '{app_name}' is not a valid DNS label "
                f"(lower-case a-z0-9 and '-', no leading/trailing '-', "
                f"{MAX_LABEL_LEN} chars max). With public_addr set the name is taken "
                "verbatim, so it has to be routable on its own."
            )
        effective_name = app_name
        effective_addr = public_addr
    else:
        effective_name, qual_err = _qualified_app_name(app_name, env_name)
        if qual_err:
            return qual_err
        effective_addr = f"{effective_name}.{TELEPORT_APP_DOMAIN}"

    logger.info(
        "expose: profile=%s env=%s app=%s name=%s uri=%s addr=%s named_company=%s",
        profile, environment, app_name, effective_name, app_uri, effective_addr,
        named_company or "-",
    )

    # Serialize on the RESOLVED cube, now that the caller is authorized for it: the read
    # below through the write and its wait is the section two calls must not share.
    if not await _lock_cube(env_info["id"]):
        return f"expose refused: {CUBE_BUSY}"
    installations = await modules._fetch_module_installations(client, env_info["id"])
    module = modules._find_module_by_coordinate(installations, TELEPORT_MULTI_APP_SERVICE_MODULE)

    entry = _app_dict(
        effective_name, app_uri, effective_addr, company,
        rewrite_headers=clean_headers, extra_labels=clean_labels, cube=env_name,
    )
    # Anything that changes the app itself rather than who can see it. Joining an
    # existing app needs none of these (see `_plan_labels`).
    config_changing = rewrite_headers is not None or labels is not None or bool(public_addr)
    prior: dict | None = None
    prior_company: str | None = None
    new_set: frozenset[str] = frozenset({company})
    joined = False
    if module is None:
        apps = [entry]
    else:
        apps, load_err = _load_apps(module)
        if load_err:
            return load_err
        # Whose entry is about to be overwritten, read BEFORE the merge.
        # `_merge_app` upserts by `name` alone, so re-exposing an existing name
        # replaces that entry's target AND its company label. `_overwrite_refusal`
        # stops a scoped caller from doing that to an app that is not exactly its
        # own; an unscoped admin still may, and for that case a collision preserves
        # the other company's `rewrite` and extra labels into the merged entry, which
        # the echo below must not read back -- see the `foreign_entry` use.
        prior = next(
            (a for a in apps if a.get("name") == effective_name), None
        )
        prior_company = (prior.get("labels") or {}).get("company") if prior else None
        if (prior is not None and reads_stored_sets() and named_company is None
                and app_companies(profile).unscoped):
            # An admin naming no company is RECONFIGURING (a port, a rewrite), not choosing
            # an audience: the label is kept verbatim. Planning it as a join added
            # DEFAULT_COMPANY to every app it touched. Dev's combining gate caught that
            # once; with every stack on "*" a regression is a SILENT grant to every
            # edgescaleai profile, on dev as on prod after the flip, and
            # test_an_ADMIN_reconfiguring_an_app_keeps_its_audience is what catches it.
            # ...including NO label: an unlabelled app stays admin-only rather than being
            # stamped DEFAULT_COMPANY (a silent grant to every edgescaleai profile).
            label_value = prior_company or ""
            new_set = label_companies(label_value)
        else:
            planned, refusal = _plan_labels(
                profile, company, prior, app_uri, config_changing, effective_name, environment,
                named=named_company is not None,
            )
            if refusal:
                return refusal
            new_set = planned
            # A "map" stack writes the one company verbatim, as it always has (it may not be
            # a name the stored model reads, and `format_label` would refuse it).
            label_value = format_label(new_set) if reads_stored_sets() else company
        # Sets, not strings: an unsorted stored label ("lear,conagra") differs from the
        # canonical one we write while holding the same companies, and a reconfigure that
        # added none must not headline "Added '<home>'".
        joined = (prior is not None and company not in label_companies(prior_company)
                  and label_companies(label_value) != label_companies(prior_company or ""))
        if (prior is not None and reads_stored_sets() and not config_changing
                and (prior.get("uri") or "") == app_uri):
            # Only the AUDIENCE changes: keep the stored entry exactly (its address,
            # rewrite and labels belong to everyone on it), relabel, stamp the cube.
            relabeled = {**prior, "labels": {**(prior.get("labels") or {}),
                                              "company": label_value, "cube": env_name}}
            apps = [relabeled if a.get("name") == effective_name else a for a in apps]
        else:
            entry["labels"]["company"] = label_value
            apps = _merge_app(apps, entry, clear_rewrite=clean_headers == [])

    # Mint a fresh App Service join token — every apps-list change triggers a
    # pod rollout/rejoin, so an old/already-consumed token would break it.
    try:
        auth_token = await tbot.mint_app_token(timeout=_mint_timeout())
    except RuntimeError as e:
        return f"expose failed: could not mint app token: {e}"

    # The module's `apps` variable is itself a JSON string (the module template
    # renders `{{ moduleVariable.apps }}` unquoted into YAML), so json.dumps(apps)
    # — already-JSON text — must go under the "apps" key, not the raw list.
    variables = json.dumps({
        "authToken": auth_token,
        "company": company,
        "apps": json.dumps(apps),
    })

    if module is None:
        result = await modules.install_module(
            client,
            environment,
            TELEPORT_MULTI_APP_SERVICE_MODULE,
            variables=variables,
            display_name="Teleport Multi-App Service",
        )
    else:
        # Pass the module's own already-installed coordinate, not the
        # (possibly newer) constant — version-safe and always an exact match.
        result = await modules.update_module_variables(
            client, environment, module["moduleMavenCoordinate"], variables=variables,
        )
    landed = _write_failed(result) or await _await_own_write(client, env_info["id"], apps)

    # The apps visible to the company this app was exposed under, and nothing else.
    # This once listed every tenant's app names on a scoped caller's successful expose
    # -- the disclosure `list_exposed`, `unexpose` and `_unreadable_apps` each prevent.
    # An unscoped admin sees just that company's here; `list_exposed` is the full view.
    tbot.forget_app(effective_name)
    app_names = ", ".join(
        a["name"] for a in apps
        if company in label_companies((a.get("labels") or {}).get("company"))
    )
    # The PUBLISHED address is the browser app proxy's, never `effective_addr` (the
    # Teleport host, which 302s to Teleport SSO). The line is always present, with a
    # stated reason when there is no URL: an omitted one is what leads a caller to
    # invent an address or reach for the Teleport one.
    url, no_url_reason = browser_app_url_or_reason(effective_name, app_uri)
    # "Visible to" LEADS: it is the answer to "did I expose this to the right
    # company?", and the one line a caller holding several companies must check.
    headline = (
        f"Added '{company}' to '{effective_name}' on {environment}"
        if joined and reads_stored_sets() and prior is not None
        else f"Exposed '{effective_name}' as a Teleport app on {environment}"
    )
    lines = [
        headline,
        f"  Visible to: {', '.join(sorted(new_set)) if module is None else _audience_text(apps, effective_name)}",
        f"  URI:     {app_uri}",
        f"  URL:     {url or f'none -- {no_url_reason}'}",
    ]
    # Echo what was WRITTEN, not what was passed, so an existing rewrite the
    # caller preserved by omission is reported just as one they set is. Silence
    # here is what let the MinIO rewrite on cube-66odzn95 stay invisible through
    # repeated exposes.
    #
    # UNLESS the entry being overwritten belonged to another company. A scoped
    # caller is refused that overwrite (`_overwrite_refusal`), but an unscoped admin
    # is not, and then a name collision merges over a stranger's app and preserves
    # their `rewrite` + extra labels — reading those back would
    # hand the caller another tenant's ingress hostnames and operator labels,
    # and archive them in the S3 telemetry sink (`expose` is not in
    # `telemetry_drop_response_tools`). That is the same disclosure class as the
    # `Apps on this module:` leak this file already filters. In that case echo
    # only what the caller themselves passed, which is never someone else's.
    #
    # The repointing itself is pre-existing and documented; only the disclosure
    # is new, so this contains the disclosure rather than changing the write.
    # `prior is not None`, NOT `prior_company is not None`: an entry with no
    # `company` label has UNKNOWN ownership, and unknown must read as foreign.
    # Those are exactly the entries a scoped caller cannot otherwise see —
    # `list_exposed` filters on `labels.company == company`, so an unlabelled
    # entry is invisible to every scoped profile — and they are the common shape
    # of the hand-written legacy entries this feature exists to migrate.
    # Foreign = the caller could not read this entry before the write. A scoped caller that
    # can SEE the app reads its rewrite and labels through `list_exposed` anyway, and any
    # company on an app may reconfigure it, so a co-tenant's reconfigure is not foreign even
    # when its home company is not on the app. The home-company test stays for an unscoped
    # admin, which is what it was written for.
    held_now = app_companies(profile)
    if prior is None:
        foreign_entry = False
    elif held_now is not None and not held_now.unscoped:
        foreign_entry = not held_now.can_see(prior_company)
    else:
        foreign_entry = company not in label_companies(prior_company)
    stored_label = next(((a.get("labels") or {}).get("company") for a in apps
                         if a.get("name") == effective_name), None)
    # A change to an app carrying a company the caller does not hold -- its target, or its
    # rewrite/labels -- is a cross-company write whether or not the caller could see it
    # (any company on an app may reconfigure it), so it gets its own WARNING: `foreign_entry`
    # governs the ECHO, and the info line above carries neither the prior target nor its
    # owners, nor the label actually written.
    if prior is not None and ((prior.get("uri") or "") != app_uri or config_changing):
        others = (label_companies(prior_company or "") if held_now is None or held_now.unscoped
                  else label_companies(prior_company or "") - held_now.held)
        if others:
            logger.warning(
                "expose: profile=%s changed an app carrying company=%s on env=%s name=%s "
                "(uri %s -> %s, config changed=%s, label written=%s)", profile,
                ",".join(sorted(others)), environment, effective_name, prior.get("uri"),
                app_uri, config_changing, label_value,
            )
    # Sets, not strings, as for `joined`: an unsorted stored label is not a change.
    if foreign_entry and label_companies(stored_label or "") != label_companies(prior_company or ""):
        logger.warning(
            "expose: profile=%s overwrote an entry owned by company=%s with "
            "company=%s on env=%s name=%s — preserved values withheld from the "
            "response", profile, prior_company, company, environment, effective_name,
        )
    stored = next((a for a in apps if a.get("name") == effective_name), {})
    if foreign_entry:
        echo_headers = list(clean_headers or [])
        echo_extra = dict(clean_labels or {})
    else:
        echo_headers = ((stored.get("rewrite") or {}).get("headers")) or []
        echo_extra = {
            k: v for k, v in (stored.get("labels") or {}).items() if k not in SERVER_LABELS
        }
    if echo_headers:
        lines.append(f"  Rewrite: {'; '.join(echo_headers)}")
    if echo_extra:
        lines.append(
            "  Labels:  "
            + ", ".join(f"{k}={v}" for k, v in sorted(echo_extra.items()))
        )
    if url:
        # Deliberately does NOT name app_proxy here — a PRESENTATION choice, not a
        # restriction. `app_proxy` remains available for any exposed app and is the
        # right tool whenever someone wants a local port; it is simply not the
        # follow-up step to publishing, and advertising it here taught "route around
        # the link". It is named only where it is the sole way in (tcp://, no apex).
        #
        # The rollout note is not optional politeness: this write is a declared-state
        # change, and the cube's Teleport app-service release takes minutes to roll
        # out (2-3 min measured, console/web/src/CubePage.tsx). Without it a caller
        # curls immediately and reports a false failure.
        lines.append("  Access:  open the URL and sign in with the same login as "
                     "cube-mcp (no Teleport account)")
        lines.append("  Note:    the URL starts answering once the cube's app-service "
                     "rolls out (usually a few minutes)")
    if public_addr and public_addr != f"{effective_name}.{TELEPORT_APP_DOMAIN}":
        # Flag the mismatch WITHOUT printing the address. Both access paths dial this
        # app by NAME (`tunnel/relay.py` SNI, `browser_proxy/resolver.py` host label),
        # so a hand-picked address that disagrees with the name may not route at all —
        # the one real diagnostic the old Address: line carried.
        lines.append("  Routing: custom public address -- both access paths dial this "
                     "app by NAME, so a mismatched address may not route. If it does not "
                     "answer, unexpose it (passing this same public_addr, which is how "
                     "unexpose finds a name taken verbatim) and expose it again without "
                     "public_addr; its name is then qualified as <app>-<cube>.")
    # Label kept verbatim: `console/writes._CROSS_TENANT_LINE_PREFIXES` matches
    # "apps on this module:" to redact this line from console logs. Rewording it
    # (e.g. "Your apps on this module") silently walks out from under that rule.
    lines.append(f"  Apps on this module: {app_names}")
    if not landed:
        lines.append(NOT_YET_VISIBLE_NOTE)
    return "\n".join(lines) + f"\n\n{_publishable_result(result)}"


async def _apply_removal(
    client: ApolloClient,
    environment: str,
    env_info: dict,
    module: dict,
    remaining: list[dict],
    removed_names: list[str],
    other_tenant_note: bool = False,
    headline: str | None = None,
) -> str:
    """Shared finish step for unexpose: write back `remaining` apps (minting a
    fresh token) if any remain, or fully tear the module down if not.

    `other_tenant_note` is set for an ``all=True`` scoped removal that leaves
    another company's apps on the shared module — the note says the module
    stays installed without naming or counting those apps: never confirm
    anything about another tenant's apps beyond the bare fact (already
    visible from the module remaining installed) that they exist.
    """
    from cube_cloud.tools import modules
    from cube_cloud.tools.environments import uninstall_entity

    removed_label = ", ".join(removed_names)

    if remaining:
        try:
            auth_token = await tbot.mint_app_token(timeout=_mint_timeout())
        except RuntimeError as e:
            return f"unexpose failed: could not mint app token: {e}"

        variables = json.dumps({"authToken": auth_token, "apps": json.dumps(remaining)})
        result = await modules.update_module_variables(
            client, environment, module["moduleMavenCoordinate"], variables=variables,
        )
        landed = _write_failed(result) or await _await_own_write(client, env_info["id"], remaining)
        note = (
            "\n  Note: the module remains installed on this environment — it "
            "still serves apps outside your company."
            if other_tenant_note else ""
        )
        if not landed:
            note += "\n" + NOT_YET_VISIBLE_NOTE
        # Said in the user's terms: what stopped is the EXPOSURE, never the app. The
        # module and the Teleport app service are how, and a reader who has not seen
        # them hears "the app was deleted".
        first = headline or (f"Removed '{removed_label}' on {environment}: it is no longer "
                             f"exposed. The app itself keeps running.")
        return f"{first}{note}\n\n{_publishable_result(result)}"

    # Nothing remains: tear the module fully down. No token mint needed —
    # nothing is left to roll out.
    module_rid = module["rid"]
    entity_names = await modules._module_installed_app_names(client, env_info["id"], module_rid)

    try:
        unlinked = await client.graphql(Q.UNINSTALL_MODULE, {"installationRid": module_rid})
    except ApolloError as e:
        return f"unexpose failed: could not unlink module: {e}"
    logger.info("unexpose: unlinkModule answered state %s on env %s",
                _module_state(((unlinked or {}).get("apollo") or {}).get("unlinkModule") or {}),
                env_info.get("id"))
    # A teardown is a write like any other: the next call must not read the module as
    # still installed with the pre-removal list, or it writes the removed app back.
    note = "" if await _await_own_write(client, env_info["id"], None) else "\n" + NOT_YET_VISIBLE_NOTE

    if not entity_names:
        return (
            f"Removed '{removed_label}' on {environment}: it is no longer exposed, and the "
            "app itself keeps running. Nothing else on this cube is exposed now, so the "
            "cube's app-exposure service (Teleport Multi-App Service) was unlinked too. No "
            "entity could be attributed to that service, so check with entity_health "
            "whether its pod is still running."
        ) + note

    entity_results = []
    failures = []
    for name in entity_names:
        try:
            res = await uninstall_entity(client, environment, name)
        except ApolloError as e:
            res = f"Error: {e}"
            failures.append(name)
        else:
            if "not found" in res.lower() or "multiple entities match" in res.lower():
                failures.append(name)
        entity_results.append(res)

    if failures:
        return (
            f"Removed '{removed_label}' on {environment}: it is no longer exposed, and the "
            "app itself keeps running. Nothing else on this cube is exposed now, so the "
            "cube's app-exposure service (Teleport Multi-App Service) was unlinked too, "
            f"but its entity could NOT be removed automatically: {', '.join(failures)}. "
            "That service's pod may still be running — re-run unexpose for the same app "
            "to retry, or remove it with uninstall_entity.\n\n"
            + "\n".join(entity_results)
        ) + note

    return (
        f"Removed '{removed_label}' on {environment}: it is no longer exposed, and the app "
        "itself keeps running. Nothing else on this cube is exposed now, so the cube's "
        "app-exposure service was removed as well.\n\n"
        + "\n".join(entity_results)
    ) + note


@_serialized_per_cube
async def unexpose(
    client: ApolloClient,
    environment: str,
    app_name: str | None = None,
    public_addr: str | None = None,
    all: bool = False,
    profile: str = "admin",
    company: str | None = None,
) -> str:
    """Remove a company from app(s) on the environment's shared Teleport
    multi-app-service module, deleting an app once no company is left on it.

    Mints a fresh join token and updates the module's `apps` list in place
    (same "any change triggers a rollout" reasoning as ``expose``). Tears the
    module fully down (unlink + uninstall its entity) once no apps remain —
    no separate confirmation step, since calling this tool already is the
    confirmation.

    A scoped caller can never learn that an app outside their own company
    exists: an unrecognized name and a real name belonging to another company
    return the identical "does not exist or you do not have permission"
    message (see the visibility check below), and ``all=True`` never names or
    counts apps it didn't touch.

    Args:
        environment: Apollo environment the app was exposed on.
        app_name: Base Teleport app name as originally passed to ``expose``
            (auto-qualified the same way — pass the same value). Mutually
            exclusive with ``all``.
        public_addr: Must match the ``public_addr`` originally passed to
            ``expose``, if any (disables auto-qualification the same way) —
            needed to compute the same effective name used as the removal key.
        all: Change several apps in one call instead of one at a time. For an
            unscoped admin naming no company that's every app on the module (full
            teardown once it's empty). Otherwise it takes ``company`` (default: the
            HOME company) off every app that carries it: an app that still has
            another company afterwards stays exposed to it, and an app without that
            company is untouched, so nothing is taken from a company not named. If
            other apps remain afterward, the module stays installed. Mutually
            exclusive with ``app_name``/``public_addr``.
        profile: Caller's Teleport profile. Used to resolve the caller's own
            companies for the visibility checks below.
        company: The app company to REMOVE. Defaults to the caller's HOME company;
            must be one it holds. Naming another one (a granted company) is how a
            partner deliberately takes an app away from that company, which is why
            it is never the default. An app that still has another company after
            the removal stays exposed to it. An unscoped admin who names no company
            removes the app outright, as before.
    """
    from cube_cloud.tools import modules

    if not tbot.is_ready:
        return "tbot credentials not ready. unexpose is not available yet."

    if all and (app_name or public_addr):
        return "unexpose refused: pass either app_name (optionally with public_addr) or all=true, not both."
    if not all and not app_name:
        return "unexpose requires either app_name or all=true."

    companies = app_companies(profile)
    if companies is None:
        return _companies_unreadable(profile, "unexpose")
    # Which company comes off. None only for an admin naming none: the whole app goes. ""
    # names none, as it does in `expose` (an MCP client sends "" for an omitted string).
    target: str | None = company or None
    if not companies.unscoped:
        target, target_err = _resolve_company(profile, company)
        if target_err:
            return target_err.replace("expose refused", "unexpose refused").replace(
                "cannot expose under", "cannot unexpose")

    try:
        env_info = await _resolve_environment(client, environment)
    except ApolloError as e:
        return f"unexpose failed: {e}"
    env_name = env_info.get("name", environment)

    if not all:
        if public_addr:
            effective_name = app_name
        else:
            effective_name, qual_err = _qualified_app_name(app_name, env_name)
            if qual_err:
                return qual_err

    # Serialize on the RESOLVED cube, now that the caller is authorized for it: the read
    # below through the write and its wait is the section two calls must not share.
    if not await _lock_cube(env_info["id"]):
        return f"unexpose refused: {CUBE_BUSY}"
    installations = await modules._fetch_module_installations(client, env_info["id"])
    module = modules._find_module_by_coordinate(installations, TELEPORT_MULTI_APP_SERVICE_MODULE)
    if module is None:
        return f"Nothing is exposed on {environment} (no Teleport multi-app module installed)."

    apps, load_err = _load_apps(module)
    if load_err:
        return load_err

    is_scoped = not companies.unscoped

    def label_of(a: dict) -> frozenset[str]:
        return label_companies((a.get("labels") or {}).get("company"))

    if all:
        if target is None:  # admin, no company named: every app, as before
            mine = [a for a in apps if companies.can_see((a.get("labels") or {}).get("company"))]
        else:
            mine = [a for a in apps if target in label_of(a)]
        if not mine:
            what = f" to {target}" if target else ""
            return f"No apps exposed on {environment}{what} that you have permission to manage."
        remaining, deleted, narrowed = _without_company(apps, {a["name"] for a in mine}, target)
        for name in [a["name"] for a in mine]:
            tbot.forget_app(name)
        headline = None
        if narrowed:
            headline = (
                f"No longer visible to {target} on {environment}: {', '.join(narrowed)}"
                + (f"\n  No longer exposed to anyone (the apps keep running): {', '.join(deleted)}"
                   if deleted else "")
            )
        return await _apply_removal(
            client, environment, env_info, module, remaining, deleted or narrowed,
            other_tenant_note=is_scoped and bool(remaining), headline=headline,
        )

    # Single-app path: an app outside the caller's company must be
    # indistinguishable from one that doesn't exist at all.
    visible_names = {
        a["name"] for a in apps if companies.can_see((a.get("labels") or {}).get("company"))
    }
    if effective_name not in visible_names:
        current = ", ".join(sorted(visible_names)) or "(none)"
        return (
            f"'{effective_name}' does not exist or you do not have permission "
            f"to manage it. Apps you can manage on {environment}: {current}."
        )

    entry = next(a for a in apps if a["name"] == effective_name)
    current = label_of(entry)
    if target is not None and target not in current:
        return (
            f"unexpose refused: '{effective_name}' is not exposed to {target} on "
            f"{environment}; it is visible to: {', '.join(sorted(current)) or '(no company)'}."
        )
    tbot.forget_app(effective_name)
    remaining, deleted, narrowed = _without_company(apps, {effective_name}, target)
    headline = None
    if narrowed:
        headline = (
            f"'{effective_name}' is no longer visible to {target} on {environment}\n"
            f"  Still visible to: {', '.join(sorted(current - {target}))}"
        )
    return await _apply_removal(
        client, environment, env_info, module, remaining, [effective_name], headline=headline,
    )


async def list_exposed(client: ApolloClient, environment: str, profile: str = "admin") -> str:
    """List apps currently exposed on an environment's shared Teleport
    multi-app-service module — the same state ``expose``/``unexpose`` manage.

    On a "map" stack a scoped caller sees only apps it can reach: anything else is
    filtered out entirely (name, uri and address never appear). On a "stored" stack
    every app on the cube is LISTED with its audience ("Visible to"), because anyone
    who can see a cube should see what is exposed on it and to whom -- but only an app
    the caller can reach shows its target, URL, rewrite and labels; the rest show name
    and audience alone. Reaching the environment at all already required Apollo
    visibility of the cube (`_resolve_environment` runs as the caller).
    """
    from cube_cloud.tools import modules

    try:
        env_info = await _resolve_environment(client, environment)
    except ApolloError as e:
        return f"list_exposed failed: {e}"
    env_name = env_info.get("name", environment)

    installations = await modules._fetch_module_installations(client, env_info["id"])
    module = modules._find_module_by_coordinate(installations, TELEPORT_MULTI_APP_SERVICE_MODULE)
    if module is None:
        return f"No apps exposed on {env_name} (no Teleport multi-app module installed)."

    apps, load_err = _load_apps(module)
    if load_err:
        return load_err

    companies = app_companies(profile)
    if companies is None:
        return _companies_unreadable(profile, "list_exposed")
    list_all = reads_stored_sets()
    if not list_all:
        apps = [a for a in apps if companies.can_see((a.get("labels") or {}).get("company"))]

    if not apps:
        return f"No apps exposed on {env_name} that you have permission to manage."

    lines = [f"Exposed apps on {env_name} ({len(apps)})", "=" * 60]
    for a in apps:
        name = a.get("name") or "?"
        label = (a.get("labels") or {}).get("company")
        # As written, unreadable tokens included: `Groundcover` IS reachable by the role that
        # matches it, and "(no company)" would be a false answer to "who can see this?".
        audience = sorted(label_companies(label)) + _unreadable_tokens(label)
        if not companies.can_see((a.get("labels") or {}).get("company")):
            # Listed so the cube's users know it exists and for whom; nothing that
            # would let them reach it or learn its internals.
            lines.append(f"  {name}")
            lines.append(f"    Visible to: {', '.join(audience) or '(no company)'}  (not you)")
            continue
        uri = a.get("uri") or ""
        # Built from the stored NAME, not the stored `public_addr`: the name is what
        # both access paths dial, and `public_addr` is Teleport's own host (see the
        # module docstring). Every app keeps an address line — it is now the browser
        # app proxy's.
        url, no_url_reason = browser_app_url_or_reason(name, uri)
        lines.append(f"  {name}")
        lines.append(f"    Visible to: {', '.join(audience) or '(no company)'}")
        lines.append(f"    URI:     {uri or '?'}")
        lines.append(f"    URL:     {url or f'none -- {no_url_reason}'}")
        # Rendering these is a PREREQUISITE for `expose`'s whole-list-replace
        # semantics, not a nicety: a caller who cannot read the current rewrite
        # headers cannot resend them, and would silently drop them on the next
        # write. Same for an operator-set label.
        headers = ((a.get("rewrite") or {}).get("headers")) or []
        if headers:
            lines.append(f"    Rewrite: {'; '.join(str(h) for h in headers)}")
        extra = {
            k: v for k, v in sorted((a.get("labels") or {}).items()) if k not in SERVER_LABELS
        }
        if extra:
            lines.append(
                "    Labels:  " + ", ".join(f"{k}={v}" for k, v in extra.items())
            )
        stored_addr = a.get("public_addr") or ""
        if stored_addr and stored_addr != f"{name}.{TELEPORT_APP_DOMAIN}":
            # Read, never printed — same reasoning as `expose`'s Routing line.
            lines.append("    Routing: custom public address -- access dials this app "
                         "by NAME, so a mismatched address may not route.")
    lines.append("")
    lines.append("Access: open an app's URL in a browser and sign in with the same "
                 "login as cube-mcp (no Teleport account).")
    return "\n".join(lines)
