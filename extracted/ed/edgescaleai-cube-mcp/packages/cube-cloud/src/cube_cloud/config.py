"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """cube-cloud configuration loaded from environment variables."""

    # AWS
    aws_region: str = "us-west-2"

    # DynamoDB table for API keys
    dynamodb_table: str = "cube-mcp-api-keys"

    # DynamoDB table for browser login sessions (shared across ECS tasks)
    login_sessions_table: str = "cube-mcp-login-sessions"

    # Secrets Manager prefix for profile credentials
    secrets_prefix: str = "cube-mcp/profiles/"

    # Where a profile's app companies come from (auth/app_companies.py,
    # docs/multi-company-app-access-spec.md). "map" is the BASELINE: exactly one app
    # company per profile, from the in-code PROFILE_COMPANY_MAP -- the stored
    # `app_companies` field is not even read. "stored" reads the set that
    # scripts/provision-access.py writes into the profile's secret. Per stack, because
    # the secrets and Teleport roles are shared by dev and prod: this is the one knob
    # that keeps a stack on baseline behaviour while another validates the new model,
    # and flipping it back is the rollback. Anything unrecognized is treated as "map".
    app_companies_source: str = "map"
    # Which app companies may be COMBINED on one app (docs/multi-company-app-access-spec.md):
    # "*" (the default) for any, or a comma-separated list to restrict it. Only read on a
    # "stored" stack; a "map" stack never combines. The default is "any" so that no stack
    # has to carry -- and remember to update -- a list at the prod flip. Dev carried a list of
    # test companies while roles still matched `company` exactly (combining a real company
    # hid the app from them); it was removed once they were migrated (2026-09-25). An empty
    # value stops all combining through expose and the console (not update_entity_config),
    # the brake if that is ever needed again. `prod.tfvars` must
    # never set it at all (test_prod_carries_no_combining_allowlist).
    app_companies_combinable: str = "*"

    # Cognito (browser login)
    cognito_user_pool_id: str = ""
    cognito_app_client_id: str = ""
    cognito_domain: str = ""  # e.g. "cube-mcp-prod.auth.us-west-2.amazoncognito.com"

    # Public domain (used to build OAuth callback URLs behind a load balancer)
    domain: str = ""  # e.g. "cube.edgescaleai-cube.com"

    # Groundcover observability.
    # API-key auth works against api.groundcover.com only (app.groundcover.com is
    # the session-auth/UI host). Override for self-hosted backends.
    groundcover_api_base: str = "https://api.groundcover.com"
    # Secrets Manager id holding the Groundcover API key (and optionally the
    # backend id). Secret value JSON: {"api_key": "...", "backend_id": "..."}
    groundcover_api_key_secret: str = "cube-mcp/groundcover/api-key"
    # Comma-separated Groundcover backend ids to fan queries out across, each
    # sent as the required X-Backend-Id header. One org API key is confirmed
    # (live, 2026-08-11) to work against every backend here — see
    # docs/groundcover-integration-spec.md "Multi-backend routing". Override via
    # the secret JSON ("backend_ids", or legacy singular "backend_id", which
    # win) or CUBE_CLOUD_GROUNDCOVER_BACKEND_IDS.
    groundcover_backend_ids: str = "groundcover"

    # Remote image builds (kaniko). Names map to the CUBE_CLOUD_* env vars set
    # by infra/terraform/ecs.tf; see infra/terraform/build.tf for the resources.
    build_ctx_bucket: str = ""            # S3 bucket for staged build contexts
    build_jobs_table: str = ""            # DynamoDB table tracking build jobs
    kaniko_cluster: str = ""              # ECS cluster to RunTask kaniko on
    kaniko_task_def: str = ""             # kaniko task-definition family
    kaniko_container: str = "kaniko"      # container name in that task-def
    kaniko_log_group: str = ""            # CloudWatch log group for build output
    build_subnets: str = ""               # comma-separated subnet ids
    build_security_group: str = ""        # egress-only SG id for the build task
    # Presigned-upload TTL and how long build-job rows live (DynamoDB TTL).
    build_upload_url_ttl_seconds: int = 900
    build_job_ttl_seconds: int = 3600
    # Tool-call analytics telemetry (see docs/tool-call-logging-spec.md).
    # Env name tags every event and keeps dev/prod records separable. Defaults
    # to "unknown" (not "prod") so a misconfigured task can't silently pollute
    # the prod partition; Terraform sets CUBE_CLOUD_ENV_NAME per stack.
    env_name: str = "unknown"  # set to "dev" | "prod" via env
    telemetry_enabled: bool = False  # kill-switch; enabled per-env via Terraform
    telemetry_bucket: str = ""  # per-env S3 bucket for the durable store
    telemetry_raw_prefix: str = "tool-calls/raw/"
    telemetry_curated_prefix: str = "tool-calls/curated/"
    # Payload-free twin of curated: the same rows with the free-text columns
    # dropped (see compaction.NARROW_EXCLUDED_COLUMNS). Physically separate files
    # on purpose — Athena reads S3 as the *caller*, so a narrow Glue table over
    # the curated files would be a convenience, not a boundary; only a separate
    # prefix can be scoped away by IAM. This is what a dashboard reads.
    telemetry_narrow_prefix: str = "tool-calls/narrow/"
    telemetry_overflow_prefix: str = "tool-calls/overflow/"
    # Per-field safety ceiling; larger fields spill to the overflow prefix.
    telemetry_field_max_bytes: int = 1_048_576  # 1 MiB
    # Tools whose RESPONSE body can carry secrets our key-based redaction can't
    # see — kubectl_exec (output such as env dumps) and acr_get_token (the
    # response IS a registry credential). For these we drop the response body +
    # error text but KEEP the (redacted) args: the kubectl command is operator
    # input, not secret output (secret retrieval is blocked at the tool), and
    # seeing which raw commands run tells us what to promote into first-class
    # tools. Comma-separated; extend without code change.
    telemetry_drop_response_tools: str = "kubectl_exec,acr_get_token"
    # Domains on which a plus-addressed login (`name+qualifier@domain`) is a TEST
    # ACCOUNT rather than a person: its rows carry actor_type="test" so distinct-user
    # counts can leave them out while the rows stay recorded. Home domains only, on
    # purpose — plus-addressing is OUR test convention, and a customer using a plus
    # alias as their only account is a real user. Comma-separated, lowercase.
    telemetry_test_account_domains: str = "edgescaleai.com"
    # Groundcover OTLP export — the primary/hot tier + future correlation layer.
    # One span per tool call. Enabled independently of the S3 archive so it can
    # be switched on once the per-env ingest creds are provisioned. Endpoint +
    # api key come from the secret (JSON: {"endpoint": "...", "api_key": "...",
    # optional "api_key_header": "apikey"}).
    otlp_enabled: bool = False
    otlp_secret: str = "cube-mcp/telemetry/otlp"
    # Console usage events (telemetry/console_events.py) — the console's analog of
    # the tool-call wrapper, recorded through the SAME sinks under source="console".
    # A sub-switch beneath `telemetry_enabled`: both must be on, so a stack with the
    # archive off cannot be made to emit console rows by this flag alone. Default
    # FALSE like every other flag here; set per-env in Terraform.
    telemetry_console_enabled: bool = False
    # A repeated SUCCESSFUL read of the same (session, event, cube, app) inside
    # this window is not recorded again. The logs page polls its route every 10s
    # and a cube page re-fetches on focus; without this an open logs tab is 360
    # "operations" an hour and active-user counting drowns in polls. Mutations
    # and errors are never suppressed. 0 disables. 300s collapses 30 polls into
    # one row. What it does NOT do: a logs tab left VISIBLE keeps polling, so it
    # still records one row per window (~288/day) and keeps that session in the
    # active-user count for as long as it stays open — a hidden tab records
    # nothing, because the SPA stops polling it. The bound on a visible tab is
    # the logs page's idle auto-pause, a separate SPA change (PR #297), not this.
    telemetry_console_suppress_seconds: int = 300

    # Console (browser UI — docs/console-spec.md).
    #
    # Master kill-switch. Defaults to FALSE and is set per-env in
    # infra/terraform/environments/*.tfvars, the same pattern as the telemetry
    # flags: off unless a stack explicitly turns it on, so a new or misconfigured
    # environment never exposes the surface by accident.
    #
    # This flag gates BOTH halves of the console together and that pairing is
    # load-bearing: the routes 404, AND the apex cookie-auth allowlist in
    # auth/middleware.py goes inert. Gating only the routes would leave prod with
    # a widened CSRF-reachable surface for a UI that isn't even served.
    console_enabled: bool = False
    # The cube page's AI tab: deploy AI Reactor models from the catalog
    # (docs/ai-reactor-deploy-spec.md). A sub-switch beneath `console_enabled`; both
    # must be on. Off: its routes 404 and the session reports `ai_enabled: false`.
    console_ai_enabled: bool = False
    # Which profiles may DEPLOY or REMOVE (any profile that can see a cube may view
    # its AI tab). Comma-separated profile names, or "*" for every profile, in which
    # case Apollo RBAC on the caller's own credentials is the only check. Starts with
    # the unscoped admin profile only and is widened deliberately.
    console_ai_write_profiles: str = "admin"
    # Secrets Manager id holding the
    # HMAC secret the CSRF token is derived from. Secret value JSON:
    # {"secret": "<random>"}. Absent ⇒ no token is minted and mutating console
    # routes fail closed (reads are unaffected).
    # No default on purpose. The secret is per-env (`<name_prefix>/console/...`),
    # so any literal here matches at most one stack — the previous
    # "cube-mcp/console/csrf-secret" matched NEITHER dev nor prod, and also fell
    # outside the IAM grant, making it a silent "secret unavailable" for anything
    # running without the env var. Terraform always sets
    # CUBE_CLOUD_CONSOLE_CSRF_SECRET on ECS; unset means unconfigured, which
    # csrf.py reports rather than chasing a bogus id.
    console_csrf_secret: str = ""
    # TTL stamped on keys minted by the console/browser cookie flow. Matches the
    # session cookie's 12h max-age so the credential and the cookie carrying it
    # expire together. The agent (session_id) flow is unaffected — it keeps
    # minting non-expiring CLI keys.
    console_key_ttl_seconds: int = 43200  # 12 hours
    # Per-profile TTL on the cached Apollo RBAC reads (LIST_ENVIRONMENTS +
    # MY_TEAMS) behind the console. Caches *visibility*, never authentication:
    # validate_key still runs on every request, so a revoked key fails
    # immediately regardless of this value.
    console_cache_ttl_seconds: float = 45.0
    # TTL on a cached /console/api/.../utilization payload, keyed (profile, cube,
    # window). SEPARATE from the visibility TTL above because it is bounding a
    # different thing: not Apollo latency but the console's largest single-request
    # amplification against a SHARED Groundcover budget. One tab load is 12 concurrent
    # `POST /api/metrics/query` calls, and the one org key carries 150 req/s / 1000
    # req/min across every backend, every `groundcover_*` MCP tool, the /status badge
    # ladder and the logs view's poll — so ~83 uncached tab loads a minute exhausts it
    # and Groundcover then rate-limits reads belonging to OTHER tenants.
    #
    # 30s is chosen against the STEP, not against the budget: the narrowest window
    # samples at 60s, so a cached payload can never be more than one point behind what
    # a fresh query would draw. Refresh is a button precisely so someone who wants
    # newer data can ask; this only bounds how often that costs 12 upstream calls.
    # 0 disables it, the same escape hatch `console_cache_ttl_seconds` has.
    console_utilization_cache_ttl_seconds: float = 30.0
    # TTL on a cached /console/api/cubes/{name}/services payload, keyed (profile, cube).
    # That read is the console's only kubectl-backed one and it now runs on EVERY
    # cube-page load (docs/console-spec.md §4.4f), so this bounds kubectl subprocesses
    # to one per (profile, cube) per TTL rather than one per view. Keyed by profile
    # because kubectl runs as the profile's own Teleport identity. A FAILED read is
    # held for `reads.SERVICES_FAILURE_TTL_SECONDS` only. The expose write path never
    # reads this cache — it enumerates fresh. 0 disables it.
    console_services_cache_ttl_seconds: float = 30.0
    # The console's per-cube view splits Apollo entities into apps and PLATFORM
    # components (docs/console-spec.md §4.9) with TWO lists, each comma-separated so
    # a change is an env var, not a code change. Anything matched by neither is an
    # "app" — fail-visible, so a new customer-facing product appears rather than
    # silently vanishing. Both lists are interim: once products carry a platform
    # label in Apollo, the label replaces them.
    #
    # EXACT product ids, case-insensitive, never a prefix. The default way to mark
    # a product as platform, and the only way for one in a group that also
    # publishes apps: `com.edgescaleai-cube`, `com.edgescaleai` and
    # `com.palantir.apollo` all do (`com.palantir.apollo:seat-forge` is an app on
    # 17 cubes), so none of those groups may go in the group list below.
    console_platform_product_ids: str = (
        "com.palantir.apollo:helm-chart-operator,"
        "com.palantir.apollo:vce-validator,"
        "com.palantir.apollo:node-diagnostics,"
        "com.palantir.apollo:telemetry-rules,"
        "com.edgescaleai:teleport-kube-agent-ecr,"
        "com.edgescaleai:groundcover-prereqs,"
        "com.edgescaleai-cube:esai-os-csr,"
        "com.edgescaleai-cube:esai-tailscale,"
        "com.edgescaleai-cube:esai-teleport-app-service,"
        "com.edgescaleai-cube:esai-groundcover,"
        "com.edgescaleai-cube:cubevts-builder,"
        "com.edgescaleai-cube:esai-cube-watchdog"
    )
    # WHOLE GROUPS only, for a vendor whose entire group is platform. An entry
    # matches the group and its subgroups at a `.` or `:` boundary, never as a bare
    # string prefix (so `com.teleport` does not swallow `com.teleportation-inc`).
    # A single product goes in `console_platform_product_ids` above, never here;
    # `test_console_platform_config.py` fails on a default entry holding a `:`.
    # NOT bare `com.palantir`: `com.palantir.demo` and `com.palantir.apollo` publish
    # apps. The setting's name says "prefixes" for history: it is live in prod.
    console_platform_product_prefixes: str = (
        "com.palantir.deployability,com.palantir.signals,"
        "com.teleport,com.groundcover"
    )

    # Feedback -> Jira Service Management (tools/feedback.py).
    #
    # Master kill-switch, DEFAULT FALSE like the telemetry and console flags: a
    # new or misconfigured stack never writes into the customer-facing CF board
    # by accident, and merging to main ships the code while the per-env tfvar
    # decides whether prod actually submits.
    jira_enabled: bool = False
    # Secrets Manager id holding the Atlassian service-account OAuth 2.0
    # client-credentials pair. Secret value JSON:
    # {"client_id": "...", "client_secret": "..."}
    jira_oauth_secret: str = "cube-mcp/jira/oauth"
    # Atlassian cloud id + the numeric JSM service desk id for project CF. No
    # defaults: the credential is write-only and cannot discover either, so an
    # unset value must fail loudly rather than post into the wrong desk.
    jira_cloud_id: str = ""
    jira_service_desk_id: str = ""

    # Freshservice -> support tickets from the console's "problem or question" form
    # (tools/freshservice.py). Feature requests still go to the Jira CF board.
    #
    # Master switch, DEFAULT FALSE like every other integration flag here: merging to
    # main ships the code and the per-env tfvar decides whether a stack files real
    # tickets into a real helpdesk queue.
    freshservice_enabled: bool = False
    # The Freshservice tenant, e.g. `edgescaleai.freshservice.com`. A bare domain or a
    # full origin both work.
    #
    # NO DEFAULT, and specifically not one derived from the product name: the product
    # is "Edgeport" but the tenant is `edgescaleai.freshservice.com` — and
    # `edgeport.freshservice.com` 404s. A wrong-but-plausible default here would send
    # real support requests into the void, so an unset value must fail loudly.
    freshservice_domain: str = ""
    # Secrets Manager id holding the API key. Value JSON: {"api_key": "..."}.
    freshservice_api_key_secret: str = "cube-mcp/freshservice/api-key"
    # LOCAL DEVELOPMENT ONLY: the key inline, bypassing Secrets Manager. Terraform must
    # never set this — an ECS task-definition env var is readable via
    # `ecs:DescribeTaskDefinition` and printed by `terraform plan`. Same rule as
    # `inventory_token`; `_load_api_key` warns whenever this path is taken.
    freshservice_api_key: str = ""

    # Cube inventory join (inventory/) -- customer, site label, serial, status and
    # location for the console, which Apollo does not carry (docs/console-spec.md
    # OI-2).
    #
    # Master switch, DEFAULT FALSE like the console, telemetry and Jira flags: a new
    # or misconfigured stack shows exactly what it showed before this feature, and
    # merging to main ships the code while the per-env tfvar decides whether a stack
    # joins anything.
    inventory_enabled: bool = False
    # "api" (the real edgescale-inventory service) or "simulated" (deterministic
    # fictional records, inventory/simulated.py).
    #
    # DEFAULTS TO "api" ON PURPOSE, even though the real backend needs a credential
    # that a fresh stack does not have. Defaulting to "simulated" would mean a stack
    # enabled without a token silently renders INVENTED customer names and site
    # labels on a customer-facing console -- fabricated data presented as fact, which
    # is far worse than the blank fields an unauthenticated "api" mode produces. So
    # the unsafe mode is the one you have to ask for by name; `lookup` additionally
    # stamps `simulated: true` onto every payload it builds, and the UI badges it.
    inventory_mode: str = "api"
    # Stage base URL, e.g. https://<id>.execute-api.us-west-2.amazonaws.com/prod.
    # No default: the prod and dev-testing stages live in DIFFERENT AWS accounts, so
    # any literal here would be wrong for at least one stack -- the same reasoning
    # that left console_csrf_secret without one.
    inventory_api_base: str = ""
    # Secrets Manager id holding the inventory API bearer. Value JSON:
    # {"token": "<bearer>"}.
    inventory_token_secret: str = "cube-mcp/inventory/api-token"
    # LOCAL DEVELOPMENT ONLY: the bearer inline, bypassing Secrets Manager.
    #
    # Exists because the join cannot otherwise be exercised on a laptop — reading the
    # real secret needs AWS credentials for the ECS task role. Checked BEFORE
    # Secrets Manager so `CUBE_CLOUD_INVENTORY_TOKEN=... uv run cube-cloud` just
    # works.
    #
    # Terraform deliberately does NOT set this, and must not: an ECS task definition
    # environment variable is readable by anyone with `ecs:DescribeTaskDefinition`
    # and is printed by `terraform plan`, which is exactly the exposure Secrets
    # Manager exists to avoid. `_load_token` logs a warning whenever this path is
    # taken, so a stack accidentally running on it says so rather than looking
    # identical to one that is not.
    inventory_token: str = ""
    # TTL on the cached whole-fleet index. Much longer than console_cache_ttl_seconds
    # because inventory facts are slow-moving (a site label or customer changes on
    # human timescales, not per deploy) and the read is a full-fleet scan. The cost of
    # staleness is a newly-relabelled cube showing its old label for a few minutes.
    inventory_cache_ttl_seconds: float = 300.0
    # Per-request timeout against the inventory API. Deliberately well under the
    # console's own patience: a slow inventory read must degrade to "no labels"
    # rather than hold a cube list hostage.
    inventory_timeout_seconds: float = 15.0
    # Above how many authorized cubes to read the whole fleet in one sweep instead
    # of one lookup per cube. 0 (the default) means NEVER sweep.
    #
    # The per-cube path is the point of the design: inventory is asked only about the
    # cubes Apollo already authorized, so no other tenant's record crosses the wire
    # or enters this process. The sweep exists only for a caller whose scope IS the
    # fleet — an admin — where N lookups cost N server-side partition scans and pull
    # exactly the same data one sweep would, making the sweep cheaper at identical
    # exposure. Raising this is a latency decision for that case, never a way to
    # widen what a scoped tenant pulls: a tenant authorized for 3 cubes is below any
    # sensible threshold and always takes the per-cube path.
    inventory_fleet_sweep_threshold: int = 0

    # Cube GPS location (ic2/): each cube router's latest GPS position from Peplink
    # InControl2, joined to the cube through inventory's router serial. Off by
    # default, like every other feature flag here.
    ic2_enabled: bool = False
    # Secrets Manager id holding THIS stack's InControl2 API client, as
    # {"client_id": "...", "client_secret": "..."}. No default: IC2 allows one live
    # token per client and a new login cancels the last, so two stacks sharing a
    # client would keep logging each other out. Terraform passes the stack's own
    # `<name_prefix>/ic2/client`, which keeps dev and prod apart by construction.
    ic2_credentials_secret: str = ""
    # LOCAL DEVELOPMENT ONLY: a client pair inline, bypassing Secrets Manager. Use
    # your own IC2 client, never a deployed stack's (logging in with it would cancel
    # that stack's token). Terraform must not set these, for the reason given at
    # `inventory_token`; `_load_credentials` warns whenever this path is taken.
    ic2_client_id: str = ""
    ic2_client_secret: str = ""
    ic2_api_base: str = "https://api.ic.peplink.com"
    # How long one org-wide `last_loc` pull is reused, give or take a minute so
    # tasks drift apart. Routers report every few minutes at best, so five minutes
    # loses little and keeps logins rare.
    ic2_cache_ttl_seconds: float = 300.0
    # Per-request timeout. Short: a slow IC2 must degrade one row, not hold a page.
    ic2_timeout_seconds: float = 10.0
    # Deadline for a whole refresh (login, org list, two calls per org). Each call
    # could otherwise come in just under its own timeout and the total run long.
    ic2_refresh_deadline_seconds: float = 10.0

    # Cube online/offline badge (docs/console-spec.md §4.14). How recent the newest
    # Groundcover log must be for a cube to read "online".
    #
    # 15 minutes, deliberately generous. The signal is log freshness, and nothing
    # guarantees a workload logs on a schedule — so a tight threshold would flip a
    # genuinely-healthy but quiet cube to "offline", which is the failure mode that
    # costs the badge its credibility. Raise it if quiet cubes flap; lower it only
    # with evidence that the fleet logs continuously.
    console_cube_online_threshold_seconds: int = 900

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # Browser app proxy (Phase 2a) per-session rate limit -- security floor,
    # not a precise quota. See browser_proxy/rate_limit.py.
    app_proxy_rate_limit_max: int = 120
    app_proxy_rate_limit_window_seconds: float = 10.0

    # Self-service password reset (auth/login_flow.py). Cognito enforces its own
    # per-user budget on forgot-password -- "between 5 and 20 attempts" in an
    # hour, by its docs -- and ours must stay under the FLOOR of that range, not
    # its ceiling. An earlier revision set 5 per 900s and called itself "tighter
    # than Cognito"; that is 20/hour, i.e. exactly the ceiling and 4x the floor,
    # so Cognito's own throttle was reachable. That matters because under
    # LEGACY a non-existent username raises UserNotFoundException before any
    # per-user counter is consulted -- so Cognito's throttle can ONLY be reached
    # for an address that has an account, which makes it an existence oracle.
    # 5 per 3600s keeps it out of reach; `_forgot_password` swallowing that
    # exception is the belt to this braces, since arithmetic here is exactly the
    # kind of thing that drifts.
    #
    # Two budgets because the abuse shapes differ: per-email bounds mailbox spam
    # for one victim, per-IP bounds a spray across many addresses AND caps how
    # many request bodies one caller can make us buffer. An office behind one
    # NAT must not be locked out by the tighter of the two.
    password_reset_rate_limit_window_seconds: float = 3600.0
    password_reset_rate_limit_per_email: int = 5
    password_reset_rate_limit_per_ip: int = 50
    # Both keys are attacker-varied, unlike the app proxy's session hashes, so
    # the limiter MUST be capped -- see browser_proxy/rate_limit.py. `max_keys`
    # bounds key COUNT; the key itself is a fixed-width hash so it cannot bound
    # bytes-per-key too (see `_reset_email_allowed`).
    password_reset_rate_limit_max_keys: int = 10000
    # Hard cap on a reset request body, enforced by streaming rather than by
    # trusting Content-Length. These are the only unauthenticated POSTs that
    # parse a body, and a login form is tiny; the app proxy's 25 MiB is sized
    # for file uploads and is wildly wrong here.
    password_reset_max_body_bytes: int = 16 * 1024

    # Browser app proxy (Phase 2a) request body cap -- bounds per-request
    # memory use, since the body is fully buffered before dialing the app.
    app_proxy_max_body_bytes: int = 25 * 1024 * 1024  # 25 MiB

    model_config = {"env_prefix": "CUBE_CLOUD_"}


settings = Settings()
