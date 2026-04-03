import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { JOIN_TIMEOUT } from './types.js';
import { addResponse, failResult, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface CancelFirstSecondCompletesData {
  threadId: string;
  run1Id: string;
  run2Id: string;
  run1Final: { status: string } | null;
  run2: { status: string } | null;
}

export class CancelFirstSecondCompletes extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<CancelFirstSecondCompletesData> {
    const graphId = benchmarkGraphOptions.graph_id;
    const longDelaySec = 3;
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    const joinParams = { ...requestParams, timeout: JOIN_TIMEOUT };
    const baseContext = benchmarkGraphOptions.context;

    const createThreadRes = http.post(`${baseUrl}/threads`, '{}', requestParams);
    addResponse(responses, 'create_thread', createThreadRes);
    if (createThreadRes.status !== 200) {
      return failResult('create_thread', responses) as BenchmarkResult<CancelFirstSecondCompletesData>;
    }
    const threadId = (createThreadRes.json() as { thread_id: string }).thread_id;

    const run1Payload = JSON.stringify({
      assistant_id: graphId,
      input: {},
      context: { ...baseContext, delay: longDelaySec, expand: 1, steps: 1 },
      config: { recursion_limit: 5 },
    });
    const run1Res = http.post(`${baseUrl}/threads/${threadId}/runs`, run1Payload, requestParams);
    addResponse(responses, 'run1', run1Res);
    if (run1Res.status !== 200) {
      return failResult('create_run1', responses) as BenchmarkResult<CancelFirstSecondCompletesData>;
    }
    const run1Id = (run1Res.json() as { run_id: string }).run_id;

    const run2Payload = JSON.stringify({
      assistant_id: graphId,
      input: {},
      context: { ...baseContext, delay: 0, expand: 1, steps: 1 },
      config: { recursion_limit: 5 },
      multitask_strategy: 'enqueue',
    });
    const run2Res = http.post(`${baseUrl}/threads/${threadId}/runs`, run2Payload, requestParams);
    addResponse(responses, 'run2', run2Res);
    if (run2Res.status !== 200) {
      return failResult('create_run2', responses) as BenchmarkResult<CancelFirstSecondCompletesData>;
    }
    const run2Id = (run2Res.json() as { run_id: string }).run_id;

    const cancelRes = http.post(
      `${baseUrl}/threads/${threadId}/runs/${run1Id}/cancel?wait=false`,
      '{}',
      requestParams
    );
    addResponse(responses, 'cancel', cancelRes);
    if (cancelRes.status !== 202 && cancelRes.status !== 200) {
      return failResult('cancel_run1', responses) as BenchmarkResult<CancelFirstSecondCompletesData>;
    }

    const run1GetRes = http.get(`${baseUrl}/threads/${threadId}/runs/${run1Id}/join`, joinParams);
    addResponse(responses, 'join_run1', run1GetRes);
    const run1Final = run1GetRes.status === 200 ? (run1GetRes.json() as { status: string }) : null;

    const run2JoinRes = http.get(`${baseUrl}/threads/${threadId}/runs/${run2Id}/join`, joinParams);
    addResponse(responses, 'join_run2', run2JoinRes);
    if (run2JoinRes.status !== 200) {
      return failResult('join_run2', responses) as BenchmarkResult<CancelFirstSecondCompletesData>;
    }
    const run2 = run2JoinRes.json() as { status: string };

    return okResult(responses, { threadId, run1Id, run2Id, run1Final, run2 });
  }

  static validate(
    result: BenchmarkResult<CancelFirstSecondCompletesData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    if (!result.ok) {
      logFailure(CancelFirstSecondCompletes.toString(), result);
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
      'Run 1 was cancelled or interrupted': () =>
        Boolean(d.run1Final && (d.run1Final.status === 'cancelled' || d.run1Final.status === 'interrupted')),
      'Run 2 completed successfully': () => d.run2?.status === 'success',
    });
    if (!success) {
      logFailure(CancelFirstSecondCompletes.toString(), result);
      errorMetrics.other_errors.add(1);
    }
    return success;
  }

  static toString(): string {
    return 'cancel_first_second_completes';
  }
}
