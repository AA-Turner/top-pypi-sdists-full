import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { addResponse, failResult, okResult } from './types.js';
import { logFailure } from './log-failure.js';

interface ThreadsSearchMetadataData {
  threadIds: string[];
  searchMetadata: { scenario: string; tag: string };
  found: Array<{ thread_id: string; metadata?: { scenario?: string; tag?: string } }>;
}

export class ThreadsSearchMetadata extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<ThreadsSearchMetadataData> {
    const tag = `bench-search-${crypto.randomUUID()}`;
    const searchMetadata = { scenario: 'threads_search_metadata', tag };
    const responses: Record<string, import('./types.js').HttpResponse> = {};

    const threadIds: string[] = [];
    for (let i = 0; i < 2; i++) {
      const createRes = http.post(`${baseUrl}/threads`, '{}', requestParams);
      addResponse(responses, `create_thread_${i}`, createRes);
      if (createRes.status !== 200) {
        return failResult(`create_thread_${i}`, responses) as BenchmarkResult<ThreadsSearchMetadataData>;
      }
      threadIds.push((createRes.json() as { thread_id: string }).thread_id);
    }

    for (let i = 0; i < 2; i++) {
      const patchPayload = JSON.stringify({ metadata: { ...searchMetadata, index: i } });
      const patchRes = http.patch(`${baseUrl}/threads/${threadIds[i]}`, patchPayload, requestParams);
      addResponse(responses, `patch_thread_${i}`, patchRes);
      if (patchRes.status !== 200) {
        return failResult(`patch_thread_${i}`, responses) as BenchmarkResult<ThreadsSearchMetadataData>;
      }
    }

    const searchPayload = JSON.stringify({ metadata: searchMetadata, limit: 10 });
    const searchRes = http.post(`${baseUrl}/threads/search`, searchPayload, requestParams);
    addResponse(responses, 'search', searchRes);
    if (searchRes.status !== 200) {
      return failResult(undefined, responses) as BenchmarkResult<ThreadsSearchMetadataData>;
    }
    const found = searchRes.json() as ThreadsSearchMetadataData['found'];

    return okResult(responses, { threadIds, searchMetadata, found });
  }

  static validate(
    result: BenchmarkResult<ThreadsSearchMetadataData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    if (!result.ok) {
      logFailure(ThreadsSearchMetadata.toString(), result);
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
      'Search returns at least 2 threads': () => d.found.length >= 2,
      'Search returns our threads': () => {
        const ids = new Set(d.found.map((t) => t.thread_id));
        return d.threadIds.every((id) => ids.has(id));
      },
      'Found threads have search metadata': () =>
        d.found.every(
          (t) =>
            t.metadata?.scenario === 'threads_search_metadata' && t.metadata?.tag === d.searchMetadata.tag
        ),
    });
    if (!success) {
      logFailure(ThreadsSearchMetadata.toString(), result, {
        extra: `found.length=${d.found.length} threadIds=${JSON.stringify(d.threadIds)}`,
      });
      errorMetrics.other_errors.add(1);
    }
    return success;
  }

  static toString(): string {
    return 'threads_search_metadata';
  }
}
