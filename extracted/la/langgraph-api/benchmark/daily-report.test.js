import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, writeFileSync, utimesSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import {
  ERROR_ATTENTION,
  buildDigest,
  collectRuns,
  describeBenchmark,
  describeThreshold,
  errorStreak,
  figureChanges,
  findLatestSummary,
  isHealthy,
  loadSentence,
  readApiVersion,
  toolLine,
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

const NIGHT = new Date('2026-08-17T12:00:00Z');
const base = { apiVersion: '0.14.0', artifactUrl: 'https://github.com/x/y/actions/runs/1', now: NIGHT };

function run(benchmarkType, overrides = {}) {
  return {
    benchmarkType,
    stepOutcome: 'success',
    summary: { metrics: healthyMetrics },
    history: [],
    ...overrides,
  };
}

const nights = (p95s, extra = () => ({})) => p95s.map((p95Duration, i) => ({ ...healthyMetrics, p95Duration, ...extra(i) }));

test('a clean night is green and says all quiet', () => {
  const { text } = buildDigest([run('wait_write')], base);
  assert.match(text, /^🟢 \*Daily Benchmark · Aug 17\* · API 0\.14\.0 · 1 of 1 passed · all quiet$/m);
  assert.doesNotMatch(text, /^🔴|\*Failed:\*|\*Errors:\*/m);
});

// The defect this whole file exists for: 58 consecutive scheduled runs failed
// on thresholds while Slack showed a green circle, because the emoji came from
// the success rate alone and k6's verdicts never reached the report.
test('crossed thresholds are red, and say which', () => {
  const { text } = buildDigest(
    [
      run('wait_write', {
        stepOutcome: 'failure',
        summary: {
          metrics: healthyMetrics,
          thresholds: {
            run_duration: { 'p(95)<3000': { ok: false } },
            successful_runs: { 'count>172500': { ok: false } },
            http_req_failed: { 'rate<0.01': { ok: true } },
          },
        },
      }),
    ],
    base
  );
  assert.match(text, /^🔴 .* · 0 of 1 passed · wait_write failed$/m);
  assert.match(text, /^\*Failed:\* wait_write: p95 5\.58s \(limit 3s\), successful runs 133,000 \(floor 172,500\)$/m);
  assert.match(text, /^\*Pass:\* p95 < 3s, at least 172,500 successful runs, request errors < 1% · ▲ better/m);
  assert.doesNotMatch(text, /http_req_failed|run_duration|count>/, 'raw k6 names must not leak into the report');
});

// `ls -t summary_*.json | head -1` under `bash -e -o pipefail` killed the step
// before anything could be posted. Silence looked identical to a healthy night.
test('a run that produced no summary still reports, and is red', () => {
  const { text, thread } = buildDigest([run('wait_write', { stepOutcome: 'failure', summary: null })], base);
  assert.match(text, /^🔴/);
  assert.match(text, /^\*Failed:\* wait_write: no results produced, step finished as `failure`$/m);
  assert.match(text, /^wait_write\s+-\s+-\s+-\s*$/m);
  assert.match(thread[0], /wait_write: no results, step finished as `failure`/);
});

test('a runner with no artifact at all is a failed run, not a shorter table', () => {
  const { text } = buildDigest([run('wait_write'), run('stream_write', { stepOutcome: 'missing', summary: null })], base);
  assert.match(text, /1 of 2 passed · stream_write failed/);
  assert.match(text, /stream_write: no results produced, step finished as `missing`/);
});

test('a skipped benchmark step is red, not green', () => {
  assert.equal(isHealthy({ stepOutcome: 'skipped', metrics: healthyMetrics }), false);
});

// A dead deployment finishes every iteration in ~1ms, so latency looks superb.
test('total outage is red and does not advertise its latency', () => {
  const { text, thread } = buildDigest(
    [
      run('wait_write', {
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
      }),
    ],
    base
  );
  assert.match(text, /^🔴/);
  assert.match(text, /wait_write: no run succeeded/);
  assert.match(text, /^wait_write\s+438\s+438\s+-\s*$/m, 'the p95 cell is blank, not a sub-millisecond number');
  assert.doesNotMatch(`${text}\n${thread[0]}`, /0\.00/, 'must not present sub-millisecond latency as a result');
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
  const { text } = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, successRate: 98.5 } } })], base);
  assert.match(text, /^\*Failed:\* wait_write: success 98\.50% \(floor 99%\)$/m);
});

test('failed requests get their own line; a handful is noted, many turn the dot yellow', () => {
  const quiet = buildDigest([run('wait_write')], base).text;
  assert.doesNotMatch(quiet, /Errors:/);

  const few = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, errors: { byStatus: { 503: 1, other: 0 } } } } })], base).text;
  assert.match(few, /^🟢 .* · 1 of 1 passed · all quiet$/m);
  assert.match(few, /^\*Errors:\* wait_write HTTP 503 × 1$/m);

  const many = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, errors: { byStatus: { 500: 2, 503: 600, other: 0 } } } } })], base).text;
  assert.match(many, /^🟡 .* · 1 of 1 passed · errors in wait_write$/m);
  assert.match(many, /^\*Errors:\* wait_write HTTP 500 × 2, HTTP 503 × 600$/m);
  assert.match(many, new RegExp(`🟡 ${ERROR_ATTENTION}\\+ failed requests or a regression`));
});

test('errors on consecutive nights are counted as a streak', () => {
  const withErrors = { ...healthyMetrics, errors: { byStatus: { 500: 92 } } };
  const clean = healthyMetrics;
  assert.equal(errorStreak([]), 1);
  assert.equal(errorStreak([withErrors, withErrors, withErrors, clean, withErrors]), 4, 'the streak stops at the first clean night');
  assert.equal(errorStreak([clean, withErrors]), 1);

  const { text } = buildDigest(
    [run('threads_search_metadata', { summary: { metrics: withErrors }, history: [withErrors, withErrors, withErrors] })],
    base
  );
  assert.match(text, /^\*Errors:\* threads_search HTTP 500 × 92, 4th night in a row$/m);

  const manual = buildDigest(
    [run('threads_search_metadata', { summary: { metrics: withErrors }, history: [withErrors, withErrors, withErrors] })],
    { ...base, manual: true }
  ).text;
  assert.match(manual, /^🟡 \*Daily Benchmark · Aug 17\* · manual run · API/m, 'a dispatched run is marked so nobody reads it as the nightly');
  assert.match(manual, /HTTP 500 × 92, 4 runs in a row$/m, 'a same-day rerun does not count itself as a night');
});

test('message survives values that would break a hand-built JSON payload', () => {
  // The old step pasted values into a JSON string literal with raw newlines.
  const { text } = buildDigest([run('wait"write\\test')], base);
  assert.equal(typeof JSON.parse(JSON.stringify({ text })).text, 'string');
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
  const { text } = buildDigest([run('wait_write', { stepOutcome: 'success', summary: null })], base);
  assert.match(text, /^🔴/);
  assert.match(text, /no results produced/);
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
    const { text, thread } = buildDigest([run('wait_write', { summary: { metrics } })], base);
    assert.equal(typeof text, 'string', `${label} produced no message`);
    assert.doesNotMatch(`${text}\n${thread.join('\n')}`, /undefined|NaN/, `${label} leaked a raw undefined/NaN`);
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

test('missing durations are blank cells, not a fast run', () => {
  const { text, thread } = buildDigest(
    [run('wait_write', { summary: { metrics: { totalRuns: 5, successfulRuns: 5, failedRuns: 0, successRate: 100 } } })],
    base
  );
  assert.match(text, /^wait_write\s+5\s+0\s+-\s*$/m);
  assert.match(thread[0], /^wait_write\s+-\s+-\s+-$/m);
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

test('the digest reads verdict, table, how-to-read, then the thread and artifacts', () => {
  const thresholds = {
    run_duration: { 'p(95)<13000': { ok: true } },
    successful_runs: { 'count>73929': { ok: true } },
    http_req_failed: { 'rate<0.01': { ok: true } },
  };
  const load = { loadSize: '500', levels: '2', plateauDuration: '300' };
  const { text, thread } = buildDigest(
    [
      run('wait_write', { summary: { metrics: healthyMetrics, thresholds }, load }),
      run('stream_write', { summary: { metrics: { ...healthyMetrics, p95Duration: 3.98 }, thresholds }, load }),
      run('threads_search_metadata', { summary: { metrics: { ...healthyMetrics, totalRuns: 31188, successfulRuns: 31096, failedRuns: 92, successRate: 99.705, p95Duration: 9.22 }, thresholds }, load: { ...load, loadSize: '150' } }),
    ],
    base
  );
  const lines = text.split('\n');
  assert.equal(lines[0], '🟢 *Daily Benchmark · Aug 17* · API 0.14.0 · 3 of 3 passed · all quiet');
  assert.equal(
    lines[1],
    'k6: 1,000 virtual users (threads_search 300), 2×60 s ramp, 5 min hold, closed model. Paths: run and wait, run and stream, thread CRUD + metadata search. Measures per-iteration latency (avg, p95) and failed requests by status. Same load nightly on a fresh revision, so a change is the server.',
    'the second line states the mechanics for a developer outside the team'
  );
  assert.equal(lines[2], '*Regressed:* not checked, 0 of 5 nights of history');
  assert.deepEqual(lines.slice(3, 8), [
    '```',
    '                     runs  failed  p95 s ',
    'wait_write        133,000       0    5.6 ',
    'stream_write      133,000       0    4.0 ',
    'threads_search     31,188      92    9.2 ',
  ]);
  assert.equal(lines[8], '```');
  assert.equal(
    lines[9],
    '*Pass:* p95 < 13s, at least 73,929 successful runs, request errors < 1% · ▲ better ▼ worse than the last 5+ nights · 🟢 quiet · 🟡 10+ failed requests or a regression · 🔴 a run failed'
  );
  assert.equal(lines[10], '*Thread:* per-run detail and how to read · <https://github.com/x/y/actions/runs/1|Artifacts:> results and charts');
  assert.equal(lines.length, 11, 'nothing else in the channel message');

  assert.match(thread[0], /^\*Per run\*/);
  assert.match(thread[0], /^wait_write\s+2\.57\s+5\.58\s+5\.50$/m);
  assert.match(thread[0], /^threads_search keeps its threads between nights on purpose, so its table grows\.$/m);
  assert.match(thread[0], /^\*How to read\*\n• \*Tests:\* wait_write = start a run and wait for its result · stream_write = .* · threads_search = .*\.\n• \*Load:\* 1,000 users, search 300, held 5 min after a 2-step ramp\.$/m, 'the long explanation ends the thread');
  assert.doesNotMatch(text, /Threads are kept|How to read/, 'neither the growing-table note nor the guide is in the channel message');
});

test('the scale-to-zero variant carries its own suffix and opens the description with its own sentence', () => {
  const { text } = buildDigest([run('wait_write')], { ...base, titleSuffix: ' (Scale to Zero)', goal: 'Cold start after scaling to zero.' });
  assert.match(text, /^🟢 \*Daily Benchmark \(Scale to Zero\) · Aug 17\*/);
  assert.match(text, /^Cold start after scaling to zero\. k6: closed model\. Paths: run and wait\. Measures/m);
});

test('the description is built from the load that ran, not a fixed sentence', () => {
  const load = { loadSize: '100', levels: '3', plateauDuration: '90' };
  assert.match(describeBenchmark([run('stream_write', { load })]), /^k6: 300 virtual users, 3×60 s ramp, 90s hold, closed model\. Paths: run and stream\./);
  assert.match(describeBenchmark([run('wait_write', { load }), run('stream_write', { load: { ...load, loadSize: '50' } })]), /^k6: 300 virtual users \(stream_write 150\), 3×60 s ramp/);
  assert.doesNotMatch(describeBenchmark([run('wait_write')]), /users|ramp|undefined|NaN/, 'no load, no invented numbers');
});

test('an unknown threshold falls back to the raw k6 expression', () => {
  assert.deepEqual(describeThreshold('iteration_duration', 'p(99)<5000', {}), {
    rule: 'iteration_duration p(99)<5000',
    breach: 'iteration_duration p(99)<5000',
  });
  assert.deepEqual(describeThreshold('run_duration', 'garbage', {}), {
    rule: 'run_duration garbage',
    breach: 'run_duration garbage',
  });
});

test('load is omitted, not invented, when the workflow did not pass it', () => {
  const { text, thread } = buildDigest([run('wait_write')], base);
  assert.doesNotMatch(`${text}\n${thread[0]}`, /Load:/);
  assert.equal(loadSentence([run('wait_write', { load: { loadSize: '', levels: '2' } })]), '');
  assert.equal(
    loadSentence([run('wait_write', { load: { loadSize: '500', levels: '2', plateauDuration: '300' } }), run('threads_search_metadata', { load: { loadSize: '150', levels: '2', plateauDuration: '300' } })]),
    '1,000 users, search 300, held 5 min after a 2-step ramp'
  );
  assert.equal(loadSentence([run('wait_write', { load: { loadSize: '100', plateauDuration: '90' } })]), '100 users, held 90s');
});

test('tonight is compared with past nights inside each figure\'s own band, and only flagged with five of them', () => {
  const past = nights([9.27, 9.07, 6.55, 9.25, 5.97, 4.36]);
  const tonight = { ...healthyMetrics, p95Duration: 7.3 };
  const changes = figureChanges(tonight, past);
  assert.deepEqual(changes.map((c) => [c.label, c.flagged]), [['p95', false], ['avg', false], ['runs', false]]);
  assert.equal(changes[0].deltaPct.toFixed(1), '-6.5');

  const spike = figureChanges({ ...healthyMetrics, p95Duration: 15.0 }, past);
  assert.equal(spike[0].flagged, true);
  assert.equal(spike[0].arrow, '▼');
  assert.equal(spike[0].move, '7.8 → 15.0 s (+92%)');

  const { text } = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, p95Duration: 15.0 } }, history: past })], base);
  assert.match(text, /^🟡 .* · 1 of 1 passed · 1 regression$/m);
  assert.match(text, /^\*Regressed:\* wait_write p95 7\.8 → 15\.0 s \(\+92%\)$/m);
  assert.match(text, /^wait_write\s+133,000\s+0\s+15\.0▼$/m);

  const faster = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, p95Duration: 3.0 } }, history: past })], base).text;
  assert.match(faster, /^🟢 .* · all quiet$/m, 'an improvement is good news, not attention');
  assert.match(faster, /^\*Regressed:\* none$/m);
  assert.match(faster, /^\*Improved:\* wait_write p95 7\.8 → 3\.0 s \(-62%\)$/m);
  assert.match(faster, /3\.0▲/);

  const four = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, p95Duration: 15.0 } }, history: past.slice(0, 4) })], base).text;
  assert.match(four, /^\*Regressed:\* not checked, 4 of 5 nights of history$/m);
  assert.match(four, /^wait_write\s+133,000\s+0\s+15\.0 $/m, 'no arrow on the cell');
});

test('run count is compared in the thread but never flagged', () => {
  const past = nights([5, 5, 5, 5, 5, 5], () => ({ totalRuns: 100000 }));
  const { text, thread } = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, p95Duration: 5, totalRuns: 130000 } }, history: past })], base);
  assert.match(text, /^\*Regressed:\* none$/m);
  assert.doesNotMatch(text, /Improved:/);
  assert.match(thread[0], /^wait_write vs 6 nights: p95 \+0\.0% · avg \+0\.0% · runs \+30\.0%$/m);
});

test('an outage night compares runs, never its failed-request latency', () => {
  const past = nights([9.27, 9.07, 6.55, 9.25, 5.97, 4.36]);
  const outage = { ...healthyMetrics, successfulRuns: 0, successRate: 0, totalRuns: 4000, p95Duration: 0.001, averageDuration: 0.001 };
  const changes = figureChanges(outage, past);
  assert.deepEqual(changes.map((c) => c.label), ['runs']);
  const { thread } = buildDigest([run('wait_write', { stepOutcome: 'failure', summary: { metrics: outage }, history: past })], base);
  assert.match(thread[0], /^wait_write vs 6 nights: runs -97\.0%$/m);
});

test('one previous night is not a baseline', () => {
  assert.deepEqual(figureChanges(healthyMetrics, [healthyMetrics]), []);
  assert.deepEqual(figureChanges(healthyMetrics, []), []);
  const { thread } = buildDigest([run('wait_write', { history: [healthyMetrics] })], base);
  assert.match(thread[0], /^wait_write: no history to compare$/m);
});

test('the tool line appears only when the test machine is a visible share of latency', () => {
  assert.equal(toolLine({ ...healthyMetrics, clientOverheadMs: { med: 40, p95: 90 } }), null, '40ms on a 2.57s average is noise');
  assert.equal(
    toolLine({ ...healthyMetrics, clientOverheadMs: { med: 400, p95: 900 } }),
    'the test machine spent 400ms per run outside requests (16% of the average); read latency with that in mind'
  );
  assert.equal(toolLine(healthyMetrics), null, 'older summaries have no overhead figure');
  const { text } = buildDigest([run('wait_write', { summary: { metrics: { ...healthyMetrics, clientOverheadMs: { med: 400, p95: 900 } } } })], base);
  assert.match(text, /^🟡/);
  assert.match(text, /^:warning: wait_write: the test machine spent 400ms per run/m);
});

test('collectRuns reads one artifact directory per runner and marks the missing one', () => {
  const root = mkdtempSync(path.join(tmpdir(), 'digest-'));
  const results = path.join(root, 'results');
  const history = path.join(root, 'history');
  const artifact = (base, runner, id) => {
    const dir = path.join(base, `benchmark-results-scale-to-zero-${runner}-${id}`);
    mkdirSync(dir, { recursive: true });
    return dir;
  };
  const wait = artifact(results, 'wait_write', 99);
  writeFileSync(path.join(wait, 'summary_1.json'), JSON.stringify({ metrics: { ...healthyMetrics, p95Duration: 4.1 } }));
  writeFileSync(path.join(wait, 'report_context.json'), JSON.stringify({ stepOutcome: 'success', loadSize: '500', levels: '2', plateauDuration: '300' }));
  const stream = artifact(results, 'stream_write', 99);
  writeFileSync(path.join(stream, 'report_context.json'), JSON.stringify({ stepOutcome: 'failure' }));
  for (const id of [11, 12]) {
    writeFileSync(path.join(artifact(path.join(history, String(id)), 'wait_write', id), 'summary_1.json'), JSON.stringify({ metrics: { ...healthyMetrics, p95Duration: id } }));
    writeFileSync(path.join(artifact(path.join(history, String(id)), 'stream_write', id), 'summary_1.json'), JSON.stringify({ metrics: { ...healthyMetrics, p95Duration: 100 + id } }));
  }

  const runs = collectRuns(results, history);
  assert.deepEqual(runs.map((r) => [r.benchmarkType, r.stepOutcome, r.summary?.metrics?.p95Duration ?? null]), [
    ['wait_write', 'success', 4.1],
    ['stream_write', 'failure', null],
    ['threads_search_metadata', 'missing', null],
  ]);
  assert.deepEqual(runs[0].load, { loadSize: '500', levels: '2', plateauDuration: '300' });
  assert.deepEqual(runs[0].history.map((m) => m.p95Duration), [12, 11], "each runner sees only its own past, newest first");
  assert.deepEqual(runs[1].history.map((m) => m.p95Duration), [112, 111]);
  assert.deepEqual(runs[2].history, []);
  assert.deepEqual(collectRuns(path.join(root, 'nowhere'), undefined).map((r) => r.stepOutcome), ['missing', 'missing', 'missing']);
});
