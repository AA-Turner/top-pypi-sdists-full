// dashboard/js/components/StatsOverview.js
import { computed } from 'vue';

const icons = {
  total: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>`,
  plan: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4Z"/></svg>`,
  execute: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
  evaluate: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
  score: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>`,
  calls: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>`,
  tokens: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
};

export const StatsOverview = {
  props: {
    tasks: { type: Array, default: () => [] },
    tokenStats: { type: Object, default: () => ({ total_tokens: 0, total_prompt_calls: 0 }) },
  },
  setup(props) {
    const total = computed(() => props.tasks.length);
    const byPhase = computed(() => {
      const counts = {};
      for (const t of props.tasks) {
        const p = t.phase || 'plan';
        counts[p] = (counts[p] || 0) + 1;
      }
      return counts;
    });
    const avgScore = computed(() => {
      const withScores = props.tasks.filter(t => t.scores);
      if (withScores.length === 0) return null;
      let sum = 0;
      let count = 0;
      for (const t of withScores) {
        for (const v of Object.values(t.scores)) {
          const s = typeof v === 'object' ? (v.score || 0) : v;
          if (typeof s === 'number' && !isNaN(s)) { sum += s; count++; }
        }
      }
      return count > 0 ? (sum / count).toFixed(1) : null;
    });

    const totalTokens = computed(() => {
      const t = props.tokenStats.total_tokens;
      if (t > 1000000) return (t / 1000000).toFixed(1) + 'M';
      if (t > 1000) return (t / 1000).toFixed(1) + 'K';
      return String(t);
    });
    const totalCalls = computed(() => props.tokenStats.total_prompt_calls || 0);

    const cardItems = computed(() => {
      const items = [
        { key: 'total', label: 'Total Tasks', value: total.value, icon: icons.total },
        { key: 'plan', label: 'Planning', value: byPhase.value.plan || 0, icon: icons.plan },
        { key: 'execute', label: 'In Progress', value: byPhase.value.execute || 0, icon: icons.execute },
        { key: 'evaluate', label: 'Reviewing', value: byPhase.value.evaluate || 0, icon: icons.evaluate },
      ];
      if (avgScore.value !== null) {
        items.push({ key: 'score', label: 'Avg Score', value: avgScore.value, icon: icons.score });
      }
      if (totalCalls.value > 0) {
        items.push({ key: 'calls', label: 'API Calls', value: totalCalls.value, icon: icons.calls });
      }
      if (totalTokens.value !== '0') {
        items.push({ key: 'tokens', label: 'Tokens', value: totalTokens.value, icon: icons.tokens });
      }
      return items;
    });

    return { cardItems };
  },
  template: `
    <div class="stats-overview">
      <div v-for="(card, idx) in cardItems" :key="card.key" class="stats-card" :style="{ animationDelay: (idx * 60) + 'ms' }">
        <div class="stats-card-icon" v-html="card.icon"></div>
        <div class="stats-card-value">{{ card.value }}</div>
        <div class="stats-card-label">{{ card.label }}</div>
      </div>
    </div>
  `
};
