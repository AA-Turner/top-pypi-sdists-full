import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { logFailure } from './log-failure.js';
import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';
import { WaitWrite } from './wait_write.js';
import { StreamWrite } from './stream_write.js';
import { Assistant } from './assistant.js';
import { Thread } from './thread.js';
import { EnqueuedRunsOrder } from './enqueued_runs_order.js';
import { CancelFirstSecondCompletes } from './cancel_first_second_completes.js';
import { ThreadRunsMetadataSearch } from './thread_runs_metadata_search.js';
import { ThreadsSearchMetadata } from './threads_search_metadata.js';

const OTHER_RUNNERS = [
  WaitWrite,
  StreamWrite,
  Assistant,
  Thread,
  EnqueuedRunsOrder,
  CancelFirstSecondCompletes,
  ThreadRunsMetadataSearch,
  ThreadsSearchMetadata,
];

interface MetaWorkloadData {
  type: string;
  result: BenchmarkResult;
  Runner: typeof BenchmarkRunner;
}

export class MetaWorkload extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<MetaWorkloadData> {
    const Runner = OTHER_RUNNERS[Math.floor(Math.random() * OTHER_RUNNERS.length)];
    const innerResult = Runner.run(baseUrl, requestParams, benchmarkGraphOptions) as BenchmarkResult;
    return {
      ok: innerResult.ok,
      step: innerResult.step,
      responses: innerResult.responses,
      data: { type: Runner.toString(), result: innerResult, Runner },
    };
  }

  static validate(
    result: BenchmarkResult<MetaWorkloadData>,
    errorMetrics: ErrorMetrics,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): boolean {
    const d = result.data;
    if (!d) {
      logFailure(MetaWorkload.toString(), result);
      errorMetrics.other_errors.add(1);
      return false;
    }
    const success = d.Runner.validate(d.result, errorMetrics, benchmarkGraphOptions);
    if (!success) {
      logFailure(MetaWorkload.toString(), result, { extra: `delegated_runner=${d.type}` });
    }
    return success;
  }

  static toString(): string {
    return 'meta_workload';
  }
}
