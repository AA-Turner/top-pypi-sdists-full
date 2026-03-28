import { WaitWrite } from './wait_write.js';
import { StreamWrite } from './stream_write.js';
import { Assistant } from './assistant.js';
import { Thread } from './thread.js';
import { EnqueuedRunsOrder } from './enqueued_runs_order.js';
import { CancelFirstSecondCompletes } from './cancel_first_second_completes.js';
import { ThreadRunsMetadataSearch } from './thread_runs_metadata_search.js';
import { ThreadsSearchMetadata } from './threads_search_metadata.js';
import { RandomStream } from './random_stream.js';
import { MetaWorkload } from './meta_workload.js';
import type { BenchmarkRunner } from './benchmark-runner.js';

export class Benchmarks {
  static getRunner(type: string): typeof BenchmarkRunner {
    switch (type) {
      case WaitWrite.toString():
        return WaitWrite;
      case StreamWrite.toString():
        return StreamWrite;
      case Assistant.toString():
        return Assistant;
      case Thread.toString():
        return Thread;
      case EnqueuedRunsOrder.toString():
        return EnqueuedRunsOrder;
      case CancelFirstSecondCompletes.toString():
        return CancelFirstSecondCompletes;
      case ThreadRunsMetadataSearch.toString():
        return ThreadRunsMetadataSearch;
      case ThreadsSearchMetadata.toString():
        return ThreadsSearchMetadata;
      case RandomStream.toString():
        return RandomStream;
      case MetaWorkload.toString():
        return MetaWorkload;
      default:
        throw new Error(`Unknown benchmark type: ${type}`);
    }
  }
}
