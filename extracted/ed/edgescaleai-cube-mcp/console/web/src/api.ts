/**
 * Console API client.
 *
 * Every call is same-origin and relies on the HttpOnly `cmcp_session` cookie —
 * the browser attaches it automatically and JS can never read it. There is no
 * token to store, nothing in localStorage, and no Authorization header here.
 *
 * `credentials: 'same-origin'` is explicit rather than relying on the default,
 * and `Accept: application/json` matters: `APIKeyMiddleware` bounces an
 * unauthenticated *HTML* request to the login page but returns 401 JSON to
 * everything else, so asking for JSON keeps an expired session a clean 401
 * instead of a login page parsed as JSON.
 */

export const CONSOLE_BASE = '/console'

/** A 401 means the session is gone (expired, or revoked by signing out). */
export class SessionExpired extends Error {
  constructor() {
    super('Session expired')
    this.name = 'SessionExpired'
  }
}

/** A 404. For a cube this is deliberately ambiguous server-side — "not yours" and
 *  "does not exist" return the same status so the API cannot be used to enumerate
 *  fleet cube names — so callers must not render copy claiming one or the other. */
export class NotFound extends Error {
  /** True when the server said the CALLER's environment list is truncated, i.e. the
   *  full list could not be read and the cube may be among the ones not fetched
   *  (OI-6). Lets the page stop blaming Apollo team roles without revealing whether
   *  the cube exists.
   *
   *  Not "on a page that is not being fetched" any more: the environment read
   *  drains every page, so this means the drain itself stopped early. */
  readonly environmentsTruncated: boolean
  constructor(environmentsTruncated = false) {
    super('Not found')
    this.name = 'NotFound'
    this.environmentsTruncated = environmentsTruncated
  }
}

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${CONSOLE_BASE}${path}`, {
    method: 'GET',
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  })
  if (res.status === 401) throw new SessionExpired()
  if (res.status === 404) {
    const body = await res.json().catch(() => null)
    throw new NotFound(Boolean(body?.environments_truncated))
  }
  if (!res.ok) {
    // The API always returns an object with `error` on failure; fall back to the
    // status if the body is something unexpected (a proxy error page, say).
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.error ?? `Request failed (${res.status})`)
  }
  return res.json() as Promise<T>
}

export type Session = {
  profile: string | null
  user_domain: string | null
  actor_type: string | null
  csrf_token: string | null
  /** False when the server could not mint a CSRF token, so writes will refuse. */
  mutations_available: boolean
  /** Mirrors CUBE_CLOUD_JIRA_ENABLED. False on a stack where a feedback submission
   *  would only fail — the "Send feedback" entry point hides itself rather than
   *  showing and failing at click time, the same rule `mutations_available` follows. */
  feedback_enabled: boolean
  /** The app companies this profile holds — who it can share an exposed app with.
   *  `held` is home first. Null when the server could not resolve them; an unscoped
   *  (admin) profile holds none by name and reaches every app. */
  app_companies?: AppCompanies | null
  /** Whether this stack lets one app be visible to several companies. False (or
   *  absent, from a server predating it) on a baseline stack, where every app keeps a
   *  single company and the page behaves exactly as it always has. */
  multi_company?: boolean
  /** Which companies may share one app on this stack: null (or absent) for any. Only
   *  meaningful when `multi_company` is true: on a baseline stack NOTHING combines,
   *  whatever this says (`can_combine` checks the stack first). The expose picker uses it
   *  to say before the click that a join would be refused. */
  combinable?: string[] | null
  /** Mirrors CUBE_CLOUD_CONSOLE_AI_ENABLED: whether the cube page shows its AI tab.
   *  Absent (a server predating it) means off. */
  ai_enabled?: boolean
  /** Whether this stack has the GPS feature on. The landing page offers its List / Map
   *  switch only when true; absent (a server predating it) reads as off. */
  gps_enabled?: boolean
}

export type AppCompanies = {
  home: string
  held: string[]
  unscoped: boolean
}

export const fetchSession = () => getJson<Session>('/api/session')

/** Inventory facts for one cube, from `edgescale-inventory` rather than Apollo
 *  (docs/console-spec.md §4.13, closing OI-2). Every field is a plain string and
 *  may be empty — a cube can exist in Apollo before anyone files its label — so
 *  the UI must render an em dash rather than assuming presence.
 *
 *  Fetched by the CUBE PAGE only, never by the list: `/inventory/lookup` is a
 *  server-side partition scan (~3.3s cold), so joining it onto the list cost an
 *  admin ~45s for a page that used to be instant. One lookup for the cube you
 *  opened, instead of one per cube you can see. */
export type Inventory = {
  customer: string
  label: string
  environment: string
  serial: string
  /** Lifecycle enum: built | pending | online | active | staged | allocated |
   *  inactive. Rendered via `statusTone`, which returns a neutral tone for an
   *  unrecognized value rather than guessing — a new enum member must not
   *  render as if it were healthy. */
  status: string
  location: string
  /** The Peplink router's MAC, as inventory stores it (case and separators are
   *  not normalized). The ONLY MAC the console shows — the host/BMC MACs are kept
   *  out server-side as network fingerprinting. Empty when unset or `TBD`.
   *  Optional because a cube-cloud task that predates the field omits it, and a
   *  rolling deploy can pair this bundle with that task. */
  router_mac?: string
}

/** Which of the three "no labels" states the server is in. Collapsing any two of
 *  these would send someone debugging the wrong thing, so they stay distinct all
 *  the way to the browser. */
export type InventorySource = {
  /** False when the stack has not opted into the join. The UI shows nothing at
   *  all — not an error, not a placeholder. */
  enabled: boolean
  /** False when the backend could not be reached. Distinct from "enabled and
   *  empty", the same way `cube_services` keeps "could not look" apart from
   *  "nothing there". */
  available: boolean
  /** True when the records are deterministic fictional stand-ins. MUST be
   *  surfaced visibly — see the banner in CubeList/CubePage. Invented customer
   *  names rendered as fact on a customer-facing console would be worse than
   *  showing no inventory data at all. */
  simulated: boolean
}

/** Rolled up from the cube's Apollo agents, never read off `agents[0]`.
 *
 *  `mixed` is a real state — 6 cubes on the live fleet have agents in disagreeing
 *  states — and `none` ("Apollo has no agent record") is a different fact from
 *  `never_reported` ("the agent exists and has never reported"). `unknown` is a
 *  status Apollo added that this build does not recognize. */
export type AgentStatus =
  | 'connected'
  | 'stale'
  | 'never_reported'
  | 'mixed'
  | 'unknown'
  | 'none'

export type Cube = {
  name: string
  rid: string
  namespace: string
  space_id: string
  cluster: string
  /** Apollo's `displayMetadataV2.displayName`, or "" — populated on roughly a third
   *  of the fleet, and server-side any value that merely echoes the id or name is
   *  dropped. A LABEL, never a key: the URL, search and every API call still use
   *  `name`. */
  display_name: string
  agent_status: AgentStatus
  /** Newest `lastUpdated` across the cube's agents (RFC3339), or "". Empty for a
   *  never-reported agent, which legitimately has no timestamp. */
  agent_last_updated: string
}

/** Note the response is an OBJECT, not a bare array — a top-level JSON array is
 *  historically readable cross-origin via `<script src>`, so the API never
 *  returns one. */
export type CubeList = { cubes: Cube[]; count: number; truncated: boolean }

export const fetchCubes = () => getJson<CubeList>('/api/cubes')

/** One app the viewer can open, from the fleet Apps page (docs/console-spec.md §4.22).
 *  The server lists only apps the viewer can open, so there is no `reachable`. */
export type FleetApp = {
  /** Qualified Teleport app name. */
  name: string
  /** Browser-app-proxy URL. Empty for a TCP app, which has no browser link. */
  url: string
  /** In-cluster target. */
  uri: string
  /** Companies the app is visible to. For a scoped viewer, ONLY the ones it holds;
   *  an admin gets the whole audience. Empty means no company can open it. */
  companies: string[]
  /** Label tokens that are not company names (admins only). */
  unreadable_companies: string[]
  /** The cube it runs on, when that is known and the viewer can see the cube. */
  cube: string
  /** Apollo's display name for that cube, or "". */
  cube_display: string
}

export type FleetApps = {
  /** False when the app list could not be read; `apps` is then empty and means nothing. */
  available: boolean
  /** False when cube names could not be read; apps are then listed without cubes. */
  cubes_available: boolean
  apps: FleetApp[]
}

export const fetchFleetApps = () => getJson<FleetApps>('/api/apps')

export type App = {
  id: string
  name: string
  entity_name: string
  product_id: string
  /** "app" | "platform" — a deterministic product-group classification, not a guess.
   *  An unrecognized product group is reported as "app" so a new customer-facing
   *  product appears rather than silently vanishing. */
  kind: string
  lifecycle: string
  version: string
  health: string
  rollout: string
  config_status: string
  blockers: string[]
  plan_state: string
  /** Publicly reachable services this entity exposes. Empty for most entities. */
  exposed: Exposed[]
}

/** One app published through Teleport and reachable via the browser app proxy. */
export type Exposed = {
  /** Qualified Teleport app name, `<app>-<cube>`. */
  name: string
  /** Browser-app-proxy URL — `https://<name>.<apex>`, reachable with the session
   *  cookie the console already holds. NOT Teleport's own `…teleport.sh` address,
   *  which would require a Teleport account. Empty if the apex is unconfigured. */
  url: string
  /** In-cluster target, e.g. `http://litellm.esai-sovereign-ai.svc.cluster.local:4000`.
   *  Shown as a title so two services of one entity are tellable apart. Empty for an
   *  app the caller cannot reach. */
  uri: string
  /** Who the app is visible to — its app companies, sorted. */
  companies: string[]
  /** Label tokens that are not app company names (a live `Groundcover`). A role matching
   *  one can reach the app, so they are shown; the console cannot add or remove them. */
  unreadable_companies?: string[]
  /** Whether the caller can open it. An unreachable app is listed so the cube's users
   *  know it exists and for whom, with no URL and no URI. */
  reachable: boolean
  /** The Service port it points at, parsed server-side from its URI, so the cube page
   *  can draw it on that port's line by EQUALITY on these three fields — the browser
   *  never parses a URI. Sent for an unreachable app too (it names one of the cube's
   *  own Services, never how the app is reached). `null` when the URI names no
   *  `<service>.<namespace>` and port; absent from a server predating the field. Both
   *  render in "Also exposed". docs/console-spec.md §4.4f. */
  target?: ServiceTarget | null
}

export type ServiceTarget = { namespace: string; service: string; port: number }

export type CubeDetail = {
  cube: Cube
  apps: App[]
  platform: App[]
  /** Exposed apps whose URI matched no entity. Surfaced rather than dropped — the
   *  join is a heuristic over Helm's Service naming, so a miss must stay visible. */
  exposed_unmatched: Exposed[]
  counts: { apps: number; platform: number; exposed: number }
  truncated: boolean
  /** The exposed-apps read succeeded. When false, `exposed` is empty because the page
   *  could not LOOK, not because nothing is exposed — so no port may read "Not exposed".
   *  Absent from a server predating it; read as true. §4.4f. */
  exposed_available?: boolean
  /** Every app on the cube is listed. False for a scoped caller on a `map` stack, where
   *  another company's app is filtered out, so "not exposed" holds only for this caller. */
  exposed_complete?: boolean
}

export type LogRow = {
  timestamp: string
  /** Lowercased: "info" | "warn" | "error" | "debug" | "" — Groundcover's own value,
   *  not normalized, so an unrecognized level renders neutral rather than as info. */
  level: string
  message: string
  workload: string
  namespace: string
  container: string
  pod: string
}

export type AppLogs = {
  cube: string
  app: string
  /** The Groundcover workloads this app owns. An app can own several — minio runs
   *  an S3 API and a console; a dbt app runs three CronJobs. */
  workloads: { workload: string; namespace: string; kind: string }[]
  rows: LogRow[]
  window_minutes?: number
  truncated: boolean
  /** No workload is reporting: a CronJob between runs, or a cube not wired to
   *  Groundcover. Not an error. */
  no_workloads?: boolean
  /** The window the server actually queried. Differs from what was asked for when
   *  `since` was clamped, so the next poll must advance from THIS, not from the
   *  requested value. */
  start?: string
  end?: string
  /** True when the server treated this as an incremental poll. */
  incremental?: boolean
}

/** `since` makes this an incremental poll: the server queries only from that
 *  timestamp, so a 10s tick transfers a few rows instead of the whole window. It is
 *  clamped server-side to a 24h lookback, so a stale value cannot become a
 *  full-retention scan. */
export const fetchAppLogs = (cube: string, app: string, since?: string) =>
  getJson<AppLogs>(
    `/api/cubes/${encodeURIComponent(cube)}/logs?app=${encodeURIComponent(app)}` +
      (since ? `&since=${encodeURIComponent(since)}` : ''),
  )

/** One health check reporting anything other than HEALTHY. `message` is the app's
 *  OWN text (Witchcraft's "actionable" check message), cleaned server-side: no
 *  newlines, no URL credentials, capped length. */
export type HealthCheckIssue = {
  /** Apollo's `ApolloHealthStatus`: TERMINAL, ERROR, WARNING, REPAIRING, SUSPENDED,
   *  DEFERRING, NO_DATA, UNKNOWN_HEALTH. */
  state: string
  check: string
  message: string
  pod: string
  container: string
  /** When that pod's report last changed. Server-computed. */
  updated_age_seconds: number | null
}

/** A container reporting not live or not ready — for apps with no health checks of
 *  their own, often the only evidence of why Apollo says Error. */
export type ContainerIssue = {
  pod: string
  container: string
  live: boolean
  ready: boolean
  updated_age_seconds: number | null
}

/** Why one app has the status it has — the health checks behind Apollo's roll-up.
 *
 *  - `issues`        something in the report is unhealthy (checks and/or containers)
 *  - `clear`         Apollo reported, and nothing in the report is unhealthy — for an
 *                    app in Error, that means Apollo's status is NOT explained by what
 *                    it exposes, which must be said rather than shown as empty
 *  - `not_reported`  Apollo holds no node health for this app at all
 *  - `unavailable`   we could not read it; never an all-clear */
export type AppHealth = {
  cube: string
  app: string
  health: string
  state: 'issues' | 'clear' | 'not_reported' | 'unavailable'
  checks: HealthCheckIssue[]
  containers: ContainerIssue[]
  passing_checks: number
  pods: number
  reported_at: string
  /** When the cube last reported for this app. Server-computed. */
  reported_age_seconds: number | null
  /** Issues left out of a very long list. */
  omitted: number
  /** The pod list could not be read to the end. */
  truncated: boolean
}

export const fetchAppHealth = (cube: string, app: string) =>
  getJson<AppHealth>(
    `/api/cubes/${encodeURIComponent(cube)}/health?app=${encodeURIComponent(app)}`,
  )

/** One publishable port on an in-cluster Service. */
export type ServicePort = {
  port: number
  protocol: string
  /** The exact string handed to expose. Built server-side by `fetch_services` so the
   *  console and the MCP tool cannot drift — a wrong port surfaces much later as
   *  Teleport "context deadline exceeded". Never reconstruct it client-side. */
  app_uri: string
  /** The same target as `tcp://`, for a service that does not speak HTTP. Note the
   *  `protocol` field above is the Kubernetes L4 protocol and reads "TCP" for every
   *  ordinary HTTP service too — it is NOT a signal about which of these to use. */
  app_uri_tcp: string
}

export type ServiceCandidate = {
  service: string
  namespace: string
  type: string
  ports: ServicePort[]
}

export type ServiceCandidates = {
  cube: string
  /** Keyed by owning entity name, via the same join that attributes exposed Services
   *  and Groundcover workloads. */
  by_entity: Record<string, ServiceCandidate[]>
  /** Services the join could not attribute. Still offered — the join is a Helm-naming
   *  convention and an operator may well want to expose one of these. */
  unattributed: ServiceCandidate[]
  /** Non-empty when kubectl/tbot failed. "Could not look" is NOT "nothing to expose",
   *  and the picker must say which. */
  error: string
  infra_hidden: number
}

/** kubectl-backed, so the cube page fetches it as its OWN request on load, beside the
 *  apps list rather than inside it: a slow or unreachable cube delays only the "Not
 *  exposed" lines, never the apps or their links. Cached server-side per
 *  (profile, cube). docs/console-spec.md §4.4f. */
export const fetchServices = (cube: string) =>
  getJson<ServiceCandidates>(`/api/cubes/${encodeURIComponent(cube)}/services`)

export type ExposeResult = {
  ok: boolean
  state?: 'applied' | 'pending' | 'refused'
  error?: string
  exposed: Exposed[]
}

/** Publish one in-cluster service. `uri` must be an `app_uri` the server itself
 *  enumerated — it re-checks, and refuses anything else. */
/** Header rewrites applied by the Teleport app service before your app sees the
 *  request. Two NAMED fields rather than a free-form list: the console's field
 *  set is fixed server-side, which is what keeps it an enumerated-args surface.
 *  Empty strings mean "no rewrite" and are omitted by the server. */
export type RewriteHeaders = { host: string; origin: string }

/** The values an Origin-checking app needs, for prefilling the form.
 *
 *  Teleport replaces the forwarded Host with the internal service address, so an
 *  app comparing Origin against Host sees them disagree. Pointing both at the
 *  app's own public URL fixes it. Built from `window.location.host` because the
 *  console is served FROM the apex, so that is the same value the server's
 *  `browser_app_url` uses — no round-trip and no second source of truth. */
export function recommendedRewrite(app: string, cube: string): RewriteHeaders {
  const host = `${dnsLabel(app)}-${dnsLabel(cube)}.${window.location.host}`
  return { host, origin: `https://${host}` }
}

/** Mirror of the server's `_sanitize_label`: lower-case, every run of anything
 *  outside [a-z0-9-] collapsed to one '-', ends trimmed.
 *
 *  Duplicating the rule is deliberate but not free — a naive `${app}-${cube}`
 *  is wrong for any cube with a capital (`Lear-Hammond-2` stores as
 *  `sqlpad-lear-hammond-2`), which is the same mismatch that once broke
 *  `_bare_app_name`. Drift here only mis-fills a field the operator can see and
 *  edit, so it is contained; the server never trusts this value. */
export function dnsLabel(raw: string): string {
  return raw.trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '')
}

export async function exposeApp(
  cube: string,
  app: string,
  uri: string,
  csrfToken: string,
  rewrite?: RewriteHeaders,
  company?: string,
): Promise<ExposeResult> {
  const res = await fetch(
    `${CONSOLE_BASE}/api/cubes/${encodeURIComponent(cube)}/expose`,
    {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Console-CSRF': csrfToken,
      },
      body: JSON.stringify({
        app,
        uri,
        ...(rewrite
          ? { rewrite_host: rewrite.host, rewrite_origin: rewrite.origin }
          : {}),
        ...(company ? { company } : {}),
      }),
    },
  )
  if (res.status === 401) throw new SessionExpired()
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.error ?? `Request failed (${res.status})`)
  }
  return res.json() as Promise<ExposeResult>
}

export type UnexposeResult = {
  /** The request was accepted. NOT "the app is already gone" — see `state`. */
  ok: boolean
  /** `applied` — confirmed gone from Apollo. `pending` — accepted, but still listed
   *  after the server's retries; the module update is a change request and Apollo
   *  gives no read-your-write guarantee, so this is not a failure. `refused` — the
   *  write was never attempted. */
  state?: 'applied' | 'pending' | 'refused'
  error?: string
  /** The cube's remaining exposed apps, so the page settles with no refetch. */
  exposed: Exposed[]
}

/** Just the exposed apps for a cube — one Apollo query, meant to be polled while a
 *  removal is still rolling out. */
export type ExposedList = {
  cube: string
  exposed: Exposed[]
  count: number
  /** The exposed-apps read succeeded, so an empty `exposed` means nothing is exposed.
   *  Unlike the cube detail's field of the same name, a missing value here reads as
   *  FALSE: the only conclusion drawn from it is "nothing is exposed on this cube",
   *  so the unknown case must not reach it. */
  exposed_available?: boolean
} & RolloutStatus

/** Whether the cube has actually stopped serving.
 *
 *  Removing an app from the module's `apps` variable changes Apollo's DECLARED state.
 *  The Teleport app-service Helm release then has to roll out — measured at 2–3 minutes —
 *  before the app stops answering. So "Apollo no longer lists it" and "it is off the
 *  internet" are different facts, and the UI must not conflate them for an action
 *  whose entire purpose is the second one.
 *
 *  Derived from that entity's plan/rollout status, NOT the module installation's
 *  `state`, which reports `Installed` throughout and never moves. */
export type RolloutStatus = {
  rollout_state?: string
  rollout_settled?: boolean
  /** What the read SAW, from `reads.rollout_of`, and the only field a rollout wait may
   *  branch on. `rollout_settled: false` alone was both "a plan is running" and "we
   *  could not read the entity"; only `in_flight` is evidence a rollout started.
   *  `absent` is a complete read with no app-service entity, which a teardown leaves.
   *  Missing (a server predating it) reads as `unknown`. */
  rollout_phase?: RolloutPhase
}

export type RolloutPhase = 'in_flight' | 'settled' | 'unknown' | 'absent'

export const fetchExposed = (cube: string) =>
  getJson<ExposedList>(`/api/cubes/${encodeURIComponent(cube)}/exposed`)

/** Stop publishing one app.
 *
 *  `csrfToken` comes from `/api/session` and is required — the server verifies it
 *  against `HMAC(secret, key_id)` and refuses without it. It is passed in rather
 *  than read from module state so a caller cannot accidentally send `null`. */
export async function unexposeApp(
  cube: string,
  app: string,
  csrfToken: string,
  /** The company to take off the app (default: the caller's home company). The app
   *  stays exposed to anyone else it is visible to. */
  company?: string,
): Promise<UnexposeResult> {
  const res = await fetch(
    `${CONSOLE_BASE}/api/cubes/${encodeURIComponent(cube)}/unexpose`,
    {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Console-CSRF': csrfToken,
      },
      body: JSON.stringify(company ? { app, company } : { app }),
    },
  )
  if (res.status === 401) throw new SessionExpired()
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.error ?? `Request failed (${res.status})`)
  }
  return res.json() as Promise<UnexposeResult>
}

/** A cube's hardware specification, from the same inventory record as `Inventory`
 *  — so the Hardware tab costs no extra request.
 *
 *  Every value is a plain string (numbers included, so the UI renders rather than
 *  formats) or an array of strings, already placeholder-cleaned server-side: the
 *  real fleet stores `TBD` and `(NEEDS TO BE SET IN 'CUBE VERSIONS')` in these
 *  fields, and `records.py` maps both to empty. An empty value means "not
 *  recorded", and roughly half the fleet is sparse, so the table omits empty rows
 *  rather than rendering a wall of dashes.
 *
 *  Deliberately ABSENT, and not to be added without a second thought: component
 *  serials, MAC addresses, and BIOS/BMC firmware revisions. See
 *  `inventory/records.py::HARDWARE_KEYS` for why each one is excluded. */
export type Hardware = {
  server_manufacturer: string
  server_model: string
  motherboard_manufacturer: string
  motherboard_model: string
  cpu_manufacturer: string
  cpu_model: string
  cpu_cores: string
  cpu_threads: string
  /** MHz, and stored WITHOUT a unit unlike `memory_speed` — the table appends one
   *  only when the value is purely numeric, so a future "4.1 GHz" is not mangled. */
  cpu_max_clock: string
  memory_total: string
  memory_type: string
  memory_speed: string
  memory_manufacturer: string
  memory_ecc: string
  memory_dimm_count: string
  memory_dimm_size: string
  memory_dimm_locators: string[]
  ssd_manufacturer: string
  ssd_model: string
  ssd_type: string
  /** One entry per drive, so its length is the drive count. */
  ssd_capacities: string[]
  gpu_manufacturers: string[]
  gpu_models: string[]
  gpu_memories: string[]
}

/** The cube page's inventory payload, backing BOTH tabs.
 *
 *  `inventory` is null when the join is disabled and when inventory has no record;
 *  `inventory_source` distinguishes those plus "the backend could not be reached".
 *  `hardware` is null when there is no record OR when the record has no hardware
 *  on file at all — an ordinary state for about half the fleet. */
export type CubeInventory = {
  cube: string
  inventory: Inventory | null
  hardware: Hardware | null
  /** False when inventory holds MORE THAN ONE record claiming this cube and the
   *  join refused to pick between them (`inventory/client.py::_exact_match`).
   *
   *  A third outcome, deliberately not folded into either of the other two.
   *  `inventory: null` with `resolved: true` means inventory genuinely has no
   *  record — ordinary, since a cube can exist in Apollo before anyone files its
   *  label — and sending someone to create a label that already exists is the wrong
   *  instruction. `available: false` would blame the backend for answering
   *  correctly. This is a data problem in inventory, and only its own state says so.
   *
   *  Absent on responses from a cube-cloud older than this field; `?? true` at every
   *  read site so a missing value reads as the ordinary case rather than as a
   *  conflict nobody has. */
  resolved?: boolean
  inventory_source: InventorySource
}

/** Its own request, fetched alongside the cube detail rather than inside it, so a
 *  slow inventory read never delays the apps list. Same pattern as
 *  `fetchServices`. A 404 here means the same non-enumerable "not yours or does
 *  not exist" as the detail endpoint. */
export const fetchCubeInventory = (name: string) =>
  getJson<CubeInventory>(`/api/cubes/${encodeURIComponent(name)}/inventory`)

/** Where a cube's router last reported its GPS position (`reads.cube_gps`).
 *
 *  A LIVE reading, kept apart from inventory's typed-in Location. Each state is its
 *  own: `unavailable` is "we couldn't look" and is never shown as `no_position`
 *  ("it never reported one"); `unmatched` is an inventory gap, not a GPS one.
 *  `lat`/`lng` are set for reported, stale and time_unknown; `reported_at` and
 *  `age_seconds` only for reported and stale. `age_seconds` is server-computed, so a
 *  skewed browser clock can't change it. */
export type GpsState =
  | 'reported'
  | 'stale'
  | 'time_unknown'
  | 'no_position'
  | 'unmatched'
  | 'not_found'
  | 'unavailable'

export type Gps = {
  state: GpsState
  /** The nearest town ("Denver, CO", "Toronto, Canada"), named server-side from an
   *  offline gazetteer. Null when there is no position, no town nearby, or the
   *  gazetteer could not be read; the row then shows coordinates. */
  place: string | null
  lat: number | null
  lng: number | null
  reported_at: string | null
  age_seconds: number | null
}

export type CubeGps = {
  cube: string
  /** Null when the feature is off on this stack. */
  gps: Gps | null
  gps_source: { enabled: boolean; available: boolean }
}

/** Its own request, like inventory, so a slow or failing upstream delays nothing. */
export const fetchCubeGps = (name: string) =>
  getJson<CubeGps>(`/api/cubes/${encodeURIComponent(name)}/gps`)

/** A cube's liveness, derived from how recently Groundcover holds a log for it.
 *
 *  `state` is the only field the badge branches on, and `unknown` is a real
 *  outcome — never fold it into `offline`. A false "offline" on a cube whose apps
 *  are demonstrably working is a claim the viewer can disprove, and it costs the
 *  badge its credibility everywhere else. */
export type CubeStatus = {
  cube: string
  state: 'online' | 'offline' | 'unknown'
  /** RFC3339, or null when no log was found at all (or we could not look). */
  last_seen: string | null
  /** Seconds since `last_seen`, computed server-side against the server's clock —
   *  do NOT recompute from `last_seen` in the browser, whose clock may be skewed. */
  age_seconds: number | null
  /** "" | "not_reporting" | "unavailable" | "no_recent_logs" | "stale_logs" */
  reason: string
  threshold_seconds: number
  /** The lookback window that produced `last_seen`, in minutes. The age is only as
   *  precise as this, so the copy says "within" rather than implying exactness. */
  window_minutes: number | null
}

export const fetchCubeStatus = (name: string) =>
  getJson<CubeStatus>(`/api/cubes/${encodeURIComponent(name)}/status`)

/** A cube's Teleport connectivity — whether Edgeport can reach INTO the cube.
 *
 *  A different question from `CubeStatus` (is the cube shipping logs) and from
 *  `Cube.agent_status` (can Apollo deploy to it). This one is what `kubectl_exec`,
 *  the service list, `expose` and the app proxy all ride on.
 *
 *  `unknown` is a real outcome and must never be folded into `disconnected`, for the
 *  same reason `CubeStatus` keeps them apart. `not_enrolled` is a fourth state, not a
 *  flavour of disconnected: a cube with no Teleport agent was never asked to join. */
export type CubeTeleport = {
  cube: string
  state: 'connected' | 'disconnected' | 'not_enrolled' | 'unknown'
  /** The name this cube registers under in Teleport. Often — but NOT always — the
   *  cube name: `redhat-lab-cube` registers as `RHLab-Houston`, and `staging-int` as
   *  `Staging-int` (a case-only difference). When connected this is the live
   *  cluster's own name; otherwise it is the module's declared `kubeClusterName`.
   *  "" when it could not be read. Display only — the server joins on `resourceId`,
   *  because the name is caller-writable. */
  cluster: string
  /** "" | "no_heartbeat" | "unavailable" | "no_cluster_name" | "no_resource_id" */
  reason: string
  /** How long a Teleport heartbeat stays valid, in seconds. Teleport's constant, not
   *  a measurement — the cluster listing carries no timestamps, so this is the only
   *  bound the copy can honestly put on "in contact". */
  heartbeat_ttl_seconds: number
}

export const fetchCubeTeleport = (name: string) =>
  getJson<CubeTeleport>(`/api/cubes/${encodeURIComponent(name)}/teleport`)

/** When an app last changed, from Apollo's plan history.
 *
 *  `state` says how much the timestamp can be trusted, and the UI must branch on it
 *  rather than on `last_changed` being present:
 *    - `changed`      a successful plan finished then; the number is real
 *    - `unsuccessful` plans ran, none succeeded — the newest END time, so the app has
 *                     been deploying and failing rather than sitting unchanged
 *    - `none`         no completed plan at all (freshly installed)
 *    - `unknown`      the plan page may not hold the newest plan, so no claim is made
 *
 *  `unknown` exists because Apollo's plan ORDERING is undocumented: a full page that
 *  is not demonstrably newest-first could be hiding newer plans, and a blank cell is
 *  a far cheaper error than a confidently wrong date. */
export type AppChange = {
  last_changed: string | null
  /** Server-computed, like the status badge's — do not re-derive from
   *  `last_changed` in the browser, whose clock may be skewed. */
  age_seconds: number | null
  state: 'changed' | 'unsuccessful' | 'none' | 'unknown'
}

/** Keyed by ENTITY name (`App.entity_name`), not display name — the display name is
 *  not unique and is not what Apollo keys plans by. */
export type CubeChanges = {
  cube: string
  changes: Record<string, AppChange>
  /** The entity list was saturated, so some apps may be missing from `changes`
   *  entirely — distinct from an app whose entry says `none`. */
  truncated: boolean
}

export const fetchCubeChanges = (name: string) =>
  getJson<CubeChanges>(`/api/cubes/${encodeURIComponent(name)}/changes`)

export const fetchCube = (name: string) =>
  // encodeURIComponent: an Apollo environment name is not guaranteed to be a safe
  // path segment, and the server resolves it by exact match against the caller's
  // visible set — so it must arrive byte-identical.
  getJson<CubeDetail>(`/api/cubes/${encodeURIComponent(name)}`)

/** Full page load, not fetch: logout is a server redirect that clears the cookie. */
export function signOut(): void {
  window.location.href = '/auth/logout'
}

export type FeedbackSubmission = {
  /** `support` files a Freshservice ticket (an agent queue with a reply path);
   *  `feature` raises a customer request on the Jira product backlog. The console's
   *  old `bug` type is gone — the MCP `submit_feedback` tool still has it, and still
   *  goes to Jira. */
  feedback_type: 'support' | 'feature'
  summary: string
  details: string
  business_impact: string
  /** Free text, not validated against the caller's cube list — matches the MCP
   *  `submit_feedback` tool's own `cube` argument. */
  cube?: string
}

export type FeedbackResult = {
  /** No link back to the ticket, deliberately — the submitter has no JSM agent
   *  seat, so a Jira browse URL would just be a dead link. The key is still
   *  useful as a reference number for an out-of-band follow-up. */
  ticket_key: string
}

/** Raise a bug/feature ticket on the CF board (docs/console-spec.md §4.4e).
 *
 *  Deliberately no `contact_email` field on `FeedbackSubmission` — unlike the MCP
 *  tool, the console form never collects one. The reporter is resolved
 *  server-side from the session cookie's key, so there is nothing for this call
 *  to send that would change who the ticket is attributed to. */
export async function submitFeedback(
  payload: FeedbackSubmission,
  csrfToken: string,
): Promise<FeedbackResult> {
  const res = await fetch(`${CONSOLE_BASE}/api/feedback`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-Console-CSRF': csrfToken,
    },
    body: JSON.stringify(payload),
  })
  if (res.status === 401) throw new SessionExpired()
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.error ?? `Request failed (${res.status})`)
  }
  return res.json() as Promise<FeedbackResult>
}

/** One plotted sample: epoch milliseconds, and a reading that may be absent.
 *
 *  `null` means there was no sample at that step, and the chart BREAKS THE LINE there.
 *  It is never zero — a flat zero line is a claim about the cube, and it is the claim
 *  most likely to be misread as healthy for CPU and as catastrophic for disk.
 *
 *  Note these are real `number`s, a deliberate departure from this file's usual
 *  convention of the server pre-formatting display data as strings (see `Hardware`).
 *  A graph has to do arithmetic on them to place a point. */
export type UtilizationPoint = [number, number | null]

export type UtilizationSeries = {
  role: 'avg' | 'max'
  /** Already carries the entity count ("Average across 5 hosts"). The server names the
   *  series because the name is a claim about what was aggregated. */
  name: string
  points: UtilizationPoint[]
  /** False when the series parsed but holds no plottable number — every reading was
   *  non-finite. The line is then absent while the legend still names it, so the UI has
   *  to say why. Server-supplied on purpose: never infer this from `points` being empty
   *  or all-null, for the same reason `state` is not inferred from `series`. */
  has_readings: boolean
}

export type UtilizationPanel = {
  key: string
  label: string
  unit: string
  /** The UI must branch on THIS, never on `series` being empty. `no_data` means the
   *  cube does not report the metric; `unavailable` means we could not look;
   *  `no_readings` means it reported a sample at every step and not one of them was a
   *  number we can plot. Rendering any as another makes the page assert a fact about the
   *  cube at exactly the moment it has none — the same trap the Hardware tab fell into
   *  fleet-wide. */
  state: 'ok' | 'no_data' | 'no_readings' | 'unavailable'
  /** How many hosts / volumes the aggregation spanned, `null` when it could not be
   *  read. Not decoration: an average silently drops entities that stop reporting, so a
   *  host dying makes the average improve, and this count is the only thing on screen
   *  that can contradict that reading. */
  entity_count: number | null
  entity_noun: string
  latest: number | null
  /** "Highest sampled", not "peak" — the series is sampled at each step, so a spike
   *  between samples is invisible. Server-computed, like `CubeStatus.age_seconds`. */
  highest_sampled: number | null
  /** A stated v1 limitation, shown in the panel rather than left to be discovered. */
  note: string
  series: UtilizationSeries[]
}

export type CubeUtilization = {
  cube: string
  /** False when there is nothing to plot at all, with `reason` saying which:
   *  `not_reporting` (Groundcover has never heard of this cube) or `unavailable` (we
   *  could not reach it). Reported ONCE at the root rather than letting every panel
   *  make the same claim separately. */
  available: boolean
  reason: string
  window: string
  window_minutes: number
  step_seconds: number
  start: string
  end: string
  panels: UtilizationPanel[]
}

export const UTILIZATION_WINDOWS = ['1h', '6h', '24h'] as const
export type UtilizationWindow = (typeof UTILIZATION_WINDOWS)[number]

/** Resource graphs for one cube. `window` is an enumerated value, not a free duration —
 *  the server maps it to a query step, and rejects anything else with a 400. */
export const fetchCubeUtilization = (name: string, window: UtilizationWindow) =>
  getJson<CubeUtilization>(
    `/api/cubes/${encodeURIComponent(name)}/utilization` +
      `?window=${encodeURIComponent(window)}`,
  )

// ---------------------------------------------------------------------------
// AI tab (docs/ai-reactor-deploy-spec.md)
// ---------------------------------------------------------------------------

/** One catalog model and where it stands on this cube. `status` is the server's
 *  verdict and the UI branches on it, never on `health`/`lifecycle` directly. */
export type AiModel = {
  id: string
  display_name: string
  description: string
  task: 'chat' | 'embedding' | 'audio_transcription'
  platform: string
  gpu_count: number
  min_vram_gb: number
  /** Size of the model's storage volume in GB; the first start downloads weights. */
  storage_gb: number
  status:
    | 'available'
    /** The console just sent a change Apollo does not show yet. */
    | 'submitted'
    | 'installing'
    | 'starting'
    | 'ready'
    | 'needs_attention'
    | 'removing'
    | 'out_of_sync'
  /** `edgeport` when the console deployed it; `outside` when someone else did. */
  owner: 'edgeport' | 'outside' | null
  /** Whether the gateway routes to it. `unknown` on a gateway that keeps its model
   *  list in its own database, which the console cannot read. */
  wired: 'yes' | 'no' | 'unknown'
  lifecycle: string
  health: string
  entity_name: string | null
  /** The writes the server will accept for this model right now. */
  actions: Array<'deploy' | 'remove'>
  /** Whether one of the cube's GPUs is big enough. `unknown` when the GPUs could not
   *  be read; the server never offers Deploy for `no`. */
  fits: 'yes' | 'no' | 'unknown'
  /** GB of its GPU this model's vLLM reserves (--gpu-memory-utilization); null or absent when unknown. */
  memory_reserved_gb?: number | null
}

/** The cube's GPUs, read from Kubernetes. `available: false` means we could not look. */
export type AiGpu = {
  available: boolean
  total: number
  /** `null` when the cards were read but not what is using them. */
  free: number | null
  /** The NVIDIA product label, e.g. `NVIDIA-RTX-PRO-4000-Blackwell`. */
  product: string
  memory_gb: number | null
  /** GPU memory in use and free, in GB, on the card with the most room (where one more
   *  model would go), from NVIDIA's DCGM exporter. `null` when it could not be read.
   *  vLLM reserves its share of a card at startup, so "in use" is what the models on it
   *  have claimed. */
  memory_used_gb?: number | null
  memory_free_gb?: number | null
  /** `namespace/workload` of what holds a GPU now, and of what is waiting for one. */
  users: string[]
  waiting: string[]
}

export type AiGateway = {
  status: 'absent' | 'manageable' | 'read_only' | 'unknown'
  /** Why a gateway is read-only, as a stable code the page words. */
  reason: string | null
  mode: 'config' | 'database' | 'unknown'
  lifecycle: string
  health: string
  release_channel: string | null
  console_installed: boolean
  /** Serving: HEALTHY, or its own health report is clean while Apollo's status lags
   *  (a serving gateway can read ACTIVE_PLAN for many minutes after a plan). */
  ready: boolean
}

export type CubeAi = {
  cube: string
  /** Whether this profile may deploy or remove (`console_ai_write_profiles`). */
  can_write: boolean
  /** The entity read came back full, so nothing is offered. */
  saturated: boolean
  /** Some catalog model is already on the cube, so its GPU is probably in use. */
  gpu_likely_taken: boolean
  gpu: AiGpu
  gateway: AiGateway
  models: AiModel[]
}

export type AiWriteResult = {
  ok: boolean
  outcome: 'applied' | 'submitted' | 'partial' | 'refused'
  message: string
  steps: string[]
  /** The cube's state re-read after the write, so the tab settles without a refetch. */
  ai: CubeAi | null
}

/** `prefetch` marks a read the page makes before anyone opens the AI tab, so the
 *  server's usage telemetry does not count it as a view of the tab. */
export const fetchCubeAi = (name: string, opts?: { prefetch: true }) =>
  getJson<CubeAi>(`/api/cubes/${encodeURIComponent(name)}/ai${opts?.prefetch ? '?prefetch=1' : ''}`)

async function postAi(
  cube: string, action: 'deploy' | 'remove', body: Record<string, string>, csrfToken: string,
): Promise<AiWriteResult> {
  const res = await fetch(
    `${CONSOLE_BASE}/api/cubes/${encodeURIComponent(cube)}/ai/${action}`,
    {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Console-CSRF': csrfToken,
      },
      body: JSON.stringify(body),
    },
  )
  if (res.status === 401) throw new SessionExpired()
  if (res.status === 404) throw new NotFound()
  if (!res.ok) {
    const detail = await res.json().catch(() => null)
    throw new Error(detail?.error ?? `Request failed (${res.status})`)
  }
  return res.json() as Promise<AiWriteResult>
}

/** Send a catalog model to a cube, optionally replacing one the console deployed. */
export const deployAiModel = (cube: string, model: string, csrfToken: string, replace?: string) =>
  postAi(cube, 'deploy', replace ? { model, replace } : { model }, csrfToken)

/** Remove a model the console deployed. */
export const removeAiModel = (cube: string, model: string, csrfToken: string) =>
  postAi(cube, 'remove', { model }, csrfToken)

/** GPS positions for every cube the viewer can see, for the landing page's map
 *  (`reads.fleet_gps`). Fetched only when the viewer chooses Map.
 *
 *  `cubes` holds only cubes with a position; `counts` covers every visible cube.
 *  `counts` may gain keys: render the ones known here and ignore the rest. */
export type FleetGpsCube = {
  name: string
  display_name: string
  /** `reported`, `stale` or `time_unknown`. Anything else is drawn as muted. */
  state: string
  lat: number
  lng: number
  reported_at: string | null
  age_seconds: number | null
  /** The nearest town ("Denver, CO"), when the server can name one. */
  place: string | null
}

export type FleetGpsCounts = {
  shown?: number
  no_position?: number
  stale?: number
  time_unknown?: number
  unmatched?: number
  not_found?: number
  unresolved?: number
  [key: string]: number | undefined
}

export type FleetGps = {
  cubes: FleetGpsCube[]
  counts: FleetGpsCounts
  gps_source: { enabled: boolean; available: boolean }
  /** Apollo's environment list stopped short, so the counts cover only the cubes
   *  read. Optional: a server that predates the field never sets it. */
  environments_truncated?: boolean
}

export const fetchFleetGps = () => getJson<FleetGps>('/api/gps')

/** The map's border outline, decoded to flat [lon, lat, lon, lat, ...] polylines in
 *  degrees, per layer. */
export type MapOutline = {
  countries: number[][]
  states: number[][]
}

/** The only asset format this reads (`scripts/build-map-outline.py`): each line is its
 *  first point in integer units of 10^-precision degrees, then integer deltas. */
const OUTLINE_FORMAT = 'delta-int-polylines'

function decodeLayer(raw: unknown, unit: number): number[][] | null {
  if (raw === undefined) return []
  if (!Array.isArray(raw)) return null
  const out: number[][] = []
  for (const line of raw) {
    if (!Array.isArray(line) || !line.every(n => Number.isInteger(n))) return null
    let lon = 0
    let lat = 0
    const flat: number[] = []
    for (let i = 0; i + 1 < line.length; i += 2) {
      lon += line[i] as number
      lat += line[i + 1] as number
      flat.push(lon / unit, lat / unit)
    }
    out.push(flat)
  }
  return out
}

/** The outline's layers in degrees, or null when the body is not an outline this
 *  understands. Never throws. */
export function parseOutline(body: unknown): MapOutline | null {
  const asset = body as { format?: unknown; precision?: unknown; layers?: unknown } | null
  if (!asset || asset.format !== OUTLINE_FORMAT) return null
  const precision = asset.precision
  if (typeof precision !== 'number' || !Number.isInteger(precision) || precision < 0 || precision > 6) {
    return null
  }
  const layers = asset.layers as { countries?: unknown; states?: unknown } | undefined
  if (!layers || typeof layers !== 'object') return null
  const unit = 10 ** precision
  const countries = decodeLayer(layers.countries, unit)
  const states = decodeLayer(layers.states, unit)
  if (!countries || !states) return null
  return { countries, states }
}

/** The outline asset, served by the console itself (`routes.map_outline`): the shell's
 *  CSP loads nothing from another origin, so there are no map tiles.
 *
 *  Null when it is missing or unreadable, never an exception: the map then draws its
 *  dots on a blank background. A static file, not under `/api/`, so it carries no
 *  session meaning; an expired session shows up on the GPS request beside it. */
export async function fetchMapOutline(): Promise<MapOutline | null> {
  try {
    const res = await fetch(`${CONSOLE_BASE}/map/outline.json`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) return null
    return parseOutline(await res.json())
  } catch {
    return null
  }
}
