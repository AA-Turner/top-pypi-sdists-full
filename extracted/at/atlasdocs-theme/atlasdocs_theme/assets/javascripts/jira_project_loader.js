/**
 * Lazy-loads a <project>.json (Jira REST API v2 format) and renders
 * a filterable, sortable issue table with sparkline chart, search bar,
 * and download options (.txt / .csv / .json).
 *
 * Usage in a .md file body:
 *
 *   <div id="jira-project"
 *        data-json="./ATLASDOC.json"
 *        data-project="ATLASDOC"
 *        data-jira-base="https://its.cern.ch/jira"></div>
 *   <script src="path/to/jira_project_loader.js"></script>
 */
(function () {

  // ---------------------------------------------------------------------------
  // Icons
  // ---------------------------------------------------------------------------

  const ICONS = {
    externalLink: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide" viewBox="0 0 24 24"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path></svg>`,
    squareArrow:  `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide" viewBox="0 0 24 24"><path d="M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6M21 3l-9 9M15 3h6v6"></path></svg>`,
    dlTxt:        `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide" viewBox="0 0 24 24"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M12 18v-6m-3 3 3 3 3-3"/></svg>`,
    dlCsv:        `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide" viewBox="0 0 24 24"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M8 13h2.5a1.5 1.5 0 0 1 0 3H8v-3ZM14 13h2"/><path d="M14 16h2"/></svg>`,
    dlJson:       `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="lucide" viewBox="0 0 24 24"><path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/></svg>`,
  };

  function ic(key) { return `<span class="twemoji">${ICONS[key]}</span>`; }

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function fmtDate(iso) { return iso ? iso.slice(0, 10) : '—'; }

  function extractTwikiUrl(description) {
    if (!description) return null;
    const m = description.match(/https:\/\/twiki\.cern\.ch\/[^\s\]\[<"]+/);
    return m ? m[0] : null;
  }

  function csvCell(val) {
    const s = String(val ?? '');
    return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  }

  const STATUS_COLOURS = {
    'Open': 'blue', 'In Progress': 'yellow',
    'Done': 'green', 'Resolved': 'green', 'Closed': 'green',
  };

  function statusLabel(name) {
    const cls = STATUS_COLOURS[name] || 'blue';
    return `<span class="atlaslabel ${cls}">${escapeHtml(name || 'Unknown')}</span>`;
  }

  // ---------------------------------------------------------------------------
  // Table
  // ---------------------------------------------------------------------------

  const SORT_COLS = [
    { key: 'key',      label: 'Ticket'    },
    { key: 'summary',  label: 'Summary'   },
    { key: 'created',  label: 'Opened'    },
    { key: 'assignee', label: 'Assignee'  },
    { key: 'comments', label: 'Comments'  },
    { key: 'updated',  label: 'Last Edit' },
  ];

  const COLGROUP = `<colgroup>`
    + `<col style="width:9%">`
    + `<col style="width:30%">`
    + `<col style="width:8%">`
    + `<col style="width:18%">`
    + `<col style="width:5%">`
    + `<col style="width:8%">`
    + `<col style="width:5%">`
    + `<col style="width:9%">`
    + `</colgroup>`;

  function buildThead(sortKey, sortDir) {
    const thFor = (col) => {
      const active = col.key === sortKey;
      const ariaSort = active ? (sortDir === 1 ? 'ascending' : 'descending') : 'none';
      return `<th data-sort="${col.key}" aria-sort="${ariaSort}">${col.label}</th>`;
    };
    const sortableThs = SORT_COLS.map(thFor).join('');
    return `<thead><tr>${sortableThs}<th>Twiki</th><th>Status</th></tr></thead>`;
  }

  function issueVal(issue, key) {
    const f = issue.fields;
    switch (key) {
      case 'key':      return parseInt(issue.key.split('-')[1]) || 0;
      case 'summary':  return (f.summary || '').toLowerCase();
      case 'created':  return f.created || '';
      case 'updated':  return f.updated || '';
      case 'assignee': return f.assignee ? f.assignee.displayName.toLowerCase() : '';
      case 'comments': return f.comment ? (f.comment.total ?? f.comment.comments.length) : 0;
      default:         return '';
    }
  }

  function sortIssues(issues, sortKey, sortDir) {
    return [...issues].sort((a, b) => {
      const av = issueVal(a, sortKey), bv = issueVal(b, sortKey);
      if (typeof av === 'number') return sortDir * (av - bv);
      return sortDir * String(av).localeCompare(String(bv));
    });
  }

  function renderRow(issue, jiraBase) {
    const f        = issue.fields;
    const twikiUrl = extractTwikiUrl(f.description);
    return `<tr>`
      + `<td><a href="${jiraBase}/browse/${issue.key}">${issue.key}</a></td>`
      + `<td>${escapeHtml(f.summary || '')}</td>`
      + `<td>${fmtDate(f.created)}</td>`
      + `<td>${escapeHtml(f.assignee ? f.assignee.displayName : '—')}</td>`
      + `<td>${f.comment ? (f.comment.total ?? f.comment.comments.length) : 0}</td>`
      + `<td>${fmtDate(f.updated)}</td>`
      + `<td>${twikiUrl ? `<a href="${twikiUrl}">${ic('squareArrow')}</a>` : '—'}</td>`
      + `<td>${statusLabel(f.status ? f.status.name : null)}</td>`
      + `</tr>`;
  }

  function buildTable(issues, jiraBase, sortKey, sortDir) {
    const sorted = sortIssues(issues, sortKey, sortDir);
    const tbody = sorted.length
      ? sorted.map(i => renderRow(i, jiraBase)).join('')
      : `<tr><td colspan="8" style="text-align:center;opacity:0.5"><em>No tickets match.</em></td></tr>`;
    return `<div class="md-typeset__scrollwrap"><div class="md-typeset__table">`
      + `<table style="table-layout:fixed;width:100%">`
      + COLGROUP + buildThead(sortKey, sortDir)
      + `<tbody>${tbody}</tbody>`
      + `</table></div></div>`;
  }

  // ---------------------------------------------------------------------------
  // Downloads
  // ---------------------------------------------------------------------------

  function triggerDownload(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url  = URL.createObjectURL(blob);
    const a    = Object.assign(document.createElement('a'), { href: url, download: filename });
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function downloadTxt(issues, project) {
    const lines = issues.map(i => {
      const f = i.fields;
      return [
        i.key,
        f.summary || '',
        f.status ? f.status.name : '',
        f.assignee ? f.assignee.displayName : '',
      ].join(' | ');
    });
    triggerDownload(`${project}.txt`, lines.join('\n'), 'text/plain');
  }

  function downloadCsv(issues, project) {
    const header = ['Key', 'Summary', 'Status', 'Assignee', 'Opened', 'Last Edit', 'Comments'];
    const rows = issues.map(i => {
      const f = i.fields;
      return [
        i.key,
        f.summary || '',
        f.status ? f.status.name : '',
        f.assignee ? f.assignee.displayName : '',
        fmtDate(f.created),
        fmtDate(f.updated),
        f.comment ? (f.comment.total ?? f.comment.comments.length) : 0,
      ].map(csvCell).join(',');
    });
    triggerDownload(`${project}.csv`, [header.join(','), ...rows].join('\r\n'), 'text/csv');
  }

  function downloadJson(issues, project) {
    triggerDownload(`${project}.json`, JSON.stringify(issues, null, 2), 'application/json');
  }

  // ---------------------------------------------------------------------------
  // Toolbar
  // ---------------------------------------------------------------------------

  function buildToolbar(jiraBase, project) {
    const projectUrl = `${jiraBase}/projects/${project}`;
    const el = document.createElement('div');
    el.className = 'indico-toolbar';
    el.innerHTML =
      `<div class="indico-toolbar-row">`
      + `<input class="indico-search-input" type="search" placeholder="Search tickets, summaries, assignees…" aria-label="Search Jira tickets" style="flex:1">`
      + `<a class="md-button md-button--primary" href="${projectUrl}" target="_blank" rel="noopener noreferrer">${ic('externalLink')} ${escapeHtml(project)}</a>`
      + `<div class="indico-toolbar-actions">`
      + `<button class="md-content__button" data-action="dl-txt"  title="Download as .txt">${ICONS.dlTxt}</button>`
      + `<button class="md-content__button" data-action="dl-csv"  title="Download as .csv">${ICONS.dlCsv}</button>`
      + `<button class="md-content__button" data-action="dl-json" title="Download as .json">${ICONS.dlJson}</button>`
      + `</div>`
      + `</div>`
      + `<span class="indico-search-count" style="display:block;min-height:1.4rem"></span>`;
    return el;
  }

  // ---------------------------------------------------------------------------
  // Filter + render
  // ---------------------------------------------------------------------------

  function matchesQuery(issue, query) {
    if (!query) return true;
    const f   = issue.fields;
    const hay = [
      issue.key,
      f.summary || '',
      f.assignee ? f.assignee.displayName : '',
      f.status   ? f.status.name          : '',
    ].join(' ').toLowerCase();
    return hay.includes(query);
  }

  function applyFilters(state) {
    const { issues, jiraBase, query, sortKey, sortDir, firstYear, countEl, summaryEl, tableEl } = state;

    const filtered = issues.filter(i => matchesQuery(i, query));

    const isFiltered = filtered.length !== issues.length;
    const open   = filtered.filter(i => i.fields.resolution === null).length;
    const closed  = filtered.length - open;

    countEl.textContent = query
      ? `${filtered.length} result${filtered.length !== 1 ? 's' : ''} for "${query}"`
      : isFiltered
        ? `${filtered.length} of ${issues.length} tickets`
        : '';

    const nDigits = String(issues.length).length;
    const num = (n) =>
      `<span style="display:inline-block;min-width:${nDigits}ch;text-align:right;font-variant-numeric:tabular-nums">${n}</span>`;
    summaryEl.innerHTML =
      `Since ${firstYear} · ${num(filtered.length)} of ${num(issues.length)} tickets · ${num(open)} open · ${num(closed)} completed`;

    tableEl.innerHTML = buildTable(filtered, jiraBase, sortKey, sortDir);
    return filtered;
  }

  // ---------------------------------------------------------------------------
  // Main render
  // ---------------------------------------------------------------------------

  function renderAll(container, issues) {
    const project  = container.dataset.project  || 'JIRA';
    const jiraBase = container.dataset.jiraBase || 'https://its.cern.ch/jira';

    const firstYear = Math.min(...issues.map(i => parseInt(i.fields.created.slice(0, 4))));

    // Insert toolbar before container
    const toolbar = buildToolbar(jiraBase, project);
    container.parentNode.insertBefore(toolbar, container);
    const searchInput = toolbar.querySelector('input');
    const countEl     = toolbar.querySelector('.indico-search-count');

    container.innerHTML =
      `<p id="jira-summary" style="text-align:center;font-size:0.82em;opacity:0.6;margin:0 0 1.2em;white-space:nowrap"></p>`
      + `<div id="jira-table"></div>`;

    const state = {
      issues, jiraBase, project, firstYear,
      query: '',
      sortKey: 'key',
      sortDir: -1,
      countEl,
      summaryEl: container.querySelector('#jira-summary'),
      tableEl: container.querySelector('#jira-table'),
    };

    // RAF-gated render — batches rapid state changes into a single frame
    let rafId = null;
    let lastFiltered = issues;

    function scheduleRender() {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(() => {
        rafId = null;
        lastFiltered = applyFilters(state);
      });
    }

    scheduleRender();

    // Search
    let searchTimer;
    searchInput.addEventListener('input', e => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => {
        state.query = e.target.value.trim().toLowerCase();
        scheduleRender();
      }, 200);
    });

    // Table sort — th[data-sort] click via event delegation
    container.addEventListener('click', e => {
      const th = e.target.closest('th[data-sort]');
      if (!th) return;
      const key = th.dataset.sort;
      if (state.sortKey === key) {
        state.sortDir = -state.sortDir;
      } else {
        state.sortKey = key;
        // numeric cols default descending, text/date cols ascending
        state.sortDir = (key === 'key' || key === 'comments') ? -1 : 1;
      }
      scheduleRender();
    });

    // Toolbar download buttons
    toolbar.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      switch (btn.dataset.action) {
        case 'dl-txt':  downloadTxt(lastFiltered,  state.project); break;
        case 'dl-csv':  downloadCsv(lastFiltered,  state.project); break;
        case 'dl-json': downloadJson(lastFiltered, state.project); break;
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Fetch + lazy-load trigger
  // ---------------------------------------------------------------------------

  function load(container) {
    const src = container.dataset.json;
    if (!src) return;
    container.innerHTML = '<p><em>Loading…</em></p>';
    fetch(src)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(data => renderAll(container, Array.isArray(data) ? data : []))
      .catch(err => { container.innerHTML = `<p><em>Could not load issues: ${err.message}</em></p>`; });
  }

  const container = document.getElementById('jira-project');
  if (!container) return;

  new IntersectionObserver((entries, obs) => {
    entries.forEach(e => { if (e.isIntersecting) { obs.unobserve(e.target); load(e.target); } });
  }, { rootMargin: '300px' }).observe(container);

})();
