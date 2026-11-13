import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import {
  MIN_HISTORY_NIGHTS,
  cellKey,
  compare,
  cpuSignature,
  describeCpus,
  flaggedChange,
  formatDelta,
  formatMove,
  hasFile,
  historyCandidates,
  loadCapacityHistory,
  loadDailyHistory,
  sameCpu,
  sparkline,
} from "./history.js";

test("compare reports the median, the past half-range and tonight's delta", () => {
  const verdict = compare(130879, [74879, 110341, 97523, 109800, 120040, 147648]);
  assert.equal(verdict.nights, 6);
  assert.equal(verdict.median, 110070.5);
  assert.equal(verdict.spreadPct.toFixed(1), "33.1");
  assert.equal(verdict.deltaPct.toFixed(1), "18.9");
  assert.equal(verdict.outside, false, "inside a 33% band, 19% is a normal night");
});

test("the band never drops below 10%, and a stable series still flags a real move", () => {
  const stable = [33.19, 33.33, 32.14, 32.51, 31.73, 34.59];
  assert.equal(compare(33.87, stable).outside, false);
  assert.equal(compare(45.0, stable).outside, true);
  assert.equal(compare(33.87, stable).spreadPct < 10, true, "this series is tighter than the floor");
});

test("compare needs two nights and a non-zero median", () => {
  assert.equal(compare(5, [5]), null);
  assert.equal(compare(5, []), null);
  assert.equal(compare(5, [0, 0]), null);
  assert.equal(compare(undefined, [1, 2]), null);
  assert.equal(compare(5, [1, "x", null, 3]).nights, 2, "non-numbers are dropped, not counted");
});

test("formatDelta carries the sign and one decimal", () => {
  assert.equal(formatDelta(18.94), "+18.9%");
  assert.equal(formatDelta(-6.5), "-6.5%");
  assert.equal(formatDelta(0), "+0.0%");
});

test("a change is flagged only with five nights, and knows which way is better", () => {
  const four = [300, 300, 280, 320];
  const five = [...four, 300];
  assert.equal(flaggedChange(250, four, { higherIsBetter: true }), null, "four nights are not a baseline");
  assert.equal(MIN_HISTORY_NIGHTS, 5);
  const drop = flaggedChange(250, five, { higherIsBetter: true });
  assert.equal(drop.better, false);
  assert.equal(drop.arrow, "▼");
  const faster = flaggedChange(2.0, [5, 5.2, 4.9, 5.1, 5], { higherIsBetter: false });
  assert.equal(faster.better, true);
  assert.equal(faster.arrow, "▲");
  assert.equal(flaggedChange(305, five, { higherIsBetter: true }), null, "inside the band is not a change");
});

test("a move reads before → after with a rounded percentage", () => {
  assert.equal(formatMove(300, 250, -16.7, "req/s"), "300 → 250 req/s (-17%)");
  assert.equal(formatMove("7.8", "4.4", -43.6, "s"), "7.8 → 4.4 s (-44%)");
  assert.equal(formatMove(850, 1400, 64.7), "850 → 1400 (+65%)");
});

function runDir(root, id) {
  const dir = path.join(root, String(id), "artifact");
  mkdirSync(dir, { recursive: true });
  return dir;
}

test("daily history takes one metrics block per run directory, newest run first", () => {
  const root = mkdtempSync(path.join(tmpdir(), "hist-"));
  writeFileSync(path.join(runDir(root, 1), "summary_a.json"), JSON.stringify({ metrics: { p95Duration: 7.3 } }));
  writeFileSync(path.join(runDir(root, 12), "summary_b.json"), JSON.stringify({ metrics: { p95Duration: 9.1 } }));
  writeFileSync(path.join(runDir(root, 3), "results_only.json"), "{}");
  writeFileSync(path.join(runDir(root, 4), "summary_bad.json"), "not json");
  const history = loadDailyHistory(root);
  assert.deepEqual(history.map((m) => m.p95Duration), [9.1, 7.3], "run 12 is newer than run 1, whatever readdir says");
  assert.deepEqual(loadDailyHistory(path.join(root, "missing")), []);
});

test("daily history can be narrowed to one runner's artifacts", () => {
  const root = mkdtempSync(path.join(tmpdir(), "hist-runner-"));
  const artifact = (id, runner) => {
    const dir = path.join(root, String(id), `benchmark-results-${runner}-${id}`);
    mkdirSync(dir, { recursive: true });
    return dir;
  };
  writeFileSync(path.join(artifact(1, "wait_write"), "summary_a.json"), JSON.stringify({ metrics: { p95Duration: 4.1 } }));
  writeFileSync(path.join(artifact(1, "stream_write"), "summary_b.json"), JSON.stringify({ metrics: { p95Duration: 5.3 } }));
  assert.deepEqual(loadDailyHistory(root, "-stream_write-").map((m) => m.p95Duration), [5.3]);
  assert.deepEqual(loadDailyHistory(root, "-threads_search_metadata-"), []);
});

test("capacity history groups nights by cell and skips crashed cells", () => {
  const root = mkdtempSync(path.join(tmpdir(), "cap-"));
  const cell = (slug, tier, type, extra) => JSON.stringify({
    config: { deploymentSlug: slug, computeTier: tier, benchmarkType: type },
    ...extra,
  });
  writeFileSync(path.join(runDir(root, 1), "staircase_summary_d_L_w.json"), cell("d", "L", "wait_write", { capacity: { targetVUs: 1000, successfulRunsPerSec: 242 } }));
  writeFileSync(path.join(runDir(root, 2), "staircase_summary_d_L_w.json"), cell("d", "L", "wait_write", { capacity: { targetVUs: 700, successfulRunsPerSec: 248 } }));
  writeFileSync(path.join(runDir(root, 3), "staircase_summary_d_L_w.json"), cell("d", "L", "wait_write", { capacity: null, error: "boom" }));
  writeFileSync(path.join(runDir(root, 4), "staircase_summary_s_L_w.json"), cell("s", "L", "wait_write", { capacity: null, throughputCeiling: { successfulRunsPerSec: 46.3 } }));
  const history = loadCapacityHistory(root);
  const key = cellKey({ deploymentSlug: "d", computeTier: "L", benchmarkType: "wait_write" });
  assert.deepEqual(history[key].map((n) => n.capacityVUs).sort((a, b) => a - b), [700, 1000]);
  const serverless = history[cellKey({ deploymentSlug: "s", computeTier: "L", benchmarkType: "wait_write" })];
  assert.deepEqual(serverless, [{ executor: "constant-vus", serverCpus: null, capacityVUs: 0, runsPerSec: 46.3 }], "a cell with no passing step keeps its ceiling, and a night without an executor is closed-model");
});

test("capacity history remembers which executor measured each night", () => {
  const root = mkdtempSync(path.join(tmpdir(), "cap-exec-"));
  writeFileSync(path.join(runDir(root, 1), "staircase_summary_d.json"), JSON.stringify({
    config: { deploymentSlug: "d", computeTier: "L", benchmarkType: "wait_write", k6Executor: "constant-arrival-rate" },
    capacity: { targetVUs: 400, successfulRunsPerSec: 398 },
  }));
  const [night] = loadCapacityHistory(root)[cellKey({ deploymentSlug: "d", computeTier: "L", benchmarkType: "wait_write" })];
  assert.equal(night.executor, "constant-arrival-rate");
});

test("capacity history remembers the CPUs each night ran on", () => {
  const root = mkdtempSync(path.join(tmpdir(), "cap-cpu-"));
  writeFileSync(path.join(runDir(root, 1), "staircase_summary_s.json"), JSON.stringify({
    config: { deploymentSlug: "s", computeTier: "M", benchmarkType: "wait_write" },
    capacity: { targetVUs: 40, successfulRunsPerSec: 39.6 },
    serverCpus: { "GenuineIntel 6/79": 1 },
  }));
  const [night] = loadCapacityHistory(root)[cellKey({ deploymentSlug: "s", computeTier: "M", benchmarkType: "wait_write" })];
  assert.equal(cpuSignature(night.serverCpus), "intel broadwell");
});

test("cpus are named the same inside and outside gVisor, and unknown ones keep their numbers", () => {
  assert.equal(cpuSignature({ "AuthenticAMD 143/49": 1 }), "amd rome", "gVisor's AMD family 143 is Linux's 23");
  assert.equal(cpuSignature({ "AuthenticAMD 23/49": 1 }), "amd rome");
  assert.equal(cpuSignature({ "GenuineIntel 6/79": 1 }), "intel broadwell");
  assert.equal(cpuSignature({ "GenuineIntel 6/207": 1 }), "GenuineIntel 6/207");
  assert.equal(cpuSignature({ "AuthenticAMD 175/17": 1 }), "AuthenticAMD 25/17", "an unnamed AMD still gets the Linux family");
  assert.equal(cpuSignature(null), null);
  assert.equal(cpuSignature({}), null);
});

test("several workers are mostly one cpu when three in four ran on it, and the description counts them", () => {
  const mixed = { "GenuineIntel 6/79": 4, "AuthenticAMD 143/49": 6 };
  assert.equal(cpuSignature(mixed), "amd rome + intel broadwell");
  assert.equal(cpuSignature({ "GenuineIntel 6/79": 9, "AuthenticAMD 143/49": 1 }), "mostly intel broadwell");
  assert.equal(cpuSignature({ "GenuineIntel 6/79": 2, "AuthenticAMD 143/49": 6 }), "mostly amd rome", "exactly three in four");
  assert.equal(describeCpus(mixed), "6 amd rome, 4 intel broadwell");
  assert.equal(describeCpus({ "AuthenticAMD 143/49": 1 }), "amd rome", "one worker needs no count");
  assert.equal(describeCpus(null), null);
});

test("only nights on the same cpus compare, and nights before the probe only compare with each other", () => {
  const rome = { serverCpus: { "AuthenticAMD 143/49": 1 }, p95Duration: 4.5 };
  const broadwell = { serverCpus: { "GenuineIntel 6/79": 1 }, p95Duration: 9.8 };
  const before = { p95Duration: 5.1 };
  const nights = [broadwell, rome, before, rome];
  assert.deepEqual(sameCpu(nights, rome.serverCpus), [rome, rome]);
  assert.deepEqual(sameCpu(nights, broadwell.serverCpus), [broadwell]);
  assert.deepEqual(sameCpu(nights, null), [before]);

  const mostlyRome = { serverCpus: { "AuthenticAMD 143/49": 8, "GenuineIntel 6/79": 2 } };
  const even = { serverCpus: { "AuthenticAMD 143/49": 5, "GenuineIntel 6/79": 5 } };
  const mostlyBroadwell = { serverCpus: { "AuthenticAMD 143/49": 1, "GenuineIntel 6/79": 9 } };
  const split = [mostlyBroadwell, even, mostlyRome, rome];
  assert.deepEqual(sameCpu(split, { "AuthenticAMD 143/49": 9, "GenuineIntel 6/79": 1 }), [mostlyRome], "one slow worker in ten compares with two, not with none, five or nine");
  assert.deepEqual(sameCpu(split, { "AuthenticAMD 143/49": 4, "GenuineIntel 6/79": 6 }), [even], "six in ten compares with five");
});

test("sparkline keeps noise mid-height, draws a real step full height, and leaves gaps for missing nights", () => {
  assert.equal(sparkline([5, 5.2, 4.9, 5.1, 5]), "▄▅▄▅▄");
  assert.equal(sparkline([12.8, 12.5, 4.6, 4.8]), "██▁▁");
  assert.equal(sparkline([1, null, 3]), "▁ █");
  assert.equal(sparkline([2, 2]), "▄▄");
  assert.equal(sparkline([null]), "");
});

test("history keeps only recent completed scheduled runs, newest first, never tonight's", () => {
  const run = (databaseId, createdAt, event = "schedule", status = "completed") => ({ databaseId, createdAt, event, status });
  const runs = [
    run(1, "2026-08-01T12:19:13Z"),
    run(5, "2026-09-27T12:07:31Z"),
    run(6, "2026-09-28T12:09:13Z"),
    run(4, "2026-09-25T15:07:23Z", "workflow_dispatch"),
    run(3, "2026-09-26T12:07:11Z"),
    run(7, "2026-09-28T13:00:00Z", "schedule", "in_progress"),
  ];
  const kept = historyCandidates(runs, { excludeRunId: 6, now: new Date("2026-09-28T12:40:00Z") });
  assert.deepEqual(kept.map((r) => r.databaseId), [5, 3]);
});

test("a night whose artifact holds only its context is not a night of results", () => {
  const dir = mkdtempSync(path.join(tmpdir(), "history-night-"));
  mkdirSync(path.join(dir, "benchmark-results-wait_write-1"));
  writeFileSync(path.join(dir, "benchmark-results-wait_write-1", "report_context.json"), "{}");
  assert.equal(hasFile(dir, "summary_"), false);
  writeFileSync(path.join(dir, "benchmark-results-wait_write-1", "summary_2026-09-29.json"), "{}");
  assert.equal(hasFile(dir, "summary_"), true);
});
