import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import type { BenchmarkResult, BenchmarkGraphOptions, HttpResponse } from './types.js';
import { addResponse, okResult, failResult } from './types.js';
import { classifyError, recordError } from './classify-error.js';
import { logFailure } from './log-failure.js';

interface InterruptResumeData {
  paused: ReturnType<typeof http.post>;
  resumed: ReturnType<typeof http.post>;
  expectedSteps: number;
}

/**
 * Pause a run mid-way and resume it. The virtual user is the human: it answers
 * at once. What is measured is the server's work around the pause: writing the
 * paused checkpoint, and on resume reading the whole thread state back before
 * continuing, which is the most expensive read a delta channel can face.
 */
export class InterruptResume extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<InterruptResumeData> {
    const base = benchmarkGraphOptions.context;
    const context = {
      ...base,
      interrupt_at: base.interrupt_at || Math.max(1, Math.ceil(base.steps / 2)),
    };
    const config = { recursion_limit: Math.max(context.expand, context.steps) + 4 };
    const responses: Record<string, HttpResponse> = {};

    const thread = http.post(`${baseUrl}/threads`, '{}', requestParams);
    addResponse(responses, 'create_thread', thread);
    if (thread.status !== 200) {
      return failResult('create_thread', responses) as BenchmarkResult<InterruptResumeData>;
    }
    const threadId = (thread.json() as { thread_id: string }).thread_id;
    const url = `${baseUrl}/threads/${threadId}/runs/wait`;

    const paused = http.post(
      url,
      JSON.stringify({ assistant_id: benchmarkGraphOptions.graph_id, input: {}, context, config }),
      requestParams
    );
    addResponse(responses, 'pause', paused);
    if (paused.status !== 200) {
      return failResult('pause', responses) as BenchmarkResult<InterruptResumeData>;
    }

    const resumed = http.post(
      url,
      JSON.stringify({
        assistant_id: benchmarkGraphOptions.graph_id,
        command: { resume: true },
        context,
        config,
      }),
      requestParams
    );
    addResponse(responses, 'resume', resumed);
    return okResult(responses, { paused, resumed, expectedSteps: context.steps });
  }

  static validate(
    result: BenchmarkResult<InterruptResumeData>,
    errorMetrics: ErrorMetrics
  ): boolean {
    const data = result.data;
    const pausedJson = safeJson(data?.paused?.body);
    const resumedJson = safeJson(data?.resumed?.body);
    let success = false;
    try {
      success = check(result, {
        'Pause request succeeded': () => (data?.paused?.status ?? 0) === 200,
        'Run paused on an interrupt': () => Array.isArray(pausedJson?.__interrupt__) && pausedJson.__interrupt__.length > 0,
        'Resume request succeeded': () => (data?.resumed?.status ?? 0) === 200,
        'Resumed run finished every step': () =>
          resumedJson != null &&
          resumedJson.__interrupt__ === undefined &&
          resumedJson.__error__ === undefined &&
          resumedJson.counter === data?.expectedSteps,
      });
    } catch (error) {
      console.log(`Unknown error checking result: ${(error as Error).message}`);
    }
    if (!success) {
      logFailure(InterruptResume.toString(), result, {
        extra: `pause=${data?.paused?.status} resume=${data?.resumed?.status} counter=${resumedJson?.counter} expected=${data?.expectedSteps}`,
      });
      recordError(
        classifyError({
          response: data?.resumed ?? data?.paused ?? result.responses?.create_thread ?? null,
          hasApiError: resumedJson?.__error__ !== undefined || pausedJson?.__error__ !== undefined,
          missingMessage: resumedJson != null && resumedJson.counter !== data?.expectedSteps,
        }),
        errorMetrics
      );
    }
    return success;
  }

  static toString(): string {
    return 'interrupt_resume';
  }
}

function safeJson(body: unknown): Record<string, any> | null {
  if (typeof body !== 'string') return null;
  try {
    const parsed = JSON.parse(body);
    return parsed != null && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}
