"""All Apollo GraphQL query and mutation strings."""

# ---------------------------------------------------------------------------
# User / team queries
# ---------------------------------------------------------------------------

MY_TEAMS = """
query MyTeams {
    me {
        apolloTeams {
            name
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Environment queries
# ---------------------------------------------------------------------------

GET_ENVIRONMENT_BY_RID = """
query GetEnv($rid: RID!) {
    apollo {
        environment(rid: $rid) {
            id
            rid
            name
            spaceId
            namespaceId
            rolePolicy {
                teamRoleStatements {
                    team { name }
                }
            }
        }
    }
}
"""

# Page size for the environment reads. Both environment queries take it as a
# VARIABLE (never a literal) so the drain loop in `apollo_pagination.py` owns it,
# and so this constant is the single place it changes.
#
# **Why 500 rather than the 200 this used to be.** Measured live against the fleet
# (202 environments, 2026-09-21): draining at 200 is two round-trips and 0.84s,
# while a single 500-row page is 0.62s. `allowed_cubes` — the Groundcover
# authorization boundary — is UNCACHED and runs on every Groundcover tool call and
# three console read paths, so an extra round-trip there is paid constantly. A page
# size comfortably above the fleet keeps the common case at one request while the
# loop stays correct at any size. Apollo does not cap it at 200 (pageSize: 1000
# returns all 202 with a null token — the `min(..., 200)` clamp in
# `tools/products.py` is this repo's own invention, not an Apollo limit).
#
# **This is a headroom choice, NOT a fix.** The fix is the loop. Raising this number
# in response to a truncation report would be re-making the bug that issue 252
# describes; the loop is what makes the fleet size stop mattering.
ENVIRONMENTS_PAGE_SIZE = 500

# `environments(filter: ApolloEnvironmentFilterSpec!, spaceId: String,
# pageToken: String, pageSize: Int!) -> ApolloEnvironmentPage!`
#
# Confirmed by introspection against the live schema on 2026-09-21
# (`scripts/apollo_introspect.py --queries environment`), not inferred from the
# `apollo.products` precedent — AGENTS.md rule 9. Two things that introspection
# settled and are worth keeping written down:
#
#   * `filter` is declared NON-NULL yet omitting it works, so it has a server-side
#     default. Do not "fix" that by sending an empty filter without checking what
#     the default actually is.
#   * `ApolloEnvironmentFilterSpec` is `{owner, accreditation, namespace,
#     remoteStatus}` — there is **no name filter**, which is why the console
#     searches client-side over the whole drained list rather than round-tripping
#     per keystroke.
LIST_ENVIRONMENTS = """
query ListEnvs($pageSize: Int!, $pageToken: String) {
    apollo {
        environments(pageSize: $pageSize, pageToken: $pageToken) {
            environments {
                id
                rid
                name
                spaceId
                namespaceId
                rolePolicy {
                    teamRoleStatements {
                        team { name }
                    }
                }
            }
            nextPageToken
        }
    }
}
"""

# NOTE: the guard on how these queries take their page size lives in a TEST
# (packages/cube-cloud/tests/test_apollo_pagination.py::test_the_environment_queries_take_the_page_size_as_a_VARIABLE),
# deliberately NOT as a module-level assert here.
#
# An import-time assert in this module ships to every user of the published
# `edgescaleai-cube-mcp` package, so a bad edit to a query would break
# `import cube_common.apollo_queries` — i.e. the whole CLI — rather than failing
# CI. It is also stripped under `python -O`, so it is not a dependable runtime
# check either. A test catches the drift where the drift is introduced.
#
# What that test pins has CHANGED with pagination, and the new property is the
# load-bearing one: it asserts each query declares `$pageSize`/`$pageToken` and
# contains **no hardcoded `pageSize: <number>`**. The old test pinned the constant
# to a literal in the query text; a literal is now exactly the regression to
# prevent, because a hardcoded size silently un-paginates the read while every
# other test still passes.

# Environments for the browser console: LIST_ENVIRONMENTS plus a display name and
# per-agent connection status (docs/console-spec.md §4.16).
#
# **A SEPARATE query rather than widening LIST_ENVIRONMENTS**, which is on two hot
# paths that need none of this:
#
#   * `auth/apollo_rbac.py::allowed_cubes` — the Groundcover authorization boundary.
#     It is NOT cached and runs on every Groundcover tool call and every
#     `/console/api/cubes/{cube}/status` request.
#   * `tools/environments.py::_resolve_environment` — reissued per MCP tool call.
#
# Measured on the live list query (166 environments): baseline 0.35s,
# +displayMetadataV2 0.36s, +agents 0.59s. Cheap for a console page cached per
# profile; a 0.24s tax on an uncached authz check is not, so those keep the lean
# query. Same reasoning, and the same shape, as CONSOLE_ENVIRONMENT_ENTITIES.
#
# Three things about this selection will bite anyone editing it:
#
# 1. **`agents` is a UNION** (`ApolloAgent_Reporting | ApolloAgent_NeverReported`), so
#    a bare `agents { agentId }` is a schema error, not an empty result. The
#    `... on IApolloAgent` interface fragment covers both members in one go.
#
# 2. **NEVER select `ApolloEnvironment.latestAgentUpdateTime` here.** It is the
#    obvious-looking field and it takes this query from ~0.5s to **~4.5s** across 166
#    environments. `ApolloAgent_Reporting.lastUpdated` is free and carries the same
#    information.
#
# 3. **`displayMetadataV2` is nullable** and only ~50 of 166 environments have one —
#    and several of those are just an echo of the environment id. It is a LABEL,
#    never a key; `console/reads.py::_display_name` drops the echoes.
CONSOLE_LIST_ENVIRONMENTS = """
query ConsoleListEnvs($pageSize: Int!, $pageToken: String) {
    apollo {
        environments(pageSize: $pageSize, pageToken: $pageToken) {
            environments {
                id
                rid
                name
                spaceId
                namespaceId
                displayMetadataV2 {
                    displayName
                }
                agents {
                    __typename
                    ... on IApolloAgent {
                        agentId
                        connectionStatus
                    }
                    ... on ApolloAgent_Reporting {
                        lastUpdated
                    }
                }
                rolePolicy {
                    teamRoleStatements {
                        team { name }
                    }
                }
            }
            nextPageToken
        }
    }
}
"""

CREATE_ENVIRONMENT = """
mutation CreateEnv($request: CreateApolloEnvironmentRequest!) {
    apollo {
        createEnvironment(request: $request) {
            id
            rid
            name
            spaceId
            namespaceId
            accreditation
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Module queries
# ---------------------------------------------------------------------------

INSTALL_MODULE = """
mutation InstallModule($request: InstallApolloProductModuleInputV2!) {
    apollo {
        installModuleV2(request: $request) {
            rid
            displayName
            moduleMavenCoordinate
            state {
                __typename
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Entity queries
# ---------------------------------------------------------------------------

ENTITY_HEALTH_FIELDS = """
    id
    rid
    displayName
    lifecycleStatus
    product { productId }
    entityLocator {
        ... on ApolloEntityLocator_ApolloEntity { entityName }
    }
    reportedStatus {
        version
        rolloutStatus
        configStatus
        healthStatus
        upgradeBlockerTypes
    }
    declaredState { config }
    installedByModuleV2 { rid displayName moduleMavenCoordinate }
    planStatus {
        __typename
        ... on ApolloEntityPlanStatus_Blocked {
            blockedChangesCount
        }
    }
    nonGenericPlans(pageSize: 5) {
        plans {
            rid
            agentId
            status {
                type
                result { summary }
                reason { summary }
            }
            startTime
            endTime
            tasks {
                description { type summary }
                status {
                    type
                    updatedAt
                }
            }
        }
    }
"""

ENVIRONMENT_ENTITIES = f"""
query EnvironmentEntities($id: String!) {{
    apollo {{
        environmentById(id: $id) {{
            name
            entities(pageSize: 100) {{
                entities {{
                    {ENTITY_HEALTH_FIELDS}
                }}
            }}
        }}
    }}
}}
"""

# Entities for the browser console's per-cube view.
#
# A SEPARATE, LEANER query than ENVIRONMENT_ENTITIES on purpose — do not "simplify"
# this by reusing ENTITY_HEALTH_FIELDS. Two fields are deliberately absent:
#
#   * `declaredState { config }` — carries CLEARTEXT deployment secrets (verified
#     live: a litellm `masterKey` on cube-66odzn95). Excluding it at the QUERY is
#     strictly stronger than excluding it at serialization: the secret never
#     crosses the network into this process, so no future logging statement,
#     traceback, telemetry payload, or debugger session can surface what was never
#     fetched. docs/console-spec.md §4.4.
#   * `nonGenericPlans` — the recent-plan/deploy history. Omitted both because the
#     console does not show it (operator decision: plan events are noise at this
#     phase) and because it is by far the largest part of the entity payload.
#
# Adding either field back is a security/performance decision, not a refactor.
CONSOLE_ENVIRONMENT_ENTITIES = """
query ConsoleEnvironmentEntities($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            entities(pageSize: 200) {
                entities {
                    id
                    displayName
                    lifecycleStatus
                    product { productId }
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    reportedStatus {
                        version
                        rolloutStatus
                        configStatus
                        healthStatus
                        upgradeBlockerTypes
                    }
                    planStatus {
                        __typename
                        ... on ApolloEntityPlanStatus_Blocked {
                            blockedChangesCount
                        }
                    }
                }
                nextPageToken
            }
        }
    }
}
"""

# The health checks behind ONE entity's `healthStatus` — the "why" behind an
# Error the app list can only name (docs/console-spec.md §4.21). Shared by the
# console's per-app drill-down and the MCP `entity_health` tool through
# `cube_cloud/tools/health_checks.py`.
#
# Shape verified by introspection (2026-09-30), not inferred: `nodeHealths` is a
# nullable `ApolloNodeHealthPage` paginated by `pageToken: PageToken`, each node
# carries `containerHealth[]`, and each container carries `checks[]` of
# `{name, type, message, state: ApolloHealthStatus, params: Any!}` — Witchcraft's
# `HealthCheckResult`, whose `message` is documented as the actionable text.
#
# Three things are load-bearing:
#
#   * **`entityById` takes a FLEET-WIDE id and authorizes nothing by environment.**
#     `environment { id }` is selected so the caller can prove the entity is on
#     the cube it already authorized; an entity id must never come from a request
#     unchecked. See `health_checks.fetch_entity_health_checks`.
#   * **`params` is selected for ONE key.** `HEALTH_CHECK_ERRORED`'s `message` is
#     a generic "The service threw an error returning health" and the actual cause
#     is `params.errorMessage`. GraphQL cannot select into `Any`, so the whole map
#     arrives — and it carries internal hosts, ports, database names and Peplink
#     serials (verified live). The normalizer keeps `errorMessage` and discards the
#     rest before anything else sees it; never log or serialize the raw map.
#   * **No `declaredState`.** Same reason as CONSOLE_ENVIRONMENT_ENTITIES.
ENTITY_HEALTH_CHECKS = """
query EntityHealthChecks($id: String!, $pageSize: Int!, $pageToken: PageToken) {
    apollo {
        entityById(apolloEntityId: $id) {
            id
            environment { id }
            reportedStatus { healthStatus }
            nodeHealths(pageSize: $pageSize, pageToken: $pageToken) {
                nodeHealths {
                    nodeId
                    updatedTimestamp
                    heartbeatTimestamp
                    containerHealth {
                        containerId
                        liveness
                        readiness
                        checks { name type message state params }
                    }
                }
                nextPageToken
            }
        }
    }
}
"""

ENTITY_HEALTH_CHECKS_PAGE_SIZE = 50

# Page size for CONSOLE_ENVIRONMENT_ENTITIES. Exported so a full page can be
# detected as SATURATION — a cube with more entities than one page would otherwise
# show a silently short app list.
#
# **This read is still single-page, and the saturation signal is correct HERE and
# nowhere else.** The environment reads used the same trick until they were
# drained (issue 252 / OI-6); `ENVIRONMENTS_PAGE_SIZE` is no longer a
# saturation constant, and `truncated` on that path now means "the drain stopped
# early", which is the opposite reading. Do not cite the two as a matching pair.
#
# Draining this one is the tracked follow-up, and it needs no new loop:
# `cube_common.apollo_pagination.drain_pages` takes a page-fetching callable and
# an `items_key`. Two things to get right when doing it — the page hangs off
# `environmentById`, which unlike `apollo.environments` is NULLABLE, so guard 4
# (an absent envelope is `truncated`, not a finished read) is load-bearing here in
# a way it is not for environments; and `_identity` will need a key suited to
# entities, since its `name` fallback is not safe for items that can share a name.
CONSOLE_ENTITIES_PAGE_SIZE = 200

# Is a Teleport KUBE AGENT actually deployed on this cube? (docs/console-spec.md §4.17)
#
# **A SEPARATE, MINIMAL query rather than reusing CONSOLE_ENVIRONMENT_ENTITIES**, for
# the same reason CONSOLE_ENTITY_PLANS is separate: that query backs the cube page's
# primary content and selects `reportedStatus`, `planStatus`, locators and display
# names for up to 200 entities. Answering "does a kube-agent chart exist here" needs
# two fields, and this endpoint is decoration that must not do the apps list's work
# twice.
#
# **`declaredState.config` is NOT selected and must never be.** Entity config is where
# cleartext deployment secrets live (AGENTS.md rule 3) — the Teleport charts are a
# live example: `entity_health`, which does select it, prints a cube's Teleport app
# join token in the clear.
#
# `nextPageToken` is selected so the reader can detect SATURATION. It matters here
# because the conclusion drawn from *absence* is a claim ("not enrolled"), so a cube
# with more entities than one page must report unknown rather than an answer derived
# from a partial list.
TELEPORT_AGENT_ENTITIES = """
query TeleportAgentEntities($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            entities(pageSize: 200) {
                entities {
                    displayName
                    lifecycleStatus
                    product { productId }
                }
                nextPageToken
            }
        }
    }
}
"""

# "Last changed" per entity for the console's app list (docs/console-spec.md §4.15).
#
# **A SEPARATE, MINIMAL query rather than widening CONSOLE_ENVIRONMENT_ENTITIES.**
# That query's own note calls omitting `nonGenericPlans` a deliberate
# security/performance decision because plans are "by far the largest part of the
# entity payload" — and it backs the apps list, the cube page's primary content. This
# query is fetched alongside it, so a slow plan read cannot delay the list, and the
# omission there stands.
#
# It selects FOUR fields per plan where `ENTITY_HEALTH_FIELDS` selects the whole task
# and event tree. Do not "reuse the existing fragment" here: the tasks/subtasks/events
# subtree is what makes plans expensive, and none of it is needed to answer "when did
# this last change".
#
# `PLANS_PAGE_SIZE` is exported so the reader can detect SATURATION. That matters
# more than usual: Apollo's plan ORDERING is not documented anywhere, and this repo
# has only ever assumed newest-first (`format_plan_details` indexes `plans[0]`;
# `cancel_active_plan` takes the first status match). A full page plus oldest-first
# ordering means the newest plans are outside the page — so the reader infers the
# direction from the page itself and reports unknown rather than a date it cannot
# stand behind. See `console/reads.py::_last_change_for`.
CONSOLE_ENTITY_PLANS = """
query ConsoleEntityPlans($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            entities(pageSize: 200) {
                entities {
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    nonGenericPlans(pageSize: 20) {
                        plans {
                            startTime
                            endTime
                            status { type }
                        }
                    }
                }
                nextPageToken
            }
        }
    }
}
"""

# Keep in step with the literal in the query above —
# packages/cube-cloud/tests/test_console_changes.py enforces it, for the same reason
# ENVIRONMENTS_PAGE_SIZE has a test rather than an import-time assert.
CONSOLE_PLANS_PAGE_SIZE = 20

INSTALL_ENTITIES = """
mutation InstallEntities($envId: String!, $namespaceId: String!, $entities: InstallApolloEntitiesOnEnvironmentRequest!) {
    apollo {
        installEntitiesOnEnvironmentV2(apolloEnvironmentId: $envId, namespaceId: $namespaceId, entities: $entities) {
            rid
            title
            requestStatus
        }
    }
}
"""

UNINSTALL_ENTITY = """
mutation UninstallEntity($namespaceId: String!, $entityId: String!) {
    apollo {
        uninstallEntityV2(namespaceId: $namespaceId, entityId: $entityId) {
            rid
            requestStatus
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Replication queries
# ---------------------------------------------------------------------------

SOURCE_ENVIRONMENT = """
query SourceEnv($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            accreditation
            moduleInstallationsV2 {
                moduleInstallations {
                    displayName
                    moduleMavenCoordinate
                    variables {
                        variableName
                        variableValue {
                            __typename
                            ... on ApolloProductModuleVariableValue_StringValue { value }
                            ... on ApolloProductModuleVariableValue_OptionValue { value }
                        }
                    }
                }
            }
            entities(pageSize: 200) {
                entities {
                    id
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName type }
                    }
                    product { productId }
                    declaredState { releaseChannel }
                    installedByModuleV2 { rid }
                    reportedConfigOverrides {
                        ... on ApolloEntityReportedConfigOverrides_Default {
                            overrides
                        }
                    }
                    secrets {
                        name
                        specification {
                            ... on ApolloSecretSpecification_MultiKey {
                                keys { key }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

TARGET_ENVIRONMENT = """
query TargetEnv($id: String!) {
    apollo {
        environmentById(id: $id) {
            moduleInstallationsV2 {
                moduleInstallations {
                    moduleMavenCoordinate
                }
            }
            entities(pageSize: 200) {
                entities {
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                }
            }
        }
    }
}
"""

CLEANUP_CHECK = """
query CleanupCheck($id: String!) {
    apollo {
        environmentById(id: $id) {
            entities(pageSize: 200) {
                entities {
                    rid
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                }
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Plan details query
# ---------------------------------------------------------------------------

PLAN_DETAILS = """
query PlanDetails($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            entities(pageSize: 200) {
                entities {
                    id
                    displayName
                    lifecycleStatus
                    product { productId }
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    reportedStatus { version }
                    nonGenericPlans(pageSize: 10) {
                        plans {
                            rid
                            agentId
                            proposedTime
                            startTime
                            endTime
                            status {
                                type
                                result { type summary metadataMap }
                                reason { type summary metadataMap }
                            }
                            stateChanges {
                                entityType
                                changeType
                            }
                            tasks {
                                rid
                                origin
                                description { type summary }
                                createdAt
                                status {
                                    type
                                    updatedAt
                                    description { type summary metadataMap }
                                }
                                latestEvent {
                                    timestamp
                                    description { summary }
                                }
                                events {
                                    timestamp
                                    description { summary }
                                }
                                subtasks {
                                    origin
                                    description { type summary }
                                    createdAt
                                    status {
                                        type
                                        updatedAt
                                        description { type summary metadataMap }
                                    }
                                    latestEvent {
                                        timestamp
                                        description { summary }
                                    }
                                    events {
                                        timestamp
                                        description { summary }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Environment management mutations
# ---------------------------------------------------------------------------

DELETE_ENVIRONMENT = """
mutation DeleteEnv($rid: RID!) {
    apollo {
        deleteEnvironment(rid: $rid) {
            rid
            requestStatus
        }
    }
}
"""

RESET_ENVIRONMENT_AGENTS = """
mutation ResetAgents($envId: String!) {
    apollo {
        resetAgentsByEnvironmentId(apolloEnvironmentId: $envId) {
            __typename
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Entity management mutations
# ---------------------------------------------------------------------------

UPDATE_ENTITY_CONFIG = """
mutation UpdateEntityConfig($spaceId: String!, $update: ApolloChangeRequestUpdateConfig!) {
    apollo {
        updateConfigByResource(spaceId: $spaceId, update: $update) {
            rid
            requestStatus
        }
    }
}
"""

# The non-deprecated config write (`updateConfigByResource` is marked deprecated:
# "Use updateConfigByResourceV2 which returns typed errors instead of throwing
# exceptions"). Introspected 2026-10-06: the result is `ApolloOpenChangeRequestResult
# {changeRequest: ApolloChangeRequest, error: ApolloOpenChangeRequestError}`, the error
# a union that includes `_NoChanges` (the submitted config equals the current one) and
# `_BaseVersionEmpty`. `update.content` is YAML; JSON is valid YAML.
UPDATE_ENTITY_CONFIG_V2 = """
mutation UpdateEntityConfigV2($spaceId: String, $update: ApolloChangeRequestUpdateConfig!) {
    apollo {
        updateConfigByResourceV2(spaceId: $spaceId, update: $update) {
            changeRequest {
                rid
                requestStatus
            }
            error {
                __typename
            }
        }
    }
}
"""

# One AI Reactor gateway entity, for the console's AI tab (docs/ai-reactor-deploy-spec.md
# §6). Selects `declaredState.config`, which console rule 3 otherwise forbids: this read
# is the scoped exception. The id must come from the authorized cube's own entity list,
# and `environment { id }` is selected so the caller can prove it, because `entityById`
# is FLEET-WIDE (see ENTITY_HEALTH_CHECKS). Every field introspected 2026-10-06.
REACTOR_GATEWAY_ENTITY = """
query ReactorGatewayEntity($id: String!) {
    apollo {
        entityById(apolloEntityId: $id) {
            id
            environment { id }
            declaredState {
                config
                releaseChannel
            }
            installedByModuleV2 {
                moduleMavenCoordinate
            }
        }
    }
}
"""

ENFORCE_ENTITY_CONFIG = """
mutation EnforceEntityConfig($rid: RID!) {
    apollo {
        enforceEntityConfig(rid: $rid) {
            rid
            requestStatus
        }
    }
}
"""

ENTITY_BY_NAME = """
query EntityByName($id: String!) {
    apollo {
        environmentById(id: $id) {
            spaceId
            entities(pageSize: 200) {
                entities {
                    id
                    rid
                    displayName
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    product { productId }
                    reportedStatus {
                        version
                        configStatus
                        upgradeBlockerTypes
                    }
                    declaredState { config }
                    # Who manages this entity's config. `update_entity_config` and
                    # `install_entity` refuse a module-managed entity without force,
                    # so this must stay selected (introspected 2026-10-20: an
                    # ApolloProductModuleInstallationV2; none of these three fields
                    # carries a variable value).
                    installedByModuleV2 { rid displayName moduleMavenCoordinate }
                    planStatus {
                        __typename
                        ... on ApolloEntityPlanStatus_Blocked {
                            blockedChangesCount
                        }
                    }
                    reportedConfigOverrides {
                        ... on ApolloEntityReportedConfigOverrides_Default {
                            overrides
                        }
                    }
                }
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Module management queries
# ---------------------------------------------------------------------------

LIST_MODULES = """
query ListModules($id: String!) {
    apollo {
        environmentById(id: $id) {
            name
            moduleInstallationsV2 {
                moduleInstallations {
                    rid
                    displayName
                    moduleMavenCoordinate
                    state {
                        __typename
                    }
                    variables {
                        variableName
                        variableValue {
                            __typename
                            ... on ApolloProductModuleVariableValue_StringValue { value }
                            ... on ApolloProductModuleVariableValue_OptionValue { value }
                        }
                    }
                }
            }
        }
    }
}
"""

UNINSTALL_MODULE = """
mutation UninstallModule($installationRid: RID!) {
    apollo {
        unlinkModule(installationRid: $installationRid) {
            rid
            state {
                __typename
            }
        }
    }
}
"""

MODULE_INSTALLED_ENTITIES = """
query ModuleInstalledEntities($id: String!) {
    apollo {
        environmentById(id: $id) {
            entities(pageSize: 200) {
                entities {
                    displayName
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    product { productId }
                    installedByModuleV2 { rid }
                }
            }
        }
    }
}
"""

UPDATE_MODULE_INSTALLATION = """
mutation UpdateModuleInstallation(
    $moduleInstallationRid: RID!
    $update: UpdateApolloProductModuleInstallationInputV2!
) {
    apollo {
        updateModuleInstallationV2(moduleInstallationRid: $moduleInstallationRid, update: $update) {
            rid
            displayName
            state {
                __typename
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Secret management mutations
# ---------------------------------------------------------------------------

CREATE_SECRET = """
mutation CreateSecrets($entityId: String!, $secrets: [ApolloCreateSecretRequest_Input!]!) {
    apollo {
        createSecrets(apolloEntityId: $entityId, secrets: $secrets)
    }
}
"""

UPDATE_SECRET = """
mutation UpdateSecrets($entityId: String!, $secrets: [ApolloUpdateSecretRequest_Input!]!) {
    apollo {
        updateSecretsByEntityId(apolloEntityId: $entityId, secrets: $secrets)
    }
}
"""

ENTITY_SECRETS = """
query EntitySecrets($id: String!) {
    apollo {
        environmentById(id: $id) {
            entities(pageSize: 200) {
                entities {
                    id
                    rid
                    displayName
                    entityLocator {
                        ... on ApolloEntityLocator_ApolloEntity { entityName }
                    }
                    secrets {
                        rid
                        name
                        specification {
                            ... on ApolloSecretSpecification_MultiKey {
                                keys { key }
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Product creation
# ---------------------------------------------------------------------------

CREATE_PRODUCT = """
mutation CreateProduct($productId: String!) {
    apollo {
        createProduct(productId: $productId) {
            ... on ApolloProduct { productId }
            ... on ApolloProductAlreadyExists { dummy }
        }
    }
}
"""

CREATE_PRODUCT_RELEASE_FROM_MANIFEST = """
mutation CreateProductRelease($productReleaseManifest: String!) {
    apollo {
        createProductReleaseFromManifestV2(productReleaseManifest: $productReleaseManifest) {
            ... on ApolloProductRelease {
                rid
                mavenCoordinate
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Product queries
# ---------------------------------------------------------------------------

LIST_PRODUCTS = """
query ListProducts($pageSize: Int!, $pageToken: String) {
    apollo {
        products(pageSize: $pageSize, pageToken: $pageToken) {
            products {
                productId
                labels {
                    labelId
                    labelValue
                }
            }
            nextPageToken
        }
    }
}
"""

GET_PRODUCT_RELEASES = """
query ProductReleases($productId: String!, $pageSize: Int!) {
    apollo {
        productByProductIdV2(productId: $productId) {
            productReleases(pageSize: $pageSize) {
                productReleases {
                    rid
                    mavenCoordinate
                    releaseChannels {
                        name
                    }
                }
                nextPageToken
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Release channel queries
# ---------------------------------------------------------------------------

LIST_RELEASE_CHANNELS = """
query ListReleaseChannels {
    apollo {
        productReleases(pageSize: 200) {
            productReleases {
                releaseChannels {
                    rid
                    name
                    metadata {
                        description
                        type
                    }
                }
            }
        }
    }
}
"""

ADD_TO_RELEASE_CHANNEL = """
mutation AddToChannel($releaseRid: RID!, $channelNames: [String!]!, $rationale: String!) {
    apollo {
        addProductReleaseToChannels(
            rid: $releaseRid,
            releaseChannelIds: $channelNames,
            rationale: $rationale
        ) {
            rid
            mavenCoordinate
            releaseChannels {
                name
            }
        }
    }
}
"""

REMOVE_FROM_RELEASE_CHANNEL = """
mutation RemoveFromChannel($releaseRid: RID!, $channelNames: [String!]!, $rationale: String!) {
    apollo {
        deleteProductReleaseFromChannels(
            rid: $releaseRid,
            releaseChannels: $channelNames,
            rationale: $rationale
        ) {
            rid
            mavenCoordinate
            releaseChannels {
                name
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Product label mutations
# ---------------------------------------------------------------------------

SET_LABEL = """
mutation SetLabel($productId: String!, $labelId: String!, $labelValue: String!) {
    apollo {
        setLabelOnProduct(productId: $productId, labelId: $labelId, labelValue: $labelValue) {
            productId
            labels {
                labelId
                labelValue
            }
        }
    }
}
"""

REMOVE_LABEL = """
mutation RemoveLabel($productId: String!, $labelId: String!) {
    apollo {
        removeLabelFromProduct(productId: $productId, labelId: $labelId) {
            productId
            labels {
                labelId
                labelValue
            }
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Change request queries
# ---------------------------------------------------------------------------

LIST_CHANGE_REQUESTS = """
query ListCRs($pageSize: Int!) {
    apollo {
        changeRequests(pageSize: $pageSize) {
            changeRequests {
                rid
                title
                requestStatus
                createdAt
                environment {
                    name
                }
            }
            nextPageToken
        }
    }
}
"""

LIST_CHANGE_REQUESTS_BY_ENV = """
query ListCRsByEnv($envId: String!, $pageSize: Int!) {
    apollo {
        environmentById(id: $envId) {
            changeRequests(pageSize: $pageSize) {
                changeRequests {
                    rid
                    title
                    requestStatus
                    createdAt
                }
                nextPageToken
            }
        }
    }
}
"""

APPROVE_CHANGE_REQUEST = """
mutation ApproveCR($rid: RID!, $comment: String) {
    apollo {
        approveChangeRequest(rid: $rid, comment: $comment) {
            rid
            requestStatus
        }
    }
}
"""

REJECT_CHANGE_REQUEST = """
mutation RejectCR($rid: RID!, $comment: String!) {
    apollo {
        rejectChangeRequest(rid: $rid, comment: $comment) {
            rid
            requestStatus
        }
    }
}
"""

CANCEL_CHANGE_REQUEST = """
mutation CancelCR($rid: RID!) {
    apollo {
        cancelChangeRequest(rid: $rid) {
            rid
            requestStatus
        }
    }
}
"""

# ---------------------------------------------------------------------------
# Plan interruption (cancel active plan)
# ---------------------------------------------------------------------------

DELETE_AGENT = """
mutation DeleteAgent($envId: String!, $agentId: String!, $options: ApolloAgentDeletionOptionsInput!) {
    apollo {
        deleteAgentById(apolloEnvironmentId: $envId, agentId: $agentId, options: $options)
    }
}
"""
