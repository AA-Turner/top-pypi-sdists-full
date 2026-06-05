const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';
const PROJECT_ROOT = path.resolve(__dirname, '../..'); // 部署到 .kanban/dashboard/ 后为项目根目录
// KANBAN_ROOT resolution (priority: env var > __dirname heuristics):
//   1. KANBAN_ROOT env var — set by Python DashboardManager.start() with the correct project path
//   2. __dirname/.. — works when deployed to .kanban/dashboard/
//   3. Walk-up fallback — for source layout (.claude/skills/kanban/dashboard/)
let KANBAN_ROOT;
if (process.env.KANBAN_ROOT && fs.existsSync(path.join(process.env.KANBAN_ROOT, 'config.json'))) {
  KANBAN_ROOT = process.env.KANBAN_ROOT;
} else {
  KANBAN_ROOT = path.resolve(__dirname, '..');
  if (!fs.existsSync(path.join(KANBAN_ROOT, 'config.json'))) {
    let searchDir = PROJECT_ROOT;
    for (let i = 0; i < 8; i++) {
      const candidateRoot = path.join(searchDir, '.kanban');
      if (fs.existsSync(path.join(candidateRoot, 'config.json'))) {
        KANBAN_ROOT = candidateRoot;
        break;
      }
      searchDir = path.resolve(searchDir, '..');
    }
  }
}

app.use(express.json());
app.use(express.static(__dirname));

// ── Shared: resolve Python binary (cross-platform) ──
function getPythonBin() {
  // 1. Config override
  try {
    const cfgPath = path.join(KANBAN_ROOT, 'config.json');
    if (fs.existsSync(cfgPath)) {
      const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf-8'));
      if (cfg.python_bin) return cfg.python_bin;
    }
  } catch (_) {}
  // 2. Env override
  if (process.env.KANBAN_PYTHON_BIN) return process.env.KANBAN_PYTHON_BIN;
  // 3. Platform defaults: try python3, python, py
  const { execSync } = require('child_process');
  for (const bin of ['python3', 'python', 'py']) {
    try {
      execSync(`${bin} --version`, { stdio: 'ignore', timeout: 3000 });
      return bin;
    } catch (_) {}
  }
  return 'python3';  // last resort
}

// Debug: log KANBAN_ROOT and check connectivity
console.log('KANBAN_ROOT:', KANBAN_ROOT);
console.log('config.json exists:', fs.existsSync(path.join(KANBAN_ROOT, 'config.json')));
console.log('tasks dir exists:', fs.existsSync(path.join(KANBAN_ROOT, 'tasks')));

// Health-check endpoint for debugging
app.get('/api/health', (req, res) => {
  const tasksDir = path.join(KANBAN_ROOT, 'tasks');
  let taskCount = 0;
  if (fs.existsSync(tasksDir)) {
    taskCount = fs.readdirSync(tasksDir).filter(d =>
      fs.existsSync(path.join(tasksDir, d, 'task.json'))
    ).length;
  }
  res.json({
    kanban_root: KANBAN_ROOT,
    config_exists: fs.existsSync(path.join(KANBAN_ROOT, 'config.json')),
    tasks_dir_exists: fs.existsSync(tasksDir),
    task_count: taskCount,
    cwd: process.cwd(),
    __dirname: __dirname,
  });
});

// ============================================================
// Input validation
// ============================================================
/**
 * Validate that a task ID parameter is safe to use in file-system operations.
 * Enforces:
 *   - Non-empty string
 *   - Maximum length of 20 characters (prevents buffer overflow / path traversal
 *     via extremely long IDs)
 *   - No ".." sequences (blocks directory traversal attacks e.g. "../", "..\\")
 */
const PATH_TRAVERSAL_PATTERN = /\.\./;

// ── JSONL timestamp index cache (built once, reused for per-task estimation) ──
let _jsonlIndex = null;
function getJSONLIndex() {
  if (_jsonlIndex) return _jsonlIndex;
  const sessionDir = findSessionDir();
  if (!sessionDir) { _jsonlIndex = { timestamps: [] }; return _jsonlIndex; }
  const timestamps = [];
  try {
    for (const f of fs.readdirSync(sessionDir).filter(f => f.endsWith('.jsonl'))) {
      const content = fs.readFileSync(path.join(sessionDir, f), 'utf-8');
      for (const line of content.split(/\r?\n/)) {
        if (!line.trim()) continue;
        try { const e = JSON.parse(line); if (e.timestamp) timestamps.push(typeof e.timestamp === 'number' ? e.timestamp : new Date(e.timestamp).getTime() / 1000); } catch (_) {}
      }
    }
  } catch (_) {}
  timestamps.sort((a, b) => a - b);
  _jsonlIndex = { timestamps, builtAt: Date.now() };
  return _jsonlIndex;
}
setInterval(() => { _jsonlIndex = null; }, 300000); // refresh every 5 min

// Step definitions with agent_type for Dashboard display (#219, #221)
const STEP_DEFINITIONS = {
  "plan.knowledge_search": { description: "知识库检索", agent_type: "general-purpose" },
  "plan.plan_A": { description: "需求澄清（brainstorming）", agent_type: null },
  "plan.check_constraints": { description: "知识库约束检查", agent_type: "general-purpose" },
  "plan.user_confirm_spec": { description: "用户确认 spec", agent_type: null },
  "plan.plan_B": { description: "任务拆解（writing-plans）", agent_type: "general-purpose" },
  "plan.complete": { description: "Plan 阶段完成", agent_type: null },
  "plan_review.spawn": { description: "6维 Plan Review", agent_type: "general-purpose" },
  "plan_review.collect": { description: "收集评审报告", agent_type: null },
  "plan_review.knowledge_cross_validate": { description: "知识引用验证", agent_type: "general-purpose" },
  "plan_review.check": { description: "评分检查", agent_type: null },
  "plan_review.complete": { description: "Plan Review 完成", agent_type: null },
  "qa_spec.spawn": { description: "QA Spec 生成", agent_type: "general-purpose" },
  "qa_spec.complete": { description: "QA Spec 完成", agent_type: null },
  "spec_review.spawn": { description: "测试规格评审", agent_type: "general-purpose" },
  "spec_review.check": { description: "评分检查", agent_type: null },
  "spec_review.user_confirm": { description: "用户确认测试用例", agent_type: null },
  "spec_review.complete": { description: "Spec Review 完成", agent_type: null },
  "execute.pitfall_check": { description: "踩坑预警", agent_type: "general-purpose" },
  "execute.spawn": { description: "执行编码（TDD）", agent_type: "kanban-executor" },
  "execute.verify": { description: "验证执行产物", agent_type: null },
  "execute.commit": { description: "Git 提交", agent_type: null },
  "execute.complete": { description: "Execute 完成", agent_type: null },
  "evaluate.spawn": { description: "4角色并行评估", agent_type: "general-purpose" },
  "evaluate.e2e_run": { description: "E2E 测试执行", agent_type: "general-purpose" },
  "evaluate.collect_scores": { description: "收集评分", agent_type: null },
  "evaluate.check_score": { description: "自迭代决策", agent_type: null },
  "evaluate.commit": { description: "Git 提交评估结果", agent_type: null },
  "evaluate.complete": { description: "Evaluate 完成", agent_type: null },
  "retrospective.spawn": { description: "复盘总结", agent_type: "general-purpose" },
  "retrospective.audit_realtime_knowledge": { description: "审计实时知识条目", agent_type: "general-purpose" },
  "retrospective.knowledge_import": { description: "导入提取的知识", agent_type: null },
  "retrospective.complete": { description: "Retrospective 完成", agent_type: null },
  "user_decision.present": { description: "展示变更摘要", agent_type: null },
  "user_decision.wait": { description: "等待用户决策", agent_type: null },
  "archive.merge": { description: "合并 worktree 代码", agent_type: null },
  "archive.guard": { description: "归档 Guards", agent_type: null },
  "archive.cleanup": { description: "清理 worktree", agent_type: null },
};

// --- Helper: discover agent types from .claude/agents/ directory ---
function discoverAgentTypes() {
  const agentTypes = new Set(['general-purpose']);
  // Scan project .claude/agents/*.md — each file defines an agent type
  const agentsDir = path.join(PROJECT_ROOT, '.claude', 'agents');
  if (fs.existsSync(agentsDir)) {
    try {
      for (const f of fs.readdirSync(agentsDir)) {
        if (!f.endsWith('.md')) continue;
        try {
          const content = fs.readFileSync(path.join(agentsDir, f), 'utf-8');
          // Extract name from frontmatter (e.g. "---\nname: kanban-executor\n---")
          const nameMatch = content.match(/^---\s*\n\s*name:\s*(.+?)\s*$/m);
          if (nameMatch) {
            agentTypes.add(nameMatch[1].trim());
          }
        } catch (_) {}
      }
    } catch (_) {}
  }
  return Array.from(agentTypes).sort();
}

// --- API: step definitions for visual step editor ---
app.get('/api/step-definitions', (req, res) => {
  const phases = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'archive'];
  const agent_types = discoverAgentTypes();
  try {
    const workflowPath = path.join(KANBAN_ROOT, 'workflow.json');
    if (fs.existsSync(workflowPath)) {
      const wf = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));
      if (wf.phases && Array.isArray(wf.phases) && wf.phases.some(p => p.steps)) {
        const steps = {};
        for (const p of wf.phases) {
          if (p.steps && Array.isArray(p.steps)) {
            const phaseSteps = {};
            for (const s of p.steps) {
              const sid = s.id || '';
              const fullId = sid.includes('.') ? sid : `${p.id}.${sid}`;
              phaseSteps[fullId] = { ...s };  // include all fields
            }
            steps[p.id] = phaseSteps;
          }
        }
        return res.json({ steps, phases, agent_types });
      }
    }
  } catch (_) { /* fall back to built-in definitions */ }
  // Fallback: load from workflows/ directory files (full step details)
  const wfDir = path.join(KANBAN_ROOT, 'workflows');
  if (fs.existsSync(wfDir)) {
    const steps = {};
    for (const f of fs.readdirSync(wfDir)) {
      if (!f.endsWith('.json')) continue;
      try {
        const modeFile = JSON.parse(fs.readFileSync(path.join(wfDir, f), 'utf-8'));
        if (modeFile.phases && Array.isArray(modeFile.phases)) {
          for (const p of modeFile.phases) {
            if (p.steps && Array.isArray(p.steps)) {
              const phaseSteps = {};
              for (const s of p.steps) {
                const sid = s.id || '';
                const fullId = sid.includes('.') ? sid : `${p.id}.${sid}`;
                phaseSteps[fullId] = { ...s };  // include all fields
              }
              steps[p.id] = { ...steps[p.id], ...phaseSteps };
            }
          }
        }
      } catch (_) {}
    }
    if (Object.keys(steps).length > 0) {
      return res.json({ steps, phases, agent_types });
    }
  }
  res.json({ steps: STEP_DEFINITIONS, phases, agent_types });
});
function isValidTaskId(id) {
  return typeof id === 'string' && id.length > 0 && id.length <= 20 && !PATH_TRAVERSAL_PATTERN.test(id);
}

// ============================================================
// Shared helpers
// ============================================================

/**
 * Collect evaluation reports for a task from its iteration directories.
 * Used by /api/tasks/:id, /api/archive/:id, and /api/archived-tasks/:id.
 *
 * @param {string} taskDir - Parent directory containing the task subdirectory (e.g. tasks/ or archive/)
 * @param {string} taskId  - The task ID (e.g. TASK-001)
 * @param {object} data    - The parsed task JSON (may contain a scores object)
 * @returns {Array} Collected report objects
 */
function collectReports(taskDir, taskId, data) {
  const reports = [];

  // 1. Reports referenced in scores object (path in score info)
  if (data.scores) {
    for (const [role, info] of Object.entries(data.scores)) {
      if (typeof info === 'object' && info.report) {
        let reportPath = path.join(KANBAN_ROOT, info.report);
        if (!fs.existsSync(reportPath)) {
          reportPath = info.report; // try as-is (may already be absolute)
        }
        if (fs.existsSync(reportPath)) {
          try {
            const reportData = JSON.parse(fs.readFileSync(reportPath, 'utf-8'));
            reports.push({ role, score: info.score, passed: info.passed, report: reportData });
          } catch (_) { /* skip malformed report */ }
        }
      }
    }
  }

  // 2. Scan iteration directories for report files
  //    <taskDir>/<taskId>/iteration-N/<role>_report.json
  const taskSubdir = path.join(taskDir, taskId);
  if (fs.existsSync(taskSubdir) && fs.statSync(taskSubdir).isDirectory()) {
    const iterEntries = fs.readdirSync(taskSubdir, { withFileTypes: true });
    for (const entry of iterEntries) {
      if (!entry.isDirectory() || !entry.name.startsWith('iteration-')) continue;
      const iterDir = path.join(taskSubdir, entry.name);
      const roleFiles = fs.readdirSync(iterDir).filter(f => f.endsWith('_report.json'));
      for (const rf of roleFiles) {
        const role = rf.replace('_report.json', '');
        // Skip if we already have this role's report from scores
        if (reports.some(r => r.role === role)) continue;
        try {
          const reportData = JSON.parse(fs.readFileSync(path.join(iterDir, rf), 'utf-8'));
          const iteration = parseInt(entry.name.replace('iteration-', ''), 10);
          reports.push({
            role,
            score: reportData.scores ? (reportData.scores.overall || null) : null,
            passed: reportData.passed || false,
            report: reportData,
            iteration
          });
        } catch (_) { /* skip malformed report */ }
      }
    }
  }

  return reports;
}

// ============================================================
// SSE (Server-Sent Events) — real-time push to dashboard
// ============================================================

const sseClients = new Set();

/** Broadcast a named SSE event to every connected client. */
function broadcastSSE(eventType, data) {
  const payload = `event: ${eventType}\ndata: ${JSON.stringify(data)}\n\n`;
  for (const client of sseClients) {
    client.write(payload);
  }
}

/**
 * Atomic-write JSON to a file: write to temp file first, then rename.
 * Avoids half-written files on crash.
 */
function atomicWriteJSON(filePath, data) {
  const tmp = filePath + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n', 'utf-8');
  fs.renameSync(tmp, filePath);
}

/**
 * Validate config.json fields. Returns { valid, errors }.
 */
function validateConfig(data) {
  const errors = [];
  if (data.timeout !== undefined) {
    for (const [k, v] of Object.entries(data.timeout)) {
      if (typeof v !== 'number' || v < 0) errors.push(`timeout.${k} must be a non-negative number`);
    }
  }
  if (data.budget !== undefined) {
    if (data.budget.per_task !== undefined && typeof data.budget.per_task !== 'number')
      errors.push('budget.per_task must be a number');
    if (data.budget.warning_threshold !== undefined &&
        (typeof data.budget.warning_threshold !== 'number' ||
         data.budget.warning_threshold < 0 || data.budget.warning_threshold > 1))
      errors.push('budget.warning_threshold must be a number between 0 and 1');
  }
  if (data.scheduler !== undefined) {
    if (data.scheduler.max_parallel !== undefined &&
        (typeof data.scheduler.max_parallel !== 'number' ||
         data.scheduler.max_parallel < 1 || data.scheduler.max_parallel > 10))
      errors.push('scheduler.max_parallel must be between 1 and 10');
  }
  if (data.knowledge !== undefined && data.knowledge.scope !== undefined) {
    if (typeof data.knowledge.scope !== 'string')
      errors.push('knowledge.scope must be a string');
    else if (data.knowledge.scope && !/^[a-z0-9][a-z0-9-]{1,15}$/.test(data.knowledge.scope))
      errors.push('knowledge.scope must match ^[a-z0-9][a-z0-9-]{1,15}$');
  }
  return { valid: errors.length === 0, errors };
}

/**
 * Validate workflow.json structure. Returns { valid, errors }.
 */
function validateWorkflow(data) {
  const errors = [];
  const validPhaseIds = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'archive'];
  if (data.phases !== undefined && Array.isArray(data.phases)) {
    for (const phase of data.phases) {
      if (phase.id && !validPhaseIds.includes(phase.id))
        errors.push(`Unknown phase id: ${phase.id}`);
      if (phase.agents !== undefined && !Array.isArray(phase.agents))
        errors.push(`phase ${phase.id}: agents must be an array`);
    }
  }
  if (data.pass_threshold !== undefined &&
      (typeof data.pass_threshold !== 'number' ||
       data.pass_threshold < 0 || data.pass_threshold > 10))
    errors.push('pass_threshold must be between 0 and 10');
  // Validate extensions
  if (data.extensions !== undefined && typeof data.extensions === 'object') {
    if (data.extensions.add_steps !== undefined && Array.isArray(data.extensions.add_steps)) {
      for (let i = 0; i < data.extensions.add_steps.length; i++) {
        const item = data.extensions.add_steps[i];
        if (!item.step || !item.step.id || !item.step.id.trim())
          errors.push(`extensions.add_steps[${i}]: step.id is required`);
        if (!item.phase || !validPhaseIds.includes(item.phase))
          errors.push(`extensions.add_steps[${i}]: invalid phase "${item.phase}"`);
      }
    }
  }
  // Validate guard config
  const validCheckNames = ['knowledge_references', 'test_files', 'tdd_evidence', 'test_spec_coverage', 'knowledge_artifact', 'quick_scope'];
  if (data.phases !== undefined && Array.isArray(data.phases)) {
    for (const phase of data.phases) {
      if (phase.guard) {
        if (phase.guard.checks !== undefined && Array.isArray(phase.guard.checks)) {
          for (const c of phase.guard.checks) {
            if (!validCheckNames.includes(c))
              errors.push(`phase ${phase.id}: unknown guard check "${c}"`);
          }
        }
        if (phase.guard.quick_limits) {
          const ql = phase.guard.quick_limits;
          for (const k of ['max_files', 'max_total_lines', 'max_added_lines']) {
            if (ql[k] !== undefined && (typeof ql[k] !== 'number' || ql[k] < 1))
              errors.push(`phase ${phase.id}: guard.quick_limits.${k} must be a positive integer`);
          }
        }
        if (phase.guard.test_spec_coverage_threshold !== undefined &&
            (typeof phase.guard.test_spec_coverage_threshold !== 'number' ||
             phase.guard.test_spec_coverage_threshold < 0 ||
             phase.guard.test_spec_coverage_threshold > 1))
          errors.push(`phase ${phase.id}: guard.test_spec_coverage_threshold must be between 0 and 1`);
      }
    }
  }
  return { valid: errors.length === 0, errors };
}

/**
 * Debounced event scheduler.
 * If the same *key* fires again within the delay window the previous
 * timer is cancelled and replaced — guarantees at most one broadcast
 * per burst.
 */
const pendingEvents = new Map();
function scheduleEvent(key, delay, fireFn) {
  const existing = pendingEvents.get(key);
  if (existing) clearTimeout(existing.timer);
  pendingEvents.set(key, {
    timer: setTimeout(() => {
      pendingEvents.delete(key);
      fireFn();
    }, delay),
    fireFn
  });
}

// --- Task cache for diff detection ---
let cachedTasks = [];

/**
 * Map role name with underscores to template filename with hyphens.
 * Bug #4 fix: code_reviewer -> code-reviewer for template lookup.
 */
function roleToTemplateFilename(role) {
  return role.replace(/_/g, '-') + '.json';
}

/** Read a single task JSON, trying both new (subdir) and old (flat) layouts. */
function readTaskJson(tasksDir, idOrFile) {
  // Try new layout first: tasks/TASK-NNN/task.json
  const subdirPath = path.join(tasksDir, idOrFile.replace(/\.json$/, ''), 'task.json');
  if (fs.existsSync(subdirPath)) {
    try {
      return JSON.parse(fs.readFileSync(subdirPath, 'utf-8'));
    } catch (_) { return null; }
  }
  // Fallback to old layout: tasks/TASK-NNN.json
  const flatPath = path.join(tasksDir, idOrFile);
  if (fs.existsSync(flatPath) && flatPath.endsWith('.json')) {
    try {
      return JSON.parse(fs.readFileSync(flatPath, 'utf-8'));
    } catch (_) { return null; }
  }
  return null;
}

/** Read every task file under .kanban/tasks/ (active only) and return a summary array. */
function readAllTasks() {
  const tasksDir = path.join(KANBAN_ROOT, 'tasks');
  const results = [];

  if (fs.existsSync(tasksDir)) {
    // Scan new layout: tasks/TASK-NNN/task.json (subdirectories)
    const entries = fs.readdirSync(tasksDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const taskJsonPath = path.join(tasksDir, entry.name, 'task.json');
      if (!fs.existsSync(taskJsonPath)) continue;
      try {
        const data = JSON.parse(fs.readFileSync(taskJsonPath, 'utf-8'));
        results.push({
          id: data.id || entry.name,
          status: data.status,
          phase: data.phase,
          phase_lock: data.phase_lock,
          iteration: data.iteration,
          updated_at: data.updated_at,
          archived: false
        });
      } catch (_) { /* skip malformed */ }
    }

    // Scan old layout: tasks/TASK-NNN.json (flat files)
    const files = fs.readdirSync(tasksDir).filter(f => f.endsWith('.json'));
    for (const f of files) {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(tasksDir, f), 'utf-8'));
        const id = data.id || f.replace('.json', '');
        // Avoid duplicates if both formats exist for same task
        if (!results.some(r => r.id === id)) {
          results.push({
            id,
            status: data.status,
            phase: data.phase,
            phase_lock: data.phase_lock,
            iteration: data.iteration,
            updated_at: data.updated_at,
            archived: false
          });
        }
      } catch (_) { /* skip malformed */ }
    }
  }

  return results;
}

/** Read archived tasks (same format as readAllTasks but from archive/). */
function readAllArchivedTasks() {
  const archiveDir = path.join(KANBAN_ROOT, 'archive');
  const results = [];

  if (fs.existsSync(archiveDir)) {
    const archiveEntries = fs.readdirSync(archiveDir, { withFileTypes: true });
    for (const entry of archiveEntries) {
      if (!entry.isDirectory()) continue;
      const taskJsonPath = path.join(archiveDir, entry.name, 'task.json');
      if (!fs.existsSync(taskJsonPath)) continue;
      try {
        const data = JSON.parse(fs.readFileSync(taskJsonPath, 'utf-8'));
        results.push({
          id: data.id || entry.name,
          status: data.status,
          phase: data.phase,
          phase_lock: data.phase_lock,
          iteration: data.iteration,
          updated_at: data.updated_at,
          archived: true
        });
      } catch (_) { /* skip malformed */ }
    }

    // Scan old layout: archive/TASK-NNN.json (flat files)
    const archiveFiles = fs.readdirSync(archiveDir).filter(f => f.endsWith('.json'));
    for (const f of archiveFiles) {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(archiveDir, f), 'utf-8'));
        const id = data.id || f.replace('.json', '');
        if (!results.some(r => r.id === id)) {
          results.push({
            id,
            status: data.status,
            phase: data.phase,
            phase_lock: data.phase_lock,
            iteration: data.iteration,
            updated_at: data.updated_at,
            archived: true
          });
        }
      } catch (_) { /* skip malformed */ }
    }
  }

  return results;
}

/**
 * Read a single archived task by ID from .kanban/archive/.
 * Tries both new layout (archive/TASK-NNN/task.json) and old layout (archive/TASK-NNN.json).
 *
 * @param {string} taskId - The task ID (e.g. TASK-001)
 * @returns {object|null} Parsed task JSON or null if not found
 */
function readArchivedTask(taskId) {
  const archiveDir = path.join(KANBAN_ROOT, 'archive');

  // Try new layout first: archive/TASK-NNN/task.json
  const subdirPath = path.join(archiveDir, taskId, 'task.json');
  if (fs.existsSync(subdirPath)) {
    try {
      return JSON.parse(fs.readFileSync(subdirPath, 'utf-8'));
    } catch (_) { /* malformed */ }
  }

  // Fallback to old layout: archive/TASK-NNN.json
  const flatPath = path.join(archiveDir, `${taskId}.json`);
  if (fs.existsSync(flatPath)) {
    try {
      return JSON.parse(fs.readFileSync(flatPath, 'utf-8'));
    } catch (_) { /* malformed */ }
  }

  return null;
}

/** Read all archived tasks from .kanban/archive/ directory. */
function readArchivedTasks() {
  const archiveDir = path.join(KANBAN_ROOT, 'archive');
  if (!fs.existsSync(archiveDir)) return [];

  const results = [];
  const entries = fs.readdirSync(archiveDir, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    // Try new layout: archive/TASK-NNN/task.json
    const taskJsonPath = path.join(archiveDir, entry.name, 'task.json');
    if (fs.existsSync(taskJsonPath)) {
      try {
        const data = JSON.parse(fs.readFileSync(taskJsonPath, 'utf-8'));
        results.push({
          id: data.id || entry.name,
          title: data.title,
          description: data.description,
          status: data.status,
          phase: data.phase,
          iteration: data.iteration,
          scores: data.scores,
          created_at: data.created_at,
          updated_at: data.updated_at
        });
      } catch (_) { /* skip malformed */ }
    }
  }

  // Also scan old layout: archive/TASK-NNN.json (flat files)
  const files = fs.readdirSync(archiveDir).filter(f => f.endsWith('.json'));
  for (const f of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(archiveDir, f), 'utf-8'));
      const id = data.id || f.replace('.json', '');
      if (!results.some(r => r.id === id)) {
        results.push({
          id,
          title: data.title,
          description: data.description,
          status: data.status,
          phase: data.phase,
          iteration: data.iteration,
          scores: data.scores,
          created_at: data.created_at,
          updated_at: data.updated_at
        });
      }
    } catch (_) { /* skip malformed */ }
  }

  return results;
}

/** Compare cached and current task lists, emit granular events. */
function diffAndBroadcastTasks() {
  const current = readAllTasks();
  const cachedMap = new Map(cachedTasks.map(t => [t.id, t]));
  const currentMap = new Map(current.map(t => [t.id, t]));

  const created = [];
  const updated = [];
  const removed = [];

  // Detect created & updated
  for (const task of current) {
    const prev = cachedMap.get(task.id);
    if (!prev) {
      created.push(task);
    } else if (
      prev.status !== task.status ||
      prev.phase !== task.phase ||
      prev.phase_lock !== task.phase_lock ||
      prev.iteration !== task.iteration ||
      prev.updated_at !== task.updated_at ||
      prev.archived !== task.archived
    ) {
      updated.push(task);
    }
  }
  // Detect removed
  for (const task of cachedTasks) {
    if (!currentMap.has(task.id)) {
      removed.push(task);
    }
  }

  // Emit granular per-task events for each change type
  for (const task of created) {
    broadcastSSE('task_created', { id: task.id, task });
  }
  for (const task of updated) {
    broadcastSSE('task_updated', { id: task.id, task });
  }
  for (const task of removed) {
    broadcastSSE('task_removed', { id: task.id, task });
  }

  // Also emit the full refresh event with the complete updated list
  if (created.length > 0 || updated.length > 0 || removed.length > 0) {
    broadcastSSE('tasks:refresh', current);
  }

  cachedTasks = current;
}

// ============================================================
// SSE endpoint
// ============================================================
app.get('/api/events', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no'
  });

  // Send an initial connected event so the client knows it is live.
  res.write(`event: connected\ndata: ${JSON.stringify({ time: Date.now() })}\n\n`);

  sseClients.add(res);

  // Heartbeat every 30 seconds to keep the connection alive through proxies.
  const heartbeat = setInterval(() => {
    res.write(': heartbeat\n\n');
  }, 30000);

  req.on('close', () => {
    clearInterval(heartbeat);
    sseClients.delete(res);
  });
});

// ============================================================
// File watchers (started alongside the server)
// ============================================================
const watchers = [];

/**
 * Set up a recursive watcher on a directory. If the directory does not exist,
 * create it so the watcher can be established. Returns the watcher or null.
 */
function watchDirectory(dir, options, callback) {
  if (!fs.existsSync(dir)) {
    try {
      fs.mkdirSync(dir, { recursive: true });
    } catch (err) {
      console.error(`[watcher] Failed to create directory ${dir}:`, err.message);
      return null;
    }
  }
  try {
    const w = fs.watch(dir, options, callback);
    w.on('error', (err) => {
      console.error(`[watcher] ${path.basename(dir)}/ watcher error:`, err.message);
    });
    watchers.push(w);
    return w;
  } catch (err) {
    console.error(`[watcher] Failed to watch ${dir}:`, err.message);
    return null;
  }
}

function setupWatchers() {
  // Initialise the task cache so the first watch callback can diff.
  cachedTasks = readAllTasks();

  // 1. Watch .kanban/tasks/ directory (including subdirectories for new layout)
  const tasksDir = path.join(KANBAN_ROOT, 'tasks');
  watchDirectory(tasksDir, { recursive: true }, (eventType, filename) => {
    if (!filename) return;
    // Watch for both flat .json files and task.json in subdirectories
    if (filename.endsWith('.json')) {
      scheduleEvent('tasks-dir', 150, () => {
        diffAndBroadcastTasks();
      });
    }
  });

  // 2. Watch .kanban/archive/ directory (for archived task changes)
  const archiveDir = path.join(KANBAN_ROOT, 'archive');
  watchDirectory(archiveDir, { recursive: true }, (eventType, filename) => {
    if (!filename) return;
    if (filename.endsWith('.json')) {
      scheduleEvent('archive-dir', 150, () => {
        const archived = readAllArchivedTasks();
        broadcastSSE('tasks:refresh-archived', archived);
        broadcastSSE('archive:changed', { filename });
      });
    }
  });

  // 3. Watch .kanban/reports/ (recursive -- legacy path for older layout)
  const reportsDir = path.join(KANBAN_ROOT, 'reports');
  if (fs.existsSync(reportsDir)) {
    watchDirectory(reportsDir, { recursive: true }, (eventType, filename) => {
      if (!filename) return;
      scheduleEvent('reports-dir', 150, () => {
        broadcastSSE('reports:changed', { filename });
      });
    });
  }

  // 4. Watch config.json
  const configPath = path.join(KANBAN_ROOT, 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const w = fs.watch(configPath, () => {
        try {
          const data = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
          broadcastSSE('config:changed', { file: 'config.json', data });
        } catch (_) { /* ignore read errors during mid-write */ }
      });
      w.on('error', (err) => {
        console.error('[watcher] config.json watcher error:', err.message);
      });
      watchers.push(w);
    } catch (err) {
      console.error('[watcher] Failed to watch config.json:', err.message);
    }
  }

  // 5. Watch workflow.json
  const workflowPath = path.join(KANBAN_ROOT, 'workflow.json');
  if (fs.existsSync(workflowPath)) {
    try {
      const w = fs.watch(workflowPath, () => {
        try {
          const data = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));
          broadcastSSE('config:changed', { file: 'workflow.json', data });
        } catch (_) { /* ignore read errors during mid-write */ }
      });
      w.on('error', (err) => {
        console.error('[watcher] workflow.json watcher error:', err.message);
      });
      watchers.push(w);
    } catch (err) {
      console.error('[watcher] Failed to watch workflow.json:', err.message);
    }
  }
}

// ============================================================
// Graceful shutdown
// ============================================================
function shutdown(signal) {
  console.log(`\nReceived ${signal}, shutting down gracefully...`);

  // Close all SSE client connections
  for (const client of sseClients) {
    client.end();
  }
  sseClients.clear();

  // Close file watchers
  for (const w of watchers) {
    w.close();
  }

  process.exit(0);
}

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// ============================================================
// REST API endpoints (original, unchanged)
// ============================================================

// --- API: read config.json ---
app.get('/api/config', (req, res) => {
  try {
    const configPath = path.join(KANBAN_ROOT, 'config.json');
    if (!fs.existsSync(configPath)) return res.json({});
    const data = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read config.json' });
  }
});

// --- API: read workflow.json ---
app.get('/api/workflow', (req, res) => {
  try {
    const workflowPath = path.join(KANBAN_ROOT, 'workflow.json');
    let data = {};
    if (fs.existsSync(workflowPath)) {
      data = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));
    }
    // Merge per-mode phases from .kanban/workflows/<mode>.json
    const wfDir = path.join(KANBAN_ROOT, 'workflows');
    if (data.modes && fs.existsSync(wfDir)) {
      const modes = { ...data.modes };
      for (const f of fs.readdirSync(wfDir)) {
        if (!f.endsWith('.json')) continue;
        const modeName = f.replace('.json', '');
        const modeCfg = modes[modeName] || {};
        try {
          const modeFile = JSON.parse(fs.readFileSync(path.join(wfDir, f), 'utf-8'));
          if (modeFile.phases && Array.isArray(modeFile.phases)) {
            // Directory file phases take priority over workflow.json
          modes[modeName] = { ...modeFile, ...modeCfg, phases: modeFile.phases };
          }
        } catch (_) {}
      }
      data = { ...data, modes };
    }
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read workflow.json' });
  }
});

// --- API: write config.json ---
app.put('/api/config', (req, res) => {
  try {
    const validation = validateConfig(req.body);
    if (!validation.valid) {
      return res.status(400).json({ error: 'Validation failed', details: validation.errors });
    }
    const configPath = path.join(KANBAN_ROOT, 'config.json');
    let existing = {};
    try { existing = JSON.parse(fs.readFileSync(configPath, 'utf-8')); } catch (_) {}
    const merged = { ...existing, ...req.body };
    atomicWriteJSON(configPath, merged);
    broadcastSSE('config:changed', merged);
    res.json({ success: true, data: merged });
  } catch (err) {
    res.status(500).json({ error: 'Failed to write config.json: ' + err.message });
  }
});

// --- API: write workflow.json ---
app.put('/api/workflow', (req, res) => {
  try {
    const validation = validateWorkflow(req.body);
    if (!validation.valid) {
      return res.status(400).json({ error: 'Validation failed', details: validation.errors });
    }
    const data = req.body;
    const workflowsDir = path.join(KANBAN_ROOT, 'workflows');

    // 1. Extract per-mode phases and write to .kanban/workflows/<mode>.json
    const modes = (data.modes && typeof data.modes === 'object') ? { ...data.modes } : {};
    for (const [modeName, modeCfg] of Object.entries(modes)) {
      if (modeCfg && typeof modeCfg === 'object' && modeCfg.phases && Array.isArray(modeCfg.phases)) {
        // Write full mode config (phase_order + phases) to directory file
        const modeFile = path.join(workflowsDir, `${modeName}.json`);
        fs.mkdirSync(workflowsDir, { recursive: true });
        atomicWriteJSON(modeFile, {
          name: modeName,
          phase_order: modeCfg.phase_order || [],
          phases: modeCfg.phases,
          gates: modeCfg.gates || {},
        });
        // Strip phases from workflow.json copy (keep metadata only)
        delete modes[modeName].phases;
      }
    }

    // 2. Clean up directory files for deleted modes
    const BUILTIN = new Set(['full', 'lightweight', 'quick']);
    const workflowPath = path.join(KANBAN_ROOT, 'workflow.json');
    if (fs.existsSync(workflowPath)) {
      try {
        const oldWf = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));
        const oldModes = (oldWf.modes && typeof oldWf.modes === 'object') ? oldWf.modes : {};
        for (const oldName of Object.keys(oldModes)) {
          if (!modes[oldName] && !BUILTIN.has(oldName)) {
            // Mode was deleted — remove its directory file
            const oldFile = path.join(workflowsDir, `${oldName}.json`);
            if (fs.existsSync(oldFile)) {
              fs.unlinkSync(oldFile);
              console.log(`Removed orphaned workflow file: ${oldName}.json`);
            }
          }
        }
      } catch (e) { console.error('Cleanup error:', e.message); }
    }

    // 3. Write stripped workflow.json (modes without phases)
    let existing = {};
    try { existing = JSON.parse(fs.readFileSync(workflowPath, 'utf-8')); } catch (_) {}
    const merged = { ...existing, ...data, modes };
    atomicWriteJSON(workflowPath, merged);

    // 4. Merge per-mode phases back from directory files for response
    // (client needs full data, not stripped modes)
    const responseModes = { ...merged.modes };
    if (fs.existsSync(workflowsDir)) {
      for (const f of fs.readdirSync(workflowsDir)) {
        if (!f.endsWith('.json')) continue;
        const modeName = f.replace('.json', '');
        try {
          const modeFile = JSON.parse(fs.readFileSync(path.join(workflowsDir, f), 'utf-8'));
          if (modeFile.phases && Array.isArray(modeFile.phases)) {
            responseModes[modeName] = { ...modeFile, ...(responseModes[modeName] || {}), phases: modeFile.phases };
          }
        } catch (_) {}
      }
    }
    const response = { ...merged, modes: responseModes };

    broadcastSSE('workflow:changed', response);
    res.json({ success: true, data: response });
  } catch (err) {
    res.status(500).json({ error: 'Failed to write workflow.json: ' + err.message });
  }
});

// --- API: knowledge health ---
app.get('/api/knowledge/health', (req, res) => {
  try {
    const { execFile } = require('child_process');
    execFile(getPythonBin(), ['-m', 'kanban_framework', 'knowledge', 'health', '--json'], {
      cwd: KANBAN_ROOT, timeout: 15000,
    }, (err, stdout, stderr) => {
      if (err) {
        return res.json({ success: false, error: err.message, raw: stderr || stdout });
      }
      try {
        const data = JSON.parse(stdout);
        res.json({ success: true, data });
      } catch (_) {
        res.json({ success: false, raw: stdout });
      }
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to check knowledge health' });
  }
});

// --- API: list pending knowledge entries ---
app.get('/api/knowledge/pending', (req, res) => {
  try {
    const { execFile } = require('child_process');
    execFile(getPythonBin(), ['-m', 'kanban_framework', 'knowledge', 'pending', '--json'], {
      cwd: KANBAN_ROOT, timeout: 10000,
    }, (err, stdout) => {
      if (err) return res.json({ success: false, error: err.message });
      try { res.json(JSON.parse(stdout)); } catch (_) { res.json({ success: false }); }
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to list pending knowledge' });
  }
});

// --- API: approve knowledge entries ---
app.post('/api/knowledge/approve', (req, res) => {
  try {
    const ids = req.body.ids || [];
    if (!ids.length) return res.status(400).json({ error: 'ids required' });
    const { execFile } = require('child_process');
    const args = ['-m', 'kanban_framework', 'knowledge', 'approve', '--json', ...ids];
    execFile(getPythonBin(), args, { cwd: KANBAN_ROOT, timeout: 10000 }, (err, stdout) => {
      if (err) return res.json({ success: false, error: err.message });
      try { res.json(JSON.parse(stdout)); } catch (_) { res.json({ success: false }); }
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to approve knowledge' });
  }
});

// --- API: reject knowledge entries ---
app.post('/api/knowledge/reject', (req, res) => {
  try {
    const ids = req.body.ids || [];
    if (!ids.length) return res.status(400).json({ error: 'ids required' });
    const { execFile } = require('child_process');
    const args = ['-m', 'kanban_framework', 'knowledge', 'reject', '--json', ...ids];
    execFile(getPythonBin(), args, { cwd: KANBAN_ROOT, timeout: 10000 }, (err, stdout) => {
      if (err) return res.json({ success: false, error: err.message });
      try { res.json(JSON.parse(stdout)); } catch (_) { res.json({ success: false }); }
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to reject knowledge' });
  }
});

// --- API: list all tasks ---
app.get('/api/tasks', (req, res) => {
  try {
    const tasksDir = path.join(KANBAN_ROOT, 'tasks');
    if (!fs.existsSync(tasksDir)) {
      return res.json([]);
    }

    const tasks = [];

    // Scan new layout: tasks/TASK-NNN/task.json (subdirectories)
    const entries = fs.readdirSync(tasksDir, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const taskJsonPath = path.join(tasksDir, entry.name, 'task.json');
      if (!fs.existsSync(taskJsonPath)) continue;
      try {
        const data = JSON.parse(fs.readFileSync(taskJsonPath, 'utf-8'));
        tasks.push({
          id: data.id || entry.name,
          title: data.title,
          description: data.description,
          status: data.status,
          phase: data.phase,
          iteration: data.iteration,
          scores: data.scores,
          assignee: data.assignee,
          created_at: data.created_at,
          updated_at: data.updated_at
        });
      } catch (_) { /* skip malformed */ }
    }

    // Scan old layout: tasks/TASK-NNN.json (flat files)
    const files = fs.readdirSync(tasksDir).filter(f => f.endsWith('.json'));
    for (const f of files) {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(tasksDir, f), 'utf-8'));
        const id = data.id || f.replace('.json', '');
        // Avoid duplicates if both formats exist for same task
        if (!tasks.some(t => t.id === id)) {
          tasks.push({
            id,
            title: data.title,
            description: data.description,
            status: data.status,
            phase: data.phase,
            iteration: data.iteration,
            scores: data.scores,
            assignee: data.assignee,
            created_at: data.created_at,
            updated_at: data.updated_at
          });
        }
      } catch (_) { /* skip malformed */ }
    }

    res.json(tasks);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read tasks' });
  }
});

// --- API: single task detail ---
app.get('/api/tasks/:id', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }
    const tasksDir = path.join(KANBAN_ROOT, 'tasks');
    const data = readTaskJson(tasksDir, `${taskId}.json`);
    if (!data) {
      return res.status(404).json({ error: 'Task not found' });
    }
    if (!data.id) data.id = taskId;

    const reports = collectReports(tasksDir, taskId, data);

    res.json({ ...data, reports });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read task' });
  }
});

// --- API: list archived tasks (read-only) ---
app.get('/api/archive', (req, res) => {
  try {
    res.json(readArchivedTasks());
  } catch (err) {
    res.status(500).json({ error: 'Failed to read archived tasks' });
  }
});

// --- API: single archived task detail ---
app.get('/api/archive/:id', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }

    const data = readArchivedTask(taskId);
    if (!data) {
      return res.status(404).json({ error: 'Archived task not found' });
    }
    if (!data.id) data.id = taskId;

    const archiveDir = path.join(KANBAN_ROOT, 'archive');
    const reports = collectReports(archiveDir, taskId, data);

    res.json({ ...data, reports });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read archived task' });
  }
});

// --- API: list all archived tasks (summary format, same as /api/tasks) ---
app.get('/api/archived-tasks', (req, res) => {
  try {
    res.json(readArchivedTasks());
  } catch (err) {
    res.status(500).json({ error: 'Failed to read archived tasks' });
  }
});

// --- API: single archived task detail (same format as /api/tasks/:id) ---
app.get('/api/archived-tasks/:id', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }

    const data = readArchivedTask(taskId);
    if (!data) {
      return res.status(404).json({ error: 'Archived task not found' });
    }
    if (!data.id) data.id = taskId;

    const archiveDir = path.join(KANBAN_ROOT, 'archive');
    const reports = collectReports(archiveDir, taskId, data);

    res.json({ ...data, reports });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read archived task' });
  }
});

/**
 * Read the latest retrospective.md for a given task from its parent directory.
 * Scans iteration-N/ subdirectories and returns the content of the latest one found.
 *
 * @param {string} parentDir - Parent directory containing the task subdirectory (e.g. tasks/ or archive/)
 * @param {string} taskId    - The task ID (e.g. TASK-001)
 * @returns {{ iteration: number, content: string }|null} Latest retrospective or null
 */
function readRetrospective(parentDir, taskId) {
  const taskSubdir = path.join(parentDir, taskId);
  if (!fs.existsSync(taskSubdir)) {
    return null;
  }

  // Find the latest iteration with a retrospective.md
  const iterEntries = fs.readdirSync(taskSubdir, { withFileTypes: true });
  let latestRetrospective = null;
  let latestIter = 0;

  for (const entry of iterEntries) {
    if (!entry.isDirectory() || !entry.name.startsWith('iteration-')) continue;
    const retroPath = path.join(taskSubdir, entry.name, 'retrospective.md');
    if (fs.existsSync(retroPath)) {
      const iterNum = parseInt(entry.name.replace('iteration-', ''), 10);
      if (iterNum > latestIter) {
        latestIter = iterNum;
        latestRetrospective = fs.readFileSync(retroPath, 'utf-8');
      }
    }
  }

  if (!latestRetrospective) {
    return null;
  }

  return { iteration: latestIter, content: latestRetrospective };
}

// --- API: retrospective for an archived task ---
app.get('/api/archived-tasks/:id/retrospective', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }

    const archiveDir = path.join(KANBAN_ROOT, 'archive');
    const result = readRetrospective(archiveDir, taskId);
    if (!result) {
      return res.status(404).json({ error: 'No retrospective found for this task' });
    }

    res.json({
      task_id: taskId,
      iteration: result.iteration,
      content: result.content
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read retrospective' });
  }
});

// --- API: retrospective for an active task ---
app.get('/api/tasks/:id/retrospective', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }

    const tasksDir = path.join(KANBAN_ROOT, 'tasks');
    const result = readRetrospective(tasksDir, taskId);
    if (!result) {
      return res.status(404).json({ error: 'No retrospective found for this task' });
    }

    res.json({
      task_id: taskId,
      iteration: result.iteration,
      content: result.content
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read retrospective' });
  }
});

// --- API: token tracking stats via pluggable StatsBackend (#213, #222) ---
app.get('/api/token-stats', (req, res) => {
  try {
    const { execSync } = require('child_process');
    const pythonBin = getPythonBin();
    // Delegate to Python stats backend (NativeBackend or CodeBurnBackend via config)
    const cmd = `${pythonBin} -m kanban_framework stats --json`;
    try {
      const result = execSync(cmd, {
        timeout: 15000, encoding: 'utf-8',
        cwd: PROJECT_ROOT,
        env: { ...process.env, KANBAN_ROOT: KANBAN_ROOT },
        stdio: ['pipe', 'pipe', 'pipe']
      });
      const parsed = JSON.parse(result);
      // Unwrap CLI response format {success, data} → extract inner data
      const stats = (parsed && parsed.data) ? parsed.data : parsed;
      res.json({ success: true, data: stats });
    } catch (pyErr) {
      // Fallback to in-process JSONL read if Python unavailable
      try {
        const jsonlStats = readJSONLStats(30);
        res.json({ success: true, data: jsonlStats });
      } catch (e) {
        res.json({ success: true, data: { total_tokens: 0, source: 'fallback', error: 'No stats available' } });
      }
    }
  } catch (err) {
    res.json({ success: false, error: err.message });
  }
});

// --- API: step progress for a task (#214) ---
app.get('/api/tasks/:id/steps', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) {
      return res.status(400).json({ error: 'Invalid task ID format' });
    }
    let progressFile = path.join(KANBAN_ROOT, 'tasks', taskId, 'progress.json');
    let taskFile = path.join(KANBAN_ROOT, 'tasks', taskId, 'task.json');
    // Also check archive/
    if (!fs.existsSync(progressFile)) {
      progressFile = path.join(KANBAN_ROOT, 'archive', taskId, 'progress.json');
      taskFile = path.join(KANBAN_ROOT, 'archive', taskId, 'task.json');
    }
    if (!fs.existsSync(progressFile)) {
      return res.json({ success: true, data: { steps: {}, phase: null } });
    }
    const progress = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
    const task = fs.existsSync(taskFile) ? JSON.parse(fs.readFileSync(taskFile, 'utf-8')) : {};
    const steps = {};
    for (const [stepId, stepInfo] of Object.entries(progress.steps || {})) {
      const def = STEP_DEFINITIONS[stepId] || {};
      steps[stepId] = {
        status: stepInfo.status || 'pending',
        completed_at: stepInfo.completed_at || null,
        phase: stepId.split('.')[0],
        description: def.description || stepId,
        agent_type: def.agent_type || null,
      };
    }
    res.json({ success: true, data: {
      steps, phase: task.phase, total: Object.keys(steps).length,
      schema: { stepId: { status: 'pending|completed', description: '...', agent_type: 'kanban-planner|kanban-executor|...', phase: 'plan|execute|...' } }
    }});
  } catch (err) {
    res.json({ success: false, error: err.message });
  }
});

// --- API: comprehensive task stats (tokens + time + steps) ---
app.get('/api/tasks/:id/stats', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) return res.status(400).json({ error: 'Invalid task ID' });

    // Check tasks/ first, then archive/
    let taskDir = path.join(KANBAN_ROOT, 'tasks', taskId);
    const archiveDir = path.join(KANBAN_ROOT, 'archive', taskId);
    const isArchived = !fs.existsSync(path.join(taskDir, 'task.json')) && fs.existsSync(path.join(archiveDir, 'task.json'));
    if (isArchived) {
      taskDir = archiveDir;
    }

    // Token tracking — delegate to StatsBackend (Python), consistent with global stats
    let tokens = { total_tokens: 0, phases: {}, agents: {}, models: {}, total_prompts: 0, prompt_count: {}, phase_duration: {} };
    try {
      const pythonBin = getPythonBin();
      const cmd = `${pythonBin} -m kanban_framework stats --task ${taskId} --json`;
      const result = execSync(cmd, {
        timeout: 15000, encoding: 'utf-8',
        cwd: PROJECT_ROOT,
        env: { ...process.env, KANBAN_ROOT: KANBAN_ROOT },
        stdio: ['pipe', 'pipe', 'pipe']
      });
      const parsed = JSON.parse(result);
      const pt = (parsed && parsed.data) ? parsed.data : parsed;
      tokens.total_tokens = pt.total_tokens || 0;
      tokens.phases = pt.phases || {};
      tokens.agents = pt.agents || {};
      tokens.models = pt.models || {};
      tokens.total_prompts = pt.total_prompts || 0;
      tokens.prompt_count = pt.prompt_count || {};
      tokens.phase_duration = pt.phase_duration || {};
      tokens.phase_api_calls = pt.phase_api_calls || {};
      tokens.step_api_calls = pt.step_api_calls || {};
      tokens.real_api_calls = pt.real_api_calls || 0;
      tokens._source = pt.source || 'stats_backend';
      if (pt.note) tokens._note = pt.note;
    } catch (pyErr) {
      // Fallback to local JSON read if Python unavailable
      const tokenFiles = [
        path.join(taskDir, 'token_tracking.json'),
        path.join(KANBAN_ROOT, 'reports', 'token_tracking.json'),
      ];
      for (const tf of tokenFiles) {
        if (fs.existsSync(tf)) {
          const td = JSON.parse(fs.readFileSync(tf, 'utf-8'));
          const entry = td[taskId] || td;
          if (entry.total_tokens > 0 || Object.keys(entry.by_phase || {}).length > 0) {
            tokens.total_tokens = entry.total_tokens || 0;
            tokens.phases = entry.by_phase || {};
            tokens.agents = entry.agent_totals || {};
            tokens.models = entry.by_model || {};
            tokens.total_prompts = entry.total_prompts || 0;
            tokens.prompt_count = entry.prompt_count || {};
            tokens.phase_duration = entry.phase_duration || {};
            tokens._entry = { sessions: entry.sessions || [], sessionPhases: entry.session_phases || {}, sessionSteps: entry.session_steps || {} };
            break;
          }
        }
      }
    }
    // Load task.json for history timestamps
    let task = {};
    try {
      const taskJsonPath = path.join(taskDir, 'task.json');
      if (fs.existsSync(taskJsonPath)) {
        task = JSON.parse(fs.readFileSync(taskJsonPath, 'utf-8'));
      }
    } catch (_) {}

    // Per-task API call count: each subagent session is fully dedicated
    // to a single task step. Count ALL entries in subagent JSONL files.
    //
    // kanban track --session <subagent_id> --step <step_id> records
    // subagent→step mapping in session_steps.
    // Falls back to session_phases for phase-level granularity.
    try {
      const sessionSteps = tokens._entry?.sessionSteps || {};
      const sessionPhases = tokens._entry?.sessionPhases || {};
      tokens.phase_api_calls = {};
      tokens.step_api_calls = {};
      let totalApiCalls = 0;
      // Per-step (preferred, more precise)
      for (const [step, sids] of Object.entries(sessionSteps)) {
        let stepTotal = 0;
        for (const sid of sids) {
          stepTotal += countSubagentEntries(sid);
        }
        tokens.step_api_calls[step] = stepTotal;
        totalApiCalls += stepTotal;
      }
      // Per-phase (fallback / aggregate)
      for (const [ph, sids] of Object.entries(sessionPhases)) {
        let phaseTotal = 0;
        for (const sid of sids) {
          phaseTotal += countSubagentEntries(sid);
        }
        tokens.phase_api_calls[ph] = phaseTotal;
      }
      tokens.real_api_calls = totalApiCalls;
    } catch (e) { /* keep prompt_count as fallback */ }

    // No token_tracking data — estimate from JSONL time window
    if (tokens.total_tokens === 0 && Object.keys(tokens.phases).length === 0) {
      tokens._source = 'jsonl_estimate';
      try {
        const taskHistory = task.history || [];
        if (taskHistory.length > 0) {
          // Get time window from history
          const ts = [];
          for (const h of taskHistory) {
            for (const k of ['started_at', 'completed_at']) {
              const v = h[k];
              if (!v) continue;
              const t = typeof v === 'number' ? v : new Date(v).getTime() / 1000;
              if (t > 0) ts.push(t);
            }
          }
          if (ts.length > 0) {
            const tMin = Math.min(...ts) - 60;
            const tMax = Math.max(...ts) + 60;
            // Use cached JSONL index (fast, built once)
            const idx = getJSONLIndex();
            const _count = (a, b) => { let n = 0; for (const t of idx.timestamps) { if (t >= a && t <= b) n++; } return n; };
            const _findLastTimestamp = (a, b) => { let last = 0; for (const t of idx.timestamps) { if (t >= a && t <= b && t > last) last = t; } return last; };
            tokens.real_api_calls = _count(tMin, tMax);
            if (tokens.real_api_calls > 0) {
              tokens.total_tokens = Math.round(tokens.real_api_calls * 800);
              tokens._note = `Estimated from ${tokens.real_api_calls} JSONL calls in task window`;
            }
            tokens.phase_api_calls = {};
            const phaseWindows = {};
            for (const h of taskHistory) {
              const ph = h.phase;
              if (!ph) continue;
              phaseWindows[ph] = phaseWindows[ph] || { min: Infinity, max: -Infinity };
              for (const key of ['started_at', 'completed_at']) {
                const v = h[key];
                if (!v) continue;
                const ts = typeof v === 'number' ? v : new Date(v).getTime() / 1000;
                if (!(ts > 0)) continue;
                if (ts < phaseWindows[ph].min) phaseWindows[ph].min = ts;
                if (ts > phaseWindows[ph].max) phaseWindows[ph].max = ts;
              }
            }
            // Build ordered timeline from completed_at timestamps for duration inference
            const completedAt = {};
            for (const h of taskHistory) {
              const ph = h.phase;
              if (!ph) continue;
              const v = h.completed_at;
              if (v) {
                const ts = typeof v === 'number' ? v : new Date(v).getTime() / 1000;
                if (ts > 0) completedAt[ph] = ts;
              }
            }
            const sortedPhases = Object.entries(completedAt).sort((a, b) => a[1] - b[1]);
            // For phases with min==max (only one timestamp), infer duration from adjacent phases
            for (let i = 0; i < sortedPhases.length; i++) {
              const [ph, endTime] = sortedPhases[i];
              const w = phaseWindows[ph];
              if (!w) continue;
              if (w.max - w.min < 1 && i > 0) {
                // Only has completed_at, infer start from previous phase end
                const prevEnd = sortedPhases[i - 1][1];
                w.min = prevEnd;
              }
            }
            // For phases still with min==max, use JSONL last entry as fallback
            for (const [ph, w] of Object.entries(phaseWindows)) {
              if (w.min < Infinity && w.max - w.min < 1) {
                const lastTs = _findLastTimestamp(w.min - 60, w.min + 3600);
                if (lastTs > w.min) w.max = lastTs;
              }
            }
            for (const [ph, w] of Object.entries(phaseWindows)) {
              if (w.min < Infinity) {
                const pc = _count(w.min - 60, w.max + 60);
                tokens.phase_api_calls[ph] = pc;
                tokens.phases[ph] = Math.round(pc * 800);
                tokens.phase_duration[ph] = Math.round(w.max - w.min);
              }
            }
            tokens.step_api_calls = {};
            try {
              const progressFile = path.join(taskDir, 'progress.json');
              if (fs.existsSync(progressFile)) {
                const progress = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
                for (const [sid, si] of Object.entries(progress.steps || {})) {
                  if (si.status !== 'completed' || !si.updated_at) continue;
                  const t = typeof si.updated_at === 'number' ? si.updated_at : new Date(si.updated_at).getTime() / 1000;
                  if (t > 0) tokens.step_api_calls[sid] = _count(t - 300, t + 10);
                }
              }
            } catch (_) {}
          }
        }
      } catch (_) {}
    }

    // Step-level token attribution: match progress.json timestamps against JSONL turns
    let stepTokens = {};
    try {
      stepTokens = attributeStepTokens(taskDir, taskId);
    } catch (e) { /* use empty */ }

    // Time tracking — check per-task first, then global reports
    let timing = { phases: {}, agents: {}, total_seconds: 0 };
    const timeFiles = [
      path.join(taskDir, 'time_tracking.json'),
      path.join(KANBAN_ROOT, 'reports', 'time_tracking.json'),
    ];
    for (const tf of timeFiles) {
      if (fs.existsSync(tf)) {
        const td = JSON.parse(fs.readFileSync(tf, 'utf-8'));
        const entry = td[taskId] || td;
        if (Object.keys(entry.phases || {}).length > 0 || Object.keys(entry.agents || {}).length > 0) {
          timing.phases = entry.phases || {};
          timing.agents = entry.agents || {};
          timing.total_seconds = 0;
          for (const [ph, pdata] of Object.entries(timing.phases)) {
            if (pdata.elapsed_seconds) timing.total_seconds += pdata.elapsed_seconds;
          }
          for (const [ag, adata] of Object.entries(timing.agents)) {
            if (adata.total_seconds) timing.total_seconds += adata.total_seconds;
          }
          break;
        }
      }
    }

    // Step progress
    let steps = {};
    const progressFile = path.join(taskDir, 'progress.json');
    if (fs.existsSync(progressFile)) {
      const prog = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
      steps = prog.steps || {};
    }

    // Subtask status
    let subtasks = [];
    const breakdownFile = path.join(taskDir, 'task_breakdown.json');
    if (fs.existsSync(breakdownFile)) {
      const bd = JSON.parse(fs.readFileSync(breakdownFile, 'utf-8'));
      subtasks = (bd.subtasks || []).map(s => ({
        id: s.id, title: s.title, status: s.status || 'pending',
        owner: s.owner || 'unassigned', blocking: s.blocking || false,
      }));
    }

    // Count prompt calls from step completions
    let totalPromptCalls = 0;
    for (const [sid, si] of Object.entries(steps)) {
      if (si.status === 'completed') totalPromptCalls++;
    }

    res.json({ success: true, data: {
      tokens, timing, steps, subtasks, totalPromptCalls, stepTokens,
      phase: JSON.parse(fs.readFileSync(path.join(taskDir, 'task.json'), 'utf-8')).phase,
    }});
  } catch (err) {
    res.json({ success: false, error: err.message });
  }
});

// ============================================================
// JSONL reader — native Node.js, no Python dependency
// ============================================================

function findSessionDir() {
  const home = require('os').homedir();
  const projectsDir = path.join(home, '.claude', 'projects');
  if (!fs.existsSync(projectsDir)) return null;

  const cwd = PROJECT_ROOT || process.cwd();
  const leaf = path.basename(cwd);

  // Search for matching project directory with JSONL files
  const dirs = fs.readdirSync(projectsDir, { withFileTypes: true });
  for (const d of dirs) {
    if (!d.isDirectory()) continue;
    // Match by leaf name (hyphens/underscores normalized), or by containing key path parts
    const normalized = d.name.replace(/-/g, '_');
    const leafNorm = leaf.replace(/-/g, '_');
    if (normalized.includes(leafNorm)) {
      const files = fs.readdirSync(path.join(projectsDir, d.name)).filter(f => f.endsWith('.jsonl'));
      if (files.length > 0) return path.join(projectsDir, d.name);
    }
  }
  // Fallback: match by broader path fragment
  for (const d of dirs) {
    if (!d.isDirectory()) continue;
    if (d.name.includes('important') && d.name.includes('demo') && !d.name.includes('worktree') && !d.name.includes('ds')) {
      const files = fs.readdirSync(path.join(projectsDir, d.name)).filter(f => f.endsWith('.jsonl'));
      if (files.length > 0) return path.join(projectsDir, d.name);
    }
  }
  return null;
}

function countSubagentEntries(subagentId) {
  // Count ALL entries in a subagent JSONL file. Subagent sessions
  // are fully dedicated to one task phase — no time window needed.
  const sessionDir = findSessionDir();
  if (!sessionDir || !subagentId) return 0;
  try {
    const dirEntries = fs.readdirSync(sessionDir, { withFileTypes: true });
    for (const entry of dirEntries) {
      if (!entry.isDirectory()) continue;
      const subDir = path.join(sessionDir, entry.name, 'subagents');
      if (!fs.existsSync(subDir)) continue;
      const targetFile = path.join(subDir, subagentId + '.jsonl');
      if (fs.existsSync(targetFile)) {
        const content = fs.readFileSync(targetFile, 'utf-8');
        return content.split(/\r?\n/).filter(l => l.trim()).length;
      }
    }
  } catch (_) {}
  return 0;
}

function countLLMCallsInWindow(tMin, tMax, sessionIds) {
  // Deprecated: use countSubagentEntries for per-task precision.
  // Kept for backward compatibility with tasks that have no session IDs.
  const sessionDir = findSessionDir();
  if (!sessionDir || !tMin || !tMax) return 0;
  let count = 0;
  try {
    for (const f of fs.readdirSync(sessionDir).filter(f => f.endsWith('.jsonl'))) {
      try {
        const content = fs.readFileSync(path.join(sessionDir, f), 'utf-8');
        for (const line of content.split(/\r?\n/)) {
          if (!line.trim()) continue;
          try {
            const e = JSON.parse(line);
            const ts = e.timestamp;
            if (!ts) continue;
            const t = typeof ts === 'number' ? ts : new Date(ts).getTime() / 1000;
            if (t >= tMin && t <= tMax) count++;
          } catch (_) {}
        }
      } catch (_) {}
    }
  } catch (_) {}
  return count;
}

function readJSONLStats(days) {
  const sessionDir = findSessionDir();
  if (!sessionDir) return { total_tokens: 0, sessions: 0, total_turns: 0 };

  const cutoff = Date.now() - days * 86400000;
  let totalInput = 0, totalOutput = 0, totalTurns = 0, sessions = 0;
  const toolCounts = {};
  const models = new Set();

  const files = fs.readdirSync(sessionDir).filter(f => f.endsWith('.jsonl'));
  for (const file of files) {
    const filepath = path.join(sessionDir, file);
    const stat = fs.statSync(filepath);
    if (stat.mtimeMs < cutoff) continue;

    sessions++;
    const content = fs.readFileSync(filepath, 'utf-8');
    const lines = content.split(/\r?\n/);

    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const d = JSON.parse(line);
        const msg = d.message;
        if (!msg || !msg.usage) continue;

        const u = msg.usage;
        totalInput += u.input_tokens || 0;
        totalOutput += u.output_tokens || 0;
        totalTurns++;

        // Extract tool usage
        const content = msg.content;
        if (Array.isArray(content)) {
          for (const block of content) {
            if (block.type === 'tool_use' && block.name) {
              toolCounts[block.name] = (toolCounts[block.name] || 0) + 1;
            }
          }
        }
        if (d.model) models.add(d.model);
      } catch (e) { /* skip malformed lines */ }
    }
  }

  // Sort tools by count
  const sortedTools = Object.entries(toolCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .reduce((acc, [k, v]) => { acc[k] = v; return acc; }, {});

  return {
    total_tokens: totalInput + totalOutput,
    total_input: totalInput,
    total_output: totalOutput,
    total_turns: totalTurns,
    sessions: sessions,
    tool_counts: sortedTools,
    models: Array.from(models),
  };
}

// Attribute JSONL tokens to individual steps based on progress.json timestamps
function attributeStepTokens(taskDir, taskId) {
  const progressFile = path.join(taskDir, 'progress.json');
  if (!fs.existsSync(progressFile)) return {};

  const progress = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
  const steps = progress.steps || {};
  if (Object.keys(steps).length === 0) return {};

  // Collect all JSONL turns with timestamps and token counts
  const sessionDir = findSessionDir();
  if (!sessionDir) return {};

  const turns = [];
  const files = fs.readdirSync(sessionDir).filter(f => f.endsWith('.jsonl'));
  for (const file of files) {
    const content = fs.readFileSync(path.join(sessionDir, file), 'utf-8');
    for (const line of content.split(/\r?\n/)) {
      if (!line.trim()) continue;
      try {
        const d = JSON.parse(line);
        const msg = d.message;
        if (!msg || !msg.usage) continue;
        const ts = d.timestamp ? new Date(d.timestamp).getTime() / 1000 : 0;
        if (!ts) continue;
        turns.push({
          ts: ts,
          tokens: (msg.usage.input_tokens || 0) + (msg.usage.output_tokens || 0),
        });
      } catch (e) {}
    }
  }
  if (turns.length === 0) return {};

  turns.sort((a, b) => a.ts - b.ts);

  // Build step time boundaries from progress.json
  const boundaries = [];
  let prevTs = turns[0].ts;
  const sortedSteps = Object.entries(steps)
    .filter(([, v]) => v.updated_at)
    .sort((a, b) => (a[1].updated_at || 0) - (b[1].updated_at || 0));

  for (const [sid, info] of sortedSteps) {
    boundaries.push({ sid, start: prevTs, end: info.updated_at });
    prevTs = info.updated_at;
  }

  // Attribute tokens
  const result = {};
  for (const b of boundaries) {
    let tokens = 0;
    for (const t of turns) {
      if (t.ts >= b.start && t.ts < b.end) tokens += t.tokens;
    }
    if (tokens > 0) result[b.sid] = tokens;
  }
  return result;
}

// ============================================================
// Write API: task editing
// ============================================================

function saveTask(taskId, data) {
  const taskFile = path.join(KANBAN_ROOT, 'tasks', taskId, 'task.json');
  if (!fs.existsSync(taskFile)) return false;
  fs.writeFileSync(taskFile, JSON.stringify(data, null, 2), 'utf-8');
  return true;
}

// POST /api/tasks/:id/phase — transition phase
app.post('/api/tasks/:id/phase', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) return res.status(400).json({ error: 'Invalid task ID' });
    const { phase } = req.body;
    if (!phase) return res.status(400).json({ error: 'phase required' });

    const taskFile = path.join(KANBAN_ROOT, 'tasks', taskId, 'task.json');
    const task = JSON.parse(fs.readFileSync(taskFile, 'utf-8'));
    task.phase = phase;
    fs.writeFileSync(taskFile, JSON.stringify(task, null, 2), 'utf-8');
    res.json({ success: true, data: { phase } });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// PUT /api/tasks/:id — update task properties
app.put('/api/tasks/:id', (req, res) => {
  try {
    const taskId = req.params.id;
    if (!isValidTaskId(taskId)) return res.status(400).json({ error: 'Invalid task ID' });
    const { title, description, mode, control_mode, lightweight } = req.body;

    const taskFile = path.join(KANBAN_ROOT, 'tasks', taskId, 'task.json');
    const task = JSON.parse(fs.readFileSync(taskFile, 'utf-8'));
    if (title !== undefined) task.title = title;
    if (description !== undefined) task.description = description;
    if (mode !== undefined) task.mode = mode;
    if (control_mode !== undefined) task.control_mode = control_mode;
    if (lightweight !== undefined) task.lightweight = lightweight;
    fs.writeFileSync(taskFile, JSON.stringify(task, null, 2), 'utf-8');
    res.json({ success: true, data: task });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// PUT /api/tasks/:id/subtask/:stId — update subtask
app.put('/api/tasks/:id/subtask/:stId', (req, res) => {
  try {
    const { id, stId } = req.params;
    if (!isValidTaskId(id)) return res.status(400).json({ error: 'Invalid task ID' });
    const { status, owner } = req.body;

    const breakdownFile = path.join(KANBAN_ROOT, 'tasks', id, 'task_breakdown.json');
    if (!fs.existsSync(breakdownFile)) {
      return res.status(404).json({ error: 'task_breakdown.json not found' });
    }
    const breakdown = JSON.parse(fs.readFileSync(breakdownFile, 'utf-8'));
    const subtask = (breakdown.subtasks || []).find(s => s.id === stId);
    if (!subtask) return res.status(404).json({ error: 'subtask not found' });

    if (status !== undefined) subtask.status = status;
    if (owner !== undefined) subtask.owner = owner;
    fs.writeFileSync(breakdownFile, JSON.stringify(breakdown, null, 2), 'utf-8');
    res.json({ success: true, data: subtask });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/tasks/:id/step/:stepId — mark step complete/in_progress
app.post('/api/tasks/:id/step/:stepId', (req, res) => {
  try {
    const { id, stepId } = req.params;
    if (!isValidTaskId(id)) return res.status(400).json({ error: 'Invalid task ID' });
    const { status: newStatus } = req.body;
    if (!newStatus) return res.status(400).json({ error: 'status required' });

    const progressFile = path.join(KANBAN_ROOT, 'tasks', id, 'progress.json');
    let progress = { steps: {} };
    if (fs.existsSync(progressFile)) {
      progress = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
    }
    progress.steps[stepId] = { status: newStatus, completed_at: newStatus === 'completed' ? new Date().toISOString() : null };
    fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2), 'utf-8');
    res.json({ success: true, data: { stepId, status: newStatus } });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// ============================================================
// Start server
// ============================================================
const server = app.listen(PORT, HOST, () => {
  setupWatchers();
  console.log(`Dashboard running at http://${HOST}:${PORT}`);
  console.log(`SSE endpoint available at http://${HOST}:${PORT}/api/events`);
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`ERROR: Port ${PORT} is already in use by another process.`);
    console.error('Another dashboard may be running. Stop it first or use --port to specify a different port.');
    process.exit(1);
  } else {
    throw err;
  }
});
