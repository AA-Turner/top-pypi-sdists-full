"""MCP tools that proxy to cube-cloud.

These tools are forwarded verbatim — the agent just passes arguments through
and returns the remote response. All the logic lives server-side.
"""

from __future__ import annotations

from mcp.types import Tool

# Tools that are proxied to cube-cloud (no local execution needed)
REMOTE_TOOLS: list[Tool] = [
    Tool(
        name="list_environments",
        description=(
            "List Apollo environments with their IDs and RIDs. "
            "Optionally filter by name substring."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": 'Optional name substring to filter by (case-insensitive). Example: "pep".',
                },
            },
        },
    ),
    Tool(
        name="install_entity",
        description=(
            "Install a Helm chart entity on an Apollo environment. Refused when an "
            "entity of the same name is managed by a module, unless force=true."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": "Target environment name or RID.",
                },
                "entity_name": {
                    "type": "string",
                    "description": "Helm chart name (e.g. mosquitto).",
                },
                "product_id": {
                    "type": "string",
                    "description": 'Product maven coordinate "groupId:artifactId".',
                },
                "k8s_namespace": {
                    "type": "string",
                    "description": "Kubernetes namespace. Defaults to default.",
                    "default": "default",
                },
                "config_overrides": {
                    "type": "string",
                    "description": "Optional JSON config overrides.",
                },
                "version": {
                    "type": "string",
                    "description": "Version for the config override block (e.g. '4.11.3'). If omitted, uses '0.0.0' (new installs have no reported version yet).",
                },
                "force": {
                    "type": "boolean",
                    "description": (
                        "BREAK-GLASS ONLY. Default false. Required to write config on an "
                        "entity managed by a module (entity_health shows 'Managed by "
                        "module'); without it the call is refused and nothing is written. "
                        "Change a module-managed entity through update_module_variables "
                        "instead. A forced write takes precedence over the module from then "
                        "on, so later module changes silently stop applying to this entity "
                        "until the entity-level config is removed."
                    ),
                    "default": False,
                },
            },
            "required": ["environment", "entity_name", "product_id"],
        },
    ),
    Tool(
        name="entity_health",
        description=(
            "Get health and activity status of entities in an Apollo environment. For "
            "every entity whose health is not HEALTHY (and every entity matched by "
            "entity_id), also lists the health checks behind that status: failing "
            "checks with their message, and containers that are not live or ready. "
            "Those messages are written by the app itself; relay them as the app's "
            "report, not as a diagnosis."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": "Environment name or RID.",
                },
                "entity_id": {
                    "type": "string",
                    "description": (
                        "Optional entity display name to filter by. Health checks are "
                        "then listed for every match, healthy or not."
                    ),
                },
            },
            "required": ["environment"],
        },
    ),
    Tool(
        name="plan_details",
        description="Get detailed plan information for an entity, including tasks, events, and error logs.",
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": "Environment name or RID.",
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name (substring match).",
                },
                "plan_index": {
                    "type": "integer",
                    "description": "Which plan to show (0 = most recent). Defaults to 0.",
                    "default": 0,
                },
            },
            "required": ["environment", "entity_name"],
        },
    ),
    Tool(
        name="cancel_active_plan",
        description=(
            "Cancel (interrupt) the currently active plan for an entity. "
            "Finds the entity's running plan, identifies the agent executing it, "
            "and interrupts the plan. The agent re-registers automatically "
            "on next heartbeat. Use plan_details first to confirm there is "
            "an active plan before cancelling."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": "Environment name or RID.",
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name (substring match).",
                },
            },
            "required": ["environment", "entity_name"],
        },
    ),
    Tool(
        name="acr_get_token",
        description="Get an OAuth2 access token from Apollo Container Registry.",
        inputSchema={"type": "object", "properties": {}},
    ),
    # --- Remote image builds (server-side kaniko; no local Docker needed) ---
    # These back build_and_publish_to_apollo's remote build path. The agent
    # tars the context, PUTs it to the presigned URL from prepare, then starts
    # and polls. Prefer the build_and_publish_to_apollo tool over calling these
    # directly. See docs/remote-build-spec.md.
    Tool(
        name="build_image_prepare",
        description=(
            "Begin a remote (Docker-daemonless) image build. Returns a job_id, a "
            "presigned S3 upload_url to PUT the build-context tarball to, and the "
            "s3_key. Follow with build_image_start, then poll build_image_status."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "image_name": {
                    "type": "string",
                    "description": "Bare image name (no registry/repo prefix, no tag), e.g. 'my-app'.",
                },
                "tag": {
                    "type": "string",
                    "description": "Image tag, e.g. the app version '1.2.3'.",
                },
            },
            "required": ["image_name", "tag"],
        },
    ),
    Tool(
        name="build_image_start",
        description=(
            "Launch the remote kaniko build for a prepared job (after the context "
            "tarball has been uploaded to the presigned URL). The ACR push token is "
            "minted server-side. Returns a task_arn; poll build_image_status until "
            "the state is SUCCEEDED or FAILED."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "job_id from build_image_prepare."},
                "dockerfile": {
                    "type": "string",
                    "description": "Dockerfile path relative to the context root. Defaults to 'Dockerfile'.",
                    "default": "Dockerfile",
                },
                "target": {
                    "type": "string",
                    "description": "Optional build stage to target in a multi-stage Dockerfile.",
                },
                "build_args": {
                    "type": "object",
                    "description": "Optional build-time args as {name: value}.",
                    "additionalProperties": {"type": "string"},
                },
                "platform": {
                    "type": "string",
                    "description": "Target platform. Defaults to 'linux/amd64' (the cube architecture).",
                    "default": "linux/amd64",
                },
            },
            "required": ["job_id"],
        },
    ),
    Tool(
        name="build_image_status",
        description=(
            "Poll a remote build job. Returns state (PENDING|RUNNING|SUCCEEDED|"
            "FAILED); on SUCCEEDED includes image_uri, on FAILED includes "
            "stopped_reason, and on terminal states includes a logs_tail."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "job_id": {"type": "string", "description": "job_id from build_image_prepare."},
            },
            "required": ["job_id"],
        },
    ),
    # NOTE: apollo_publish_manifest is intentionally NOT exposed here.
    # It only publishes metadata — it does NOT push the Helm chart to ACR.
    # Users should use build_and_publish_to_apollo (local tool) which handles
    # the full pipeline: build -> push to ACR -> publish manifest.
    # The build pipeline calls apollo_publish_manifest internally via CloudClient.
    # Entity management
    Tool(
        name="uninstall_entity",
        description=(
            "Uninstall an entity from an Apollo environment. Removes the specified "
            "entity (Helm chart) via a change request. Use entity_health to find "
            "entity names and plan_details to monitor uninstall progress."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "entity_name": {
                    "type": "string",
                    "description": 'Entity display name or entity name (substring match, e.g. "mosquitto").',
                },
            },
            "required": ["environment", "entity_name"],
        },
    ),
    Tool(
        name="update_entity_config",
        description=(
            "Update configuration overrides for an entity in an Apollo environment. "
            "REPLACES the entity's whole config overrides (Helm value overrides) with "
            "the object given. Use entity_health to see the current overrides and "
            "whether the entity is managed by a module before updating. A "
            "module-managed entity is refused: change it with update_module_variables "
            "on its module. force=true overrides that for break-glass situations only, "
            "because the entity-level config then takes precedence over the module "
            "and later module changes silently stop applying."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name or entity name (substring match).",
                },
                "config_overrides": {
                    "type": "string",
                    "description": (
                        "JSON object of config overrides (e.g. '{\"replicaCount\": 2}'). "
                        "Replaces the existing overrides entirely, so include every value "
                        "to keep. Values entity_health shows as <hidden, N chars> must be "
                        "supplied for real; a placeholder is refused."
                    ),
                },
                "version": {
                    "type": "string",
                    "description": "Version for the config override block (e.g. '4.11.3'). If omitted, uses the entity's current reported version.",
                },
                "force": {
                    "type": "boolean",
                    "description": (
                        "BREAK-GLASS ONLY. Default false. Required to write config on an "
                        "entity managed by a module (entity_health shows 'Managed by "
                        "module'); without it the call is refused and nothing is written. "
                        "Change a module-managed entity through update_module_variables "
                        "instead. A forced write takes precedence over the module from then "
                        "on, so later module changes silently stop applying to this entity "
                        "until the entity-level config is removed."
                    ),
                    "default": False,
                },
            },
            "required": ["environment", "entity_name", "config_overrides"],
        },
    ),
    Tool(
        name="enforce_entity_config",
        description=(
            "Force config re-enforcement on an entity. Re-submits current config "
            "overrides, triggering Apollo to create a new enforce config plan. "
            "Useful when config has drifted or a previous enforcement failed."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name or entity name (substring match).",
                },
            },
            "required": ["environment", "entity_name"],
        },
    ),
    # Module management
    Tool(
        name="list_modules",
        description=(
            "List modules installed on an Apollo environment. Shows display names, "
            "maven coordinates, state, variables, and RIDs. Use this before "
            "updating variables or unlinking a module. NOTE: values of "
            "secret-looking variables (authToken, password, secret, key, ...) are "
            "shown as '<hidden, N chars>' and CANNOT be read back — never copy that "
            "placeholder into a write; it is refused. For a non-admin profile this "
            "tool does not show the Teleport multi-app module's `apps` list either: "
            "use list_exposed for the apps on a cube."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "search": {
                    "type": "string",
                    "description": "Optional substring to filter modules by name or coordinate (case-insensitive).",
                },
            },
            "required": ["environment"],
        },
    ),
    Tool(
        name="install_module",
        description=(
            "Install a module on an Apollo environment. Modules are collections of "
            "related entities managed together. If already installed, use "
            "update_module_variables to change variables. "
            "The Teleport Multi-App Service module (the one behind exposed apps) is "
            "managed only through expose, unexpose and list_exposed for non-admin "
            "profiles, and this tool refuses it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Target environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "maven_coordinate": {
                    "type": "string",
                    "description": 'Module maven coordinate (e.g. "module:builtin-control-plane-minimal:0.0.40").',
                },
                "variables": {
                    "type": "string",
                    "description": "Optional JSON object of module variables as {\"varName\": \"value\", ...}.",
                },
                "display_name": {
                    "type": "string",
                    "description": "Optional display name for the module installation.",
                },
                "ignore_secret_requirements": {
                    "type": "boolean",
                    "description": "If true, allows installation even if required secrets are not set.",
                    "default": False,
                },
            },
            "required": ["environment", "maven_coordinate"],
        },
    ),
    Tool(
        name="uninstall_module",
        description=(
            "Unlink a module from an Apollo environment. This does NOT remove the "
            "apps/pods the module installed — they keep running as standalone "
            "deployments. The tool returns the list of those apps/pods plus cleanup "
            "guidance: ask the user to confirm before removing any, refer to them as "
            'apps/pods (not "entities") when talking to the user, and remove confirmed '
            "ones with the uninstall_entity tool. "
            "The Teleport Multi-App Service module (the one behind exposed apps) is "
            "managed only through expose, unexpose and list_exposed for non-admin "
            "profiles, and this tool refuses it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "module_name": {
                    "type": "string",
                    "description": 'Module display name or maven coordinate substring (e.g. "control-plane").',
                },
            },
            "required": ["environment", "module_name"],
        },
    ),
    Tool(
        name="update_module_variables",
        description=(
            "Update variables on an installed module. MERGE semantics: the variables "
            "you pass are merged onto the installation's existing variables — only the "
            "keys you include change; every other variable is left at its current "
            "value. Pass every variable you intend to change in a single call (an "
            "omitted variable is preserved, not reset; this tool cannot unset a "
            "variable). Apollo's underlying update is a full-installation replace, so "
            "the tool reads the current variables and resends the complete set with "
            "your changes applied. The change is submitted as a change request that "
            "may require approval before it takes effect. Call list_modules first to "
            "see current variable NAMES — secret values are masked there and cannot "
            "be read back. Since omitted variables are preserved, simply leave a "
            "secret you are not changing out of the call; passing the masked "
            "placeholder is refused. "
            "The Teleport Multi-App Service module (the one behind exposed apps) is "
            "managed only through expose, unexpose and list_exposed for non-admin "
            "profiles, and this tool refuses it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "module_name": {
                    "type": "string",
                    "description": "Module display name or maven coordinate substring.",
                },
                "variables": {
                    "type": "string",
                    "description": 'JSON object of variables to update as {"varName": "newValue", ...}.',
                },
            },
            "required": ["environment", "module_name", "variables"],
        },
    ),
    # Teleport app exposure
    Tool(
        name="expose",
        description=(
            "Publish a running in-cluster service at a public URL, scoped by "
            "company label. Mints a fresh short-lived App Service join token from "
            "the cube-mcp bot identity (no human Teleport account needed) and "
            "adds/updates this app on the environment's shared Teleport multi-app-"
            "service module (one shared module per environment — re-running expose "
            "for the same app updates it in place, it never duplicates). Returns "
            "the app's URL, https://<app_name>-<cube>.<cube-mcp apex>: open it in a "
            "browser and sign in with the same login as cube-mcp. Hand out THAT "
            "url — never Teleport's own address, which needs a Teleport account. "
            "The URL usually starts answering a few minutes after the call, once the cube rolls the "
            "app-service release out. Who can see the app is its app companies: the "
            "first detail line of the response, 'Visible to: …', says which — "
            "tell the user."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Apollo environment / cube to expose the app on (e.g. "pep-onlogicmc610-4").',
                },
                "app_name": {
                    "type": "string",
                    "description": 'Base app name (e.g. "trino"). Auto-suffixed with the environment name for uniqueness across cubes ("trino-<env>"); that qualified name becomes the leftmost label of the public URL, and is what you pass to unexpose (and to app_proxy).',
                },
                "app_uri": {
                    "type": "string",
                    "description": (
                        "Internal service URI, e.g. "
                        '"http://svc.namespace.svc.cluster.local:8080". Use the REAL '
                        "service + targetPort — a wrong port surfaces as Teleport "
                        '"context deadline exceeded".'
                    ),
                },
                "public_addr": {
                    "type": "string",
                    "description": "Rarely needed. Overrides the app's TELEPORT public address — a Teleport-registration detail, NOT the URL this tool publishes (that is always the browser-proxy host, derived from app_name). Keep it consistent with <app_name>.<Teleport proxy host> or Teleport may not route. When set, app_name is taken verbatim with no auto-qualification, so it must be a valid DNS label on its own (lower-case a-z0-9 and '-', no leading/trailing '-', 63 chars max).",
                },
                "company": {
                    "type": "string",
                    "description": (
                        "The app company to expose this app TO — who can see it. Omit for "
                        "the profile's home company. If the user's profile holds more than "
                        "one app company, ASK the user which company should see this app "
                        "before calling; never guess, because the wrong company shows the "
                        "app to the wrong people. Exposing an app that already exists under "
                        "the same name and target ADDS a company to it (it stays visible to "
                        "the others): the one named here, or the profile's home company if "
                        "the profile is not already on the app. A profile already on the app "
                        "adds nothing unless it NAMES the company, so to share an app you can "
                        "already see, pass company. On a stack that reads stored company sets, changing "
                        "an existing app (its target, headers or labels) while naming NO "
                        "company keeps its audience exactly as it is; name a company only to "
                        "add it. On the baseline stack an app has ONE company, and an admin "
                        'who names none re-labels it "edgescaleai": there, name the app\'s '
                        "current company to keep its audience. Unscoped admin profiles may "
                        'name any company (default "edgescaleai" for a NEW app).'
                    ),
                },
                # JSON-in-a-string, matching `update_module_variables.variables`,
                # `install_entity.config_overrides` and `create_secret.secret_keys`.
                # Declared as a native array first, which failed against a real MCP
                # client: the value arrived as the string "[...]" and was rejected by
                # schema validation before any of our code ran. Every structured
                # argument in this file is a JSON string for that reason.
                "rewrite_headers": {
                    "type": "string",
                    "description": (
                        'JSON ARRAY of headers the app service rewrites on requests it '
                        'forwards to your service, each as "Name: value" — e.g. '
                        '\'["Host: app.internal"]\'. Two '
                        "uses: (1) selecting an nginx-ingress vhost — the value must match "
                        "the in-cluster ingress rule, which is NOT this app's own address, "
                        "so it carries across a migration unchanged; (2) satisfying an app "
                        "that compares Origin against Host, such as anything using a "
                        "WebSocket with a same-origin check. For (2) set BOTH, pointing at "
                        "the app's own public URL host: Teleport replaces the Host with the "
                        "internal service address before your app sees it, so without a "
                        "rewrite Host and Origin disagree and the check fails. A rewrite "
                        "naming an OLD address (e.g. *.teleport.sh) has the same effect and "
                        "must be re-pointed, not simply deleted. OMIT to leave any existing "
                        "rewrite untouched; pass '[]' (the two-character JSON empty array) "
                        "to remove all of them. Cannot be used with a tcp:// app. Read the "
                        "current values with list_exposed — this replaces the whole list "
                        "rather than merging into it."
                    ),
                },
                "labels": {
                    "type": "string",
                    "description": (
                        'JSON OBJECT of extra Teleport labels for this app, e.g. '
                        '\'{"app-type": "console"}\'. '
                        "Merged under the resolved company, which this cannot set. Omit to "
                        "leave existing extra labels untouched. Mainly for migrating an app "
                        "that already carries an operator-set label, which would otherwise "
                        "be dropped."
                    ),
                },
            },
            "required": ["environment", "app_name", "app_uri"],
        },
    ),
    Tool(
        name="unexpose",
        description=(
            "Take a company off a previously-exposed app (or off every app it is "
            "on, with all=true) on the environment's shared Teleport multi-app-"
            "service module. An app stays exposed while any other company remains "
            "on it and is deleted once none does. Mints a fresh join token and "
            "updates the module in place; once no apps remain, the module is automatically unlinked "
            "and its underlying entity uninstalled — no separate confirmation "
            "step, since calling this tool already is the confirmation. Use the "
            "same app_name/public_addr you passed to expose. An app name that "
            "doesn't exist and one you don't have permission to manage return "
            "the identical error — you can't tell which from the response. The "
            "app's public URL stops working once the cube rolls the change out "
            "(usually a few minutes), not the moment this returns."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Apollo environment / cube the app was exposed on (e.g. "pep-onlogicmc610-4").',
                },
                "app_name": {
                    "type": "string",
                    "description": "Base app name as originally passed to expose (auto-qualified the same way; pass the same value, NOT the qualified name from list_exposed). Mutually exclusive with all.",
                },
                "public_addr": {
                    "type": "string",
                    "description": "Must match the public_addr originally passed to expose, if any (disables auto-qualification the same way).",
                },
                "all": {
                    "type": "boolean",
                    "description": (
                        "Take the company off every exposed app it is on in one call, "
                        "tearing the module down once nothing remains, instead of "
                        "minting a fresh token per app. Mutually exclusive with "
                        "app_name/public_addr."
                    ),
                    "default": False,
                },
                "company": {
                    "type": "string",
                    "description": (
                        "The app company to remove. Omit to remove the profile's home "
                        "company. Naming any other company takes the app away from that "
                        "company's users: only do it when the user explicitly asks for "
                        "that company to lose access. For an unscoped ADMIN profile, "
                        "omitting it (or sending an empty string) removes the WHOLE app "
                        "for every company on it."
                    ),
                },
            },
            "required": ["environment"],
        },
    ),
    Tool(
        name="list_exposed",
        description=(
            "List apps currently exposed on an environment's shared Teleport "
            "multi-app-service module (the apps expose/unexpose manage) — name, "
            "who it is visible to, and for apps you can reach, internal URI and "
            "public URL. The URL per app is the one to hand out: browser-reachable "
            "with the same login as cube-mcp. Use this before expose/unexpose to "
            "see what's already there. Apps you cannot reach are either omitted or "
            "listed by name and audience only, depending on the stack."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Apollo environment / cube to list exposed apps on (e.g. "pep-onlogicmc610-4").',
                },
            },
            "required": ["environment"],
        },
    ),
    # Secret management
    Tool(
        name="create_secret",
        description=(
            "Create a secret for an entity in an Apollo environment. "
            "Provide secret_value for a single value (stored as a key matching "
            "the secret name), or secret_keys as a JSON object for multiple key-value pairs."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name or entity name (substring match).",
                },
                "secret_name": {
                    "type": "string",
                    "description": 'Name for the secret (e.g. "mqtt-credentials").',
                },
                "secret_value": {
                    "type": "string",
                    "description": "Value for a single-value secret (stored as key=secret_name). Mutually exclusive with secret_keys.",
                },
                "secret_keys": {
                    "type": "string",
                    "description": 'JSON object of key-value pairs (e.g. \'{"username": "admin", "password": "secret"}\').',
                },
                "description": {
                    "type": "string",
                    "description": "Optional description for the secret.",
                },
            },
            "required": ["environment", "entity_name", "secret_name"],
        },
    ),
    Tool(
        name="update_secret",
        description=(
            "Update an existing secret for an entity. Provide secret_key and "
            "secret_key_value to set a specific key, or secret_value to set "
            "the key matching the secret name."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Environment name or RID (e.g. "pep-onlogicmc610-4").',
                },
                "entity_name": {
                    "type": "string",
                    "description": "Entity display name or entity name (substring match).",
                },
                "secret_name": {
                    "type": "string",
                    "description": "Name of the existing secret to update.",
                },
                "secret_value": {
                    "type": "string",
                    "description": "New value (sets the key matching secret_name).",
                },
                "secret_key": {
                    "type": "string",
                    "description": "Key name to set/update in the secret.",
                },
                "secret_key_value": {
                    "type": "string",
                    "description": "Value for the key specified by secret_key.",
                },
                "description": {
                    "type": "string",
                    "description": "New description for the secret.",
                },
            },
            "required": ["environment", "entity_name", "secret_name"],
        },
    ),
    # Product & release channel management
    Tool(
        name="list_products",
        description=(
            "List available products in Apollo. Products represent deployable software "
            "(Helm charts, assets). Use this to discover product IDs for install_entity."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": "Optional substring to filter products by name or ID (case-insensitive).",
                },
                "page_size": {
                    "type": "integer",
                    "description": "Number of products to return (default 50, max 200).",
                    "default": 50,
                },
            },
        },
    ),
    Tool(
        name="compare_product_versions",
        description=(
            "Compare what version of a product is installed across multiple environments. "
            "Shows installed version, rollout status, health, and release channel."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": 'Product maven coordinate "groupId:artifactId" (e.g. "com.edgescaleai-cube:esai-platform-z").',
                },
                "environments": {
                    "type": "string",
                    "description": 'Comma-separated environment names (e.g. "pep-onlogicmc610-4, joel-cube").',
                },
            },
            "required": ["product_id", "environments"],
        },
    ),
    Tool(
        name="list_release_channels",
        description=(
            "List available Apollo release channels. By default only shows ordinary "
            "(non-environment-specific) channels."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "search": {
                    "type": "string",
                    "description": "Optional substring to filter channels by name (case-insensitive).",
                },
                "include_env_specific": {
                    "type": "boolean",
                    "description": "If true, also show environment-specific channels.",
                    "default": False,
                },
            },
        },
    ),
    Tool(
        name="get_product_releases",
        description=(
            "Get release history for a product, showing versions and their release channels."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": 'Product maven coordinate "groupId:artifactId" (e.g. "com.edgescaleai-cube:esai-platform-z").',
                },
                "page_size": {
                    "type": "integer",
                    "description": "Number of releases to return (default 10, max 50).",
                    "default": 10,
                },
            },
            "required": ["product_id"],
        },
    ),
    # Phase 2: Server-side Teleport + kubectl tools
    Tool(
        name="cube_status",
        description="Get the status of a Cube node (server-side kubectl via tbot).",
        inputSchema={
            "type": "object",
            "properties": {
                "cluster": {
                    "type": "string",
                    "description": "Cube cluster name (from cube_list).",
                },
            },
            "required": ["cluster"],
        },
    ),
    Tool(
        name="cube_list",
        description="List available Cube clusters accessible via server-side tbot.",
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="kubectl_exec",
        description=(
            "Execute a kubectl command server-side. "
            "Destructive commands (delete, apply, create, etc.) are blocked."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cluster": {
                    "type": "string",
                    "description": "Target Cube cluster name (from cube_list).",
                },
                "command": {
                    "type": "string",
                    "description": 'kubectl command without the "kubectl" prefix. Example: "get pods -n default".',
                },
            },
            "required": ["cluster", "command"],
        },
    ),
    Tool(
        name="app_list",
        description=(
            "List exposed apps across the Teleport tenant (server-side via tbot), "
            "with each app's public URL — browser-reachable with the same login as "
            "cube-mcp. Use list_exposed for one cube's apps and their company labels."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": 'Optional filter by company label (e.g. "edgescaleai", "lear").',
                },
            },
        },
    ),
    Tool(
        name="list_services",
        description=(
            "List Kubernetes Services running in a cube's cluster, with a "
            "ready-made internal app_uri suggestion per port. Use this to find "
            "what's available before calling expose — picking the wrong port "
            'surfaces as Teleport "context deadline exceeded".'
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "environment": {
                    "type": "string",
                    "description": 'Apollo environment / cube to list services on (e.g. "pep-onlogicmc610-4").',
                },
                "namespace": {
                    "type": "string",
                    "description": "Optional Kubernetes namespace to filter to. Omit to list across all namespaces, which hides known infra/system namespaces (kube-system, openshift*, groundcover, teleport, etc.) by default — pass one of those explicitly to see it.",
                },
            },
            "required": ["environment"],
        },
    ),

    # --- Groundcover observability (read-only, scoped per cube) ---
    # All tools authorize `cube` against the caller's Apollo-visible cubes and
    # pin the cluster label/condition server-side. Endpoints are the real
    # Groundcover REST API (see tools/groundcover.py).
    Tool(
        name="groundcover_list_clusters",
        description=(
            "List the cubes you are authorized to read that are reporting to "
            "Groundcover. Authorization is scoped to the cubes your account can "
            "see in Apollo (admins see all). Start here to find a valid 'cube'."
        ),
        inputSchema={"type": "object", "properties": {}},
    ),
    Tool(
        name="groundcover_list_workloads",
        description=(
            "List Kubernetes workloads (deployments/pods) and their health "
            "(cpu, memory, rps, error rate, pod count, readiness, issues) for one "
            "cube. Scoped to your cube."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for (see groundcover_list_clusters)."},
                "namespace": {"type": "string", "description": "Optional k8s namespace filter."},
                "limit": {"type": "integer", "description": "Max workloads (1-1000). Defaults to 100."},
            },
            "required": ["cube"],
        },
    ),
    Tool(
        name="groundcover_query_metrics",
        description=(
            "Query Groundcover metrics for one cube. The PromQL is built "
            "server-side and always pinned to your cube (cluster label) — you "
            "cannot read another cube. Omit start/end for an instant query; "
            "provide both for a range query."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for."},
                "metric": {"type": "string", "description": 'Metric name, e.g. "groundcover_host_cpu_usage_percent" (whole-host CPU) or "groundcover_pvc_usage_percent" (volume fill). NOTE names are host-/node-/pvc-prefixed: a bare "groundcover_cpu_usage_percent" does NOT exist. Use groundcover_list_metrics to discover names.'},
                "match": {
                    "type": "object",
                    "description": 'Optional extra label matchers as {label: value} (exact). The "cluster" label is reserved and pinned to your cube.',
                    "additionalProperties": {"type": "string"},
                },
                "aggregation": {"type": "string", "description": 'Optional. Range fns need a window: rate, irate, increase, delta, idelta, deriv. Instant aggregations: sum, avg, min, max, count, stddev, stdvar.'},
                "window": {"type": "string", "description": 'Range window for rate-style aggregations, e.g. "5m".'},
                "start": {"type": "string", "description": "RFC3339 start time (range query)."},
                "end": {"type": "string", "description": "RFC3339 end time (range query)."},
                "step": {"type": "string", "description": 'Range step, e.g. "1m". Defaults to 1m.'},
            },
            "required": ["cube", "metric"],
        },
    ),
    Tool(
        name="groundcover_list_metrics",
        description=(
            "Discover metrics for one cube. Groundcover metric names are NOT standard "
            "Prometheus/k8s names (e.g. PVC fill is groundcover_pvc_usage_percent, not "
            "kube_persistentvolumeclaim_*). Call WITHOUT filter to get a families/"
            "vocabulary map (prefix + count + examples); call WITH filter (a prefix or "
            "word like 'pvc'/'disk'/'cpu') to get matching metric names to pass to "
            "groundcover_query_metrics. Scoped to your cube."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for."},
                "filter": {"type": "string", "description": "Optional substring to match metric names server-side (e.g. 'pvc', 'disk', 'fs', 'cpu'). Omit to see the families map."},
                "start": {"type": "string", "description": "RFC3339 start. Defaults to 1h ago."},
                "end": {"type": "string", "description": "RFC3339 end. Defaults to now."},
                "limit": {"type": "integer", "description": "Max names to scan (1-5000). Defaults to 1000."},
            },
            "required": ["cube"],
        },
    ),
    Tool(
        name="groundcover_search_logs",
        description=(
            "Search logs for one cube. Always pinned to your cube. `query` uses "
            "Groundcover's log search syntax (e.g. 'level:error | limit 10')."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for."},
                "start": {"type": "string", "description": "RFC3339 start. Defaults to 1h ago."},
                "end": {"type": "string", "description": "RFC3339 end. Defaults to now."},
                "query": {"type": "string", "description": "Optional Groundcover log search query (e.g. 'level:error'). A '| limit N' is appended automatically if absent."},
                "limit": {"type": "integer", "description": "Max rows (1-1000). Defaults to 100."},
            },
            "required": ["cube"],
        },
    ),
    Tool(
        name="groundcover_search_traces",
        description="Search distributed traces for one cube. Always pinned to your cube.",
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for."},
                "start": {"type": "string", "description": "RFC3339 start. Defaults to 1h ago."},
                "end": {"type": "string", "description": "RFC3339 end. Defaults to now."},
                "query": {"type": "string", "description": "Optional Groundcover trace search query. A '| limit N' is appended automatically if absent."},
                "limit": {"type": "integer", "description": "Max rows (1-1000). Defaults to 100."},
            },
            "required": ["cube"],
        },
    ),
    Tool(
        name="groundcover_k8s_events",
        description="Search Kubernetes events (e.g. crashes, OOMKills, scheduling) for one cube. Pinned to your cube.",
        inputSchema={
            "type": "object",
            "properties": {
                "cube": {"type": "string", "description": "Cube/cluster name you are authorized for."},
                "start": {"type": "string", "description": "RFC3339 start. Defaults to 1h ago."},
                "end": {"type": "string", "description": "RFC3339 end. Defaults to now."},
            },
            "required": ["cube"],
        },
    ),
    Tool(
        name="send_feedback",
        description=(
            "Send feedback about the Cube or Edgeport to the EdgescaleAI team. "
            "ALWAYS ASK THE USER WHICH KIND THIS IS BEFORE CALLING, unless they "
            "have already made it obvious: is something broken ('support') — or do "
            "they have an idea for something new ('feature')? The answer decides "
            "which tracker it lands in, and it is not something to guess. "
            "DO NOT promise the user a reply, a response time, or that someone "
            "will follow up: feedback is recorded and read, and there is no "
            "support rotation behind it. Say it has been recorded, and give them "
            "the reference number the tool returns. "
            "The submitter is identified from the caller's own credential, so do "
            "not ask for their email unless the tool says it is needed."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "feedback_type": {
                    "type": "string",
                    "enum": ["support", "feature"],
                    "description": (
                        "support = something is broken or not behaving as "
                        "expected; filed as a bug report. feature = the user wants "
                        "a capability that does not exist yet; recorded on the "
                        "product backlog. Ask the user rather than inferring — "
                        "'it is broken' and 'it should do X' are genuinely "
                        "different requests. (The wire value reads 'support' for "
                        "compatibility; present it to the user as a bug report, "
                        "and do not offer it as a way to ask a question — nobody "
                        "is staffed to answer one.)"
                    ),
                },
                "summary": {
                    "type": "string",
                    "description": "One-line title for the ticket.",
                },
                "details": {
                    "type": "string",
                    "description": (
                        "The feedback itself. For a bug, include what happened, "
                        "what was expected, and steps to reproduce."
                    ),
                },
                "business_impact": {
                    "type": "string",
                    "description": (
                        "Why this matters — who is blocked and what it costs. "
                        "REQUIRED for 'feature'. Optional for 'support': it is a "
                        "reasonable thing to ask of a roadmap request and pure "
                        "friction in front of a question."
                    ),
                },
                "cube": {
                    "type": "string",
                    "description": "Optional cube the feedback is about, recorded as context.",
                },
                "submitter_name": {
                    "type": "string",
                    "description": "Reporter's name. Defaults to the local part of their email.",
                },
                "submitter_role": {
                    "type": "string",
                    "description": "Reporter's role, e.g. 'Deployment Strategist'. Defaults to 'Cube MCP user'.",
                },
                "contact_email": {
                    "type": "string",
                    "description": (
                        "Fallback contact address, used ONLY when the calling key "
                        "has no address on file (a bot or CLI key). For a normal "
                        "browser login the address is resolved server-side and "
                        "anything passed here is ignored."
                    ),
                },
            },
            "required": ["feedback_type", "summary", "details"],
        },
    ),
]

REMOTE_TOOL_NAMES = {t.name for t in REMOTE_TOOLS}
