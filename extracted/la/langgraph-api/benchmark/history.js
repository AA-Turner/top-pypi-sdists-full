/**
 * Previous nights' results, for a "vs last N nights" line in the reports.
 *
 * Usage (CI):
 *   node history.js fetch --workflow "<workflow name>" --prefix <artifact prefix> \
 *     --out <dir> --exclude <current run id> [--limit 7]
 */

import { spawnSync } from "node:child_process";
import { mkdirSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function fetchHistory({ workflow, prefix, outDir, excludeRunId, limit = 7 }) {
  mkdirSync(outDir, { recursive: true });
  const list = spawnSync(
    "gh",
    [
      "run", "list",
      "--workflow", workflow,
      "--event", "schedule",
      "--status", "completed",
      "--limit", String(limit + 1),
      "--json", "databaseId,createdAt",
    ],
    { encoding: "utf8" },
  );
  if (list.status !== 0) {
    throw new Error(`gh run list failed: ${(list.stderr || "").trim()}`);
  }
  const runs = JSON.parse(list.stdout)
    .filter((run) => String(run.databaseId) !== String(excludeRunId))
    .slice(0, limit);
  const fetched = [];
  for (const run of runs) {
    const dir = path.join(outDir, String(run.databaseId));
    const download = spawnSync(
      "gh",
      ["run", "download", String(run.databaseId), "-p", `${prefix}*`, "-D", dir],
      { encoding: "utf8" },
    );
    if (download.status === 0) {
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

function argValue(argv, flag) {
  const index = argv.indexOf(flag);
  return index >= 0 ? argv[index + 1] : undefined;
}

function main(argv) {
  if (argv[0] !== "fetch") {
    console.error("usage: node history.js fetch --workflow <name> --prefix <artifact prefix> --out <dir> --exclude <run id> [--limit 7]");
    process.exit(2);
  }
  const fetched = fetchHistory({
    workflow: argValue(argv, "--workflow"),
    prefix: argValue(argv, "--prefix"),
    outDir: argValue(argv, "--out") ?? "history",
    excludeRunId: argValue(argv, "--exclude"),
    limit: Number(argValue(argv, "--limit") ?? 7),
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
