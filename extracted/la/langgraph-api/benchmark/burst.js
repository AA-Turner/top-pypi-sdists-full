import http from 'k6/http';
import { check } from 'k6';
import { Counter, Trend, Rate } from 'k6/metrics';
import exec from 'k6/execution';

// Custom metrics
const runDuration = new Trend('run_duration');
const successfulRuns = new Counter('successful_runs');
const failedRuns = new Counter('failed_runs');
const timeoutErrors = new Counter('timeout_errors');
const connectionErrors = new Counter('connection_errors');
const serverErrors = new Counter('server_errors');
const otherErrors = new Counter('other_errors');
const burstSuccessRate = new Rate('burst_success_rate');

// URL of your LangGraph server
const BASE_URL = __ENV.BASE_URL || 'http://localhost:9123';
// LangSmith API key only needed with a custom server endpoint
const LANGSMITH_API_KEY = __ENV.LANGSMITH_API_KEY;

// Params for the runner
const BURST_SIZE = parseInt(__ENV.BURST_SIZE || '100');

// Params for the agent
const DATA_SIZE = parseInt(__ENV.DATA_SIZE || '1000');
const DELAY = parseInt(__ENV.DELAY || '0');
const EXPAND = parseInt(__ENV.EXPAND || '50');
const MODE = __ENV.MODE || 'single';

// Burst testing configuration
export let options = {
  scenarios: {
    burst_test: {
      executor: 'shared-iterations',  // All VUs share the total iterations
      vus: BURST_SIZE,  // Number of concurrent requests in the burst
      iterations: BURST_SIZE,  // Each VU does one request per burst
      maxDuration: '10s',  // Time limit for each burst
    },
  },
  thresholds: {
    'run_duration': ['p(95)<2000'],
    'burst_success_rate': ['rate>=0.99'],
  },
};

// Main test function - executes during the burst
export default function() {
  const startTime = new Date().getTime();

  // Create a unique identifier for each VU
  const burstId = __ENV.BURST_ID || '1';

  try {
    // Log burst start
    console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} starting request`);

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
      }
    });

    // Make a single request to the wait endpoint
    const response = http.post(`${BASE_URL}/runs/wait`, payload, {
      headers,
      timeout: '35s'
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
      burstSuccessRate.add(1);  // 1 = success

      // Optional: Log successful run details
      console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} completed in ${duration/1000}s`);
    } else {
      // Handle failure
      failedRuns.add(1);
      burstSuccessRate.add(0);  // 0 = failure

      // Classify error based on status code or response
      if (response.status >= 500) {
        serverErrors.add(1);
        console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} server error: ${response.status}`);
      } else if (response.status === 408 || response.error === 'timeout') {
        timeoutErrors.add(1);
        console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} timeout error: ${response.error}`);
      } else {
        otherErrors.add(1);
        console.log(`response: ${JSON.stringify(response)}`);
        console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} other error: Status ${response.status}, ${response.error}`);
      }
    }

  } catch (error) {
    // Handle exceptions (network errors, etc.)
    failedRuns.add(1);
    burstSuccessRate.add(0);  // 0 = failure

    if (error.message.includes('timeout')) {
      timeoutErrors.add(1);
      console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} timeout error: ${error.message}`);
    } else if (error.message.includes('connection') || error.message.includes('network')) {
      connectionErrors.add(1);
      console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} connection error: ${error.message}`);
    } else {
      otherErrors.add(1);
      console.log(`[Burst ${burstId}] VU ${exec.vu.idInInstance} unexpected error: ${error.message}`);
    }
  }
}

// Setup function
export function setup() {
  console.log(`Starting burst benchmark`);
  console.log(`Running on pod: ${__ENV.POD_NAME || 'local'}`);
  console.log(`Burst size: ${BURST_SIZE}`);

  return { startTime: new Date().toISOString() };
}

// Handle summary
export function handleSummary(data) {
  // Helper function to safely access nested properties
  const safeGet = (obj, path, defaultValue) => {
    try {
      const parts = path.split('.');
      let result = obj;

      for (const part of parts) {
        if (result === undefined || result === null) return defaultValue;
        result = result[part];
      }

      return result === undefined || result === null ? defaultValue : result;
    } catch (e) {
      return defaultValue;
    }
  };

  // Calculate average burst success rate
  const burstRate = safeGet(data, 'metrics.burst_success_rate.values.rate', 0) * 100;

  // Create a condensed summary with key metrics
  const summary = {
    timestamp: new Date().toISOString(),
    podName: __ENV.POD_NAME || 'local',
    burstSettings: {
      burstSize: BURST_SIZE,
    },
    metrics: {
      totalRuns: safeGet(data, 'metrics.iterations.values.count', 0),
      successfulRuns: safeGet(data, 'metrics.successful_runs.values.count', 0),
      failedRuns: safeGet(data, 'metrics.failed_runs.values.count', 0),
      burstSuccessRate: burstRate.toFixed(2) + '%',
      avgDuration: safeGet(data, 'metrics.run_duration.values.avg', 0) / 1000,
      p95Duration: safeGet(data, 'metrics.run_duration.values.p(95)', 0) / 1000,
      errors: {
        timeout: safeGet(data, 'metrics.timeout_errors.values.count', 0),
        connection: safeGet(data, 'metrics.connection_errors.values.count', 0),
        server: safeGet(data, 'metrics.server_errors.values.count', 0),
        other: safeGet(data, 'metrics.other_errors.values.count', 0)
      }
    },
    raw: {
      http_reqs: safeGet(data, 'metrics.http_reqs.values.count', 0),
      http_req_failed: safeGet(data, 'metrics.http_req_failed.values.rate', 0),
      http_req_duration: {
        avg: safeGet(data, 'metrics.http_req_duration.values.avg', 0),
        min: safeGet(data, 'metrics.http_req_duration.values.min', 0),
        med: safeGet(data, 'metrics.http_req_duration.values.med', 0),
        max: safeGet(data, 'metrics.http_req_duration.values.max', 0),
        p90: safeGet(data, 'metrics.http_req_duration.values.p(90)', 0),
        p95: safeGet(data, 'metrics.http_req_duration.values.p(95)', 0),
        p99: safeGet(data, 'metrics.http_req_duration.values.p(99)', 0)
      }
    }
  };

  // Print the summary as JSON to the logs
  console.log(`====== BURST TEST SUMMARY ======`);
  console.log(`SUMMARY_JSON_START ${JSON.stringify(summary)} SUMMARY_JSON_END`);

  // Generate output files
  const burstStr = `burst${BURST_SIZE}`;
  const timestamp = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');

  return {
    [`results_${burstStr}_${timestamp}.json`]: JSON.stringify(data, null, 2),
    [`summary_${burstStr}_${timestamp}.json`]: JSON.stringify(summary, null, 2),
    stdout: JSON.stringify(summary, null, 2)  // Also print summary to console
  };
}