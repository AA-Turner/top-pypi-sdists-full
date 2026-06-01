/**
 * Lazy-loads a category_XXXX.json and renders meeting admonitions inline.
 *
 * Usage in a .md file body:
 *
 *   <div id="indico-meetings" data-json="./category_XXXX.json"></div>
 *   <script src="path/to/indico_category_loader.js"></script>
 *
 * Or inline the script directly after the div.
 * The div is populated once it scrolls into view (IntersectionObserver).
 */
(function () {

    // Capture synchronously — document.currentScript is null in async callbacks.
    const SCRIPT_BASE = document.currentScript
        ? document.currentScript.src.replace(/[^/]+$/, '')
        : '/assets/javascripts/';

    // ---------------------------------------------------------------------------
    // Lucide SVG icon strings (inline — no external dependency)
    // ---------------------------------------------------------------------------

    const ICONS = {
        calendar: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M8 2v4M16 2v4"/><rect height="18" rx="2" width="18" x="3" y="4"/><path d="M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/></svg>`,
        clock: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>`,
        mapPin: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>`,
        notes: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4M2 6h4M2 10h4M2 14h4M2 18h4"/><path d="M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"/></svg>`,
        link: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
        users: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M16 3.128a4 4 0 0 1 0 7.744M22 21v-2a4 4 0 0 0-3-3.87"/><circle cx="9" cy="7" r="4"/></svg>`,
        file: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5M10 9H8M16 13H8M16 17H8"/></svg>`,
        // toolbar icons
        table: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg>`,
        cards: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/><path d="M14 4h7M14 9h7M14 15h7M14 20h7"/></svg>`,
        dlTxt: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M12 18v-6m-3 3 3 3 3-3"/></svg>`,
        paperclip: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>`,
        braces: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/></svg>`,
        extLink: `<svg class="lucide" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>`,
    };

    function ic(key) {
        return `<span class="twemoji">${ICONS[key]}</span>`;
    }

    // Registry: contrib.url → minutes {html, url, modified_dt}
    const _minutesData = new Map();

    // ---------------------------------------------------------------------------
    // Formatting helpers
    // ---------------------------------------------------------------------------

    const MONTHS = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    function ordinalSup(n) {
        const v = n % 100;
        const suffix = (v >= 11 && v <= 13) ? 'th'
            : ['th', 'st', 'nd', 'rd'][n % 10] || 'th';
        return `${n}<sup>${suffix}</sup>`;
    }

    function formatDate(dateStr) {
        const [y, m, d] = dateStr.split('-').map(Number);
        return `${MONTHS[m - 1]} ${ordinalSup(d)} ${y}`;
    }

    // start_time format in JSON: "1900-01-01 HH:MM:SS+00:00" (dummy date, real time)
    function extractTime(timeStr) {
        if (!timeStr) return null;
        const m = timeStr.match(/\s(\d{2}:\d{2}):\d{2}/);
        return m ? m[1] : null;
    }

    function meetingTimeRange(contributions) {
        const times = contributions
            .map(c => extractTime(c.start_time))
            .filter(Boolean)
            .sort();
        if (!times.length) return null;
        return times.length > 1 ? `${times[0]}–${times[times.length - 1]}` : times[0];
    }

    function humanSize(bytes) {
        if (!bytes || bytes <= 0) return '';
        const units = ['B', 'kB', 'MB', 'GB'];
        let i = 0;
        while (bytes >= 1024 && i < units.length - 1) { bytes /= 1024; i++; }
        return `(${bytes.toFixed(1)}${units[i]})`;
    }

    function speakerName(s) {
        if (typeof s === 'string') return s;
        return s.fullName || [s.first_name, s.last_name].filter(Boolean).join(' ');
    }

    // ---------------------------------------------------------------------------
    // Pre-compute row data once per event — avoids repeated derivation on sort.
    // ---------------------------------------------------------------------------

    function buildRow(ev) {
        const contribs = ev.contributions || [];
        const attachCount = contribs.reduce((n, c) => n + (c.attachments || []).length, 0);
        const authorCount = new Set(
            contribs.flatMap(c => (c.speakers || []).map(speakerName).filter(Boolean))
        ).size;
        return {
            ev,
            date: ev.date,
            title: ev.title || '',
            url: ev.url || '',
            minutesUrl: ev.minutes_url || '',
            attachCount,
            authorCount,
        };
    }

    // ---------------------------------------------------------------------------
    // Card view renderer
    // ---------------------------------------------------------------------------

    function renderAttachment(att) {
        const url = att.download_url || att.url || '';
        const title = att.title || att.filename || 'attachment';
        const size = humanSize(att.size);
        return `<li>${ic('file')} <a href="${url}">${title}</a>`
            + (size ? ` <span style="color:#777777">${size}</span>` : '')
            + `</li>`;
    }

    function formatSpeakers(raw) {
        if (!raw) return '';
        if (typeof raw === 'string') return raw;
        return raw.map(s => {
            const name = speakerName(s);
            return s.affiliation ? `${name} (${s.affiliation})` : name;
        }).filter(Boolean).join(', ');
    }

    function renderContribution(contrib) {
        const speakers = formatSpeakers(contrib.speakers);
        const minutes  = contrib.minutes;
        const atts     = (contrib.attachments || []).map(renderAttachment).join('');

        let line = `<a href="${contrib.url}">${contrib.title}</a>`;
        if (speakers) line += ` | <strong>${ic('users')}</strong> ${speakers}`;

        let minutesBtn = '';
        if (minutes && minutes.html && minutes.html.trim()) {
            _minutesData.set(contrib.url, minutes);
            minutesBtn = `<button data-mid="${contrib.url}" title="Toggle minutes">${ic('notes')} Minutes</button>`;
        }

        return `<li>`
            + `<p class="indico-contrib-row">`
            + `<span class="indico-contrib-title">${line}</span>`
            + minutesBtn
            + `</p>`
            + (atts ? `<ul>${atts}</ul>` : '')
            + `</li>`;
    }

    function renderMeeting(ev) {
        const time       = meetingTimeRange(ev.contributions || []);
        const room       = ev.room || ev.location || '';


        const meta = [`<strong>${ic('calendar')} Date:</strong> ${formatDate(ev.date)}`];
        if (time) meta.push(`<strong>${ic('clock')} Time:</strong> ${time}`);
        if (room) meta.push(`<strong>${ic('mapPin')} Room:</strong> ${room}`);
        meta.push(`<strong>${ic('link')} <a href="${ev.url}">Event</a></strong>`);

        // Event-level minutes button — only if there is actual HTML content.
        const eventMinutesHtml = ev.minutes?.html?.trim();
        let titleBar;
        if (eventMinutesHtml) {
            _minutesData.set(`event:${ev.url}`, ev.minutes);
            titleBar = `<p class="admonition-title" style="display:flex;align-items:center;gap:0.5em">`
                + `<span style="flex:1"><a href="${ev.url}">${ev.title}</a></span>`
                + `<button data-mid="event:${ev.url}" title="Toggle minutes">${ic('notes')} Minutes</button>`
                + `</p>`;
        } else {
            titleBar = `<p class="admonition-title"><a href="${ev.url}">${ev.title}</a></p>`;
        }

        const contribsHtml = (ev.contributions || []).map(renderContribution).join('');

        return `<div class="admonition quote">`
            + titleBar
            + `<p>${meta.join(' | ')}</p>`
            + (contribsHtml ? `<hr><ul>${contribsHtml}</ul>` : '')
            + `</div>`;
    }

    function renderCards(container, rows) {
        if (!rows.length) {
            container.innerHTML = '<p><em>No meetings found.</em></p>';
            return;
        }

        const byMonth = new Map();
        rows.forEach(r => {
            const [y, m] = r.date.split('-').map(Number);
            const key = `${y}-${String(m).padStart(2, '0')}`;
            if (!byMonth.has(key)) byMonth.set(key, { label: `${MONTHS[m - 1]} ${y}`, rows: [] });
            byMonth.get(key).rows.push(r);
        });

        container.innerHTML = [...byMonth.entries()]
            .sort(([a], [b]) => b.localeCompare(a))
            .map(([, { label, rows: rs }]) =>
                `<h2>${label}</h2>\n` + rs.map(r => renderMeeting(r.ev)).join('\n')
            )
            .join('\n');
    }

    // ---------------------------------------------------------------------------
    // Table view renderer
    // ---------------------------------------------------------------------------

    const SORT_COLS = [
        { key: 'date', label: 'Date' },
        { key: 'title', label: 'Title' },
        { key: 'attachCount', label: 'Attachments' },
        { key: 'authorCount', label: 'Authors' },
    ];

    function sortedRows(rows, key, dir) {
        return [...rows].sort((a, b) => {
            const av = a[key], bv = b[key];
            if (typeof av === 'number') return dir * (av - bv);
            return dir * String(av).localeCompare(String(bv));
        });
    }

    function renderTable(container, rows, sortKey, sortDir) {
        if (!rows.length) {
            container.innerHTML = '<p><em>No meetings found.</em></p>';
            return;
        }

        const sorted = sortedRows(rows, sortKey, sortDir);

        const thFor = (col) => {
            const active = col.key === sortKey;
            const ariaSort = active ? (sortDir === 1 ? 'ascending' : 'descending') : 'none';
            return `<th data-sort="${col.key}" aria-sort="${ariaSort}" class="indico-th-${col.key}">${col.label}</th>`;
        };

        const thead = SORT_COLS.map(thFor).join('')
            + `<th class="indico-th-links">Links</th>`;

        const today = new Date().toISOString().slice(0, 10);

        const tbody = sorted.map(r => {
            const future = r.date > today;
            const links = `<a href="${r.url}" title="Indico event">${ICONS.extLink}</a>`
                + (r.minutesUrl ? ` <a href="${r.minutesUrl}" title="Minutes">${ICONS.notes}</a>` : '');
            return `<tr${future ? ' class="indico-future"' : ''}>`
                + `<td class="indico-td-date">${r.date}</td>`
                + `<td><a href="${r.url}">${r.title}</a></td>`
                + `<td class="indico-td-num indico-td-attachCount">${r.attachCount || '–'}</td>`
                + `<td class="indico-td-num indico-td-authorCount">${r.authorCount || '–'}</td>`
                + `<td class="indico-td-links">${links}</td>`
                + `</tr>`;
        }).join('');

        container.innerHTML =
            `<div class="md-typeset__scrollwrap"><div class="md-typeset__table">`
            + `<table class="indico-table">`
            + `<colgroup>`
            + `<col class="indico-col-date">`
            + `<col class="indico-col-title">`
            + `<col class="indico-col-attach">`
            + `<col class="indico-col-authors">`
            + `<col class="indico-col-links">`
            + `</colgroup>`
            + `<thead><tr>${thead}</tr></thead>`
            + `<tbody>${tbody}</tbody>`
            + `</table></div></div>`;
    }

    // ---------------------------------------------------------------------------
    // Downloads
    // ---------------------------------------------------------------------------

    function triggerDownload(filename, content, mime) {
        const blob = new Blob([content], { type: mime });
        const url = URL.createObjectURL(blob);
        const a = Object.assign(document.createElement('a'), { href: url, download: filename });
        a.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    function downloadTxt(rows) {
        triggerDownload(
            'meetings.txt',
            rows.map(r => `${r.date}, ${r.title}, ${r.url}`).join('\n'),
            'text/plain'
        );
    }

    function downloadAttachments(rows) {
        const lines = [];
        rows.forEach(r =>
            (r.ev.contributions || []).forEach(c =>
                (c.attachments || []).forEach(att => {
                    const url = att.download_url || att.url || '';
                    const title = att.title || att.filename || 'attachment';
                    lines.push(`${r.date}, ${r.title}, ${title}, ${url}`);
                })
            )
        );
        triggerDownload('attachments.txt', lines.join('\n'), 'text/plain');
    }

    function downloadJson(rows) {
        triggerDownload(
            'meetings.json',
            JSON.stringify(rows.map(r => r.ev), null, 2),
            'application/json'
        );
    }

    // ---------------------------------------------------------------------------
    // Toolbar
    // ---------------------------------------------------------------------------

    function buildToolbar(initialView, indicoSearchBase) {
        const el = document.createElement('div');
        el.className = 'indico-toolbar';
        el.innerHTML =
            `<div class="indico-toolbar-row">`
            + `<input class="indico-search-input" type="search" placeholder="Search meetings, talks, speakers…" aria-label="Search meetings">`
            + (indicoSearchBase
                ? `<a class="md-button md-button--primary indico-search-btn" href="${indicoSearchBase}" target="_blank" rel="noopener noreferrer">Use Indico Search</a>`
                : '')
            + `<div class="indico-toolbar-actions">`
            + `<button class="md-content__button" data-action="view" title="${initialView === 'cards' ? 'Switch to table view' : 'Switch to card view'}">`
            + (initialView === 'cards' ? ICONS.table : ICONS.cards)
            + `</button>`
            + `<button class="md-content__button" data-action="dl-txt"  title="Download meeting list (.txt)">${ICONS.dlTxt}</button>`
            + `<button class="md-content__button" data-action="dl-att"  title="Download attachment list (.txt)">${ICONS.paperclip}</button>`
            + `<button class="md-content__button" data-action="dl-json" title="Download JSON">${ICONS.braces}</button>`
            + `</div>`
            + `</div>`
            + `<span class="indico-search-count"></span>`;
        return el;
    }

    // ---------------------------------------------------------------------------
    // Fuse.js search workers
    // Workers are built from the pre-built _search.json index, not the full
    // category JSON.  Each returns a Set<event_url> for the matched events.
    // ---------------------------------------------------------------------------

    class FuseWorker {
        constructor(items, keys, options = {}) {
            this._items = items;
            this._keys = keys;
            this._options = { threshold: 0.35, ignoreLocation: true, ...options };
            this._fuse = null;
        }

        init(FuseClass) {
            this._fuse = new FuseClass(this._items, { keys: this._keys, ...this._options });
        }

        _matchingUrls(query) {
            const hits = (query && this._fuse)
                ? this._fuse.search(query).map(r => r.item)
                : this._items;
            return new Set(hits.map(item => item.event_url || item.url));
        }
    }

    class MeetingWorker extends FuseWorker {
        constructor(index) {
            super(index.filter(r => r.type === 'event'), [{ name: 'title', weight: 1 }]);
        }
        matchingUrls(query) { return this._matchingUrls(query); }
    }

    class ContributionWorker extends FuseWorker {
        constructor(index) {
            super(index.filter(r => r.type === 'contribution'), [{ name: 'title', weight: 1 }]);
        }
        matchingUrls(query) { return this._matchingUrls(query); }
    }

    class SpeakerWorker extends FuseWorker {
        constructor(index) {
            super(index.filter(r => r.type === 'speaker'), [
                { name: 'name', weight: 2 },
                { name: 'variants', weight: 1 },
            ]);
        }
        matchingUrls(query) { return this._matchingUrls(query); }
    }

    // ---------------------------------------------------------------------------
    // Fuse.js loader — loads the vendored fuse.min.js via script tag, then
    // immediately captures and clears window.Fuse so it doesn't linger.
    // ---------------------------------------------------------------------------

    let _fusePromise = null;
    function loadFuse() {
        if (_fusePromise) return _fusePromise;
        _fusePromise = new Promise(resolve => {
            const s = document.createElement('script');
            s.src = SCRIPT_BASE + 'fuse.min.js';
            s.onload = () => {
                const F = window.Fuse;
                delete window.Fuse;
                resolve(F || null);
            };
            s.onerror = () => resolve(null);
            document.head.appendChild(s);
        });
        return _fusePromise;
    }

    // ---------------------------------------------------------------------------
    // Sidebar — upcoming events
    // ---------------------------------------------------------------------------

    function fillSidebar(allRows) {
        const sidebar = document.querySelector(
            '[data-md-component="sidebar"][data-md-type="toc"]'
        );
        if (!sidebar) return;

        sidebar.removeAttribute('data-md-type');

        // Let the scrollwrap size naturally instead of the JS-injected fixed height.
        const scrollwrap = sidebar.querySelector('.md-sidebar__scrollwrap');
        if (scrollwrap) scrollwrap.style.height = 'auto';

        const inner = sidebar.querySelector('.md-sidebar__inner');
        if (!inner) return;

        const today = new Date().toISOString().slice(0, 10);
        const upcoming = allRows
            .filter(r => r.date > today)
            .sort((a, b) => a.date.localeCompare(b.date));

        const listItems = upcoming.length
            ? upcoming.map(r =>
                `<li class="md-nav__item">`
                + `<span class="indico-nav-date">${r.date}</span>`
                + `<a class="md-nav__link" href="${r.url}" target="_blank" rel="noopener noreferrer">`
                + `<span class="md-ellipsis"><span class="md-typeset">${r.title}</span></span>`
                + `</a>`
                + `</li>`
            ).join('\n')
            : `<li class="md-nav__item"><em>No upcoming events.</em></li>`;

        inner.innerHTML =
            `<nav class="md-nav md-nav--secondary" aria-label="Upcoming events">`
            + `<label class="md-nav__title">Upcoming Events</label>`
            + `<ul class="md-nav__list">${listItems}</ul>`
            + `</nav>`;
    }

    // ---------------------------------------------------------------------------
    // ---------------------------------------------------------------------------
    // Fetch + lazy-load trigger
    // ---------------------------------------------------------------------------

    function load(container) {
        const src = container.dataset.json;
        if (!src) return;

        const searchSrc = container.dataset.search
            || src.replace(/\.json$/, '_search.json');

        // Derive Indico category ID from the JSON filename (category_492.json → 492).
        const catId = (src.match(/category[_/](\d+)/) || [])[1];
        const indicoSearchBase = catId
            ? `https://indico.cern.ch/category/${catId}/search`
            : null;

        container.innerHTML = '<p><em>Loading…</em></p>';

        Promise.all([
            fetch(src).then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); }),
            fetch(searchSrc).then(r => r.ok ? r.json() : []).catch(() => []),
            loadFuse(),
        ]).then(([data, index, FuseClass]) => {
            const events = (Array.isArray(data) ? data : (data.events || []))
                .filter(ev => ev._type !== 'category_metadata' && ev.date)
                .sort((a, b) => b.date.localeCompare(a.date));

            // Pre-compute all derived values once — sort never re-derives them.
            const allRows = events.map(buildRow);

            fillSidebar(allRows);

            const meetingWorker = new MeetingWorker(index);
            const contributionWorker = new ContributionWorker(index);
            const speakerWorker = new SpeakerWorker(index);
            if (FuseClass) {
                [meetingWorker, contributionWorker, speakerWorker]
                    .forEach(w => w.init(FuseClass));
            }

            // --- state ---
            let currentRows = allRows;
            let sortKey = 'date';
            let sortDir = -1;
            let currentView = localStorage.getItem('indico-view-pref') || 'cards';
            let rafId = null;

            // Single RAF-gated render — batches any state changes in the same frame.
            function scheduleRender() {
                if (rafId) cancelAnimationFrame(rafId);
                rafId = requestAnimationFrame(() => {
                    rafId = null;
                    if (currentView === 'table') {
                        renderTable(container, currentRows, sortKey, sortDir);
                    } else {
                        renderCards(container, currentRows);
                    }
                });
            }

            // --- toolbar ---
            const toolbar = buildToolbar(currentView, indicoSearchBase);
            container.parentNode.insertBefore(toolbar, container);
            const input = toolbar.querySelector('input');
            const countEl = toolbar.querySelector('.indico-search-count');
            const indicoBtn = toolbar.querySelector('.indico-search-btn');

            // Search
            let searchTimer;
            input.addEventListener('input', e => {
                clearTimeout(searchTimer);
                searchTimer = setTimeout(() => {
                    const query = e.target.value.trim();
                    if (!query) {
                        currentRows = allRows;
                        countEl.textContent = '';
                        if (indicoBtn) indicoBtn.href = indicoSearchBase;
                    } else {
                        const urls = new Set([
                            ...meetingWorker.matchingUrls(query),
                            ...(currentView === 'table' ? [] : contributionWorker.matchingUrls(query)),
                            ...speakerWorker.matchingUrls(query),
                        ]);
                        currentRows = allRows.filter(r => urls.has(r.url));
                        countEl.textContent = `${currentRows.length} result${currentRows.length !== 1 ? 's' : ''}`;
                        if (indicoBtn) indicoBtn.href = `${indicoSearchBase}?q=${encodeURIComponent(query)}`;
                    }
                    scheduleRender();
                }, 200);
            });

            // Toolbar button actions
            toolbar.addEventListener('click', e => {
                const btn = e.target.closest('[data-action]');
                if (!btn) return;
                switch (btn.dataset.action) {
                    case 'view':
                        currentView = currentView === 'cards' ? 'table' : 'cards';
                        localStorage.setItem('indico-view-pref', currentView);
                        btn.title = currentView === 'cards' ? 'Switch to table view' : 'Switch to card view';
                        btn.innerHTML = currentView === 'cards' ? ICONS.table : ICONS.cards;
                        scheduleRender();
                        break;
                    case 'dl-txt': downloadTxt(currentRows); break;
                    case 'dl-att': downloadAttachments(currentRows); break;
                    case 'dl-json': downloadJson(currentRows); break;
                }
            });

            // Table sort + minutes toggle via event delegation
            container.addEventListener('click', e => {
                // Table sort — th[data-sort] clicks
                const th = e.target.closest('th[data-sort]');
                if (th) {
                    const key = th.dataset.sort;
                    if (sortKey === key) {
                        sortDir = -sortDir;
                    } else {
                        sortKey = key;
                        sortDir = (key === 'attachCount' || key === 'authorCount') ? -1 : 1;
                    }
                    scheduleRender();
                    return;
                }

                // Minutes toggle — buttons with data-mid
                const btn = e.target.closest('button[data-mid]');
                if (!btn) return;

                const mid     = btn.dataset.mid;
                const minutes = _minutesData.get(mid);
                if (!minutes) return;

                // Determine insertion parent before touching DOM
                const li          = btn.closest('li');
                const admonition  = btn.closest('.admonition');
                const insertParent = li || admonition;
                if (!insertParent) return;

                // Toggle off if already open
                const existing = insertParent.querySelector(`.indico-minutes-panel[data-mid="${CSS.escape(mid)}"]`);
                if (existing) {
                    existing.remove();
                    btn.setAttribute('aria-expanded', 'false');
                    return;
                }

                btn.setAttribute('aria-expanded', 'true');

                const dt    = (minutes.modified_dt || '').slice(0, 10);
                const panel = document.createElement('div');
                panel.className   = 'indico-minutes-panel';
                panel.dataset.mid = mid;
                const header = (minutes.url || dt)
                    ? `<p>`
                        + (minutes.url ? `<a href="${minutes.url}" target="_blank" rel="noopener noreferrer">${ic('extLink')} View on Indico</a>` : '')
                        + (minutes.url && dt ? ` · ` : '')
                        + (dt ? `Last modified: ${dt}` : '')
                        + `</p>`
                    : '';
                panel.innerHTML =
                    `<hr>`
                    + header
                    + `<div class="indico-minutes-html">${minutes.html || ''}</div>`
                    + `<hr>`;

                if (li) {
                    li.appendChild(panel);
                } else {
                    const metaP = admonition.querySelector('p:not(.admonition-title)');
                    if (metaP) metaP.insertAdjacentElement('afterend', panel);
                }
            });

            scheduleRender();

        }).catch(err => {
            container.innerHTML = `<p><em>Could not load meetings: ${err.message}</em></p>`;
        });
    }

    const container = document.getElementById('indico-meetings');
    if (!container) return;

    // Pre-load 300 px before the div enters the viewport
    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) { obs.unobserve(entry.target); load(entry.target); }
            });
        },
        { rootMargin: '300px' }
    );

    observer.observe(container);
})();
