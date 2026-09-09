import test from 'node:test';
import assert from 'node:assert/strict';
// Compiled output: the source is TypeScript, and `npm test` runs after
// `npm run build` both locally and in CI.
import { classifyError, recordError } from './dist/classify-error.js';

test('5xx is a server error', () => {
  assert.equal(classifyError({ response: { status: 500 } }), 'server');
  assert.equal(classifyError({ response: { status: 503 } }), 'server');
});

test('408 and timeout error strings are timeouts', () => {
  assert.equal(classifyError({ response: { status: 408 } }), 'timeout');
  assert.equal(
    classifyError({ response: { status: 0, error: 'request timeout' } }),
    'timeout'
  );
});

// The bucket that had never once been written to. A refused connection has no
// HTTP status, so every runner used to file it under something else.
test('an unreachable deployment is a connection error', () => {
  assert.equal(
    classifyError({ response: { status: 0, error: 'dial: connection refused' } }),
    'connection'
  );
  assert.equal(classifyError({ response: { status: 0 } }), 'connection');
});

test('connection beats the runner-specific fallbacks', () => {
  // Before this classifier, stream_write reported exactly this case as
  // missing_message and wait_write as other.
  const unreachable = { status: 0, error: 'dial: connection refused' };
  assert.equal(
    classifyError({ response: unreachable, missingMessage: true }),
    'connection'
  );
  assert.equal(
    classifyError({ response: unreachable, hasApiError: true }),
    'connection'
  );
});

test('a 200 that came back wrong falls to the runner-specific buckets', () => {
  const ok = { status: 200 };
  assert.equal(classifyError({ response: ok, hasApiError: true }), 'api');
  assert.equal(classifyError({ response: ok, missingMessage: true }), 'missing_message');
  assert.equal(classifyError({ response: ok }), 'other');
});

test('4xx that is not 408 is not mistaken for anything else', () => {
  assert.equal(classifyError({ response: { status: 422 } }), 'other');
  assert.equal(classifyError({ response: { status: 404 } }), 'other');
});

test('a missing response is not reported as unreachable', () => {
  // No response object at all means the runner never got that far; that is not
  // evidence about the network, so it must not claim `connection`.
  assert.equal(classifyError({}), 'other');
  assert.equal(classifyError({ response: null, missingMessage: true }), 'missing_message');
});

// classifyError picks the bucket; recordError is what actually increments a
// counter, and it was previously untested. A mutation that unwired
// connection_errors passed the whole suite.
function spyMetrics(omit = []) {
  const names = [
    'server_errors',
    'timeout_errors',
    'connection_errors',
    'api_errors',
    'missing_message_errors',
    'other_errors',
  ];
  const counts = {};
  const metrics = {};
  for (const name of names) {
    counts[name] = 0;
    if (!omit.includes(name)) metrics[name] = { add: (n) => (counts[name] += n) };
  }
  return { metrics, counts };
}

test('recordError increments the counter the bucket names', async (t) => {
  const cases = [
    ['server', 'server_errors'],
    ['timeout', 'timeout_errors'],
    ['connection', 'connection_errors'],
    ['api', 'api_errors'],
    ['missing_message', 'missing_message_errors'],
    ['other', 'other_errors'],
  ];
  for (const [bucket, counter] of cases) {
    await t.test(`${bucket} -> ${counter}`, () => {
      const { metrics, counts } = spyMetrics();
      recordError(bucket, metrics);
      assert.equal(counts[counter], 1, `${bucket} did not increment ${counter}`);
      const strays = Object.entries(counts).filter(([k, v]) => k !== counter && v !== 0);
      assert.deepEqual(strays, [], `${bucket} also incremented ${strays.map(([k]) => k)}`);
    });
  }
});

test('recordError falls back to other_errors for counters the entrypoint omits', () => {
  // Preserves what the runners open-coded for api_errors and
  // missing_message_errors, and covers older entrypoints without connection.
  for (const [bucket, counter] of [
    ['connection', 'connection_errors'],
    ['api', 'api_errors'],
    ['missing_message', 'missing_message_errors'],
  ]) {
    const { metrics, counts } = spyMetrics([counter]);
    recordError(bucket, metrics);
    assert.equal(counts.other_errors, 1, `${bucket} did not fall back to other_errors`);
  }
});
