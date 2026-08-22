import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { addResponse, okResult } from './types.js';
import { logFailure } from './log-failure.js';

const DEFAULT_STORE_VALUE_SIZE = 1024 * 1024;
const STORE_NAMESPACE = ['benchmark'];

type K6Response = ReturnType<typeof http.put> | ReturnType<typeof http.get> | ReturnType<typeof http.del>;

interface StoreData {
  key: string;
  expectedPayload: string;
  payloadSize: number;
  putResponse?: K6Response;
  getResponse?: K6Response;
  deleteResponse?: K6Response;
}

interface StoreItem {
  value?: {
    marker?: string;
    payload?: string;
  };
}

export class Store extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<StoreData> {
    const key = crypto.randomUUID();
    const payloadSize = benchmarkGraphOptions.context.store_value_size ?? DEFAULT_STORE_VALUE_SIZE;
    if (!Number.isInteger(payloadSize) || payloadSize <= 0) {
      throw new Error(`STORE_VALUE_SIZE must be a positive integer, got ${payloadSize}`);
    }

    const responses: Record<string, import('./types.js').HttpResponse> = {};
    const expectedPayload = 'x'.repeat(payloadSize);
    const putPayload = JSON.stringify({
      namespace: STORE_NAMESPACE,
      key,
      value: { marker: key, payload: expectedPayload },
      index: false,
    });
    let putResponse: K6Response | undefined;
    let getResponse: K6Response | undefined;
    let deleteResponse: K6Response | undefined;

    try {
      putResponse = http.put(`${baseUrl}/store/items`, putPayload, requestParams);
      addResponse(responses, 'put', putResponse);

      const namespace = encodeURIComponent(STORE_NAMESPACE.join('.'));
      getResponse = http.get(
        `${baseUrl}/store/items?namespace=${namespace}&key=${encodeURIComponent(key)}`,
        requestParams
      );
      addResponse(responses, 'get', getResponse);
    } finally {
      const deletePayload = JSON.stringify({ namespace: STORE_NAMESPACE, key });
      deleteResponse = http.del(`${baseUrl}/store/items`, deletePayload, requestParams);
      addResponse(responses, 'delete', deleteResponse);
    }

    return okResult(responses, {
      key,
      expectedPayload,
      payloadSize,
      putResponse,
      getResponse,
      deleteResponse,
    });
  }

  static validate(
    result: BenchmarkResult<StoreData>,
    errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const data = result.data;
    if (!data) {
      logFailure(Store.toString(), result);
      errorMetrics.other_errors.add(1);
      return false;
    }

    let item: StoreItem | null = null;
    if (data.getResponse?.status === 200) {
      try {
        item = data.getResponse.json() as StoreItem;
      } catch {
        item = null;
      }
    }

    const success = check(result, {
      'Store put response is successful': () => data.putResponse?.status === 204,
      'Store get response is successful': () => data.getResponse?.status === 200,
      'Store get response contains the correct item': () => item?.value?.marker === data.key,
      'Store get response contains the exact payload': () => item?.value?.payload === data.expectedPayload,
      'Store delete response is successful': () => data.deleteResponse?.status === 204,
    });

    if (!success) {
      logFailure(Store.toString(), result, { extra: `key=${data.key} payload_size=${data.payloadSize}` });
      const statuses = [data.putResponse, data.getResponse, data.deleteResponse].map((response) => response?.status);
      if (statuses.some((status) => status != null && status >= 500)) {
        errorMetrics.server_errors.add(1);
      } else if (statuses.some((status) => status === 408)) {
        errorMetrics.timeout_errors.add(1);
      } else {
        errorMetrics.other_errors.add(1);
      }
    }
    return success;
  }

  static toString(): string {
    return 'store';
  }
}
