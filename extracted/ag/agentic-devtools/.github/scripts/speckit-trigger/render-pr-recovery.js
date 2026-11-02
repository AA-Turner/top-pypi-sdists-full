'use strict';

function buildPrRecoveryComment(env) {
  const repo = env.GITHUB_REPOSITORY || '';
  const phase = Number(env.NEXT_PHASE);
  const phaseName = env.NEXT_PHASE_NAME || 'unknown';
  const hierarchyLevel = env.HIERARCHY_LEVEL || 'unknown';
  const prNumber = env.CREATED_PR_NUMBER || '';
  const prUrl = env.CREATED_PR_URL || '';
  const runId = env.GITHUB_RUN_ID || '';
  if (!/^[\w.-]+\/[\w.-]+$/.test(repo) ||
      ![1, 2, 3].includes(phase) ||
      !/^[1-9]\d*$/.test(runId) ||
      (prNumber && !/^[1-9]\d*$/.test(prNumber)) ||
      (!prNumber && !prUrl)) {
    throw new Error('Valid repository, phase (1-3), run ID, and created PR identity are required.');
  }

  const requiredLabels = [`speckit:phase-${phase}`];
  if (['epic', 'feature', 'task'].includes(hierarchyLevel)) {
    requiredLabels.push(`speckit:level-${hierarchyLevel}`);
  }
  const labelCommand = prNumber
    ? [
        `gh api --method POST "repos/${repo}/issues/${prNumber}/labels" \\`,
        requiredLabels.map(label => `  --raw-field "labels[]=${label}"`).join(' \\\n'),
      ].join('\n')
    : 'Use the PR URL to determine its number, then apply the required labels with the REST labels API.';
  const postMergeRecovery = phase < 3
    ? `If the PR was already merged, manually dispatch Phase ${phase + 1} from the SpecKit Phase Progression workflow.`
    : 'If the PR was already merged, follow the workflow logs to recover the post-Phase-3 action; Phase 4 is not a valid dispatch phase.';
  const labelSetupFailed = env.LABEL_SETUP_STATUS === 'failed';
  const runUrl = `https://github.com/${repo}/actions/runs/${runId}`;

  return [
    labelSetupFailed
      ? `## SpecKit: Phase ${phase} (${phaseName}) PR Created, Routing Labels Failed`
      : `## SpecKit: Phase ${phase} (${phaseName}) PR Created, Workflow Incomplete`,
    '',
    `The PR${prNumber ? ` #${prNumber}` : ''}${prUrl ? ` (${prUrl})` : ''} already exists, but the workflow did not complete successfully.`,
    labelSetupFailed
      ? `Do not merge until these required routing labels are present: ${requiredLabels.map(label => `\`${label}\``).join(', ')}.`
      : 'Check the workflow logs before merging; the PR workflow did not reach a verified completion state.',
    '',
    '### Recovery',
    '',
    '1. Use the workflow logs to create any missing required labels.',
    '2. Apply the required labels with the REST API:',
    '',
    '```bash',
    labelCommand,
    '```',
    '',
    `3. Verify all labels with \`gh api --paginate --jq '.[].name' "repos/${repo}/issues/${prNumber || '<PR_NUMBER>'}/labels"\`.`,
    '4. Inspect the CRITICAL and artifact gate results and complete any skipped artifact repair before marking the PR ready or merging. Label recovery alone does not satisfy the artifact gates.',
    env.ARTIFACT_GATE_RESULT === 'fail'
      ? 'The artifact gate reported violations. The automatic repair-request step may have been skipped after PR setup failed; confirm the repair request was posted and the violations are fixed.'
      : 'Confirm that required artifact verification completed successfully; recover any failed or skipped gate before proceeding.',
    postMergeRecovery,
    '',
    `**Workflow Run**: [View logs](${runUrl})`,
    '',
    '---',
    `_This comment was posted by the [SpecKit GitHub Action](${runUrl})._`,
  ].join('\n');
}

module.exports = { buildPrRecoveryComment };

if (require.main === module) {
  try {
    process.stdout.write(buildPrRecoveryComment(process.env) + '\n');
  } catch (error) {
    console.error(`Could not render SpecKit PR recovery: ${error.message}`);
    process.exitCode = 1;
  }
}
