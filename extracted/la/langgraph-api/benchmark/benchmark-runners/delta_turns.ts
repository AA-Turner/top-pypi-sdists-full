import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';
import { Trend } from 'k6/metrics';
import type { BenchmarkResult, BenchmarkGraphOptions, HttpResponse } from './types.js';
import { addResponse, okResult, failResult } from './types.js';
import { classifyError, recordError } from './classify-error.js';
import { logFailure } from './log-failure.js';
import {
  planTurn,
  deltaGuardFailure,
  stateDrift,
  unusableCheckpointSize,
} from './delta-turns-lib.js';
import type { DeltaTurnsOptions, TurnPlan } from './delta-turns-lib.js';

const CHANNEL = 'cumulative_checkpoint';

/** Tagged by depth: VUs ramp in, so clock time is not thread length. */
const turnDuration = new Trend('turn_duration', true);

const TURN_CONFIG: Omit<DeltaTurnsOptions, 'graphId'> = {
  migrateFromGraphId: __ENV.MIGRATE_FROM_GRAPH_ID || '',
  migrateAfter: parseInt(__ENV.MIGRATE_AFTER || '0', 10),
  expectDelta: (__ENV.EXPECT_DELTA || 'true') === 'true',
  verifyEvery: parseInt(__ENV.VERIFY_EVERY || '50', 10),
  bucketSize: parseInt(__ENV.DEPTH_BUCKET || '100', 10),
};

// Each k6 VU runs this module in its own context, so these are per VU.
let threadId: string | null = null;
let turn = 0;

interface DeltaTurnsData {
  rawResponse: ReturnType<typeof http.post>;
  plan: TurnPlan;
  guardFailure: string | null;
  drift: string | null;
}

export class DeltaTurns extends BenchmarkRunner {
  static run(
    baseUrl: string,
    requestParams: Record<string, unknown>,
    benchmarkGraphOptions: BenchmarkGraphOptions
  ): BenchmarkResult<DeltaTurnsData> {
    const responses: Record<string, HttpResponse> = {};

    if (unusableCheckpointSize(benchmarkGraphOptions.context.checkpoint_size)) {
      return failResult('checkpoint_size', responses) as BenchmarkResult<DeltaTurnsData>;
    }

    if (threadId === null) {
      const thread = http.post(`${baseUrl}/threads`, '{}', requestParams);
      addResponse(responses, 'create_thread', thread);
      if (thread.status !== 200) {
        return failResult('create_thread', responses) as BenchmarkResult<DeltaTurnsData>;
      }
      threadId = (thread.json() as { thread_id: string }).thread_id;
      turn = 0;
    }

    turn += 1;
    const plan = planTurn(turn, { ...TURN_CONFIG, graphId: benchmarkGraphOptions.graph_id });
    const payload = JSON.stringify({
      assistant_id: plan.graphId,
      input: {},
      context: { ...benchmarkGraphOptions.context, steps: plan.steps },
      config: { recursion_limit: plan.steps + 2 },
    });

    const startedAt = Date.now();
    const response = http.post(
      `${baseUrl}/threads/${threadId}/runs/wait`,
      payload,
      requestParams
    );
    turnDuration.add(Date.now() - startedAt, { depth: plan.depthBucket });
    addResponse(responses, 'wait', response);

    let guardFailure: string | null = null;
    let drift: string | null = null;
    // A failed body is not state, and comparing against it would report drift
    // on top of the failure that caused it.
    if (response.status === 200 && (plan.guard || plan.verify)) {
      const state = http.get(`${baseUrl}/threads/${threadId}/state`, requestParams);
      addResponse(responses, 'state', state);
      const body = state.status === 200 ? safeJson(state.body) : null;
      if (body === null) {
        guardFailure = plan.guard ? 'state_unreadable' : guardFailure;
        drift = plan.verify ? 'state_unreadable' : drift;
      } else {
        if (plan.guard) {
          guardFailure = deltaGuardFailure(body.metadata, plan.expectDelta);
        }
        if (plan.verify) {
          // `/runs/wait` returns the state values themselves; `/state` nests them.
          drift = stateDrift(safeJson(response.body), body.values, CHANNEL);
        }
      }
    }

    return okResult(responses, { rawResponse: response, plan, guardFailure, drift });
  }

  static validate(
    result: BenchmarkResult<DeltaTurnsData>,
    errorMetrics: ErrorMetrics
  ): boolean {
    const res = result.data?.rawResponse;
    const plan = result.data?.plan;
    const json = res?.status === 200 ? safeJson(res.body) : null;
    let success = false;

    try {
      success = check(result, {
        'Run completed successfully': () => (res?.status ?? 0) === 200,
        'Response contains valid JSON': () => json != null,
        'Response does not contain __error__': () => json?.__error__ === undefined,
        'Run advanced the thread by one turn': () =>
          json == null || plan == null || json.counter === plan.steps,
        'Delta storage is as expected': () => result.data?.guardFailure == null,
        'Cold re-read matches the run': () => result.data?.drift == null,
      });
    } catch (error) {
      console.log(`Unknown error checking result: ${(error as Error).message}`);
    }

    if (!success) {
      const detail = [
        plan ? `turn=${plan.steps} graph=${plan.graphId}` : '',
        res ? `status=${res.status}` : '',
        result.data?.guardFailure ? `guard=${result.data.guardFailure}` : '',
        result.data?.drift ? `drift=${result.data.drift}` : '',
      ]
        .filter(Boolean)
        .join(' ');
      logFailure(DeltaTurns.toString(), result, { extra: detail });
      recordError(
        classifyError({
          response: res ?? result.responses?.create_thread ?? null,
          hasApiError: json?.__error__ !== undefined,
          missingMessage: result.data?.drift != null || result.data?.guardFailure != null,
        }),
        errorMetrics
      );
      // The thread is now at an unknown depth, so later turns would be tagged
      // with a depth they do not have.
      threadId = null;
    }
    return success;
  }

  static toString(): string {
    return 'delta_turns';
  }
}

/** k6 returns a null body on a connection failure. */
function safeJson(body: string | null | ArrayBuffer): Record<string, any> | null {
  if (typeof body !== 'string') return null;
  try {
    const parsed = JSON.parse(body);
    return parsed != null && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}
