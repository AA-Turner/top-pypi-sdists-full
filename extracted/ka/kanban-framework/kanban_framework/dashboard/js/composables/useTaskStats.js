// dashboard/js/composables/useTaskStats.js
import { ref } from 'vue';
import { api } from '../utils/api.js';

export function useTaskStats() {
  const stats = ref(null);
  const loadingStats = ref(false);

  async function loadStats(taskId) {
    loadingStats.value = true;
    try {
      const res = await api.getTaskStats(taskId);
      if (res.success) stats.value = res.data;
    } catch (e) {
      stats.value = null;
    } finally {
      loadingStats.value = false;
    }
  }

  function formatTokens(n) {
    if (!n) return '0';
    if (n > 1000000) return (n / 1000000).toFixed(1) + 'M';
    if (n > 1000) return (n / 1000).toFixed(1) + 'K';
    return String(n);
  }

  function formatSeconds(s) {
    if (!s) return '0s';
    if (s < 60) return Math.round(s) + 's';
    if (s < 3600) return Math.floor(s / 60) + 'm ' + Math.round(s % 60) + 's';
    return Math.floor(s / 3600) + 'h ' + Math.floor((s % 3600) / 60) + 'm';
  }

  function maxTokens(statsData) {
    if (!statsData) return 1;
    return Math.max(1, ...Object.values(statsData.tokens?.phases || {}),
      ...Object.values(statsData.tokens?.agents || {}));
  }

  return { stats, loadingStats, loadStats, formatTokens, formatSeconds, maxTokens };
}
