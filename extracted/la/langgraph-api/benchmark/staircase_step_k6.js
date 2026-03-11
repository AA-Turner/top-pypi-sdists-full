/**
 * Single step of the staircase benchmark.
 *
 * Runs TARGET constant VUs (or TARGET iter/s with constant-arrival-rate)
 * for PLATEAU_DURATION seconds. Each VU discards its first WARMUP_ITERS
 * iterations (default 1) to warm HTTP connections and server-side caches.
 * Only post-warmup iterations contribute to the reported metrics.
 *
 * Set K6_EXECUTOR=constant-arrival-rate to use open-model load testing
 * (fixed arrival rate regardless of response time). Defaults to
 * constant-vus (closed model).
 */

import { Counter, Trend } from 'k6/metrics';
import { Benchmarks } from './benchmark-runners/benchmarks.js';

const BASE_URL = __ENV.BASE_URL;
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;
const TARGET = parseInt(__ENV.TARGET || '10');
const PLATEAU_DURATION = parseInt(__ENV.PLATEAU_DURATION || '60');
const WARMUP_ITERS = parseInt(__ENV.WARMUP_ITERS || '1');
const BENCHMARK_TYPE = __ENV.BENCHMARK_TYPE || 'wait_write';
const RUN_MODE = __ENV.RUN_MODE || 'stateless';

const K6_EXECUTOR = __ENV.K6_EXECUTOR || 'constant-vus';
const MAX_VUS_MULTIPLIER = parseInt(__ENV.MAX_VUS_MULTIPLIER || '10');
const MAX_VUS = parseInt(__ENV.MAX_VUS || String(TARGET * MAX_VUS_MULTIPLIER));
const PRE_ALLOCATED_VUS = parseInt(__ENV.PRE_ALLOCATED_VUS || String(TARGET));

const DATA_SIZE = parseInt(__ENV.DATA_SIZE || '1000');
const DELAY = parseInt(__ENV.DELAY || '0');
const EXPAND = parseInt(__ENV.EXPAND || '50');
const AGENT_STEPS = __ENV.STEPS ? parseInt(__ENV.STEPS) : undefined;
const MODE = __ENV.MODE || 'single';

const runDuration = new Trend('run_duration');
const iterationsStarted = new Counter('iterations_started');
const successfulRuns = new Counter('successful_runs');
const timeoutErrors = new Counter('timeout_errors');
const connectionErrors = new Counter('connection_errors');
const serverErrors = new Counter('server_errors');
const missingMessageErrors = new Counter('missing_message_errors');
const otherErrors = new Counter('other_errors');

const errorMetrics = {
  timeout_errors: timeoutErrors,
  connection_errors: connectionErrors,
  missing_message_errors: missingMessageErrors,
  other_errors: otherErrors,
  server_errors: serverErrors,
};

function buildScenario() {
  if (K6_EXECUTOR === 'constant-arrival-rate') {
    return {
      executor: 'constant-arrival-rate',
      rate: TARGET,
      timeUnit: '1s',
      duration: `${PLATEAU_DURATION}s`,
      preAllocatedVUs: PRE_ALLOCATED_VUS,
      maxVUs: MAX_VUS,
    };
  }
  return {
    executor: 'constant-vus',
    vus: TARGET,
    duration: `${PLATEAU_DURATION}s`,
  };
}

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  scenarios: {
    step: buildScenario(),
  },
};

const runner = Benchmarks.getRunner(BENCHMARK_TYPE);

const input = { data_size: DATA_SIZE, delay: DELAY, expand: EXPAND, mode: MODE };
if (AGENT_STEPS !== undefined) input.steps = AGENT_STEPS;

const benchmarkGraphOptions = {
  graph_id: 'benchmark',
  input,
  stateful: RUN_MODE === 'stateful',
};

function makeHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) headers['x-api-key'] = LANGSMITH_API_KEY;
  return headers;
}

const requestParams = { headers: makeHeaders(), timeout: '120s' };

export default function () {
  if (__ITER < WARMUP_ITERS) {
    try {
      runner.run(BASE_URL, requestParams, benchmarkGraphOptions);
    } catch (_) {}
    return;
  }

  iterationsStarted.add(1);
  const startTime = Date.now();

  let result;
  try {
    result = runner.run(BASE_URL, requestParams, benchmarkGraphOptions);
  } catch (error) {
    otherErrors.add(1);
    return;
  }

  const duration = Date.now() - startTime;
  const success = runner.validate(result, errorMetrics, benchmarkGraphOptions);

  if (success) {
    runDuration.add(duration);
    successfulRuns.add(1);
  }
}

export function handleSummary(data) {
  const total = data.metrics.iterations_started?.values?.count || 0;
  const successes = data.metrics.successful_runs?.values?.count || 0;
  const failures = total - successes;
  const dur = data.metrics.run_duration?.values;

  const result = {
    target: TARGET,
    totalRuns: total,
    successfulRuns: successes,
    failedRuns: failures,
    successRate: total > 0 ? Math.round((successes / total) * 10000) / 100 : 0,
    avgDurationMs: dur?.avg != null ? Math.round(dur.avg) : null,
    medDurationMs: dur?.med != null ? Math.round(dur.med) : null,
    p95DurationMs: dur?.['p(95)'] != null ? Math.round(dur['p(95)']) : null,
    p99DurationMs: dur?.['p(99)'] != null ? Math.round(dur['p(99)']) : null,
    errors: {
      timeout: data.metrics.timeout_errors?.values?.count || 0,
      connection: data.metrics.connection_errors?.values?.count || 0,
      server: data.metrics.server_errors?.values?.count || 0,
      missingMessage: data.metrics.missing_message_errors?.values?.count || 0,
      other: data.metrics.other_errors?.values?.count || 0,
    },
  };

  const resultFile = __ENV.K6_RESULT_FILE || '/dev/stdout';
  return { [resultFile]: JSON.stringify(result) };
}
