'use strict';

const fs = require('fs');
const path = require('path');

const SUPPORTED_LEVELS = new Set(['epic', 'feature', 'task']);
const HIERARCHY_LEVEL_PATTERN = /^level:[ \t]*(?:"([^"]*)"|'([^']*)'|([^#\n]*?))(?:[ \t]+#.*)?[ \t]*$/;
const CLOUD_MARKER_PATTERN = /<!--\s*speckit:agent-assigned schema_version=1 engine=cloud-agent issue=(\d+) phase=(\d+) hierarchy=([^\s]+) correlation_id=([0-9a-fA-F-]+)\s*-->/;
const TRUSTED_MARKER_ASSOCIATIONS = new Set(['OWNER', 'MEMBER', 'COLLABORATOR']);
function expectedCloudBaseRef(issueNumber, phase, hierarchyLevel) {
  if (phase === 2) {
    return `speckit/${issueNumber}/phase-1-specify`;
  }
  if (phase === 3 && hierarchyLevel !== 'task') {
    return `speckit/${issueNumber}/phase-2-clarify`;
  }
  return 'main';
}

function analyzeChangedFiles(changedFiles, labeledLevel, core) {
  const activeFiles = changedFiles.filter(file => file.status !== 'removed');
  const candidateSpecDirs = new Set(
    activeFiles
      .map(file => {
        const generatedMatch = file.filename.match(/^(.*)\/generated\/[^/]+$/);
        if (generatedMatch) {
          return generatedMatch[1];
        }
        if (/(?:^|\/)(?:spec|plan|tasks|research)\.md$/.test(file.filename) || file.filename.endsWith('/hierarchy.yml')) {
          return file.filename.replace(/\/[^/]+$/, '');
        }
        return null;
      })
      .filter(Boolean)
  );

  const candidates = Array.from(candidateSpecDirs).sort((a, b) => a.localeCompare(b));
  if (candidates.length > 1) {
    core?.warning(`Multiple changed spec directories found; hierarchy is unknown: ${candidates.join(', ')}`);
    return { ambiguous: true, fallbackLevel: 'unknown', specDir: '' };
  }
  const specDir = candidates[0] || '';
  const fallbackLevel = labeledLevel || 'unknown';

  return { ambiguous: false, fallbackLevel, specDir };
}

function parseHierarchyLevel(hierarchyContent, fallbackLevel, returnMetadata = false) {
  let rawLevel = null;
  let declarationCount = 0;
  let parsedDeclarationCount = 0;
  for (const line of hierarchyContent.split(/\r?\n/)) {
    if (/^level:/.test(line)) {
      declarationCount++;
    }
    const hierarchyMatch = line.match(HIERARCHY_LEVEL_PATTERN);
    if (!hierarchyMatch) {
      continue;
    }
    parsedDeclarationCount++;
    if (rawLevel !== null) {
      return returnMetadata ? { level: fallbackLevel, valid: false } : fallbackLevel;
    }
    rawLevel = hierarchyMatch.slice(1).find(group => group !== undefined).trim().toLowerCase();
  }
  const valid = declarationCount === 1 && parsedDeclarationCount === 1 && SUPPORTED_LEVELS.has(rawLevel);
  const level = valid ? rawLevel : fallbackLevel;
  return returnMetadata ? { level, valid } : level;
}

function resolveValidatedHierarchyLevel({
  canonicalLevel,
  fallbackLevel = '',
  authoritativeLevel = '',
  authoritativeReadSucceeded = true,
}) {
  if (authoritativeLevel === 'epic') {
    return 'epic';
  }
  if (!authoritativeReadSucceeded) {
    return 'unknown';
  }
  if (
    SUPPORTED_LEVELS.has(canonicalLevel)
    && SUPPORTED_LEVELS.has(authoritativeLevel)
    && canonicalLevel !== authoritativeLevel
  ) {
    return 'unknown';
  }
  if (SUPPORTED_LEVELS.has(canonicalLevel)) {
    return canonicalLevel;
  }
  if (SUPPORTED_LEVELS.has(authoritativeLevel)) {
    return authoritativeLevel;
  }
  return SUPPORTED_LEVELS.has(fallbackLevel) ? fallbackLevel : 'unknown';
}

async function getAuthoritativeIssueLevel(github, context, issueNumber) {
  if (!issueNumber || !github.rest.issues?.get) {
    return { level: '', succeeded: false };
  }
  try {
    const { data: issue } = await github.rest.issues.get({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: issueNumber,
    });
    const values = [
      ...(Array.isArray(issue.labels) ? issue.labels.map(label => label?.name) : []),
      issue.type?.name,
    ].filter(value => typeof value === 'string').map(value => value.trim().toLowerCase());
    if (values.includes('epic')) {
      return { level: 'epic', succeeded: true };
    }
    const nonEpicLevels = ['task', 'feature'].filter(l => values.includes(l));
    if (nonEpicLevels.length > 1) {
      return { level: '', succeeded: false };
    }
    if (nonEpicLevels.includes('task')) {
      return { level: 'task', succeeded: true };
    }
    if (nonEpicLevels.includes('feature')) {
      return { level: 'feature', succeeded: true };
    }
    return { level: '', succeeded: true };
  } catch (error) {
    return { level: '', succeeded: false };
  }
}

function hasTerminalArtifactSet(level, hasPlanArtifact, hasTasksArtifact, hasAnalysisReport) {
  if (level === 'feature') {
    return hasPlanArtifact && hasTasksArtifact && hasAnalysisReport;
  }
  if (level === 'epic') {
    return hasPlanArtifact && hasAnalysisReport;
  }
  if (level === 'task') {
    return hasTasksArtifact;
  }
  return false;
}

async function listDirectoryEntriesAtMerge(github, context, mergeCommitSha, contentPath) {
  try {
    const response = await github.rest.repos.getContent({
      owner: context.repo.owner,
      repo: context.repo.repo,
      path: contentPath,
      ref: mergeCommitSha,
    });
    return Array.isArray(response.data) ? response.data : [response.data];
  } catch (error) {
    if (error.status === 404) {
      return [];
    }
    throw error;
  }
}

async function loadMergedSpecState(
  github,
  context,
  mergeCommitSha,
  specDir,
  fallbackLevel,
  authoritativeLevel = '',
  ambiguous = false,
  authoritativeReadSucceeded = true,
) {
  const specEntries = specDir
    ? await listDirectoryEntriesAtMerge(github, context, mergeCommitSha, specDir)
    : [];
  const hierarchyEntries = specDir
    ? await listDirectoryEntriesAtMerge(github, context, mergeCommitSha, `${specDir}/hierarchy.yml`)
    : [];
  const generatedEntries = specEntries.some(entry => entry.type === 'dir' && entry.name === 'generated')
    ? await listDirectoryEntriesAtMerge(github, context, mergeCommitSha, `${specDir}/generated`)
    : [];
  const hasHierarchyEntry = hierarchyEntries.length > 0;
  const hierarchyContent = typeof hierarchyEntries[0]?.content === 'string'
    ? Buffer.from(hierarchyEntries[0].content, 'base64').toString('utf8')
    : '';
  const parsedHierarchy = hasHierarchyEntry
    ? parseHierarchyLevel(hierarchyContent, 'unknown', true)
    : { level: 'unknown', valid: false };
  const parsedLevel = parsedHierarchy.level;
  const level = resolveValidatedHierarchyLevel({
    authoritativeLevel:
      authoritativeLevel === 'epic' || (!ambiguous && (!hasHierarchyEntry || parsedHierarchy.valid))
        ? authoritativeLevel
        : '',
    authoritativeReadSucceeded,
    canonicalLevel: parsedLevel,
    fallbackLevel: !hasHierarchyEntry && !ambiguous ? fallbackLevel : '',
  });
  const hasAnalysisReport = specEntries.some(entry => entry.type === 'file' && entry.name === 'analysis-report.md')
    || generatedEntries.some(entry => entry.type === 'file' && entry.name === 'analysis-report.md');
  const hasTasksArtifact = specEntries.some(entry => entry.type === 'file' && entry.name === 'tasks.md');
  const hasPlanArtifact = specEntries.some(entry => entry.type === 'file' && entry.name === 'plan.md');

  return {
    hasAnalysisReport,
    hasPlanArtifact,
    hasTasksArtifact,
    hasTerminalArtifact: hasTerminalArtifactSet(level, hasPlanArtifact, hasTasksArtifact, hasAnalysisReport),
    level,
    specDir,
  };
}

function findFirstLabelMatch(labels, pattern) {
  for (const label of labels) {
    const match = label.match(pattern);
    if (match) {
      return match;
    }
  }
  return null;
}

function extractIssueNumberFromPr(pr) {
  const headRef = pr.head.ref || '';
  const branchMatch = headRef.match(/^speckit\/(\d+)\//);
  if (branchMatch) {
    return parseInt(branchMatch[1], 10);
  }
  const body = pr.body || '';
  const issueMatch = body.match(/Relates to #(\d+)/);
  return issueMatch ? parseInt(issueMatch[1], 10) : null;
}

async function loadTrustedIssueMarkers(github, context, issueNumber) {
  const comments = await github.paginate(github.rest.issues.listComments, {
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: issueNumber,
    per_page: 100,
  });
  return comments
    .map(comment => ({ comment, match: (comment.body || '').match(CLOUD_MARKER_PATTERN) }))
    .filter(entry => {
      if (!entry.match) return false;
      return TRUSTED_MARKER_ASSOCIATIONS.has(entry.comment?.author_association || '');
    })
    .sort((a, b) => new Date(b.comment.created_at) - new Date(a.comment.created_at));
}

function collectSpecDirectoriesForIssue(specsRoot, issueNumberText) {
  if (!fs.existsSync(specsRoot)) {
    return [];
  }

  const matches = [];
  const stack = [specsRoot];
  while (stack.length > 0) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) {
        continue;
      }
      const fullPath = path.join(current, entry.name);
      if (entry.name.startsWith(`${issueNumberText}-`) || entry.name === issueNumberText) {
        matches.push(fullPath);
        continue;
      }
      stack.push(fullPath);
    }
  }

  return matches.sort((a, b) => a.localeCompare(b));
}

function resolveHierarchyLevelFromWorkspace(issueNumber, workspacePath, core, returnMetadata = false) {
  const specsRoot = path.join(workspacePath, 'specs');
  const issueNumberText = String(issueNumber || '').trim();
  if (!issueNumberText) {
    return returnMetadata ? { ambiguous: false, level: '', metadataValid: true } : '';
  }

  const matches = collectSpecDirectoriesForIssue(specsRoot, issueNumberText);
  if (matches.length > 1) {
    core.warning(
      `Multiple spec directories found for issue #${issueNumberText}; hierarchy is unknown: ` +
      matches.map(match => path.relative(workspacePath, match)).join(', ')
    );
    return returnMetadata ? { ambiguous: true, level: '', metadataValid: true } : '';
  }

  const specDir = matches[0];
  if (!specDir) {
    return returnMetadata ? { ambiguous: false, level: '', metadataValid: true } : '';
  }

  const hierarchyPath = path.join(specDir, 'hierarchy.yml');
  if (!fs.existsSync(hierarchyPath)) {
    return returnMetadata ? { ambiguous: false, level: '', metadataValid: true } : '';
  }

  let hierarchyContent;
  try {
    hierarchyContent = fs.readFileSync(hierarchyPath, 'utf8');
  } catch (readError) {
    core.warning(`Failed to read hierarchy metadata at ${hierarchyPath}: ${readError.message}`);
    return returnMetadata ? { ambiguous: false, level: 'unknown', metadataValid: false } : 'unknown';
  }
  const parsedHierarchy = parseHierarchyLevel(hierarchyContent, '', true);
  return returnMetadata
    ? { ambiguous: false, level: parsedHierarchy.level, metadataValid: parsedHierarchy.valid }
    : parsedHierarchy.level;
}

async function run({ github, context, core, workflowDispatchPhase, workflowDispatchIssueNumber }) {
  if (context.eventName === 'workflow_dispatch') {
    const nextPhase = parseInt(workflowDispatchPhase, 10);
    const issueNumber = parseInt(workflowDispatchIssueNumber, 10);
    const completedPhase = nextPhase - 1;
    const phaseNames = { 1: 'specify', 2: 'clarify', 3: 'plan', 4: 'complete' };
    const nextPhaseName = phaseNames[nextPhase] || 'unknown';
    const workspacePath = process.env.GITHUB_WORKSPACE || process.cwd();
    const workspaceResult = resolveHierarchyLevelFromWorkspace(issueNumber, workspacePath, core, true);
    const {
      level: authoritativeLevel,
      succeeded: authoritativeReadSucceeded,
    } = await getAuthoritativeIssueLevel(github, context, issueNumber);
    const resolvedHierarchyLevel = resolveValidatedHierarchyLevel({
      authoritativeLevel:
        authoritativeLevel === 'epic' ||
        (workspaceResult.metadataValid && !workspaceResult.ambiguous)
          ? authoritativeLevel
          : '',
      authoritativeReadSucceeded,
      canonicalLevel: workspaceResult.metadataValid ? workspaceResult.level : '',
      fallbackLevel: '',
    });

    core.setOutput('completed_phase', completedPhase.toString());
    core.setOutput('next_phase', nextPhase.toString());
    core.setOutput('next_phase_name', nextPhaseName);
    core.setOutput('issue_number', issueNumber.toString());
    core.setOutput('merged_pr_url', '');
    core.setOutput('terminal_hierarchy_level', resolvedHierarchyLevel);
    core.info(`[workflow_dispatch] Next Phase: ${nextPhase} (${nextPhaseName}), Issue: ${issueNumber}`);
    return;
  }

  const pr = context.payload.pull_request;
  const labels = pr.labels.map(label => label.name);
  const cloudMarkerMatch = (pr.body || '').match(CLOUD_MARKER_PATTERN);
  let trustedCloudMarker = null;
  if (cloudMarkerMatch && pr.user?.login === 'copilot-swe-agent[bot]') {
    const markerIssue = parseInt(cloudMarkerMatch[1], 10);
    const markerPhase = parseInt(cloudMarkerMatch[2], 10);
    const markerHierarchy = String(cloudMarkerMatch[3] || '').toLowerCase();
    const expectedBase = expectedCloudBaseRef(markerIssue, markerPhase, markerHierarchy);
    if (pr.base?.ref !== expectedBase) {
      core.warning(
        `Cloud marker on PR #${pr.number} rejected: expected base '${expectedBase}', got '${pr.base?.ref || 'unknown'}'`
      );
    } else {
      try {
        const trustedMarkers = await loadTrustedIssueMarkers(github, context, markerIssue);
        const newestMarker = trustedMarkers.find(entry =>
          Number(entry.match[1]) === markerIssue &&
          Number(entry.match[2]) === markerPhase
        );
        if (newestMarker && newestMarker.match[0] === cloudMarkerMatch[0]) {
          trustedCloudMarker = {
            issueNumber: markerIssue,
            phase: markerPhase,
          };
        } else {
          core.warning(
            `Cloud marker on PR #${pr.number} rejected: no matching trusted issue marker found for issue #${markerIssue}, phase ${markerPhase}`
          );
        }
      } catch (error) {
        core.warning(`Could not validate trusted cloud marker for PR #${pr.number}: ${error.message || error}`);
      }
    }
  }
  const completedPhaseMatch = findFirstLabelMatch(labels, /^speckit:phase-(\d+)$/);
  let completedPhase = 0;
  if (completedPhaseMatch) {
    completedPhase = parseInt(completedPhaseMatch[1], 10);
  } else if (trustedCloudMarker) {
    completedPhase = trustedCloudMarker.phase;
    core.info(`No speckit:phase-N label found; using validated cloud-agent marker phase ${completedPhase}`);
  } else {
    core.setFailed('Could not extract phase number from PR labels or cloud-agent marker');
    return;
  }
  const nextPhase = completedPhase + 1;
  const hierarchyLabelMatches = labels
    .map(l => l.match(/^speckit:level-(epic|feature|task)$/))
    .filter(Boolean);
  const distinctHierarchyLevels = [...new Set(hierarchyLabelMatches.map(m => m[1]))];
  const labeledLevel = distinctHierarchyLevels.length === 1 ? distinctHierarchyLevels[0] : '';
  const issueNumberFromBranchOrBody = trustedCloudMarker ? trustedCloudMarker.issueNumber : extractIssueNumberFromPr(pr);
  const { level: authoritativeLevel, succeeded: authReadSucceeded } = await getAuthoritativeIssueLevel(
    github,
    context,
    issueNumberFromBranchOrBody,
  );

  const loadChangedFiles = async () => github.paginate(github.rest.pulls.listFiles, {
    owner: context.repo.owner,
    repo: context.repo.repo,
    pull_number: pr.number,
    per_page: 100,
  });

  let effectiveNextPhase;
  let terminalHierarchyLevel = 'unknown';
  if (completedPhase === 5) {
    const changedFiles = await loadChangedFiles();
    const { ambiguous, fallbackLevel, specDir } = analyzeChangedFiles(changedFiles, labeledLevel, core);
    terminalHierarchyLevel = (
      await loadMergedSpecState(
        github,
        context,
        pr.merge_commit_sha,
        specDir,
        authReadSucceeded ? fallbackLevel : '',
        authoritativeLevel,
        ambiguous,
        authReadSucceeded,
      )
    ).level;
    effectiveNextPhase = 4;
  } else if (completedPhase === 4) {
    // Legacy: old 5-phase pipeline's task-breakdown phase. Task-level issues ran only
    // phase 4 (tasks.md is their terminal artifact); feature/epic issues still need
    // plan+analyze. Load artifact state to distinguish the two cases.
    const changedFiles = await loadChangedFiles();
    const { ambiguous, fallbackLevel, specDir } = analyzeChangedFiles(changedFiles, labeledLevel, core);
    const { hasAnalysisReport, hasTasksArtifact, hasPlanArtifact, hasTerminalArtifact, level } =
      await loadMergedSpecState(
        github,
        context,
        pr.merge_commit_sha,
        specDir,
        authReadSucceeded ? fallbackLevel : '',
        authoritativeLevel,
        ambiguous,
        authReadSucceeded,
      );
    terminalHierarchyLevel = level;
    core.info(
      `Legacy phase-4 PR #${pr.number}: spec dir=${specDir || 'unknown'}, ` +
      `merged plan.md present=${hasPlanArtifact}, ` +
      `merged tasks.md present=${hasTasksArtifact}, ` +
      `merged analysis-report.md present=${hasAnalysisReport}, ` +
      `derived hierarchy=${terminalHierarchyLevel} — routing to ` +
      `${hasTerminalArtifact ? '4 (terminal)' : '3 (legacy recovery)'}`
    );
    effectiveNextPhase = hasTerminalArtifact ? 4 : 3;
  } else if (completedPhase === 3) {
    const changedFiles = await loadChangedFiles();
    const { ambiguous, fallbackLevel, specDir } = analyzeChangedFiles(changedFiles, labeledLevel, core);
    const { hasAnalysisReport, hasTasksArtifact, hasPlanArtifact, hasTerminalArtifact, level } =
      await loadMergedSpecState(
        github,
        context,
        pr.merge_commit_sha,
        specDir,
        authReadSucceeded ? fallbackLevel : '',
        authoritativeLevel,
        ambiguous,
        authReadSucceeded,
      );
    terminalHierarchyLevel = level;
    core.info(
      `Phase-3 PR #${pr.number}: spec dir=${specDir || 'unknown'}, ` +
      `merged plan.md present=${hasPlanArtifact}, ` +
      `merged tasks.md present=${hasTasksArtifact}, ` +
      `merged analysis-report.md present=${hasAnalysisReport}, ` +
      `derived hierarchy=${terminalHierarchyLevel} — routing to ` +
      `${hasTerminalArtifact ? '4 (terminal)' : '3 (legacy recovery)'}`
    );
    effectiveNextPhase = hasTerminalArtifact ? 4 : 3;
  } else {
    effectiveNextPhase = nextPhase;
    if (authoritativeLevel === 'epic') {
      terminalHierarchyLevel = 'epic';
    } else {
      const workspacePath = process.env.GITHUB_WORKSPACE || process.cwd();
      const workspaceResult = resolveHierarchyLevelFromWorkspace(
        issueNumberFromBranchOrBody,
        workspacePath,
        core,
        true,
      );
      const resolvedHierarchyLevel = resolveValidatedHierarchyLevel({
        authoritativeLevel:
          authoritativeLevel === 'epic' ||
          (workspaceResult.metadataValid && !workspaceResult.ambiguous)
            ? authoritativeLevel
            : '',
        authoritativeReadSucceeded: authReadSucceeded,
        canonicalLevel: workspaceResult.metadataValid ? workspaceResult.level : '',
        fallbackLevel:
          workspaceResult.metadataValid && authReadSucceeded && !workspaceResult.ambiguous
            ? labeledLevel
            : '',
      });
      if ((workspaceResult.level && !workspaceResult.ambiguous) || (authReadSucceeded && (authoritativeLevel || labeledLevel))) {
        terminalHierarchyLevel = resolvedHierarchyLevel;
      } else {
        const changedFiles = await loadChangedFiles();
        const { ambiguous, fallbackLevel, specDir } = analyzeChangedFiles(changedFiles, labeledLevel, core);
        terminalHierarchyLevel = (
          await loadMergedSpecState(
            github,
            context,
            pr.merge_commit_sha,
            specDir,
            authReadSucceeded ? fallbackLevel : '',
            authoritativeLevel,
            ambiguous,
            authReadSucceeded,
          )
        ).level;
      }
    }
  }

  const headRef = pr.head.ref || '';
  const speckitBranchPattern = /^speckit\/\d+\/phase-\d+-/;
  let issueNumber;
  if (!speckitBranchPattern.test(headRef)) {
    if (trustedCloudMarker) {
      issueNumber = trustedCloudMarker.issueNumber;
      core.info(`Using validated cloud-agent marker for issue #${issueNumber} from non-speckit head '${headRef}'`);
    } else {
      core.warning(
        `Branch '${headRef}' does not match expected speckit/<issue>/phase-<N>-* pattern. ` +
        'This PR may have been accidentally labeled. Skipping phase progression.'
      );
      core.setOutput('next_phase', '0');
      core.setOutput('issue_number', '0');
      core.setOutput('completed_phase', '0');
      core.setOutput('next_phase_name', '');
      core.setOutput('merged_pr_url', '');
      return;
    }
  }

  if (!issueNumber) {
    const branchMatch = headRef.match(/^speckit\/(\d+)\//);
    if (branchMatch) {
      issueNumber = parseInt(branchMatch[1], 10);
      core.info(`Extracted issue number from branch name: ${issueNumber}`);
    } else if (trustedCloudMarker) {
      issueNumber = trustedCloudMarker.issueNumber;
      core.info(`Extracted issue number from validated cloud-agent marker: ${issueNumber}`);
    } else {
      const body = pr.body || '';
      const issueMatch = body.match(/Relates to #(\d+)/);
      if (!issueMatch) {
        core.setFailed('Could not extract issue number from branch name or PR body');
        return;
      }
      issueNumber = parseInt(issueMatch[1], 10);
      core.info(`Extracted issue number from PR body: ${issueNumber}`);
    }
  }

  const phaseNames = { 1: 'specify', 2: 'clarify', 3: 'plan', 4: 'complete' };
  const nextPhaseName = phaseNames[effectiveNextPhase] || 'unknown';
  terminalHierarchyLevel = terminalHierarchyLevel || 'unknown';

  core.setOutput('completed_phase', completedPhase.toString());
  core.setOutput('next_phase', effectiveNextPhase.toString());
  core.setOutput('next_phase_name', nextPhaseName);
  core.setOutput('issue_number', issueNumber.toString());
  core.setOutput('merged_pr_url', pr.html_url);
  core.setOutput('terminal_hierarchy_level', terminalHierarchyLevel);

  core.info(`Completed Phase: ${completedPhase}`);
  core.info(`Next Phase: ${effectiveNextPhase} (${nextPhaseName})`);
  core.info(`Issue Number: ${issueNumber}`);
}

module.exports = {
  analyzeChangedFiles,
  collectSpecDirectoriesForIssue,
  expectedCloudBaseRef,
  extractIssueNumberFromPr,
  hasTerminalArtifactSet,
  loadMergedSpecState,
  parseHierarchyLevel,
  resolveValidatedHierarchyLevel,
  resolveHierarchyLevelFromWorkspace,
  run,
};
