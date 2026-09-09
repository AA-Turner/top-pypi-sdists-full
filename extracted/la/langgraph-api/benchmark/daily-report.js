/*
 * Build and post the daily benchmark report.
 *
 * Replaces ~50 lines of bash that pasted values straight into a JSON string
 * literal, decided red/green from the success rate alone, and could not run at
 * all when there was no summary to read.
 *
 * The verdict is NOT recomputed here. k6 exits non-zero when a threshold is
 * crossed, so the step outcome already carries it; this reads that outcome and
 * explains it.
 */

import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve against this file, not the working directory, so the step does not
// have to be run from a particular place for the paths to line up.
const HERE = path.dirname(fileURLToPath(import.meta.url));

const GREEN = '🟢';
const RED = '🔴';

/**
 * A run must beat this success rate to be healthy, strictly. 99 exactly is not
 * enough, which is the bar the workflow's `SUCCESS_RATE > 99` already used and
 * is preserved here deliberately. The value matches staircase.py's
 * MIN_SUCCESS_RATE, the one such number in this repo with a recorded rationale.
 */
export const MIN_SUCCESS_RATE = 99;

/**
 * Every threshold k6 marked as crossed, as readable lines.
 *
 * Shape is `{ "<metric>": { "<expression>": { ok } } }`, verified against
 * k6 v2.2.0. Reading k6's own verdicts rather than re-deriving them means this
 * cannot drift from the thresholds actually configured in ramp.js.
 */
export function breaches(thresholds) {
  const lines = [];
  for (const [metric, expressions] of Object.entries(thresholds ?? {})) {
    for (const [expression, verdict] of Object.entries(expressions ?? {})) {
      if (verdict && verdict.ok === false) lines.push(`${metric} ${expression}`);
    }
  }
  return lines;
}

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

function seconds(value) {
  return isNumber(value) ? `${value.toFixed(2)}s` : 'n/a';
}

function percent(value) {
  return isNumber(value) ? `${value.toFixed(3)}%` : 'n/a';
}

function count(value) {
  return isNumber(value) ? String(value) : 'n/a';
}

export function buildMessage(context) {
  const {
    summary,
    stepOutcome,
    apiVersion,
    titleSuffix = '',
    benchmarkType,
    artifactName,
    artifactUrl,
    errorLogUrl,
    runTime,
  } = context;
  const metrics = summary?.metrics;
  const healthy = isHealthy({ stepOutcome, metrics });
  const lines = [
    `📊 *Daily Benchmark Results${titleSuffix} - ${benchmarkType}* ${healthy ? GREEN : RED}`,
    '',
    `*API Version*: ${apiVersion || 'unknown'}`,
    '',
  ];

  if (!metrics) {
    // The case the old bash could never report: `ls summary_*.json` failed
    // under `bash -e -o pipefail`, killing the step before anything was sent.
    lines.push(
      `*No results produced.* The benchmark step finished as \`${stepOutcome}\` without writing a summary.`,
      'Nothing was measured, so the numbers below are absent rather than good.'
    );
  } else {
    lines.push('*Performance Metrics:*');
    lines.push(`- *Total Runs*: ${count(metrics.totalRuns)}`);
    lines.push(`- *Success Rate*: ${percent(metrics.successRate)}`);
    lines.push(`- *Failed Runs*: ${count(metrics.failedRuns)}`);
    if (metrics.successfulRuns) {
      lines.push(`- *Avg Duration*: ${seconds(metrics.averageDuration)}`);
      lines.push(`- *P95 Duration*: ${seconds(metrics.p95Duration)}`);
      if (metrics.p95SuccessDuration != null) {
        lines.push(`- *P95 Duration (successes only)*: ${seconds(metrics.p95SuccessDuration)}`);
      }
    } else {
      // Failing instantly is fast. Printing sub-millisecond latency beside a red
      // emoji reads as a contradiction, so say why it is missing instead.
      lines.push('- *Duration*: not reported, no run succeeded');
    }

    const errorsByStatus = metrics.errors?.byStatus;
    if (
      errorsByStatus &&
      typeof errorsByStatus === 'object' &&
      Object.values(errorsByStatus).some((n) => n > 0)
    ) {
      const parts = Object.entries(errorsByStatus)
        .filter(([, n]) => n > 0)
        .map(([status, n]) => `${status}: ${n}`);
      lines.push(`- *HTTP failures*: ${parts.join(', ')}`);
    }
  }

  const crossed = breaches(summary?.thresholds);
  if (crossed.length > 0) {
    lines.push('', `*SLO breached:* ${crossed.join(' | ')}`);
  }
  if (stepOutcome !== 'success') {
    lines.push('', `*Benchmark step outcome:* \`${stepOutcome}\``);
  }

  lines.push('', `📁 *Download Results & Charts*: <${artifactUrl}|${artifactName}>`);
  if (errorLogUrl) lines.push('', `*Error Logs:* <${errorLogUrl}|deployment errors>`);
  lines.push('', `🕐 *Run Time*: ${runTime}`);
  return lines.join('\n');
}

/**
 * Newest `summary_*.json`, or null when the run produced none.
 *
 * This was `ls -t summary_*.json | head -1` in the workflow. Under the default
 * `bash -e -o pipefail` that assignment fails when the glob matches nothing,
 * which killed the step before it could report the very outage that caused it.
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

async function postSlack(message) {
  const token = process.env.SLACK_BOT_TOKEN;
  const channel = process.env.SLACK_CHANNEL;
  if (!token || !channel) {
    console.log('SLACK_BOT_TOKEN or SLACK_CHANNEL not set; printing instead of posting');
    console.log(message);
    return;
  }
  const response = await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ channel, text: message }),
  });
  // Slack rejects a bad payload with HTTP 200 and ok:false, so the status code
  // alone is not enough. The old `curl` checked neither and went green while
  // posting nothing.
  const result = await response.json().catch(() => ({}));
  if (!result.ok) {
    throw new Error(`Slack API error: ${result.error ?? `HTTP ${response.status}`}`);
  }
  console.log('Posted benchmark report to Slack');
}

function safeBuildMessage(context) {
  try {
    return buildMessage(context);
  } catch (error) {
    // The whole point of this file is that a bad night still gets reported.
    // If formatting itself fails, say so rather than failing the step.
    return [
      `📊 *Daily Benchmark Results${context.titleSuffix || ''} - ${context.benchmarkType}* ${RED}`,
      '',
      `*Could not build the report:* ${error.message}`,
      `*Benchmark step outcome:* \`${context.stepOutcome}\``,
      '',
      `📁 <${context.artifactUrl}|${context.artifactName}>`,
    ].join('\n');
  }
}

async function main() {
  const message = safeBuildMessage({
    summary: readSummary(process.env.SUMMARY_FILE || findLatestSummary()),
    stepOutcome: process.env.STEP_OUTCOME || 'unknown',
    apiVersion: process.env.API_VERSION || readApiVersion(),
    titleSuffix: process.env.TITLE_SUFFIX || '',
    benchmarkType: process.env.BENCHMARK_TYPE,
    artifactName: process.env.ARTIFACT_NAME,
    artifactUrl: process.env.ARTIFACT_URL,
    errorLogUrl: process.env.ERROR_LOG_URL,
    runTime: new Date().toISOString().replace('T', ' ').slice(0, 16) + ' UTC',
  });
  console.log(message);
  await postSlack(message);
}

if (process.argv[1] && process.argv[1].endsWith('daily-report.js')) {
  main().catch((error) => {
    console.error(`Failed to post benchmark report: ${error.message}`);
    process.exit(1);
  });
}
