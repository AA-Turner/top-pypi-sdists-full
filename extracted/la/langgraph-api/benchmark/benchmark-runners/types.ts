/**
 * Normalized HTTP response summary for consistent logging across benchmarks.
 * All runners should put their HTTP responses here (via toHttpResponse).
 */
export interface HttpResponse {
  status?: number;
  error?: string;
  body?: string;
}

/**
 * Every benchmark run returns this shape. Runner-specific payload goes in `data`.
 */
export interface BenchmarkResult<T = unknown> {
  ok: boolean;
  /** Set when ok is false to indicate which step failed */
  step?: string;
  /** Named HTTP response summaries for logFailure to log */
  responses: Record<string, HttpResponse>;
  /** Runner-specific payload (events, ids, etc.) */
  data?: T;
}

/** Default assistant/graph id for benchmark runs */
export const DEFAULT_GRAPH_ID = 'benchmark';

/** Timeout for a single run join. */
export const JOIN_TIMEOUT = '90s';

/** Number of runs to enqueue in enqueued_runs_order benchmark. */
export const NUM_ENQUEUED_RUNS = 3;

/** Default benchmark context for graph runs. */
export interface BenchmarkContext {
  delay: number;
  delay_jitter_ratio: number;
  expand: number;
  steps: number;
  checkpoint_size: number;
  llm_enabled: boolean;
  stream_size: number;
  chunk_size: number;
  burst_mode: boolean;
  burst_probability: number;
  burst_size: number;
}

/**
 * Options passed to run() from the ramp/capacity scripts.
 */
export interface BenchmarkGraphOptions {
  graph_id: string;
  context: BenchmarkContext;
  stateful: boolean;
  resumable: boolean;
}

/** k6-style response (has status, error, body). */
interface K6ResponseLike {
  status?: number;
  error?: string;
  body?: string | unknown;
}

const MAX_BODY_LEN = 400;

/**
 * Normalize a k6 (or similar) response into HttpResponse for logging.
 */
export function toHttpResponse(res: K6ResponseLike | null | undefined): HttpResponse {
  if (res == null || typeof res !== 'object') {
    return {};
  }
  let body: string | undefined;
  const b = res.body;
  if (typeof b === 'string') {
    body = b.length > MAX_BODY_LEN ? b.substring(0, MAX_BODY_LEN) + '...' : b;
  }
  return {
    status: res.status,
    error: res.error,
    body,
  };
}

/**
 * Add a response into the responses map. Use in runners: addResponse(responses, 'create', createRes)
 */
export function addResponse(
  responses: Record<string, HttpResponse>,
  name: string,
  res: K6ResponseLike | null | undefined
): void {
  responses[name] = toHttpResponse(res);
}

/**
 * Build a failure result with optional step and responses for logging.
 */
export function failResult(
  step?: string,
  responses: Record<string, HttpResponse> = {}
): BenchmarkResult<unknown> {
  return { ok: false, step, responses };
}

/**
 * Build a success result with responses and optional data.
 */
export function okResult<T>(
  responses: Record<string, HttpResponse>,
  data?: T
): BenchmarkResult<T> {
  return { ok: true, responses, data };
}

/**
 * Helper function to parse SSE text into events.
 * @param text - The SSE text to parse.
 * @returns The parsed events.
 */
export function parseSSE(text: string): Array<{ event: string; data: unknown }> {
  const events: Array<{ event: string; data: unknown }> = [];
  const lines = text.split('\r\n');
  let currentEvent = { event: '', data: '' as string };

  for (const line of lines) {
    if (line.startsWith('event:')) {
      currentEvent.event = line.substring(6).trim();
    } else if (line.startsWith('data:')) {
      currentEvent.data = line.substring(5).trim();
    } else if (line === '') {
      if (currentEvent.data) {
        try {
          events.push({ event: currentEvent.event, data: JSON.parse(currentEvent.data) });
        } catch {
          events.push({ event: currentEvent.event, data: currentEvent.data });
        }
      }
      currentEvent = { event: '', data: '' };
    }
  }
  return events;
}
