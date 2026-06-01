// dashboard/js/composables/useScoreChart.js
import { ref } from 'vue';

export function useScoreChart() {
  const chartCanvas = ref(null);

  function renderChart(source) {
    if (!chartCanvas.value) return;
    const ctx = chartCanvas.value.getContext('2d');
    if (!ctx) return;

    const w = chartCanvas.value.width || 300;
    const h = chartCanvas.value.height || 150;
    ctx.clearRect(0, 0, w, h);

    if (!source || source.length === 0) return;

    // Auto-detect format: score_history has 'average', reports have 'role'/'score'
    let points;
    if (source[0] && typeof source[0].average === 'number') {
      // score_history format: [{iteration, average, roles}]
      points = source.map(e => ({ iter: e.iteration, score: e.average }));
    } else if (source[0] && (source[0].role || source[0].score !== undefined)) {
      // Reports format: group by iteration
      const byIter = {};
      for (const r of source) {
        const iter = r.iteration || 1;
        if (!byIter[iter]) byIter[iter] = [];
        byIter[iter].push(typeof r.score === 'number' ? r.score : (r.score?.score || 0));
      }
      const iterations = Object.keys(byIter).sort((a, b) => a - b);
      points = iterations.map(iter => ({
        iter: Number(iter),
        score: byIter[iter].reduce((a, b) => a + b, 0) / byIter[iter].length,
      }));
    } else {
      // pass-through: [{iter, score}] or unknown
      points = source.filter(e => typeof e.score === 'number').map(e => ({
        iter: e.iteration || e.iter || 1,
        score: e.score,
      }));
    }

    if (!points || points.length === 0) return;

    const maxScore = 10;
    const pad = { top: 10, right: 10, bottom: 20, left: 35 };
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;

    // Axes
    ctx.strokeStyle = '#ccc';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.left, pad.top);
    ctx.lineTo(pad.left, h - pad.bottom);
    ctx.lineTo(w - pad.right, h - pad.bottom);
    ctx.stroke();

    // Y-axis labels
    ctx.fillStyle = '#666';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'right';
    for (let s = 0; s <= maxScore; s += 2) {
      const y = pad.top + plotH * (1 - s / maxScore);
      ctx.fillText(String(s), pad.left - 5, y + 4);
    }

    // Pass threshold line
    const passY = pad.top + plotH * (1 - 9.0 / maxScore);
    ctx.strokeStyle = 'rgba(34,197,94,0.5)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(pad.left, passY);
    ctx.lineTo(w - pad.right, passY);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#22c55e';
    ctx.textAlign = 'left';
    ctx.font = '9px sans-serif';
    ctx.fillText('9.0', w - pad.right + 2, passY + 4);

    // Plot
    if (points.length === 1) {
      const x = pad.left + plotW / 2;
      const y = pad.top + plotH * (1 - points[0].score / maxScore);
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
      // Score label
      ctx.fillStyle = '#333';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(points[0].score.toFixed(1), x, y - 10);
    } else {
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let i = 0; i < points.length; i++) {
        const x = pad.left + (plotW * i) / (points.length - 1);
        const y = pad.top + plotH * (1 - points[i].score / maxScore);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Dots + labels
      for (let i = 0; i < points.length; i++) {
        const x = pad.left + (plotW * i) / (points.length - 1);
        const y = pad.top + plotH * (1 - points[i].score / maxScore);

        ctx.fillStyle = points[i].score >= 9.0 ? '#22c55e' : '#ef4444';
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fill();

        // Iteration label
        ctx.fillStyle = '#888';
        ctx.font = '9px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('#' + points[i].iter, x, h - 3);
      }
    }
  }

  function destroyChart() {
    if (!chartCanvas.value) return;
    const ctx = chartCanvas.value.getContext('2d');
    if (ctx) ctx.clearRect(0, 0, chartCanvas.value.width, chartCanvas.value.height);
  }

  return { chartCanvas, renderChart, destroyChart };
}
