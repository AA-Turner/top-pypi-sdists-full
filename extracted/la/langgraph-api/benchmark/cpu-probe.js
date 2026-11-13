/*
 * Which CPUs the deployment's workers run on, asked of the benchmark graph:
 * every run returns the `host` and `host_cpu` of the worker that ran it.
 * Staging hands out machines of several CPU generations and the oldest runs the
 * same code about 1.5x slower, so the reports only compare nights that ran on
 * the same kind. Callers ask from handleSummary, after the measured scenario,
 * so the probe never warms a fresh scale-to-zero deployment before its cold
 * start is timed, and it sees the workers a deployment added under load.
 */
import http from 'k6/http';

// A dedicated deployment spreads runs over up to ten workers; twenty runs see most of them.
const PROBE_RUNS = 20;
// After an overloaded staircase step a run waits behind the backlog; the summary should not wait with it.
const PROBE_BUDGET_MS = 30000;

/** `{ "<host>": "<vendor family/model>" }` for each worker that answered. */
export function probeServerCpus(baseUrl, apiKey) {
  const headers = { 'Content-Type': 'application/json' };
  if (apiKey) headers['x-api-key'] = apiKey;
  const body = JSON.stringify({
    assistant_id: 'benchmark',
    input: {},
    context: { steps: 1, expand: 1 },
    config: { recursion_limit: 3 },
  });
  const deadline = Date.now() + PROBE_BUDGET_MS;
  const cpuByHost = {};
  for (let i = 0; i < PROBE_RUNS && Date.now() < deadline; i++) {
    const response = http.post(`${baseUrl}/runs/wait`, body, {
      headers,
      timeout: Math.max(1000, deadline - Date.now()),
      // Not part of the measurement, so a failed probe must not count against http_req_failed.
      responseCallback: http.expectedStatuses({ min: 100, max: 599 }),
    });
    if (response.status !== 200) continue;
    let output;
    try {
      output = response.json();
    } catch (error) {
      continue;
    }
    if (typeof output?.host === 'string' && typeof output?.host_cpu === 'string') {
      cpuByHost[output.host] = output.host_cpu;
    }
  }
  return cpuByHost;
}

/** `{ "<vendor family/model>": workers seen }`, or null when no worker answered. */
export function countByCpu(cpuByHost) {
  const counts = {};
  for (const cpu of Object.values(cpuByHost ?? {})) counts[cpu] = (counts[cpu] ?? 0) + 1;
  return Object.keys(counts).length > 0 ? counts : null;
}
