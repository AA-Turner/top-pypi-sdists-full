const $ = (id) => document.getElementById(id);
const view = $("view");
const connWrap = $("conn-wrap");
const connBtn = $("conn-btn");
const connPopover = $("conn-popover");
const connTitle = $("conn-title");
const connBody = $("conn-body");
const modal = $("modal");
const modalTitle = $("modal-title");
const modalBody = $("modal-body");
const modalCopy = $("modal-copy");
const scrollTopBtn = $("scroll-top-btn");
const SCROLL_TOP_AT = 280;

const AUTO_REFRESH_MS = 5_000;

const state = {
    jobsPage: 1,
    jobsFilter: {status: "", spider: ""},
    jobPage: {items: 1, requests: 1, logs: 1},
    requestFilter: "",
    requestIdFilter: null,
    logLevel: "",
    modalRaw: "",
    jobsLoadError: null,
    expandedItemNests: new Set(),
    scrollLoading: false,
    scrollObserver: null,
};

let refreshTimer = null;

const JOB_TAB_ORDER = ["overview", "stats", "items", "requests", "logs"];
const JOB_TABS = new Set(JOB_TAB_ORDER);

const TAB_LABELS = {overview: "Overview", stats: "Stats", items: "Items", requests: "Requests", logs: "Logs"};
const TAB_COUNT_KEYS = {
    stats: "stats_count", items: "items_count", requests: "requests_count", logs: "logs_count",
};
const JOBS_PAGE_SIZE = 10;
const ITEMS_PAGE_SIZE = 20;
const REQUESTS_PAGE_SIZE = 20;
const LOGS_PAGE_SIZE = 25;

const CARD_ICONS = {
    jobs: '<path d="M4 7h16M4 12h16M4 17h10"/>',
    running: '<circle cx="12" cy="12" r="9"/><path d="M10 8.5v7l5.5-3.5z"/>',
    finished: '<path d="M9 12.5l2 2 4.5-4.5"/><circle cx="12" cy="12" r="9"/>',
    spiders: '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M8 7l2 9M16 7l-2 9M7.5 6h9"/>',
    items: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>',
    requests: '<path d="M4 6h16v12H4z"/><path d="M4 10h16"/><path d="M8 14h4"/>',
    success: '<path d="M9 12.5l2 2 6-6"/><circle cx="12" cy="12" r="9"/>',
    failed: '<path d="M15 9l-6 6M9 9l6 6"/><circle cx="12" cy="12" r="9"/>',
    logs: '<path d="M6 5h12v14H6z"/><path d="M9 9h6M9 13h6M9 17h4"/>',
    errors: '<path d="M12 8v5"/><circle cx="12" cy="16" r="0.5" fill="currentColor"/><path d="M10.3 4.5h3.4L20 19H4L10.3 4.5z"/>',
};

const DASHBOARD_CARDS = [["Total jobs", "total_jobs", "jobs"], ["Running", "running", "running"], ["Finished", "finished", "finished"], ["Spiders", "spider_count", "spiders"],];

const JOB_METRICS = [["Items", "items_count", "items"], ["Requests", "requests_count", "requests"], ["Successful", "success_requests", "success"], ["Failed", "failed_requests", "failed"], ["Logs", "logs_count", "logs"], ["Errors", "errors_count", "errors"],];

/** Home jobs table: same metrics as detail cards except Successful. */
const JOB_LIST_METRICS = JOB_METRICS.filter(([, , nav]) => nav !== "success");
const JOBS_TABLE_COLSPAN = 2 + JOB_LIST_METRICS.length + 4;
/** Job metric → tab and optional list filters (hash query: req, level). */
const METRIC_NAV = {
    items: {tab: "items"},
    requests: {tab: "requests"},
    success: {tab: "requests", req: "ok"},
    failed: {tab: "requests", req: "fail"},
    logs: {tab: "logs"},
    errors: {tab: "logs", level: "ERROR"},
};

const jobsTableColgroup = () => `<col style="width:8%"><col style="width:14%">${JOB_LIST_METRICS.map(() => `<col style="width:7%">`).join("")}<col style="width:8%"><col style="width:16%"><col style="width:16%"><col style="width:12%">`;

const jobNavLink = (jobId, label, nav = {tab: "overview"}, extraClass = "") => {
    const cls = extraClass ? `job-count-link ${extraClass}` : "job-count-link";
    return `<button type="button" class="${cls}" data-job-id="${esc(jobId)}" data-nav-tab="${nav.tab}" data-nav-req="${nav.req || ""}" data-nav-level="${nav.level || ""}">${label}</button>`;
};

const jobCountLink = (jobId, count, navKey) => {
    const nav = METRIC_NAV[navKey];
    return nav ? jobNavLink(jobId, fmtNum(count), nav) : fmtNum(count);
};

const jobsTableShell = (bodyRows) => {
    const metricHead = JOB_LIST_METRICS.map(([label, , nav]) => `<th scope="col" class="col-num col-metric-${nav}">${label}</th>`).join("");
    return `<table class="data jobs-table"><colgroup>${jobsTableColgroup()}</colgroup><thead><tr><th scope="col" class="col-text col-job">Job</th><th scope="col" class="col-text col-spider">Spider</th>${metricHead}<th scope="col" class="col-text col-runtime">Runtime</th><th scope="col" class="col-text col-started">Started</th><th scope="col" class="col-text col-finished">Finished</th><th scope="col" class="col-text col-outcome">Outcome</th></tr></thead><tbody>${bodyRows}</tbody></table>`;
};

const jobRowHtml = (j) => {
    const id = esc(j.job_id);
    const metrics = JOB_LIST_METRICS.map(([label, key, nav]) => `<td class="col-num col-metric-${nav}" data-label="${esc(label)}">${jobCountLink(j.job_id, j[key], nav)}</td>`).join("");
    return `<tr data-job-id="${id}"><td class="col-text col-job" data-label="Job">${jobNavLink(j.job_id, id, {tab: "overview"}, "mono")}</td><td class="col-text col-spider" data-label="Spider" title="${esc(j.spider_name)}">${esc(j.spider_name)}</td>${metrics}<td class="col-text col-runtime mono" data-label="Runtime">${esc(fmtJobElapsed(j))}</td><td class="col-text col-started" data-label="Started">${fmtTime(j.started_at)}</td><td class="col-text col-finished" data-label="Finished">${fmtTime(j.finished_at)}</td><td class="col-text col-outcome" data-label="Outcome">${statusPill(j.status)}</td></tr>`;
};

const HOME_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10.5L12 4l8 6.5V19a1 1 0 0 1-1 1h-5v-5.5H10V20H5a1 1 0 0 1-1-1v-8.5z"/></svg>';

const esc = (s) => String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const fmtNum = (n) => {
    if (n == null || n === "") return "—";
    const x = Number(n);
    return Number.isFinite(x) ? x.toLocaleString() : esc(n);
};

const fmtTime = (v) => (v ? esc(String(v).replace("T", " ").slice(0, 19)) : "—");

const parseJobTime = (v) => {
    if (!v) return null;
    const d = new Date(String(v).includes("T") ? String(v) : String(v).replace(" ", "T"));
    return Number.isNaN(d.getTime()) ? null : d;
};

const fmtDuration = (secs) => {
    const s = Math.max(0, Math.round(secs));
    if (s < 60) return `${s}s`;
    const m = Math.floor(s / 60);
    const r = s % 60;
    if (m < 60) return r ? `${m}m ${r}s` : `${m}m`;
    const h = Math.floor(m / 60);
    const rm = m % 60;
    return rm ? `${h}h ${rm}m` : `${h}h`;
};

const fmtJobElapsed = (job) => {
    let secs = Number(job.elapsed_seconds);
    const started = parseJobTime(job.started_at);
    if ((job.status || "").toLowerCase() === "running" && started) {
        secs = Math.max(Number.isFinite(secs) ? secs : 0, (Date.now() - started.getTime()) / 1000);
    }
    if (!Number.isFinite(secs) || secs <= 0) return started ? fmtDuration((Date.now() - started.getTime()) / 1000) : "—";
    return fmtDuration(secs);
};

const cardIcon = (name) => {
    const body = CARD_ICONS[name];
    return body ? `<span class="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">${body}</svg></span>` : "";
};

const dashCardBody = (label, value, variant) => `<div class="dash-card-header">${cardIcon(variant)}<label>${esc(label)}</label></div><strong>${typeof value === "number" ? fmtNum(value) : esc(value)}</strong>`;

const dashCard = (label, value, variant) => `<div class="dash-card dash-card--${variant}">${dashCardBody(label, value, variant)}</div>`;

const jobIdPath = (jobId) => String(jobId ?? "")
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");

const jobApiPath = (jobId, suffix = "") => `/api/jobs/${jobIdPath(jobId)}${suffix}`;

const jobHash = (jobId, tab, {req = "", level = ""} = {}) => {
    const q = new URLSearchParams({tab});
    if (req) q.set("req", req);
    if (level) q.set("level", level);
    return `#/job/${jobIdPath(jobId)}?${q}`;
};

const goJobTab = (jobId, tab, {req = "", level = ""} = {}) => {
    Object.keys(state.jobPage).forEach((k) => {
        state.jobPage[k] = 1;
    });
    setHash(jobHash(jobId, tab, {req, level}));
};

const statusPill = (status) => {
    const s = (status || "unknown").toLowerCase();
    const cls = s === "finished" ? "finished" : s === "running" ? "running" : "muted";
    return `<span class="pill ${cls}">${esc(s)}</span>`;
};

const skeletonHtml = () => `<div class="panel skeleton-panel"><div class="skeleton-line w40"></div><div class="skeleton-line w60"></div><div class="skeleton-line w80"></div></div>`;

const emptyState = (icon, title, hint) => `<div class="empty-state"><div class="empty-state-icon">${icon}</div><p><strong>${esc(title)}</strong></p>${hint ? `<p>${esc(hint)}</p>` : ""}</div>`;

const jobsPageErrorHtml = (message) => `<div class="jobs-board">${breadcrumbHomeOnly()}<div class="panel jobs-panel jobs-panel--error"><div class="error-banner error-banner--page" role="alert"><p class="error-banner-title">Could not load jobs</p><p class="error-banner-detail">${esc(message)}</p></div></div></div>`;

const tabToolbar = (inner = "") => `<div class="tab-toolbar"><div class="tab-toolbar-start">${inner}</div></div>`;

const tabToolbarSpacer = () => tabToolbar();

const jobStaticTabHtml = (panel) => `${tabToolbarSpacer()}<div class="items-list">${panel}</div>`;

const infiniteListBody = (listKey, chunk, empty) => chunk ? `<div class="items-list" data-infinite-list="${listKey}">${chunk}</div>` : emptyState(...empty);

const jobListQuery = (page, pageSize, extra = {}) => {
    const q = new URLSearchParams({page: String(page), page_size: String(pageSize)});
    Object.entries(extra).forEach(([k, v]) => {
        if (v != null && v !== "") q.set(k, String(v));
    });
    return q;
};

const bindOnReset = (container, reset, pairs) => {
    if (!reset) return;
    pairs.forEach(([sel, type, fn]) => container.querySelector(sel)?.addEventListener(type, fn));
};

const clearAutoRefresh = () => {
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = null;
};

function teardownInfiniteScroll() {
    state.scrollObserver?.disconnect();
    state.scrollObserver = null;
    state.scrollLoading = false;
}

function infiniteFooter(loaded, total, {loading = false} = {}) {
    const msg = loading ? "Loading more…" : `Showing ${fmtNum(loaded)} of ${fmtNum(total)} · scroll for more`;
    return `<div class="infinite-footer" data-infinite-footer><span>${msg}</span><div class="infinite-sentinel" aria-hidden="true"></div></div>`;
}

function setupInfiniteScroll(container, hasMore, onLoadMore) {
    state.scrollObserver?.disconnect();
    const sentinel = container.querySelector(".infinite-sentinel");
    if (!hasMore || !sentinel) {
        state.scrollObserver = null;
        return;
    }
    state.scrollObserver = new IntersectionObserver((entries) => {
        if (!entries.some((e) => e.isIntersecting) || state.scrollLoading) return;
        onLoadMore();
    }, {root: null, rootMargin: "320px 0px", threshold: 0});
    state.scrollObserver.observe(sentinel);
}

function setInfiniteLoading(container, loading) {
    state.scrollLoading = loading;
    container.querySelector("[data-infinite-footer]")?.classList.toggle("is-loading", loading);
}

function patchInfiniteFooter(container, loaded, total, done) {
    const foot = container.querySelector("[data-infinite-footer]");
    if (done) {
        foot?.remove();
        return;
    }
    const html = infiniteFooter(loaded, total);
    if (foot) foot.outerHTML = html; else if (total) container.insertAdjacentHTML("beforeend", html);
}

async function loadPagedTab(container, jobId, cfg, reset = false) {
    const {key, pageSize, url, loadingLabel, renderChunk, buildShell, afterPage} = cfg;
    if (state.scrollLoading || (!reset && container.dataset[`${key}Done`] === "1")) return;

    const page = reset ? 1 : Number(container.dataset[`${key}Page`] || 0) + 1;
    if (reset) {
        container.dataset[`${key}Page`] = "0";
        container.dataset[`${key}Done`] = "";
        container.innerHTML = `<div class="empty">Loading ${loadingLabel}…</div>`;
    }

    setInfiniteLoading(container, true);
    let data;
    try {
        data = await api(url(jobId, page));
    } catch (err) {
        if (reset) container.innerHTML = `<div class="error-banner">${esc(err.message)}</div>`;
        setInfiniteLoading(container, false);
        return;
    }

    const pageSz = data.page_size || pageSize;
    const base = (data.page - 1) * pageSz;
    const chunk = renderChunk(data, base, container);
    const loaded = base + data.items.length;
    const done = data.page >= data.pages;
    const footer = data.total && !done ? infiniteFooter(loaded, data.total) : "";

    if (reset) {
        container.innerHTML = buildShell(chunk, data, footer);
    } else {
        container.querySelector(`[data-infinite-list="${key}"]`)?.insertAdjacentHTML("beforeend", chunk);
        patchInfiniteFooter(container, loaded, data.total, done);
    }

    container.dataset[`${key}Page`] = String(data.page);
    container.dataset[`${key}Done`] = done ? "1" : "";
    state.jobPage[key] = data.page;
    afterPage?.(container, jobId, {reset, data});
    setInfiniteLoading(container, false);
    setupInfiniteScroll(container, !done, () => loadPagedTab(container, jobId, cfg, false));
}

const syncAutoRefresh = () => {
    clearAutoRefresh();
    if (state.jobsLoadError) return;
    const route = parseRoute();
    if (route.name === "jobs" || route.name === "job") {
        refreshTimer = setInterval(autoRefreshTick, AUTO_REFRESH_MS);
    }
};

function patchJobSummary(job) {
    const grid = view.querySelector(".dash-grid.job-metrics");
    if (grid) {
        grid.innerHTML = JOB_METRICS.map(([label, key, variant]) => dashCard(label, job[key], variant)).join("");
    }
    view.querySelectorAll(".tab[data-tab]").forEach((btn) => {
        const countKey = TAB_COUNT_KEYS[btn.dataset.tab];
        if (!countKey) return;
        const val = fmtNum(job[countKey]);
        let badge = btn.querySelector(".tab-badge");
        if (badge) badge.textContent = val; else {
            btn.insertAdjacentHTML("beforeend", `<span class="tab-badge">${val}</span>`);
        }
    });
}

async function refreshJobSummary(jobId) {
    if (!view.querySelector(".job-board")) return;
    try {
        patchJobSummary(await api(jobApiPath(jobId)));
    } catch {
        /* background poll */
    }
}

async function autoRefreshTick() {
    if (document.hidden || !modal.hidden || state.jobsLoadError) return;
    const route = parseRoute();
    if (route.name === "jobs") await renderJobs({keepSpiderFocus: true}); else if (route.name === "job") await refreshJobSummary(route.jobId);
}

const filterSelect = (id, label, value, options) => `<select id="${id}" aria-label="${label}">${options
    .map(([v, t]) => `<option value="${v}"${value === v ? " selected" : ""}>${t}</option>`)
    .join("")}</select>`;

const LOG_LEVEL_OPTS = [["", "All levels"], ["ERROR", "ERROR"], ["WARNING", "WARNING"], ["INFO", "INFO"], ["DEBUG", "DEBUG"],];

const REQ_FILTER_OPTS = [["", "All requests"], ["ok", "Successful only"], ["fail", "Failed only"],];

const pagerHtml = (page, pages, total) => `<div class="pager"><span>${fmtNum(total)} row(s) · page ${page} of ${pages}</span><div class="pager-actions"><button type="button" class="btn" data-page="prev" ${page <= 1 ? "disabled" : ""}>← Prev</button><button type="button" class="btn" data-page="next" ${page >= pages ? "disabled" : ""}>Next →</button></div></div>`;

const bindPager = (container, page, pages, cb) => {
    container.querySelectorAll("[data-page]").forEach((btn) => {
        btn.addEventListener("click", () => {
            const dir = btn.getAttribute("data-page");
            if (dir === "prev" && page > 1) cb(page - 1);
            if (dir === "next" && page < pages) cb(page + 1);
        });
    });
};

const filterParams = (base = {}) => {
    const q = new URLSearchParams(base);
    const dq = new URLSearchParams();
    for (const key of ["status", "spider"]) {
        if (state.jobsFilter[key]) {
            q.set(key, state.jobsFilter[key]);
            dq.set(key, state.jobsFilter[key]);
        }
    }
    return {q, dq};
};

const breadcrumbHomeOnly = () => `<nav class="breadcrumb" aria-label="Breadcrumb"><span class="breadcrumb-home is-current" aria-current="page" title="Home">${HOME_ICON}</span></nav>`;

const breadcrumbForJob = (spiderName, jobId) => {
    const spider = spiderName || "Job";
    const spiderQ = encodeURIComponent(spider);
    return `<nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/" class="breadcrumb-home" aria-label="Home" title="Home">${HOME_ICON}</a><span class="breadcrumb-sep">/</span><a href="#/?spider=${spiderQ}" class="breadcrumb-parent breadcrumb-link">${esc(spider)}</a><span class="breadcrumb-sep">/</span><button type="button" class="job-id-copy breadcrumb-job-id" data-copy="${esc(jobId)}" title="Click to copy">${esc(jobId)}</button></nav>`;
};

const highlightJson = (obj) => JSON.stringify(obj, null, 2).replace(/("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g, (match, str, colon, bool) => {
    if (colon) return `<span class="json-key">${str}</span>${colon}`;
    if (bool) return `<span class="json-bool">${bool}</span>`;
    if (match === "null") return `<span class="json-null">null</span>`;
    if (/^-?\d/.test(match)) return `<span class="json-num">${match}</span>`;
    return `<span class="json-str">${match}</span>`;
});

function initTheme() {
    const saved = localStorage.getItem("ingest-dashboard-theme");
    document.documentElement.setAttribute("data-theme", saved === "light" ? "light" : "dark");
}

function toggleTheme() {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("ingest-dashboard-theme", next);
}

initTheme();
$("theme-toggle")?.addEventListener("click", toggleTheme);

view.addEventListener("click", (e) => {
    const jobNav = e.target.closest(".job-count-link");
    if (jobNav?.dataset.jobId) {
        e.preventDefault();
        e.stopPropagation();
        goJobTab(jobNav.dataset.jobId, jobNav.dataset.navTab || "overview", {
            req: jobNav.dataset.navReq || "", level: jobNav.dataset.navLevel || "",
        });
        return;
    }
    const nestBtn = e.target.closest(".item-nest-toggle");
    if (nestBtn) {
        e.preventDefault();
        e.stopPropagation();
        const wrap = nestBtn.closest(".item-nest-collapse");
        if (wrap) setNestCollapsed(wrap, nestBtn.classList.contains("item-nest-toggle--collapse"));
        return;
    }
    const btn = e.target.closest(".log-more");
    if (!btn) return;
    const box = btn.closest(".log-msg--expandable");
    const full = box?.querySelector(".log-msg-full");
    if (!full) return;
    const on = box.classList.toggle("is-expanded");
    btn.closest(".log-row")?.classList.toggle("is-expanded", on);
    btn.textContent = on ? "Less" : "More";
    full.hidden = !on;
});
const copyYear = $("copy-year");
if (copyYear) copyYear.textContent = String(new Date().getFullYear());

const formatApiError = (detail, fallback) => {
    if (typeof detail === "string" && detail.trim()) return detail;
    if (Array.isArray(detail)) {
        return detail
            .map((d) => (d && typeof d === "object" && d.msg ? d.msg : String(d ?? "")))
            .filter(Boolean)
            .join("; ");
    }
    if (detail && typeof detail === "object" && detail.message) return String(detail.message);
    return fallback;
};

async function api(path) {
    const res = await fetch(path, {cache: "no-store"});
    if (!res.ok) {
        let detail = res.statusText || "Request failed";
        const raw = await res.text();
        if (raw) {
            try {
                detail = formatApiError(JSON.parse(raw).detail, detail);
            } catch (_) {
                detail = raw.trim() || detail;
            }
        }
        throw new Error(detail || "Request failed");
    }
    return res.json();
}

const parseRoute = () => {
    const hash = location.hash.replace(/^#/, "") || "/";
    const [pathPart, queryPart] = hash.split("?");
    const params = new URLSearchParams(queryPart || "");
    if (pathPart.startsWith("/job/")) {
        const tabParam = params.get("tab") || "items";
        const tab = JOB_TABS.has(tabParam) ? tabParam : "items";
        const req = params.get("req");
        const level = params.get("level");
        const rawId = pathPart.slice("/job/".length).replace(/\/+$/, "");
        return {
            name: "job",
            jobId: decodeURIComponent(rawId),
            tab,
            req: req === "ok" || req === "fail" ? req : "",
            logLevel: level ? level.toUpperCase() : "",
        };
    }
    return {
        name: "jobs", spider: params.get("spider") || "", status: params.get("status") || "",
    };
};

const setHash = (path) => {
    if (location.hash !== path) location.hash = path;
};

function openModal(title, obj) {
    modalTitle.textContent = title;
    state.modalRaw = JSON.stringify(obj, null, 2);
    modalBody.innerHTML = highlightJson(obj);
    modal.hidden = false;
}

function closeModal() {
    modal.hidden = true;
}

modal.querySelectorAll("[data-close]").forEach((el) => el.addEventListener("click", closeModal));
modalCopy?.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(state.modalRaw);
        modalCopy.textContent = "Copied";
        setTimeout(() => {
            modalCopy.textContent = "Copy";
        }, 1500);
    } catch (_) {
    }
});

document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    closeModal();
    setConnOpen(false);
});

function renderConnection(info) {
    if (!connTitle || !connBody) return;
    connTitle.textContent = info.title || "Connection";
    const rows = [["Type", info.destination === "database" ? info.kind : "search"], ["Endpoint", info.display_url], info.schema ? ["Schema", info.schema] : null, ["Jobs table", info.jobs_table], ["Items table", info.items_table],]
        .filter(Boolean)
        .map(([k, v]) => `<div class="conn-row"><dt>${esc(k)}</dt><dd class="mono">${esc(v)}</dd></div>`)
        .join("");
    connBody.innerHTML = rows || '<p class="conn-empty">No connection info</p>';
}

function setConnOpen(open) {
    if (!connWrap || !connBtn || !connPopover) return;
    connWrap.classList.toggle("open", open);
    connBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) connPopover.removeAttribute("hidden"); else connPopover.setAttribute("hidden", "");
}

if (connBtn && connWrap) {
    connBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        setConnOpen(!connWrap.classList.contains("open"));
    });
    document.addEventListener("click", (e) => {
        if (!connWrap.contains(e.target)) setConnOpen(false);
    });
}

let healthInfo = null;

async function loadHealth() {
    if (healthInfo) {
        renderConnection(healthInfo);
        return;
    }
    try {
        healthInfo = await api("/api/health");
        renderConnection(healthInfo);
    } catch {
        if (connBody) connBody.innerHTML = '<p class="conn-empty">Could not load connection</p>';
    }
}

function bindJobIdCopy(root) {
    root.querySelectorAll(".job-id-copy").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            navigator.clipboard.writeText(btn.dataset.copy || "").catch(() => {
            });
            btn.classList.add("is-copied");
            btn.setAttribute("title", "Copied!");
            setTimeout(() => {
                btn.classList.remove("is-copied");
                btn.setAttribute("title", "Click to copy");
            }, 1600);
        });
    });
}

const statusCodeClass = (code) => {
    const n = Number(code);
    if (!Number.isFinite(n)) return "";
    if (n >= 200 && n < 400) return "ok";
    if (n < 500) return "warn";
    return "bad";
};

const dashboardCards = (d) => `<div class="dash-grid" role="region" aria-label="Job statistics">${DASHBOARD_CARDS.map(([label, key, variant]) => dashCard(label, d[key], variant)).join("")}</div>`;

async function renderJobs({keepSpiderFocus = false} = {}) {
    view.classList.add("view--dash");
    let spiderCaret = null;
    if (keepSpiderFocus) {
        const active = view.querySelector("#filter-spider");
        if (active && document.activeElement === active) {
            spiderCaret = {start: active.selectionStart, end: active.selectionEnd};
        }
    } else {
        view.innerHTML = skeletonHtml();
    }
    const {q, dq} = filterParams({page: String(state.jobsPage), page_size: String(JOBS_PAGE_SIZE)});
    try {
        const [data, dash] = await Promise.all([api(`/api/jobs?${q}`), api(`/api/dashboard?${dq}`)]);
        state.jobsLoadError = null;
        const body = data.items.map(jobRowHtml).join("") || `<tr class="row-static"><td colspan="${JOBS_TABLE_COLSPAN}">${emptyState("📭", "No jobs yet", "Run a spider with ingest enabled, then refresh.")}</td></tr>`;
        view.innerHTML = `<div class="jobs-board">${breadcrumbHomeOnly()}${dashboardCards(dash)}<div class="panel jobs-panel"><div class="panel-head"><div><h2>Recent jobs</h2></div><div class="toolbar"><div class="field"><label for="filter-spider">Spider</label><input type="search" id="filter-spider" placeholder="Filter by name…" value="${esc(state.jobsFilter.spider)}" autocomplete="off" /></div><div class="field"><label for="filter-status">Status</label><select id="filter-status"><option value="">All</option><option value="running" ${state.jobsFilter.status === "running" ? "selected" : ""}>Running</option><option value="finished" ${state.jobsFilter.status === "finished" ? "selected" : ""}>Finished</option></select></div></div></div><div class="table-wrap">${jobsTableShell(body)}</div>${pagerHtml(data.page, data.pages, data.total)}</div></div>`;
        const spiderInput = view.querySelector("#filter-spider");
        let spiderTimer;
        spiderInput.addEventListener("keyup", () => {
            clearTimeout(spiderTimer);
            spiderTimer = setTimeout(() => {
                const v = spiderInput.value.trim();
                if (v === state.jobsFilter.spider) return;
                state.jobsFilter.spider = v;
                state.jobsPage = 1;
                renderJobs({keepSpiderFocus: true});
            }, 300);
        });
        if (spiderCaret) {
            const el = view.querySelector("#filter-spider");
            if (el) {
                el.focus();
                el.setSelectionRange(spiderCaret.start, spiderCaret.end);
            }
        }
        view.querySelector("#filter-status").addEventListener("change", (e) => {
            state.jobsFilter.status = e.target.value;
            state.jobsPage = 1;
            renderJobs();
        });
        bindPager(view, data.page, data.pages, (p) => {
            state.jobsPage = p;
            renderJobs();
        });
        syncAutoRefresh();
    } catch (err) {
        const message = err?.message || "Request failed";
        state.jobsLoadError = message;
        view.innerHTML = jobsPageErrorHtml(message);
        clearAutoRefresh();
    }
}

const jobTabHtml = (name, active, job) => {
    const countKey = TAB_COUNT_KEYS[name];
    const badge = countKey != null ? `<span class="tab-badge">${fmtNum(job[countKey])}</span>` : "";
    return `<button type="button" role="tab" class="tab ${active ? "active" : ""}" data-tab="${name}" aria-selected="${active ? "true" : "false"}"><span class="tab-label">${TAB_LABELS[name]}</span>${badge}</button>`;
};

async function renderJob(jobId, tab) {
    teardownInfiniteScroll();
    view.classList.remove("view--dash");
    view.innerHTML = skeletonHtml();
    try {
        const job = await api(jobApiPath(jobId));
        const tabs = JOB_TAB_ORDER.map((t) => jobTabHtml(t, t === tab, job)).join("");
        const metrics = JOB_METRICS.map(([label, key, variant]) => dashCard(label, job[key], variant)).join("");
        view.innerHTML = `<div class="jobs-board job-board">${breadcrumbForJob(job.spider_name || "Job", job.job_id)}<div class="dash-grid job-metrics">${metrics}</div><div class="panel panel--tabs job-detail-panel"><div class="tab-frame"><div class="tabs-row"><nav class="tabs" role="tablist" aria-label="Job sections">${tabs}</nav><div class="tabs-status">${statusPill(job.status)}</div></div><div id="tab-body" class="tab-body" role="tabpanel"></div></div></div></div>`;
        bindJobIdCopy(view);
        view.querySelectorAll(".tab").forEach((btn) => {
            btn.addEventListener("click", () => goJobTab(jobId, btn.dataset.tab));
        });
        const body = view.querySelector("#tab-body");
        const tabRender = {
            overview: () => renderOverviewTab(body, job),
            stats: () => renderStatsTab(body, job),
            items: () => renderItemsTab(body, jobId),
            requests: () => renderRequestsTab(body, jobId),
            logs: () => renderLogsTab(body, jobId),
        };
        await tabRender[tab]?.();
        syncAutoRefresh();
    } catch (err) {
        view.innerHTML = `<div class="error-banner">${esc(err.message)}</div>`;
        clearAutoRefresh();
    }
}

/** Collapse toggle when sibling count exceeds this (5+ rows). */
const ITEM_NEST_COLLAPSE_AT = 4;

const nestChevronSvg = (d) => `<span class="item-nest-chevron" aria-hidden="true"><svg class="item-nest-chevron-svg" viewBox="0 0 16 16" width="13" height="13"><path d="${d}" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/></svg></span>`;

const NEST_ICON = {
    expand: nestChevronSvg("M6 3.5 10.5 8 6 12.5"), collapse: nestChevronSvg("M3.5 10 8 5.5 12.5 10"),
};

function isItemObject(v) {
    return v !== null && typeof v === "object" && !Array.isArray(v);
}

function isScalarItem(v) {
    return !isItemObject(v) && !Array.isArray(v);
}

function wrapCollapsibleNest(rows, {nestPath = "", badgeCount = rows.length} = {}) {
    if (rows.length <= ITEM_NEST_COLLAPSE_AT) return rows.join("");
    const label = esc(badgeCount === 1 ? "Expand 1 item" : `Expand ${badgeCount} items`);
    const pathAttr = nestPath ? ` data-nest-path="${esc(nestPath)}"` : "";
    const body = rows.join("");
    return `<div class="item-nest-collapse" data-collapsed="true"${pathAttr}>
    <button type="button" class="item-nest-toggle item-nest-toggle--expand" aria-expanded="false">${NEST_ICON.expand} ${label}</button>
    <div class="item-nest-body">${body}</div>
    <button type="button" class="item-nest-toggle item-nest-toggle--collapse" aria-expanded="false">${NEST_ICON.collapse} Collapse</button>
  </div>`;
}

function setNestCollapsed(wrap, collapsed) {
    wrap.dataset.collapsed = collapsed ? "true" : "false";
    const path = wrap.dataset.nestPath;
    if (path) (collapsed ? state.expandedItemNests.delete(path) : state.expandedItemNests.add(path));
    const open = String(!collapsed);
    wrap.querySelector(".item-nest-toggle--expand")?.setAttribute("aria-expanded", open);
    wrap.querySelector(".item-nest-toggle--collapse")?.setAttribute("aria-expanded", open);
}

function syncExpandedItemNests(container, mode) {
    if (mode === "save") {
        container.querySelectorAll('.item-nest-collapse[data-collapsed="false"]').forEach((el) => {
            if (el.dataset.nestPath) state.expandedItemNests.add(el.dataset.nestPath);
        });
        return;
    }
    state.expandedItemNests.forEach((path) => {
        const el = container.querySelector(`.item-nest-collapse[data-nest-path="${CSS.escape(path)}"]`);
        if (el) setNestCollapsed(el, false);
    });
}

function formatItemValue(v) {
    if (v === null || v === undefined) return '<span class="item-placeholder">N/A</span>';
    if (typeof v === "boolean") return esc(String(v));
    if (typeof v === "number") return esc(String(v));
    const s = String(v);
    if (/^https?:\/\//i.test(s)) {
        return `<a href="${esc(s)}" target="_blank" rel="noopener">${esc(s)}</a>`;
    }
    return esc(s);
}

function itemNestShell(inner, depth, root = false) {
    const cls = root ? "item-nest item-nest--root" : "item-nest";
    return `<div class="${cls}" style="--nest:${depth}">${inner}</div>`;
}

function itemNestEntries(entries, depth, nestPath) {
    const blocks = entries.map(([k, v]) => itemFieldBlock(k, v, depth, `${nestPath}/${k}`));
    return wrapCollapsibleNest(blocks, {nestPath, badgeCount: entries.length});
}

function itemArrayRow(el, depth, path) {
    if (isItemObject(el)) {
        return `<div class="item-nest-group">${itemNestEntries(Object.entries(el), depth, path)}</div>`;
    }
    if (Array.isArray(el)) return itemNestShell(itemArrayInner(el, depth, path), depth);
    return `<div class="item-scalar">${formatItemValue(el)}</div>`;
}

function itemArrayInner(value, depth, nestPath) {
    if (!value.length) return '<span class="item-placeholder">[]</span>';
    let rows;
    if (value.every(isItemObject)) {
        rows = value.map((obj, i) => itemArrayRow(obj, depth + 1, `${nestPath}/${i}`));
    } else if (value.every(isScalarItem)) {
        rows = value.map((el) => `<div class="item-scalar">${formatItemValue(el)}</div>`);
    } else {
        rows = value.map((el, i) => itemArrayRow(el, depth + 1, `${nestPath}/${i}`));
    }
    return wrapCollapsibleNest(rows, {nestPath, badgeCount: rows.length});
}

function itemFieldBlock(key, value, depth, nestPath) {
    const k = `<div class="item-k">${esc(key)}</div>`;
    if (Array.isArray(value)) {
        if (!value.length) return `<div class="item-field">${k}<div class="item-v"><span class="item-placeholder">[]</span></div></div>`;
        return `<div class="item-field item-field--branch">${k}${itemNestShell(itemArrayInner(value, depth + 1, nestPath), depth)}</div>`;
    }
    if (isItemObject(value)) {
        if (!Object.keys(value).length) return `<div class="item-field">${k}<div class="item-v"><span class="item-placeholder">{}</span></div></div>`;
        return `<div class="item-field item-field--branch">${k}${itemNestShell(itemNestEntries(Object.entries(value), depth + 1, nestPath), depth)}</div>`;
    }
    return `<div class="item-field">${k}<div class="item-v">${formatItemValue(value)}</div></div>`;
}

function itemValueCell(value, depth = 0, nestPath = "root") {
    if (Array.isArray(value)) {
        return value.length ? itemNestShell(itemArrayInner(value, depth + 1, nestPath), depth, true) : '<span class="item-placeholder">[]</span>';
    }
    if (isItemObject(value)) {
        return Object.keys(value).length ? itemNestShell(itemNestEntries(Object.entries(value), depth + 1, nestPath), depth, true) : '<span class="item-placeholder">{}</span>';
    }
    return formatItemValue(value);
}

function itemFieldsTable(item, itemIndex) {
    const root = isItemObject(item) ? item : {value: item};
    const keys = Object.keys(root);
    if (!keys.length) {
        return '<p class="item-empty-fields">No fields</p>';
    }
    const rows = Object.entries(root)
        .map(([k, v]) => `<tr class="item-root-row"><th scope="row">${esc(k)}</th><td class="item-root-val">${itemValueCell(v, 0, `i${itemIndex}/${k}`)}</td></tr>`)
        .join("");
    return `<table class="item-fields"><tbody>${rows}</tbody></table>`;
}

function itemPanelHtml(row, itemIndex) {
    return `<article class="item-panel"><header class="item-panel-head"><div class="item-panel-title"><span class="item-panel-label">Item</span> <span class="item-panel-id">${esc(itemIndex)}</span><time class="item-panel-time">${fmtTime(row.created_at)}</time></div><button type="button" class="btn btn-sm btn-ghost item-json-btn" data-json-idx="${itemIndex}">JSON</button></header>${itemFieldsTable(row.item, itemIndex)}</article>`;
}

function bindItemJsonButtons(container) {
    if (!container._itemsData) container._itemsData = [];
    container.querySelectorAll(".item-json-btn[data-json-idx]").forEach((btn) => {
        if (btn.dataset.bound) return;
        btn.dataset.bound = "1";
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const row = container._itemsData[Number(btn.dataset.jsonIdx)];
            if (row) openModal("Item JSON", row.item);
        });
    });
}

const ITEMS_TAB = {
    key: "items",
    pageSize: ITEMS_PAGE_SIZE,
    loadingLabel: "items",
    url: (jobId, page) => `${jobApiPath(jobId)}/items?page=${page}&page_size=${ITEMS_PAGE_SIZE}`,
    renderChunk(data, base, container) {
        if (!container._itemsData) container._itemsData = [];
        return data.items
            .map((row, i) => {
                const idx = base + i;
                container._itemsData[idx] = row;
                return itemPanelHtml(row, idx);
            })
            .join("");
    },
    buildShell: (chunk, _data, footer) => `${tabToolbarSpacer()}${infiniteListBody("items", chunk, ["📦", "No items", "This job has not scraped any items yet."])}${footer}`,
    afterPage(container) {
        bindItemJsonButtons(container);
    },
};

async function renderItemsTab(container, jobId) {
    state.expandedItemNests.clear();
    container._itemsData = [];
    await loadPagedTab(container, jobId, ITEMS_TAB, true);
}

function formatDurationMs(secs) {
    if (secs == null || secs === "") return null;
    const n = Number(secs);
    if (!Number.isFinite(n)) return null;
    return `${Math.round(n * 1000).toLocaleString()} ms`;
}

function requestFieldRow(label, valueHtml) {
    return `<tr class="item-root-row"><th scope="row">${esc(label)}</th><td class="item-root-val">${valueHtml}</td></tr>`;
}

function fieldsTableHtml(rowsHtml) {
    return `<table class="item-fields"><tbody>${rowsHtml}</tbody></table>`;
}

function detailPanelHtml(label, panelId, timeText, bodyHtml, extraClass = "") {
    const timePart = timeText ? `<time class="item-panel-time">${timeText}</time>` : "";
    const cls = extraClass ? `item-panel ${extraClass}` : "item-panel";
    return `<article class="${cls}"><header class="item-panel-head"><div class="item-panel-title"><span class="item-panel-label">${esc(label)}</span> <span class="item-panel-id">${esc(String(panelId))}</span>${timePart}</div></header>${bodyHtml}</article>`;
}

function overviewSectionRow(label) {
    return `<tr class="overview-section-row"><td colspan="2">${esc(label)}</td></tr>`;
}

function renderOverviewTab(body, job) {
    const rows = [requestFieldRow("Started", fmtTime(job.started_at)), requestFieldRow("Finished", fmtTime(job.finished_at)), requestFieldRow("Finish reason", esc(job.finish_reason || "—")), requestFieldRow("Elapsed", esc(job.elapsed_seconds != null ? `${job.elapsed_seconds}s` : "—")), requestFieldRow("Scrape rate", esc(job.items_per_min != null ? `${job.items_per_min}/min` : "—")), overviewSectionRow("Spider args"),];

    const args = job.spider_args && typeof job.spider_args === "object" ? job.spider_args : null;
    const argKeys = args ? Object.keys(args) : [];
    if (argKeys.length) {
        argKeys.forEach((k) => {
            rows.push(requestFieldRow(k, itemValueCell(args[k], 0, `spider-args/${k}`)));
        });
    } else {
        rows.push(requestFieldRow("—", '<span class="item-placeholder">No crawl arguments recorded</span>'));
    }

    const panel = detailPanelHtml("Job", job.job_id || "—", fmtTime(job.started_at), fieldsTableHtml(rows.join("")), "overview-panel");
    body.innerHTML = jobStaticTabHtml(panel);
}

function formatStatValue(v) {
    if (v === null || v === undefined) return '<span class="item-placeholder">N/A</span>';
    if (typeof v === "boolean") return esc(String(v));
    if (typeof v === "number") return esc(Number.isInteger(v) ? v.toLocaleString() : String(v));
    if (typeof v === "object") return `<span class="mono">${esc(JSON.stringify(v))}</span>`;
    return formatItemValue(v);
}

function renderStatsTab(container, job) {
    const stats = job.stats;
    const keys = stats && typeof stats === "object" ? Object.keys(stats) : [];
    let panel;
    if (!keys.length) {
        panel = detailPanelHtml("Stats", "—", fmtTime(job.finished_at), '<p class="panel-empty">Scrapy crawl stats appear here when the job finishes or while stats are being collected.</p>', "stats-panel");
    } else {
        const rows = keys
            .sort((a, b) => a.localeCompare(b))
            .map((k) => requestFieldRow(k, formatStatValue(stats[k])))
            .join("");
        panel = detailPanelHtml("Stats", keys.length, fmtTime(job.finished_at || job.started_at), fieldsTableHtml(rows), "stats-panel");
    }
    container.innerHTML = jobStaticTabHtml(panel);
}

function requestFieldsTable(r) {
    const rows = [];
    const ms = formatDurationMs(r.response_time_secs);
    if (ms) rows.push(requestFieldRow("Duration", esc(ms)));
    if (r.fingerprint) {
        rows.push(requestFieldRow("Fingerprint", `<span class="mono">${esc(r.fingerprint)}</span>`));
    }
    rows.push(requestFieldRow("HTTP Method", esc(r.method || "GET")));
    if (r.parent_id != null && r.parent_id !== "") {
        rows.push(requestFieldRow("Parent Request #", `<button type="button" class="link-btn req-parent-link" data-parent-id="${esc(r.parent_id)}">${esc(r.parent_id)}</button>`));
    }
    if (r.response_size_bytes) {
        rows.push(requestFieldRow("Response Size", esc(String(r.response_size_bytes))));
    }
    if (r.status_code != null && r.status_code !== "") {
        rows.push(requestFieldRow("HTTP Status", `<span class="status-code ${statusCodeClass(r.status_code)}">${esc(r.status_code)}</span>`));
    }
    if (r.created_at) rows.push(requestFieldRow("Last Seen", fmtTime(r.created_at)));
    if (r.url) rows.push(requestFieldRow("Url", formatItemValue(r.url)));
    return fieldsTableHtml(rows.join(""));
}

function requestPanelHtml(r, reqIndex) {
    return detailPanelHtml("Request", reqIndex, fmtTime(r.created_at), requestFieldsTable(r), "request-panel");
}

function bindRequestParentLinks(container, jobId) {
    container.querySelectorAll(".req-parent-link[data-parent-id]:not([data-parent-bound])").forEach((btn) => {
        btn.dataset.parentBound = "1";
        btn.addEventListener("click", () => {
            state.requestIdFilter = Number(btn.dataset.parentId);
            renderJob(jobId, "requests");
        });
    });
}

function requestsToolbarHtml() {
    const idFilterBar = state.requestIdFilter != null ? `<div class="req-id-filter"><span>Showing request #${esc(state.requestIdFilter)}</span><button type="button" class="btn btn-sm btn-ghost" id="req-clear-id">Show all requests</button></div>` : "";
    return tabToolbar(`${idFilterBar}${filterSelect("req-filter", "Filter requests", state.requestFilter, REQ_FILTER_OPTS)}`);
}

const REQUESTS_TAB = {
    key: "requests",
    pageSize: REQUESTS_PAGE_SIZE,
    loadingLabel: "requests",
    url(jobId, page) {
        const extra = {};
        if (state.requestFilter === "ok") extra.success = "true"; else if (state.requestFilter === "fail") extra.success = "false";
        if (state.requestIdFilter != null) extra.request_id = state.requestIdFilter;
        return `${jobApiPath(jobId)}/requests?${jobListQuery(page, REQUESTS_PAGE_SIZE, extra)}`;
    },
    renderChunk: (data, base) => data.items.map((r, i) => requestPanelHtml(r, base + i)).join(""),
    buildShell: (chunk, _data, footer) => `${requestsToolbarHtml()}${infiniteListBody("requests", chunk, ["🌐", "No requests", "Request logging may be disabled for this crawl."])}${footer}`,
    afterPage(container, jobId, {reset}) {
        bindOnReset(container, reset, [["#req-filter", "change", (e) => {
            state.requestFilter = e.target.value;
            renderJob(jobId, "requests");
        }], ["#req-clear-id", "click", () => {
            state.requestIdFilter = null;
            renderJob(jobId, "requests");
        }],]);
        bindRequestParentLinks(container, jobId);
    },
};

const renderRequestsTab = (container, jobId) => loadPagedTab(container, jobId, REQUESTS_TAB, true);

const logLineText = (log) => {
    const head = log.logger ? `[${log.logger}] ${log.message ?? ""}` : (log.message ?? "");
    return (log.exception ? `${head}\n${log.exception}` : head).trim();
};

const formatLogText = (text) => esc(text).replace(/(https?:\/\/[^\s<]+)/g, '<a class="log-url" href="$1" target="_blank" rel="noopener">$1</a>');

const LOG_PREVIEW = 220;

const logExpandParts = (text) => {
    const i = text.indexOf("\n");
    const head = i < 0 ? text : text.slice(0, i);
    const tail = i < 0 ? "" : text.slice(i + 1);
    const over = head.length > LOG_PREVIEW;
    let extra = over ? head.slice(LOG_PREVIEW).trimStart() : tail;
    if (over && tail) extra = `${extra}\n${tail}`;
    if (!extra.trim()) return null;
    return {
        preview: over ? `${head.slice(0, LOG_PREVIEW).trimEnd()}…` : head, extra,
    };
};

const logMsgHtml = (text) => {
    const p = logExpandParts(text);
    const head = formatLogText(p ? p.preview : text);
    if (!p) return `<div class="log-msg">${head}</div>`;
    return `<div class="log-msg log-msg--expandable"><div class="log-msg-head">${head} <button type="button" class="link-btn log-more">More</button></div><pre class="log-msg-full" hidden>${formatLogText(p.extra)}</pre></div>`;
};

const logRowHtml = (log, idx) => {
    const lv = String(log.level || "INFO").toUpperCase();
    const rowLv = lv === "CRITICAL" ? "critical" : lv.toLowerCase();
    return `<tr class="log-row log-row--${rowLv}"><td class="log-idx"><span class="log-idx-num">${idx}</span></td><td class="log-time">${fmtTime(log.time)}</td><td><span class="log-level level-${esc(lv)}">${esc(lv)}</span></td><td class="log-msg-cell">${logMsgHtml(logLineText(log))}</td></tr>`;
};

const logsToolbar = () => tabToolbar(filterSelect("log-level", "Filter log level", state.logLevel, LOG_LEVEL_OPTS));

const LOGS_TAB = {
    key: "logs",
    pageSize: LOGS_PAGE_SIZE,
    loadingLabel: "logs",
    url: (jobId, page) => `${jobApiPath(jobId)}/logs?${jobListQuery(page, LOGS_PAGE_SIZE, {level: state.logLevel || null})}`,
    renderChunk: (data, base) => data.items.map((log, i) => logRowHtml(log, base + i)).join(""),
    buildShell(chunk, data, footer) {
        if (!data.items.length) {
            return `${logsToolbar()}${emptyState("📋", "No logs", "No log lines were stored for this job.")}`;
        }
        const panelBody = `<table class="logs-table"><thead><tr><th class="log-idx">#</th><th>Time</th><th>Level</th><th>Message</th></tr></thead><tbody data-infinite-list="logs">${chunk}</tbody></table>`;
        const panel = detailPanelHtml("Logs", fmtNum(data.total), "", panelBody, "logs-panel");
        return `${logsToolbar()}<div class="items-list">${panel}</div>${footer}`;
    },
    afterPage: (container, jobId, {reset}) => bindOnReset(container, reset, [["#log-level", "change", (e) => {
        state.logLevel = e.target.value;
        renderJob(jobId, "logs");
    },],]),
};

const renderLogsTab = (container, jobId) => loadPagedTab(container, jobId, LOGS_TAB, true);

async function render() {
    const route = parseRoute();
    await loadHealth();
    if (route.name === "job") {
        state.requestFilter = route.req;
        state.logLevel = route.logLevel;
        await renderJob(route.jobId, route.tab);
        return;
    }
    state.jobsFilter.spider = route.spider;
    state.jobsFilter.status = route.status;
    state.jobsPage = 1;
    await renderJobs();
}

const syncScrollTopBtn = () => {
    if (scrollTopBtn) scrollTopBtn.hidden = window.scrollY < SCROLL_TOP_AT;
};

scrollTopBtn?.addEventListener("click", () => window.scrollTo({top: 0, behavior: "smooth"}));
window.addEventListener("scroll", syncScrollTopBtn, {passive: true});
document.addEventListener("visibilitychange", () => {
    if (document.hidden || state.jobsLoadError) return;
    autoRefreshTick();
    syncAutoRefresh();
});
window.addEventListener("hashchange", render);
syncScrollTopBtn();
render();
