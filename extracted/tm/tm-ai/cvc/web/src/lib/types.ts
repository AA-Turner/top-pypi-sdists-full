// ═══════════════════════════════════════════════════════
//  CVC Dashboard — TypeScript Type Definitions
//  Mirrors gateway response shapes (cvc/gateway.py).
// ═══════════════════════════════════════════════════════

// ── Service / Status ────────────────────────────────
export type ServiceStatus = "running" | "stopped" | "unknown" | "error";

export interface ServiceInfo {
  name: string;
  status: ServiceStatus;
  port?: number;
  pid?: number | null;
  uptime?: string | null;
  url?: string;
}

export interface ServicesResponse {
  services: Record<string, ServiceInfo>;
  gateway_uptime?: string;
}

// ── Analytics / Stats ───────────────────────────────
export interface AnalyticsResponse {
  commits: {
    total: number;
    by_type: Record<string, number>;
    by_branch?: Record<string, number>;
  };
  branches: Array<{ name: string; head: string; status: string }>;
  tokens?: { total: number; estimated_cost_usd: number };
  recent_activity?: unknown[];
}

export interface StatsResponse {
  total_commits: number;
  total_branches: number;
  total_agents: number;
  commits_by_type: Record<string, number>;
  total_tokens: number;
  estimated_cost_usd: number;
  database_size_bytes: number;
  blob_count: number;
  head?: string | null;
}

// ── Commits / Timeline ─────────────────────────────
export interface CommitEntry {
  hash: string;
  short_hash?: string;
  message: string;
  timestamp: string | number;
  commit_type?: string;
  branch?: string;
  parent_hash?: string | null;
  content?: string;
  metadata?: Record<string, unknown>;
  author?: string;
}

export interface TimelineEntry {
  hash: string;
  message: string;
  timestamp: string | number;
  commit_type?: string;
  branch?: string;
}

// ── Event Spine (C5) — append-only activity ledger ─────────────
export interface EventSpineEntry {
  id: string;                  // ULID
  ts: number;                  // unix seconds
  ts_iso: string;
  ts_mono_ms: number;
  workspace: string | null;
  workspace_name: string | null;
  channel: string;
  channel_detail: string | null;
  actor: string | null;
  actor_detail: string | null;
  kind: string;
  summary: string;
  data: Record<string, unknown>;
  provider: string | null;
  model: string | null;
  branch: string | null;
  session_id: string | null;
  parent_event_id: string | null;
  duration_ms: number;
  tokens_in: number;
  tokens_out: number;
  bytes: number;
  status: string;
  error: string | null;
  tags: string[];
}

// ── Operations ──────────────────────────────────────
export interface CommitRequest {
  message: string;
  content?: string;
  commit_type?: string;
  metadata?: Record<string, unknown>;
}
export interface BranchRequest {
  name: string;
}
export interface MergeRequest {
  source_branch?: string;
  source?: string;
  target?: string;
  strategy?: string;
}
export interface RestoreRequest {
  commit_hash: string;
}
export interface OperationResult {
  status: string;
  hash?: string;
  branch?: string;
  message?: string;
  error?: string;
  [key: string]: unknown;
}
export interface RecallResult {
  results: Array<{
    hash: string;
    message: string;
    score: number;
    content?: string;
    excerpt?: string;
    timestamp?: string | number;
  }>;
}
export interface DiffResult {
  commit_a: string;
  commit_b: string;
  diff: string | Record<string, unknown>;
}

// ── Memory / Context ────────────────────────────────
export interface ContextEntry {
  role: string;
  content: string;
  timestamp?: string;
}
export interface MemoryContextResponse {
  context: ContextEntry[];
  token_count?: number;
}
export interface BlobEntry {
  hash: string;
  size_bytes: number;
  modified?: number;
  type?: string;
}
export interface MemoryBlobsResponse {
  blobs: BlobEntry[];
  total: number;
}
export interface MemoryStatsResponse {
  database_size_bytes: number;
  blob_count: number;
  blob_total_bytes: number;
  cvc_root?: string;
}

// ── Models ──────────────────────────────────────────
export interface ModelInfo {
  id: string;
  name: string;
  provider?: string;
  context_window?: number;
  max_output?: number;
  description?: string;
  /** Marks the provider's primary/default model — picker shows a PRIMARY pill. */
  is_primary?: boolean;
  /** Pre-formatted provider header label (e.g. "GitHub Copilot (18 models)"). */
  provider_label?: string;
}
export interface ModelCatalog {
  providers: Record<string, ModelInfo[]>;
  current_provider?: string;
  current_model?: string;
  /** Optional per-provider display label (e.g. "GitHub Copilot (18 models)"). */
  provider_labels?: Record<string, string>;
}
export interface CurrentModel {
  provider: string;
  model: string;
  api_key_set?: boolean;
}

// ── GitHub Copilot dynamic models ──────────────────
// Returned by GET /api/providers/copilot/models — the LIVE list of
// models available on the user's Copilot plan (different from the
// static fallback_models in cvc/providers/base.py). The dashboard
// uses this to populate the model picker with the actual available
// set rather than a hardcoded list.
export interface CopilotModelEntry {
  id: string;
  name: string;
  owned_by?: string;
  capabilities?: Record<string, unknown>;
  billing?: Record<string, unknown>;
  version?: string;
}
export interface CopilotModelsResponse {
  ok: boolean;
  models: CopilotModelEntry[];
  source: "copilot_api" | "copilot_api_refresh" | "no_token" | "unavailable" | "error";
  cached_at?: number | null;
  account: "individual" | "business" | "enterprise" | "unknown";
  token_source?: string;
  note?: string;
  error?: string;
}

// ── MCP ─────────────────────────────────────────────
export interface MCPTool {
  name: string;
  description?: string;
  parameters?: Record<string, unknown>;
}
export interface MCPStatus {
  available?: boolean;
  transport: string;
  tools_count?: number;
  status?: string;
  note?: string;
}

// ── Chat ────────────────────────────────────────────
export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}
export interface Attachment {
  name: string;
  stored_name: string;
  path: string;
  rel_path: string;
  size: number;
  mime: string;
  kind: "image" | "document" | "pdf" | "doc" | "sheet" | "slides" | "audio" | "video" | "text" | "other";
  data_url?: string;
}
export interface ChatRequest {
  messages: ChatMessage[];
  model?: string;
  stream?: boolean;
  /** One of none|minimal|low|medium|high|xhigh — forwarded to the provider. */
  reasoning_effort?: ReasoningEffort;
  /** Active persona id (default|ajay|jha|robin|samantha|tina|…). */
  persona_id?: string;
  /** v3.5.0 — Time Portal: pin chat context to a historical snapshot.
   *  When set, the gateway injects the snapshot's soul-context block into
   *  the system prompt and skips per-turn soul updates so the present
   *  soul isn't polluted by talking to past-Jai. Generated client-side
   *  via api.portalEnter(target). */
  portal_session_id?: string;
}
export interface ChatEvent {
  type:
    | "text"
    | "tool_start"
    | "tool_result"
    | "tool_confirm"
    | "tool_timeout"
    | "status"
    | "done"
    | "error"
    | "subagent_start"
    | "subagent_tool_start"
    | "subagent_tool_result"
    | "subagent_progress"
    | "subagent_parallel_batch"
    | "subagent_done"
    | "setup_required"
    | "ping"
    | "clarify_request"
    | "clarify_resolved"
    | "cost_budget_warning"
    | "cost_budget_exceeded"
    | "tool_risk"
    | "tool_dud_warning";
  content?: string;
  name?: string;
  args?: Record<string, unknown>;
  output?: string;
  message?: string;
  timeout_s?: number;
  mode?: string;
  /** v2.92.3 — Cost budget (loop primitive) */
  cap_usd?: number;
  spent_usd?: number;
  remaining_usd?: number;
  /** 0..1, fraction of cap spent. Only set on cost_budget_warning. */
  fraction?: number;
  /** v2.92.3 — Tool risk tier (loop primitive) */
  risk_tier?: "read_only" | "reversible_write" | "network_write" | "destructive";
  /** Clarify (ask_user) request — id of the pending entry to resolve. */
  clarify_id?: string;
  /** Clarify request — the question text. */
  question?: string;
  /** Clarify request — up to 4 multiple-choice options. */
  choices?: string[] | null;
  /** Clarify request — true when there are no choices (open-ended). */
  open_ended?: boolean;
  /** Clarify resolved — the user's response text (may be "" on timeout/abort). */
  response?: string;
  /** Sub-agent name (Explore, Plan, Security, …) — set on subagent_* events. */
  agent?: string;
  /** Wall-clock seconds the sub-agent tool took. */
  elapsed_s?: number;
  /** Success flag from the sub-agent tool / sub-agent run. */
  ok?: boolean;
  /** Provider model used by the sub-agent. */
  model?: string;
  /** setup_required: provider id that failed to initialise. */
  provider?: string;
  /** setup_required: human-readable instructions / list of supported keys. */
  detail?: string;
  /** setup_required: list of env var names the gateway will accept. */
  env_keys?: string[];
  /** ping: tool name and elapsed seconds for the running sub-agent. */
  scope?: string;
  tool?: string;
  /** subagent_progress fields */
  turn?: number;
  max_turns?: number;
  novel?: number;
  cached?: number;
  total_calls?: number;
  narration?: string;
  /** v2.74: subagent_progress phase ("tool_running" | "stall" | undefined). */
  phase?: string;
  /** subagent_tool_start: how many times this exact (name,args) has been called. */
  repeat?: number;
  /** subagent_tool_start: true when the result came from the runtime cache. */
  turns?: number;
  /** v2.83: stable per-run identifier so the dashboard can render N parallel sub-agents as N panes. */
  run_id?: string;
  /** v2.83: 1-based index of this sub-agent within a parallel_agents batch. */
  agent_index?: number;
  /** v2.83: total number of sub-agents in this parallel_agents batch. */
  agent_total?: number;
  /** v2.83: cumulative wall-clock seconds since the sub-agent started (carried on every event). */
  elapsed_total_s?: number;
  /** v2.83: cumulative tool-call count for this sub-agent (carried on every event). */
  tools_run?: number;
  /** v2.85: subagent_tool_start — true when the tool ran in a parallel batch. */
  parallel?: boolean;
  /** v2.85: subagent_parallel_batch — number of tools dispatched concurrently. */
  count?: number;
  /** v2.85: subagent_parallel_batch — names of tools in the batch. */
  tools?: string[];
  /** v2.85: subagent_parallel_batch — pool size. */
  workers?: number;
  /**
   * v3.3.7 — Monotonic millisecond timestamps from the gateway's
   * agent thread, NOT client-clock Date.now(). Used by tool_start /
   * tool_result handlers to render accurate durations when the WS
   * frame round-trip is faster than 1ms (which is common — the
   * client and server clocks can return the same value). Set on
   * tool_start and tool_result events.
   */
  started_at_ms?: number;
  ended_at_ms?: number;
  duration_ms?: number;
}

// ── Hive Mind / SDK ─────────────────────────────────
export interface HiveMindAgent {
  agent_id: string;
  name?: string;
  role?: string;
  rank?: string;
  squad?: string;
  registered_at?: string | number;
}
export interface RegisterAgentRequest {
  agent_id: string;
  name?: string;
  role?: string;
  rank?: string;
  squad?: string;
}

// ── Connections ─────────────────────────────────────
export interface ConnectionInfo {
  name: string;
  description?: string;
  icon?: string;
  base_url?: string;
  api_key?: string;
  instructions?: string;
}

// ── VCS ─────────────────────────────────────────────
export interface VCSStatus {
  provider: string;
  repo_root?: string;
  current_branch?: string;
  has_repo: boolean;
  hooks_installed?: boolean;
}

// ── Audit ───────────────────────────────────────────
export interface AuditEntry {
  timestamp: string | number;
  action: string;
  details?: string;
  [key: string]: unknown;
}

// ── Config / Workspace ──────────────────────────────
export interface GatewayConfig {
  proxy_port?: number;
  gateway_port?: number;
  db_path?: string;
  provider?: string;
  model?: string;
  [key: string]: unknown;
}

// ── Settings ────────────────────────────────────────
export interface SettingsFieldOption {
  value: string;
  label: string;
  desc?: string;
}
export interface SettingsField {
  key: string;
  type:
    | "text" | "number" | "password" | "select" | "toggle" | "radio"
    | "slider" | "tag_list" | "key_value" | "hook_editor"
    | "plugin_toggles" | "model_select";
  label: string;
  description?: string;
  placeholder?: string;
  options?: string[] | SettingsFieldOption[];
  depends_on?: string;
  level: "global" | "project" | "local";
  min?: number;
  max?: number;
  step?: number;
  visible_when?: Record<string, string>;
  hook_events?: string[];
}
export interface SettingsSection {
  id: string;
  title: string;
  icon?: string;
  fields: SettingsField[];
}
export interface SettingsSchema {
  sections: SettingsSection[];
}
export interface SettingsGlobal {
  provider: string;
  model: string;
  agent_id: string;
  api_keys: Record<string, string>;
}
export interface SettingsProject {
  permissions?: { allow: string[]; deny: string[]; ask: string[] };
  env?: Record<string, string>;
  hooks?: Record<string, unknown[]>;
  outputStyle?: string;
  autoMemoryEnabled?: boolean;
  alwaysThinkingEnabled?: boolean;
  autoCompactThreshold?: number;
  enabledPlugins?: Record<string, boolean>;
  trust_mode?: string;
  plan_display?: string;
  trusted_commands?: string[];
  blocked_commands?: string[];
  [key: string]: unknown;
}
export interface SettingsResponse {
  global: SettingsGlobal;
  project: SettingsProject;
  schema: SettingsSchema;
}

// ── Agent Templates ─────────────────────────────────
export interface AgentTemplate {
  id: string;
  name: string;
  description?: string;
  system_prompt?: string;
  tools_allow?: string[];
  tools_deny?: string[];
  tool_tier?: string;
  model_override?: string;
  provider_override?: string;
  max_turns?: number;
  rank?: string;
  squad?: string;
  capabilities?: string[];
  skills?: string[];
  auto_respond?: boolean;
  auto_share_to_hive?: boolean;
  created_at?: number;
  updated_at?: number;
  created_by?: string;
  is_builtin?: boolean;
  source?: string;
}
export interface AgentsListResponse {
  registered: Record<string, unknown>[];
  templates: AgentTemplate[];
  builtins: AgentTemplate[];
  total: number;
}
export interface AgentFromPromptResponse {
  status: string;
  template: AgentTemplate;
  raw_description?: string;
}

// ── Hive Memory ─────────────────────────────────────
export interface HiveMemoryEntry {
  id: string;
  agent_id: string;
  content: string;
  category: string;
  tags: string[];
  timestamp: number;
  commit_hash?: string;
  message?: string;
}
export interface HiveMemoryResponse {
  entries: HiveMemoryEntry[];
  total: number;
}
export interface HiveMemoryStats {
  total_entries: number;
  categories: Record<string, number>;
  contributing_agents: string[];
  agent_count: number;
}
export interface SquadInfo {
  name: string;
  branch?: string;
  agents: Record<string, unknown>[];
  agent_count: number;
}

// ── Workspace ───────────────────────────────────────
export interface WorkspaceInfo {
  workspace_id?: string;
  path?: string;
  name?: string;
}

// ── Git (active-workspace scoped) ───────────────────
export interface GitStatusInfo {
  is_repo: boolean;
  path?: string;
  branch?: string;
  head?: string;
  detached?: boolean;
  dirty?: boolean;
  dirty_count?: number;
}
export interface GitBranchEntry {
  name: string;
  head: string;
  last_commit_at: string;
  last_commit_subject: string;
  is_current: boolean;
  /** "local" or "remote" — distinguishes refs/heads from refs/remotes. */
  kind?: "local" | "remote";
  /** For local branches: upstream tracking ref, e.g. "origin/main". */
  upstream?: string | null;
  /** Ahead/behind counts vs upstream (local branches only). */
  ahead?: number;
  behind?: number;
  /** Upstream gone (deleted remotely). */
  gone?: boolean;
  /** For remote branches: short name without "<remote>/" prefix. */
  short_name?: string;
  /** Remote name (e.g. "origin") for remote-kind entries. */
  remote?: string;
  /** True if a local branch with this short_name already exists (remote-kind only). */
  has_local?: boolean;
  /** True if some local branch tracks this remote ref (remote-kind only). */
  tracked_by_local?: boolean;
}
export interface GitBranchesResponse {
  /** Back-compat: same as `local`. */
  branches: GitBranchEntry[];
  local?: GitBranchEntry[];
  remote?: GitBranchEntry[];
  current: string;
  detached: boolean;
  count: number;
  remote_count?: number;
  fetched?: boolean;
  fetch_error?: string | null;
}
export interface GitCheckoutResponse {
  status: string;
  branch: string;
  head: string;
  created: boolean;
}
export interface GitSyncResult {
  status: "ok" | "diverged" | "dirty" | "no_upstream";
  branch: string;
  remote: string;
  fetched: boolean;
  pulled: number;
  pushed: number;
  ahead: number;
  behind: number;
  head: string;
  message: string;
}

// ── Branches ────────────────────────────────────────
export interface BranchSummary {
  name: string;
  head: string;
  status: string;
  commit_count?: number;
  last_activity?: string | number;
  is_active?: boolean;
}

export interface OpsStatus {
  branch: string;
  head: string;
  total_commits: number;
  workspace?: string;
}

// ── Gateway workspaces ──────────────────────────────
export interface GatewayWorkspaceEntry {
  workspace_id: string;
  id?: string;
  name?: string;
  // v2.91.66 — The gateway's `/gateway/workspaces` endpoint actually
  // returns the absolute path under the `path` key, not `root_path`.
  // Keeping `root_path` as a fallback for older gateways.
  path?: string;
  root_path?: string;
  status?: string;
  last_seen?: string | number;
  [key: string]: unknown;
}
export interface GatewayWorkspacesResponse {
  workspaces: GatewayWorkspaceEntry[];
  count?: number;
}
export interface SessionEntry {
  id?: string;
  session_id?: string;
  model?: string;
  provider?: string;
  started_at?: string | number;
  message_count?: number;
  [key: string]: unknown;
}
export interface SessionsResponse {
  sessions: SessionEntry[];
  error?: string;
}
export interface RegisterWorkspaceRequest {
  workspace_id?: string;
  id?: string;
  name?: string;
  root_path?: string;
}
export interface TelemetryEvent {
  event: string;
  target_agent_id?: string;
  [key: string]: unknown;
}

// ── Providers / Credentials (Phase-1) ─────────────────────────────────────
export interface ProviderProfile {
  name: string;
  aliases?: string[];
  env_vars?: string[];
  base_url?: string | null;
  auth_type?: string;
  api_mode?: string;
  fallback_models?: string[];
  fixed_temperature?: number | null;
  default_max_tokens?: number | null;
  supports_streaming?: boolean;
  supports_tools?: boolean;
  supports_reasoning?: boolean;
  supports_prompt_cache?: boolean;
  per_model_api_mode?: Record<string, string>;
  extra_headers?: Record<string, string>;
}

export interface PooledCredentialView {
  id: string;
  provider: string;
  label: string;
  auth_type?: string;
  base_url?: string | null;
  masked_token: string;
  exhausted: boolean;
  exhausted_reason?: string | null;
  exhausted_at?: number | null;
  use_count?: number;
  last_used?: number | null;
  created_at?: number;
}

export interface CredentialPoolStats {
  total: number;
  available: number;
  exhausted: number;
  by_provider: Record<string, { total: number; available: number; exhausted: number }>;
}

// ── Agentic loop (Phase-1 Cat 2) ──────────────────────────────────────────
export interface LoopBudgetView {
  active: boolean;
  max: number;
  used: number;
  remaining: number;
  exhausted: boolean;
}

export interface LoopGuardrailsView {
  active: boolean;
  max_identical_per_turn: number;
  max_total_per_turn: number;
  calls_this_turn: number;
}

export interface LoopCompressorView {
  active: boolean;
  trigger_tokens?: number | null;
  target_ratio?: number | null;
  keep_recent?: number | null;
}

export interface LoopRecorderView {
  active: boolean;
  enabled: boolean;
  path?: string | null;
}

export interface LoopSnapshot {
  budget: LoopBudgetView;
  guardrails: LoopGuardrailsView;
  compressor: LoopCompressorView;
  recorder: LoopRecorderView;
  last_turn: Record<string, unknown>;
  recent_turns: Record<string, unknown>[];
}

export interface LoopConfig {
  budget: { default_parent_max: number; default_subagent_max: number };
  compression: {
    trigger_tokens?: number | null;
    target_ratio?: number | null;
    keep_recent?: number | null;
  };
  output_limits: Record<string, number>;
  guardrails: { max_identical_per_turn: number; max_total_per_turn: number };
}

// ── Trajectory ────────────────────────────────────────────────────────────
export interface TrajectoryFile {
  name: string;
  path: string;
  size_bytes: number;
  modified: number;
}

export interface TrajectoryTurn {
  turn: number;
  timestamp: number;
  messages?: unknown[];
  tool_calls?: unknown[];
  tool_results?: unknown[];
  prompt_tokens?: number;
  completion_tokens?: number;
  cache_read_tokens?: number;
  model?: string;
  provider?: string;
  metadata?: Record<string, unknown>;
}

export interface TrajectorySummary {
  path: string | null;
  turns: number;
  tokens: { prompt: number; completion: number; cache_read?: number };
  models?: string[];
}

// ── Team (Core 4) ─────────────────────────────────────────────────────────
export interface TeamMember {
  agent_id: string;
  name: string;
  role: string;
  rank: string;
  squad: string;
  status?: string;
  description?: string;
  capabilities?: string[];
}

export interface TeamSnapshot {
  team: TeamMember[];
  total: number;
  canonical: TeamMember[];
}

// ── Composer-bar (personas, reasoning, context meter, workspace tree) ─────
export interface PersonaSummary {
  id: string;
  name: string;
  description?: string | null;
  default_model: string;
  default_provider: string;
  skills_count: number;
  system_prompt_path?: string | null;
}

export interface PersonaDetail extends PersonaSummary {
  system_prompt: string;
  skills: string[];
}

export interface PersonaActive {
  workspace_id: string;
  persona_id: string;
}

// ── Conversation history (new in 2.23.1) ──────────────────────────────────

export interface ConversationThread {
  id: string;
  workspace_path: string;
  title: string;
  persona_id: string | null;
  hostname: string;
  created_at: number;
  updated_at: number;
  message_count: number;
}

export interface ConversationMessage {
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  created_at?: number;
  id?: number;
  reply_to?: number | null;
  pinned?: 0 | 1 | boolean;
  parent_preview?: string | null;
}

// ── DX (Developer Experience) ───────────────────────────────────────────

export interface DxSlashArg {
  name: string;
  type: string;
  choices?: string[];
}

export interface DxSlashCommand {
  cmd: string;
  group: string;
  desc: string;
  args: DxSlashArg[];
  /** Dispatch strategy: "client" | "route" | "agent". Defaults to "agent". */
  exec?: "client" | "route" | "agent";
  route?: string;
  client_action?: string;
  /** If set, this command is an alias of another canonical command. */
  alias_of?: string;
}

export interface DxSlashRegistry {
  count: number;
  commands: DxSlashCommand[];
}

export interface DxSlashRunResult {
  cmd: string;
  entry: DxSlashCommand;
  delegate?: boolean;
  insight_id?: number;
  insights?: DxInsight[];
  error?: string;
}

export interface DxPinnedMessage {
  id: number;
  role: string;
  content: string;
  created_at: number;
  reply_to: number | null;
}

export interface DxPinnedList {
  thread_id: string;
  count: number;
  messages: DxPinnedMessage[];
}

export interface DxReplyResult {
  ok: boolean;
  message_id: number;
  thread_id: string;
  reply_to: number;
  parent_preview: string;
}

export interface DxInsight {
  id: number;
  workspace_path: string;
  thread_id?: string | null;
  kind: "preference" | "fact" | "pitfall" | "decision" | "rule";
  content: string;
  source?: string;
  weight: number;
  use_count: number;
  created_at: number;
  last_used: number;
}

export interface DxInsightsList {
  count: number;
  insights: DxInsight[];
}

export interface DxFile {
  path: string;
  name: string;
  size: number;
  score: number;
}

export interface DxFilesResult {
  workspace_path: string;
  query: string;
  scanned: number;
  count: number;
  files: DxFile[];
}

export interface DxCostSummary {
  thread_id: string | null;
  available: boolean;
  summary: string;
  data: Record<string, unknown>;
  error?: string;
}

export interface DxExportResult {
  thread_id: string;
  format: "md" | "json";
  filename?: string;
  content?: string;
  thread?: unknown;
  messages?: unknown[];
}

export interface ConversationDetail extends ConversationThread {
  messages: ConversationMessage[];
}

export type ReasoningEffort =
  | "none"
  | "minimal"
  | "low"
  | "medium"
  | "high"
  | "xhigh";

export interface ContextMeter {
  used_tokens: number;
  total_tokens: number;
  used_pct: number;
  remaining_tokens?: number;
  remaining_pct?: number;
  auto_compact_threshold_tokens: number;
  auto_compact_threshold_pct: number;
  tokens_until_auto_compact?: number;
  pct_until_auto_compact?: number;
  breakdown?: {
    system: number;
    user: number;
    assistant: number;
    tool: number;
    other: number;
  };
  model: string;
  provider: string;
  last_auto_compact_at?: string | null;
}

export interface WorkspaceTreeNode {
  name: string;
  path: string;
  rel_path: string;
  is_dir: boolean;
  size: number;
  mtime: number;
  children?: WorkspaceTreeNode[] | null;
}

// ═══════════════════════════════════════════════════════
//  Soul Layer (P5) + Universal Adapter System (7.1)
//  + Apple-Grade Security (7.2) + Swarm Cluster (7.3)
// ═══════════════════════════════════════════════════════

// ── Soul ──────────────────────────────────────────
export interface SoulLifeEvent {
  description: string;
  event_type: string;
  emotional_weight: number;
  timestamp: number;
  date: string;
}
export interface SoulMood {
  mood: string;
  intensity: number;
  trigger: string;
  timestamp: number;
  date: string;
}
export interface SoulEntity {
  name: string;
  type: string;
  relationship: string;
  mention_count: number;
  attributes: Record<string, unknown>;
}
export interface SoulValue {
  statement: string;
  category: string;
  confidence: number;
}
export interface SoulLifeStory {
  soul_narrative: string;
  name: string;
  life_events: SoulLifeEvent[];
  emotional_arc: SoulMood[];
  entity_graph: SoulEntity[];
  values: SoulValue[];
  timeline_density: Record<string, number>;
  total_interactions: number;
  first_interaction: number | null;
  first_interaction_date: string | null;
}
export interface SoulUserModel {
  name: string;
  soul_narrative: string;
  narrative_summary: string;
  entities: Array<{
    name: string;
    type: string;
    relationship: string;
    mention_count: number;
    first_mentioned?: number;
    last_mentioned?: number;
    attributes: Record<string, unknown>;
    context_snippets: string[];
  }>;
  values: Array<{
    statement: string;
    category: string;
    confidence: number;
    superseded: boolean;
  }>;
  temporal_facts: Array<{
    statement: string;
    scope: string;
    category: string;
    confidence: number;
    still_valid: boolean;
  }>;
  emotional_context_count: number;
  life_events: Array<{
    description: string;
    type: string;
    weight: number;
  }>;
  expertise_areas: string[];
  communication_style: string;
  preferred_languages: string[];
  preferred_tools: string[];
  // v2.1 — Self-Correction Loop
  corrections?: SoulCorrection[];
  active_corrections_count?: number;
}

// ── Soul Corrections (P7 — the soul learns from pushback) ─────────────
// Direct corrections from the owner override inferred claims.
// Append-only, versioned via superseded_by.
export type SoulCorrectionClaimType =
  | "entity"
  | "value"
  | "temporal_fact"
  | "life_event"
  | "emotional_context"
  | "narrative"
  | "communication_style"
  | "expertise_area"
  | "preferred_language"
  | "preferred_tool";

export interface SoulCorrection {
  correction_id: string;
  claim_type: SoulCorrectionClaimType;
  original_inference: string;
  corrected_value: string;
  reason: string;
  confidence_override: number;
  created_at: number;
  created_at_iso: string;
  source_commit: string;
  conversation_snippet: string;
  superseded_by: string | null;
  active: boolean;
}

export interface SoulCorrectionRequest {
  claim_type: SoulCorrectionClaimType;
  corrected_value: string;
  original_inference?: string;
  reason?: string;
  source_commit?: string;
  conversation_snippet?: string;
}

export interface SoulCorrectionResponse {
  ok: boolean;
  correction?: SoulCorrection;
  superseded_id?: string | null;
  active_corrections_count?: number;
  error?: string;
}

export interface SoulCorrectionsResponse {
  corrections: SoulCorrection[];
  count: number;
  active_count: number;
  superseded_count?: number;
  by_claim_type?: Record<string, number>;
  error?: string;
}

// ── Soul Will & Executor Protocol (P8 — digital-parents arc) ───────────
// A will is the soul's plan for what happens to it when its owner is gone.
// v1 ships manual release only. v2 will add time_locked + death_verified
// + Shamir M-of-N executor key release.
export type SoulExecutorRole = "primary" | "witness" | "backup";
export type SoulReleaseCondition = "manual" | "time_locked" | "death_verified";

export interface SoulExecutor {
  executor_id: string;
  name: string;
  relationship: string;
  contact: string;
  role: SoulExecutorRole;
  public_key_pem: string;
  created_at: number;
  created_at_iso: string;
}

export interface SoulWill {
  exists: true;
  will_id: string;
  owner_name: string;
  created_at: number;
  created_at_iso: string;
  updated_at: number;
  updated_at_iso: string;
  version: number;
  release_condition: SoulReleaseCondition;
  executors: SoulExecutor[];
  current_blob_name: string;
  blob_history_count: number;
  release_count: number;
  last_released_at: number;
}
export interface SoulWillMissing {
  exists: false;
  executors?: never[];
  error?: string;
}
export type SoulWillResponse = SoulWill | SoulWillMissing;

export interface SoulWillCreateRequest {
  owner_name: string;
  will_text: string;
  release_condition?: SoulReleaseCondition;
  executors?: Array<{
    name: string;
    relationship?: string;
    contact?: string;
    role?: SoulExecutorRole;
    public_key_pem?: string;
  }>;
}
export interface SoulWillCreateResponse {
  ok: boolean;
  will?: SoulWill;
  generated_private_keys?: Record<string, string>; // executor_id → PEM
  private_key_warning?: string | null;
  error?: string;
}

export interface SoulWillExecutorAddRequest {
  name: string;
  relationship?: string;
  contact?: string;
  role?: SoulExecutorRole;
  public_key_pem?: string;
}
export interface SoulWillExecutorAddResponse {
  ok: boolean;
  will?: SoulWill;
  executor?: SoulExecutor;
  generated_private_key?: string; // one-time
  private_key_warning?: string | null;
  error?: string;
}

export interface SoulWillExecutorRemoveRequest {
  executor_id: string;
}
export interface SoulWillExecutorRemoveResponse {
  ok: boolean;
  will?: SoulWill;
  error?: string;
}

export interface SoulWillReleaseRequest {
  actor?: string;
  reason?: string;
}
export interface SoulWillReleaseResponse {
  ok?: boolean;
  error?: string;
}

export interface SoulWillArtifact {
  will_id: string;
  owner_name: string;
  version: number;
  released_at: number;
  released_at_iso: string;
  released_by: string;
  reason: string;
  release_condition: SoulReleaseCondition;
  executors: SoulExecutor[];
  will_text: string;
  audit_chain_hash: string;
  schema: "cvc.soul.v1";
}

// ── Preservation Mode (P9 — "the last session handshake") ──────────────
// Entered when the owner knows they're at the end. Every new interaction
// is captured at maximum fidelity. The soul narrative is frozen. A Final
// Summary is generated for whoever inherits the soul.
export interface SoulPreservationState {
  enabled: boolean;
  enabled_at: number;
  enabled_at_iso: string;
  enabled_by: string;
  frozen_narrative_present: boolean;
  frozen_narrative_at: number;
  frozen_narrative_at_iso: string;
  auto_correct: boolean;
  require_explicit_correction: boolean;
  final_summary_blob: string;
  final_summary_generated_at: number;
  final_summary_generated_at_iso: string;
  final_summary_word_count: number;
  total_interactions_in_preservation: number;
  last_interaction_at: number;
  last_interaction_at_iso: string;
}

export interface SoulFinalSummarySection {
  who_they_were: string;
  people_in_their_life: Array<{
    name: string;
    relationship: string;
    note: string;
  }>;
  what_they_believed: string[];
  what_they_built: string[];
  milestones: Array<{ description: string; weight: number }>;
  how_they_felt_late: string;
  what_they_wanted_you_to_know: string;
  final_word_from_the_soul: string;
}

export interface SoulFinalSummary {
  title: string;
  generated_at: number;
  generated_at_iso: string;
  model: string;
  word_count: number;
  sections: SoulFinalSummarySection;
  schema: "cvc.soul.final_summary.v1";
}

export interface SoulFinalSummaryVaultLocked {
  vault_locked: true;
  blob_name: string;
}

export type SoulFinalSummaryResponse =
  | SoulFinalSummary
  | SoulFinalSummaryVaultLocked
  | null;

export interface SoulPreservationResponse {
  enabled: boolean;
  enabled_at: number;
  enabled_at_iso: string;
  enabled_by: string;
  frozen_narrative_present: boolean;
  frozen_narrative_at: number;
  frozen_narrative_at_iso: string;
  auto_correct: boolean;
  require_explicit_correction: boolean;
  final_summary_blob: string;
  final_summary_generated_at: number;
  final_summary_generated_at_iso: string;
  final_summary_word_count: number;
  total_interactions_in_preservation: number;
  last_interaction_at: number;
  last_interaction_at_iso: string;
  final_summary?: SoulFinalSummaryResponse;
  error?: string;
}

export interface SoulPreservationEnableRequest {
  auto_correct?: boolean;
  freeze_narrative?: boolean;
  freeze_narrative_text?: string;
  actor?: string;
}
export interface SoulPreservationEnableResponse {
  ok: boolean;
  state?: SoulPreservationState;
  error?: string;
}

export interface SoulPreservationDisableRequest {
  actor?: string;
}
export interface SoulPreservationDisableResponse {
  ok: boolean;
  state?: SoulPreservationState;
  error?: string;
}

export interface SoulPreservationSummarizeRequest {
  adapter_id?: string;
  model?: string;
  include_will?: boolean;
}
export interface SoulPreservationSummarizeResponse {
  ok: boolean;
  state?: SoulPreservationState;
  summary?: SoulFinalSummary;
  adapter_used?: string;
  model_used?: string;
  error?: string;
}
export interface SoulDream {
  dream_id: string;
  timestamp: number;
  date: string;
  narrative: string;
  concept_tags: string[];
  insights: string[];
  contradictions: string[];
  candidate_count: number;
}
export interface SoulDreams {
  dreams: SoulDream[];
  count: number;
}
export interface SoulNarrative {
  narrative: string;
  name: string;
  has_data: boolean;
  error?: string;
}

// ── Soul Letters (P6 — "the soul writes back") ────────────────────────
// Weekly letters from the soul to its owner. Proactive, not reactive.
export interface SoulLetter {
  letter_id: string;
  week_of: string;            // ISO year-week, e.g. "2026-W26"
  week_start: number;         // unix timestamp
  week_end: number;
  week_start_iso: string;     // "2026-06-23"
  week_end_iso: string;       // "2026-06-29"
  generated_at: number;
  generated_at_iso: string;

  // Letter body
  greeting: string;
  narrative: string;
  signoff: string;

  // Structured observations
  observations: string[];
  soul_changes: string[];
  week_themes: string[];

  // Provenance
  source_commits: string[];
  source_commit_count: number;
  user_name: string;
  model_used: string;
  generation_seconds: number;
}
export interface SoulLettersResponse {
  letters: SoulLetter[];
  count: number;
  last_week: string | null;
  weeks_tracked: number;
  error?: string;
}
export interface SoulLetterResponse {
  found: boolean;
  week_of: string;
  letter?: SoulLetter;
  error?: string;
}
export interface SoulLetterGenerateResponse {
  generated: boolean;
  week_of: string;
  reason?: string;            // "already_exists" | "no_healthy_adapter_available" | ...
  adapter_used?: string;
  model_used?: string;
  letter?: SoulLetter;
  error?: string;
}

// ── Adapters ──────────────────────────────────────
export interface AdapterReport {
  adapter_id: string;
  display_name: string;
  capabilities: string[];
  healthy: boolean;
  last_error: string;
  last_check: number;
  supports_streaming: boolean;
  supports_tools: boolean;
  supports_vision: boolean;
  supports_local: boolean;
  default_model: string;
}
export interface AdapterSnapshot {
  adapters: AdapterReport[];
  total: number;
  healthy: number;
  discovered_at: number;
}
export interface AdapterNegotiation {
  required: string[];
  matched: AdapterReport | null;
  total_healthy: number;
}

// ── Security ──────────────────────────────────────
export interface SecurityVault {
  initialized: boolean;
  unlocked: boolean;
  blobs: number;
  vault_dir: string;
  kdf: string;
  kdf_params: Record<string, number>;
  cipher: string;
}
export interface SecuritySentinelStats {
  allowed: number;
  blocked: number;
  allowed_brains: string[];
  allowed_hosts: string[];
  blocked_hosts: string[];
  permissive: boolean;
  allow_loopback?: boolean;
}
export interface SecurityStatus {
  vault: SecurityVault;
  sentinel: SecuritySentinelStats;
  audit_entries: number;
  ready: boolean;
}
export interface SecurityAuditEntry {
  timestamp: number;
  action: string;
  actor: string;
  target: string;
  detail: Record<string, unknown>;
  prev_hash: string;
  chain_hash: string;
}

// ── Swarm ─────────────────────────────────────────
export interface SwarmIdentity {
  peer_id: string;
  display_name: string;
  created_at: number;
  public_key_fp: string;
  capabilities: string[];
}
export interface SwarmPolicy {
  identity: string;
  entities: string;
  values: string;
  dreams: string;
  insights: string;
}
export interface SwarmPeer {
  peer_id: string;
  display_name: string;
  address: string;
  last_seen: number;
  capabilities: string[];
  trust: number;
}
export interface SwarmBroadcast {
  broadcast_id: string;
  topic: string;
  payload: Record<string, unknown>;
  timestamp: number;
  peer_id: string;
  signature: string;
}

// ───────────────────────────────────────────────────────────────────
// H1 — Time Portal (then vs now)
// ───────────────────────────────────────────────────────────────────

export interface TimePortalSnapshotMeta {
  name: string;
  timestamp?: number;
  _snapshot_timestamp?: number;
  _snapshot_id?: string | null;
  _is_empty?: boolean;
}

export interface TimePortalEmotionalStats {
  count: number;
  mean_intensity: number;
  dominant_mood: string | null;
}

export interface TimePortalEntityStrengthened {
  name: string;
  mentions_before: number;
  mentions_after: number;
  delta: number;
}

export interface TimePortalDiff {
  entities: {
    added: string[];
    removed: string[];
    strengthened: TimePortalEntityStrengthened[];
  };
  values: {
    added: string[];
    superseded: string[];
  };
  life_events: {
    new_in_between: string[];
  };
  emotional_drift: {
    then: TimePortalEmotionalStats;
    now: TimePortalEmotionalStats;
    intensity_delta: number;
  };
  narrative: {
    changed: boolean;
    length_delta: number;
  };
  summary: string;
  then_meta: TimePortalSnapshotMeta;
  now_meta: TimePortalSnapshotMeta;
}

export interface TimePortalTargetOption {
  snapshot_id: string;
  timestamp: number;
  iso: string;
  trigger: string;
  commit_hash: string | null;
}

export interface TimePortalResponse {
  then: Record<string, unknown>;
  now: Record<string, unknown>;
  diff: TimePortalDiff;
  target_resolved: string;
  target_timestamp: number;
  available_targets: TimePortalTargetOption[];
  error?: string;
}

// ───────────────────────────────────────────────────────────────────
// H1b — Time Portal session (active portal in chat)
// ───────────────────────────────────────────────────────────────────

export interface PortalSession {
  snapshot_id: string;
  snapshot_timestamp: number;
  iso_date: string;
  target_resolved: string;
  label: string;
  trigger: string;
  created_at: number;
  /** v3.5.1 — "snapshot" (single) or "day" (consolidated). */
  scope?: "snapshot" | "day";
  /** v3.5.1 — Number of snapshots consolidated (day scope only). */
  snapshot_count?: number;
  /** v3.5.1 — When scope="day", the date YYYY-MM-DD. */
  date?: string;
}

export interface PortalEnterResponse {
  ok: boolean;
  error?: string;
  portal_id?: string;
  snapshot_id?: string;
  timestamp?: number;
  iso_date?: string;
  label?: string;
  target_resolved?: string;
  trigger?: string;
  /** v3.5.1 — echo scope back so client doesn't have to guess. */
  scope?: "snapshot" | "day";
  /** v3.5.1 — count of snapshots consolidated (day scope). */
  snapshot_count?: number;
  /** v3.5.1 — date when scope="day" (YYYY-MM-DD). */
  date?: string;
}

export interface PortalActiveResponse {
  active: boolean;
  portal_id?: string;
  session?: PortalSession;
  sessions?: Record<string, PortalSession>;
  count?: number;
  error?: string;
}

export interface PortalExitResponse {
  ok: boolean;
  error?: string;
  portal_id?: string;
  existed?: boolean;
}

export interface PortalChatContextResponse {
  ok: boolean;
  error?: string;
  portal_id?: string;
  snapshot_id?: string;
  iso_date?: string;
  context?: string;
  context_length?: number;
}

/** v3.5.1 — one day in the day-index returned by /time-portal/days. */
export interface PortalDayEntry {
  date: string;            // YYYY-MM-DD
  snapshot_count: number;  // raw per_turn_auto snapshots on this day
  first_ts: number;        // unix timestamp of earliest snapshot
  last_ts: number;         // unix timestamp of latest snapshot
  first_id: string;
  last_id: string;
  has_day_canonical: boolean;
  day_snapshot_id?: string;
}

/** v3.5.1 — GET /api/soul/time-portal/days response. */
export interface PortalDaysResponse {
  ok: boolean;
  error?: string;
  days?: PortalDayEntry[];
  count?: number;
}

export interface SnapshotStats {
  total: number;
  oldest: number | null;
  newest: number | null;
  by_trigger: Record<string, number>;
  total_size_bytes: number;
}

export interface SnapshotsListResponse {
  snapshots: TimePortalTargetOption[];
  stats: SnapshotStats;
  error?: string;
}

// ───────────────────────────────────────────────────────────────────
// H2 — Emotional Arc + Entity Graph
// ───────────────────────────────────────────────────────────────────

export interface EmotionalArcObservation {
  mood: string;
  intensity: number;
  trigger: string;
  timestamp: number;
  date: string;
}

export interface EmotionalArcBucket {
  label: string;
  count: number;
  mean_intensity: number;
  dominant_mood: string;
}

export interface EmotionalArcAggregate {
  total: number;
  mood_distribution: Record<string, number>;
  mean_intensity: number;
  dominant_mood: string;
  volatility: number;
  period_start: string;
  period_end: string;
}

export interface EmotionalArcResponse {
  observations: EmotionalArcObservation[];
  aggregate: EmotionalArcAggregate;
  buckets: EmotionalArcBucket[];
  error?: string;
}

export interface EntityNode {
  id: string;
  name: string;
  type: string;
  relationship: string;
  mention_count: number;
  first_mentioned: number;
  last_mentioned: number;
  first_mentioned_date: string;
  last_mentioned_date: string;
  attributes: Record<string, string>;
}

export interface EntityEdge {
  source: string;
  target: string;
  kind: string;
  weight: number;
}

export interface EntityGraphStats {
  total_entities: number;
  by_type: Record<string, number>;
  by_relationship: Record<string, number>;
  total_edges: number;
  top_mentioned: Array<{ name: string; mention_count: number }>;
}

export interface EntityGraphResponse {
  nodes: EntityNode[];
  edges: EntityEdge[];
  stats: EntityGraphStats;
  error?: string;
}

export interface ClassifyMoodResponse {
  mood: string;
  intensity: number;
  confidence: number;
  trigger: string;
  error?: string;
}

export interface ExtractedEntity {
  name: string;
  type: string;
  relationship: string;
  confidence: number;
  context_snippet: string;
  attributes: Record<string, string>;
}

export interface ExtractEntitiesResponse {
  entities: ExtractedEntity[];
  count: number;
  error?: string;
}

// ── H5 Persona-aware soul framing ────────────────────────────────────
// Renamed to SoulPersona* to avoid collision with the ComposerBar's
// PersonaSummary (chat-side persona templates) at line 761.
export interface SoulPersonaSummary {
  id: string;
  label: string;
  description: string;
  identity_language: string;
  tone_guidance: string;
  reflection_questions: string[];
  surface_format: "letter" | "log" | "narrative" | "vision";
}

export interface SoulPersonaOverlay extends SoulPersonaSummary {
  persona: string;
  persona_label: string;
  contextual_seed: string;
  markdown_block: string;
}

export interface SoulPersonaListResponse {
  personas: SoulPersonaSummary[];
  error?: string;
}

export interface SoulPersonaApplyResponse extends SoulPersonaOverlay {
  error?: string;
}

export interface SoulPersonaPreviewResponse {
  personas: SoulPersonaOverlay[];
  user_model_name: string;
  error?: string;
}

// ── Mind: world model + counterfactual self-test loop (Fable5) ────────────

export interface WorldModelConflict {
  value_a: string;
  value_b: string;
  winner: string;
  situation: string;
  resolution: string;
  confidence: number;
}

export interface ValuesHierarchy {
  revision_id: string;
  created_at: number;
  ranking: Record<string, number>;
  conflicts: WorldModelConflict[];
  context_overrides: Record<string, Record<string, number>>;
  narrative: string;
  supersedes: string | null;
}

export interface ReasoningStyle {
  revision_id: string;
  created_at: number;
  top_down_vs_bottom_up: number;
  data_vs_precedent: number;
  fast_revise_vs_slow_commit: number;
  risk_posture: number;
  decision_autonomy: number;
  confidence: Record<string, number>;
  narrative: string;
  supersedes: string | null;
}

export interface UncertaintyFlag {
  flag_id: string;
  created_at: number;
  kind: string;
  description: string;
  resolved: boolean;
  resolved_at: number | null;
  resolved_by: string | null;
}

export interface WorldModelResponse {
  ok: boolean;
  values_hierarchy: ValuesHierarchy | null;
  reasoning_style: ReasoningStyle | null;
  uncertainty_flags: UncertaintyFlag[];
  resolved_flags_count: number;
  hierarchy_history: string[];
  style_history: string[];
  injection_preview: string;
  error?: string;
}

export interface CounterfactualProbe {
  probe_id: string;
  created_at: number;
  target_kind: string;
  target_id: string;
  scenario: string;
  prediction: string;
  prediction_reasoning: string;
  confidence: number;
  status: "pending" | "confirmed" | "corrected" | "skipped";
  owner_response: string;
  graded_at: number | null;
}

export interface CalibrationRecord {
  total_probes: number;
  confirmed: number;
  corrected: number;
  skipped: number;
  brier_sum: number;
  accuracy: number;
  brier_score: number;
}

export interface ProbeListResponse {
  ok: boolean;
  probes: CounterfactualProbe[];
  calibration: CalibrationRecord;
  summary: string;
  error?: string;
}

export interface ProbeGradeResponse {
  ok: boolean;
  probe?: CounterfactualProbe;
  calibration?: CalibrationRecord;
  error?: string;
}

export interface ProbeGenerateResponse {
  ok: boolean;
  probe?: CounterfactualProbe;
  error?: string;
}
