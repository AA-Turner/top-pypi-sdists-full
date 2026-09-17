#!/usr/bin/env node
'use strict';

const path = require('path');

const { run, isEligibleForNormalization } = require(path.join(__dirname, '..', 'normalize-copilot-pr.js'));

let PASS = 0;
let FAIL = 0;

function assertEqual(desc, expected, actual) {
  if (JSON.stringify(expected) === JSON.stringify(actual)) {
    console.log(`  ✓ ${desc}`);
    PASS++;
  } else {
    console.log(`  ✗ ${desc} (expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)})`);
    FAIL++;
  }
}

function assertTruthy(desc, value) {
  if (value) {
    console.log(`  ✓ ${desc}`);
    PASS++;
  } else {
    console.log(`  ✗ ${desc} (expected truthy, got ${JSON.stringify(value)})`);
    FAIL++;
  }
}

function createMockCore() {
  const infos = [];
  const warnings = [];
  return {
    infos,
    warnings,
    info: message => infos.push(message),
    warning: message => warnings.push(message),
  };
}

function createMockGithub(issueComments = [], issueCommentsByNumber = {}) {
  const calls = { addLabels: [], createComment: [], removeLabel: [] };
  return {
    calls,
    paginate: async (_fn, params = {}) => {
      const number = params.issue_number;
      if (Object.prototype.hasOwnProperty.call(issueCommentsByNumber, number)) {
        return issueCommentsByNumber[number];
      }
      return issueComments;
    },
    rest: {
      issues: {
        listComments: async () => ({ data: issueComments }),
        addLabels: async params => { calls.addLabels.push(params); },
        createComment: async params => { calls.createComment.push(params); },
        removeLabel: async params => {
          calls.removeLabel.push(params);
          return {};
        },
      },
    },
  };
}

function makeContext() {
  return { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } };
}

(async () => {
console.log('=== Testing isEligibleForNormalization ===');
{
  const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=100 phase=1 hierarchy=feature correlation_id=11111111-1111-4111-8111-aaaaaaaaaaaa -->';
  assertTruthy('a PR with a valid marker is eligible', isEligibleForNormalization({ body: marker, labels: [] }));
}
{
  assertTruthy(
    'a PR with a speckit:spec label is eligible',
    isEligibleForNormalization({ body: '', labels: [{ name: 'speckit:spec' }] }),
  );
}
{
  assertTruthy(
    'a PR with a speckit:phase-N label is eligible',
    isEligibleForNormalization({ body: '', labels: [{ name: 'speckit:phase-2' }] }),
  );
}
{
  assertTruthy(
    'a PR with a speckit:level-N label is eligible',
    isEligibleForNormalization({ body: '', labels: [{ name: 'speckit:level-task' }] }),
  );
}
{
  // Regression: a Copilot audit PR that merely quotes the marker prefix in its body
  // (for example, documenting the marker format) does not satisfy the full marker
  // regex and carries none of the SpecKit labels, so it must be ineligible.
  const quotedPrefix = 'This PR documents the `speckit:agent-assigned schema_version=1 engine=cloud-agent` marker format.';
  assertEqual(
    'a PR quoting the marker prefix without a full match and no labels is ineligible',
    false,
    isEligibleForNormalization({ body: quotedPrefix, labels: [] }),
  );
}
{
  assertEqual(
    'a PR with neither marker nor SpecKit labels is ineligible',
    false,
    isEligibleForNormalization({ body: '', labels: [{ name: 'unrelated-label' }] }),
  );
}

console.log('=== Testing run() eligibility guard (zero-mutation regression) ===');
{
  // Regression: the security-critical guard added for issue #4204 must cause zero
  // comments, zero labels, and zero source-issue mutations for a Copilot audit PR that
  // quotes the marker prefix but carries no valid marker and no SpecKit label.
  const core = createMockCore();
  const github = createMockGithub();
  const quotedPrefix = 'This PR documents the `speckit:agent-assigned schema_version=1 engine=cloud-agent` marker format.';
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 900,
      body: quotedPrefix,
      labels: [],
    },
  });
  assertEqual('ineligible PR triggers zero addLabels calls', 0, github.calls.addLabels.length);
  assertEqual('ineligible PR triggers zero createComment calls', 0, github.calls.createComment.length);
  assertEqual('ineligible PR triggers zero removeLabel calls', 0, github.calls.removeLabel.length);
  assertTruthy(
    'ineligible PR logs a skip-without-diagnostics info message',
    core.infos.some(msg => msg.includes('skipping normalization without diagnostics'))
  );
}
{
  // Same guard, but the PR has no marker at all (e.g. a plain unrelated Copilot PR that
  // still matched the coarse job-level `if:` gate) and also carries no SpecKit label.
  const core = createMockCore();
  const github = createMockGithub();
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 901,
      body: 'Just a regular PR body with no markers.',
      labels: [],
    },
  });
  assertEqual('unrelated PR without marker or label triggers zero addLabels calls', 0, github.calls.addLabels.length);
  assertEqual('unrelated PR without marker or label triggers zero createComment calls', 0, github.calls.createComment.length);
}
{
  // A markerless PR with a prior UUID-correlated success comment must not be treated as
  // a legacy PR, even when its old SpecKit labels remain.
  const core = createMockCore();
  const github = createMockGithub([
    {
      user: { login: 'AMARSNIK_swica' },
      body: '<!-- speckit:agent-pr-normalizer pr=902 correlation_id=44444444-4444-4444-8444-dddddddddddd -->',
    },
  ]);
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 902,
      body: 'Relates to #952',
      labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
    },
  });
  assertEqual('prior correlated normalization skips label mutation', 0, github.calls.addLabels.length);
  assertEqual('prior correlated normalization skips comments', 0, github.calls.createComment.length);
  assertEqual('prior correlated normalization skips tracking cleanup', 0, github.calls.removeLabel.length);
  assertTruthy(
    'prior correlated normalization logs a legacy-normalization warning',
    core.warnings.some(msg => msg.includes('skipping legacy normalization'))
  );
}
{
  // An untrusted commenter must not be able to suppress legacy normalization with a
  // forged UUID-correlated success marker.
  const core = createMockCore();
  const github = createMockGithub([
    {
      user: { login: 'untrusted-collaborator' },
      body: '<!-- speckit:agent-pr-normalizer pr=907 correlation_id=55555555-5555-4555-8555-eeeeeeeeeeee -->',
    },
  ]);
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 907,
      body: 'Relates to #953',
      labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
    },
  });
  assertEqual('untrusted prior correlation does not suppress label mutation', 1, github.calls.addLabels.length);
  assertEqual('untrusted prior correlation does not suppress normalization comment', 1, github.calls.createComment.length);
  assertEqual('untrusted prior correlation does not suppress tracking cleanup', 4, github.calls.removeLabel.length);
}

console.log('=== Testing run() diagnostic paths ===');
{
  // A speckit:spec-labeled PR without a marker or resolvable phase/level metadata fails
  // validation and must post a single failure diagnostic and speckit:failed label.
  const core = createMockCore();
  const github = createMockGithub();
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 902,
      body: '',
      labels: [{ name: 'speckit:spec' }],
    },
  });
  assertEqual('missing phase/level metadata adds speckit:failed label', 1, github.calls.addLabels.length);
  assertEqual('missing phase/level metadata posts one failure comment', 1, github.calls.createComment.length);
  assertTruthy(
    'missing phase/level metadata failure comment references required marker or reference',
    github.calls.createComment[0].body.includes('must contain a valid `speckit:agent-assigned` marker')
  );
}

console.log('=== Testing run() successful normalization ===');
{
  const core = createMockCore();
  const github = createMockGithub();
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 903,
      body: 'Relates to #950',
      labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
    },
  });
  assertEqual('successful normalization adds the required labels', 1, github.calls.addLabels.length);
  assertEqual(
    'successful normalization requests phase/level/spec labels',
    ['speckit:phase-2', 'speckit:level-feature', 'speckit:spec'],
    github.calls.addLabels[0].labels
  );
  assertEqual('successful normalization posts exactly one status comment', 1, github.calls.createComment.length);
  assertTruthy(
    'successful normalization status comment includes the status marker',
    github.calls.createComment[0].body.includes('speckit:agent-pr-normalizer pr=903 correlation_id=none')
  );
}
{
  // Regression: an existing status comment must not be duplicated.
  const core = createMockCore();
  const github = createMockGithub([
    { body: '<!-- speckit:agent-pr-normalizer pr=904 correlation_id=none -->' },
  ]);
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 904,
      body: 'Relates to #951',
      labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
    },
  });
  assertEqual('existing status comment is not duplicated', 0, github.calls.createComment.length);
}

console.log('=== Testing run() marker trust validation ===');
{
  // A PR body marker that is not corroborated by a trusted source-issue comment must
  // fail validation and post a diagnostic rather than normalize.
  const core = createMockCore();
  const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=960 phase=1 hierarchy=feature correlation_id=22222222-2222-4222-8222-bbbbbbbbbbbb -->';
  const github = createMockGithub([], { 960: [] });
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 905,
      body: marker,
      labels: [],
    },
  });
  assertEqual('untrusted marker adds speckit:failed label only to the PR', 1, github.calls.addLabels.length);
  assertEqual('untrusted marker does not remove source issue tracking', 0, github.calls.removeLabel.length);
  assertTruthy(
    'untrusted marker posts a diagnostic naming the correlation ID',
    github.calls.createComment.some(call => call.body.includes('No trusted source issue comment matched correlation ID'))
  );
}
{
  // A PR body marker corroborated by the exact trusted login succeeds.
  const core = createMockCore();
  const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=961 phase=1 hierarchy=feature correlation_id=33333333-3333-4333-8333-cccccccccccc -->';
  const github = createMockGithub([], {
    961: [{ user: { login: 'AMARSNIK_swica' }, body: marker, created_at: '2026-01-01T00:00:00Z' }],
  });
  await run({
    github,
    context: makeContext(),
    core,
    pr: {
      number: 906,
      body: marker,
      labels: [],
    },
  });
  assertEqual('trusted marker normalizes without a failure comment', 1, github.calls.createComment.length);
  assertTruthy(
    'trusted marker posts the success status comment',
    github.calls.createComment[0].body.includes('SpecKit Copilot PR normalized')
  );
}

console.log(`\nResults: ${PASS} passed, ${FAIL} failed`);
if (FAIL > 0) {
  process.exit(1);
}
})();
