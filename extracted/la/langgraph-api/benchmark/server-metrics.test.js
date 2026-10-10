import assert from "node:assert/strict";
import test from "node:test";

import { cellWindow, formatServerMetrics, summarizeServerMetrics } from "./server-metrics.js";

const chart = (series, points) => ({
  series: series.map(([id, name]) => ({ id, name })),
  data: points.map(([series_id, value]) => ({ series_id, value, timestamp: "2026-09-11T05:00:00Z" })),
});

const SECTION = {
  title: "Metrics for daily-cap-benchmark-dedicated",
  sub_sections: [
    {
      title: "workers",
      charts: [
        chart([["r", "replica_count"]], [["r", 1], ["r", 4], ["r", 12], ["r", 12]]),
        chart([["a", "cpu_usage_avg"], ["m", "cpu_usage_max"]], [["a", 1.2], ["m", 3.7], ["m", 2.9]]),
        chart([["w", "worker_active"], ["p", "runs_pending"]], [["w", 110], ["p", 0], ["p", 340]]),
      ],
    },
    {
      title: "api-server",
      charts: [chart([["r", "replica_count"]], [["r", 2], ["r", 2]])],
    },
    {
      title: "postgres",
      charts: [chart([["c", "cpu_usage_max"]], [["c", 0.91], ["c", null], ["c", "n/a"]])],
    },
  ],
};

test("summarize keeps min and max per series under the dashboard's group", () => {
  const summary = summarizeServerMetrics(SECTION);
  assert.deepEqual(summary.groups.queue.replica_count, { min: 1, max: 12, samples: 4 });
  assert.deepEqual(summary.groups.queue.cpu_usage_max, { min: 2.9, max: 3.7, samples: 2 });
  assert.deepEqual(summary.groups.api.replica_count, { min: 2, max: 2, samples: 2 });
  assert.deepEqual(summary.groups.db.cpu_usage_max, { min: 0.91, max: 0.91, samples: 1 }, "non-numeric points are ignored");
});

test("the cell line reads pods, cpu and queue depth in order", () => {
  assert.equal(
    formatServerMetrics(summarizeServerMetrics(SECTION)),
    "queue pods 1→12 · queue cpu max 3.7 · workers active max 110 · runs pending max 340 · api pods 2→2 · db cpu max 0.91",
  );
});

test("an empty or missing payload renders nothing rather than throwing", () => {
  assert.equal(formatServerMetrics(summarizeServerMetrics(undefined)), "");
  assert.equal(formatServerMetrics(summarizeServerMetrics({ sub_sections: [] })), "");
  assert.equal(formatServerMetrics(undefined), "");
});

test("the cell window spans the first step start to the last step end", () => {
  const steps = [
    { startedAt: "2026-09-11T05:07:00Z", endedAt: "2026-09-11T05:08:05Z" },
    { startedAt: "2026-09-11T05:05:00Z", endedAt: "2026-09-11T05:06:05Z" },
    { error: true },
  ];
  assert.deepEqual(cellWindow(steps), { startTime: "2026-09-11T05:05:00Z", endTime: "2026-09-11T05:08:05Z" });
  assert.equal(cellWindow([{ error: true }]), null, "steps without timestamps give no window");
  assert.equal(cellWindow(undefined), null);
});
