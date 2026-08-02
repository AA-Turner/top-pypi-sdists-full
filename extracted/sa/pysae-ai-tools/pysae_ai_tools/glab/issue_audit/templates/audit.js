const { createApp, ref, shallowRef, triggerRef, computed, watch, nextTick } = Vue;
const { createVuetify } = Vuetify;

const app = createApp({
  setup() {
    // --- Config (from Python rules registry) ---
    const ALL_CHECKS = ref([]);
    const CHECK_LABELS = ref({});
    const CHECK_COLORS = ref({});
    const FIX_LABELS = ref({});
    const configLoaded = ref(false);

    fetch('/api/config').then(r => r.json()).then(cfg => {
      ALL_CHECKS.value = cfg.all_checks;
      CHECK_LABELS.value = cfg.check_labels;
      CHECK_COLORS.value = cfg.check_colors;
      FIX_LABELS.value = cfg.fix_labels;
      selectedChecks.value = [...cfg.all_checks];
      configLoaded.value = true;
    });

    // --- Data model ---
    // Metadata (context, scopes, label_colors, perf, plan_perf)
    const meta = ref(null);
    // Issues stored in a Map for O(1) upsert, wrapped in shallowRef for reactivity
    const issueMap = shallowRef(new Map());
    const _emptyData = {
      total_issues: 0, issues_with_errors: 0, total_violations: 0,
      fixable: 0, issues_with_fixable: 0, by_check: {},
      active_scopes: {}, context: {}, label_colors: {},
      known_projects: [], plan: { issues: [] },
      perf: null, plan_perf: null, issues: [],
    };
    // Always returns an object (never null) — avoids CLS from v-if transitions
    const data = computed(() => {
      if (!meta.value) return _emptyData;
      return { ...meta.value, issues: [...issueMap.value.values()] };
    });
    const dataReady = computed(() => meta.value !== null);

    function issueKey(issue) {
      return `${issue.project_id}:${issue.iid}`;
    }

    // --- Filters ---
    const selectedChecks = ref([]);
    const selectedProjects = ref([]);

    const activeChecks = computed(() =>
      ALL_CHECKS.value.filter(c => meta.value?.active_scopes?.[c] !== false)
    );

    const activeProjects = computed(() => {
      // Use known_projects from metadata if available (populated at preload)
      if (meta.value?.known_projects?.length > 0) {
        return [...meta.value.known_projects].sort();
      }
      // Fallback: derive from issues
      const projects = new Set();
      for (const issue of issueMap.value.values()) {
        projects.add(issue.project_path);
      }
      return [...projects].sort();
    });

    function labelStyle(label) {
      const colors = meta.value?.label_colors || {};
      const bg = colors[label];
      if (!bg) return {};
      const hex = bg.replace('#', '');
      const r = parseInt(hex.substr(0, 2), 16);
      const g = parseInt(hex.substr(2, 2), 16);
      const b = parseInt(hex.substr(4, 2), 16);
      const brightness = (r * 299 + g * 587 + b * 114) / 1000;
      return { backgroundColor: bg, color: brightness > 128 ? '#333' : '#fff' };
    }

    const scopedIssues = computed(() => {
      const issues = [...issueMap.value.values()];
      if (selectedProjects.value.length === 0) return issues;
      return issues.filter(i => selectedProjects.value.includes(i.project_path));
    });

    const filteredIssues = computed(() => {
      return scopedIssues.value.filter(issue => {
        if (issue.violations.length === 0) return true;
        if (selectedChecks.value.length > 0) {
          if (!issue.violations.some(v => selectedChecks.value.includes(v.check))) return false;
        }
        return true;
      });
    });

    const isFiltered = computed(() =>
      (selectedProjects.value.length > 0 && selectedProjects.value.length < activeProjects.value.length) ||
      (selectedChecks.value.length > 0 && selectedChecks.value.length < activeChecks.value.length)
    );

    const filteredStats = computed(() => {
      const scoped = scopedIssues.value;
      const displayed = filteredIssues.value;
      const total = scoped.length;
      const withErrors = displayed.filter(i => i.violations.some(v => v.severity === 'error')).length;
      const withWarnings = displayed.filter(i => i.violations.length > 0 && !i.violations.some(v => v.severity === 'error')).length;
      const withFixable = displayed.filter(i => i.violations.some(v => v.fixable)).length;
      const violations = displayed.reduce((sum, i) => sum + i.violations.length, 0);
      const violationErrors = displayed.reduce((sum, i) => sum + i.violations.filter(v => v.severity === 'error').length, 0);
      const violationWarnings = displayed.reduce((sum, i) => sum + i.violations.filter(v => v.severity === 'warning').length, 0);
      const fixable = displayed.reduce((sum, i) => sum + i.violations.filter(v => v.fixable).length, 0);
      const byCheck = {};
      for (const issue of displayed) {
        for (const v of issue.violations) {
          if (!byCheck[v.check]) byCheck[v.check] = { error: 0, warning: 0 };
          byCheck[v.check][v.severity] = (byCheck[v.check][v.severity] || 0) + 1;
        }
      }
      return { total, withErrors, withWarnings, withFixable, violations, violationErrors, violationWarnings, fixable, byCheck };
    });

    // --- Charts (debounced) ---
    let issuesChart = null;
    let checksChart = null;
    let chartDebounce = null;

    function renderCharts() {
      if (typeof Chart === 'undefined') return; // Chart.js not loaded yet (async)
      const s = filteredStats.value;
      const issuesEl = document.getElementById('issuesChart');
      const checksEl = document.getElementById('checksChart');
      if (!issuesEl || !checksEl) return;

      const issuesOk = s.total - s.withErrors - s.withWarnings;

      if (issuesChart) {
        issuesChart.data.datasets[0].data = [issuesOk, s.withWarnings, s.withErrors];
        issuesChart.update();
      } else {
        issuesChart = new Chart(issuesEl, {
          type: 'doughnut',
          data: {
            labels: ['Conformes', 'Warnings', 'Erreurs'],
            datasets: [{ data: [issuesOk, s.withWarnings, s.withErrors], backgroundColor: ['#4caf50', '#ffc107', '#f44336'] }]
          },
          options: { responsive: true, animation: { duration: 300 }, plugins: { legend: { position: 'bottom' } } }
        });
      }

      const checksLabels = [];
      const checksData = [];
      const checksColors = [];
      for (const [check, counts] of Object.entries(s.byCheck)) {
        const total = (counts.error || 0) + (counts.warning || 0);
        if (total > 0) {
          checksLabels.push(CHECK_LABELS.value[check] || check);
          checksData.push(total);
          checksColors.push(CHECK_COLORS.value[check] || '#6c757d');
        }
      }

      if (checksChart) {
        checksChart.data.labels = checksLabels;
        checksChart.data.datasets[0].data = checksData;
        checksChart.data.datasets[0].backgroundColor = checksColors;
        checksChart.update();
      } else {
        checksChart = new Chart(checksEl, {
          type: 'doughnut',
          data: { labels: checksLabels, datasets: [{ data: checksData, backgroundColor: checksColors }] },
          options: { responsive: true, animation: { duration: 300 }, plugins: { legend: { position: 'bottom' } } }
        });
      }
    }

    function debouncedChartUpdate() {
      clearTimeout(chartDebounce);
      chartDebounce = setTimeout(() => nextTick().then(renderCharts), 500);
    }

    watch(filteredIssues, () => {
      if (meta.value) debouncedChartUpdate();
    });

    watch(selectedChecks, (val) => {
      if (val.length === 0) selectedChecks.value = [...activeChecks.value];
    });

    watch(selectedProjects, (val) => {
      if (val.length === 0) selectedProjects.value = [...activeProjects.value];
    });

    // --- Progress & snackbar ---
    const progress = ref(null);
    const lastDetail = ref('');
    const snackbar = ref(false);
    const snackbarText = ref('');
    const snackbarColor = ref('green');

    function showSnackbar(text, color = 'green') {
      snackbarText.value = text;
      snackbarColor.value = color;
      snackbar.value = true;
    }

    // --- Load full results (initial load + final sync) ---
    async function loadResults() {
      try {
        const resp = await fetch('/api/results');
        if (!resp.ok) { setTimeout(loadResults, 1000); return; }
        const payload = await resp.json();
        if (!payload.issues) { setTimeout(loadResults, 1000); return; }
        // Extract issues into Map, rest into meta
        const { issues, ...rest } = payload;
        const wasNull = meta.value === null;
        meta.value = rest;
        // Only rebuild issueMap if issue count changed (avoids CLS on full sync
        // when issues were already streamed via SSE)
        if (issues.length !== issueMap.value.size) {
          const newMap = new Map();
          for (const issue of issues) {
            newMap.set(issueKey(issue), issue);
          }
          issueMap.value = newMap;
          triggerRef(issueMap);
        }
        if (wasNull) {
          selectedProjects.value = [...activeProjects.value];
          selectedChecks.value = [...activeChecks.value];
        }
        debouncedChartUpdate();
      } catch (e) {
        showSnackbar(`Erreur de chargement : ${e.message}`, 'red');
        setTimeout(loadResults, 3000);
      }
    }

    loadResults();

    // --- SSE ---
    let sse = new EventSource('/api/events');

    // Full sync (initial results, final diagnostic, final plan)
    sse.addEventListener('update', () => {
      progress.value = null;
      lastDetail.value = '';
      aborting.value = false;
      loadResults();
    });

    // Incremental issue (diagnostic or fix_plan enrichment)
    sse.addEventListener('issue', (e) => {
      try {
        const issue = JSON.parse(e.data);
        issueMap.value.set(issueKey(issue), issue);
        triggerRef(issueMap);
        debouncedChartUpdate();
      } catch {}
    });

    // Incremental plan issue (fix button appears)
    sse.addEventListener('plan_issue', (e) => {
      try {
        const planIssue = JSON.parse(e.data);
        // Update the corresponding issue's plan in meta
        if (meta.value) {
          const existing = meta.value.plan.issues;
          const idx = existing.findIndex(p => p.iid === planIssue.iid && p.project_path === planIssue.project_path);
          if (idx >= 0) {
            existing[idx] = planIssue;
          } else {
            existing.push(planIssue);
          }
        }
      } catch {}
    });

    // Progress updates
    sse.addEventListener('progress', (e) => {
      try {
        const p = JSON.parse(e.data);
        if (p.phase === 'aborting') {
          lastDetail.value = '';
        } else if (p.detail) {
          lastDetail.value = p.detail;
        }
        progress.value = p;
      } catch {}
    });

    sse.onerror = () => {
      showSnackbar('Connexion au serveur perdue, reconnexion...', 'orange');
    };

    // Keep server alive
    setInterval(() => fetch('/api/keepalive', { method: 'POST' }).catch(() => {}), 15000);

    // --- Fix state ---
    const fixDialog = ref(false);
    const fixTarget = ref(null);
    const fixLoading = ref(false);
    const fixApplying = ref(false);
    const fixPlan = ref(null);
    const fixRequestId = ref(null);
    const fixOutput = ref('');
    const fixError = ref(null);

    async function openFixDialog(issue) {
      fixTarget.value = issue;
      fixPlan.value = null;
      fixOutput.value = '';
      fixError.value = null;
      fixLoading.value = true;
      fixApplying.value = false;
      fixDialog.value = true;

      try {
        const resp = await fetch(`/api/fix/${issue.project_path}/${issue.iid}`, { method: 'POST' });
        if (!resp.ok) throw new Error(await resp.text());
        const result = await resp.json();
        fixRequestId.value = result.request_id;
        fixPlan.value = result.plan;
        fixLoading.value = false;
      } catch (e) {
        fixError.value = `Erreur: ${e.message}`;
        fixLoading.value = false;
      }
    }

    async function confirmFix() {
      fixApplying.value = true;
      fixError.value = null;
      try {
        const resp = await fetch(`/api/fix-apply/${fixRequestId.value}`, { method: 'POST' });
        if (!resp.ok) throw new Error(await resp.text());
        for (let i = 0; i < 60; i++) {
          await new Promise(r => setTimeout(r, 1000));
          const statusResp = await fetch(`/api/fix-status/${fixRequestId.value}`);
          const task = await statusResp.json();
          if (task.status === 'applying') continue;
          if (task.status === 'done') {
            fixOutput.value = task.output || '';
            fixTarget.value._fixed = true;
            fixApplying.value = false;
            return;
          }
          fixError.value = task.output || 'L\'application a échoué';
          fixApplying.value = false;
          return;
        }
        fixError.value = 'Timeout lors de l\'application';
        fixApplying.value = false;
      } catch (e) {
        fixError.value = `Erreur: ${e.message}`;
        fixApplying.value = false;
      }
    }

    async function refreshAudit() {
      try {
        const resp = await fetch('/api/refresh', { method: 'POST' });
        if (!resp.ok) {
          const body = await resp.json().catch(() => ({}));
          throw new Error(body.error || `HTTP ${resp.status}`);
        }
        // Reset to initial state
        meta.value = null;
        issueMap.value = new Map();
        triggerRef(issueMap);
        progress.value = null;
        lastDetail.value = '';
        issuesChart = null;
        checksChart = null;
      } catch (e) {
        showSnackbar(`Erreur lors du rafraîchissement : ${e.message}`, 'red');
      }
    }

    const fixableIssues = computed(() =>
      filteredIssues.value.filter(i => i.violations.some(v => v.fixable) && !i._fixed)
    );
    const fixingAll = ref(false);

    async function fixAllFiltered() {
      const issues = fixableIssues.value.map(i => `${i.project_path}#${i.iid}`);
      if (!issues.length) return;
      fixingAll.value = true;
      try {
        const resp = await fetch('/api/fix-all', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ issues }),
        });
        if (!resp.ok) {
          const body = await resp.json().catch(() => ({}));
          throw new Error(body.error || `HTTP ${resp.status}`);
        }
        const { request_id, count } = await resp.json();
        showSnackbar(`Correction de ${count} issues en cours...`, 'orange');
        for (let i = 0; i < 120; i++) {
          await new Promise(r => setTimeout(r, 1000));
          const statusResp = await fetch(`/api/fix-status/${request_id}`);
          const task = await statusResp.json();
          if (task.status === 'applying') continue;
          if (task.status === 'done') {
            fixableIssues.value.forEach(i => { i._fixed = true; });
            showSnackbar(`${count} issues corrigées avec succès`, 'green');
            fixingAll.value = false;
            return;
          }
          showSnackbar(`Échec de la correction : ${task.output || 'erreur inconnue'}`, 'red');
          fixingAll.value = false;
          return;
        }
        showSnackbar('Timeout lors de la correction', 'red');
      } catch (e) {
        showSnackbar(`Erreur : ${e.message}`, 'red');
      } finally {
        fixingAll.value = false;
      }
    }

    // --- Phase meta ---
    const PHASE_META = {
      preload: { icon: 'mdi-download', label: 'Chargement des données' },
      diagnostic: { icon: 'mdi-magnify-scan', label: 'Diagnostic des issues' },
      fix_plan: { icon: 'mdi-wrench-outline', label: 'Construction du plan de correction' },
      aborting: { icon: 'mdi-stop-circle-outline', label: 'Interruption en cours…' },
    };
    function phaseIcon(phase) { return (PHASE_META[phase] || PHASE_META.diagnostic).icon; }
    function phaseLabel(phase) { return (PHASE_META[phase] || PHASE_META.diagnostic).label; }

    const aborting = ref(false);

    async function abortAudit() {
      aborting.value = true;
      try {
        await fetch('/api/abort', { method: 'POST' });
        showSnackbar('Interruption demandée, résultats partiels en cours...', 'orange');
      } catch (e) {
        showSnackbar(`Erreur: ${e.message}`, 'red');
      }
    }

    function formatMs(ms) {
      if (ms >= 1000) return (ms / 1000).toFixed(2) + ' s';
      return ms.toFixed(1) + ' ms';
    }

    function selectAllProjects() { selectedProjects.value = [...activeProjects.value]; }
    function selectNoProjects() { selectedProjects.value = []; }
    function selectOnlyProject(proj) { selectedProjects.value = [proj]; }
    function selectAllChecks() { selectedChecks.value = [...activeChecks.value]; }
    function selectNoChecks() { selectedChecks.value = []; }
    function selectOnlyCheck(check) { selectedChecks.value = [check]; }

    const buildingProgress = computed(() =>
      progress.value && ['diagnostic', 'fix_plan', 'aborting'].includes(progress.value.phase) && data.value
    );

    return {
      data, meta, dataReady, progress, lastDetail, aborting, phaseIcon, phaseLabel, buildingProgress,
      selectedChecks, selectedProjects, isFiltered, snackbar, snackbarText, snackbarColor,
      refreshAudit, abortAudit, fixableIssues, fixingAll, fixAllFiltered,
      allChecks: ALL_CHECKS, checkLabels: CHECK_LABELS, checkColors: CHECK_COLORS, fixLabels: FIX_LABELS, configLoaded,
      activeChecks, activeProjects, filteredIssues, filteredStats,
      selectAllChecks, selectNoChecks, selectOnlyCheck,
      selectAllProjects, selectNoProjects, selectOnlyProject,
      fixDialog, fixTarget, fixLoading, fixApplying, fixPlan, fixOutput, fixError,
      openFixDialog, confirmFix, labelStyle, formatMs,
    };
  }
});

app.use(createVuetify());
app.mount('#app');
