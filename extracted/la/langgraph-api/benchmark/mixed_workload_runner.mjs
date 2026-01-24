/*
 * Mixed workload benchmark runner.
 * Runs k6 with JSON output, parses slowest runs from metric tags, and merges into summary.
 */

import { execFileSync } from 'node:child_process';
import { readdirSync, readFileSync, writeFileSync, createReadStream } from 'node:fs';
import { join } from 'node:path';
import readline from 'node:readline';

const SLOWEST_N = envInt('SLOWEST_N', 2);

function envInt(name, def) {
  const v = process.env[name];
  if (!v) return def;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : def;
}

const BASE_URL = process.env.BASE_URL;
const LANGSMITH_API_KEY = process.env.LANGSMITH_API_KEY;

// Workload configs
const QUICK_VUS = envInt('QUICK_VUS', 250);
const QUICK_ITERATIONS = envInt('QUICK_ITERATIONS', 1000);
const QUICK_STEPS = envInt('QUICK_STEPS', 5);
const QUICK_DATA_SIZE = envInt('QUICK_DATA_SIZE', 100);
const QUICK_MAX_WAIT_SECONDS = envInt('QUICK_MAX_WAIT_SECONDS', 120);
const QUICK_POLL_INTERVAL = envInt('QUICK_POLL_INTERVAL', 2);
const LONG_VUS = envInt('LONG_VUS', 10);
const LONG_ITERATIONS = envInt('LONG_ITERATIONS', 10);
const LONG_STEPS = envInt('LONG_STEPS', 50);
const LONG_DELAY = envInt('LONG_DELAY', 1);
const LONG_DATA_SIZE = envInt('LONG_DATA_SIZE', 10000);
const LONG_MAX_WAIT_SECONDS = envInt('LONG_MAX_WAIT_SECONDS', 300);
const LONG_POLL_INTERVAL = envInt('LONG_POLL_INTERVAL', 5);

if (!BASE_URL) {
  console.error('BASE_URL is required');
  process.exit(1);
}

function runK6() {
  const env = {
    ...process.env,
    BASE_URL,
    LANGSMITH_API_KEY,
    QUICK_VUS: String(QUICK_VUS),
    QUICK_ITERATIONS: String(QUICK_ITERATIONS),
    QUICK_STEPS: String(QUICK_STEPS),
    QUICK_DATA_SIZE: String(QUICK_DATA_SIZE),
    QUICK_MAX_WAIT_SECONDS: String(QUICK_MAX_WAIT_SECONDS),
    QUICK_POLL_INTERVAL: String(QUICK_POLL_INTERVAL),
    LONG_VUS: String(LONG_VUS),
    LONG_ITERATIONS: String(LONG_ITERATIONS),
    LONG_STEPS: String(LONG_STEPS),
    LONG_DELAY: String(LONG_DELAY),
    LONG_DATA_SIZE: String(LONG_DATA_SIZE),
    LONG_MAX_WAIT_SECONDS: String(LONG_MAX_WAIT_SECONDS),
    LONG_POLL_INTERVAL: String(LONG_POLL_INTERVAL),
  };

  const ts = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
  const rawOut = `mixed_workload_raw_${ts}.json`;

  console.log('Running mixed workload benchmark...');
  execFileSync('k6', ['run', '--out', `json=${rawOut}`, 'mixed_workload_k6.js'], {
    cwd: process.cwd(),
    env,
    stdio: 'inherit',
  });

  return { rawOut, ts };
}

function loadLatestSummary() {
  const files = readdirSync(process.cwd())
    .filter((f) => f.startsWith('mixed_workload_') && f.endsWith('.json') && !f.includes('_raw_'))
    .sort();
  if (files.length === 0) {
    throw new Error('No mixed workload summary file found');
  }
  const latest = files[files.length - 1];
  const content = readFileSync(join(process.cwd(), latest), 'utf-8');
  return { filename: latest, data: JSON.parse(content) };
}

async function extractSlowestRuns(rawFile) {
  const quickRuns = [];
  const longRuns = [];

  await new Promise((resolve, reject) => {
    const rl = readline.createInterface({
      input: createReadStream(join(process.cwd(), rawFile), { encoding: 'utf-8' }),
      crlfDelay: Infinity,
    });

    rl.on('line', (line) => {
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'Point') {
          const name = entry.metric;
          const tags = entry?.data?.tags;
          const v = entry?.data?.value;

          if (tags?.runId && tags?.threadId && Number.isFinite(v)) {
            const run = {
              durationMs: v,
              runId: tags.runId,
              threadId: tags.threadId,
            };

            if (name === 'quick_run_duration') {
              quickRuns.push(run);
            } else if (name === 'long_run_duration') {
              longRuns.push(run);
            }
          }
        }
      } catch (_) {
        // ignore parse errors
      }
    });

    rl.on('close', resolve);
    rl.on('error', reject);
  });

  // Sort and take top N for each
  const formatRuns = (runs) =>
    runs
      .sort((a, b) => b.durationMs - a.durationMs)
      .slice(0, SLOWEST_N)
      .map((r) => ({
        durationSeconds: r.durationMs / 1000,
        runId: r.runId,
        threadId: r.threadId,
      }));

  return {
    quick: formatRuns(quickRuns),
    long: formatRuns(longRuns),
  };
}

async function main() {
  const { rawOut } = runK6();

  // Load the summary file that k6 created
  const { filename, data } = loadLatestSummary();

  // Extract slowest runs from raw JSON output
  const slowestRuns = await extractSlowestRuns(rawOut);
  console.log(`Extracted ${slowestRuns.quick.length} quick and ${slowestRuns.long.length} long slowest runs`);

  // Merge slowest runs into the summary
  data.slowestRuns = slowestRuns;

  // Write back
  writeFileSync(join(process.cwd(), filename), JSON.stringify(data, null, 2));
  console.log(`Updated ${filename} with slowest runs`);


  // Output summary
  console.log(JSON.stringify(data, null, 2));
}

main().catch((e) => {
  console.error('Fatal error:', e?.message || e);
  process.exit(1);
});
