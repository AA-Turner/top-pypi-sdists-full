"""Why an app is unhealthy — the health checks behind Apollo's `healthStatus`.

The app list can only NAME an entity's health (`reportedStatus.healthStatus` is a
bare enum); this module reads the checks that produced it (`docs/console-spec.md`
§4.21). **It is shared by both surfaces**: the console's per-app drill-down
(`console/reads.py::app_health`) and the MCP `entity_health` tool
(`tools/entities.py`). It lives under `tools/` for the reason `teleport_status.py`
does — the dependency runs `console/ -> tools/` and never back.

**What Apollo gives, measured across every ERROR entity in prod (101, 2026-09-30):**
65 had a failing check with a readable message (`password authentication failed
for user "postgres"`, `ACCESS_REFUSED`, `no schema returned for catalog postgres`);
33 had no checks but a container reporting not live or not ready; 3 had nothing
that explains the roll-up. So the result carries both kinds of evidence, and a
fourth state for "Apollo says unhealthy and shows nothing" — which must be said
rather than rendered as an empty panel that reads as healthy. Those counts are a
dated snapshot; the sources for every fact here, and what is still unverified, are in
§4.21's "Evidence" subsection, and `scripts/survey-entity-health.py` re-measures them.

**Authorization is the CALLER's, as in `teleport_status`.** The console resolves
the cube out of `_visible_environments` and the entity out of that cube's entity
list; the MCP tool uses `_resolve_environment`. Neither can be shared. What this
module adds is the one check both need and neither could do alone:
`entityById` takes a FLEET-WIDE id, so the fetched entity's `environment.id` is
compared to the environment the caller authorized, and a mismatch is refused.
Callers must still only pass ids read from the authorized environment's own entity
list — the comparison is the second barrier, not the first.

**The text in a check is written by the app, not by us.** `message` and
`params.errorMessage` are free text from in-cube code, so they are treated as
untrusted at this boundary: whitespace (newlines included) is collapsed so a
message cannot forge extra lines in tool output, control characters are dropped,
`scheme://user:pass@` userinfo is replaced, and length is capped. The rest of
`params` — internal hosts, ports, database names, Peplink serials, verified live —
is discarded here and never reaches either surface.

Presentation stays with each surface: `fetch_entity_health_checks` returns an
`EntityHealthChecks`, the console serializes it through its own allowlist, and the
MCP tool renders `format_entity_health_checks`.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from cube_common import apollo_queries as Q
from cube_common.apollo_client import ApolloClient
from cube_common.apollo_pagination import drain_pages

logger = logging.getLogger(__name__)

HEALTHY = "HEALTHY"

# Entity statuses that assert a FAULT, so a clean report under one is worth saying
# is "not explained". The rest (SUSPENDED, DEFERRING, and Apollo's own NO_DATA,
# OUT_OF_DATE, ACTIVE_PLAN, ...) are not faults, and a clean report under them is
# just a clean report. Mirrors the warn/bad tones of `AppHealth.tsx::healthTone`.
FAULT_STATUSES = frozenset({"ERROR", "TERMINAL", "WARNING", "REPAIRING"})

# Result states. `issues` and `clear` both mean "Apollo reported, and we read it";
# they differ in whether anything in the report is unhealthy. `not_reported` is
# Apollo holding no node health at all for the entity, and `unavailable` is us
# failing to read — never folded into `clear`, which would be a false all-clear.
STATE_ISSUES = "issues"
STATE_CLEAR = "clear"
STATE_NOT_REPORTED = "not_reported"
STATE_UNAVAILABLE = "unavailable"

# Most severe first. From Witchcraft's `HealthState` docs (the source of Apollo's
# `ApolloHealthStatus`): TERMINAL "unrecoverable", ERROR "operationally unhealthy",
# WARNING "trending towards an error", REPAIRING "degraded, but capable of
# automatically recovering", SUSPENDED "no longer serving requests", DEFERRING
# "fully operational ... requesting to defer shutdown". NO_DATA / UNKNOWN_HEALTH
# are Apollo's own and undocumented. An unrecognized state sorts last rather than
# being guessed into a rank.
_SEVERITY = {
    "TERMINAL": 0, "ERROR": 1, "WARNING": 2, "REPAIRING": 3,
    "SUSPENDED": 4, "DEFERRING": 5, "UNKNOWN_HEALTH": 6, "NO_DATA": 7,
}

# The check whose `message` is always the same generic sentence; its cause is in
# `params.errorMessage` (verified live: "dial tcp 10.128.0.104:8443: connect:
# connection refused").
HEALTH_CHECK_ERRORED = "HEALTH_CHECK_ERRORED"

MAX_MESSAGE_CHARS = 500
# Bounds on what one result carries. A cube-wide outage can put the same failing
# check on every replica; past this the count of what was left out is reported.
MAX_ISSUES = 50
# Pages of nodes one read will follow. 50 nodes a page; the largest entity seen
# live had 7. Stopping early is reported as `truncated`, never as complete.
MAX_NODE_PAGES = 5

# Unanchored sibling of `tools/modules.py::_URL_WITH_USERINFO_RE`: that one asks
# whether a whole VALUE is a credential-bearing URL; this one finds such URLs
# inside free text, because a check message is prose that may quote a DSN.
#
# **Written to run in linear time, and the two differences from the obvious pattern
# are what buy it.** `[^/\s@]+:[^/\s@]+@` is quadratic: with `:` allowed on both
# sides, `a://!:!:!:…` (no `@`) is retried at every `:`, and CodeQL flags the
# anchored sibling as `py/polynomial-redos` for exactly that. (1) The USER part
# excludes `:` (RFC 3986: the first `:` in userinfo ends the user), so there is one
# split point. (2) The scheme is bounded, so an unanchored scan does not re-walk a
# long run of scheme characters from every word boundary. Pinned by
# `test_cleaning_runs_in_linear_time_on_adversarial_text`.
_URL_USERINFO_RE = re.compile(
    r"\b([a-z][a-z0-9+.-]{0,31}://)[^/\s@:]+:[^/\s@]*@", re.I
)
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")


@dataclass(frozen=True)
class CheckIssue:
    """One check reporting anything other than HEALTHY."""

    state: str
    check: str
    message: str
    pod: str
    container: str
    updated: str


@dataclass(frozen=True)
class ContainerIssue:
    """A container reporting not live or not ready — often the ONLY evidence."""

    pod: str
    container: str
    live: bool
    ready: bool
    updated: str


@dataclass(frozen=True)
class EntityHealthChecks:
    state: str
    checks: tuple[CheckIssue, ...] = ()
    containers: tuple[ContainerIssue, ...] = ()
    passing_checks: int = 0
    pods: int = 0
    # Newest `heartbeatTimestamp` across the entity's pods: when the cube last
    # reported, as opposed to `updated` on an issue, which is when that pod's
    # report last changed.
    reported_at: str = ""
    # Issues left out by `MAX_ISSUES`, and whether the node drain stopped early.
    omitted: int = 0
    truncated: bool = False


def clean_text(value: object) -> str:
    """Make app-written check text safe to show. See the module docstring."""
    if not isinstance(value, str):
        return ""
    text = _URL_USERINFO_RE.sub(r"\1<redacted>@", value)
    text = _CONTROL_RE.sub(" ", text)
    text = " ".join(text.split())
    if len(text) > MAX_MESSAGE_CHARS:
        text = text[: MAX_MESSAGE_CHARS - 1].rstrip() + "…"
    return text


def parse_timestamp(raw: str) -> datetime | None:
    """Apollo's RFC 3339 stamps, which carry NANOSECONDS (`…:10.522324011Z`).

    `datetime.fromisoformat` rejects more than six fractional digits on the
    Pythons this runs on, and comparing the strings is wrong within one second
    (`.` sorts before `Z`), so the fraction is trimmed to microseconds first.
    """
    if not raw or not isinstance(raw, str):
        return None
    text = raw.strip().replace("Z", "+00:00")
    text = re.sub(r"(\.\d{6})\d+", r"\1", text)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _check_message(check: dict) -> str:
    message = clean_text(check.get("message"))
    if (check.get("type") or check.get("name")) == HEALTH_CHECK_ERRORED:
        params = check.get("params")
        detail = clean_text(params.get("errorMessage")) if isinstance(params, dict) else ""
        if detail:
            return f"{message}: {detail}" if message else detail
    return message


class _Refused(Exception):
    """The entity is absent, or not on the environment the caller authorized."""


def _summarize(nodes: list[dict], truncated: bool) -> EntityHealthChecks:
    checks: list[CheckIssue] = []
    containers: list[ContainerIssue] = []
    passing = 0
    newest: tuple[datetime, str] | None = None

    for node in nodes:
        pod = node.get("nodeId") or ""
        updated = node.get("updatedTimestamp") or ""
        beat = node.get("heartbeatTimestamp") or ""
        parsed = parse_timestamp(beat)
        if parsed and (newest is None or parsed > newest[0]):
            newest = (parsed, beat)
        for ch in node.get("containerHealth") or []:
            container = ch.get("containerId") or ""
            live, ready = ch.get("liveness") is True, ch.get("readiness") is True
            if not (live and ready):
                containers.append(ContainerIssue(pod, container, live, ready, updated))
            for check in ch.get("checks") or []:
                state = check.get("state") or ""
                if state == HEALTHY:
                    passing += 1
                    continue
                checks.append(CheckIssue(
                    state=state or "UNKNOWN_HEALTH",
                    check=clean_text(check.get("type") or check.get("name")),
                    message=_check_message(check),
                    pod=pod, container=container, updated=updated,
                ))

    checks.sort(key=lambda c: (_SEVERITY.get(c.state, len(_SEVERITY)), c.check, c.pod))
    omitted = max(0, len(checks) - MAX_ISSUES) + max(0, len(containers) - MAX_ISSUES)

    if not nodes:
        # Nothing read AND the drain stopped early is a failed read, not Apollo
        # holding no report: `not_reported` is a claim about the entity.
        state = STATE_UNAVAILABLE if truncated else STATE_NOT_REPORTED
    elif checks or containers:
        state = STATE_ISSUES
    else:
        state = STATE_CLEAR

    return EntityHealthChecks(
        state=state,
        checks=tuple(checks[:MAX_ISSUES]),
        containers=tuple(containers[:MAX_ISSUES]),
        passing_checks=passing,
        pods=len(nodes),
        reported_at=newest[1] if newest else "",
        omitted=omitted,
        truncated=truncated,
    )


async def fetch_entity_health_checks(
    client: ApolloClient, env_id: str, entity_id: str
) -> EntityHealthChecks:
    """The health checks of ONE entity, which must be on environment `env_id`.

    `env_id` is the environment the CALLER already authorized and `entity_id` an id
    read from that environment's own entity list. Never raises: every failure is
    `unavailable`, because both callers render this as secondary detail beside a
    status they already have, and a failed drill-down must not take that down.
    """
    if not env_id or not entity_id:
        return EntityHealthChecks(state=STATE_UNAVAILABLE)

    async def fetch_page(token: str | None) -> dict | None:
        data = await client.graphql(Q.ENTITY_HEALTH_CHECKS, {
            "id": entity_id,
            "pageSize": Q.ENTITY_HEALTH_CHECKS_PAGE_SIZE,
            "pageToken": token,
        })
        entity = ((data or {}).get("apollo") or {}).get("entityById")
        if not entity:
            raise _Refused("entity not found")
        if ((entity.get("environment") or {}).get("id") or "") != env_id:
            raise _Refused("entity is on a different environment")
        page = entity.get("nodeHealths")
        if page is None and token is None:
            # A null page on the FIRST request is Apollo holding no node health for
            # this entity at all — `not_reported`. A null on a later page is a read
            # that fell short, which `drain_pages` reports as truncated.
            return {"nodeHealths": [], "nextPageToken": None}
        return page

    try:
        result = await drain_pages(
            fetch_page, items_key="nodeHealths",
            what=f"entity health checks for {entity_id}",
            max_pages=MAX_NODE_PAGES,
        )
    except _Refused as e:
        # Ids only — neither is secret, and the pair is what an operator needs to
        # tell a stale id from a caller probing another tenant's entity.
        logger.warning(
            "health checks refused for entity=%s env=%s: %s", entity_id, env_id, e
        )
        return EntityHealthChecks(state=STATE_UNAVAILABLE)
    except Exception as e:  # noqa: BLE001 — never raise; see the docstring.
        # Class name ONLY: an ApolloError's text embeds the raw GraphQL body, which
        # here would include every check's `params` — the fields discarded above.
        logger.warning(
            "health checks read failed for entity=%s: %s", entity_id, type(e).__name__
        )
        return EntityHealthChecks(state=STATE_UNAVAILABLE)

    return _summarize(result.items, result.truncated)


# --- MCP text rendering ------------------------------------------------------

_CHECK_ICONS = {
    "TERMINAL": "✗", "ERROR": "✗", "WARNING": "!", "REPAIRING": "⟳",
    "SUSPENDED": "-", "DEFERRING": "-",
}


def _container_problem(c: ContainerIssue) -> str:
    if not c.live and not c.ready:
        return "not live, not ready"
    return "not live" if not c.live else "not ready"


def format_entity_health_checks(
    result: EntityHealthChecks, entity_health: str, indent: str = "    "
) -> list[str]:
    """Text lines for `entity_health`. The console never calls this."""
    lines: list[str] = []
    healthy = entity_health == HEALTHY

    if result.state == STATE_UNAVAILABLE:
        return [f"{indent}Health checks: could not be read from Apollo."]
    if result.state == STATE_NOT_REPORTED:
        return [f"{indent}Health checks: Apollo holds no node health report for this entity."]

    when = f" (last report {result.reported_at[:19].replace('T', ' ')} UTC)" if result.reported_at else ""
    if result.state == STATE_CLEAR:
        if result.truncated:
            # Never an all-clear about pods we did not read.
            return [
                f"{indent}Health checks: the pod list could not be read to the end{when};",
                f"{indent}  nothing is failing among the {result.pods} pod(s) that were read,",
                f"{indent}  but that says nothing about the rest.",
            ]
        if healthy:
            return [f"{indent}Health checks: all {result.passing_checks} passing{when}."]
        if entity_health not in FAULT_STATUSES:
            return [f"{indent}Health checks: none failing and every container live and ready{when}."]
        return [
            f"{indent}Health checks: none failing and every container live and ready{when}.",
            f"{indent}  Apollo's {entity_health} is not explained by the checks it exposes;",
            f"{indent}  the app's logs (groundcover_search_logs) are the next place to look.",
        ]

    # Messages are the app's own words; saying so keeps an agent from relaying them
    # as our diagnosis.
    lines.append(f"{indent}Health checks{when}, as reported by the app:")
    for c in result.checks:
        where = f"{c.pod}/{c.container}" if c.container else c.pod
        text = f": {c.message}" if c.message else ""
        lines.append(f"{indent}  {_CHECK_ICONS.get(c.state, '?')} {c.state} {c.check}{text}  [{where}]")
    for c in result.containers:
        lines.append(f"{indent}  ✗ container {c.pod}/{c.container}: {_container_problem(c)}")
    if result.passing_checks:
        lines.append(f"{indent}  ({result.passing_checks} other check{'s' if result.passing_checks != 1 else ''} passing)")
    if result.omitted:
        lines.append(f"{indent}  ({result.omitted} more not shown)")
    if result.truncated:
        lines.append(f"{indent}  (the pod list was incomplete; more may be failing)")
    return lines
