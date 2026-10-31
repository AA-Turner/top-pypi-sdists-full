/**
 * Daily capacity benchmark orchestrator.
 *
 * Usage:
 *   DEPLOYMENT=daily-cap-benchmark-dedicated node capacity-ci.js
 *   node capacity-ci.js --all-deployments
 *   node capacity-ci.js --aggregate --summaries-dir ./artifacts --slack
 */

import { spawnSync } from "node:child_process";
import { readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  getDeploymentMetrics,
  pollDeploymentHealthy,
  requireApiKey,
  setResourceTiers,
} from "./host-v2.js";
import { RUNNERS } from "./daily-report.js";
import {
  MIN_HISTORY_NIGHTS,
  cellKey,
  flaggedChange,
  formatMove,
  loadCapacityHistory,
} from "./history.js";
import { runnerColumnName, runnerShortName } from "./runner-descriptions.js";
import { cellWindow, peakCpu, podRange, summarizeServerMetrics } from "./server-metrics.js";
import { dotFor, footer, postReport } from "./slack.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * @typedef {{startLoad?: string, stepSize?: string, numSteps?: string, warmupLoad?: string}} StaircaseGeometry
 * @type {Array<{slug: string, name: string, deploymentId: string, baseUrl: string, tiers: string[], staircase?: StaircaseGeometry}>}
 */
const CAPACITY_DEPLOYMENTS = [
  {
    slug: "daily-cap-benchmark-dedicated",
    name: "Dedicated",
    deploymentId: "22a22e9d-521e-4635-9bcb-a096a22820cc",
    baseUrl:
      "https://daily-cap-benchmark-dedicat-9669b63626045e0681f1f1fda08ef4ce.staging.langgraph.app",
    tiers: ["DEDICATED_L", "DEDICATED_M", "DEDICATED_S"],
    // Dedicated L serves about 450 runs/sec at most; 600 leaves the collapse
    // visible without spending steps far past it.
    staircase: { startLoad: "50", stepSize: "50", numSteps: "12", warmupLoad: "50" },
  },
  {
    slug: "daily-cap-benchmark-serverless",
    name: "Serverless",
    deploymentId: "becfa8bb-e2e3-4d96-8d08-3191b17c5d4d",
    baseUrl:
      "https://daily-cap-benchmark-serverl-b5dc9d9f7fa05990b279939863ae08de.staging.langgraph.app",
    tiers: ["SERVERLESS_L", "SERVERLESS_M", "SERVERLESS_S"],
    // Serverless tiers start at one queue pod of N_JOBS_PER_WORKER slots and a
    // 60s step never waits for a second, so their ceiling is a few dozen
    // runs/sec. The dedicated geometry starts above the range a step can pass.
    staircase: { startLoad: "10", stepSize: "5", numSteps: "13", warmupLoad: "20" },
  },
];

// Open model: a fixed arrival rate per step, so capacity reads directly as the
// service rate. Closed-model users back off as the server slows and flatter it.
const STAIRCASE_EXECUTOR = "constant-arrival-rate";
// Fallback geometry for a deployment without its own, in the executor's unit.
const STAIRCASE_START_LOAD = "50";
const STAIRCASE_STEP_SIZE = "50";
const STAIRCASE_NUM_STEPS = "12";
const STAIRCASE_PLATEAU_DURATION = "60";

const OPEN_MODEL = "constant-arrival-rate";

function executorOf(summaries) {
  return summaries.find((s) => s?.config?.k6Executor)?.config.k6Executor ?? OPEN_MODEL;
}

function unitFor(executor) {
  return executor === OPEN_MODEL ? "req/s" : "users";
}

/**
 * Parse a comma-separated allowlist from an env var.
 *
 * Returns null for unset/blank, meaning "no filtering". Scheduled runs leave
 * these empty, so the default path is unaffected.
 *
 * @param {string | undefined} raw
 * @returns {string[] | null}
 */
function parseFilter(raw) {
  if (!raw) return null;
  const values = raw
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
  return values.length > 0 ? values : null;
}

/**
 * Apply an allowlist, preserving `available` order so results stay comparable
 * across runs. Throws when the filter matches nothing, because silently running
 * zero cells looks identical to a healthy run that found no capacity.
 *
 * @param {string[]} available
 * @param {string[] | null} allowed
 * @param {string} label
 * @returns {string[]}
 */
function applyFilter(available, allowed, label) {
  if (!allowed) return available;
  const unknown = allowed.filter((value) => !available.includes(value));
  if (unknown.length > 0) {
    throw new Error(
      `Unknown ${label}: ${unknown.join(", ")}. Available: ${available.join(", ")}`,
    );
  }
  return available.filter((value) => allowed.includes(value));
}

function validateDeployment(deployment) {
  const missing = [];
  if (!deployment.slug) missing.push("slug");
  if (!deployment.deploymentId) missing.push("deploymentId");
  if (!deployment.baseUrl) missing.push("baseUrl");
  if (!deployment.tiers?.length) missing.push("tiers");
  if (missing.length > 0) {
    throw new Error(
      `Deployment ${deployment.slug || "<unknown>"} is missing required fields: ${missing.join(", ")}. ` +
        "Update CAPACITY_DEPLOYMENTS in capacity-ci.js.",
    );
  }
}

function getDeployment(slug, deployments = CAPACITY_DEPLOYMENTS) {
  const deployment = deployments.find((entry) => entry.slug === slug);
  if (!deployment) {
    const known = deployments.map((entry) => entry.slug).join(", ");
    throw new Error(
      `Unknown deployment ${JSON.stringify(slug)}. Known deployments: ${known}`,
    );
  }
  return deployment;
}

/** Normalise a thrown value to a message string. */
function errorMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

/**
 * Summary written for a cell that never produced one, so a crashed cell is
 * distinguishable from a cell that ran and found no capacity. Same shape as a
 * real summary, so every consumer can read it without special-casing.
 *
 * @param {{deploymentSlug: string, computeTier: string, benchmarkType: string}} cell
 * @param {unknown} error
 */
export function buildErrorSummary(cell, error) {
  return {
    capacity: null,
    maxThroughput: null,
    error: errorMessage(error),
    config: { ...cell },
    steps: [],
  };
}

function writeErrorSummary(summaryPath, cell, error) {
  writeFileSync(
    summaryPath,
    `${JSON.stringify(buildErrorSummary(cell, error), null, 2)}\n`,
  );
}

/**
 * Render one cell of the capacity table.
 *
 * `ERR` and `0` mean opposite things and must not collapse into the same
 * glyph: `ERR` is "we learned nothing", `0` is "this tier could not sustain
 * even the first step", which is a real and actionable result.
 */
export function capacityVus(summary) {
  if (!summary) return "-";
  if (summary.error) return "ERR";
  if (!summary.capacity) {
    const ceiling = summary.throughputCeiling?.successfulRunsPerSec;
    return ceiling == null ? "0" : `0 (~${Math.round(ceiling)}/s ceiling)`;
  }
  const vus = summary.capacity.targetVUs ?? "-";
  const perSec = summary.capacity.successfulRunsPerSec;
  return perSec == null ? String(vus) : `${vus} (${perSec}/s)`;
}

const BOTTLENECK_CPU_PCT = 95;
const COMPONENTS = [
  ["queue", "queue"],
  ["api", "api"],
  ["db", "database"],
  ["redis", "redis"],
];

function deploymentName(deployment) {
  return deployment.name ?? deployment.slug;
}

function tierLabel(deployment, tier) {
  const prefix = `${deploymentName(deployment).toUpperCase()}_`;
  return tier.startsWith(prefix) ? tier.slice(prefix.length) : tier;
}

function cellName(deployment, tier, runner) {
  return `${deploymentName(deployment)} ${tierLabel(deployment, tier)} ${runnerColumnName(runner)}`;
}

function indexCells(deployments, summaries) {
  /** @type {Record<string, Record<string, Record<string, object>>>} */
  const byDeployment = Object.fromEntries(deployments.map((d) => [d.slug, {}]));
  for (const summary of summaries) {
    const { deploymentSlug, computeTier, benchmarkType } = summary.config ?? {};
    if (deploymentSlug && computeTier && benchmarkType) {
      byDeployment[deploymentSlug] ??= {};
      byDeployment[deploymentSlug][computeTier] ??= {};
      byDeployment[deploymentSlug][computeTier][benchmarkType] = summary;
    }
  }
  return byDeployment;
}

function pastNights(deployment, tier, runner, summary, history) {
  const executor = summary?.config?.k6Executor ?? "constant-vus";
  // Nights measured in users and nights measured in req/s are different
  // scales; only the same executor is a baseline.
  return (history[cellKey({ deploymentSlug: deployment.slug, computeTier: tier, benchmarkType: runner })] ?? [])
    .filter((night) => (night.executor ?? "constant-vus") === executor)
    .map((night) => night.capacityVUs);
}

function analyseDeployment(deployment, cells, history) {
  const rows = [];
  let nights = 0;
  for (const tier of deployment.tiers) {
    for (const runner of RUNNERS) {
      const summary = cells[tier]?.[runner];
      const past = summary && !summary.error ? pastNights(deployment, tier, runner, summary, history) : [];
      nights = Math.max(nights, past.length);
      const change =
        summary && !summary.error
          ? flaggedChange(summary.capacity?.targetVUs ?? 0, past, { higherIsBetter: true })
          : null;
      rows.push({
        deployment,
        tier,
        runner,
        summary,
        change,
        hot: hotComponents(summary),
      });
    }
  }
  return { rows, nights };
}

function hotComponents(summary) {
  const groups = summary?.serverMetricsAtCapacity?.groups ?? {};
  return COMPONENTS.flatMap(([label, name]) => {
    const cpu = peakCpu(groups[label]);
    return cpu != null && cpu >= BOTTLENECK_CPU_PCT ? [{ name, cpu: Math.round(cpu) }] : [];
  });
}

function bottleneckLines(rows) {
  const groups = new Map();
  for (const row of rows) {
    for (const { name, cpu } of row.hot) {
      const key = `${row.deployment.slug}|${name}`;
      const group = groups.get(key) ?? { deployment: row.deployment, name, tiers: new Set(), cpus: [] };
      group.tiers.add(tierLabel(row.deployment, row.tier));
      group.cpus.push(cpu);
      groups.set(key, group);
    }
  }
  const order = (group) => COMPONENTS.findIndex(([, name]) => name === group.name);
  return [...groups.values()].sort((a, b) => order(a) - order(b)).map(({ deployment, name, tiers, cpus }) => {
    const low = Math.min(...cpus);
    const high = Math.max(...cpus);
    const range = low === high ? `${high}%` : `${low} to ${high}%`;
    return `${deploymentName(deployment)} ${[...tiers].join(", ")}: ${name} at ${range}`;
  });
}

function crashedTiers(rows) {
  const byTier = new Map();
  for (const row of rows) {
    if (!row.summary?.error) continue;
    const key = `${row.deployment.slug}|${row.tier}`;
    (byTier.get(key) ?? byTier.set(key, { row, runners: [] }).get(key)).runners.push(row.runner);
  }
  return [...byTier.values()].map(({ row, runners }) => {
    const where = `${deploymentName(row.deployment)} ${tierLabel(row.deployment, row.tier)}`;
    const detail = runners.length === RUNNERS.length
      ? `${where}, all ${RUNNERS.length} tests (ERR)`
      : `${where} ${runners.map(runnerColumnName).join(", ")} (ERR)`;
    return { where, detail };
  });
}

function moveLine(row, unit) {
  const now = row.summary.capacity?.targetVUs ?? 0;
  return `${cellName(row.deployment, row.tier, row.runner)} ${formatMove(Math.round(row.change.median), now, row.change.deltaPct, unit)}`;
}

export function capacityCell(summary) {
  if (!summary) return "-";
  if (summary.error) return "ERR";
  const vus = String(summary.capacity?.targetVUs ?? 0);
  // Passing the last step says only that the server is at least this fast.
  const lastStep = summary.config?.numSteps;
  return lastStep != null && summary.capacity?.step === lastStep ? `${vus}+` : vus;
}

function plural(n, word) {
  return `${n} ${word}${n === 1 ? "" : "s"}`;
}

function capacityTable(deployment, rows, unit) {
  const labels = deployment.tiers.map((tier) => tierLabel(deployment, tier));
  const labelWidth = Math.max(2, ...labels.map((l) => l.length)) + 1;
  const column = (text, arrow = " ") => `${text.padStart(6)}${arrow}`;
  const lines = [
    `*${deploymentName(deployment)}* · ${unit} at SLO`,
    "```",
    `${"".padEnd(labelWidth)}${RUNNERS.map((r) => column(runnerColumnName(r))).join("")}`,
  ];
  for (const tier of deployment.tiers) {
    const cells = rows.filter((row) => row.tier === tier);
    lines.push(
      `${tierLabel(deployment, tier).padEnd(labelWidth)}${cells.map((row) => column(capacityCell(row.summary), row.change?.arrow)).join("")}`,
    );
  }
  lines.push("```");
  return lines;
}

export function formatAggregateTable(
  deployments,
  summaries,
  warnings = [],
  now = new Date(),
  history = {},
  apiVersion = null,
  manual = false,
) {
  const byDeployment = indexCells(deployments, summaries);
  const analysed = deployments.map((deployment) => ({
    deployment,
    ...analyseDeployment(deployment, byDeployment[deployment.slug] ?? {}, history),
  }));
  const rows = analysed.flatMap((a) => a.rows);

  const expected = rows.length;
  const failed = rows.filter((row) => row.summary?.error).length;
  const missing = rows.filter((row) => !row.summary).length;
  const jobFailed = process.env.CAPACITY_JOB_RESULT === "failure";
  const regressed = rows.filter((row) => row.change && !row.change.better);
  const improved = rows.filter((row) => row.change?.better);
  const bottlenecks = bottleneckLines(rows);
  const allWarnings = [...warnings, ...toolOverheadWarnings(summaries)];

  const executor = executorOf(summaries);
  const unit = unitFor(executor);
  const date = now.toLocaleDateString("en-US", { month: "short", day: "numeric", timeZone: "UTC" });
  const ran = failed + missing === 0 ? `all ${expected} cells ran` : `${expected - failed - missing} of ${expected} cells ran`;
  const verdict = [];
  const crashed = crashedTiers(rows);
  if (crashed.length > 0) verdict.push(`${crashed.map((tier) => tier.where).join(", ")} crashed`);
  if (missing > 0) verdict.push(`${missing} never ran`);
  if (jobFailed) verdict.push("job failed");
  if (regressed.length > 0) verdict.push(plural(regressed.length, "regression"));
  if (improved.length > 0) verdict.push(plural(improved.length, "improvement"));
  if (bottlenecks.length > 0) verdict.push(plural(bottlenecks.length, "bottleneck"));
  if (verdict.length === 0) verdict.push("all quiet");

  const dot = dotFor({
    failed: failed + missing > 0 || jobFailed,
    attention: regressed.length + bottlenecks.length + allWarnings.length > 0,
  });
  const lines = [
    `${dot} *Capacity · ${date}*${manual ? " · manual run" : ""}${apiVersion ? ` · API ${apiVersion}` : ""} · ${ran} · ${verdict.join(", ")}`,
  ];

  const failedParts = crashed.map((tier) => tier.detail);
  for (const row of rows) {
    if (!row.summary) failedParts.push(`${cellName(row.deployment, row.tier, row.runner)} never ran`);
  }
  if (jobFailed) failedParts.push("the capacity job exited with failure");
  if (failedParts.length > 0) {
    lines.push(`*Failed:* ${failedParts.join(" · ")} · treat the table as incomplete`);
  }
  // hostRequest appends the response body, which can span lines; the detail is often on a later one.
  const reasons = new Set(rows.map((row) => row.summary?.error?.replace(/\s+/g, " ").trim()).filter(Boolean));
  if (reasons.size > 0) lines.push(`*Why:* ${[...reasons].join(" · ")}`);
  if (regressed.length > 0) lines.push(`*Regressed:* ${regressed.map((row) => moveLine(row, unit)).join(" · ")}`);
  if (bottlenecks.length > 0) lines.push(`*Bottlenecks:* ${bottlenecks.join(" · ")}`);
  for (const warning of allWarnings) lines.push(`:warning: ${warning}`);

  for (const { deployment, rows: deploymentRows, nights } of analysed) {
    lines.push("", ...capacityTable(deployment, deploymentRows, unitFor(executorOf(deploymentRows.map((r) => r.summary).filter(Boolean)))));
    if (nights < MIN_HISTORY_NIGHTS) {
      lines.push(`_${nights} of ${MIN_HISTORY_NIGHTS} nights of history, no change flags yet_`);
    }
  }
  return lines.join("\n");
}

export function formatImprovements(deployments, summaries, history = {}) {
  const byDeployment = indexCells(deployments, summaries);
  const rows = deployments.flatMap((d) => analyseDeployment(d, byDeployment[d.slug] ?? {}, history).rows);
  const unit = unitFor(executorOf(summaries));
  const improved = rows.filter((row) => row.change?.better);
  return improved.length > 0 ? `*Improved:* ${improved.map((row) => moveLine(row, unit)).join(" · ")}` : null;
}

function servedRate(summary) {
  const rate = summary?.capacity?.successfulRunsPerSec;
  if (rate != null) return String(Math.round(rate));
  const ceiling = summary?.throughputCeiling?.successfulRunsPerSec;
  return ceiling != null ? `0 (ceiling ${Math.round(ceiling)})` : "-";
}

function serverColumns(summaries, kind) {
  const has = kind === "pods" ? podRange : (g) => peakCpu(g) != null;
  return COMPONENTS.map(([label]) => label).filter((label) =>
    summaries.some((s) => {
      const group = s?.serverMetrics?.groups?.[label];
      return group && has(group);
    }),
  );
}

function serverCell(summary, label, kind) {
  const group = summary?.serverMetrics?.groups?.[label];
  if (kind === "pods") {
    const range = podRange(group);
    return range ? `${range.min}→${range.max}` : "-";
  }
  const cpu = peakCpu(group);
  return cpu != null ? String(Math.round(cpu)) : "-";
}

// Tier rows head their runners so each line fits PHONE_WIDTH; a "L search" label column would not.
function serverTable(deployment, cells, kind) {
  const present = deployment.tiers.flatMap((tier) => RUNNERS.map((r) => cells[tier]?.[r]).filter((s) => s?.serverMetrics));
  const columns = serverColumns(present, kind);
  if (columns.length === 0) return null;
  const labelWidth = Math.max(...RUNNERS.map((r) => runnerColumnName(r).length)) + 1;
  const widths = columns.map((label) =>
    Math.max(label.length, ...present.map((s) => serverCell(s, label, kind).length)) + 1,
  );
  const lines = ["```", `${"".padEnd(labelWidth)}${columns.map((label, i) => label.padStart(widths[i])).join("")}`];
  for (const tier of deployment.tiers) {
    const runners = RUNNERS.filter((r) => cells[tier]?.[r]?.serverMetrics);
    if (runners.length === 0) continue;
    lines.push(tierLabel(deployment, tier));
    for (const runner of runners) {
      const row = columns.map((label, i) => serverCell(cells[tier][runner], label, kind).padStart(widths[i]));
      lines.push(`${` ${runnerColumnName(runner)}`.padEnd(labelWidth)}${row.join("")}`);
    }
  }
  lines.push("```");
  return lines.join("\n");
}

export function formatServerView(deployments, summaries) {
  const byDeployment = indexCells(deployments, summaries);
  const blocks = [];
  for (const deployment of deployments) {
    const cells = byDeployment[deployment.slug] ?? {};
    const present = Object.values(cells).flatMap((byRunner) => Object.values(byRunner));
    if (present.length === 0) continue;
    const served = deployment.tiers
      .map((tier) => `${tierLabel(deployment, tier)} ${RUNNERS.map((r) => servedRate(cells[tier]?.[r])).join(" / ")}`)
      .join(" · ");
    const servedLine = `Runs/sec actually served at the top step, as ${RUNNERS.map(runnerColumnName).join(" / ")}: ${served}`;
    // The served rate is k6's; the pod and CPU tables are the dashboard's, which is best effort.
    const cpu = serverTable(deployment, cells, "cpu");
    const pods = serverTable(deployment, cells, "pods");
    blocks.push(
      [
        `*${deploymentName(deployment)}*`,
        cpu ? `_CPU, % of request_\n${cpu}` : null,
        pods ? `_Pods, start → end_\n${pods}` : null,
        servedLine,
      ]
        .filter(Boolean)
        .join("\n"),
    );
  }
  if (blocks.length === 0) return null;
  return [
    "*Pods and CPU per cell*, peak over the whole cell including the steps that failed. CPU over 100 means bursting above the pod's request.",
    ...blocks,
  ].join("\n\n");
}

function toolOverheadWarnings(summaries) {
  const lines = [];
  for (const summary of summaries) {
    const config = summary?.config ?? {};
    const step = (summary?.steps ?? []).find(
      (s) => s?.clientOverheadMs?.med && s?.medDurationMs && s.clientOverheadMs.med > 0.1 * s.medDurationMs,
    );
    if (step) {
      lines.push(
        `${config.computeTier} ${runnerShortName(config.benchmarkType)}: the test tool spent ${step.clientOverheadMs.med}ms per iteration outside requests at step ${step.step} (${Math.round((step.clientOverheadMs.med / step.medDurationMs) * 100)}% of a ${step.medDurationMs}ms median)`,
      );
    }
  }
  return lines;
}

function warningsPathFor(deploymentSlug) {
  return path.join(__dirname, `staircase_warnings_${deploymentSlug}.json`);
}

/** Read warnings written alongside the summaries, so the report can show them. */
export function collectWarnings(directory) {
  return readdirSync(directory)
    .filter(
      (name) => name.startsWith("staircase_warnings_") && name.endsWith(".json"),
    )
    .sort()
    .flatMap((name) => {
      try {
        return JSON.parse(readFileSync(path.join(directory, name), "utf8"));
      } catch {
        return [];
      }
    });
}

function summaryPathFor(deploymentSlug, tier, runner) {
  const safeTier = tier.replaceAll("/", "-");
  return path.join(
    __dirname,
    `staircase_summary_${deploymentSlug}_${safeTier}_${runner}.json`,
  );
}

function runCommand(command, args, env) {
  const result = spawnSync(command, args, {
    cwd: __dirname,
    env: { ...process.env, ...env },
    stdio: "inherit",
  });
  if (result.status !== 0) {
    throw new Error(
      `${command} ${args.join(" ")} failed with exit code ${result.status}`,
    );
  }
}

function ensureBuild() {
  runCommand("npm", ["run", "build"], {});
}

function runReset(baseUrl, apiKey) {
  runCommand("node", ["clean-cli.js"], {
    BASE_URL: baseUrl,
    LANGSMITH_API_KEY: apiKey,
  });
}

function runStaircase({
  baseUrl,
  apiKey,
  runner,
  deploymentSlug,
  computeTier,
  summaryPath,
  geometry = {},
  overrides = {},
}) {
  runCommand(process.env.PYTHON || "python3", ["staircase.py"], {
    BASE_URL: baseUrl,
    LANGSMITH_API_KEY: apiKey,
    BENCHMARK_TYPE: runner,
    DEPLOYMENT_SLUG: deploymentSlug,
    COMPUTE_TIER: computeTier,
    SUMMARY_PATH: summaryPath,
    // `||` rather than `??`: workflow_dispatch passes "" on scheduled runs, and
    // staircase.py int()s these, so an empty string must not reach it.
    K6_EXECUTOR: process.env.K6_EXECUTOR || STAIRCASE_EXECUTOR,
    START_LOAD:
      process.env.START_LOAD || geometry.startLoad || STAIRCASE_START_LOAD,
    STEP_SIZE: process.env.STEP_SIZE || geometry.stepSize || STAIRCASE_STEP_SIZE,
    NUM_STEPS: process.env.NUM_STEPS || geometry.numSteps || STAIRCASE_NUM_STEPS,
    PLATEAU_DURATION:
      process.env.PLATEAU_DURATION || STAIRCASE_PLATEAU_DURATION,
    // The staircase grows the thread table *while* load ramps, so a slower step
    // cannot be attributed to load or to table size. The ramp benchmark leaves
    // this off, because there the growth is the thing under test.
    DELETE_THREADS: "1",
    ...overrides,
  });
}

/**
 * Drive a short, low load at the deployment and throw the result away.
 *
 * A tier change leaves connection pools cold and caches empty, and without this
 * the first cell of the matrix absorbs that. WARMUP_ITERS is per VU and far too
 * small to cover it.
 */
function runWarmup(deployment, apiKey, tier, runner) {
  const summaryPath = path.join(
    __dirname,
    `staircase_warmup_${deployment.slug}_${tier}.json`,
  );
  console.log(`\n>> ${deployment.slug} / ${tier} / warm-up (discarded)`);
  runStaircase({
    baseUrl: deployment.baseUrl,
    apiKey,
    runner,
    deploymentSlug: deployment.slug,
    computeTier: tier,
    summaryPath,
    geometry: deployment.staircase,
    overrides: {
      NUM_STEPS: "1",
      START_LOAD: process.env.WARMUP_LOAD || deployment.staircase?.warmupLoad || "50",
      PLATEAU_DURATION: process.env.WARMUP_DURATION || "60",
      COOLDOWN_DURATION: "0",
    },
  });
  rmSync(summaryPath, { force: true });
}

/**
 * Wait for the deployment to be healthy again before the next cell measures it.
 *
 * Cells run back to back on one deployment and a staircase ends by overloading
 * it, so without this the next cell measures the previous cell's damage.
 */
async function awaitRecovery(deployment, apiKey, tier, runner) {
  try {
    await pollDeploymentHealthy(deployment.baseUrl, apiKey, { checkDb: true });
  } catch (error) {
    throw new Error(
      `${tier} / ${runner}: deployment did not recover from the previous cell: ${error.message}`,
    );
  }
}

function printDeploymentTable(deployment, tiers, runners, summaryPaths) {
  /** @type {Record<string, Record<string, object>>} */
  const byKey = {};
  for (const summaryPath of summaryPaths) {
    // Tolerate an unreadable summary. This runs at the very end of a job that
    // takes over an hour, and losing the console table (plus the exit-code
    // reporting after it) because one file is malformed is a bad trade. The
    // artifacts are uploaded regardless.
    try {
      const summary = JSON.parse(readFileSync(summaryPath, "utf8"));
      const config = summary.config ?? {};
      byKey[`${config.computeTier}:${config.benchmarkType}`] = summary;
    } catch (error) {
      console.warn(`Could not read ${summaryPath}: ${error.message}`);
    }
  }

  const header =
    "tier".padEnd(16) +
    runners.map((runner) => runnerShortName(runner).padEnd(20)).join("");
  console.log(
    `\nCapacity results - ${deployment.slug} (max VUs @ SLO, runs/sec there)\n${header}`,
  );
  for (const tier of tiers) {
    let row = tier.padEnd(16);
    for (const runner of runners) {
      const summary = byKey[`${tier}:${runner}`];
      row += capacityVus(summary).padEnd(20);
    }
    console.log(row);
  }
}

async function runDeploymentMatrix(deployment, apiKey) {
  console.log(
    `\n${"=".repeat(80)}\nCapacity matrix: ${deployment.slug}\n${"=".repeat(80)}`,
  );
  validateDeployment(deployment);

  const tiers = applyFilter(
    deployment.tiers,
    parseFilter(process.env.TIERS),
    `tier for ${deployment.slug}`,
  );
  const runners = applyFilter(
    RUNNERS,
    parseFilter(process.env.RUNNERS),
    "runner",
  );
  if (
    tiers.length !== deployment.tiers.length ||
    runners.length !== RUNNERS.length
  ) {
    console.log(`Filtered to tiers [${tiers}] and runners [${runners}]`);
  }

  /** @type {string[]} */
  const summaryPaths = [];
  /** @type {Array<{tier: string, runner: string, message: string}>} */
  const failures = [];
  /** @type {string[]} */
  const warnings = [];
  const recordWarning = (message) => {
    console.warn(message);
    warnings.push(`${deployment.slug}: ${message}`);
  };

  const recordFailure = (tier, runner, error) => {
    const summaryPath = summaryPathFor(deployment.slug, tier, runner);
    const cell = {
      deploymentSlug: deployment.slug,
      computeTier: tier,
      benchmarkType: runner,
    };
    writeErrorSummary(summaryPath, cell, error);
    failures.push({ tier, runner, message: errorMessage(error) });
    return summaryPath;
  };

  for (const tier of tiers) {
    console.log(`\n--- Tier ${tier} ---`);
    // Clear leftovers on the outgoing tier, before the resize, so the delete
    // load does not land on the tier we are about to measure.
    try {
      runReset(deployment.baseUrl, apiKey);
    } catch (error) {
      recordWarning(`pre-resize reset failed: ${error.message}`);
    }

    try {
      const databaseTier = tier.startsWith("DEDICATED_") ? tier : undefined;
      await setResourceTiers(
        deployment.deploymentId,
        tier,
        databaseTier,
        apiKey,
        deployment.baseUrl,
      );
    } catch (error) {
      // A tier that will not resize costs us that tier, not the whole
      // deployment.
      console.error(`Tier ${tier} unavailable: ${error.message}`);
      for (const runner of runners) {
        summaryPaths.push(recordFailure(tier, runner, error));
      }
      continue;
    }

    try {
      runWarmup(deployment, apiKey, tier, runners[0]);
    } catch (error) {
      // A warm-up that will not run is a symptom, not the measurement. Log it
      // and let the cells below record the real failure with their own context.
      recordWarning(`warm-up for ${tier} failed: ${error.message}`);
    }

    for (const [cellIndex, runner] of runners.entries()) {
      console.log(`\n>> ${deployment.slug} / ${tier} / ${runner}`);
      const summaryPath = summaryPathFor(deployment.slug, tier, runner);
      try {
        // The first cell of a tier does not need a recovery wait: the tier
        // switch already established sustained health and the warm-up ran
        // straight after it. Waiting again would burn a health window per tier
        // for nothing.
        if (cellIndex > 0) {
          await awaitRecovery(deployment, apiKey, tier, runner);
        }
        runReset(deployment.baseUrl, apiKey);
        runStaircase({
          baseUrl: deployment.baseUrl,
          apiKey,
          runner,
          deploymentSlug: deployment.slug,
          computeTier: tier,
          summaryPath,
          geometry: deployment.staircase,
        });
        summaryPaths.push(summaryPath);
        try {
          await attachServerMetrics(deployment, apiKey, summaryPath);
        } catch (error) {
          // The capacity number stands on its own; the server view is context.
          recordWarning(`server metrics unavailable for ${tier} / ${runner}: ${error.message}`);
        }
      } catch (error) {
        console.error(`Cell ${tier} / ${runner} failed: ${error.message}`);
        summaryPaths.push(recordFailure(tier, runner, error));
      }
    }
  }

  printDeploymentTable(deployment, tiers, runners, summaryPaths);
  if (warnings.length > 0) {
    // Persisted next to the summaries so the aggregate can surface them in the
    // posted report; a warning that only exists in the job log is invisible.
    writeFileSync(
      warningsPathFor(deployment.slug),
      `${JSON.stringify(warnings, null, 2)}\n`,
    );
  }
  return { summaryPaths, failures, warnings };
}

// The steps past capacity saturate everything, so a bottleneck read over the
// whole cell names a component the tier never hit while it was passing.
async function attachServerMetrics(deployment, apiKey, summaryPath) {
  const summary = JSON.parse(readFileSync(summaryPath, "utf8"));
  const window = cellWindow(summary.steps);
  if (!window) throw new Error("steps carry no timestamps");
  summary.serverMetrics = summarizeServerMetrics(
    await getDeploymentMetrics(deployment.deploymentId, apiKey, window),
  );
  const capacityStep = summary.capacity?.step;
  const held = capacityStep ? cellWindow(summary.steps.filter((s) => s.step <= capacityStep)) : null;
  summary.serverMetricsAtCapacity = held
    ? summarizeServerMetrics(await getDeploymentMetrics(deployment.deploymentId, apiKey, held))
    : null;
  writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);
}

function collectSummaries(directory) {
  const paths = readdirSync(directory)
    .filter(
      (name) => name.startsWith("staircase_summary_") && name.endsWith(".json"),
    )
    .sort()
    .map((name) => path.join(directory, name));
  if (paths.length === 0) {
    throw new Error(`No staircase_summary_*.json files found in ${directory}`);
  }
  return paths.map((summaryPath) =>
    JSON.parse(readFileSync(summaryPath, "utf8")),
  );
}

/** The checked-out repo is usually ahead of staging, so the version comes from the deployments. */
export async function deployedVersion(deployments, fetchImpl = fetch) {
  const versions = await Promise.all(
    deployments.map(async ({ baseUrl }) => {
      try {
        const response = await fetchImpl(`${baseUrl}/info`, { signal: AbortSignal.timeout(15000) });
        return response.ok ? ((await response.json())?.version ?? null) : null;
      } catch {
        return null;
      }
    }),
  );
  const known = [...new Set(versions.filter(Boolean))];
  return known.length > 0 ? known.join("/") : null;
}

async function runAggregate(summariesDir, { postToSlack, historyDir }) {
  const summaries = collectSummaries(summariesDir);
  const warnings = collectWarnings(summariesDir);
  const history = historyDir ? loadCapacityHistory(historyDir) : {};
  let text = formatAggregateTable(
    CAPACITY_DEPLOYMENTS,
    summaries,
    warnings,
    new Date(),
    history,
    await deployedVersion(CAPACITY_DEPLOYMENTS),
    process.env.MANUAL === "true",
  );
  text += `\n\n${footer("capacity", process.env.GITHUB_RUN_URL)}`;
  const thread = [
    [formatImprovements(CAPACITY_DEPLOYMENTS, summaries, history), formatServerView(CAPACITY_DEPLOYMENTS, summaries)].filter(Boolean).join("\n\n"),
  ];
  if (postToSlack) {
    await postReport({ text, thread });
  } else {
    for (const part of [text, ...thread]) console.log(`${part}\n`);
  }
}

function parseArgs(argv) {
  return {
    allDeployments: argv.includes("--all-deployments"),
    aggregate: argv.includes("--aggregate"),
    slack: argv.includes("--slack"),
    summariesDir:
      argv.includes("--summaries-dir") &&
      argv[argv.indexOf("--summaries-dir") + 1]
        ? path.resolve(argv[argv.indexOf("--summaries-dir") + 1])
        : __dirname,
    historyDir:
      argv.includes("--history-dir") && argv[argv.indexOf("--history-dir") + 1]
        ? path.resolve(argv[argv.indexOf("--history-dir") + 1])
        : null,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.aggregate) {
    await runAggregate(args.summariesDir, {
      postToSlack: args.slack,
      historyDir: args.historyDir,
    });
    return;
  }

  const apiKey = requireApiKey();
  /** @type {Array<{tier: string, runner: string, message: string}>} */
  const failures = [];
  /** @type {string[]} */
  const warnings = [];

  if (args.allDeployments) {
    ensureBuild();
    for (const deployment of CAPACITY_DEPLOYMENTS) {
      const result = await runDeploymentMatrix(deployment, apiKey);
      failures.push(...result.failures);
      warnings.push(...result.warnings);
    }
    reportWarnings(warnings);
    reportFailures(failures);
    return;
  }

  const slug = process.env.DEPLOYMENT;
  if (!slug) {
    console.error(
      "Set DEPLOYMENT to a slug from CAPACITY_DEPLOYMENTS in capacity-ci.js, or pass --all-deployments",
    );
    process.exit(1);
  }

  ensureBuild();
  const result = await runDeploymentMatrix(getDeployment(slug), apiKey);
  reportWarnings(result.warnings);
  reportFailures(result.failures);
}

/**
 * Fail the job when any cell failed, but only after every other cell has had
 * its turn. Uses exitCode rather than exit() so buffered stdout still flushes.
 */
function reportWarnings(warnings) {
  if (warnings.length === 0) return;
  console.warn(`\n${warnings.length} warning(s):`);
  for (const warning of warnings) {
    console.warn(`  ${warning}`);
  }
}

function reportFailures(failures) {
  if (failures.length === 0) return;
  console.error(`\n${failures.length} cell(s) failed:`);
  for (const failure of failures) {
    console.error(`  ${failure.tier} / ${failure.runner}: ${failure.message}`);
  }
  process.exitCode = 1;
}

const isMain =
  process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main().catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}
