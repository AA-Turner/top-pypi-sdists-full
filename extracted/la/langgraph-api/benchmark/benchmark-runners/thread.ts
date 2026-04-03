import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { addResponse, okResult } from './types.js';
import { logFailure } from './log-failure.js';

type K6Response = ReturnType<typeof http.post> | ReturnType<typeof http.get> | ReturnType<typeof http.del>;

interface ThreadData {
  threadId: string;
  searchResponse: K6Response;
  getResponse: K6Response;
  patchResponse: K6Response;
  getResponse2: K6Response;
  countResponse: K6Response;
  deleteResponse: K6Response;
}

export class Thread extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    _benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<ThreadData> {
    const responses: Record<string, import('./types.js').HttpResponse> = {};
    let metadata: Record<string, string> = {
      description: `Test benchmark thread ${crypto.randomUUID()}`,
    };

    const createPayload = JSON.stringify({ metadata });
    const createResponse = http.post(`${baseUrl}/threads`, createPayload, requestParams);
    addResponse(responses, 'create', createResponse);
    const threadId = (createResponse.json() as { thread_id: string }).thread_id;

    const searchPayload = JSON.stringify({ metadata, limit: 1 });
    const searchResponse = http.post(`${baseUrl}/threads/search`, searchPayload, requestParams);
    addResponse(responses, 'search', searchResponse);

    const getResponse = http.get(`${baseUrl}/threads/${threadId}`, requestParams);
    addResponse(responses, 'get', getResponse);

    metadata = { description: `Test benchmark thread ${crypto.randomUUID()}` };
    const patchPayload = JSON.stringify({ metadata });
    const patchResponse = http.patch(`${baseUrl}/threads/${threadId}`, patchPayload, requestParams);
    addResponse(responses, 'patch', patchResponse);

    const getResponse2 = http.get(`${baseUrl}/threads/${threadId}`, requestParams);
    addResponse(responses, 'get2', getResponse2);

    const countPayload = JSON.stringify({ metadata });
    const countResponse = http.post(`${baseUrl}/threads/count`, countPayload, requestParams);
    addResponse(responses, 'count', countResponse);

    const deleteResponse = http.del(`${baseUrl}/threads/${threadId}`, '{}', requestParams);
    addResponse(responses, 'delete', deleteResponse);

    return okResult(responses, {
      threadId,
      searchResponse,
      getResponse,
      patchResponse,
      getResponse2,
      countResponse,
      deleteResponse,
    });
  }

  static validate(
    result: BenchmarkResult<ThreadData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const d = result.data;
    if (!d) {
      logFailure(Thread.toString(), result);
      errorMetrics.other_errors.add(1);
      return false;
    }
    let success = false;
    try {
      success = check(result, {
        'Search response contains a single thread': () => (d.searchResponse.json() as unknown[]).length === 1,
        'Search response contains the correct thread': () =>
          (d.searchResponse.json() as { thread_id: string }[])[0].thread_id === d.threadId,
        'Get response contains the correct thread': () =>
          (d.getResponse.json() as { thread_id: string }).thread_id === d.threadId,
        'Patch response contains the correct thread': () =>
          (d.patchResponse.json() as { thread_id: string }).thread_id === d.threadId,
        'Get response 2 contains the correct thread': () =>
          (d.getResponse2.json() as { thread_id: string }).thread_id === d.threadId,
        'Get response 2 contains the new description': () => {
          const g2 = d.getResponse2.json() as { metadata?: { description?: string } };
          const g1 = d.getResponse.json() as { metadata?: { description?: string } };
          const p = d.patchResponse.json() as { metadata?: { description?: string } };
          return g2.metadata?.description !== g1.metadata?.description && g2.metadata?.description === p.metadata?.description;
        },
        'Count response contains the correct number of threads': () =>
          parseInt((d.countResponse.json() as unknown) as string, 10) === 1,
        'Delete response is successful': () => (d.deleteResponse as { status?: number }).status === 204,
      });
    } catch (error) {
      console.log(`Unknown error checking response: ${(error as Error).message}`);
    }
    if (!success) {
      logFailure(Thread.toString(), result);
      const statuses = [d.searchResponse, d.getResponse, d.patchResponse, d.getResponse2, d.countResponse, d.deleteResponse]
        .map((r) => (r as { status?: number }).status);
      if (statuses.some((s) => s === 502)) {
        errorMetrics.server_errors.add(1);
      } else if (statuses.some((s) => s === 408)) {
        errorMetrics.timeout_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
    }
    return success;
  }

  static toString(): string {
    return 'threads';
  }
}
