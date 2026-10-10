/**
 * Reduce a deployment's dashboard metrics payload to the few numbers a capacity
 * cell needs beside it: how many pods served it and how hot they ran.
 */

const GROUP_LABELS = [
  ["worker", "queue"],
  ["api", "api"],
  ["postgres", "db"],
  ["redis", "redis"],
];

function groupLabel(title) {
  const lower = String(title ?? "").toLowerCase();
  const hit = GROUP_LABELS.find(([needle]) => lower.includes(needle));
  return hit ? hit[1] : lower || "other";
}

function isNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

function round(value, digits = 0) {
  const factor = 10 ** digits;
  return String(Math.round(value * factor) / factor);
}

export function cellWindow(steps) {
  const started = (steps ?? []).map((s) => s?.startedAt).filter(Boolean).sort();
  const ended = (steps ?? []).map((s) => s?.endedAt).filter(Boolean).sort();
  if (started.length === 0 || ended.length === 0) return null;
  return { startTime: started[0], endTime: ended[ended.length - 1] };
}

/** Series keep the dashboard's own names so the report and the UI say the same thing. */
export function summarizeServerMetrics(section) {
  const groups = {};
  for (const sub of section?.sub_sections ?? []) {
    const group = (groups[groupLabel(sub?.title)] ??= {});
    for (const chart of sub?.charts ?? []) {
      const names = Object.fromEntries(
        (chart?.series ?? []).map((s) => [String(s.id), s.name ?? String(s.id)]),
      );
      const bySeries = {};
      for (const point of chart?.data ?? []) {
        if (!isNumber(point?.value)) continue;
        (bySeries[names[point.series_id] ?? String(point.series_id)] ??= []).push(point.value);
      }
      for (const [name, values] of Object.entries(bySeries)) {
        group[name] = {
          min: Math.min(...values),
          max: Math.max(...values),
          samples: values.length,
        };
      }
    }
  }
  return { groups };
}

function pick(group, ...needles) {
  const hit = Object.keys(group).find((name) =>
    needles.every((needle) => name.toLowerCase().includes(needle)),
  );
  return hit ? group[hit] : null;
}

export function podRange(group) {
  const replicas = pick(group ?? {}, "replica");
  return replicas ? { min: Math.round(replicas.min), max: Math.round(replicas.max) } : null;
}

export function peakCpu(group) {
  const cpu = pick(group ?? {}, "cpu", "max") ?? pick(group ?? {}, "cpu");
  return cpu ? cpu.max : null;
}

export function formatServerMetrics(summary) {
  const parts = [];
  for (const label of ["queue", "api", "db", "redis"]) {
    const group = summary?.groups?.[label];
    if (!group) continue;
    const replicas = pick(group, "replica");
    if (replicas) parts.push(`${label} pods ${round(replicas.min)}→${round(replicas.max)}`);
    const cpu = pick(group, "cpu", "max") ?? pick(group, "cpu");
    if (cpu) parts.push(`${label} cpu max ${round(cpu.max, 2)}`);
    if (label === "queue") {
      const active = pick(group, "active");
      if (active) parts.push(`workers active max ${round(active.max)}`);
      const pending = pick(group, "pending");
      if (pending) parts.push(`runs pending max ${round(pending.max)}`);
    }
  }
  return parts.join(" · ");
}
