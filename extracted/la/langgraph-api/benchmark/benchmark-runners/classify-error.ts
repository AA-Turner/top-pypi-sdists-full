import type { ErrorMetrics } from './benchmark-runner.js';

/**
 * Which error counter a failed run belongs in.
 *
 * `wait_write` and `stream_write` each grew their own copy of this ladder, and
 * both had the same hole: neither could ever produce `connection`. That bucket
 * is declared in ramp.js and staircase_step_k6.js, wired into the metrics map,
 * and printed in every report - but no runner has ever written to it, so it has
 * read 0 in all 32 scheduled runs on record. A refused connection has no HTTP
 * status, so it fell through to `missing_message` (stream) or `other` (wait):
 * "the server answered but left something out" when the truth was "the server
 * never answered".
 */
export type ErrorBucket =
  | 'connection'
  | 'timeout'
  | 'server'
  | 'api'
  | 'missing_message'
  | 'other';

/**
 * Only the two fields the ladder reads. Structurally satisfied by both k6's
 * RefinedResponse and our normalized HttpResponse, so runners can pass either
 * without converting.
 */
export interface ClassifiableResponse {
  status?: number;
  error?: string;
}

export interface ClassifyInput {
  /** The response the run hinges on, if there was one. */
  response?: ClassifiableResponse | null;
  /** Runner-specific: the response body carried an `__error__` key. */
  hasApiError?: boolean;
  /** Runner-specific: the expected message/counter never arrived. */
  missingMessage?: boolean;
}

/** k6 reports a status of 0 when no HTTP response was received at all. */
function isUnreachable(response?: ClassifiableResponse | null): boolean {
  if (response == null) return false;
  const status = response.status;
  if (status != null && status > 0) return false;
  return status === 0 || (response.error ?? '') !== '';
}

function isTimeout(response?: ClassifiableResponse | null): boolean {
  if (response?.status === 408) return true;
  return (response?.error ?? '').includes('timeout');
}

/**
 * Order matters: a timeout is reported by k6 as an error string on a status-0
 * response, so it has to be tested before the general unreachable case.
 */
export function classifyError(input: ClassifyInput): ErrorBucket {
  const { response, hasApiError, missingMessage } = input;
  const status = response?.status;

  if (status != null && status >= 500) return 'server';
  if (isTimeout(response)) return 'timeout';
  if (isUnreachable(response)) return 'connection';
  if (hasApiError) return 'api';
  if (missingMessage) return 'missing_message';
  return 'other';
}

/**
 * Add one to the counter for `bucket`, falling back to `other_errors` when the
 * entrypoint did not supply that counter. Preserves the behaviour the runners
 * open-coded for `api_errors` and `missing_message_errors`.
 */
export function recordError(bucket: ErrorBucket, errorMetrics: ErrorMetrics): void {
  const counters: Record<ErrorBucket, { add(n: number): void } | undefined> = {
    server: errorMetrics.server_errors,
    timeout: errorMetrics.timeout_errors,
    connection: errorMetrics.connection_errors,
    api: errorMetrics.api_errors,
    missing_message: errorMetrics.missing_message_errors,
    other: errorMetrics.other_errors,
  };
  (counters[bucket] ?? errorMetrics.other_errors).add(1);
}
