/* GhostPC — Dashboard Logic */

let ws = null;
let isPaused = false;
let logFilter = 'all';

// ── Init ──────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  connectWS();
  setupNav();
  setupLogFilters();
  loadInitialData();
});

// ── WebSocket ─────────────────────────────────────────────────

function connectWS() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new GhostWS(`${proto}//${location.host}/ws/dashboard`, {
    onMessage: handleWSMessage,
    onOpen: () => setConnectionStatus(true),
    onClose: () => setConnectionStatus(false),
  });
}

function handleWSMessage(data) {
  if (data.type === 'status') {
    updateStatus(data.data);
  } else if (data.type === 'logs') {
    for (const entry of data.data) {
      appendLog(entry);
    }
  }
}

// ── Navigation ────────────────────────────────────────────────

function setupNav() {
  document.querySelectorAll('[data-section]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      const section = el.dataset.section;
      showSection(section);
    });
  });
}

function showSection(name) {
  // Update nav
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const navItem = document.querySelector(`.nav-item[data-section="${name}"]`);
  if (navItem) navItem.classList.add('active');

  // Show section
  document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
  const section = document.getElementById(`section-${name}`);
  if (section) section.classList.add('active');
}

// ── Status updates ────────────────────────────────────────────

function updateStatus(status) {
  // WhatsApp
  const waEl = document.getElementById('waStatus');
  if (status.whatsapp_connected) {
    waEl.textContent = 'Connected';
    waEl.className = 'card-value text-accent';
  } else {
    waEl.textContent = 'Disconnected';
    waEl.className = 'card-value text-danger';
  }

  // Agent state
  const stateEl = document.getElementById('agentState');
  if (status.paused) {
    stateEl.textContent = 'Paused';
    stateEl.className = 'card-value text-warning';
    isPaused = true;
  } else if (status.processing) {
    stateEl.textContent = 'Processing';
    stateEl.className = 'card-value text-accent';
    isPaused = false;
  } else {
    stateEl.textContent = 'Ready';
    stateEl.className = 'card-value';
    isPaused = false;
  }

  // Update pause button
  const pauseBtn = document.getElementById('pauseBtn');
  pauseBtn.textContent = isPaused ? 'Resume' : 'Pause';

  // Uptime
  if (status.uptime_seconds != null) {
    document.getElementById('uptime').textContent = formatUptime(status.uptime_seconds);
  }

  // ── Feature status cards ──
  updateFeatureCards(status);
}

function updateFeatureCards(status) {
  // Notifications
  const notifEl = document.getElementById('notifStatus');
  if (notifEl && status.notifications) {
    if (status.notifications.active) {
      notifEl.textContent = 'Active';
      notifEl.className = 'card-value card-value-sm text-accent';
    } else if (status.notifications.enabled) {
      notifEl.textContent = 'Enabled';
      notifEl.className = 'card-value card-value-sm text-warning';
    } else {
      notifEl.textContent = 'Disabled';
      notifEl.className = 'card-value card-value-sm text-dim';
    }
  }

  // Memory
  const memEl = document.getElementById('memoryStatus');
  if (memEl && status.memory) {
    const backend = status.memory.backend;
    if (backend === 'chromadb') {
      memEl.textContent = 'ChromaDB';
      memEl.className = 'card-value card-value-sm text-accent';
    } else if (backend === 'sqlite') {
      memEl.textContent = 'SQLite (Persistent)';
      memEl.className = 'card-value card-value-sm text-accent';
    } else {
      memEl.textContent = 'In-Memory';
      memEl.className = 'card-value card-value-sm text-dim';
    }
  }

  // Voice
  const voiceEl = document.getElementById('voiceStatus');
  if (voiceEl && status.voice) {
    if (status.voice.active) {
      voiceEl.textContent = 'Listening';
      voiceEl.className = 'card-value card-value-sm text-accent';
    } else if (status.voice.enabled) {
      voiceEl.textContent = 'Ready';
      voiceEl.className = 'card-value card-value-sm text-warning';
    } else {
      voiceEl.textContent = 'Disabled';
      voiceEl.className = 'card-value card-value-sm text-dim';
    }
  }

  // Confirmations
  const confEl = document.getElementById('confirmStatus');
  if (confEl && status.confirmations) {
    const pending = status.confirmations.pending_count || 0;
    if (!status.confirmations.enabled) {
      confEl.textContent = 'Disabled';
      confEl.className = 'card-value card-value-sm text-dim';
    } else if (pending > 0) {
      confEl.textContent = `${pending} Pending`;
      confEl.className = 'card-value card-value-sm text-warning';
    } else {
      confEl.textContent = 'Active';
      confEl.className = 'card-value card-value-sm text-accent';
    }
  }
}

function setConnectionStatus(connected) {
  const dot = document.getElementById('connDot');
  const text = document.getElementById('connText');
  if (connected) {
    dot.className = 'status-dot green pulse';
    text.textContent = 'Connected';
  } else {
    dot.className = 'status-dot red';
    text.textContent = 'Disconnected';
  }
}

function formatUptime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

// ── Log display ───────────────────────────────────────────────

function appendLog(entry) {
  addLogEntry('recentLogs', entry, 100);
  addLogEntry('fullLogs', entry, 2000);
}

function addLogEntry(panelId, entry, maxEntries) {
  const panel = document.getElementById(panelId);
  if (!panel) return;

  const el = document.createElement('div');
  el.className = `log-entry level-${entry.level}`;
  el.dataset.level = entry.level;

  const time = new Date(entry.timestamp * 1000);
  const timeStr = time.toLocaleTimeString('en-US', { hour12: false });

  el.innerHTML = `
    <span class="log-time">${timeStr}</span>
    <span class="log-level">${entry.level}</span>
    <span class="log-msg">${escapeHtml(entry.message)}</span>
  `;

  // Apply current filter
  if (logFilter !== 'all' && entry.level !== logFilter) {
    el.style.display = 'none';
  }

  panel.appendChild(el);

  // Limit entries
  while (panel.children.length > maxEntries) {
    panel.removeChild(panel.firstChild);
  }

  // Auto-scroll
  panel.scrollTop = panel.scrollHeight;
}

function setupLogFilters() {
  document.querySelectorAll('.log-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.log-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      logFilter = btn.dataset.level;
      applyLogFilter();
    });
  });
}

function applyLogFilter() {
  document.querySelectorAll('#fullLogs .log-entry').forEach(entry => {
    if (logFilter === 'all' || entry.dataset.level === logFilter) {
      entry.style.display = '';
    } else {
      entry.style.display = 'none';
    }
  });
}

// ── Initial data load ─────────────────────────────────────────

async function loadInitialData() {
  // Load existing logs
  const logsRes = await api('/api/logs?count=100');
  if (logsRes.ok && logsRes.data.logs) {
    for (const entry of logsRes.data.logs) {
      appendLog(entry);
    }
  }

  // Load cost
  const costRes = await api('/api/cost');
  if (costRes.ok) {
    updateCost(costRes.data);
  }

  // Load status
  const statusRes = await api('/api/status');
  if (statusRes.ok) {
    updateStatus(statusRes.data);
  }
}

function updateCost(data) {
  const el = document.getElementById('costValue');
  if (data.total_tokens != null) {
    const tokens = data.total_tokens;
    if (tokens >= 1000000) {
      el.textContent = `${(tokens / 1000000).toFixed(1)}M tokens`;
    } else if (tokens >= 1000) {
      el.textContent = `${(tokens / 1000).toFixed(1)}K tokens`;
    } else {
      el.textContent = `${tokens} tokens`;
    }
  } else {
    el.textContent = '0 tokens';
  }
}

// ── Controls ──────────────────────────────────────────────────

async function togglePause() {
  const endpoint = isPaused ? '/api/control/resume' : '/api/control/pause';
  const res = await api(endpoint, { method: 'POST' });
  if (res.ok) {
    isPaused = !isPaused;
    document.getElementById('pauseBtn').textContent = isPaused ? 'Resume' : 'Pause';
    toast(isPaused ? 'Agent paused' : 'Agent resumed', 'info');
  }
}

async function emergencyStop() {
  if (!confirm('Are you sure you want to stop GhostPC?')) return;
  const res = await api('/api/control/stop', { method: 'POST' });
  if (res.ok) {
    toast('GhostPC stopping...', 'warning');
  }
}

// ── Utilities ─────────────────────────────────────────────────

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
