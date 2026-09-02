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
    'returns null when non-speckit branch has no Relates-to reference',
    null,
    extractPhaseInfo.extractIssueNumberFromPr({
      head: { ref: 'copilot/fix-no-relates' },
      body: cloudMarker,
    })
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
    const core = createMockCore();
    const marker = '<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent issue=889 phase=2 hierarchy=feature correlation_id=11111111-1111-4111-8111-bbbbbbbbbbbb -->';
    await extractPhaseInfo.run({
      github: createMockGithub([], {}, [
        {
          author_association: 'MEMBER',
          body: marker.replace('bbbbbbbbbbbb', 'cccccccccccc'),
          created_at: '2026-01-01T00:00:00Z',
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

  console.log('');
  console.log(`Results: ${PASS} passed, ${FAIL} failed`);
  if (FAIL > 0) {
    process.exit(1);
  }
})();
