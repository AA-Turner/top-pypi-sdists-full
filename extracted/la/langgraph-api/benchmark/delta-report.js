/*
 * The nightly delta-channel report. Reads the k6 raw sample files because the
 * per-depth numbers live only in sample tags; the summary has aggregates for
 * the whole run.
 */

import { createReadStream, existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

import { ERROR_ATTENTION, MIN_SUCCESS_RATE, describeThreshold, errorParts, findLatestSummary, isHealthy, readApiVersion, readSummary } from './daily-report.js';
import { MIN_HISTORY_NIGHTS, compare, flaggedChange, formatDelta, formatMove } from './history.js';
import { dotFor, postReport } from './slack.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/** `cell` is the matrix key and the artifact infix. Snapshot frequency is fixed per graph. */
export const CELLS = [
  { cell: 'control', graph: 'benchmark', column: 'non-delta', label: 'plain channel', snapshot: null },
  { cell: 'delta_50', graph: 'benchmark_delta_freq', column: '50', label: 'delta, snapshot every 50 (deepagents)', snapshot: 50 },
  { cell: 'delta_500', graph: 'benchmark_delta_500', column: '500', label: 'delta, snapshot every 500', snapshot: 500 },
  { cell: 'delta_1000', graph: 'benchmark_delta', column: '1000', label: 'delta, snapshot every 1000 (library default)', snapshot: 1000 },
];

/** The channel table compares against the setting customers actually run. */
export const HEADLINE = ['control', 'delta_50'];

/** Metric key, label, printer. All three are lower-is-better. */
const METRICS = [
  ['readP50Ms', 'read', (v) => (isNumber(v) ? (v / 1000).toFixed(2) : '-')],
  ['saveMs', 'write', (v) => (isNumber(v) ? (v / 1000).toFixed(2) : '-')],
  ['bytes', 'KB', (v) => (isNumber(v) ? String(Math.round(v / 1024)) : '-')],
];

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

export function bucketStart(bucket) {
  const n = parseInt(String(bucket).split('-')[0], 10);
  return Number.isFinite(n) ? n : Number.MAX_SAFE_INTEGER;
}

const byDepth = (a, b) => bucketStart(a) - bucketStart(b);

/** Rows are labelled by the turn they end on, where the cold read and storage read happen. */
function depthLabel(bucket) {
  return String(bucket).split('-')[1] ?? String(bucket);
}

function bucketEnd(bucket) {
  const n = parseInt(depthLabel(bucket), 10);
  return Number.isFinite(n) ? n : 0;
}

/** Every 250 turns is enough to see a slope; the first and deepest rows anchor it. */
export const HEADLINE_EVERY = 250;

/** `keep` adds rows that must show regardless of spacing: the ones carrying a flagged change. */
export function headlineRows(depths, keep = []) {
  const sorted = [...depths].sort(byDepth);
  const last = sorted.at(-1);
  const kept = new Set(keep);
  return sorted.filter((d, i) => i === 0 || d === last || kept.has(d) || bucketEnd(d) % HEADLINE_EVERY === 0);
}

/**
 * The turn before each snapshot and the snapshot turn are the peaks and resets
 * of the read sawtooth; the rows in between only repeat the slope.
 */
export function sweepRows(depths, frequencies) {
  const sorted = [...depths].sort(byDepth);
  if (sorted.length === 0) return [];
  const width = bucketEnd(sorted[0]) - bucketStart(sorted[0]) + 1;
  const last = bucketEnd(sorted.at(-1));
  const wanted = new Set([bucketEnd(sorted[0]), last]);
  for (const f of frequencies.filter((f) => isNumber(f) && f > width)) {
    for (let turn = f; turn <= last; turn += f) {
      wanted.add(turn - width);
      wanted.add(turn);
    }
  }
  return sorted.filter((d) => wanted.has(bucketEnd(d)));
}

/** Bytes keep the largest reading in the bucket: the thread only grows. */
export function aggregateSamples(points) {
  const turns = {};
  const reads = {};
  const saves = {};
  const rowSaves = {};
  const bytes = {};
  for (const point of points) {
    const depth = point.tags?.depth;
    if (depth == null || !isNumber(point.value)) continue;
    if (point.metric === 'turn_duration') (turns[depth] ??= []).push(point.value);
    else if (point.metric === 'state_read_duration') (reads[depth] ??= []).push(point.value);
    else if (point.metric === 'checkpoint_save') {
      (saves[depth] ??= []).push(point.value);
      if (point.tags?.row_turn === '1') (rowSaves[depth] ??= []).push(point.value);
    }
    else if (point.metric === 'thread_storage_bytes') bytes[depth] = Math.max(bytes[depth] ?? 0, point.value);
  }
  const buckets = {};
  for (const depth of new Set([...Object.keys(turns), ...Object.keys(reads), ...Object.keys(saves), ...Object.keys(bytes)])) {
    const sorted = (turns[depth] ?? []).sort((a, b) => a - b);
    const sortedReads = (reads[depth] ?? []).sort((a, b) => a - b);
    const sortedSaves = (saves[depth] ?? []).sort((a, b) => a - b);
    const sortedRowSaves = (rowSaves[depth] ?? []).sort((a, b) => a - b);
    const p50Ms = percentile(sorted, 0.5);
    // One cold read per thread per VERIFY_EVERY turns is few samples, so the median only.
    const readP50Ms = percentile(sortedReads, 0.5);
    buckets[depth] = {
      turns: sorted.length,
      p50Ms,
      p95Ms: percentile(sorted, 0.95),
      readP50Ms,
      saveMs: percentile(sortedSaves, 0.5),
      rowSaveMs: percentile(sortedRowSaves, 0.5),
      bytes: bytes[depth] ?? null,
    };
  }
  return buckets;
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

/**
 * One directory per cell, as `actions/download-artifact` lays them out without
 * merging. A cell with no directory never ran.
 */
export async function collectCells(resultsDir) {
  const dirs = existsSync(resultsDir)
    ? readdirSync(resultsDir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)
    : [];
  const cells = [];
  for (const spec of CELLS) {
    const name = dirs.find((dir) => dir.startsWith(`delta-results-${spec.cell}-`));
    const dir = name ? path.join(resultsDir, name) : null;
    const context = dir ? readSummary(path.join(dir, 'report_context.json')) ?? {} : {};
    const raw = dir ? newestRawData(dir) : null;
    cells.push({
      ...spec,
      stepOutcome: context.stepOutcome ?? (dir ? 'unknown' : 'missing'),
      summary: dir ? readSummary(findLatestSummary(dir)) : null,
      load: { loadSize: context.loadSize, plateauDuration: context.plateauDuration, checkpointSize: context.checkpointSize },
      buckets: raw ? aggregateSamples(await readSamples(raw)) : {},
    });
  }
  return cells;
}

export function loadDeltaHistory(dir) {
  const nights = [];
  let runs;
  try {
    runs = readdirSync(dir, { withFileTypes: true }).filter((e) => e.isDirectory());
  } catch {
    return nights;
  }
  for (const run of runs) {
    let files;
    try {
      files = readdirSync(path.join(dir, run.name), { recursive: true });
    } catch {
      continue;
    }
    const file = files.find((name) => path.basename(name) === 'delta_report.json');
    const report = file ? readSummary(path.join(dir, run.name, file)) : null;
    if (report?.cells) nights.push(report.cells);
  }
  return nights;
}

function healthy(cell) {
  return isHealthy({ stepOutcome: cell.stepOutcome, metrics: cell.summary?.metrics });
}

function guardFailures(cell) {
  const n = cell.summary?.metrics?.errors?.missingMessage;
  return isNumber(n) ? n : 0;
}

function httpErrorCount(cell) {
  const byStatus = cell.summary?.metrics?.errors?.byStatus;
  if (!byStatus || typeof byStatus !== 'object') return 0;
  return Object.values(byStatus).filter(isNumber).reduce((sum, n) => sum + n, 0);
}

function deepest(buckets) {
  const depths = Object.keys(buckets).filter((d) => buckets[d].turns > 0);
  return depths.length ? depths.sort(byDepth).at(-1) : null;
}

/**
 * A bucket counts as measured when it has a cold read: the row is about read
 * and write. A run that stops mid-bucket has turns there but no read yet, and a
 * verify turn whose state read failed can leave storage bytes with no read.
 */
function hasRead(bucket) {
  return isNumber(bucket?.readP50Ms);
}

function measuredDeepest(buckets) {
  const depths = Object.keys(buckets).filter((d) => hasRead(buckets[d]));
  return depths.length ? depths.sort(byDepth).at(-1) : null;
}

/**
 * Rows every cell in a table has a read for, checked per row: a slower cell
 * stops earlier, and a verify turn whose state read failed leaves a hole at
 * any depth. A row where one column is `-` compares nothing; how far each cell
 * got is reported as its own line instead.
 */
function sharedDepths(cells, depths) {
  return [...depths].filter((d) => cells.every((c) => hasRead(c.buckets?.[d]))).sort(byDepth);
}

function depthLine(cells, plateauDuration) {
  const held = heldFor(plateauDuration) ?? 'the run';
  const parts = cells.map((c) => {
    const top = measuredDeepest(c.buckets ?? {});
    return `${cellName(c)} ${top ? count(bucketEnd(top)) : '-'}`;
  });
  return `_Last measured turn in ${held}: ${parts.join(' · ')}_`;
}

function failureReason(cell) {
  const metrics = cell.summary?.metrics;
  if (!metrics) return `no results produced, step finished as \`${cell.stepOutcome}\``;
  const crossed = [];
  for (const [metric, expressions] of Object.entries(cell.summary.thresholds ?? {})) {
    for (const [expression, verdict] of Object.entries(expressions ?? {})) {
      if (verdict?.ok === false) crossed.push(describeThreshold(metric, expression, metrics).breach);
    }
  }
  if (crossed.length > 0) return crossed.join(', ');
  if (!metrics.successfulRuns) return 'no turn succeeded';
  if (isNumber(metrics.successRate) && metrics.successRate <= MIN_SUCCESS_RATE) {
    return `success ${metrics.successRate.toFixed(2)}% (floor ${MIN_SUCCESS_RATE}%)`;
  }
  return `step finished as \`${cell.stepOutcome}\``;
}

/**
 * Compared per metric at the deepest turn with a reading tonight and every
 * night: a shallower one would hide a regression that only shows at depth, and
 * a run that stops mid-bucket has turns there but no cold read yet.
 */
export function cellChanges(cell, history) {
  const buckets = cell.buckets ?? {};
  const changes = [];
  for (const [key, label, format] of METRICS) {
    const depth = Object.keys(buckets)
      .filter((d) => isNumber(buckets[d][key]) && history.every((night) => isNumber(night[cell.cell]?.buckets?.[d]?.[key])))
      .sort(byDepth)
      .at(-1);
    if (!depth) continue;
    const past = history.map((night) => night[cell.cell].buckets[depth][key]);
    const flagged = flaggedChange(buckets[depth][key], past, { higherIsBetter: false });
    const verdict = flagged ?? compare(buckets[depth][key], past);
    if (!verdict) continue;
    changes.push({
      key,
      label,
      depth,
      flagged: Boolean(flagged),
      better: flagged?.better ?? null,
      arrow: flagged?.arrow ?? null,
      deltaPct: verdict.deltaPct,
      move: formatMove(format(verdict.median), format(buckets[depth][key]), verdict.deltaPct, key === 'bytes' ? 'KB' : 's'),
    });
  }
  return changes;
}

function heldFor(plateauDuration) {
  const plateau = Number(plateauDuration);
  if (!isNumber(plateau) || plateau <= 0) return null;
  return plateau % 60 === 0 ? `${plateau / 60} min` : `${plateau}s`;
}

/** Same shape as the daily digest's second line: k6, paths, measures. */
export function describeDelta(cells) {
  const withLoad = cells.find((c) => Number(c.load?.loadSize) > 0);
  const users = withLoad ? `${count(Number(withLoad.load.loadSize))} users` : 'a few users';
  const held = heldFor(withLoad?.load?.plateauDuration);
  const load = [users, 'one thread each', held ? `${held} hold` : null, 'closed model'].filter(Boolean).join(', ');
  const bytes = Number(withLoad?.load?.checkpointSize);
  const appended = bytes >= 1024 ? `${Math.round(bytes / 1024)} KB` : bytes > 0 ? `${bytes} B` : null;
  return (
    `k6: ${load}. Paths: one turn per iteration on a growing thread (run and wait${appended ? `, ${appended} appended` : ''}), plus a cold state read and a storage read every 50 turns. ` +
    'Cells: plain channel vs DeltaChannel with a snapshot every 50 (deepagents), 500 and 1000 (library default). ' +
    "Measures read, write and checkpoint bytes by thread depth. Same load nightly on the day's revision, so a change is the server."
  );
}

function groupName(cell) {
  return cell.cell === 'control' ? 'non-delta' : `delta, snap ${cell.column}`;
}

export function headlineTable(cells, changesByCell) {
  const pair = HEADLINE.map((key) => cells.find((c) => c.cell === key)).filter(Boolean);
  const flaggedDepths = pair.flatMap((c) => (changesByCell.get(c) ?? []).filter((ch) => ch.flagged).map((ch) => ch.depth));
  // The deepest bucket often has turns but no cold read yet; a row of dashes says nothing.
  const measured = new Set(pair.flatMap((c) => Object.keys(c.buckets ?? {}).filter((d) => hasRead(c.buckets[d]))));
  const depths = headlineRows(sharedDepths(pair, measured), flaggedDepths);
  if (depths.length === 0) return ['*No per-depth samples were recorded.*'];
  const w = 8;
  const units = { read: 'read s', write: 'write s', KB: 'KB' };
  const lines = [
    '```',
    ['turn'.padEnd(6), ...pair.map((c) => groupName(c).padStart(w * 3))].join(''),
    [''.padEnd(6), ...pair.flatMap(() => METRICS.map(([, label]) => units[label].padStart(w)))].join(''),
  ];
  for (const depth of depths) {
    const row = [depthLabel(depth).padEnd(6)];
    for (const cell of pair) {
      const b = cell.buckets?.[depth];
      for (const [key, , format] of METRICS) {
        const change = changesByCell.get(cell)?.find((c) => c.key === key && c.depth === depth && c.flagged);
        const value = b && b.turns > 0 ? format(b[key]) : '-';
        row.push(`${value}${change?.arrow ?? ''}`.padStart(w));
      }
    }
    lines.push(row.join(''));
  }
  lines.push('```');
  return lines;
}

export function sweepTables(cells) {
  const deltas = cells.filter((c) => c.cell !== 'control');
  const depths = sweepRows(sharedDepths(deltas, new Set(deltas.flatMap((c) => Object.keys(c.buckets ?? {})))), deltas.map((c) => c.snapshot));
  if (depths.length === 0) return [];
  const w = 10;
  const titles = { read: 'read, median seconds', write: 'write, median / at the row\'s turn, seconds', KB: 'storage, KB at that turn' };
  const cellText = (b, key, format) => {
    if (!(b?.turns > 0)) return '-';
    if (key === 'saveMs' && isNumber(b.rowSaveMs)) return `${format(b[key])}/${format(b.rowSaveMs)}`;
    return format(b[key]);
  };
  return METRICS.map(([key, label, format]) => {
    const lines = [`*${titles[label]}*`, '```'];
    lines.push(['turn'.padEnd(6), ...deltas.map((c) => `snap ${c.column}`.padStart(w))].join(''));
    for (const depth of depths) {
      lines.push(
        [depthLabel(depth).padEnd(6), ...deltas.map((c) => cellText(c.buckets?.[depth], key, format).padStart(w))].join('')
      );
    }
    lines.push('```');
    return lines.join('\n');
  });
}

function cellName(cell) {
  return cell.cell === 'control' ? 'non-delta' : `delta/${cell.column}`;
}

/**
 * Cells whose successful runs returned no `save_ms`: the deployed graph predates
 * the save timing. A cell with no successful run is already reported as failed.
 */
function cellsWithoutSaves(cells) {
  return cells.filter(
    (c) => c.summary?.metrics?.successfulRuns > 0 && !Object.values(c.buckets ?? {}).some((b) => isNumber(b.saveMs))
  );
}

function anyBytes(cells) {
  return cells.some((c) => Object.values(c.buckets ?? {}).some((b) => isNumber(b.bytes)));
}

/**
 * @param {Array<object>} cells from collectCells
 * @param {{apiVersion?: string|null, artifactUrl?: string|null, now?: Date, manual?: boolean, history?: object[]}} context
 * @returns {{text: string, thread: string[]}}
 */
export function buildReport(cells, context = {}) {
  const { apiVersion = null, artifactUrl = null, now = new Date(), manual = false, history = [] } = context;

  const changesByCell = new Map(cells.map((cell) => [cell, cell.summary?.metrics ? cellChanges(cell, history) : []]));
  const unhealthy = cells.filter((cell) => !healthy(cell));
  const withGuard = cells.filter((cell) => guardFailures(cell) > 0);
  const withHttp = cells.filter((cell) => errorParts(cell.summary?.metrics).length > 0);
  // Same bar as the daily digest: a stray 503 is noted, not escalated. A guard
  // failure is a correctness bug, so one is enough.
  const manyHttp = withHttp.filter((cell) => httpErrorCount(cell) >= ERROR_ATTENTION);
  const regressed = [];
  const improved = [];
  for (const cell of cells) {
    for (const change of changesByCell.get(cell)) {
      if (!change.flagged) continue;
      (change.better ? improved : regressed).push(`${cellName(cell)} ${change.label}@turn ${depthLabel(change.depth)} ${change.move}`);
    }
  }
  const nights = history.length;
  const checked = nights >= MIN_HISTORY_NIGHTS;

  const clauses = [];
  if (unhealthy.length > 0) clauses.push(`${unhealthy.map(cellName).join(', ')} failed`);
  if (withGuard.length > 0) clauses.push(`correctness check failed in ${withGuard.map(cellName).join(', ')}`);
  if (manyHttp.length > 0) clauses.push(`errors in ${manyHttp.map(cellName).join(', ')}`);
  if (regressed.length > 0) clauses.push(`${regressed.length} regression${regressed.length === 1 ? '' : 's'}`);
  if (clauses.length === 0) clauses.push('all quiet');

  const dot = dotFor({
    failed: unhealthy.length > 0,
    attention: withGuard.length + manyHttp.length + regressed.length > 0,
  });
  const date = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
  const passed = cells.length - unhealthy.length;
  const lines = [
    `${dot} *Delta Channel · ${date}*${manual ? ' · manual run' : ''}${apiVersion ? ` · API ${apiVersion}` : ''} · ${passed} of ${cells.length} cells passed · ${clauses.join(' · ')}`,
    describeDelta(cells),
  ];
  if (unhealthy.length > 0) {
    lines.push(`*Failed:* ${unhealthy.map((cell) => `${cellName(cell)}: ${failureReason(cell)}`).join(' · ')}`);
  }
  if (withGuard.length + withHttp.length > 0) {
    const parts = cells
      .filter((cell) => withGuard.includes(cell) || withHttp.includes(cell))
      .map(
        (cell) =>
          `${cellName(cell)} ${[...errorParts(cell.summary.metrics), guardFailures(cell) > 0 ? `correctness check failed × ${count(guardFailures(cell))}` : null].filter(Boolean).join(', ')}`
      );
    lines.push(`*Errors:* ${parts.join(' · ')}`);
  }
  if (!checked) {
    lines.push(`*Regressed:* not checked, ${nights} of ${MIN_HISTORY_NIGHTS} nights of history`);
  } else {
    lines.push(`*Regressed:* ${regressed.length > 0 ? regressed.join(' · ') : 'none'}`);
    if (improved.length > 0) lines.push(`*Improved:* ${improved.join(' · ')}`);
  }

  lines.push(
    '',
    `*Plain channel vs DeltaChannel at the deepagents setting* · a row every ${HEADLINE_EVERY} turns of a thread, plus the first and deepest; read and write are medians of the 50 turns before it, KB at that turn. Delta should keep both flat as the thread deepens.`
  );
  lines.push(...headlineTable(cells, changesByCell));
  lines.push(depthLine(cells, cells.find((c) => c.load?.plateauDuration)?.load.plateauDuration));
  const unsaved = cellsWithoutSaves(cells);
  if (unsaved.length > 0) {
    lines.push(
      `_write reads \`-\` for ${unsaved.map(cellName).join(', ')}: its runs returned no \`save_ms\`, so the deployed benchmark graph predates langgraph-server-benchmarks#22._`
    );
  }
  if (!anyBytes(cells)) {
    lines.push('_KB reads `-`: the deployment runs an API without `GET /threads/{id}/storage` yet._');
  }

  lines.push(
    [
      '*Pass:* errors < 1% and success > 99% per cell, delta on where expected, cold re-read matches the run',
      `▲ better ▼ worse than the last ${MIN_HISTORY_NIGHTS}+ nights`,
      `🟢 quiet · 🟡 a correctness check failed, ${ERROR_ATTENTION}+ failed requests or a regression · 🔴 a cell failed`,
    ].join(' · ')
  );
  lines.push(`*Thread:* per-cell detail, the snapshot-frequency sweep and how to read${artifactUrl ? ` · <${artifactUrl}|Artifacts:> summaries and raw samples` : ''}`);

  return { text: lines.join('\n'), thread: [perCellDetail(cells, changesByCell, history.length), howToRead(cells)] };
}

function perCellDetail(cells, changesByCell, nights) {
  const withLoad = cells.find((c) => Number(c.load?.loadSize) > 0);
  const threads = withLoad ? Number(withLoad.load.loadSize) : null;
  const lines = ['*Per cell* · tonight, then against the past nights at the deepest turn every night reached'];
  for (const cell of cells) {
    const m = cell.summary?.metrics;
    if (!m) {
      lines.push(`${cellName(cell)}: no results, step finished as \`${cell.stepOutcome}\``);
      continue;
    }
    const top = deepest(cell.buckets);
    const shape = threads && top ? ` (${count(threads)} threads × ${depthLabel(top)} deep)` : '';
    const parts = [`${count(m.failedRuns)} failed of ${count(m.totalRuns)} turns${shape}`];
    const changes = changesByCell.get(cell);
    const sameDepth = new Set(changes.map((c) => c.depth)).size === 1;
    const drift =
      changes.length > 0
        ? `vs ${nights} nights${sameDepth ? ` at turn ${depthLabel(changes[0].depth)}` : ''}: ${changes
            .map((c) => `${c.label} ${formatDelta(c.deltaPct)}${sameDepth ? '' : ` (turn ${depthLabel(c.depth)})`}${c.flagged ? ` ${c.arrow}` : ''}`)
            .join(' · ')}`
        : nights < 2
          ? 'no history to compare'
          : 'no turn every night reached';
    lines.push(`${cellName(cell)}: ${parts.join(' · ')} · ${drift}`);
  }
  lines.push(
    '',
    '*Snapshot frequency sweep* · delta cells only, columns are the snapshot frequency. Rows: the first turn, the turn before and at each snapshot, and the deepest. Read climbs between snapshots and resets at each one; the full series is in the artifacts.',
    ...sweepTables(cells)
  );
  return lines.join('\n');
}

/** The longer explanation, at the end of the thread so the channel message stays short. */
function howToRead(cells) {
  const withLoad = cells.find((c) => Number(c.load?.loadSize) > 0);
  const held = heldFor(withLoad?.load?.plateauDuration);
  return [
    '*How to read*',
    `• *Tests:* ${cells.map((c) => `${cellName(c)} = ${c.label}`).join(' · ')}. Each is one k6 run of the same graph logic; only the channel type and snapshot frequency differ.`,
    withLoad ? `• *Load:* ${count(Number(withLoad.load.loadSize))} users, one thread each${held ? `, held ${held}` : ''}, one turn per iteration, no ramp.` : null,
    '• *Turn:* one `POST /runs/wait` on the thread, which reads the last checkpoint, runs one step and saves a new one. The row label is the thread depth the cold read was taken at.',
    '• *Read:* a cold `GET /threads/{id}/state` every 50 turns, timed to the server\'s first byte, so sending the state back is not counted. The server rebuilds the value from storage with nothing to write. With delta that is the replay of every diff since the last snapshot.',
    '• *Write:* the checkpoint save, timed by the worker as the gap between the graph\'s two steps, with saves made synchronous so nothing overlaps it. The sweep also shows the save at the row\'s own turn: snapshots fall on those turns, so at a snapshot row it is the full-value write the median hides.',
    '• *Storage:* `GET /threads/{id}/storage` every 50 turns, the bytes the thread occupies at that turn.',
    `• *Regressed / Improved:* read, write or storage at the deepest turn every night reached, outside its own usual range over the last ${MIN_HISTORY_NIGHTS}+ nights.`,
    `• *Errors:* failed requests by HTTP status. ${ERROR_ATTENTION} or more turn the dot yellow even when the cell passes.`,
    '• *Correctness check:* at turn 2 each cell confirms delta is on (delta cells) or off (plain cell), because a too-old langgraph silently degrades a DeltaChannel to a plain one. Every 50 turns the cold re-read is compared to what the run returned. A failure of either is a bug, not a slow night.',
    '• *Rows:* the channel table shows a row every 250 turns plus the first and deepest; the sweep shows the turn before and at each snapshot. Tables stop at the depth every cell reached; the line under the channel table says how far each got. Every 50-turn row is in the run artifacts.',
    '• `-` in a cell: no number, the cell produced no results or no thread reached that depth.',
  ]
    .filter(Boolean)
    .join('\n');
}

function safeBuildReport(cells, context) {
  try {
    return buildReport(cells, context);
  } catch (error) {
    // A bad night still gets reported: say so rather than failing the step.
    return {
      text: [
        '🔴 *Delta Channel*',
        `*Could not build the report:* ${error.message}`,
        `*Step outcomes:* ${cells.map((c) => `${cellName(c)} \`${c.stepOutcome}\``).join(' · ')}`,
        context.artifactUrl ? `<${context.artifactUrl}|Artifacts>` : '',
      ]
        .filter(Boolean)
        .join('\n'),
      thread: [],
    };
  }
}

async function main() {
  const cells = await collectCells(process.env.RESULTS_DIR || path.join(HERE, 'results'));
  const outDir = process.env.OUT_DIR || path.join(HERE, 'delta-report');
  mkdirSync(outDir, { recursive: true });
  // Tonight's aggregate, for the "vs last nights" line of the nights to come.
  writeFileSync(
    path.join(outDir, 'delta_report.json'),
    JSON.stringify({ cells: Object.fromEntries(cells.map((c) => [c.cell, { buckets: c.buckets }])) }, null, 2)
  );
  const report = safeBuildReport(cells, {
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
