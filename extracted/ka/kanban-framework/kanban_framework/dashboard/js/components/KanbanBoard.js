// dashboard/js/components/KanbanBoard.js
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { api } from '../utils/api.js';
import { useSearchFilter } from '../composables/useSearchFilter.js';
import { useReportViewer } from '../composables/useReportViewer.js';
import { useTaskDetail } from '../composables/useTaskDetail.js';
import { useRealtime } from '../composables/useRealtime.js';
import { useScoreChart } from '../composables/useScoreChart.js';
import { useTokenChart } from '../composables/useTokenChart.js';
import { StatsOverview } from './StatsOverview.js';
import { useTaskStats } from '../composables/useTaskStats.js';

export const KanbanBoard = {
  components: {
    StatsOverview
  },
  setup() {
    const { tasks, connectionStatus, archivedTasks } = useRealtime();
    const loading = ref(true);

    // Step progress per task (#214)
    const taskSteps = ref({});

    async function loadTaskSteps(taskList) {
      for (const task of taskList) {
        if (task.phase === 'archived' || task.phase === 'cancelled') continue;
        try {
          const res = await api.getTaskSteps(task.id);
          if (res.success && res.data) {
            taskSteps.value[task.id] = res.data;
          }
        } catch (e) {
          // Silently skip
        }
      }
    }

    // Task stats composable
    const { stats: taskStats, loadStats, formatTokens, formatSeconds, maxTokens } = useTaskStats();

    // Token stats (#213)
    const tokenStats = ref({ total_tokens: 0, total_prompt_calls: 0 });

    async function loadTokenStats() {
      try {
        const res = await api.getTokenStats();
        if (res.success && res.data) {
          tokenStats.value = res.data;
        }
      } catch (e) {
        // Silently skip
      }
    }

    watch(tasks, async (newTasks) => {
      await loadTaskSteps(newTasks);
      await loadTokenStats();
    }, { deep: false });

    function stepProgress(taskId) {
      const s = taskSteps.value[taskId];
      if (!s || !s.total) return { pct: 0, done: 0, total: 0 };
      const done = Object.values(s.steps).filter(v => v.status === 'completed').length;
      return { pct: Math.round((done / s.total) * 100), done, total: s.total };
    }

    // SVG icons for column headers (Lucide-style)
    const colIcons = {
      knowledge: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>',
      brainstorm: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 1 1 7.072 0l-.548.547A3.374 3.374 0 0 0 14 18.469V19a2 2 0 1 1-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>',
      breakdown: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4Z"/></svg>',
      coding: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
      verify: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
      review: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
      done: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    };

    // Step-based columns (#214 improved)
    const columns = [
      { key: 'knowledge', label: 'Knowledge', icon: colIcons.knowledge, cssClass: 'column-plan' },
      { key: 'brainstorm', label: 'Brainstorm', icon: colIcons.brainstorm, cssClass: 'column-plan' },
      { key: 'breakdown', label: 'Plan', icon: colIcons.breakdown, cssClass: 'column-plan' },
      { key: 'coding', label: 'Code', icon: colIcons.coding, cssClass: 'column-execute' },
      { key: 'verify', label: 'Verify', icon: colIcons.verify, cssClass: 'column-evaluate' },
      { key: 'review', label: 'Review', icon: colIcons.review, cssClass: 'column-evaluate' },
      { key: 'done', label: 'Done', icon: colIcons.done, cssClass: 'column-archive' },
    ];

    // Map step IDs to columns
    const stepToColumn = (stepId) => {
      if (!stepId) return 'knowledge';
      if (stepId.startsWith('plan.knowledge')) return 'knowledge';
      if (stepId.startsWith('plan.plan_A')) return 'brainstorm';
      if (stepId.startsWith('plan.check_constraints') || stepId.startsWith('plan.plan_B') || stepId.startsWith('plan.user_confirm') || stepId.startsWith('plan.complete')) return 'breakdown';
      if (stepId.startsWith('execute.pitfall') || stepId.startsWith('execute.spawn')) return 'coding';
      if (stepId.startsWith('execute.verify') || stepId.startsWith('execute.commit') || stepId.startsWith('execute.complete')) return 'verify';
      if (stepId.startsWith('evaluate')) return 'review';
      return 'coding';
    };

    // ── Drag-and-Drop ──
    const dragTask = ref(null);

    function onDragStart(task) {
      if (task.archived || task.phase === 'archive') return;
      dragTask.value = task;
    }

    function onDragOver(e) { e.preventDefault(); }

    async function onDrop(colKey) {
      const task = dragTask.value;
      if (!task) return;
      dragTask.value = null;

      // Done column → mark all steps complete
      if (colKey === 'done') {
        try {
          const steps = taskSteps.value[task.id];
          if (steps && steps.steps) {
            for (const [sid, si] of Object.entries(steps.steps)) {
              if (si.status !== 'completed') {
                await api.markStep(task.id, sid, 'completed');
              }
            }
          }
          await api.updateTaskPhase(task.id, 'archive');
        } catch (e) { console.error('Drop failed', e); }
        await refreshBoard();
        return;
      }

      // Find the first pending step for this column
      const colFirstSteps = {
        'knowledge': ['plan.knowledge_search'],
        'brainstorm': ['plan.plan_A'],
        'breakdown': ['plan.check_constraints', 'plan.plan_B', 'plan.user_confirm_spec', 'plan.complete'],
        'coding': ['execute.pitfall_check', 'execute.spawn'],
        'verify': ['execute.verify', 'execute.commit', 'execute.complete'],
        'review': ['evaluate.e2e_run', 'evaluate.spawn', 'evaluate.spawn_qa', 'evaluate.collect_scores', 'evaluate.check_score', 'evaluate.complete'],
      };

      const stepIds = colFirstSteps[colKey] || [];
      try {
        // Complete all prior steps, mark first target step in_progress
        const steps = taskSteps.value[task.id];
        if (steps && steps.steps) {
          let foundTarget = false;
          for (const [sid, si] of Object.entries(steps.steps)) {
            if (stepIds.includes(sid) && !foundTarget) {
              await api.markStep(task.id, sid, 'in_progress');
              foundTarget = true;
            } else if (!foundTarget && si.status !== 'completed') {
              await api.markStep(task.id, sid, 'completed');
            }
          }
        }
        // Update phase to match column
        const ph = ['knowledge','brainstorm','breakdown'].includes(colKey) ? 'plan'
          : colKey === 'coding' ? 'execute'
          : colKey === 'verify' ? 'execute'
          : colKey === 'review' ? 'evaluate' : null;
        if (ph) await api.updateTaskPhase(task.id, ph);
      } catch (e) { console.error('Drop failed', e); }
      await refreshBoard();
    }

    async function refreshBoard() {
      loading.value = true;
      try {
        const res = await api.getTasks();
        tasks.value = res.data || res || [];
        await loadTaskSteps(tasks.value);
      } catch (e) { console.error('Refresh failed', e); }
      loading.value = false;
    }

    const getTasksForColumn = (colKey) => {
      return filteredTasks.value.filter(t => {
        // Archived → Done column
        if (colKey === 'done') return t.archived === true || t.phase === 'archive' || t.phase === 'archived';
        if (t.archived === true || t.phase === 'archive' || t.phase === 'archived') return false;

        // Find current step for this task
        const steps = taskSteps.value[t.id];
        if (!steps || !steps.steps) {
          // Fallback: use phase → column mapping
          const ph = t.phase || 'plan';
          if (ph === 'plan') return ['knowledge','brainstorm','breakdown'].includes(colKey);
          if (ph === 'plan_review' || ph === 'qa_spec' || ph === 'spec_review') return colKey === 'review';
          if (ph === 'execute') return colKey === 'coding';
          if (ph === 'evaluate' || ph === 'retrospective' || ph === 'user_decision') return colKey === 'review';
          return false;
        }

        // Find first non-completed step to determine current column
        const stepIds = Object.keys(steps.steps).sort();
        let currentStep = null;
        for (const sid of stepIds) {
          const s = steps.steps[sid];
          if (s.status !== 'completed' && s.status !== 'skipped') {
            currentStep = sid;
            break;
          }
        }
        // If all complete, show in verify or review based on phase
        if (!currentStep) {
          const ph = t.phase || 'plan';
          if (ph === 'plan') return colKey === 'breakdown';
          if (ph === 'execute') return colKey === 'verify';
          if (ph === 'evaluate') return colKey === 'review';
          return false;
        }

        return stepToColumn(currentStep) === colKey;
      });
    };

    // Composables (order matters: taskDetail must exist before report viewer)
    const {
      searchQuery, selectedPhases, filterMenuOpen, filteredTasks,
      restoreFilterFromURL, togglePhase, toggleFilterMenu, closeFilterMenu
    } = useSearchFilter(tasks);

    const {
      selectedTask, taskDetail, selectedTaskIsArchived, openDetail, closeDetail,
      editing, editForm, saving, startEdit, cancelEdit, saveEdit, changePhase,
    } = useTaskDetail();

    const {
      selectedIteration, expandedReports, iterationReports,
      currentIterationReports, toggleReport, isReportExpanded,
      scoreClass, getDimensions
    } = useReportViewer(taskDetail);

    // Token trend chart composable
    const { tokenCanvas, callsCanvas, render: renderTokenChart } = useTokenChart();

    watch(tokenStats, (ts) => {
      if (ts && ts.daily) {
        nextTick(() => renderTokenChart(ts.daily));
      }
    }, { deep: false });

    // Score trend chart composable
    const { chartCanvas, renderChart, destroyChart } = useScoreChart();

    // Whether the task has enough iteration data to show the chart
    const showScoreChart = computed(() => {
      if (!taskDetail.value) return false;
      // Prefer score_history (explicit per-iteration scores)
      if (taskDetail.value.score_history && taskDetail.value.score_history.length >= 1) {
        return true;
      }
      // Fall back to reports
      if (taskDetail.value.reports && taskDetail.value.reports.length > 0) {
        const iterations = new Set(taskDetail.value.reports.map(r => r.iteration || 1));
        return iterations.size >= 1;
      }
      return false;
    });

    // Watch taskDetail to render chart
    watch(taskDetail, async (detail) => {
      await nextTick();
      if (detail && detail.score_history && detail.score_history.length > 0) {
        renderChart(detail.score_history);
      } else if (detail && detail.reports && detail.reports.length > 0) {
        renderChart(detail.reports);
      } else {
        destroyChart();
      }
    });

    // Wrap openDetail to also reset iteration and tab
    const handleOpenDetail = async (task) => {
      await openDetail(task);
      selectedIteration.value = 0;
      detailTab.value = 'overview';
      loadStats(task.id);
    };

    // Render description as Markdown with DOMPurify sanitization
    const renderedDescription = computed(() => {
      if (!taskDetail.value || !taskDetail.value.description) return '';
      const rawHtml = window.marked.parse(taskDetail.value.description);
      return window.DOMPurify.sanitize(rawHtml);
    });

    const avgScore = (scores) => {
      if (!scores) return null;
      const values = Object.values(scores).map(s => typeof s === 'object' ? s.score : s).filter(v => typeof v === 'number' && !isNaN(v));
      if (values.length === 0) return null;
      return (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
    };

    // Extract numeric score value from a score entry (may be number or {score, ...} object)
    const getScoreValue = (info) => typeof info === 'object' ? info.score : info;

    const currentStepName = (task) => {
      const steps = taskSteps.value[task.id];
      if (!steps || !steps.steps) return null;
      const stepIds = Object.keys(steps.steps).sort();
      for (const sid of stepIds) {
        if (steps.steps[sid].status !== 'completed' && steps.steps[sid].status !== 'skipped') {
          const names = {
            'plan.knowledge_search': 'Knowledge',
            'plan.plan_A': 'Brainstorm',
            'plan.check_constraints': 'Constraints',
            'plan.plan_B': 'Task Plan',
            'execute.pitfall_check': 'Pitfall',
            'execute.spawn': 'Coding',
            'execute.verify': 'Verify',
            'execute.commit': 'Commit',
            'evaluate.e2e_run': 'E2E',
            'evaluate.spawn': 'Review',
            'evaluate.spawn_qa': 'QA',
            'evaluate.collect_scores': 'Scores',
          };
          return names[sid] || sid.split('.').pop();
        }
      }
      return null;
    };

    const formatPhase = (phase) => {
      const map = { plan: 'Planning', execute: 'In Progress', evaluate: 'Evaluating', archive: 'Done' };
      return map[phase] || phase;
    };

    // History timeline SVG icons
    const iconPlan = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
    const iconExec = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>';
    const iconEval = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>';
    const iconDone = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    const iconDoc  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>';
    const iconTest = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>';
    const iconRev  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4Z"/></svg>';
    const iconRetro= '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>';

    const phaseIcons = {
      plan: iconPlan, planning: iconPlan, pending: iconPlan,
      plan_review: iconRev, qa_spec: iconTest, spec_review: iconRev,
      execute: iconExec,
      evaluate: iconEval, evaluating: iconEval,
      user_decision: iconDoc,
      self_improve: iconRetro,
      retrospective: iconRetro,
      archive: iconDone, archived: iconDone,
    };

    const fallbackIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="12" r="10" stroke-dasharray="4 4"/></svg>';
    const getPhaseIcon = (phase) => phaseIcons[phase] || fallbackIcon;

    const formatHistoryPhase = (phase) => {
      const map = {
        plan: 'Plan',
        planning: 'Planning',
        pending: 'Pending',
        plan_review: 'Plan Review',
        qa_spec: 'QA Spec',
        spec_review: 'Spec Review',
        execute: 'Execute',
        evaluate: 'Evaluate',
        evaluating: 'Evaluating',
        user_decision: 'User Decision',
        self_improve: 'Self Improve',
        retrospective: 'Retrospective',
        archive: 'Archive',
        archived: 'Archived',
      };
      return map[phase] || phase;
    };

    const formatHistoryStatus = (h) => {
      if (h.status === 'completed') return 'Completed';
      if (h.status === 'entered') return 'In Progress';
      if (h.type === 'full') return 'Full Iteration';
      if (h.type === 'hot') return 'Hot Iteration';
      return h.status || h.type || '';
    };

    const formatTimestamp = (ts) => {
      if (!ts) return '';
      try {
        const d = new Date(ts);
        const month = d.toLocaleString('en-US', { month: 'short' });
        const day = d.getDate();
        const year = d.getFullYear();
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        return `${month} ${day}, ${year}, ${hours}:${minutes}`;
      } catch {
        return ts;
      }
    };

    const getHistoryTimestamp = (h) => {
      return h.exited_at || h.entered_at || '';
    };

    const phaseColorClass = (phase) => {
      const map = {
        plan: 'timeline-phase-plan',
        planning: 'timeline-phase-plan',
        pending: 'timeline-phase-plan',
        plan_review: 'timeline-phase-plan',
        qa_spec: 'timeline-phase-plan',
        spec_review: 'timeline-phase-plan',
        execute: 'timeline-phase-execute',
        evaluate: 'timeline-phase-evaluate',
        evaluating: 'timeline-phase-evaluate',
        user_decision: 'timeline-phase-evaluate',
        self_improve: 'timeline-phase-self-improve',
        retrospective: 'timeline-phase-self-improve',
        archive: 'timeline-phase-archive',
        archived: 'timeline-phase-archive',
      };
      return map[phase] || '';
    };

    onMounted(async () => {
      restoreFilterFromURL();
      // fetchInitialData + connect already called by app.js on startup
      // Just wait for tasks to be populated
      loading.value = false;
    });

    // Detail panel tab state
    const detailTab = ref('overview');
    const detailTabs = [
      { key: 'overview', label: 'Overview', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>' },
      { key: 'progress', label: 'Progress', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>' },
      { key: 'reports', label: 'Reports', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>' },
    ];

    return {
      tasks, archivedTasks, loading, columns, selectedTask, taskDetail,
      getTasksForColumn, avgScore, getScoreValue, openDetail: handleOpenDetail, closeDetail, formatPhase, currentStepName,
      renderedDescription,
      searchQuery, selectedPhases, filteredTasks,
      togglePhase, filterMenuOpen, toggleFilterMenu, closeFilterMenu,
      selectedIteration, iterationReports, currentIterationReports,
      scoreClass, getDimensions, expandedReports, toggleReport, isReportExpanded,
      connectionStatus,
      // Score trend chart
      chartCanvas, showScoreChart,
      // Token trend chart
      tokenCanvas, callsCanvas,
      // History timeline helpers
      getPhaseIcon, formatHistoryPhase, formatHistoryStatus,
      formatTimestamp, getHistoryTimestamp, phaseColorClass,
      // Step progress + token stats (#213 #214)
      tokenStats, stepProgress, taskSteps,
      // Task stats
      taskStats, formatTokens, formatSeconds, maxTokens,
      // Drag-and-drop
      dragTask, onDragStart, onDragOver, onDrop,
      // Task editing
      selectedTaskIsArchived,
      editing, editForm, saving, startEdit, cancelEdit, saveEdit, changePhase,
      // Detail tabs
      detailTab, detailTabs,
    };
  },
  template: `
    <div v-if="loading" class="loading">Loading tasks...</div>
    <div v-else>
      <!-- Search and Filter Toolbar -->
      <div class="board-toolbar">
        <input class="search-input" type="text" v-model="searchQuery" placeholder="Search by ID or title..." />
        <div class="filter-dropdown">
          <button class="filter-btn" @click="toggleFilterMenu">
            Filter: {{ selectedPhases.length }}/4 phases
          </button>
          <div v-if="filterMenuOpen" class="filter-menu">
            <label v-for="col in columns" :key="col.key">
              <input type="checkbox" :checked="selectedPhases.includes(col.key)" @change="togglePhase(col.key)" />
              {{ col.label }}
            </label>
          </div>
        </div>
        <span class="connection-status" :class="connectionStatus">
          {{ connectionStatus === 'connected' ? 'Live' : connectionStatus === 'error' ? 'Reconnecting...' : 'Offline' }}
        </span>
      </div>

      <!-- Statistics Overview Cards -->
      <stats-overview :tasks="tasks" :token-stats="tokenStats"></stats-overview>

      <!-- Token Trend Charts -->
      <div v-if="tokenStats && tokenStats.daily && tokenStats.daily.length > 0" class="chart-row">
        <div class="chart-container">
          <div class="chart-title"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg> API Calls</div>
          <canvas ref="callsCanvas" width="500" height="160"></canvas>
        </div>
        <div class="chart-container">
          <div class="chart-title"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg> Tokens</div>
          <canvas ref="tokenCanvas" width="500" height="160"></canvas>
        </div>
      </div>

      <div class="kanban-columns" @click="closeFilterMenu">
        <div v-for="col in columns" :key="col.key"
             class="kanban-column" :class="col.cssClass"
             @dragover="onDragOver" @drop="onDrop(col.key)">
          <div class="column-header">
            <span class="column-header-label"><span class="column-header-icon" v-html="col.icon"></span> {{ col.label }}</span>
            <span class="column-count">{{ getTasksForColumn(col.key).length }}</span>
          </div>
          <div v-for="task in getTasksForColumn(col.key)" :key="task.id"
               class="task-card" @click="openDetail(task)"
               draggable="true" @dragstart="onDragStart(task)"
               :class="{ 'task-dragging': dragTask && dragTask.id === task.id }">
            <div class="task-id">{{ task.id }}</div>
            <div class="task-title">{{ task.title }}</div>
            <div class="task-meta">
              <span class="task-badge" :class="'badge-' + task.phase">
                {{ currentStepName(task) || formatPhase(task.phase) }}
                <template v-if="task.phase === 'archive' && avgScore(task.scores)">
                  · {{ avgScore(task.scores) }}
                </template>
              </span>
              <div class="task-avatar"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg></div>
            </div>
            <!-- Step progress bar (#214) -->
            <div v-if="stepProgress(task.id).total > 0" class="step-progress" @click.stop>
              <div class="step-progress-bar">
                <div class="step-progress-fill" :style="{ width: stepProgress(task.id).pct + '%' }"></div>
              </div>
              <div class="step-progress-label">{{ stepProgress(task.id).done }}/{{ stepProgress(task.id).total }}</div>
            </div>
          </div>
          <div v-if="getTasksForColumn(col.key).length === 0" class="empty-state">
            <div class="empty-state-icon" v-html="col.icon"></div>
            <span>No tasks</span>
          </div>
        </div>

        <!-- Task Detail Panel -->
        <div v-if="taskDetail" class="task-detail-overlay" @keydown.escape="closeDetail">
          <!-- Sticky Header -->
          <div class="detail-sticky-header">
            <div class="detail-header-top">
              <div class="detail-header-info">
                <span class="detail-task-id">{{ taskDetail.id }}</span>
                <h2 class="detail-title">{{ taskDetail.title }}</h2>
                <div class="detail-meta-row">
                  <span class="detail-phase-badge" :class="'badge-' + (taskDetail.phase || 'plan')">
                    <span class="detail-phase-dot" :class="'dot-' + (taskDetail.phase || 'plan')"></span>
                    {{ formatPhase(taskDetail.phase) }}
                  </span>
                  <span v-if="taskDetail.iteration > 1" class="detail-iter-badge">Iter {{ taskDetail.iteration }}</span>
                  <span v-if="avgScore(taskDetail.scores)" class="detail-score-badge" :class="scoreClass(parseFloat(avgScore(taskDetail.scores)))">{{ avgScore(taskDetail.scores) }}</span>
                </div>
              </div>
              <button class="close-btn" @click="closeDetail" aria-label="Close detail panel">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>
            <!-- Tab Navigation -->
            <div class="detail-tabs">
              <button v-for="tab in detailTabs" :key="tab.key"
                      class="detail-tab" :class="{ active: detailTab === tab.key }"
                      @click="detailTab = tab.key">
                <span class="detail-tab-icon" v-html="tab.icon"></span>
                {{ tab.label }}
              </button>
            </div>
          </div>

          <!-- Tab: Overview -->
          <div v-show="detailTab === 'overview'" class="detail-tab-content">
            <!-- Description -->
            <div v-if="taskDetail.description" class="detail-card">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                Description
              </div>
              <div class="markdown-body" style="font-size:0.82rem;" v-html="renderedDescription"></div>
            </div>

            <!-- Scores -->
            <div class="detail-card" v-if="taskDetail.scores && Object.keys(taskDetail.scores).length">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                Scores
                <span v-if="avgScore(taskDetail.scores)" class="detail-card-badge detail-card-badge-score" :class="scoreClass(parseFloat(avgScore(taskDetail.scores)))">avg {{ avgScore(taskDetail.scores) }}</span>
              </div>
              <div class="score-grid-v2">
                <div v-for="(info, role) in taskDetail.scores" :key="role" class="score-card-v2" :class="scoreClass(getScoreValue(info))">
                  <span class="score-card-v2-label">{{ role }}</span>
                  <span class="score-card-v2-value">{{ getScoreValue(info) }}</span>
                  <div class="score-card-v2-bar">
                    <div class="score-card-v2-fill" :style="{ width: (getScoreValue(info) * 10) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Resource Usage -->
            <div v-if="taskStats && taskStats.tokens.total_tokens > 0" class="detail-card">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
                Resource Usage
                <span class="detail-card-badge">{{ formatTokens(taskStats.tokens.total_tokens) }} tokens</span>
                <span class="detail-card-badge">{{ formatSeconds(Object.values(taskStats.tokens.phase_duration || {}).reduce((a,b)=>a+b,0)) }}</span>
                <span class="detail-card-badge">{{ taskStats.tokens.real_api_calls || taskStats.tokens.total_prompts || 0 }} calls</span>
              </div>
              <div class="phase-table">
                <div class="phase-table-header">
                  <span>Phase</span><span>Tokens</span><span>Duration</span><span>Calls</span>
                </div>
                <div v-for="ph in [...new Set([...Object.keys(taskStats.tokens.phases || {}), ...Object.keys(taskStats.tokens.phase_api_calls || {})])].sort()" :key="'row-'+ph" class="phase-table-row">
                  <span class="phase-table-name">{{ ph }}</span>
                  <span class="phase-table-num">{{ formatTokens((taskStats.tokens.phases || {})[ph] || 0) }}</span>
                  <span class="phase-table-num">{{ formatSeconds((taskStats.tokens.phase_duration || {})[ph] || 0) }}</span>
                  <span class="phase-table-num">{{ (taskStats.tokens.phase_api_calls || {})[ph] || 0 }}</span>
                </div>
              </div>
              <div v-if="taskStats.tokens._note" class="detail-hint">{{ taskStats.tokens._note }}</div>
            </div>
          </div>

          <!-- Tab: Progress -->
          <div v-show="detailTab === 'progress'" class="detail-tab-content">
            <!-- Steps -->
            <div v-if="taskSteps[selectedTask.id] && taskSteps[selectedTask.id].steps" class="detail-card">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
                Steps
                <span class="detail-card-badge">{{ Object.values(taskSteps[selectedTask.id].steps).filter(v=>v.status==='completed').length }}/{{ Object.keys(taskSteps[selectedTask.id].steps).length }}</span>
              </div>
              <div class="steps-list">
                <div v-for="(si, sid) in taskSteps[selectedTask.id].steps" :key="sid" class="step-item" :class="{ 'step-done': si.status === 'completed', 'step-active': si.status === 'in_progress' }">
                  <span class="step-status-icon">
                    <svg v-if="si.status === 'completed'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                    <svg v-else-if="si.status === 'in_progress'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                    <span v-else class="step-dot"></span>
                  </span>
                  <span class="step-name">{{ sid.split('.').pop() }}</span>
                  <span v-if="si.agent_type" class="step-agent">{{ si.agent_type.replace('kanban-','') }}</span>
                  <span v-if="taskStats && taskStats.stepTokens && taskStats.stepTokens[sid]" class="step-tokens">{{ formatTokens(taskStats.stepTokens[sid]) }}</span>
                </div>
              </div>
            </div>

            <!-- History Timeline -->
            <div class="detail-card">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                History
              </div>
              <div v-if="taskDetail.history && taskDetail.history.length" class="history-timeline">
                <div v-for="(h, i) in taskDetail.history" :key="i"
                     class="timeline-entry"
                     :class="[phaseColorClass(h.phase), { 'timeline-entry-latest': i === taskDetail.history.length - 1 }]">
                  <div class="timeline-dot-wrapper">
                    <span class="timeline-dot"></span>
                    <span v-if="i < taskDetail.history.length - 1" class="timeline-line"></span>
                  </div>
                  <div class="timeline-content">
                    <div class="timeline-header">
                      <span class="timeline-icon" v-html="getPhaseIcon(h.phase)"></span>
                      <span class="timeline-phase-name">{{ formatHistoryPhase(h.phase) }}</span>
                      <span v-if="h.iteration" class="timeline-iteration">Iter {{ h.iteration }}</span>
                      <span class="timeline-status" :class="'status-' + (h.status || 'default')">{{ formatHistoryStatus(h) }}</span>
                    </div>
                    <div v-if="getHistoryTimestamp(h)" class="timeline-timestamp">
                      {{ formatTimestamp(getHistoryTimestamp(h)) }}
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="timeline-empty">No history recorded</div>
            </div>
          </div>

          <!-- Tab: Reports -->
          <div v-show="detailTab === 'reports'" class="detail-tab-content">
            <!-- Score Trend Chart -->
            <div class="detail-card" v-if="showScoreChart">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                Score Trend
              </div>
              <div class="score-chart-container">
                <canvas ref="chartCanvas"></canvas>
              </div>
            </div>

            <!-- Evaluation Reports -->
            <div class="detail-card" v-if="currentIterationReports.length">
              <div class="detail-card-header">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                Evaluation Reports
              </div>
              <div class="iteration-tabs" v-if="iterationReports.length > 1">
                <button v-for="(iterGroup, idx) in iterationReports" :key="idx"
                        class="iteration-tab" :class="{ active: selectedIteration === idx }"
                        @click="selectedIteration = idx">
                  Iter {{ iterGroup.iteration }}
                </button>
              </div>

              <div v-for="r in currentIterationReports" :key="r.role" class="eval-report-card">
                <div class="eval-report-header" @click="toggleReport(r.role)">
                  <div class="eval-report-header-left">
                    <span class="eval-expand-icon" :class="{ collapsed: !isReportExpanded(r.role) }">&#9662;</span>
                    <span class="eval-role-name">{{ r.role }}</span>
                    <span class="eval-score-badge" :class="scoreClass(r.score)">{{ r.score }}</span>
                  </div>
                  <span class="eval-pass-fail" :class="r.passed ? 'eval-pass' : 'eval-fail'">
                    {{ r.passed ? 'PASS' : 'FAIL' }}
                  </span>
                </div>

                <div v-if="isReportExpanded(r.role)" class="eval-report-body">
                  <div class="eval-dimensions">
                    <div v-for="dim in getDimensions(r.report)" :key="dim.name" class="eval-dimension-row">
                      <span class="eval-dim-name" :title="dim.name">{{ dim.name }}</span>
                      <div class="eval-dim-bar-bg">
                        <div class="eval-dim-bar" :class="scoreClass(dim.score)" :style="{ width: (dim.score * 10) + '%' }"></div>
                      </div>
                      <span class="eval-dim-value">{{ dim.score }}</span>
                    </div>
                  </div>

                  <div v-for="dim in getDimensions(r.report)" :key="'fi-' + dim.name" class="eval-findings-issues">
                    <template v-if="dim.findings.length">
                      <div class="eval-list-title">Findings ({{ dim.name }})</div>
                      <div v-for="(f, fi) in dim.findings" :key="'f' + fi" class="eval-list-item">
                        <span class="eval-list-icon finding">\u{2713}</span>
                        <span>{{ typeof f === 'string' ? f : f.message || f.text || JSON.stringify(f) }}</span>
                      </div>
                    </template>
                    <template v-if="dim.issues.length">
                      <div class="eval-list-title">Issues ({{ dim.name }})</div>
                      <div v-for="(issue, ii) in dim.issues" :key="'i' + ii" class="eval-list-item">
                        <span class="eval-list-icon issue">\u{26A0}</span>
                        <span>{{ typeof issue === 'string' ? issue : issue.message || issue.text || JSON.stringify(issue) }}</span>
                      </div>
                    </template>
                  </div>

                  <div v-if="getDimensions(r.report).length === 0" class="eval-findings-issues">
                    <template v-if="r.report && r.report.findings && r.report.findings.length">
                      <div class="eval-list-title">Findings</div>
                      <div v-for="(f, fi) in r.report.findings" :key="'rf' + fi" class="eval-list-item">
                        <span class="eval-list-icon finding">\u{2713}</span>
                        <span>{{ typeof f === 'string' ? f : f.message || f.text || JSON.stringify(f) }}</span>
                      </div>
                    </template>
                    <template v-if="r.report && r.report.issues && r.report.issues.length">
                      <div class="eval-list-title">Issues</div>
                      <div v-for="(issue, ii) in r.report.issues" :key="'ri' + ii" class="eval-list-item">
                        <span class="eval-list-icon issue">\u{26A0}</span>
                        <span>{{ typeof issue === 'string' ? issue : issue.message || issue.text || JSON.stringify(issue) }}</span>
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
};
