"""Teleport connectivity for one cube — is its kube agent in contact?

The data layer behind the console's Teleport chip (`docs/console-spec.md` §4.17), and
**the place a future `teleport_status` MCP tool should call.** It lives under `tools/`
rather than in `console/reads.py` for the reason `clusters.fetch_services` does: the
dependency runs `console/ -> tools/` and never back, so platform knowledge parked in
the console layer is knowledge an MCP tool can only reach by inverting the layering or
by reimplementing the join — and reimplementing here means an agent reasoning over
`cube_list` and `list_modules` TEXT, which is the trap `console/reads.py`'s module
docstring rejects and which would re-make both bugs this module already fixed.

**Authorization is the CALLER's, and it cannot be shared.** `fetch_teleport_status`
takes an already-resolved `env_id` and performs no authorization of its own, because
the two surfaces authorize differently and deliberately so: the console resolves a cube
out of `_visible_environments` (cached per profile, exact case-sensitive match,
non-enumerable 404), while MCP tools use `tools/environments.py::_resolve_environment`
(RIDs and fuzzy names, uncached, distinct not-found/ambiguous/denied messages). Sharing
the console's path would hand an MCP tool a CACHED authorization decision on a surface
that re-resolves per call. `client` is already the caller's per-tenant Apollo
credential, so a wrong `env_id` fails at Apollo rather than leaking.

Presentation stays with each surface: this module returns a `TeleportStatus`, the
console serializes it through its own allowlist, and an MCP tool would render
`format_teleport_status`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from cube_common import apollo_queries as Q
from cube_common.apollo_client import ApolloClient

from cube_cloud.teleport.tbot_manager import TELEPORT_HEARTBEAT_TTL_SECONDS, tbot
from cube_cloud.tools import modules

logger = logging.getLogger(__name__)

#
# A third reachability chip on the cube page, beside Apollo's and Groundcover's. It
# answers a question neither of those does: **is this cube's Teleport agent in
# contact, so the platform can reach INTO it** — `kubectl_exec`, `list_services`, the
# app proxy and `expose` all ride that agent, and every one of them fails with a
# transport error rather than a diagnosis when it is down.
#
# **The signal is presence in `tsh kube ls`, and its time constant is Teleport's
# heartbeat TTL** (`TELEPORT_HEARTBEAT_TTL_SECONDS`, 900s). That listing carries no
# timestamp at all — name and labels only — so unlike the Groundcover badge there is
# no age to report, and the copy must not imply one. What presence bounds is "this
# agent announced itself within the last ~15 minutes"; what it does NOT bound is
# whether the cluster behind the agent is answering. Both facts are on the live fleet:
# `pico-cube-test` has held a fresh heartbeat while failing Teleport's own health
# check against its kube API since 2026-06-20.
#
# **Richer signals exist and were left alone deliberately.** `tctl get kube_server`
# carries `metadata.expires` (a real last-heartbeat bound), the agent version, and
# `status.target_health` — Teleport health-checking the cube's kube API, which is the
# single most actionable signal available anywhere. Reading it needs `kube_server`
# read/list verbs, and no role in this system has them: the cloud's `tctl` runs on the
# token-minter identity, scoped to `token:create` alone and deliberately without the
# shared-identity fallback (`teleport/tbot_manager.py::token_minter_identity_path`),
# and the per-profile roles `scripts/provision-access.py::ensure_teleport_role` writes
# carry no `rules:` block. So it would cost a new Teleport role, a new tbot identity
# output, a Secrets-Manager tbot config change and a redeploy — widening a credential
# that exists precisely to be narrow. `tsh kube ls` needs none of that; it is the call
# `cube_list` already makes on the identity we already hold.
#
# **Page only, not the cube list.** The join key (below) is a module variable, so an
# exact join costs one `LIST_MODULES` per cube — the same per-cube cost that kept
# inventory off the list (§4.13). The cube page already issues that query for
# `_exposed_apps`, so there the key is free.


# Both coordinates the Teleport agent ships under. `teleport-agent-module-ecr` is not
# a typo or a legacy alias — both are installed on the live fleet right now (0.5.0 and
# 0.4.0 of the former, 0.3.0 of the latter), so matching one silently reports every
# cube on the other as never enrolled.
#
# These are BASE coordinates — no `:version` segment — and they are matched with
# `modules._module_base_coordinate` rather than passed to
# `modules._find_module_by_coordinate`. That helper strips a trailing segment from
# whatever it is given, so a version-free constant loses its last WORD instead
# ("module:teleport-agent-module" -> "module:teleport-agent"), which matches nothing
# and reports the whole fleet as never enrolled. Every other caller happens to pass a
# versioned constant, so the trap is invisible until you do not.
TELEPORT_AGENT_MODULE_COORDINATES = (
    "module:teleport-agent-module",
    "module:teleport-agent-module-ecr",
)

# The Teleport label carrying the agent's resource id, which the module writes from
# its own `resourceId` variable. This is THE JOIN KEY — see `fetch_teleport_status`.
# It replaced the cluster name, which is caller-writable and therefore made this read
# a fleet-wide liveness oracle. Every one of the 53 live clusters a cube actually
# claims carries this label (fleet audit 2026-09-05); the three that do not are
# orphans no module declares.
TELEPORT_RESOURCE_ID_LABEL = "teleport.internal/resource-id"

# Apollo products that ARE a Teleport kube agent — the chart that gives the platform
# `kubectl` access into a cube. Both are live on the fleet, mirroring the module split.
#
# **`com.teleport:teleport-app-service` is deliberately NOT here, and that omission is
# the whole point of this constant.** The app service is the `expose` pathway: it
# publishes in-cube HTTP apps as Teleport *apps*. It grants no Kubernetes access, it
# does not register a kube cluster, and a cube can run it with no kube agent at all —
# which is exactly the configuration that made an earlier version of this read report
# "Disconnected" on cubes that had never had kube access (`cube-0rv5koeu`,
# `lear-flint-1`, verified live 2026-09-04). Adding it here would restore that bug.
TELEPORT_KUBE_AGENT_PRODUCT_IDS = (
    "com.teleport:teleport-kube-agent",
    "com.edgescaleai:teleport-kube-agent-ecr",
)

TELEPORT_STATES = frozenset(
    {"connected", "disconnected", "not_enrolled", "unknown"}
)


def _teleport_module(installations: list) -> dict | None:
    """The cube's Teleport agent module installation, under either coordinate.

    Version-agnostic, like `modules._find_module_by_coordinate` — but matching the
    base coordinates directly rather than going through it, for the reason on
    `TELEPORT_AGENT_MODULE_COORDINATES`.
    """
    for installed in installations:
        if not isinstance(installed, dict):
            continue
        base = modules.module_base_coordinate(
            installed.get("moduleMavenCoordinate") or ""
        )
        if base in TELEPORT_AGENT_MODULE_COORDINATES:
            return installed
    return None


def _teleport_agent_entity(entities: list) -> dict | None:
    """The cube's Teleport KUBE AGENT entity, or None if no such chart is installed.

    Matched on the product id rather than the display name: the name is editable in
    Apollo and `teleport-app-service` / `teleport-kube-agent` differ by one word, so a
    substring or name match is exactly how the app service gets mistaken for kube
    access. `TELEPORT_KUBE_AGENT_PRODUCT_IDS` says why that mistake is expensive.

    **Lifecycle is recorded, not gated on.** Anything but `INSTALLED` is logged so the
    enum can be learned from production, because it is not in the public schema and
    guessing it would reintroduce the same class of bug at a finer grain: rejecting an
    unrecognized-but-healthy lifecycle would report an enrolled cube as never enrolled.
    """
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        product = ((entity.get("product") or {}).get("productId") or "").strip()
        if product not in TELEPORT_KUBE_AGENT_PRODUCT_IDS:
            continue
        lifecycle = (entity.get("lifecycleStatus") or "").strip()
        if lifecycle and lifecycle != "INSTALLED":
            logger.info(
                "console teleport: kube agent entity %s has lifecycle %s, which this "
                "read does not recognize — treating it as deployed; confirm the enum "
                "before gating on it.",
                product, lifecycle,
            )
        return entity
    return None


# Every `reason` this module can emit. A definition site, because the vocabulary had
# none: the values were implied by five `return` statements and described only in a
# TypeScript comment. A second consumer branching on `reason` should not have to read
# the control flow to enumerate it.
TELEPORT_REASONS = frozenset({
    "",                  # connected
    "no_heartbeat",      # enrolled, agent not in Teleport's live listing
    "unavailable",       # we could not look (Apollo, tsh, or a saturated page)
    "no_cluster_name",   # a kube agent is deployed but no module identifies it
    "no_resource_id",    # the module carries no resourceId, so it cannot be matched
})


@dataclass(frozen=True)
class TeleportStatus:
    """One cube's Teleport connectivity. Data only — no colours, labels or copy."""

    cube: str
    state: str
    #: The cube's `kubeClusterName`; "" when it could not be read. Often NOT the
    #: cube name — see `TELEPORT_AGENT_MODULE_COORDINATES`.
    cluster: str
    reason: str
    heartbeat_ttl_seconds: int


async def fetch_teleport_status(
    client: ApolloClient, env_id: str, cube: str
) -> TeleportStatus:
    """Teleport connectivity for one cube, or None if the caller cannot see it.

    Returns `{cube, state, cluster, reason, heartbeat_ttl_seconds}` where `state` is
    `connected` | `disconnected` | `not_enrolled` | `unknown`.

    **Enrollment is the ENTITY; the module is only the join key.** The
    `teleport-agent-module` being linked to an environment mints an authToken and names
    a cluster, but it deploys nothing — the agent is a separate Apollo entity
    (`TELEPORT_KUBE_AGENT_PRODUCT_IDS`). Cubes exist with the module linked and no kube
    agent installed, running only `teleport-app-service`, which is the `expose` pathway
    and grants no Kubernetes access. An earlier version of this read treated the module
    as enrollment and reported those cubes "Disconnected" — a claim about cubes that had
    never had kube access. Verified live 2026-09-04 on `cube-0rv5koeu` and
    `lear-flint-1`. The entity is read first, and the module only after it confirms
    something is deployed.

    **The join key is the module's `resourceId`, and it must NOT be the cluster
    name.** The obvious key is `kubeClusterName` — the variable that tells the agent
    what to register as — and the first version used it. That is a security bug:
    `update_module_variables` accepts an arbitrary `kubeClusterName` on any
    environment the caller can already write, so joining on it turned this read into a
    **fleet-wide liveness oracle**. A scoped tenant could point their own enrolled
    cube at another tenant's cluster name and read the answer back: `connected` meant
    that name was live in Teleport right now, `disconnected` that it was not. The
    listing is read on the unscoped identity, so the answer spanned the whole fleet.
    `resourceId` is a UUID minted by the module install, so probing with it means
    guessing 122 bits.

    **The environment name is not the key either**, and that remains the trap it
    always was. Apollo's environment name IS the Groundcover cluster name
    (`auth/apollo_rbac.py::cluster_name`, verified against `ri.apollo.main`), and it is
    tempting to assume the same of Teleport. The full fleet audit (2026-09-05, all 172
    environments) found **three** divergences: `redhat-lab-cube` registers as
    `RHLab-Houston`, `hamza-blackwell` as `hamza-blackwell-ywkc`, and `staging-int` as
    `Staging-int` — a **case-only** difference, which is why any comparison against a
    cluster name must stay exact and case-sensitive rather than being "helpfully"
    normalized.

    **The audit is what made the id join safe, and it reversed an earlier decision
    recorded here.** This docstring used to say `resourceId` "can only disprove a
    match, never make one", because `dual-4000` carries no `teleport.internal/
    resource-id` label on the Teleport side. That reasoning was drawn from an 11-cube
    sample and does not survive the fleet:

      * **121 of 121** agent modules carry a `resourceId` (and a `kubeClusterName`);
        none is missing.
      * Every `resourceId` and every `kubeClusterName` on the fleet is **unique** — no
        two cubes contend for one cluster.
      * Of 56 live Teleport clusters, 53 are claimed by a module and **all 53 carry
        the resource-id label**. The three that do not are ORPHANS — `dual-4000`,
        `pico-cube-test` and `cube-pxh4b1bk` — registered in Teleport with no module
        declaring them. `dual-4000`, the one that blocked this design, is among them,
        so it can never be a legitimate join target and its missing label costs
        nothing.

    **The one cost, named so it is not rediscovered as a bug.** A module whose
    `resourceId` has drifted from the running agent's matches no cluster and therefore
    reports `disconnected` — a false claim on a healthy cube. The audit found exactly
    one, and it is REAL rather than a stale snapshot: `esai-dgx-spark-nanocube`'s
    module declares `4a5b4827…` while its running agent advertises `e8fe16c1…`,
    re-confirmed against live Teleport on 2026-09-08. That cube therefore reads
    DISCONNECTED on the console until the two are reconciled. The drift is loudly
    logged at ERROR with both values whenever the declared name IS live, which makes it
    self-identifying; the fix is to reconcile the module with the agent, not to soften
    this read. Softening it by falling back to the name is exactly what reopens the
    oracle.

    **Four states, and none of them collapse into another.**

      * `connected`    — the module's cluster is in Teleport's live listing.
      * `disconnected` — the cube has an agent module but no live cluster. A real
                         observation, and often intended: an air-gapped cube, or one
                         whose network forbids egress, looks exactly like this.
      * `not_enrolled` — no agent module at all. This cube was never asked to join
                         Teleport, so `disconnected` would be a complaint about a
                         configuration nobody chose. Rendered with the quietest
                         treatment available, never hidden — see
                         `TeleportStatus.tsx` rule 1a.
      * `unknown`      — we could not ask, or the answer was contradictory. Never
                         rendered as `disconnected`, for the reason
                         `CubeStatus.tsx` rule 1 gives: a false negative on a cube
                         the viewer is actively using costs the chip its credibility
                         everywhere else.

    **Authorization belongs to the caller, and the response carries no other
    tenant's data.** The only Teleport datum in it is a cluster name that this cube's
    own module claims by resource id, which the caller can already read through
    `list_modules`; the fleet listing itself never leaves this function.

    The cross-tenant liveness oracle that the name join opened is **closed** by keying
    on `resourceId` (above), not merely mitigated. What remains is a UUID-confirmation
    oracle — a caller who already knows another cube's `resourceId` could confirm that
    it is live — and reaching that state means reading a module they are authorized to
    read, so it grants nothing they did not already have.

    **Never raises**, and never logs an Apollo error's text — `LIST_MODULES` selects
    every module's variable values, and `ApolloError` embeds the raw response body, so
    `%s` on it would put another module's secret in CloudWatch. Class name only, the
    same rule as `_exposed_apps_read`.
    """
    def result(state: str, cluster: str = "", reason: str = "") -> TeleportStatus:
        return TeleportStatus(
            cube=cube,
            state=state,
            # The name the cube registers under, published because it is often NOT
            # the cube name and a viewer looking at `tsh` output needs to connect the
            # two. It is this cube's own module variable, not a fleet fact.
            cluster=cluster,
            reason=reason,
            # What presence in the listing bounds, so the client can say "in contact"
            # with a stated window instead of implying a live probe.
            heartbeat_ttl_seconds=TELEPORT_HEARTBEAT_TTL_SECONDS,
        )

    # ENROLLMENT IS THE ENTITY, NOT THE MODULE — and this ordering is the fix for a
    # live bug rather than a preference. See `TELEPORT_KUBE_AGENT_PRODUCT_IDS`: the
    # `teleport-agent-module` being linked mints an authToken and names a cluster, but
    # it does not deploy anything. The chart is a separate Apollo entity, and cubes
    # exist with the module linked and no kube agent installed — they run only the
    # app service. Reading the module first and treating it as enrollment reported
    # those cubes as "Disconnected", a claim about a cube that had never had kube
    # access at all.
    #
    # The entity read comes FIRST so an un-enrolled cube costs one Apollo query rather
    # than two; the module is then read only for its join key.
    try:
        data = await client.graphql(Q.TELEPORT_AGENT_ENTITIES, {"id": env_id})
        page = (
            (data.get("apollo") or {}).get("environmentById") or {}
        ).get("entities") or {}
        entities = page.get("entities") or []
        saturated = bool(page.get("nextPageToken"))
    except Exception as e:
        logger.warning(
            "teleport status: entity read failed for %s (%s)", cube, type(e).__name__
        )
        return result("unknown", reason="unavailable")

    agent = _teleport_agent_entity(entities)
    if agent is None:
        if saturated:
            # "Not enrolled" is a conclusion drawn from ABSENCE, so a partial entity
            # list cannot support it — the agent may be on the page we did not read.
            logger.warning(
                "teleport status: %s has a saturated entity page and no kube agent "
                "in it; reporting unknown rather than not_enrolled.", cube,
            )
            return result("unknown", reason="unavailable")
        return result("not_enrolled")

    try:
        installations = await modules._fetch_module_installations(client, env_id)
    except Exception as e:
        logger.warning(
            "teleport status: module read failed for %s (%s) — use the "
            "list_modules tool to see the underlying error.",
            cube, type(e).__name__,
        )
        return result("unknown", reason="unavailable")

    module = _teleport_module(installations)
    if module is None:
        # The chart is installed but the module that configures it is not, so nothing
        # says which cluster name the agent registers under. `not_enrolled` would
        # contradict the entity we just found; `disconnected` would be a guess.
        logger.warning(
            "teleport status: %s has a Teleport kube agent entity but no agent "
            "module, so its cluster name is unknown; coordinates present: %s",
            cube,
            sorted(
                modules.module_base_coordinate(
                    (i or {}).get("moduleMavenCoordinate") or ""
                )
                for i in installations
                if isinstance(i, dict)
            ),
        )
        return result("unknown", reason="no_cluster_name")

    declared_id = modules.module_variable(module, "resourceId")
    declared_name = modules.module_variable(module, "kubeClusterName")

    if not declared_id:
        # Nothing to look the cube up BY. Reporting `disconnected` would blame the
        # cube for a module we cannot read. The fleet audit of 2026-09-05 found 121
        # of 121 agent modules carrying a resourceId, so this branch should never
        # fire — it exists so a module that somehow lacks one degrades to an
        # admission rather than a claim.
        logger.warning(
            "teleport status: %s has a teleport agent module with no resourceId "
            "variable, so it cannot be matched to a Teleport cluster", cube,
        )
        return result("unknown", cluster=declared_name, reason="no_resource_id")

    # The ADMIN identity deliberately, not the caller's profile. A per-profile
    # `tsh kube ls` is already scoped by the Teleport role's
    # `kubernetes_labels: {cube: [...]}`, but that scoping is only as good as the
    # `cube` label — which just 18 of 56 live clusters advertise, because it needs
    # teleport-agent module >= 0.5.0 (docs/rbac-architecture.md, and
    # `provision-access.py::check_cube_labels`, which warns about exactly this). A
    # scoped identity would therefore under-report arbitrarily and render enrolled
    # cubes as disconnected. Apollo is the authority for what this caller may see, and
    # the resolve above has already applied it.
    clusters, ok = await tbot.list_kube_clusters_detailed()
    if not ok:
        return result("unknown", cluster=declared_name, reason="unavailable")

    # THE LOOKUP KEY IS THE RESOURCE ID, NOT THE NAME — see this module's security
    # note. `kubeClusterName` is caller-writable through `update_module_variables`,
    # so joining on it made this read a fleet-wide liveness oracle: a scoped tenant
    # could point their own cube at another tenant's cluster name and read back
    # whether it was live. A resource id is a UUID minted by the module install, so
    # probing with it means guessing 122 bits.
    by_resource_id = {
        rid: name
        for name, labels in clusters.items()
        if (rid := str((labels or {}).get(TELEPORT_RESOURCE_ID_LABEL) or "").strip())
    }

    matched = by_resource_id.get(declared_id)
    if matched:
        # The matched cluster's OWN name, not the module's declared one: they agree
        # in every audited case, and where they could differ the live cluster is the
        # authority on what it is called.
        return result("connected", cluster=matched)

    # Not found by id. `declared_name` is deliberately NOT consulted to soften this
    # answer — doing so is exactly what reopens the oracle, since the caller chooses
    # that string. It is used only to LOG a drift, server-side, which changes nothing
    # the caller can observe.
    if declared_name and declared_name in clusters:
        # This is ALSO the detection signal for the oracle attempt the id join
        # closes: a caller who points their own module at a cluster they do not own
        # produces exactly this shape. Benign drift is far likelier (the 2026-09-05
        # audit found one, `esai-dgx-spark-nanocube`, and zero name collisions), so
        # the message names both readings rather than accusing — but a burst of these
        # across cubes, or one naming another tenant's cluster, is worth looking at.
        logger.error(
            "teleport status: %s declares resourceId=%s which no live Teleport "
            "cluster advertises, yet a cluster named %s IS live. Either that "
            "module's resourceId is stale after a reinstall (the common case, and "
            "the fix is to reconcile module and agent), or the module has been "
            "pointed at a cluster this cube does not own. Reported DISCONNECTED "
            "either way — the answer never depends on the declared name.",
            cube, declared_id, declared_name,
        )

    # A kube agent IS deployed here and no live cluster carries this cube's resource
    # id, so the agent is not reporting. Verified as a real state rather than a
    # leftover: `cube-nvqfm723` has the chart installed and is absent from the
    # listing.
    return result("disconnected", cluster=declared_name, reason="no_heartbeat")


def format_teleport_status(status: TeleportStatus) -> str:
    """Render a `TeleportStatus` as operator-facing text, for an MCP tool.

    Separate from the computation so the console can serialize the same structured
    value instead of parsing this — the `fetch_services` / `list_services` split.
    Deliberately states the heartbeat window rather than an age: `tsh kube ls` carries
    no timestamp, so there is none to report.
    """
    lines = [f"Teleport connectivity for {status.cube}:", "=" * 50]
    window = status.heartbeat_ttl_seconds // 60
    if status.state == "connected":
        lines.append(f"  State:   CONNECTED (reported in within ~{window}m)")
    elif status.state == "disconnected":
        lines.append(
            f"  State:   DISCONNECTED (no heartbeat for at least ~{window}m)"
        )
        lines.append(
            "           The cube may be air gapped, or its network may disallow "
            "egress to Edgeport — not necessarily a fault."
        )
    elif status.state == "not_enrolled":
        lines.append("  State:   NOT ENROLLED (no Teleport kube agent deployed)")
        lines.append(
            "           kubectl_exec, list_services and app proxying are "
            "unavailable on this cube."
        )
    else:
        lines.append("  State:   UNKNOWN (could not be determined)")
    if status.reason:
        lines.append(f"  Reason:  {status.reason}")
    if status.cluster:
        lines.append(f"  Cluster: {status.cluster}")
        if status.cluster != status.cube:
            lines.append("           (registers in Teleport under that name)")
    return "\n".join(lines)
