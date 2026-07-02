/**
 * CVC dashboard API client (Phase B+C).
 *
 * Talks to the gateway's REST surface (cvc/gateway.py). Same-origin by default;
 * Vite dev proxy in vite.config.ts forwards `/api` → CVC_GATEWAY_URL.
 *
 * Themes are local-only (stored in localStorage by ThemeProvider) — no server
 * round-trip needed; the no-op stubs here just satisfy the ThemeProvider's
 * optional `apiClient` slot.
 */

import type { DashboardTheme, ThemeListResponse } from "@/themes/types";
export type * from "./types";
export type { CommitEntry as CommitSummary } from "./types";
import type {
  AdapterNegotiation,
  AdapterReport,
  AdapterSnapshot,
  AgentFromPromptResponse,
  AgentTemplate,
  AgentsListResponse,
  AnalyticsResponse,
  AuditEntry,
  BranchRequest,
  BranchSummary,
  ChatRequest,
  CommitEntry,
  CommitRequest,
  ConnectionInfo,
  CurrentModel,
  DiffResult,
  GatewayConfig,
  HiveMemoryEntry,
  HiveMemoryResponse,
  HiveMemoryStats,
  HiveMindAgent,
  MCPStatus,
  MCPTool,
  MemoryBlobsResponse,
  MemoryContextResponse,
  MemoryStatsResponse,
  MergeRequest,
  ModelCatalog,
  OperationResult,
  OpsStatus,
  RecallResult,
  RegisterAgentRequest,
  RestoreRequest,
  SecurityAuditEntry,
  SecuritySentinelStats,
  SecurityStatus,
  SecurityVault,
  ServicesResponse,
  SettingsResponse,
  SettingsSchema,
  SoulCorrectionRequest,
  SoulCorrectionResponse,
  SoulCorrectionsResponse,
  SoulDreams,
  SoulLetterGenerateResponse,
  SoulLetterResponse,
  SoulLettersResponse,
  SoulLifeStory,
  SoulNarrative,
  SoulUserModel,
  SoulPreservationDisableRequest,
  SoulPreservationDisableResponse,
  SoulPreservationEnableRequest,
  SoulPreservationEnableResponse,
  SoulPreservationResponse,
  SoulPreservationSummarizeRequest,
  SoulPreservationSummarizeResponse,
  SoulWillArtifact,
  SoulWillCreateRequest,
  SoulWillCreateResponse,
  SoulWillExecutorAddRequest,
  SoulWillExecutorAddResponse,
  SoulWillExecutorRemoveRequest,
  SoulWillExecutorRemoveResponse,
  SoulWillReleaseRequest,
  SoulWillResponse,
  TimePortalResponse,
  SnapshotsListResponse,
  EmotionalArcResponse,
  EntityGraphResponse,
  EventSpineEntry,
  ClassifyMoodResponse,
  ExtractEntitiesResponse,
  PortalEnterResponse,
  PortalActiveResponse,
  PortalExitResponse,
  PortalChatContextResponse,
  PortalDaysResponse,
  SoulPersonaListResponse,
  SoulPersonaApplyResponse,
  SoulPersonaPreviewResponse,
  SquadInfo,
  StatsResponse,
  SwarmBroadcast,
  SwarmIdentity,
  SwarmPeer,
  SwarmPolicy,
  TimelineEntry,
  VCSStatus,
  WorkspaceInfo,
} from "./types";

function readBase(): string {
  const w = typeof window !== "undefined" ? window : undefined;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const injected = (w as any)?.__CVC_API_BASE__;
  if (typeof injected === "string" && injected.length) {
    return injected.replace(/\/+$/, "");
  }
  return "/api";
}

export const CVC_API_BASE = readBase();

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export async function fetchJSON<T>(path: string, init?: RequestInit): Promise<T> {
  const url = path.startsWith("http") ? path : `${CVC_API_BASE}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: {
      "content-type": "application/json",
      accept: "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!res.ok) {
    let body = "";
    try {
      body = await res.text();
    } catch {
      /* ignore */
    }
    throw new ApiError(
      res.status,
      `${init?.method ?? "GET"} ${path} → ${res.status} ${res.statusText}${body ? ` — ${body.slice(0, 200)}` : ""}`,
    );
  }
  return (await res.json()) as T;
}

const get = <T>(path: string) => fetchJSON<T>(path);
const post = <T>(path: string, body?: unknown) =>
  fetchJSON<T>(path, {
    method: "POST",
    body: body != null ? JSON.stringify(body) : undefined,
  });
const put = <T>(path: string, body?: unknown) =>
  fetchJSON<T>(path, {
    method: "PUT",
    body: body != null ? JSON.stringify(body) : undefined,
  });
const del = <T>(path: string) =>
  fetchJSON<T>(path, { method: "DELETE" });

/** Build a ?workspace_path=… query string for any /api/soul/* call.
 *  hotfix/soul-wiring-2026-06-30 — the backend accepts this param
 *  on every soul endpoint; when present it resolves the .cvc/
 *  directly instead of trusting fragile host-state caches. */
function soulQ(workspacePath: string | undefined, path: string): string {
  if (!workspacePath) return path;
  const sep = path.includes("?") ? "&" : "?";
  return `${path}${sep}workspace_path=${encodeURIComponent(workspacePath)}`;
}
// ─────────────────────────────────────────────────────────────────────────
// Domain-grouped API surface
// ─────────────────────────────────────────────────────────────────────────

export const api = {
  // ── health / workspace ─────────────────────────────────────────────────
  async health(): Promise<{ status: string; service?: string; version?: string }> {
    // /health is mounted outside /api on the gateway
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    return fetchJSON(`${origin}/health`);
  },
  workspaceCurrent(workspace_path?: string): Promise<WorkspaceInfo> {
    const q = workspace_path
      ? `?workspace_path=${encodeURIComponent(workspace_path)}`
      : "";
    return get<WorkspaceInfo>(`/workspace/current${q}`);
  },
  workspaceAdd(path: string, switchTo: boolean = true): Promise<{
    status: string;
    workspace_id: string;
    path: string;
    name: string;
    branch: string;
    switched: boolean;
  }> {
    return post("/workspace/add", { path, switch: switchTo });
  },
  // v2.91.46 — Remove a workspace from the persisted list.
  // `purge=true` also deletes the on-disk .cvc/ directory (irreversible).
  workspaceRemove(
    path: string,
    purge: boolean = false,
  ): Promise<{
    status: string;
    removed: boolean;
    path: string;
    was_active: boolean;
    new_active: string | null;
    purged?: boolean;
    purge_error?: string;
    memory_entries_dropped?: number;
  }> {
    return del(`/workspace/remove?path=${encodeURIComponent(path)}&purge=${purge}`);
  },

  // v2.91.49 — Native OS folder picker. The gateway shells out to the
  // platform's native dialog (osascript on Mac, PowerShell FolderBrowserDialog
  // on Windows, zenity/kdialog/tkinter on Linux) and returns the selected
  // absolute path. Returns {cancelled: true, path: null} on user Cancel.
  // NOTE: this is intentionally POST not GET — the gateway endpoint is
  // blocking (the dialog is modal) and we don't want it cached or
  // pre-fetched by the browser.
  async pickFolder(): Promise<{ path: string | null; cancelled: boolean }> {
    return post<{ path: string | null; cancelled: boolean }>("/system/pick-folder", {});
  },

  // v2.91.46 — Persistent user memory (lives in ~/.cvc/memory/, survives
  // gateway restarts and workspace deletes).
  userMemoryList(opts?: {
    category?: "preference" | "note" | "fact";
    scope?: string;
    search?: string;
  }): Promise<{
    entries: Array<{
      id: string;
      category: string;
      content: string;
      scope: string;
      tags: string[];
      source: string;
      created_at: number;
      updated_at: number;
    }>;
    stats: {
      total: number;
      by_category: Record<string, number>;
      by_scope: Record<string, number>;
      path: string;
      exists: boolean;
      size_bytes: number;
    };
  }> {
    const params = new URLSearchParams();
    if (opts?.category) params.set("category", opts.category);
    if (opts?.scope) params.set("scope", opts.scope);
    if (opts?.search) params.set("search", opts.search);
    const q = params.toString();
    return get(`/memory${q ? "?" + q : ""}`);
  },
  userMemoryCreate(body: {
    category: "preference" | "note" | "fact";
    content: string;
    scope?: string;
    tags?: string[];
    source?: string;
  }): Promise<{
    id: string;
    category: string;
    content: string;
    scope: string;
    tags: string[];
    source: string;
    created_at: number;
    updated_at: number;
  }> {
    return post("/memory", body);
  },
  userMemoryDelete(id: string): Promise<{ status: string; deleted: string }> {
    return del(`/memory/${id}`);
  },
  userMemoryWipe(body: { category?: string; scope?: string } = {}): Promise<{
    status: string;
    removed: number;
  }> {
    return post("/memory/wipe", body);
  },
  async transcribe(blob: Blob, filename: string = "recording.webm"): Promise<{ text: string; provider: string }> {
    const form = new FormData();
    form.append("audio", blob, filename);
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    const res = await fetch(`${origin}/api/voice/transcribe`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      const detail = await res.text().catch(() => "");
      const err = new Error(`Transcribe failed (${res.status}): ${detail || res.statusText}`);
      (err as any).status = res.status;
      throw err;
    }
    return res.json();
  },

  // ── voice setup (free offline transcription) ───────────────────────────
  async voiceStatus(): Promise<{
    installed: boolean;
    model: string;
    loaded: boolean;
    providers: { local_whisper: boolean; groq: boolean; openai: boolean; gemini: boolean };
  }> {
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    const res = await fetch(`${origin}/api/voice/local/status`);
    if (!res.ok) throw new Error(`voiceStatus failed (${res.status})`);
    return res.json();
  },

  /**
   * Install faster-whisper locally. Streams progress lines via callback.
   * Resolves with the final phase ("done" or "error") + message.
   */
  async voiceInstall(onLog?: (line: string) => void): Promise<{ ok: boolean; msg: string }> {
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    const res = await fetch(`${origin}/api/voice/local/install`, { method: "POST" });
    if (!res.ok || !res.body) {
      const t = await res.text().catch(() => "");
      throw new Error(`voiceInstall failed (${res.status}): ${t || res.statusText}`);
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    let last: { ok: boolean; msg: string } = { ok: false, msg: "Install ended without status." };
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const parts = buf.split("\n\n");
      buf = parts.pop() ?? "";
      for (const chunk of parts) {
        const line = chunk.split("\n").find((l) => l.startsWith("data:"));
        if (!line) continue;
        try {
          const evt = JSON.parse(line.slice(5).trim());
          if (evt?.msg && onLog) onLog(String(evt.msg));
          if (evt?.phase === "done") last = { ok: true, msg: String(evt.msg || "Installed.") };
          else if (evt?.phase === "error") last = { ok: false, msg: String(evt.msg || "Install failed.") };
        } catch { /* ignore parse errors */ }
      }
    }
    return last;
  },

  // ── file upload (multimodal attachments) ───────────────────────────────
  async uploadFiles(files: File[]): Promise<{ files: import("./types").Attachment[] }> {
    const form = new FormData();
    for (const f of files) form.append("files", f, f.name);
    const res = await fetch(`${CVC_API_BASE}/files/upload`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      const detail = await res.text().catch(() => "");
      throw new Error(`Upload failed (${res.status}): ${detail || res.statusText}`);
    }
    return res.json();
  },

  // ── ops ────────────────────────────────────────────────────────────────
  opsStatus(opts?: { workspace_path?: string }): Promise<OpsStatus> {
    const q = opts?.workspace_path
      ? `?workspace_path=${encodeURIComponent(opts.workspace_path)}`
      : "";
    return get<Record<string, unknown>>(`/ops/status${q}`).then((r) => ({
      branch: (r.branch as string) ?? (r.current_branch as string) ?? "main",
      head: (r.head as string) ?? "",
      total_commits: (r.total_commits as number) ?? 0,
      workspace: r.workspace as string | undefined,
    }));
  },
  opsBranches(): Promise<{ branches: BranchSummary[] } | string[]> {
    return get("/ops/branches");
  },
  opsTimeline(
    limit = 50,
    workspace_path?: string,
  ): Promise<{ entries: TimelineEntry[] } | TimelineEntry[]> {
    const q = new URLSearchParams({ limit: String(limit) });
    if (workspace_path) q.set("workspace_path", workspace_path);
    return get(`/ops/timeline?${q.toString()}`);
  },

  // ── Event Spine (C5) ──────────────────────────────────────────────
  // Reads from ~/.cvc/events/ — append-only ledger of EVERY interaction
  // across all workspaces and channels. Singular.
  events(opts?: {
    workspace_path?: string;
    channel?: string | string[];
    kind?: string | string[];
    actor?: string;
    session_id?: string;
    since?: number;
    until?: number;
    tags?: string | string[];
    search?: string;
    limit?: number;
    offset?: number;
    reverse?: boolean;
  }): Promise<{
    events: EventSpineEntry[];
    total: number;
    limit: number;
    offset: number;
    has_more: boolean;
  }> {
    const params = new URLSearchParams();
    if (!opts) opts = {};
    if (opts.workspace_path) params.set("workspace", opts.workspace_path);
    if (opts.channel) params.set("channel", Array.isArray(opts.channel) ? opts.channel.join(",") : opts.channel);
    if (opts.kind) params.set("kind", Array.isArray(opts.kind) ? opts.kind.join(",") : opts.kind);
    if (opts.actor) params.set("actor", opts.actor);
    if (opts.session_id) params.set("session_id", opts.session_id);
    if (opts.since !== undefined) params.set("since", String(opts.since));
    if (opts.until !== undefined) params.set("until", String(opts.until));
    if (opts.tags) params.set("tags", Array.isArray(opts.tags) ? opts.tags.join(",") : opts.tags);
    if (opts.search) params.set("search", opts.search);
    if (opts.limit !== undefined) params.set("limit", String(opts.limit));
    if (opts.offset !== undefined) params.set("offset", String(opts.offset));
    if (opts.reverse !== undefined) params.set("reverse", String(opts.reverse));
    return get(`/events?${params.toString()}`);
  },
  eventsStats(opts?: { workspace_path?: string; since?: number; days?: number }): Promise<{
    total: number;
    by_kind: Record<string, number>;
    by_channel: Record<string, number>;
    by_day: Array<{ day: string; count: number }>;
  }> {
    const params = new URLSearchParams();
    if (opts?.workspace_path) params.set("workspace", opts.workspace_path);
    if (opts?.since !== undefined) params.set("since", String(opts.since));
    if (opts?.days !== undefined) params.set("days", String(opts.days));
    return get(`/events/stats?${params.toString()}`);
  },
  eventsInfo(): Promise<{
    root: string;
    files: Array<{ file: string; events: number; bytes: number }>;
    total_events: number;
    total_bytes: number;
    known_kinds: string[];
    known_channels: string[];
  }> {
    return get("/events/info");
  },
  opsCommit(req: CommitRequest): Promise<OperationResult> {
    return post("/ops/commit", req);
  },
  opsBranch(req: BranchRequest): Promise<OperationResult> {
    return post("/ops/branch", req);
  },
  opsMerge(req: MergeRequest): Promise<OperationResult> {
    return post("/ops/merge", req);
  },
  opsRestore(req: RestoreRequest): Promise<OperationResult> {
    return post("/ops/restore", req);
  },
  opsRecall(query: string, limit = 10): Promise<RecallResult> {
    return get(`/ops/recall?query=${encodeURIComponent(query)}&limit=${limit}`);
  },
  opsDiff(hash1: string, hash2: string): Promise<DiffResult> {
    return get(`/ops/diff?hash1=${encodeURIComponent(hash1)}&hash2=${encodeURIComponent(hash2)}`);
  },

  // ── gateway / analytics ────────────────────────────────────────────────
  services(): Promise<ServicesResponse> {
    return get("/gateway/services");
  },
  serviceAction(service: string, action: string): Promise<OperationResult> {
    return post(`/gateway/services/${encodeURIComponent(service)}/${encodeURIComponent(action)}`);
  },
  analytics(): Promise<AnalyticsResponse> {
    return get("/gateway/analytics");
  },
  commits(limit = 50, workspace_path?: string): Promise<CommitEntry[]> {
    const q = new URLSearchParams({ limit: String(limit) });
    if (workspace_path) q.set("workspace_path", workspace_path);
    return get(`/gateway/commits?${q.toString()}`);
  },
  gatewayConfig(): Promise<GatewayConfig> {
    return get("/gateway/config");
  },

  // ── memory ─────────────────────────────────────────────────────────────
  memoryStats(): Promise<MemoryStatsResponse> {
    return get("/memory/stats");
  },
  memoryBlobs(limit = 20): Promise<MemoryBlobsResponse> {
    return get(`/memory/blobs?limit=${limit}`);
  },
  memoryContext(): Promise<MemoryContextResponse> {
    return get("/memory/context");
  },

  // ── models ─────────────────────────────────────────────────────────────
  modelCatalog(): Promise<ModelCatalog> {
    return get("/models/catalog");
  },
  // v3.3.43 — Rich per-provider catalog with context windows, capabilities,
  // base URLs, and 30+ providers (z.ai/GLM, Kimi, StepFun, Alibaba, …)
  // pulled from the vendored Hermes Agent tree + models.dev cache.
  catalogProviders(): Promise<{
    providers: Array<{
      id: string;
      display_name: string;
      base_url: string;
      env_vars: string[];
      is_aggregator: boolean;
      model_count: number;
      models: Array<{
        id: string;
        name: string;
        context_window: number;
        max_output: number;
        reasoning: boolean;
        tool_call: boolean;
        vision: boolean;
      }>;
    }>;
    provider_count: number;
  }> {
    return get("/catalog/providers");
  },
  catalogFlat(): Promise<ModelCatalog> {
    // Same wire shape as modelCatalog() but with the new Hermes-catalog
    // providers baked in. Use this when you want the dashboard picker
    // to surface z.ai/GLM, Kimi, etc. alongside the hand-written ones.
    return get("/catalog/flat");
  },
  catalogRefresh(): Promise<{ ok: boolean; provider_count: number; duration_ms: number }> {
    return post("/catalog/refresh", {});
  },
  currentModel(): Promise<CurrentModel> {
    return get("/models/current");
  },
  switchModel(provider: string, model: string): Promise<OperationResult> {
    return post("/models/switch", { provider, model });
  },
  /**
   * v2.90 — GitHub Copilot dynamic model discovery.
   *
   * Calls `GET /api/providers/copilot/models` which uses the user's
   * Copilot token to query GitHub's `GET /models` endpoint and returns
   * the LIVE list of models enabled on their plan/org. Different from
   * the static `ModelCatalog` from `/api/catalog/flat` — that one is
   * hand-curated + models.dev, this one is account-scoped truth.
   *
   * When the user has no Copilot token configured (or token exchange
   * fails), returns `{ok: true, models: [], source: "no_token"}` so
   * the UI can show a friendly "configure Copilot auth" hint instead
   * of an error.
   */
  copilotModels(forceRefresh = false): Promise<import("./types").CopilotModelsResponse> {
    const tail = forceRefresh ? "?force_refresh=true" : "";
    return get(`/providers/copilot/models${tail}`);
  },

  // ── chat (streaming SSE) ───────────────────────────────────────────────
  async *chatStream(req: ChatRequest): AsyncGenerator<import("./types").ChatEvent, void, unknown> {
    const res = await fetch(`${CVC_API_BASE}/chat`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ ...req, stream: true }),
    });
    if (!res.ok) throw new ApiError(res.status, `Chat ${res.status}`);
    const reader = res.body?.getReader();
    if (!reader) return;
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop()!;
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") return;
          try {
            const parsed = JSON.parse(data);
            if (parsed.type) {
              yield parsed as import("./types").ChatEvent;
            } else if (parsed.choices?.[0]?.delta?.content) {
              yield { type: "text", content: parsed.choices[0].delta.content };
            }
          } catch {
            /* skip malformed SSE */
          }
        }
      }
    }
  },
  chatModels(): Promise<{ models: string[] }> {
    return get("/chat/models");
  },

  // ── MCP ────────────────────────────────────────────────────────────────
  mcpTools(): Promise<{ tools: MCPTool[]; total?: number }> {
    return get("/mcp/tools");
  },
  mcpStatus(): Promise<MCPStatus> {
    return get("/mcp/status");
  },

  // ── VCS ────────────────────────────────────────────────────────────────
  vcsStatus(): Promise<VCSStatus> {
    return get("/vcs/status");
  },

  // ── audit / stats / sessions / connections ─────────────────────────────
  audit(limit = 100): Promise<AuditEntry[] | { entries: AuditEntry[] }> {
    return get(`/audit?limit=${limit}`);
  },
  stats(workspace_path?: string): Promise<StatsResponse> {
    const q = workspace_path
      ? `?workspace_path=${encodeURIComponent(workspace_path)}`
      : "";
    return get(`/stats${q}`);
  },
  sessions(): Promise<unknown[] | { sessions: unknown[] }> {
    return get("/sessions");
  },
  connections(): Promise<{ connections: ConnectionInfo[] } | ConnectionInfo[]> {
    return get("/connections");
  },

  // ── external channels (Telegram, Discord, Slack, WhatsApp, Matrix, Email, Webhook) ──
  channels: {
    list(): Promise<{
      channels: Array<{
        name: string;
        enabled: boolean;
        healthy: boolean;
        capabilities: string[];
        started_at: number | null;
        last_activity_at: number | null;
        last_error: string | null;
        info: Record<string, unknown>;
        config_keys: string[];
      }>;
    }> {
      return get("/channels");
    },
    status(name: string): Promise<Record<string, unknown>> {
      return get(`/channels/${name}/status`);
    },
    start(name: string, config: Record<string, unknown>): Promise<{ ok: boolean; name: string }> {
      return post(`/channels/${name}/start`, config);
    },
    stop(name: string): Promise<{ ok: boolean; name: string }> {
      return post(`/channels/${name}/stop`, {});
    },
    send(name: string, payload: Record<string, unknown>): Promise<{ ok: boolean; result: unknown }> {
      return post(`/channels/${name}/send`, payload);
    },
  },

  // ── hive mind agents ───────────────────────────────────────────────────
  hivemindAgents(): Promise<HiveMindAgent[] | { agents: HiveMindAgent[] }> {
    return get("/hivemind/agents");
  },
  swarmTopology(): Promise<{
    nodes: Array<{
      id: string;
      name?: string;
      role?: string;
      rank?: string;
      squad?: string;
      tier?: "mc" | "captain" | "specialist" | "misc";
      status?: string;
    }>;
    squads: Array<{ name: string; members: string[]; captain: string | null; count: number }>;
    edges: Array<{ from: string; to: string; type: "command" | "squad" }>;
    total_nodes: number;
    total_squads: number;
    workspace?: string;
  }> {
    return get("/swarm");
  },
  hivemindFeed(limit = 30): Promise<{
    events: Array<{
      hash?: string;
      agent_id?: string;
      branch?: string;
      message?: string;
      timestamp?: number;
    }>;
    total: number;
  }> {
    return get(`/hivemind/feed?limit=${limit}`);
  },
  hivemindStats(): Promise<{
    total_agents: number;
    total_commits: number;
    by_squad: Record<string, number>;
    by_rank: Record<string, number>;
    commits_last_hour: number;
    commits_last_24h: number;
  }> {
    return get("/hivemind/stats");
  },
  hivemindRegister(req: RegisterAgentRequest): Promise<OperationResult> {
    return post("/hivemind/register", req);
  },
  hivemindRemove(agentId: string): Promise<OperationResult> {
    return del(`/hivemind/agents/${encodeURIComponent(agentId)}`);
  },

  // ── hive memory ────────────────────────────────────────────────────────
  hiveMemory(opts?: {
    query?: string;
    category?: string;
    agent_id?: string;
    limit?: number;
  }): Promise<HiveMemoryResponse> {
    const params = new URLSearchParams();
    if (opts?.query) params.set("query", opts.query);
    if (opts?.category) params.set("category", opts.category);
    if (opts?.agent_id) params.set("agent_id", opts.agent_id);
    params.set("limit", String(opts?.limit ?? 50));
    return get(`/hivemind/memory?${params}`);
  },
  hiveMemoryWrite(
    agent_id: string,
    content: string,
    category = "general",
    tags: string[] = [],
  ): Promise<{ status: string; entry: HiveMemoryEntry }> {
    return post("/hivemind/memory", { agent_id, content, category, tags });
  },
  hiveMemoryStats(): Promise<HiveMemoryStats> {
    return get("/hivemind/memory/stats");
  },
  hiveMemorySummary(limit = 10): Promise<{ context: string }> {
    return get(`/hivemind/memory/summary?limit=${limit}`);
  },
  hiveMemoryCompact(): Promise<OperationResult> {
    return post("/hivemind/memory/compact");
  },

  // ── settings ───────────────────────────────────────────────────────────
  settings(): Promise<SettingsResponse> {
    return get("/settings");
  },
  settingsSchema(): Promise<SettingsSchema> {
    return get("/settings/schema");
  },
  settingsUpdate(level: "global" | "project" | "local", data: Record<string, unknown>): Promise<OperationResult> {
    return put(`/settings/${level}`, data);
  },
  settingsReset(level: string): Promise<OperationResult> {
    return post("/settings/reset", { level });
  },

  // ── soul layer (P5) ────────────────────────────────────────────────────
  // hotfix/soul-wiring-2026-06-30 — every read MUST carry the active
  // workspace path. Without it the backend falls back to the host's
  // active-workspace pointer, which can drift across tab refreshes,
  // gateway restarts, or page navigation. Threading workspacePath
  // through here is what makes the Soul page actually reflect the
  // user model of the project the user is currently in.
  soulLifeStory(workspacePath?: string): Promise<SoulLifeStory> {
    return get(soulQ(workspacePath, "/soul/life-story"));
  },
  soulUserModel(workspacePath?: string): Promise<SoulUserModel> {
    return get(soulQ(workspacePath, "/soul/user-model"));
  },
  soulDreams(workspacePath?: string, limit = 10): Promise<SoulDreams> {
    const base = soulQ(workspacePath, "/soul/dreams");
    return get(`${base}${base.includes("?") ? "&" : "?"}limit=${limit}`);
  },
  soulNarrative(workspacePath?: string): Promise<SoulNarrative> {
    return get(soulQ(workspacePath, "/soul/narrative"));
  },
  // POST /api/soul/refresh — force a fresh narrative synthesis from
  // the current soul store. Used by the Soul page's Refresh button
  // so the dashboard sees an updated narrative without having to
  // wait for the next chat turn to fire per_turn_soul.
  soulRefresh(workspacePath?: string): Promise<{ ok: boolean; narrative_preview?: string; error?: string }> {
    return post(soulQ(workspacePath, "/soul/refresh"), {});
  },
  // Wipe the soul back to a fresh-install state. Confirm-phrase gated
  // server-side; the only caller is the Soul page's hidden Shift+click
  // affordance on the SOULWARE badge. Returns the backup path so the
  // UI can show the user where their old model lives if they ever
  // want to recover it.
  soulReset(workspacePath?: string): Promise<{ ok: boolean; backup?: string | null; dropped_events?: number; error?: string }> {
    return post(soulQ(workspacePath, "/soul/reset"), {
      confirm: "RESET MY SOUL",
    });
  },
  // ── H1 Time Portal — what you knew then vs what you know now ──────────
  soulTimePortal(
    workspacePath?: string,
    target?: string,
  ): Promise<TimePortalResponse> {
    const base = soulQ(workspacePath, "/soul/time-portal");
    const tail = target
      ? `${base.includes("?") ? "&" : "?"}target=${encodeURIComponent(target)}`
      : "";
    return get(`${base}${tail}`);
  },
  soulSnapshots(
    workspacePath?: string,
    limit = 50,
    trigger?: string,
  ): Promise<SnapshotsListResponse> {
    const parts: string[] = [`limit=${limit}`];
    if (trigger) parts.push(`trigger=${encodeURIComponent(trigger)}`);
    const base = soulQ(workspacePath, "/soul/snapshots");
    const sep = base.includes("?") ? "&" : "?";
    return get(`${base}${sep}${parts.join("&")}`);
  },
  // ── H2 Emotional Arc + Entity Graph ──────────────────────────────────
  soulEmotionalArc(
    workspacePath?: string,
    bucket: "day" | "week" | "month" = "day",
    sinceDays = 90,
  ): Promise<EmotionalArcResponse> {
    const base = soulQ(workspacePath, "/soul/emotional-arc");
    const sep = base.includes("?") ? "&" : "?";
    return get(
      `${base}${sep}bucket=${bucket}&since_days=${sinceDays}`,
    );
  },
  soulEntityGraph(
    workspacePath?: string,
    minMentions = 1,
    entityType?: string,
  ): Promise<EntityGraphResponse> {
    const parts = [`min_mentions=${minMentions}`];
    if (entityType) parts.push(`entity_type=${encodeURIComponent(entityType)}`);
    const base = soulQ(workspacePath, "/soul/entity-graph");
    const sep = base.includes("?") ? "&" : "?";
    return get(`${base}${sep}${parts.join("&")}`);
  },
  classifySoulMood(text: string): Promise<ClassifyMoodResponse> {
    return post("/soul/classify-mood", { text });
  },
  extractSoulEntities(text: string): Promise<ExtractEntitiesResponse> {
    return post("/soul/extract-entities", { text });
  },
  // ── H5 Persona-aware soul framing ───────────────────────────────────
  soulPersonas(): Promise<SoulPersonaListResponse> {
    return get("/soul/personas");
  },
  soulPersonaApply(personaId: string): Promise<SoulPersonaApplyResponse> {
    return get(`/soul/persona/${encodeURIComponent(personaId)}/apply`);
  },
  soulPersonaPreview(): Promise<SoulPersonaPreviewResponse> {
    return get("/soul/persona/preview");
  },
  // ── H1b Time Portal session lifecycle ─────────────────────────────────
  // Enter the portal — pin chat to a historical snapshot.
  // target can be "snap-<id>", an ISO date "YYYY-MM-DD", or a Unix timestamp.
  // portal_id is generated client-side (so multiple tabs can hold
  // different portals simultaneously); it's stored in localStorage so a
  // page reload restores the portal banner state.
  portalEnter(
    portalId: string,
    target: string,
    workspacePath?: string,
    label?: string,
  ): Promise<PortalEnterResponse> {
    return post(
      `${soulQ(workspacePath, "/soul/time-portal/enter")}`,
      { portal_id: portalId, target, label },
    );
  },
  // Look up an active portal session (or all of them).
  portalActive(
    portalId?: string,
    workspacePath?: string,
  ): Promise<PortalActiveResponse> {
    const base = soulQ(workspacePath, "/soul/time-portal/active");
    const tail = portalId
      ? `${base.includes("?") ? "&" : "?"}portal_id=${encodeURIComponent(portalId)}`
      : "";
    return get(`${base}${tail}`);
  },
  // Exit the portal — clear the session so chat returns to present.
  portalExit(
    portalId: string,
    workspacePath?: string,
  ): Promise<PortalExitResponse> {
    return post(`${soulQ(workspacePath, "/soul/time-portal/exit")}`, {
      portal_id: portalId,
    });
  },
  // Fetch the formatted chat-context block for a portal session.
  portalChatContext(
    portalId: string,
    workspacePath?: string,
  ): Promise<PortalChatContextResponse> {
    const base = soulQ(workspacePath, "/soul/time-portal/chat-context");
    const sep = base.includes("?") ? "&" : "?";
    return get(`${base}${sep}portal_id=${encodeURIComponent(portalId)}`);
  },
  // v3.5.1 — TIME PORTAL day-scope: enter the portal pinned to a whole
  // day. Backend consolidates every snapshot for the date into a single
  // canonical model and pins chat to it.
  portalEnterDay(
    portalId: string,
    date: string,
    workspacePath?: string,
    label?: string,
  ): Promise<PortalEnterResponse> {
    return post(
      `${soulQ(workspacePath, "/soul/time-portal/enter-day")}`,
      { portal_id: portalId, date, label },
    );
  },
  // v3.5.1 — list every day that has at least one snapshot. The UI uses
  // this to render the day-row accordion (one row per day instead of one
  // per snapshot — collapses the cluttered per-second pill grid).
  portalDays(workspacePath?: string): Promise<PortalDaysResponse> {
    return get(soulQ(workspacePath, "/soul/time-portal/days"));
  },
  // ── soul letters (P6 — the soul writes back) ──────────────────────────
  soulLetters(limit = 12): Promise<SoulLettersResponse> {
    return get(`/soul/letters?limit=${limit}`);
  },
  soulLetter(weekOf: string): Promise<SoulLetterResponse> {
    return get(`/soul/letters/${encodeURIComponent(weekOf)}`);
  },
  generateSoulLetter(
    body: {
      week_of?: string;
      adapter_id?: string;
      model?: string;
      force?: boolean;
      /** Manual trigger from the dashboard "Write Now" button.
       *  Walks back up to 12 weeks to find a week with commits if
       *  the current week is empty. The Sunday cron never sends this. */
      manual?: boolean;
    } = {},
  ): Promise<SoulLetterGenerateResponse> {
    return post("/soul/letters/generate", body);
  },
  // ── soul corrections (P7 — self-correction loop) ─────────────────────
  soulCorrections(
    workspacePath?: string,
    includeSuperseded: boolean = true,
  ): Promise<SoulCorrectionsResponse> {
    const base = soulQ(workspacePath, "/soul/corrections");
    return get(
      `${base}${base.includes("?") ? "&" : "?"}include_superseded=${includeSuperseded ? "true" : "false"}`,
    );
  },
  correctSoulClaim(body: SoulCorrectionRequest): Promise<SoulCorrectionResponse> {
    return post("/soul/correct", body);
  },
  // ── soul will (P8 — digital-parents arc) ────────────────────────────
  soulWill(): Promise<SoulWillResponse> {
    return get("/soul/will");
  },
  createSoulWill(body: SoulWillCreateRequest): Promise<SoulWillCreateResponse> {
    return post("/soul/will/create", body);
  },
  addSoulWillExecutor(
    body: SoulWillExecutorAddRequest,
  ): Promise<SoulWillExecutorAddResponse> {
    return post("/soul/will/executor/add", body);
  },
  removeSoulWillExecutor(
    body: SoulWillExecutorRemoveRequest,
  ): Promise<SoulWillExecutorRemoveResponse> {
    return post("/soul/will/executor/remove", body);
  },
  /** Triggers the soul release. Returns the response object — the
   *  artifact body comes back as application/json with
   *  Content-Disposition: attachment, so we save it to disk via the
   *  browser's download mechanism. Returns metadata about the download. */
  async downloadSoulWill(
    body: SoulWillReleaseRequest = {},
  ): Promise<{
    ok: boolean;
    filename: string;
    will_id?: string;
    version?: number;
    audit_chain_hash?: string;
    error?: string;
  }> {
    try {
      const url = `${CVC_API_BASE}/soul/will/release`;
      const res = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        let detail = "";
        try {
          detail = await res.text();
        } catch {
          /* ignore */
        }
        return {
          ok: false,
          filename: "",
          error: `${res.status} ${res.statusText}${detail ? ` — ${detail.slice(0, 200)}` : ""}`,
        };
      }
      // Read response headers BEFORE consuming the body.
      const willId = res.headers.get("X-Soul-Release") || undefined;
      const version = res.headers.get("X-Soul-Version") || undefined;
      const auditHash = res.headers.get("X-Audit-Chain-Hash") || undefined;
      const disposition = res.headers.get("Content-Disposition") || "";
      // Try to extract filename from header; fallback to will_id-version.
      const match = /filename="?([^";]+)"?/i.exec(disposition);
      const filename =
        match?.[1] ||
        (willId && version ? `${willId}-v${version}.soul` : "soul-will.soul");
      const blob = await res.blob();
      // Trigger browser download
      const objectUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = objectUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      // Defer revoke so the browser has time to start the download.
      setTimeout(() => URL.revokeObjectURL(objectUrl), 5000);
      return {
        ok: true,
        filename,
        will_id: willId,
        version: version ? Number(version) : undefined,
        audit_chain_hash: auditHash,
      };
    } catch (e) {
      return {
        ok: false,
        filename: "",
        error: String((e as Error)?.message ?? e),
      };
    }
  },
  async parseSoulWillArtifact(text: string): Promise<SoulWillArtifact | null> {
    try {
      return JSON.parse(text) as SoulWillArtifact;
    } catch {
      return null;
    }
  },
  // ── soul preservation (P9 — "the last session handshake") ───────────
  soulPreservation(): Promise<SoulPreservationResponse> {
    return get("/soul/preservation");
  },
  enableSoulPreservation(
    body: SoulPreservationEnableRequest = {},
  ): Promise<SoulPreservationEnableResponse> {
    return post("/soul/preservation/enable", body);
  },
  disableSoulPreservation(
    body: SoulPreservationDisableRequest = {},
  ): Promise<SoulPreservationDisableResponse> {
    return post("/soul/preservation/disable", body);
  },
  generateSoulPreservationSummary(
    body: SoulPreservationSummarizeRequest = {},
  ): Promise<SoulPreservationSummarizeResponse> {
    return post("/soul/preservation/summarize", body);
  },

  // ── universal adapter system (Phase 7.1) ──────────────────────────────
  adapters(): Promise<AdapterSnapshot> {
    return get("/adapters");
  },
  healthyAdapters(): Promise<{ adapters: AdapterReport[]; count: number }> {
    return get("/adapters/healthy");
  },
  negotiateAdapters(req: { capabilities: string[] }): Promise<AdapterNegotiation> {
    return post("/adapters/negotiate", req);
  },

  // ── Apple-grade security (Phase 7.2) ──────────────────────────────────
  securityStatus(): Promise<SecurityStatus> {
    return get("/security/status");
  },
  securityInit(passphrase: string): Promise<{ ok: boolean; status: SecurityVault }> {
    return post("/security/initialize", { passphrase });
  },
  securityUnlock(passphrase: string): Promise<{ ok: boolean; status: SecurityVault }> {
    return post("/security/unlock", { passphrase });
  },
  securityLock(): Promise<{ ok: boolean; status: SecurityVault }> {
    return post("/security/lock", {});
  },
  securityAudit(n = 50): Promise<{ entries: SecurityAuditEntry[]; count: number }> {
    return get(`/security/audit?n=${n}`);
  },
  securityAuditVerify(): Promise<{ ok: boolean; message: string; entries: number }> {
    return post("/security/audit/verify", {});
  },
  sentinelCheck(url: string): Promise<{ url: string; allowed: boolean }> {
    return post("/security/sentinel/check", { url });
  },
  sentinelStats(): Promise<SecuritySentinelStats> {
    return get("/security/sentinel/stats");
  },

  // ── swarm cluster (Phase 7.3) ──────────────────────────────────────────
  swarmIdentity(): Promise<SwarmIdentity> {
    return get("/swarm/identity");
  },
  swarmRename(display_name: string): Promise<SwarmIdentity> {
    return post("/swarm/rename", { display_name });
  },
  swarmPolicy(): Promise<SwarmPolicy> {
    return get("/swarm/policy");
  },
  swarmSetPolicy(p: Partial<SwarmPolicy>): Promise<SwarmPolicy> {
    return post("/swarm/policy", p);
  },
  swarmPeers(): Promise<{ peers: SwarmPeer[]; count: number }> {
    return get("/swarm/peers");
  },
  swarmAddPeer(p: Partial<SwarmPeer>): Promise<SwarmPeer> {
    return post("/swarm/peers", p);
  },
  swarmRemovePeer(peer_id: string): Promise<{ ok: boolean; removed: string }> {
    return del(`/swarm/peers/${encodeURIComponent(peer_id)}`);
  },
  swarmBroadcast(topic: string, payload: Record<string, unknown>): Promise<SwarmBroadcast> {
    return post("/swarm/broadcast", { topic, payload });
  },
  swarmInbox(limit = 50): Promise<{ broadcasts: SwarmBroadcast[]; count: number }> {
    return get(`/swarm/inbox?limit=${limit}`);
  },
  apiKeys(): Promise<Record<string, string>> {
    return get("/settings/keys");
  },
  setApiKey(provider: string, key: string): Promise<OperationResult> {
    return put(`/settings/keys/${encodeURIComponent(provider)}`, { api_key: key });
  },
  removeApiKey(provider: string): Promise<OperationResult> {
    return del(`/settings/keys/${encodeURIComponent(provider)}`);
  },
  testApiKey(provider: string): Promise<OperationResult> {
    return post(`/settings/keys/${encodeURIComponent(provider)}/test`);
  },
  hooks(): Promise<Record<string, unknown[]>> {
    return get<unknown>("/settings/hooks").then((r) => {
      // Gateway wraps as {hooks: {...}} — unwrap to flat dict.
      if (r && typeof r === "object" && "hooks" in r && typeof (r as { hooks: unknown }).hooks === "object") {
        return ((r as { hooks: Record<string, unknown[]> }).hooks) || {};
      }
      return (r as Record<string, unknown[]>) || {};
    });
  },
  addHook(event: string, command: string): Promise<OperationResult> {
    return post("/settings/hooks", { event, command });
  },
  removeHook(event: string, index: number): Promise<OperationResult> {
    return del(`/settings/hooks/${encodeURIComponent(event)}/${index}`);
  },
  envVars(): Promise<Record<string, string>> {
    return get<unknown>("/settings/env").then((r) => {
      if (r && typeof r === "object" && "env" in r && typeof (r as { env: unknown }).env === "object") {
        return ((r as { env: Record<string, string> }).env) || {};
      }
      return (r as Record<string, string>) || {};
    });
  },
  setEnvVars(vars: Record<string, string>): Promise<OperationResult> {
    return put("/settings/env", vars);
  },
  settingsLevel(level: "global" | "project" | "local"): Promise<Record<string, unknown>> {
    return get(`/settings/${level}`);
  },

  // ── agent templates ────────────────────────────────────────────────────
  agentsList(): Promise<AgentsListResponse> {
    return get("/agents");
  },
  agentsBuiltin(): Promise<AgentTemplate[]> {
    return get("/agents/builtin");
  },
  agentCreate(template: Partial<AgentTemplate>): Promise<{ status: string; agent: AgentTemplate }> {
    return post("/agents", template);
  },
  agentFromPrompt(prompt: string): Promise<AgentFromPromptResponse> {
    return post("/agents/from-prompt", { prompt });
  },
  agentDetail(id: string): Promise<AgentTemplate> {
    return get(`/agents/${encodeURIComponent(id)}`);
  },
  agentUpdate(id: string, data: Partial<AgentTemplate>): Promise<{ status: string; agent: AgentTemplate }> {
    return put(`/agents/${encodeURIComponent(id)}`, data);
  },
  agentDelete(id: string): Promise<OperationResult> {
    return del(`/agents/${encodeURIComponent(id)}`);
  },
  agentHistory(id: string): Promise<CommitEntry[]> {
    return get(`/agents/${encodeURIComponent(id)}/history`);
  },
  squadCreate(name: string, agents: string[]): Promise<OperationResult> {
    return post("/agents/squad", { name, agents });
  },
  squadList(): Promise<SquadInfo[]> {
    return get<{ squads: SquadInfo[] }>("/agents/squads").then((r) => r.squads ?? []);
  },

  // ── gateway workspaces / sessions / telemetry ──────────────────────────
  gatewayWorkspaces(): Promise<import("./types").GatewayWorkspacesResponse> {
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    return fetchJSON(`${origin}/gateway/workspaces`);
  },
  gatewayRegisterWorkspace(
    req: import("./types").RegisterWorkspaceRequest,
  ): Promise<OperationResult> {
    const origin = typeof window !== "undefined" ? window.location.origin : "";
    return fetchJSON(`${origin}/gateway/register_workspace`, {
      method: "POST",
      body: JSON.stringify(req),
    });
  },
  workspaceClose(workspace_id: string): Promise<OperationResult> {
    return post("/workspace/close", { workspace_id });
  },
  workspaceSwitch(workspace_id: string): Promise<OperationResult> {
    return post("/workspace/switch", { workspace_id });
  },

  // ── git (active-workspace scoped) ───────────────────────────────────────
  gitStatus(workspacePath?: string): Promise<import("./types").GitStatusInfo> {
    const q = workspacePath ? `?workspace_path=${encodeURIComponent(workspacePath)}` : "";
    return get<import("./types").GitStatusInfo>(`/git/status${q}`);
  },
  gitBranches(workspacePath?: string): Promise<import("./types").GitBranchesResponse> {
    const q = workspacePath ? `?workspace_path=${encodeURIComponent(workspacePath)}` : "";
    return get<import("./types").GitBranchesResponse>(`/git/branches${q}`);
  },
  gitCheckout(
    name: string,
    opts: { create?: boolean; force?: boolean; workspacePath?: string } = {},
  ): Promise<import("./types").GitCheckoutResponse> {
    const q = opts.workspacePath ? `?workspace_path=${encodeURIComponent(opts.workspacePath)}` : "";
    return post<import("./types").GitCheckoutResponse>(`/git/checkout${q}`, {
      name,
      create: !!opts.create,
      force: !!opts.force,
    });
  },
  gitSync(
    opts: { remote?: string; push?: boolean; rebase?: boolean; workspacePath?: string } = {},
  ): Promise<import("./types").GitSyncResult> {
    const q = opts.workspacePath ? `?workspace_path=${encodeURIComponent(opts.workspacePath)}` : "";
    return post<import("./types").GitSyncResult>(`/git/sync${q}`, {
      remote: opts.remote ?? "origin",
      push: opts.push ?? true,
      rebase: opts.rebase ?? false,
    });
  },

  // ── personas ───────────────────────────────────────────────────────────
  personas(): Promise<{ personas: import("./types").PersonaSummary[] }> {
    return get("/personas");
  },
  persona(id: string): Promise<import("./types").PersonaDetail> {
    return get(`/personas/${encodeURIComponent(id)}`);
  },
  personaSkills(id: string): Promise<{ skills: string[] }> {
    return get(`/personas/${encodeURIComponent(id)}/skills`);
  },
  activePersona(): Promise<import("./types").PersonaActive> {
    return get("/personas/active");
  },
  setActivePersona(
    workspace_id: string,
    persona_id: string,
  ): Promise<import("./types").PersonaActive> {
    return post("/personas/active", { workspace_id, persona_id });
  },
  createPersona(body: {
    id: string;
    name: string;
    description?: string;
    default_model?: string;
    default_provider?: string;
    system_prompt?: string;
    skills?: string[];
  }): Promise<import("./types").PersonaDetail> {
    return post("/personas", body);
  },
  updatePersona(
    id: string,
    body: Partial<{
      name: string;
      description: string;
      default_model: string;
      default_provider: string;
      system_prompt: string;
      skills: string[];
    }>,
  ): Promise<import("./types").PersonaDetail> {
    return put(`/personas/${encodeURIComponent(id)}`, body);
  },
  deletePersona(id: string): Promise<{ deleted: string }> {
    return del(`/personas/${encodeURIComponent(id)}`);
  },
  skillsCatalog(): Promise<{
    skills: { id: string; kind: string; description: string }[];
    count: number;
  }> {
    return get("/skills");
  },

  // ── conversation history ───────────────────────────────────────────────
  conversations(
    workspacePath?: string,
    limit = 200,
  ): Promise<import("./types").ConversationThread[]> {
    const q = new URLSearchParams();
    if (workspacePath) q.set("workspace_path", workspacePath);
    q.set("limit", String(limit));
    return get(`/conversations?${q.toString()}`);
  },
  conversation(threadId: string): Promise<import("./types").ConversationDetail> {
    return get(`/conversations/${encodeURIComponent(threadId)}`);
  },
  createConversation(req: {
    workspace_path: string;
    title?: string;
    persona_id?: string;
    first_message?: { role: string; content: string };
  }): Promise<import("./types").ConversationThread> {
    return post("/conversations", req);
  },
  appendMessage(
    threadId: string,
    role: string,
    content: string,
  ): Promise<import("./types").ConversationThread> {
    return post(
      `/conversations/${encodeURIComponent(threadId)}/messages`,
      { role, content },
    );
  },
  renameConversation(
    threadId: string,
    title: string,
  ): Promise<import("./types").ConversationThread> {
    return fetchJSON(
      `/conversations/${encodeURIComponent(threadId)}`,
      { method: "PATCH", body: JSON.stringify({ title }) },
    );
  },
  deleteConversation(threadId: string): Promise<{ status: string }> {
    return fetchJSON(
      `/conversations/${encodeURIComponent(threadId)}`,
      { method: "DELETE" },
    );
  },

  // ── reasoning effort ───────────────────────────────────────────────────
  getReasoningEffort(): Promise<{ effort: import("./types").ReasoningEffort }> {
    return get("/chat/reasoning_effort");
  },
  setReasoningEffort(
    effort: import("./types").ReasoningEffort,
  ): Promise<{ effort: import("./types").ReasoningEffort }> {
    return put("/chat/reasoning_effort", { effort });
  },

  // ── approval mode (VS Code-style: default | bypass | autopilot) ────────
  // Shared state with CLI (`cvc agent` /mode command) — single source of truth.
  getApprovalMode(): Promise<{ mode: "default" | "bypass" | "autopilot" }> {
    return get("/chat/approval-mode");
  },
  setApprovalMode(
    mode: "default" | "bypass" | "autopilot",
  ): Promise<{ mode: "default" | "bypass" | "autopilot" }> {
    return post("/chat/approval-mode", { mode });
  },

  // ── loop config (v2.92.3 — CostBudget + ToolRiskRegistry) ──────────
  // Shared state with the CLI. The dashboard flips these mid-session;
  // the agent_chat and ws_chat paths enforce them.
  getLoopConfig(): Promise<{
    max_budget_usd: number;
    spent_usd: number;
    remaining_usd: number;
    exhausted: boolean;
    accept_network: boolean;
    yes_destroy: boolean;
    warn_threshold: number;
  }> {
    return get("/chat/loop-config");
  },
  setLoopConfig(body: {
    max_budget_usd?: number;
    accept_network?: boolean;
    yes_destroy?: boolean;
    reset_spent?: boolean;
  }): Promise<{
    max_budget_usd: number;
    spent_usd: number;
    remaining_usd: number;
    exhausted: boolean;
    accept_network: boolean;
    yes_destroy: boolean;
    warn_threshold: number;
  }> {
    return post("/chat/loop-config", body);
  },
  resetLoopSpend(): Promise<{
    max_budget_usd: number;
    spent_usd: number;
    remaining_usd: number;
    exhausted: boolean;
    accept_network: boolean;
    yes_destroy: boolean;
    warn_threshold: number;
  }> {
    return post("/chat/loop-config/reset-spend", {});
  },

  // ── context meter ──────────────────────────────────────────────────────
  contextMeter(): Promise<import("./types").ContextMeter> {
    return get("/chat/context_meter");
  },

  // ── workspace tree ─────────────────────────────────────────────────────
  workspaceTree(
    path = "",
    depth = 2,
    showHidden = false,
  ): Promise<import("./types").WorkspaceTreeNode> {
    const params = new URLSearchParams();
    if (path) params.set("path", path);
    params.set("depth", String(depth));
    if (showHidden) params.set("show_hidden", "true");
    return get(`/workspace/tree?${params}`);
  },
  workspaceFile(path: string): Promise<{
    name: string;
    path: string;
    rel_path: string;
    size: number;
    mtime: number;
    ext: string;
    mime: string;
    is_text: boolean;
    truncated: boolean;
    content: string;
  }> {
    return get(`/workspace/file?path=${encodeURIComponent(path)}`);
  },
  workspaceFileDiff(path: string): Promise<{
    status: "clean" | "modified" | "untracked" | "not_git" | "error";
    rel_path: string;
    hunks: Array<{
      old_start: number;
      old_lines: number;
      new_start: number;
      new_lines: number;
      header: string;
      lines: Array<{ kind: "add" | "del" | "ctx"; content: string }>;
    }>;
    message?: string;
  }> {
    return get(`/workspace/file-diff?path=${encodeURIComponent(path)}`);
  },
  telemetry(event: import("./types").TelemetryEvent): Promise<unknown> {
    return post("/telemetry", event).catch(() => ({}));
  },

  // ── providers / credentials (Phase-1 surface) ──────────────────────────
  providers(): Promise<{ providers: import("./types").ProviderProfile[]; count: number }> {
    return get("/providers");
  },
  setupRegistry(): Promise<{
    providers: Array<{
      key: string;
      display_name: string;
      description: string;
      hint?: string;
      color?: string;
      recommended: boolean;
      free_tier: boolean;
      local: boolean;
      transport: string;
      auth_kind: string;
      env_key: string;
      default_model: string;
    }>;
    provider_count: number;
    features: Array<{
      key: string;
      name: string;
      category: string;
      description: string;
      default_enabled: boolean;
      requires_provider?: string | null;
    }>;
    feature_count: number;
    feature_categories: string[];
    schema_version: number;
  }> {
    return get("/setup/registry");
  },
  provider(name: string): Promise<import("./types").ProviderProfile> {
    return get(`/providers/${encodeURIComponent(name)}`);
  },
  credentials(provider?: string): Promise<{
    credentials: Record<string, import("./types").PooledCredentialView[]>;
    total: number;
  }> {
    const q = provider ? `?provider=${encodeURIComponent(provider)}` : "";
    return get(`/credentials${q}`);
  },
  addCredential(req: {
    provider: string;
    label: string;
    access_token: string;
    auth_type?: string;
    base_url?: string;
  }): Promise<{ ok: boolean; credential: import("./types").PooledCredentialView }> {
    return post("/credentials", req);
  },
  removeCredential(provider: string, id: string): Promise<{ ok: boolean }> {
    return del(`/credentials/${encodeURIComponent(provider)}/${encodeURIComponent(id)}`);
  },
  resetCredential(provider: string, id: string): Promise<{ ok: boolean }> {
    return post(`/credentials/${encodeURIComponent(provider)}/${encodeURIComponent(id)}/reset`);
  },
  credentialStats(): Promise<import("./types").CredentialPoolStats> {
    return get("/credentials/stats");
  },
  fallbackPreview(provider: string, model: string): Promise<{
    requested: { provider: string; model: string };
    chain: { provider: string; model: string }[];
  }> {
    return get(
      `/fallback/preview?provider=${encodeURIComponent(provider)}&model=${encodeURIComponent(model)}`,
    );
  },

  // ── agentic loop ────────────────────────────────────────────────────────
  loopState(): Promise<import("./types").LoopSnapshot> {
    return get("/loop/state");
  },
  loopConfig(): Promise<import("./types").LoopConfig> {
    return get("/loop/config");
  },

  // ── trajectory ──────────────────────────────────────────────────────────
  trajectoryFiles(): Promise<{ dir: string; files: import("./types").TrajectoryFile[] }> {
    return get("/trajectory/files");
  },
  trajectoryTail(
    file?: string,
    limit = 50,
  ): Promise<{ path: string; turns: import("./types").TrajectoryTurn[] }> {
    const qs = `?limit=${limit}` + (file ? `&file=${encodeURIComponent(file)}` : "");
    return get(`/trajectory/tail${qs}`);
  },
  trajectorySummary(file?: string): Promise<import("./types").TrajectorySummary> {
    const qs = file ? `?file=${encodeURIComponent(file)}` : "";
    return get(`/trajectory/summary${qs}`);
  },

  // ── team (Core 4) ───────────────────────────────────────────────────────
  team(): Promise<import("./types").TeamSnapshot> {
    return get("/team");
  },
  teamEnsure(): Promise<{ inserted: unknown[]; count: number }> {
    return post("/team/ensure", {});
  },

  // ── themes (server-persisted active id; theme defs live client-side) ────
  async getThemes(): Promise<ThemeListResponse> {
    try {
      const r = await get<{ active_theme?: string; default_theme?: string }>(
        "/dashboard/theme",
      );
      return { themes: [], active: r.active_theme ?? "cvc-red" };
    } catch {
      return { themes: [], active: "cvc-red" };
    }
  },
  async setTheme(name: string): Promise<{ active: string }> {
    try {
      const r = await post<{ active_theme: string }>("/dashboard/theme", {
        theme_id: name,
      });
      return { active: r.active_theme ?? name };
    } catch {
      return { active: name };
    }
  },
  async createTheme(_definition: DashboardTheme): Promise<{ name: string }> {
    return { name: _definition.name };
  },

  // ── DX namespace (Phase B) ───────────────────────────────────────────
  dx: {
    slashRegistry(): Promise<import("./types").DxSlashRegistry> {
      return get("/dx/slash/registry");
    },
    slashRun(
      command: string,
      thread_id?: string | null,
      args?: Record<string, unknown>,
    ): Promise<import("./types").DxSlashRunResult> {
      return post("/dx/slash/run", { command, thread_id, args });
    },
    pin(
      thread_id: string,
      message_id: number,
      pinned: boolean,
    ): Promise<{ ok: boolean; message_id: number; pinned: boolean }> {
      return post(`/dx/threads/${encodeURIComponent(thread_id)}/pin`, {
        message_id,
        pinned,
      });
    },
    listPinned(thread_id: string): Promise<import("./types").DxPinnedList> {
      return get(`/dx/threads/${encodeURIComponent(thread_id)}/pinned`);
    },
    reply(
      thread_id: string,
      reply_to: number,
      content: string,
      role: "user" | "assistant" | "system" = "user",
    ): Promise<import("./types").DxReplyResult> {
      return post(`/dx/threads/${encodeURIComponent(thread_id)}/reply`, {
        reply_to,
        content,
        role,
      });
    },
    listInsights(
      workspace_path: string,
      thread_id?: string | null,
      limit = 50,
    ): Promise<import("./types").DxInsightsList> {
      const q = new URLSearchParams();
      q.set("workspace_path", workspace_path);
      if (thread_id) q.set("thread_id", thread_id);
      q.set("limit", String(limit));
      return get(`/dx/insights?${q.toString()}`);
    },
    addInsight(req: {
      workspace_path: string;
      thread_id?: string | null;
      kind: "preference" | "fact" | "pitfall" | "decision" | "rule";
      content: string;
      weight?: number;
    }): Promise<import("./types").DxInsight> {
      return post("/dx/insights", req);
    },
    deleteInsight(id: number): Promise<{ ok: boolean }> {
      return del(`/dx/insights/${id}`);
    },
    filesSearch(
      workspace_path: string,
      q: string,
      limit = 40,
    ): Promise<import("./types").DxFilesResult> {
      const sp = new URLSearchParams();
      sp.set("workspace_path", workspace_path);
      sp.set("q", q);
      sp.set("limit", String(limit));
      return get(`/dx/files/search?${sp.toString()}`);
    },
    cost(thread_id?: string | null): Promise<import("./types").DxCostSummary> {
      const sp = new URLSearchParams();
      if (thread_id) sp.set("thread_id", thread_id);
      const qs = sp.toString();
      return get(`/dx/cost${qs ? `?${qs}` : ""}`);
    },
    exportThread(
      thread_id: string,
      format: "md" | "json" = "md",
    ): Promise<import("./types").DxExportResult> {
      return get(
        `/dx/threads/${encodeURIComponent(thread_id)}/export?format=${format}`,
      );
    },
  },
};

// ─────────────────────────────────────────────────────────────────────────
// WebSocket — dashboard event bus (existing)
// ─────────────────────────────────────────────────────────────────────────

export function dashboardWsUrl(): string {
  const base = CVC_API_BASE.startsWith("http")
    ? CVC_API_BASE
    : `${typeof window !== "undefined" ? window.location.origin : ""}${CVC_API_BASE}`;
  return base.replace(/^http/, "ws").replace(/\/api$/, "") + "/ws/dashboard";
}

// ─────────────────────────────────────────────────────────────────────────
// WebSocket — chat bridge (/api/ws/chat)
// ─────────────────────────────────────────────────────────────────────────

export function chatWsUrl(): string {
  const base = CVC_API_BASE.startsWith("http")
    ? CVC_API_BASE
    : `${typeof window !== "undefined" ? window.location.origin : ""}${CVC_API_BASE}`;
  return base.replace(/^http/, "ws") + "/ws/chat";
}

type ChatHandler = (ev: import("./types").ChatEvent) => void;

export class ChatWS {
  private ws: WebSocket | null = null;
  private url: string;
  private handlers: Partial<Record<import("./types").ChatEvent["type"], ChatHandler>> = {};
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectDelay = 2000;
  private readonly maxReconnectDelay = 30_000;
  private alive = true;
  private pendingSend: unknown | null = null;

  // v2.68.14 — resumable-turn state.
  // turnId is set by the server's first `turn_start` frame and cleared shortly
  // after `done`. lastSeq tracks the highest server-assigned seq we've seen so
  // we can ask the server to replay missed events on reconnect.
  private turnId: string | null = null;
  private lastSeq = 0;
  private inFlight = false;
  private turnIdClearTimer: ReturnType<typeof setTimeout> | null = null;

  constructor(url?: string) {
    this.url = url ?? chatWsUrl();
  }

  on(type: import("./types").ChatEvent["type"], handler: ChatHandler): this {
    this.handlers[type] = handler;
    return this;
  }

  off(type: import("./types").ChatEvent["type"]): this {
    delete this.handlers[type];
    return this;
  }

  private dispatch(ev: import("./types").ChatEvent): void {
    const h = this.handlers[ev.type];
    if (h) h(ev);
  }

  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) return;
    try {
      this.ws = new WebSocket(this.url);
    } catch {
      this.scheduleReconnect();
      return;
    }
    this.ws.onopen = () => {
      this.reconnectDelay = 2000;
      // Resume path takes precedence over pendingSend: if a turn is mid-flight
      // we must NOT start a new one — we ask the server to replay from
      // lastSeq+1 and the existing turn continues streaming on this socket.
      if (this.inFlight && this.turnId) {
        try {
          this.ws!.send(JSON.stringify({
            type: "resume",
            turn_id: this.turnId,
            last_seq: this.lastSeq,
          }));
        } catch {
          /* will retry on next reconnect */
        }
        return;
      }
      if (this.pendingSend !== null) {
        this.ws!.send(JSON.stringify(this.pendingSend));
        this.pendingSend = null;
      }
    };
    this.ws.onmessage = (ev) => {
      try {
        const raw = JSON.parse(ev.data) as Record<string, unknown>;
        // Server tags every frame with a monotonic `seq`. Drop replayed
        // duplicates and advance lastSeq for new ones.
        const seqVal = raw["seq"];
        if (typeof seqVal === "number" && Number.isFinite(seqVal)) {
          if (seqVal <= this.lastSeq) return;
          this.lastSeq = seqVal;
        }
        const turnIdVal = raw["turn_id"];
        if (typeof turnIdVal === "string" && turnIdVal && this.turnId !== turnIdVal) {
          // turn_start or first server frame of a new turn — adopt its id.
          this.turnId = turnIdVal;
          this.inFlight = true;
        }
        const msg = raw as unknown as import("./types").ChatEvent;
        // turn_start / resume_complete / resume_failed are control frames the
        // UI doesn't need to render — keep them internal.
        const t = msg.type as string;
        if (t === "turn_start" || t === "resume_complete") {
          return;
        }
        if (t === "resume_failed") {
          // Server has no record of this turn — give up and let the user retry.
          this.clearTurn();
          this.dispatch({
            type: "status",
            message: "Connection lost — the previous request couldn't be recovered. Please try again.",
          } as import("./types").ChatEvent);
          return;
        }
        if (t === "done") {
          // Mark not-in-flight immediately so a reconnect during the late-frame
          // grace window doesn't try to resume a finished turn. Hold the
          // turnId briefly in case a stray frame arrives.
          this.inFlight = false;
          if (this.turnIdClearTimer) clearTimeout(this.turnIdClearTimer);
          this.turnIdClearTimer = setTimeout(() => {
            this.turnId = null;
            this.lastSeq = 0;
            this.turnIdClearTimer = null;
          }, 5000);
        }
        this.dispatch(msg);
      } catch {
        /* ignore malformed frames */
      }
    };
    this.ws.onclose = () => {
      if (this.alive) this.scheduleReconnect();
    };
    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  disconnect(): void {
    this.alive = false;
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.turnIdClearTimer) clearTimeout(this.turnIdClearTimer);
    this.clearTurn();
    this.ws?.close();
    this.ws = null;
  }

  send(req: {
    messages: import("./types").ChatMessage[];
    model?: string;
    persona_id?: string;
    reasoning_effort?: import("./types").ReasoningEffort;
    provider?: string;
    workspace_id?: string;
    workspace_path?: string;
    thread_id?: string;
    reply_to?: number;
    attachments?: import("./types").Attachment[];
    /** v3.5.0 — Time Portal: pin chat to a historical soul snapshot. */
    portal_session_id?: string;
  }): void {
    // Reset turn state for the new request.
    this.clearTurn();
    this.inFlight = true;
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(req));
    } else {
      this.pendingSend = req;
      if (!this.ws || this.ws.readyState === WebSocket.CLOSED) this.connect();
    }
  }

  abort(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: "abort" }));
    }
  }

  confirmTool(decision: "allow_once" | "allow_always" | "trust_all" | "deny" | "deny_suggest"): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: "confirm", result: decision }));
    }
  }

  private clearTurn(): void {
    if (this.turnIdClearTimer) {
      clearTimeout(this.turnIdClearTimer);
      this.turnIdClearTimer = null;
    }
    this.turnId = null;
    this.lastSeq = 0;
    this.inFlight = false;
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.reconnectTimer = setTimeout(() => this.connect(), this.reconnectDelay);
    this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, this.maxReconnectDelay);
  }
}
