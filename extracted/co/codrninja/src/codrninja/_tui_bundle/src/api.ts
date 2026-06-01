const BASE = process.env['CODRNINJA_SERVER'] ?? 'http://127.0.0.1:7384';

export async function withRetry<T>(fn: () => Promise<T>, retries = 3, delayMs = 1000): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try { return await fn(); }
    catch (e) {
      if (i === retries - 1) throw e;
      await new Promise(r => setTimeout(r, delayMs));
    }
  }
  throw new Error('unreachable');
}

export interface Session {
  id: string;
  name: string;
  slug?: string;
  created_at: string;
  updated_at?: string;
  model?: string;
  provider?: string;
  git_branch?: string;
  running?: boolean;
}

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface AgentEvent {
  type: 'assistant_chunk' | 'pre_tool_text' | 'tool_start' | 'tool_result' | 'result' | 'token_update' | 'permission_request';
  // assistant_chunk / pre_tool_text
  text?: string;
  // tool_start / tool_result / permission_request
  call_id?: string;
  tool?: string;
  args?: Record<string, unknown>;
  output?: string;
  success?: boolean;
  step?: number;
  max_steps?: number;
  perm_mode?: string;
  duration_ms?: number;
  line_start?: number;
  context_before?: string[];
  context_after?: string[];
  // permission_request
  action?: string;
  target?: string;
  params?: Record<string, unknown>;
  // token_update
  tokens_input?: number;
  tokens_output?: number;
  // result
  result?: {
    success: boolean;
    response?: string;
    error?: string;
    iterations?: number;
    tool_calls?: number;
    tokens?: { input: number; output: number };
  };
}

export async function fetchSessions(): Promise<Session[]> {
  const r = await fetch(`${BASE}/sessions`);
  const data = await r.json() as { sessions: Session[] };
  return data.sessions;
}

export async function fetchSession(name: string): Promise<{ messages: Message[] }> {
  const r = await fetch(`${BASE}/sessions/${encodeURIComponent(name)}`);
  if (!r.ok) throw new Error(`Session not found: ${name}`);
  return r.json() as Promise<{ messages: Message[] }>;
}

export async function deleteSession(name: string): Promise<void> {
  await fetch(`${BASE}/sessions/${encodeURIComponent(name)}`, { method: 'DELETE' });
}

export async function renameSession(oldName: string, newName: string): Promise<{ renamed: boolean; new_name: string }> {
  const r = await fetch(`${BASE}/sessions/${encodeURIComponent(oldName)}/rename`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ new_name: newName }),
  });
  if (!r.ok) { const e = await r.json() as { detail?: string }; throw new Error(e.detail ?? 'Rename failed'); }
  return r.json() as Promise<{ renamed: boolean; new_name: string }>;
}

export async function fetchVersion(): Promise<string> {
  try {
    const r = await fetch(`${BASE}/version`);
    const d = await r.json() as { version: string };
    return d.version;
  } catch {
    return '';
  }
}

export async function createSession(name: string): Promise<Session> {
  const r = await fetch(`${BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  return r.json() as Promise<Session>;
}

export async function fetchConfig(): Promise<Record<string, string>> {
  const r = await fetch(`${BASE}/config`);
  return r.json() as Promise<Record<string, string>>;
}

export type AuthMethod = 'oauth' | 'apikey' | 'setuptoken' | 'ollama' | null;

export interface ProviderInfo {
  name: string;
  active: boolean;
  authenticated: boolean;
  oauth: boolean;
  expired: boolean;
  auth_method?: AuthMethod;
}

export async function fetchProviders(): Promise<{ providers: ProviderInfo[]; current: string }> {
  const r = await fetch(`${BASE}/providers`);
  return r.json() as Promise<{ providers: ProviderInfo[]; current: string }>;
}

export async function setActiveProvider(provider: string): Promise<{ provider: string }> {
  const r = await fetch(`${BASE}/config/provider`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ provider }),
  });
  return r.json() as Promise<{ provider: string }>;
}


export async function setApiKey(provider: string, api_key: string): Promise<{ success: boolean }> {
  const r = await fetch(`${BASE}/providers/${encodeURIComponent(provider)}/apikey`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key }),
  });
  return r.json() as Promise<{ success: boolean }>;
}

export async function configureOllama(url: string): Promise<{ success: boolean; models: string[]; url: string }> {
  const r = await fetch(`${BASE}/providers/ollama/configure`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!r.ok) {
    const err = await r.json() as { detail?: string };
    throw new Error(err.detail ?? 'Failed');
  }
  return r.json() as Promise<{ success: boolean; models: string[]; url: string }>;
}

export type OAuthEvent =
  | { type: 'url'; url: string; url_file?: string | null }
  | { type: 'waiting' }
  | { type: 'success' }
  | { type: 'error'; error: string };

function streamOAuth(
  endpoint: string,
  onEvent: (e: OAuthEvent) => void,
  onDone: () => void,
): () => void {
  const ctrl = new AbortController();
  fetch(`${BASE}${endpoint}`, {
    method: 'POST', signal: ctrl.signal,
    headers: { 'Content-Type': 'application/json' },
    body: '{}',
  }).then(async (res) => {
    if (!res.body) { onDone(); return; }
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop() ?? '';
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try { onEvent(JSON.parse(line.slice(6)) as OAuthEvent); } catch { /* ignore */ }
        } else if (line.startsWith('event: done')) {
          onDone(); return;
        }
      }
    }
    onDone();
  }).catch((e: unknown) => {
    if (e instanceof Error && e.name !== 'AbortError') onDone();
  });
  return () => ctrl.abort();
}

export function streamOpenAIOAuth(
  onEvent: (e: OAuthEvent) => void,
  onDone: () => void,
): () => void {
  return streamOAuth('/providers/openai/oauth', onEvent, onDone);
}

export async function submitOAuthCallback(provider: string, callbackUrl: string): Promise<{ success: boolean }> {
  const r = await fetch(`${BASE}/providers/${provider}/oauth/callback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: callbackUrl }),
  });
  if (!r.ok) throw new Error(`callback submit failed: ${r.status}`);
  return r.json() as Promise<{ success: boolean }>;
}

export async function loadOpenAICredentials(): Promise<{ success: boolean; error?: string }> {
  const r = await fetch(`${BASE}/providers/openai/credentials`, { method: 'POST' });
  return r.json() as Promise<{ success: boolean; error?: string }>;
}

export interface ModelsResult {
  by_provider: Record<string, string[]>;
  models: string[];
  current_model: string;
  current_provider: string;
}

export async function fetchModels(): Promise<ModelsResult> {
  const r = await fetch(`${BASE}/models`);
  return r.json() as Promise<ModelsResult>;
}

export async function setReasoningLevel(level: string): Promise<{ reasoning_level: string }> {
  const r = await fetch(`${BASE}/config/reasoning`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ level }),
  });
  return r.json() as Promise<{ reasoning_level: string }>;
}

export async function setModel(model: string, provider?: string): Promise<{ model: string; provider: string }> {
  const r = await fetch(`${BASE}/config/model`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, provider }),
  });
  return r.json() as Promise<{ model: string; provider: string }>;
}

export async function setSessionModel(
  sessionName: string,
  model: string,
  provider?: string,
  setAsDefault = false,
): Promise<{ model: string; provider: string }> {
  const r = await fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/model`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, provider, set_as_default: setAsDefault }),
  });
  return r.json() as Promise<{ model: string; provider: string }>;
}

export interface OllamaServer {
  url: string;
  active: boolean;
  online: boolean;
  models: string[];
}

export async function fetchOllamaServers(): Promise<{ servers: OllamaServer[]; primary: string }> {
  const r = await fetch(`${BASE}/providers/ollama/servers`);
  return r.json() as Promise<{ servers: OllamaServer[]; primary: string }>;
}

export async function addOllamaServer(url: string): Promise<{ success: boolean; models: string[] }> {
  const r = await fetch(`${BASE}/providers/ollama/add-server`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!r.ok) { const e = await r.json() as { detail?: string }; throw new Error(e.detail ?? 'Failed'); }
  return r.json() as Promise<{ success: boolean; models: string[] }>;
}

export async function removeOllamaServer(url: string): Promise<{ success: boolean }> {
  const r = await fetch(`${BASE}/providers/ollama/remove-server`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return r.json() as Promise<{ success: boolean }>;
}

export async function toggleOllamaServer(url: string): Promise<{ success: boolean; active: string[] }> {
  const r = await fetch(`${BASE}/providers/ollama/toggle-server`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return r.json() as Promise<{ success: boolean; active: string[] }>;
}

export async function setOllamaApiKey(api_key: string, url = 'https://ollama.com'): Promise<{ success: boolean; models: string[] }> {
  const r = await fetch(`${BASE}/providers/ollama/apikey`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key, url }),
  });
  if (!r.ok) {
    const err = await r.json() as { detail?: string };
    throw new Error(err.detail ?? 'Failed to configure Ollama API key');
  }
  return r.json() as Promise<{ success: boolean; models: string[] }>;
}

export interface RunResult {
  success: boolean;
  output?: string;
  error?: string;
}

export async function fetchModelPrefs(): Promise<Record<string, string[]>> {
  const r = await fetch(`${BASE}/config/model-prefs`);
  const d = await r.json() as { prefs: Record<string, string[]> };
  return d.prefs ?? {};
}

export async function saveModelPrefs(prefs: Record<string, string[]>): Promise<void> {
  await fetch(`${BASE}/config/model-prefs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prefs }),
  });
}

export async function setPermissionMode(mode: string): Promise<{ success: boolean; mode: string }> {
  const r = await fetch(`${BASE}/permissions/mode`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode }),
  });
  return r.json() as Promise<{ success: boolean; mode: string }>;
}

export async function respondPermission(
  sessionName: string,
  callId: string,
  decision: 'yes' | 'always' | 'no' | 'never',
): Promise<{ success: boolean }> {
  const r = await fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/permission_respond`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ call_id: callId, decision }),
  });
  return r.json() as Promise<{ success: boolean }>;
}

export async function runExec(command: string): Promise<RunResult> {
  const r = await fetch(`${BASE}/run/exec`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command }),
  });
  return r.json() as Promise<RunResult>;
}

export async function runSearch(query: string): Promise<RunResult> {
  const r = await fetch(`${BASE}/run/search`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return r.json() as Promise<RunResult>;
}

export async function runFetch(url: string): Promise<RunResult> {
  const r = await fetch(`${BASE}/run/fetch`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return r.json() as Promise<RunResult>;
}

export async function runCommit(message: string): Promise<RunResult> {
  const r = await fetch(`${BASE}/run/commit`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  return r.json() as Promise<RunResult>;
}

export async function runTest(command = 'pytest -q'): Promise<RunResult> {
  const r = await fetch(`${BASE}/run/test`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command }),
  });
  return r.json() as Promise<RunResult>;
}

/** Attach to an already-running agent on the server (GET /sessions/{name}/stream).
 *  Calls onDone immediately if no run is active (404). */
export function reconnectStream(
  sessionName: string,
  onEvent: (event: AgentEvent) => void,
  onDone: () => void,
  onError: (err: Error) => void,
): () => void {
  const controller = new AbortController();

  fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/stream`, {
    method: 'GET',
    signal: controller.signal,
  })
    .then(async (res) => {
      if (res.status === 404) { onDone(); return; }
      if (!res.ok || !res.body) { onError(new Error(`HTTP ${res.status}`)); return; }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop() ?? '';
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const raw = line.slice(6).trim();
            if (raw) { try { onEvent(JSON.parse(raw) as AgentEvent); } catch { /* ignore */ } }
          } else if (line.startsWith('event: done')) {
            onDone(); return;
          }
        }
      }
      onDone();
    })
    .catch((err: unknown) => {
      if (err instanceof Error && err.name !== 'AbortError') onError(err);
    });

  return () => controller.abort();
}

export type AgentModeName =
  | 'build' | 'build-auto' | 'build-ask' | 'build-readonly'
  | 'plan' | 'review' | 'vision';

export function streamAgent(
  sessionName: string,
  message: string,
  onEvent: (event: AgentEvent) => void,
  onDone: () => void,
  onError: (err: Error) => void,
  mode: AgentModeName = 'build-ask',
  temperature?: number,
): () => void {
  const controller = new AbortController();

  fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, auto_approve: false, mode, temperature }),
    signal: controller.signal,
  })
    .then(async (res) => {
      if (!res.ok || !res.body) {
        onError(new Error(`HTTP ${res.status}`));
        return;
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buf = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop() ?? '';
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const raw = line.slice(6).trim();
            if (raw) {
              try {
                onEvent(JSON.parse(raw) as AgentEvent);
              } catch { /* ignore malformed */ }
            }
          } else if (line.startsWith('event: done')) {
            onDone();
            return;
          }
        }
      }
      onDone();
    })
    .catch((err: unknown) => {
      if (err instanceof Error && err.name !== 'AbortError') onError(err instanceof Error ? err : new Error(String(err)));
    });

  return () => controller.abort();
}

export async function pingHealth(): Promise<boolean> {
  try {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), 3000);
    const r = await fetch(`${BASE}/health`, { signal: ctrl.signal });
    clearTimeout(t);
    return r.ok;
  } catch {
    return false;
  }
}

export function restartServer(): void {
  const bin = process.env['CODRNINJA_BIN'] ?? 'codrninja';
  const port = (() => { try { return new URL(BASE).port || '7384'; } catch { return '7384'; } })();
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const cp = require('child_process') as typeof import('child_process');
    cp.spawn(bin, ['serve', '--port', port], { detached: true, stdio: 'ignore' }).unref();
  } catch { /* ignore — best-effort */ }
}

export interface ClaudeSession {
  session_id: string;
  path: string;
  preview: string;
  message_count: number;
  updated_at: string;
  project_hash: string;
}

export async function listClaudeSessions(): Promise<ClaudeSession[]> {
  try {
    const r = await fetch(`${BASE}/sessions/claude-import/list`);
    if (!r.ok) return [];
    const d = await r.json() as { sessions: ClaudeSession[] };
    return d.sessions;
  } catch {
    return [];
  }
}

export async function stopAgent(sessionName: string): Promise<void> {
  try {
    await fetch(`${BASE}/sessions/${encodeURIComponent(sessionName)}/stop`, { method: 'POST' });
  } catch { /* ignore */ }
}

export async function importClaudeSession(path: string, name: string): Promise<{ name: string; imported_messages: number }> {
  const r = await fetch(`${BASE}/sessions/claude-import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, name }),
  });
  if (!r.ok) {
    const err = await r.json() as { detail?: string };
    throw new Error(err.detail ?? 'Import failed');
  }
  return r.json() as Promise<{ name: string; imported_messages: number }>;
}
