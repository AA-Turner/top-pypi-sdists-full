'use strict';

const { execFile: nodeExecFile } = require('node:child_process');
const { isAbsolute } = require('node:path');

const UPSTREAM_WORKFLOW_NAME = 'Running Copilot cloud agent';
const UPSTREAM_WORKFLOW_PATH = 'dynamic/copilot-swe-agent/copilot';
const MAX_ASSOCIATED_PR_PAGES = 10;
const PAGE_SIZE = 100;

const ASSESSMENT_RESULTS = Object.freeze([
  Object.freeze(['verified_empty', 'verified_no_delivery']),
  Object.freeze(['unknown', 'assessment_adapter_unavailable']),
  Object.freeze(['unknown', 'delivery_evidence_unknown']),
  Object.freeze(['unknown', 'delivery_evidence_incomplete']),
  Object.freeze(['unknown', 'delivery_evidence_malformed']),
  Object.freeze(['unknown', 'delivery_not_admitted']),
  Object.freeze(['not_admitted', 'workflow_not_success']),
  Object.freeze(['not_admitted', 'pr_missing']),
  Object.freeze(['not_admitted', 'pr_ambiguous']),
  Object.freeze(['not_admitted', 'cross_repository']),
  Object.freeze(['not_admitted', 'stale_head']),
  Object.freeze(['not_admitted', 'pr_lookup_unavailable']),
]);
const STATUS_REASON_PAIRS = new Set(ASSESSMENT_RESULTS.map(([status, reason]) => `${status}:${reason}`));

function assessment(status, reason) {
  if (!STATUS_REASON_PAIRS.has(`${status}:${reason}`)) {
    return { assessment_status: 'unknown', assessment_reason: 'delivery_evidence_malformed' };
  }
  return { assessment_status: status, assessment_reason: reason };
}

function repositoryName(value) {
  return typeof value === 'string' && /^[^/]+\/[^/]+$/.test(value)
    ? value.toLowerCase()
    : null;
}

function repositoryIdentity(pr) {
  return repositoryName(pr?.base?.repo?.full_name);
}

function validPullNumber(number) {
  return Number.isSafeInteger(number) && number > 0;
}

function uniqueByNumber(pullRequests) {
  const unique = new Map();
  for (const pr of pullRequests) {
    if (validPullNumber(pr?.number)) unique.set(pr.number, pr);
  }
  return [...unique.values()];
}

function selectCandidates(pullRequests, expectedRepository, headSha = null) {
  const candidates = [];
  let sawForeignRepository = false;
  for (const pr of pullRequests) {
    if (!validPullNumber(pr?.number)) continue;
    const identity = repositoryIdentity(pr);
    if (identity && identity !== expectedRepository) {
      sawForeignRepository = true;
      continue;
    }
    if (headSha && typeof pr.head?.sha === 'string' && pr.head.sha !== headSha) continue;
    candidates.push(pr);
  }
  return { candidates: uniqueByNumber(candidates), sawForeignRepository };
}

async function lookupAssociatedPullRequests(github, owner, repo, headSha) {
  const pullRequests = [];
  for (let page = 1; page <= MAX_ASSOCIATED_PR_PAGES; page++) {
    const response = await github.rest.repos.listPullRequestsAssociatedWithCommit({
      owner,
      repo,
      commit_sha: headSha,
      per_page: PAGE_SIZE,
      page,
    });
    if (!Array.isArray(response?.data)) throw new Error('Invalid pull request lookup response');
    pullRequests.push(...response.data);
    if (response.data.length < PAGE_SIZE) return pullRequests;
  }
  throw new Error('Pull request lookup exceeded the page limit');
}

async function correlatePullRequest({ github, owner, repo, expectedRepository, workflowRun, headSha }) {
  const payloadAssociations = Array.isArray(workflowRun.pull_requests)
    ? workflowRun.pull_requests
    : [];
  let candidates;
  let sawForeignRepository = false;

  if (payloadAssociations.length > 0) {
    const selected = selectCandidates(payloadAssociations, expectedRepository, headSha);
    candidates = selected.candidates;
    sawForeignRepository = selected.sawForeignRepository;
    if (candidates.length > 1) return assessment('not_admitted', 'pr_ambiguous');
    if (candidates.length === 0 && sawForeignRepository) {
      return assessment('not_admitted', 'cross_repository');
    }
  }

  if (!candidates || candidates.length === 0) {
    let associated;
    try {
      associated = await lookupAssociatedPullRequests(github, owner, repo, headSha);
    } catch {
      return assessment('not_admitted', 'pr_lookup_unavailable');
    }
    const selected = selectCandidates(associated, expectedRepository, headSha);
    candidates = selected.candidates;
    sawForeignRepository = selected.sawForeignRepository;
    if (candidates.length > 1) return assessment('not_admitted', 'pr_ambiguous');
    if (candidates.length === 0 && sawForeignRepository) {
      return assessment('not_admitted', 'cross_repository');
    }
  }

  if (!candidates || candidates.length === 0) {
    return assessment('not_admitted', 'pr_missing');
  }

  const pullNumber = candidates[0].number;
  let livePullRequest;
  try {
    const response = await github.rest.pulls.get({
      owner,
      repo,
      pull_number: pullNumber,
    });
    livePullRequest = response?.data;
  } catch {
    return assessment('not_admitted', 'pr_lookup_unavailable');
  }

  if (!livePullRequest || livePullRequest.number !== pullNumber) {
    return assessment('not_admitted', 'pr_lookup_unavailable');
  }
  const liveRepository = repositoryIdentity(livePullRequest);
  if (liveRepository && liveRepository !== expectedRepository) {
    return assessment('not_admitted', 'cross_repository');
  }
  if (!liveRepository) return assessment('not_admitted', 'pr_lookup_unavailable');
  if (livePullRequest.head?.sha !== headSha) {
    return assessment('not_admitted', 'stale_head');
  }

  return {
    identity: { repository: `${owner}/${repo}`, prNumber: pullNumber, headSha },
    body: livePullRequest.body,
  };
}

function isRecord(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function validateDeliveryResult(result, identity) {
  const fields = ['repository', 'prNumber', 'headSha', 'outcome', 'complete', 'diffEvidence'];
  if (
    !isRecord(result)
    || Object.keys(result).length !== fields.length
    || !fields.every(field => Object.hasOwn(result, field))
    || typeof result.repository !== 'string'
    || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(result.repository)
    || result.repository.trim() !== result.repository
    || repositoryName(result.repository) !== repositoryName(identity.repository)
    || !validPullNumber(result.prNumber)
    || result.prNumber !== identity.prNumber
    || typeof result.headSha !== 'string'
    || !/^[0-9a-fA-F]{40}$/.test(result.headSha)
    || result.headSha.length !== 40
    || result.headSha.toLowerCase() !== identity.headSha.toLowerCase()
    || !(
      (result.outcome === 'DELIVERED' && result.complete === true && result.diffEvidence === 'NON_ZERO_DIFF')
      || (result.outcome === 'UNKNOWN' && result.complete === false && result.diffEvidence === 'UNKNOWN')
    )
  ) {
    throw new Error('Invalid delivery evidence');
  }
  return {
    repository: identity.repository,
    prNumber: identity.prNumber,
    headSha: identity.headSha,
    outcome: result.outcome,
    complete: result.complete,
    diffEvidence: result.diffEvidence,
  };
}

function createPythonDeliveryAdapter({
  execFile = nodeExecFile,
  env = process.env,
  timeoutMs = 120000,
  pythonExecutable = 'python',
  cwd = process.env.GITHUB_WORKSPACE,
  maxBuffer = 65536,
} = {}) {
  if (
    typeof execFile !== 'function'
    || typeof pythonExecutable !== 'string' || !pythonExecutable.trim()
    || typeof cwd !== 'string' || !isAbsolute(cwd)
    || !Number.isSafeInteger(timeoutMs) || timeoutMs <= 0 || timeoutMs > 120000
    || !Number.isSafeInteger(maxBuffer) || maxBuffer <= 0 || maxBuffer > 65536
    || !isRecord(env)
    || !['PATH', 'GH_TOKEN', 'HOME'].every(
      key => Object.hasOwn(env, key) && typeof env[key] === 'string' && env[key].length > 0,
    )
  ) {
    throw new Error('Invalid delivery adapter configuration');
  }
  const childEnv = {};
  for (const key of ['PATH', 'GH_TOKEN', 'HOME', 'XDG_CONFIG_HOME', 'XDG_CACHE_HOME', 'TMPDIR', 'RUNNER_TEMP']) {
    if (Object.hasOwn(env, key)) {
      if (typeof env[key] !== 'string') throw new Error('Invalid delivery adapter configuration');
      childEnv[key] = env[key];
    }
  }
  return async identity => {
    if (
      !isRecord(identity)
      || typeof identity.repository !== 'string'
      || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(identity.repository)
      || identity.repository.trim() !== identity.repository
      || !validPullNumber(identity.prNumber)
      || typeof identity.headSha !== 'string'
      || !/^[0-9a-fA-F]{40}$/.test(identity.headSha)
      || identity.headSha.length !== 40
    ) {
      throw new Error('Invalid delivery identity');
    }
    return new Promise((resolve, reject) => {
      try {
        execFile(pythonExecutable, [
          '-m', 'agentic_devtools.cli.ci.pipeline.delivery_bridge',
          '--repository', identity.repository,
          '--pr-number', String(identity.prNumber),
          '--head-sha', identity.headSha.toLowerCase(),
        ], { cwd, env: childEnv, shell: false, windowsHide: true, timeout: timeoutMs, maxBuffer, encoding: 'utf8' },
        (error, stdout) => {
          try {
            if (error || typeof stdout !== 'string' || Buffer.byteLength(stdout, 'utf8') > maxBuffer) {
              throw new Error('Delivery invocation failed');
            }
            const framedOutput = stdout.endsWith('\n') ? stdout.slice(0, -1) : stdout;
            if (!framedOutput.startsWith('{') || !framedOutput.endsWith('}')) {
              throw new Error('Invalid delivery output');
            }
            resolve(validateDeliveryResult(JSON.parse(framedOutput), identity));
          } catch {
            reject(new Error('Delivery evidence unavailable'));
          }
        });
      } catch {
        reject(new Error('Delivery evidence unavailable'));
      }
    });
  };
}

async function assessDelivery(identity, adapter) {
  if (typeof adapter !== 'function') {
    return assessment('unknown', 'assessment_adapter_unavailable');
  }

  let result;
  try {
    result = await adapter(identity);
  } catch {
    return assessment('unknown', 'delivery_evidence_unknown');
  }

  if (
    !isRecord(result)
    || typeof result.repository !== 'string'
    || !validPullNumber(result.prNumber)
    || typeof result.headSha !== 'string'
    || typeof result.outcome !== 'string'
    || typeof result.complete !== 'boolean'
  ) {
    return assessment('unknown', 'delivery_evidence_malformed');
  }

  if (!['NO_DELIVERY', 'DELIVERED', 'UNKNOWN', 'ZERO_DIFF', 'NON_ZERO_DIFF'].includes(result.outcome)) {
    return assessment('unknown', 'delivery_evidence_malformed');
  }

  if (
    repositoryName(result.repository) !== repositoryName(identity.repository)
    || result.prNumber !== identity.prNumber
    || result.headSha !== identity.headSha
  ) {
    return assessment('unknown', 'delivery_evidence_unknown');
  }

  if (!result.complete || result.outcome === 'ZERO_DIFF' || result.outcome === 'NON_ZERO_DIFF') {
    return assessment('unknown', 'delivery_evidence_incomplete');
  }

  if (result.outcome === 'NO_DELIVERY') {
    return assessment('verified_empty', 'verified_no_delivery');
  }
  if (result.outcome === 'DELIVERED') {
    return assessment('unknown', 'delivery_not_admitted');
  }
  return assessment('unknown', 'delivery_evidence_unknown');
}

async function assessCompletion({ github, context, workflowRun, assessDelivery: adapter, core }) {
  const owner = context?.repo?.owner;
  const repo = context?.repo?.repo;
  const expectedRepository = repositoryName(
    typeof owner === 'string' && typeof repo === 'string' ? `${owner}/${repo}` : null,
  );
  const runRepository = repositoryName(workflowRun?.repository?.full_name);
  const headSha = workflowRun?.head_sha;
  let result;
  let deliveryEvidence;

  if (
    !isRecord(workflowRun)
    || workflowRun.name !== UPSTREAM_WORKFLOW_NAME
    || workflowRun.path !== UPSTREAM_WORKFLOW_PATH
    || !expectedRepository
    || !runRepository
    || !headSha
    || typeof headSha !== 'string'
  ) {
    result = assessment('not_admitted', 'pr_lookup_unavailable');
  } else if (runRepository !== expectedRepository) {
    result = assessment('not_admitted', 'cross_repository');
  } else if (workflowRun.conclusion !== 'success') {
    result = assessment('not_admitted', 'workflow_not_success');
  } else {
    const correlated = await correlatePullRequest({
      github,
      owner,
      repo,
      expectedRepository,
      workflowRun,
      headSha,
    });
    if (correlated.assessment_status) {
      result = correlated;
    } else {
      const captureEvidence = typeof adapter === 'function'
        ? async identity => {
          const deliveryResult = await adapter(identity);
          try {
            const validated = validateDeliveryResult(deliveryResult, identity);
            deliveryEvidence = {
              identity: {
                repository: validated.repository,
                prNumber: validated.prNumber,
                headSha: validated.headSha,
              },
              diffEvidence: validated.diffEvidence,
            };
          } catch {
            deliveryEvidence = undefined;
          }
          return deliveryResult;
        }
        : adapter;
      result = await assessDelivery(correlated.identity, captureEvidence);
      if (deliveryEvidence) result = { ...result, deliveryEvidence };
      if (
        result.assessment_status === 'unknown'
        && result.assessment_reason === 'delivery_not_admitted'
        && deliveryEvidence?.diffEvidence === 'NON_ZERO_DIFF'
        && correlated.body === 'None retained'
        && core?.summary
      ) {
        await core.summary
          .addRaw(`PR #${deliveryEvidence.identity.prNumber} at head ${deliveryEvidence.identity.headSha}: stale PR-body sentinel \`None retained\`; diff evidence: NON_ZERO_DIFF; assessment reason: delivery_not_admitted. This diagnostic does not authorize delivery, readiness, or PR lifecycle changes.`)
          .write();
      }
    }
  }

  if (core?.setOutput) {
    core.setOutput('assessment_status', result.assessment_status);
    core.setOutput('assessment_reason', result.assessment_reason);
  }
  return result;
}

module.exports = {
  assessCompletion,
  createPythonDeliveryAdapter,
  ASSESSMENT_RESULTS,
  UPSTREAM_WORKFLOW_NAME,
  MAX_ASSOCIATED_PR_PAGES,
};
