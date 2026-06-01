// dashboard/js/composables/useTokenChart.js
import { ref } from 'vue';

export function useTokenChart() {
  const tokenCanvas = ref(null);
  const callsCanvas = ref(null);

  function _render(ctx, w, h, title, values, maxV, color, unit) {
    const pad = { top: 22, right: 16, bottom: 28, left: 48 };
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;

    // Match page theme via CSS
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const bg = isDark ? '#1a1a2e' : '#f9f8f5';
    const fg = isDark ? '#aaa' : '#777';
    const grid = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.06)';

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // Grid
    ctx.strokeStyle = grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (plotH * i / 4);
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(w - pad.right, y);
      ctx.stroke();
    }

    // Y axis labels
    ctx.fillStyle = fg;
    ctx.font = '9px JetBrains Mono, monospace';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 4; i++) {
      const v = Math.round(maxV * (1 - i / 4));
      const y = pad.top + (plotH * i / 4);
      ctx.fillText(String(v), pad.left - 5, y + 3);
    }

    // Line
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    for (let i = 0; i < values.length; i++) {
      const x = pad.left + (plotW * i / (values.length - 1 || 1));
      const y = pad.top + plotH - (values[i] / maxV * plotH);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Area fill
    ctx.fillStyle = color + '18';
    ctx.lineTo(pad.left + plotW, pad.top + plotH);
    ctx.lineTo(pad.left, pad.top + plotH);
    ctx.closePath();
    ctx.fill();

    // Dots
    ctx.fillStyle = color;
    for (let i = 0; i < values.length; i++) {
      if (values[i] === 0) continue;
      const x = pad.left + (plotW * i / (values.length - 1 || 1));
      const y = pad.top + plotH - (values[i] / maxV * plotH);
      ctx.beginPath();
      ctx.arc(x, y, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }

    // Title
    ctx.fillStyle = fg;
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(title + ' (' + unit + ')', pad.left, pad.top - 6);
  }

  function render(daily) {
    if (!daily || daily.length === 0) return;

    const data = [...daily].sort((a, b) => a.date.localeCompare(b.date));
    const labels = data.map(d => d.date.slice(5));
    const calls = data.map(d => d.calls || 0);
    const tokens = data.map(d => (d.tokens || 0) / 1000);

    // Token chart
    const tCtx = tokenCanvas.value?.getContext('2d');
    if (tCtx) {
      const tw = tokenCanvas.value.width || 500;
      const th = tokenCanvas.value.height || 160;
      const maxT = Math.max(...tokens, 1);
      _render(tCtx, tw, th, 'Token 消耗', tokens, maxT, '#ff8a65', 'K');
      // X labels
      const pad = { top: 22, right: 16, bottom: 28, left: 48 };
      tCtx.fillStyle = document.documentElement.getAttribute('data-theme') === 'dark' ? '#888' : '#777';
      tCtx.font = '8px JetBrains Mono, monospace';
      tCtx.textAlign = 'center';
      const step = Math.max(1, Math.floor(labels.length / 10));
      for (let i = 0; i < labels.length; i += step) {
        const x = pad.left + ((tw - pad.left - pad.right) * i / (labels.length - 1 || 1));
        tCtx.fillText(labels[i], x, th - 6);
      }
    }

    // Calls chart
    const cCtx = callsCanvas.value?.getContext('2d');
    if (cCtx) {
      const cw = callsCanvas.value.width || 500;
      const ch = callsCanvas.value.height || 160;
      const maxC = Math.max(...calls, 1);
      _render(cCtx, cw, ch, 'Prompt 次数', calls, maxC, '#4fc3f7', '次');
      const pad = { top: 22, right: 16, bottom: 28, left: 48 };
      cCtx.fillStyle = document.documentElement.getAttribute('data-theme') === 'dark' ? '#888' : '#777';
      cCtx.font = '8px JetBrains Mono, monospace';
      cCtx.textAlign = 'center';
      const step = Math.max(1, Math.floor(labels.length / 10));
      for (let i = 0; i < labels.length; i += step) {
        const x = pad.left + ((cw - pad.left - pad.right) * i / (labels.length - 1 || 1));
        cCtx.fillText(labels[i], x, ch - 6);
      }
    }
  }

  return { tokenCanvas, callsCanvas, render };
}
