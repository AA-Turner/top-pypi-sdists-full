import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend } from 'k6/metrics';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

// Custom metrics
const runDuration = new Trend('run_duration');
const successfulRuns = new Counter('successful_runs');
const failedRuns = new Counter('failed_runs');
const timeoutErrors = new Counter('timeout_errors');
const connectionErrors = new Counter('connection_errors');
const serverErrors = new Counter('server_errors');
const otherErrors = new Counter('other_errors');

// URL of your LangGraph server
const BASE_URL = __ENV.BASE_URL || 'http://localhost:9123';
// LangSmith API key only needed with a custom server endpoint
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;

// Params for the runner
const LOAD_SIZE = parseInt(__ENV.LOAD_SIZE || '100');
const LEVELS = parseInt(__ENV.LEVELS || '10');
const PLATEAU_DURATION = parseInt(__ENV.PLATEAU_DURATION || '300');

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
stages.push({ duration: '30s', target: 0 }); // Ramp down

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
    'run_duration': ['p(95)<30000'],  // 95% of runs should complete within 30s
    'successful_runs': ['count>100'],  // At least 100 successful runs
    'http_req_failed': ['rate<0.2'],   // Error rate should be less than 20%
  },
};

// Main test function
export default function() {
  const startTime = new Date().getTime();

  try {
    // Prepare the request payload
    const headers = { 'Content-Type': 'application/json' };
    if (LANGSMITH_API_KEY) {
      headers['x-api-key'] = LANGSMITH_API_KEY;
    }

    // Create a payload with the LangGraph agent configuration
    const payload = JSON.stringify({
        assistant_id: "benchmark",
        input: {
          data_size: DATA_SIZE,
          delay: DELAY,
          expand: EXPAND,
          mode: MODE,
        },
        config: {
          recursion_limit: EXPAND + 2,
        },
      });

    // Make a single request to the wait endpoint
    const response = http.post(`${BASE_URL}/runs/wait`, payload, {
      headers,
      timeout: '120s'  // k6 request timeout slightly longer than the server timeout
    });

    // Don't include verification in the duration of the request
    const duration = new Date().getTime() - startTime;

    // Check the response
    const expected_length = MODE === 'single' ? 1 : EXPAND + 1;
    const success = check(response, {
      'Run completed successfully': (r) => r.status === 200,
      'Response contains expected number of messages': (r) => JSON.parse(r.body).messages.length === expected_length,
    });

    if (success) {
      // Record success metrics
      runDuration.add(duration);
      successfulRuns.add(1);

      // Optional: Log successful run details
      console.log(`Run completed successfully in ${duration/1000}s`);
    } else {
      // Handle failure
      failedRuns.add(1);

      // Classify error based on status code or response
      if (response.status >= 500) {
        serverErrors.add(1);
        console.log(`Server error: ${response.status}`);
      } else if (response.status === 408 || response.error === 'timeout') {
        timeoutErrors.add(1);
        console.log(`Timeout error: ${response.error}`);
      } else {
        otherErrors.add(1);
        console.log(`Other error: Status ${response.status}, ${JSON.stringify(response)}`);
      }
    }

  } catch (error) {
    // Handle exceptions (network errors, etc.)
    failedRuns.add(1);

    if (error.message.includes('timeout')) {
      timeoutErrors.add(1);
      console.log(`Timeout error: ${error.message}`);
    } else if (error.message.includes('connection') || error.message.includes('network')) {
      connectionErrors.add(1);
      console.log(`Connection error: ${error.message}`);
    } else {
      otherErrors.add(1);
      console.log(`Unexpected error: ${error.message}`);
    }
  }

  // Add a small random sleep between iterations to prevent thundering herd
  sleep(randomIntBetween(0.2, 0.5) / 1.0);
}

// Setup function
export function setup() {
  console.log(`Starting ramp benchmark`);
  console.log(`Running on pod: ${__ENV.POD_NAME || 'local'}`);
  console.log(`Running ${LEVELS} levels with base size ${LOAD_SIZE}`);

  return { startTime: new Date().toISOString() };
}

// Handle summary
export function handleSummary(data) {
  const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');

  // Create summary information with aggregated metrics
  const summary = {
    timestamp: timestamp,
    metrics: {
      totalRuns: data.metrics.successful_runs.values.count + data.metrics.failed_runs.values.count,
      successfulRuns: data.metrics.successful_runs.values.count,
      failedRuns: data.metrics.failed_runs.values.count,
      successRate: data.metrics.successful_runs.values.count /
                  (data.metrics.successful_runs.values.count + data.metrics.failed_runs.values.count) * 100,
      averageDuration: data.metrics.run_duration.values.avg / 1000,  // in seconds
      p95Duration: data.metrics.run_duration.values["p(95)"] / 1000, // in seconds
      errors: {
        timeout: data.metrics.timeout_errors ? data.metrics.timeout_errors.values.count : 0,
        connection: data.metrics.connection_errors ? data.metrics.connection_errors.values.count : 0,
        server: data.metrics.server_errors ? data.metrics.server_errors.values.count : 0,
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