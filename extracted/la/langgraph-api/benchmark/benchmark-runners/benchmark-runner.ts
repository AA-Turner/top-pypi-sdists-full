import type { BenchmarkResult, BenchmarkGraphOptions } from './types.js';

export interface ErrorMetrics {
  server_errors: { add(n: number): void };
  timeout_errors: { add(n: number): void };
  api_errors?: { add(n: number): void };
  missing_message_errors?: { add(n: number): void };
  other_errors: { add(n: number): void };
}

/**
 * Abstract base for benchmark runners. All runners return BenchmarkResult
 * and validate() receives that same shape.
 */
export abstract class BenchmarkRunner {
  static run(
    _baseUrl: string,
    _requestParams: Record<string, unknown>,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): BenchmarkResult<unknown> {
    throw new Error('Not implemented');
  }

  static toString(): string {
    throw new Error('Not implemented');
  }

  static validate(
    _result: BenchmarkResult<unknown>,
    _errorMetrics: ErrorMetrics,
    _benchmarkGraphOptions?: BenchmarkGraphOptions
  ): boolean {
    throw new Error('Not implemented');
  }
}
