"""Entity health and plan details tools."""

from __future__ import annotations

import asyncio

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common import apollo_queries as Q
from cube_common.apollo_models import format_entity_health, format_plan_details

from cube_cloud.tools import health_checks
from cube_cloud.tools.environments import _resolve_environment, withholds_config
from cube_cloud.tools.health_checks import format_entity_health_checks


async def entity_health(
    client: ApolloClient, environment: str, entity_id: str | None = None,
    *, protected: frozenset[str] | None = None,
) -> str:
    """Health, config and recent plans of an environment's entities.

    ``protected`` is the caller's `expose.protected_module_bases`: for a scoped
    caller, the config of a Teleport app service is withheld (`withholds_config`).
    """
    env_info = await _resolve_environment(client, environment)
    environment_id = env_info["id"]
    env_name = env_info.get("name", environment)

    data = await client.graphql(Q.ENVIRONMENT_ENTITIES, {"id": environment_id})
    env = data.get("apollo", {}).get("environmentById")
    if not env:
        return f"Environment not found: {environment_id}"

    all_entities = env.get("entities", {}).get("entities", [])
    if not all_entities:
        return f"No entities found in environment: {env.get('name', env_name)}"

    if entity_id:
        search = entity_id.lower()
        matched = [
            e for e in all_entities
            if search in (e.get("displayName") or e.get("id") or "").lower()
        ]
        if not matched:
            names = [e.get("displayName") or e.get("id") for e in all_entities]
            return (
                f"Entity '{entity_id}' not found. Available entities:\n"
                + "\n".join(f"  - {n}" for n in names)
            )
        entities = matched
    else:
        entities = all_entities

    checks, skipped = await _health_checks_for(
        client, environment_id, entities, filtered=bool(entity_id)
    )

    lines = [f"Entity Health: {env.get('name', env_name)}", "=" * 50]
    lines.append(f"{len(entities)} entit{'y' if len(entities) == 1 else 'ies'}\n")

    for entity in entities:
        result = checks.get(entity.get("id") or "")
        lines.extend(format_entity_health(
            entity,
            format_entity_health_checks(result, _health_of(entity)) if result else None,
            withhold_config=withholds_config(entity, protected),
        ))
        lines.append("")

    if skipped:
        lines.append(
            f"Health checks were not fetched for {skipped} more unhealthy "
            f"entit{'y' if skipped == 1 else 'ies'}; pass entity_id to see them."
        )

    return "\n".join(lines)


# How many entities one `entity_health` call drills into, and how many at once. A
# cube-wide outage can make most of a 45-entity cube unhealthy; each drill is one
# ~0.2s Apollo read, so this bounds the call rather than the cube.
MAX_HEALTH_CHECK_DRILLS = 25
HEALTH_CHECK_CONCURRENCY = 8


def _health_of(entity: dict) -> str:
    return ((entity.get("reportedStatus") or {}).get("healthStatus")) or ""


async def _health_checks_for(
    client: ApolloClient, environment_id: str, entities: list[dict], *, filtered: bool
) -> tuple[dict[str, health_checks.EntityHealthChecks], int]:
    """Health checks for the entities worth explaining, keyed by entity id.

    Unfiltered, that is every entity whose health is reported and not HEALTHY — the
    "why is this in Error" case. Filtered with `entity_id`, it is every match,
    healthy ones included, because naming an entity is asking about it. Ids come
    from `environment_id`'s own entity list, which `_resolve_environment` already
    authorized; `fetch_entity_health_checks` re-checks the environment besides.
    """
    wanted = [
        e for e in entities
        if e.get("id") and (filtered or _health_of(e) not in ("", health_checks.HEALTHY))
    ]
    drilled, skipped = wanted[:MAX_HEALTH_CHECK_DRILLS], max(0, len(wanted) - MAX_HEALTH_CHECK_DRILLS)
    sem = asyncio.Semaphore(HEALTH_CHECK_CONCURRENCY)

    async def one(entity: dict) -> tuple[str, health_checks.EntityHealthChecks]:
        async with sem:
            return entity["id"], await health_checks.fetch_entity_health_checks(
                client, environment_id, entity["id"]
            )

    return dict(await asyncio.gather(*(one(e) for e in drilled))), skipped


async def plan_details(
    client: ApolloClient,
    environment: str,
    entity_name: str,
    plan_index: int = 0,
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    data = await client.graphql(Q.PLAN_DETAILS, {"id": env_id})
    env = data.get("apollo", {}).get("environmentById")
    if not env:
        return f"Environment not found: {env_id}"

    all_entities = env.get("entities", {}).get("entities", [])
    if not all_entities:
        return f"No entities in environment: {env_name}"

    search = entity_name.lower()
    matched = [
        e for e in all_entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if not matched:
        names = sorted(set(
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "") or e.get("id", "")
            for e in all_entities
        ))
        return (
            f"Entity '{entity_name}' not found in {env_name}.\n\n"
            f"Available entities:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if len(matched) > 1:
        exact = [
            e for e in matched
            if (e.get("displayName") or "").lower() == search
            or ((e.get("entityLocator") or {}).get("entityName") or "").lower() == search
        ]
        if len(exact) == 1:
            matched = exact
        else:
            names = [e.get("displayName") or e.get("id") for e in matched]
            return (
                f"Multiple entities match '{entity_name}':\n"
                + "\n".join(f"  - {n}" for n in names)
                + "\n\nPlease be more specific."
            )

    return format_plan_details(matched[0], env_name, plan_index)


async def cancel_active_plan(
    client: ApolloClient,
    environment: str,
    entity_name: str,
) -> str:
    """Cancel (interrupt) the active plan for an entity.

    Finds the entity's most recent ACTIVE plan, extracts the agent running it,
    and calls deleteAgentById with interruptActivePlans=true and
    removeReportedEntities=false. The agent re-registers automatically on
    its next heartbeat and Apollo creates new plans as needed.
    """
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    data = await client.graphql(Q.PLAN_DETAILS, {"id": env_id})
    env = data.get("apollo", {}).get("environmentById")
    if not env:
        return f"Environment not found: {env_id}"

    all_entities = env.get("entities", {}).get("entities", [])
    if not all_entities:
        return f"No entities in environment: {env_name}"

    search = entity_name.lower()
    matched = [
        e for e in all_entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if not matched:
        names = sorted(set(
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "") or e.get("id", "")
            for e in all_entities
        ))
        return (
            f"Entity '{entity_name}' not found in {env_name}.\n\n"
            f"Available entities:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if len(matched) > 1:
        exact = [
            e for e in matched
            if (e.get("displayName") or "").lower() == search
            or ((e.get("entityLocator") or {}).get("entityName") or "").lower() == search
        ]
        if len(exact) == 1:
            matched = exact
        else:
            names = [e.get("displayName") or e.get("id") for e in matched]
            return (
                f"Multiple entities match '{entity_name}':\n"
                + "\n".join(f"  - {n}" for n in names)
                + "\n\nPlease be more specific."
            )

    entity = matched[0]
    ename = entity.get("displayName") or entity.get("id", "unknown")
    plans = (entity.get("nonGenericPlans") or {}).get("plans", [])

    # Find the most recent active plan
    active_plan = None
    for plan in plans:
        status_type = (plan.get("status") or {}).get("type", "")
        if status_type in ("ACTIVE", "PENDING_INTERRUPTION"):
            active_plan = plan
            break

    if not active_plan:
        return f"No active plan found for entity '{ename}' in {env_name}."

    agent_id = active_plan.get("agentId")
    if not agent_id:
        return f"Active plan for '{ename}' has no agent ID — cannot interrupt."

    plan_rid = active_plan.get("rid", "unknown")

    await client.graphql(Q.DELETE_AGENT, {
        "envId": env_id,
        "agentId": agent_id,
        "options": {
            "interruptActivePlans": True,
            "removeReportedEntities": False,
        },
    })

    return (
        f"Active plan interrupted for '{ename}' in {env_name}.\n\n"
        f"  Plan RID:  {plan_rid}\n"
        f"  Agent ID:  {agent_id}\n"
        f"  Action:    Agent deleted with interruptActivePlans=true, "
        f"removeReportedEntities=false\n\n"
        f"The agent will re-register automatically on next heartbeat. "
        f"Use plan_details to verify the plan was interrupted."
    )
