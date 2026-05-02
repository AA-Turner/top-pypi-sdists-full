/* GhostPC — Setup Wizard Logic */

const TOTAL_STEPS = 10;
let currentStep = 1;
let ws = null;

// Config accumulator — submitted at step 10
const config = {
  gemini_api_key: '',
  model_tier: 'flash',
  browser_method: 'vision',
  features: [],
  allowed_numbers: [],
  stream_port: 8443,
  screen_fps: 10,
  jpeg_quality: 70,
  autostart_enabled: false,
};

// ── Init ──────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  buildStepIndicator();
  buildStepDots();
  connectWS();
  loadExistingConfig();
  setupRadioGroups();
  setupCheckboxGroups();
});

function connectWS() {
  const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  ws = new GhostWS(`${proto}//${location.host}/ws/setup`, {
    onMessage: handleWSMessage,
    onOpen: () => {},
    onClose: () => {},
  });
}

function handleWSMessage(data) {
  if (data.type === 'progress') {
    if (data.step === 'pairing') {
      document.getElementById('pairStatus').textContent = data.message;
    }
  } else if (data.type === 'qr') {
    renderQR(data.data);
  } else if (data.type === 'paired') {
    document.getElementById('pairStatus').textContent = data.message;
    document.getElementById('pairStatus').className = 'mt-sm text-accent';
    toast('WhatsApp connected!', 'success');
  } else if (data.type === 'error') {
    document.getElementById('pairStatus').textContent = data.message;
    document.getElementById('pairStatus').className = 'mt-sm text-danger';
    toast(data.message, 'error', 8000);
  }
}

// ── Step navigation ───────────────────────────────────────────

function goToStep(step) {
  if (step < 1 || step > TOTAL_STEPS) return;

  // Collect data from current step before leaving
  collectStepData(currentStep);

  // Hide current
  const allSteps = document.querySelectorAll('.step');
  allSteps.forEach(s => s.classList.remove('active'));

  // Show target
  const target = document.querySelector(`.step[data-step="${step}"]`);
  if (target) target.classList.add('active');

  currentStep = step;
  updateIndicators();
  updateNavButtons();

  // Run step-specific init
  onStepEnter(step);
}

function nextStep() {
  if (currentStep < TOTAL_STEPS) goToStep(currentStep + 1);
}

function prevStep() {
  if (currentStep > 1) goToStep(currentStep - 1);
}

function updateNavButtons() {
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  prevBtn.style.visibility = currentStep <= 1 ? 'hidden' : 'visible';

  // Hide next button on welcome (step 1) and summary (step 10)
  if (currentStep === 1 || currentStep === TOTAL_STEPS) {
    nextBtn.style.visibility = 'hidden';
  } else {
    nextBtn.style.visibility = 'visible';
    nextBtn.textContent = 'Next';
  }
}

// ── Step indicator ────────────────────────────────────────────

function buildStepIndicator() {
  const container = document.getElementById('stepIndicator');
  for (let i = 1; i <= TOTAL_STEPS; i++) {
    const pip = document.createElement('div');
    pip.className = 'step-pip' + (i === 1 ? ' active' : '');
    pip.dataset.step = i;
    container.appendChild(pip);
  }
}

function buildStepDots() {
  const container = document.getElementById('stepDots');
  for (let i = 1; i <= TOTAL_STEPS; i++) {
    const dot = document.createElement('div');
    dot.className = 'step-dot' + (i === 1 ? ' active' : '');
    dot.dataset.step = i;
    container.appendChild(dot);
  }
}

function updateIndicators() {
  document.querySelectorAll('.step-pip').forEach(pip => {
    const s = parseInt(pip.dataset.step);
    pip.className = 'step-pip';
    if (s < currentStep) pip.classList.add('completed');
    else if (s === currentStep) pip.classList.add('active');
  });

  document.querySelectorAll('.step-dot').forEach(dot => {
    const s = parseInt(dot.dataset.step);
    dot.className = 'step-dot';
    if (s < currentStep) dot.classList.add('completed');
    else if (s === currentStep) dot.classList.add('active');
  });
}

// ── Radio / checkbox helpers ──────────────────────────────────

function setupRadioGroups() {
  document.querySelectorAll('.radio-group').forEach(group => {
    group.querySelectorAll('.radio-option').forEach(opt => {
      opt.addEventListener('click', () => {
        group.querySelectorAll('.radio-option').forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        opt.querySelector('input[type="radio"]').checked = true;
      });
    });
  });
}

function setupCheckboxGroups() {
  document.querySelectorAll('.checkbox-group').forEach(group => {
    group.querySelectorAll('.checkbox-option').forEach(opt => {
      opt.addEventListener('click', (e) => {
        if (e.target.type === 'checkbox') return; // Let native toggle happen
        const cb = opt.querySelector('input[type="checkbox"]');
        cb.checked = !cb.checked;
        opt.classList.toggle('selected', cb.checked);
      });
      // Sync on direct checkbox change
      const cb = opt.querySelector('input[type="checkbox"]');
      cb.addEventListener('change', () => {
        opt.classList.toggle('selected', cb.checked);
      });
    });
  });
}

// ── Collect data from current step ────────────────────────────

function collectStepData(step) {
  switch (step) {
    case 3:
      config.gemini_api_key = document.getElementById('apiKeyInput').value.trim();
      break;
    case 4:
      config.model_tier = document.querySelector('input[name="modelTier"]:checked')?.value || 'flash';
      break;
    case 5:
      config.browser_method = document.querySelector('input[name="browserMethod"]:checked')?.value || 'vision';
      break;
    case 6:
      config.features = Array.from(document.querySelectorAll('input[name="features"]:checked'))
        .map(cb => cb.value);
      break;
    case 7: {
      const raw = document.getElementById('numbersInput').value.trim();
      config.allowed_numbers = raw
        ? raw.split(',').map(n => n.trim()).filter(Boolean)
        : [];
      break;
    }
    case 8:
      config.stream_port = parseInt(document.getElementById('portInput').value) || 8443;
      config.screen_fps = parseInt(document.getElementById('fpsInput').value) || 10;
      config.jpeg_quality = parseInt(document.getElementById('qualityInput').value) || 70;
      break;
  }
}

// ── Step-specific init ────────────────────────────────────────

async function onStepEnter(step) {
  switch (step) {
    case 2:
      await checkPrerequisites();
      break;
    case 10:
      buildSummary();
      break;
  }
}

// ── Load existing config ──────────────────────────────────────

async function loadExistingConfig() {
  const res = await api('/api/setup/config');
  if (!res.ok) return;

  const cfg = res.data;
  document.getElementById('versionText').textContent = `v${cfg.version || '0.1.0'}`;

  // Populate fields
  if (cfg.gemini_api_key) {
    document.getElementById('apiKeyInput').value = cfg.gemini_api_key;
    config.gemini_api_key = cfg.gemini_api_key;
  }

  // Model tier
  if (cfg.model_tier) {
    config.model_tier = cfg.model_tier;
    const radio = document.querySelector(`input[name="modelTier"][value="${cfg.model_tier}"]`);
    if (radio) {
      radio.checked = true;
      document.querySelectorAll('#modelTierGroup .radio-option').forEach(o => o.classList.remove('selected'));
      radio.closest('.radio-option').classList.add('selected');
    }
  }

  // Browser method
  if (cfg.browser_method) {
    config.browser_method = cfg.browser_method;
    const radio = document.querySelector(`input[name="browserMethod"][value="${cfg.browser_method}"]`);
    if (radio) {
      radio.checked = true;
      document.querySelectorAll('#browserMethodGroup .radio-option').forEach(o => o.classList.remove('selected'));
      radio.closest('.radio-option').classList.add('selected');
    }
  }

  // Features
  if (cfg.installed_extras && cfg.installed_extras.length) {
    config.features = cfg.installed_extras;
    cfg.installed_extras.forEach(extra => {
      const cb = document.querySelector(`input[name="features"][value="${extra}"]`);
      if (cb) {
        cb.checked = true;
        cb.closest('.checkbox-option').classList.add('selected');
      }
    });
  }

  // Numbers
  if (cfg.allowed_numbers && cfg.allowed_numbers.length) {
    config.allowed_numbers = cfg.allowed_numbers;
    document.getElementById('numbersInput').value = cfg.allowed_numbers.join(', ');
  }

  // Advanced
  if (cfg.stream_port) {
    config.stream_port = cfg.stream_port;
    document.getElementById('portInput').value = cfg.stream_port;
  }
  if (cfg.screen_fps) {
    config.screen_fps = cfg.screen_fps;
    document.getElementById('fpsInput').value = cfg.screen_fps;
  }
  if (cfg.jpeg_quality) {
    config.jpeg_quality = cfg.jpeg_quality;
    document.getElementById('qualityInput').value = cfg.jpeg_quality;
  }
}

// ── Step 2: Prerequisites ─────────────────────────────────────

async function checkPrerequisites() {
  const container = document.getElementById('prereqResults');
  container.innerHTML = '<div class="text-dim">Checking...</div>';

  const res = await api('/api/setup/prerequisites');
  if (!res.ok) return;

  container.innerHTML = '';
  for (const check of res.data.checks) {
    const item = document.createElement('div');
    item.className = 'prereq-item';

    const statusBadge = check.status === 'ok'
      ? '<span class="badge badge-ok">OK</span>'
      : check.status === 'warn'
        ? '<span class="badge badge-warn">WARN</span>'
        : '<span class="badge badge-fail">FAIL</span>';

    item.innerHTML = `
      ${statusBadge}
      <span class="prereq-name">${check.name}</span>
      <span class="prereq-detail">${check.detail || ''}</span>
    `;
    container.appendChild(item);
  }
}

// ── Step 3: Validate API key ──────────────────────────────────

async function validateKey() {
  const key = document.getElementById('apiKeyInput').value.trim();
  const statusEl = document.getElementById('apiKeyStatus');
  const btn = document.getElementById('validateKeyBtn');

  if (!key) {
    statusEl.innerHTML = '<span class="text-warning">No key entered</span>';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Checking...';
  statusEl.innerHTML = '<span class="text-dim">Validating...</span>';

  const res = await api('/api/setup/validate-key', {
    method: 'POST',
    body: { api_key: key },
  });

  btn.disabled = false;
  btn.textContent = 'Validate';

  if (res.ok && res.data.valid) {
    statusEl.innerHTML = '<span class="text-accent">Valid API key</span>';
    config.gemini_api_key = key;
  } else {
    const err = res.data?.error || 'Invalid key';
    statusEl.innerHTML = `<span class="text-danger">Validation failed: ${err}</span>`;
  }
}

// ── Step 9: WhatsApp pairing ─────────────────────────────────

async function startPairing() {
  const btn = document.getElementById('pairBtn');
  btn.disabled = true;
  btn.textContent = 'Pairing...';
  document.getElementById('pairStatus').textContent = 'Starting bridge...';

  const res = await api('/api/setup/pair-whatsapp', { method: 'POST' });

  btn.disabled = false;
  btn.textContent = 'Start Pairing';

  if (!res.ok || !res.data.ok) {
    document.getElementById('pairStatus').textContent = 'Error: ' + (res.data?.error || 'Unknown');
  }
}

function renderQR(data) {
  const container = document.getElementById('qrContainer');
  container.innerHTML = '';

  try {
    const qr = qrcode(0, 'M');
    qr.addData(data);
    qr.make();
    container.innerHTML = qr.createSvgTag(4, 0);

    // Style the generated SVG
    const svg = container.querySelector('svg');
    if (svg) {
      svg.style.background = '#fff';
      svg.style.borderRadius = '12px';
      svg.style.padding = '12px';
      svg.style.maxWidth = '260px';
      svg.style.maxHeight = '260px';
    }
  } catch {
    container.innerHTML = '<div class="qr-placeholder"><p class="text-dim">Failed to render QR code.</p></div>';
  }
}

// ── Step 10: Summary ──────────────────────────────────────────

function buildSummary() {
  // Collect all remaining data
  for (let i = 1; i <= 9; i++) collectStepData(i);

  const table = document.getElementById('summaryTable');
  const rows = [
    ['API Key', config.gemini_api_key ? config.gemini_api_key.substring(0, 8) + '...' : 'Not set'],
    ['Model Tier', config.model_tier],
    ['Browser Method', config.browser_method],
    ['Features', config.features.length ? config.features.join(', ') : 'None'],
    ['Allowed Numbers', config.allowed_numbers.length ? config.allowed_numbers.join(', ') : 'All'],
    ['Stream Port', config.stream_port],
    ['Screen FPS', config.screen_fps],
    ['JPEG Quality', config.jpeg_quality],
  ];

  table.innerHTML = rows.map(([key, val]) => `
    <div class="summary-row">
      <div class="summary-key">${key}</div>
      <div class="summary-val">${val}</div>
    </div>
  `).join('');
}

async function saveAndFinish() {
  const res = await saveConfig();
  if (res) {
    toast('Configuration saved! Starting GhostPC — you can close this tab.', 'success');
    // Disable buttons to prevent double-click
    document.querySelectorAll('.step[data-step="10"] button').forEach(b => b.disabled = true);
    if (ws) ws.send({ action: 'done', autoStart: true });
  }
}

async function saveOnly() {
  const res = await saveConfig();
  if (res) {
    toast('Configuration saved! You can close this tab.', 'success');
    document.querySelectorAll('.step[data-step="10"] button').forEach(b => b.disabled = true);
    if (ws) ws.send({ action: 'done', autoStart: false });
  }
}

async function saveConfig() {
  const res = await api('/api/setup/save', {
    method: 'POST',
    body: config,
  });

  if (res.ok && res.data.ok) {
    return true;
  } else {
    toast('Failed to save: ' + (res.data?.error || 'Unknown error'), 'error');
    return false;
  }
}

// ── Utilities ─────────────────────────────────────────────────

function appendLog(elementId, message) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const line = document.createElement('div');
  line.textContent = message;
  el.appendChild(line);
  el.scrollTop = el.scrollHeight;
}
