const BASE = '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

// ── Dynamic discovery ──

export interface ModeInfo { name: string; [k: string]: unknown }
export const getModes = () => request<{ modes: Record<string, ModeInfo> }>('/modes')

export const getPhases = (mode?: string) =>
  request<{ mode: string; phases: string[] }>(`/phases${mode ? `?mode=${mode}` : ''}`)

export interface StepDef {
  id: string; description: string; agent_type: string | null;
  parallel: boolean; user_action: boolean; interactive: boolean;
  spawn_prompt: string | null; required_artifacts: string[];
  after: string[]; type: string; guard: unknown; gateway: unknown;
  knowledge?: { enabled: boolean; intent?: string; max_results?: number; min_score?: number; categories?: string[]; severity?: string; biz_context?: string } | null;
}
export const getSteps = (mode?: string) =>
  request<{ mode: string; steps: Record<string, StepDef[]> }>(`/steps${mode ? `?mode=${mode}` : ''}`)

export const getAgents = () => request<{ agents: string[] }>('/agents')

export interface StepTemplate {
  id: string; label: string; description: string; phase: string;
  agent_type?: string | null; spawn_prompt?: string | null;
  actions?: string[]; interactive?: boolean; user_action?: boolean;
  type?: string; guard?: unknown; gateway?: unknown;
  knowledge?: StepDef['knowledge'];
  source: 'builtin' | 'user'; file: string;
}
export const getStepTemplates = () => request<{ templates: StepTemplate[] }>('/step-templates')

// ── Tasks ──

export interface Task {
  id: string; title: string; description?: string;
  phase?: string; status?: string; mode?: string;
  iteration?: number; score_history?: unknown[];
  subtasks?: unknown[]; [k: string]: unknown;
}
export const listTasks = () => request<{ tasks: Task[] }>('/tasks')
export const getTask = (id: string) => request<Task>(`/tasks/${id}`)
export const updateTask = (id: string, body: Record<string, unknown>) =>
  request<{ success: boolean }>(`/tasks/${id}`, { method: 'PUT', body: JSON.stringify(body) })
export const transitionPhase = (id: string, phase: string) =>
  request<unknown>(`/tasks/${id}/phase`, { method: 'POST', body: JSON.stringify({ phase }) })

export interface StepProgress { steps: Record<string, { status: string; updated_at: number }> }
export const getTaskSteps = (id: string) => request<StepProgress>(`/tasks/${id}/steps`)
export const getTaskStats = (id: string) => request<unknown>(`/tasks/${id}/stats`)

export const updateStep = (taskId: string, stepId: string, status: string) =>
  request<unknown>(`/tasks/${taskId}/step/${stepId}`, { method: 'POST', body: JSON.stringify({ status }) })

export const updateSubtask = (taskId: string, stId: string, body: Record<string, unknown>) =>
  request<unknown>(`/tasks/${taskId}/subtask/${stId}`, { method: 'PUT', body: JSON.stringify(body) })

// ── Config ──

export const getConfig = () => request<Record<string, unknown>>('/config')
export const putConfig = (body: Record<string, unknown>) =>
  request<{ success: boolean }>('/config', { method: 'PUT', body: JSON.stringify(body) })
export const getWorkflow = () => request<Record<string, unknown>>('/workflow')
export const putWorkflow = (body: Record<string, unknown>) =>
  request<{ success: boolean }>('/workflow', { method: 'PUT', body: JSON.stringify(body) })
export const getWorkflowMode = (mode: string) => request<Record<string, unknown>>(`/workflow/${mode}`)
export const putWorkflowMode = (mode: string, body: Record<string, unknown>) =>
  request<{ success: boolean }>(`/workflow/${mode}`, { method: 'PUT', body: JSON.stringify(body) })

// ── Knowledge ──

export const knowledgeHealth = () => request<unknown>('/knowledge/health')
export const knowledgeEntries = (params?: { q?: string; domain?: string; status?: string }) => {
  const qs = new URLSearchParams()
  if (params?.q) qs.set('q', params.q)
  if (params?.domain) qs.set('domain', params.domain)
  if (params?.status) qs.set('status', params.status)
  const query = qs.toString()
  return request<{ entries: unknown[] }>(`/knowledge/entries${query ? `?${query}` : ''}`)
}
export const knowledgeEntry = (id: string) => request<unknown>(`/knowledge/entries/${id}`)
export const knowledgeApprove = (ids: string[]) =>
  request<unknown>('/knowledge/approve', { method: 'POST', body: JSON.stringify({ ids }) })
export const knowledgeReject = (ids: string[]) =>
  request<unknown>('/knowledge/reject', { method: 'POST', body: JSON.stringify({ ids }) })

// ── Archive ──

export const listArchive = () => request<{ tasks: Task[] }>('/archive')
export const getArchivedTask = (id: string) => request<Task>(`/archive/${id}`)

// ── SSE ──

export function connectSSE(
  handlers: Record<string, (data: unknown) => void>,
  onError?: (e: Event) => void,
): EventSource {
  const es = new EventSource('/api/events')
  es.addEventListener('connected', (e) => handlers.connected?.(JSON.parse((e as MessageEvent).data)))
  es.addEventListener('task_updated', (e) => handlers.task_updated?.(JSON.parse((e as MessageEvent).data)))
  es.addEventListener('archive:changed', (e) => handlers['archive:changed']?.(JSON.parse((e as MessageEvent).data)))
  es.addEventListener('config:changed', (e) => handlers['config:changed']?.(JSON.parse((e as MessageEvent).data)))
  if (onError) es.onerror = onError
  return es
}
