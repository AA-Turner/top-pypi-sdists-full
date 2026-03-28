import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { DEFAULT_GRAPH_ID, DEFAULT_INPUT, JOIN_TIMEOUT } from './types.js';
import { addResponse, failResult, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface ThreadRunsMetadataSearchData {
  threadId: string;
  runId: string;
  runs: Array<{ run_id: string; metadata?: { scenario?: string } }>;
}

export class ThreadRunsMetadataSearch extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<ThreadRunsMetadataSearchData> {
    const graphId = benchmarkGraphOptions?.graph_id ?? DEFAULT_GRAPH_ID;
    const tag = `bench-metadata-${crypto.randomUUID()}`;
    const threadMetadata = { scenario: 'thread_runs_metadata_search', tag };
    const runMetadata = { scenario: 'thread_runs_metadata_search', tag };
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    const joinParams = { ...requestParams, timeout: JOIN_TIMEOUT } as Record<string, unknown>;

    const createThreadRes = http.post(
      `${baseUrl}/threads`,
      JSON.stringify({ metadata: threadMetadata }),
      requestParams
    );
    addResponse(responses, 'create_thread', createThreadRes);
    if (createThreadRes.status !== 200) {
      return failResult(undefined, responses) as BenchmarkResult<ThreadRunsMetadataSearchData>;
    }
    const threadId = (createThreadRes.json() as { thread_id: string }).thread_id;

    const payload = JSON.stringify({
      assistant_id: graphId,
      input: benchmarkGraphOptions?.input ?? DEFAULT_INPUT,
      config: { recursion_limit: 5 },
      metadata: runMetadata,
    });
    const createRunRes = http.post(`${baseUrl}/threads/${threadId}/runs`, payload, requestParams);
    addResponse(responses, 'create_run', createRunRes);
    if (createRunRes.status !== 200) {
      return failResult('create_run', responses) as BenchmarkResult<ThreadRunsMetadataSearchData>;
    }
    const runId = (createRunRes.json() as { run_id: string }).run_id;

    const joinRes = http.get(`${baseUrl}/threads/${threadId}/runs/${runId}/join`, joinParams);
    addResponse(responses, 'join_run', joinRes);
    if (joinRes.status !== 200) {
      return failResult('join_run', responses) as BenchmarkResult<ThreadRunsMetadataSearchData>;
    }

    const listRes = http.get(`${baseUrl}/threads/${threadId}/runs?limit=10`, requestParams);
    addResponse(responses, 'list_runs', listRes);
    if (listRes.status !== 200) {
      return failResult(undefined, responses) as BenchmarkResult<ThreadRunsMetadataSearchData>;
    }
    const runs = listRes.json() as ThreadRunsMetadataSearchData['runs'];

    return okResult(responses, { threadId, runId, runs });
  }

  static validate(
    result: BenchmarkResult<ThreadRunsMetadataSearchData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    if (!result.ok) {
      logFailure(ThreadRunsMetadataSearch.toString(), result);
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
      'List returns at least 1 run': () => d.runs.length >= 1,
      'Listed runs include our run id': () => {
        const ids = new Set(d.runs.map((run) => run.run_id));
        return ids.has(d.runId);
      },
      'Run has metadata': () => {
        const byId = Object.fromEntries(d.runs.map((run) => [run.run_id, run]));
        return byId[d.runId]?.metadata?.scenario === 'thread_runs_metadata_search';
      },
    });
    if (!success) {
      logFailure(ThreadRunsMetadataSearch.toString(), result, {
        extra: `runs.length=${d.runs.length} runId=${d.runId}`,
      });
      errorMetrics.other_errors.add(1);
    }
    return success;
  }

  static toString(): string {
    return 'thread_runs_metadata_search';
  }
}
