import test from 'node:test';
import assert from 'node:assert/strict';
import { CELLS, aggregateSamples, buildReport, cellChanges, headlineRows, sweepRows, sweepTables } from './delta-report.js';

const point = (metric, depth, value) => ({ metric, value, tags: { depth } });

test('aggregates turn latency, cold read, derived write and end-of-bucket bytes per depth', () => {
  const buckets = aggregateSamples([
    point('turn_duration', '1-100', 100),
    point('turn_duration', '1-100', 300),
    point('turn_duration', '1-100', 200),
    point('thread_storage_bytes', '1-100', 1024),
    point('thread_storage_bytes', '1-100', 4096),
    point('state_read_duration', '1-100', 50),
    point('state_read_duration', '1-100', 70),
    point('turn_duration', '101-200', 900),
  ]);
  assert.deepEqual(buckets['1-100'], { turns: 3, p50Ms: 200, p95Ms: 300, readP50Ms: 50, saveMs: null, rowSaveMs: null, bytes: 4096 });
  assert.deepEqual(buckets['101-200'], { turns: 1, p50Ms: 900, p95Ms: 900, readP50Ms: null, saveMs: null, rowSaveMs: null, bytes: null });
});

const bucket = (readMs, writeMs, bytes) => ({
  turns: 500,
  p50Ms: readMs + writeMs,
  p95Ms: (readMs + writeMs) * 1.5,
  readP50Ms: readMs,
  saveMs: writeMs,
  bytes,
});

function cell(key, { readMs = 40, writeMs = 400, bytes = 40960, successRate = 100, stepOutcome = 'success', guard = 0, summary } = {}) {
  const spec = CELLS.find((c) => c.cell === key);
  return {
    ...spec,
    stepOutcome,
    summary:
      summary === null
        ? null
        : {
            metrics: { totalRuns: 1000, successfulRuns: 1000, failedRuns: 0, successRate, errors: { missingMessage: guard, byStatus: {} } },
            thresholds: { http_req_failed: { 'rate<0.01': { ok: true } } },
          },
    load: { loadSize: '20', plateauDuration: '1500' },
    buckets: summary === null ? {} : { '1-50': bucket(readMs, writeMs, bytes), '51-100': bucket(readMs * 1.2, writeMs, bytes * 2) },
  };
}

const night = (overrides = {}) => [
  cell('control', overrides.control),
  cell('delta_50', { bytes: 4096, ...overrides.delta_50 }),
  cell('delta_500', { readMs: 80, bytes: 4096, ...overrides.delta_500 }),
  cell('delta_1000', { readMs: 120, bytes: 4096, ...overrides.delta_1000 }),
];

const base = { apiVersion: '0.14.2', now: new Date('2026-09-22T14:00:00Z'), artifactUrl: 'https://github.com/x/y/actions/runs/1' };

test('a clean night is green, says all quiet, and puts non-delta beside delta at 50', () => {
  const { text, thread } = buildReport(night(), base);
  assert.match(text, /^🟢 \*Delta Channel · Sep 22\* · API 0\.14\.2 · 4 of 4 cells passed · all quiet$/m);
  assert.match(text, /^\*Regressed:\* not checked, 0 of 5 nights of history$/m);
  assert.match(text, /^turn\s+non-delta\s+delta, snap 50$/m);
  assert.match(text, /^\s+read s\s+write s\s+KB\s+read s\s+write s\s+KB$/m);
  assert.match(text, /^50\s+0\.04\s+0\.40\s+40\s+0\.04\s+0\.40\s+4$/m);
  assert.match(text, /^100\s+0\.05\s+0\.40\s+80\s+0\.05\s+0\.40\s+8$/m);
  const rows = text.split('\n').filter((line) => /^\d+\s+\d/.test(line));
  assert.ok(rows.every((row) => row.length <= 56), 'table rows fit a phone');
  assert.match(text, /^\*Thread:\* per-cell detail.*<https:\/\/github\.com\/x\/y\/actions\/runs\/1\|Artifacts:>/m);
  assert.equal(thread.length, 2);
  assert.match(thread[0], /^\*Per cell\*/);
  assert.match(thread[0], /^turn\s+snap 50\s+snap 500\s+snap 1000$/m);
  assert.match(thread[1], /^\*How to read\*/);
});

test('sweep tables carry read, write and storage per snapshot frequency', () => {
  const [read, write, storage] = sweepTables(night()).map((t) => t.split('\n'));
  assert.match(read[0], /^\*read, median seconds\*/);
  assert.match(read[3], /^50\s+0\.04\s+0\.08\s+0\.12$/);
  assert.match(write[3], /^50\s+0\.40\s+0\.40\s+0\.40$/);
  assert.match(storage[3], /^50\s+4\s+4\s+4$/);
});

test('a cell under the success bar is red and named, with its reason', () => {
  const { text } = buildReport(night({ delta_1000: { successRate: 98.5, stepOutcome: 'failure' } }), base);
  assert.match(text, /^🔴 .* 3 of 4 cells passed · delta\/1000 failed$/m);
  assert.match(text, /^\*Failed:\* delta\/1000: success 98\.50% \(floor 99%\)$/m);
});

test('a cell that never ran is a failed cell, not a shorter table', () => {
  const { text } = buildReport(night({ delta_500: { summary: null, stepOutcome: 'missing' } }), base);
  assert.match(text, /3 of 4 cells passed · delta\/500 failed/);
  assert.match(text, /delta\/500: no results produced, step finished as `missing`/);
});

test('guard or drift failures turn the dot yellow and are spelled out', () => {
  const { text } = buildReport(night({ delta_50: { guard: 3 } }), base);
  assert.match(text, /^🟡 .* 4 of 4 cells passed · correctness check failed in delta\/50$/m);
  assert.match(text, /^\*Errors:\* delta\/50 correctness check failed × 3$/m);
});

const asHistory = (cells) => Object.fromEntries(cells.map((c) => [c.cell, { buckets: c.buckets }]));

test('regressions are flagged at the deepest shared depth once five nights exist, and marked in the table', () => {
  const past = Array.from({ length: 5 }, () => asHistory(night()));
  const tonight = night({ delta_50: { readMs: 90 } });
  const { text } = buildReport(tonight, { ...base, history: past });
  assert.match(text, /^🟡 .* 1 regression$/m);
  assert.match(text, /^\*Regressed:\* delta\/50 read@turn 100 0\.05 → 0\.11 s \(\+125%\)$/m);
  assert.match(text, /^100\s+.*0\.11▼/m);
  const changes = cellChanges(tonight[1], past);
  assert.equal(changes.find((c) => c.key === 'readP50Ms').flagged, true);
  assert.equal(changes.find((c) => c.key === 'bytes').flagged, false);
});

test('fewer than five nights compares in the thread but flags nothing', () => {
  const past = Array.from({ length: 2 }, () => asHistory(night()));
  const { text, thread } = buildReport(night({ delta_50: { readMs: 90 } }), { ...base, history: past });
  assert.match(text, /^\*Regressed:\* not checked, 2 of 5 nights of history$/m);
  assert.ok(text.split('\n').filter((line) => /^\d+\s+\d/.test(line)).every((row) => !row.includes('▼')), 'no arrows in the table');
  assert.match(thread[0], /delta\/50: 0 failed of 1,000 turns \(20 threads × 100 deep\) · vs 2 nights at turn 100: read \+125\.0%/);
});

const every50 = (deepest) => Array.from({ length: deepest / 50 }, (_, i) => `${i * 50 + 1}-${(i + 1) * 50}`);

test('the channel table keeps the first row, every 250th turn and the deepest', () => {
  assert.deepEqual(headlineRows(every50(1300)).map((d) => d.split('-')[1]), ['50', '250', '500', '750', '1000', '1250', '1300']);
  assert.deepEqual(headlineRows(every50(100)).map((d) => d.split('-')[1]), ['50', '100']);
  assert.deepEqual(headlineRows(every50(300), ['101-150']).map((d) => d.split('-')[1]), ['50', '150', '250', '300']);
});

test('the sweep keeps the first row, the deepest, and the turn before and at each snapshot', () => {
  assert.deepEqual(sweepRows(every50(1300), [50, 500, 1000]).map((d) => d.split('-')[1]), ['50', '450', '500', '950', '1000', '1300']);
  assert.deepEqual(sweepRows(every50(300), [50, 500, 1000]).map((d) => d.split('-')[1]), ['50', '300']);
});

test('a night that stops mid-bucket compares at the last turn with a cold read, not the partial one', () => {
  const past = Array.from({ length: 5 }, () => asHistory(night()));
  const tonight = night({ delta_50: { readMs: 90 } });
  tonight[1].buckets['101-150'] = { turns: 7, p50Ms: 500, p95Ms: 600, readP50Ms: null, saveMs: null, bytes: null };
  const { text } = buildReport(tonight, { ...base, history: past });
  assert.match(text, /^\*Regressed:\* delta\/50 read@turn 100 0\.05 → 0\.11 s \(\+125%\)$/m);
  assert.match(text, /^100\s+.*0\.11▼/m);
});

test('tables stop where the slowest cell stopped, and the depth each cell reached is its own line', () => {
  const tonight = night();
  tonight[0].buckets['101-150'] = bucket(50, 400, 122880);
  tonight[0].buckets['151-200'] = bucket(50, 400, 163840);
  // delta/50 got nine turns into the next bucket, with no cold read there yet.
  tonight[1].buckets['101-150'] = { turns: 9, p50Ms: 450, p95Ms: 600, readP50Ms: null, saveMs: null, bytes: null };
  // delta/500's one thread there had its state read fail; only the storage probe answered.
  tonight[2].buckets['101-150'] = { turns: 1, p50Ms: 450, p95Ms: 450, readP50Ms: null, saveMs: null, bytes: 1024 };
  // delta/1000's first verify turn had its state read fail, with storage answering: a hole, not the end.
  tonight[3].buckets['1-50'] = { turns: 500, p50Ms: 450, p95Ms: 600, readP50Ms: null, saveMs: null, bytes: 4096 };
  const { text, thread } = buildReport(tonight, base);
  assert.match(text, /^50\s+/m);
  assert.match(text, /^100\s+/m);
  assert.doesNotMatch(text, /^(150|200)\s+/m);
  assert.match(text, /^_Last measured turn in 25 min: non-delta 200 · delta\/50 100 · delta\/500 100 · delta\/1000 100_$/m);
  assert.doesNotMatch(thread[0], /^(50|150|200)\s+/m);
  assert.match(thread[0], /^100\s+/m);
});

test('a deepest bucket with turns but no cold read yet is not a row of dashes', () => {
  const tonight = night();
  for (const c of tonight) c.buckets['101-150'] = { turns: 9, p50Ms: 450, p95Ms: 600, readP50Ms: null, saveMs: null, bytes: null };
  const { text } = buildReport(tonight, base);
  assert.match(text, /^100\s+/m);
  assert.doesNotMatch(text, /^150\s+/m);
});

test('write is the measured save, and the sweep shows the save at the row turn where snapshots land', () => {
  const save = (value, rowTurn) => ({ metric: 'checkpoint_save', value, tags: { depth: '1-50', row_turn: rowTurn } });
  const buckets = aggregateSamples([save(20, '0'), save(30, '0'), save(25, '0'), save(900, '1'), save(1100, '1')]);
  assert.equal(buckets['1-50'].saveMs, 30);
  assert.equal(buckets['1-50'].rowSaveMs, 900);
  const tonight = night();
  for (const c of tonight) c.buckets['1-50'] = { ...c.buckets['1-50'], saveMs: 30, rowSaveMs: 900 };
  const [, write] = sweepTables(tonight).map((t) => t.split('\n'));
  assert.match(write[0], /^\*write, median \/ at the row's turn, seconds\*/);
  assert.match(write[3], /^50\s+0\.03\/0\.90\s+0\.03\/0\.90\s+0\.03\/0\.90$/);
});

test('a cell whose runs returned no save_ms says why write is blank', () => {
  const tonight = night();
  for (const b of Object.values(tonight[1].buckets)) b.saveMs = null;
  const { text } = buildReport(tonight, base);
  assert.match(text, /^_write reads `-` for delta\/50: its runs returned no `save_ms`/m);
  assert.doesNotMatch(buildReport(night(), base).text, /returned no `save_ms`/);
  tonight[1].summary.metrics.successfulRuns = 0;
  assert.doesNotMatch(buildReport(tonight, base).text, /returned no `save_ms`/);
});
