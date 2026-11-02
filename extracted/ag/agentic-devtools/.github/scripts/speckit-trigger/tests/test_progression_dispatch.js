#!/usr/bin/env node
'use strict';

const path = require('path');
const {
  DISPATCH_HIERARCHY_LEVELS,
  normalizeHierarchyLevelForDispatch,
  resolveInitialProgressionPhase,
  buildPhaseProgressionInputs,
} = require(path.join(__dirname, '..', 'progression-dispatch.js'));

let PASS = 0;
let FAIL = 0;

function assertEqual(description, expected, actual) {
  if (JSON.stringify(expected) === JSON.stringify(actual)) {
    console.log(`  ✓ ${description}`);
    PASS++;
  } else {
    console.log(`  ✗ ${description} (expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)})`);
    FAIL++;
  }
}

function assertThrows(description, expectedMessage, callback) {
  try {
    callback();
    console.log(`  ✗ ${description} (did not throw)`);
    FAIL++;
  } catch (error) {
    assertEqual(description, true, error.message.includes(expectedMessage));
  }
}

function createMockGithub() {
  const calls = [];
  return {
    calls,
    rest: {
      actions: {
        createWorkflowDispatch: async payload => calls.push(payload),
      },
    },
  };
}

async function dispatchInitial(github, engine, issueNumber, hierarchyLevel, specDir, specContext = '') {
  const phase = resolveInitialProgressionPhase(engine, hierarchyLevel, specContext);
  const inputs = buildPhaseProgressionInputs({ issueNumber, phase, hierarchyLevel, specDir, specContext });
  await github.rest.actions.createWorkflowDispatch({
    owner: 'swai-factory',
    repo: 'agentic-devtools',
    workflow_id: 'speckit-phase-progression.yml',
    ref: 'main',
    inputs,
  });
}

async function dispatchFollowing(github, issueNumber, skippedPhase, hierarchyLevel, specDir = '', specContext = '') {
  if (skippedPhase >= 3) return;
  const inputs = buildPhaseProgressionInputs({
    issueNumber,
    phase: skippedPhase + 1,
    hierarchyLevel,
    specDir,
    specContext,
  });
  await github.rest.actions.createWorkflowDispatch({
    owner: 'swai-factory',
    repo: 'agentic-devtools',
    workflow_id: 'speckit-phase-progression.yml',
    ref: 'main',
    inputs,
  });
}

(async () => {
  console.log('=== Testing outbound hierarchy normalization ===');
  assertEqual('exports the four receiver choices', ['auto', 'feature', 'epic', 'task'], DISPATCH_HIERARCHY_LEVELS);
  for (const level of DISPATCH_HIERARCHY_LEVELS) {
    assertEqual(`preserves ${level}`, level, normalizeHierarchyLevelForDispatch(level));
    assertEqual(`trims and lowercases ${level}`, level, normalizeHierarchyLevelForDispatch(` ${level.toUpperCase()} `));
  }
  for (const value of [
    'unknown',
    ' UNKNOWN ',
    '',
    ' \t ',
    null,
    undefined,
    7,
    {},
    'unsupported',
    'task\r\nfeature',
  ]) {
    assertEqual(`maps ${JSON.stringify(value)} to auto`, 'auto', normalizeHierarchyLevelForDispatch(value));
  }
  const unmodified = { level: ' UNKNOWN ' };
  assertEqual('normalization does not mutate the input', ' UNKNOWN ', unmodified.level);
  assertEqual('explicit auto remains auto', 'auto', normalizeHierarchyLevelForDispatch(' AUTO '));

  console.log('=== Testing initial phase routing ===');
  for (const [engine, level, contextOrExpected, optionalExpected] of [
    ['cloud-agent', 'task', 1],
    ['cloud-agent', ' TASK ', 1],
    ['cloud-agent', 'task', 'specs/parent/spec.md', 3],
    ['cloud-agent', 'unknown', 1],
    ['legacy', 'task', 1],
    ['legacy', 'feature', 1],
    ['cloud-agent', 'epic', 1],
    ['cloud-agent', 'feature', 1],
    ['unsupported', 'task', 1],
  ]) {
    const context = typeof contextOrExpected === 'string' ? contextOrExpected : '';
    const expectedPhase = optionalExpected ?? contextOrExpected;
    assertEqual(
      `${engine}/${level} routes to phase ${expectedPhase}`,
      expectedPhase,
      resolveInitialProgressionPhase(engine, level, context),
    );
  }

  console.log('=== Testing shared progression input builder ===');
  assertEqual(
    'builds canonical string payloads and retains an empty spec directory',
    { issue_number: '42', phase: '3', hierarchy_level: 'auto', spec_dir: '', spec_context: '' },
    buildPhaseProgressionInputs({
      issueNumber: '0042', phase: 3, hierarchyLevel: 'unknown', specDir: '', specContext: '',
    }),
  );
  assertEqual(
    'omits an unsupplied spec directory',
    { issue_number: '42', phase: '2', hierarchy_level: 'feature' },
    buildPhaseProgressionInputs({ issueNumber: 42, phase: '2', hierarchyLevel: ' FEATURE ' }),
  );
  assertThrows('rejects zero issue numbers', 'positive integer', () =>
    buildPhaseProgressionInputs({ issueNumber: 0, phase: 1, hierarchyLevel: 'task' }));
  assertThrows('rejects negative issue numbers', 'positive integer', () =>
    buildPhaseProgressionInputs({ issueNumber: -1, phase: 1, hierarchyLevel: 'task' }));
  assertThrows('rejects malformed issue numbers', 'positive integer', () =>
    buildPhaseProgressionInputs({ issueNumber: '1.5', phase: 1, hierarchyLevel: 'task' }));
  assertThrows('rejects non-string/non-number issue numbers', 'positive integer', () =>
    buildPhaseProgressionInputs({ issueNumber: {}, phase: 1, hierarchyLevel: 'task' }));
  for (const phase of [0, 4, 'phase-1', null]) {
    assertThrows(`rejects phase ${JSON.stringify(phase)}`, '1, 2, or 3', () =>
      buildPhaseProgressionInputs({ issueNumber: 1, phase, hierarchyLevel: 'task' }));
  }
  assertEqual(
    'canonicalizes a valid numeric phase string',
    '2',
    buildPhaseProgressionInputs({ issueNumber: 1, phase: '02', hierarchyLevel: 'task' }).phase,
  );

  console.log('=== Testing initial dispatch payloads ===');
  for (const engine of ['legacy', 'cloud-agent']) {
    const github = createMockGithub();
    await dispatchInitial(github, engine, 41, 'unknown', '');
    assertEqual(
      `${engine} unknown hierarchy dispatches phase 1 using auto`,
      [{
        owner: 'swai-factory',
        repo: 'agentic-devtools',
        workflow_id: 'speckit-phase-progression.yml',
        ref: 'main',
        inputs: { issue_number: '41', phase: '1', hierarchy_level: 'auto', spec_dir: '', spec_context: '' },
      }],
      github.calls,
    );
  }
  {
    const github = createMockGithub();
    await dispatchInitial(github, 'cloud-agent', '42', 'task', 'specs/42-task', 'specs/parent/spec.md');
    assertEqual(
      'verified cloud task dispatches phase 3 with its spec directory',
      {
        issue_number: '42',
        phase: '3',
        hierarchy_level: 'task',
        spec_dir: 'specs/42-task',
        spec_context: 'specs/parent/spec.md',
      },
      github.calls[0].inputs,
    );
  }
  for (const [engine, level] of [['legacy', 'task'], ['legacy', 'feature'], ['cloud-agent', 'epic']]) {
    const github = createMockGithub();
    await dispatchInitial(github, engine, 43, level, '');
    assertEqual(`${engine}/${level} dispatches phase 1`, '1', github.calls[0].inputs.phase);
    assertEqual(`${engine}/${level} preserves its normalized hierarchy`, level, github.calls[0].inputs.hierarchy_level);
  }

  console.log('=== Testing skipped-phase self-dispatch payloads ===');
  for (const [skippedPhase, expectedPhase] of [[1, '2'], [2, '3']]) {
    const github = createMockGithub();
    await dispatchFollowing(github, 51, skippedPhase, 'unknown');
    assertEqual(
      `skipped phase ${skippedPhase} dispatches phase ${expectedPhase} with auto`,
      { issue_number: '51', phase: expectedPhase, hierarchy_level: 'auto', spec_dir: '', spec_context: '' },
      github.calls[0]?.inputs,
    );
  }
  {
    const github = createMockGithub();
    await dispatchFollowing(github, 52, 1, 'feature');
    assertEqual('self-dispatch preserves known hierarchy', 'feature', github.calls[0]?.inputs.hierarchy_level);
  }
  {
    const github = createMockGithub();
    await dispatchFollowing(github, 53, 3, 'unknown');
    assertEqual('skipped phase 3 does not dispatch another phase', 0, github.calls.length);
  }

  console.log('=== Testing durable progression dispatch context ===');
  {
    const mutations = [];
    const inputs = { issue_number: '54', phase: '2', hierarchy_level: 'auto', spec_dir: '', spec_context: '' };
    const github = { rest: {
      issues: { createComment: async args => { mutations.push(['marker', args]); } },
      actions: { createWorkflowDispatch: async args => { mutations.push(['dispatch', args]); } },
    } };
    await require('../progression-dispatch.js').dispatchRecordedProgression({
      github, context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } }, inputs,
    });
    assertEqual('records marker before dispatch', ['marker', 'dispatch'], mutations.map(entry => entry[0]));
    assertEqual(
      'records exact receiver inputs including intentional auto and empty spec directory',
      `<!-- speckit:progression-dispatch schema_version=1 ${JSON.stringify(inputs)} -->`,
      mutations[0][1].body,
    );
    assertEqual('dispatch preserves exact recorded inputs', inputs, mutations[1][1].inputs);
  }
  {
    let dispatched = false;
    const github = { rest: {
      issues: { createComment: async () => { throw new Error('marker write failed'); } },
      actions: { createWorkflowDispatch: async () => { dispatched = true; } },
    } };
    try {
      await require('../progression-dispatch.js').dispatchRecordedProgression({
        github, context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
        inputs: { issue_number: '55', phase: '1', hierarchy_level: 'feature' },
      });
      assertEqual('marker failure must propagate', true, false);
    } catch (error) {
      assertEqual('marker failure propagates', 'marker write failed', error.message);
    }
    assertEqual('marker failure prevents untracked dispatch', false, dispatched);
  }
  console.log(`\nResults: ${PASS} passed, ${FAIL} failed`);
  if (FAIL > 0) process.exit(1);
})();
