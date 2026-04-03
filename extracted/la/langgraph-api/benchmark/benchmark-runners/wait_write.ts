import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { addResponse, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface WaitWriteData {
  rawResponse: ReturnType<typeof http.post>;
}

export class WaitWrite extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<WaitWriteData> {
    const context = benchmarkGraphOptions.context;
    const expand = context.expand;
    const steps = context.steps;
    let url = `${baseUrl}/runs/wait`;
    const payload = JSON.stringify({
      assistant_id: benchmarkGraphOptions.graph_id,
      input: {},
      context: benchmarkGraphOptions.context,
      config: { recursion_limit: Math.max(expand, steps) + 2 },
    });

    if (benchmarkGraphOptions.stateful) {
      const thread = http.post(`${baseUrl}/threads`, '{}', requestParams);
      const threadId = (thread.json() as { thread_id: string }).thread_id;
      url = `${baseUrl}/threads/${threadId}/runs/wait`;
    }

    const response = http.post(url, payload, requestParams);
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    addResponse(responses, 'wait', response);
    return okResult(responses, { rawResponse: response });
  }

  static validate(
    result: BenchmarkResult<WaitWriteData>,
    errorMetrics: ErrorMetrics,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const res = result.data?.rawResponse;
    const expected_steps = benchmarkGraphOptions.context.steps;
    let success = false;
    let json: unknown = null;
    if (res?.status === 200) {
      try {
        json = res.json();
      } catch {
        console.error('JSON response parsing failed');
      }
    }

    try {
      success = check(result, {
        'Run completed successfully': () => (res?.status ?? 0) === 200,
        'Response contains valid JSON': () => json != null && typeof json === 'object',
        'Response does not contain __error__': () =>
          !json || typeof json !== 'object' || (json as Record<string, unknown>).__error__ === undefined,
        'Response contains expected number of steps': () =>
          !json ||
          typeof json !== 'object' ||
          (() => {
            const counter = (json as Record<string, unknown>).counter;
            return typeof counter !== 'number' || counter === expected_steps;
          })(),
      });
    } catch (error) {
      console.log(`Unknown error checking result: ${(error as Error).message}`);
    }

    if (!success) {
      logFailure(WaitWrite.toString(), result, { extra: `status=${res?.status}` });
      if (res?.status != null && res.status >= 500) {
        errorMetrics.server_errors.add(1);
      } else if (res?.status === 408 || (res as { error?: string }).error?.includes('timeout')) {
        errorMetrics.timeout_errors.add(1);
      } else if (json && typeof json === 'object' && (json as Record<string, unknown>).__error__) {
        if (errorMetrics.api_errors) errorMetrics.api_errors.add(1);
        else errorMetrics.other_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
    }
    return success;
  }

  static toString(): string {
    return 'wait_write';
  }
}
