/*
 * The nightly delta-channel report. Reads the k6 raw sample file because the
 * per-cell, per-depth numbers live only in sample tags; the summary has
 * aggregates for the whole run.
 */

import { createReadStream, existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

import { ERROR_ATTENTION, MIN_SUCCESS_RATE, describeThreshold, errorParts, findLatestSummary, isHealthy, readApiVersion, readSummary } from './daily-report.js';
import { MIN_HISTORY_NIGHTS, flaggedChange, formatMove, sparkline } from './history.js';
import { dotFor, footer, postReport } from './slack.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/** `cell` is the DELTA_CELLS name the runner tags samples with. */
export const CELLS = [
  { cell: 'control', label: 'base' },
  { cell: 'delta_50', label: 'delta' },
];

/** Nights measured another way (one cell per job, a bytes channel, a median write) do not compare with these. */
export const DESIGN = 'paired-messages-mean';

/** Tonight plus the nine nights before it, as in the daily report. */
const NIGHTS = 10;

/** The thread's growth tables, one row per this many turns. Matches STORAGE_EVERY in the workflow. */
export const ROW_EVERY = 350;

/** Metric key, label, printer, unit. All are lower-is-better. */
const METRICS = [
  ['turnMeanMs', 'turn', formatSeconds, 's'],
  ['saveMeanMs', 'write', formatSeconds, 's'],
  ['readP50Ms', 'read', formatSeconds, 's'],
  ['bytes', 'data', formatMb, 'MB'],
];

/** From 10 s on, one decimal: five characters would fill the column and touch the one before it. */
function formatSeconds(v) {
  return isNumber(v) ? (v / 1000).toFixed(v >= 10_000 ? 1 : 2) : '-';
}

function formatMb(v) {
  if (!isNumber(v)) return '-';
  const mb = v / 1024 / 1024;
  return mb >= 100 ? String(Math.round(mb)) : mb.toFixed(1);
}

function isNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function count(value) {
  return isNumber(value) ? Math.round(value).toLocaleString('en-US') : 'n/a';
}

function percentile(sorted, p) {
  if (sorted.length === 0) return null;
  return sorted[Math.min(sorted.length - 1, Math.max(0, Math.ceil(sorted.length * p) - 1))];
}

function mean(values) {
  return values.length > 0 ? values.reduce((sum, v) => sum + v, 0) / values.length : null;
}

export function bucketStart(bucket) {
  const n = parseInt(String(bucket).split('-')[0], 10);
  return Number.isFinite(n) ? n : Number.MAX_SAFE_INTEGER;
}

const byDepth = (a, b) => bucketStart(a) - bucketStart(b);

/** Rows are labelled by the turn they end on. */
function depthLabel(bucket) {
  return String(bucket).split('-')[1] ?? String(bucket);
}

function bucketEnd(bucket) {
  const n = parseInt(depthLabel(bucket), 10);
  return Number.isFinite(n) ? n : 0;
}

/** Bytes keep the largest reading in the bucket: the thread only grows. */
export function aggregateSamples(points) {
  const turns = {};
  const reads = {};
  const saves = {};
  const bytes = {};
  for (const point of points) {
    const depth = point.tags?.depth;
    if (depth == null || !isNumber(point.value)) continue;
    if (point.metric === 'turn_duration') (turns[depth] ??= []).push(point.value);
    else if (point.metric === 'state_read_duration') (reads[depth] ??= []).push(point.value);
    else if (point.metric === 'checkpoint_save') (saves[depth] ??= []).push(point.value);
    else if (point.metric === 'thread_storage_bytes') bytes[depth] = Math.max(bytes[depth] ?? 0, point.value);
  }
  const buckets = {};
  for (const depth of new Set([...Object.keys(turns), ...Object.keys(reads), ...Object.keys(saves), ...Object.keys(bytes)])) {
    buckets[depth] = {
      turns: (turns[depth] ?? []).length,
      // Averages, so a delta thread's snapshot turn counts: one write in 50
      // saves the whole value, and a median never sees it.
      turnMeanMs: mean(turns[depth] ?? []),
      saveMeanMs: mean(saves[depth] ?? []),
      // One cold read per thread per bucket is few samples, so the median only.
      readP50Ms: percentile((reads[depth] ?? []).sort((a, b) => a - b), 0.5),
      bytes: bytes[depth] ?? null,
    };
  }
  return buckets;
}

/** One run carries every cell; the runner's `cell` tag splits them. */
export function aggregateByCell(points) {
  const byCell = {};
  for (const point of points) {
    const cell = point.tags?.cell;
    if (cell) (byCell[cell] ??= []).push(point);
  }
  return Object.fromEntries(Object.entries(byCell).map(([cell, cellPoints]) => [cell, aggregateSamples(cellPoints)]));
}

async function readSamples(file) {
  const points = [];
  const lines = readline.createInterface({ input: createReadStream(file), crlfDelay: Infinity });
  for await (const line of lines) {
    if (!line.includes('"Point"')) continue;
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      continue;
    }
    if (!['turn_duration', 'state_read_duration', 'checkpoint_save', 'thread_storage_bytes'].includes(entry.metric)) continue;
    points.push({ metric: entry.metric, value: entry.data?.value, tags: entry.data?.tags });
  }
  return points;
}

function newestRawData(dir) {
  try {
    return (
      readdirSync(dir, { recursive: true })
        .filter((name) => path.basename(name).startsWith('raw_data_') && name.endsWith('.json'))
        .map((name) => path.join(dir, name))
        .sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0] ?? null
    );
  } catch {
    return null;
  }
}

/** The run's one artifact, flat in `resultsDir` or in its own `delta-results-*` directory. Neither means it never ran. */
export async function collectRun(resultsDir) {
  const name = existsSync(resultsDir)
    ? readdirSync(resultsDir, { withFileTypes: true }).find((e) => e.isDirectory() && e.name.startsWith('delta-results-'))?.name
    : null;
  // download-artifact extracts a single matched artifact straight into the path,
  // and gives each its own directory only when several match.
  const flat = existsSync(path.join(resultsDir, 'report_context.json')) || newestRawData(resultsDir) !== null;
  const dir = name ? path.join(resultsDir, name) : flat ? resultsDir : null;
  const context = dir ? readSummary(path.join(dir, 'report_context.json')) ?? {} : {};
  const raw = dir ? newestRawData(dir) : null;
  const byCell = raw ? aggregateByCell(await readSamples(raw)) : {};
  return {
    stepOutcome: context.stepOutcome ?? (dir ? 'unknown' : 'missing'),
    load: { loadSize: context.loadSize, turns: context.turns },
    summary: dir ? readSummary(findLatestSummary(dir)) : null,
    cells: CELLS.map((spec) => ({ ...spec, buckets: byCell[spec.cell] ?? {} })),
  };
}

/** Newest night first. */
export function loadDeltaHistory(dir) {
  let runs;
  try {
    runs = readdirSync(dir, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .map((e) => e.name)
      .sort((a, b) => Number(b) - Number(a));
  } catch {
    return [];
  }
  const nights = [];
  for (const run of runs) {
    let files;
    try {
      files = readdirSync(path.join(dir, run), { recursive: true });
    } catch {
      continue;
    }
    const file = files.find((name) => path.basename(name) === 'delta_report.json');
    const report = file ? readSummary(path.join(dir, run, file)) : null;
    if (report?.design === DESIGN && report.cells) nights.push(report.cells);
  }
  return nights;
}

function hasRead(bucket) {
  return isNumber(bucket?.readP50Ms);
}

/**
 * The deepest bucket every user finished on both cells. A cold read does not
 * prove that: each user reads at its own offset, so a run that stopped at turn
 * 1380 already has reads in 1351-1400. Without a user count, the deepest bucket
 * both cells have a cold read for.
 */
function deepestComplete(cells, users) {
  const done = users
    ? (d) => cells.every((c) => (c.buckets[d]?.turns ?? 0) >= users * (bucketEnd(d) - bucketStart(d) + 1))
    : (d) => cells.every((c) => hasRead(c.buckets[d]));
  return Object.keys(cells[0]?.buckets ?? {}).filter(done).sort(byDepth).at(-1) ?? null;
}

function anyBytes(cell) {
  return Object.values(cell.buckets).some((b) => isNumber(b.bytes));
}

function failureReason(run) {
  const metrics = run.summary?.metrics;
  if (!metrics) return `no results produced, step finished as \`${run.stepOutcome}\``;
  const crossed = [];
  for (const [metric, expressions] of Object.entries(run.summary.thresholds ?? {})) {
    for (const [expression, verdict] of Object.entries(expressions ?? {})) {
      if (verdict?.ok === false) crossed.push(describeThreshold(metric, expression, metrics).breach);
    }
  }
  if (crossed.length > 0) return crossed.join(', ');
  if (!metrics.successfulRuns) return 'no turn succeeded';
  if (isNumber(metrics.successRate) && metrics.successRate <= MIN_SUCCESS_RATE) {
    return `success ${metrics.successRate.toFixed(2)}% (floor ${MIN_SUCCESS_RATE}%)`;
  }
  return `step finished as \`${run.stepOutcome}\``;
}

/** Per metric, tonight at `depth` against the past nights there, flagged from five nights on. */
export function cellChanges(cell, depth, history) {
  const tonight = cell.buckets?.[depth];
  const changes = [];
  for (const [key, label, format, unit] of METRICS) {
    const past = history.map((night) => night[cell.cell]?.buckets?.[depth]?.[key]).filter(isNumber);
    const flagged = flaggedChange(tonight?.[key], past, { higherIsBetter: false });
    if (!flagged) continue;
    changes.push({ key, better: flagged.better, text: `${cell.label} ${label} ${formatMove(format(flagged.median), format(tonight[key]), flagged.deltaPct, unit)}` });
  }
  return changes;
}

/** How many times better `cell` is than `base`, where lower is better. */
export function gain(base, cell) {
  if (!isNumber(base) || !isNumber(cell) || base <= 0 || cell <= 0) return '-';
  const ratio = base / cell;
  // About the night-to-night noise on these numbers; closer reads as a tie.
  if (ratio > 0.85 && ratio < 1.15) return 'same';
  return ratio >= 10 ? `${Math.round(ratio)}x` : `${ratio.toFixed(1)}x`;
}

/** Tonight's values for both cells at `depth`, and the delta cell's last NIGHTS nights. */
function mainTable(cells, depth, history) {
  const [base, delta] = cells;
  const lines = ['```', `${''.padEnd(6)}${'base'.padStart(5)} delta last ${NIGHTS}`];
  for (const [key, label, format] of METRICS) {
    if (key === 'bytes' && !anyBytes(base)) continue;
    const past = history.slice(0, NIGHTS - 1).reverse().map((night) => night[delta.cell]?.buckets?.[depth]?.[key]);
    const trend = sparkline([...past, delta.buckets[depth]?.[key]]);
    lines.push(`${label.padEnd(6)}${format(base.buckets[depth]?.[key]).padStart(5)}${format(delta.buckets[depth]?.[key]).padStart(5)} ${trend}`);
  }
  lines.push('```');
  return lines;
}

/** Why delta wins or loses: each metric as the threads deepen, with the gain at every row. */
export function growthTables(cells) {
  const [base, delta] = cells;
  const depths = Object.keys(base.buckets)
    .filter((d) => bucketEnd(d) % ROW_EVERY === 0 && delta.buckets[d])
    .sort(byDepth);
  return METRICS.filter(([key]) => depths.some((d) => isNumber(base.buckets[d][key]))).map(([key, label, format, unit]) => {
    const lines = ['```', `${label} ${unit}`, `${'turn'.padEnd(5)}${'base'.padStart(6)}${'delta'.padStart(6)}${'gain'.padStart(6)}`];
    for (const d of depths) {
      const [b, x] = [base.buckets[d][key], delta.buckets[d][key]];
      lines.push(`${depthLabel(d).padEnd(5)}${format(b).padStart(6)}${format(x).padStart(6)}${gain(b, x).padStart(6)}`);
    }
    lines.push('```');
    return lines.join('\n');
  });
}

/**
 * @param {{stepOutcome: string, load: object, summary: object|null, cells: object[]}} run from collectRun
 * @param {{apiVersion?: string|null, artifactUrl?: string|null, now?: Date, manual?: boolean, history?: object[]}} context
 * @returns {{text: string, thread: string[]}}
 */
export function buildReport(run, context = {}) {
  const { apiVersion = null, artifactUrl = null, now = new Date(), manual = false, history = [] } = context;
  const metrics = run.summary?.metrics;
  const failed = !isHealthy({ stepOutcome: run.stepOutcome, metrics });
  const guard = isNumber(metrics?.errors?.missingMessage) ? metrics.errors.missingMessage : 0;
  const httpParts = errorParts(metrics);
  const httpCount = Object.values(metrics?.errors?.byStatus ?? {}).filter(isNumber).reduce((sum, n) => sum + n, 0);
  const depth = deepestComplete(run.cells, Number(run.load?.loadSize) || null);
  const target = Number(run.load?.turns) || null;
  const stoppedAt = target && (!depth || bucketEnd(depth) < target) ? (depth ? bucketEnd(depth) : 0) : null;
  const changes = depth ? run.cells.flatMap((cell) => cellChanges(cell, depth, history)) : [];
  const regressed = changes.filter((c) => !c.better);
  const improved = changes.filter((c) => c.better);

  // Same bar as the daily digest: a stray 503 is noted, not escalated. A guard
  // failure is a correctness bug, so one is enough.
  const clauses = [];
  if (failed) clauses.push('failed');
  if (guard > 0) clauses.push('correctness check failed');
  if (httpCount >= ERROR_ATTENTION) clauses.push('errors');
  if (stoppedAt !== null) clauses.push(`threads stopped at turn ${count(stoppedAt)} of ${count(target)}`);
  if (regressed.length > 0) clauses.push(`${regressed.length} regression${regressed.length === 1 ? '' : 's'}`);
  if (clauses.length === 0) clauses.push('all quiet');

  const dot = dotFor({ failed, attention: guard > 0 || httpCount >= ERROR_ATTENTION || stoppedAt !== null || regressed.length > 0 });
  const date = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
  const lines = [`${dot} *Delta Channel · ${date}*${manual ? ' · manual run' : ''}${apiVersion ? ` · API ${apiVersion}` : ''} · ${clauses.join(' · ')}`];
  if (failed) lines.push(`*Failed:* ${failureReason(run)}`);
  if (guard > 0 || httpParts.length > 0) {
    lines.push(`*Errors:* ${[...httpParts, guard > 0 ? `correctness check failed × ${count(guard)}` : null].filter(Boolean).join(', ')}`);
  }
  for (const change of regressed) lines.push(`⚠️ *${change.text}*`);
  if (depth) {
    lines.push(`_at turn ${depthLabel(depth)}_`, ...mainTable(run.cells, depth, history));
  } else {
    lines.push('*No turn was finished by every user on both cells.*');
  }
  if (depth && !anyBytes(run.cells[0])) {
    lines.push('_No data row: the deployment runs an API without `GET /threads/{id}/storage` yet._');
  }
  if (history.length < MIN_HISTORY_NIGHTS) lines.push(`_${history.length} of ${MIN_HISTORY_NIGHTS} nights of history, no change flags yet_`);
  lines.push(footer('delta-channel', artifactUrl));

  return { text: lines.join('\n'), thread: [threadText(run, metrics, guard, improved)] };
}

function threadText(run, metrics, guard, improved) {
  const users = Number(run.load?.loadSize) || null;
  const turns = Number(run.load?.turns) || null;
  const shape = users && turns ? `${count(users)} users × ${count(turns)} turns × ${run.cells.length} setups · ` : '';
  const health = metrics
    ? `${count(metrics.failedRuns)} failed of ${count(metrics.totalRuns)} turns · ${guard > 0 ? `correctness check failed × ${count(guard)}` : 'no correctness failures'}`
    : 'no results';
  return [
    '*As the thread grows*',
    ...growthTables(run.cells),
    `*Run* · ${shape}${health}`,
    ...(improved.length > 0 ? [`*Improved:* ${improved.map((c) => c.text).join(' · ')}`] : []),
  ].join('\n');
}

function safeBuildReport(run, context) {
  try {
    return buildReport(run, context);
  } catch (error) {
    // A bad night still gets reported: say so rather than failing the step.
    return {
      text: ['🔴 *Delta Channel*', `*Could not build the report:* ${error.message}`, `*Step outcome:* \`${run.stepOutcome}\``, context.artifactUrl ? `<${context.artifactUrl}|Artifacts>` : '']
        .filter(Boolean)
        .join('\n'),
      thread: [],
    };
  }
}

async function main() {
  const run = await collectRun(process.env.RESULTS_DIR || path.join(HERE, 'results'));
  const outDir = process.env.OUT_DIR || path.join(HERE, 'delta-report');
  mkdirSync(outDir, { recursive: true });
  // Tonight's aggregate, for the trend and flags of the nights to come.
  writeFileSync(
    path.join(outDir, 'delta_report.json'),
    JSON.stringify({ design: DESIGN, cells: Object.fromEntries(run.cells.map((c) => [c.cell, { buckets: c.buckets }])) }, null, 2)
  );
  const report = safeBuildReport(run, {
    apiVersion: process.env.API_VERSION || readApiVersion(),
    artifactUrl: process.env.ARTIFACT_URL,
    manual: process.env.MANUAL === 'true',
    history: process.env.HISTORY_DIR ? loadDeltaHistory(process.env.HISTORY_DIR) : [],
  });
  await postReport(report);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(`Failed to post delta report: ${error.message}`);
    process.exit(1);
  });
}
