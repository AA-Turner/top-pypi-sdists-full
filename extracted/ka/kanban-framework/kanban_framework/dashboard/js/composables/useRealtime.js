// dashboard/js/composables/useRealtime.js
// EventSource singleton composable for SSE real-time updates.
//
// Server-side events (see server.js /api/events):
//   connected       -> { time }            connection established
//   task_created    -> { id, task }         a new task was created
//   task_updated    -> { id, task }         a task was modified
//   task_archived   -> { id, task }         a task was removed/archived
//   task_removed    -> { id, task }         a task was deleted
//   tasks:refresh   -> [task, ...]          full task array after any change
//   archive:changed -> { filename }         archive directory changed
//   reports:changed -> { filename }         a report file changed
//   config:changed  -> <parsed JSON>       config.json or workflow.json changed
//
// The composable exposes:
//   - tasks            (readonly ref)  unified task array (active + archived)
//   - archivedTasks    (readonly ref)  archived-only subset for convenience
//   - connectionStatus (readonly ref)  'disconnected' | 'connecting' | 'connected' | 'error'
//   - connect(), disconnect(), fetchInitialData()
//   - onTaskUpdate(cb) -> unsubscribe fn   fires on task_created, task_updated, task_archived, tasks:refresh OR reports:changed
//   - onConfigChanged(cb) -> unsubscribe fn  fires on config:changed

import { ref, readonly, computed } from 'vue';
import { api } from '../utils/api.js';

// ---------------------------------------------------------------------------
// Module-level singleton state (shared across all components)
// ---------------------------------------------------------------------------

const tasks = ref([]);
const connectionStatus = ref('disconnected');

let eventSource = null;
let taskUpdateListeners = [];
let configListeners = [];
let archiveListeners = [];

// ---------------------------------------------------------------------------
// useRealtime composable
// ---------------------------------------------------------------------------

export function useRealtime() {

  // Computed: archived tasks derived from the unified tasks array
  const archivedTasks = computed(() => tasks.value.filter(t => t.archived === true));

  // ---- Connection management ------------------------------------------------

  /**
   * Open an EventSource connection to /api/events.
   * If a connection already exists this is a no-op.
   */
  const connect = () => {
    if (eventSource) return; // singleton -- already connected or connecting

    connectionStatus.value = 'connecting';
    eventSource = new EventSource('/api/events');

    // -- connected --
    eventSource.addEventListener('connected', () => {
      connectionStatus.value = 'connected';
    });

    // -- tasks:refresh (server sends active task array after file change) --
    eventSource.addEventListener('tasks:refresh', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (Array.isArray(data)) {
          // Merge: keep archived tasks, replace active with fresh data
          const archived = tasks.value.filter(t => t.archived === true);
          const active = data.map(t => ({ ...t, archived: false }));
          tasks.value = [...active, ...archived];
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'tasks:refresh', data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse tasks:refresh data', err);
      }
    });

    // -- tasks:refresh-archived (server sends archived task array) --
    eventSource.addEventListener('tasks:refresh-archived', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (Array.isArray(data)) {
          const active = tasks.value.filter(t => t.archived !== true);
          const archived = data.map(t => ({ ...t, archived: true }));
          tasks.value = [...active, ...archived];
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'tasks:refresh-archived', data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse tasks:refresh-archived data', err);
      }
    });

    // -- task_created (granular: a new task appeared) --
    eventSource.addEventListener('task_created', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data && data.task) {
          const newTask = { ...data.task, archived: !!data.task.archived };
          // Add to tasks if not already present
          if (!tasks.value.some(t => t.id === newTask.id)) {
            tasks.value = [...tasks.value, newTask];
          }
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'task_created', ...data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse task_created data', err);
      }
    });

    // -- task_updated (granular: a task was modified) --
    eventSource.addEventListener('task_updated', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data && data.task) {
          const updatedTask = { ...data.task, archived: !!data.task.archived };
          // Replace the existing task in the array
          tasks.value = tasks.value.map(t => t.id === updatedTask.id ? updatedTask : t);
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'task_updated', ...data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse task_updated data', err);
      }
    });

    // -- task_archived (granular: a task was removed/archived) --
    eventSource.addEventListener('task_archived', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data && data.task) {
          const archivedTask = { ...data.task, archived: true };
          // Update the task in-place to mark as archived
          tasks.value = tasks.value.map(t => t.id === archivedTask.id ? archivedTask : t);
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'task_archived', ...data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse task_archived data', err);
      }
    });

    // -- task_removed (granular: a task was deleted from filesystem) --
    eventSource.addEventListener('task_removed', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data && data.id) {
          // Remove the task from the array entirely
          tasks.value = tasks.value.filter(t => t.id !== data.id);
        }
        taskUpdateListeners.forEach(fn => fn({ type: 'task_removed', ...data }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse task_removed data', err);
      }
    });

    // -- reports:changed --
    eventSource.addEventListener('reports:changed', (e) => {
      try {
        const data = JSON.parse(e.data);
        // Notify task-update listeners so detail panels can refresh
        taskUpdateListeners.forEach(fn => fn({ type: 'reports:changed', __reportsChanged: true, filename: data.filename }));
      } catch (err) {
        console.error('[useRealtime] Failed to parse reports:changed data', err);
      }
    });

    // -- archive:changed (archive directory contents changed) --
    eventSource.addEventListener('archive:changed', () => {
      // Re-fetch archived tasks from the API to stay in sync
      api.getArchivedTasks()
        .then(list => {
          // Mark all fetched tasks as archived
          const archived = (Array.isArray(list) ? list : []).map(t => ({ ...t, archived: true }));
          // Merge: keep active tasks from current state, replace archived tasks with fresh list
          const active = tasks.value.filter(t => !t.archived);
          tasks.value = [...active, ...archived];
        })
        .catch(() => {});
      archiveListeners.forEach(fn => fn({ type: 'archive:changed' }));
    });

    // -- config:changed (carries full config or workflow JSON) --
    eventSource.addEventListener('config:changed', (e) => {
      try {
        const data = JSON.parse(e.data);
        configListeners.forEach(fn => fn(data));
      } catch (err) {
        console.error('[useRealtime] Failed to parse config:changed data', err);
      }
    });

    // -- error handling --
    eventSource.onerror = () => {
      // EventSource.readyState:
      //   0 = CONNECTING (will auto-retry)
      //   2 = CLOSED
      if (eventSource && eventSource.readyState === EventSource.CLOSED) {
        connectionStatus.value = 'error';
        // Clear the reference so a new connect() can retry later.
        eventSource = null;
      } else {
        // Still in reconnecting state -- mark as error but keep reference
        // so the browser's native retry continues.
        connectionStatus.value = 'error';
      }
    };

    eventSource.onopen = () => {
      connectionStatus.value = 'connected';
    };
  };

  /**
   * Close the EventSource connection and reset status.
   */
  const disconnect = () => {
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
    connectionStatus.value = 'disconnected';
  };

  // ---- Initial data loading -------------------------------------------------

  /**
   * Fetch active tasks and archived tasks via REST API, merge into a unified
   * tasks array. Active tasks from /api/tasks, archived tasks from
   * /api/archived-tasks. Archived tasks are marked with archived: true.
   * Should be called once on app startup, followed by connect() to receive
   * incremental SSE updates.
   */
  const fetchInitialData = async () => {
    const [tasksRes, archivedRes] = await Promise.allSettled([
      api.getTasks(),
      api.getArchivedTasks()
    ]);

    const activeTasks = tasksRes.status === 'fulfilled' && Array.isArray(tasksRes.value)
      ? tasksRes.value.map(t => ({ ...t, archived: false }))
      : [];

    const archivedTasksList = archivedRes.status === 'fulfilled' && Array.isArray(archivedRes.value)
      ? archivedRes.value.map(t => ({ ...t, archived: true }))
      : [];

    // Merge into a unified tasks array
    tasks.value = [...activeTasks, ...archivedTasksList];
  };

  // ---- Listener registration ------------------------------------------------

  /**
   * Register a callback fired on task change events.
   * Returns an unsubscribe function.
   *
   * Callback receives an object with:
   *   - type: 'task_created' | 'task_updated' | 'task_archived' | 'task_removed' | 'tasks:refresh' | 'reports:changed'
   *   - Additional fields vary by type:
   *     task_created/updated/archived: { id, task }
   *     tasks:refresh: { data: task[] }
   *     reports:changed: { __reportsChanged: true, filename }
   */
  const onTaskUpdate = (callback) => {
    taskUpdateListeners.push(callback);
    return () => {
      taskUpdateListeners = taskUpdateListeners.filter(fn => fn !== callback);
    };
  };

  /**
   * Register a callback fired on config:changed events.
   * Returns an unsubscribe function.
   *
   * Callback receives the parsed config/workflow JSON object.
   */
  const onConfigChanged = (callback) => {
    configListeners.push(callback);
    return () => {
      configListeners = configListeners.filter(fn => fn !== callback);
    };
  };

  /**
   * Register a callback fired on archive:changed events.
   * Returns an unsubscribe function.
   *
   * Callback receives the event payload { type: 'archive:changed' }.
   */
  const onArchiveChanged = (callback) => {
    archiveListeners.push(callback);
    return () => {
      archiveListeners = archiveListeners.filter(fn => fn !== callback);
    };
  };

  // ---- Public API -----------------------------------------------------------

  return {
    tasks: readonly(tasks),
    archivedTasks: readonly(archivedTasks),
    connectionStatus: readonly(connectionStatus),
    connect,
    disconnect,
    fetchInitialData,
    onTaskUpdate,
    onConfigChanged,
    onArchiveChanged
  };
}
