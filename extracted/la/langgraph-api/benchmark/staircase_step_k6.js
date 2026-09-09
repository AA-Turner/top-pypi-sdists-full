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
import { Benchmarks } from './benchmark-runners/dist/benchmarks.js';
import { get_profile } from './benchmark-runners/dist/benchmark_profiles.js';

const BASE_URL = __ENV.BASE_URL;
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;
const TARGET = parseInt(__ENV.TARGET || '10');
const PLATEAU_DURATION = parseInt(__ENV.PLATEAU_DURATION || '60');
const WARMUP_ITERS = parseInt(__ENV.WARMUP_ITERS || '1');
const profile = get_profile(__ENV);
const BENCHMARK_TYPE = profile.benchmarkType;
const RUN_MODE = profile.runMode;
const EFFECTIVE_CONTEXT = profile.context;
const RESUMABLE = profile.resumable;

const K6_EXECUTOR = __ENV.K6_EXECUTOR || 'constant-vus';
const MAX_VUS_MULTIPLIER = parseInt(__ENV.MAX_VUS_MULTIPLIER || '10');
const MAX_VUS = parseInt(__ENV.MAX_VUS || String(TARGET * MAX_VUS_MULTIPLIER));
const PRE_ALLOCATED_VUS = parseInt(__ENV.PRE_ALLOCATED_VUS || String(TARGET));

// A request slower than this has already blown the p95 SLO several times over,
// so there is nothing left to learn by waiting longer.
const REQUEST_TIMEOUT = __ENV.REQUEST_TIMEOUT || '30s';
const TIMEOUT_MS = parseInt(REQUEST_TIMEOUT, 10) * (/ms$/.test(REQUEST_TIMEOUT) ? 1 : 1000);
// Time k6 allows in-flight iterations to finish after the plateau ends. Set
// well above REQUEST_TIMEOUT so iterations terminate rather than being killed.
const GRACEFUL_STOP = __ENV.GRACEFUL_STOP || '60s';

const runDuration = new Trend('run_duration');
const runDurationSuccess = new Trend('run_duration_success');
const iterationsStarted = new Counter('iterations_started');
const successfulRuns = new Counter('successful_runs');
const failedRuns = new Counter('failed_runs');
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

// A single `server_errors` bucket cannot distinguish an application 500 from a
// gateway 503, and a capacity run produces both: 500s from the database still
// resizing after a tier change, and Envoy-generated 503s during scale-up that
// never reach the upstream and so appear in no api-server log. Splitting by
// status makes that readable from the artifact instead of from gateway logs.
//
// Counters must be constructed in init context, hence the fixed set. Read off
// result.responses here rather than in each runner's validate(), so all ten
// runners get this without being touched.
const statusErrors = {
  500: new Counter('errors_http_500'),
  502: new Counter('errors_http_502'),
  503: new Counter('errors_http_503'),
  504: new Counter('errors_http_504'),
};
const otherStatusErrors = new Counter('errors_http_other');

function recordFailureStatuses(result) {
  const responses = result?.responses;
  if (!responses) return;
  for (const response of Object.values(responses)) {
    const status = response?.status;
    if (status == null || status < 400) continue;
    (statusErrors[status] ?? otherStatusErrors).add(1);
  }
}

function buildScenario() {
  if (K6_EXECUTOR === 'constant-arrival-rate') {
    return {
      executor: 'constant-arrival-rate',
      rate: TARGET,
      timeUnit: '1s',
      duration: `${PLATEAU_DURATION}s`,
      preAllocatedVUs: PRE_ALLOCATED_VUS,
      maxVUs: MAX_VUS,
      gracefulStop: GRACEFUL_STOP,
    };
  }
  return {
    executor: 'constant-vus',
    vus: TARGET,
    duration: `${PLATEAU_DURATION}s`,
    gracefulStop: GRACEFUL_STOP,
  };
}

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  scenarios: {
    step: buildScenario(),
  },
};

const runner = Benchmarks.getRunner(BENCHMARK_TYPE);

const benchmarkGraphOptions = {
  graph_id: 'benchmark',
  input: {},
  context: EFFECTIVE_CONTEXT,
  stateful: RUN_MODE === 'stateful',
  resumable: RESUMABLE,
};

function makeHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) headers['x-api-key'] = LANGSMITH_API_KEY;
  return headers;
}

const requestParams = { headers: makeHeaders(), timeout: REQUEST_TIMEOUT };

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
    failedRuns.add(1);
    runDuration.add(Date.now() - startTime);
    return;
  }

  const duration = Date.now() - startTime;
  const success = runner.validate(result, errorMetrics, benchmarkGraphOptions);

  // Every completed iteration contributes, successful or not: under load the
  // failures are the slow requests, and excluding them flatters the latency of
  // exactly the steps that are struggling.
  runDuration.add(duration);
  if (success) {
    runDurationSuccess.add(duration);
    successfulRuns.add(1);
  } else {
    failedRuns.add(1);
    recordFailureStatuses(result);
  }
}

export function handleSummary(data) {
  const started = data.metrics.iterations_started?.values?.count || 0;
  const successes = data.metrics.successful_runs?.values?.count || 0;
  const failures = data.metrics.failed_runs?.values?.count || 0;
  // Counted from completions rather than starts, because an iteration k6 kills
  // at the end of a step neither succeeded nor failed. `truncated` should be 0;
  // a non-zero value means an iteration outlived gracefulStop and check_slo
  // rejects the step.
  const total = successes + failures;
  const truncated = started - total;
  const dur = data.metrics.run_duration?.values;
  const durOk = data.metrics.run_duration_success?.values;

  const result = {
    target: TARGET,
    totalRuns: total,
    iterationsStarted: started,
    truncatedRuns: truncated,
    successfulRuns: successes,
    failedRuns: failures,
    successRate: total > 0 ? Math.round((successes / total) * 10000) / 100 : 0,
    avgDurationMs: dur?.avg != null ? Math.round(dur.avg) : null,
    medDurationMs: dur?.med != null ? Math.round(dur.med) : null,
    p95DurationMs: dur?.['p(95)'] != null ? Math.round(dur['p(95)']) : null,
    p99DurationMs: dur?.['p(99)'] != null ? Math.round(dur['p(99)']) : null,
    p95SuccessDurationMs:
      durOk?.['p(95)'] != null ? Math.round(durOk['p(95)']) : null,
    // A timed-out request is cut off at REQUEST_TIMEOUT, so its recorded
    // duration is a floor, not a measurement: a request that would have taken
    // 45s is written down as 30s. Report the cap and how many durations hit it
    // so nobody reads those as exact, or averages them as if they were.
    requestTimeoutMs: TIMEOUT_MS,
    durationsFlooredAtTimeout:
      data.metrics.timeout_errors?.values?.count || 0,
    errors: {
      timeout: data.metrics.timeout_errors?.values?.count || 0,
      connection: data.metrics.connection_errors?.values?.count || 0,
      server: data.metrics.server_errors?.values?.count || 0,
      missingMessage: data.metrics.missing_message_errors?.values?.count || 0,
      other: data.metrics.other_errors?.values?.count || 0,
      byStatus: {
        500: data.metrics.errors_http_500?.values?.count || 0,
        502: data.metrics.errors_http_502?.values?.count || 0,
        503: data.metrics.errors_http_503?.values?.count || 0,
        504: data.metrics.errors_http_504?.values?.count || 0,
        other: data.metrics.errors_http_other?.values?.count || 0,
      },
    },
  };

  const resultFile = __ENV.K6_RESULT_FILE || '/dev/stdout';
  return { [resultFile]: JSON.stringify(result) };
}
