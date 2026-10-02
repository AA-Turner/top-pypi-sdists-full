const CLIENT_VERSION = '44';
const $ = id => document.getElementById(id);

let apiToken = '';
let cfg = null;
let activeModule = 'vdedr';
let formState = {};
let interactiveBlocked = false;
let pendingPayload = null;
let pendingModule = null;
let activeLogRun = null;
let logTimer = null;
let logPaused = false;
let showHiddenRuns = false;
let defaultTabOrder = [];
let uiSaveTimer = null;
let historyRowsCache = [];
let historySort = {key:'created_utc', dir:'desc'};
const HISTORY_COLUMN_DEFAULTS = {launched:150,module:110,project:320,control:130,experience:230,families:220,period:125,status:135,actions:270};
const HISTORY_COLUMN_MIN = {launched:110,module:90,project:180,control:100,experience:150,families:140,period:105,status:105,actions:220};
let historyColumnWidths = {...HISTORY_COLUMN_DEFAULTS};
let historyFilters = {module:'', project:'', status:'', search:''};
let projectEditState = null;
let historyMutationPending = 0;


function esc(s) {
  return String(s ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}
function clone(v) { return JSON.parse(JSON.stringify(v)); }
function uniq(xs) { return [...new Set(xs || [])]; }
function lines(v) { return String(v ?? '').split(/\r?\n/).map(x => x.trim()).filter(Boolean); }
function nonempty(v) { return v !== null && v !== undefined && String(v).trim() !== ''; }

function loadToken() {
  const hash = new URLSearchParams(location.hash.replace(/^#/, ''));
  const fromUrl = hash.get('token') || '';
  if (fromUrl) {
    sessionStorage.setItem('pikobs_web_token', fromUrl);
    history.replaceState(null, '', location.pathname + location.search);
    return fromUrl;
  }
  return sessionStorage.getItem('pikobs_web_token') || '';
}
apiToken = loadToken();

async function apiJson(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (apiToken) headers.set('X-Pikobs-Token', apiToken);
  const r = await fetch(path, {...options, headers, cache: 'no-store'});
  const text = await r.text();
  let data = {};
  try { data = text ? JSON.parse(text) : {}; }
  catch (_) { throw new Error(`Backend returned non-JSON data (HTTP ${r.status}): ${text.slice(0, 240)}`); }
  if (!r.ok) {
    const detail = data?.detail;
    if (typeof detail === 'string') throw new Error(detail);
    if (detail?.message) throw new Error(detail.message);
    if (detail !== undefined) throw new Error(JSON.stringify(detail));
    throw new Error(`HTTP ${r.status}`);
  }
  return data;
}

function choicesFor(field) {
  if (field.source === 'families') return cfg.families || [];
  if (field.source === 'regions') return cfg.regions || [];
  if (field.source === 'flags') return cfg.flags_criteria || [];
  if (field.source === 'projections') return cfg.projections || [];
  return field.choices || [];
}


function comparisonFieldDisabled(module, field) {
  const spec = cfg?.module_specs?.[module];
  const st = formState?.[module] || {};
  return Boolean(field?.comparison_only && spec?.control === 'optional_mode' && st._control_mode === 'experience');
}

function canonicalChoice(raw, choices) {
  const q = String(raw).trim().toLowerCase();
  return (choices || []).find(v => String(v).toLowerCase() === q) ?? null;
}

function helpButton(help, fieldKey) {
  const id = `help-${activeModule}-${fieldKey}-${Math.random().toString(36).slice(2,7)}`;
  return `<button class="helpButton" type="button" data-help="${id}" aria-expanded="false" aria-label="Help">?</button>` +
         `<div class="helpPopover hidden" id="${id}">${esc(help)}</div>`;
}

function fieldShell(module, key, label, help, inner, cls = '') {
  return `<div class="field ${cls}" data-field="${esc(key)}">
    <div class="fieldLabelRow"><span class="fieldLabel">${esc(label)}</span>${helpButton(help, key)}</div>
    ${inner}
    <div class="fieldError"></div>
  </div>`;
}

function plainInput(module, key, label, help, opts = {}) {
  const st = formState[module];
  const value = st[key] ?? '';
  const type = opts.type || 'text';
  const list = opts.list ? ` list="${esc(opts.list)}"` : '';
  const attrs = `${opts.min !== undefined ? ` min="${opts.min}"` : ''}${opts.max !== undefined ? ` max="${opts.max}"` : ''}${opts.step !== undefined ? ` step="${opts.step}"` : ''}`;
  const disabled = opts.disabled ? ' disabled' : '';
  const inner = `<input data-bind="${esc(key)}" data-kind="${esc(type === 'number' ? 'number' : 'string')}" type="${esc(type)}" value="${esc(value)}"${list}${attrs}${disabled} autocomplete="off">`;
  return fieldShell(module, key, label, help, inner, `${opts.cls || ''}${opts.disabled ? ' modeDisabled' : ''}`.trim());
}

function selectInput(module, field) {
  const value = formState[module][field.key] ?? '';
  const options = choicesFor(field).map(v => `<option value="${esc(v)}" ${String(v) === String(value) ? 'selected' : ''}>${esc(v)}</option>`).join('');
  const disabled = field.disabled ? ' disabled' : '';
  return fieldShell(module, field.key, field.label, field.help, `<select data-bind="${esc(field.key)}" data-kind="string"${disabled}>${options}</select>`, `${field.cls || ''}${field.disabled ? ' modeDisabled' : ''}`.trim());
}

function tokenInput(module, field) {
  const values = Array.isArray(formState[module][field.key]) ? formState[module][field.key] : [];
  const disabledAttr = field.disabled ? ' disabled' : '';
  const tags = values.map((v, i) => `<span class="tag"><span class="tagText">${esc(v)}</span><button type="button" class="tagRemove" data-remove-token="${i}" aria-label="Remove ${esc(v)}"${disabledAttr}>×</button></span>`).join('');
  const placeholder = field.placeholder || (field.source ? 'Start typing…' : 'Type a value, then Enter');
  const inner = `<div class="tokenEditor" data-token-editor="${esc(field.key)}">
      <div class="tagList">${tags}</div>
      <input type="text" data-token-draft="${esc(field.key)}" placeholder="${esc(placeholder)}" autocomplete="off"${disabledAttr}>
      <div class="suggestions hidden"></div>
    </div>`;
  return fieldShell(module, field.key, field.label, field.help, inner, `${field.cls || ''}${field.disabled ? ' modeDisabled' : ''}`.trim());
}

function renderDynamicField(module, field) {
  const viewField = {...field, disabled: comparisonFieldDisabled(module, field)};
  if (viewField.kind === 'tokens' || viewField.kind === 'number_tokens') return tokenInput(module, viewField);
  if (viewField.kind === 'select') return selectInput(module, viewField);
  if (viewField.kind === 'number') return plainInput(module, viewField.key, viewField.label, viewField.help, {type:'number', min:viewField.min, max:viewField.max, step:viewField.step ?? 'any', disabled:viewField.disabled});
  return plainInput(module, viewField.key, viewField.label, viewField.help, {disabled:viewField.disabled});
}

function renderControl(module, spec) {
  if (spec.control === 'none') return '';
  const st = formState[module];
  let mode = '';
  if (spec.control === 'optional_mode') {
    st._control_mode = st._control_mode || (st.path_control_files ? 'control' : 'experience');
    mode = `<fieldset class="modeBox"><legend>Comparison mode ${helpButton(spec.comparison_help || 'Choose Control vs Experience to compare against a control, or Experience only to process experiments independently.', 'control-mode')}</legend>
      <div class="modeChoices">
        <label class="inlineCheck"><input type="radio" name="${module}ControlMode" value="control" ${st._control_mode === 'control' ? 'checked' : ''}> Control vs Experience</label>
        <label class="inlineCheck"><input type="radio" name="${module}ControlMode" value="experience" ${st._control_mode === 'experience' ? 'checked' : ''}> Experience only</label>
      </div></fieldset>`;
  }
  const optional = spec.control !== 'required';
  const badge = spec.control === 'optional' ? `<span class="controlModeBadge" data-control-badge>${st.path_control_files ? 'Control vs Experience' : 'Experience only'}</span>` : '';
  const disabled = spec.control === 'optional_mode' && st._control_mode === 'experience';
  return `${mode}<div class="grid2 ${disabled ? 'modeDisabled' : ''}" data-control-fields>
    ${fieldShell(module, 'path_control_files', `Control path${optional ? ' (optional)' : ''}`, optional ? 'Leave empty to run the experiment(s) without a control.' : 'Directory containing the required control files.', `<input data-bind="path_control_files" data-kind="string" list="controlPathHistory" value="${esc(st.path_control_files || '')}" autocomplete="off" ${disabled ? 'disabled' : ''}>${badge}`)}
    ${fieldShell(module, 'control_name', 'Control name', 'Short label used for the control in plots and the viewer.', `<input data-bind="control_name" data-kind="string" value="${esc(st.control_name || 'control')}" ${disabled ? 'disabled' : ''}>`)}
  </div>`;
}

function recentExperienceButtons(module) {
  const items = uniq(cfg.memory?.experience || []).slice(0, 8);
  if (!items.length) return '';
  return `<div class="recentChoices"><span class="muted">Recent:</span>${items.map(v => `<button type="button" class="recentChoice" data-recent-exp="${esc(v)}">${esc(v)}</button>`).join('')}</div>`;
}

function renderExperiences(module, spec) {
  const st = formState[module];
  const one = spec.experience === 'one';
  const paths = Array.isArray(st.path_experience_files) ? st.path_experience_files : [];
  const names = Array.isArray(st.experience_name) ? st.experience_name : [];
  if (one) {
    return `<div class="grid2">
      ${fieldShell(module, 'path_experience_files', 'Experience path', 'OBSCOUNTDB requires exactly one experiment directory.', `<input data-bind="path_experience_files" data-kind="single-list" value="${esc(paths[0] || '')}" autocomplete="off">${recentExperienceButtons(module)}`)}
      ${fieldShell(module, 'experience_name', 'Experience name', 'Short label for the experiment.', `<input data-bind="experience_name" data-kind="single-list" value="${esc(names[0] || 'Experience')}">`)}
    </div>`;
  }
  return `<div class="grid2">
    ${fieldShell(module, 'path_experience_files', 'Experience path(s), one per line', 'One directory per experiment. Keep the same order as the names.', `<textarea data-bind="path_experience_files" data-kind="lines" rows="3">${esc(paths.join('\n'))}</textarea>${recentExperienceButtons(module)}`)}
    ${fieldShell(module, 'experience_name', 'Experience name(s), one per line', 'One short name per experiment directory, in exactly the same order.', `<textarea data-bind="experience_name" data-kind="lines" rows="3">${esc(names.join('\n'))}</textarea>`)}
  </div>`;
}

function renderFieldSet(module, fields) {
  const out = [];
  for (let i = 0; i < fields.length;) {
    const field = fields[i];
    if (!field.group) {
      out.push(renderDynamicField(module, field));
      i += 1;
      continue;
    }
    const grouped = [];
    const groupName = field.group;
    while (i < fields.length && fields[i].group === groupName) {
      grouped.push(fields[i]);
      i += 1;
    }
    out.push(`<div class="fieldGroup fieldGroup${grouped.length}" data-field-group="${esc(groupName)}">${grouped.map(f => renderDynamicField(module, f)).join('')}</div>`);
  }
  return out.join('');
}

function renderModule(module) {
  const spec = cfg.module_specs[module];
  const st = formState[module];
  const fields = renderFieldSet(module, spec.fields);
  const pbsNote = spec.pbs_note ? `<div class="pbsNote">${esc(spec.pbs_note)}</div>` : '';
  return `<section class="modulePanel card ${module === activeModule ? '' : 'hidden'}" data-module="${esc(module)}" id="${esc(module)}Panel">
    <form data-module-form="${esc(module)}" novalidate>
      <div class="formHeader">
        <div>
          <div class="moduleTitleRow"><h2>${esc(module.toUpperCase())}</h2><a class="docsLink" href="${esc(spec.docs)}" target="_blank" rel="noopener">Documentation ↗</a></div>
          <p class="moduleIntro">${esc(spec.intro)}</p>
        </div>
        <button type="button" class="secondary compactButton" data-reset-module="${esc(module)}">Reset to defaults</button>
      </div>
      ${pbsNote}

      <div class="formSection"><div class="formSectionTitle">Runs</div>
        ${renderControl(module, spec)}
        ${renderExperiences(module, spec)}
      </div>

      <div class="formSection"><div class="formSectionTitle">Output and period</div>
        ${fieldShell(module, 'pathwork', 'WORK PATH', 'Output directory used exactly as written. First-use default: /fs/site8/eccc/. After a submitted run, Pikobs Web remembers the last WORK PATH for the next session. No internal RUN_ID is appended.', `<input data-bind="pathwork" data-kind="string" list="pathworkHistory" value="${esc(st.pathwork || '')}" autocomplete="off">`, 'full')}
        <div class="grid2">
          ${fieldShell(module, 'datestart', 'DATESTART', 'First UTC cycle, format YYYYMMDDHH. Both ends are included.', `<input data-bind="datestart" data-kind="string" inputmode="numeric" maxlength="10" value="${esc(st.datestart || '')}" placeholder="YYYYMMDDHH">`)}
          ${fieldShell(module, 'dateend', 'DATEEND', 'Last UTC cycle, format YYYYMMDDHH. Defaults are recalculated each time the web app loads.', `<input data-bind="dateend" data-kind="string" inputmode="numeric" maxlength="10" value="${esc(st.dateend || '')}" placeholder="YYYYMMDDHH">`)}
        </div>
      </div>

      <div class="formSection"><div class="formSectionTitle">Selection and options</div>
        <div class="fieldGrid">${fields}</div>
      </div>

      <div class="formSection"><div class="fieldGrid">
        ${fieldShell(module, 'n_cpus', 'N_CPUS', 'Pikobs worker count used by the module.', `<input type="number" data-bind="n_cpus" data-kind="number" min="1" max="256" step="1" value="${esc(st.n_cpus ?? 80)}">`)}
      </div></div>

      <fieldset class="publishBox"><legend>Viewer publication</legend>
        <label><input type="checkbox" data-bind="publish" data-kind="boolean" ${st.publish ? 'checked' : ''}> Publish viewer link when finished ${helpButton('Optional. When the viewer HTML appears, Pikobs Web creates a public symlink and shows the resulting URL. The WORK PATH itself is not renamed.', 'publish')}</label>
      </fieldset>

      <div class="warningMessage hidden" data-warning-box></div>
      <div class="validationMessage" data-validation-message></div>
      <div class="formActions">
        <button type="button" class="secondary" data-interactive-command="${esc(module)}">Interactive command</button>
        <button type="submit" data-run-button="${esc(module)}">Review &amp; Run ${esc(module.toUpperCase())}</button>
      </div>
      <div class="message" data-module-message></div>
    </form>
  </section>`;
}

function orderedModuleIds() {
  return (cfg?.modules || []).filter(m => m.enabled).map(m => m.id);
}

function applyTabOrder(order) {
  if (!cfg?.modules?.length) return;
  const byId = new Map(cfg.modules.map(m => [m.id, m]));
  const seen = new Set();
  const arranged = [];
  for (const id of order || []) {
    if (byId.has(id) && !seen.has(id)) { arranged.push(byId.get(id)); seen.add(id); }
  }
  for (const m of cfg.modules) {
    if (!seen.has(m.id)) { arranged.push(m); seen.add(m.id); }
  }
  cfg.modules = arranged;
}

function saveUiPreferences(patch) {
  clearTimeout(uiSaveTimer);
  uiSaveTimer = setTimeout(() => {
    apiJson('/api/preferences/ui', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(patch),
    }).catch(err => console.warn('Could not save UI preferences:', err));
  }, 120);
}

function persistTabOrder() {
  saveUiPreferences({tab_order: orderedModuleIds(), last_tab: activeModule});
}

function wireTabDragging() {
  const nav = $('moduleTabs');
  let dragged = null;
  nav.querySelectorAll('[data-module-tab]:not(:disabled)').forEach(btn => {
    btn.draggable = true;
    btn.title = 'Drag to reorder modules';
    btn.addEventListener('dragstart', ev => {
      dragged = btn;
      btn.classList.add('dragging');
      ev.dataTransfer.effectAllowed = 'move';
      ev.dataTransfer.setData('text/plain', btn.dataset.moduleTab);
    });
    btn.addEventListener('dragover', ev => {
      if (!dragged || dragged === btn) return;
      ev.preventDefault();
      ev.dataTransfer.dropEffect = 'move';
      nav.querySelectorAll('.dragTarget').forEach(x => x.classList.remove('dragTarget'));
      btn.classList.add('dragTarget');
      const rect = btn.getBoundingClientRect();
      const before = ev.clientX < rect.left + rect.width / 2;
      nav.insertBefore(dragged, before ? btn : btn.nextSibling);
    });
    btn.addEventListener('drop', ev => { ev.preventDefault(); });
    btn.addEventListener('dragend', () => {
      btn.classList.remove('dragging');
      nav.querySelectorAll('.dragTarget').forEach(x => x.classList.remove('dragTarget'));
      const order = [...nav.querySelectorAll('[data-module-tab]')].map(x => x.dataset.moduleTab);
      applyTabOrder(order);
      dragged = null;
      persistTabOrder();
    });
  });
}

function renderTabs() {
  $('moduleTabs').innerHTML = (cfg.modules || []).map(m => `<button type="button" class="moduleTab ${m.id === activeModule ? 'active' : ''}" data-module-tab="${esc(m.id)}" ${m.enabled ? 'draggable="true"' : 'disabled'}>${esc(m.label)}</button>`).join('');
  wireTabDragging();
}

function renderAllModules() {
  $('modulePanels').innerHTML = (cfg.modules || []).filter(m => m.enabled).map(m => renderModule(m.id)).join('');
  renderTabs();
  wireGlobalHelp();
  for (const m of cfg.modules.filter(x => x.enabled)) wireModule(m.id);
}

function wireGlobalHelp() {
  document.querySelectorAll('.helpButton').forEach(btn => {
    if (btn.dataset.helpReady === '1') return;
    btn.dataset.helpReady = '1';
    btn.addEventListener('click', ev => {
    ev.preventDefault(); ev.stopPropagation();
    const pop = document.getElementById(btn.dataset.help);
    if (!pop) return;
    const open = pop.classList.toggle('hidden') === false;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.querySelectorAll('.helpPopover').forEach(other => { if (other !== pop) other.classList.add('hidden'); });
    document.querySelectorAll('.helpButton').forEach(other => { if (other !== btn) other.setAttribute('aria-expanded', 'false'); });
    });
  });
}

document.addEventListener('click', ev => {
  if (!ev.target.closest('.helpButton') && !ev.target.closest('.helpPopover')) {
    document.querySelectorAll('.helpPopover').forEach(x => x.classList.add('hidden'));
    document.querySelectorAll('.helpButton').forEach(x => x.setAttribute('aria-expanded', 'false'));
  }
});

function setBoundValue(module, key, kind, el) {
  if (kind === 'boolean') formState[module][key] = Boolean(el.checked);
  else if (kind === 'number') formState[module][key] = el.value === '' ? null : Number(el.value);
  else if (kind === 'lines') formState[module][key] = lines(el.value);
  else if (kind === 'single-list') formState[module][key] = el.value.trim() ? [el.value.trim()] : [];
  else formState[module][key] = el.value;
  if (key === 'path_control_files') updateControlBadge(module);
  updateValidation(module);
}

function updateControlBadge(module) {
  const panel = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  const badge = panel?.querySelector('[data-control-badge]');
  if (badge) badge.textContent = formState[module].path_control_files ? 'Control vs Experience' : 'Experience only';
}

function addToken(module, field, raw) {
  let value = String(raw ?? '').trim();
  if (!value) return true;
  const choices = choicesFor(field);
  if (field.kind === 'number_tokens') {
    const n = Number(value);
    if (!Number.isFinite(n)) return false;
    value = n;
  } else if (!field.allow_custom && choices.length) {
    const canon = canonicalChoice(value, choices);
    if (canon === null) return false;
    value = canon;
  }
  const arr = Array.isArray(formState[module][field.key]) ? formState[module][field.key] : [];
  if (!arr.some(x => String(x).toLowerCase() === String(value).toLowerCase())) arr.push(value);
  formState[module][field.key] = arr;
  refreshTokenEditor(module, field);
  updateValidation(module);
  return true;
}

function refreshTokenEditor(module, field) {
  const root = document.querySelector(`[data-module="${CSS.escape(module)}"] [data-token-editor="${CSS.escape(field.key)}"]`);
  if (!root) return;
  const arr = Array.isArray(formState[module][field.key]) ? formState[module][field.key] : [];
  const disabled = comparisonFieldDisabled(module, field);
  root.querySelector('.tagList').innerHTML = arr.map((v, i) => `<span class="tag"><span class="tagText">${esc(v)}</span><button type="button" class="tagRemove" data-remove-token="${i}" aria-label="Remove ${esc(v)}"${disabled ? ' disabled' : ''}>×</button></span>`).join('');
  root.querySelectorAll('[data-remove-token]').forEach(btn => btn.addEventListener('click', () => {
    formState[module][field.key].splice(Number(btn.dataset.removeToken), 1);
    refreshTokenEditor(module, field); updateValidation(module);
  }));
}


function familyCatalogHtml(module, field, query, used) {
  const catalog = cfg?.family_catalog;
  if (!catalog?.stages?.length) return '';
  const q = String(query || '').trim().toLowerCase();
  const chunks = [];
  for (const stage of catalog.stages) {
    const stageMatches = !q || String(stage.label || stage.id || '').toLowerCase().includes(q);
    const rows = [];
    for (const group of stage.groups || []) {
      const values = (group.values || []).filter(v => !used.has(String(v).toLowerCase()));
      if (!values.length) continue;
      const haystack = [stage.label, stage.id, group.instrument, group.family, ...(group.suffixes || []), ...values].join(' ').toLowerCase();
      if (q && !stageMatches && !haystack.includes(q)) continue;
      const buttons = values.map(v => `<button type="button" class="suggestionButton familySuggestionButton" data-suggest="${esc(v)}"><span class="familyChoiceValue">${esc(v)}</span></button>`).join('');
      const suffixes = (group.suffixes || []).join(', ');
      rows.push(`<div class="familyCatalogRow"><div class="familyInstrument">${esc(group.instrument || group.family || '')}</div><div class="familyChoiceButtons">${buttons}</div>${suffixes ? `<div class="familySuffixes">Files: ${esc(suffixes)}</div>` : ''}</div>`);
    }
    if (rows.length) chunks.push(`<div class="familyStage"><div class="familyStageTitle">${esc(String(stage.label || stage.id || '').toUpperCase())}</div>${rows.join('')}</div>`);
  }
  const extras = (catalog.extras || []).filter(v => !used.has(String(v).toLowerCase()) && (!q || String(v).toLowerCase().includes(q)));
  if (extras.length) chunks.push(`<div class="familyStage"><div class="familyStageTitle">OTHER INSTALLED FAMILIES</div><div class="familyChoiceButtons familyExtras">${extras.map(v => `<button type="button" class="suggestionButton familySuggestionButton" data-suggest="${esc(v)}"><span class="familyChoiceValue">${esc(v)}</span></button>`).join('')}</div></div>`);
  return chunks.join('');
}

function showTokenSuggestions(module, field, input, box) {
  const choices = choicesFor(field);
  if (!choices.length || document.activeElement !== input) { box.classList.add('hidden'); box.innerHTML = ''; return; }
  const q = input.value.trim().toLowerCase();
  const used = new Set((formState[module][field.key] || []).map(x => String(x).toLowerCase()));

  if (field.source === 'families' && cfg?.family_catalog?.stages?.length) {
    const html = familyCatalogHtml(module, field, q, used);
    if (!html) { box.classList.add('hidden'); box.innerHTML = ''; return; }
    box.innerHTML = html;
  } else {
    const matches = choices.filter(v => !used.has(String(v).toLowerCase()) && (!q || String(v).toLowerCase().includes(q)));
    if (!matches.length) { box.classList.add('hidden'); box.innerHTML = ''; return; }
    box.innerHTML = matches.map(v => `<button type="button" class="suggestionButton" data-suggest="${esc(v)}">${esc(v)}</button>`).join('');
  }
  box.classList.remove('hidden');
  box.querySelectorAll('[data-suggest]').forEach(btn => btn.addEventListener('mousedown', ev => {
    ev.preventDefault(); addToken(module, field, btn.dataset.suggest); input.value = ''; box.classList.add('hidden'); input.focus();
  }));
}

function wireTokenEditor(module, field) {
  const root = document.querySelector(`[data-module="${CSS.escape(module)}"] [data-token-editor="${CSS.escape(field.key)}"]`);
  if (!root) return;
  const input = root.querySelector('[data-token-draft]');
  const box = root.querySelector('.suggestions');
  refreshTokenEditor(module, field);
  input.addEventListener('input', () => showTokenSuggestions(module, field, input, box));
  input.addEventListener('focus', () => showTokenSuggestions(module, field, input, box));
  input.addEventListener('keydown', ev => {
    const canSpaceCommit = field.kind === 'number_tokens' || (!field.allow_custom && choicesFor(field).length);
    if (ev.key === 'Enter' || ev.key === ',' || (ev.key === ' ' && canSpaceCommit)) {
      if (!input.value.trim()) return;
      ev.preventDefault();
      const ok = addToken(module, field, input.value);
      if (ok) { input.value = ''; box.classList.add('hidden'); }
      else setFieldError(module, field.key, `Unknown or invalid value: ${input.value.trim()}`);
    }
    if (ev.key === 'Backspace' && !input.value && (formState[module][field.key] || []).length) {
      formState[module][field.key].pop(); refreshTokenEditor(module, field); updateValidation(module);
    }
  });
  input.addEventListener('paste', ev => {
    const text = ev.clipboardData?.getData('text') || '';
    let parts = [];
    if (field.kind === 'number_tokens') parts = text.split(/[\s,]+/).filter(Boolean);
    else if (field.allow_custom) parts = text.split(/[\n,]+/).map(x => x.trim()).filter(Boolean);
    else parts = text.split(/[\s,]+/).filter(Boolean);
    if (parts.length > 1) {
      const allOk = parts.every(p => field.kind === 'number_tokens' ? Number.isFinite(Number(p)) : (field.allow_custom || canonicalChoice(p, choicesFor(field)) !== null));
      if (allOk) { ev.preventDefault(); parts.forEach(p => addToken(module, field, p)); input.value = ''; box.classList.add('hidden'); }
    }
  });
  input.addEventListener('blur', () => setTimeout(() => {
    if (input.value.trim()) {
      const ok = addToken(module, field, input.value);
      if (ok) input.value = '';
    }
    box.classList.add('hidden'); updateValidation(module);
  }, 120));
}

function wireModule(module) {
  const panel = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  const spec = cfg.module_specs[module];
  if (!panel) return;

  panel.querySelectorAll('[data-bind]').forEach(el => {
    const handler = () => setBoundValue(module, el.dataset.bind, el.dataset.kind || 'string', el);
    el.addEventListener('input', handler); el.addEventListener('change', handler);
  });
  spec.fields.filter(f => f.kind === 'tokens' || f.kind === 'number_tokens').forEach(f => wireTokenEditor(module, f));

  panel.querySelectorAll(`input[name="${module}ControlMode"]`).forEach(radio => radio.addEventListener('change', () => {
    formState[module]._control_mode = radio.value;
    rerenderModule(module);
  }));

  panel.querySelectorAll('[data-recent-exp]').forEach(btn => btn.addEventListener('click', () => {
    const path = btn.dataset.recentExp;
    const arr = formState[module].path_experience_files || [];
    if (spec.experience === 'one') formState[module].path_experience_files = [path];
    else if (!arr.includes(path)) arr.push(path);
    rerenderModule(module);
  }));

  panel.querySelector('[data-module-form]')?.addEventListener('submit', ev => requestReview(module, ev));
  panel.querySelector('[data-interactive-command]')?.addEventListener('click', () => showInteractiveCommand(module));
  panel.querySelector('[data-reset-module]')?.addEventListener('click', () => resetModule(module));
  updateValidation(module);
}

function rerenderModule(module) {
  const old = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  if (!old) return;
  const holder = document.createElement('div'); holder.innerHTML = renderModule(module).trim();
  old.replaceWith(holder.firstElementChild); wireGlobalHelp(); wireModule(module); switchModule(module);
}

function setFieldError(module, key, text = '') {
  const panel = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  const field = panel?.querySelector(`[data-field="${CSS.escape(key)}"]`);
  if (!field) return;
  field.classList.toggle('invalid', Boolean(text));
  const target = field.querySelector('.fieldError'); if (target) target.textContent = text;
}

function fieldMap(spec) {
  return Object.fromEntries(spec.fields.map(f => [f.key, f]));
}

function validateModule(module) {
  const spec = cfg.module_specs[module];
  const st = formState[module];
  const errors = {};
  const warnings = [];
  const add = (k, m) => { if (!errors[k]) errors[k] = m; };

  const mode = st._control_mode || 'control';
  if (spec.control === 'required') {
    if (!nonempty(st.path_control_files)) add('path_control_files', 'Control path is required.');
    if (!nonempty(st.control_name)) add('control_name', 'Control name is required.');
  } else if (spec.control === 'optional_mode' && mode === 'control') {
    if (!nonempty(st.path_control_files)) add('path_control_files', 'Enter a control path or choose Experience only.');
    if (!nonempty(st.control_name)) add('control_name', 'Control name is required in comparison mode.');
  } else if (spec.control === 'optional' && nonempty(st.path_control_files) && !nonempty(st.control_name)) add('control_name', 'Control name is required when a control path is used.');

  const expPaths = st.path_experience_files || [], expNames = st.experience_name || [];
  if (!expPaths.length) add('path_experience_files', 'At least one Experience path is required.');
  if (!expNames.length) add('experience_name', 'At least one Experience name is required.');
  if (expPaths.length !== expNames.length) {
    add('path_experience_files', 'Experience paths and names must have the same number of entries.');
    add('experience_name', 'Experience paths and names must have the same number of entries.');
  }
  if (spec.experience === 'one' && expPaths.length !== 1) add('path_experience_files', 'Exactly one Experience path is required.');
  if (!nonempty(st.pathwork)) add('pathwork', 'WORK PATH is required.');
  if (!/^\d{10}$/.test(st.datestart || '')) add('datestart', 'Use YYYYMMDDHH.');
  if (!/^\d{10}$/.test(st.dateend || '')) add('dateend', 'Use YYYYMMDDHH.');
  if (/^\d{10}$/.test(st.datestart || '') && /^\d{10}$/.test(st.dateend || '') && st.datestart > st.dateend) add('dateend', 'DATEEND must be after DATESTART.');

  const panel = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  for (const f of spec.fields) {
    if (f.comparison_only && spec.control === 'optional_mode' && mode === 'experience') continue;
    const value = st[f.key];
    if (f.kind === 'tokens' || f.kind === 'number_tokens') {
      const draft = panel?.querySelector(`[data-token-editor="${CSS.escape(f.key)}"] [data-token-draft]`)?.value.trim() || '';
      if (draft) {
        if (f.kind === 'number_tokens' && !Number.isFinite(Number(draft))) add(f.key, `Invalid numeric value: ${draft}`);
        else if (!f.allow_custom && choicesFor(f).length && canonicalChoice(draft, choicesFor(f)) === null) add(f.key, `Unknown value: ${draft}`);
        else add(f.key, 'Press Enter or choose a suggestion to add the typed value.');
      }
    }
    if ((f.kind === 'tokens' || f.kind === 'number_tokens') && f.required && (!Array.isArray(value) || !value.length)) add(f.key, `${f.label} requires at least one value.`);
    if (f.kind === 'tokens' && Array.isArray(value) && !f.allow_custom) {
      const choices = choicesFor(f).map(x => String(x).toLowerCase());
      const bad = value.filter(v => choices.length && !choices.includes(String(v).toLowerCase()));
      if (bad.length) add(f.key, `Unknown value: ${bad.join(', ')}`);
    }
    if (f.kind === 'number_tokens' && Array.isArray(value) && value.some(v => !Number.isFinite(Number(v)))) add(f.key, 'Use numeric values only.');
    if (f.kind === 'number') {
      const n = Number(value);
      if (!Number.isFinite(n)) add(f.key, 'A number is required.');
      else if (f.min !== undefined && n < Number(f.min)) add(f.key, `Minimum is ${f.min}.`);
      else if (f.max !== undefined && n > Number(f.max)) add(f.key, `Maximum is ${f.max}.`);
    }
    if (f.kind === 'select' && !choicesFor(f).map(String).includes(String(value))) add(f.key, 'Choose one of the available values.');
  }
  if (!Number.isInteger(Number(st.n_cpus)) || Number(st.n_cpus) < 1 || Number(st.n_cpus) > 256) add('n_cpus', 'N_CPUS must be an integer from 1 to 256.');

  if (module === 'mapobs' && String(st.dashboard_6h).toLowerCase() === 'on' && (st.family || []).some(x => ['iasi','cris'].includes(String(x).toLowerCase()))) {
    warnings.push('MAPOBS: 6-hour dashboards for interferometer/radiance families can create very large images and use substantial memory.');
  }
  return {errors, warnings};
}

function updateValidation(module) {
  const panel = document.querySelector(`[data-module="${CSS.escape(module)}"]`);
  if (!panel) return;
  panel.querySelectorAll('.field').forEach(f => { f.classList.remove('invalid'); const e=f.querySelector('.fieldError'); if(e)e.textContent=''; });
  const result = validateModule(module);
  Object.entries(result.errors).forEach(([k,m]) => setFieldError(module,k,m));
  const box = panel.querySelector('[data-validation-message]');
  const n = Object.keys(result.errors).length;
  if (n) { box.className='validationMessage invalid'; box.textContent=`Fix ${n} highlighted field${n===1?'':'s'} before running.`; }
  else { box.className='validationMessage valid'; box.textContent=interactiveBlocked ? 'Form is valid. Batch submission is blocked while an interactive PBS session is active.' : 'Ready to review.'; }
  const warn = panel.querySelector('[data-warning-box]');
  if (result.warnings.length) { warn.textContent=result.warnings.join('\n'); warn.classList.remove('hidden'); } else warn.classList.add('hidden');
  const run = panel.querySelector('[data-run-button]'); if (run) run.disabled = n > 0 || interactiveBlocked;
  return result;
}

function collectPayload(module) {
  const spec = cfg.module_specs[module];
  const out = clone(formState[module]);
  delete out._control_mode;
  if (spec.control === 'optional_mode' && formState[module]._control_mode === 'experience') {
    out.path_control_files = '';
    out.control_name = out.control_name || 'control';
    for (const f of spec.fields) {
      if (!f.comparison_only) continue;
      if (f.key === 'match') out[f.key] = 'off';
      else if (f.kind === 'select' && (f.choices || []).includes('off')) out[f.key] = 'off';
    }
  }
  if (spec.control === 'none') { delete out.path_control_files; delete out.control_name; }
  out.n_cpus = Number(out.n_cpus);
  for (const f of spec.fields) {
    if (f.kind === 'number') out[f.key] = Number(out[f.key]);
    if (f.kind === 'number_tokens') out[f.key] = (out[f.key] || []).map(Number);
  }
  return out;
}

function fmt(v) {
  if (Array.isArray(v)) return v.length ? v.join(', ') : '(none)';
  if (v === true) return 'yes'; if (v === false) return 'no';
  return nonempty(v) ? String(v) : '(none)';
}

function confirmationText(module, payload) {
  const spec = cfg.module_specs[module];
  const rows = [`Module: ${module.toUpperCase()}`];
  if (spec.control !== 'none') rows.push(`Control: ${payload.path_control_files ? `${payload.control_name} · ${payload.path_control_files}` : 'Experience only'}`);
  rows.push(`Experience path(s): ${fmt(payload.path_experience_files)}`);
  rows.push(`Experience name(s): ${fmt(payload.experience_name)}`);
  rows.push(`WORK PATH: ${payload.pathwork}`);
  rows.push(`Period: ${payload.datestart} → ${payload.dateend}`);
  rows.push(`Family: ${fmt(payload.family)}`);
  rows.push(`Region: ${fmt(payload.region)}`);
  if (payload.projection) rows.push(`Projection: ${fmt(payload.projection)}`);
  if (payload.flags_criteria !== undefined) rows.push(`FLAGS_CRITERIA: ${fmt(payload.flags_criteria)}`);
  const skip = new Set(['family','region','flags_criteria','projection','svg']);
  for (const f of spec.fields) {
    if (skip.has(f.key)) continue;
    if (f.comparison_only && spec.control === 'optional_mode' && !payload.path_control_files) continue;
    const v = payload[f.key];
    if (Array.isArray(v) && !v.length) continue;
    rows.push(`${f.label}: ${fmt(v)}`);
  }
  if (payload.svg !== undefined) rows.push(`SVG: ${fmt(payload.svg)}`);
  rows.push(`N_CPUS: ${payload.n_cpus}`);
  if (spec.pbs_note) rows.push(`PBS: ${spec.pbs_note}`);
  rows.push(`Publish viewer: ${payload.publish ? 'yes' : 'no'}`);
  return rows.join('\n');
}

function moduleMessage(module, text) {
  const el = document.querySelector(`[data-module="${CSS.escape(module)}"] [data-module-message]`);
  if (el) el.textContent = text;
}

function switchModule(module, {persist=true} = {}) {
  if (!cfg?.modules?.some(x => x.id === module && x.enabled)) return;
  activeModule = module;
  document.querySelectorAll('.modulePanel').forEach(p => p.classList.toggle('hidden', p.dataset.module !== module));
  document.querySelectorAll('[data-module-tab]').forEach(b => b.classList.toggle('active', b.dataset.moduleTab === module));
  updateValidation(module);
  if (persist) saveUiPreferences({last_tab: module});
}

async function loadConfig({preserveActive=true} = {}) {
  const previous = activeModule;
  cfg = await apiJson('/api/config');
  if (cfg.session?.version !== CLIENT_VERSION) console.warn(`Pikobs Web client ${CLIENT_VERSION}, server ${cfg.session?.version}`);
  defaultTabOrder = (cfg.modules || []).map(m => m.id);
  applyTabOrder(cfg.ui_preferences?.tab_order || []);
  $('session').textContent = `${cfg.session.user}@${cfg.session.host} · Web ${cfg.session.version}${cfg.scheduler?.ready ? ' · PBS ready' : ' · PBS unavailable'}`;
  fillDatalist('controlPathHistory', cfg.memory?.control || []);
  fillDatalist('pathworkHistory', cfg.memory?.pathwork || []);
  historySort = clone(cfg.ui_preferences?.history_sort || {key:'created_utc', dir:'desc'});
  historyColumnWidths = {...HISTORY_COLUMN_DEFAULTS, ...(cfg.ui_preferences?.history_column_widths || {})};
  formState = {};
  for (const m of cfg.modules.filter(x => x.enabled)) {
    formState[m.id] = clone(cfg.defaults[m.id] || {});
    if (cfg.module_specs[m.id]?.control === 'optional_mode') formState[m.id]._control_mode = formState[m.id].path_control_files ? 'control' : 'experience';
  }
  const savedLast = cfg.ui_preferences?.last_tab || '';
  if (preserveActive && cfg.modules.some(x => x.id === previous && x.enabled)) activeModule = previous;
  else if (cfg.modules.some(x => x.id === savedLast && x.enabled)) activeModule = savedLast;
  else activeModule = cfg.modules.find(x => x.enabled)?.id || 'vdedr';
  renderAllModules();
}

function fillDatalist(id, values) {
  $(id).innerHTML = uniq(values).map(v => `<option value="${esc(v)}"></option>`).join('');
}

async function checkInteractive() {
  const data = await apiJson('/api/interactive');
  interactiveBlocked = Boolean(data.jobs?.length);
  if (interactiveBlocked) {
    $('interactive').classList.remove('hidden');
    $('interactive').textContent = `Interactive PBS session detected (${data.jobs.map(j => j.job_id).join(', ')}). Close it before submitting a batch job. Interactive-command generation remains available.`;
  } else $('interactive').classList.add('hidden');
  for (const m of cfg.modules.filter(x => x.enabled)) updateValidation(m.id);
}

function requestReview(module, ev) {
  ev.preventDefault();
  const result = updateValidation(module);
  if (Object.keys(result.errors).length || interactiveBlocked) {
    moduleMessage(module, Object.keys(result.errors).length ? 'Cannot submit until the highlighted values are fixed.' : 'Cannot submit while an interactive PBS session is active.');
    return;
  }
  pendingPayload = collectPayload(module); pendingModule = module;
  $('confirmTitle').textContent = `Confirm ${module.toUpperCase()} submission`;
  $('confirmSummary').textContent = confirmationText(module, pendingPayload);
  $('confirmDialog').showModal();
}

async function showInteractiveCommand(module) {
  const result = updateValidation(module);
  if (Object.keys(result.errors).length) { moduleMessage(module, 'Fix the highlighted values before generating the command.'); return; }
  const payload = collectPayload(module);
  try {
    const data = await apiJson(`/api/modules/${module}/interactive-command`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    $('commandTitle').textContent = `${module.toUpperCase()} · interactive command`;
    $('interactiveCommand').textContent = data.command || '';
    $('commandDialog').showModal();
  } catch (e) { moduleMessage(module, `ERROR: ${e.message}`); }
}

async function doSubmit() {
  if (!pendingPayload || !pendingModule) return;
  const payload = pendingPayload, module = pendingModule;
  pendingPayload = null; pendingModule = null; $('confirmDialog').close();
  moduleMessage(module, 'Submitting…');
  try {
    const data = await apiJson(`/api/modules/${module}/jobs`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    moduleMessage(module, `Submitted PBS job ${data.job_id}\nRun: ${data.run_id}\nPATHWORK: ${data.pathwork}${payload.publish ? '\nPublic viewer link will appear when the viewer HTML is ready.' : ''}`);
    await refreshJobs();
  } catch (e) { moduleMessage(module, `ERROR: ${e.message}`); }
  finally { try { await checkInteractive(); } catch (_) { updateValidation(module); } }
}


async function refreshLiveOptions({rerender=false} = {}) {
  const data = await apiJson('/api/options');
  cfg.families = data.families || [];
  cfg.family_catalog = data.family_catalog || {stage_order:[], stages:[], extras:[]};
  cfg.regions = data.regions || [];
  cfg.flags_criteria = data.flags_criteria || [];
  cfg.projections = data.projections || [];
  cfg.options_meta = data.options_meta || {};
  if (rerender && activeModule) {
    rerenderModule(activeModule);
    switchModule(activeModule, {persist:false});
  }
  return data;
}

async function resetModule(module) {
  if (!confirm(`Reset saved ${module.toUpperCase()} settings to its wrapper defaults?\n\nRecent path history is kept.`)) return;
  try {
    const keep = clone(formState);
    await apiJson(`/api/preferences/reset/${module}`, {method:'POST'});
    const fresh = await apiJson('/api/config');
    cfg = fresh;
    for (const m of cfg.modules.filter(x => x.enabled)) {
      if (m.id !== module && keep[m.id]) formState[m.id] = keep[m.id];
    }
    formState[module] = clone(cfg.defaults[module] || {});
    if (cfg.module_specs[module]?.control === 'optional_mode') formState[module]._control_mode = formState[module].path_control_files ? 'control' : 'experience';
    fillDatalist('controlPathHistory', cfg.memory?.control || []);
    fillDatalist('pathworkHistory', cfg.memory?.pathwork || []);
  historySort = clone(cfg.ui_preferences?.history_sort || {key:'created_utc', dir:'desc'});
    rerenderModule(module); switchModule(module);
    moduleMessage(module, 'Reset to module defaults.');
  } catch (e) { moduleMessage(module, `ERROR: ${e.message}`); }
}

const FINAL_STATES = new Set(['COMPLETED','FAILED','CANCELLED','FINISHED_UNKNOWN','SUBMIT_FAILED']);
function isFinished(row) { return FINAL_STATES.has(String(row?.pbs?.state || '').toUpperCase()); }
function formatLaunched(value) {
  if (!value) return '-';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return String(value);
  return d.toLocaleString([], {year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit'});
}

function compactList(value, fallback='-') {
  const arr = Array.isArray(value) ? value : (nonempty(value) ? [value] : []);
  return arr.length ? arr.join(', ') : fallback;
}

function historyTooltip(row) {
  const p = row.pbs || {};
  const req = row.request || {};
  const lines = [
    `Module: ${String(row.module || '').toUpperCase()}`,
    `Launched: ${formatLaunched(row.created_utc)}`,
    `Run ID: ${row.run_id || '-'}`,
    `PBS job ID: ${row.job_id || '-'}`,
    `Status: ${p.state || '-'}`,
    `Node: ${p.node || '-'}`,
    `Walltime: ${p.walltime || '-'}`,
    `WORK PATH: ${row.pathwork || req.pathwork || '-'}`,
    '',
    'Run settings:'
  ];
  Object.keys(req).sort().forEach(key => {
    const value = req[key];
    lines.push(`${key}: ${Array.isArray(value) ? value.join(', ') : String(value ?? '')}`);
  });
  return lines.join('\n');
}

function activeJobRow(row) {
  const p = row.pbs || {}, state = p.state || '-';
  const viewer = row.viewer_ready && row.viewer_url ? `<a href="${esc(row.viewer_url)}" target="_blank" rel="noopener">${row.publish ? 'Public viewer' : 'Viewer'}</a>` : `<span class="muted">${row.publish ? 'Public viewer pending' : 'Viewer pending'}</span>`;
  return `<tr class="${row.hidden ? 'hiddenRun' : ''}"><td>${esc(String(row.module || '').toUpperCase())}</td><td>${esc(row.run_id)}</td><td>${esc(row.job_id || '-')}</td><td><span class="status status-${esc(String(state).toLowerCase())}">${esc(state)}</span></td><td>${esc(p.node || '-')}</td><td>${esc(p.walltime || '-')}</td><td><button class="linkButton logBtn" data-run="${esc(row.run_id)}" type="button">Log</button>${viewer}</td></tr>`;
}

const PROJECT_PALETTE = ['#2563eb','#16a34a','#d97706','#9333ea','#dc2626','#0891b2','#4f46e5','#be185d','#65a30d','#0f766e'];
const DEFAULT_RUN_COLOR = '#94a3b8';
function runHistoryColor(row) {
  const color = String(row?.history_color || '').trim().toLowerCase();
  return /^#[0-9a-f]{6}$/.test(color) ? color : DEFAULT_RUN_COLOR;
}
function projectCell(row) {
  const label = String(row.request?.project_label || '').trim();
  const shown = label || '—';
  return `<button type="button" class="projectInline" data-project-edit="${esc(row.run_id)}" data-project-old="${esc(label)}" title="Click to rename project">${esc(shown)}</button>`;
}
function runColorCell(row) {
  const color = runHistoryColor(row);
  return `<button type="button" class="runColorButton" data-run-color="${esc(row.run_id)}" title="Change row color" aria-label="Change row color"><span class="runColorSwatch" style="background:${esc(color)}"></span></button>`;
}
function historyValue(row, key) {
  const req = row.request || {}, p = row.pbs || {};
  if (key === 'created_utc') return new Date(row.created_utc || 0).getTime() || 0;
  if (key === 'module') return String(row.module || '').toUpperCase();
  if (key === 'project_label') return String(req.project_label || '');
  if (key === 'control') return String(req.control_name || (req.path_control_files ? 'control' : ''));
  if (key === 'experience') return compactList(req.experience_name, '');
  if (key === 'families') return compactList(req.family, '');
  if (key === 'period') return String(req.datestart || '');
  if (key === 'status') return String(p.state || '');
  return '';
}

function historyJobRow(row) {
  const p = row.pbs || {}, state = p.state || '-', req = row.request || {};
  const project = req.project_label || '-';
  const control = req.control_name || (req.path_control_files ? 'control' : '-');
  const experience = compactList(req.experience_name, 'experience');
  const families = compactList(req.family);
  const periodStart = req.datestart || '-';
  const periodEnd = req.dateend || '-';
  const tooltip = historyTooltip(row);
  const viewerAction = row.viewer_ready && row.viewer_url
    ? `<a class="historyAction primaryAction" href="${esc(row.viewer_url)}" target="_blank" rel="noopener">Viewer</a>`
    : (row.pathwork ? `<button class="historyAction outputBtn" data-path="${esc(row.pathwork)}" type="button">Output</button>` : '');
  const remove = !row.hidden ? `<button class="historyMenuAction removeBtn" data-run="${esc(row.run_id)}" type="button">Remove from History</button>` : '';
  const more = remove ? `<details class="historyMore"><summary aria-label="More actions" title="More actions">⋯</summary><div class="historyMoreMenu">${remove}</div></details>` : '';
  return `<tr class="${row.hidden ? 'hiddenRun' : ''}" style="--run-row-color:${esc(runHistoryColor(row))}">
    <td class="runColorCell">${runColorCell(row)}</td>
    <td>${esc(formatLaunched(row.created_utc))}</td>
    <td>${esc(String(row.module || '').toUpperCase())}</td>
    <td class="historyProject">${projectCell(row)}</td>
    <td>${esc(control)}</td>
    <td><span class="historyExperience" title="${esc(tooltip)}">${esc(experience)}</span></td>
    <td class="historyFamilies" title="${esc(families)}">${esc(families)}</td>
    <td class="historyPeriod"><span>${esc(periodStart)}</span><span>${esc(periodEnd)}</span></td>
    <td><span class="status status-${esc(String(state).toLowerCase())}">${esc(state)}</span></td>
    <td class="historyActionsCell"><div class="historyActions">${viewerAction}<button class="historyAction logBtn" data-run="${esc(row.run_id)}" type="button">Log</button><button class="historyAction rerunBtn" data-run="${esc(row.run_id)}" type="button">Reuse</button>${more}</div></td>
  </tr>`;
}
function emptyRow(text, colspan=7) { return `<tr><td colspan="${colspan}" class="emptyState">${esc(text)}</td></tr>`; }

function setSelectOptions(id, values, current, allLabel) {
  const el = $(id); if (!el) return;
  const unique = uniq(values.filter(nonempty)).sort((a,b) => String(a).localeCompare(String(b), undefined, {numeric:true, sensitivity:'base'}));
  el.innerHTML = `<option value="">${esc(allLabel)}</option>` + unique.map(v => `<option value="${esc(v)}" ${String(v)===String(current)?'selected':''}>${esc(v)}</option>`).join('');
}

function syncHistoryFilterOptions(rows) {
  setSelectOptions('historyModuleFilter', rows.map(r => String(r.module || '').toUpperCase()), historyFilters.module, 'All modules');
  setSelectOptions('historyProjectFilter', rows.map(r => String(r.request?.project_label || '')), historyFilters.project, 'All projects');
  setSelectOptions('historyStatusFilter', rows.map(r => String(r.pbs?.state || '')), historyFilters.status, 'All statuses');
}

function filteredSortedHistoryRows() {
  const q = historyFilters.search.trim().toLowerCase();
  let rows = historyRowsCache.filter(row => {
    const req = row.request || {}, p = row.pbs || {};
    if (historyFilters.module && String(row.module || '').toUpperCase() !== historyFilters.module) return false;
    if (historyFilters.project && String(req.project_label || '') !== historyFilters.project) return false;
    if (historyFilters.status && String(p.state || '') !== historyFilters.status) return false;
    if (q) {
      const haystack = [
        row.module, req.project_label, req.control_name, req.path_control_files,
        ...(req.experience_name || []), ...(req.path_experience_files || []),
        ...(req.family || []), req.datestart, req.dateend, row.pathwork,
        p.state, p.node, row.run_id, row.job_id,
      ].map(x => String(x ?? '')).join(' ').toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });
  const direction = historySort.dir === 'asc' ? 1 : -1;
  const collator = new Intl.Collator(undefined, {numeric:true, sensitivity:'base'});
  rows = rows.map((row, i) => ({row, i})).sort((a,b) => {
    const av = historyValue(a.row, historySort.key), bv = historyValue(b.row, historySort.key);
    let cmp = 0;
    if (typeof av === 'number' && typeof bv === 'number') cmp = av - bv;
    else cmp = collator.compare(String(av), String(bv));
    return cmp ? cmp * direction : a.i - b.i;
  }).map(x => x.row);
  return rows;
}

function updateSortHeaders() {
  document.querySelectorAll('[data-history-sort]').forEach(btn => {
    const active = btn.dataset.historySort === historySort.key;
    btn.classList.toggle('active', active);
    btn.querySelector('.sortMark').textContent = active ? (historySort.dir === 'asc' ? '↑' : '↓') : '↕';
    btn.setAttribute('aria-sort', active ? (historySort.dir === 'asc' ? 'ascending' : 'descending') : 'none');
  });
}

function applyHistoryColumnWidths() {
  const table = $('historyTable');
  if (!table) return;
  table.querySelectorAll('col[data-history-col]').forEach(col => {
    const key = col.dataset.historyCol;
    const min = HISTORY_COLUMN_MIN[key] || 80;
    const raw = Number(historyColumnWidths[key] ?? HISTORY_COLUMN_DEFAULTS[key] ?? min);
    const width = Math.max(min, Math.round(raw));
    col.style.width = `${width}px`;
  });
}

function resetHistoryColumnWidths() {
  historyColumnWidths = {...HISTORY_COLUMN_DEFAULTS};
  applyHistoryColumnWidths();
  saveUiPreferences({history_column_widths: historyColumnWidths});
}

function wireHistoryColumnResizers() {
  document.querySelectorAll('#historyTable th[data-history-col] .historyResizeHandle').forEach(handle => {
    handle.addEventListener('pointerdown', ev => {
      ev.preventDefault();
      ev.stopPropagation();
      const th = handle.closest('th[data-history-col]');
      const key = th?.dataset.historyCol;
      if (!key) return;
      const startX = ev.clientX;
      const startWidth = th.getBoundingClientRect().width;
      const min = HISTORY_COLUMN_MIN[key] || 80;
      handle.setPointerCapture?.(ev.pointerId);
      document.body.classList.add('historyResizing');
      const move = e => {
        const next = Math.max(min, Math.round(startWidth + e.clientX - startX));
        historyColumnWidths[key] = next;
        applyHistoryColumnWidths();
      };
      const up = e => {
        handle.removeEventListener('pointermove', move);
        handle.removeEventListener('pointerup', up);
        handle.removeEventListener('pointercancel', up);
        document.body.classList.remove('historyResizing');
        saveUiPreferences({history_column_widths: historyColumnWidths});
      };
      handle.addEventListener('pointermove', move);
      handle.addEventListener('pointerup', up);
      handle.addEventListener('pointercancel', up);
    });
    handle.addEventListener('dblclick', ev => {
      ev.preventDefault(); ev.stopPropagation();
      const key = handle.closest('th[data-history-col]')?.dataset.historyCol;
      if (!key) return;
      historyColumnWidths[key] = HISTORY_COLUMN_DEFAULTS[key];
      applyHistoryColumnWidths();
      saveUiPreferences({history_column_widths: historyColumnWidths});
    });
  });
}

function wireHistoryRows() {
  document.querySelectorAll('#historyJobs .logBtn').forEach(b => b.addEventListener('click', () => openLog(b.dataset.run)));
  document.querySelectorAll('#historyJobs .rerunBtn').forEach(b => b.addEventListener('click', () => runAgain(b.dataset.run)));
  document.querySelectorAll('#historyJobs .removeBtn').forEach(b => b.addEventListener('click', () => removeRunFromHistory(b.dataset.run)));
  document.querySelectorAll('#historyJobs .outputBtn').forEach(b => b.addEventListener('click', async () => { const path=b.dataset.path||''; try { await navigator.clipboard.writeText(path); const old=b.textContent; b.textContent='Copied'; setTimeout(()=>{ if (b.isConnected) b.textContent=old; },900); } catch (_) { window.prompt('WORK PATH', path); } }));
  document.querySelectorAll('#historyJobs [data-project-edit]').forEach(b => b.addEventListener('click', () => beginProjectRename(b)));
  document.querySelectorAll('#historyJobs [data-run-color]').forEach(b => b.addEventListener('click', () => beginRunColor(b)));
}
async function renameProject(runId, oldLabel, newLabel) {
  return apiJson('/api/projects/rename', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({run_id:runId, old_label:oldLabel, new_label:newLabel})});
}

function applyProjectLabelLocal(runId, oldLabel, newLabel) {
  const changed = [];
  historyRowsCache.forEach(row => {
    const current = String(row.request?.project_label || '').trim();
    const sameProject = oldLabel ? current === oldLabel : String(row.run_id || '') === runId;
    if (!sameProject) return;
    row.request = {...(row.request || {}), project_label:newLabel};
    changed.push(String(row.run_id || ''));
  });
  return changed;
}

function setProjectLabelForRuns(runIds, label) {
  const wanted = new Set(runIds || []);
  historyRowsCache.forEach(row => {
    if (!wanted.has(String(row.run_id || ''))) return;
    row.request = {...(row.request || {}), project_label:label};
  });
}

function beginProjectRename(button) {
  if (projectEditState) return;
  const runId = button.dataset.projectEdit || '';
  const oldLabel = button.dataset.projectOld || '';
  const input = document.createElement('input');
  input.type = 'text';
  input.className = 'projectInlineInput';
  input.value = oldLabel;
  input.placeholder = 'Project / Label';
  input.autocomplete = 'off';
  input.spellcheck = false;
  projectEditState = {runId, oldLabel};
  button.replaceWith(input);
  input.focus({preventScroll:true});
  const end = input.value.length;
  try { input.setSelectionRange(end, end); } catch (_) {}

  let done = false;
  const commit = () => {
    if (done) return;
    done = true;
    const value = input.value.trim();
    projectEditState = null;

    // Update the UI immediately. Saving to FastAPI is intentionally detached
    // from the editor so Enter/blur never waits on network or disk I/O.
    const changedRunIds = value !== oldLabel ? applyProjectLabelLocal(runId, oldLabel, value) : [];
    syncHistoryFilterOptions(historyRowsCache);
    renderHistory();
    if (value === oldLabel) return;

    historyMutationPending += 1;
    renameProject(runId, oldLabel, value)
      .catch(e => {
        setProjectLabelForRuns(changedRunIds, oldLabel);
        syncHistoryFilterOptions(historyRowsCache);
        renderHistory();
        alert(`Project rename failed: ${e.message}`);
      })
      .finally(() => { historyMutationPending = Math.max(0, historyMutationPending - 1); });
  };

  const cancel = () => {
    if (done) return;
    done = true;
    projectEditState = null;
    renderHistory();
  };

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); commit(); }
    else if (e.key === 'Escape') { e.preventDefault(); cancel(); }
  });
  input.addEventListener('blur', commit, {once:true});
}

function closeProjectPalette() {
  document.querySelectorAll('.projectPalette').forEach(p => p.remove());
}
function beginRunColor(button) {
  const runId = button.dataset.runColor || '';
  if (!runId) return;
  const rowData = historyRowsCache.find(r => String(r.run_id || '') === runId);
  const currentColor = runHistoryColor(rowData || {});

  const existing = document.querySelector('.projectPalette');
  if (existing) { existing.remove(); return; }

  const palette = document.createElement('div');
  palette.className = 'projectPalette';
  palette.setAttribute('role', 'dialog');
  palette.setAttribute('aria-label', 'Choose row color');

  PROJECT_PALETTE.forEach(color => {
    const c = document.createElement('button');
    c.type = 'button';
    c.className = 'projectPaletteChoice';
    c.style.background = color;
    c.title = `Use ${color}`;
    if (currentColor.toLowerCase() === color.toLowerCase()) c.classList.add('selected');
    c.addEventListener('click', ev => {
      ev.stopPropagation();
      const previous = currentColor;
      const local = historyRowsCache.find(r => String(r.run_id || '') === runId);
      if (local) local.history_color = color;
      closeProjectPalette();
      renderHistory();

      historyMutationPending += 1;
      apiJson(`/api/runs/${encodeURIComponent(runId)}/color`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({color})})
        .catch(e => {
          const rollback = historyRowsCache.find(r => String(r.run_id || '') === runId);
          if (rollback) rollback.history_color = previous;
          renderHistory();
          alert(`Row color failed: ${e.message}`);
        })
        .finally(() => { historyMutationPending = Math.max(0, historyMutationPending - 1); });
    });
    palette.appendChild(c);
  });

  document.body.appendChild(palette);
  const r = button.getBoundingClientRect();
  const gap = 8;
  const pw = Math.min(360, window.innerWidth - 24);
  palette.style.width = `${pw}px`;
  let left = r.left;
  if (left + pw > window.innerWidth - 12) left = window.innerWidth - pw - 12;
  left = Math.max(12, left);
  palette.style.left = `${left}px`;
  palette.style.top = `${Math.min(window.innerHeight - palette.offsetHeight - 12, r.bottom + gap)}px`;

  const onOutside = ev => {
    if (!palette.contains(ev.target) && ev.target !== button && !button.contains(ev.target)) {
      closeProjectPalette();
      document.removeEventListener('pointerdown', onOutside, true);
    }
  };
  setTimeout(() => document.addEventListener('pointerdown', onOutside, true), 0);
}


function renderHistory() {
  const rows = filteredSortedHistoryRows();
  $('historyCount').textContent = rows.length === historyRowsCache.length ? rows.length : `${rows.length}/${historyRowsCache.length}`;
  $('historyJobs').innerHTML = rows.length ? rows.map(historyJobRow).join('') : emptyRow('No runs match the current History filters.', 10);
  updateSortHeaders();
  wireHistoryRows();
}

async function refreshJobs() {
  const data = await apiJson(`/api/runs?include_hidden=${showHiddenRuns ? 'true' : 'false'}`), rows = data.runs || [];
  const active = rows.filter(r => !isFinished(r));
  const remoteHistory = rows.filter(isFinished);
  $('activeCount').textContent = active.length;
  $('jobs').innerHTML = active.length ? active.map(activeJobRow).join('') : emptyRow('No active jobs.', 7);
  document.querySelectorAll('#jobs .logBtn').forEach(b => b.addEventListener('click', () => openLog(b.dataset.run)));
  $('showHidden').textContent = showHiddenRuns ? 'Hide hidden' : `Show hidden${data.hidden_count ? ` (${data.hidden_count})` : ''}`;

  // History is polled every 10 s for PBS state changes. Never rebuild the
  // History table while a project label is being edited: replacing the row
  // would steal focus and discard partially typed text. We still refresh the
  // cache and active-job panel; History is repainted as soon as editing ends.
  const editingProject = !!projectEditState || document.activeElement?.classList?.contains('projectInlineInput');
  const colorOpen = !!document.querySelector('.projectPalette');
  const historyBusy = editingProject || colorOpen || historyMutationPending > 0;
  if (!historyBusy) {
    historyRowsCache = remoteHistory;
    syncHistoryFilterOptions(historyRowsCache);
    renderHistory();
  }
}

async function runAgain(runId) {
  try {
    const data = await apiJson(`/api/runs/${runId}`);
    const module = String(data.module || '').toLowerCase();
    if (!cfg.module_specs[module] || !data.request) throw new Error('This run does not contain reusable settings.');
    formState[module] = {...clone(cfg.defaults[module]), ...clone(data.request)};
    formState[module].project_label = ''; // Project metadata is assigned only from History.
    if (cfg.module_specs[module].control === 'optional_mode') formState[module]._control_mode = formState[module].path_control_files ? 'control' : 'experience';
    rerenderModule(module); switchModule(module); window.scrollTo({top:0, behavior:'smooth'});
    moduleMessage(module, `Loaded settings from ${runId}. Review them before submitting.`);
  } catch (e) { moduleMessage(activeModule, `ERROR: ${e.message}`); }
}

async function removeRunFromHistory(runId) {
  if (!confirm(`Remove ${runId} from Pikobs Web history?\n\nResults, logs and viewer files will NOT be deleted.`)) return;
  await apiJson(`/api/runs/${runId}/hide`, {method:'POST'}); await refreshJobs();
}
async function clearHistory() {
  if (!confirm('Clear all finished runs from Pikobs Web history?\n\nResults, logs and viewer files will NOT be deleted.')) return;
  await apiJson('/api/history/clear', {method:'POST'}); showHiddenRuns=false; await refreshJobs();
}

async function fetchLog() {
  if (!activeLogRun || logPaused) return;
  const data = await apiJson(`/api/runs/${activeLogRun}/log?lines=500`);
  const pre = $('log'); pre.textContent = data.exists ? data.text : '(log not created yet)'; pre.scrollTop = pre.scrollHeight;
}
async function openLog(runId) {
  activeLogRun = runId; logPaused=false; $('pauseLog').textContent='Pause'; $('logTitle').textContent=`Log · ${runId}`; $('logMeta').textContent='Live refresh'; $('logCard').classList.remove('hidden');
  await fetchLog(); clearInterval(logTimer); logTimer=setInterval(() => fetchLog().catch(()=>{}), 1200); $('logCard').scrollIntoView({behavior:'smooth', block:'start'});
}

document.querySelectorAll('[data-history-sort]').forEach(btn => btn.addEventListener('click', () => {
  const key = btn.dataset.historySort;
  historySort = historySort.key === key ? {key, dir: historySort.dir === 'asc' ? 'desc' : 'asc'} : {key, dir: key === 'created_utc' ? 'desc' : 'asc'};
  saveUiPreferences({history_sort: historySort});
  renderHistory();
}));
wireHistoryColumnResizers();
applyHistoryColumnWidths();
$('historyResetColumns').addEventListener('click', resetHistoryColumnWidths);
$('historyModuleFilter').addEventListener('change', ev => { historyFilters.module = ev.target.value; renderHistory(); });
$('historyProjectFilter').addEventListener('change', ev => { historyFilters.project = ev.target.value; renderHistory(); });
$('historyStatusFilter').addEventListener('change', ev => { historyFilters.status = ev.target.value; renderHistory(); });
$('historySearch').addEventListener('input', ev => { historyFilters.search = ev.target.value; renderHistory(); });
$('historyClearFilters').addEventListener('click', () => {
  historyFilters = {module:'', project:'', status:'', search:''};
  $('historySearch').value = '';
  syncHistoryFilterOptions(historyRowsCache);
  renderHistory();
});

$('moduleTabs').addEventListener('click', ev => { const b=ev.target.closest('[data-module-tab]'); if(b)switchModule(b.dataset.moduleTab); });
$('resetTabOrder').addEventListener('click', () => {
  applyTabOrder(defaultTabOrder);
  renderTabs();
  persistTabOrder();
});
$('refresh').addEventListener('click', async () => { try { await refreshJobs(); await checkInteractive(); } catch(e){ moduleMessage(activeModule,`ERROR: ${e.message}`); } });
$('toggleHistory').addEventListener('click', () => { const wrap=$('historyWrap'), hidden=wrap.classList.toggle('hidden'); $('toggleHistory').textContent=hidden?'Show history':'Hide history'; });
$('showHidden').addEventListener('click', async () => { showHiddenRuns=!showHiddenRuns; $('historyWrap').classList.remove('hidden'); $('toggleHistory').textContent='Hide history'; await refreshJobs(); });
$('clearHistory').addEventListener('click', () => clearHistory().catch(e => moduleMessage(activeModule,`ERROR: ${e.message}`)));
$('closeLog').addEventListener('click', () => { activeLogRun=null; clearInterval(logTimer); $('logCard').classList.add('hidden'); });
$('pauseLog').addEventListener('click', () => { logPaused=!logPaused; $('pauseLog').textContent=logPaused?'Resume':'Pause'; $('logMeta').textContent=logPaused?'Refresh paused':'Live refresh'; if(!logPaused)fetchLog().catch(()=>{}); });
$('cancelConfirm').addEventListener('click', () => { pendingPayload=null; pendingModule=null; $('confirmDialog').close(); });
$('confirmRun').addEventListener('click', doSubmit);
$('closeCommand').addEventListener('click', () => $('commandDialog').close());
$('copyCommand').addEventListener('click', async () => {
  const text=$('interactiveCommand').textContent;
  try { await navigator.clipboard.writeText(text); $('copyCommand').textContent='Copied'; setTimeout(()=>$('copyCommand').textContent='Copy command',1200); }
  catch (_) { window.prompt('Copy this command:', text); }
});


let lastOptionsRefresh = Date.now();
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'visible') return;
  if (Date.now() - lastOptionsRefresh < 60000) return;
  lastOptionsRefresh = Date.now();
  refreshLiveOptions({rerender:false}).catch(err => console.warn('Could not refresh Pikobs options:', err));
});

(async function init(){
  try {
    await loadConfig({preserveActive:false}); await checkInteractive(); await refreshJobs(); switchModule(activeModule, {persist:false});
    setInterval(() => refreshJobs().catch(()=>{}), 10000);
  } catch(e) {
    $('modulePanels').innerHTML = `<section class="card"><h2>Pikobs Web could not start</h2><pre>${esc(e.message)}</pre></section>`;
  }
})();
