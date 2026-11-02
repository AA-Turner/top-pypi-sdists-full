#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const extractPhaseInfo = require(path.join(__dirname, '..', 'extract-phase-info.js'));

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
  const outputs = {};
  const infos = [];
  const warnings = [];
  const failures = [];
  return {
    failures,
    infos,
    outputs,
    warnings,
    info: message => infos.push(message),
    setFailed: message => failures.push(message),
    setOutput: (key, value) => { outputs[key] = value; },
    warning: message => warnings.push(message),
  };
}

function createMockGithub(changedFiles, contentByPath, issueComments = []) {
  const listComments = async () => ({ data: issueComments });
  const listFiles = async () => ({ data: changedFiles });
  const getContent = async ({ path: requestedPath }) => {
    if (Object.prototype.hasOwnProperty.call(contentByPath, requestedPath)) {
      return { data: contentByPath[requestedPath] };
    }
    const error = new Error(`Not found: ${requestedPath}`);
    error.status = 404;
    throw error;
  };
  return {
    paginate: async (_fn, params = {}) => {
      if (Object.prototype.hasOwnProperty.call(params, 'issue_number')) {
        return issueComments;
      }
      return changedFiles;
    },
    rest: {
      issues: {
        listComments,
        get: async () => ({ data: { labels: [] } }),
      },
      pulls: {
        listFiles,
      },
      repos: {
        getContent,
      },
    },
  };
}

function createReconcileGithub(issueComments, issueData = { labels: [{ name: 'feature' }] }) {
  const mutations = { added: [], removed: [] };
  return {
    mutations,
    paginate: async () => issueComments,
    rest: {
      issues: {
        listComments: async () => ({ data: issueComments }),
        get: async () => ({ data: issueData }),
        addLabels: async params => { mutations.added.push(params); },
        removeLabel: async params => { mutations.removed.push(params); },
      },
    },
  };
}

console.log('=== Testing analyzeChangedFiles ===');
{
  const result = extractPhaseInfo.analyzeChangedFiles([
    { status: 'modified', filename: 'specs/123-my-feature/plan.md' },
    { status: 'modified', filename: 'specs/123-my-feature/generated/analysis-report.md' },
  ], '');
  assertEqual('infers spec directory from changed artifacts', 'specs/123-my-feature', result.specDir);
  assertEqual('does not infer level from directory naming convention', 'unknown', result.fallbackLevel);
}
{
  const result = extractPhaseInfo.analyzeChangedFiles([
    { status: 'modified', filename: 'specs/123-widget/plan.md' },
    { status: 'modified', filename: 'specs/123-widget/generated/analysis-report.md' },
  ], '');
  assertEqual('infers spec directory from changed artifacts (no level in name)', 'specs/123-widget', result.specDir);
  assertEqual('defaults to unknown when level cannot be inferred', 'unknown', result.fallbackLevel);
}
{
  const core = createMockCore();
  const result = extractPhaseInfo.analyzeChangedFiles([
    { status: 'modified', filename: 'specs/123-first/plan.md' },
    { status: 'modified', filename: 'specs/123-second/plan.md' },
  ], 'task', core);
  assertEqual('rejects multiple changed spec directories', true, result.ambiguous);
  assertEqual('does not select an arbitrary directory', '', result.specDir);
  assertEqual('ambiguous hierarchy fails closed', 'unknown', result.fallbackLevel);
  assertEqual('logs every ambiguous directory', 1, core.warnings.length);
}

console.log('=== Testing hasTerminalArtifactSet ===');
{
  assertEqual('feature requires plan + tasks + analysis', true, extractPhaseInfo.hasTerminalArtifactSet('feature', true, true, true));
  assertEqual('feature missing tasks is not terminal', false, extractPhaseInfo.hasTerminalArtifactSet('feature', true, false, true));
  assertEqual('epic requires plan + analysis (no tasks)', true, extractPhaseInfo.hasTerminalArtifactSet('epic', true, false, true));
  assertEqual('epic missing analysis is not terminal', false, extractPhaseInfo.hasTerminalArtifactSet('epic', true, false, false));
  assertEqual('task requires only tasks', true, extractPhaseInfo.hasTerminalArtifactSet('task', false, true, false));
  assertEqual('task missing tasks is not terminal', false, extractPhaseInfo.hasTerminalArtifactSet('task', true, false, true));
  for (const hasPlan of [false, true]) {
    for (const hasTasks of [false, true]) {
      for (const hasAnalysis of [false, true]) {
        assertEqual(
          `unknown level fails closed for hasPlan=${hasPlan}, hasTasks=${hasTasks}, hasAnalysis=${hasAnalysis}`,
          false,
          extractPhaseInfo.hasTerminalArtifactSet('unknown', hasPlan, hasTasks, hasAnalysis)
        );
      }

    }
  }
}

console.log('=== Testing expectedCloudBaseRef ===');
{
  assertEqual('phase 1 routes to main', 'main', extractPhaseInfo.expectedCloudBaseRef(10, 1, 'feature'));
  assertEqual(
    'phase 2 routes to phase-1 specify branch',
    'speckit/10/phase-1-specify',
    extractPhaseInfo.expectedCloudBaseRef(10, 2, 'feature')
  );
  assertEqual(
    'phase 3 feature routes to phase-2 clarify branch',
    'speckit/10/phase-2-clarify',
    extractPhaseInfo.expectedCloudBaseRef(10, 3, 'feature')
  );
  assertEqual('phase 3 task routes to main', 'main', extractPhaseInfo.expectedCloudBaseRef(10, 3, 'task'));
}

console.log('=== Testing extractIssueNumberFromPr ===');
{
  const cloudMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=999 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-dddddddddddd -->';
  assertEqual(
    'extracts issue number from speckit branch',
    123,
    extractPhaseInfo.extractIssueNumberFromPr({
      head: { ref: 'speckit/123/phase-2-clarify' },
      body: `${cloudMarker}\nRelates to #456`,
    })
  );
  assertEqual(
    'ignores untrusted cloud marker in body fallback and uses Relates to',
    456,
    extractPhaseInfo.extractIssueNumberFromPr({
      head: { ref: 'copilot/fix-456' },
      body: `${cloudMarker}\nRelates to #456`,
    })
  );
  assertEqual(
    'extracts issue number from Closes reference on a Copilot branch',
    457,
    extractPhaseInfo.extractIssueNumberFromPr({
      head: { ref: 'copilot/fix-457' },
      body: 'Closes #457',
    })
  );
  assertEqual(
    'returns null when non-speckit branch has no Relates-to reference',
    null,
    extractPhaseInfo.extractIssueNumberFromPr({
      head: { ref: 'copilot/fix-no-relates' },
      body: cloudMarker,
    })
  );
}
{
  const unsupportedMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=999 phase=4 hierarchy=feature correlation_id=11111111-1111-4111-8111-dddddddddddd -->';
  assertEqual(
    'rejects Cloud Agent markers above phase 3',
    null,
    extractPhaseInfo.parseCloudAgentMarker(unsupportedMarker)
  );
}

console.log('=== Testing parseHierarchyLevel ===');
{
  assertEqual(
    'accepts valid YAML inline comments after unquoted supported levels',
    'task',
    extractPhaseInfo.parseHierarchyLevel('level: task # inherited context\n', 'unknown')
  );
  assertEqual(
    'treats unspaced hashes as scalar content and fails closed',
    'unknown',
    extractPhaseInfo.parseHierarchyLevel('level: task#typo\n', 'unknown')
  );
  assertEqual(
    'treats quoted hashes as scalar content and fails closed',
    'unknown',
    extractPhaseInfo.parseHierarchyLevel('level: "task # typo"\n', 'unknown')
  );
  assertEqual(
    'treats duplicate top-level level keys as invalid and fails closed',
    'unknown',
    extractPhaseInfo.parseHierarchyLevel('level: epic\nlevel: task\n', 'unknown')
  );
  assertEqual(
    'reports malformed level declarations as invalid metadata',
    { level: 'unknown', valid: false },
    extractPhaseInfo.parseHierarchyLevel('level: task\nlevel: "feature\n', 'unknown', true)
  );
}

console.log('=== Testing collectSpecDirectoriesForIssue ===');
{
  assertEqual(
    'returns empty list when specs root is missing',
    [],
    extractPhaseInfo.collectSpecDirectoriesForIssue('/path/that/does/not/exist', '10')
  );
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-'));
  try {
    const specsRoot = path.join(tempRoot, 'specs');
    fs.mkdirSync(path.join(specsRoot, '10-legacy-flat'), { recursive: true });
    fs.mkdirSync(path.join(specsRoot, '10-abc'), { recursive: true });
    fs.mkdirSync(path.join(specsRoot, '10', '11', '12'), { recursive: true });
    fs.mkdirSync(path.join(specsRoot, '100-should-not-match-issue-10'), { recursive: true });
    const matches = extractPhaseInfo.collectSpecDirectoriesForIssue(specsRoot, '10');
    assertEqual(
      'collects both flat and nested directories for an issue',
      [path.join(specsRoot, '10'), path.join(specsRoot, '10-abc'), path.join(specsRoot, '10-legacy-flat')],
      matches
    );
    const issueOneMatches = extractPhaseInfo.collectSpecDirectoriesForIssue(specsRoot, '1');
    assertEqual('does not treat 10-* as a match for issue 1', [], issueOneMatches);
  } finally {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
}

console.log('=== Testing workflow_dispatch path ===');
(async () => {
  const core = createMockCore();
  await extractPhaseInfo.run({
    github: createMockGithub([], {}),
    context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
    core,
    workflowDispatchPhase: '2',
    workflowDispatchIssueNumber: '321',
  });
  assertEqual('workflow_dispatch sets completed_phase', '1', core.outputs.completed_phase);
  assertEqual('workflow_dispatch sets next_phase', '2', core.outputs.next_phase);
  assertEqual('workflow_dispatch sets next_phase_name', 'clarify', core.outputs.next_phase_name);
  assertEqual('workflow_dispatch sets issue_number', '321', core.outputs.issue_number);
  assertEqual('workflow_dispatch defaults hierarchy level to unknown', 'unknown', core.outputs.terminal_hierarchy_level);
  assertEqual('workflow_dispatch defaults task downgrade signal to false', 'false', core.outputs.task_downgraded);
  assertEqual('workflow_dispatch defaults task-resolution failure signal to false', 'false', core.outputs.task_resolution_failed);

  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-parentless-task-dispatch-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const github = createMockGithub([], {});
      github.rest.issues = {
        get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
      };
      github.graphql = async () => ({ repository: { issue: { parent: null } } });
      const dispatchCore = createMockCore();
      await extractPhaseInfo.run({
        github,
        context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
        core: dispatchCore,
        workflowDispatchPhase: '3',
        workflowDispatchIssueNumber: '99002',
      });
      assertEqual('direct Phase 3 dispatch downgrades a parentless Task to Feature', 'feature', dispatchCore.outputs.terminal_hierarchy_level);
      assertEqual('direct Phase 3 dispatch exposes the verified Task downgrade', 'true', dispatchCore.outputs.task_downgraded);
      assertEqual('direct Phase 3 dispatch reports successful Task parent resolution', 'false', dispatchCore.outputs.task_resolution_failed);
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-task-parent-lookup-failure-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const github = createMockGithub([], {});
      github.rest.issues = {
        get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
      };
      github.graphql = async () => {
        throw new Error('parent lookup unavailable');
      };
      const dispatchCore = createMockCore();
      await extractPhaseInfo.run({
        github,
        context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
        core: dispatchCore,
        workflowDispatchPhase: '3',
        workflowDispatchIssueNumber: '99003',
      });
      assertEqual('Task parent lookup failure remains unknown', 'unknown', dispatchCore.outputs.terminal_hierarchy_level);
      assertEqual('Task parent lookup failure is surfaced for explicit handling', 'true', dispatchCore.outputs.task_resolution_failed);
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-dispatch-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '321'), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, 'specs', '321', 'hierarchy.yml'), 'level: epic\n', 'utf8');
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const dispatchCore = createMockCore();
        await extractPhaseInfo.run({
          github: createMockGithub([], {}),
          context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
          core: dispatchCore,
          workflowDispatchPhase: '2',
          workflowDispatchIssueNumber: '321',
        });
        assertEqual(
          'workflow_dispatch derives hierarchy from local hierarchy.yml when present',
          'epic',
          dispatchCore.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-dispatch-ambiguous-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '321-first'), { recursive: true });
      fs.mkdirSync(path.join(tempRoot, 'specs', '321-second'), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, 'specs', '321-first', 'hierarchy.yml'), 'level: task\n', 'utf8');
      fs.writeFileSync(path.join(tempRoot, 'specs', '321-second', 'hierarchy.yml'), 'level: task\n', 'utf8');
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const dispatchCore = createMockCore();
        const github = createMockGithub([], {});
        github.rest.issues = {
          get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
        };
        await extractPhaseInfo.run({
          github,
          context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
          core: dispatchCore,
          workflowDispatchPhase: '2',
          workflowDispatchIssueNumber: '321',
        });
        assertEqual(
          'workflow_dispatch fails closed for ambiguous hierarchy despite task metadata',
          'unknown',
          dispatchCore.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-dispatch-malformed-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '321'), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, 'specs', '321', 'hierarchy.yml'), 'level: "task\n', 'utf8');
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const dispatchCore = createMockCore();
        const github = createMockGithub([], {});
        github.rest.issues = {
          get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
        };
        await extractPhaseInfo.run({
          github,
          context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
          core: dispatchCore,
          workflowDispatchPhase: '2',
          workflowDispatchIssueNumber: '321',
        });
        assertEqual(
          'workflow_dispatch fails closed for malformed hierarchy despite task metadata',
          'unknown',
          dispatchCore.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  {
    // Use a directory named hierarchy.yml so existsSync returns true but readFileSync throws EISDIR.
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-dispatch-unreadable-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '321', 'hierarchy.yml'), { recursive: true });
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const dispatchCore = createMockCore();
        const github = createMockGithub([], {});
        github.rest.issues = {
          get: async () => ({ data: { labels: [{ name: 'Epic' }], type: { name: 'Epic' } } }),
        };
        await extractPhaseInfo.run({
          github,
          context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
          core: dispatchCore,
          workflowDispatchPhase: '2',
          workflowDispatchIssueNumber: '321',
        });
        assertEqual(
          'unreadable hierarchy.yml fails closed to unknown, preserving Epic override only',
          'epic',
          dispatchCore.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  console.log('=== Testing merged phase-3 terminal routing ===');
  {
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/123-feature-demo/plan.md' },
      { status: 'modified', filename: 'specs/123-feature-demo/tasks.md' },
      { status: 'modified', filename: 'specs/123-feature-demo/generated/analysis-report.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/123-feature-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'file', name: 'tasks.md' },
        { type: 'dir', name: 'generated' },
      ],
      'specs/123-feature-demo/generated': [
        { type: 'file', name: 'analysis-report.md' },
      ],
      'specs/123-feature-demo/hierarchy.yml': {
        type: 'file',
        content: Buffer.from('level: feature\n', 'utf8').toString('base64'),
      },
    });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 17,
            labels: [{ name: 'speckit:phase-3' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/123/phase-3-plan' },
            body: '',
            merge_commit_sha: 'abc123',
            html_url: 'https://example.test/pr/17',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('terminal merged phase-3 routes to completion sentinel', '4', core.outputs.next_phase);
    assertEqual('terminal merged phase-3 preserves issue number', '123', core.outputs.issue_number);
    assertEqual('terminal merged phase-3 records hierarchy level', 'feature', core.outputs.terminal_hierarchy_level);
    assertTruthy('terminal merged phase-3 logs routing decision', core.infos.some(msg => msg.includes('routing to 4 (terminal)')));
  }
  {
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/4000-epic-demo/plan.md' },
      { status: 'modified', filename: 'specs/4000-epic-demo/generated/analysis-report.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/4000-epic-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'dir', name: 'generated' },
      ],
      'specs/4000-epic-demo/generated': [
        { type: 'file', name: 'analysis-report.md' },
      ],
      'specs/4000-epic-demo/hierarchy.yml': {
        type: 'file',
        content: Buffer.from('level: feature\n', 'utf8').toString('base64'),
      },
    });
    github.rest.issues = {
      get: async () => ({ data: { labels: [{ name: 'Epic' }], type: { name: 'Epic' } } }),
    };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 47,
            labels: [{ name: 'speckit:phase-3' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/4000/phase-3-plan' },
            body: '',
            merge_commit_sha: 'epic4000',
            html_url: 'https://example.test/pr/47',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('authoritative Epic issue metadata overrides stale feature PR label', 'epic', core.outputs.terminal_hierarchy_level);
  }
  {
    // hierarchy.yml absent: authoritative task level must be preserved, not overridden by stale PR label.
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/5000-task-demo/plan.md' },
      { status: 'modified', filename: 'specs/5000-task-demo/tasks.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/5000-task-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'file', name: 'tasks.md' },
      ],
    });
    github.rest.issues = {
      get: async () => ({ data: { labels: [{ name: 'task' }], type: null } }),
    };
    github.graphql = async () => ({
      repository: { issue: { parent: { number: 100, repository: { nameWithOwner: 'swai-factory/agentic-devtools' } } } },
    });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 48,
            labels: [{ name: 'speckit:phase-3' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/5000/phase-3-plan' },
            body: '',
            merge_commit_sha: 'task5000',
            html_url: 'https://example.test/pr/48',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('absent hierarchy.yml preserves authoritative task level over stale feature PR label', 'task', core.outputs.terminal_hierarchy_level);
  }
  {
    // hierarchy.yml absent with no authoritative issue level: preserve the validated PR-label fallback.
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/5002-feature-demo/plan.md' },
      { status: 'modified', filename: 'specs/5002-feature-demo/tasks.md' },
      { status: 'modified', filename: 'specs/5002-feature-demo/generated/analysis-report.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/5002-feature-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'file', name: 'tasks.md' },
        { type: 'dir', name: 'generated' },
      ],
      'specs/5002-feature-demo/generated': [
        { type: 'file', name: 'analysis-report.md' },
      ],
    });
    github.rest.issues = {
      get: async () => ({ data: { labels: [], type: null } }),
    };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 49,
            labels: [{ name: 'speckit:phase-3' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/5002/phase-3-plan' },
            body: '',
            merge_commit_sha: 'feature5002',
            html_url: 'https://example.test/pr/49',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('absent hierarchy.yml preserves validated feature fallback when issue metadata is empty', 'feature', core.outputs.terminal_hierarchy_level);
  }
  {
    // A present-but-empty hierarchy.yml is malformed canonical metadata, not an absent file.
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/5001-task-demo/plan.md' },
      { status: 'modified', filename: 'specs/5001-task-demo/tasks.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/5001-task-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'file', name: 'tasks.md' },
      ],
      'specs/5001-task-demo/hierarchy.yml': {
        type: 'file',
        content: '',
      },
    });
    github.rest.issues = {
      get: async () => ({ data: { labels: [{ name: 'Task' }], type: null } }),
    };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 49,
            labels: [{ name: 'speckit:phase-3' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/5001/phase-3-plan' },
            body: '',
            merge_commit_sha: 'task5001',
            html_url: 'https://example.test/pr/49',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('empty hierarchy.yml fails closed instead of falling back to authoritative task metadata', 'unknown', core.outputs.terminal_hierarchy_level);
  }

  console.log('=== Testing legacy phase-3 recovery routing ===');
  {
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/456-epic-demo/plan.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/456-epic-demo': [
        { type: 'file', name: 'plan.md' },
      ],
      'specs/456-epic-demo/hierarchy.yml': {
        type: 'file',
        content: Buffer.from('level: epic\n', 'utf8').toString('base64'),
      },
    });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 18,
            labels: [{ name: 'speckit:phase-3' }],
            head: { ref: 'speckit/456/phase-3-plan' },
            body: '',
            merge_commit_sha: 'def456',
            html_url: 'https://example.test/pr/18',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('legacy plan-only phase-3 routes back through phase 3', '3', core.outputs.next_phase);
    assertEqual('legacy plan-only phase-3 records inferred epic level', 'epic', core.outputs.terminal_hierarchy_level);
  }

  console.log('=== Testing legacy phase-4 routing ===');
  {
    // Task-level issue: tasks.md is the terminal artifact → routes to completion sentinel (4).
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/10/42/555-task-demo/tasks.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/10/42/555-task-demo': [
        { type: 'file', name: 'tasks.md' },
      ],
      'specs/10/42/555-task-demo/hierarchy.yml': {
        type: 'file',
        content: Buffer.from('level: task\n', 'utf8').toString('base64'),
      },
    });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 30,
            labels: [{ name: 'speckit:phase-4' }],
            head: { ref: 'speckit/555/phase-4-tasks' },
            body: '',
            merge_commit_sha: 'legacy04a',
            html_url: 'https://example.test/pr/30',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('legacy phase-4 task with tasks.md routes to completion sentinel', '4', core.outputs.next_phase);
    assertEqual('legacy phase-4 task records task level', 'task', core.outputs.terminal_hierarchy_level);
    assertTruthy('legacy phase-4 task logs routing to terminal', core.infos.some(msg => msg.includes('routing to 4 (terminal)')));
  }
  {
    // Feature-level issue: no analysis-report.md → terminal artifact incomplete → routes back to phase 3.
    const core = createMockCore();
    const changedFiles = [
      { status: 'modified', filename: 'specs/666-feature-demo/plan.md' },
      { status: 'modified', filename: 'specs/666-feature-demo/tasks.md' },
    ];
    const github = createMockGithub(changedFiles, {
      'specs/666-feature-demo': [
        { type: 'file', name: 'plan.md' },
        { type: 'file', name: 'tasks.md' },
      ],
      'specs/666-feature-demo/hierarchy.yml': {
        type: 'file',
        content: Buffer.from('level: feature\n', 'utf8').toString('base64'),
      },
    });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 31,
            labels: [{ name: 'speckit:phase-4' }],
            head: { ref: 'speckit/666/phase-4-tasks' },
            body: '',
            merge_commit_sha: 'legacy04b',
            html_url: 'https://example.test/pr/31',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('legacy phase-4 feature without analysis-report.md routes to phase-3 recovery', '3', core.outputs.next_phase);
    assertEqual('legacy phase-4 feature records feature level', 'feature', core.outputs.terminal_hierarchy_level);
    assertTruthy('legacy phase-4 feature logs routing to legacy recovery', core.infos.some(msg => msg.includes('routing to 3 (legacy recovery)')));
  }

  console.log('=== Testing phase-1/2 terminal_hierarchy_level output ===');
  {
    const core = createMockCore();
    const github = createMockGithub([], {});
    github.rest.issues.get = async () => ({ data: { labels: [{ name: 'task' }] } });
    github.graphql = async () => { throw new Error('parent lookup unavailable'); };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 18,
            labels: [{ name: 'speckit:phase-1' }],
            head: { ref: 'speckit/788/phase-1-specify' },
            body: '',
            merge_commit_sha: 'failed-task-parent',
            html_url: 'https://example.test/pr/18',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual(
      'merged PR propagates failed Task parent resolution to guarded failure handling',
      'true',
      core.outputs.task_resolution_failed
    );
  }
  {
    const core = createMockCore();
    const github = createMockGithub([], {});
    github.rest.issues.get = async () => ({ data: { labels: [{ name: 'task' }] } });
    github.graphql = async () => ({ repository: { issue: { parent: null } } });
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 19,
            labels: [{ name: 'speckit:phase-3' }],
            head: { ref: 'speckit/789/phase-3-plan' },
            body: '',
            merge_commit_sha: 'downgraded-task',
            html_url: 'https://example.test/pr/19',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('merged PR propagates verified Task downgrade to cascade handling', 'true', core.outputs.task_downgraded);
  }
  {
    const core = createMockCore();
    const github = createMockGithub([], {});
    github.rest.issues = {
      get: async () => ({ data: { labels: [{ name: 'Epic' }], type: { name: 'Epic' } } }),
    };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 19,
            labels: [{ name: 'speckit:phase-1' }, { name: 'speckit:level-epic' }],
            head: { ref: 'speckit/789/phase-1-specify' },
            body: '',
            merge_commit_sha: 'ghi789',
            html_url: 'https://example.test/pr/19',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('phase-1 with level label passes labeled level through', 'epic', core.outputs.terminal_hierarchy_level);
    assertEqual('phase-1 with level label routes to next phase', '2', core.outputs.next_phase);
  }
  {
    // When the issue API fails transiently, fall closed to unknown rather than
    // accepting stale PR labels as authoritative hierarchy metadata.
    const core = createMockCore();
    const github = createMockGithub([], {});
    github.rest.issues = {
      get: async () => { throw Object.assign(new Error('Service unavailable'), { status: 503 }); },
    };
    await extractPhaseInfo.run({
      github,
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 19,
            labels: [{ name: 'speckit:phase-1' }, { name: 'speckit:level-feature' }],
            head: { ref: 'speckit/789/phase-1-specify' },
            body: '',
            merge_commit_sha: 'ghi789',
            html_url: 'https://example.test/pr/19',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('phase-1 api failure falls closed to unknown ignoring stale level label', 'unknown', core.outputs.terminal_hierarchy_level);
  }
  {
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 20,
            labels: [{ name: 'speckit:phase-1' }],
            head: { ref: 'speckit/790/phase-1-specify' },
            body: '',
            merge_commit_sha: 'jkl012',
            html_url: 'https://example.test/pr/20',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('phase-1 without level label defaults to unknown when no artifacts can be inspected', 'unknown', core.outputs.terminal_hierarchy_level);
    assertEqual('phase-1 without level label routes to next phase', '2', core.outputs.next_phase);
  }
  {
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=23 correlation_id=none -->',
          user: { login: 'github-actions[bot]' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 23,
            labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
            base: { ref: 'speckit/792/phase-1-specify' },
            head: { ref: 'copilot/implement-792' },
            body: 'Closes #792',
            merge_commit_sha: 'copilot123',
            html_url: 'https://example.test/pr/23',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('normalized Copilot branch uses the validated phase label', '2', core.outputs.completed_phase);
    assertEqual('normalized Copilot branch uses the PR issue reference', '792', core.outputs.issue_number);
    assertEqual('normalized Copilot branch advances phase progression', '3', core.outputs.next_phase);
  }
  {
    // Regression: a previously normalized Cloud Agent PR keeps its speckit:phase-N label
    // and an earlier UUID-correlated normalizer success comment. If the PR body marker is
    // later stripped and an "edited" normalizer run posts a fresh correlation_id=none
    // success comment, the markerless fallback must not treat this as a legacy markerless
    // PR and must not advance the superseded assignment.
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=24 correlation_id=11111111-1111-4111-8111-dddddddddddd -->',
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=24 correlation_id=none -->',
          created_at: '2026-01-02T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 24,
            labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
            base: { ref: 'speckit/793/phase-1-specify' },
            head: { ref: 'copilot/implement-793' },
            body: 'Closes #793',
            merge_commit_sha: 'copilot124',
            html_url: 'https://example.test/pr/24',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual(
      'superseded normalized Copilot PR with stripped marker is skipped rather than advanced',
      '0',
      core.outputs.next_phase
    );
    assertEqual(
      'superseded normalized Copilot PR with stripped marker clears issue number output',
      '0',
      core.outputs.issue_number
    );
    assertTruthy(
      'superseded normalized Copilot PR logs a warning that the fallback was skipped',
      core.warnings.some(msg => msg.includes('Skipping Copilot fallback') && msg.includes('normalization did not succeed'))
    );
  }
  {
    // Regression (label-stripped variant): same superseded-assignment scenario, but the
    // speckit:phase-N label was also removed alongside the body marker, so the check in
    // `hasSuccessfulNormalization`'s initial computation path (not just the branch fallback)
    // must also refuse to treat the PR as legacy markerless.
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=25 correlation_id=22222222-2222-4222-8222-eeeeeeeeeeee -->',
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=25 correlation_id=none -->',
          created_at: '2026-01-02T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 25,
            labels: [],
            base: { ref: 'speckit/794/phase-1-specify' },
            head: { ref: 'copilot/implement-794' },
            body: 'Closes #794',
            merge_commit_sha: 'copilot125',
            html_url: 'https://example.test/pr/25',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'superseded normalized Copilot PR without label logs the prior-correlation warning',
      core.warnings.some(msg => msg.includes('prior UUID-correlated normalization'))
    );
    assertTruthy(
      'superseded normalized Copilot PR without label fails closed for missing phase info',
      core.failures.some(msg => msg.includes('Could not extract phase number from PR labels or cloud-agent marker'))
    );
  }
  {
    // Regression: the normalizer workflow posts its status comments through
    // `github-script` using a PAT (`SPECKIT_PR_TOKEN`, `COPILOT_GITHUB_TOKEN`, or
    // `DEFAULT_CLASSIC_REPO_WORKFLOW_PAT`), so GitHub attributes the comment to the
    // PAT owner rather than `github-actions[bot]`, with `author_association` reflecting
    // that account's real repo role (e.g. `MEMBER`) instead of `BOT`. The
    // stale-assignment guard must still recognize the earlier UUID-correlated success
    // comment under this real author shape (the exact `AMARSNIK_swica` login trusted
    // for PAT-authored automation) and refuse to trust the later `correlation_id=none`
    // comment.
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: '<!-- speckit:agent-pr-normalizer pr=26 correlation_id=33333333-3333-4333-8333-ffffffffffff -->',
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'AMARSNIK_swica' },
        },
        {
          author_association: 'MEMBER',
          body: '<!-- speckit:agent-pr-normalizer pr=26 correlation_id=none -->',
          created_at: '2026-01-02T00:00:00Z',
          user: { login: 'AMARSNIK_swica' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 26,
            labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }],
            base: { ref: 'speckit/795/phase-1-specify' },
            head: { ref: 'copilot/implement-795' },
            body: 'Closes #795',
            merge_commit_sha: 'copilot126',
            html_url: 'https://example.test/pr/26',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual(
      'superseded normalized Copilot PR is skipped when normalizer comments use a PAT-owner author shape',
      '0',
      core.outputs.next_phase
    );
    assertTruthy(
      'PAT-owner authored normalizer comments still trigger the prior-correlation warning',
      core.warnings.some(msg => msg.includes('Skipping Copilot fallback') && msg.includes('normalization did not succeed'))
    );
  }
  {
    // Security regression: `author_association` describes a commenter's repo role, not
    // the credential that authored the comment. An arbitrary current OWNER/MEMBER/
    // COLLABORATOR (i.e. not the exact `AMARSNIK_swica` login trusted for PAT-authored
    // automation) must not be able to forge a `speckit:agent-pr-normalizer` success
    // marker just by holding a privileged repo role.
    const core = createMockCore();
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'OWNER',
          body: '<!-- speckit:agent-pr-normalizer pr=27 correlation_id=none -->\n\n- Phase: 2',
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'some-other-owner' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 27,
            labels: [],
            base: { ref: 'main' },
            head: { ref: 'copilot/implement-796' },
            body: 'Closes #796',
            merge_commit_sha: 'copilot127',
            html_url: 'https://example.test/pr/27',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'an untrusted OWNER/MEMBER/COLLABORATOR login cannot forge a normalizer success marker',
      core.failures.some(msg => msg.includes('Could not extract phase number from PR labels or cloud-agent marker'))
    );
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-pr-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '790'), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, 'specs', '790', 'hierarchy.yml'), 'level: epic\n', 'utf8');
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const core = createMockCore();
        await extractPhaseInfo.run({
          github: createMockGithub([], {}),
          context: {
            eventName: 'pull_request',
            payload: {
              pull_request: {
                number: 21,
                labels: [{ name: 'speckit:phase-1' }],
                head: { ref: 'speckit/790/phase-1-specify' },
                body: '',
                merge_commit_sha: 'mno345',
                html_url: 'https://example.test/pr/21',
              },
            },
            repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
          },
          core,
          workflowDispatchPhase: '',
          workflowDispatchIssueNumber: '',
        });
        assertEqual(
          'phase-1 without label derives level from hierarchy.yml in workspace',
          'epic',
          core.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  console.log('=== Testing authoritative cloud marker validation ===');
  {
    const core = createMockCore();
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=888 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-aaaaaaaaaaaa -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: marker,
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'AMARSNIK_swica' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 45,
            user: { login: 'copilot-swe-agent[bot]' },
            labels: [],
            base: { ref: 'speckit/888/phase-1-specify' },
            head: { ref: 'copilot/fix-888' },
            body: marker,
            merge_commit_sha: 'marker123',
            html_url: 'https://example.test/pr/45',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertEqual('trusted cloud marker sets completed phase when label is missing', '2', core.outputs.completed_phase);
    assertEqual('trusted cloud marker advances next phase', '3', core.outputs.next_phase);
    assertEqual('trusted cloud marker sets issue number', '888', core.outputs.issue_number);
  }
  {
    // Security regression: an assignment marker comment posted by an arbitrary
    // OWNER/MEMBER/COLLABORATOR (i.e. not the exact `AMARSNIK_swica` login trusted for
    // PAT-authored automation, and not the legacy `github-actions[bot]`/`BOT` shape)
    // must not be treated as authoritative just because of its repo role.
    const core = createMockCore();
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=891 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-eeeeeeeeeeee -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: marker,
          created_at: '2026-01-01T00:00:00Z',
          user: { login: 'some-other-member' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 48,
            user: { login: 'copilot-swe-agent[bot]' },
            labels: [],
            base: { ref: 'speckit/891/phase-1-specify' },
            head: { ref: 'copilot/fix-891' },
            body: marker,
            merge_commit_sha: 'marker126',
            html_url: 'https://example.test/pr/48',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'an untrusted OWNER/MEMBER/COLLABORATOR login cannot authenticate an assignment marker',
      core.failures.some(msg => msg.includes('Could not extract phase number from PR labels or cloud-agent marker'))
    );
  }
  {
    const core = createMockCore();
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=889 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-bbbbbbbbbbbb -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: marker.replace('bbbbbbbbbbbb', 'cccccccccccc'),
          created_at: '2026-01-01T00:00:00Z',
        },
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=46 correlation_id=none -->\n\n- Phase: 2',
          created_at: '2026-01-02T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 46,
            user: { login: 'copilot-swe-agent[bot]' },
            labels: [],
            base: { ref: 'speckit/889/phase-1-specify' },
            head: { ref: 'copilot/fix-889' },
            body: marker,
            merge_commit_sha: 'marker124',
            html_url: 'https://example.test/pr/46',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'unmatched cloud marker is rejected without phase label',
      core.failures.some(msg => msg.includes('Could not extract phase number from PR labels or cloud-agent marker'))
    );
  }
  {
    const core = createMockCore();
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=890 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-cccccccccccc -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: marker.replace('cccccccccccc', 'dddddddddddd'),
          created_at: '2026-01-01T00:00:00Z',
        },
        {
          author_association: 'BOT',
          body: '<!-- speckit:agent-pr-normalizer pr=47 correlation_id=none -->\n\n- Phase: 2',
          created_at: '2026-01-02T00:00:00Z',
          user: { login: 'github-actions[bot]' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 47,
            user: { login: 'copilot-swe-agent[bot]' },
            labels: [{ name: 'speckit:phase-2' }],
            base: { ref: 'speckit/890/phase-1-specify' },
            head: { ref: 'copilot/fix-890' },
            body: marker,
            merge_commit_sha: 'marker125',
            html_url: 'https://example.test/pr/47',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'unmatched cloud marker fails closed even when the stale PR still has a phase label and success comment',
      core.failures.some(msg => msg.includes('non-authoritative cloud-agent marker'))
    );
  }
  {
    const core = createMockCore();
    const staleMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=892 phase=1 hierarchy=feature correlation_id=22222222-2222-4222-8222-bbbbbbbbbbbb -->';
    const currentMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=892 phase=2 hierarchy=feature correlation_id=33333333-3333-4333-8333-cccccccccccc -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: staleMarker,
          created_at: '2026-01-01T00:00:00Z',
          id: 201,
          user: { login: 'AMARSNIK_swica' },
        },
        {
          author_association: 'MEMBER',
          body: currentMarker,
          created_at: '2026-01-01T00:00:00Z',
          id: 202,
          user: { login: 'AMARSNIK_swica' },
        },
      ]),
      context: {
        eventName: 'pull_request',
        payload: {
          pull_request: {
            number: 49,
            user: { login: 'copilot-swe-agent[bot]' },
            labels: [],
            base: { ref: 'main' },
            head: { ref: 'copilot/fix-892' },
            body: staleMarker,
            merge_commit_sha: 'marker127',
            html_url: 'https://example.test/pr/49',
          },
        },
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
      },
      core,
      workflowDispatchPhase: '',
      workflowDispatchIssueNumber: '',
    });
    assertTruthy(
      'a cloud marker superseded by an equal-timestamp later phase fails extraction',
      core.failures.some(msg => msg.includes('non-authoritative cloud-agent marker'))
    );
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-pr-ambiguous-'));
    try {
      fs.mkdirSync(path.join(tempRoot, 'specs', '791-first'), { recursive: true });
      fs.mkdirSync(path.join(tempRoot, 'specs', '791-second'), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, 'specs', '791-first', 'hierarchy.yml'), 'level: feature\n', 'utf8');
      fs.writeFileSync(path.join(tempRoot, 'specs', '791-second', 'hierarchy.yml'), 'level: task\n', 'utf8');
      const prevWorkspace = process.env.GITHUB_WORKSPACE;
      try {
        process.env.GITHUB_WORKSPACE = tempRoot;
        const core = createMockCore();
        const github = createMockGithub([], {});
        github.rest.issues = {
          get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
        };
        await extractPhaseInfo.run({
          github,
          context: {
            eventName: 'pull_request',
            payload: {
              pull_request: {
                number: 22,
                labels: [{ name: 'speckit:phase-1' }],
                head: { ref: 'speckit/791/phase-1-specify' },
                body: '',
                merge_commit_sha: 'pqr678',
                html_url: 'https://example.test/pr/22',
              },
            },
            repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
          },
          core,
          workflowDispatchPhase: '',
          workflowDispatchIssueNumber: '',
        });
        assertEqual(
          'phase-1 fails closed to unknown when workspace hierarchy is ambiguous',
          'unknown',
          core.outputs.terminal_hierarchy_level
        );
      } finally {
        process.env.GITHUB_WORKSPACE = prevWorkspace;
      }
    } finally {
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  console.log('=== Testing parentless Task Phase 1-to-3 progression with reused Task metadata ===');
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-parentless-task-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const issueNumber = 99001;
      const specDir = `specs/${issueNumber}-feature`;
      fs.mkdirSync(path.join(tempRoot, specDir), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, specDir, 'hierarchy.yml'), 'level: task\n', 'utf8');
      for (const [completedPhase, expectedNextPhase] of [[1, '2'], [2, '3'], [3, '4']]) {
        const changedFiles = completedPhase === 3
          ? [
            { status: 'modified', filename: `${specDir}/plan.md` },
            { status: 'modified', filename: `${specDir}/tasks.md` },
            { status: 'modified', filename: `${specDir}/generated/analysis-report.md` },
          ]
          : [{ status: 'modified', filename: `${specDir}/spec.md` }];
        const contentByPath = completedPhase === 3
          ? {
            [specDir]: [
              { type: 'file', name: 'spec.md' },
              { type: 'file', name: 'plan.md' },
              { type: 'file', name: 'tasks.md' },
              { type: 'dir', name: 'generated' },
            ],
            [`${specDir}/generated`]: [{ type: 'file', name: 'analysis-report.md' }],
            [`${specDir}/hierarchy.yml`]: {
              type: 'file',
              content: Buffer.from('level: task\n', 'utf8').toString('base64'),
            },
          }
          : {};
        const github = createMockGithub(changedFiles, contentByPath);
        github.rest.issues = {
          get: async () => ({ data: { labels: [] } }),
        };
        github.graphql = async () => ({ repository: { issue: { parent: null } } });
        const core = createMockCore();

        await extractPhaseInfo.run({
          github,
          context: {
            eventName: 'pull_request',
            payload: {
              pull_request: {
                number: 99,
                labels: [{ name: `speckit:phase-${completedPhase}` }],
                head: { ref: `speckit/${issueNumber}/phase-${completedPhase}-progress` },
                body: '',
                merge_commit_sha: `merge-${completedPhase}`,
                html_url: 'https://example.test/pr/99',
              },
            },
            repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
          },
          core,
          workflowDispatchPhase: '',
          workflowDispatchIssueNumber: '',
        });

        assertEqual(
          `metadata-only Task with no parent is treated as Feature after merged Phase ${completedPhase}`,
          'feature',
          core.outputs.terminal_hierarchy_level,
        );
        assertEqual(
          `parentless Task advances from Phase ${completedPhase} to ${expectedNextPhase}`,
          expectedNextPhase,
          core.outputs.next_phase,
        );
        if (completedPhase === 3) {
          assertEqual('complete standalone artifacts preserve the Feature continuation', 'false', core.outputs.standalone_prerequisites_missing);
        }
      }
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-parentless-task-invalid-metadata-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const issueNumber = 99004;
      const specDir = path.join(tempRoot, 'specs', `${issueNumber}-feature`);
      fs.mkdirSync(specDir, { recursive: true });
      fs.writeFileSync(path.join(specDir, 'hierarchy.yml'), 'level: invalid\n', 'utf8');
      const github = createMockGithub([], {});
      github.rest.issues = {
        get: async () => ({ data: { labels: [{ name: 'Task' }] } }),
      };
      github.graphql = async () => ({ repository: { issue: { parent: null } } });
      const core = createMockCore();

      await extractPhaseInfo.run({
        github,
        context: {
          eventName: 'pull_request',
          payload: {
            pull_request: {
              number: 100,
              labels: [{ name: 'speckit:phase-1' }],
              head: { ref: `speckit/${issueNumber}/phase-1-specify` },
              body: '',
              merge_commit_sha: 'invalid-parentless-task-metadata',
              html_url: 'https://example.test/pr/100',
            },
          },
          repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        },
        core,
        workflowDispatchPhase: '',
        workflowDispatchIssueNumber: '',
      });

      assertEqual('merged Phase 1 keeps verified Feature downgrade despite invalid metadata', 'feature', core.outputs.terminal_hierarchy_level);
      assertEqual('merged Phase 1 continues to clarification after verified downgrade', '2', core.outputs.next_phase);
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-parentless-task-phase3-prerequisites-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const issueNumber = 99005;
      const specDir = `specs/${issueNumber}-feature`;
      fs.mkdirSync(path.join(tempRoot, specDir), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, specDir, 'hierarchy.yml'), 'level: task\n', 'utf8');
      const github = createMockGithub(
        [{ status: 'modified', filename: `${specDir}/tasks.md` }],
        {
          [specDir]: [
            { type: 'file', name: 'tasks.md' },
            { type: 'file', name: 'hierarchy.yml' },
          ],
          [`${specDir}/hierarchy.yml`]: {
            type: 'file',
            content: Buffer.from('level: task\n', 'utf8').toString('base64'),
          },
        },
      );
      github.rest.issues = {
        get: async () => ({ data: { labels: [] } }),
      };
      github.graphql = async () => ({ repository: { issue: { parent: null } } });
      const core = createMockCore();

      await extractPhaseInfo.run({
        github,
        context: {
          eventName: 'pull_request',
          payload: {
            pull_request: {
              number: 101,
              labels: [{ name: 'speckit:phase-3' }],
              head: { ref: `speckit/${issueNumber}/phase-3-tasks` },
              body: '',
              merge_commit_sha: 'parentless-task-tasks-only',
              html_url: 'https://example.test/pr/101',
            },
          },
          repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        },
        core,
        workflowDispatchPhase: '',
        workflowDispatchIssueNumber: '',
      });

      assertEqual('merged tasks-only Phase 3 without standalone prerequisites requests restart', 'true', core.outputs.standalone_prerequisites_missing);
      assertEqual('tasks-only Phase 3 recovery is still identified as Feature', 'feature', core.outputs.terminal_hierarchy_level);
      assertEqual('tasks-only Phase 3 recovery routes to Phase 3', '3', core.outputs.next_phase);
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }
  {
    const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'extract-phase-info-parentless-task-missing-spec-'));
    const previousWorkspace = process.env.GITHUB_WORKSPACE;
    process.env.GITHUB_WORKSPACE = tempRoot;
    try {
      const issueNumber = 99006;
      const specDir = `specs/${issueNumber}-feature`;
      fs.mkdirSync(path.join(tempRoot, specDir), { recursive: true });
      fs.writeFileSync(path.join(tempRoot, specDir, 'hierarchy.yml'), 'level: task\n', 'utf8');
      const github = createMockGithub(
        [
          { status: 'modified', filename: `${specDir}/plan.md` },
          { status: 'modified', filename: `${specDir}/tasks.md` },
          { status: 'modified', filename: `${specDir}/generated/analysis-report.md` },
        ],
        {
          [specDir]: [
            { type: 'file', name: 'plan.md' },
            { type: 'file', name: 'tasks.md' },
            { type: 'dir', name: 'generated' },
            { type: 'file', name: 'hierarchy.yml' },
          ],
          [`${specDir}/generated`]: [{ type: 'file', name: 'analysis-report.md' }],
          [`${specDir}/hierarchy.yml`]: {
            type: 'file',
            content: Buffer.from('level: task\n', 'utf8').toString('base64'),
          },
        },
      );
      github.rest.issues = {
        get: async () => ({ data: { labels: [] } }),
      };
      github.graphql = async () => ({ repository: { issue: { parent: null } } });
      const core = createMockCore();

      await extractPhaseInfo.run({
        github,
        context: {
          eventName: 'pull_request',
          payload: {
            pull_request: {
              number: 102,
              labels: [{ name: 'speckit:phase-3' }],
              head: { ref: `speckit/${issueNumber}/phase-3-plan` },
              body: '',
              merge_commit_sha: 'parentless-task-complete-artifacts-missing-spec',
              html_url: 'https://example.test/pr/102',
            },
          },
          repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        },
        core,
        workflowDispatchPhase: '',
        workflowDispatchIssueNumber: '',
      });

      assertEqual('missing spec after Task downgrade requests restart', 'true', core.outputs.standalone_prerequisites_missing);
      assertEqual('terminal artifacts without spec route to Phase 3 recovery', '3', core.outputs.next_phase);
      assertEqual(
        'missing standalone prerequisite is logged as recovery',
        true,
        core.infos.some(message => message.includes('routing to 3 (standalone prerequisite recovery)')),
      );
    } finally {
      process.env.GITHUB_WORKSPACE = previousWorkspace;
      fs.rmSync(tempRoot, { recursive: true, force: true });
    }
  }

  console.log('=== Testing reconcileMergedPr mutation paths ===');
  {
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=901 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-aaaaaaaaaaaa -->';
    const github = createReconcileGithub([{
      author_association: 'MEMBER',
      body: marker,
      created_at: '2026-01-01T00:00:00Z',
      user: { login: 'AMARSNIK_swica' },
    }]);
    const core = createMockCore();
    await extractPhaseInfo.reconcileMergedPr({
      github,
      context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core,
      pr: {
        number: 90,
        body: marker,
        labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:phase-1' }, { name: 'speckit:level-feature' }],
      },
    });
    assertEqual('reconcile adds canonical labels', ['speckit:phase-2', 'speckit:level-feature', 'speckit:spec'], github.mutations.added[0].labels);
    assertEqual('reconcile removes stale phase labels', 'speckit:phase-1', github.mutations.removed[0].name);
  }
  {
    const github = createReconcileGithub([]);
    github.rest.issues.get = async () => {
      throw Object.assign(new Error('Service unavailable'), { status: 503 });
    };
    await extractPhaseInfo.reconcileMergedPr({
      github,
      context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core: createMockCore(),
      pr: { number: 91, body: 'Relates to #902', labels: [{ name: 'speckit:phase-2' }] },
    });
    assertEqual('reconcile does not mutate labels when issue API fails', 0, github.mutations.added.length);
  }
  {
    const olderMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=903 phase=2 hierarchy=feature correlation_id=33333333-3333-4333-8333-cccccccccccc -->';
    const newerMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=903 phase=2 hierarchy=feature correlation_id=44444444-4444-4444-8444-dddddddddddd -->';
    const github = createReconcileGithub([
      { author_association: 'MEMBER', body: olderMarker, created_at: '2026-01-01T00:00:00Z', id: 301, user: { login: 'AMARSNIK_swica' } },
      { author_association: 'MEMBER', body: newerMarker, created_at: '2026-01-01T00:00:00Z', id: 302, user: { login: 'AMARSNIK_swica' } },
    ]);
    await extractPhaseInfo.reconcileMergedPr({
      github,
      context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core: createMockCore(),
      pr: { number: 92, body: olderMarker, labels: [] },
    });
    assertEqual('reconcile rejects an older trusted marker with an equal timestamp', 0, github.mutations.added.length);
  }
  {
    const staleMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=905 phase=1 hierarchy=feature correlation_id=66666666-6666-4666-8666-ffffffffffff -->';
    const currentMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=905 phase=2 hierarchy=feature correlation_id=77777777-7777-4777-8777-aaaaaaaaaaaa -->';
    const github = createReconcileGithub([
      { author_association: 'MEMBER', body: staleMarker, created_at: '2026-01-01T00:00:00Z', user: { login: 'AMARSNIK_swica' } },
      { author_association: 'MEMBER', body: currentMarker, created_at: '2026-01-02T00:00:00Z', user: { login: 'AMARSNIK_swica' } },
    ]);
    await extractPhaseInfo.reconcileMergedPr({
      github,
      context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core: createMockCore(),
      pr: { number: 94, body: staleMarker, labels: [] },
    });
    assertEqual('reconcile rejects a marker superseded by a later phase', 0, github.mutations.added.length);
  }
  {
    // Security regression: an assignment marker on the source issue posted by an
    // arbitrary OWNER/MEMBER/COLLABORATOR login must not be trusted for label
    // reconciliation just because of its repo role.
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=904 phase=2 hierarchy=feature correlation_id=55555555-5555-4555-8555-eeeeeeeeeeee -->';
    const github = createReconcileGithub([{
      author_association: 'MEMBER',
      body: marker,
      created_at: '2026-01-01T00:00:00Z',
      user: { login: 'some-other-member' },
    }]);
    await extractPhaseInfo.reconcileMergedPr({
      github,
      context: { repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core: createMockCore(),
      pr: { number: 93, body: marker, labels: [] },
    });
    assertEqual('reconcile ignores an untrusted MEMBER-authored assignment marker', 0, github.mutations.added.length);
  }

  console.log('');
  console.log('=== Testing event identity resolution and locked phase recheck ===');
  for (const [issue, phase] of [['', '1'], ['0', '1'], ['321junk', '1'], ['321', '4']]) {
    const core = createMockCore();
    await extractPhaseInfo.resolveEventContext({
      github: createMockGithub([], {}),
      context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core,
      workflowDispatchIssueNumber: issue,
      workflowDispatchPhase: phase,
    });
    assertEqual(`invalid dispatch ${issue}/${phase} fails before publishing identity`, 1, core.failures.length);
    assertEqual('invalid dispatch emits no issue output', undefined, core.outputs.issue_number);
  }
  for (const [expectedIssue, state, labels, expectedPhase, failures] of [
    [undefined, 'open', [], '2', 0],
    ['321', 'open', [], '2', 0],
    ['999', 'open', [], undefined, 1],
    ['321', 'closed', [], '0', 0],
    ['321', 'open', ['speckit:completed'], '0', 0],
    ['321', 'open', ['speckit:phase-2-complete'], '0', 0],
    ['321', 'open', ['speckit:phase-3-complete'], '0', 0],
  ]) {
    const github = createMockGithub([], {});
    github.rest.issues.get = async () => ({ data: { state, labels: labels.map(name => ({ name })) } });
    const core = createMockCore();
    await extractPhaseInfo.resolveEventContext({
      github,
      context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core,
      workflowDispatchIssueNumber: '321',
      workflowDispatchPhase: '2',
      expectedIssueNumber: expectedIssue,
    });
    assertEqual(`locked ${expectedIssue}/${state}/${labels} phase`, expectedPhase, core.outputs.next_phase);
    assertEqual('locked identity failures', failures, core.failures.length);
  }
  {
    const github = createMockGithub([], {});
    github.rest.issues.get = async () => ({ data: {
      state: 'open', labels: [{ name: 'speckit:phase-3-complete' }],
    } });
    const core = createMockCore();
    await extractPhaseInfo.resolveEventContext({
      github,
      context: { eventName: 'workflow_dispatch', repo: { owner: 'swai-factory', repo: 'agentic-devtools' } },
      core,
      workflowDispatchIssueNumber: '321',
      workflowDispatchPhase: '3',
      expectedIssueNumber: '321',
    });
    assertEqual('phase-3 completion label alone does not suppress artifact recovery', '3', core.outputs.next_phase);
  }
  {
    const core = createMockCore();
    await extractPhaseInfo.resolveEventContext({
      github: createMockGithub([], {}),
      context: {
        eventName: 'pull_request',
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        payload: { pull_request: {
          number: 97, labels: [{ name: 'speckit:phase-1' }],
          head: { ref: 'unrelated-branch' }, body: '', merge_commit_sha: 'abc',
        } },
      },
      core,
    });
    assertEqual('unresolved PR fails closed', 1, core.failures.length);
    assertEqual('unresolved PR emits no issue identity', undefined, core.outputs.issue_number);
  }
  console.log('=== Testing pre-mutation merged PR identity gate ===');
  for (const expectedIssueNumber of [undefined, null, '']) {
    const core = createMockCore();
    await extractPhaseInfo.revalidateMergedPrIssueIdentity({
      github: {}, context: {}, core, expectedIssueNumber,
    });
    assertEqual('absent expected identity needs no provider lookup', [], core.failures);
  }
  {
    const core = createMockCore();
    await extractPhaseInfo.revalidateMergedPrIssueIdentity({
      github: {}, context: { payload: {} }, core, expectedIssueNumber: '321',
    });
    assertEqual('missing PR fails before any provider lookup',
      ['Resolved issue identity changed before acquiring the issue lock'], core.failures);
  }
  const identityMarker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=321 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-dddddddddddd -->';
  const otherIdentityMarker = identityMarker.replace('phase=2', 'phase=1');
  const trustedIdentityComment = { body: identityMarker, user: { login: 'AMARSNIK_swica' } };
  for (const testCase of [
    { name: 'authoritative marker overrides conflicting branch and body references',
      body: `${identityMarker}\nRelates to #999`, ref: 'speckit/999/phase-2-clarify',
      login: 'copilot-swe-agent[bot]', comments: [trustedIdentityComment], expected: '321', failures: 0, lookups: 1 },
    { name: 'authoritative marker rejects a different locked issue',
      body: identityMarker, login: 'copilot-swe-agent', comments: [trustedIdentityComment],
      expected: '999', failures: 1, lookups: 1 },
    { name: 'branch fallback accepts the locked issue', ref: 'speckit/321/phase-2-clarify',
      expected: 321, failures: 0, lookups: 0 },
    { name: 'body fallback accepts the locked issue', body: 'Closes #321',
      expected: '321', failures: 0, lookups: 0 },
    { name: 'untrusted PR author cannot override the fallback', body: identityMarker,
      ref: 'speckit/999/phase-2-clarify', login: 'contributor', expected: '999', failures: 0, lookups: 0 },
    { name: 'missing assignment marker uses the fallback', body: identityMarker,
      ref: 'speckit/999/phase-2-clarify', login: 'copilot-swe-agent',
      comments: [], expected: '999', failures: 0, lookups: 1 },
    { name: 'untrusted assignment marker uses the fallback', body: identityMarker,
      ref: 'speckit/999/phase-2-clarify', login: 'copilot-swe-agent',
      comments: [{ body: identityMarker, user: { login: 'contributor' } }],
      expected: '999', failures: 0, lookups: 1 },
    { name: 'mismatched assignment marker uses the fallback', body: identityMarker,
      ref: 'speckit/999/phase-2-clarify', login: 'copilot-swe-agent',
      comments: [{ body: otherIdentityMarker, user: { login: 'AMARSNIK_swica' } }],
      expected: '999', failures: 0, lookups: 1 },
    { name: 'assignment lookup failure warns and uses the fallback', body: identityMarker,
      ref: 'speckit/321/phase-2-clarify', login: 'copilot-swe-agent',
      lookupError: true, expected: '321', failures: 0, lookups: 1 },
    { name: 'changed fallback identity fails closed', ref: 'speckit/999/phase-2-clarify',
      expected: '321', failures: 1, lookups: 0 },
    { name: 'unresolved fallback identity fails closed',
      expected: '321', failures: 1, lookups: 0 },
    { name: 'zero fallback identity fails closed', ref: 'speckit/0/phase-2-clarify',
      expected: '321', failures: 1, lookups: 0 },
  ]) {
    const calls = { pulls: [], comments: [] };
    const github = createMockGithub([], {}, testCase.comments || []);
    github.rest.pulls.get = async params => {
      calls.pulls.push(params);
      return { data: {
        body: testCase.body || '', head: { ref: testCase.ref || 'unrelated-branch' },
        user: { login: testCase.login || 'contributor' },
      } };
    };
    github.paginate = async (method, params) => {
      calls.comments.push(params);
      assertTruthy(`${testCase.name}: reads issue comments`, method === github.rest.issues.listComments);
      if (testCase.lookupError) throw new Error('provider unavailable');
      return testCase.comments || [];
    };
    const core = createMockCore();
    await extractPhaseInfo.revalidateMergedPrIssueIdentity({
      github,
      context: {
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        payload: { pull_request: { number: 97 } },
      },
      core,
      expectedIssueNumber: testCase.expected,
    });
    assertEqual(`${testCase.name}: failure result`, testCase.failures ?
      ['Resolved issue identity changed before acquiring the issue lock'] : [], core.failures);
    assertEqual(`${testCase.name}: re-fetches authoritative PR metadata`,
      [{ owner: 'swai-factory', repo: 'agentic-devtools', pull_number: 97 }], calls.pulls);
    assertEqual(`${testCase.name}: assignment lookup`, testCase.lookups ?
      [{ owner: 'swai-factory', repo: 'agentic-devtools', issue_number: 321, per_page: 100 }] : [], calls.comments);
    assertEqual(`${testCase.name}: lookup warning`, testCase.lookupError ?
      ['Could not validate trusted cloud marker while revalidating issue identity: provider unavailable'] : [], core.warnings);
  }
  console.log('=== Testing bounded identity-provider retries ===');
  const httpError = (status, headers) => Object.assign(new Error('provider unavailable'), {
    status, response: { status, headers },
  });
  const retryCases = [
    { name: '503 then success', errors: [httpError(503)], waits: [1500] },
    { name: '503 twice then success', errors: [httpError(503), httpError(503)], waits: [1500, 3000] },
    { name: '503 exhaustion', errors: [httpError(503), httpError(503), httpError(503)],
      waits: [1500, 3000], terminal: true },
    { name: 'response status alone', errors: [{ response: { status: 503 } }], waits: [1500] },
    { name: '503 followed by permanent failure', errors: [httpError(503), httpError(403)],
      waits: [1500], terminal: true },
    { name: 'numeric Retry-After', errors: [httpError(503, { 'retry-after': '7' })], waits: [7000] },
    { name: 'HTTP-date Retry-After', errors: [httpError(503, { 'retry-after': 'Thu, 01 Jan 2026 00:00:05 GMT' })],
      waits: [5000] },
    { name: 'rate-limit reset', errors: [httpError(503, { 'x-ratelimit-reset': '1767225608' })], waits: [8000] },
    { name: 'latest hint wins', errors: [httpError(503, { 'Retry-After': '3', 'X-RateLimit-Reset': '1767225608' })],
      waits: [8000] },
    { name: 'expired hints permit immediate retry',
      errors: [httpError(503, { 'retry-after': 'Thu, 01 Jan 2026 00:00:00 GMT', 'x-ratelimit-reset': '1' })],
      waits: [0] },
    { name: 'zero hint', errors: [httpError(503, { 'retry-after': '0' })], waits: [0] },
    { name: 'invalid hints use backoff',
      errors: [httpError(503, { 'retry-after': 'invalid', 'x-ratelimit-reset': 'invalid' })], waits: [1500] },
    { name: 'negative hints use backoff',
      errors: [httpError(503, { 'retry-after': '-1', 'x-ratelimit-reset': '-1' })], waits: [1500] },
    { name: 'hint beyond cap', errors: [httpError(503, { 'retry-after': '31' })], waits: [], terminal: true },
    { name: 'oversized hint', errors: [httpError(503, { 'retry-after': '9'.repeat(400) })],
      waits: [], terminal: true },
    { name: 'reset beyond cap', errors: [httpError(503, { 'x-ratelimit-reset': '1767225631' })],
      waits: [], terminal: true },
    { name: 'aggregate cap', errors: [httpError(503, { 'retry-after': '20' }), httpError(503, { 'retry-after': '11' })],
      waits: [20000], terminal: true },
    { name: 'backoff exceeds remaining budget', errors: [httpError(503, { 'retry-after': '29' }), httpError(503)],
      waits: [29000], terminal: true },
    { name: 'exact aggregate cap', errors: [httpError(503, { 'retry-after': '20' }), httpError(503, { 'retry-after': '10' })],
      waits: [20000, 10000] },
    { name: 'identity mismatch after recovery', errors: [httpError(503)], waits: [1500], mismatch: true },
    { name: 'identity mismatch without retries', errors: [], waits: [], mismatch: true },
    ...[400, 401, 403, 404, 429, 500, 502, 504, undefined, '503'].map(status => ({
      name: `non-503 status ${status}`, errors: [httpError(status)], waits: [], terminal: true,
    })),
    { name: 'message is not confirmed status', errors: [new Error('HTTP 503')], waits: [], terminal: true },
    { name: 'provider error without message', errors: [{ status: 403 }], waits: [], terminal: true },
  ];
  for (const boundary of ['pulls', 'comments']) {
    for (const testCase of retryCases) {
      const desc = `${boundary}: ${testCase.name}`;
      const calls = { pulls: 0, comments: 0, mutations: 0 };
      const waits = [];
      let clock = Date.parse('2026-01-01T00:00:00Z');
      let caught;
      const pr = {
        number: 97,
        body: boundary === 'comments' ? identityMarker : '',
        head: { ref: 'speckit/321/phase-2-clarify' },
        user: { login: 'copilot-swe-agent[bot]' },
      };
      const github = createMockGithub([], {});
      const read = kind => {
        const attempt = calls[kind]++;
        if (kind === boundary && attempt < testCase.errors.length) throw testCase.errors[attempt];
      };
      github.rest.pulls.get = async () => {
        read('pulls');
        return { data: pr };
      };
      github.paginate = async () => {
        read('comments');
        return [trustedIdentityComment];
      };
      github.rest.issues.addLabels = async () => { calls.mutations++; };
      const core = createMockCore();
      const context = {
        repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
        payload: { pull_request: { number: 97 } },
      };
      try {
        await extractPhaseInfo.revalidateMergedPrIssueIdentity({
          github, context, core, expectedIssueNumber: testCase.mismatch ? '999' : '321',
          sleep: async ms => { waits.push(ms); clock += ms; },
          now: () => clock,
          random: () => 0.5,
        });
        if (core.failures.length === 0) {
          await extractPhaseInfo.reconcileMergedPr({
            github, context, core,
            pr: { ...pr, body: '', labels: [{ name: 'speckit:phase-2' }, { name: 'speckit:level-feature' }] },
          });
        }
      } catch (error) {
        caught = error;
      }
      const finalError = testCase.errors[waits.length];
      const fallback = boundary === 'comments' && testCase.terminal
        && (finalError.status ?? finalError.response?.status) !== 503;
      const terminal = testCase.terminal && !fallback;
      assertEqual(`${desc}: attempts`, terminal ? waits.length + 1 : testCase.errors.length + (fallback ? 0 : 1),
        calls[boundary]);
      assertEqual(`${desc}: does not repeat other reads`, boundary === 'comments' ? 1 : 0,
        calls[boundary === 'comments' ? 'pulls' : 'comments']);
      assertEqual(`${desc}: bounded deterministic waits`, testCase.waits, waits);
      assertTruthy(`${desc}: surfaces original provider failure`,
        terminal ? caught === testCase.errors[waits.length] : caught === undefined);
      assertEqual(`${desc}: identity comparison preserved`, testCase.mismatch ? 1 : 0, core.failures.length);
      assertEqual(`${desc}: non-503 comment fallback preserved`, fallback ? 1 : 0, core.warnings.length);
      assertEqual(`${desc}: progression mutations exactly once or skipped`,
        terminal || testCase.mismatch ? 0 : 1, calls.mutations);
    }
  }
  {
    const originalTimeout = global.setTimeout;
    const originalNow = Date.now;
    const originalRandom = Math.random;
    const waits = [];
    const calls = { pulls: 0, comments: 0 };
    let clock = Date.parse('2026-01-01T00:00:00Z');
    const core = createMockCore();
    const github = createMockGithub([], {});
    github.rest.pulls.get = async () => {
      calls.pulls++;
      if (calls.pulls === 1) throw Object.assign(new Error('unavailable'), { status: 503 });
      if (calls.pulls === 2) throw httpError(503, { 'x-ratelimit-reset': '1767225603' });
      return { data: {
        body: identityMarker, head: { ref: 'speckit/321/phase-2-clarify' },
        user: { login: 'copilot-swe-agent[bot]' },
      } };
    };
    const commentError = httpError(503, { 'retry-after': '28' });
    github.paginate = async () => { calls.comments++; throw commentError; };
    let caught;
    try {
      global.setTimeout = (callback, ms) => { waits.push(ms); clock += ms; callback(); };
      Date.now = () => clock;
      Math.random = () => 0;
      await extractPhaseInfo.revalidateMergedPrIssueIdentity({
        github, core, expectedIssueNumber: '321',
        context: {
          repo: { owner: 'swai-factory', repo: 'agentic-devtools' },
          payload: { pull_request: { number: 97 } },
        },
      });
    } catch (error) {
      caught = error;
    } finally {
      global.setTimeout = originalTimeout;
      Date.now = originalNow;
      Math.random = originalRandom;
    }
    assertEqual('default timer and clock honor backoff and reset without real sleeping', [1000, 2000], waits);
    assertEqual('wait cap is shared across both identity reads', { pulls: 3, comments: 1 }, calls);
    assertTruthy('shared wait cap surfaces the comment provider failure', caught === commentError);
    assertEqual('exhausted 503 does not use comment fallback', [], core.warnings);
  }
  const progressionWorkflow = fs.readFileSync(
    path.join(__dirname, '..', '..', '..', 'workflows', 'speckit-phase-progression.yml'), 'utf8');
  assertTruthy('label reconciliation remains gated on successful identity revalidation',
    /- name: Reconcile Required SpecKit Labels\s+if: [^\n]*steps\.revalidate-identity\.outcome == 'success'/.test(progressionWorkflow));
  console.log(`Results: ${PASS} passed, ${FAIL} failed`);
  if (FAIL > 0) {
    process.exit(1);
  }
})();
