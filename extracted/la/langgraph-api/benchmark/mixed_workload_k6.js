/**
 * Mixed Workload Benchmark
 *
 * Tests how the system handles a mix of:
 * - Many quick, small runs (simulating typical API traffic)
 * - A few long-running runs (simulating complex agent tasks)
 *
 * This is useful for testing:
 * - Queue fairness in DR vs standard runtime
 * - Whether long runs starve short runs (or vice versa)
 * - Tail latency impact of mixed workloads
 */

import http from 'k6/http';
import { sleep } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';
import { baseUrlToBaseUrlName } from './capacity_urls.mjs';

// Metrics for quick runs
const quickRunDuration = new Trend('quick_run_duration');
const quickSuccessfulRuns = new Counter('quick_successful_runs');
const quickFailedRuns = new Counter('quick_failed_runs');
const quickSuccessRate = new Rate('quick_success_rate');

// Metrics for long runs
const longRunDuration = new Trend('long_run_duration');
const longSuccessfulRuns = new Counter('long_successful_runs');
const longFailedRuns = new Counter('long_failed_runs');
const longSuccessRate = new Rate('long_success_rate');

// Error tracking - by error type
const errorThreadCreate = new Counter('error_thread_create');
const errorRunCreate = new Counter('error_run_create');
const errorStatusPoll = new Counter('error_status_poll');
const errorRunFailed = new Counter('error_run_failed');
const errorRunPending = new Counter('error_run_pending');
const errorException = new Counter('error_exception');

// Env
const BASE_URL = __ENV.BASE_URL;
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;
const THREAD_TTL_MINUTES = parseInt(__ENV.THREAD_TTL_MINUTES || '60');

// Workload configs - override via env vars or use defaults
const QUICK = {
  vus: parseInt(__ENV.QUICK_VUS || '20'),
  iterations: parseInt(__ENV.QUICK_ITERATIONS || '100'),
  steps: parseInt(__ENV.QUICK_STEPS || '5'),
  dataSize: parseInt(__ENV.QUICK_DATA_SIZE || '100'),
  delay: 0,
  maxWaitSeconds: parseInt(__ENV.QUICK_MAX_WAIT_SECONDS || '120'),
  pollIntervalSeconds: parseInt(__ENV.QUICK_POLL_INTERVAL || '2'),
};

const LONG = {
  vus: parseInt(__ENV.LONG_VUS || '2'),
  iterations: parseInt(__ENV.LONG_ITERATIONS || '2'),
  steps: parseInt(__ENV.LONG_STEPS || '50'),
  dataSize: parseInt(__ENV.LONG_DATA_SIZE || '10000'),
  delay: parseInt(__ENV.LONG_DELAY || '1'),  // seconds per step
  maxWaitSeconds: parseInt(__ENV.LONG_MAX_WAIT_SECONDS || '300'),
  pollIntervalSeconds: parseInt(__ENV.LONG_POLL_INTERVAL || '5'),
};

export const options = {
  scenarios: {
    quick_runs: {
      executor: 'shared-iterations',
      vus: QUICK.vus,
      iterations: QUICK.iterations,
      maxDuration: `${QUICK.maxWaitSeconds + 60}s`,
      exec: 'quickRun',
      tags: { workload: 'quick' },
    },
    long_runs: {
      executor: 'shared-iterations',
      vus: LONG.vus,
      iterations: LONG.iterations,
      maxDuration: `${LONG.maxWaitSeconds + 120}s`,
      exec: 'longRun',
      tags: { workload: 'long' },
      startTime: '2s',
    },
  },
};

function headers() {
  const h = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) h['x-api-key'] = LANGSMITH_API_KEY;
  return h;
}

function createAndWaitForRun(config, runType) {
  const reqHeaders = headers();

  try {
    // Create thread with TTL
    const tRes = http.post(`${BASE_URL}/threads`, JSON.stringify({
      ttl: { strategy: 'delete', ttl: THREAD_TTL_MINUTES },
    }), { headers: reqHeaders, timeout: '60s' });

    if (tRes.status !== 200) {
      errorThreadCreate.add(1);
      return { success: false, duration: null, error: 'thread_create_failed', errorType: 'thread_create', statusCode: tRes.status };
    }
    const threadId = tRes.json().thread_id;

    // Create run - capture time for duration calculation
    const createdAt = new Date().getTime();
    const rRes = http.post(`${BASE_URL}/threads/${threadId}/runs`, JSON.stringify({
      assistant_id: 'benchmark',
      input: {
        data_size: config.dataSize,
        delay: config.delay,
        expand: 1,
        steps: config.steps,
      },
      config: { recursion_limit: config.steps + 2 },
    }), { headers: reqHeaders, timeout: '60s' });

    if (rRes.status !== 200) {
      errorRunCreate.add(1);
      return { success: false, duration: null, error: 'run_create_failed', errorType: 'run_create', statusCode: rRes.status };
    }
    const runId = rRes.json().run_id;

    // Poll until run completes or timeout
    const maxWaitMs = config.maxWaitSeconds * 1000;
    const pollIntervalMs = config.pollIntervalSeconds * 1000;
    let elapsed = 0;
    let runStatus = null;
    let run = null;

    while (elapsed < maxWaitMs) {
      sleep(config.pollIntervalSeconds);
      elapsed += pollIntervalMs;

      const statusRes = http.get(`${BASE_URL}/threads/${threadId}/runs/${runId}`, {
        headers: reqHeaders,
        timeout: '60s',
      });

      if (statusRes.status !== 200) {
        errorStatusPoll.add(1);
        return { success: false, duration: null, error: 'status_poll_failed', errorType: 'status_poll', statusCode: statusRes.status };
      }

      run = statusRes.json();
      runStatus = run?.status;

      // If no longer pending/running, we're done polling
      if (runStatus !== 'pending' && runStatus !== 'running') {
        break;
      }
    }

    const success = runStatus === 'success';

    // Calculate duration from API timestamps
    let durationMs = null;
    if (success && run.updated_at) {
      durationMs = new Date(run.updated_at).getTime() - createdAt;
      if (Number.isNaN(durationMs) || durationMs < 0) {
        durationMs = null;
      }
    }

    // Track non-success run statuses
    if (!success) {
      if (runStatus === 'error') {
        errorRunFailed.add(1);
        return { success: false, duration: null, error: 'run_error', errorType: 'run_failed', runStatus };
      } else if (runStatus === 'pending' || runStatus === 'running') {
        // Timed out - still pending after max wait
        errorRunPending.add(1);
        return { success: false, duration: null, error: 'run_timeout', errorType: 'run_pending', runStatus, elapsedSeconds: elapsed / 1000 };
      }
    }

    return { success, duration: durationMs, runId, threadId };
  } catch (e) {
    errorException.add(1);
    return { success: false, duration: null, error: e.message, errorType: 'exception' };
  }
}


export function quickRun() {
  const result = createAndWaitForRun(QUICK, 'quick');
  if (result.success) {
    quickSuccessfulRuns.add(1);
    quickSuccessRate.add(1);
    if (result.duration) {
      quickRunDuration.add(result.duration, { runId: result.runId, threadId: result.threadId });
    }
  } else {
    quickFailedRuns.add(1);
    quickSuccessRate.add(0);
  }
}

export function longRun() {
  const result = createAndWaitForRun(LONG, 'long');
  if (result.success) {
    longSuccessfulRuns.add(1);
    longSuccessRate.add(1);
    if (result.duration) {
      longRunDuration.add(result.duration, { runId: result.runId, threadId: result.threadId });
    }
  } else {
    longFailedRuns.add(1);
    longSuccessRate.add(0);
  }
}

export function handleSummary(data) {
  const ts = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');

  // Helper to build duration stats (convert ms to seconds)
  function durationStats(metricName) {
    const vals = data.metrics[metricName]?.values;
    if (!vals) return { avg: null, p50: null, p95: null, max: null };
    return {
      avg: vals.avg ? vals.avg / 1000 : null,
      p50: vals.med ? vals.med / 1000 : null,
      p95: vals['p(95)'] ? vals['p(95)'] / 1000 : null,
      max: vals.max ? vals.max / 1000 : null,
    };
  }

  // Helper to get metrics for a workload
  function getWorkloadMetrics(successMetric, failedMetric, durationMetric) {
    const succ = data.metrics[successMetric]?.values?.count ?? 0;
    const fail = data.metrics[failedMetric]?.values?.count ?? 0;
    const total = succ + fail;
    return {
      totalRuns: total,
      successfulRuns: succ,
      failedRuns: fail,
      successRate: total > 0 ? (succ / total) * 100 : 0,
      runDuration: durationStats(durationMetric),
    };
  }

  // Get error counts
  function getErrorCounts() {
    return {
      threadCreate: data.metrics.error_thread_create?.values?.count ?? 0,
      runCreate: data.metrics.error_run_create?.values?.count ?? 0,
      statusPoll: data.metrics.error_status_poll?.values?.count ?? 0,
      runFailed: data.metrics.error_run_failed?.values?.count ?? 0,
      runPending: data.metrics.error_run_pending?.values?.count ?? 0,
      exception: data.metrics.error_exception?.values?.count ?? 0,
    };
  }

  const errors = getErrorCounts();
  const totalErrors = errors.threadCreate + errors.runCreate + errors.statusPoll +
                      errors.runFailed + errors.runPending + errors.exception;

  const combinedSummary = {
    timestamp: ts,
    settings: {
      baseUrl: BASE_URL,
      baseUrlName: baseUrlToBaseUrlName[BASE_URL],
      quickVUs: `${QUICK.vus}`,
      longVUs: `${LONG.vus}`,
      scenario: `q${QUICK.vus}:l${LONG.vus}`,
    },
    config: {
      benchmarkType: 'mixed_workload',
      quickSteps: QUICK.steps,
      quickDataSize: QUICK.dataSize,
      longSteps: LONG.steps,
      longDataSize: LONG.dataSize,
      longDelay: LONG.delay,
    },
    quick: getWorkloadMetrics('quick_successful_runs', 'quick_failed_runs', 'quick_run_duration'),
    long: getWorkloadMetrics('long_successful_runs', 'long_failed_runs', 'long_run_duration'),
    errors: {
      total: totalErrors,
      breakdown: errors,
    },
  };

  return {
    [`mixed_workload_${ts}.json`]: JSON.stringify(combinedSummary, null, 2),
    stdout: JSON.stringify(combinedSummary, null, 2),
  };
}
