// dashboard/js/app.js
import { createApp, ref, computed, onMounted, watch } from 'vue';
import { api } from './utils/api.js';
import { KanbanBoard } from './components/KanbanBoard.js';
import { StatsOverview } from './components/StatsOverview.js';
import { SettingsPanel } from './components/SettingsPanel.js';
import { useRealtime } from './composables/useRealtime.js';

const app = createApp({
  setup() {
    const currentRoute = ref(window.location.hash.slice(1) || '/board');
    const stats = ref({ completed: 0, active: 0 });

    // Theme management
    const isDark = ref(false);

    const initTheme = () => {
      const stored = localStorage.getItem('dashboard-theme');
      if (stored) {
        isDark.value = stored === 'dark';
      } else {
        isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
      applyTheme();
    };

    const applyTheme = () => {
      document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light');
    };

    const toggleTheme = () => {
      isDark.value = !isDark.value;
      localStorage.setItem('dashboard-theme', isDark.value ? 'dark' : 'light');
      applyTheme();
    };

    // Sidebar state for mobile
    const sidebarOpen = ref(false);

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value;
    };

    const closeSidebar = () => {
      sidebarOpen.value = false;
    };

    const navItems = [
      { path: '/board', label: 'Board', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>' },
      { path: '/settings', label: 'Settings', icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>' },
    ];

    const { connectionStatus, connect, fetchInitialData, tasks } = useRealtime();

    // stats from useRealtime tasks
    watch(tasks, (newTasks) => {
      stats.value.completed = newTasks.filter(t => t.status === 'archived' || t.phase === 'archive').length;
      stats.value.active = newTasks.filter(t => t.status !== 'archived' && t.phase !== 'archive').length;
    }, { immediate: true });

    window.addEventListener('hashchange', () => {
      currentRoute.value = window.location.hash.slice(1) || '/board';
      closeSidebar();
    });

    const currentComponent = computed(() => {
      if (currentRoute.value === '/settings') return 'settings-panel';
      return 'kanban-board';
    });

    const breadcrumbPage = computed(() => {
      const item = navItems.find(n => n.path === currentRoute.value);
      return item ? item.label : 'Board';
    });

    onMounted(async () => {
      initTheme();
      try {
        await fetchInitialData();
        connect();
      } catch (e) { /* ignore */ }
    });

    return {
      currentRoute, currentComponent, navItems, stats, breadcrumbPage,
      isDark, toggleTheme,
      sidebarOpen, toggleSidebar, closeSidebar,
      connectionStatus
    };
  },
  template: `
    <div style="display:flex;">
      <aside class="sidebar" :class="{ 'sidebar-open': sidebarOpen }">
        <div class="sidebar-header">
          <h1><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg> Kanban Dashboard</h1>
          <small>important_demo</small>
        </div>
        <nav class="sidebar-nav">
          <a v-for="item in navItems" :key="item.path"
             :href="'#' + item.path"
             class="nav-item" :class="{ active: currentRoute === item.path }">
            <span class="nav-icon" v-html="item.icon"></span> {{ item.label }}
          </a>
        </nav>
        <div class="sidebar-footer">
          {{ stats.completed }} completed · {{ stats.active }} active
        </div>
      </aside>
      <div class="sidebar-overlay" :class="{ visible: sidebarOpen }" @click="closeSidebar"></div>
      <main class="main-content">
        <div class="top-bar">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <button class="hamburger-btn" @click="toggleSidebar" aria-label="Toggle sidebar">☰</button>
            <div class="breadcrumb">
              Dashboard <span class="sep">/</span>
              <span class="current">{{ breadcrumbPage }}</span>
            </div>
          </div>
          <div class="top-actions">
            <span class="connection-status" :class="connectionStatus">
              {{ connectionStatus === 'connected' ? 'Live' : connectionStatus === 'error' ? 'Reconnecting...' : 'Offline' }}
            </span>
            <button class="theme-toggle" @click="toggleTheme" :title="isDark ? 'Switch to light theme' : 'Switch to dark theme'" aria-label="Toggle theme">
              <svg v-if="isDark" viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>
              <svg v-else viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/></svg>
            </button>
          </div>
        </div>
        <div class="content-area">
          <component :is="currentComponent"></component>
        </div>
      </main>
    </div>
  `
});

app.component('kanban-board', KanbanBoard);
app.component('stats-overview', StatsOverview);
app.component('settings-panel', SettingsPanel);
app.mount('#app');
