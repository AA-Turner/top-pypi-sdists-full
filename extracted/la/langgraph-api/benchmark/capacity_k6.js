import { check, fail } from 'k6';
import { Trend, Counter } from 'k6/metrics';
import { Benchmarks } from './benchmark-runners/benchmarks.js';

// Metrics
const runExecutionLatency = new Trend('run_execution_latency');
// This object is taken in by runner.validate
const errorMetrics = {
  server_errors: new Counter('server_errors'),
  timeout_errors: new Counter('timeout_errors'),
  missing_message_errors: new Counter('missing_message_errors'),
  api_errors: new Counter('api_errors'), // For __error__ responses with 200 status
  other_errors: new Counter('other_errors'),
};

// Environment variables
const BASE_URL = __ENV.BASE_URL;
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;
const TARGET = parseInt(__ENV.TARGET || '10');
const RUN_EXECUTION_TIMEOUT_SECONDS = parseInt(__ENV.RUN_EXECUTION_TIMEOUT_SECONDS || '10');

// Run mode: 'stateless' (default) or 'stateful' (creates thread first)
const RUN_MODE = __ENV.RUN_MODE || 'stateless';

// Benchmark type: 'wait_write' (default), 'stream_write', 'thread', 'assistant'
const BENCHMARK_TYPE = __ENV.BENCHMARK_TYPE || 'wait_write';

// Agent params
const DATA_SIZE = parseInt(__ENV.DATA_SIZE || '1000');
const DELAY = parseInt(__ENV.DELAY || '0');
const EXPAND = parseInt(__ENV.EXPAND || '10');
const STEPS = parseInt(__ENV.STEPS || '10');

// K6 options
export const options = {
  scenarios: {
    capacity_test: {
      executor: 'per-vu-iterations',
      vus: TARGET,
      iterations: 1,  // Each VU executes once
      maxDuration: `${RUN_EXECUTION_TIMEOUT_SECONDS + 30}s`,
    },
  },
};

// Build request params for benchmark runners
function buildRequestParams() {
  const headers = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) {
    headers['x-api-key'] = LANGSMITH_API_KEY;
  }
  return {
    headers,
    timeout: `${RUN_EXECUTION_TIMEOUT_SECONDS + 10}s`,
  };
}

// Build benchmark graph options
function buildBenchmarkGraphOptions() {
  return {
    graph_id: 'benchmark',
    stateful: RUN_MODE === 'stateful',
    input: {
      data_size: DATA_SIZE,
      delay: DELAY,
      expand: EXPAND,
      steps: STEPS,
    },
  };
}

export function setup() {
  return {};
}

export default function(data) {
  // Print parameters (only once from VU 1)
  if (__VU === 1 && __ITER === 0) {
    console.log(`\n=== K6 Test Parameters ===`);
    console.log(`BASE_URL: ${BASE_URL}`);
    console.log(`TARGET: ${TARGET}`);
    console.log(`BENCHMARK_TYPE: ${BENCHMARK_TYPE}`);
    console.log(`RUN_MODE: ${RUN_MODE}`);
    console.log(`RUN_EXECUTION_TIMEOUT_SECONDS: ${RUN_EXECUTION_TIMEOUT_SECONDS}`);
    console.log(`EXPAND: ${EXPAND}`);
    console.log(`DATA_SIZE: ${DATA_SIZE}`);
    console.log(`=========================\n`);
  }

  const startTime = Date.now();
  const requestParams = buildRequestParams();
  const benchmarkGraphOptions = buildBenchmarkGraphOptions();

  // Get the appropriate benchmark runner
  const runner = Benchmarks.getRunner(BENCHMARK_TYPE);

  // Run the benchmark
  const result = runner.run(BASE_URL, requestParams, benchmarkGraphOptions);

  const totalDuration = (Date.now() - startTime) / 1000;

  // Record execution latency (convert to ms) - do this before timeout check so we capture all durations
  runExecutionLatency.add(totalDuration * 1000);

  const timeoutSuccess = totalDuration <= RUN_EXECUTION_TIMEOUT_SECONDS;

  if (!timeoutSuccess) {
    console.log(`VU ${__VU}: status=${result.status} duration=${totalDuration.toFixed(2)}s success=false (timeout)`);
    errorMetrics.timeout_errors.add(1);
    fail(`Benchmark execution timeout exceeded for VU ${__VU}: ${totalDuration.toFixed(2)}s > ${RUN_EXECUTION_TIMEOUT_SECONDS}s`);
    return; // Exit early to avoid further validation
  }

  // Validate the result using the runner's validation
  const success = runner.validate(result, errorMetrics, benchmarkGraphOptions);

  console.log(`VU ${__VU}: status=${result.status} duration=${totalDuration.toFixed(2)}s success=${success}`);

  // Fail the VU iteration if validation failed
  if (!success) {
    fail(`Benchmark validation failed for VU ${__VU}: status=${result.status}`);
  }
}

export function handleSummary(data) {
  const avgLatency = data.metrics.run_execution_latency?.values?.avg / 1000;

  // Collect error counts
  const errors = {
    server: data.metrics.server_errors?.values?.count || 0,
    timeout: data.metrics.timeout_errors?.values?.count || 0,
    missing_message: data.metrics.missing_message_errors?.values?.count || 0,
    api: data.metrics.api_errors?.values?.count || 0,
    other: data.metrics.other_errors?.values?.count || 0,
  };
  const totalErrors = errors.server + errors.timeout + errors.missing_message + errors.api + errors.other;
  // TODO: fix this to use actual success rate
  const totalRequests = TARGET;
  const successfulRequests = totalRequests - totalErrors;
  let successRate = totalRequests > 0 ? (successfulRequests / totalRequests) * 100 : 0;

  return {
    stdout: JSON.stringify({
      target: TARGET,
      avgExecutionLatencySeconds: avgLatency || null,
      successRate: successRate,
      errors: totalErrors > 0 ? errors : undefined,
    }),
  };
}
