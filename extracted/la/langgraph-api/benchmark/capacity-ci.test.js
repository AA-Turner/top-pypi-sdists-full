/**
 * Run with: npm test  (node's built-in runner, no dependencies)
 *
 * Covers how a failed cell is recorded and rendered. The distinction these
 * assert - "did not run" vs "ran and found no capacity" - is the reason the
 * serverless half of the report read as nine blank cells for a week.
 */

import assert from "node:assert/strict";
import test from "node:test";

import {
  buildErrorSummary,
  capacityVus,
  formatAggregateTable,
} from "./capacity-ci.js";

const CELL = {
  deploymentSlug: "daily-cap-benchmark-serverless",
  computeTier: "SERVERLESS_L",
  benchmarkType: "wait_write",
};

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
  assert.equal(capacityVus({ capacity: { targetVUs: 900 } }), "900");
  assert.equal(
    capacityVus({ capacity: { targetVUs: 900, successfulRunsPerSec: 366 } }),
    "900 (366/s)",
    "throughput at capacity rides alongside the VU count",
  );
});

test("a failed cell renders as ERR in the posted table", () => {
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

  assert.match(tierA, /^TIER_A\s+900 \(366\/s\)/);
  assert.match(tierB, /^TIER_B\s+ERR\b/);
  assert.match(tierA, /-\s*$/);
});

test("an incomplete run says so above the table", () => {
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
  assert.match(table, /:warning: 1 failed, 1 never ran of 3 cells/);
  assert.match(table, /success >= 99%, p50 <= 3s, p95 <= 10s/);
  assert.match(table, /Server overhead, not a customer workload/);

  const clean = formatAggregateTable(deployments, [
    { capacity: { targetVUs: 900 }, config: cell("wait_write") },
    { capacity: { targetVUs: 800 }, config: cell("stream_write") },
    { capacity: { targetVUs: 300 }, config: cell("threads_search_metadata") },
  ]);
  assert.doesNotMatch(clean, /warning/);
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
