/**
 * Lazy-loads a changelog.json (produced by build_changelog.py) and renders
 * a filterable, sortable merge-request table grouped by release.
 *
 * Usage in a .md file body:
 *
 *   <div id="athena-changelog"
 *        data-json="./changelog.json"
 *        data-project="atlas/athena"
 *        data-gitlab="https://gitlab.cern.ch"></div>
 *   <script src="athena_changelog_loader.js"></script>
 */
(function () {

  // ---------------------------------------------------------------------------
  // Icons
  // ---------------------------------------------------------------------------

  const ICONS = {
    externalLink: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>`,
    merge:        `<svg xmlns="http://www.w3.org/2000/svg" width="0.7em" height="0.7em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/></svg>`,
    tag:          `<svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2H2v10l9.29 9.29a1 1 0 0 0 1.41 0l7.29-7.29a1 1 0 0 0 0-1.41z"/><path d="M7 7h.01"/></svg>`,
  };

  function ic(key) { return `<span class="twemoji">${ICONS[key]}</span>`; }

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function boldCamelCase(s) {
    // Bold any word containing a lowercase→uppercase transition (e.g. AnalysisBase, xAOD, MuonSpectrometer)
    return s.replace(/\b[A-Za-z]*[a-z][A-Z][A-Za-z]*\b/g, '<strong>$&</strong>');
  }

  // ---------------------------------------------------------------------------
  // Numeric version sort — handles "24.0.10" > "24.0.9" correctly
  // ---------------------------------------------------------------------------

  function parseVersion(v) {
    return String(v || '').split(/[\.\-_]/).map(p => { const n = parseInt(p, 10); return isNaN(n) ? p : n; });
  }

  function compareVersions(a, b) {
    const pa = parseVersion(a), pb = parseVersion(b);
    for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
      const x = pa[i] ?? -Infinity, y = pb[i] ?? -Infinity;
      if (x < y) return -1;
      if (x > y) return  1;
    }
    return 0;
  }

  // ---------------------------------------------------------------------------
  // Label colour cycling — deterministic by label name
  // ---------------------------------------------------------------------------

  const LABEL_COLOURS = ['blue','green','yellow','purple','teal','orange'];

  const _labelColourCache = {};
  function labelColour(name) {
    if (!_labelColourCache[name]) {
      let h = 0;
      for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) & 0xffff;
      _labelColourCache[name] = LABEL_COLOURS[h % LABEL_COLOURS.length];
    }
    return _labelColourCache[name];
  }

  function renderLabels(labels) {
    if (!labels || !labels.length) return '—';
    return labels
      .map(l => `<span class="atlaslabel ${labelColour(l)}" style="font-size:0.75em;margin:0 1px">${escapeHtml(l)}</span>`)
      .join(' ');
  }

  // ---------------------------------------------------------------------------
  // Flatten all MRs from releases into a single row list
  // ---------------------------------------------------------------------------

  function flattenMRs(releases) {
    const rows = [];
    for (const rel of releases) {
      for (const mr of (rel.mrs || [])) {
        rows.push({ ...mr, release: rel.version, release_date: rel.date, tag: rel.tag });
      }
    }
    return rows;
  }

  // ---------------------------------------------------------------------------
  // Table — fixed column widths
  // ---------------------------------------------------------------------------

  const COLS = [
    ['MR',       '5%'],
    ['Title',    '38%'],
    ['Author',   '14%'],
    ['Merged',   '8%'],
    ['Labels',   '21%'],
    ['Release',  '14%'],
  ];

  const COLGROUP = `<colgroup>${COLS.map(([,w]) => `<col style="width:${w}">`).join('')}</colgroup>`;
  const THEAD    = `<thead><tr>${COLS.map(([h]) => `<th>${h}</th>`).join('')}</tr></thead>`;

  function renderRow(row, gitlabBase, project) {
    const tagCell = row.tag
      ? `<a href="${gitlabBase}/${project}/-/tags/${escapeHtml(row.tag)}">${escapeHtml(row.release)}</a>`
      : `<em>${escapeHtml(row.release)}</em>`;

    return `<tr>`
      + `<td><a href="${escapeHtml(row.web_url)}">${ic('merge')}!${row.iid}</a></td>`
      + `<td>${boldCamelCase(escapeHtml(row.title))}</td>`
      + `<td>${escapeHtml(row.author)}</td>`
      + `<td>${row.merged_at || '—'}</td>`
      + `<td>${renderLabels(row.labels)}</td>`
      + `<td>${tagCell}</td>`
      + `</tr>`;
  }

  function buildTable(rows, gitlabBase, project) {
    if (!rows.length) return '<p><em>No merge requests match.</em></p>';
    return `<div class="md-typeset__scrollwrap"><div class="md-typeset__table">`
      + `<table style="table-layout:fixed;width:100%">`
      + COLGROUP + THEAD
      + `<tbody>${rows.map(r => renderRow(r, gitlabBase, project)).join('')}</tbody>`
      + `</table></div></div>`;
  }

  // ---------------------------------------------------------------------------
  // Sparkline — MRs merged per year
  // ---------------------------------------------------------------------------

  function buildSvg(rows) {
    const yearMap = {};
    for (const r of rows) {
      const yr = (r.merged_at || '').slice(0, 4);
      if (yr) yearMap[yr] = (yearMap[yr] || 0) + 1;
    }
    const yearCounts = Object.entries(yearMap).sort(([a],[b]) => a.localeCompare(b));
    const n = yearCounts.length;
    if (n === 0) return '';

    const W = 480, H = 126, padL = 28, padR = 28;
    const xRange = W - padL - padR;
    const bottomY = 72, topPad = 20, chartH = bottomY - topPad;
    const currentYear = String(new Date().getFullYear());
    const maxCount = Math.max(...yearCounts.map(([,c]) => c), 1);

    const pts = yearCounts.map(([yr, count], i) => ({
      x: n === 1 ? Math.round(W / 2) : padL + Math.round(i * xRange / (n - 1)),
      y: Math.round(bottomY - (count / maxCount) * chartH),
      yr, count,
    }));

    let lines = '', dots = '';
    for (let i = 0; i < pts.length - 1; i++) {
      const dashed = pts[i+1].yr >= currentYear ? ' stroke-dasharray="5 3"' : '';
      lines += `<line x1="${pts[i].x}" y1="${pts[i].y}" x2="${pts[i+1].x}" y2="${pts[i+1].y}" stroke="currentColor" stroke-width="1.5" opacity="0.65"${dashed}></line>`;
    }
    for (const pt of pts) {
      const hollow = pt.yr >= currentYear;
      dots += `<circle cx="${pt.x}" cy="${pt.y}" r="3" fill="${hollow?'none':'currentColor'}" stroke="currentColor" stroke-width="1.5" opacity="0.8"></circle>`;
      dots += `<text x="${pt.x}" y="${pt.y-7}" text-anchor="middle" font-size="9" font-family="inherit" fill="currentColor" opacity="0.7">${pt.count.toLocaleString()}</text>`;
      dots += `<text x="${pt.x}" y="88" text-anchor="middle" font-size="9" font-family="inherit" fill="currentColor" opacity="0.4">${pt.yr}</text>`;
    }

    return `<div style="text-align:center;margin-bottom:1.6em">`
      + `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;display:inline-block;">`
      + lines + dots + `</svg></div>`;
  }

  // ---------------------------------------------------------------------------
  // Filter + sort
  // ---------------------------------------------------------------------------

  function applyFilters(state) {
    const { rows, gitlabBase, project, release, author, selectedLabels, labelMode, sortKey, countEl, tableEl } = state;

    let filtered = release ? rows.filter(r => r.release === release) : [...rows];
    if (author) filtered = filtered.filter(r => r.author === author);

    // Label filter: ANY label in selectedLabels must appear on the MR
    if (selectedLabels.size < state.allLabels.size) {
      filtered = filtered.filter(r =>
        (r.labels || []).some(l => selectedLabels.has(l))
      );
    }

    filtered.sort((a, b) => {
      switch (sortKey) {
        case 'iid-asc':      return a.iid - b.iid;
        case 'iid-desc':     return b.iid - a.iid;
        case 'merged-asc':   return (a.merged_at || '').localeCompare(b.merged_at || '');
        case 'merged-desc':  return (b.merged_at || '').localeCompare(a.merged_at || '');
        case 'release-asc':  return (a.release_date || '').localeCompare(b.release_date || '');
        case 'release-desc': return (b.release_date || '').localeCompare(a.release_date || '');
        default:             return b.iid - a.iid;
      }
    });

    countEl.textContent = `Showing ${filtered.length.toLocaleString()} of ${rows.length.toLocaleString()} merge requests.`;
    tableEl.innerHTML = buildTable(filtered, gitlabBase, project);
  }

  // ---------------------------------------------------------------------------
  // Main render
  // ---------------------------------------------------------------------------

  function renderAll(container, data) {
    const project    = container.dataset.project || data.project || 'atlas/athena';
    const gitlabBase = (container.dataset.gitlab  || 'https://gitlab.cern.ch').replace(/\/$/, '');
    const releases   = data.releases || [];
    const allRows    = flattenMRs(releases);
    const generated  = (data.generated_at || '').slice(0, 10);

    const releaseNames = [...new Set(releases.map(r => r.version))]
      .sort((a, b) => compareVersions(b, a));   // newest first, numeric
    const authors = [...new Set(allRows.map(r => r.author).filter(Boolean))].sort((a,b) => a.localeCompare(b));

    // All unique labels, sorted alphabetically
    const allLabelsSet = new Set();
    for (const row of allRows) for (const l of (row.labels || [])) allLabelsSet.add(l);
    const allLabels = [...allLabelsSet].sort((a,b) => a.localeCompare(b));

    const ctrlStyle = [
      'padding:0.28em 0.55em','font-size:0.82em',
      'border:1px solid var(--md-default-fg-color--lightest)',
      'border-radius:4px','background:var(--md-default-bg-color)',
      'color:inherit','outline:none',
    ].join(';');

    const releaseOptions = [`<option value="">All releases (${releaseNames.length})</option>`]
      .concat(releaseNames.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`))
      .join('');

    const authorOptions = [`<option value="">All authors (${authors.length})</option>`]
      .concat(authors.map(a => `<option value="${escapeHtml(a)}">${escapeHtml(a)}</option>`))
      .join('');

    const labelChips = allLabels.map(l => {
      const cls = labelColour(l);
      return `<label style="cursor:pointer;user-select:none">`
        + `<input type="checkbox" value="${escapeHtml(l)}" checked style="position:absolute;opacity:0;width:0;height:0">`
        + `<span class="atlaslabel ${cls}" style="font-size:0.8em">${escapeHtml(l)}</span>`
        + `</label>`;
    }).join('');

    container.innerHTML =
      `<div class="admonition info">`
      + `<p class="admonition-title">${ic('tag')} ${escapeHtml(project)} merge requests`
      + (generated ? ` <span style="font-weight:normal;opacity:0.6;font-size:0.9em">· generated ${generated}</span>` : '')
      + ` · <a href="${gitlabBase}/${project}/-/merge_requests">${ic('merge')} GitLab</a>`
      + `</p></div>`

      + `<p style="text-align:center;font-size:0.82em;opacity:0.6;margin:0 0 1.2em">`
      + `${releaseNames.length} releases · ${allRows.length.toLocaleString()} merge requests · ${authors.length} contributors`
      + `</p>`

      + buildSvg(allRows)

      + `<div style="display:flex;flex-wrap:wrap;gap:0.5em;align-items:center;margin-bottom:0.75em">`
      + `<select id="cl-release" style="${ctrlStyle};flex:1;min-width:150px">${releaseOptions}</select>`
      + `<select id="cl-author"  style="${ctrlStyle};flex:1;min-width:150px">${authorOptions}</select>`
      + `<select id="cl-sort"    style="${ctrlStyle}">`
      + `<option value="iid-desc">MR ↓</option>`
      + `<option value="iid-asc">MR ↑</option>`
      + `<option value="merged-desc">Merged ↓</option>`
      + `<option value="merged-asc">Merged ↑</option>`
      + `<option value="release-desc">Release ↓</option>`
      + `<option value="release-asc">Release ↑</option>`
      + `</select></div>`

      + `<details style="margin-bottom:0.8em"><summary style="font-size:0.82em;cursor:pointer;opacity:0.7">Filter by label (${allLabels.length})</summary>`
      + `<div id="cl-chips" style="display:flex;flex-wrap:wrap;gap:0.35em;margin-top:0.5em">${labelChips}</div>`
      + `</details>`

      + `<p id="cl-count" style="font-size:0.82em;opacity:0.6;margin:0 0 0.5em"></p>`
      + `<div id="cl-table"></div>`;

    const state = {
      rows: allRows, gitlabBase, project,
      release: '', author: '',
      selectedLabels: new Set(allLabels),
      allLabels: new Set(allLabels),
      sortKey: 'iid-desc',
      countEl: container.querySelector('#cl-count'),
      tableEl: container.querySelector('#cl-table'),
    };

    applyFilters(state);

    container.querySelector('#cl-release').addEventListener('change', e => { state.release = e.target.value; applyFilters(state); });
    container.querySelector('#cl-author').addEventListener('change',  e => { state.author  = e.target.value; applyFilters(state); });
    container.querySelector('#cl-sort').addEventListener('change',    e => { state.sortKey = e.target.value; applyFilters(state); });

    container.querySelector('#cl-chips').addEventListener('change', e => {
      const cb = e.target;
      if (cb.type !== 'checkbox') return;
      const chip = cb.nextElementSibling;
      if (cb.checked) { state.selectedLabels.add(cb.value);    chip.style.opacity = ''; }
      else            { state.selectedLabels.delete(cb.value);  chip.style.opacity = '0.3'; }
      applyFilters(state);
    });
  }

  // ---------------------------------------------------------------------------
  // Compact renderer — all MRs grouped under H2 release headers
  // ---------------------------------------------------------------------------

  function renderCompact(container, data) {
    const project    = container.dataset.project || data.project || 'atlas/athena';
    const gitlabBase = (container.dataset.gitlab  || 'https://gitlab.cern.ch').replace(/\/$/, '');
    const releases   = (data.releases || [])
      .filter(r => r.mrs && r.mrs.length)
      .sort((a, b) => compareVersions(b.version, a.version));

    const totalMRs = releases.reduce((n, r) => n + r.mrs.length, 0);

    const sections = releases.map(rel => {
      const tagHref = rel.tag
        ? `${gitlabBase}/${project}/-/tags/${escapeHtml(rel.tag)}`
        : `${gitlabBase}/${project}/-/merge_requests`;
      const dateStr = rel.date ? ` <span style="font-weight:normal;opacity:0.5;font-size:0.8em"> · ${rel.date}</span>` : '';
      const heading = `<h2 style="margin:1.4em 0 0.3em"><a href="${tagHref}">${escapeHtml(rel.version)}${dateStr}</a></h2>`;
      const items = rel.mrs.map(mr =>
        `<p style="margin:0.15em 0;font-size:0.88em;font-family:var(--md-code-font,monospace)">`
        + `<a href="${escapeHtml(mr.web_url)}">${ic('merge')}!${mr.iid}</a>`
        + ` — ${boldCamelCase(escapeHtml(mr.title))}`
        + `</p>`
      ).join('');
      return heading + items;
    }).join('');

    container.innerHTML =
      `<p style="font-size:0.82em;opacity:0.6;margin:0 0 0.8em">`
      + `${releases.length} releases · ${totalMRs.toLocaleString()} merge requests`
      + `</p>`
      + (sections || '<p><em>No merge requests found.</em></p>');
  }

  // ---------------------------------------------------------------------------
  // Fetch + lazy-load trigger
  // ---------------------------------------------------------------------------

  function load(container) {
    const src = container.dataset.json;
    if (!src) return;
    container.innerHTML = '<p><em>Loading…</em></p>';
    const compact = container.dataset.compact === 'true';
    fetch(src)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(data => compact ? renderCompact(container, data) : renderAll(container, data))
      .catch(err => { container.innerHTML = `<p><em>Could not load changelog: ${err.message}</em></p>`; });
  }

  const container = document.getElementById('athena-changelog');
  if (!container) return;

  new IntersectionObserver((entries, obs) => {
    entries.forEach(e => { if (e.isIntersecting) { obs.unobserve(e.target); load(e.target); } });
  }, { rootMargin: '300px' }).observe(container);

})();
