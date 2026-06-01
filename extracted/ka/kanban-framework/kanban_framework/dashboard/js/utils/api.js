// dashboard/js/utils/api.js
const API_BASE = '/api';

async function fetchJSON(url, { allow404 = false } = {}) {
  const res = await fetch(API_BASE + url);
  if (!res.ok) {
    if (allow404 && res.status === 404) return null;
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

async function postJSON(url, body) {
  const res = await fetch(API_BASE + url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

async function putJSON(url, body) {
  const res = await fetch(API_BASE + url, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getConfig: () => fetchJSON('/config'),
  getWorkflow: () => fetchJSON('/workflow'),
  getTasks: () => fetchJSON('/tasks'),
  getTask: (id) => fetchJSON(`/tasks/${id}`),
  getArchivedTasks: () => fetchJSON('/archived-tasks'),
  getArchivedTask: (id) => fetchJSON(`/archived-tasks/${id}`),
  getRetrospective: (id, archived) => fetchJSON(`/${archived ? 'archived-tasks' : 'tasks'}/${id}/retrospective`, { allow404: true }),
  getTokenStats: () => fetchJSON('/token-stats'),
  getTaskSteps: (id) => fetchJSON(`/tasks/${id}/steps`),
  getTaskStats: (id) => fetchJSON(`/tasks/${id}/stats`),
  // Write APIs
  updateTaskPhase: (id, phase) => postJSON(`/tasks/${id}/phase`, { phase }),
  updateTask: (id, data) => putJSON(`/tasks/${id}`, data),
  updateSubtask: (taskId, stId, data) => putJSON(`/tasks/${taskId}/subtask/${stId}`, data),
  markStep: (taskId, stepId, status) => postJSON(`/tasks/${taskId}/step/${stepId}`, { status }),
  // Settings APIs
  saveConfig: (data) => putJSON('/config', data),
  saveWorkflow: (data) => putJSON('/workflow', data),
  getKnowledgeHealth: () => fetchJSON('/knowledge/health'),
  getStepDefinitions: () => fetchJSON('/step-definitions'),
};
