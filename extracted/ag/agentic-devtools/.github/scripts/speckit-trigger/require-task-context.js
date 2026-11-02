'use strict';
const fs = require('fs');
const path = require('path');

function validTaskContext(workspace, specContext) {
  if (!workspace || !specContext.startsWith('specs/') || !specContext.endsWith('/spec.md') ||
      specContext.split('/').some(part => part === '' || part === '.' || part === '..')) return false;
  try {
    const repo = fs.realpathSync(workspace);
    const specs = fs.realpathSync(path.join(repo, 'specs'));
    if (!specs.startsWith(repo + path.sep)) return false;
    const spec = path.resolve(repo, specContext);
    const plan = path.join(path.dirname(spec), 'plan.md');
    return [spec, plan].every(file =>
      fs.realpathSync(file).startsWith(specs + path.sep) && fs.lstatSync(file).isFile());
  } catch {
    return false;
  }
}

async function requireTaskContext({ github, context, core, env = process.env }) {
  const issueNumber = Number(env.ISSUE_NUMBER);
  if (env.HIERARCHY_LEVEL === 'blocked') {
    core.setOutput('handled', 'true');
    core.setFailed(`Task-level issue #${issueNumber} is blocked pending its parent spec; resolver already notified.`);
    return;
  }
  if (validTaskContext(env.GITHUB_WORKSPACE, env.SPEC_CONTEXT || '')) return;
  const target = { owner: context.repo.owner, repo: context.repo.repo, issue_number: issueNumber };
  if (env.SPECKIT_COMMENT_ON_ISSUE !== 'false') {
    await github.rest.issues.createComment({ ...target,
      body: `❌ SpecKit: task-level issue #${issueNumber} has no usable parent planning context\n\nAdd a same-repository parent with merged, regular, non-symlinked \`spec.md\` and \`plan.md\` files inside \`specs/\` on \`main\`, or change the issue type to Feature and re-trigger. Symlink escapes are not permitted.`,
    });
  }
  await github.rest.issues.addLabels({ ...target, labels: ['speckit:failed'] });
  try {
    await github.rest.issues.removeLabel({ ...target, name: 'speckit:processing' });
  } catch (error) {
    if (error.status !== 404) core.warning(`Could not remove speckit:processing: ${error.message}`);
  }
  core.setOutput('handled', 'true');
  core.setFailed(`Task-level issue #${issueNumber} has no valid parent planning context (requires regular, non-symlinked spec.md and plan.md files)`);
}

module.exports = { validTaskContext, requireTaskContext };
