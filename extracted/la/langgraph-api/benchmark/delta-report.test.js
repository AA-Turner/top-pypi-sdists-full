import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { DESIGN, aggregateByCell, aggregateSamples, buildReport, collectRun, gain, growthTables, loadDeltaHistory } from './delta-report.js';
import { PHONE_WIDTH, footer, widestCodeLine } from './slack.js';

const MB = 1024 * 1024;
const point = (metric, depth, value, cell) => ({ metric, value, tags: { depth, ...(cell ? { cell } : {}) } });

test('turn and write are averages so a snapshot write counts, read is the median, bytes the largest reading', () => {
  const buckets = aggregateSamples([
    point('turn_duration', '1-50', 100),
    point('turn_duration', '1-50', 300),
    point('checkpoint_save', '1-50', 30),
    point('checkpoint_save', '1-50', 30),
    point('checkpoint_save', '1-50', 600),
    point('thread_storage_bytes', '1-50', 1024),
    point('thread_storage_bytes', '1-50', 4096),
    point('state_read_duration', '1-50', 50),
    point('state_read_duration', '1-50', 70),
    point('turn_duration', '51-100', 900),
  ]);
  assert.deepEqual(buckets['1-50'], { turns: 2, turnMeanMs: 200, saveMeanMs: 220, readP50Ms: 50, bytes: 4096 });
  assert.deepEqual(buckets['51-100'], { turns: 1, turnMeanMs: 900, saveMeanMs: null, readP50Ms: null, bytes: null });
});

test('samples from one run split by the cell the runner tagged them with', () => {
  const byCell = aggregateByCell([
    point('checkpoint_save', '1-50', 300, 'control'),
    point('checkpoint_save', '1-50', 60, 'delta_50'),
    point('checkpoint_save', '1-50', 999),
  ]);
  assert.deepEqual(Object.keys(byCell).sort(), ['control', 'delta_50']);
  assert.equal(byCell.control['1-50'].saveMeanMs, 300);
  assert.equal(byCell.delta_50['1-50'].saveMeanMs, 60);
});

const bucket = (turnMeanMs, saveMeanMs, readP50Ms, bytes) => ({ turns: 1000, turnMeanMs, saveMeanMs, readP50Ms, bytes });

function run({ base = {}, delta = {}, summary, stepOutcome = 'success' } = {}) {
  const b = { turn: 1600, save: 310, read: 110, bytes: 980 * MB, ...base };
  const d = { turn: 1400, save: 60, read: 100, bytes: 22 * MB, ...delta };
  const rows = (t, s, r, bytes) => ({
    '301-350': bucket(t / 4, s / 4, r * 0.6, bytes / 16),
    '651-700': bucket(t / 2, s / 2, r * 0.7, bytes / 4),
    '1001-1050': bucket(t * 0.75, s * 0.75, r * 0.9, bytes / 2),
    '1301-1350': bucket(t, s, r, null),
    '1351-1400': bucket(t, s, r, bytes),
  });
  return {
    stepOutcome,
    load: { loadSize: '20', turns: '1400' },
    summary:
      summary === null
        ? null
        : {
            metrics: { totalRuns: 56000, successfulRuns: 56000, failedRuns: 0, successRate: 100, errors: { missingMessage: 0, byStatus: {} }, ...summary },
            thresholds: { http_req_failed: { 'rate<0.01': { ok: true } } },
          },
    cells: [
      { cell: 'control', label: 'base', buckets: rows(b.turn, b.save, b.read, b.bytes) },
      { cell: 'delta_50', label: 'delta', buckets: rows(d.turn, d.save, d.read, d.bytes) },
    ],
  };
}

const nightFrom = (r) => Object.fromEntries(r.cells.map((c) => [c.cell, { buckets: c.buckets }]));
const base = { apiVersion: '0.16.0rc2', now: new Date('2026-09-30T14:00:00Z'), artifactUrl: 'https://github.com/x/y/actions/runs/1' };

test('a clean night is the verdict, one table at the last turn, and a footer', () => {
  const history = Array.from({ length: 9 }, () => nightFrom(run()));
  const { text } = buildReport(run(), { ...base, history });
  assert.deepEqual(text.split('\n'), [
    '🟢 *Delta Channel · Sep 30* · API 0.16.0rc2 · all quiet',
    '_at turn 1400_',
    '```',
    '       base delta last 10',
    'turn   1.60 1.40 ▄▄▄▄▄▄▄▄▄▄',
    'write  0.31 0.06 ▄▄▄▄▄▄▄▄▄▄',
    'read   0.11 0.10 ▄▄▄▄▄▄▄▄▄▄',
    'data    980 22.0 ▄▄▄▄▄▄▄▄▄▄',
    '```',
    footer('delta-channel', 'https://github.com/x/y/actions/runs/1'),
  ]);
  assert.ok(widestCodeLine(text) <= PHONE_WIDTH, 'the table fits a phone');
});

test('a turn of ten seconds or more keeps a space before it', () => {
  const { text } = buildReport(run({ delta: { turn: 10500 } }), base);
  assert.match(text, /^turn   1\.60 10\.5 /m);
});

test('the thread shows each metric as the threads grow, with the gain at every row', () => {
  const { thread } = buildReport(run(), base);
  assert.match(thread[0], /^\*As the thread grows\*$/m);
  assert.match(thread[0], /^turn s\nturn\s+base\s+delta\s+gain\n350\s+0\.40\s+0\.35\s+same$/m, 'a whole turn gains less than its write');
  assert.match(thread[0], /^write s\nturn\s+base\s+delta\s+gain\n350\s+0\.08\s+0\.01\s+5\.2x$/m);
  assert.match(thread[0], /^data MB$/m);
  assert.match(thread[0], /^1400\s+0\.11\s+0\.10\s+same$/m, 'read within 15% is a tie');
  assert.match(thread[0], /^1400\s+980\s+22\.0\s+45x$/m);
  assert.doesNotMatch(thread[0], /^1350/m, 'rows are every 350 turns only');
  assert.match(thread[0], /^\*Run\* · 20 users × 1,400 turns × 2 setups · 0 failed of 56,000 turns · no correctness failures$/m);
  assert.ok(widestCodeLine(thread[0]) <= PHONE_WIDTH, 'every table fits a phone');
});

test('a delta metric outside its usual range is named above the table once five nights exist', () => {
  const history = Array.from({ length: 5 }, () => nightFrom(run()));
  const { text, thread } = buildReport(run({ delta: { read: 130, save: 30 } }), { ...base, history });
  assert.match(text, /^🟡 .* · 1 regression$/m);
  assert.match(text, /^⚠️ \*delta read 0\.10 → 0\.13 s \(\+30%\)\*$/m);
  assert.match(text, /^read\s+0\.11 0\.13 ▃▃▃▃▃▆$/m, 'the trend shows tonight against the nights before it');
  assert.match(thread[0], /^\*Improved:\* delta write 0\.06 → 0\.03 s \(-50%\)$/m);
});

test('fewer than five nights compare nothing, and the post says so', () => {
  const history = Array.from({ length: 4 }, () => nightFrom(run()));
  const { text } = buildReport(run({ delta: { read: 500 } }), { ...base, history });
  assert.doesNotMatch(text, /⚠️/);
  assert.match(text, /^_4 of 5 nights of history, no change flags yet_$/m);
});

test('history keeps only nights measured with this design, newest first', () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'delta-history-'));
  const write = (runId, report) => {
    mkdirSync(path.join(dir, runId, 'delta-report'), { recursive: true });
    writeFileSync(path.join(dir, runId, 'delta-report', 'delta_report.json'), JSON.stringify(report));
  };
  write('100', { design: DESIGN, cells: { control: { tag: 'older' } } });
  write('300', { design: DESIGN, cells: { control: { tag: 'newer' } } });
  write('200', { cells: { control: { tag: 'one job per cell' } } });
  write('250', { design: 'paired-messages', cells: { control: { tag: 'median write' } } });
  assert.deepEqual(loadDeltaHistory(dir).map((night) => night.control.tag), ['newer', 'older']);
});

test('without storage readings the data row is left out and the post says why', () => {
  const r = run();
  for (const c of r.cells) for (const b of Object.values(c.buckets)) b.bytes = null;
  const { text } = buildReport(r, base);
  assert.doesNotMatch(text, /^data/m);
  assert.match(text, /^_No data row: the deployment runs an API without `GET \/threads\/\{id\}\/storage` yet\._$/m);
});

test('a run with no results is red and says why', () => {
  const { text } = buildReport(run({ summary: null, stepOutcome: 'failure' }), base);
  assert.match(text, /^🔴 .* · failed$/m);
  assert.match(text, /^\*Failed:\* no results produced, step finished as `failure`$/m);
});

test('a correctness check failure turns the dot yellow and is counted', () => {
  const { text, thread } = buildReport(run({ summary: { errors: { missingMessage: 2, byStatus: { 503: 1 } } } }), base);
  assert.match(text, /^🟡 .* · correctness check failed$/m);
  assert.match(text, /^\*Errors:\* HTTP 503 × 1, correctness check failed × 2$/m);
  assert.match(thread[0], /correctness check failed × 2$/m);
});

test('a run that stopped short compares at the last turn every user finished, and says so', () => {
  const r = run();
  r.cells[1].buckets['1351-1400'].turns = 900;
  const { text } = buildReport(r, base);
  assert.match(text, /^🟡 .* · threads stopped at turn 1,350 of 1,400$/m);
  assert.match(text, /^_at turn 1350_$/m, 'a cold read in the last bucket does not mean every user got there');
});

test('storage missing at the compared turn shows as a dash, not as an API without the endpoint', () => {
  const r = run();
  for (const c of r.cells) c.buckets['1351-1400'].bytes = null;
  const { text } = buildReport(r, base);
  assert.match(text, /^data\s+-\s+- /m);
  assert.doesNotMatch(text, /No data row/);
});

test('gain says how many times better delta is, and a tie as same', () => {
  assert.equal(gain(310, 60), '5.2x');
  assert.equal(gain(980, 22), '45x');
  assert.equal(gain(110, 100), 'same');
  assert.equal(gain(110, 580), '0.2x');
  assert.equal(gain(null, 60), '-');
});

test('growth tables skip a metric no row measured', () => {
  const r = run();
  for (const c of r.cells) for (const b of Object.values(c.buckets)) b.bytes = null;
  assert.equal(growthTables(r.cells).length, 3);
});

test('a single downloaded artifact is read from the results directory itself', async () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'delta-flat-'));
  writeFileSync(path.join(dir, 'report_context.json'), JSON.stringify({ stepOutcome: 'success', loadSize: '1', turns: '50' }));
  const sample = { metric: 'checkpoint_save', type: 'Point', data: { value: 30, tags: { depth: '1-50', cell: 'delta_50' } } };
  writeFileSync(path.join(dir, 'raw_data_1.json'), `${JSON.stringify(sample)}\n`);
  const run = await collectRun(dir);
  assert.equal(run.stepOutcome, 'success');
  assert.equal(run.cells.find((c) => c.cell === 'delta_50').buckets['1-50'].saveMeanMs, 30);
});
