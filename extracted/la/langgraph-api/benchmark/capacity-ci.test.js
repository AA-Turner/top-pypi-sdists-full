/**
 * Run with: npm test  (node's built-in runner, no dependencies)
 *
 * Covers how a failed cell is recorded and rendered. The distinction these
 * assert - "did not run" vs "ran and found no capacity" - is the reason the
 * serverless half of the report read as nine blank cells for a week.
 */

import assert from "node:assert/strict";
import test from "node:test";

import { PHONE_WIDTH, widestCodeLine } from "./slack.js";

import {
  buildErrorSummary,
  capacityCell,
  deployedVersion,
  capacityVus,
  formatAggregateTable,
  formatImprovements,
  formatServerView,
} from "./capacity-ci.js";

const CELL = {
  deploymentSlug: "daily-cap-benchmark-serverless",
  computeTier: "SERVERLESS_L",
  benchmarkType: "wait_write",
};

const NIGHT = new Date("2026-09-11T07:42:00Z");

const nights = (...values) => values.map((capacityVUs) => ({ capacityVUs, executor: "constant-arrival-rate" }));

test("error summary keeps the config keys the aggregate grids on", () => {
  const summary = buildErrorSummary(CELL, new Error("DEPLOY_FAILED"));
  // formatAggregateTable indexes by exactly these three; dropping one silently
  // removes the cell from the table rather than showing it as failed.
  assert.deepEqual(summary.config, CELL);
  assert.equal(summary.error, "DEPLOY_FAILED");
  assert.equal(summary.capacity, null);
  assert.deepEqual(summary.steps, []);
});

test("error summary accepts a non-Error throw", () => {
  assert.equal(buildErrorSummary(CELL, "boom").error, "boom");
});

test("capacityVus separates no-data, failure and genuine zero", () => {
  assert.equal(capacityVus(undefined), "-", "no summary file at all");
  assert.equal(
    capacityVus(buildErrorSummary(CELL, new Error("nope"))),
    "ERR",
    "cell crashed",
  );
  assert.equal(
    capacityVus({ capacity: null, steps: [{ step: 1 }] }),
    "0",
    "ran, but no step met SLO",
  );
  assert.equal(
    capacityVus({
      capacity: null,
      throughputCeiling: { successfulRunsPerSec: 46.3, atVUs: 200, passesSLO: false },
    }),
    "0 (~46/s ceiling)",
    "no step met SLO, but the cell still measured a service rate",
  );
  assert.equal(capacityVus({ capacity: { targetVUs: 900 } }), "900");
  assert.equal(
    capacityVus({ capacity: { targetVUs: 900, successfulRunsPerSec: 366 } }),
    "900 (366/s)",
    "throughput at capacity rides alongside the VU count",
  );
});

test("the posted cell is the load alone; the served rate lives in the thread", () => {
  assert.equal(capacityCell(undefined), "-");
  assert.equal(capacityCell(buildErrorSummary(CELL, new Error("nope"))), "ERR");
  assert.equal(capacityCell({ capacity: null, throughputCeiling: { successfulRunsPerSec: 46.3 } }), "0");
  assert.equal(capacityCell({ capacity: { targetVUs: 900, successfulRunsPerSec: 366 } }), "900");
});

test("a cell that passed the last step reads as a floor, not a ceiling", () => {
  const config = { numSteps: 13 };
  assert.equal(capacityCell({ config, capacity: { step: 13, targetVUs: 70 } }), "70+");
  assert.equal(capacityCell({ config, capacity: { step: 12, targetVUs: 65 } }), "65");
});

test("a failed cell renders as ERR in the posted table and is named in the Failed line", () => {
  const deployments = [
    { slug: "dep", tiers: ["TIER_A", "TIER_B"] },
  ];
  const summaries = [
    {
      capacity: { targetVUs: 900, successfulRunsPerSec: 366 },
      config: {
        deploymentSlug: "dep",
        computeTier: "TIER_A",
        benchmarkType: "wait_write",
      },
    },
    buildErrorSummary(
      {
        deploymentSlug: "dep",
        computeTier: "TIER_B",
        benchmarkType: "wait_write",
      },
      new Error("DEPLOY_FAILED"),
    ),
  ];

  const table = formatAggregateTable(deployments, summaries);
  const [tierA, tierB] = table
    .split("\n")
    .filter((line) => line.startsWith("TIER_"));

  assert.match(tierA, /^TIER_A\s+900\s+-\s+-\s*$/);
  assert.match(tierB, /^TIER_B\s+ERR\s+-\s+-\s*$/);
  assert.match(table, /^🔴 \*Capacity · .*\* · 1 of 6 cells ran · dep TIER_B crashed, 4 never ran$/m);
  assert.match(table, /^\*Failed:\* dep TIER_B wait \(ERR\) · dep TIER_A stream never ran · .* · treat the table as incomplete$/m);
});

test("an incomplete run says so, a clean run says all quiet", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const cell = (benchmarkType) => ({
    deploymentSlug: "dep",
    computeTier: "TIER_A",
    benchmarkType,
  });

  // 3 expected, 1 failed, 1 never produced a file.
  const table = formatAggregateTable(deployments, [
    { capacity: { targetVUs: 900 }, config: cell("wait_write") },
    buildErrorSummary(cell("stream_write"), new Error("boom")),
  ]);
  assert.match(table, /^🔴 .* · 1 of 3 cells ran · dep TIER_A crashed, 1 never ran$/m);
  assert.match(table, /^\*Failed:\* dep TIER_A stream \(ERR\) · dep TIER_A search never ran · treat the table as incomplete$/m);
  assert.match(table.split("\n")[1], /^\*Failed:\*/, "what went wrong comes right after the verdict");
  assert.match(table, /^\*Why:\* boom$/m);


  const clean = formatAggregateTable(deployments, [
    { capacity: { targetVUs: 900 }, config: cell("wait_write") },
    { capacity: { targetVUs: 800 }, config: cell("stream_write") },
    { capacity: { targetVUs: 300 }, config: cell("threads_search_metadata") },
  ]);
  assert.match(clean, /^🟢 .* · all 3 cells ran · all quiet$/m);
  assert.doesNotMatch(clean, /Failed:/);
  assert.doesNotMatch(clean, /Bottlenecks:/, "nothing to report, no line");
});

test("a whole tier crashing is said once, and a failed job turns the dot red", () => {
  const deployments = [{ slug: "dep", name: "Dep", tiers: ["DEP_A"] }];
  const summaries = ["wait_write", "stream_write", "threads_search_metadata"].map((benchmarkType) =>
    buildErrorSummary({ deploymentSlug: "dep", computeTier: "DEP_A", benchmarkType }, new Error("boom")),
  );
  const table = formatAggregateTable(deployments, summaries);
  assert.match(table, /^\*Failed:\* Dep A, all 3 tests \(ERR\) · treat the table as incomplete$/m);
  assert.match(table, /^A\s+ERR\s+ERR\s+ERR\s*$/m, "the tier drops its deployment prefix under a named deployment");

  process.env.CAPACITY_JOB_RESULT = "failure";
  try {
    const failed = formatAggregateTable(deployments, [
      { capacity: { targetVUs: 900 }, config: { deploymentSlug: "dep", computeTier: "DEP_A", benchmarkType: "wait_write" } },
      { capacity: { targetVUs: 800 }, config: { deploymentSlug: "dep", computeTier: "DEP_A", benchmarkType: "stream_write" } },
      { capacity: { targetVUs: 300 }, config: { deploymentSlug: "dep", computeTier: "DEP_A", benchmarkType: "threads_search_metadata" } },
    ]);
    assert.match(failed, /^🔴 .* · all 3 cells ran · job failed$/m);
    assert.match(failed, /^\*Failed:\* the capacity job exited with failure · treat the table as incomplete$/m);
  } finally {
    delete process.env.CAPACITY_JOB_RESULT;
  }
});

test("warnings reach the posted report, not just the job log", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const summaries = [
    {
      capacity: { targetVUs: 900 },
      config: {
        deploymentSlug: "dep",
        computeTier: "TIER_A",
        benchmarkType: "wait_write",
      },
    },
  ];

  const table = formatAggregateTable(deployments, summaries, [
    "dep: warm-up for TIER_A failed: boom",
  ]);
  assert.match(table, /:warning: dep: warm-up for TIER_A failed: boom/);

  assert.doesNotMatch(
    formatAggregateTable(deployments, summaries, []),
    /warm-up/,
  );
});

test("the header carries date and API version, and the mechanics stay out of the channel", () => {
  const deployments = [
    { slug: "dedicated", tiers: ["DEDICATED_L"] },
    {
      slug: "serverless",
      tiers: ["SERVERLESS_L"],
      staircase: { startLoad: "25", stepSize: "25", numSteps: "12" },
    },
  ];
  const cell = (slug, benchmarkType, extra = {}) => ({
    capacity: { targetVUs: 200 },
    config: { deploymentSlug: slug, computeTier: `${slug.toUpperCase()}_L`, benchmarkType, ...extra },
  });

  const table = formatAggregateTable(
    deployments,
    [cell("dedicated", "wait_write"), cell("serverless", "wait_write")],
    [],
    NIGHT,
    {},
    "0.16.0",
  );
  assert.match(table, /^🔴 \*Capacity · Sep 11\* · API 0\.16\.0 · 2 of 6 cells ran · 4 never ran$/m);
  assert.match(table, /^\*dedicated\* · req\/s at SLO$/m, "a deployment without a display name falls back to its slug");
  assert.equal((table.match(/```/g) ?? []).length, 4, "each table sits in its own code block");
  assert.doesNotMatch(table, /How to read|\*Tests:\*|▲ better|k6 |Cell = /, "the explanation lives in REPORTS.md");
  assert.doesNotMatch(formatAggregateTable(deployments, [], [], NIGHT), /API [0-9u]/, "no version is omitted, not printed as unknown");
  assert.match(
    formatAggregateTable(deployments, [cell("dedicated", "wait_write")], [], NIGHT, {}, null, true),
    /^🔴 \*Capacity · Sep 11\* · manual run · /m,
    "a dispatched run is marked so nobody reads it as the nightly",
  );

});

test("a move outside the usual range is flagged in the table and named above it", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const cell = (benchmarkType, targetVUs) => ({
    capacity: { targetVUs, successfulRunsPerSec: 416 },
    config: { deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType, k6Executor: "constant-arrival-rate" },
  });
  const history = {
    "dep|TIER_A|wait_write": nights(1000, 700, 800, 900, 850),
    "dep|TIER_A|stream_write": nights(1300, 1500, 1400, 1450, 1350),
  };
  const search = cell("threads_search_metadata", 300);
  const table = formatAggregateTable(deployments, [cell("wait_write", 1400), cell("stream_write", 1400), search], [], NIGHT, history);
  assert.match(table, /^🟢 .* · all 3 cells ran · 1 improvement$/m);
  assert.doesNotMatch(table, /Regressed:|Improved:/, "the count is in the header; the numbers are in the thread");
  assert.equal(
    formatImprovements(deployments, [cell("wait_write", 1400), cell("stream_write", 1400), search], history),
    "*Improved:* dep TIER_A wait 850 → 1400 req/s (+65%)",
  );
  assert.match(table, /^TIER_A\s+1400▲\s+1400\s+300\s*$/m, "only the moved cell carries an arrow");

  const drop = formatAggregateTable(deployments, [cell("wait_write", 300), cell("stream_write", 1400), search], [], NIGHT, history);
  assert.match(drop, /1 regression/);
  assert.match(drop, /^\*Regressed:\* dep TIER_A wait 850 → 300 req\/s \(-65%\)$/m);
  assert.match(drop, /^TIER_A\s+300▼/m);
  assert.equal(formatImprovements(deployments, [cell("wait_write", 300), cell("stream_write", 1400), search], history), null, "no improvements, no thread line");
});

test("fewer than five nights of history means no flags, and the report says so", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const tonight = {
    capacity: { targetVUs: 1400 },
    config: { deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType: "wait_write", k6Executor: "constant-arrival-rate" },
  };
  const three = formatAggregateTable(deployments, [tonight], [], NIGHT, { "dep|TIER_A|wait_write": nights(700, 800, 900) });
  assert.match(three, /^_3 of 5 nights of history, no change flags yet_$/m);
  assert.match(three, /^TIER_A\s+1400\s+-\s+-\s*$/m, "no arrow on the cell");

  const none = formatAggregateTable(deployments, [tonight], [], NIGHT, {});
  assert.match(none, /^_0 of 5 nights of history, no change flags yet_$/m);
});

test("a deployment still building its baseline says so under its table while the other is checked", () => {
  const deployments = [
    { slug: "dedicated", name: "Dedicated", tiers: ["DEDICATED_L"] },
    { slug: "serverless", name: "Serverless", tiers: ["SERVERLESS_L"] },
  ];
  const cell = (slug, tier) => ({
    capacity: { targetVUs: 300 },
    config: { deploymentSlug: slug, computeTier: tier, benchmarkType: "wait_write", k6Executor: "constant-arrival-rate" },
  });
  const table = formatAggregateTable(
    deployments,
    [cell("dedicated", "DEDICATED_L"), cell("serverless", "SERVERLESS_L")],
    [],
    NIGHT,
    {
      "dedicated|DEDICATED_L|wait_write": nights(300, 300, 280, 320, 300),
      "serverless|SERVERLESS_L|wait_write": nights(25, 25, 30),
    },
  );
  assert.doesNotMatch(table, /Regressed:/);
  assert.match(table, /^\*Serverless\* · req\/s at SLO\n```\n.*\nL\s+300\s+-\s+-\s*\n```\n_3 of 5 nights of history, no change flags yet_$/m);
  assert.doesNotMatch(table, /Dedicated\*[^]*?no change flags yet[^]*?\*Serverless/, "the note belongs to the deployment that lacks history");
});

test("labels follow the executor the cells ran with", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const cell = (executor) => ({
    capacity: { targetVUs: 400, successfulRunsPerSec: 398 },
    config: { deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType: "wait_write", k6Executor: executor, startLoad: 50, stepSize: 50, numSteps: 12 },
  });
  const open = formatAggregateTable(deployments, [cell("constant-arrival-rate")]);
  assert.match(open, /^\*dep\* · req\/s at SLO$/m);

  const closed = formatAggregateTable(deployments, [cell("constant-vus")]);
  assert.match(closed, /^\*dep\* · users at SLO$/m);
});

test("history only counts nights measured with the same executor", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const tonight = {
    capacity: { targetVUs: 400 },
    config: { deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType: "wait_write", k6Executor: "constant-arrival-rate" },
  };
  const mixed = {
    "dep|TIER_A|wait_write": [
      { capacityVUs: 1400, executor: "constant-vus" },
      { capacityVUs: 1000, executor: "constant-vus" },
      { capacityVUs: 1200, executor: "constant-vus" },
      { capacityVUs: 390, executor: "constant-arrival-rate" },
      { capacityVUs: 410, executor: "constant-arrival-rate" },
    ],
  };
  const table = formatAggregateTable(deployments, [tonight], [], NIGHT, mixed);
  assert.match(table, /2 of 5 nights of history, no change flags yet/, "the three closed-model nights are not a baseline for an open-model night");
});

test("a component at or over 95% CPU is the tier's bottleneck, grouped by component", () => {
  const deployments = [{ slug: "dep", name: "Dep", tiers: ["DEP_L", "DEP_S"] }];
  const cpu = (max) => ({ cpu_usage_max: { min: 0, max } });
  const cell = (tier, benchmarkType, groups) => ({
    capacity: { targetVUs: 400, step: 8 },
    config: { deploymentSlug: "dep", computeTier: tier, benchmarkType },
    serverMetrics: { groups: Object.fromEntries(Object.keys(groups).map((k) => [k, cpu(199)])) },
    serverMetricsAtCapacity: { groups },
  });
  const table = formatAggregateTable(deployments, [
    cell("DEP_L", "wait_write", { redis: cpu(111.8), db: cpu(28) }),
    cell("DEP_L", "stream_write", { redis: cpu(92) }),
    cell("DEP_S", "wait_write", { redis: cpu(102.6), db: cpu(100), queue: cpu(45) }),
    cell("DEP_S", "stream_write", { db: cpu(95) }),
    cell("DEP_L", "threads_search_metadata", {}),
    cell("DEP_S", "threads_search_metadata", {}),
  ]);
  assert.match(table, /^\*Bottlenecks:\* Dep S: database at 95 to 100% · Dep L, S: redis at 103 to 112%$/m, "the verdict uses the passing-step window, not the whole-cell peak");
  assert.doesNotMatch(table, /199/);

  const wholeCellOnly = formatAggregateTable(deployments, [
    { capacity: null, config: { deploymentSlug: "dep", computeTier: "DEP_L", benchmarkType: "wait_write" }, serverMetrics: { groups: { db: cpu(100) } }, serverMetricsAtCapacity: null },
  ]);
  assert.doesNotMatch(wholeCellOnly, /Bottlenecks:/, "a cell that never passed a step has nothing to name");
  assert.match(table, /2 bottlenecks/);
  assert.match(table, /^🟡/);
});

test("the thread carries CPU and pods per cell as tier-grouped tables that fit a phone", () => {
  const deployments = [
    { slug: "dep", name: "Dep", tiers: ["DEP_A"] },
    { slug: "bare", tiers: ["BARE_A"] },
  ];
  const cell = (slug, tier, benchmarkType, extra) => ({
    capacity: { targetVUs: 1400, successfulRunsPerSec: 416.4 },
    config: { deploymentSlug: slug, computeTier: tier, benchmarkType },
    ...extra,
  });
  const view = formatServerView(deployments, [
    cell("dep", "DEP_A", "wait_write", {
      serverMetrics: { groups: { queue: { replica_count: { min: 1, max: 12 }, cpu_usage_max: { min: 1, max: 3.7 } }, redis: { cpu_usage_max: { min: 0, max: 40.2 } } } },
    }),
    cell("dep", "DEP_A", "stream_write", {}),
    { capacity: null, throughputCeiling: { successfulRunsPerSec: 46.3 }, config: { deploymentSlug: "dep", computeTier: "DEP_A", benchmarkType: "threads_search_metadata" } },
    cell("bare", "BARE_A", "wait_write", {}),
  ]);
  assert.match(view, /^\*Pods and CPU per cell\*, peak over the whole cell including the steps that failed\./);
  assert.match(view, /^\*Dep\*\n_CPU, % of request_\n```\n\s+queue redis\nA\n wait\s+4\s+40\n```\n_Pods, start → end_\n```\n\s+queue\nA\n wait\s+1→12\n```$/m);
  assert.doesNotMatch(view, /^ stream/m, "a cell without metrics gets no row");
  assert.ok(widestCodeLine(view) <= PHONE_WIDTH, `widest table line is ${widestCodeLine(view)}`);
  assert.match(view, /^Runs\/sec actually served at the top step, as wait \/ stream \/ search: A 416 \/ 416 \/ 0 \(ceiling 46\)$/m);
  assert.match(view, /^\*bare\*\nRuns\/sec actually served at the top step, as wait \/ stream \/ search: A 416 \/ - \/ -$/m, "the served rate is k6's and prints even when the dashboard gave nothing");
  assert.doesNotMatch(view, /bare\*\n```/, "no pod or CPU table without dashboard data");

  assert.equal(formatServerView(deployments, []), null);
});

test("a step where the tool's own work is a visible share of latency is called out", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const summary = {
    capacity: { targetVUs: 400 },
    config: { deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType: "wait_write" },
    steps: [
      { step: 1, medDurationMs: 800, clientOverheadMs: { med: 20 } },
      { step: 7, medDurationMs: 900, clientOverheadMs: { med: 250 } },
    ],
  };
  const table = formatAggregateTable(deployments, [summary]);
  assert.match(table, /:warning: TIER_A wait_write: the test tool spent 250ms per iteration outside requests at step 7 \(28% of a 900ms median\)/);
  assert.doesNotMatch(table, /at step 1/);
});

test("the version is the deployments', and is left out when none answers", async () => {
  const answer = (byUrl) => async (url) => {
    const version = byUrl[url];
    if (version instanceof Error) throw version;
    return { ok: version !== undefined, json: async () => ({ version }) };
  };
  const deployments = [{ baseUrl: "https://a" }, { baseUrl: "https://b" }];
  assert.equal(await deployedVersion(deployments, answer({ "https://a/info": "0.14.4", "https://b/info": "0.14.4" })), "0.14.4");
  assert.equal(await deployedVersion(deployments, answer({ "https://a/info": "0.14.4", "https://b/info": "0.15.0" })), "0.14.4/0.15.0");
  assert.equal(await deployedVersion(deployments, answer({ "https://a/info": new Error("down") })), null, "an unreachable deployment is not a version");
});

test("the CPU table fits a phone even with every component reporting", () => {
  const deployments = [{ slug: "dep", name: "Dep", tiers: ["DEP_L", "DEP_S"] }];
  const cpu = (max) => ({ cpu_usage_max: { min: 0, max } });
  const summaries = ["DEP_L", "DEP_S"].flatMap((tier) =>
    ["wait_write", "stream_write", "threads_search_metadata"].map((benchmarkType) => ({
      capacity: { targetVUs: 550, successfulRunsPerSec: 548 },
      config: { deploymentSlug: "dep", computeTier: tier, benchmarkType },
      serverMetrics: { groups: { queue: cpu(203.4), api: { ...cpu(133), replica_count: { min: 1, max: 12 } }, db: cpu(100), redis: cpu(160) } },
    })),
  );
  const view = formatServerView(deployments, summaries);
  assert.ok(widestCodeLine(view) <= PHONE_WIDTH, `widest table line is ${widestCodeLine(view)}`);
});

test("tiers that crashed for the same reason name it once", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A", "TIER_B"] }];
  const crash = (computeTier) =>
    buildErrorSummary({ deploymentSlug: "dep", computeTier, benchmarkType: "wait_write" }, new Error("Deployment failed with status: BUILD_FAILED"));
  const table = formatAggregateTable(deployments, [crash("TIER_A"), crash("TIER_B")]);
  assert.match(table, /^\*Why:\* Deployment failed with status: BUILD_FAILED$/m);
});

test("a crashed cell's multi-line error keeps its detail on the Why line", () => {
  const deployments = [{ slug: "dep", tiers: ["TIER_A"] }];
  const error = new Error('PATCH /resource-tiers failed: 409 {\n  "detail": "Unable to resize the deployment database."\n}');
  const table = formatAggregateTable(deployments, [buildErrorSummary({ deploymentSlug: "dep", computeTier: "TIER_A", benchmarkType: "wait_write" }, error)]);
  assert.match(table, /^\*Why:\* PATCH \/resource-tiers failed: 409 \{ "detail": "Unable to resize the deployment database\." \}$/m);
});
