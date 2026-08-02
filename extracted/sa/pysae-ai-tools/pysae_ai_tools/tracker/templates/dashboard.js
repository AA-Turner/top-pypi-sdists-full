const { createApp, ref, computed, watch, onMounted, nextTick } = Vue;

const COLORS = [
  '#4CAF50', '#2196F3', '#FF9800', '#E91E63', '#9C27B0',
  '#00BCD4', '#FF5722', '#3F51B5', '#8BC34A', '#FFC107',
  '#607D8B', '#795548', '#009688', '#CDDC39', '#F44336',
];

const ROOT_GROUP_PREFIX = 'pysae/';

function shortProject(path) {
  if (!path) return '';
  return path.startsWith(ROOT_GROUP_PREFIX) ? path.slice(ROOT_GROUP_PREFIX.length) : path;
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

function addDays(dateStr, n) {
  const d = new Date(dateStr);
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
}

function mondayOfWeek(dateStr) {
  const d = new Date(dateStr);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  d.setDate(diff);
  return d.toISOString().slice(0, 10);
}

function firstOfMonth(dateStr) {
  return dateStr.slice(0, 8) + '01';
}

function lastOfMonth(dateStr) {
  const d = new Date(dateStr);
  const last = new Date(d.getFullYear(), d.getMonth() + 1, 0);
  return last.toISOString().slice(0, 10);
}

const app = createApp({
  setup() {
    const startDate = ref(today());
    const endDate = ref(today());
    const groupBy = ref('smart');
    const maxGap = ref(15);
    const activeFilters = ref([]);
    const loading = ref(false);
    const drawer = ref(false);
    const data = ref(null);
    const heatmapData = ref(null);
    const timelineData = ref(null);
    const filterOptions = ref({ smart: [], issues: [], epics: [], labels: [], projects: [] });

    // Contextualize dialog state
    const sessionsData = ref(null);
    const assignDialog = ref(false);
    const assignTarget = ref(null);
    const issueSearch = ref('');
    const issuesLoading = ref(false);
    const gitlabIssues = ref({ priority_issues: [], other_issues: [] });

    const uncontextualizedSessions = computed(() => {
      if (!sessionsData.value) return [];
      return sessionsData.value.sessions.filter(s => !s.issue_iid);
    });

    const isMultiDay = computed(() => startDate.value !== endDate.value);

    const barChart = ref(null);
    const doughnutChart = ref(null);
    const heatmapChart = ref(null);
    const timelineChart = ref(null);
    let barChartInstance = null;
    let doughnutChartInstance = null;
    let heatmapChartInstance = null;
    let timelineChartInstance = null;

    const quickDates = [
      { label: "Aujourd'hui", fn: () => ({ s: today(), e: today() }) },
      { label: 'Hier', fn: () => ({ s: addDays(today(), -1), e: addDays(today(), -1) }) },
      { label: 'Cette semaine', fn: () => ({ s: mondayOfWeek(today()), e: today() }) },
      { label: 'Semaine derniere', fn: () => {
        const mon = mondayOfWeek(addDays(today(), -7));
        return { s: mon, e: addDays(mon, 6) };
      }},
      { label: 'Ce mois', fn: () => ({ s: firstOfMonth(today()), e: today() }) },
      { label: 'Mois dernier', fn: () => {
        const prev = addDays(firstOfMonth(today()), -1);
        return { s: firstOfMonth(prev), e: prev };
      }},
    ];

    const startDateObj = computed({
      get: () => new Date(startDate.value + 'T00:00:00'),
      set: (d) => { if (d instanceof Date) startDate.value = d.toISOString().slice(0, 10); }
    });
    const endDateObj = computed({
      get: () => new Date(endDate.value + 'T00:00:00'),
      set: (d) => { if (d instanceof Date) endDate.value = d.toISOString().slice(0, 10); }
    });

    const scopeLabel = computed(() => ({
      smart: 'Catégories', issue: 'Issues', epic: 'Epics', label: 'Labels', project: 'Projets', session: 'Sessions'
    }[groupBy.value] || 'Items'));

    const dayCount = computed(() => {
      if (!startDate.value || !endDate.value) return 0;
      const diff = new Date(endDate.value) - new Date(startDate.value);
      return Math.max(1, Math.floor(diff / 86400000) + 1);
    });

    const avgHoursPerDay = computed(() => {
      if (!data.value || dayCount.value === 0) return '0';
      return (data.value.total_hours / dayCount.value).toFixed(1);
    });

    const barChartHeight = computed(() => {
      if (!data.value) return 300;
      return Math.max(300, data.value.entries.length * 35);
    });

    const hasAnyFilter = computed(() => {
      const f = filterOptions.value;
      return f.smart.length > 0 || f.issues.length > 0 || f.epics.length > 0 || f.labels.length > 0 || f.projects.length > 0;
    });

    const tableHeaders = [
      { title: 'Scope', key: 'label', sortable: true },
      { title: 'Heures', key: 'total_hours', sortable: true },
      { title: '%', key: 'pct', sortable: false },
    ];

    function pct(item) {
      return item.percentage != null ? item.percentage.toFixed(1) : '0';
    }

    function applyQuickDate(q) {
      const { s, e } = q.fn();
      startDate.value = s;
      endDate.value = e;
    }

    const activeQuickDate = computed(() => {
      for (const q of quickDates) {
        const { s, e } = q.fn();
        if (s === startDate.value && e === endDate.value) return q.label;
      }
      return null;
    });

    const activeFilterSet = computed(() => new Set(activeFilters.value));

    function toggleFilter(scope, value) {
      const key = scope + ':' + value;
      const idx = activeFilters.value.indexOf(key);
      if (idx >= 0) {
        activeFilters.value.splice(idx, 1);
      } else {
        activeFilters.value.push(key);
      }
    }

    function buildFilterParams() {
      const params = new URLSearchParams();
      for (const f of activeFilters.value) {
        const [scope, ...rest] = f.split(':');
        const value = rest.join(':');
        params.append('filter_' + scope, value);
      }
      return params;
    }

    let fetchTimeout = null;
    function debouncedFetch() {
      clearTimeout(fetchTimeout);
      fetchTimeout = setTimeout(fetchData, 300);
    }

    async function fetchData() {
      if (!startDate.value || !endDate.value) return;
      loading.value = true;
      try {
        const filterParams = buildFilterParams();
        const baseParams = `start_date=${startDate.value}&end_date=${endDate.value}&max_gap_minutes=${maxGap.value}`;
        const dashParams = `${baseParams}&group_by=${groupBy.value}`;
        const filterStr = filterParams.toString();
        const dashQs = filterStr ? dashParams + '&' + filterStr : dashParams;

        const [dashRes, heatRes, filterRes, timelineRes, sessionsRes] = await Promise.all([
          fetch('/api/dashboard?' + dashQs),
          fetch(`/api/heatmap?${baseParams}`),
          fetch(`/api/filters?${baseParams}`),
          fetch(`/api/timeline?${dashQs}&group_by=${groupBy.value}`),
          fetch(`/api/sessions?${baseParams}`),
        ]);
        data.value = await dashRes.json();
        heatmapData.value = await heatRes.json();
        filterOptions.value = await filterRes.json();
        timelineData.value = await timelineRes.json();
        sessionsData.value = await sessionsRes.json();
        await nextTick();
        renderCharts();
        // Vuetify layout settles asynchronously; re-render after stabilization
        setTimeout(() => {
          for (const id of Object.keys(Chart.instances)) Chart.instances[id].resize();
        }, 200);
      } catch (e) {
        console.error('Fetch error:', e);
      } finally {
        loading.value = false;
      }
    }

    function renderCharts() {
      if (!data.value) return;
      renderBarChart();
      renderDoughnutChart();
      renderHeatmapChart();
      renderTimelineChart();
    }

    function renderBarChart() {
      if (!barChart.value || !data.value) return;
      const entries = data.value.entries;
      const labels = entries.map(e => truncate(e.label, 50));
      const values = entries.map(e => e.total_hours);
      const pcts = entries.map(e => e.percentage);
      const colors = entries.map((_, i) => COLORS[i % COLORS.length]);

      if (barChartInstance) barChartInstance.destroy();
      barChartInstance = new Chart(barChart.value, {
        type: 'bar',
        data: {
          labels,
          datasets: [{ data: values, backgroundColor: colors, borderWidth: 0 }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: ctx => ctx.parsed.x.toFixed(2) + 'h (' + pcts[ctx.dataIndex].toFixed(1) + '%)'
              }
            },
            datalabels: {
              anchor: 'end',
              align: 'end',
              font: { size: 11, weight: 'bold' },
              formatter: (val, ctx) => pcts[ctx.dataIndex].toFixed(1) + '%',
              color: '#333',
            }
          },
          layout: { padding: { right: 35 } },
          scales: {
            x: { title: { display: true, text: 'Heures' }, beginAtZero: true },
            y: { ticks: { font: { size: 11 } } }
          }
        }
      });
    }

    function renderDoughnutChart() {
      if (!doughnutChart.value || !data.value) return;
      const entries = data.value.entries.slice(0, 10);
      const labels = entries.map(e => truncate(e.label, 30));
      const values = entries.map(e => e.total_hours);
      const pcts = entries.map(e => e.percentage);
      const colors = entries.map((_, i) => COLORS[i % COLORS.length]);

      if (doughnutChartInstance) doughnutChartInstance.destroy();
      doughnutChartInstance = new Chart(doughnutChart.value, {
        type: 'doughnut',
        data: {
          labels,
          datasets: [{ data: values, backgroundColor: colors, borderWidth: 1 }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 12 } },
            tooltip: {
              callbacks: {
                label: ctx => ctx.label + ': ' + ctx.parsed.toFixed(2) + 'h (' + pcts[ctx.dataIndex].toFixed(1) + '%)'
              }
            },
            datalabels: {
              formatter: (val, ctx) => {
                const p = pcts[ctx.dataIndex];
                return p >= 5 ? p.toFixed(1) + '%' : '';
              },
              color: '#fff',
              font: { size: 11, weight: 'bold' },
            }
          }
        }
      });
    }

    function renderHeatmapChart() {
      if (!heatmapChart.value || !heatmapData.value) return;
      const days = heatmapData.value.days;
      if (days.length <= 1) return;

      const labels = days.map(d => d.date);
      const values = days.map(d => d.total_hours);

      if (heatmapChartInstance) heatmapChartInstance.destroy();
      heatmapChartInstance = new Chart(heatmapChart.value, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: '#2196F3',
            borderRadius: 3,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { display: false },
            datalabels: { display: false },
            tooltip: {
              callbacks: { label: ctx => ctx.parsed.y.toFixed(2) + 'h' }
            }
          },
          scales: {
            y: { title: { display: true, text: 'Heures' }, beginAtZero: true },
            x: { ticks: { font: { size: 10 } } }
          }
        }
      });
    }

    function renderTimelineChart() {
      if (!timelineChart.value || !timelineData.value) return;
      const td = timelineData.value;
      if (!td.times || !td.times.length || !td.series || !td.series.length) return;

      const labels = td.times.map(t => {
        const d = new Date(t);
        return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      });

      const datasets = td.series.map((s, i) => ({
        label: truncate(s.label, 30),
        data: s.points.map(p => p.percentage),
        backgroundColor: COLORS[i % COLORS.length] + '80',
        borderColor: COLORS[i % COLORS.length],
        borderWidth: 1,
        fill: true,
        stepped: 'middle',
        pointRadius: 0,
        pointHitRadius: 8,
      }));

      if (timelineChartInstance) timelineChartInstance.destroy();
      timelineChartInstance = new Chart(timelineChart.value, {
        type: 'line',
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 9 }, boxWidth: 10 } },
            datalabels: { display: false },
            tooltip: {
              mode: 'index',
              callbacks: {
                title: ctx => {
                  const t = td.times[ctx[0].dataIndex];
                  return new Date(t).toLocaleString('fr-FR', {
                    day: '2-digit', month: '2-digit',
                    hour: '2-digit', minute: '2-digit'
                  });
                },
                label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(0) + '%'
              }
            }
          },
          scales: {
            y: {
              stacked: true,
              title: { display: true, text: 'Densite (%)' },
              beginAtZero: true,
            },
            x: {
              ticks: { font: { size: 9 }, maxRotation: 45 },
            }
          }
        }
      });
    }

    function openAssignDialog(session) {
      assignTarget.value = session;
      issueSearch.value = '';
      gitlabIssues.value = { priority_issues: [], other_issues: [] };
      assignDialog.value = true;
      fetchGitlabIssues();
    }

    let issueSearchTimeout = null;
    function debouncedSearchIssues() {
      clearTimeout(issueSearchTimeout);
      issueSearchTimeout = setTimeout(fetchGitlabIssues, 400);
    }

    async function fetchGitlabIssues() {
      if (!assignTarget.value) return;
      issuesLoading.value = true;
      try {
        const params = new URLSearchParams();
        if (assignTarget.value.project_path) params.set('project_path', assignTarget.value.project_path);
        if (issueSearch.value) params.set('search', issueSearch.value);
        // Add other projects from sessions
        if (sessionsData.value) {
          const otherProjects = new Set(
            sessionsData.value.sessions
              .map(s => s.project_path)
              .filter(p => p && p !== assignTarget.value.project_path)
          );
          for (const p of otherProjects) params.append('other_projects', p);
        }
        const res = await fetch('/api/gitlab-issues?' + params);
        gitlabIssues.value = await res.json();
      } catch (e) {
        console.error('Fetch gitlab issues error:', e);
      } finally {
        issuesLoading.value = false;
      }
    }

    async function assignIssue(issue) {
      if (!assignTarget.value) return;
      const targetDate = assignTarget.value.start.slice(0, 10);
      try {
        await fetch('/api/contextualize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: assignTarget.value.session_id,
            target_date: targetDate,
            project_path: issue.project_path,
            project_id: issue.project_id,
            issue_iid: issue.iid,
            issue_title: issue.title,
            issue_url: issue.web_url,
            issue_labels: issue.labels,
          }),
        });
        assignDialog.value = false;
        fetchData();
      } catch (e) {
        console.error('Assign issue error:', e);
      }
    }

    function truncate(str, max) {
      return str.length > max ? str.slice(0, max - 1) + '\u2026' : str;
    }

    watch([startDate, endDate, groupBy, maxGap, activeFilters], debouncedFetch, { deep: true });

    onMounted(async () => {
      try {
        const res = await fetch('/api/date-range');
        const range = await res.json();
        if (range.max_date) {
          endDate.value = range.max_date;
          startDate.value = range.max_date;
        }
      } catch (_) { /* ignore */ }
      fetchData();
    });

    return {
      startDate, endDate, startDateObj, endDateObj, groupBy, maxGap, activeFilters, loading, drawer,
      data, heatmapData, timelineData, filterOptions,
      barChart, doughnutChart, heatmapChart, timelineChart,
      quickDates, scopeLabel, dayCount, avgHoursPerDay, barChartHeight,
      hasAnyFilter, tableHeaders, pct, applyQuickDate,
      activeQuickDate, activeFilterSet, toggleFilter,
      sessionsData, uncontextualizedSessions, isMultiDay,
      assignDialog, assignTarget, issueSearch, issuesLoading, gitlabIssues,
      openAssignDialog, debouncedSearchIssues, assignIssue,
      shortProject,
    };
  }
});

app.use(Vuetify.createVuetify({ theme: { defaultTheme: 'light' } }));
app.mount('#app');
