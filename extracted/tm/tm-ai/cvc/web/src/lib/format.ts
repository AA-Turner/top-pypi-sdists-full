/**
 * Shared formatting + display helpers used by every Data-section page.
 * Pure functions only — no JSX (use ../components/Stat for cards).
 */

export function shortHash(h: string | undefined | null, len = 12): string {
  if (!h) return "—";
  return String(h).slice(0, len);
}

export function fullHash(h: string | undefined | null): string {
  if (!h) return "—";
  return String(h);
}

export function toMs(ts: number | string | undefined | null): number {
  if (ts === undefined || ts === null || ts === "") return 0;
  if (typeof ts === "number") return ts < 1e12 ? ts * 1000 : ts;
  const n = Date.parse(ts);
  return Number.isFinite(n) ? n : 0;
}

export function fmtTs(ts: number | string | undefined | null): string {
  const t = toMs(ts);
  if (!t) return "—";
  const d = new Date(t);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleString(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

export function fmtDate(ts: number | string | undefined | null): string {
  const t = toMs(ts);
  if (!t) return "—";
  const d = new Date(t);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleDateString();
}

export function fmtTime(ts: number | string | undefined | null): string {
  const t = toMs(ts);
  if (!t) return "—";
  const d = new Date(t);
  if (isNaN(d.getTime())) return "—";
  return d.toLocaleTimeString();
}

export function ago(ts: number | string | undefined | null): string {
  const t = toMs(ts);
  if (!t) return "—";
  const d = Date.now() - t;
  if (d < 0) return "just now";
  const sec = Math.floor(d / 1000);
  if (sec < 60) return `${sec}s ago`;
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min}m ago`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr}h ago`;
  const day = Math.floor(hr / 24);
  if (day < 30) return `${day}d ago`;
  const mon = Math.floor(day / 30);
  if (mon < 12) return `${mon}mo ago`;
  return `${Math.floor(mon / 12)}y ago`;
}

export function fmtBytes(n: number | undefined | null): string {
  if (n === undefined || n === null || !Number.isFinite(n)) return "—";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let v = n;
  let i = 0;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(v < 10 ? 2 : v < 100 ? 1 : 0)} ${units[i]}`;
}

export function fmtNum(n: number | undefined | null): string {
  if (n === undefined || n === null || !Number.isFinite(n)) return "—";
  return n.toLocaleString();
}

/**
 * Pretty-print a JSON snippet for inline preview, capped at N chars.
 */
export function jsonPreview(obj: unknown, max = 280): string {
  if (obj === undefined || obj === null) return "—";
  let s: string;
  try {
    s = JSON.stringify(obj, null, 2);
  } catch {
    s = String(obj);
  }
  if (s.length <= max) return s;
  return s.slice(0, max) + `… (+${s.length - max} more)`;
}

/**
 * Truncate text on word boundary with ellipsis.
 */
export function truncate(s: string | undefined | null, max = 200): string {
  if (!s) return "";
  if (s.length <= max) return s;
  return s.slice(0, max).replace(/\s+\S*$/, "") + "…";
}

export function bucketOf(
  ts: number | string | undefined | null,
): "Today" | "Yesterday" | "This Week" | "This Month" | "Older" {
  const t = toMs(ts);
  if (!t) return "Older";
  const now = new Date();
  const startToday = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
  ).getTime();
  if (t >= startToday) return "Today";
  if (t >= startToday - 86400_000) return "Yesterday";
  if (t >= startToday - 7 * 86400_000) return "This Week";
  if (t >= startToday - 30 * 86400_000) return "This Month";
  return "Older";
}

/**
 * Classname constants reused across pages for visual consistency.
 */
export const cardCls =
  "rounded-xl border border-white/10 bg-white/5 p-5 text-white";
export const cardCompact =
  "rounded-lg border border-white/10 bg-white/5 p-3 text-white";
export const subCls =
  "text-xs font-semibold uppercase tracking-[0.2em] text-white/55";
export const monoCls = "font-mono text-[0.7rem] text-white/75";
export const microCls =
  "text-[0.65rem] uppercase tracking-[0.18em] text-white/45 font-mono-ui";

/**
 * Pretty commit-icon picker — colored dot by type.
 */
export function commitIcon(type: string | undefined): string {
  if (!type) return "●";
  const t = type.toLowerCase();
  if (t.includes("anchor") || t.includes("genesis")) return "★";
  if (t.includes("merge")) return "⇄";
  if (t.includes("branch")) return "⑂";
  if (t.includes("checkpoint")) return "◆";
  if (t.includes("analysis")) return "◇";
  if (t.includes("generation")) return "✦";
  return "●";
}

export function copyToClipboard(text: string): void {
  if (typeof navigator !== "undefined" && navigator.clipboard) {
    void navigator.clipboard.writeText(text).catch(() => {
      /* no-op */
    });
  }
}
