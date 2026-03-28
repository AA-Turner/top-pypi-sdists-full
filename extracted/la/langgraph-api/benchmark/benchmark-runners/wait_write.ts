import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { DEFAULT_GRAPH_ID } from './types.js';
import { addResponse, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface WaitWriteData {
  rawResponse: ReturnType<typeof http.post>;
}

export class WaitWrite extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<WaitWriteData> {
    const input = benchmarkGraphOptions?.input;
    const expand = input?.expand ?? 1;
    const steps = input?.steps ?? 1;
    let url = `${baseUrl}/runs/wait`;
    const payload = JSON.stringify({
      assistant_id: benchmarkGraphOptions?.graph_id ?? DEFAULT_GRAPH_ID,
      input: benchmarkGraphOptions?.input ?? {},
      config: { recursion_limit: Math.max(expand, steps) + 2 },
    });

    if (benchmarkGraphOptions?.stateful) {
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
    benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    const res = result.data?.rawResponse;
    const input = benchmarkGraphOptions?.input;
    const expected_length = input?.mode === 'single' ? 1 : (input?.expand ?? 1) + 1;
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
      const checks = {
        'Run completed successfully': () => {
          if (res?.status !== 200) return false;
          if (!json || typeof json !== 'object') return false;
          const j = json as Record<string, unknown>;
          if (j.__error__ !== undefined) return false;
          if (j.expand === undefined) return false;
          if (j.messages != null && Array.isArray(j.messages) && j.messages.length !== expected_length) return false;
          return true;
        },
      };
      success = check(result, checks);
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
