import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { DEFAULT_GRAPH_ID, DEFAULT_INPUT, JOIN_TIMEOUT, NUM_ENQUEUED_RUNS } from './types.js';
import { addResponse, failResult, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface EnqueuedRunsOrderData {
  threadId: string;
  runIds: string[];
  completedAt: Array<{ runId: string; status: string; updated_at: string }>;
}

export class EnqueuedRunsOrder extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<EnqueuedRunsOrderData> {
    const graphId = benchmarkGraphOptions?.graph_id ?? DEFAULT_GRAPH_ID;
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    const joinParams = { ...requestParams, timeout: JOIN_TIMEOUT } as Record<string, unknown>;

    const createThreadRes = http.post(`${baseUrl}/threads`, '{}', requestParams);
    addResponse(responses, 'create_thread', createThreadRes);
    if (createThreadRes.status !== 200) {
      return failResult(undefined, responses) as BenchmarkResult<EnqueuedRunsOrderData>;
    }
    const threadId = (createThreadRes.json() as { thread_id: string }).thread_id;

    const runIds: string[] = [];
    for (let i = 0; i < NUM_ENQUEUED_RUNS; i++) {
      const payload = JSON.stringify({
        assistant_id: graphId,
        input: benchmarkGraphOptions?.input ?? DEFAULT_INPUT,
        config: { recursion_limit: 5 },
        multitask_strategy: 'enqueue',
      });
      const createRunRes = http.post(`${baseUrl}/threads/${threadId}/runs`, payload, requestParams);
      addResponse(responses, `create_run_${i}`, createRunRes);
      if (createRunRes.status !== 200) {
        return failResult(`create_run_${i}`, responses) as BenchmarkResult<EnqueuedRunsOrderData>;
      }
      runIds.push((createRunRes.json() as { run_id: string }).run_id);
    }

    const completedAt: EnqueuedRunsOrderData['completedAt'] = [];
    for (let i = 0; i < NUM_ENQUEUED_RUNS; i++) {
      const runId = runIds[i];
      const joinRes = http.get(`${baseUrl}/threads/${threadId}/runs/${runId}/join`, joinParams);
      addResponse(responses, `join_run_${i}`, joinRes);
      if (joinRes.status !== 200) {
        return failResult(`join_run_${i}`, responses) as BenchmarkResult<EnqueuedRunsOrderData>;
      }
      const run = joinRes.json() as { status: string; updated_at: string };
      completedAt.push({ runId, status: run.status, updated_at: run.updated_at });
    }

    return okResult(responses, { threadId, runIds, completedAt });
  }

  static validate(
    result: BenchmarkResult<EnqueuedRunsOrderData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    if (!result.ok) {
      logFailure(EnqueuedRunsOrder.toString(), result);
      const statuses = Object.values(result.responses).map((r) => r.status);
      if (statuses.some((s) => s != null && s >= 500)) {
        errorMetrics.server_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
      return false;
    }
    const d = result.data!;
    const success = check(result, {
      'All runs completed': () => d.completedAt.length === NUM_ENQUEUED_RUNS,
      'All runs succeeded': () => d.completedAt.every((c) => c.status === 'success'),
      'Runs completed in order': () => {
        const times = d.completedAt.map((c) => new Date(c.updated_at).getTime());
        return times[0] <= times[1] && times[1] <= times[2];
      },
    });
    if (!success) {
      logFailure(EnqueuedRunsOrder.toString(), result, {
        extra: `completedAt=${JSON.stringify(d.completedAt)}`,
      });
      errorMetrics.other_errors.add(1);
    }
    return success;
  }

  static toString(): string {
    return 'enqueued_runs_order';
  }
}
