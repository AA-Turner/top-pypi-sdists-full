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

const AUTO_REFRESH_MS = 5_000;

const state = {
  jobsPage: 1,
  jobsFilter: { status: "", spider: "" },
  jobPage: { items: 1, requests: 1, logs: 1 },
  requestFilter: "",
  requestIdFilter: null,
  logLevel: "",
  modalRaw: "",
  jobsLoadError: null,
};

let refreshTimer = null;

const JOB_TAB_ORDER = ["overview", "stats", "items", "requests", "logs"];
const JOB_TABS = new Set(JOB_TAB_ORDER);

const TAB_LABELS = { overview: "Overview", stats: "Stats", items: "Items", requests: "Requests", logs: "Logs" };
const TAB_COUNT_KEYS = {
  stats: "stats_count",
  items: "items_count",
  requests: "requests_count",
  logs: "logs_count",
};
const JOBS_PAGE_SIZE = 10;

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

const DASHBOARD_CARDS = [
  ["Total jobs", "total_jobs", "jobs"],
  ["Running", "running", "running"],
  ["Finished", "finished", "finished"],
  ["Spiders", "spider_count", "spiders"],
];

const JOB_METRICS = [
  ["Items", "items_count", "items"],
  ["Requests", "requests_count", "requests"],
  ["Successful", "success_requests", "success"],
  ["Failed", "failed_requests", "failed"],
  ["Logs", "logs_count", "logs"],
  ["Errors", "errors_count", "errors"],
];

const HOME_ICON =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10.5L12 4l8 6.5V19a1 1 0 0 1-1 1h-5v-5.5H10V20H5a1 1 0 0 1-1-1v-8.5z"/></svg>';

const esc = (s) =>
  String(s ?? "")
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
  return body
    ? `<span class="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">${body}</svg></span>`
    : "";
};

const dashCard = (label, value, variant) =>
  `<div class="dash-card dash-card--${variant}"><div class="dash-card-header">${cardIcon(variant)}<label>${esc(label)}</label></div><strong>${typeof value === "number" ? fmtNum(value) : esc(value)}</strong></div>`;

const statusPill = (status) => {
  const s = (status || "unknown").toLowerCase();
  const cls = s === "finished" ? "finished" : s === "running" ? "running" : "muted";
  return `<span class="pill ${cls}">${esc(s)}</span>`;
};

const skeletonHtml = () =>
  `<div class="panel skeleton-panel"><div class="skeleton-line w40"></div><div class="skeleton-line w60"></div><div class="skeleton-line w80"></div></div>`;

const emptyState = (icon, title, hint) =>
  `<div class="empty-state"><div class="empty-state-icon">${icon}</div><p><strong>${esc(title)}</strong></p>${hint ? `<p>${esc(hint)}</p>` : ""}</div>`;

const jobsPageErrorHtml = (message) =>
  `<div class="jobs-board">${breadcrumbHomeOnly()}<div class="panel jobs-panel jobs-panel--error"><div class="error-banner error-banner--page" role="alert"><p class="error-banner-title">Could not load jobs</p><p class="error-banner-detail">${esc(message)}</p></div></div></div>`;

const tabToolbar = (inner = "") =>
  `<div class="tab-toolbar"><div class="tab-toolbar-start">${inner}</div></div>`;

const tabToolbarSpacer = () => tabToolbar();

const clearAutoRefresh = () => {
  if (refreshTimer) clearInterval(refreshTimer);
  refreshTimer = null;
};

const syncAutoRefresh = () => {
  clearAutoRefresh();
  if (state.jobsLoadError) return;
  const route = parseRoute();
  if (route.name === "jobs" || (route.name === "job" && route.tab === "items")) {
    refreshTimer = setInterval(autoRefreshTick, AUTO_REFRESH_MS);
  }
};

async function autoRefreshTick() {
  if (document.hidden || !modal.hidden || state.jobsLoadError) return;
  const route = parseRoute();
  if (route.name === "jobs") await renderJobs({ keepSpiderFocus: true });
  else if (route.name === "job" && route.tab === "items") {
    const body = view.querySelector("#tab-body");
    if (body) await renderItemsTab(body, route.jobId, { silent: true });
  }
}

const filterSelect = (id, label, value, options) =>
  `<select id="${id}" aria-label="${label}">${options
    .map(([v, t]) => `<option value="${v}"${value === v ? " selected" : ""}>${t}</option>`)
    .join("")}</select>`;

const LOG_LEVEL_OPTS = [
  ["", "All levels"],
  ["ERROR", "ERROR"],
  ["WARNING", "WARNING"],
  ["INFO", "INFO"],
  ["DEBUG", "DEBUG"],
];

const REQ_FILTER_OPTS = [
  ["", "All requests"],
  ["ok", "Successful only"],
  ["fail", "Failed only"],
];

const pagerHtml = (page, pages, total) =>
  `<div class="pager"><span>${fmtNum(total)} row(s) · page ${page} of ${pages}</span><div class="pager-actions"><button type="button" class="btn" data-page="prev" ${page <= 1 ? "disabled" : ""}>← Prev</button><button type="button" class="btn" data-page="next" ${page >= pages ? "disabled" : ""}>Next →</button></div></div>`;

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
  return { q, dq };
};

const breadcrumbHomeOnly = () =>
  `<nav class="breadcrumb" aria-label="Breadcrumb"><span class="breadcrumb-home is-current" aria-current="page" title="Home">${HOME_ICON}</span></nav>`;

const breadcrumbForJob = (spiderName, jobId) => {
  const spider = spiderName || "Job";
  const spiderQ = encodeURIComponent(spider);
  return `<nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/" class="breadcrumb-home" aria-label="Home" title="Home">${HOME_ICON}</a><span class="breadcrumb-sep">/</span><a href="#/?spider=${spiderQ}" class="breadcrumb-parent breadcrumb-link">${esc(spider)}</a><span class="breadcrumb-sep">/</span><button type="button" class="job-id-copy breadcrumb-job-id" data-copy="${esc(jobId)}" title="Click to copy">${esc(jobId)}</button></nav>`;
};

const highlightJson = (obj) =>
  JSON.stringify(obj, null, 2).replace(
    /("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g,
    (match, str, colon, bool) => {
      if (colon) return `<span class="json-key">${str}</span>${colon}`;
      if (bool) return `<span class="json-bool">${bool}</span>`;
      if (match === "null") return `<span class="json-null">null</span>`;
      if (/^-?\d/.test(match)) return `<span class="json-num">${match}</span>`;
      return `<span class="json-str">${match}</span>`;
    }
  );

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
  const res = await fetch(path);
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
  const m = pathPart.match(/^\/job\/([^/?]+)/);
  if (m) {
    const tabParam = params.get("tab") || "items";
    const tab = JOB_TABS.has(tabParam) ? tabParam : "items";
    return { name: "job", jobId: decodeURIComponent(m[1]), tab };
  }
  return {
    name: "jobs",
    spider: params.get("spider") || "",
    status: params.get("status") || "",
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
  } catch (_) {}
});

document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  closeModal();
  setConnOpen(false);
});

function renderConnection(info) {
  if (!connTitle || !connBody) return;
  connTitle.textContent = info.title || "Connection";
  const rows = [
    ["Type", info.destination === "database" ? info.kind : "search"],
    ["Endpoint", info.display_url],
    info.schema ? ["Schema", info.schema] : null,
    ["Jobs table", info.jobs_table],
    ["Items table", info.items_table],
  ]
    .filter(Boolean)
    .map(([k, v]) => `<div class="conn-row"><dt>${esc(k)}</dt><dd class="mono">${esc(v)}</dd></div>`)
    .join("");
  connBody.innerHTML = rows || '<p class="conn-empty">No connection info</p>';
}

function setConnOpen(open) {
  if (!connWrap || !connBtn || !connPopover) return;
  connWrap.classList.toggle("open", open);
  connBtn.setAttribute("aria-expanded", open ? "true" : "false");
  if (open) connPopover.removeAttribute("hidden");
  else connPopover.setAttribute("hidden", "");
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
      navigator.clipboard.writeText(btn.dataset.copy || "").catch(() => {});
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

const dashboardCards = (d) =>
  `<div class="dash-grid" role="region" aria-label="Job statistics">${DASHBOARD_CARDS.map(([label, key, variant]) =>
    dashCard(label, d[key], variant)
  ).join("")}</div>`;

async function renderJobs({ keepSpiderFocus = false } = {}) {
  view.classList.add("view--dash");
  let spiderCaret = null;
  if (keepSpiderFocus) {
    const active = view.querySelector("#filter-spider");
    if (active && document.activeElement === active) {
      spiderCaret = { start: active.selectionStart, end: active.selectionEnd };
    }
  } else {
    view.innerHTML = skeletonHtml();
  }
  const { q, dq } = filterParams({ page: String(state.jobsPage), page_size: String(JOBS_PAGE_SIZE) });
  try {
    const [data, dash] = await Promise.all([api(`/api/jobs?${q}`), api(`/api/dashboard?${dq}`)]);
    state.jobsLoadError = null;
    const rows = data.items
      .map(
        (j) =>
          `<tr class="clickable" data-job-id="${esc(j.job_id)}"><td><span class="mono">${esc(j.job_id)}</span></td><td>${esc(j.spider_name)}</td><td>${statusPill(j.status)}</td><td>${fmtTime(j.started_at)}</td><td>${fmtTime(j.finished_at)}</td><td class="num mono">${esc(fmtJobElapsed(j))}</td><td class="num">${fmtNum(j.items_count)}</td><td class="num">${fmtNum(j.requests_count)}</td><td class="num">${fmtNum(j.failed_requests)}</td><td class="num">${fmtNum(j.logs_count)}</td><td class="num">${fmtNum(j.errors_count)}</td></tr>`
      )
      .join("");
    view.innerHTML = `<div class="jobs-board">${breadcrumbHomeOnly()}${dashboardCards(dash)}<div class="panel jobs-panel"><div class="panel-head"><div><h2>Recent jobs</h2></div><div class="toolbar"><div class="field"><label for="filter-spider">Spider</label><input type="search" id="filter-spider" placeholder="Filter by name…" value="${esc(state.jobsFilter.spider)}" autocomplete="off" /></div><div class="field"><label for="filter-status">Status</label><select id="filter-status"><option value="">All</option><option value="running" ${state.jobsFilter.status === "running" ? "selected" : ""}>Running</option><option value="finished" ${state.jobsFilter.status === "finished" ? "selected" : ""}>Finished</option></select></div></div></div><div class="table-wrap"><table class="data"><thead><tr><th>Job ID</th><th>Spider</th><th>Status</th><th>Started</th><th>Finished</th><th>Elapsed</th><th>Items</th><th>Requests</th><th>Failed</th><th>Logs</th><th>Errors</th></tr></thead><tbody>${rows || `<tr class="row-static"><td colspan="11">${emptyState("📭", "No jobs yet", "Run a spider with ingest enabled, then refresh.")}</td></tr>`}</tbody></table></div>${pagerHtml(data.page, data.pages, data.total)}</div></div>`;
    const spiderInput = view.querySelector("#filter-spider");
    let spiderTimer;
    spiderInput.addEventListener("keyup", () => {
      clearTimeout(spiderTimer);
      spiderTimer = setTimeout(() => {
        const v = spiderInput.value.trim();
        if (v === state.jobsFilter.spider) return;
        state.jobsFilter.spider = v;
        state.jobsPage = 1;
        renderJobs({ keepSpiderFocus: true });
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
    view.querySelectorAll("tbody tr[data-job-id]").forEach((tr) => {
      tr.addEventListener("click", () => setHash(`#/job/${encodeURIComponent(tr.dataset.jobId)}?tab=items`));
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

const kvRow = (label, value) => `<tr class="row-static"><th>${esc(label)}</th><td>${value}</td></tr>`;

const jobTabHtml = (name, active, job) => {
  const countKey = TAB_COUNT_KEYS[name];
  const badge =
    countKey != null ? `<span class="tab-badge">${fmtNum(job[countKey])}</span>` : "";
  return `<button type="button" role="tab" class="tab ${active ? "active" : ""}" data-tab="${name}" aria-selected="${active ? "true" : "false"}"><span class="tab-label">${TAB_LABELS[name]}</span>${badge}</button>`;
};

async function renderJob(jobId, tab) {
  view.classList.remove("view--dash");
  view.innerHTML = skeletonHtml();
  try {
    const job = await api(`/api/jobs/${encodeURIComponent(jobId)}`);
    const tabs = JOB_TAB_ORDER.map((t) => jobTabHtml(t, t === tab, job)).join("");
    const metrics = JOB_METRICS.map(([label, key, variant]) =>
      dashCard(label, fmtNum(job[key]), variant)
    ).join("");
    view.innerHTML = `<div class="jobs-board job-board">${breadcrumbForJob(job.spider_name || "Job", job.job_id)}<div class="dash-grid job-metrics">${metrics}</div><div class="panel panel--tabs job-detail-panel"><div class="tab-frame"><div class="tabs-row"><nav class="tabs" role="tablist" aria-label="Job sections">${tabs}</nav><div class="tabs-status">${statusPill(job.status)}</div></div><div id="tab-body" class="tab-body" role="tabpanel"></div></div></div></div>`;
    bindJobIdCopy(view);
    view.querySelectorAll(".tab").forEach((btn) => {
      btn.addEventListener("click", () => setHash(`#/job/${encodeURIComponent(jobId)}?tab=${btn.dataset.tab}`));
    });
    const body = view.querySelector("#tab-body");
    if (tab === "overview") {
      body.innerHTML = `${tabToolbarSpacer()}<div class="table-wrap"><table class="data kv-table"><tbody>${kvRow("Started", fmtTime(job.started_at))}${kvRow("Finished", fmtTime(job.finished_at))}${kvRow("Finish reason", esc(job.finish_reason || "—"))}${kvRow("Elapsed", esc(job.elapsed_seconds != null ? `${job.elapsed_seconds}s` : "—"))}${kvRow("Scrape rate", esc(job.items_per_min != null ? `${job.items_per_min}/min` : "—"))}</tbody></table></div>`;
      clearAutoRefresh();
      return;
    }
    if (tab === "stats") {
      renderStatsTab(body, job);
      clearAutoRefresh();
      return;
    }
    if (tab === "items") await renderItemsTab(body, jobId);
    if (tab === "requests") await renderRequestsTab(body, jobId);
    if (tab === "logs") await renderLogsTab(body, jobId);
    syncAutoRefresh();
  } catch (err) {
    view.innerHTML = `<div class="error-banner">${esc(err.message)}</div>`;
    clearAutoRefresh();
  }
}

function isItemObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}

function formatItemValue(v) {
  if (v === null || v === undefined) return '<span class="item-na">N/A</span>';
  if (typeof v === "boolean") return esc(String(v));
  if (typeof v === "number") return esc(String(v));
  const s = String(v);
  if (/^https?:\/\//i.test(s)) {
    return `<a href="${esc(s)}" target="_blank" rel="noopener">${esc(s)}</a>`;
  }
  return esc(s);
}

function itemNestEntries(entries, depth) {
  return entries.map(([k, v]) => itemFieldBlock(k, v, depth)).join("");
}

function isScalarItem(v) {
  return !isItemObject(v) && !Array.isArray(v);
}

function itemArrayInner(value, depth) {
  if (!value.length) return '<span class="item-na">[]</span>';
  if (value.every(isItemObject)) {
    return itemNestEntries(
      value.flatMap((obj) => Object.entries(obj)),
      depth + 1
    );
  }
  if (value.every(isScalarItem)) {
    return value.map((el) => `<div class="item-scalar">${formatItemValue(el)}</div>`).join("");
  }
  return value
    .map((el) => {
      if (isItemObject(el)) {
        return `<div class="item-nest-group">${itemNestEntries(Object.entries(el), depth + 1)}</div>`;
      }
      if (Array.isArray(el)) {
        return `<div class="item-nest">${itemArrayInner(el, depth + 1)}</div>`;
      }
      return `<div class="item-scalar">${formatItemValue(el)}</div>`;
    })
    .join("");
}

function itemFieldBlock(key, value, depth) {
  if (Array.isArray(value)) {
    if (!value.length) {
      return `<div class="item-field"><div class="item-k">${esc(key)}</div><div class="item-v"><span class="item-na">[]</span></div></div>`;
    }
    const inner = itemArrayInner(value, depth + 1);
    return `<div class="item-field item-field--branch"><div class="item-k">${esc(key)}</div><div class="item-nest" style="--nest:${depth}">${inner}</div></div>`;
  }
  if (isItemObject(value)) {
    if (!Object.keys(value).length) {
      return `<div class="item-field"><div class="item-k">${esc(key)}</div><div class="item-v"><span class="item-na">{{}}</span></div></div>`;
    }
    return `<div class="item-field item-field--branch"><div class="item-k">${esc(key)}</div><div class="item-nest" style="--nest:${depth}">${itemNestEntries(Object.entries(value), depth + 1)}</div></div>`;
  }
  return `<div class="item-field"><div class="item-k">${esc(key)}</div><div class="item-v">${formatItemValue(value)}</div></div>`;
}

function itemValueCell(value, depth = 0) {
  if (Array.isArray(value)) {
    if (!value.length) return '<span class="item-na">[]</span>';
    return `<div class="item-nest item-nest--root" style="--nest:${depth}">${itemArrayInner(value, depth + 1)}</div>`;
  }
  if (isItemObject(value)) {
    if (!Object.keys(value).length) return '<span class="item-na">{}</span>';
    return `<div class="item-nest item-nest--root" style="--nest:${depth}">${itemNestEntries(Object.entries(value), depth + 1)}</div>`;
  }
  return formatItemValue(value);
}

function itemFieldsTable(item) {
  const root = isItemObject(item) ? item : { value: item };
  const keys = Object.keys(root);
  if (!keys.length) {
    return '<p class="item-empty-fields">No fields</p>';
  }
  const rows = Object.entries(root)
    .map(
      ([k, v]) =>
        `<tr class="item-root-row"><th scope="row">${esc(k)}</th><td class="item-root-val">${itemValueCell(v, 0)}</td></tr>`
    )
    .join("");
  return `<table class="item-fields"><tbody>${rows}</tbody></table>`;
}

function itemPanelHtml(row, index, itemIndex) {
  return `<article class="item-panel"><header class="item-panel-head"><div class="item-panel-title"><span class="item-panel-label">Item</span> <span class="item-panel-id">${esc(itemIndex)}</span><time class="item-panel-time">${fmtTime(row.created_at)}</time></div><button type="button" class="btn btn-sm btn-ghost item-json-btn" data-json-idx="${index}">JSON</button></header>${itemFieldsTable(row.item)}</article>`;
}

async function renderItemsTab(container, jobId, { silent = false } = {}) {
  if (!silent) container.innerHTML = '<div class="empty">Loading items…</div>';
  const page = state.jobPage.items;
  const pageSize = 20;
  let data;
  try {
    data = await api(`/api/jobs/${encodeURIComponent(jobId)}/items?page=${page}&page_size=${pageSize}`);
  } catch (err) {
    if (silent) return;
    container.innerHTML = `<div class="error-banner">${esc(err.message)}</div>`;
    return;
  }
  const indexBase = (data.page - 1) * (data.page_size || pageSize);
  const panels = data.items.map((row, i) => itemPanelHtml(row, i, indexBase + i)).join("");
  container.innerHTML = `${tabToolbarSpacer()}${panels ? `<div class="items-list">${panels}</div>` : emptyState("📦", "No items", "This job has not scraped any items yet.")}${pagerHtml(data.page, data.pages, data.total)}`;
  container.querySelectorAll(".item-json-btn[data-json-idx]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      openModal("Item JSON", data.items[Number(btn.dataset.jsonIdx)].item);
    });
  });
  bindPager(container, data.page, data.pages, (p) => {
    state.jobPage.items = p;
    renderJob(jobId, "items");
  });
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

function formatStatValue(v) {
  if (v === null || v === undefined) return '<span class="item-na">N/A</span>';
  if (typeof v === "boolean") return esc(String(v));
  if (typeof v === "number") return esc(Number.isInteger(v) ? v.toLocaleString() : String(v));
  if (typeof v === "object") return `<span class="mono">${esc(JSON.stringify(v))}</span>`;
  return formatItemValue(v);
}

function renderStatsTab(container, job) {
  const stats = job.stats;
  if (!stats || typeof stats !== "object" || !Object.keys(stats).length) {
    container.innerHTML = `${tabToolbarSpacer()}${emptyState(
      "📊",
      "No stats",
      "Scrapy crawl stats appear here when the job finishes or while stats are being collected."
    )}`;
    return;
  }
  const rows = Object.keys(stats)
    .sort((a, b) => a.localeCompare(b))
    .map((k) => requestFieldRow(k, formatStatValue(stats[k])))
    .join("");
  container.innerHTML = `${tabToolbarSpacer()}<div class="table-wrap"><table class="stats-table"><tbody>${rows}</tbody></table></div>`;
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
    rows.push(
      requestFieldRow(
        "Parent Request #",
        `<button type="button" class="link-btn req-parent-link" data-parent-id="${esc(r.parent_id)}">${esc(r.parent_id)}</button>`
      )
    );
  }
  if (r.response_size_bytes) {
    rows.push(requestFieldRow("Response Size", esc(String(r.response_size_bytes))));
  }
  if (r.status_code != null && r.status_code !== "") {
    rows.push(
      requestFieldRow(
        "HTTP Status",
        `<span class="status-code ${statusCodeClass(r.status_code)}">${esc(r.status_code)}</span>`
      )
    );
  }
  if (r.created_at) rows.push(requestFieldRow("Last Seen", fmtTime(r.created_at)));
  if (r.url) rows.push(requestFieldRow("Url", formatItemValue(r.url)));
  return `<table class="item-fields"><tbody>${rows.join("")}</tbody></table>`;
}

function requestPanelHtml(r, reqIndex) {
  return `<article class="item-panel request-panel"><header class="item-panel-head"><div class="item-panel-title"><span class="item-panel-label">Request</span> <span class="item-panel-id">${esc(reqIndex)}</span><time class="item-panel-time">${fmtTime(r.created_at)}</time></div></header>${requestFieldsTable(r)}</article>`;
}

async function renderRequestsTab(container, jobId) {
  container.innerHTML = '<div class="empty">Loading requests…</div>';
  const page = state.jobPage.requests;
  const pageSize = 20;
  const q = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
  if (state.requestFilter === "ok") q.set("success", "true");
  if (state.requestFilter === "fail") q.set("success", "false");
  if (state.requestIdFilter != null) q.set("request_id", String(state.requestIdFilter));
  const data = await api(`/api/jobs/${encodeURIComponent(jobId)}/requests?${q}`);
  const indexBase = (data.page - 1) * (data.page_size || pageSize);
  const panels = data.items.map((r, i) => requestPanelHtml(r, indexBase + i)).join("");
  const idFilterBar =
    state.requestIdFilter != null
      ? `<div class="req-id-filter"><span>Showing request #${esc(state.requestIdFilter)}</span><button type="button" class="btn btn-sm btn-ghost" id="req-clear-id">Show all requests</button></div>`
      : "";
  container.innerHTML = `${tabToolbar(`${idFilterBar}${filterSelect("req-filter", "Filter requests", state.requestFilter, REQ_FILTER_OPTS)}`)}${panels ? `<div class="items-list">${panels}</div>` : emptyState("🌐", "No requests", "Request logging may be disabled for this crawl.")}${pagerHtml(data.page, data.pages, data.total)}`;
  container.querySelector("#req-filter")?.addEventListener("change", (e) => {
    state.requestFilter = e.target.value;
    state.jobPage.requests = 1;
    renderJob(jobId, "requests");
  });
  container.querySelector("#req-clear-id")?.addEventListener("click", () => {
    state.requestIdFilter = null;
    state.jobPage.requests = 1;
    renderJob(jobId, "requests");
  });
  container.querySelectorAll(".req-parent-link[data-parent-id]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.requestIdFilter = Number(btn.dataset.parentId);
      state.jobPage.requests = 1;
      renderJob(jobId, "requests");
    });
  });
  bindPager(container, data.page, data.pages, (p) => {
    state.jobPage.requests = p;
    renderJob(jobId, "requests");
  });
}

const logLineText = (log) => {
  const head = log.logger ? `[${log.logger}] ${log.message ?? ""}` : (log.message ?? "");
  return (log.exception ? `${head}\n${log.exception}` : head).trim();
};

const formatLogText = (text) =>
  esc(text).replace(
    /(https?:\/\/[^\s<]+)/g,
    '<a class="log-url" href="$1" target="_blank" rel="noopener">$1</a>'
  );

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
    preview: over ? `${head.slice(0, LOG_PREVIEW).trimEnd()}…` : head,
    extra,
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
  return `<tr class="log-row log-row--${rowLv}"><td class="log-idx"><span class="log-idx-num">${idx}:</span></td><td class="log-time">${fmtTime(log.time)}</td><td><span class="log-level level-${esc(lv)}">${esc(lv)}</span></td><td class="log-msg-cell">${logMsgHtml(logLineText(log))}</td></tr>`;
};

async function renderLogsTab(container, jobId) {
  container.innerHTML = '<div class="empty">Loading logs…</div>';
  const page = state.jobPage.logs;
  const pageSize = 100;
  const q = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
  if (state.logLevel) q.set("level", state.logLevel);
  const data = await api(`/api/jobs/${encodeURIComponent(jobId)}/logs?${q}`);
  const base = (data.page - 1) * (data.page_size || pageSize);
  const rows = data.items.map((log, i) => logRowHtml(log, base + i)).join("");
  container.innerHTML = `${tabToolbar(filterSelect("log-level", "Filter log level", state.logLevel, LOG_LEVEL_OPTS))}<div class="table-wrap"><table class="logs-table"><thead><tr><th class="log-idx"><span class="sr-only">Line</span></th><th>Time (UTC)</th><th>Level</th><th>Message</th></tr></thead><tbody>${rows || `<tr><td colspan="4">${emptyState("📋", "No logs", "No log lines were stored for this job.")}</td></tr>`}</tbody></table></div>${pagerHtml(data.page, data.pages, data.total)}`;
  container.querySelector("#log-level").addEventListener("change", (e) => {
    state.logLevel = e.target.value;
    state.jobPage.logs = 1;
    renderJob(jobId, "logs");
  });
  bindPager(container, data.page, data.pages, (p) => {
    state.jobPage.logs = p;
    renderJob(jobId, "logs");
  });
}

async function render() {
  const route = parseRoute();
  await loadHealth();
  if (route.name === "job") {
    await renderJob(route.jobId, route.tab);
    return;
  }
  state.jobsFilter.spider = route.spider;
  state.jobsFilter.status = route.status;
  state.jobsPage = 1;
  await renderJobs();
}

document.addEventListener("visibilitychange", () => {
  if (document.hidden || state.jobsLoadError) return;
  autoRefreshTick();
  syncAutoRefresh();
});

window.addEventListener("hashchange", render);
render();
