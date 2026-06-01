// dashboard/js/composables/useTaskDetail.js
import { ref } from 'vue';
import { api } from '../utils/api.js';
import { useRealtime } from './useRealtime.js';

export function useTaskDetail() {
  const selectedTask = ref(null);
  const taskDetail = ref(null);
  const selectedTaskIsArchived = ref(false);
  const retrospectiveContent = ref(null);
  const { onTaskUpdate } = useRealtime();

  let unsubTaskUpdate = null;

  /**
   * Determine whether a task object represents an archived task.
   * Checks both the `archived` flag (set by useRealtime) and the `phase` field.
   */
  const isArchivedTask = (task) => task.archived === true || task.phase === 'archive' || task.phase === 'archived';

  /**
   * Fetch task detail using the appropriate API endpoint.
   * Archived tasks use /api/archived-tasks/:id, active tasks use /api/tasks/:id.
   */
  const fetchDetail = (id, archived) => {
    return archived ? api.getArchivedTask(id) : api.getTask(id);
  };

  const openDetail = async (task) => {
    try {
      const archived = isArchivedTask(task);
      taskDetail.value = await fetchDetail(task.id, archived);
      selectedTask.value = task.id;
      selectedTaskIsArchived.value = archived;

      // Fetch retrospective if available
      retrospectiveContent.value = null;
      try {
        const retro = await api.getRetrospective(task.id, archived);
        retrospectiveContent.value = retro.content || null;
      } catch (_) {
        // No retrospective available, that's fine
        retrospectiveContent.value = null;
      }

      // Clean up old listener
      if (unsubTaskUpdate) unsubTaskUpdate();

      // Listen for task updates, auto-refresh detail
      unsubTaskUpdate = onTaskUpdate((update) => {
        // update has a type field: 'task_created', 'task_updated', 'task_archived',
        // 'tasks:refresh', or 'reports:changed'
        const shouldRefresh =
          update.__reportsChanged ||
          update.type === 'task_updated' ||
          update.type === 'task_created' ||
          update.type === 'task_archived' ||
          (update.type === 'tasks:refresh' && Array.isArray(update.data) && update.data.some(t => t.id === selectedTask.value));
        if (shouldRefresh) {
          fetchDetail(selectedTask.value, selectedTaskIsArchived.value).then(d => { taskDetail.value = d; }).catch(() => {});
        }
      });
    } catch (e) {
      console.error('Failed to load task detail', e);
    }
  };

  const closeDetail = () => {
    selectedTask.value = null;
    taskDetail.value = null;
    selectedTaskIsArchived.value = false;
    retrospectiveContent.value = null;
    if (unsubTaskUpdate) { unsubTaskUpdate(); unsubTaskUpdate = null; }
  };

  // Edit operations
  const editing = ref(false);
  const editForm = ref({ title: '', description: '', phase: '', mode: '', control_mode: '' });
  const saving = ref(false);

  const startEdit = () => {
    if (!taskDetail.value) return;
    const d = taskDetail.value;
    editForm.value = {
      title: d.title || '', description: d.description || '',
      phase: d.phase || '', mode: d.mode || '', control_mode: d.control_mode || 'semi',
    };
    editing.value = true;
  };

  const cancelEdit = () => { editing.value = false; };

  const saveEdit = async () => {
    saving.value = true;
    try {
      const id = selectedTask.value;
      const f = editForm.value;
      if (f.phase && f.phase !== taskDetail.value?.phase) {
        await api.updateTaskPhase(id, f.phase);
      }
      await api.updateTask(id, {
        title: f.title, description: f.description,
        mode: f.mode, control_mode: f.control_mode,
      });
      taskDetail.value = await fetchDetail(id, selectedTaskIsArchived.value);
      editing.value = false;
    } catch (e) {
      console.error('Save failed', e);
    } finally {
      saving.value = false;
    }
  };

  const changePhase = async (phase) => {
    try {
      await api.updateTaskPhase(selectedTask.value, phase);
      taskDetail.value = await fetchDetail(selectedTask.value, selectedTaskIsArchived.value);
    } catch (e) { console.error('Phase change failed', e); }
  };

  return { selectedTask, taskDetail, retrospectiveContent, openDetail, closeDetail,
           editing, editForm, saving, startEdit, cancelEdit, saveEdit, changePhase };
}
