import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { parseSSE } from './types.js';
import { addResponse, okResult } from './types.js';
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
      const threadId = (thread.json() as { thread_id: string }).thread_id;
      url = `${baseUrl}/threads/${threadId}/runs/stream`;
    }

    const response = http.post(url, payload, requestParams);
    addResponse(responses, 'stream', response);
    const events = parseSSE(response.body as string);
    return okResult(responses, { events, rawResponse: response });
  }

  static validate(
    result: BenchmarkResult<StreamWriteData>,
    errorMetrics: ErrorMetrics,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const expected_steps = benchmarkGraphOptions.context.steps;
    const expected_events = getExpectedEvents(benchmarkGraphOptions.context);
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
      const status = result.data?.rawResponse?.status;
      if (status != null && status >= 500) {
        errorMetrics.server_errors.add(1);
      } else if (status === 408) {
        errorMetrics.timeout_errors.add(1);
      } else if (!hasExpectedCounter) {
        if (errorMetrics.missing_message_errors) errorMetrics.missing_message_errors.add(1);
        else errorMetrics.other_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
    }
    return success;
  }

  static toString(): string {
    return 'stream_write';
  }
}
