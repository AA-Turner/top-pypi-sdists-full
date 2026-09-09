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
  pollDeploymentHealthy,
  requireApiKey,
  setResourceTiers,
} from "./host-v2.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {Array<{slug: string, deploymentId: string, baseUrl: string, tiers: string[]}>} */
const CAPACITY_DEPLOYMENTS = [
  {
    slug: "daily-cap-benchmark-dedicated",
    deploymentId: "22a22e9d-521e-4635-9bcb-a096a22820cc",
    baseUrl:
      "https://daily-cap-benchmark-dedicat-9669b63626045e0681f1f1fda08ef4ce.staging.langgraph.app",
    tiers: ["DEDICATED_L", "DEDICATED_M", "DEDICATED_S"],
  },
  {
    slug: "daily-cap-benchmark-serverless",
    deploymentId: "becfa8bb-e2e3-4d96-8d08-3191b17c5d4d",
    baseUrl:
      "https://daily-cap-benchmark-serverl-b5dc9d9f7fa05990b279939863ae08de.staging.langgraph.app",
    tiers: ["SERVERLESS_L", "SERVERLESS_M", "SERVERLESS_S"],
  },
];

const RUNNERS = ["wait_write", "stream_write", "threads_search_metadata"];

const RUNNER_LABELS = {
  wait_write: "wait_write",
  stream_write: "stream_write",
  threads_search_metadata: "threads_search",
};

// 200 + 100 * (19 - 1) = 2000 VUs
const STAIRCASE_START_LOAD = "200";
const STAIRCASE_STEP_SIZE = "100";
const STAIRCASE_NUM_STEPS = "19";
const STAIRCASE_PLATEAU_DURATION = "60";

// Mirrors staircase.py's SLO defaults, for the report header only. Kept here
// rather than parsed out of a summary so the header still renders when every
// cell failed and there is no config to read.
const SLO = { minSuccessRate: 99, maxP50Ms: 3000, maxP95Ms: 10000 };

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
  if (!summary.capacity) return "0";
  const vus = summary.capacity.targetVUs ?? "-";
  const perSec = summary.capacity.successfulRunsPerSec;
  return perSec == null ? String(vus) : `${vus} (${perSec}/s)`;
}

export function formatAggregateTable(deployments, summaries, warnings = []) {
  /** @type {Record<string, Record<string, Record<string, object>>>} */
  const byDeployment = Object.fromEntries(deployments.map((d) => [d.slug, {}]));

  for (const summary of summaries) {
    const config = summary.config ?? {};
    const { deploymentSlug, computeTier, benchmarkType } = config;
    if (deploymentSlug && computeTier && benchmarkType) {
      byDeployment[deploymentSlug] ??= {};
      byDeployment[deploymentSlug][computeTier] ??= {};
      byDeployment[deploymentSlug][computeTier][benchmarkType] = summary;
    }
  }

  // Say what "capacity" means in the message: a bare number cannot tell the
  // reader what bar was cleared, nor that `default` is a trivial graph.
  const lines = [
    "*Daily Capacity Benchmark*",
    `Max load sustained at SLO (success >= ${SLO.minSuccessRate}%, p50 <= ${SLO.maxP50Ms / 1000}s, p95 <= ${SLO.maxP95Ms / 1000}s), with runs/sec there.`,
    "Profile `default`: 1 step, no LLM, 1KB checkpoint. Server overhead, not a customer workload.",
  ];

  // Say out loud when the run was not clean. Without this a run where half the
  // matrix never executed posts a tidy-looking table and reads as authoritative.
  const expected = deployments.reduce(
    (total, deployment) => total + deployment.tiers.length * RUNNERS.length,
    0,
  );
  const failed = summaries.filter((summary) => summary.error).length;
  const missing = expected - summaries.length;
  const problems = [];
  if (failed > 0) problems.push(`${failed} failed`);
  if (missing > 0) problems.push(`${missing} never ran`);
  if (process.env.CAPACITY_JOB_RESULT === "failure") {
    problems.push("the capacity job itself failed");
  }
  if (problems.length > 0) {
    lines.push(
      `:warning: ${problems.join(", ")} of ${expected} cells - treat this table as incomplete`,
    );
  }
  for (const warning of warnings) {
    lines.push(`:warning: ${warning}`);
  }
  lines.push("");
  for (const deployment of deployments) {
    lines.push(`*${deployment.slug}*`);
    lines.push(
      `${"".padEnd(16)}${RUNNERS.map((runner) => RUNNER_LABELS[runner].padEnd(18)).join("")}`,
    );
    for (const tier of deployment.tiers) {
      let row = tier.padEnd(16);
      for (const runner of RUNNERS) {
        const summary = byDeployment[deployment.slug]?.[tier]?.[runner];
        row += capacityVus(summary).padEnd(18);
      }
      lines.push(row);
    }
    lines.push("");
  }
  return lines.join("\n").trimEnd();
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
    START_LOAD: process.env.START_LOAD || STAIRCASE_START_LOAD,
    STEP_SIZE: process.env.STEP_SIZE || STAIRCASE_STEP_SIZE,
    NUM_STEPS: process.env.NUM_STEPS || STAIRCASE_NUM_STEPS,
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
    overrides: {
      NUM_STEPS: "1",
      START_LOAD: process.env.WARMUP_LOAD || "50",
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
    runners.map((runner) => RUNNER_LABELS[runner].padEnd(18)).join("");
  console.log(
    `\nCapacity results - ${deployment.slug} (max VUs @ SLO, runs/sec there)\n${header}`,
  );
  for (const tier of tiers) {
    let row = tier.padEnd(16);
    for (const runner of runners) {
      const summary = byKey[`${tier}:${runner}`];
      row += capacityVus(summary).padEnd(18);
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
        });
        summaryPaths.push(summaryPath);
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

async function postSlack(message) {
  const token = process.env.SLACK_BOT_TOKEN;
  const channel = process.env.SLACK_CHANNEL;
  if (!token || !channel) {
    console.log(
      "SLACK_BOT_TOKEN or SLACK_CHANNEL not set; skipping Slack post",
    );
    console.log(message);
    return;
  }

  const response = await fetch("https://slack.com/api/chat.postMessage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ channel, text: message }),
  });
  const result = await response.json();
  if (!result.ok) {
    throw new Error(`Slack API error: ${result.error ?? "unknown"}`);
  }
  console.log("Posted aggregate summary to Slack");
}

async function runAggregate(summariesDir, { postToSlack }) {
  const summaries = collectSummaries(summariesDir);
  const warnings = collectWarnings(summariesDir);
  const message = formatAggregateTable(
    CAPACITY_DEPLOYMENTS,
    summaries,
    warnings,
  );
  console.log(message);
  if (postToSlack) {
    const artifactUrl = process.env.GITHUB_RUN_URL;
    const slackMessage = artifactUrl
      ? `${message}\n\n<${artifactUrl}|Download artifacts>`
      : message;
    await postSlack(slackMessage);
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
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.aggregate) {
    await runAggregate(args.summariesDir, { postToSlack: args.slack });
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
