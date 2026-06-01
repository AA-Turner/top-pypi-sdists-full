let _pages = [];
let _authors = {};
let _fusePages = null;
let _activeWeb = null;
let _myActiveAuthor = null;
let _activeView = 'pages';
let _searchTmo = null;
let _currentSort = 'pagerank';
let _currentFilter = 'all';
let _viewMode = 'card';
let _pagesTableSort = { column: 'pagerank_rank', dir: 'asc' };
let _authorsTableSort = { column: 'pagesEdited', dir: 'desc' };
let _dormantAuthors = new Set();
let _pageRevMeta = {};            // url -> {nRevisions, nUniqueAuthors, dateCreated}
let _historyLut = {};            // html_file -> [{revision, date, username}] — loaded after initial render
let _authorSparkEntries = [];     // current author's page entries (for sparkline re-render)
let _authorSparkName = null;   // current author key
let _authorPageMode = 'all'; // 'created' | 'revised' | 'all'
let _authorPageIndex = {};       // author → page[] (pages where p.author or p.created_by === author)
let _authorAllPagesIndex = {};   // author → page[] (all pages touched: created + revised via history)
let _authorList = [];            // sorted list for suggestion dropdown — rebuilt after init pass
let _authorStats = null;         // cached result of getAuthorsData()
let _authorLastEditTs = {};      // author → timestamp (ms) of most recent revision
let _authorFirstEditTs = {};     // author → timestamp (ms) of earliest revision
let _authorYearRevCounts = {};   // author → count of own revisions within last year
const MASS_EDIT_USER = 'pete';   // account treated as mass-edit noise; shown as background on sparklines
let _peteRevsByYear = {};        // global: pete revision count per year
let _bannerYearData = null;      // null → use global data; set to web/selection-scoped data
let _bannerPeteData = null;      // pete revisions matching current banner scope
const _PAGE_SIZE = 150;          // initial cards/rows rendered; remainder shown on demand
let _authorSparkCache = {};      // author → { pages_yearly, pages_cumulative, revisions_yearly, revisions_cumulative }
let _dataBase = '';              // set during init — base URL path for data files (e.g. '/twikiregistry/')
let _ghostAuthors = new Set();   // editors with no activity in 5+ years
let _lastViewedLut = {};         // 'Web/Topic' → {v: views, lv: last_viewed_on}
let _pageCats = {};              // html_file → [category strings]
let _catIndex = {};              // category → [pages] — built in buildCategoriesTree
let _pagesWithHistoryCount = 0; // Counter for pages with history
let _authorCreatedPagesLut = {}; // author → [pages they created]
let _authorsMostRecentPages = {}; // author → [pages they most recently edited]
let _pageToMostRecentAuthor = {};      // html_file → author (inverse of above, built during init)
let _authorsLastEditedPages = {}; // author → [pages they last edited (all, not just active)]
let _pageToLastEditedAuthor = {};      // html_file → author (fallback for pages with no active editors)
let _currentEntries = null;           // currently displayed page entries (set by renderList)
let _isCustomSelection = false;       // true when displaying search results
let _currentSearchSlug = '';          // slugified search query for CSV filename
let _selectionBannerToken = 0;        // incremented each search; stale callbacks self-cancel

const SCRIPT_BASE = document.currentScript
    ? document.currentScript.src.replace(/[^/]+$/, '')
    : '/assets/javascripts/';

let _fusePromise = null;
function loadFuse() {
    if (_fusePromise) return _fusePromise;
    _fusePromise = new Promise(resolve => {
        if (typeof Fuse !== 'undefined') { resolve(Fuse); return; }
        const s = document.createElement('script');
        s.src = SCRIPT_BASE + 'fuse.min.js';
        s.onload = () => { const F = window.Fuse; resolve(F || null); };
        s.onerror = () => resolve(null);
        document.head.appendChild(s);
    });
    return _fusePromise;
}

function downloadEntryMarkdown(htmlFile) {
    const base = htmlFile.replace(/\.html?$/, '');
    const url = _dataBase + 'twikimd/' + base + '.txt';
    fetch(url)
        .then(r => { if (!r.ok) throw new Error('not found'); return r.blob(); })
        .then(blob => {
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = base + '.md';
            a.click();
            URL.revokeObjectURL(a.href);
        })
        .catch(() => alert('Markdown file not available for this page.'));
}

function escHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// author_split is stored as an array ["First","Last"] in authors_metadata
// page entries store it as a pre-joined string or null — handle both
function displayName(authorKey) {
    const auth = _authors[authorKey];
    if (auth) {
        const sp = auth.author_split;
        if (Array.isArray(sp)) return sp.join(' ');
        if (sp) return String(sp);
    }
    return authorKey || 'Unknown';
}

function pageDisplayName(entry) {
    // On page entries author_split is a pre-joined string set by the Python script
    if (entry.author_split && typeof entry.author_split === 'string') return entry.author_split;
    if (Array.isArray(entry.author_split)) return entry.author_split.join(' ');
    return entry.author || 'Unknown';
}

function fmtDate(dateStr) {
    if (!dateStr || dateStr === 'Unknown') return dateStr || 'Unknown';
    return dateStr.split(' - ')[0];
}

function dateYear(dateStr) {
    if (!dateStr || dateStr === 'Unknown') return null;
    const clean = String(dateStr).split(' - ')[0].trim();
    if (!clean) return null;
    const d = new Date(clean);
    if (isNaN(d.getTime())) return null;
    const y = d.getFullYear();
    return (y >= 1990 && y <= new Date().getFullYear() + 2) ? y : null;
}

function setStatus(state, text) {
    const dot = document.querySelector('.status-dot');
    if (dot) dot.className = `status-dot ${state}`;
    const statusEl = document.getElementById('statusText');
    if (statusEl) statusEl.textContent = text;
}

function getAgeStatus(dateStr) {
    if (!dateStr || dateStr === 'Unknown') return { cls: '', label: 'Unknown' };
    const lastEdit = new Date(dateStr.split(' - ')[0]);
    if (isNaN(lastEdit)) return { cls: '', label: 'Unknown' };
    const yearsDiff = (new Date() - lastEdit) / (1000 * 60 * 60 * 24 * 365.25);
    if (yearsDiff > 5) return { cls: 'age-danger', label: '>5 years' };
    if (yearsDiff > 2) return { cls: 'age-warning', label: '2–5 years' };
    return { cls: 'age-success', label: 'Date Created' };
}

function getAgeClass(dateStr) {
    return getAgeStatus(dateStr).cls;
}

function medianInterval(history) {
    if (history.length < 2) return 'N/A';
    const dates = history.map(h => {
        const [d, t] = h.date.split(' - ');
        return new Date(`${d.replace(/-/g, '/')} ${t}`);
    }).sort((a, b) => a - b);
    const diffs = [];
    for (let i = 1; i < dates.length; i++) {
        diffs.push((dates[i] - dates[i - 1]) / (86400 * 1000));
    }
    diffs.sort((a, b) => a - b);
    const mid = Math.floor(diffs.length / 2);
    return (diffs.length % 2 === 0 ? (diffs[mid - 1] + diffs[mid]) / 2 : diffs[mid]).toFixed(1);
}

function getWebName(url) {
    if (!url) return 'Unknown';
    const m = url.match(/\/(view|oops|manage)\/([^\/]+)\//);
    return m ? m[2] : 'Unknown';
}

function applyFiltersAndSort(entries) {
    // Drop entries with no title and no absolute URL (they render as blank cards
    // with a link that resolves back to the current page's query string).
    let filtered = entries.filter(e => {
        const hasTitle = e.title && e.title.trim();
        const hasUrl = e.url && /^https?:\/\//i.test(e.url);
        return hasTitle || hasUrl;
    });
    if (_currentFilter !== 'all') {
        filtered = filtered.filter(e => {
            const age = getAgeClass(e.date);
            if (_currentFilter === 'recent') return age === 'age-success';
            if (_currentFilter === 'medium') return age === 'age-warning';
            if (_currentFilter === 'old') return age === 'age-danger';
            if (_currentFilter === 'editor-inactive') return e.author && _ghostAuthors.has(e.author);
            return true;
        });
    }
    filtered.sort((a, b) => {
        if (_currentSort === 'pagerank') return (a.pagerank_rank || 9999) - (b.pagerank_rank || 9999);
        if (_currentSort === 'title-asc') return (a.title || '').localeCompare(b.title || '');
        if (_currentSort === 'title-desc') return (b.title || '').localeCompare(a.title || '');
        if (_currentSort === 'date-desc') {
            const da = new Date(a.date?.split(' - ')[0] || '1900');
            const db = new Date(b.date?.split(' - ')[0] || '1900');
            return db - da;
        }
        if (_currentSort === 'date-asc') {
            const da = new Date(a.date?.split(' - ')[0] || '1900');
            const db = new Date(b.date?.split(' - ')[0] || '1900');
            return da - db;
        }
        return 0;
    });
    return filtered;
}

function renderEntry(entry) {
    const status = getAgeStatus(entry.date);
    const card = document.createElement('div');
    const _ph = _historyLut[entry.html_file] || [];

    // Determine most recent author in priority order:
    // 1. Last revision in history (most authoritative)
    // 2. Most recent active editor (from authors_last_active_edited_pages_lut.json)
    // 3. Last edited (all, even inactive) (from authors_last_edited_pages_lut.json)
    // 4. Entry author fallback
    let mostRecentAuthorKey = null;
    if (_ph.length > 0) {
        // Get the last (most recent) revision's author
        const lastRev = _ph[_ph.length - 1];
        mostRecentAuthorKey = lastRev.username;
    }
    if (!mostRecentAuthorKey) {
        mostRecentAuthorKey = _pageToMostRecentAuthor[entry.html_file] || _pageToLastEditedAuthor[entry.html_file] || entry.author;
    }
    const isGhostEditor = mostRecentAuthorKey && _ghostAuthors.has(mostRecentAuthorKey);
    const isDormantEditor = mostRecentAuthorKey && _dormantAuthors.has(mostRecentAuthorKey);
    card.className = `entry-card ${status.cls}${isGhostEditor ? ' ghost-editor' : ''}`;

    const revCount = parseInt(entry.revision) || _ph.length || 0;
    const rankDisplay = entry.pagerank_rank ? `#${entry.pagerank_rank}` : '—';

    // Find most recent active author if most recent author is dormant
    let displayAuthorKey = mostRecentAuthorKey;
    let displayLabel = 'Most Recent Active Author';
    if (isDormantEditor && _ph.length > 0) {
        // Search history backwards for the most recent active (non-dormant, non-ghost) author
        for (let i = _ph.length - 1; i >= 0; i--) {
            const histAuthor = _ph[i].username;
            if (histAuthor && !_dormantAuthors.has(histAuthor) && !_ghostAuthors.has(histAuthor)) {
                displayAuthorKey = histAuthor;
                displayLabel = `Most Recent Active Author`;
                break;
            }
        }
    }

    const authorName = displayAuthorKey ? displayName(displayAuthorKey) : (pageDisplayName(entry) || 'Unknown');
    const mostRecentAuthorName = displayName(mostRecentAuthorKey);
    const showLastEditor = authorName !== mostRecentAuthorName;
    const authorLink = _authors[displayAuthorKey]
        ? `<a href="#" class="author-link" onclick="showAuthor('${escHtml(displayAuthorKey)}'); return false;">${escHtml(authorName)}</a>${showLastEditor ? `(<a href="#" class="author-link" onclick="showAuthor('${escHtml(mostRecentAuthorKey)}'); return false;">${escHtml(mostRecentAuthorName)}</a>)` : ''}`
        : escHtml(authorName);
    const dateCreated = fmtDate(entry.date_created) || '—';
    const firstRev = _ph.length ? [..._ph].sort((a, b) => a.date.localeCompare(b.date))[0] : null;
    const creatorKey = _ph?.[0]?.username || entry.created_by || entry.author || null;
    const creatorName = creatorKey ? displayName(creatorKey) : '—';
    const creatorLink = creatorKey && _authors[creatorKey]
        ? `<a href="#" class="author-link" onclick="showAuthor('${escHtml(creatorKey)}'); return false;">${escHtml(creatorName)}</a>`
        : escHtml(creatorName);

    let revHistoryHTML = '';
    if (_ph.length > 0) {
        const rows = [..._ph]
            .sort((a, b) => parseInt(b.revision || 0) - parseInt(a.revision || 0))
            .map(h => {
                const revNum = h.revision || '?';
                const revDate = fmtDate(h.date || '');
                const revUser = h.username || h.author || 'Unknown';
                const authorCell = _authors[revUser]
                    ? `<span onclick="showAuthor('${escHtml(revUser)}')" style="cursor:pointer;color:var(--accent);">${escHtml(revUser)}</span>`
                    : `<span>${escHtml(revUser)}</span>`;
                return `<tr>
          <td class="rev-num">r${escHtml(String(revNum))}</td>
          <td class="rev-date">${escHtml(revDate)}</td>
          <td class="rev-author">${authorCell}</td>
        </tr>`;
            }).join('');
        revHistoryHTML = `
      <div class="revision-history">
        <div class="revision-history-title">Revision History (${_ph.length})</div>
        <table class="revision-table">
          <thead><tr><th>Rev</th><th>Date</th><th>Author</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
    }

    card.innerHTML = `
    <div class="entry-head" style="position:relative;">
      <div onclick="event.stopPropagation();" style="position:absolute;top:6px;right:8px;display:flex;gap:4px;align-items:center;">
        <span style="width:1px;height:18px;background:var(--border);margin:0 4px;display:inline-block;"></span>
        <a href="${escHtml(entry.url.replace(/\/bin\/view(?:auth)?\//i, '/bin/edit/') + '?t;nowysiwyg=1')}" target="_blank"
          title="Edit the TWiki" style="background:none;border:none;cursor:pointer;padding:2px;color:var(--text-muted);opacity:0.6;line-height:0;text-decoration:none;"
          onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.6'">
         <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-type-corner-icon lucide-file-type-corner"><path d="M12 22h6a2 2 0 0 0 2-2V8a2.4 2.4 0 0 0-.706-1.706l-3.588-3.588A2.4 2.4 0 0 0 14 2H6a2 2 0 0 0-2 2v6"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M3 16v-1.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5V16"/><path d="M6 22h2"/><path d="M7 14v8"/></svg>
        </a>
      </div>
      <div class="entry-row">
        <div class="block rank-block">
          <div class="rank-number" title="PageRank ranking">${rankDisplay}</div>
          <div class="rank-revisions">Revisions: ${revCount}</div>
        </div>
        <div class="block title-block">
          <div class="main-title">
            <a href="${escHtml(entry.url)}" target="_blank">Twiki > ${escHtml(getWebName(entry.url))} > ${escHtml(entry.title || entry.html_file || 'Untitled')}</a>
          </div>
          <div class="edit-date">
            ${escHtml(displayLabel)}: ${escHtml(fmtDate(entry.date))} by ${authorLink}
          </div>
        </div>
        <div class="info-block" style="text-align:left;">
          <div class="last-edit-line"><span class="meta-label">Date Created</span>${escHtml(dateCreated || '—')}</div>
          <div class="creation-line"><span class="meta-label">Created by</span>${creatorLink}</div>
        </div>
      </div>
    </div>

    <div class="entry-details">

      <div class="info-list">
        <div><strong>Web:</strong> ${escHtml(getWebName(entry.url))}</div>
        <div><strong>Median interval:</strong> ${medianInterval(_ph)} days</div>
        <div><strong>Byte size:</strong> ${entry.byte_size || '—'}</div>
        ${entry.js_count ? `<div><strong>JS count:</strong>  ${entry.js_count}</div>` : ''}
        ${entry.css_count ? `<div><strong>CSS count:</strong> ${entry.css_count}</div>` : ''}
        <div><strong>Links out:</strong>  ${entry.n_links || 0}</div>
        <div><strong>Backlinks:</strong>  ${entry.n_backlinks || 0}</div>
        <div><strong>PageRank:</strong>   ${entry.pagerank?.toFixed(8) || '—'}</div>
        ${entry.description ? `<div><strong>Description:</strong> ${escHtml(entry.description)}</div>` : ''}
        ${(() => { const topicKey = getWebName(entry.url) + '/' + (entry.url?.split('/').pop() || ''); const lv = _lastViewedLut[topicKey]; return lv ? `<div><strong>Last viewed:</strong> ${escHtml(lv.lv)} · ${lv.v} views</div>` : ''; })()}
        ${isGhostEditor ? `<div style="color:#8b5cf6;font-weight:500;">⚠ Last editor inactive 5+ years</div>` : ''}
      </div>
      ${revHistoryHTML}
    </div>
  `;

    card.querySelector('.entry-head').onclick = (e) => {
        if (e.target.tagName === 'A') return;
        const det = card.querySelector('.entry-details');
        det.style.display = det.style.display === 'block' ? 'none' : 'block';
    };
    return card;
}

function renderPagesCards(processed, container) {
    container.innerHTML = '';
    const list = document.createElement('div');
    list.className = 'entries-list';
    let shown = Math.min(_PAGE_SIZE, processed.length);
    processed.slice(0, shown).forEach(e => list.appendChild(renderEntry(e)));
    container.appendChild(list);

    function addCardPageBtn() {
        if (shown >= processed.length) return;
        const remaining = processed.length - shown;
        const batch = Math.min(100, remaining);
        const btn = document.createElement('button');
        btn.className = 'show-more-btn';
        btn.textContent = `Show next ${batch} (${remaining} remaining)`;
        btn.onclick = () => {
            btn.remove();
            const next = Math.min(shown + 100, processed.length);
            processed.slice(shown, next).forEach(e => list.appendChild(renderEntry(e)));
            shown = next;
            addCardPageBtn();
        };
        container.appendChild(btn);
    }
    addCardPageBtn();
}

function sortPagesData(data) {
    const { column, dir } = _pagesTableSort;
    return [...data].sort((a, b) => {
        let va, vb;

        // Handle columns that need special sorting logic
        if (column === 'author') {
            // Sort by most recent author
            const authA = _pageToMostRecentAuthor[a.html_file] || _pageToLastEditedAuthor[a.html_file] || a.author;
            const authB = _pageToMostRecentAuthor[b.html_file] || _pageToLastEditedAuthor[b.html_file] || b.author;
            va = displayName(authA).toLowerCase();
            vb = displayName(authB).toLowerCase();
        } else if (column === 'revision') {
            // Sort by revision count
            const pageKeyA = a.url || a.html_file || a.title;
            const pageKeyB = b.url || b.html_file || b.title;
            const metaA = _pageRevMeta[pageKeyA] || { nRevisions: 0 };
            const metaB = _pageRevMeta[pageKeyB] || { nRevisions: 0 };
            va = metaA.nRevisions;
            vb = metaB.nRevisions;
        } else {
            va = a[column];
            vb = b[column];
        }

        if (['pagerank_rank', 'n_links', 'n_backlinks', 'byte_size', 'revision'].includes(column)) {
            va = parseFloat(va) || 0;
            vb = parseFloat(vb) || 0;
        } else if (column === 'date' || column === 'date_created') {
            va = new Date(String(va || '').split(' - ')[0] || '1900');
            vb = new Date(String(vb || '').split(' - ')[0] || '1900');
        } else if (typeof va === 'string' || typeof vb === 'string') {
            va = String(va || '').toLowerCase();
            vb = String(vb || '').toLowerCase();
        }
        if (va < vb) return dir === 'asc' ? -1 : 1;
        if (va > vb) return dir === 'asc' ? 1 : -1;
        return 0;
    });
}

function _pageTableRowHTML(e) {
    const pageKey = e.url || e.html_file || e.title;
    const meta = _pageRevMeta[pageKey] || { nRevisions: 0, nUniqueAuthors: 0, dateCreated: null };
    const nRevs = meta.nRevisions || parseInt(e.revision) || 0;
    const nAuthors = meta.nUniqueAuthors || 0;
    const created = fmtDate(e.date_created) || '—';

    // Use most recent author from _pageToMostRecentAuthor (active editors) if available,
    // otherwise fall back to _pageToLastEditedAuthor (all editors, even if inactive)
    const mostRecentAuthorKey = _pageToMostRecentAuthor[e.html_file] || _pageToLastEditedAuthor[e.html_file] || e.author;
    const editorDormant = mostRecentAuthorKey && _dormantAuthors.has(mostRecentAuthorKey);
    const status = getAgeStatus(e.date);
    const rowExtra = editorDormant ? ' editor-dormant' : '';
    const authorName = mostRecentAuthorKey ? displayName(mostRecentAuthorKey) : (pageDisplayName(e) || 'Unknown');
    const authorCell = _authors[mostRecentAuthorKey]
        ? `<a href="#" onclick="showAuthor('${escHtml(mostRecentAuthorKey)}');return false;">${escHtml(authorName)}</a>`
        : escHtml(authorName);
    return `
      <tr class="${status.cls}${rowExtra}">
        <td class="num">${e.pagerank_rank ? '#' + e.pagerank_rank : '—'}</td>
        <td><a href="${escHtml(e.url)}" target="_blank">${escHtml(e.title || e.html_file || 'Untitled')}</a></td>
        <td>${escHtml(created)}</td>
        <td>${escHtml(fmtDate(e.date))}</td>
        <td>${authorCell}</td>
        <td class="num">${nRevs}</td>
        <td class="num">${nAuthors}</td>
        <td class="num">${e.n_backlinks || 0}</td>
        <td class="num">${e.byte_size || '—'}</td>
      </tr>`;
}

function renderPagesTable(processed, container) {
    const sorted = sortPagesData(processed);
    const { column: sc, dir: sd } = _pagesTableSort;

    const columns = [
        { key: 'pagerank_rank', label: 'Rank', cls: 'num' },
        { key: 'title', label: 'Title', cls: '' },
        { key: 'date_created', label: 'Date Created', cls: '' },
        { key: 'date', label: 'Last Edit', cls: '' },
        { key: 'author', label: 'Editor', cls: '' },
        { key: 'revision', label: 'Revs', cls: 'num' },
        { key: 'revision', label: 'Authors', cls: 'num' },
        { key: 'n_backlinks', label: 'Backlinks', cls: 'num' },
        { key: 'byte_size', label: 'Size', cls: 'num' },
    ];

    const headHTML = '<tr>' + columns.map(col => {
        const active = col.key === sc ? ` data-sort-dir="${sd}"` : '';
        return `<th data-column="${col.key}"${active} class="${col.cls}">${col.label}</th>`;
    }).join('') + '</tr>';

    const table = document.createElement('table');
    table.className = 'pages-table';
    table.innerHTML = `<thead>${headHTML}</thead><tbody>${sorted.slice(0, _PAGE_SIZE).map(_pageTableRowHTML).join('')}</tbody>`;

    table.querySelectorAll('thead th[data-column]').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const col = th.dataset.column;
            if (_pagesTableSort.column === col) {
                _pagesTableSort.dir = _pagesTableSort.dir === 'asc' ? 'desc' : 'asc';
            } else {
                _pagesTableSort.column = col;
                _pagesTableSort.dir = 'asc';
            }
            renderPagesTable(processed, container);
        });
    });

    container.innerHTML = '';
    container.appendChild(table);

    if (sorted.length > _PAGE_SIZE) {
        let shownTable = _PAGE_SIZE;
        function addTablePageBtn() {
            if (shownTable >= sorted.length) return;
            const remaining = sorted.length - shownTable;
            const batch = Math.min(100, remaining);
            const btn = document.createElement('button');
            btn.className = 'show-more-btn';
            btn.textContent = `Show next ${batch} (${remaining} remaining)`;
            btn.onclick = () => {
                btn.remove();
                const next = Math.min(shownTable + 100, sorted.length);
                table.querySelector('tbody').insertAdjacentHTML('beforeend',
                    sorted.slice(shownTable, next).map(_pageTableRowHTML).join(''));
                shownTable = next;
                addTablePageBtn();
            };
            container.appendChild(btn);
        }
        addTablePageBtn();
    }
}

function renderAuthorCard(a) {
    const card = document.createElement('div');
    card.className = `entry-card ${a.ageClass}`;
    const total = a.pagesEdited || 1;
    const statusLabel = a.ageClass === 'age-success' ? 'Active' : a.ageClass === 'age-warning' ? 'Moderate' : 'Inactive';

    card.innerHTML = `
    <div class="author-card-header">
      <span class="author-card-name" onclick="showAuthor('${escHtml(a.author)}');">${escHtml(a.displayName)}</span>
      <span class="author-card-meta">${a.pagesEdited} page${a.pagesEdited !== 1 ? 's' : ''} · ${a.totalRevisions} rev${a.totalRevisions !== 1 ? 's' : ''} · h-index <strong>${a.hIndex}</strong></span>
      <div class="status-badge ${a.ageClass}">${statusLabel}</div>
    </div>
    <div class="author-page-bands">
      <div class="band-success" style="flex:${a.pagesActive}"></div>
      <div class="band-warning" style="flex:${a.pagesMedium}"></div>
      <div class="band-danger"  style="flex:${a.pagesOld + (total - a.pagesActive - a.pagesMedium - a.pagesOld)}"></div>
    </div>
    <div class="author-band-counts">
      <span class="bc bc-success"><span class="dot"></span>${a.pagesActive} active</span>
      <span class="bc bc-warning"><span class="dot"></span>${a.pagesMedium} 2–5yr</span>
      <span class="bc bc-danger"><span class="dot"></span>${a.pagesOld} >5yr</span>
      <span class="bc" style="margin-left:auto;color:var(--text-dim);">Last: ${escHtml(a.lastActivity)}</span>
    </div>
  `;
    return card;
}

function renderAuthorsCards(authorsData, container) {
    container.innerHTML = '';
    const list = document.createElement('div');
    list.className = 'entries-list';
    authorsData.forEach(a => list.appendChild(renderAuthorCard(a)));
    container.appendChild(list);
}

function sortAuthorsData(data) {
    const { column, dir } = _authorsTableSort;
    return [...data].sort((a, b) => {
        let va = a[column], vb = b[column];
        if (['pagesEdited', 'lastYearRevisions', 'totalRevisions', 'pagesActive', 'pagesMedium', 'pagesOld', 'pctOld', 'hIndex'].includes(column)) {
            va = parseFloat(va) || 0;
            vb = parseFloat(vb) || 0;
        } else if (column === 'lastActivity' || column === 'authorSince') {
            va = new Date(va === '—' ? '1900' : va);
            vb = new Date(vb === '—' ? '1900' : vb);
        } else {
            va = String(va || '').toLowerCase();
            vb = String(vb || '').toLowerCase();
        }
        if (va < vb) return dir === 'asc' ? -1 : 1;
        if (va > vb) return dir === 'asc' ? 1 : -1;
        return 0;
    });
}

function _authorTableRowHTML(a) {
    const dormant = _dormantAuthors.has(a.author);
    const rowCls = dormant ? 'author-dormant' : a.ageClass;
    return `
    <tr class="${rowCls}">
      <td><a href="#" class="author-name" onclick="showAuthor('${escHtml(a.author)}');return false;">${escHtml(a.displayName)}</a></td>
      <td class="num">${a.pagesEdited}</td>
      <td class="num" style="color:var(--age-green)">${a.pagesActive}</td>
      <td class="num" style="color:var(--age-orange)">${a.pagesMedium}</td>
      <td class="num" style="color:var(--age-red)">${a.pagesOld}</td>
      <td class="num" style="color:var(--age-red)">${a.pctOld}%</td>
      <td class="num" style="color:var(--accent);font-weight:600">${a.hIndex}</td>
      <td class="num">${a.totalRevisions}</td>
      <td>${escHtml(a.lastActivity)}</td>
      <td class="num">${a.lastYearRevisions}</td>
    </tr>`;
}

function renderAuthorsTable(authorsData, container, skipTableSort = false) {
    // If skipTableSort is true, use authorsData as-is (already sorted by dropdown)
    // Otherwise, apply table column sorting
    const sorted = skipTableSort ? authorsData : sortAuthorsData(authorsData);
    const { column: sc, dir: sd } = _authorsTableSort;

    const columns = [
        { key: 'displayName', label: 'Name', cls: '' },
        { key: 'pagesEdited', label: 'Pages', cls: 'num' },
        { key: 'pagesActive', label: '<2yr', cls: 'num' },
        { key: 'pagesMedium', label: '2–5yr', cls: 'num' },
        { key: 'pagesOld', label: '>5yr', cls: 'num' },
        { key: 'pctOld', label: '%stale', cls: 'num' },
        { key: 'hIndex', label: 'h-idx', cls: 'num' },
        { key: 'totalRevisions', label: 'Revisions', cls: 'num' },
        { key: 'lastActivity', label: 'Last Active', cls: '' },
        { key: 'lastYearRevisions', label: 'Rev (1yr)', cls: 'num' },
    ];

    const headHTML = '<tr>' + columns.map(col => {
        const active = col.key === sc ? ` data-sort-dir="${sd}"` : '';
        return `<th data-column="${col.key}"${active} class="${col.cls}">${col.label}</th>`;
    }).join('') + '</tr>';

    const table = document.createElement('table');
    table.className = 'authors-table';
    table.innerHTML = `<thead>${headHTML}</thead><tbody>${sorted.slice(0, _PAGE_SIZE).map(_authorTableRowHTML).join('')}</tbody>`;

    table.querySelectorAll('thead th[data-column]').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const col = th.dataset.column;
            if (_authorsTableSort.column === col) {
                _authorsTableSort.dir = _authorsTableSort.dir === 'asc' ? 'desc' : 'asc';
            } else {
                _authorsTableSort.column = col;
                _authorsTableSort.dir = 'desc';
            }
            // Clear dropdown sort when clicking table header
            _currentSort = 'pagesEdited';
            document.getElementById('sortSelect').value = 'pagesEdited';
            // Don't skip table sort - apply column-based sorting
            renderAuthorsTable(authorsData, container, false);
        });
    });

    container.innerHTML = '';
    container.appendChild(table);

    if (sorted.length > _PAGE_SIZE) {
        let shownAuthors = _PAGE_SIZE;
        function addAuthorsPageBtn() {
            if (shownAuthors >= sorted.length) return;
            const remaining = sorted.length - shownAuthors;
            const batch = Math.min(100, remaining);
            const btn = document.createElement('button');
            btn.className = 'show-more-btn';
            btn.textContent = `Show next ${batch} (${remaining} remaining)`;
            btn.onclick = () => {
                btn.remove();
                const next = Math.min(shownAuthors + 100, sorted.length);
                table.querySelector('tbody').insertAdjacentHTML('beforeend',
                    sorted.slice(shownAuthors, next).map(_authorTableRowHTML).join(''));
                shownAuthors = next;
                addAuthorsPageBtn();
            };
            container.appendChild(btn);
        }
        addAuthorsPageBtn();
    }
}

function renderAuthorsView(authorsData, container) {
    renderAuthorsTable(authorsData, container, true);
    const legend = document.getElementById('legend');
    if (legend) legend.style.display = 'none';
    const searchCount = document.getElementById('searchCount');
    if (searchCount) searchCount.textContent = authorsData.length;
}

function downloadCurrentCSV() {
    let rows = [];
    let filename = 'twiki_';

    if (_activeView === 'all-authors') {
        let data = getAuthorsData();
        if (_currentFilter !== 'all') {
            data = data.filter(a => {
                if (_currentFilter === 'active') return a.lastYearRevisions >= 1;
                if (_currentFilter === 'inactive') return a.lastYearRevisions === 0;
                if (_currentFilter === 'prolific') return a.pagesEdited >= 50;
                if (_currentFilter === 'onepage') return a.pagesEdited === 1;
                return true;
            });
        }
        const filterPart = _currentFilter !== 'all' ? `_${_currentFilter}` : '';
        filename += `authors${filterPart}.csv`;
        rows = [
            ['Author', 'Display Name', 'Pages Edited', 'Last Activity', 'Revisions Last Year'],
            ...data.map(a => [a.author, a.displayName, a.pagesEdited, a.lastActivity, a.lastYearRevisions])
        ];
    } else {
        let entries;
        if (_isCustomSelection && _currentEntries) {
            entries = _currentEntries;
            filename = `twiki_pages_${_currentSearchSlug || 'selection'}.csv`;
        } else {
            let scopePart = 'all';
            if (_activeWeb) {
                entries = _pages.filter(e => getWebName(e.url) === _activeWeb);
                scopePart = `web_${_activeWeb}`;
            } else if (_myActiveAuthor) {
                entries = getAuthorPagesByMode(_myActiveAuthor, _authorPageMode);
                const authorSlug = displayName(_myActiveAuthor).replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '');
                const modeSlug = _authorPageMode === 'created' ? 'created' : _authorPageMode === 'most_recent' ? 'last_active' : 'all_edited';
                scopePart = `${modeSlug}_author_${authorSlug}`;
            } else {
                entries = _pages;
            }
            entries = applyFiltersAndSort(entries);
            const filterPart = _currentFilter !== 'all' ? `_${_currentFilter}` : '';
            const sortPart = _currentSort !== 'pagerank' ? `_${_currentSort.replace('-', '_')}` : '';
            filename += `pages_${scopePart}${filterPart}${sortPart}.csv`;
        }

        if (_myActiveAuthor) {
            const modeLabel = _authorPageMode === 'created' ? 'Pages Created' : _authorPageMode === 'most_recent' ? 'Last Active Author' : 'All Edited Pages';
            rows.push([`Author: ${displayName(_myActiveAuthor)} — ${modeLabel}`]);
            rows.push([]);
        }
        rows.push(['Title', 'URL', 'Web', 'Last Edit', 'Author', 'Byte Size', 'Links Out', 'Backlinks', 'Rank']);
        rows.push(...entries.map(e => [
            e.title || e.html_file || '',
            e.url,
            getWebName(e.url),
            e.date || '',
            pageDisplayName(e),
            e.byte_size || '',
            e.n_links || 0,
            e.n_backlinks || 0,
            e.pagerank_rank || ''
        ]));
    }

    const csvContent = rows
        .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
        .join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
}

function renderList(entries, container) {
    const processed = applyFiltersAndSort(entries);
    _currentEntries = processed;
    if (_viewMode === 'table') renderPagesTable(processed, container);
    else renderPagesCards(processed, container);

    const legend = document.getElementById('legend');
    if (legend) {
        legend.style.display = processed.length ? 'flex' : 'none';
    }

    const searchCount = document.getElementById('searchCount');
    if (searchCount) {
        searchCount.textContent = processed.length;
    }
}

function calcHIndex(pages) {
    const revCounts = pages
        .map(p => parseInt(p.revision) || (_historyLut[p.html_file] || []).length || 0)
        .sort((a, b) => b - a);
    let h = 0;
    for (let i = 0; i < revCounts.length; i++) {
        if (revCounts[i] >= i + 1) h = i + 1;
        else break;
    }
    return h;
}

function countAuthorRevisions(authorKey, pageList) {
    let total = 0;
    for (const p of pageList) {
        const history = _historyLut[p.html_file];
        if (history && history.length > 0) {
            total += history.filter(h => h.username === authorKey).length;
        } else if (p.author === authorKey || p.created_by === authorKey) {
            total += 1;                     // fallback for pages without history
        }
    }
    return total;
}

function getAuthorsData() {
    if (_authorStats) return _authorStats;
    const now = new Date();
    _authorStats = Object.keys(_authors).map(author => {
        const pages = _authorAllPagesIndex[author] || [];
        const totalRevisions = countAuthorRevisions(author, pages);
        const pagesActive = pages.filter(p => getAgeClass(p.date) === 'age-success').length;
        const pagesMedium = pages.filter(p => getAgeClass(p.date) === 'age-warning').length;
        const pagesOld = pages.filter(p => getAgeClass(p.date) === 'age-danger').length;
        const pctOld = pages.length > 0 ? Math.round(pagesOld / pages.length * 100) : 0;
        const hIndex = calcHIndex(pages);
        const leTs = _authorLastEditTs[author];
        const feTs = _authorFirstEditTs[author];
        const age = leTs ? (now - leTs) / (1000 * 60 * 60 * 24 * 365.25) : 999;
        const ageClass = age > 5 ? 'age-danger' : age > 2 ? 'age-warning' : 'age-success';
        return {
            author,
            displayName: displayName(author),
            pagesEdited: pages.length,
            pagesActive, pagesMedium, pagesOld, pctOld,
            totalRevisions,
            lastYearRevisions: _authorYearRevCounts[author] || 0,
            hIndex,
            authorSince: feTs ? new Date(feTs).toISOString().split('T')[0] : '—',
            lastActivity: leTs ? new Date(leTs).toISOString().split('T')[0] : '—',
            ageClass,
        };
    });
    return _authorStats;
}

function updateAuthorBannerStats(author, entries) {
    const pagesActive = entries.filter(p => getAgeClass(p.date) === 'age-success').length;
    const pagesMedium = entries.filter(p => getAgeClass(p.date) === 'age-warning').length;
    const pagesOld = entries.filter(p => getAgeClass(p.date) === 'age-danger').length;
    const total = entries.length || 1;

    // === NEW: pages that actually have revision history ===
    const pagesWithHistory = entries.filter(p => {
        const hist = _historyLut[p.html_file];
        return Array.isArray(hist) && hist.length > 0;
    }).length;

    // Update the stat BEFORE the "Pages" button
    const histNum = document.getElementById('authorHistNum');
    const histTotal = document.getElementById('authorHistTotal');
    if (histNum) histNum.textContent = pagesWithHistory;
    if (histTotal) histTotal.textContent = total;

    // FIXED: only count revisions THIS author actually made
    const totalRevisions = countAuthorRevisions(author, entries);
    const leTs = _authorLastEditTs[author];
    const feTs = _authorFirstEditTs[author];
    const lastStr = leTs ? new Date(leTs).toISOString().split('T')[0] : '—';
    const sinceStr = feTs ? new Date(feTs).toISOString().split('T')[0] : '—';
    const hIndex = calcHIndex(entries);

    const bannerBands = document.getElementById('authorBannerBands');
    const bannerCounts = document.getElementById('authorBannerCounts');
    bannerBands.innerHTML = `
    <div class="band-success" style="flex:${pagesActive}"></div>
    <div class="band-warning" style="flex:${pagesMedium}"></div>
    <div class="band-danger" style="flex:${pagesOld + (total - pagesActive - pagesMedium - pagesOld)}"></div>`;

    bannerCounts.innerHTML = `
    <span class="bc bc-success"><span class="dot"></span><span class="bc-num">${pagesActive}</span> active</span>
    <span class="bc bc-warning"><span class="dot"></span><span class="bc-num">${pagesMedium}</span> 2–5yr</span>
    <span class="bc bc-danger"><span class="dot"></span><span class="bc-num">${pagesOld}</span> >5yr</span>
    <span class="bc" style="margin-left:auto;color:var(--text-dim);">Last: ${escHtml(lastStr)}</span>
</div>`;
}

function getAuthorPagesByMode(author, mode) {
    // Created: pages where author is explicitly the creator (from author_created_pages_lut)
    if (mode === 'created') {
        const createdPages = _authorCreatedPagesLut[author] || [];
        const createdSet = new Set(createdPages);
        return _pages.filter(e => createdSet.has(e.html_file));
    }

    // Most Recent: pages where author is the most recent editor (from _authorsMostRecentPages)
    if (mode === 'most_recent') {
        const mostRecentPages = _authorsMostRecentPages[author] || [];
        const mostRecentSet = new Set(mostRecentPages);
        return _pages.filter(e => mostRecentSet.has(e.html_file));
    }

    // Revised: pages where author has ≥1 history entry
    const revisedSet = new Set();
    _pages.forEach(p => {
        const _ph = _historyLut[p.html_file];
        if (_ph?.some(h => h.username === author)) revisedSet.add(p.html_file);
    });
    const revised = _pages.filter(e => revisedSet.has(e.html_file));

    if (mode === 'revised') return revised;

    // 'all': pages where author created OR revised
    const createdPages = _authorCreatedPagesLut[author] || [];
    const createdSet = new Set(createdPages);
    const allPages = new Set([...createdSet, ...revisedSet]);
    return _pages.filter(e => allPages.has(e.html_file));
}

function setAuthorPageMode(author, mode) {
    _authorPageMode = mode;
    document.querySelectorAll('.author-filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    const entries = getAuthorPagesByMode(author, mode);

    updateAuthorBannerStats(author, entries);
    _authorSparkEntries = entries;   // still needed for future metric/mode switches

    // Just render — let renderAuthorSparkline() handle counting when needed
    renderAuthorSparkline(author, entries);

    const modeLabel = mode === 'created' ? 'created' : mode === 'revised' ? 'revised' : mode === 'most_recent' ? 'as most recent' : 'total';
    setPageTitle(
        `Author: ${escHtml(displayName(author))}`,
        `${entries.length} pages ${modeLabel}`
    );
    renderList(entries, document.getElementById('content'));
}

function showAuthor(author) {
    clearTimeout(_searchTmo);
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    _isCustomSelection = false;
    _currentSearchSlug = '';
    _selectionBannerToken++;
    if (_activeView !== 'author') {
        _currentSort = 'pagerank';
        _currentFilter = 'all';
        _viewMode = 'card';
        document.getElementById('sortSelect').value = 'pagerank';
        document.getElementById('viewSelect').value = 'card';
    }
    const viewModeControl = document.getElementById('viewModeControl');
    if (viewModeControl) viewModeControl.style.display = 'none';
    _setAuthorSortOptions(false);
    updateFilterOptions(FILTER_OPTIONS_PAGES, 'all', 'Filter pages:');
    _activeView = 'author';
    _myActiveAuthor = author;
    _activeWeb = null;
    const auth = _authors[author];
    if (!auth) return;

    document.getElementById('authorBanner').style.display = 'block';
    _authorSparkName = author;
    _authorBannerMetric = 'revisions';
    _authorBannerMode = 'yearly';

    // Use pre-built indexes — avoids O(pages × history) scan on every author click
    const allEntries = _authorAllPagesIndex[author] || [];

    // Created: pages explicitly from author_created_pages_lut
    const createdPages = _authorCreatedPagesLut[author] || [];
    const createdEntries = _pages.filter(e => createdPages.includes(e.html_file));
    const createdSet = new Set(createdEntries.map(p => p.html_file));

    // Revised: pages with edits but NOT created by this author
    const revisedEntries = allEntries.filter(p => !createdSet.has(p.html_file));

    _authorSparkEntries = allEntries;
    // Author view: show only the author sparkline, hide the all-pages banner
    document.getElementById('allPagesBanner').style.display = 'none';
    // Defer sparkline so the page list renders first (non-blocking)
    requestAnimationFrame(() => renderAuthorSparkline(author, _authorSparkEntries));

    // Calculate pages where this author is the most recent editor
    const mostRecentPages = getAuthorPagesByMode(author, 'most_recent');

    // Render filter buttons — three modes
    const filterBar = document.getElementById('authorFilterBar');
    if (!filterBar) return;
    filterBar.innerHTML = `
    <button class="author-filter-btn ${_authorPageMode === 'all' ? 'active' : ''}"
      data-mode="all" data-author="${escHtml(author)}">
       <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pencil-icon lucide-pencil"><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/><path d="m15 5 4 4"/></svg>All Edited Pages<span class="filter-count">${allEntries.length}</span>
    </button>
    <button class="author-filter-btn ${_authorPageMode === 'most_recent' ? 'active' : ''}"
      data-mode="most_recent" data-author="${escHtml(author)}">
     <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-type-icon lucide-file-type"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M11 18h2"/><path d="M12 12v6"/><path d="M9 13v-.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 .5.5v.5"/></svg>Last Active Author<span class="filter-count">${mostRecentPages.length}</span>
    </button>
    <button class="author-filter-btn ${_authorPageMode === 'created' ? 'active' : ''}"
      data-mode="created" data-author="${escHtml(author)}">
     <svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-type-icon lucide-file-type"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M11 18h2"/><path d="M12 12v6"/><path d="M9 13v-.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 .5.5v.5"/></svg>Created by<span class="filter-count">${createdEntries.length}</span>
    </button>`;

    // Show progress bar and page list for current mode
    const activeEntries = _authorPageMode === 'created' ? createdEntries
        : _authorPageMode === 'revised' ? revisedEntries
            : _authorPageMode === 'most_recent' ? mostRecentPages
                : allEntries;
    updateAuthorBannerStats(author, activeEntries);
    document.getElementById('content').style.display = 'block';
    const modeLabel = _authorPageMode === 'created' ? 'created' : _authorPageMode === 'revised' ? 'revised' : _authorPageMode === 'most_recent' ? 'as most recent' : 'total';
    setPageTitle(
        `Author: ${escHtml(displayName(author))}`,
        `${activeEntries.length} pages ${modeLabel}`
    );
    renderList(activeEntries, document.getElementById('content'));
}



function renderAuthorSparkline(author, entries, metric, mode) {
    if (metric) _authorBannerMetric = metric;
    if (mode) _authorBannerMode = mode;
    metric = _authorBannerMetric;
    mode = _authorBannerMode;

    const wrap = document.getElementById('authorSparkline');
    if (!wrap) return;

    const LABEL_MAP = {
        pages_yearly: { label: 'Pages Shown', color: 'var(--atlas-blue)' },
        pages_cumulative: { label: 'Pages Shown', color: 'var(--atlas-blue)' },
        revisions_yearly: { label: 'Revisions Shown', color: 'var(--atlas-green)' },
        revisions_cumulative: { label: 'Revisions Shown', color: 'var(--atlas-green)' },
    };

    const cache = _authorPageMode === 'all' && _authorSparkCache[author];

    if (cache) {
        // === FAST PATH (cached data) ===
        const key = `${metric}_${mode}`;
        const cfg = LABEL_MAP[key] || LABEL_MAP.revisions_yearly;
        let vals = cache[key] || cache.revisions_yearly;

        const bgVals = (metric === 'revisions' && mode === 'yearly')
            ? cache.years.map(y => _peteRevsByYear[y] || 0)
            : null;

        // FIXED: for cumulative mode, show the FINAL total only (no double-counting)
        const totalOverride = (mode === 'cumulative') ? vals[vals.length - 1] : null;

        _renderSparkSVG(wrap, cache.years, vals, cfg.color, cfg.label, '', bgVals, totalOverride);
    } else {
        // === SLOW PATH (on-the-fly for 'created' / 'revised' modes) ===
        const startYear = 2005;
        const endYear = new Date().getFullYear();
        const years = [];
        for (let y = startYear; y <= endYear; y++) years.push(y);

        const revByYear = {}, pagesCreatedByYear = {}, pagesLastEditedByYear = {}, peteRevByYear = {};
        years.forEach(y => {
            revByYear[y] = 0;
            pagesCreatedByYear[y] = 0;
            pagesLastEditedByYear[y] = 0;
            peteRevByYear[y] = 0;
        });

        entries.forEach(p => {
            const _ph = _historyLut[p.html_file];
            if (!_ph?.length) return;

            // For 'most_recent' mode: count when they became the most recent editor
            if (_authorPageMode === 'most_recent' && _pageToMostRecentAuthor[p.html_file] === author) {
                const lastRevY = dateYear(_ph[_ph.length - 1]?.date);
                if (lastRevY && pagesLastEditedByYear[lastRevY] !== undefined) pagesLastEditedByYear[lastRevY]++;
            }

            // For 'created' mode: count pages they actually created (from _authorCreatedPagesLut)
            if (_authorPageMode === 'created') {
                const createdPages = _authorCreatedPagesLut[author] || [];
                if (createdPages.includes(p.html_file)) {
                    const firstRev = _ph[0];
                    const cy = dateYear(firstRev?.date);
                    if (cy && pagesCreatedByYear[cy] !== undefined) pagesCreatedByYear[cy]++;
                }
            }

            _ph.forEach(h => {
                const y = dateYear(h.date);
                if (h.username === MASS_EDIT_USER && y && peteRevByYear[y] !== undefined) peteRevByYear[y]++;
                if (h.username !== author) return;
                if (y && revByYear[y] !== undefined) revByYear[y]++;
            });
        });

        let cumPages = 0, cumRevs = 0;
        const cumPagesMap = {}, cumRevsMap = {};
        const pagesMetric = _authorPageMode === 'most_recent' ? pagesLastEditedByYear : pagesCreatedByYear;
        years.forEach(y => {
            cumPages += pagesMetric[y] || 0;
            cumRevs += revByYear[y] || 0;
            cumPagesMap[y] = cumPages;
            cumRevsMap[y] = cumRevs;
        });

        const AUTHOR_METRIC_MAP = {
            pages: { yearly: { getData: y => pagesMetric[y] || 0 }, cumulative: { getData: y => cumPagesMap[y] || 0 } },
            revisions: { yearly: { getData: y => revByYear[y] || 0 }, cumulative: { getData: y => cumRevsMap[y] || 0 } },
        };

        const key = `${metric}_${mode}`;
        const cfg = LABEL_MAP[key] || LABEL_MAP.revisions_yearly;
        const getData = (AUTHOR_METRIC_MAP[metric] || AUTHOR_METRIC_MAP.revisions)[mode]?.getData
            || AUTHOR_METRIC_MAP.revisions.yearly.getData;

        let vals = years.map(getData);

        const bgVals = (metric === 'revisions' && mode === 'yearly')
            ? years.map(y => peteRevByYear[y] || 0)
            : null;

        // FIXED: for cumulative mode, show the FINAL total only (no double-counting)
        const totalOverride = (mode === 'cumulative') ? vals[vals.length - 1] : null;

        _renderSparkSVG(wrap, years, vals, cfg.color, cfg.label, '', bgVals, totalOverride);
    }

    // Update active buttons (unchanged)
    document.querySelectorAll('#authorBanner .metric-btn').forEach(b =>
        b.classList.toggle('active', b.dataset.metric === metric));
    document.querySelectorAll('#authorBanner .mode-btn').forEach(b =>
        b.classList.toggle('active', b.dataset.mode === mode));
}

function _hideBanner() {
    document.getElementById('authorBanner').style.display = 'none';
    document.getElementById('allPagesBanner').style.display = 'none';
}

function _resetAuthorInput() {
    const inp = document.getElementById('authorSearchInput');
    const sug = document.getElementById('authorSuggestions');
    if (inp) inp.value = '';
    if (sug) sug.style.display = 'none';
}

function _setAuthorSortOptions(visible) {
    const authorOnly = ['pctOld-desc', 'hIndex-desc', 'pages-desc', 'revisions-desc', 'lastActive-desc'];
    const pagesOnly = ['pagerank', 'title-asc', 'title-desc', 'date-desc', 'date-asc'];
    document.querySelectorAll('#sortSelect .authors-only').forEach(o => { o.style.display = visible ? '' : 'none'; });
    document.querySelectorAll('#sortSelect .pages-sort').forEach(o => { o.style.display = visible ? 'none' : ''; });
    if (visible && pagesOnly.includes(_currentSort)) {
        _currentSort = 'pages-desc';
        document.getElementById('sortSelect').value = 'pages-desc';
    }
    if (!visible && authorOnly.includes(_currentSort)) {
        _currentSort = 'pagerank';
        document.getElementById('sortSelect').value = 'pagerank';
    }
}

function showAll() {
    _authorPageMode = 'all';
    _isCustomSelection = false;
    _selectionBannerToken++;
    const viewModeControl = document.getElementById('viewModeControl');
    if (viewModeControl) {
        viewModeControl.style.display = 'block';
        document.getElementById('viewSelect').value = _viewMode;
    }
    updateFilterOptions(FILTER_OPTIONS_PAGES, 'all', 'Filter pages:');
    _setAuthorSortOptions(false);
    _activeView = 'pages';
    _activeWeb = null;
    _myActiveAuthor = null;
    _hideBanner();
    _resetAuthorInput();
    document.getElementById('allPagesBanner').style.display = 'block';
    _bannerMetric = 'pages';
    _bannerMode = 'yearly';
    _bannerYearData = null;
    _bannerPeteData = null;
    renderAllPagesBanner();
    document.getElementById('welcome').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    setPageTitle('All TWiki Pages', `${_pages.length} pages`);
    renderList(_pages, document.getElementById('content'));
}

function showWeb(web) {
    _authorPageMode = 'all';
    const viewModeControl = document.getElementById('viewModeControl');
    if (viewModeControl) {
        viewModeControl.style.display = 'block';
        document.getElementById('viewSelect').value = _viewMode;
    }
    updateFilterOptions(FILTER_OPTIONS_PAGES, 'all', 'Filter pages:');
    _setAuthorSortOptions(false);
    _activeView = 'web';
    _activeWeb = web;
    _myActiveAuthor = null;
    _hideBanner();
    _resetAuthorInput();
    const entries = _pages.filter(e => getWebName(e.url) === web);
    const webData = _buildPagesYearData(_pages.filter(e => getWebName(e.url) === web));
    _bannerYearData = webData.yearBuckets;
    _bannerPeteData = webData.peteRevsByYear;
    _bannerMetric = 'revisions';
    _bannerMode = 'yearly';
    document.getElementById('allPagesBanner').style.display = 'block';
    renderAllPagesBanner();
    document.getElementById('welcome').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    setPageTitle(`Web: ${web}`, `${entries.length} pages`);
    renderList(entries, document.getElementById('content'));
}

function showAllAuthors() {
    _authorPageMode = 'all';
    if (_activeView !== 'all-authors' && _activeView !== 'author') {
        _currentSort = 'pagerank';
        _currentFilter = 'all';
        document.getElementById('sortSelect').value = 'pagerank';
    }
    updateFilterOptions(FILTER_OPTIONS_AUTHORS, 'all', 'Filter authors:');
    _setAuthorSortOptions(true);
    const viewModeControl = document.getElementById('viewModeControl');
    if (viewModeControl) viewModeControl.style.display = 'none';
    _activeView = 'all-authors';
    _activeWeb = null;
    _myActiveAuthor = null;
    _hideBanner();
    document.getElementById('welcome').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    setPageTitle('All TWiki Authors', `${Object.keys(_authors).length} authors`);

    let data = getAuthorsData();
    if (_currentFilter !== 'all') {
        data = data.filter(a => {
            if (_currentFilter === 'active') return a.lastYearRevisions >= 1;
            if (_currentFilter === 'inactive') return a.lastYearRevisions === 0;
            if (_currentFilter === 'prolific') return a.pagesEdited >= 50;
            if (_currentFilter === 'onepage') return a.pagesEdited === 1;
            return true;
        });
    }
    if (_currentSort === 'pctOld-desc') {
        data = [...data].sort((a, b) => b.pctOld - a.pctOld);
    } else if (_currentSort === 'hIndex-desc') {
        data = [...data].sort((a, b) => b.hIndex - a.hIndex);
    } else if (_currentSort === 'pages-desc') {
        data = [...data].sort((a, b) => b.pagesEdited - a.pagesEdited);
    } else if (_currentSort === 'revisions-desc') {
        data = [...data].sort((a, b) => b.totalRevisions - a.totalRevisions);
    } else if (_currentSort === 'lastActive-desc') {
        data = [...data].sort((a, b) => (b.lastActivity === '—' ? '' : b.lastActivity).localeCompare(a.lastActivity === '—' ? '' : a.lastActivity));
    }
    renderAuthorsView(data, document.getElementById('content'));
}

function rerenderCurrentView() {
    if (_activeView === 'pages') showAll();
    else if (_activeView === 'web') showWeb(_activeWeb);
    else if (_activeView === 'author') showAuthor(_myActiveAuthor);
    else if (_activeView === 'all-authors') showAllAuthors();
}

const FILTER_OPTIONS_PAGES = [
    { value: 'all', text: 'All' },
    { value: 'recent', text: 'Recently updated' },
    { value: 'medium', text: '2–5 years' },
    { value: 'old', text: '>5 years' },
    { value: 'editor-inactive', text: 'Editor inactive 5yr+' },
];
const FILTER_OPTIONS_AUTHORS = [
    { value: 'all', text: 'All authors' },
    { value: 'active', text: 'Active last year' },
    { value: 'inactive', text: 'Inactive last year' },
    // { value: 'prolific', text: 'Prolific (≥50 pages)' },
    // { value: 'onepage', text: 'One-page authors' }
];

function updateFilterOptions(optionsArray, defaultValue = 'all', labelText = 'Filter:') {
    const select = document.getElementById('filterSelect');
    const label = document.getElementById('filterLabel');
    select.innerHTML = '';
    optionsArray.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.value;
        el.textContent = opt.text;
        select.appendChild(el);
    });
    select.value = _currentFilter || defaultValue;
    _currentFilter = select.value;
    label.textContent = labelText;
    select.onchange = () => { _currentFilter = select.value; rerenderCurrentView(); };
}

function setPageTitle(title, subtitle = '') {
    document.getElementById('pageTitle').textContent = title;
    document.getElementById('pageSubtitle').textContent = subtitle;
}

function renderSearch(query) {
    const q = query.trim();
    if (!q) { showAll(); return; }
    if (!_fusePages) return;
    const countEl = document.getElementById('searchCount');
    if (countEl) countEl.textContent = '…';
    setPageTitle('Searching...', `"${escHtml(q)}"`);
    const searchResults = _fusePages.search(q, { limit: 800 });
    let items = searchResults.map(r => r.item);
    items.sort((a, b) => (a.pagerank_rank || 9999) - (b.pagerank_rank || 9999));
    const count = items.length;
    recordSearch(q, count);
    if (countEl) countEl.textContent = count;
    setPageTitle('Search Results', `"${escHtml(q)}" — ${count} matches ${count >= 800 ? '(showing top 800)' : ''}`);
    document.getElementById('welcome').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.getElementById('authorBanner').style.display = 'none';
    document.getElementById('allPagesBanner').style.display = 'block';
    _isCustomSelection = true;
    _currentSearchSlug = q.trim().replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '').toUpperCase();
    renderList(items, document.getElementById('content'));
    const token = ++_selectionBannerToken;
    const captured = items.slice();
    setTimeout(() => {
        if (_selectionBannerToken !== token) return;
        const data = _buildPagesYearData(captured);
        _bannerYearData = data.yearBuckets;
        _bannerPeteData = data.peteRevsByYear;
        renderAllPagesBanner();
    }, 0);
}

const _searchAnalytics = {
    queries: {},
    session: 0,
};

function recordSearch(term, resultCount) {
    if (!term) return;
    const t = term.toLowerCase().trim();
    if (!_searchAnalytics.queries[t]) {
        _searchAnalytics.queries[t] = { count: 0, totalResults: 0, lastTs: 0 };
    }
    const q = _searchAnalytics.queries[t];
    q.count++;
    q.totalResults += resultCount;
    q.lastTs = Date.now();
    _searchAnalytics.session++;
}

function showAnalytics() {
    const modal = document.getElementById('analytics-modal');
    const content = document.getElementById('analyticsContent');
    const entries = Object.entries(_searchAnalytics.queries)
        .map(([term, d]) => ({ term, ...d, avgResults: d.totalResults / d.count }))
        .sort((a, b) => b.count - a.count);

    const totalSearches = _searchAnalytics.session;
    const uniqueTerms = entries.length;
    const zeroResults = entries.filter(e => e.avgResults < 0.5);
    const maxCount = entries[0]?.count || 1;

    content.innerHTML = `
    <div class="analytics-kpi-row">
      <div class="analytics-kpi"><div class="kpi-val">${totalSearches}</div><div class="kpi-label">Total searches</div></div>
      <div class="analytics-kpi"><div class="kpi-val">${uniqueTerms}</div><div class="kpi-label">Unique terms</div></div>
      <div class="analytics-kpi"><div class="kpi-val">${zeroResults.length}</div><div class="kpi-label">Zero-result queries</div></div>
    </div>
    <div class="analytics-section">
      <h4>Top queries <span class="analytics-clear" onclick="clearAnalytics()">Clear all</span></h4>
      ${entries.length === 0 ? '<div style="color:var(--text-dim);font-size:13px;">No searches yet — try the search box.</div>' :
            entries.slice(0, 20).map(e => `
          <div class="query-row">
            <span class="query-term" onclick="replaySearch('${e.term.replace(/'/g, "\\'")}'); closeAnalytics();">${escHtml(e.term)}</span>
            <div class="query-bar-wrap"><div class="query-bar" style="width:${Math.round(e.count / maxCount * 100)}%"></div></div>
            <span class="query-count">${e.count}×</span>
            <span class="query-results ${e.avgResults < 0.5 ? 'zero' : ''}">${Math.round(e.avgResults)} results</span>
          </div>`).join('')}
    </div>
    ${zeroResults.length > 0 ? `
    <div class="analytics-section zero-queries">
      <h4>Zero-result queries</h4>
      ${zeroResults.slice(0, 12).map(e => `
        <div class="query-row">
          <span class="query-term" onclick="replaySearch('${e.term.replace(/'/g, "\\'")}'); closeAnalytics();">${escHtml(e.term)}</span>
          <span class="query-count">${e.count}×</span>
          <span class="query-results zero">0 results</span>
        </div>`).join('')}
    </div>` : ''}
  `;
    modal.style.display = 'flex';
}

function closeAnalytics() {
    document.getElementById('analytics-modal').style.display = 'none';
}

function clearAnalytics() {
    _searchAnalytics.queries = {};
    _searchAnalytics.session = 0;
    showAnalytics();
}

function replaySearch(term) {
    const input = document.getElementById('searchInput');
    input.value = term;
    renderSearch(term);
}





const HISTO_FIELD_META = {
    byte_size: { label: 'Byte Size', unit: 'bytes', fmt: v => v >= 1024 ? (v / 1024).toFixed(1) + 'K' : String(v) },
    n_links: { label: 'Outgoing Links', unit: 'links', fmt: v => String(v) },
    n_backlinks: { label: 'Backlinks', unit: 'links', fmt: v => String(v) },
    total_revisions: {
        label: 'Total Revisions', unit: '', fmt: v => String(v),
        derive: e => parseInt(e.revision) || (_historyLut[e.html_file] || []).length || 0
    },
    pagerank: { label: 'PageRank Value', unit: '', fmt: v => v.toExponential(2) },
    betweenness: { label: 'Betweenness Centrality', unit: '', fmt: v => v.toExponential(2) },
};

let _histoField = null;
let _histoValues = [];
let _histoLogMode = false;

function showHistogram(field) {
    let entries = [];
    if (_activeWeb) entries = _pages.filter(e => getWebName(e.url) === _activeWeb);
    else if (_myActiveAuthor) entries = _pages.filter(e => e.author === _myActiveAuthor || e.created_by === _myActiveAuthor);
    else entries = _pages;

    const meta = HISTO_FIELD_META[field] || { label: field, unit: '', fmt: v => String(v) };
    const values = entries
        .map(e => meta.derive ? meta.derive(e) : e[field])
        .filter(v => typeof v === 'number' && isFinite(v) && v >= 0);

    if (values.length === 0) {
        alert('No numeric data available for this field in the current view.');
        return;
    }

    _histoField = field;
    _histoValues = values;
    _histoLogMode = document.getElementById('histoLogScale')?.checked || false;
    document.getElementById('histogramTitle').textContent = meta.label + ' Distribution';

    const sorted = [...values].sort((a, b) => a - b);
    const sum = values.reduce((a, b) => a + b, 0);
    const mean = sum / values.length;
    const median = sorted[Math.floor(sorted.length / 2)];
    const p95 = sorted[Math.floor(sorted.length * 0.95)];
    const min = sorted[0], max = sorted[sorted.length - 1];

    document.getElementById('histogramSubtitle').textContent = `n = ${values.length.toLocaleString()}`;
    document.getElementById('histogramStats').innerHTML = [
        `<span><strong>Min</strong> ${meta.fmt(min)}</span>`,
        `<span><strong>Median</strong> ${meta.fmt(median)}</span>`,
        `<span><strong>Mean</strong> ${meta.fmt(+mean.toFixed(2))}</span>`,
        `<span><strong>P95</strong> ${meta.fmt(p95)}</span>`,
        `<span><strong>Max</strong> ${meta.fmt(max)}</span>`,
    ].join('');

    renderHistoSVG();
    document.querySelector('.histo-log-toggle').style.display = '';
    const leg = document.getElementById('histoLegend');
    if (leg) { leg.style.display = 'none'; leg.innerHTML = ''; }
    document.getElementById('histogram-modal').style.display = 'flex';
}

function renderHistoSVG() {
    const wrap = document.getElementById('histoSvgWrap');
    const field = _histoField;
    const meta = HISTO_FIELD_META[field] || { label: field, unit: '', fmt: v => v };
    const values = _histoValues;
    const logMode = _histoLogMode;

    const k = Math.min(30, Math.max(8, Math.ceil(1 + Math.log2(values.length))));
    const rawMin = Math.min(...values);
    const rawMax = Math.max(...values);
    const span = rawMax - rawMin || 1;
    const binW = span / k;

    const bins = Array.from({ length: k }, (_, i) => ({
        lo: rawMin + i * binW,
        hi: rawMin + (i + 1) * binW,
        count: 0,
    }));
    values.forEach(v => {
        let i = Math.floor((v - rawMin) / binW);
        if (i >= k) i = k - 1;
        bins[i].count++;
    });

    const maxCount = Math.max(...bins.map(b => b.count));
    const W = 740, H = 300;
    const pad = { top: 16, right: 20, bottom: 52, left: 52 };
    const chartW = W - pad.left - pad.right;
    const chartH = H - pad.top - pad.bottom;
    const barW = chartW / k;

    function yScale(count) {
        if (count === 0) return chartH;
        if (logMode) {
            const logMax = Math.log1p(maxCount);
            return chartH - (Math.log1p(count) / logMax) * chartH;
        }
        return chartH - (count / maxCount) * chartH;
    }

    const yTicks = [];
    const tickCount = 5;
    for (let i = 0; i <= tickCount; i++) {
        const val = logMode
            ? Math.round(Math.expm1((i / tickCount) * Math.log1p(maxCount)))
            : Math.round((i / tickCount) * maxCount);
        yTicks.push({ y: chartH - (i / tickCount) * chartH, val });
    }

    const bars = bins.map((b, i) => {
        const bh = chartH - yScale(b.count);
        const x = i * barW;
        const y = yScale(b.count);
        return `<rect class="histo-bar" x="${x + 1}" y="${y}" width="${barW - 2}" height="${bh}"
      data-lo="${meta.fmt(+b.lo.toFixed(4))}" data-hi="${meta.fmt(+b.hi.toFixed(4))}" data-count="${b.count}" />`;
    }).join('');

    const xLabelStep = Math.ceil(k / 6);
    const xLabels = bins.filter((_, i) => i % xLabelStep === 0).map((b, li) => {
        const i = li * xLabelStep;
        const x = i * barW + barW / 2;
        return `<text x="${x}" y="${chartH + 18}" text-anchor="middle" class="histo-tick" style="font-size:10px;fill:var(--text-muted)">${meta.fmt(+b.lo.toFixed(2))}</text>`;
    }).join('');

    const yTicksSVG = yTicks.map(t => `
    <line x1="-5" y1="${t.y}" x2="${chartW}" y2="${t.y}" stroke="var(--border)" stroke-width="1" fill="none"/>
    <text x="-8" y="${t.y + 4}" text-anchor="end" class="histo-tick" style="font-size:10px;fill:var(--text-muted)">${t.val}</text>
  `).join('');

    const svg = `<svg class="histo-svg" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(${pad.left},${pad.top})">
      ${yTicksSVG}
      ${bars}
      <line x1="0" y1="0" x2="0" y2="${chartH}" stroke="var(--border)" stroke-width="1"/>
      <line x1="0" y1="${chartH}" x2="${chartW}" y2="${chartH}" stroke="var(--border)" stroke-width="1"/>
      ${xLabels}
      <text x="${chartW / 2}" y="${chartH + 42}" text-anchor="middle" class="histo-label" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">${meta.label}${meta.unit ? ' (' + meta.unit + ')' : ''}</text>
      <text x="-36" y="${chartH / 2}" text-anchor="middle" transform="rotate(-90,-36,${chartH / 2})" class="histo-label" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">Count${logMode ? ' (log)' : ''}</text>
    </g>
  </svg>`;

    wrap.innerHTML = svg;

    const tooltip = document.getElementById('histoTooltip');
    wrap.querySelectorAll('.histo-bar').forEach(rect => {
        rect.addEventListener('mouseenter', e => {
            tooltip.textContent = `${rect.dataset.lo} – ${rect.dataset.hi}: ${parseInt(rect.dataset.count).toLocaleString()} pages`;
            tooltip.style.opacity = '1';
        });
        rect.addEventListener('mousemove', e => {
            const r = wrap.getBoundingClientRect();
            tooltip.style.left = (e.clientX - r.left + 12) + 'px';
            tooltip.style.top = (e.clientY - r.top - 28) + 'px';
        });
        rect.addEventListener('mouseleave', () => { tooltip.style.opacity = '0'; });
    });
}

function closeHistogram() {
    document.getElementById('histogram-modal').style.display = 'none';
    const leg = document.getElementById('histoLegend');
    if (leg) { leg.style.display = 'none'; leg.innerHTML = ''; }
    _histoField = null;
    _histoValues = [];
}

function showTimeSeries(seriesKey) {
    const now = new Date();
    const currentYear = now.getFullYear();
    const years = {};
    const authorFirstYear = {};

    _pages.forEach(page => {
        const _ph = _historyLut[page.html_file];
        const createdDate = _ph?.length
            ? _ph.reduce((min, h) => h.date < min ? h.date : min, _ph[0].date)
            : page.date;
        const cy = dateYear(createdDate);
        if (cy && cy >= 1990 && cy <= currentYear) {
            if (!years[cy]) years[cy] = { pages: 0, revisions: 0, authorSet: new Set(), activeAuthorSet: new Set(), intervalSums: [], intervalAll: [] };
            years[cy].pages++;
        }

        if (_ph && _ph.length >= 2) {
            const sorted = [..._ph]
                .map(h => new Date(h.date.split(' - ')[0]))
                .filter(d => !isNaN(d))
                .sort((a, b) => a - b);
            const intervals = [];
            for (let i = 1; i < sorted.length; i++) {
                const days = (sorted[i] - sorted[i - 1]) / 86400000;
                if (days >= 0) intervals.push(days);
            }
            const pageYear = dateYear(page.date);
            if (pageYear && pageYear >= 1990 && pageYear <= currentYear) {
                if (!years[pageYear]) years[pageYear] = { pages: 0, revisions: 0, authorSet: new Set(), activeAuthorSet: new Set(), intervalSums: [], intervalAll: [] };
                years[pageYear].intervalSums.push(...intervals);
                years[pageYear].intervalAll.push(intervals);
            }
        }

        if (_ph?.length) {
            _ph.forEach(h => {
                const ry = dateYear(h.date);
                if (!ry || ry < 1990 || ry > currentYear) return;
                if (!years[ry]) years[ry] = { pages: 0, revisions: 0, authorSet: new Set(), activeAuthorSet: new Set(), intervalSums: [], intervalAll: [] };
                years[ry].revisions++;
                if (h.username) {
                    years[ry].authorSet.add(h.username);
                    if (!authorFirstYear[h.username] || ry < authorFirstYear[h.username]) {
                        authorFirstYear[h.username] = ry;
                    }
                }
            });
        }
    });

    const sortedYears = Object.keys(years).map(Number).sort((a, b) => a - b);
    if (sortedYears.length === 0) { alert('No date data available.'); return; }

    const cumulativeByYear = {};
    sortedYears.forEach(y => {
        cumulativeByYear[y] = Object.values(authorFirstYear).filter(fy => fy <= y).length;
    });

    function calcAvgInterval(y) {
        const all = years[y].intervalSums;
        if (!all.length) return 0;
        return all.reduce((s, v) => s + v, 0) / all.length;
    }
    function calcModeInterval(y) {
        const all = years[y].intervalSums;
        if (!all.length) return 0;
        const binW = 7;
        const freq = {};
        all.forEach(v => {
            const b = Math.floor(v / binW);
            freq[b] = (freq[b] || 0) + 1;
        });
        const modeB = Object.keys(freq).reduce((best, k) => freq[k] > freq[best] ? k : best, Object.keys(freq)[0]);
        return (+modeB * binW) + binW / 2;
    }
    function calcRevPerPage(y) {
        const p = years[y].pages;
        if (!p) return 0;
        return years[y].revisions / p;
    }

    const newAuthorsByYear = {};
    sortedYears.forEach(y => { newAuthorsByYear[y] = 0; });
    Object.values(authorFirstYear).forEach(fy => {
        if (newAuthorsByYear[fy] !== undefined) newAuthorsByYear[fy]++;
    });

    const SERIES_CONFIG = {
        pages: { label: 'Pages Created per Year', color: 'var(--atlas-blue)', yLabel: 'Pages', fmt: v => v.toFixed(0), val: y => years[y].pages },
        revisions: { label: 'Revisions per Year', color: 'var(--atlas-green)', yLabel: 'Revisions', fmt: v => v.toFixed(0), val: y => years[y].revisions },
        authors: { label: 'Active Authors per Year', color: 'var(--atlas-orange)', yLabel: 'Authors', fmt: v => v.toFixed(0), val: y => years[y].authorSet.size },
        new_authors: { label: 'New Authors per Year', color: 'var(--atlas-purple, #8b5cf6)', yLabel: 'New Authors', fmt: v => v.toFixed(0), val: y => newAuthorsByYear[y] || 0 },
        active_authors: { label: 'Cumulative Authors Over Time', color: 'var(--atlas-red)', yLabel: 'Authors', fmt: v => v.toFixed(0), val: y => cumulativeByYear[y] || 0 },
        avg_interval: { label: 'Avg Revision Interval per Page', color: 'var(--atlas-blue)', yLabel: 'Days (avg)', fmt: v => v.toFixed(1), val: y => calcAvgInterval(y) },
        mode_interval: { label: 'Mode Revision Interval per Page', color: 'var(--atlas-green)', yLabel: 'Days (mode)', fmt: v => v.toFixed(0), val: y => calcModeInterval(y) },
        rev_per_page: { label: 'Revisions per Page per Year', color: 'var(--atlas-orange)', yLabel: 'Rev / page', fmt: v => v.toFixed(2), val: y => calcRevPerPage(y) },
    };
    const cfg = SERIES_CONFIG[seriesKey] || SERIES_CONFIG.pages;
    const dataPoints = sortedYears.map(y => ({ year: y, val: cfg.val(y) }));
    const maxVal = Math.max(...dataPoints.map(d => d.val), 1);

    const nonZero = dataPoints.filter(d => d.val > 0);
    const avgVal = nonZero.length ? nonZero.reduce((s, d) => s + d.val, 0) / nonZero.length : 0;
    const peak = dataPoints.reduce((best, d) => d.val > best.val ? d : best, dataPoints[0]);

    document.getElementById('histogramTitle').textContent = cfg.label;
    document.getElementById('histogramSubtitle').textContent = `${sortedYears[0]}–${sortedYears[sortedYears.length - 1]}`;
    document.getElementById('histogramStats').innerHTML = [
        `<span><strong>Years</strong> ${sortedYears.length}</span>`,
        `<span><strong>Avg</strong> ${cfg.fmt(avgVal)}</span>`,
        `<span><strong>Peak</strong> ${cfg.fmt(peak.val)} (${peak.year})</span>`,
    ].join('');

    const W = 740, H = 300;
    const pad = { top: 20, right: 24, bottom: 50, left: 58 };
    const cW = W - pad.left - pad.right;
    const cH = H - pad.top - pad.bottom;
    const n = dataPoints.length;
    const barW = Math.max(2, cW / n - 1);

    function xPos(i) { return i * (cW / n) + barW / 2; }
    function yPos(v) { return cH - (v / maxVal) * cH; }

    const yTickCount = 5;
    const yTicks = Array.from({ length: yTickCount + 1 }, (_, i) => ({
        y: cH - (i / yTickCount) * cH,
        val: (i / yTickCount) * maxVal,
    }));

    const yTicksSVG = yTicks.map(t => {
        const label = cfg.fmt(t.val);
        return `<line x1="-5" y1="${t.y}" x2="${cW}" y2="${t.y}" stroke="var(--border)" stroke-dasharray="${t.val === 0 ? 'none' : '4 3'}" stroke-width="0.5"/>
     <text x="-8" y="${(t.y + 4).toFixed(1)}" text-anchor="end" style="font-size:10px;fill:var(--text-muted);font-family:var(--font-mono)">${label}</text>`;
    }).join('');

    const bars = dataPoints.map((d, i) =>
        `<rect class="histo-bar" x="${xPos(i) - barW / 2 + 0.5}" y="${yPos(d.val)}" width="${barW - 1}" height="${cH - yPos(d.val)}"
      style="fill:${cfg.color};opacity:0.75"
      data-lo="${d.year}" data-hi="${d.year}" data-count="${d.val}" />`
    ).join('');

    const xStep = Math.ceil(n / 12);
    const xLabels = dataPoints
        .filter((_, i) => i % xStep === 0 || i === n - 1)
        .map(d => {
            const i = dataPoints.indexOf(d);
            return `<text x="${xPos(i)}" y="${H - 1}" text-anchor="middle" style="font-size:10px;fill:var(--text-muted);font-family:var(--font-mono)">${d.year}</text>`;
        }).join('');

    const svg = `<svg class="histo-svg" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(${pad.left},${pad.top})">
      ${yTicksSVG}
      ${bars}
      <polyline points="${dataPoints.map((d, i) => `${xPos(i)},${yPos(d.val)}`).join(' ')}"
        fill="none" stroke="${cfg.color}" stroke-width="2" stroke-linejoin="round"/>
      ${dataPoints.map((d, i) => `<circle cx="${xPos(i)}" cy="${yPos(d.val)}" r="3" fill="${cfg.color}" class="histo-bar"
        data-lo="${d.year}" data-hi="${d.year}" data-count="${d.val}"/>`).join('')}
      <line x1="0" y1="0" x2="0" y2="${cH}" stroke="var(--border)" stroke-width="1"/>
      <line x1="0" y1="${cH}" x2="${cW}" y2="${cH}" stroke="var(--border)" stroke-width="1"/>
      ${xLabels}
      <text x="${cW / 2}" y="${cH + 40}" text-anchor="middle" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">Year</text>
      <text x="-44" y="${cH / 2}" text-anchor="middle" transform="rotate(-90,-44,${cH / 2})" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">${cfg.yLabel}</text>
    </g>
  </svg>`;

    const wrap = document.getElementById('histoSvgWrap');
    wrap.innerHTML = svg;

    const tooltip = document.getElementById('histoTooltip');
    wrap.querySelectorAll('.histo-bar').forEach(el => {
        el.addEventListener('mouseenter', () => {
            const v = parseFloat(el.dataset.count);
            tooltip.textContent = `${el.dataset.lo}: ${cfg.fmt(v)} ${cfg.yLabel.toLowerCase()}`;
            tooltip.style.opacity = '1';
        });
        el.addEventListener('mousemove', e => {
            const r = wrap.getBoundingClientRect();
            tooltip.style.left = (e.clientX - r.left + 12) + 'px';
            tooltip.style.top = (e.clientY - r.top - 28) + 'px';
        });
        el.addEventListener('mouseleave', () => { tooltip.style.opacity = '0'; });
    });

    document.querySelector('.histo-log-toggle').style.display = 'none';
    const leg = document.getElementById('histoLegend');
    if (leg) { leg.style.display = 'none'; leg.innerHTML = ''; }
    document.getElementById('histogram-modal').style.display = 'flex';
}

function renderStackedSVG(title, subtitle, statsHTML, xAxisLabel, yAxisLabel, layers, xLabels, wrap, legendEl, tooltipEl) {
    document.getElementById('histogramTitle').textContent = title;
    document.getElementById('histogramSubtitle').textContent = subtitle;
    document.getElementById('histogramStats').innerHTML = statsHTML;
    document.querySelector('.histo-log-toggle').style.display = 'none';

    const n = xLabels.length;
    const W = 740, H = 320;
    const pad = { top: 20, right: 20, bottom: 54, left: 62 };
    const cW = W - pad.left - pad.right;
    const cH = H - pad.top - pad.bottom;
    const gap = 1;
    const barW = Math.max(2, (cW / n) - gap);

    const totals = xLabels.map((_, i) => layers.reduce((s, l) => s + (l.values[i] || 0), 0));
    const maxTotal = Math.max(...totals, 1);

    function yScale(v) { return cH - (v / maxTotal) * cH; }

    const tickCount = 5;
    const yTicks = Array.from({ length: tickCount + 1 }, (_, i) => {
        const frac = i / tickCount;
        return { y: cH * (1 - frac), val: Math.round(maxTotal * frac) };
    });
    const yTicksSVG = yTicks.map(t =>
        `<line x1="-5" y1="${t.y.toFixed(1)}" x2="${cW}" y2="${t.y.toFixed(1)}" stroke="var(--border)" stroke-dasharray="${t.val === 0 ? 'none' : '4 3'}" stroke-width="0.5"/>
     <text x="-8" y="${(t.y + 4).toFixed(1)}" text-anchor="end" style="font-size:10px;fill:var(--text-muted);font-family:var(--font-mono)">${t.val >= 1000 ? (t.val / 1000).toFixed(1) + 'K' : t.val}</text>`
    ).join('');

    const barsHTML = xLabels.map((lbl, i) => {
        let yBase = cH;
        return layers.map(layer => {
            const val = layer.values[i] || 0;
            const h = (val / maxTotal) * cH;
            yBase -= h;
            const dataStr = `data-year="${lbl}" data-layer="${layer.label}" data-count="${val}" data-total="${totals[i]}"`;
            return `<rect class="stacked-seg" x="${(i * (barW + gap) + gap / 2).toFixed(1)}" y="${yBase.toFixed(1)}" width="${barW.toFixed(1)}" height="${Math.max(0, h).toFixed(1)}" fill="${layer.color}" opacity="0.82" ${dataStr}/>`;
        }).join('');
    }).join('');

    const xStep = Math.max(1, Math.ceil(n / 14));
    const xLabelsHTML = xLabels
        .filter((_, i) => i % xStep === 0 || i === n - 1)
        .map(lbl => {
            const i = xLabels.indexOf(lbl);
            const x = i * (barW + gap) + barW / 2;
            return `<text x="${x.toFixed(1)}" y="${(cH + 18).toFixed(1)}" text-anchor="middle" style="font-size:10px;fill:var(--text-muted);font-family:var(--font-mono)">${lbl}</text>`;
        }).join('');

    const svg = `<svg class="histo-svg" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(${pad.left},${pad.top})">
      ${yTicksSVG}
      ${barsHTML}
      <line x1="0" y1="0" x2="0" y2="${cH}" stroke="var(--border)" stroke-width="1"/>
      <line x1="0" y1="${cH}" x2="${cW}" y2="${cH}" stroke="var(--border)" stroke-width="1"/>
      ${xLabelsHTML}
      <text x="${(cW / 2).toFixed(1)}" y="${(cH + 42).toFixed(1)}" text-anchor="middle" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">${xAxisLabel}</text>
      <text x="-44" y="${(cH / 2).toFixed(1)}" text-anchor="middle" transform="rotate(-90,-44,${(cH / 2).toFixed(1)})" style="font-size:11px;fill:var(--text-muted);font-family:var(--font-mono)">${yAxisLabel}</text>
    </g>
  </svg>`;

    wrap.innerHTML = svg;

    wrap.querySelectorAll('.stacked-seg').forEach(el => {
        el.style.cursor = 'default';
        el.addEventListener('mouseenter', () => {
            const pct = totals[xLabels.indexOf(el.dataset.year)] > 0
                ? Math.round(parseInt(el.dataset.count) / parseInt(el.dataset.total) * 100) : 0;
            tooltipEl.textContent = `${el.dataset.year} · ${el.dataset.layer}: ${parseInt(el.dataset.count).toLocaleString()} (${pct}%)`;
            tooltipEl.style.opacity = '1';
        });
        el.addEventListener('mousemove', e => {
            const r = wrap.getBoundingClientRect();
            tooltipEl.style.left = (e.clientX - r.left + 12) + 'px';
            tooltipEl.style.top = (e.clientY - r.top - 28) + 'px';
        });
        el.addEventListener('mouseleave', () => { tooltipEl.style.opacity = '0'; });
    });

    legendEl.style.display = 'flex';
    legendEl.innerHTML = [...layers].reverse().map(l =>
        `<span class="histo-legend-item"><span class="histo-legend-swatch" style="background:${l.color}"></span>${escHtml(l.label)}</span>`
    ).join('');
}

function showStackedChart(key) {
    const now = new Date();
    const currentYear = now.getFullYear();
    const wrap = document.getElementById('histoSvgWrap');
    const legendEl = document.getElementById('histoLegend');
    const tooltip = document.getElementById('histoTooltip');

    function yearsSince(dateStr) {
        if (!dateStr) return 999;
        const d = new Date(dateStr.split(' - ')[0]);
        if (isNaN(d)) return 999;
        return (now - d) / (1000 * 60 * 60 * 24 * 365.25);
    }

    if (key === 'pages_by_edit_age') {
        const byYear = {};
        _pages.forEach(p => {
            const y = dateYear(p.date);
            if (!y || y < 1995 || y > currentYear) return;
            if (!byYear[y]) byYear[y] = { recent: 0, med: 0, old5: 0, old10: 0 };
            const age = yearsSince(p.date);
            if (age < 2) byYear[y].recent++;
            else if (age < 5) byYear[y].med++;
            else if (age < 10) byYear[y].old5++;
            else byYear[y].old10++;
        });
        const years = Object.keys(byYear).sort();
        const total = years.reduce((s, y) => s + byYear[y].recent + byYear[y].med + byYear[y].old5 + byYear[y].old10, 0);
        const peak = years.reduce((best, y) => {
            const t = byYear[y].recent + byYear[y].med + byYear[y].old5 + byYear[y].old10;
            return t > best.val ? { year: y, val: t } : best;
        }, { year: years[0], val: 0 });

        renderStackedSVG(
            'Pages Last Edited per Year', 'by how long ago the edit was',
            `<span><strong>Total pages</strong> ${total.toLocaleString()}</span><span><strong>Peak year</strong> ${peak.year} (${peak.val})</span>`,
            'Year of last edit', 'Pages',
            [
                { label: 'Active (<2yr)', color: 'var(--atlas-green-saturated)', values: years.map(y => byYear[y].recent) },
                { label: '2–5 years old', color: 'var(--atlas-orange-saturated)', values: years.map(y => byYear[y].med) },
                { label: '5–10 years old', color: 'var(--atlas-red-saturated)', values: years.map(y => byYear[y].old5) },
                { label: '>10 years old', color: 'var(--atlas-blue-saturated)', values: years.map(y => byYear[y].old10) },
            ],
            years, wrap, legendEl, tooltip
        );

    } else if (key === 'revisions_by_tenure') {
        const authorFirstSeen = {};
        _pages.forEach(p => {
            const _ph = _historyLut[p.html_file];
            if (!_ph?.length) return;
            _ph.forEach(h => {
                const y = dateYear(h.date);
                if (!y || !h.username) return;
                if (!authorFirstSeen[h.username] || y < authorFirstSeen[h.username]) {
                    authorFirstSeen[h.username] = y;
                }
            });
        });

        const byYear = {};
        _pages.forEach(p => {
            const _ph = _historyLut[p.html_file];
            if (!_ph?.length) return;
            _ph.forEach(h => {
                const y = dateYear(h.date);
                if (!y || y < 1995 || y > currentYear) return;
                if (!byYear[y]) byYear[y] = { new1: 0, yr1to5: 0, yr5to10: 0, veteran: 0 };
                const firstYear = authorFirstSeen[h.username];
                if (!firstYear) { byYear[y].new1++; return; }
                const tenure = y - firstYear;
                if (tenure <= 1) byYear[y].new1++;
                else if (tenure <= 5) byYear[y].yr1to5++;
                else if (tenure <= 10) byYear[y].yr5to10++;
                else byYear[y].veteran++;
            });
        });
        const years = Object.keys(byYear).sort();
        const total = years.reduce((s, y) => s + byYear[y].new1 + byYear[y].yr1to5 + byYear[y].yr5to10 + byYear[y].veteran, 0);

        renderStackedSVG(
            'Revisions per Year by Author Tenure', 'how long the author had been on TWiki at time of edit',
            `<span><strong>Total revisions</strong> ${total.toLocaleString()}</span>`,
            'Year', 'Revisions',
            [
                { label: 'New (<=1yr)', color: 'var(--atlas-green-saturated)', values: years.map(y => byYear[y].new1) },
                { label: '1–5yr tenure', color: 'var(--atlas-blue-saturated)', values: years.map(y => byYear[y].yr1to5) },
                { label: '5–10yr tenure', color: 'var(--atlas-orange-saturated)', values: years.map(y => byYear[y].yr5to10) },
                { label: 'Veteran (>10yr)', color: 'var(--atlas-red-saturated)', values: years.map(y => byYear[y].veteran) },
            ],
            years, wrap, legendEl, tooltip
        );

    } else if (key === 'staleness') {
        const buckets = {};
        _pages.forEach(p => {
            const age = Math.floor(yearsSince(p.date));
            const cap = Math.min(age, 20);
            const lbl = cap >= 20 ? '20+' : String(cap);
            if (!buckets[lbl]) buckets[lbl] = { low: 0, mid: 0, high: 0 };
            const revs = parseInt(p.revision) || (_historyLut[p.html_file] || []).length || 0;
            if (revs <= 3) buckets[lbl].low++;
            else if (revs <= 15) buckets[lbl].mid++;
            else buckets[lbl].high++;
        });
        const lbls = [...Array.from({ length: 20 }, (_, i) => String(i)), '20+'];
        lbls.forEach(l => { if (!buckets[l]) buckets[l] = { low: 0, mid: 0, high: 0 }; });
        const total = lbls.reduce((s, l) => s + buckets[l].low + buckets[l].mid + buckets[l].high, 0);

        renderStackedSVG(
            'Page Staleness Distribution', 'years since last edit, by revision count',
            `<span><strong>Total pages</strong> ${total.toLocaleString()}</span>`,
            'Years since last edit', 'Pages',
            [
                { label: '1–3 revisions', color: 'var(--atlas-red)', values: lbls.map(l => buckets[l].low) },
                { label: '4–15 revisions', color: 'var(--atlas-orange)', values: lbls.map(l => buckets[l].mid) },
                { label: '>15 revisions', color: 'var(--atlas-green)', values: lbls.map(l => buckets[l].high) },
            ],
            lbls, wrap, legendEl, tooltip
        );
    }

    document.getElementById('histogram-modal').style.display = 'flex';
}

let _allPagesYearData = null;

function _buildAllPagesYearData() {
    return _allPagesYearData; // pre-built during init
}

function _buildPagesYearData(pages) {
    const currentYear = new Date().getFullYear();
    const yearBuckets = {};
    const peteRevsByYear = {};
    const authorFirstYear = {};

    pages.forEach(p => {
        const ph = _historyLut[p.html_file];

        // === UNIFIED CREATION YEAR (exactly one count per page) ===
        const creationDateStr = ph?.length ? ph[0].date : p.date;
        const cy = dateYear(creationDateStr);

        if (cy && cy >= 2005 && cy <= currentYear) {
            if (!yearBuckets[cy]) yearBuckets[cy] = { pagesCreated: 0, revisions: 0 };
            yearBuckets[cy].pagesCreated++;
        }

        // === REVISIONS + PETE + AUTHOR FIRST YEAR (only if history exists) ===
        if (ph?.length) {
            ph.forEach(h => {
                const ry = dateYear(h.date);
                if (!ry || ry < 2005 || ry > currentYear) return;

                if (!yearBuckets[ry]) yearBuckets[ry] = { pagesCreated: 0, revisions: 0 };
                yearBuckets[ry].revisions++;

                if (h.username === MASS_EDIT_USER) {
                    peteRevsByYear[ry] = (peteRevsByYear[ry] || 0) + 1;
                }
                if (h.username && (!authorFirstYear[h.username] || ry < authorFirstYear[h.username])) {
                    authorFirstYear[h.username] = ry;
                }
            });
        }
    });

    // === CUMULATIVE BLOCK (exactly as in the original global version) ===
    const allYears = Object.keys(yearBuckets).map(Number).sort((a, b) => a - b);
    let cumAuthors = 0, cumPages = 0, cumRevisions = 0;
    allYears.forEach(y => {
        const newThisYear = Object.values(authorFirstYear).filter(fy => fy === y).length;
        cumAuthors += newThisYear;
        cumPages += yearBuckets[y].pagesCreated;
        cumRevisions += yearBuckets[y].revisions;

        yearBuckets[y].newAuthors = newThisYear;
        yearBuckets[y].totalAuthors = cumAuthors;
        yearBuckets[y].cumPages = cumPages;
        yearBuckets[y].cumRevisions = cumRevisions;
    });

    return { yearBuckets, peteRevsByYear };
}

let _bannerMetric = 'pages';
let _bannerMode = 'yearly';
let _authorBannerMetric = 'pages';
let _authorBannerMode = 'yearly';

function _renderSparkSVG(wrap, years, vals, color, label, unit, bgVals = null, totalOverride = null) {
    const maxV = Math.max(...vals, 1);
    const W = 760, H = 54;
    const padT = 2, padB = 16;
    const cH = H - padT - padB;
    const n = years.length;
    const gap = 1.5;
    const barW = (W / n) - gap;

    // Background bars (mass-edit noise)
    const bgBars = bgVals ? years.map((_y, i) => {
        const v = Math.min(bgVals[i] || 0, maxV);
        if (!v) return '';
        const bh = (v / maxV) * cH;
        const x = i * (barW + gap);
        return `<rect x="${x.toFixed(1)}" y="${(padT + cH - bh).toFixed(1)}" width="${barW.toFixed(1)}" height="${bh.toFixed(1)}" fill="var(--text-muted)" opacity="0.18" rx="1"/>`;
    }).join('') : '';

    const bars = years.map((y, i) => {
        const v = vals[i];
        const bh = v > 0 ? Math.max(2, (v / maxV) * cH) : 0;
        const x = i * (barW + gap);
        const bY = padT + cH - bh;
        return `<rect x="${x.toFixed(1)}" y="${bY.toFixed(1)}" width="${barW.toFixed(1)}" height="${bh.toFixed(1)}"
      fill="${color}" opacity="0.78" rx="1"><title>${y}: ${v.toLocaleString()}${unit}</title></rect>`;
    }).join('');

    const labels = years
        .filter((y, i) => i % 3 === 0 || y === years[years.length - 1])
        .map(y => {
            const i = years.indexOf(y);
            const x = i * (barW + gap) + barW / 2;
            return `<text x="${x.toFixed(1)}" y="${H - 1}" text-anchor="middle"
        font-size="12" font-family="var(--font-mono)" fill="var(--text-muted)">${y}</text>`;
        }).join('');

    const peak = vals.reduce((b, v, i) => v > b.v ? { v, i } : b, { v: 0, i: 0 });

    // FIXED: No more double-counting on cumulative!
    // For cumulative we take the FINAL value only. For yearly we sum.
    const total = totalOverride !== null ? totalOverride : vals.reduce((s, v) => s + v, 0);

    wrap.innerHTML = `
    <div style="display:flex;justify-content:space-between;font-size:11px;font-family:var(--font-mono);color:var(--text-muted);margin-bottom:3px;">
      <span>${label}: <strong>${total.toLocaleString()}${unit}</strong></span>
      <span>Peak: <strong>${peak.v.toLocaleString()}${unit}</strong> in <strong>${years[peak.i]}</strong></span>
    </div>
    <svg viewBox="0 0 ${W} ${H}" style="width:100%;display:block;" xmlns="http://www.w3.org/2000/svg">
      ${bgBars}${bars}${labels}
    </svg>`;
}

function renderAllPagesBanner(metric, mode) {
    if (metric) _bannerMetric = metric;
    if (mode) _bannerMode = mode;
    metric = _bannerMetric;
    mode = _bannerMode;

    const yearBuckets = _bannerYearData || _buildAllPagesYearData();
    const pete = _bannerPeteData || _peteRevsByYear;
    const wrap = document.getElementById('allPagesSparkline');
    if (!wrap) return;

    const startYear = 2005;
    const endYear = new Date().getFullYear();
    const years = [];
    for (let y = startYear; y <= endYear; y++) years.push(y);

    const noCumul = metric === 'median_interval';
    const modeKey = noCumul ? 'yearly' : mode;

    // FIXED LABELS + correct keys
    const METRIC_MAP = {
        pages: {
            yearly: { key: 'pagesCreated', label: 'Total pages', color: 'var(--atlas-blue)', unit: '' },
            cumulative: { key: 'cumPages', label: 'Total pages', color: 'var(--atlas-blue)', unit: '' }
        },
        authors: {
            yearly: { key: 'newAuthors', label: 'Total authors', color: 'var(--atlas-orange)', unit: '' },
            cumulative: { key: 'totalAuthors', label: 'Total authors', color: 'var(--atlas-orange)', unit: '' }
        },
        revisions: {
            yearly: { key: 'revisions', label: 'Total Revisions', color: 'var(--atlas-green)', unit: '' },
            cumulative: { key: 'cumRevisions', label: 'Total Revisions', color: 'var(--atlas-green)', unit: '' }
        },
        median_interval: {
            yearly: { key: 'medianInterval', label: 'Median rev. interval', color: 'var(--atlas-purple, #8b5cf6)', unit: ' days' },
            cumulative: { key: 'medianInterval', label: 'Median rev. interval', color: 'var(--atlas-purple, #8b5cf6)', unit: ' days' }
        },
    };

    const cfg = (METRIC_MAP[metric] || METRIC_MAP.pages)[modeKey];
    let vals = years.map(y => (yearBuckets[y] || {})[cfg.key] || 0);

    let bgVals = null;
    if (metric === 'revisions' && modeKey === 'yearly') {
        bgVals = years.map(y => pete[y] || 0);
        vals = vals.map((v, i) => Math.max(0, v - (bgVals[i] || 0)));
    }

    // FIXED: Pass the correct total for cumulative mode
    const isCumulative = modeKey === 'cumulative' && !noCumul;
    const totalOverride = isCumulative ? vals[vals.length - 1] : null;

    _renderSparkSVG(wrap, years, vals, cfg.color, cfg.label, cfg.unit, bgVals, totalOverride);

    document.querySelectorAll('#allPagesBanner .metric-btn').forEach(b =>
        b.classList.toggle('active', b.dataset.metric === metric));
    document.querySelectorAll('#allPagesBanner .mode-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.mode === modeKey);
        b.disabled = noCumul;
        b.style.opacity = noCumul ? '0.4' : '';
    });
}

function buildWebTree() {
    const tree = document.getElementById('webTree');
    tree.innerHTML = '';

    const webGroups = {};
    _pages.forEach(e => { const w = getWebName(e.url); if (!webGroups[w]) webGroups[w] = []; webGroups[w].push(e); });

    const MAIN_WEBS = ['AtlasPublic', 'AtlasProtected', 'AtlasComputing', 'Atlas'];

    MAIN_WEBS.forEach(w => {
        if (!webGroups[w]) return;
        const btn = document.createElement('button');
        btn.className = 'web-main-btn';
        btn.innerHTML = `<span class="web-main-name">${escHtml(w)}</span><span class="cat-count">${webGroups[w].length}</span>`;
        btn.onclick = () => { window.scrollTo(0, 0); showWeb(w); };
        tree.appendChild(btn);
    });

    const others = Object.keys(webGroups)
        .filter(w => !MAIN_WEBS.includes(w))
        .sort((a, b) => webGroups[b].length - webGroups[a].length);

    if (others.length > 0) {
        const totalOthers = others.reduce((s, w) => s + webGroups[w].length, 0);
        const groupId = 'othersWebGroup';
        const group = document.createElement('div');
        group.className = 'cat-item';
        group.innerHTML = `
      <div class="cat-head" style="cursor:pointer;" onclick="var el=document.getElementById('${groupId}');el.style.display=el.style.display==='none'?'block':'none';">
        <span class="cat-name" style="color:var(--text-muted);">Others (${others.length})</span>
        <span class="cat-count">${totalOthers}</span>
      </div>
      <div id="${groupId}" style="display:none;padding-left:10px;">
        ${others.map(w => `<div class="cat-item" onclick="window.scrollTo(0,0);showWeb('${escHtml(w)}');" style="cursor:pointer;"><div class="cat-head"><span class="cat-name" style="font-size:12px;">${escHtml(w)}</span><span class="cat-count">${webGroups[w].length}</span></div></div>`).join('')}
      </div>`;
        tree.appendChild(group);
    }
}

function buildAuthorTree() {
    const listEl = document.getElementById('authorTreeList');
    listEl.innerHTML = '';

    const allBtn = document.createElement('div');
    allBtn.className = 'cat-item';
    allBtn.innerHTML = `<div class="cat-head"><span class="cat-name" style="font-weight:bold;color:var(--accent);">ALL AUTHORS</span><span class="cat-count">${Object.keys(_authors).length}</span></div>`;
    allBtn.onclick = () => { window.scrollTo(0, 0); showAllAuthors(); };
    listEl.appendChild(allBtn);

    if (!_authorList.length) {
        _authorList = Object.keys(_authors)
            .sort((a, b) => displayName(a).localeCompare(displayName(b)))
            .map(author => ({
                author,
                displayName: displayName(author),
                pageCount: (_authorAllPagesIndex[author] || []).length,
                ageClass: _dormantAuthors.has(author) ? 'dot-dormant' : 'dot-active',
            }));
    }

    // Build active / inactive groups when author activity data is available
    if (Object.keys(_authorLastEditTs).length > 0) {
        const nowTs = Date.now();
        const yr1 = 365.25 * 86400000;

        function ageMs(a) { return _authorLastEditTs[a] ? nowTs - _authorLastEditTs[a] : Infinity; }
        function dotClass(a) {
            const ms = ageMs(a);
            if (ms < yr1) return 'dot-active';
            if (ms < 2 * yr1) return 'dot-medium';
            if (ms < 3 * yr1) return 'dot-red';
            return 'dot-dormant';
        }

        const green = [], orange = [], red = [], grey = [];
        Object.keys(_authors).forEach(a => {
            const ms = ageMs(a);
            if (ms < yr1) green.push(a);
            else if (ms < 2 * yr1) orange.push(a);
            else if (ms < 3 * yr1) red.push(a);
            else grey.push(a);
        });
        [green, orange, red, grey].forEach(arr =>
            arr.sort((a, b) => displayName(a).localeCompare(displayName(b))));

        function makeAuthorItem(a) {
            const dName = displayName(a);
            const count = (_authorAllPagesIndex[a] || []).length;
            const dc = dotClass(a);
            return `<div class="author-group-item" onclick="window.scrollTo(0,0);showAuthor('${escHtml(a)}');">
              <span class="sug-dot ${dc}"></span>
              <span class="author-group-name">${escHtml(dName)}</span>
              <span class="sug-count">${count}</span>
            </div>`;
        }

        const activeTotal = green.length + orange.length + red.length;
        const activeGroupId = 'authorActiveGroup';
        const activeGroup = document.createElement('div');
        activeGroup.className = 'cat-item';
        activeGroup.innerHTML = `
        <div class="cat-head author-group-toggle" style="cursor:pointer;" onclick="var el=document.getElementById('${activeGroupId}');el.style.display=el.style.display==='none'?'block':'none';">
          <span class="cat-name" style="color:var(--age-green);font-weight:600;">Active Authors</span>
          <span class="cat-count">${activeTotal}</span>
        </div>
        <div id="${activeGroupId}" style="display:none;max-height:320px;overflow-y:auto;">
          ${green.length ? `<div class="author-subgroup-label" style="color:var(--age-green);">● Edited &lt;1yr ago (${green.length})</div>${green.map(makeAuthorItem).join('')}` : ''}
          ${orange.length ? `<div class="author-subgroup-label" style="color:var(--age-orange);">● Edited 1–2yr ago (${orange.length})</div>${orange.map(makeAuthorItem).join('')}` : ''}
          ${red.length ? `<div class="author-subgroup-label" style="color:var(--age-red);">● Edited 2–3yr ago (${red.length})</div>${red.map(makeAuthorItem).join('')}` : ''}
        </div>`;
        listEl.appendChild(activeGroup);

        const inactiveGroupId = 'authorInactiveGroup';
        const inactiveGroup = document.createElement('div');
        inactiveGroup.className = 'cat-item';
        inactiveGroup.innerHTML = `
        <div class="cat-head author-group-toggle" style="cursor:pointer;" onclick="var el=document.getElementById('${inactiveGroupId}');el.style.display=el.style.display==='none'?'block':'none';">
          <span class="cat-name" style="color:var(--text-muted);">Inactive Authors</span>
          <span class="cat-count">${grey.length}</span>
        </div>
        <div id="${inactiveGroupId}" style="display:none;max-height:320px;overflow-y:auto;">
          ${grey.map(makeAuthorItem).join('')}
        </div>`;
        listEl.appendChild(inactiveGroup);
    }

    const input = document.getElementById('authorSearchInput');
    const sugBox = document.getElementById('authorSuggestions');
    let activeIdx = -1;

    function showSuggestions(q) {
        const filtered = q.length < 1
            ? _authorList.slice(0, 30)
            : _authorList.filter(a => {
                const name = String(a.displayName || a.author || '').toLowerCase();
                const key = String(a.author || '').toLowerCase();
                const sq = q.toLowerCase();
                return name.includes(sq) || key.includes(sq);
            }).slice(0, 40);

        if (!filtered.length) { sugBox.style.display = 'none'; return; }
        sugBox.innerHTML = filtered.map((a, i) =>
            `<div class="author-suggestion" data-author="${escHtml(a.author)}" data-idx="${i}">
        <span class="sug-dot ${a.ageClass}"></span>
        <span class="sug-name">${escHtml(a.displayName)}</span>
        <span class="sug-count">${a.pageCount}</span>
      </div>`
        ).join('');
        sugBox.style.display = 'block';
        activeIdx = -1;

        sugBox.querySelectorAll('.author-suggestion').forEach(el => {
            el.addEventListener('mousedown', e => {
                e.preventDefault();
                window.scrollTo(0, 0);
                showAuthor(el.dataset.author);
                input.value = '';
                sugBox.style.display = 'none';
            });
        });
    }

    // Remove old handlers before re-attaching (safe re-call)
    if (input._blurHandler) {
        input.removeEventListener('focus', input._focusHandler);
        input.removeEventListener('input', input._inputHandler);
        input.removeEventListener('blur', input._blurHandler);
        input.removeEventListener('keydown', input._keydownHandler);
    }
    input._focusHandler = () => showSuggestions(input.value);
    input._inputHandler = () => showSuggestions(input.value);
    input._blurHandler = () => setTimeout(() => { sugBox.style.display = 'none'; }, 150);
    input._keydownHandler = e => {
        const items = sugBox.querySelectorAll('.author-suggestion');
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            activeIdx = Math.min(activeIdx + 1, items.length - 1);
            items.forEach((el, i) => el.classList.toggle('active', i === activeIdx));
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            activeIdx = Math.max(activeIdx - 1, 0);
            items.forEach((el, i) => el.classList.toggle('active', i === activeIdx));
        } else if (e.key === 'Enter' && activeIdx >= 0) {
            e.preventDefault();
            const chosen = items[activeIdx]?.dataset.author;
            if (chosen) { window.scrollTo(0, 0); showAuthor(chosen); input.value = ''; sugBox.style.display = 'none'; }
        } else if (e.key === 'Escape') {
            sugBox.style.display = 'none';
        }
    };
    input.addEventListener('focus', input._focusHandler);
    input.addEventListener('input', input._inputHandler);
    input.addEventListener('blur', input._blurHandler);
    input.addEventListener('keydown', input._keydownHandler);
}

function buildCategoriesTree() {
    const catEl = document.getElementById('categoryTree');
    if (!catEl) return;
    if (!Object.keys(_pageCats).length) {
        catEl.innerHTML = '<div style="padding:8px 16px;color:var(--text-dim);font-size:12px;">No category data loaded</div>';
        return;
    }
    _catIndex = {};
    _pages.forEach(p => {
        const cats = _pageCats[p.html_file];
        if (!cats) return;
        cats.forEach(cat => {
            if (!_catIndex[cat]) _catIndex[cat] = [];
            _catIndex[cat].push(p);
        });
    });
    const sorted = Object.keys(_catIndex).sort((a, b) => _catIndex[b].length - _catIndex[a].length);
    catEl.innerHTML = '';
    sorted.forEach(cat => {
        const item = document.createElement('div');
        item.className = 'cat-item';
        item.innerHTML = `<div class="cat-head"><span class="cat-name">${escHtml(cat)}</span><span class="cat-count">${_catIndex[cat].length}</span></div>`;
        item.onclick = () => { window.scrollTo(0, 0); showCategory(cat); };
        catEl.appendChild(item);
    });
}

function showCategory(cat) {
    _authorPageMode = 'all';
    _viewMode = 'card';
    document.getElementById('viewSelect').value = 'card';
    updateFilterOptions(FILTER_OPTIONS_PAGES, 'all', 'Filter pages:');
    _setAuthorSortOptions(false);
    _activeView = 'pages';
    _activeWeb = null;
    _myActiveAuthor = null;
    _hideBanner();
    _resetAuthorInput();
    const entries = _pages.filter(p => (_pageCats[p.html_file] || []).includes(cat));
    document.getElementById('welcome').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    setPageTitle(`Category: ${escHtml(cat)}`, `${entries.length} pages`);
    renderList(entries, document.getElementById('content'));
}

function initSectionToggles() {
    document.querySelectorAll('.section-toggle').forEach(toggle => {
        const targetId = toggle.dataset.target;
        if (!targetId) return;
        const content = document.getElementById(targetId);
        if (!content) return;
        toggle.classList.add('collapsed'); content.style.display = 'none';
        toggle.addEventListener('click', () => {
            const collapsed = toggle.classList.toggle('collapsed');
            content.style.display = collapsed ? 'none' : 'block';
        });
    });
}

function _setProgress(pct, label) {
    const oBar = document.getElementById('overlayBar');
    const oLbl = document.getElementById('overlayLabel');
    if (oBar) oBar.style.width = pct + '%';
    if (oLbl) oLbl.textContent = label;

    // Only show the sidebar bar when the overlay is not active
    const overlay = document.getElementById('pageLoadOverlay');
    const overlayActive = overlay && overlay.style.display !== 'none' && overlay.style.opacity !== '0';
    if (!overlayActive) {
        const bar = document.getElementById('loadingBar');
        const lbl = document.getElementById('loadingLabel');
        const wrap = document.getElementById('loadingProgress');
        if (wrap) wrap.style.display = 'block';
        if (bar) bar.style.width = pct + '%';
        if (lbl) lbl.textContent = label;
    }
}

function _hideProgress() {
    const wrap = document.getElementById('loadingProgress');
    if (wrap) wrap.style.display = 'none';
    const overlay = document.getElementById('pageLoadOverlay');
    if (overlay) {
        overlay.style.opacity = '0';
        overlay.style.pointerEvents = 'none';
        setTimeout(() => { overlay.style.display = 'none'; }, 420);
    }
}

function _yield() { return new Promise(r => setTimeout(r, 0)); }

async function _processInChunks(arr, chunkSize, fn) {
    if (!Array.isArray(arr) || typeof fn !== 'function') return;
    for (let i = 0; i < arr.length; i += chunkSize) {
        const chunk = arr.slice(i, i + chunkSize);
        fn(chunk, i);
        await _yield();
    }
}

/* === BROTLI-AWARE FETCH WITH SESSION CACHE ===
 * Checks the browser Cache API first so JSON files are only fetched from the
 * network once per browser session.  Falls back to a plain network request if
 * the Cache API is unavailable (e.g. non-secure context).
 * Tries path+'.br' first (browsers auto-decompress Content-Encoding:br),
 * then falls back to the plain file.
 */
const _CACHE_NAME = 'twiki-registry-v1';

async function fetchJSON(path) {
    // Fetch plain JSON only. Production servers handle Brotli transparently via
    // Content-Encoding: br; fetching .br directly fails on python -m http.server
    // because it serves raw Brotli bytes without that header.
    try {
        if ('caches' in window) {
            try {
                const cache = await caches.open(_CACHE_NAME);
                const hit = await cache.match(path);
                if (hit) return hit.json();
                const res = await fetch(path);
                if (res.ok) {
                    cache.put(path, res.clone()).catch(() => { });
                    return res.json();
                }
            } catch (_cacheErr) {
                // Cache API unavailable — fall through to plain fetch
            }
        }
        const res = await fetch(path);
        if (res.ok) return res.json();
    } catch (_) { }
    throw new Error(`Failed to fetch ${path}`);
}

async function _dataIsCached(base) {
    try {
        // Check SW cache first, then fall back to Cache API
        const swHit = await caches.open('twiki-registry-data-v1')
            .then(c => c.match(base + 'conversion_map.json')).catch(() => null);
        if (swHit) return true;
        const apiHit = await caches.open(_CACHE_NAME)
            .then(c => c.match(base + 'conversion_map.json')).catch(() => null);
        return !!apiHit;
    } catch (_) { return false; }
}

async function init() {
    const FuseClass = await loadFuse();
    if (!FuseClass) { console.warn('[twikiregistry] Fuse.js failed to load'); return; }

    const overlay = document.getElementById('pageLoadOverlay');
    if (overlay && overlay.parentElement !== document.body) {
        document.body.appendChild(overlay);
    }

    // Compute DATA_BASE early so we can check the cache before showing the overlay
    const DATA_BASE = (() => {
        let pathname = window.location.pathname;
        if (!pathname.endsWith('/')) pathname += '/';
        const parts = pathname.split('/').filter(Boolean);
        if (parts.length > 0) {
            const last = parts[parts.length - 1].toLowerCase();
            if (['index', 'index2', 'index.html', 'index2.html'].includes(last) || last.endsWith('.html')) parts.pop();
        }
        return parts.length ? '/' + parts.join('/') + '/' : '/';
    })();
    _dataBase = DATA_BASE;

    const cached = await _dataIsCached(DATA_BASE);
    if (!cached) {
        setStatus('loading', 'Loading registry…');
        _setProgress(2, 'Fetching pages…');
    } else {
        _hideProgress();
    }


    try {
        // --- Step 1: fetch data ---
        // DATA_BASE already computed above (needed for cache check before overlay)

        // Kick off history LUT, page categories, and last-viewed LUT in parallel.
        const historyFetchPromise = fetchJSON(DATA_BASE + 'pages_history_lut.json')
            .then(data => { _historyLut = data; })
            .catch(err => console.warn('History LUT unavailable:', err));

        fetchJSON(DATA_BASE + 'page_cats.json')
            .then(data => { _pageCats = data; })
            .catch(() => { /* optional — silently skip */ });

        fetchJSON(DATA_BASE + 'last_viewed_lut.json')
            .then(data => { _lastViewedLut = data; })
            .catch(() => { /* optional — silently skip */ });

        fetchJSON(DATA_BASE + 'author_created_pages_lut.json')
            .then(data => { _authorCreatedPagesLut = data; })
            .catch(() => { /* optional — silently skip */ });

        fetchJSON(DATA_BASE + 'authors_last_active_edited_pages_lut.json')
            .then(data => {
                _authorsMostRecentPages = data;
                // Build inverse index: page → author
                Object.keys(data).forEach(author => {
                    data[author].forEach(page => {
                        _pageToMostRecentAuthor[page] = author;
                    });
                });
            })
            .catch(() => { /* optional — silently skip */ });

        fetchJSON(DATA_BASE + 'authors_last_edited_pages_lut.json')
            .then(data => {
                _authorsLastEditedPages = data;
                // Build inverse index: page → author (fallback for pages with no active editors)
                Object.keys(data).forEach(author => {
                    data[author].forEach(page => {
                        _pageToLastEditedAuthor[page] = author;
                    });
                });
            })
            .catch(() => { /* optional — silently skip */ });

        _pages = await fetchJSON(DATA_BASE + 'conversion_map.json');
        _setProgress(18, `Fetched ${_pages.length} pages — loading authors…`);
        await _yield();

        _authors = await fetchJSON(DATA_BASE + 'authors_metadata.json');
        _setProgress(28, `Loaded ${Object.keys(_authors).length} authors — building search index…`);
        await _yield();
        // --- Step 2: build Fuse index in chunks (non-blocking) ---
        const CHUNK = 400;
        _fusePages = new FuseClass(_pages.slice(0, CHUNK), {
            keys: [
                { name: 'title', weight: 0.7 },
                { name: 'author_split', weight: 0.15 },
                { name: 'author', weight: 0.10 },
                { name: 'description', weight: 0.05 },
                // { name: 'html_file', weight: 0.05 },
                // { name: 'url', weight: 0.03 }
            ],
            threshold: 0.2,
            includeScore: true,
            minMatchCharLength: 2,
            ignoreLocation: true,
            distance: 150
        });
        (async () => {
            for (let i = CHUNK; i < _pages.length; i += CHUNK) {
                _pages.slice(i, i + CHUNK).forEach(p => _fusePages.add(p));
                await _yield();
            }
        })();

        // --- Step 3: UI trees (fast, sync) ---
        _setProgress(38, 'Building navigation…');
        await _yield();
        buildWebTree();
        buildAuthorTree();
        initSectionToggles();

        // Await history LUT before computing activity (Steps 4-5 depend on revision data).
        _setProgress(50, 'Loading page revision data…');
        await historyFetchPromise;
        await _yield();

        // --- Step 4: single merged pass — dormant authors, page meta, year data, inverted index ---
        const authorKeys = Object.keys(_authors);
        const now = new Date();
        const nowTs = now.getTime();
        const oneYearAgo = nowTs - 365.25 * 86400000;
        const currentYear = now.getFullYear();

        _dormantAuthors = new Set();
        _pageRevMeta = {};
        _authorPageIndex = {};
        _authorAllPagesIndex = {};
        _authorLastEditTs = {};
        _authorFirstEditTs = {};
        _authorYearRevCounts = {};
        _authorStats = null;
        _authorSparkCache = {};
        _peteRevsByYear = {};



        const _authorLastEditLocal = {};   // ← THIS WAS THE MISSING LINE
        const _sparkRaw = {};
        const yearBuckets = {};
        const authorFirstYear = {};
        const yearIntervals = {};

        let pagesProcessed = 0;

        await _processInChunks(_pages, 200, (chunk) => {
            chunk.forEach(p => {
                const ph = _historyLut[p.html_file];


                // === UNIFIED CREATION YEAR (exactly ONE count per page) ===
                const creationDateStr = ph?.length ? ph[0].date : p.date;
                const cy = dateYear(creationDateStr);
                if (cy && cy >= 1995 && cy <= currentYear + 1) {
                    if (!yearBuckets[cy]) yearBuckets[cy] = { pagesCreated: 0, revisions: 0 };
                    yearBuckets[cy].pagesCreated++;
                }

                // === SPARKLINE PAGES CREATED ===
                if (cy && cy >= 2005) {
                    const creator = ph?.length ? ph[0].username : (p.created_by || p.author);
                    if (creator) {
                        if (!_sparkRaw[creator]) _sparkRaw[creator] = { r: {}, c: {} };
                        _sparkRaw[creator].c[cy] = (_sparkRaw[creator].c[cy] || 0) + 1;
                    }
                }

                const owners = new Set([p.author, p.created_by].filter(Boolean));
                owners.forEach(a => {
                    if (!_authorPageIndex[a]) _authorPageIndex[a] = [];
                    _authorPageIndex[a].push(p);
                });

                if (!ph?.length) {
                    owners.forEach(a => {
                        if (!_authorAllPagesIndex[a]) _authorAllPagesIndex[a] = [];
                        _authorAllPagesIndex[a].push(p);
                    });
                    const key = p.url || p.html_file || p.title;
                    if (key) _pageRevMeta[key] = { nRevisions: parseInt(p.revision) || 0, nUniqueAuthors: 0, dateCreated: null };
                    return;
                }

                ph.sort((a, b) => a.date.localeCompare(b.date));
                const uniqueAuthorsSet = new Set(ph.map(h => h.username).filter(Boolean));
                const allTouched = new Set([...owners, ...uniqueAuthorsSet]);
                allTouched.forEach(a => {
                    if (!_authorAllPagesIndex[a]) _authorAllPagesIndex[a] = [];
                    _authorAllPagesIndex[a].push(p);
                });

                const dateCreated = ph[0].date.split(' - ')[0];
                const key = p.url || p.html_file || p.title;
                if (key) _pageRevMeta[key] = {
                    nRevisions: parseInt(p.revision) || ph.length,
                    nUniqueAuthors: uniqueAuthorsSet.size,
                    dateCreated
                };

                for (let i = 0; i < ph.length; i++) {
                    const h = ph[i];
                    const ry = dateYear(h.date);
                    if (ry && ry >= 2005 && ry <= currentYear) {
                        if (!yearBuckets[ry]) yearBuckets[ry] = { pagesCreated: 0, revisions: 0 };
                        yearBuckets[ry].revisions++;

                        _pagesWithHistoryCount++; // Increment counter for pages with history
                    }
                    if (h.username) {
                        const ts = new Date(h.date.split(' - ')[0]).getTime();
                        if (!_authorLastEditLocal[h.username] || ts > _authorLastEditLocal[h.username]) _authorLastEditLocal[h.username] = ts;
                        if (!_authorFirstEditTs[h.username] || ts < _authorFirstEditTs[h.username]) _authorFirstEditTs[h.username] = ts;
                        if (ry && (!authorFirstYear[h.username] || ry < authorFirstYear[h.username])) authorFirstYear[h.username] = ry;
                        if (ts >= oneYearAgo) _authorYearRevCounts[h.username] = (_authorYearRevCounts[h.username] || 0) + 1;
                        if (h.username === MASS_EDIT_USER && ry) _peteRevsByYear[ry] = (_peteRevsByYear[ry] || 0) + 1;

                        if (ry && ry >= 2005) {
                            if (!_sparkRaw[h.username]) _sparkRaw[h.username] = { r: {}, c: {} };
                            _sparkRaw[h.username].r[ry] = (_sparkRaw[h.username].r[ry] || 0) + 1;
                        }
                    }
                    if (i > 0) {
                        const d1 = new Date(ph[i - 1].date.split(' - ')[0]);
                        const d2 = new Date(h.date.split(' - ')[0]);
                        const days = (d2 - d1) / 86400000;
                        if (days >= 0 && ry && ry >= 2005 && ry <= currentYear) {
                            if (!yearIntervals[ry]) yearIntervals[ry] = [];
                            yearIntervals[ry].push(days);
                        }
                    }
                }
            });

            pagesProcessed += chunk.length;
            const pct = 52 + Math.round((pagesProcessed / _pages.length) * 36);
            _setProgress(pct, `Processing… (${pagesProcessed}/${_pages.length} pages)`);
        });

        // === FINALISE DORMANT AUTHORS ===
        Object.assign(_authorLastEditTs, _authorLastEditLocal);
        _ghostAuthors = new Set();
        authorKeys.forEach(author => {
            const le = _authorLastEditLocal[author];
            const yearsAgo = le ? (nowTs - le) / (1000 * 60 * 60 * 24 * 365.25) : 999;
            if (yearsAgo >= 3) _dormantAuthors.add(author);
            if (yearsAgo >= 5) _ghostAuthors.add(author);
        });

        // === VALIDATION ===
        const totalCounted = Object.values(yearBuckets).reduce((sum, b) => sum + (b.pagesCreated || 0), 0);
        console.log(`✅ Pages by creation year: ${totalCounted} | Actual pages: ${_pages.length}`);
        console.log(`✅ Pages with history: ${_pagesWithHistoryCount} | Pages without history: ${_pages.length - _pagesWithHistoryCount}`);
        if (totalCounted !== _pages.length) {
            console.warn(`⚠️ Mismatch! ${Math.abs(totalCounted - _pages.length)} pages had unparseable creation dates`);
        }

        // === SPARKLINE CACHE + AUTHOR LIST + YEAR FINALISATION ===
        {
            const sparkYears = [];
            for (let y = 2005; y <= currentYear; y++) sparkYears.push(y);
            Object.keys(_sparkRaw).forEach(author => {
                const raw = _sparkRaw[author];
                const revYearly = sparkYears.map(y => raw.r[y] || 0);
                const pagesYearly = sparkYears.map(y => raw.c[y] || 0);
                let cumR = 0, cumP = 0;
                _authorSparkCache[author] = {
                    years: sparkYears,
                    pages_yearly: pagesYearly,
                    pages_cumulative: pagesYearly.map(v => (cumP += v)),
                    revisions_yearly: revYearly,
                    revisions_cumulative: revYearly.map(v => (cumR += v)),

                };
            });
            Object.keys(_sparkRaw).forEach(k => delete _sparkRaw[k]);
        }

        _authorList = Object.keys(_authors)
            .sort((a, b) => (_authorAllPagesIndex[b] || []).length - (_authorAllPagesIndex[a] || []).length)
            .map(author => ({
                author,
                displayName: displayName(author),
                pageCount: (_authorAllPagesIndex[author] || []).length,
                ageClass: _dormantAuthors.has(author) ? 'dot-dormant' : 'dot-active',
            }));
        buildAuthorTree();
        buildCategoriesTree();

        const allYears = Object.keys(yearBuckets).map(Number).sort((a, b) => a - b);
        let cumAuthors = 0, cumPages = 0, cumRevisions = 0;
        allYears.forEach(y => {
            const newThisYear = Object.values(authorFirstYear).filter(fy => fy === y).length;
            cumAuthors += newThisYear;
            cumPages += yearBuckets[y].pagesCreated;
            cumRevisions += yearBuckets[y].revisions;
            yearBuckets[y].newAuthors = newThisYear;
            yearBuckets[y].totalAuthors = cumAuthors;
            yearBuckets[y].cumPages = cumPages;
            yearBuckets[y].cumRevisions = cumRevisions;
        });
        allYears.forEach(y => {
            const arr = (yearIntervals[y] || []).sort((a, b) => a - b);
            const mid = Math.floor(arr.length / 2);
            yearBuckets[y].medianInterval = arr.length === 0 ? 0
                : Math.round(arr.length % 2 === 0 ? (arr[mid - 1] + arr[mid]) / 2 : arr[mid]);
        });
        _allPagesYearData = yearBuckets;

        // --- Step 6: finalise ---
        _setProgress(90, 'Finalising…');
        await _yield();

        document.getElementById('loadedStats').textContent = `${_pages.length} pages • ${Object.keys(_authors).length} authors`;
        setStatus('ready', `${_pages.length} pages, ${Object.keys(_authors).length} authors`);
        updateFilterOptions(FILTER_OPTIONS_PAGES, 'all', 'Filter pages:');
        _setProgress(100, 'Ready');
        await _yield();
        _hideProgress();
        showAll();


    } catch (err) {
        setStatus('error', 'Failed to load data');
        _setProgress(100, 'Error loading data');
        console.error(err);
    }
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/twikiregistry/sw.js', { scope: '/twikiregistry/' })
        .catch(() => { /* SW unavailable — Cache API fallback still active */ });
}

function buildUI(root) {
    // Overlay must be a direct child of body so position:fixed is never
    // constrained by a CSS transform on an ancestor (MkDocs content wrapper).
    if (!document.getElementById('pageLoadOverlay')) {
        const ov = document.createElement('div');
        ov.id = 'pageLoadOverlay';
        ov.style.cssText = 'position:fixed;left:0;right:0;bottom:0;top:0;z-index:500;background:var(--md-default-bg-color,#fff);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;opacity:1;transition:opacity 0.4s ease;pointer-events:all;cursor:default;';
        ov.innerHTML = `
  <div style="font-size:20px;font-weight:600;color:var(--text);font-family:var(--font-ui);letter-spacing:-0.02em;">TWiki Registry</div>
  <div style="width:260px;">
    <div style="font-size:12px;font-family:var(--font-mono);color:var(--text-muted);margin-bottom:8px;min-height:1.4em;" id="overlayLabel">Loading…</div>
    <div style="height:5px;background:var(--bg3);border-radius:3px;overflow:hidden;border:1px solid var(--border);">
      <div id="overlayBar" style="height:100%;width:0%;background:var(--accent);border-radius:3px;transition:width 0.25s ease;"></div>
    </div>
  </div>`;
        document.body.appendChild(ov);
    }

    root.innerHTML = `
<div class="shell">
<aside class="sidebar">
<div class="search-wrap">
<input id="searchInput" class="search-input" placeholder="Search titles, authors, webs, URLs...">
<span class="search-icon"><svg xmlns="http://www.w3.org/2000/svg" width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11.1 22H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.706.706l3.589 3.588A2.4 2.4 0 0 1 20 8v3.25"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="m21 22-2.88-2.88"/><circle cx="16" cy="17" r="3"/></svg></span>
</div>
<div style="padding: 0 8px 6px;">
<button class="histogram-btn" style="font-weight:600;color:var(--accent);width:100%;text-align:left;" onclick="window.scrollTo(0,0);showAll();">All Pages</button>
</div>
<div class="loaded-stats" id="loadedStats"><span id="statusText"><span class="status-dot ready"></span> 0 pages • 0 authors</span></div>
<div id="loadingProgress" style="display:none; padding: 4px 16px 8px;">
  <div style="font-size:11px;font-family:var(--font-mono);color:var(--text-dim);margin-bottom:4px;" id="loadingLabel">Initialising…</div>
  <div style="height:4px;background:var(--bg3);border-radius:2px;overflow:hidden;">
    <div id="loadingBar" style="height:100%;width:0%;background:var(--accent);border-radius:2px;transition:width 0.2s ease;"></div>
  </div>
</div>
<div class="sidebar-section">
<h4 class="section-toggle" data-target="webTree">Webs</h4>
<div id="webTree" class="cat-tree" style="display:none;"></div>
</div>
<div class="sidebar-section">
<h4>Authors</h4>
<div id="authorTree" class="cat-tree">
  <div class="author-search-wrap">
    <input id="authorSearchInput" class="author-search-input" placeholder="Type to filter authors…" autocomplete="off">
    <div id="authorSuggestions" class="author-suggestions"></div>
  </div>
  <div id="authorTreeList"></div>
</div>
</div>
</aside>
<main class="main">
<div id="pageHeader" style="margin-bottom:16px;text-align:center;">
<h1 id="pageTitle" class="page-title"></h1>
<p id="pageSubtitle" class="page-subtitle"></p>
<div id="authorBanner" style="display:none;margin:10px auto 0;max-width:640px;padding:8px 18px 10px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);text-align:left;">
  <div id="authorBannerBands" class="author-page-bands" style="margin:0 0 6px;border-radius:3px;"></div>
  <div id="authorBannerCounts" class="author-band-counts" style="padding:0;"></div>
  <div style="margin-top:10px;">
    <div style="display:flex;gap:6px;margin-bottom:6px;flex-wrap:wrap;align-items:center;">
    <span id="authorHistoryStat" style="font-size:12px;color:var(--text-muted);white-space:nowrap;margin-right:7px;padding-right:5px;border-right:1px solid var(--border);min-width:130px;display:flex;align-items:center;gap:4px;">
      <strong id="authorHistNum">0</strong>/<strong id="authorHistTotal">0</strong> have history
    </span>
      <button class="all-pages-spark-btn metric-btn active" data-metric="pages" data-scope="author">Creation Date</button>
      <button class="all-pages-spark-btn metric-btn" data-metric="revisions" data-scope="author">Revision Date</button>
      <span style="width:1px;height:18px;background:var(--border);margin:0 4px;display:inline-block;"></span>
      <button class="all-pages-spark-btn mode-btn active" data-mode="yearly" data-scope="author">Per year</button>
      <button class="all-pages-spark-btn mode-btn" data-mode="cumulative" data-scope="author">Cumulative</button>
    </div>
    <div id="authorSparkline"></div>
  </div>
  <div id="authorFilterBar" class="author-filter-bar"></div>
</div>
<div id="allPagesBanner" style="display:none;margin:10px auto 0;max-width:800px;padding:10px 18px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:var(--radius);text-align:left;">
  <div style="display:flex;gap:6px;margin-bottom:6px;flex-wrap:wrap;align-items:center;">
    <button class="all-pages-spark-btn metric-btn active" data-metric="pages">Pages</button>
    <button class="all-pages-spark-btn metric-btn" data-metric="authors">Authors</button>
    <button class="all-pages-spark-btn metric-btn" data-metric="revisions">Revisions</button>
    <span style="width:1px;height:18px;background:var(--border);margin:0 4px;display:inline-block;"></span>
    <button class="all-pages-spark-btn mode-btn active" data-mode="yearly">Per year</button>
    <button class="all-pages-spark-btn mode-btn" data-mode="cumulative">Cumulative</button>
  </div>
  <div id="allPagesSparkline"></div>
</div>
</div>
<div class="controls">
<div>
<label for="sortSelect">Sort by:</label>
<select id="sortSelect" class="sort-select">
<option value="pagerank" class="pages-sort">PageRank (best first)</option>
<option value="title-asc" class="pages-sort">Title A–Z</option>
<option value="title-desc" class="pages-sort">Title Z–A</option>
<option value="date-desc" class="pages-sort">Last Edit Newest</option>
<option value="date-asc" class="pages-sort">Last Edit Oldest</option>
<option value="pctOld-desc" class="authors-only" style="display:none">Most stale %</option>
<option value="hIndex-desc" class="authors-only" style="display:none">h-index (highest)</option>
<option value="pages-desc" class="authors-only" style="display:none">Most pages</option>
<option value="revisions-desc" class="authors-only" style="display:none">Most revisions</option>
<option value="lastActive-desc" class="authors-only" style="display:none">Most recently active</option>
</select>
</div>
<div id="viewModeControl">
<label for="viewSelect">View:</label>
<select id="viewSelect" class="view-select">
<option value="card">Cards</option>
<option value="table">Table (Compact)</option>
</select>
</div>
<div>
<label id="filterLabel" for="filterSelect">Filter:</label>
<select id="filterSelect" class="filter-select"></select>
</div>
<div style="display:flex;align-items:center;">
<button id="downloadCsvBtn" class="md-content__button md-icon" title="Download current selections as .csv" aria-label="Download CSV">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1rem" height="1rem" fill="currentColor">
    <path d="M5 20h14v-2H5v2zm7-18L5.33 9h3.84v6h5.66V9h3.84L12 2z"/>
  </svg>
  Download CSV
</button>
</div>
</div>
<div class="legend" id="legend" style="display:none;">
<div class="legend-item"><div class="legend-color age-success"></div>Recently updated (&lt;2 years)</div>
<div class="legend-item"><div class="legend-color age-warning"></div>2–5 years ago</div>
<div class="legend-item"><div class="legend-color age-danger"></div>&gt;5 years old</div>
<div class="legend-item"><div class="legend-color ghost-editor"></div>Editor inactive 5+ years</div>
</div>
<div id="welcome">
<h2>Welcome to Twiki Registry</h2>
<p>Recent / active pages are shown below. Click a web or author in the sidebar to explore.</p>
</div>
<div id="content"></div>
</main>
</div>
<div id="histogram-modal" onclick="if(event.target===this)closeHistogram()">
  <div class="histogram-container">
    <button class="histogram-close" onclick="closeHistogram()" aria-label="Close">\xd7</button>
    <div class="histogram-header">
      <h3 class="histogram-title" id="histogramTitle">Distribution</h3>
      <span class="histogram-subtitle" id="histogramSubtitle"></span>
    </div>
    <div class="histogram-stats" id="histogramStats"></div>
    <label class="histo-log-toggle"><input type="checkbox" id="histoLogScale"> Log scale</label>
    <div class="histo-svg-wrap" id="histoSvgWrap"></div>
    <div class="histo-legend" id="histoLegend" style="display:none;margin-top:12px;"></div>
    <div class="histo-tooltip" id="histoTooltip"></div>
  </div>
</div>
<div id="analytics-modal" onclick="if(event.target===this)closeAnalytics()">
  <div class="analytics-container">
    <button class="analytics-close" onclick="closeAnalytics()" aria-label="Close">\xd7</button>
    <h3 class="analytics-title">Search Analytics</h3>
    <div id="analyticsContent"></div>
  </div>
</div>
<div id="timelineOverlay" onclick="if(event.target===this)closeTimeline()">
  <div class="timeline-container">
    <div class="timeline-header">
      <div style="flex:1">
        <div class="timeline-season-label" id="tlSeasonLabel">—</div>
        <div class="timeline-narrative" id="tlNarrative"></div>
      </div>
      <button class="timeline-close" onclick="closeTimeline()">\xd7</button>
    </div>
    <div class="timeline-body">
      <div class="timeline-chart-area" id="tlChartArea"></div>
      <div class="timeline-collaborators" id="tlCollaborators"></div>
    </div>
    <div class="timeline-footer">
      <button class="timeline-btn" id="tlPrevBtn" onclick="timelineStep(-1)">◄ Prev</button>
      <div style="flex:1;">
        <div class="timeline-progress-track">
          <div class="timeline-progress-fill" id="tlProgressFill" style="width:0%"></div>
        </div>
      </div>
      <span class="timeline-season-counter" id="tlCounter"></span>
      <button class="timeline-btn primary" id="tlNextBtn" onclick="timelineStep(1)">Next ►</button>
      <button class="timeline-btn" id="tlPlayBtn" onclick="timelineTogglePlay()">► Play</button>
    </div>
  </div>
</div>`;
}

function setup() {
    const root = document.getElementById('twikiregistry-root');
    if (!root) return;  // not on this page

    if (!document.querySelector('link[href*="twikiregistry.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = SCRIPT_BASE + '../stylesheets/twikiregistry.css';
        document.head.appendChild(link);
    }

    buildUI(root);

    // Delegate on .shell so listeners are scoped to this page's DOM and
    // garbage-collected when the content is replaced on SPA navigation.
    const shell = root.querySelector('.shell');
    if (shell) {
        shell.addEventListener('click', e => {
            const filterBtn = e.target.closest('.author-filter-btn');
            if (filterBtn) {
                const author = filterBtn.dataset.author;
                const mode = filterBtn.dataset.mode;
                if (author && mode) setAuthorPageMode(author, mode);
            }
        });
        shell.addEventListener('click', e => {
            const btn = e.target.closest('.all-pages-spark-btn');
            if (!btn) return;
            const scope = btn.dataset.scope;
            if (scope === 'author') {
                const metric = btn.classList.contains('metric-btn') ? btn.dataset.metric : undefined;
                const mode = btn.classList.contains('mode-btn') ? btn.dataset.mode : undefined;
                if (_authorSparkEntries.length && _authorSparkName) {
                    renderAuthorSparkline(_authorSparkName, _authorSparkEntries, metric, mode);
                }
            } else {
                const metric = btn.classList.contains('metric-btn') ? btn.dataset.metric : undefined;
                const mode = btn.classList.contains('mode-btn') ? btn.dataset.mode : undefined;
                renderAllPagesBanner(metric, mode);
            }
        });
    }

    document.getElementById('sortSelect').addEventListener('change', e => { _currentSort = e.target.value; rerenderCurrentView(); });
    document.getElementById('viewSelect').addEventListener('change', e => { _viewMode = e.target.value; rerenderCurrentView(); });
    document.getElementById('searchInput').addEventListener('input', e => {
        clearTimeout(_searchTmo);
        _searchTmo = setTimeout(() => renderSearch(e.target.value.trim()), 420);
    });
    document.getElementById('downloadCsvBtn').addEventListener('click', downloadCurrentCSV);
    document.getElementById('histoLogScale')?.addEventListener('change', e => {
        _histoLogMode = e.target.checked;
        if (_histoField) renderHistoSVG();
    });
    init();
}
// <script> is at page bottom — all elements above are already parsed on both
// first load and SPA re-execution (Zensical injects content before running scripts).
setup();
