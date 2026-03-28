import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { DEFAULT_GRAPH_ID, parseSSE } from './types.js';
import { addResponse } from './types.js';
import { logFailure } from './log-failure.js';

interface RandomStreamData {
  events: Array<{ event: string; data: unknown }>;
  rawResponse: ReturnType<typeof http.post>;
  input: Record<string, unknown>;
  threadId: string;
}

export class RandomStream extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<RandomStreamData> {
    const graphId = benchmarkGraphOptions?.graph_id ?? DEFAULT_GRAPH_ID;
    const modes = ['single', 'sequential', 'parallel'];
    const mode = modes[Math.floor(Math.random() * modes.length)];

    let expand = 1;
    let delay = 0;
    // Aim to keep all runs under two minutes
    if (mode === 'single') {
      delay = Math.floor(Math.random() * 31);
    } else if (mode === 'sequential') {
      expand = 5 + Math.floor(Math.random() * 25);
      delay = Math.floor(Math.random() * 6);
    } else {
      expand = 5 + Math.floor(Math.random() * 25);
      delay = Math.floor(Math.random() * 31);
    }

    const input = {
      mode,
      delay,
      expand,
      steps: expand,
      data_size: 100,
    };
    const payload = JSON.stringify({
      assistant_id: graphId,
      input,
      config: { recursion_limit: expand + 2 },
    });
    const responses: Record<string, import('./types.js').HttpResponse> = {};

    const threadRes = http.post(`${baseUrl}/threads`, '{}', requestParams);
    addResponse(responses, 'create_thread', threadRes);
    if (threadRes.status !== 200) {
      return { ok: false, responses };
    }
    const threadId = (threadRes.json() as { thread_id: string }).thread_id;

    const streamParams = { ...requestParams, timeout: '200s' };
    const response = http.post(
      `${baseUrl}/threads/${threadId}/runs/stream`,
      payload,
      streamParams
    );
    addResponse(responses, 'stream', response);
    const events = parseSSE(response.body as string);
    const lastData = events.length > 0 ? (events[events.length - 1].data as Record<string, unknown>) : null;
    const hasError = lastData?.__error__ != null;

    const ok = response.status === 200 && !hasError;
    return { ok, responses, data: { events, rawResponse: response, input, threadId } };
  }

  static validate(
    result: BenchmarkResult<RandomStreamData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    if (!result.ok) {
      logFailure(RandomStream.toString(), result);
      const status = result.responses?.stream?.status;
      if (status != null && status >= 500) {
        errorMetrics.server_errors.add(1);
      } else if (status === 408) {
        errorMetrics.timeout_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
      return false;
    }
    const d = result.data!;
    const success = check(result, {
      'Stream completed with 200': () => d.rawResponse?.status === 200,
      'Received streaming events': () => (d.events?.length ?? 0) >= 2,
      'First event is metadata': () => d.events?.[0]?.event === 'metadata',
      'No error in stream': () => !(d.events ?? []).some((e) => (e.data as Record<string, unknown>)?.__error__),
      'Last event has messages or values': () => {
        const last = d.events?.[d.events.length - 1]?.data as Record<string, unknown> | undefined;
        return Boolean(last && (last.messages != null || last.values != null));
      },
    });
    if (!success) {
      logFailure(RandomStream.toString(), result, { extra: `events.length=${d.events?.length ?? 0}` });
      errorMetrics.other_errors.add(1);
    }
    return success;
  }

  static toString(): string {
    return 'random_stream';
  }
}
