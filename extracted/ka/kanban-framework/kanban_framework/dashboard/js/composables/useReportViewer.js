// dashboard/js/composables/useReportViewer.js
import { ref, computed } from 'vue';

export function useReportViewer(taskDetail) {
  const selectedIteration = ref(0);
  const expandedReports = ref({});

  // Score color class helper
  const scoreClass = (score) => {
    if (score >= 9) return 'high';
    if (score >= 7) return 'mid';
    return 'low';
  };

  // Extract dimension data from a report
  const getDimensions = (report) => {
    if (!report) return [];
    const dims = [];
    if (report.dimensions && typeof report.dimensions === 'object') {
      for (const [name, val] of Object.entries(report.dimensions)) {
        if (typeof val === 'object' && val.score !== undefined) {
          dims.push({ name, score: val.score, findings: val.findings || [], issues: val.issues || [] });
        } else if (typeof val === 'number') {
          dims.push({ name, score: val, findings: [], issues: [] });
        }
      }
    } else {
      for (const [name, val] of Object.entries(report)) {
        if (typeof val === 'object' && val !== null && !Array.isArray(val)) {
          if (val.score !== undefined && typeof val.score === 'number') {
            dims.push({ name, score: val.score, findings: val.findings || [], issues: val.issues || [] });
          }
        } else if (typeof val === 'number') {
          dims.push({ name, score: val, findings: [], issues: [] });
        }
      }
    }
    return dims;
  };

  // Get reports grouped by iteration
  const iterationReports = computed(() => {
    if (!taskDetail.value || !taskDetail.value.reports) return [];
    const reports = taskDetail.value.reports;
    if (reports.length === 0) return [];

    const hasIteration = reports.some(r => r.iteration !== undefined);
    if (!hasIteration) {
      return [{ iteration: 1, reports }];
    }

    const groups = {};
    reports.forEach(r => {
      const iter = r.iteration || 1;
      if (!groups[iter]) groups[iter] = [];
      groups[iter].push(r);
    });

    return Object.entries(groups)
      .map(([iter, reps]) => ({ iteration: Number(iter), reports: reps }))
      .sort((a, b) => a.iteration - b.iteration);
  });

  const currentIterationReports = computed(() => {
    const iterations = iterationReports.value;
    if (iterations.length === 0) return [];
    const idx = Math.min(selectedIteration.value, iterations.length - 1);
    return iterations[idx] ? iterations[idx].reports : [];
  });

  const toggleReport = (role) => {
    expandedReports.value[role] = !expandedReports.value[role];
  };

  const isReportExpanded = (role) => {
    return expandedReports.value[role] !== false;
  };

  return {
    selectedIteration,
    expandedReports,
    iterationReports,
    currentIterationReports,
    toggleReport,
    isReportExpanded,
    scoreClass,
    getDimensions
  };
}
