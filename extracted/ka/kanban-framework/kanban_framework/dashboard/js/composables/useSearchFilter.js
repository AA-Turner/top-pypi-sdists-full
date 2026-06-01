// dashboard/js/composables/useSearchFilter.js
import { ref, computed, watch } from 'vue';

export function useSearchFilter(tasks) {
  const searchQuery = ref('');
  const selectedPhases = ref(['plan', 'execute', 'evaluate', 'archive']);
  const filterMenuOpen = ref(false);

  // Restore filter state from URL hash
  const restoreFilterFromURL = () => {
    const hash = window.location.hash;
    const queryIndex = hash.indexOf('?');
    if (queryIndex === -1) return;
    const params = new URLSearchParams(hash.slice(queryIndex + 1));
    if (params.has('search')) searchQuery.value = params.get('search');
    if (params.has('phase')) {
      const phases = params.get('phase').split(',').filter(Boolean);
      if (phases.length > 0) selectedPhases.value = phases;
    }
  };

  // Sync filter state to URL hash
  const syncFilterToURL = () => {
    const base = '#/board';
    const params = new URLSearchParams();
    if (searchQuery.value) params.set('search', searchQuery.value);
    const phases = selectedPhases.value.join(',');
    if (phases !== 'plan,execute,evaluate,archive') {
      params.set('phase', phases);
    }
    const qs = params.toString();
    const newHash = qs ? `${base}?${qs}` : base;
    if (window.location.hash !== newHash) {
      history.replaceState(null, '', newHash);
    }
  };

  watch([searchQuery, selectedPhases], () => {
    syncFilterToURL();
  }, { deep: true });

  const filteredTasks = computed(() => {
    let result = tasks.value;
    // Phase filter
    if (selectedPhases.value.length < 4) {
      result = result.filter(t => selectedPhases.value.includes(t.phase));
    }
    // Search filter
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.trim().toLowerCase();
      result = result.filter(t =>
        t.id.toLowerCase().includes(q) ||
        t.title.toLowerCase().includes(q)
      );
    }
    return result;
  });

  const togglePhase = (phase) => {
    const idx = selectedPhases.value.indexOf(phase);
    if (idx >= 0) {
      // Don't allow deselecting all
      if (selectedPhases.value.length > 1) {
        selectedPhases.value.splice(idx, 1);
      }
    } else {
      selectedPhases.value.push(phase);
    }
  };

  const toggleFilterMenu = () => {
    filterMenuOpen.value = !filterMenuOpen.value;
  };

  const closeFilterMenu = () => {
    filterMenuOpen.value = false;
  };

  return {
    searchQuery,
    selectedPhases,
    filterMenuOpen,
    filteredTasks,
    restoreFilterFromURL,
    togglePhase,
    toggleFilterMenu,
    closeFilterMenu
  };
}
