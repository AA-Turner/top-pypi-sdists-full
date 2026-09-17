'use strict';

const MARKER_REGEX = /<!--\s*speckit:agent-assigned schema_version=1 engine=cloud-agent issue=(\d+) phase=([1-3]) hierarchy=(epic|feature|task) correlation_id=([0-9a-fA-F-]+)\s*-->/i;
const ISSUE_REFERENCE_REGEX = /(?:Relates to|Closes) #(\d+)/i;
const TRUSTED_NORMALIZER_LOGINS = new Set(['AMARSNIK_swica', 'github-actions[bot]']);
const NORMALIZER_SUCCESS_REGEX = /<!--\s*speckit:agent-pr-normalizer pr=(\d+) correlation_id=([0-9a-fA-F-]+)\s*-->/i;
const SUPPORTED_LEVELS = new Set(['epic', 'feature', 'task']);
const PHASE_LABEL_REGEX = /^speckit:phase-(\d+)$/;
const LEVEL_LABEL_REGEX = /^speckit:level-(epic|feature|task)$/;

function isTrustedNormalizerComment(comment) {
  return TRUSTED_NORMALIZER_LOGINS.has(comment.user?.login || '');
}

// Whether a PR carries either a syntactically valid `speckit:agent-assigned` marker or
// one of the SpecKit labels the normalizer itself would have applied on a prior run. A
// Copilot PR that merely quotes the marker prefix (for example, an audit PR documenting
// the marker format) fails this check and must be skipped without posting any comment,
// applying any label, or mutating the source issue — this is the security-critical guard
// that keeps normalization diagnostics from firing on unrelated Copilot PRs.
function isEligibleForNormalization(pr) {
  const body = pr.body || '';
  const labelNames = (pr.labels || []).map(label => label.name || '');
  const markerMatch = body.match(MARKER_REGEX);
  const hasSpecKitLabel = labelNames.includes('speckit:spec')
    || labelNames.some(name => PHASE_LABEL_REGEX.test(name))
    || labelNames.some(name => LEVEL_LABEL_REGEX.test(name));
  return Boolean(markerMatch) || hasSpecKitLabel;
}

async function run({ github, context, core, pr }) {
  const owner = context.repo.owner;
  const repo = context.repo.repo;
  const body = pr.body || '';
  const existingLabelNames = (pr.labels || []).map(label => label.name || '');
  const phaseLabels = existingLabelNames.filter(name => PHASE_LABEL_REGEX.test(name));
  const levelLabels = existingLabelNames.filter(name => LEVEL_LABEL_REGEX.test(name));
  const markerMatch = body.match(MARKER_REGEX);
  const issueReferenceMatch = body.match(ISSUE_REFERENCE_REGEX);
  const existingPhase = phaseLabels.map(name => name.match(PHASE_LABEL_REGEX))[0];
  const existingLevel = levelLabels.map(name => name.match(LEVEL_LABEL_REGEX))[0];

  if (!isEligibleForNormalization(pr)) {
    core.info(
      `PR #${pr.number} has no valid speckit:agent-assigned marker and no SpecKit labels; `
      + 'skipping normalization without diagnostics.',
    );
    return;
  }

  const issueNumber = markerMatch
    ? Number(markerMatch[1])
    : (issueReferenceMatch ? Number(issueReferenceMatch[1]) : 0);
  const phase = markerMatch ? Number(markerMatch[2]) : Number(existingPhase?.[1] || 0);
  const level = (markerMatch?.[3] || existingLevel?.[1] || '').toLowerCase();
  const correlationId = markerMatch?.[4] || 'none';
  const gateFailed = /gate_status\s*:\s*failed\b/i.test(body)
    || existingLabelNames.includes('speckit:gate-failed');
  const failureMarker = `<!-- speckit:agent-pr-normalizer-failure pr=${pr.number} -->`;
  const statusMarker = `<!-- speckit:agent-pr-normalizer pr=${pr.number} correlation_id=${correlationId} -->`;

  const comments = await github.paginate(github.rest.issues.listComments, {
    owner, repo, issue_number: pr.number, per_page: 100,
  });
  const hasComment = marker => comments.some(comment => (comment.body || '').includes(marker));
  if (!markerMatch && comments.some(comment => {
    const match = (comment.body || '').match(NORMALIZER_SUCCESS_REGEX);
    return match
      && Number(match[1]) === pr.number
      && isTrustedNormalizerComment(comment);
  })) {
    core.warning(
      `PR #${pr.number} has prior UUID-correlated normalization but no current assignment marker; `
      + 'skipping legacy normalization.',
    );
    return;
  }

  const removeIssueTracking = async (number, resolvedPhase) => {
    if (!number) return;
    const labels = resolvedPhase
      ? [`speckit:agent-assigned-phase-${resolvedPhase}`, 'speckit:processing']
      : ['speckit:processing'];
    for (const name of labels) {
      try {
        await github.rest.issues.removeLabel({
          owner, repo, issue_number: number, name,
        });
      } catch (error) {
        if (error.status !== 404) {
          core.warning(`Could not remove ${name} from issue #${number}: ${error.message}`);
        }
      }
    }
  };

  const postDiagnostic = async (message, sourceIssueNumber = 0, resolvedPhase = 0) => {
    await github.rest.issues.addLabels({
      owner, repo, issue_number: pr.number, labels: ['speckit:failed'],
    });
    if (!hasComment(failureMarker)) {
      await github.rest.issues.createComment({
        owner, repo, issue_number: pr.number,
        body: `${failureMarker}\n\n## ⚠️ SpecKit Copilot PR normalization failed\n\n${message}`,
      });
    }
    if (sourceIssueNumber) {
      await removeIssueTracking(sourceIssueNumber, resolvedPhase);
      try {
        await github.rest.issues.addLabels({
          owner, repo, issue_number: sourceIssueNumber, labels: ['speckit:failed'],
        });
      } catch (error) {
        core.warning(`Could not mark source issue #${sourceIssueNumber} as failed: ${error.message}`);
      }
      try {
        const sourceComments = await github.paginate(github.rest.issues.listComments, {
          owner, repo, issue_number: sourceIssueNumber, per_page: 100,
        });
        if (!sourceComments.some(comment => (comment.body || '').includes(failureMarker))) {
          await github.rest.issues.createComment({
            owner, repo, issue_number: sourceIssueNumber,
            body: `${failureMarker}\n\n## ⚠️ SpecKit Copilot PR normalization failed\n\n${message}`,
          });
        }
      } catch (error) {
        core.warning(`Could not post diagnostic on source issue #${sourceIssueNumber}: ${error.message}`);
      }
    }
  };

  if (new Set(phaseLabels.map(name => name.match(PHASE_LABEL_REGEX)[1])).size > 1
      || new Set(levelLabels.map(name => name.match(LEVEL_LABEL_REGEX)[1])).size > 1) {
    await postDiagnostic(
      'The PR has conflicting SpecKit phase or level labels; exactly one distinct phase and level is required.',
      issueNumber,
      phase,
    );
    return;
  }

  if (!issueNumber || phase < 1 || phase > 3 || !SUPPORTED_LEVELS.has(level)) {
    await postDiagnostic(
      'The PR must contain a valid `speckit:agent-assigned` marker or `Relates to #N`/`Closes #N` reference together with phase 1-3 and valid level metadata.',
      issueNumber,
      phase,
    );
    return;
  }
  if (markerMatch && issueReferenceMatch && Number(issueReferenceMatch[1]) !== issueNumber) {
    await postDiagnostic(
      `The marker references issue #${issueNumber}, but the PR body references issue #${issueReferenceMatch[1]}.`,
      issueNumber,
      phase,
    );
    return;
  }

  if (markerMatch) {
    let authoritativeMarker = null;
    try {
      const sourceComments = await github.paginate(github.rest.issues.listComments, {
        owner, repo, issue_number: issueNumber, per_page: 100,
      });
      authoritativeMarker = sourceComments
        .filter(isTrustedNormalizerComment)
        .map(comment => ({
          comment,
          match: (comment.body || '').match(MARKER_REGEX),
        }))
        .filter(entry => entry.match
          && Number(entry.match[1]) === issueNumber
          && Number(entry.match[2]) === phase)
        .sort((a, b) => new Date(b.comment.created_at) - new Date(a.comment.created_at))
        .at(0);
    } catch (error) {
      await postDiagnostic(`Could not validate the source issue marker: ${error.message}`, issueNumber, phase);
      return;
    }
    if (!authoritativeMarker || authoritativeMarker.match[0] !== markerMatch[0]) {
      await postDiagnostic(
        `No trusted source issue comment matched correlation ID \`${correlationId}\` for issue #${issueNumber}, phase ${phase}.`,
      );
      return;
    }
  }

  const requiredLabels = [`speckit:phase-${phase}`, `speckit:level-${level}`, 'speckit:spec'];
  if (gateFailed) requiredLabels.push('speckit:gate-failed');
  await github.rest.issues.addLabels({
    owner, repo, issue_number: pr.number, labels: requiredLabels,
  });
  await removeIssueTracking(issueNumber, phase);
  for (const number of [pr.number, issueNumber]) {
    try {
      await github.rest.issues.removeLabel({
        owner, repo, issue_number: number, name: 'speckit:failed',
      });
    } catch (error) {
      if (error.status !== 404) {
        core.warning(`Could not clear speckit:failed from #${number}: ${error.message}`);
      }
    }
  }

  if (!hasComment(statusMarker)) {
    await github.rest.issues.createComment({
      owner, repo, issue_number: pr.number,
      body: [
        statusMarker,
        '',
        '✅ **SpecKit Copilot PR normalized**',
        '',
        `- Issue: #${issueNumber}`,
        `- Phase: ${phase}`,
        `- Level: ${level}`,
        `- Correlation ID: \`${correlationId}\``,
        `- Gate status: ${gateFailed ? 'failed' : 'passed or not declared'}`,
      ].join('\n'),
    });
  }
  core.info(`Normalized PR #${pr.number} for issue #${issueNumber}, phase ${phase}, level ${level}`);
}

module.exports = {
  run,
  isEligibleForNormalization,
  MARKER_REGEX,
};
