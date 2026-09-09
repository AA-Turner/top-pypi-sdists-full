import test from 'node:test';
import assert from 'node:assert/strict';
import {
  planTurn,
  deltaGuardFailure,
  stateDrift,
  unusableCheckpointSize,
} from './dist/delta-turns-lib.js';
import { getBenchmarkProfile } from './dist/benchmark_profiles.js';

const BASE = {
  graphId: 'benchmark_delta',
  migrateFromGraphId: '',
  migrateAfter: 0,
  expectDelta: true,
  verifyEvery: 50,
  bucketSize: 100,
};

const MIGRATING = {
  ...BASE,
  migrateFromGraphId: 'benchmark',
  migrateAfter: 200,
};

test('steps equals the turn number, because steps is cumulative on a reused thread', () => {
  assert.equal(planTurn(1, BASE).steps, 1);
  assert.equal(planTurn(937, BASE).steps, 937);
});

test('without migration every turn uses the same graph', () => {
  assert.equal(planTurn(1, BASE).graphId, 'benchmark_delta');
  assert.equal(planTurn(500, BASE).graphId, 'benchmark_delta');
  assert.equal(planTurn(500, BASE).expectDelta, true);
});

test('migration switches graph and delta expectation at the boundary', () => {
  assert.equal(planTurn(200, MIGRATING).graphId, 'benchmark');
  assert.equal(planTurn(200, MIGRATING).expectDelta, false);
  assert.equal(planTurn(201, MIGRATING).graphId, 'benchmark_delta');
  assert.equal(planTurn(201, MIGRATING).expectDelta, true);
});

test('migrateAfter is ignored without a graph to migrate from', () => {
  const plan = planTurn(1, { ...BASE, migrateAfter: 200 });
  assert.equal(plan.graphId, 'benchmark_delta');
  assert.equal(plan.expectDelta, true);
});

test('the guard runs on turn 2, never on turn 1', () => {
  assert.equal(planTurn(1, BASE).guard, false);
  assert.equal(planTurn(2, BASE).guard, true);
  assert.equal(planTurn(3, BASE).guard, false);
});

test('migration guards again two turns after the switch', () => {
  assert.equal(planTurn(201, MIGRATING).guard, false);
  assert.equal(planTurn(202, MIGRATING).guard, true);
});

test('the guard never lands on a snapshot boundary, where absent counters are correct', () => {
  const guarded = [];
  for (let turn = 1; turn <= 1000; turn += 1) {
    if (planTurn(turn, MIGRATING).guard) guarded.push(turn);
  }
  assert.deepEqual(guarded, [2, 202]);
  for (const turn of guarded) {
    assert.notEqual(turn % 50, 0);
    assert.notEqual(turn % 1000, 0);
  }
});

test('cold re-read runs on the configured cadence and can be disabled', () => {
  assert.equal(planTurn(50, BASE).verify, true);
  assert.equal(planTurn(51, BASE).verify, false);
  assert.equal(planTurn(50, { ...BASE, verifyEvery: 0 }).verify, false);
});

test('depth buckets group turns and stay stable at the edges', () => {
  assert.equal(planTurn(1, BASE).depthBucket, '1-100');
  assert.equal(planTurn(100, BASE).depthBucket, '1-100');
  assert.equal(planTurn(101, BASE).depthBucket, '101-200');
  assert.equal(planTurn(7, { ...BASE, bucketSize: 0 }).depthBucket, '7');
});

test('a delta graph without counters is a silent fallback to a plain channel', () => {
  assert.equal(deltaGuardFailure({ counters_since_delta_snapshot: { c: [3, 3] } }, true), null);
  assert.equal(deltaGuardFailure({ step: 4 }, true), 'delta_off_on_delta_graph');
  assert.equal(deltaGuardFailure(null, true), 'delta_off_on_delta_graph');
});

test('empty counters read as absent, matching Pregel filtering out zero entries', () => {
  assert.equal(deltaGuardFailure({ counters_since_delta_snapshot: {} }, true), 'delta_off_on_delta_graph');
  assert.equal(deltaGuardFailure({ counters_since_delta_snapshot: {} }, false), null);
});

test('counters on the control graph mean the wrong graph is under test', () => {
  assert.equal(deltaGuardFailure({ counters_since_delta_snapshot: { c: [1, 1] } }, false), 'delta_on_on_plain_graph');
  assert.equal(deltaGuardFailure({ step: 4 }, false), null);
});

test('matching live and stored state is no drift', () => {
  const values = { counter: 12, cumulative_checkpoint: 'abcd' };
  assert.equal(stateDrift(values, { ...values }, 'cumulative_checkpoint'), null);
});

test('a lost write shows up as a shorter stored channel', () => {
  const live = { counter: 12, cumulative_checkpoint: 'abcd' };
  const cold = { counter: 12, cumulative_checkpoint: 'ab' };
  assert.equal(stateDrift(live, cold, 'cumulative_checkpoint'), 'channel_drift:abcd!=ab');
});

test('same-length channel corruption is still drift', () => {
  const live = { counter: 12, cumulative_checkpoint: 'abcd' };
  const cold = { counter: 12, cumulative_checkpoint: 'abce' };
  assert.equal(stateDrift(live, cold, 'cumulative_checkpoint'), 'channel_drift:abcd!=abce');
});

test('a counter that does not survive the read is drift', () => {
  const live = { counter: 12, cumulative_checkpoint: 'ab' };
  const cold = { counter: 11, cumulative_checkpoint: 'ab' };
  assert.equal(stateDrift(live, cold, 'cumulative_checkpoint'), 'counter_drift:12!=11');
});

test('missing values are reported rather than passing silently', () => {
  assert.equal(stateDrift(null, {}, 'cumulative_checkpoint'), 'run_values_missing');
  assert.equal(stateDrift({}, null, 'cumulative_checkpoint'), 'cold_values_missing');
});

test('a non-string channel encoding is still comparable', () => {
  const live = { counter: 1, cumulative_checkpoint: { data: [1, 2, 3] } };
  const cold = { counter: 1, cumulative_checkpoint: { data: [1, 2] } };
  assert.equal(
    stateDrift(live, cold, 'cumulative_checkpoint'),
    'channel_drift:{"data":[1,2,3]}!={"data":[1,2]}'
  );
});

test('the first turn of a migration runs on the graph being migrated from', () => {
  assert.equal(planTurn(1, MIGRATING).graphId, 'benchmark');
  assert.equal(planTurn(1, MIGRATING).expectDelta, false);
});

test('adjacent guard turns do not collapse when the switch is early', () => {
  const early = { ...MIGRATING, migrateAfter: 1 };
  assert.equal(planTurn(2, early).guard, true);
  assert.equal(planTurn(3, early).guard, true);
  assert.equal(planTurn(2, early).expectDelta, true);
});

test('a channel absent from both sides compares equal, which is why checkpoint_size must be > 0', () => {
  const drift = stateDrift({ counter: 1 }, { counter: 1 }, 'cumulative_checkpoint');
  assert.equal(drift, null);
});

test('a checkpoint size of zero makes the run meaningless and is rejected', () => {
  assert.equal(unusableCheckpointSize(0), true);
  assert.equal(unusableCheckpointSize(undefined), true);
  assert.equal(unusableCheckpointSize(-1), true);
  assert.equal(unusableCheckpointSize(256), false);
});

test('the delta-turns profile is wired and writes a growing channel', () => {
  const { profile } = getBenchmarkProfile('delta-turns');
  assert.equal(profile.runMode, 'stateful');
  assert.equal(unusableCheckpointSize(profile.context.checkpoint_size), false);
  assert.equal(profile.context.delay, 0);
  assert.equal(profile.context.steps, 1);
});
