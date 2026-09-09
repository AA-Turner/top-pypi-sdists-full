import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { parseSSE } from './types.js';
import { addResponse, okResult, failResult } from './types.js';
import { classifyError, recordError } from './classify-error.js';
import { logFailure } from './log-failure.js';
import { getExpectedEvents } from './benchmark_profiles.js';

interface StreamWriteData {
  events: Array<{ event: string; data: unknown }>;
  rawResponse: ReturnType<typeof http.post>;
}

export class StreamWrite extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<StreamWriteData> {
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    let url = `${baseUrl}/runs/stream`;
    const context = benchmarkGraphOptions.context;
    const expand = context.expand;
    const steps = context.steps;
    const payload = JSON.stringify({
      assistant_id: benchmarkGraphOptions.graph_id,
      input: {},
      context: benchmarkGraphOptions.context,
      stream_mode: ['values', 'messages'],
      stream_resumable: benchmarkGraphOptions.resumable,
      config: { recursion_limit: Math.max(expand, steps) + 2 },
    });

    if (benchmarkGraphOptions.stateful) {
      const thread = http.post(`${baseUrl}/threads`, '{}', requestParams);
      addResponse(responses, 'create_thread', thread);
      // Check before parsing. `thread.json()` on a failed create throws, and the
      // throw surfaced as a generic other_error instead of the real cause.
      if (thread.status !== 200) {
        return failResult('create_thread', responses) as BenchmarkResult<StreamWriteData>;
      }
      const threadId = (thread.json() as { thread_id: string }).thread_id;
      url = `${baseUrl}/threads/${threadId}/runs/stream`;
    }

    const response = http.post(url, payload, requestParams);
    addResponse(responses, 'stream', response);
    // Guarded: on a connection failure k6 returns a response whose body is null,
    // and parseSSE would throw out of run(), discarding the responses map that
    // the error classifier needs to see the failure for what it was.
    const events = typeof response.body === 'string' ? parseSSE(response.body) : [];
    return okResult(responses, { events, rawResponse: response });
  }

  static validate(
    result: BenchmarkResult<StreamWriteData>,
    errorMetrics: ErrorMetrics,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const expected_steps = benchmarkGraphOptions.context.steps;
    const expected_events = getExpectedEvents(benchmarkGraphOptions);
    const events = result.data?.events ?? [];
    const hasExpectedCounter = events.some((event) => {
      if (!event?.data || typeof event.data !== 'object') return false;
      const data = event.data as { counter?: unknown };
      return typeof data.counter === 'number' && data.counter >= expected_steps;
    });
    let success = false;
    try {
      success = check(result, {
        'Run completed successfully': () => (result.data?.rawResponse?.status ?? 0) === 200,
        'Response contains events': () => events.length >= expected_events,
        'Response contains metadata event': () => events[0]?.event === 'metadata',
        'Response contains expected counter value': () => hasExpectedCounter,
      });
    } catch (error) {
      console.log(`Unknown error checking result: ${(error as Error).message}`);
    }

    if (!success) {
      logFailure(StreamWrite.toString(), result, {
        extra: `events.length=${events.length} expected_events=${expected_events} expected_steps=${expected_steps} hasExpectedCounter=${hasExpectedCounter}`,
      });
      recordError(
        classifyError({
          response: result.responses?.stream ?? result.responses?.create_thread ?? null,
          missingMessage: !hasExpectedCounter,
        }),
        errorMetrics
      );
    }
    return success;
  }

  static toString(): string {
    return 'stream_write';
  }
}
