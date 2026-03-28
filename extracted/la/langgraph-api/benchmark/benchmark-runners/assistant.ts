import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { DEFAULT_GRAPH_ID } from './types.js';
import { addResponse, okResult } from './types.js';
import { logFailure } from './log-failure.js';

type K6Response = ReturnType<typeof http.post> | ReturnType<typeof http.get> | ReturnType<typeof http.del>;

interface AssistantData {
  assistantId: string;
  searchResponse: K6Response;
  getResponse: K6Response;
  patchResponse: K6Response;
  getResponse2: K6Response;
  countResponse: K6Response;
  deleteResponse: K6Response;
}

export class Assistant extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<AssistantData> {
    const graph_id = DEFAULT_GRAPH_ID;
    let metadata: Record<string, string> = {
      description: `Test benchmark assistant ${crypto.randomUUID()}`,
      created_by: 'benchmark',
    };
    const responses: Record<string, import('./types.js').HttpResponse> = {};

    const createPayload = JSON.stringify({ graph_id, metadata });
    const createResponse = http.post(`${baseUrl}/assistants`, createPayload, requestParams);
    addResponse(responses, 'create', createResponse);
    const assistantId = (createResponse.json() as { assistant_id: string }).assistant_id;

    const searchPayload = JSON.stringify({ graph_id, metadata, limit: 1 });
    const searchResponse = http.post(`${baseUrl}/assistants/search`, searchPayload, requestParams);
    addResponse(responses, 'search', searchResponse);

    const getResponse = http.get(`${baseUrl}/assistants/${assistantId}`, requestParams);
    addResponse(responses, 'get', getResponse);

    metadata = { description: `Test benchmark assistant ${crypto.randomUUID()}` };
    const patchPayload = JSON.stringify({ metadata });
    const patchResponse = http.patch(`${baseUrl}/assistants/${assistantId}`, patchPayload, requestParams);
    addResponse(responses, 'patch', patchResponse);

    const getResponse2 = http.get(`${baseUrl}/assistants/${assistantId}`, requestParams);
    addResponse(responses, 'get2', getResponse2);

    const countPayload = JSON.stringify({ graph_id, metadata });
    const countResponse = http.post(`${baseUrl}/assistants/count`, countPayload, requestParams);
    addResponse(responses, 'count', countResponse);

    const deleteResponse = http.del(`${baseUrl}/assistants/${assistantId}`, '{}', requestParams);
    addResponse(responses, 'delete', deleteResponse);

    return okResult(responses, {
      assistantId,
      searchResponse,
      getResponse,
      patchResponse,
      getResponse2,
      countResponse,
      deleteResponse,
    });
  }

  static validate(
    result: BenchmarkResult<AssistantData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    const d = result.data;
    if (!d) {
      logFailure(Assistant.toString(), result);
      errorMetrics.other_errors.add(1);
      return false;
    }
    let success = false;
    try {
      success = check(result, {
        'Search response contains a single assistant': () => (d.searchResponse.json() as unknown[]).length === 1,
        'Search response contains the correct assistant': () =>
          (d.searchResponse.json() as { assistant_id: string }[])[0].assistant_id === d.assistantId,
        'Get response contains the correct assistant': () =>
          (d.getResponse.json() as { assistant_id: string }).assistant_id === d.assistantId,
        'Patch response contains the correct assistant': () =>
          (d.patchResponse.json() as { assistant_id: string }).assistant_id === d.assistantId,
        'Get response 2 contains the correct assistant': () =>
          (d.getResponse2.json() as { assistant_id: string }).assistant_id === d.assistantId,
        'Get response 2 contains the new description': () => {
          const g2 = d.getResponse2.json() as { metadata?: { description?: string } };
          const g1 = d.getResponse.json() as { metadata?: { description?: string } };
          const p = d.patchResponse.json() as { metadata?: { description?: string } };
          return g2.metadata?.description !== g1.metadata?.description && g2.metadata?.description === p.metadata?.description;
        },
        'Get response 2 contains the correct created_by': () =>
          (d.getResponse2.json() as { metadata?: { created_by?: string } }).metadata?.created_by === 'benchmark',
        'Count response contains the correct number of assistants': () =>
          parseInt((d.countResponse.json() as unknown) as string, 10) === 1,
        'Delete response is successful': () => (d.deleteResponse as { status?: number }).status === 204,
      });
    } catch (error) {
      console.log(`Unknown error checking response: ${(error as Error).message}`);
    }
    if (!success) {
      logFailure(Assistant.toString(), result);
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
    return 'assistants';
  }
}
