// No k6 imports here, so `node --test` can import the compiled output.

export interface DeltaTurnsOptions {
  graphId: string;
  /** Drives the first `migrateAfter` turns. Empty disables migration. */
  migrateFromGraphId: string;
  migrateAfter: number;
  /** Whether `graphId` is delta-backed. */
  expectDelta: boolean;
  /** Cold re-read cadence, in turns. 0 disables. */
  verifyEvery: number;
  bucketSize: number;
}

export interface TurnPlan {
  graphId: string;
  /** Cumulative on a reused thread, so turn N asks for N. */
  steps: number;
  expectDelta: boolean;
  guard: boolean;
  verify: boolean;
  depthBucket: string;
}

const DELTA_COUNTERS_KEY = 'counters_since_delta_snapshot';

/** At size 0 the thread deepens but the channel stays empty, measuring nothing. */
export function unusableCheckpointSize(checkpointSize: number | undefined): boolean {
  return !(typeof checkpointSize === 'number' && checkpointSize > 0);
}

export function planTurn(turn: number, options: DeltaTurnsOptions): TurnPlan {
  const migrating = options.migrateFromGraphId !== '' && options.migrateAfter > 0;
  const beforeSwitch = migrating && turn <= options.migrateAfter;
  return {
    graphId: beforeSwitch ? options.migrateFromGraphId : options.graphId,
    steps: turn,
    expectDelta: beforeSwitch ? false : options.expectDelta,
    guard: isGuardTurn(turn, options, migrating),
    verify: options.verifyEvery > 0 && turn % options.verifyEvery === 0,
    depthBucket: depthBucket(turn, options.bucketSize),
  };
}

/**
 * Turn 1 has no counters yet, and on a snapshot point Pregel drops the counters
 * entry, so its absence there is correct rather than a fallback.
 */
function isGuardTurn(turn: number, options: DeltaTurnsOptions, migrating: boolean): boolean {
  if (turn === 2) return true;
  return migrating && turn === options.migrateAfter + 2;
}

function depthBucket(turn: number, bucketSize: number): string {
  if (bucketSize <= 0) return String(turn);
  const floor = Math.floor((turn - 1) / bucketSize) * bucketSize;
  return `${floor + 1}-${floor + bucketSize}`;
}

/**
 * The delta import is version-guarded and its stub degrades to a plain channel,
 * so without this a delta cell can silently measure the control graph.
 */
export function deltaGuardFailure(metadata: unknown, expectDelta: boolean): string | null {
  const counters =
    metadata != null && typeof metadata === 'object'
      ? (metadata as Record<string, unknown>)[DELTA_COUNTERS_KEY]
      : undefined;
  const present = counters != null && Object.keys(counters as object).length > 0;
  if (expectDelta && !present) return 'delta_off_on_delta_graph';
  if (!expectDelta && present) return 'delta_on_on_plain_graph';
  return null;
}

/**
 * Delta bugs return the right answer live and lose it on the next read, so the
 * run's own output is the reference and the stored value is under test.
 */
export function stateDrift(
  runValues: unknown,
  coldValues: unknown,
  channel: string
): string | null {
  if (runValues == null || typeof runValues !== 'object') return 'run_values_missing';
  if (coldValues == null || typeof coldValues !== 'object') return 'cold_values_missing';
  const live = runValues as Record<string, unknown>;
  const cold = coldValues as Record<string, unknown>;

  if (live.counter !== cold.counter) {
    return `counter_drift:${String(live.counter)}!=${String(cold.counter)}`;
  }
  const liveEnc = encodeChannel(live[channel]);
  const coldEnc = encodeChannel(cold[channel]);
  if (liveEnc !== coldEnc) return `channel_drift:${liveEnc}!=${coldEnc}`;
  return null;
}

/** Bytes arrive as a string, other channels as objects. */
function encodeChannel(value: unknown): string {
  if (value == null) return '';
  return typeof value === 'string' ? value : JSON.stringify(value);
}
