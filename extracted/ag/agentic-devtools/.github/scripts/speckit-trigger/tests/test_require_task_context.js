'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { requireTaskContext } = require('../require-task-context');

async function run(env, removeError) {
  const calls = [];
  const github = { rest: { issues: {
    createComment: async args => calls.push(['comment', args]),
    addLabels: async args => calls.push(['labels', args]),
    removeLabel: async args => { if (removeError) throw removeError; calls.push(['remove', args]); },
  } } };
  const core = {
    setOutput: (...args) => calls.push(['output', ...args]),
    setFailed: message => calls.push(['failed', message]),
    warning: message => calls.push(['warning', message]),
  };
  await requireTaskContext({ github, context: { repo: { owner: 'o', repo: 'r' } }, core,
    env: { ISSUE_NUMBER: '42', ...env } });
  return calls;
}

test('task context requires contained regular parent spec and plan files, including symlink escapes', async () => {
  const root = fs.mkdtempSync(path.join(process.cwd(), '.context-test-'));
  const workspace = path.join(root, 'workspace');
  const parent = path.join(workspace, 'specs', '10-parent');
  fs.mkdirSync(parent, { recursive: true });
  const env = { GITHUB_WORKSPACE: workspace, SPEC_CONTEXT: 'specs/10-parent/spec.md' };
  try {
    fs.writeFileSync(path.join(parent, 'spec.md'), 'spec');
    assert.ok((await run(env)).some(([type]) => type === 'failed'));
    fs.writeFileSync(path.join(parent, 'plan.md'), 'plan');
    assert.deepEqual(await run(env), []);
    for (const value of ['', '../outside/spec.md', 'specs//spec.md', 'specs/./spec.md', 'specs/../spec.md', 'specs/missing/spec.md', 'specs/10-parent/plan.md']) {
      assert.ok((await run({ ...env, SPEC_CONTEXT: value })).some(([type]) => type === 'failed'));
    }
    const outside = path.join(root, 'outside');
    fs.mkdirSync(outside);
    fs.writeFileSync(path.join(outside, 'spec.md'), 'spec');
    fs.writeFileSync(path.join(outside, 'plan.md'), 'plan');
    fs.symlinkSync(outside, path.join(workspace, 'specs', 'escape'), 'junction');
    assert.ok((await run({ ...env, SPEC_CONTEXT: 'specs/escape/spec.md' })).some(([type]) => type === 'failed'));
    fs.rmSync(path.join(workspace, 'specs', 'escape'));
    fs.rmSync(path.join(parent, 'plan.md'));
    fs.symlinkSync(path.join(outside, 'plan.md'), path.join(parent, 'plan.md'));
    assert.ok((await run(env)).some(([type]) => type === 'failed'));
    fs.rmSync(path.join(parent, 'plan.md'));
    fs.writeFileSync(path.join(parent, 'plan.md'), 'plan');
    fs.rmSync(path.join(workspace, 'specs'), { recursive: true });
    fs.symlinkSync(outside, path.join(workspace, 'specs'), 'junction');
    assert.ok((await run({ ...env, SPEC_CONTEXT: 'specs/spec.md' })).some(([type]) => type === 'failed'));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('blocked resolution stops without conflicting mutations', async () => {
  const calls = await run({ HIERARCHY_LEVEL: 'blocked' });
  assert.deepEqual(calls.map(([type]) => type), ['output', 'failed']);
});

test('failed gate posts actionable comment and clears processing; respects comment setting', async () => {
  const calls = await run({});
  assert.deepEqual(calls.map(([type]) => type), ['comment', 'labels', 'remove', 'output', 'failed']);
  assert.match(calls[0][1].body, /spec\.md/);
  assert.match(calls[0][1].body, /plan\.md/);
  assert.ok(!(await run({ SPECKIT_COMMENT_ON_ISSUE: 'false' })).some(([type]) => type === 'comment'));
  assert.ok(!(await run({}, { status: 404 })).some(([type]) => type === 'warning'));
  assert.ok((await run({}, { status: 500, message: 'error' })).some(([type]) => type === 'warning'));
});
