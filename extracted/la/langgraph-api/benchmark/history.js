/**
 * Previous nights' results, for a "vs last N nights" line in the reports.
 *
 * Usage (CI):
 *   node history.js fetch --workflow "<workflow name>" --prefix <artifact prefix> \
 *     --out <dir> --exclude <current run id> [--limit 7] [--require <file prefix>]
 */

import { spawnSync } from "node:child_process";
import { mkdirSync, readdirSync, readFileSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MAX_HISTORY_AGE_DAYS = 30;
// Covers MAX_HISTORY_AGE_DAYS of nightly runs plus the manual dispatches between them.
const RUNS_TO_LIST = 200;

/**
 * Newest first. The filtering happens here because `gh run list --event
 * schedule --status completed` has returned months-old runs in place of last
 * week's, and a run that is kept but has no artifact would still use up a night.
 */
export function historyCandidates(runs, { excludeRunId, now = new Date() }) {
  const oldest = now.getTime() - MAX_HISTORY_AGE_DAYS * 24 * 60 * 60 * 1000;
  return runs
    .filter((run) => run.event === "schedule" && run.status === "completed")
    .filter((run) => String(run.databaseId) !== String(excludeRunId))
    .filter((run) => Date.parse(run.createdAt) >= oldest)
    .sort((a, b) => Date.parse(b.createdAt) - Date.parse(a.createdAt));
}

export function fetchHistory({ workflow, prefix, outDir, excludeRunId, limit = 7, requireFile }) {
  mkdirSync(outDir, { recursive: true });
  const list = spawnSync(
    "gh",
    [
      "run", "list",
      "--workflow", workflow,
      "--limit", String(RUNS_TO_LIST),
      "--json", "databaseId,createdAt,event,status",
    ],
    { encoding: "utf8" },
  );
  if (list.status !== 0) {
    throw new Error(`gh run list failed: ${(list.stderr || "").trim()}`);
  }
  const runs = historyCandidates(JSON.parse(list.stdout), { excludeRunId });
  const fetched = [];
  for (const run of runs) {
    if (fetched.length >= limit) break;
    const dir = path.join(outDir, String(run.databaseId));
    const download = spawnSync(
      "gh",
      ["run", "download", String(run.databaseId), "-p", `${prefix}*`, "-D", dir],
      { encoding: "utf8" },
    );
    if (download.status === 0 && requireFile && !hasFile(dir, requireFile)) {
      // A night that failed before producing results still uploads its context.
      rmSync(dir, { recursive: true, force: true });
      console.warn(`run ${run.databaseId}: no ${requireFile}* file, not a night to compare with`);
    } else if (download.status === 0) {
      fetched.push({ runId: run.databaseId, createdAt: run.createdAt, dir });
    } else {
      console.warn(`run ${run.databaseId}: no ${prefix}* artifact (${(download.stderr || "").trim()})`);
    }
  }
  return fetched;
}

function isNumber(value) {
  return typeof value === "number" && Number.isFinite(value);
}

export function hasFile(dir, prefix) {
  return walk(dir).some((file) => path.basename(file).startsWith(prefix));
}

function walk(dir) {
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return [];
  }
  return entries.flatMap((entry) => {
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

/** Newest run first. fetchHistory names each directory by run id, which grows with time. */
function runDirs(dir) {
  try {
    return readdirSync(dir, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort((a, b) => Number(b) - Number(a) || b.localeCompare(a))
      .map((name) => path.join(dir, name));
  } catch {
    return [];
  }
}

function readJson(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

// `within` tells one runner's artifacts apart when a run directory holds several.
export function loadDailyHistory(dir, within = "") {
  const history = [];
  for (const run of runDirs(dir)) {
    const newest = walk(run)
      .filter((file) => /^summary_.*\.json$/.test(path.basename(file)))
      .filter((file) => !within || path.dirname(file).includes(within))
      .sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0];
    const summary = newest ? readJson(newest) : null;
    if (summary?.metrics) history.push(summary.metrics);
  }
  return history;
}

export function cellKey(config) {
  return `${config.deploymentSlug}|${config.computeTier}|${config.benchmarkType}`;
}

export function loadCapacityHistory(dir) {
  const history = {};
  for (const run of runDirs(dir)) {
    for (const file of walk(run)) {
      if (!/^staircase_summary_.*\.json$/.test(path.basename(file))) continue;
      const summary = readJson(file);
      const config = summary?.config;
      if (!config?.deploymentSlug || !config?.computeTier || !config?.benchmarkType) continue;
      if (summary.error) continue;
      (history[cellKey(config)] ??= []).push({
        executor: config.k6Executor ?? "constant-vus",
        serverCpus: summary.serverCpus ?? null,
        capacityVUs: summary.capacity?.targetVUs ?? 0,
        runsPerSec:
          summary.capacity?.successfulRunsPerSec ??
          summary.throughputCeiling?.successfulRunsPerSec ??
          null,
      });
    }
  }
  return history;
}

// The CPUs staging's E2 machines come with, keyed `vendor family/model` as cpu-probe.js records them.
const CPU_NAMES = {
  "GenuineIntel 6/63": "intel haswell",
  "GenuineIntel 6/79": "intel broadwell",
  "GenuineIntel 6/85": "intel skylake or cascade lake",
  "AuthenticAMD 23/49": "amd rome",
  "AuthenticAMD 25/1": "amd milan",
};

/** gVisor prints an AMD family as `(extended << 4) | 0xF`, 143 where Linux says 23. */
function cpuName(key) {
  const match = /^(\S+) (\d+)\/(\d+)$/.exec(key);
  if (!match) return key;
  const [, vendor, familyText, model] = match;
  const raw = Number(familyText);
  const family = raw > 0xf && (raw & 0xf) === 0xf ? 0xf + (raw >> 4) : raw;
  const normalized = `${vendor} ${family}/${model}`;
  return CPU_NAMES[normalized] ?? normalized;
}

/** `[name, workers]` per kind of CPU, most workers first. */
function cpuCounts(serverCpus) {
  const counts = {};
  for (const [key, workers] of Object.entries(serverCpus ?? {})) {
    const name = cpuName(key);
    counts[name] = (counts[name] ?? 0) + (isNumber(workers) ? workers : 0);
  }
  return Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

/**
 * The key the reports compare nights by, null when unknown: "amd rome" when
 * every worker ran on it, "mostly amd rome" when at least three in four did,
 * every CPU seen otherwise. The share of slow workers moves a night's p95 and
 * capacity, so one slow worker in ten and nine in ten are different machines;
 * the wide middle keeps near-even mixes, the usual case on staging, on one baseline.
 */
export function cpuSignature(serverCpus) {
  const entries = cpuCounts(serverCpus);
  if (entries.length < 2) return entries[0]?.[0] ?? null;
  const workers = entries.reduce((sum, [, n]) => sum + n, 0);
  const [top, most] = entries[0];
  return most * 4 >= workers * 3 ? `mostly ${top}` : entries.map(([name]) => name).sort().join(" + ");
}

/** "amd rome" for one worker, "6 amd rome, 4 intel broadwell" for several. */
export function describeCpus(serverCpus) {
  const entries = cpuCounts(serverCpus);
  if (entries.length === 0) return null;
  const workers = entries.reduce((sum, [, n]) => sum + n, 0);
  return workers === 1 ? entries[0][0] : entries.map(([name, n]) => `${n} ${name}`).join(", ");
}

/**
 * The nights with tonight's CPU label. A night without the probe only
 * matches a night without it, so reports keep their history until the probe
 * starts answering.
 */
export function sameCpu(nights, serverCpus) {
  const tonight = cpuSignature(serverCpus);
  return nights.filter((night) => cpuSignature(night?.serverCpus) === tonight);
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

// Fewer nights flag most cells against a "usual" range of zero.
export const MIN_HISTORY_NIGHTS = 5;

/**
 * Tonight against the past. The band is the past's own half-range, floored at
 * 10%: a series that swings 40% night to night must not be flagged for
 * moving 15%.
 */
export function compare(current, past) {
  const values = (past ?? []).filter(isNumber);
  if (!isNumber(current) || values.length < 2) return null;
  const med = median(values);
  if (med === 0) return null;
  const spreadPct = ((Math.max(...values) - Math.min(...values)) / 2 / med) * 100;
  const deltaPct = ((current - med) / med) * 100;
  return {
    median: med,
    spreadPct,
    deltaPct,
    nights: values.length,
    outside: Math.abs(deltaPct) > Math.max(10, spreadPct),
  };
}

export function formatDelta(pct) {
  return `${pct >= 0 ? "+" : "-"}${Math.abs(pct).toFixed(1)}%`;
}

export function flaggedChange(current, past, { higherIsBetter }) {
  const verdict = compare(current, past);
  if (!verdict || verdict.nights < MIN_HISTORY_NIGHTS || !verdict.outside) return null;
  const better = higherIsBetter ? verdict.deltaPct > 0 : verdict.deltaPct < 0;
  return { ...verdict, better, arrow: better ? "▲" : "▼" };
}

export function formatMove(before, after, deltaPct, unit = "") {
  const suffix = unit ? ` ${unit}` : "";
  return `${before} → ${after}${suffix} (${deltaPct >= 0 ? "+" : "-"}${Math.abs(Math.round(deltaPct))}%)`;
}

const BARS = "▁▂▃▄▅▆▇█";

/**
 * Oldest first. A missing night is a gap, so a hole in the data is not drawn as
 * a low. The height spans at least half the series' peak, so night-to-night
 * noise stays mid-height instead of filling the whole range.
 */
export function sparkline(values) {
  const known = values.filter(isNumber);
  if (known.length === 0) return "";
  const high = Math.max(...known);
  const low = Math.min(...known);
  const span = Math.max(high - low, Math.abs(high) * 0.5);
  const floor = (high + low) / 2 - span / 2;
  return values
    .map((v) => (!isNumber(v) ? " " : high === low ? BARS[3] : BARS[Math.round(((v - floor) / span) * (BARS.length - 1))]))
    .join("");
}

function argValue(argv, flag) {
  const index = argv.indexOf(flag);
  return index >= 0 ? argv[index + 1] : undefined;
}

function main(argv) {
  if (argv[0] !== "fetch") {
    console.error("usage: node history.js fetch --workflow <name> --prefix <artifact prefix> --out <dir> --exclude <run id> [--limit 7] [--require <file prefix>]");
    process.exit(2);
  }
  const fetched = fetchHistory({
    workflow: argValue(argv, "--workflow"),
    prefix: argValue(argv, "--prefix"),
    outDir: argValue(argv, "--out") ?? "history",
    excludeRunId: argValue(argv, "--exclude"),
    limit: Number(argValue(argv, "--limit") ?? 7),
    requireFile: argValue(argv, "--require"),
  });
  console.log(`fetched ${fetched.length} previous run(s)`);
}

const isMain =
  process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  try {
    main(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
