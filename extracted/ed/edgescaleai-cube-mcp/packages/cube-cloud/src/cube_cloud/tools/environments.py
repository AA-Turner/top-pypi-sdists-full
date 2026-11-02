"""Apollo environment management tools: list, create, replicate, install_entity."""

from __future__ import annotations

import json

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common.apollo_pagination import fetch_all_environments
from cube_common import apollo_queries as Q
from cube_common import entity_config
from cube_common.apollo_models import CONFIG_WITHHELD, module_label, module_manager

# RBAC helpers now live in auth/apollo_rbac.py so the Groundcover tools share one
# copy. Re-exported under their original private names for backward compat.
from cube_cloud.auth.apollo_rbac import (
    get_user_team_names as _get_user_team_names,
    has_environment_access as _has_environment_access,
)


# Appended to a "not found" error when the environment list we searched was
# itself incomplete. Without it the message is confidently wrong in exactly the
# case where it is most misleading: it blames the name, and then sends the caller
# to `list_environments`, which is drained by the same code and would have shown
# the same gap. An agent relays that to a user as "there is no such cube".
#
# No issue number here, and none in the tool WARNING below. Both strings are
# relayed to a user in our voice, and an internal tracker id is not something they
# can act on — the pointer belongs in the log line beside it, which is where
# someone diagnosing this will actually be.
_TRUNCATED_HINT = (
    " NOTE: the environment list could not be read completely, so this name may "
    "belong to a cube that was not fetched rather than to no cube at all."
)


# The warning every module-managed config write carries: in the refusal, in the
# `force` parameter's schema description (proxy_tools.py), and in the response when
# `force=true` was used. Apollo's entity-level config takes precedence over the
# module's render, so a hand-written config freezes the entity at what was written:
# jacanda-orin-agx-nanocube lost its `cube` Teleport label for six weeks that way.
MODULE_OVERRIDE_WARNING = (
    "Overriding a module-managed entity's config is for BREAK-GLASS situations only: "
    "the entity-level config then takes precedence over the module, so later module "
    "changes silently stop applying to this entity until the entity-level config is "
    "removed."
)


def _module_refusal(tool: str, display: str, env_name: str, module: dict) -> str:
    """The pre-write refusal for a module-managed entity. Nothing has been written."""
    return (
        f"{tool} refused: {display} on {env_name} is managed by module "
        f"{module_label(module)}. Its config is the module's render; change it with "
        "update_module_variables on that module (list_modules shows its variables). "
        f"{MODULE_OVERRIDE_WARNING} Nothing was written. Re-run with force=true only "
        "if the module path cannot fix the problem."
    )


def _forced_warning(module: dict) -> str:
    return (
        f"  WARNING: force=true overrode the config of an entity managed by module "
        f"{module_label(module)}. {MODULE_OVERRIDE_WARNING}"
    )


# Teleport app-service products. Their config's `apps` key is every company's app
# list on the cube (verified 2026-10-20 on cube-66odzn95 and cube-9likqvpd, module-
# managed, and lear-flint-1, a legacy hand-managed one: all block YAML). The esai
# product is what `teleport-multi-app-service-module` installs.
TELEPORT_APP_SERVICE_PRODUCTS = frozenset({
    "com.teleport:teleport-app-service",
    "com.edgescaleai-cube:esai-teleport-app-service",
})


def withholds_config(entity: dict, protected: frozenset[str] | None) -> bool:
    """Whether a caller with ``protected`` (`expose.protected_module_bases`) may NOT
    read ``entity``'s config.

    The fifth exit for the multi-app module's `apps` list, contained the way
    `list_modules` contains it: a scoped caller (``protected`` set) never sees the
    config of an entity that a protected module manages, nor of any Teleport
    app-service entity (a legacy one carries the same list with no module behind it).
    An unscoped admin (``protected`` None) keeps full fidelity.
    """
    if protected is None:
        return False
    from cube_cloud.tools.modules import is_protected

    module = module_manager(entity)
    if module and is_protected(module.get("moduleMavenCoordinate"), protected):
        return True
    return ((entity.get("product") or {}).get("productId") or "") in TELEPORT_APP_SERVICE_PRODUCTS


def _parse_overrides(config_overrides: str) -> tuple[dict | None, str]:
    """``config_overrides`` (a JSON object) -> (overrides, "") or (None, error)."""
    try:
        overrides = json.loads(config_overrides)
    except json.JSONDecodeError:
        return None, f"Error: config_overrides must be valid JSON. Got: {config_overrides[:200]}"
    if not isinstance(overrides, dict):
        return None, "Error: config_overrides must be a JSON object of Helm value overrides."
    masked = entity_config.masked_paths(overrides)
    if masked:
        return None, (
            f"Error: refusing to write masked placeholder value(s) at: {', '.join(masked)}. "
            "That text is what entity_health shows INSTEAD of a secret; this write replaces "
            "the whole config, so it would store the placeholder as the real value. "
            "Supply the real value."
        )
    return overrides, ""


async def _resolve_environment(client: ApolloClient, name_or_rid: str) -> dict:
    """Resolve an environment name or RID to {id, rid, name}.

    Raises ApolloError if not found, ambiguous, or the caller lacks access.

    The name path drains every page (issue 252 / OI-6). This function backs every
    MCP tool that takes a cube name, so a short read here did not merely hide a
    cube — it made every tool on that cube answer "no such environment".
    """
    if "ri." in name_or_rid:
        data = await client.graphql(Q.GET_ENVIRONMENT_BY_RID, {"rid": name_or_rid})
        env = data.get("apollo", {}).get("environment")
        if not env:
            raise ApolloError(f"Environment not found: {name_or_rid}")
    else:
        result = await fetch_all_environments(client, Q.LIST_ENVIRONMENTS)
        envs = result.items
        search = name_or_rid.lower()

        env = None
        for e in envs:
            if e.get("name", "").lower() == search:
                env = e
                break

        if env is None:
            matches = [e for e in envs if search in e.get("name", "").lower()]
            if len(matches) == 1:
                env = matches[0]
            elif len(matches) == 0:
                raise ApolloError(
                    f"No environment found matching '{name_or_rid}'. Use list_environments to see available names."
                    + (_TRUNCATED_HINT if result.truncated else "")
                )
            else:
                names = [f"  - {m['name']}" for m in matches[:10]]
                raise ApolloError(
                    f"Multiple environments match '{name_or_rid}':\n" + "\n".join(names) + "\n\nPlease be more specific."
                )

    # RBAC check: verify the caller's team has a role on this environment
    user_teams = await _get_user_team_names(client)
    if not _has_environment_access(env, user_teams):
        raise ApolloError(
            f"Access denied: your account does not have a role on environment "
            f"'{env.get('name')}'.\nUse list_environments to see environments you have access to."
        )
    return env


async def list_environments(client: ApolloClient, search: str | None = None) -> str:
    result = await fetch_all_environments(client, Q.LIST_ENVIRONMENTS)
    envs = result.items

    # RBAC filtering: only show environments where the user's team has a role
    user_teams = await _get_user_team_names(client)
    envs = [e for e in envs if _has_environment_access(e, user_teams)]

    if search:
        search_lower = search.lower()
        envs = [e for e in envs if search_lower in e.get("name", "").lower()]

    # An incomplete list is stated in the OUTPUT, not just logged. This tool's
    # whole job is to answer "what can I see", and an agent reading a short list
    # has no other way to tell it is short — it would report the absence as fact.
    # Said on the empty path too, where it is the more useful of the two: "no
    # environments found" is the answer most likely to be taken at face value.
    #
    # FIRST line, not last: appended after a couple of hundred rows it qualifies a
    # count the reader has already passed, and the count is the thing it corrects.
    warning = (
        "WARNING: this list is INCOMPLETE — the environment list could not be read "
        "completely, so environments may be missing.\n"
        if result.truncated else ""
    )

    if not envs:
        suffix = f' matching "{search}"' if search else ""
        return f"{warning}No environments found{suffix}."

    lines = [f"Apollo Environments ({len(envs)})", "=" * 60]
    for env in sorted(envs, key=lambda e: e.get("name", "")):
        name = env.get("name", "unknown")
        rid = env.get("rid", "")
        ns = env.get("namespaceId", "")
        lines.append(f"  {name}")
        lines.append(f"    RID: {rid}")
        if ns:
            lines.append(f"    Namespace: {ns}")

    return warning + "\n".join(lines)


async def uninstall_entity(
    client: ApolloClient, environment: str, entity_name: str
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    data = await client.graphql(Q.ENTITY_BY_NAME, {"id": env_id})
    entities = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("entities", {})
        .get("entities", [])
    )

    search = entity_name.lower()
    matched = [
        e for e in entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if not matched:
        names = [
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "?")
            for e in entities
        ]
        return (
            f"Entity '{entity_name}' not found in {env_name}.\n"
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
            names = [e.get("displayName") or "?" for e in matched]
            return (
                f"Multiple entities match '{entity_name}':\n"
                + "\n".join(f"  - {n}" for n in names)
                + "\n\nPlease be more specific."
            )

    entity = matched[0]
    entity_rid = entity["rid"]
    entity_id = entity["id"]
    display = (
        entity.get("displayName")
        or (entity.get("entityLocator") or {}).get("entityName", "?")
    )

    uninstall_data = await client.graphql(
        Q.UNINSTALL_ENTITY,
        {"namespaceId": env_info.get("namespaceId"), "entityId": entity_id},
    )
    cr = uninstall_data.get("apollo", {}).get("uninstallEntityV2", {})

    return (
        f"Entity uninstall requested: {display} on {env_name}\n"
        f"  RID:    {entity_rid}\n"
        f"  Status: {cr.get('requestStatus', '?')}\n"
        f"  CR RID: {cr.get('rid', '')}"
    )


async def update_entity_config(
    client: ApolloClient, environment: str, entity_name: str, config_overrides: str,
    version: str | None = None, force: bool = False,
    *, protected: frozenset[str] | None = None,
) -> str:
    """Replace an entity's config overrides with ``config_overrides``.

    A full replace, written as block YAML. Refuses a module-managed entity unless
    ``force`` is True: see `MODULE_OVERRIDE_WARNING`. Every refusal returns before
    the mutation, so it writes nothing. ``protected`` (the caller's
    `expose.protected_module_bases`) decides whether the previous config may be
    echoed back (`withholds_config`).
    """
    overrides, error = _parse_overrides(config_overrides)
    if error:
        return error
    if version is not None and not entity_config.valid_version(version):
        return f"Error: version must look like a release version (e.g. 4.11.3). Got: {version[:100]}"

    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)
    namespace_id = env_info.get("namespaceId")

    data = await client.graphql(Q.ENTITY_BY_NAME, {"id": env_id})
    entities = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("entities", {})
        .get("entities", [])
    )

    search = entity_name.lower()
    matched = [
        e for e in entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if not matched:
        names = [
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "?")
            for e in entities
        ]
        return (
            f"Entity '{entity_name}' not found in {env_name}.\n"
            f"Available entities:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if len(matched) > 1:
        exact = [
            e for e in matched
            if (e.get("displayName") or "").lower() == search
            or ((e.get("entityLocator") or {}).get("entityName") or "").lower() == search
        ]
        matched = exact if len(exact) == 1 else matched
    if len(matched) > 1:
        names = [e.get("displayName") or "?" for e in matched]
        return (
            f"Multiple entities match '{entity_name}':\n"
            + "\n".join(f"  - {n}" for n in names)
            + "\n\nPlease be more specific."
        )

    entity = matched[0]
    entity_id = entity["id"]
    display = (
        entity.get("displayName")
        or (entity.get("entityLocator") or {}).get("entityName", "?")
    )

    module = module_manager(entity)
    if module and not force:
        return _module_refusal("update_entity_config", display, env_name, module)

    # Get spaceId from the environment (returned by ENTITY_BY_NAME query)
    space_id = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("spaceId")
    )

    # Determine version for the config override block
    reported_status = entity.get("reportedStatus") or {}
    config_version = version or reported_status.get("version") or "0.0.0"
    if not entity_config.valid_version(config_version):
        return (
            f"Error: the entity's reported version ({config_version[:100]}) cannot be "
            "used as a config block version; pass version explicitly."
        )
    version_warning = ""
    if not version and not reported_status.get("version"):
        version_warning = (
            "\n  Warning: No reported version found, using 0.0.0."
            " Apollo requires a version matching the target release."
            " Use get_product_releases to find the correct version,"
            " then re-run with version param."
        )

    # Previous declared config, for context. Parsed as YAML, which reads the block
    # form modules and the Apollo UI write as well as the JSON form this tool used
    # to write; shown masked, like entity_health.
    prev_blocks: list[entity_config.ConfigBlock] = []
    for cfg_str in (entity.get("declaredState") or {}).get("config") or []:
        prev_blocks = entity_config.parse_config(cfg_str)
        if prev_blocks:
            break

    config_str = entity_config.render_block(config_version, overrides)
    update: dict = {
        "type": {"entity": {"apolloEntityId": entity_id}},
        "content": config_str,
    }
    if namespace_id:
        update["namespaceId"] = namespace_id

    # Surface pre-existing config issues
    config_status = reported_status.get("configStatus", "")
    blocker_types = reported_status.get("upgradeBlockerTypes") or []
    blocker_warning = ""
    if blocker_types:
        blocker_warning = f"\n  Warning: Entity has upgrade blockers: {', '.join(blocker_types)}"

    result_data = await client.graphql(
        Q.UPDATE_ENTITY_CONFIG,
        {"spaceId": space_id, "update": update},
    )
    cr = result_data.get("apollo", {}).get("updateConfigByResource", {})

    # Check plan status for blocking info
    plan_status = entity.get("planStatus") or {}
    plan_typename = plan_status.get("__typename", "")
    is_blocked = "Blocked" in plan_typename
    blocked_count = plan_status.get("blockedChangesCount")

    lines = [
        f"Config updated: {display} on {env_name}",
        f"  Version: {config_version}",
        f"  Status:  {cr.get('requestStatus', '?')}",
        f"  CR RID:  {cr.get('rid', '')}",
    ]
    if module:
        lines.append(_forced_warning(module))
    withheld = withholds_config(entity, protected)
    for block in prev_blocks:
        lines.append(f"  Previous config version: {block.version}")
        if withheld:
            lines.append(f"  Previous overrides: {CONFIG_WITHHELD}")
        elif not block.readable:
            lines.append("  Previous overrides: (could not be parsed; not shown)")
        else:
            lines.append("  Previous overrides (secret-named values hidden):")
            lines.extend(f"    {ol}" for ol in entity_config.display_lines(block.overrides))
    if config_status:
        lines.append(f"  Config status: {config_status}")
    if is_blocked:
        lines.append(f"  Plan was blocked ({blocked_count} constraint{'s' if (blocked_count or 0) > 1 else ''})")
    if blocker_warning:
        lines.append(blocker_warning)
    if version_warning:
        lines.append(version_warning)

    return "\n".join(lines)


async def enforce_entity_config(
    client: ApolloClient, environment: str, entity_name: str
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    data = await client.graphql(Q.ENTITY_BY_NAME, {"id": env_id})
    entities = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("entities", {})
        .get("entities", [])
    )

    search = entity_name.lower()
    matched = [
        e for e in entities
        if search in (e.get("displayName") or "").lower()
        or search in ((e.get("entityLocator") or {}).get("entityName") or "").lower()
    ]

    if not matched:
        names = [
            e.get("displayName") or (e.get("entityLocator") or {}).get("entityName", "?")
            for e in entities
        ]
        return (
            f"Entity '{entity_name}' not found in {env_name}.\n"
            f"Available entities:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if len(matched) > 1:
        exact = [
            e for e in matched
            if (e.get("displayName") or "").lower() == search
            or ((e.get("entityLocator") or {}).get("entityName") or "").lower() == search
        ]
        matched = exact if len(exact) == 1 else matched
    if len(matched) > 1:
        names = [e.get("displayName") or "?" for e in matched]
        return (
            f"Multiple entities match '{entity_name}':\n"
            + "\n".join(f"  - {n}" for n in names)
            + "\n\nPlease be more specific."
        )

    entity = matched[0]
    entity_rid = entity["rid"]
    display = (
        entity.get("displayName")
        or (entity.get("entityLocator") or {}).get("entityName", "?")
    )

    result_data = await client.graphql(
        Q.ENFORCE_ENTITY_CONFIG, {"rid": entity_rid}
    )
    cr = result_data.get("apollo", {}).get("enforceEntityConfig", {})

    # Surface config validation info
    reported_status = entity.get("reportedStatus") or {}
    config_status = reported_status.get("configStatus", "")
    blocker_types = reported_status.get("upgradeBlockerTypes") or []

    lines = [
        f"Config enforcement requested: {display} on {env_name}",
        f"  Status: {cr.get('requestStatus', '?')}",
        f"  CR RID: {cr.get('rid', '')}",
    ]
    if config_status:
        lines.append(f"  Config status: {config_status}")
    if blocker_types:
        lines.append(f"  Warning: Entity has upgrade blockers: {', '.join(blocker_types)}")

    return "\n".join(lines)


async def install_entity(
    client: ApolloClient,
    environment: str,
    entity_name: str,
    product_id: str,
    k8s_namespace: str = "default",
    config_overrides: str | None = None,
    version: str | None = None,
    force: bool = False,
) -> str:
    """Install a Helm chart entity, with its config written as block YAML.

    Refuses, unless ``force``, when an entity of the same name on the environment is
    module-managed: whether Apollo treats this install as an update of that entity's
    config is not verified, and if it does, it is the same override
    `update_entity_config` refuses. Every refusal returns before the mutation.
    """
    config_version = version or "0.0.0"
    if not entity_config.valid_version(config_version):
        return f"Error: version must look like a release version (e.g. 4.11.3). Got: {config_version[:100]}"
    overrides: dict = {}
    if config_overrides:
        overrides, error = _parse_overrides(config_overrides)
        if error:
            return error

    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    existing = await client.graphql(Q.ENTITY_BY_NAME, {"id": env_id})
    same_name = [
        e for e in (
            existing.get("apollo", {}).get("environmentById", {})
            .get("entities", {}).get("entities", [])
        )
        if ((e.get("entityLocator") or {}).get("entityName") or "") == entity_name
    ]
    module = next((m for m in map(module_manager, same_name) if m), None)
    if module and not force:
        return _module_refusal("install_entity", entity_name, env_name, module)

    optional: dict = {"configOverrides": entity_config.render_block(config_version, overrides)}

    helm_chart = {
        "helmChartName": entity_name,
        "productId": product_id,
        "k8sNamespace": k8s_namespace,
        "entityInstallationOptionalInputs": optional,
    }

    try:
        data = await client.graphql(Q.INSTALL_ENTITIES, {
            "envId": env_id,
            "namespaceId": env_info.get("namespaceId"),
            "entities": {"helmCharts": [helm_chart]},
        })
    except ApolloError as e:
        error_msg = str(e)
        lines = [
            f"Error installing entity '{entity_name}' on {env_name}",
            "=" * 50,
            f"  Product:   {product_id}",
            f"  Namespace: {k8s_namespace}",
            "",
            f"  Error: {error_msg}",
            "",
            "Troubleshooting:",
            "  1. Verify the product has a published release:",
            f"     Use get_product_releases(product_id=\"{product_id}\")",
            "  2. Verify the release is on a release channel (e.g., DEV):",
            f"     Use get_product_releases(product_id=\"{product_id}\") to check channel membership "
            "(Apollo adds newly published releases to DEV automatically).",
            "  3. Check the environment has an agent connected:",
            f"     Use entity_health(environment=\"{env_name}\")",
        ]
        return "\n".join(lines)

    cr = data.get("apollo", {}).get("installEntitiesOnEnvironmentV2", {})
    lines = [
        f"Entity installed on {env_name}",
        "=" * 50,
        f"  Entity:          {entity_name}",
        f"  Product:         {product_id}",
        f"  Namespace:       {k8s_namespace}",
        f"  Config:          {'custom overrides' if config_overrides else 'none'}",
        "",
        f"  Change Request:  {cr.get('requestStatus', '?')}",
        f"  CR RID:          {cr.get('rid', '')}",
    ]
    if module:
        lines.append(_forced_warning(module))

    return "\n".join(lines)
