import type { BenchmarkResult } from './types.js';

export interface LogFailureOptions {
  extra?: string;
}

/**
 * k6's console.log is synchronous, so logging every failure throttles the load
 * generator exactly when the server starts failing.
 *
 * Sampling is keyed on the VU rather than a counter because every k6 VU runs in
 * its own JavaScript runtime, so a "first N" counter would emit N lines per VU.
 * Only VU 1 logs, capped at MAX_LOGGED_SAMPLES; the error counters already
 * carry the volume. BENCHMARK_VERBOSE_FAILURES=1 restores full logging.
 */
const VERBOSE = __ENV.BENCHMARK_VERBOSE_FAILURES === '1';
const MAX_LOGGED_SAMPLES = Number(__ENV.BENCHMARK_FAILURE_SAMPLES || '5');
let logged = 0;
let suppressed = 0;

function shouldLog(): boolean {
  if (VERBOSE) return true;
  // Only VU 1 narrates. Every other VU counts silently.
  if (__VU !== 1) return false;
  if (logged < MAX_LOGGED_SAMPLES) {
    logged++;
    return true;
  }
  suppressed++;
  if (suppressed === 1) {
    console.log(
      `[benchmark] further failures suppressed after ${MAX_LOGGED_SAMPLES} samples; see error counters for totals`
    );
  }
  return false;
}

/**
 * Log useful information when a benchmark run or validation fails.
 * Uses the consistent BenchmarkResult shape: ok, step, responses.
 */
export function logFailure(
  benchmarkType: string,
  result: Partial<BenchmarkResult<unknown>> | null | undefined,
  options: LogFailureOptions = {}
): void {
  if (!shouldLog()) return;

  const parts: string[] = [`[${benchmarkType}] FAIL`];
  if (result?.ok === false) {
    parts.push('result.ok=false');
  }
  if (result?.step != null) {
    parts.push(`step=${result.step}`);
  }
  if (result?.responses && typeof result.responses === 'object') {
    for (const [name, res] of Object.entries(result.responses)) {
      if (res && typeof res === 'object') {
        const status = res.status ?? '?';
        parts.push(`${name}=${status}${res.error ? ` error=${res.error}` : ''}`);
        if (res.body != null && (res.status == null || res.status >= 400)) {
          parts.push(`body=${res.body}`);
        }
      }
    }
  }
  if (options.extra) {
    parts.push(options.extra);
  }
  console.log(parts.join(' '));
}
