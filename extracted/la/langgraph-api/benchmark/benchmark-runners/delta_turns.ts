import { BenchmarkRunner } from './benchmark-runner.js';
import type { ErrorMetrics } from './benchmark-runner.js';
import { check } from 'k6';
import crypto from 'k6/crypto';
import encoding from 'k6/encoding';
import http from 'k6/http';
import { Trend } from 'k6/metrics';
import type { BenchmarkResult, BenchmarkGraphOptions, HttpResponse } from './types.js';
import { addResponse, okResult, failResult } from './types.js';
import { classifyError, recordError } from './classify-error.js';
import { logFailure } from './log-failure.js';
import {
  planTurn,
  deltaGuardFailure,
  digestDrift,
  unusableCheckpointSize,
} from './delta-turns-lib.js';
import type { DeltaTurnsOptions, TurnPlan } from './delta-turns-lib.js';

const PAYLOAD_CHANNELS = [
  'cumulative_checkpoint',
  'payload_2',
  'payload_3',
  'payload_4',
  'payload_5',
  'payload_6',
  'payload_7',
  'payload_8',
] as const;

/** Tagged by depth: VUs ramp in, so clock time is not thread length. */
const turnDuration = new Trend('turn_duration', true);
/** The read path alone: a cold GET /state replays the channel without writing. */
const stateReadDuration = new Trend('state_read_duration', true);
const checkpointSaveDuration = new Trend('checkpoint_save', true);
const threadStorageBytes = new Trend('thread_storage_bytes', false);

const TURN_CONFIG: Omit<DeltaTurnsOptions, 'graphId'> = {
  migrateFromGraphId: __ENV.MIGRATE_FROM_GRAPH_ID || '',
  migrateAfter: parseInt(__ENV.MIGRATE_AFTER || '0', 10),
  expectDelta: (__ENV.EXPECT_DELTA || 'true') === 'true',
  verifyEvery: parseInt(__ENV.VERIFY_EVERY || '50', 10),
  // One bucket per cold read, so every row of the report is one sample per thread.
  bucketSize: parseInt(__ENV.DEPTH_BUCKET || __ENV.VERIFY_EVERY || '50', 10),
};

// Each k6 VU runs this module in its own context, so these are per VU.
let threadId: string | null = null;
let turn = 0;

interface DeltaTurnsData {
  rawResponse: ReturnType<typeof http.post>;
  plan: TurnPlan;
  guardFailure: string | null;
  drift: string | null;
  /** Non-200 status of the cold state read, which is a failed request, not a correctness failure. */
  stateStatus: number | null;
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
      // The graph times its own checkpoint save as the gap between its two
      // steps; a background save would overlap the second step and hide in it.
      durability: 'sync',
    });

    const startedAt = Date.now();
    const response = http.post(
      `${baseUrl}/threads/${threadId}/runs/wait`,
      payload,
      requestParams
    );
    turnDuration.add(Date.now() - startedAt, { depth: plan.depthBucket });
    addResponse(responses, 'wait', response);
    const saveMs = response.status === 200 ? safeJson(response.body)?.save_ms : null;
    if (typeof saveMs === 'number' && saveMs > 0) {
      // Snapshots land on multiples of the bucket width, so the bucket's last
      // turn is where a snapshot save shows; a percentile over the bucket hides it.
      const rowTurn = plan.steps % TURN_CONFIG.bucketSize === 0 ? '1' : '0';
      checkpointSaveDuration.add(saveMs, { depth: plan.depthBucket, row_turn: rowTurn });
    }

    let guardFailure: string | null = null;
    let drift: string | null = null;
    let stateStatus: number | null = null;
    // A failed body is not state, and comparing against it would report drift
    // on top of the failure that caused it.
    if (response.status === 200 && (plan.guard || plan.verify)) {
      const state = http.get(`${baseUrl}/threads/${threadId}/state`, requestParams);
      // Time to first byte: the server cannot start answering before it has
      // rebuilt the value, and the body that follows is the whole state, which
      // at depth is hundreds of KB the turn itself never sends. Wall time made
      // a plain-channel read cost as much as a whole turn. The turn-2 guard
      // read is at depth 2, not the bucket's end, so it is not timed.
      if (state.status === 200 && plan.verify) {
        stateReadDuration.add(state.timings.waiting, { depth: plan.depthBucket });
      }
      addResponse(responses, 'state', state);
      const body = state.status === 200 ? safeJson(state.body) : null;
      if (state.status !== 200) {
        stateStatus = state.status;
      } else if (body === null) {
        guardFailure = plan.guard ? 'state_unreadable' : guardFailure;
        drift = plan.verify ? 'state_unreadable' : drift;
      } else {
        if (plan.guard) {
          guardFailure = deltaGuardFailure(body.metadata, plan.expectDelta);
        }
        if (plan.verify) {
          drift = digestDrift(safeJson(response.body)?.payload_sha256, coldDigest(body.values));
        }
      }
      if (plan.verify) {
        // Servers before 0.16 have no storage endpoint. A 404 there is a missing
        // sample, not a failed request: without this, one 404 per 50 turns is
        // about 2% and trips the 1% error budget on every cell.
        const storage = http.get(`${baseUrl}/threads/${threadId}/storage`, {
          ...requestParams,
          responseCallback: http.expectedStatuses(200, 404),
        });
        addResponse(responses, 'storage', storage);
        const total = storage.status === 200 ? safeJson(storage.body)?.total_bytes : null;
        if (typeof total === 'number') {
          threadStorageBytes.add(total, { depth: plan.depthBucket, graph: plan.graphId });
        }
      }
    }

    return okResult(responses, { rawResponse: response, plan, guardFailure, drift, stateStatus });
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
        'Cold state read succeeded': () => result.data?.stateStatus == null,
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
        result.data?.stateStatus ? `state_status=${result.data.stateStatus}` : '',
        result.data?.guardFailure ? `guard=${result.data.guardFailure}` : '',
        result.data?.drift ? `drift=${result.data.drift}` : '',
      ]
        .filter(Boolean)
        .join(' ');
      logFailure(DeltaTurns.toString(), result, { extra: detail });
      recordError(
        classifyError({
          response: result.data?.stateStatus
            ? result.responses?.state ?? null
            : res ?? result.responses?.create_thread ?? null,
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

function coldDigest(values: Record<string, unknown> | undefined): string | null {
  if (values == null || typeof values !== 'object') return null;
  // Reproduce the graph's payload_digest: every bytes channel in order, then
  // the concatenated message contents. Absent channels default to empty, so
  // they add nothing, exactly as the unwritten bytes channels do server-side.
  const hasher = crypto.createHash('sha256');
  for (const name of PAYLOAD_CHANNELS) {
    const stored = values[name];
    if (typeof stored === 'string' && stored.length > 0) {
      hasher.update(encoding.b64decode(stored));
    }
  }
  const messages = values.messages;
  if (Array.isArray(messages) && messages.length > 0) {
    hasher.update(messages.map((m) => String((m as { content?: unknown })?.content ?? '')).join(''));
  }
  return hasher.digest('hex');
}
