"""Module management tools."""

from __future__ import annotations

import json

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_common import apollo_queries as Q
from cube_common import secret_names

from cube_cloud.tools.environments import _resolve_environment


async def _fetch_module_installations(client: ApolloClient, env_id: str) -> list:
    """Raw moduleInstallations list for an environment (LIST_MODULES, unwrapped)."""
    data = await client.graphql(Q.LIST_MODULES, {"id": env_id})
    return (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("moduleInstallationsV2", {})
        .get("moduleInstallations", [])
    )


def _variable_string(value: object) -> str:
    """Serialize a module-variable value to the string Apollo stores.

    Apollo module variables are always strings (there is no native list/bool
    type), so a caller's structured value has to be flattened to text. Use
    `json.dumps` for anything that isn't already a string — NOT `str()`.

    `str()` emits a Python **repr**, which for a list/dict means single-quoted
    keys: `[{'name': 'litellm-cube-66odzn95', ...}]`. That is not JSON, so
    whatever later reads the variable back can never parse it. This is exactly
    how `cube-66odzn95`'s Teleport multi-app `apps` variable was corrupted,
    which blocked `expose`/`unexpose`/`list_exposed` on that cube (the read
    side refuses to guess — see `tools/expose.py::_load_apps`).

    A value that is already a string passes through untouched: `expose` hands
    us pre-serialized JSON text under the `apps` key on purpose, and
    re-dumping it would double-encode.
    """
    if isinstance(value, str):
        return value
    return json.dumps(value)


def module_base_coordinate(coordinate: str) -> str:
    """Strip the trailing `:version` segment, e.g.
    'module:teleport-multi-app-service-module:0.2.0' -> 'module:teleport-multi-app-service-module'.

    Public because `tools/teleport_status.py` matches version-free base coordinates
    directly rather than through `_find_module_by_coordinate` — see the comment on
    `TELEPORT_AGENT_MODULE_COORDINATES` for why that helper is the wrong tool there.
    """
    return coordinate.rsplit(":", 1)[0]


def is_protected(coordinate: str | None, protected: frozenset[str] | None) -> bool:
    """Whether ``coordinate`` names a module in ``protected`` (a set of BASE coordinates).

    Matched against the base itself or the base plus a ``:version``, case-insensitively,
    rather than through `module_base_coordinate`: that strips the last segment WHATEVER
    it is, so a version-free coordinate a caller typed (`install_module` checks the
    caller's own string) lost its last word and slipped past the guard.
    """
    coord = (coordinate or "").strip().lower()
    return bool(protected) and any(
        coord == base.lower() or coord.startswith(base.lower() + ":") for base in protected
    )


def protected_refusal(coordinate: str, env_name: str, protected: frozenset[str] | None) -> str | None:
    """Refusal when a generic module tool targets a module the caller may not touch.

    ``protected`` is a set of BASE coordinates (`module_base_coordinate`) that only the
    dispatch layer passes, and only for a scoped profile: today just the Teleport
    multi-app module, whose `apps` variable holds every company's exposed apps on the
    cube. Writing it here would bypass every app-company rule in `tools/expose.py`
    (any label, any target) and uninstalling it takes down every company's apps. The
    internal calls `expose`/`unexpose` make pass nothing, so they are unaffected.
    """
    if is_protected(coordinate, protected):
        return (
            f"Refused: the Teleport multi-app module on {env_name} serves every company's "
            "exposed apps on this cube, so it is managed only through expose, unexpose and "
            "list_exposed. Use those tools instead."
        )
    return None


def module_variable(module: dict, name: str) -> str:
    """One module variable's value as a string, or "" when it is absent.

    **Never call this for a secret-named variable.** It returns the raw stored value
    with none of `_display_variable`'s name-based masking, so reading `authToken` here
    and putting it in a response or a log would hand out a live Teleport join token.
    Use `_display_variable` for anything that will be rendered.
    """
    for var in module.get("variables") or []:
        if not isinstance(var, dict) or var.get("variableName") != name:
            continue
        return str((var.get("variableValue") or {}).get("value") or "").strip()
    return ""


def _find_module_by_coordinate(installations: list, coordinate: str) -> dict | None:
    """Match a module installation by maven coordinate, ignoring version.

    Version-agnostic on purpose: if the configured coordinate's version is
    bumped (env var or code constant) after an environment already has the
    module installed at an older version, this must still find that existing
    installation so it gets updated in place rather than duplicated. Used by
    expose/unexpose (always looking for *the* well-known module name), unlike
    `_find_module`'s fuzzy substring search (built for human-driven tools that
    pass a free-text display-name/coordinate search string).
    """
    base = module_base_coordinate(coordinate)
    for m in installations:
        if module_base_coordinate(m.get("moduleMavenCoordinate") or "") == base:
            return m
    return None


# Which variable VALUES are never printed. The predicate (names, the never-secret
# allowlist, the userinfo-URL check and the mask shape) lives in
# `cube_common/secret_names.py`, because entity config renders the same credentials
# (`apollo_models.format_entity_health`) and must mask them by the same rule. The
# private aliases below keep this module's existing callers and tests unchanged.
_SECRET_VARIABLE_HINTS = secret_names.SECRET_NAME_HINTS
_NEVER_SECRET_VARIABLES = secret_names.NEVER_SECRET_NAMES
_URL_WITH_USERINFO_RE = secret_names.URL_WITH_USERINFO_RE
_is_secret_variable = secret_names.is_secret_name
_value_is_sensitive = secret_names.value_is_sensitive

# The exact shape `_display_variable` emits. Shared so the write-path guard below
# recognizes precisely what the read path produced — not a lookalike regex.
_MASK_RE = secret_names.MASK_RE

# Indent of one rendered variable line in `update_module_variables`' confirmation.
# Shared with `redact_variable_line` for the same reason `_MASK_RE` is shared: a
# caller redacting a line must match what this module actually emitted.
_VARIABLE_LINE_INDENT = "    "


def _variable_line(name: str, value: object) -> str:
    """One `    name = value` line of the changed-variables confirmation."""
    return f"{_VARIABLE_LINE_INDENT}{name} = {_display_variable(name, value)}"


def redact_variable_line(text: str, name: str, replacement: str) -> str:
    """Replace the rendered value of variable ``name`` in ``text``.

    For a variable whose VALUE is not secret by name but is still not fit to
    publish — the Teleport multi-app module's `apps`, which carries every app on
    the cube (other companies' names, internal URIs, and Teleport addresses)
    — the caller keeps the rest of the confirmation (including any failure text
    `update_module_variables` returns as a string rather than raising) and
    replaces just that one line. Containment lives at the calling boundary, not
    here, so `list_modules` stays the admin's full-fidelity view.

    Matching is anchored on `_variable_line`'s own indent + `name = ` prefix, so
    it cannot drift from what the renderer emits. Non-matching text is returned
    unchanged.
    """
    prefix = f"{_VARIABLE_LINE_INDENT}{name} = "
    return "\n".join(
        f"{prefix}{replacement}" if line.startswith(prefix) else line
        for line in text.split("\n")
    )


_is_masked_placeholder = secret_names.is_masked_placeholder


def _reject_masked(var_dict: dict) -> str:
    """Refuse a write that would store a MASK as a real value -> error or "".

    Masking created this hazard. `install_module` sends the COMPLETE variable set
    (not a merge), and `proxy_tools.py` tells agents to read current values first —
    so the documented re-install flow is: read `list_modules`, resend the set. With
    masking, `authToken` reads back as `<hidden, 32 chars>`, and `_variable_string`
    passes any string through untouched, so that literal would become the Teleport
    join token. The app-service pod rolls out, fails to rejoin, and EVERY exposed app
    on the cube goes dark.

    Refusing is the only safe answer: the real value is unrecoverable through the MCP
    surface by design, so the caller must omit the key (update merges and preserves
    it) or supply the true value from Secrets Manager.
    """
    masked = sorted(k for k, v in var_dict.items() if _is_masked_placeholder(v))
    if not masked:
        return ""
    names = ", ".join(masked)
    return (
        f"Error: refusing to write masked placeholder value(s) for: {names}. "
        "That text is what tool output shows INSTEAD of a secret — writing it back "
        "would replace the real value and break the module. Omit these keys "
        "(update_module_variables merges, so omitted keys keep their current values), "
        "or supply the real value."
    )


def _display_variable(name: str, value: object) -> str:
    """How a variable is shown in tool output. Secret-named values never appear.

    The length is reported so an operator can still tell "it was set" from "it was
    set to the empty string", which is the only diagnostic the value provided here.
    """
    if _is_secret_variable(name) or _value_is_sensitive(value):
        return secret_names.mask(value)
    return str(value)


async def list_modules(
    client: ApolloClient, environment: str, search: str | None = None,
    *, protected: frozenset[str] | None = None,
) -> str:
    """Every module installed on ``environment`` with its variables (secret-named ones masked).

    ``protected`` (a scoped caller's `expose.protected_module_bases`) withholds the
    shared multi-app module's `apps` value -- every company's app names, internal URIs
    and labels on the cube, the payload `expose`, `unexpose` and the console each keep
    from a scoped caller -- and its `company` value, the last company to expose there.
    `list_exposed` is the per-company view.
    """
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    modules = await _fetch_module_installations(client, env_id)

    if search:
        search_lower = search.lower()
        modules = [
            m for m in modules
            if search_lower in (m.get("displayName") or "").lower()
            or search_lower in (m.get("moduleMavenCoordinate") or "").lower()
        ]

    if not modules:
        suffix = f' matching "{search}"' if search else ""
        return f"No modules found on {env_name}{suffix}."

    lines = [f"Modules on {env_name} ({len(modules)})", "=" * 60]
    for m in modules:
        name = m.get("displayName") or "(unnamed)"
        coord = m.get("moduleMavenCoordinate", "?")
        rid = m.get("rid", "")
        state = (
            m.get("state", {})
            .get("__typename", "")
            .replace("ApolloProductModuleInstallationStateV2_", "")
        )
        variables = m.get("variables", [])

        lines.append(f"  {name}")
        lines.append(f"    Coordinate: {coord}")
        lines.append(f"    State:      {state}")
        lines.append(f"    RID:        {rid}")
        if variables:
            for v in variables:
                vname = v.get("variableName", "?")
                vval = v.get("variableValue", {}).get("value", "?")
                # Masked by NAME: the Teleport multi-app module carries a live
                # `authToken` join credential, so listing modules on any cube with an
                # exposed app was printing it.
                # `company` too: it holds whichever company exposed LAST on the cube, which
                # tells a scoped caller that another tenant exposes apps here, and when.
                if vname in ("apps", "company") and is_protected(coord, protected):
                    lines.append(f"    Var: {vname} = <not shown; use list_exposed>")
                    continue
                lines.append(f"    Var: {vname} = {_display_variable(vname, vval)}")

    return "\n".join(lines)


def _find_module(modules: list, search: str) -> dict | None:
    """Find a module by display name or coordinate substring."""
    search_lower = search.lower()

    # Exact match first
    for m in modules:
        if (m.get("displayName") or "").lower() == search_lower:
            return m
        if (m.get("moduleMavenCoordinate") or "").lower() == search_lower:
            return m

    # Substring match
    matches = [
        m for m in modules
        if search_lower in (m.get("displayName") or "").lower()
        or search_lower in (m.get("moduleMavenCoordinate") or "").lower()
    ]
    if len(matches) == 1:
        return matches[0]

    return None


async def install_module(
    client: ApolloClient,
    environment: str,
    maven_coordinate: str,
    variables: str | None = None,
    display_name: str | None = None,
    ignore_secret_requirements: bool = False,
    *,
    protected: frozenset[str] | None = None,
) -> str:
    if (refusal := protected_refusal(maven_coordinate, environment, protected)):
        return refusal
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    var_inputs = []
    if variables:
        try:
            var_dict = json.loads(variables)
        except json.JSONDecodeError as e:
            # Not echoed — see the note on `update_module_variables`.
            return f"Error: variables must be valid JSON ({e})."

        if (masked_err := _reject_masked(var_dict)):
            return masked_err

        for k, v in var_dict.items():
            var_inputs.append({
                "variableName": k,
                "variableValue": {"stringValue": _variable_string(v)},
            })

    request: dict = {
        "apolloEnvironmentId": env_id,
        "mavenCoordinate": maven_coordinate,
        "variables": var_inputs,
        "options": [],
    }
    if display_name:
        request["displayName"] = display_name
    if ignore_secret_requirements:
        request["ignoreSecretRequirements"] = True

    data = await client.graphql(Q.INSTALL_MODULE, {"request": request})
    result = data.get("apollo", {}).get("installModuleV2", {})
    state = (
        result.get("state", {})
        .get("__typename", "")
        .replace("ApolloProductModuleInstallationStateV2_", "")
    )

    return (
        f"Module installed on {env_name}\n"
        f"  Coordinate: {maven_coordinate}\n"
        f"  Display:    {result.get('displayName', display_name or '')}\n"
        f"  RID:        {result.get('rid', '')}\n"
        f"  State:      {state}"
    )


async def uninstall_module(
    client: ApolloClient, environment: str, module_name: str,
    *, protected: frozenset[str] | None = None,
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    modules = await _fetch_module_installations(client, env_id)

    module = _find_module(modules, module_name)
    if not module:
        names = [
            m.get("displayName") or m.get("moduleMavenCoordinate", "?")
            for m in modules
        ]
        return (
            f"Module '{module_name}' not found on {env_name}.\n"
            f"Available modules:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if (refusal := protected_refusal(module.get("moduleMavenCoordinate"), env_name, protected)):
        return refusal
    module_rid = module["rid"]
    display = module.get("displayName") or module.get("moduleMavenCoordinate", "?")

    # Capture the apps/pods this module installed BEFORE unlinking: unlinking
    # leaves them running as standalone deployments and severs the
    # installedByModuleV2 link, so they can't be enumerated afterward.
    app_names = await _module_installed_app_names(client, env_id, module_rid)

    result_data = await client.graphql(
        Q.UNINSTALL_MODULE, {"installationRid": module_rid}
    )
    result = result_data.get("apollo", {}).get("unlinkModule", {}) or {}
    state = (
        (result.get("state") or {})
        .get("__typename", "")
        .replace("ApolloProductModuleInstallationStateV2_", "")
    )

    lines = [
        f"Module unlink requested on {env_name}: {display}",
        f"  RID: {module_rid}",
    ]
    if state:
        lines.append(f"  State: {state}")

    lines.append("")
    lines.append(
        "IMPORTANT: unlinking the module did NOT remove the app(s)/pod(s) it "
        "installed — they keep running on the cube as standalone deployments."
    )
    if app_names:
        lines.append("Apps/pods this module installed:")
        lines.extend(f"  - {n}" for n in app_names)
        lines.append("")
        lines.append(
            "Next step: ask the user whether they also want these app(s)/pod(s) "
            'removed (refer to them as apps/pods to the user, not "entities"). '
            "Only after they confirm, remove each one with the uninstall_entity "
            f'tool (environment "{env_name}", one call per app/pod). Do not remove '
            "anything without explicit confirmation."
        )
    else:
        lines.append(
            "No apps/pods could be attributed to this module (it may not have "
            "installed any, or they were already removed). If the user expected "
            "running apps/pods to be cleaned up, confirm with them before removing "
            "anything with the uninstall_entity tool."
        )
    return "\n".join(lines)


async def _module_installed_app_names(
    client: ApolloClient, env_id: str, module_rid: str
) -> list[str]:
    """Names of the apps/pods (entities) installed by a module installation, for
    post-unlink cleanup guidance. Best-effort — returns [] if the lookup fails."""
    try:
        data = await client.graphql(Q.MODULE_INSTALLED_ENTITIES, {"id": env_id})
    except ApolloError:
        return []
    entities = (
        data.get("apollo", {})
        .get("environmentById", {})
        .get("entities", {})
        .get("entities", [])
    )
    names: list[str] = []
    for e in entities:
        if (e.get("installedByModuleV2") or {}).get("rid") != module_rid:
            continue
        names.append(
            e.get("displayName")
            or (e.get("entityLocator") or {}).get("entityName")
            or (e.get("product") or {}).get("productId")
            or "(unnamed)"
        )
    return names


async def update_module_variables(
    client: ApolloClient,
    environment: str,
    module_name: str,
    variables: str,
    *,
    protected: frozenset[str] | None = None,
) -> str:
    env_info = await _resolve_environment(client, environment)
    env_id = env_info["id"]
    env_name = env_info.get("name", environment)

    try:
        var_dict = json.loads(variables)
    except json.JSONDecodeError as e:
        # The payload is NOT echoed: `expose`/`unexpose` build it around a freshly
        # minted Teleport join token. The decoder's position is enough to fix a
        # hand-written value and carries none of its content.
        return f"Error: variables must be valid JSON ({e})."

    if (masked_err := _reject_masked(var_dict)):
        return masked_err

    modules = await _fetch_module_installations(client, env_id)

    module = _find_module(modules, module_name)
    if not module:
        names = [
            m.get("displayName") or m.get("moduleMavenCoordinate", "?")
            for m in modules
        ]
        return (
            f"Module '{module_name}' not found on {env_name}.\n"
            f"Available modules:\n" + "\n".join(f"  - {n}" for n in names)
        )

    if (refusal := protected_refusal(module.get("moduleMavenCoordinate"), env_name, protected)):
        return refusal
    module_rid = module["rid"]
    coord = module.get("moduleMavenCoordinate")
    display = module.get("displayName") or coord or "?"

    # Apollo's updateModuleInstallationV2 takes the COMPLETE variable set (full
    # replace), so read the installation's current variables and overlay the
    # caller's changes ("merge"). Variables the caller omits are preserved at
    # their current values; a variable cannot be unset through this tool.
    # NOTE: list returns effective values (defaults filled in) with no
    # default/override flag, so resending pins any defaulted variable to its
    # current value.
    merged: dict[str, dict] = {}
    for v in module.get("variables", []):
        name = v.get("variableName")
        if not name:
            continue
        val = v.get("variableValue") or {}
        field = "optionValue" if "OptionValue" in val.get("__typename", "") else "stringValue"
        merged[name] = {field: val.get("value")}

    for k, new_val in var_dict.items():
        # Preserve an existing variable's value type; default new keys to string.
        field = "optionValue" if "optionValue" in merged.get(k, {}) else "stringValue"
        merged[k] = {field: _variable_string(new_val)}

    update_input: dict = {
        "mavenCoordinate": coord,
        "variables": [
            {"variableName": name, "variableValue": vv} for name, vv in merged.items()
        ],
        "options": [],
    }
    if module.get("displayName"):
        update_input["displayName"] = module["displayName"]

    result_data = await client.graphql(
        Q.UPDATE_MODULE_INSTALLATION,
        {"moduleInstallationRid": module_rid, "update": update_input},
    )
    result = result_data.get("apollo", {}).get("updateModuleInstallationV2", {}) or {}
    state = (
        (result.get("state") or {})
        .get("__typename", "")
        .replace("ApolloProductModuleInstallationStateV2_", "")
    )

    lines = [
        f"Module variable update requested on {env_name}: {display}",
        f"  RID:   {module_rid}",
    ]
    if state:
        lines.append(f"  State: {state}")
    lines.append("  Changed variables:")
    for k, v in var_dict.items():
        lines.append(_variable_line(k, v))
    lines.append("")
    lines.append(
        "Note: variables are MERGED onto the module's existing values — only the "
        "keys above were changed; all others were preserved. This is submitted as a "
        "change request and may need approval before it takes effect."
    )
    return "\n".join(lines)
