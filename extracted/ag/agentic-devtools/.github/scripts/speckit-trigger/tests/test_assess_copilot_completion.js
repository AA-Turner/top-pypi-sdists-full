#!/usr/bin/env node
'use strict';

const assert = require('assert').strict;
const path = require('path');

const { assessCompletion, createPythonDeliveryAdapter } = require(path.join(__dirname, '..', 'assess-copilot-completion.js'));

const REPOSITORY = 'swai-factory/agentic-devtools';
const HEAD_SHA = '0123456789abcdef0123456789abcdef01234567';
const PR_NUMBER = 42;

function makePullRequest({
  number = PR_NUMBER,
  repository = REPOSITORY,
  headSha = HEAD_SHA,
  body = null,
} = {}) {
  return {
    number,
    body,
    base: { repo: { full_name: repository } },
    head: { sha: headSha },
  };
}

function makeWorkflowRun({
  conclusion = 'success',
  pullRequests = [makePullRequest()],
  repository = REPOSITORY,
  name = 'Running Copilot cloud agent',
  path = 'dynamic/copilot-swe-agent/copilot',
} = {}) {
  return {
    name,
    path,
    conclusion,
    head_sha: HEAD_SHA,
    repository: { full_name: repository },
    pull_requests: pullRequests,
  };
}

function makeGithub({
  pullRequests = [],
  livePullRequests = {},
  lookupError = null,
} = {}) {
  const calls = {
    lookup: 0,
    get: [],
    mutations: [],
  };
  const github = {
    paginate: async () => {
      throw new Error('Unexpected pagination call');
    },
    rest: {
      repos: {
        listPullRequestsAssociatedWithCommit: async params => {
          calls.lookup++;
          calls.lookupParams = params;
          if (lookupError) throw lookupError;
          return { data: pullRequests };
        },
      },
      pulls: {
        get: async params => {
          calls.get.push(params);
          const pr = livePullRequests[params.pull_number] || makePullRequest({ number: params.pull_number });
          return { data: pr };
        },
        update: async (...args) => calls.mutations.push(['pulls.update', args]),
        createReview: async (...args) => calls.mutations.push(['pulls.createReview', args]),
        requestReviewers: async (...args) => calls.mutations.push(['pulls.requestReviewers', args]),
      },
      issues: {
        addLabels: async (...args) => calls.mutations.push(['issues.addLabels', args]),
        createComment: async (...args) => calls.mutations.push(['issues.createComment', args]),
        removeLabel: async (...args) => calls.mutations.push(['issues.removeLabel', args]),
      },
    },
  };
  return { github, calls };
}

function makeContext() {
  return { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } };
}

function makeAssessment(overrides = {}) {
  return {
    repository: REPOSITORY,
    prNumber: PR_NUMBER,
    headSha: HEAD_SHA,
    outcome: 'DELIVERED',
    complete: true,
    diffEvidence: 'NON_ZERO_DIFF',
    ...overrides,
  };
}

function makeLegacyAssessment(overrides = {}) {
  return {
    repository: REPOSITORY,
    prNumber: PR_NUMBER,
    headSha: HEAD_SHA,
    outcome: 'NO_DELIVERY',
    complete: true,
    ...overrides,
  };
}

async function runCase({
  workflowRun = makeWorkflowRun(),
  pullRequests,
  livePullRequests,
  lookupError,
  assessDelivery,
} = {}) {
  const { github, calls } = makeGithub({ pullRequests, livePullRequests, lookupError });
  const summary = [];
  const outputs = [];
  let summaryWrites = 0;
  const result = await assessCompletion({
    github,
    context: makeContext(),
    workflowRun,
    assessDelivery,
    core: {
      setOutput: (name, value) => outputs.push([name, value]),
      summary: {
        addRaw(text) {
          summary.push(text);
          return this;
        },
        async write() { summaryWrites++; },
      },
    },
  });
  assert.deepEqual(calls.mutations, [], 'assessment must not call PR or issue mutation APIs');
  assert.deepEqual(outputs, [
    ['assessment_status', result.assessment_status],
    ['assessment_reason', result.assessment_reason],
  ], 'only the two existing assessment outputs are emitted');
  assert.equal(summaryWrites, summary.length, 'each diagnostic is written exactly once');
  return { result, calls, summary };
}

async function main() {
  await testPythonAdapter();
  await testBodySentinelDiagnostic();
  let adapterCalls = 0;
  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({
        name: 'Running Copilot cloud agent',
        path: 'dynamic/copilot-swe-agent/copilot',
      }),
      assessDelivery: async identity => {
        adapterCalls++;
        assert.deepEqual(identity, {
          repository: REPOSITORY,
          prNumber: PR_NUMBER,
          headSha: HEAD_SHA,
        });
        return makeLegacyAssessment();
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'verified_empty',
      assessment_reason: 'verified_no_delivery',
    });
    assert.equal(calls.get.length, 1, 'a payload association is re-fetched before assessment');
    assert.equal(calls.lookup, 0, 'a correlated payload association avoids fallback lookup');
  }

  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({ conclusion: 'failure' }),
      assessDelivery: async () => {
        adapterCalls++;
        throw new Error('must not assess a failed workflow');
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'workflow_not_success',
    });
    assert.equal(calls.get.length, 0, 'non-success routing does not correlate a PR');
    assert.equal(calls.lookup, 0);
  }
  assert.equal(adapterCalls, 1, 'only the successful run invokes the adapter');

  for (const workflowRun of [
    makeWorkflowRun({ name: 'Copilot cloud agent' }),
    makeWorkflowRun({ path: 'dynamic/copilot-swe-agent/copilot-other' }),
    (() => {
      const run = makeWorkflowRun();
      delete run.path;
      return run;
    })(),
  ]) {
    let adapterWasCalled = false;
    const { result, calls } = await runCase({
      workflowRun,
      assessDelivery: async () => {
        adapterWasCalled = true;
        return makeAssessment();
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'pr_lookup_unavailable',
    });
    assert.equal(adapterWasCalled, false, 'invalid upstream identities are rejected before assessment');
    assert.equal(calls.lookup, 0, 'invalid upstream identities are rejected before PR correlation');
    assert.equal(calls.get.length, 0);
  }

  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({
        pullRequests: [makePullRequest({ headSha: 'fedcba9876543210fedcba9876543210fedcba98' })],
      }),
      pullRequests: [makePullRequest()],
      assessDelivery: async () => makeLegacyAssessment(),
    });
    assert.deepEqual(result, {
      assessment_status: 'verified_empty',
      assessment_reason: 'verified_no_delivery',
    });
    assert.equal(calls.lookup, 1, 'a payload association for a different head is not correlated');
  }

  {
    const { result, calls } = await runCase({ workflowRun: makeWorkflowRun({ pullRequests: [] }) });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'pr_missing',
    });
    assert.equal(calls.lookup, 1, 'the run payload without a PR uses the unique association lookup');
  }

  {
    let assessedIdentity;
    const otherHeadSha = 'fedcba9876543210fedcba9876543210fedcba98';
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [] }),
      pullRequests: [makePullRequest(), makePullRequest({ number: 51, headSha: otherHeadSha })],
      assessDelivery: async identity => {
        assessedIdentity = identity;
        return makeLegacyAssessment();
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'verified_empty',
      assessment_reason: 'verified_no_delivery',
    });
    assert.deepEqual(assessedIdentity, {
      repository: REPOSITORY,
      prNumber: PR_NUMBER,
      headSha: HEAD_SHA,
    });
    assert.equal(calls.lookup, 1, 'fallback lookup filters associations to the run head');
    assert.deepEqual(calls.get, [{
      owner: 'swai-factory',
      repo: 'agentic-devtools',
      pull_number: PR_NUMBER,
    }], 'only the exact-head PR is re-fetched');
  }

  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [] }),
      pullRequests: [makePullRequest()],
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'assessment_adapter_unavailable',
    });
    assert.equal(calls.lookup, 1);
    assert.equal(calls.get.length, 1, 'a unique lookup result is re-fetched before adapter availability is checked');
  }

  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [] }),
      pullRequests: [],
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'pr_missing',
    });
  }

  {
    const { result } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [] }),
      pullRequests: [makePullRequest({ number: 51 }), makePullRequest({ number: 52 })],
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'pr_ambiguous',
    });
  }

  {
    const { result, calls } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [makePullRequest({ repository: 'other/repo' })] }),
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'cross_repository',
    });
    assert.equal(calls.get.length, 0, 'foreign repository associations are rejected before re-fetch');
  }

  {
    let adapterWasCalled = false;
    const { result } = await runCase({
      livePullRequests: {
        [PR_NUMBER]: makePullRequest({ headSha: 'fedcba9876543210fedcba9876543210fedcba98' }),
      },
      assessDelivery: async () => {
        adapterWasCalled = true;
        return makeAssessment();
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'stale_head',
    });
    assert.equal(adapterWasCalled, false, 'stale live heads are rejected before delivery assessment');
  }

  {
    const { result } = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [] }),
      lookupError: new Error('private API response must not be surfaced'),
    });
    assert.deepEqual(result, {
      assessment_status: 'not_admitted',
      assessment_reason: 'pr_lookup_unavailable',
    });
    assert.equal(JSON.stringify(result).includes('private API'), false);
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => makeAssessment({ outcome: 'UNKNOWN' }),
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_unknown',
    });
    assert.equal(Object.hasOwn(result, 'deliveryEvidence'), false);
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => {
        throw new Error('private adapter diagnostic must not be surfaced');
      },
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_unknown',
    });
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => makeAssessment({ outcome: 'DELIVERED' }),
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_not_admitted',
      deliveryEvidence: expectedEvidence(),
    });
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => makeAssessment({ complete: false, outcome: 'ZERO_DIFF' }),
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_incomplete',
    });
  }

  for (const [legacy, expected] of [
    [makeLegacyAssessment(), { assessment_status: 'verified_empty', assessment_reason: 'verified_no_delivery' }],
    [makeLegacyAssessment({ complete: false }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_incomplete' }],
    [makeLegacyAssessment({ outcome: 'DELIVERED' }), { assessment_status: 'unknown', assessment_reason: 'delivery_not_admitted' }],
    [makeLegacyAssessment({ outcome: 'DELIVERED', complete: false }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_incomplete' }],
    [makeLegacyAssessment({ outcome: 'UNKNOWN' }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_unknown' }],
    [makeLegacyAssessment({ outcome: 'ZERO_DIFF' }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_incomplete' }],
    [makeLegacyAssessment({ outcome: 'NON_ZERO_DIFF' }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_incomplete' }],
    [makeLegacyAssessment({ outcome: 'NOT_A_REAL_OUTCOME' }), { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_malformed' }],
  ]) {
    const { result } = await runCase({ assessDelivery: async () => legacy });
    assert.deepEqual(result, expected);
    assert.equal(Object.hasOwn(result, 'deliveryEvidence'), false, 'legacy results do not retain unvalidated bridge evidence');
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => makeAssessment({ outcome: 'ZERO_DIFF' }),
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_incomplete',
    });
  }

  {
    const { result } = await runCase({
      assessDelivery: async () => makeAssessment({ prNumber: PR_NUMBER + 1 }),
    });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_unknown',
    });
    assert.equal(Object.hasOwn(result, 'deliveryEvidence'), false);
  }

  for (const malformed of [
    null,
    { ...makeAssessment(), outcome: 'NOT_A_REAL_OUTCOME' },
    { ...makeAssessment(), complete: 'true' },
    { ...makeAssessment(), headSha: null },
  ]) {
    const { result } = await runCase({ assessDelivery: async () => malformed });
    assert.deepEqual(result, {
      assessment_status: 'unknown',
      assessment_reason: 'delivery_evidence_malformed',
    });
    assert.equal(Object.hasOwn(result, 'deliveryEvidence'), false);
  }

  console.log('All Copilot completion assessment tests passed.');
}

async function testBodySentinelDiagnostic() {
  const livePullRequests = {
    [PR_NUMBER]: makePullRequest({ body: 'None retained' }),
  };
  const expectedDiagnostic = `PR #${PR_NUMBER} at head ${HEAD_SHA}: stale PR-body sentinel \`None retained\`; diff evidence: NON_ZERO_DIFF; assessment reason: delivery_not_admitted. This diagnostic does not authorize delivery, readiness, or PR lifecycle changes.`;
  const { result, calls, summary } = await runCase({
    livePullRequests,
    assessDelivery: async () => makeAssessment(),
  });
  assert.deepEqual(summary, [expectedDiagnostic]);
  assert.deepEqual(result, {
    assessment_status: 'unknown',
    assessment_reason: 'delivery_not_admitted',
    deliveryEvidence: expectedEvidence(),
  });
  assert.equal(calls.lookup, 0, 'the diagnostic does not add correlation');
  assert.equal(calls.get.length, 1, 'the diagnostic reuses the existing PR read');
  assert.equal(JSON.stringify(result).includes('None retained'), false, 'body is not transported');

  for (const body of [
    null, undefined, '', 'None retained ', ' None retained', ' none retained',
    'none retained', 'NONE RETAINED', 'None retained\n', 'None retained\r\n',
    'Summary: None retained', 'None retained; other changes', 'Ordinary authored prose.',
    42, ['None retained'], { body: 'None retained' },
  ]) {
    const rejected = await runCase({
      workflowRun: makeWorkflowRun({ pullRequests: [makePullRequest({ body: 'None retained' })] }),
      livePullRequests: { [PR_NUMBER]: makePullRequest({ body }) },
      assessDelivery: async () => makeAssessment(),
    });
    assert.deepEqual(rejected.summary, [], 'only the exact live API body is eligible');
  }

  for (const evidence of [
    null, {},
    makeLegacyAssessment(),
    makeLegacyAssessment({ outcome: 'DELIVERED' }),
    makeAssessment({ complete: false }),
    makeAssessment({ complete: 'true' }),
    makeAssessment({ outcome: 'NO_DELIVERY' }),
    makeAssessment({ outcome: 'ZERO_DIFF', diffEvidence: 'ZERO_DIFF' }),
    makeAssessment({ outcome: 'NON_ZERO_DIFF' }),
    makeAssessment({ outcome: 'UNKNOWN', complete: false, diffEvidence: 'UNKNOWN' }),
    makeAssessment({ outcome: 'UNKNOWN' }),
    makeAssessment({ outcome: 'invalid' }),
    makeAssessment({ diffEvidence: 'UNKNOWN' }),
    makeAssessment({ diffEvidence: 'ZERO_DIFF' }),
    makeAssessment({ diffEvidence: undefined }),
    makeAssessment({ repository: 'other/repo' }),
    makeAssessment({ prNumber: PR_NUMBER + 1 }),
    makeAssessment({ headSha: 'f'.repeat(40) }),
    { ...makeAssessment(), unexpected: true },
  ]) {
    const rejected = await runCase({ livePullRequests, assessDelivery: async () => evidence });
    assert.deepEqual(rejected.summary, [], 'unproven, stale or incomplete evidence cannot claim a mismatch');
  }
  for (const assessDelivery of [undefined, async () => { throw new Error('private evidence'); }]) {
    const rejected = await runCase({ livePullRequests, assessDelivery });
    assert.deepEqual(rejected.summary, []);
  }
  for (const overrides of [
    { workflowRun: makeWorkflowRun({ conclusion: 'failure' }) },
    { livePullRequests: { [PR_NUMBER]: makePullRequest({ body: 'None retained', headSha: 'f'.repeat(40) }) } },
    { livePullRequests: { [PR_NUMBER]: makePullRequest({ body: 'None retained', repository: 'other/repo' }) } },
    { workflowRun: makeWorkflowRun({ pullRequests: [makePullRequest(), makePullRequest({ number: 43 })] }) },
  ]) {
    const rejected = await runCase({
      livePullRequests,
      assessDelivery: async () => makeAssessment(),
      ...overrides,
    });
    assert.deepEqual(rejected.summary, [], 'unadmitted completions cannot claim a mismatch');
  }
}

function expectedEvidence(diffEvidence = 'NON_ZERO_DIFF', headSha = HEAD_SHA) {
  return {
    identity: { repository: REPOSITORY, prNumber: PR_NUMBER, headSha },
    diffEvidence,
  };
}

async function testPythonAdapter() {
  const identity = expectedEvidence().identity;
  const env = { PATH: '/trusted/bin', GH_TOKEN: 'offline-token', HOME: '/home/offline' };
  const cwd = '/trusted/checkout';
  let calls = 0;
  const adapter = createPythonDeliveryAdapter({
    env: { ...env, XDG_CONFIG_HOME: '/config', XDG_CACHE_HOME: '/cache', TMPDIR: '/tmp', RUNNER_TEMP: '/runner', SECRET: 'not-forwarded', PYTHONPATH: '/untrusted' },
    cwd,
    timeoutMs: 1234,
    maxBuffer: 4096,
    execFile: (executable, args, options, callback) => {
      calls++;
      assert.equal(executable, 'python');
      assert.deepEqual(args, [
        '-m', 'agentic_devtools.cli.ci.pipeline.delivery_bridge',
        '--repository', REPOSITORY, '--pr-number', '42', '--head-sha', HEAD_SHA,
      ]);
      assert.deepEqual(options, {
        cwd, env: { ...env, XDG_CONFIG_HOME: '/config', XDG_CACHE_HOME: '/cache', TMPDIR: '/tmp', RUNNER_TEMP: '/runner' },
        shell: false, windowsHide: true, timeout: 1234, maxBuffer: 4096, encoding: 'utf8',
      });
      callback(null, `${JSON.stringify(makeAssessment())}\n`, 'private stderr must not be emitted');
    },
  });
  assert.deepEqual(await adapter(identity), makeAssessment());
  assert.equal(calls, 1);

  for (const missing of ['PATH', 'GH_TOKEN', 'HOME']) {
    const incompleteEnv = { ...env };
    delete incompleteEnv[missing];
    assert.throws(() => createPythonDeliveryAdapter({ env: incompleteEnv, cwd }));
  }
  assert.throws(() => createPythonDeliveryAdapter({ env: Object.create(env), cwd }));
  for (const config of [
    { cwd: '' }, { cwd: 'relative' }, { timeoutMs: 0 }, { timeoutMs: 1.5 },
    { timeoutMs: Infinity }, { timeoutMs: 120001 }, { maxBuffer: 0 },
    { maxBuffer: 1.5 }, { maxBuffer: 65537 }, { pythonExecutable: '' },
  ]) {
    assert.throws(() => createPythonDeliveryAdapter({ env, cwd, ...config }));
  }
  assert.throws(() => createPythonDeliveryAdapter({ env: { ...env, TMPDIR: null }, cwd }));
  for (const invalid of [
    { repository: 'owner/repo;bad' }, { repository: 'owner/repo\n' },
    { prNumber: 0 }, { prNumber: '42' }, { prNumber: Number.MAX_SAFE_INTEGER + 1 },
    { headSha: 'bad' }, { headSha: `${HEAD_SHA}\n` },
  ]) {
    await assert.rejects(adapter({ ...identity, ...invalid }));
  }

  for (const output of [
    '', 'not json', '{}\n{}', '{}\n\n', ' {}', '{} ', 'diagnostic{}', '{}diagnostic',
    '[]', 'null', undefined,
    JSON.stringify({ ...makeAssessment(), body: 'must not retain' }),
    JSON.stringify(makeAssessment({ repository: 'other/repo' })),
    JSON.stringify(makeAssessment({ prNumber: 43 })),
    JSON.stringify(makeAssessment({ headSha: 'f'.repeat(40) })),
    JSON.stringify(makeAssessment({ headSha: `${HEAD_SHA}\n` })),
    JSON.stringify(makeAssessment({ repository: `${REPOSITORY}\n` })),
    ' '.repeat(65537),
  ]) {
    const badAdapter = createPythonDeliveryAdapter({
      env, cwd, execFile: (_executable, _args, _options, callback) => callback(null, output, 'private'),
    });
    await assert.rejects(badAdapter(identity), error => !error.message.includes('private'));
  }
  const throwing = createPythonDeliveryAdapter({
    env, cwd, execFile: () => { throw new Error('private subprocess diagnostic'); },
  });
  await assert.rejects(throwing(identity), { message: 'Delivery evidence unavailable' });
  for (const outcome of ['DELIVERED', 'UNKNOWN', 'NO_DELIVERY', 'ZERO_DIFF', 'NON_ZERO_DIFF', 'OTHER']) {
    for (const complete of [true, false, 'true']) {
      for (const diffEvidence of ['NON_ZERO_DIFF', 'UNKNOWN', 'ZERO_DIFF', undefined]) {
        const valid = (outcome === 'DELIVERED' && complete === true && diffEvidence === 'NON_ZERO_DIFF')
          || (outcome === 'UNKNOWN' && complete === false && diffEvidence === 'UNKNOWN');
        const value = makeAssessment({ outcome, complete, diffEvidence });
        const testAdapter = createPythonDeliveryAdapter({
          env, cwd, execFile: (_exe, _args, _opts, callback) => callback(null, JSON.stringify(value), ''),
        });
        if (valid) {
          assert.deepEqual(await testAdapter(identity), value);
        } else {
          await assert.rejects(testAdapter(identity));
        }
      }
    }
  }
  for (const error of [Object.assign(new Error('private'), { code: 1 }), Object.assign(new Error('private'), { killed: true }), Object.assign(new Error('private'), { code: 'ERR_CHILD_PROCESS_STDIO_MAXBUFFER' })]) {
    const failing = createPythonDeliveryAdapter({
      env, cwd, execFile: (_exe, _args, _opts, callback) => callback(error, 'private', 'private'),
    });
    const { result } = await runCase({ assessDelivery: failing });
    assert.deepEqual(result, { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_unknown' });
  }
  const mixedCase = createPythonDeliveryAdapter({
    env, cwd, pythonExecutable: '/trusted/python',
    execFile: (exe, args, options, callback) => {
      assert.equal(exe, '/trusted/python');
      assert.equal(args[7], HEAD_SHA.toLowerCase());
      assert.deepEqual(options.env, env);
      callback(null, JSON.stringify(makeAssessment({ repository: REPOSITORY.toUpperCase(), headSha: HEAD_SHA.toUpperCase() })), '');
    },
  });
  assert.equal((await mixedCase(identity)).headSha, HEAD_SHA);
  assert.equal((await mixedCase({ ...identity, headSha: HEAD_SHA.toUpperCase() })).headSha, HEAD_SHA.toUpperCase());
  const outputs = [];
  const { github } = makeGithub();
  const result = await assessCompletion({
    github, context: makeContext(), workflowRun: makeWorkflowRun(),
    assessDelivery: async () => makeAssessment({ outcome: 'UNKNOWN', complete: false, diffEvidence: 'UNKNOWN' }),
    core: { setOutput: (...args) => outputs.push(args) },
  });
  assert.deepEqual(result, {
    assessment_status: 'unknown', assessment_reason: 'delivery_evidence_incomplete',
    deliveryEvidence: expectedEvidence('UNKNOWN'),
  });
  assert.deepEqual(outputs, [['assessment_status', 'unknown'], ['assessment_reason', 'delivery_evidence_incomplete']]);
  const uppercase = await runCase({ assessDelivery: mixedCase });
  assert.deepEqual(uppercase.result.deliveryEvidence, expectedEvidence());
  const uppercaseRun = makeWorkflowRun({ pullRequests: [makePullRequest({ headSha: HEAD_SHA.toUpperCase() })] });
  uppercaseRun.head_sha = HEAD_SHA.toUpperCase();
  const uppercaseRequest = await runCase({
    workflowRun: uppercaseRun,
    livePullRequests: { [PR_NUMBER]: { ...makePullRequest({ headSha: HEAD_SHA.toUpperCase() }), body: 'private PR body' } },
    assessDelivery: mixedCase,
  });
  assert.deepEqual(
    uppercaseRequest.result.deliveryEvidence,
    expectedEvidence('NON_ZERO_DIFF', HEAD_SHA.toUpperCase()),
  );
  assert.equal(JSON.stringify(uppercaseRequest.result).includes('private PR body'), false);

  const rejectedNoDelivery = createPythonDeliveryAdapter({
    env, cwd,
    execFile: (_exe, _args, _options, callback) => callback(
      null,
      JSON.stringify(makeAssessment({ outcome: 'NO_DELIVERY' })),
      '',
    ),
  });
  const productionNoDelivery = await runCase({ assessDelivery: rejectedNoDelivery });
  assert.deepEqual(productionNoDelivery.result, {
    assessment_status: 'unknown',
    assessment_reason: 'delivery_evidence_unknown',
  });
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
