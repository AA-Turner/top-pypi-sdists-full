import type { BenchmarkResult } from './types.js';

export interface LogFailureOptions {
  extra?: string;
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
