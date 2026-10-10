/*
 * The verdict is NOT recomputed here. k6 exits non-zero when a threshold is
 * crossed, so the step outcome already carries it; this reads that outcome and
 * explains it.
 */

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { MIN_HISTORY_NIGHTS, compare, flaggedChange, formatDelta, formatMove, loadDailyHistory } from './history.js';
import { describeRunnerBriefly, runnerColumnName, runnerGloss, runnerShortName } from './runner-descriptions.js';
import { dotFor, postReport } from './slack.js';

// Resolve against this file, not the working directory, so the step does not
// have to be run from a particular place for the paths to line up.
const HERE = path.dirname(fileURLToPath(import.meta.url));

/** Must match the matrix in _benchmark-daily.yml. */
export const RUNNERS = ['wait_write', 'stream_write', 'threads_search_metadata'];

/**
 * A run must beat this success rate to be healthy, strictly. 99 exactly is not
 * enough, which is the bar the workflow's `SUCCESS_RATE > 99` already used and
 * is preserved here deliberately. The value matches staircase.py's
 * MIN_SUCCESS_RATE, the one such number in this repo with a recorded rationale.
 */
export const MIN_SUCCESS_RATE = 99;


/**
 * Red unless the run both completed and produced healthy numbers.
 *
 * A crossed threshold fails the k6 step, so `stepOutcome` already covers it.
 * The other two clauses catch what an exit code cannot: a run that never
 * produced a summary, and a run where every iteration failed.
 */
export function isHealthy({ stepOutcome, metrics }) {
  if (stepOutcome !== 'success') return false;
  if (!metrics) return false;
  if (!metrics.successfulRuns) return false;
  // A success rate that is absent, NaN or not a number is not evidence of
  // health, so it must not be compared loosely into a pass.
  if (!isNumber(metrics.successRate)) return false;
  return metrics.successRate > MIN_SUCCESS_RATE;
}

/**
 * Formatting here is deliberately total. A truncated or partial summary is one
 * of the cases this reporter exists to survive: throwing while formatting would
 * fail the step and post nothing, which is the silence it replaces.
 */
function isNumber(value) {
  return typeof value === 'number' && Number.isFinite(value);
}

function seconds(value, digits = 2) {
  return isNumber(value) ? `${value.toFixed(digits)}s` : 'n/a';
}

function count(value) {
  return isNumber(value) ? Math.round(value).toLocaleString('en-US') : 'n/a';
}

/**
 * A k6 threshold in words. `count>N` is a throughput floor and `rate<X` an
 * error budget, which the raw expression does not say.
 */
export function describeThreshold(metric, expression, metrics) {
  const raw = `${metric} ${expression}`;
  const match = /^([a-z0-9()]+)([<>]=?)([\d.]+)$/i.exec(expression.replace(/\s+/g, ''));
  if (!match) return { rule: raw, breach: raw };
  const [, aggregate, , limitText] = match;
  const limit = Number(limitText);
  if (metric === 'run_duration' && aggregate === 'p(95)') {
    const limitSeconds = `${limit / 1000}s`;
    return {
      rule: `p95 < ${limitSeconds}`,
      breach: `p95 ${seconds(metrics?.p95Duration)} (limit ${limitSeconds})`,
    };
  }
  if (metric === 'successful_runs' && aggregate === 'count') {
    return {
      rule: `at least ${count(limit)} successful runs`,
      breach: `successful runs ${count(metrics?.successfulRuns)} (floor ${count(limit)})`,
    };
  }
  if (metric === 'http_req_failed' && aggregate === 'rate') {
    const budget = `${Number((limit * 100).toPrecision(6))}%`;
    return { rule: `request errors < ${budget}`, breach: `request errors over ${budget}` };
  }
  return { rule: raw, breach: raw };
}

function describedThresholds(thresholds, metrics) {
  const described = [];
  for (const [metric, expressions] of Object.entries(thresholds ?? {})) {
    for (const [expression, verdict] of Object.entries(expressions ?? {})) {
      described.push({ ...describeThreshold(metric, expression, metrics), ok: verdict?.ok });
    }
  }
  return described;
}

function usersOf({ loadSize, levels }) {
  const load = Number(loadSize);
  if (!isNumber(load) || load <= 0) return null;
  const levelCount = Number(levels);
  return isNumber(levelCount) && levelCount > 0 ? load * levelCount : load;
}

function heldFor(plateauDuration) {
  const plateau = Number(plateauDuration);
  if (!isNumber(plateau) || plateau <= 0) return '';
  return plateau % 60 === 0 ? `${plateau / 60} min` : `${plateau}s`;
}

function usersSentence(runs) {
  const withLoad = runs.filter((run) => usersOf(run.load ?? {}) != null);
  if (withLoad.length === 0) return null;
  const common = Math.max(...withLoad.map((run) => usersOf(run.load)));
  const others = withLoad
    .filter((run) => usersOf(run.load) !== common)
    .map((run) => `${runName(run)} ${count(usersOf(run.load))}`);
  return `${count(common)} virtual users${others.length > 0 ? ` (${others.join(', ')})` : ''}`;
}

// The 60 s per level is ramp.js's stage length.
export function describeBenchmark(runs, prefix = '') {
  const withLoad = runs.filter((run) => usersOf(run.load ?? {}) != null);
  const { levels, plateauDuration } = withLoad[0]?.load ?? {};
  const levelCount = Number(levels);
  const users = usersSentence(runs);
  const held = heldFor(plateauDuration);
  const load = [
    users,
    isNumber(levelCount) && levelCount > 0 ? `${levelCount}×60 s ramp` : null,
    held ? `${held} hold` : null,
    'closed model',
  ]
    .filter(Boolean)
    .join(', ');
  const paths = runs.map((run) => runnerGloss(run.benchmarkType)).join(', ');
  return [
    prefix.trim(),
    `k6: ${load}. Paths: ${paths}. Measures per-iteration latency (avg, p95) and failed requests by status. Same load nightly on a fresh revision, so a change is the server.`,
  ]
    .filter(Boolean)
    .join(' ');
}

export function loadSentence(runs) {
  const withLoad = runs.filter((run) => usersOf(run.load ?? {}) != null);
  if (withLoad.length === 0) return '';
  const users = withLoad.map((run) => usersOf(run.load));
  const common = users.sort((a, b) => b - a)[0];
  const parts = [`${count(common)} users`];
  for (const run of withLoad) {
    if (usersOf(run.load) !== common) parts.push(`${runnerColumnName(run.benchmarkType)} ${count(usersOf(run.load))}`);
  }
  const { levels, plateauDuration } = withLoad[0].load;
  const held = heldFor(plateauDuration);
  if (held) parts.push(`held ${held}`);
  const levelCount = Number(levels);
  const ramp = isNumber(levelCount) && levelCount > 0 ? ` after a ${levelCount}-step ramp` : '';
  return `${parts.join(', ')}${ramp}`;
}

export function toolLine(metrics) {
  const overhead = metrics?.clientOverheadMs?.med;
  const average = metrics?.averageDuration;
  if (!isNumber(overhead) || !isNumber(average) || average <= 0) return null;
  const share = overhead / (average * 1000);
  if (share <= 0.1) return null;
  return `the test machine spent ${Math.round(overhead)}ms per run outside requests (${Math.round(share * 100)}% of the average); read latency with that in mind`;
}

export function errorParts(metrics) {
  const byStatus = metrics?.errors?.byStatus;
  if (!byStatus || typeof byStatus !== 'object') return [];
  return Object.entries(byStatus)
    .filter(([, n]) => isNumber(n) && n > 0)
    .map(([status, n]) => `${/^\d+$/.test(status) ? `HTTP ${status}` : status} × ${count(n)}`);
}

function hasErrors(metrics) {
  return errorParts(metrics).length > 0;
}

function errorCount(metrics) {
  const byStatus = metrics?.errors?.byStatus;
  if (!byStatus || typeof byStatus !== 'object') return 0;
  return Object.values(byStatus).filter(isNumber).reduce((sum, n) => sum + n, 0);
}

/** Counts tonight, so a clean history is a streak of 1. */
export function errorStreak(history) {
  let streak = 1;
  for (const night of history) {
    if (!hasErrors(night)) break;
    streak += 1;
  }
  return streak;
}

function ordinal(n) {
  const suffix = n % 100 >= 11 && n % 100 <= 13 ? 'th' : { 1: 'st', 2: 'nd', 3: 'rd' }[n % 10] ?? 'th';
  return `${n}${suffix}`;
}

// Run count follows latency under a fixed user count, so it is compared but never flagged.
const FIGURES = [
  ['p95', 'p95Duration', true, (v) => seconds(v, 1), true],
  ['avg', 'averageDuration', true, (v) => seconds(v, 1), true],
  ['runs', 'totalRuns', false, count, false],
];

// wait_write posts one 503 most nights; that is worth a line, not a yellow dot.
export const ERROR_ATTENTION = 10;

const succeeded = (metrics) => Number(metrics?.successfulRuns) > 0;

/**
 * Tonight's figures against past nights, each in its own band. Latency is only
 * compared between nights with successes: a night where nothing succeeded
 * reports its failed requests' latency, and comparing against it advertises
 * the outage as a speed-up.
 */
export function figureChanges(metrics, history) {
  const changes = [];
  for (const [label, key, isDuration, format, flaggable] of FIGURES) {
    if (isDuration && !succeeded(metrics)) continue;
    const baseline = (isDuration ? history.filter(succeeded) : history).map((night) => night?.[key]);
    const flagged = flaggable ? flaggedChange(metrics?.[key], baseline, { higherIsBetter: !isDuration }) : null;
    const verdict = flagged ?? compare(metrics?.[key], baseline);
    if (!verdict) continue;
    changes.push({
      label,
      key,
      flagged: Boolean(flagged),
      better: flagged?.better ?? null,
      arrow: flagged?.arrow ?? null,
      deltaPct: verdict.deltaPct,
      move: formatMove(format(verdict.median).replace(/s$/, ''), format(metrics[key]).replace(/s$/, ''), verdict.deltaPct, isDuration ? 's' : ''),
    });
  }
  return changes;
}

function runName(run) {
  return runnerShortName(run.benchmarkType);
}

function failureReason(run) {
  const metrics = run.summary?.metrics;
  if (!metrics) return `no results produced, step finished as \`${run.stepOutcome}\``;
  const crossed = describedThresholds(run.summary.thresholds, metrics).filter((t) => t.ok === false);
  if (crossed.length > 0) return crossed.map((t) => t.breach).join(', ');
  if (!metrics.successfulRuns) return 'no run succeeded';
  if (isNumber(metrics.successRate) && metrics.successRate <= MIN_SUCCESS_RATE) {
    return `success ${metrics.successRate.toFixed(2)}% (floor ${MIN_SUCCESS_RATE}%)`;
  }
  return `step finished as \`${run.stepOutcome}\``;
}

function digestTable(runs, changesByRun) {
  const labelWidth = Math.max(...runs.map((run) => runName(run).length)) + 2;
  const lines = ['```', `${''.padEnd(labelWidth)}${'runs'.padStart(9)}${'failed'.padStart(8)}${'p95 s'.padStart(7)} `];
  for (const run of runs) {
    const metrics = run.summary?.metrics;
    const p95 = changesByRun.get(run)?.find((c) => c.key === 'p95Duration');
    const cells = metrics
      ? [count(metrics.totalRuns), count(metrics.failedRuns), succeeded(metrics) && isNumber(metrics.p95Duration) ? metrics.p95Duration.toFixed(1) : '-']
      : ['-', '-', '-'];
    lines.push(`${runName(run).padEnd(labelWidth)}${cells[0].padStart(9)}${cells[1].padStart(8)}${cells[2].padStart(7)}${p95?.arrow ?? ' '}`);
  }
  lines.push('```');
  return lines;
}

/**
 * @param {Array<{benchmarkType: string, stepOutcome: string, summary: object|null, history?: object[], load?: object}>} runs
 * @returns {{text: string, thread: string[]}}
 */
export function buildDigest(runs, context = {}) {
  const {
    titleSuffix = '',
    apiVersion = null,
    goal = '',
    artifactUrl = null,
    now = new Date(),
    manual = false,
  } = context;

  const changesByRun = new Map(
    runs.map((run) => [run, run.summary?.metrics ? figureChanges(run.summary.metrics, run.history ?? []) : []])
  );
  const unhealthy = runs.filter((run) => !isHealthy({ stepOutcome: run.stepOutcome, metrics: run.summary?.metrics }));
  const withErrors = runs.filter((run) => hasErrors(run.summary?.metrics));
  const manyErrors = withErrors.filter((run) => errorCount(run.summary.metrics) >= ERROR_ATTENTION);
  const regressed = [];
  const improved = [];
  for (const run of runs) {
    for (const change of changesByRun.get(run)) {
      if (!change.flagged) continue;
      (change.better ? improved : regressed).push(`${runName(run)} ${change.label} ${change.move}`);
    }
  }
  const nights = Math.max(0, ...runs.map((run) => (run.history ?? []).length));
  const checked = nights >= MIN_HISTORY_NIGHTS;
  const tools = runs.map((run) => [run, toolLine(run.summary?.metrics)]).filter(([, line]) => line);

  const clauses = [];
  if (unhealthy.length > 0) clauses.push(`${unhealthy.map(runName).join(', ')} failed`);
  if (manyErrors.length > 0) clauses.push(`errors in ${manyErrors.map(runName).join(', ')}`);
  if (regressed.length > 0) clauses.push(`${regressed.length} regression${regressed.length === 1 ? '' : 's'}`);
  if (clauses.length === 0) clauses.push('all quiet');

  const dot = dotFor({
    failed: unhealthy.length > 0,
    attention: manyErrors.length + regressed.length + tools.length > 0,
  });
  const date = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
  const passed = runs.length - unhealthy.length;
  const lines = [
    `${dot} *Daily Benchmark${titleSuffix} · ${date}*${manual ? ' · manual run' : ''}${apiVersion ? ` · API ${apiVersion}` : ''} · ${passed} of ${runs.length} passed · ${clauses.join(' · ')}`,
    describeBenchmark(runs, goal),
  ];
  if (unhealthy.length > 0) {
    lines.push(`*Failed:* ${unhealthy.map((run) => `${runName(run)}: ${failureReason(run)}`).join(' · ')}`);
  }
  if (withErrors.length > 0) {
    lines.push(
      `*Errors:* ${withErrors
        .map((run) => {
          const streak = errorStreak(run.history ?? []);
          const again = manual ? `${streak} runs in a row` : `${ordinal(streak)} night in a row`;
          return `${runName(run)} ${errorParts(run.summary.metrics).join(', ')}${streak > 1 ? `, ${again}` : ''}`;
        })
        .join(' · ')}`
    );
  }
  if (!checked) {
    lines.push(`*Regressed:* not checked, ${nights} of ${MIN_HISTORY_NIGHTS} nights of history`);
  } else {
    lines.push(`*Regressed:* ${regressed.length > 0 ? regressed.join(' · ') : 'none'}`);
    if (improved.length > 0) lines.push(`*Improved:* ${improved.join(' · ')}`);
  }
  for (const [run, line] of tools) lines.push(`:warning: ${runName(run)}: ${line}`);

  lines.push(...digestTable(runs, changesByRun));

  const rules = [...new Set(runs.flatMap((run) => describedThresholds(run.summary?.thresholds, run.summary?.metrics).map((t) => t.rule)))];
  const legend = [
    rules.length > 0 ? `*Pass:* ${rules.join(', ')}` : null,
    `▲ better ▼ worse than the last ${MIN_HISTORY_NIGHTS}+ nights`,
    `🟢 quiet · 🟡 ${ERROR_ATTENTION}+ failed requests or a regression · 🔴 a run failed`,
  ].filter(Boolean);
  lines.push(legend.join(' · '));
  lines.push(`*Thread:* per-run detail and how to read${artifactUrl ? ` · <${artifactUrl}|Artifacts:> results and charts` : ''}`);

  return { text: lines.join('\n'), thread: [perRunDetail(runs, changesByRun, loadSentence(runs))] };
}

function howToRead(runs, load) {
  return [
    '*How to read*',
    `• *Tests:* ${runs.map((run) => `${runName(run)} = ${describeRunnerBriefly(run.benchmarkType)}`).join(' · ')}.`,
    load ? `• *Load:* ${load}.` : null,
    `• *Regressed / Improved:* a figure outside the usual range of the last ${MIN_HISTORY_NIGHTS}+ nights of the same test. Run count is compared here but never flagged; under a fixed user count it follows latency.`,
    `• *Errors:* failed requests by HTTP status. ${ERROR_ATTENTION} or more turn the dot yellow even when the run passes.`,
    '• `-` in a cell: no number, the run produced no results or nothing succeeded.',
  ].filter(Boolean);
}

function perRunDetail(runs, changesByRun, load) {
  const labelWidth = Math.max(...runs.map((run) => runName(run).length)) + 2;
  const lines = [
    '*Per run* · seconds, then tonight against the past nights',
    '```',
    `${''.padEnd(labelWidth)}${'avg'.padStart(7)}${'p95'.padStart(7)}${'p95 ok'.padStart(8)}`,
  ];
  for (const run of runs) {
    const metrics = run.summary?.metrics;
    const cells = !metrics
      ? ['-', '-', '-']
      : !succeeded(metrics)
        ? ['-', '-', '-']
        : [metrics.averageDuration, metrics.p95Duration, metrics.p95SuccessDuration].map((v) => (isNumber(v) ? v.toFixed(2) : '-'));
    lines.push(`${runName(run).padEnd(labelWidth)}${cells[0].padStart(7)}${cells[1].padStart(7)}${cells[2].padStart(8)}`);
  }
  lines.push('```');
  for (const run of runs) {
    const changes = changesByRun.get(run);
    const nights = (run.history ?? []).length;
    if (changes.length === 0) {
      lines.push(`${runName(run)}: ${run.summary?.metrics ? (nights < 2 ? 'no history to compare' : succeeded(run.summary.metrics) ? 'nothing to compare' : 'no run succeeded, latency not compared') : `no results, step finished as \`${run.stepOutcome}\``}`);
      continue;
    }
    lines.push(`${runName(run)} vs ${nights} nights: ${changes.map((c) => `${c.label} ${formatDelta(c.deltaPct)}${c.flagged ? ` ${c.arrow}` : ''}`).join(' · ')}`);
  }
  if (runs.some((run) => run.benchmarkType === 'threads_search_metadata')) {
    lines.push('threads_search keeps its threads between nights on purpose, so its table grows.');
  }
  lines.push('', ...howToRead(runs, load));
  return lines.join('\n');
}

/**
 * Newest `summary_*.json`, or null when the run produced none.
 *
 * A missing summary is one of the outages this reporter exists to report, so
 * it must be a value here and never an exception.
 */
export function findLatestSummary(directory = HERE) {
  try {
    return (
      readdirSync(directory)
        .filter((name) => name.startsWith('summary_') && name.endsWith('.json'))
        .map((name) => path.join(directory, name))
        .sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0] ?? null
    );
  } catch {
    return null;
  }
}

/** Version of the checked-out api package, or null if it cannot be read. */
export function readApiVersion(file = path.join(HERE, '..', 'langgraph_api', '__init__.py')) {
  try {
    const match = readFileSync(file, 'utf8').match(/^__version__\s*=\s*"([^"]+)"/m);
    return match ? match[1] : null;
  } catch {
    return null;
  }
}

export function readSummary(file) {
  if (!file) return null;
  try {
    return JSON.parse(readFileSync(file, 'utf8'));
  } catch (error) {
    console.warn(`Could not read summary ${file}: ${error.message}`);
    return null;
  }
}

// Layout is actions/download-artifact without merge-multiple: one directory
// per artifact. report_context.json is written by the benchmark job.
export function collectRuns(resultsDir, historyDir) {
  const dirs = existsSync(resultsDir) ? readdirSync(resultsDir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name) : [];
  return RUNNERS.map((benchmarkType) => {
    const name = dirs.find((dir) => dir.includes(`-${benchmarkType}-`));
    const dir = name ? path.join(resultsDir, name) : null;
    const context = dir ? readSummary(path.join(dir, 'report_context.json')) ?? {} : {};
    return {
      benchmarkType,
      stepOutcome: context.stepOutcome ?? (dir ? 'unknown' : 'missing'),
      summary: dir ? readSummary(findLatestSummary(dir)) : null,
      load: { loadSize: context.loadSize, levels: context.levels, plateauDuration: context.plateauDuration },
      history: historyDir ? loadDailyHistory(historyDir, `-${benchmarkType}-`) : [],
    };
  });
}

function safeBuildDigest(runs, context) {
  try {
    return buildDigest(runs, context);
  } catch (error) {
    // The whole point of this file is that a bad night still gets reported.
    // If formatting itself fails, say so rather than failing the step.
    return {
      text: [
        `🔴 *Daily Benchmark${context.titleSuffix || ''}*`,
        `*Could not build the report:* ${error.message}`,
        `*Step outcomes:* ${runs.map((run) => `${runnerShortName(run.benchmarkType)} \`${run.stepOutcome}\``).join(' · ')}`,
        context.artifactUrl ? `<${context.artifactUrl}|Artifacts>` : '',
      ]
        .filter(Boolean)
        .join('\n'),
      thread: [],
    };
  }
}

async function main() {
  const runs = collectRuns(process.env.RESULTS_DIR || path.join(HERE, 'results'), process.env.HISTORY_DIR);
  const report = safeBuildDigest(runs, {
    titleSuffix: process.env.TITLE_SUFFIX || '',
    apiVersion: process.env.API_VERSION || readApiVersion(),
    goal: process.env.REPORT_GOAL || '',
    artifactUrl: process.env.ARTIFACT_URL,
    manual: process.env.MANUAL === 'true',
  });
  await postReport(report);
}

if (process.argv[1] && process.argv[1].endsWith('daily-report.js')) {
  main().catch((error) => {
    console.error(`Failed to post benchmark report: ${error.message}`);
    process.exit(1);
  });
}
