import { sleep } from 'k6';
import { Counter, Trend } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
import { Benchmarks } from './benchmark-runners/benchmarks.js';

// Custom metrics
const runDuration = new Trend('run_duration');
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
}

// URL of your Agent Server
const BASE_URL = __ENV.BASE_URL || 'http://localhost:9123';
// LangSmith API key only needed with a custom server endpoint
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;

// Params for the runner
const LOAD_SIZE = parseInt(__ENV.LOAD_SIZE || '500');
const LEVELS = parseInt(__ENV.LEVELS || '2');
const PLATEAU_DURATION = parseInt(__ENV.PLATEAU_DURATION || '300');
const BENCHMARK_TYPE = __ENV.BENCHMARK_TYPE || 'wait_write';
const STATEFUL = __ENV.STATEFUL === 'true'; // Should the runner be stateful if possible?
const P95_RUN_DURATION = __ENV.P95_RUN_DURATION; // Expected P95 run duration in milliseconds
const AVERAGE_RUN_DURATION = __ENV.AVERAGE_RUN_DURATION; // Expected average run duration in milliseconds

// Params for the agent
const DATA_SIZE = parseInt(__ENV.DATA_SIZE || '1000');
const DELAY = parseInt(__ENV.DELAY || '0');
const EXPAND = parseInt(__ENV.EXPAND || '50');
const MODE = __ENV.MODE || 'single';

const stages = [];
for (let i = 1; i <= LEVELS; i++) {
  stages.push({ duration: '60s', target: LOAD_SIZE * i });
}
stages.push({ duration: `${PLATEAU_DURATION}s`, target: LOAD_SIZE * LEVELS});
stages.push({ duration: '60s', target: 0 }); // Ramp down

// These are rough estimates from running in github actions. Actual results should be better so long as load is 1-1 with jobs available.
const p95_run_duration = {
  'sequential': 18000,
  'parallel': 8500,
  'single': 1500,
}

const average_run_duration = {
  'sequential': 9000,
  'parallel': 4250,
  'single': 750,
}

function getP95RunDuration(mode) {
  return P95_RUN_DURATION ? parseInt(P95_RUN_DURATION) : p95_run_duration[mode];
}

function getAverageRunDuration(mode) {
  return AVERAGE_RUN_DURATION ? parseInt(AVERAGE_RUN_DURATION) : average_run_duration[mode];
}

function getSuccessfulRunsThreshold(mode) {
  // Number of expected successful runs per time period * average number of users for that time period
  const plateau_runs = (PLATEAU_DURATION / (getAverageRunDuration(mode) / 1000)) * LOAD_SIZE * LEVELS;
  const scale_up_runs = (30 * LEVELS / (getAverageRunDuration(mode) / 1000)) * LOAD_SIZE;
  const scale_down_runs = (30 / (getAverageRunDuration(mode) / 1000)) * LOAD_SIZE;
   // This 75% factor is arbitrary, but seems to be the spot for single api host and single redis (which is the slowest)
  return Math.ceil((plateau_runs + scale_up_runs + scale_down_runs) * 0.75);
}

// Test configuration
export let options = {
  scenarios: {
    constant_load: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages,
      gracefulRampDown: '120s',
    },
  },
  thresholds: {
    'run_duration': [`p(95)<${getP95RunDuration(MODE)}`],
    'successful_runs': [`count>${getSuccessfulRunsThreshold(MODE)}`],
    'http_req_failed': ['rate<0.01'],   // Error rate should be less than 1%
  },
};

const runner = Benchmarks.getRunner(BENCHMARK_TYPE);

const benchmarkGraphOptions = {
  graph_id: "benchmark",
  input: {
    data_size: DATA_SIZE,
    delay: DELAY,
    expand: EXPAND,
    mode: MODE,
  },
  stateful: STATEFUL,
}

// Main test function
export default function() {
  const startTime = new Date().getTime();

  // Prepare the request payload
  const headers = { 'Content-Type': 'application/json' };
  if (LANGSMITH_API_KEY) {
    headers['x-api-key'] = LANGSMITH_API_KEY;
  }
  const requestParams = {
    headers,
    timeout: '120s',  // k6 request timeout slightly longer than the server timeout
  };

  let result;
  try {
    result = runner.run(BASE_URL, requestParams, benchmarkGraphOptions);
  } catch (error) {
    failedRuns.add(1);
    otherErrors.add(1);
    console.log(`Unknown error running benchmark: ${error.message}`);
  }

  // Don't include verification in the duration of the request
  const duration = new Date().getTime() - startTime;

  let success = runner.validate(result, errorMetrics, benchmarkGraphOptions);

  if (success) {
    runDuration.add(duration);
    successfulRuns.add(1);
  } else {
    // Don't log the duration for failed runs
    failedRuns.add(1);
  }

  // Add a small random sleep between iterations to prevent thundering herd
  sleep(randomIntBetween(0.2, 0.5) / 1.0);
}

// Setup function
export function setup() {
  console.log(`Starting ramp benchmark`);
  console.log(`Running on pod: ${__ENV.POD_NAME || 'local'}`);
  console.log(`Running with the following ramp config: load size ${LOAD_SIZE}, levels ${LEVELS}, plateau duration ${PLATEAU_DURATION}, stateful ${STATEFUL}`);
  console.log(`Running with the following agent config: data size ${DATA_SIZE}, delay ${DELAY}, expand ${EXPAND}, mode ${MODE}`);
  console.log(`Running with the following thresholds: p95 run duration ${getP95RunDuration(MODE)}ms, average run duration ${getAverageRunDuration(MODE)}ms, successful runs threshold ${getSuccessfulRunsThreshold(MODE)}, error rate < 1%`);

  return { startTime: new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '') };
}

// Handle summary
export function handleSummary(data) {
  const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');

  // Create summary information with aggregated metrics
  const summary = {
    startTimestamp: data.setup_data.startTime,
    endTimestamp: timestamp,
    metrics: {
      totalRuns: data.metrics.successful_runs.values.count + (data.metrics.failed_runs?.values?.count || 0),
      successfulRuns: data.metrics.successful_runs.values.count,
      failedRuns: data.metrics.failed_runs?.values?.count || 0,
      successRate: data.metrics.successful_runs.values.count /
                  (data.metrics.successful_runs.values.count + (data.metrics.failed_runs?.values?.count || 0)) * 100,
      averageDuration: data.metrics.run_duration.values.avg / 1000,  // in seconds
      p95Duration: data.metrics.run_duration.values["p(95)"] / 1000, // in seconds
      errors: {
        timeout: data.metrics.timeout_errors ? data.metrics.timeout_errors.values.count : 0,
        connection: data.metrics.connection_errors ? data.metrics.connection_errors.values.count : 0,
        server: data.metrics.server_errors ? data.metrics.server_errors.values.count : 0,
        missingMessage: data.metrics.missing_message_errors ? data.metrics.missing_message_errors.values.count : 0,
        other: data.metrics.other_errors ? data.metrics.other_errors.values.count : 0
      }
    }
  };

  return {
    [`results_${timestamp}.json`]: JSON.stringify(data, null, 2),
    [`summary_${timestamp}.json`]: JSON.stringify(summary, null, 2),
    stdout: JSON.stringify(summary, null, 2)  // Also print summary to console
  };
}
