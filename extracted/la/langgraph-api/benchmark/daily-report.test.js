import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, utimesSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import {
  breaches,
  buildMessage,
  findLatestSummary,
  isHealthy,
  readApiVersion,
} from './daily-report.js';

const healthyMetrics = {
  totalRuns: 133000,
  successfulRuns: 133000,
  failedRuns: 0,
  successRate: 100,
  averageDuration: 2.57,
  p95Duration: 5.58,
  p95SuccessDuration: 5.5,
  errors: { byStatus: { 500: 0, 502: 0, 503: 0, 504: 0, other: 0 } },
};

const base = {
  stepOutcome: 'success',
  apiVersion: '0.14.0',
  benchmarkType: 'wait_write',
  artifactName: 'benchmark-results-wait_write-1',
  artifactUrl: 'https://github.com/x/y/actions/runs/1',
  runTime: '2026-08-17 12:00 UTC',
};

test('a clean run is green', () => {
  const message = buildMessage({ ...base, summary: { metrics: healthyMetrics } });
  assert.match(message, /🟢/);
  assert.doesNotMatch(message, /🔴/);
});

// The defect this whole commit exists for: 58 consecutive scheduled runs failed
// on thresholds while Slack showed a green circle, because the emoji came from
// the success rate alone and k6's verdicts never reached the report.
test('crossed thresholds are red, and say which', () => {
  const message = buildMessage({
    ...base,
    stepOutcome: 'failure',
    summary: {
      metrics: healthyMetrics,
      thresholds: {
        run_duration: { 'p(95)<3000': { ok: false } },
        successful_runs: { 'count>172500': { ok: false } },
        http_req_failed: { 'rate<0.01': { ok: true } },
      },
    },
  });
  assert.match(message, /🔴/);
  assert.match(message, /run_duration p\(95\)<3000/);
  assert.match(message, /successful_runs count>172500/);
  assert.doesNotMatch(message, /http_req_failed/, 'a passing threshold must not be listed');
});

// `ls -t summary_*.json | head -1` under `bash -e -o pipefail` killed the step
// before anything could be posted. Silence looked identical to a healthy night.
test('a run that produced no summary still reports, and is red', () => {
  const message = buildMessage({ ...base, stepOutcome: 'failure', summary: null });
  assert.match(message, /🔴/);
  assert.match(message, /No results produced/);
  assert.match(message, /`failure`/);
});

test('a skipped benchmark step is red, not green', () => {
  assert.equal(isHealthy({ stepOutcome: 'skipped', metrics: healthyMetrics }), false);
});

// A dead deployment finishes every iteration in ~1ms, so latency looks superb.
test('total outage is red and does not advertise its latency', () => {
  const message = buildMessage({
    ...base,
    stepOutcome: 'failure',
    summary: {
      metrics: {
        totalRuns: 438,
        successfulRuns: 0,
        failedRuns: 438,
        successRate: 0,
        averageDuration: 0.001,
        p95Duration: 0.002,
        p95SuccessDuration: null,
        errors: { byStatus: {} },
      },
    },
  });
  assert.match(message, /🔴/);
  assert.match(message, /no run succeeded/);
  assert.doesNotMatch(message, /0\.00s/, 'must not present sub-millisecond latency as a result');
});

test('success rate at or below the floor is red even when the step passed', () => {
  assert.equal(
    isHealthy({ stepOutcome: 'success', metrics: { ...healthyMetrics, successRate: 98.5 } }),
    false
  );
  assert.equal(
    isHealthy({ stepOutcome: 'success', metrics: { ...healthyMetrics, successRate: 99.9 } }),
    true
  );
});

test('HTTP failure statuses are surfaced only when non-zero', () => {
  const quiet = buildMessage({ ...base, summary: { metrics: healthyMetrics } });
  assert.doesNotMatch(quiet, /HTTP failures/);
  const noisy = buildMessage({
    ...base,
    summary: {
      metrics: { ...healthyMetrics, errors: { byStatus: { 500: 2, 503: 600, other: 0 } } },
    },
  });
  assert.match(noisy, /HTTP failures.*500: 2.*503: 600/);
});

test('breaches tolerates a summary written before thresholds were reported', () => {
  assert.deepEqual(breaches(undefined), []);
  assert.deepEqual(breaches({}), []);
  assert.deepEqual(breaches({ run_duration: {} }), []);
});

test('message survives values that would break a hand-built JSON payload', () => {
  // The old step pasted values into a JSON string literal with raw newlines.
  const message = buildMessage({
    ...base,
    benchmarkType: 'wait"write\\test',
    summary: { metrics: healthyMetrics },
  });
  assert.equal(typeof JSON.parse(JSON.stringify({ text: message })).text, 'string');
});

// The two guards in isHealthy that a mutation could remove without any test
// noticing, because every existing case reached red by another route first.

test('a summary claiming success with zero successful runs is still red', () => {
  // Contradictory input is exactly what a defensive guard is for: without it
  // the success rate alone would call this healthy.
  assert.equal(
    isHealthy({
      stepOutcome: 'success',
      metrics: { ...healthyMetrics, successfulRuns: 0, successRate: 100 },
    }),
    false
  );
});

test('a passing step with no summary is red, not a crash', () => {
  // k6 can exit 0 and still leave no readable summary, for example when the
  // file is missing from the working directory. Nothing else in this suite
  // reaches the metrics guard with stepOutcome success.
  assert.equal(isHealthy({ stepOutcome: 'success', metrics: null }), false);
  assert.equal(isHealthy({ stepOutcome: 'success', metrics: undefined }), false);
  const message = buildMessage({ ...base, stepOutcome: 'success', summary: null });
  assert.match(message, /🔴/);
  assert.match(message, /No results produced/);
});

// A truncated or partial summary is one of the cases this reporter exists to
// survive. Throwing while formatting would fail the step and post nothing,
// which is precisely the silence it replaces.
test('a malformed summary reports, and never throws', () => {
  const malformed = [
    ['successRate missing', { totalRuns: 5, successfulRuns: 5 }],
    ['metrics empty', {}],
    ['successRate not a number', { totalRuns: 5, successfulRuns: 5, successRate: '100' }],
    ['successRate NaN', { totalRuns: 5, successfulRuns: 5, successRate: NaN }],
    ['durations missing', { totalRuns: 5, successfulRuns: 5, successRate: 100 }],
    ['byStatus not an object', { totalRuns: 1, successfulRuns: 1, successRate: 100, errors: { byStatus: 5 } }],
  ];
  for (const [label, metrics] of malformed) {
    const message = buildMessage({ ...base, summary: { metrics } });
    assert.equal(typeof message, 'string', `${label} produced no message`);
    assert.doesNotMatch(message, /undefined|NaN/, `${label} leaked a raw undefined/NaN`);
  }
});

test('an untrustworthy success rate is never green', () => {
  for (const successRate of [undefined, null, NaN, '100', Infinity]) {
    assert.equal(
      isHealthy({ stepOutcome: 'success', metrics: { ...healthyMetrics, successRate } }),
      false,
      `successRate ${String(successRate)} was treated as healthy`
    );
  }
});

test('missing durations are reported as n/a, not as a fast run', () => {
  const message = buildMessage({
    ...base,
    summary: { metrics: { totalRuns: 5, successfulRuns: 5, failedRuns: 0, successRate: 100 } },
  });
  assert.match(message, /Avg Duration\*: n\/a/);
});

// Both of these were shell before: `ls -t summary_*.json | head -1` and an awk
// over the version file, each wrapped in `|| true` because failing killed the
// step before it could report anything.

test('findLatestSummary picks the newest, ignores everything else', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'bench-'));
  const write = (name, ageSeconds) => {
    const file = path.join(dir, name);
    writeFileSync(file, '{}');
    const when = Date.now() / 1000 - ageSeconds;
    utimesSync(file, when, when);
    return file;
  };
  write('summary_old.json', 300);
  const newest = write('summary_new.json', 10);
  write('results_newest.json', 0);
  write('summary_notjson.txt', 0);
  assert.equal(findLatestSummary(dir), newest);
});

test('findLatestSummary returns null rather than throwing', () => {
  assert.equal(findLatestSummary(mkdtempSync(path.join(tmpdir(), 'empty-'))), null);
  assert.equal(findLatestSummary('/definitely/not/a/directory'), null);
});

test('readApiVersion parses the version, and survives a missing file', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'ver-'));
  const file = path.join(dir, '__init__.py');
  writeFileSync(file, '"""doc"""\n__version__ = "1.2.3"\nother = "9.9.9"\n');
  assert.equal(readApiVersion(file), '1.2.3');
  assert.equal(readApiVersion(path.join(dir, 'nope.py')), null);
  writeFileSync(file, 'no version here\n');
  assert.equal(readApiVersion(file), null);
});

test('the success-rate floor is strict, and the boundary is pinned', () => {
  const metrics = (successRate) => ({ ...healthyMetrics, successRate });
  // 99 exactly is not enough. Documented as strict because a reader could
  // reasonably assume "minimum" means inclusive.
  assert.equal(isHealthy({ stepOutcome: 'success', metrics: metrics(99) }), false);
  assert.equal(isHealthy({ stepOutcome: 'success', metrics: metrics(99.001) }), true);
  assert.equal(isHealthy({ stepOutcome: 'success', metrics: metrics(98.999) }), false);
});
