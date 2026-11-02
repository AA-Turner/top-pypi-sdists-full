'use strict';

const DISPATCH_HIERARCHY_LEVELS = Object.freeze(['auto', 'feature', 'epic', 'task']);
const DISPATCH_HIERARCHY_LEVEL_SET = new Set(DISPATCH_HIERARCHY_LEVELS);

function normalizeHierarchyLevelForDispatch(value) {
  if (typeof value !== 'string') return 'auto';
  const normalized = value.trim().toLowerCase();
  return DISPATCH_HIERARCHY_LEVEL_SET.has(normalized) ? normalized : 'auto';
}

function resolveInitialProgressionPhase(engine, resolvedLevel, specContext) {
  const normalizedEngine = typeof engine === 'string' ? engine.trim().toLowerCase() : '';
  return normalizedEngine === 'cloud-agent' &&
    normalizeHierarchyLevelForDispatch(resolvedLevel) === 'task' &&
    typeof specContext === 'string' && specContext.trim() !== ''
    ? 3
    : 1;
}

function parsePositiveInteger(value, name) {
  if (typeof value === 'number') {
    if (Number.isSafeInteger(value) && value > 0) return value;
  } else if (typeof value === 'string' && /^\d+$/.test(value.trim())) {
    const parsed = Number(value.trim());
    if (Number.isSafeInteger(parsed) && parsed > 0) return parsed;
  }
  throw new TypeError(`${name} must be a positive integer`);
}

function parsePhase(value) {
  const phase = typeof value === 'number'
    ? value
    : typeof value === 'string' && /^\d+$/.test(value.trim())
      ? Number(value.trim())
      : NaN;
  if (!Number.isInteger(phase) || ![1, 2, 3].includes(phase)) {
    throw new TypeError('phase must be 1, 2, or 3');
  }
  return phase;
}

function buildPhaseProgressionInputs(options = {}) {
  if (options === null || typeof options !== 'object' || Array.isArray(options)) {
    throw new TypeError('progression inputs must be an object');
  }

  const { issueNumber, phase, hierarchyLevel, specDir, specContext } = options;
  const inputs = {
    issue_number: String(parsePositiveInteger(issueNumber, 'issue number')),
    phase: String(parsePhase(phase)),
    hierarchy_level: normalizeHierarchyLevelForDispatch(hierarchyLevel),
  };
  if (specDir !== undefined) {
    if (typeof specDir !== 'string') throw new TypeError('specDir must be a string when supplied');
    inputs.spec_dir = specDir;
  }
  if (specContext !== undefined) {
    if (typeof specContext !== 'string') throw new TypeError('specContext must be a string when supplied');
    inputs.spec_context = specContext;
  }
  return inputs;
}

async function dispatchRecordedProgression({ github, context, inputs }) {
  const recordedInputs = buildPhaseProgressionInputs({
    issueNumber: inputs.issue_number,
    phase: inputs.phase,
    hierarchyLevel: inputs.hierarchy_level,
    specDir: inputs.spec_dir ?? '',
    specContext: inputs.spec_context ?? '',
  });
  await github.rest.issues.createComment({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: Number(recordedInputs.issue_number),
    body: `<!-- speckit:progression-dispatch schema_version=1 ${JSON.stringify(recordedInputs)} -->`,
  });
  await github.rest.actions.createWorkflowDispatch({
    owner: context.repo.owner,
    repo: context.repo.repo,
    workflow_id: 'speckit-phase-progression.yml',
    ref: 'main',
    inputs: recordedInputs,
  });
}

module.exports = {
  DISPATCH_HIERARCHY_LEVELS,
  normalizeHierarchyLevelForDispatch,
  resolveInitialProgressionPhase,
  buildPhaseProgressionInputs,
  dispatchRecordedProgression,
};
