/**
 * Real-time refresh tests for Dashboard server.
 * Tests SSE granular events (task_created, task_updated, task_archived),
 * archive endpoint, and new-layout directory support.
 *
 * Uses Node.js native http module -- no test framework required.
 *
 * Run: node tests/realtime.test.js
 */

const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = 3201; // Unique port to avoid conflicts with other test files
const BASE = `http://localhost:${PORT}`;

// Path resolution mirrors server.js exactly:
//   server.js uses __dirname = dashboard/ directory
//   KANBAN_ROOT = path.resolve(__dirname, '..')
//   PROJECT_ROOT = path.resolve(__dirname, '../..')
// We compute the same paths here so that file writes go where the server reads.
const SERVER_DIR = path.resolve(__dirname, '..'); // dashboard/
const KANBAN_ROOT = path.resolve(SERVER_DIR, '..'); // parent of dashboard/
const PROJECT_ROOT = path.resolve(SERVER_DIR, '..', '..');

// API endpoints use PROJECT_ROOT/.kanban/tasks which equals KANBAN_ROOT/tasks
// when deployed (dashboard/ is under .kanban/). In the worktree, dashboard/ is
// under .claude/skills/kanban/ so the paths differ. We write to both locations
// to cover both the watcher (KANBAN_ROOT) and the API (PROJECT_ROOT/.kanban/tasks).
const TASKS_DIR_WATCHER = path.join(KANBAN_ROOT, 'tasks');
const TASKS_DIR_API = path.join(PROJECT_ROOT, '.kanban', 'tasks');
const ARCHIVE_DIR_WATCHER = path.join(KANBAN_ROOT, 'archive');
const ARCHIVE_DIR_API = path.join(PROJECT_ROOT, '.kanban', 'archive');

// ---------- helpers ----------

let passed = 0;
let failed = 0;
let serverProcess = null;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  PASS: ${label}`);
  } else {
    failed++;
    console.log(`  FAIL: ${label}`);
  }
}

// ---------- setup / teardown ----------

function waitForPort(port, timeoutMs) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function tryConnect() {
      const req = http.request(`http://localhost:${port}/api/config`, { method: 'GET' }, (res) => {
        res.resume();
        resolve();
      });
      req.on('error', () => {
        if (Date.now() - start > timeoutMs) {
          reject(new Error(`Server did not start within ${timeoutMs}ms`));
        } else {
          setTimeout(tryConnect, 200);
        }
      });
      req.end();
    }
    tryConnect();
  });
}

async function startServer() {
  return new Promise((resolve, reject) => {
    serverProcess = spawn('node', ['server.js'], {
      cwd: path.join(__dirname, '..'),
      env: { ...process.env, PORT: String(PORT) },
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    serverProcess.on('error', (err) => {
      reject(err);
    });

    waitForPort(PORT, 10000).then(resolve, reject);
  });
}

function stopServer() {
  if (serverProcess) {
    serverProcess.kill('SIGTERM');
    serverProcess = null;
  }
}

function get(urlPath) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, BASE);
    const req = http.request(url, { method: 'GET' }, (res) => {
      let body = '';
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        let parsed = null;
        try { parsed = JSON.parse(body); } catch (_) { /* not json */ }
        resolve({ status: res.statusCode, headers: res.headers, body, json: parsed });
      });
    });
    req.on('error', reject);
    req.end();
  });
}

/**
 * Parse a single SSE message block into { event, data, comment }.
 */
function parseSSE(raw) {
  const lines = raw.split('\n');
  let eventType = null;
  let data = null;
  let comment = null;

  for (const line of lines) {
    if (line.startsWith(': ')) {
      comment = line.substring(2);
    } else if (line.startsWith('event: ')) {
      eventType = line.substring(7).trim();
    } else if (line.startsWith('data: ')) {
      const rawStr = line.substring(6);
      try { data = JSON.parse(rawStr); } catch (_) { data = rawStr; }
    }
  }

  if (eventType || data !== null || comment !== null) {
    return { event: eventType, data, comment };
  }
  return null;
}

/**
 * Connect to SSE and collect events for a specified duration.
 */
function collectEvents(durationMs) {
  return new Promise((resolve, reject) => {
    const url = new URL('/api/events', BASE);
    const req = http.request(url, { method: 'GET' }, (res) => {
      const events = [];
      let buffer = '';

      res.on('data', (chunk) => {
        buffer += chunk.toString();
        const parts = buffer.split('\n\n');
        buffer = parts.pop() || '';
        for (const part of parts) {
          if (part.trim().length === 0) continue;
          const parsed = parseSSE(part);
          if (parsed) events.push(parsed);
        }
      });

      setTimeout(() => {
        if (buffer.trim().length > 0) {
          const parsed = parseSSE(buffer);
          if (parsed) events.push(parsed);
        }
        res.destroy();
        resolve(events);
      }, durationMs);
    });

    req.on('error', reject);
    req.end();
  });
}

/**
 * Wait for a specific SSE event type matching a filter, with timeout.
 */
function waitForEvent(durationMs, filterFn) {
  return new Promise((resolve, reject) => {
    const url = new URL('/api/events', BASE);
    const req = http.request(url, { method: 'GET' }, (res) => {
      let buffer = '';

      res.on('data', (chunk) => {
        buffer += chunk.toString();
        const parts = buffer.split('\n\n');
        buffer = parts.pop() || '';
        for (const part of parts) {
          if (part.trim().length === 0) continue;
          const parsed = parseSSE(part);
          if (parsed && filterFn(parsed)) {
            res.destroy();
            resolve(parsed);
            return;
          }
        }
      });

      setTimeout(() => {
        res.destroy();
        resolve(null);
      }, durationMs);
    });

    req.on('error', reject);
    req.end();
  });
}

// ---------- test utilities ----------

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function cleanupDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

/**
 * Write a file to both the watcher path and the API path.
 * This ensures the file watcher detects the change AND the API can read it,
 * regardless of where server.js is deployed.
 */
function writeTaskFile(taskId, data) {
  const content = JSON.stringify(data, null, 2);
  for (const base of [TASKS_DIR_WATCHER, TASKS_DIR_API]) {
    const taskDir = path.join(base, taskId);
    ensureDir(taskDir);
    fs.writeFileSync(path.join(taskDir, 'task.json'), content);
  }
}

function removeTaskDir(taskId) {
  for (const base of [TASKS_DIR_WATCHER, TASKS_DIR_API]) {
    const taskDir = path.join(base, taskId);
    cleanupDir(taskDir);
  }
}

function writeArchiveFile(taskId, data) {
  const content = JSON.stringify(data, null, 2);
  for (const base of [ARCHIVE_DIR_WATCHER, ARCHIVE_DIR_API]) {
    const taskDir = path.join(base, taskId);
    ensureDir(taskDir);
    fs.writeFileSync(path.join(taskDir, 'task.json'), content);
  }
}

function removeArchiveDir(taskId) {
  for (const base of [ARCHIVE_DIR_WATCHER, ARCHIVE_DIR_API]) {
    const taskDir = path.join(base, taskId);
    cleanupDir(taskDir);
  }
}

function cleanupArchiveBase() {
  for (const base of [ARCHIVE_DIR_WATCHER, ARCHIVE_DIR_API]) {
    try {
      if (fs.existsSync(base) && fs.readdirSync(base).length === 0) {
        fs.rmdirSync(base);
      }
    } catch (_) {}
  }
}

// ---------- test suites ----------

/**
 * Test: /api/archive returns empty array when no archive exists
 */
async function testArchiveEndpointEmpty() {
  console.log('\n--- testArchiveEndpointEmpty ---');
  const res = await get('/api/archive');
  assert(res.status === 200, `/api/archive returns 200 (got ${res.status})`);
  assert(Array.isArray(res.json), `/api/archive returns an array`);
}

/**
 * Test: /api/archive/:id returns 404 for nonexistent task
 */
async function testArchiveDetailNotFound() {
  console.log('\n--- testArchiveDetailNotFound ---');
  const res = await get('/api/archive/NONEXISTENT-99999');
  assert(res.status === 404, `/api/archive/:id returns 404 for nonexistent (got ${res.status})`);
}

/**
 * Test: /api/archive reads archived tasks from new layout (subdirectory)
 */
async function testArchiveReadsNewLayout() {
  console.log('\n--- testArchiveReadsNewLayout ---');

  const taskData = {
    id: 'TEST-ARCH-001',
    title: 'Test Archived Task',
    status: 'archived',
    phase: 'archive',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  writeArchiveFile('TEST-ARCH-001', taskData);

  try {
    const res = await get('/api/archive');
    assert(res.status === 200, `/api/archive returns 200`);
    assert(Array.isArray(res.json), `/api/archive returns an array`);
    const found = res.json.find(t => t.id === 'TEST-ARCH-001');
    assert(found !== undefined, `Archived task list includes TEST-ARCH-001`);
    if (found) {
      assert(found.title === 'Test Archived Task', `Archived task has correct title`);
      assert(found.phase === 'archive', `Archived task has correct phase`);
    }

    // Test individual archived task detail
    const detailRes = await get('/api/archive/TEST-ARCH-001');
    assert(detailRes.status === 200, `/api/archive/:id returns 200 (got ${detailRes.status})`);
    assert(detailRes.json.id === 'TEST-ARCH-001', `Archived task detail has correct id`);
    assert(detailRes.json.title === 'Test Archived Task', `Archived task detail has correct title`);
  } finally {
    removeArchiveDir('TEST-ARCH-001');
    cleanupArchiveBase();
  }
}

/**
 * Test: SSE emits task_created event when a new task file appears in new layout
 */
async function testSSETaskCreatedNewLayout() {
  console.log('\n--- testSSETaskCreatedNewLayout ---');

  const taskData = {
    id: 'TEST-SSE-CREATE',
    title: 'SSE Created Test',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  try {
    // Start listening for task_created event
    const eventPromise = waitForEvent(5000, (e) => e.event === 'task_created');
    await new Promise(r => setTimeout(r, 200));

    // Create the task in new layout
    writeTaskFile('TEST-SSE-CREATE', taskData);

    const event = await eventPromise;
    assert(event !== null, `Received task_created event for new layout task`);

    if (event && event.data) {
      assert(event.data.id === 'TEST-SSE-CREATE', `task_created event has correct task id`);
      assert(event.data.task !== undefined, `task_created event includes task object`);
    }
  } finally {
    removeTaskDir('TEST-SSE-CREATE');
  }
}

/**
 * Test: SSE emits task_updated event when a task file is modified
 */
async function testSSETaskUpdated() {
  console.log('\n--- testSSETaskUpdated ---');

  const taskData = {
    id: 'TEST-SSE-UPDATE',
    title: 'SSE Update Test',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  try {
    // Create the task first
    writeTaskFile('TEST-SSE-UPDATE', taskData);
    // Wait for the initial create event to settle
    await new Promise(r => setTimeout(r, 500));

    // Now listen for task_updated
    const eventPromise = waitForEvent(5000, (e) => e.event === 'task_updated');
    await new Promise(r => setTimeout(r, 200));

    // Modify the task
    taskData.status = 'planning';
    taskData.phase = 'plan';
    taskData.updated_at = new Date().toISOString();
    writeTaskFile('TEST-SSE-UPDATE', taskData);

    const event = await eventPromise;
    assert(event !== null, `Received task_updated event after modification`);

    if (event && event.data) {
      assert(event.data.id === 'TEST-SSE-UPDATE', `task_updated event has correct task id`);
    }
  } finally {
    removeTaskDir('TEST-SSE-UPDATE');
  }
}

/**
 * Test: SSE emits task_archived event when a task file is removed
 */
async function testSSETaskArchived() {
  console.log('\n--- testSSETaskArchived ---');

  const taskData = {
    id: 'TEST-SSE-ARCHIVE',
    title: 'SSE Archive Test',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  try {
    // Create the task first
    writeTaskFile('TEST-SSE-ARCHIVE', taskData);
    // Wait for the initial create event to settle
    await new Promise(r => setTimeout(r, 500));

    // Now listen for task_archived
    const eventPromise = waitForEvent(5000, (e) => e.event === 'task_archived');
    await new Promise(r => setTimeout(r, 200));

    // Delete the task
    removeTaskDir('TEST-SSE-ARCHIVE');

    const event = await eventPromise;
    assert(event !== null, `Received task_archived event after deletion`);

    if (event && event.data) {
      assert(event.data.id === 'TEST-SSE-ARCHIVE', `task_archived event has correct task id`);
    }
  } finally {
    // Already cleaned up
  }
}

/**
 * Test: SSE also sends tasks:refresh alongside granular events
 */
async function testSSETasksRefreshAlongsideGranular() {
  console.log('\n--- testSSETasksRefreshAlongsideGranular ---');

  const taskData = {
    id: 'TEST-SSE-REFRESH',
    title: 'SSE Refresh Test',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  try {
    // Start collecting events
    const eventsPromise = collectEvents(3000);
    await new Promise(r => setTimeout(r, 300));

    // Create the task
    writeTaskFile('TEST-SSE-REFRESH', taskData);

    const events = await eventsPromise;

    const hasCreated = events.some(e => e.event === 'task_created');
    const hasRefresh = events.some(e => e.event === 'tasks:refresh');
    assert(hasCreated, `task_created event was emitted`);
    assert(hasRefresh, `tasks:refresh event was also emitted`);

    // Check that tasks:refresh data is an array containing the new task
    const refreshEvent = events.find(e => e.event === 'tasks:refresh');
    if (refreshEvent && refreshEvent.data) {
      assert(Array.isArray(refreshEvent.data), `tasks:refresh data is an array`);
      assert(
        refreshEvent.data.some(t => t.id === 'TEST-SSE-REFRESH'),
        `tasks:refresh data includes the new task`
      );
    }
  } finally {
    removeTaskDir('TEST-SSE-REFRESH');
  }
}

/**
 * Test: /api/tasks/:id reads iteration reports from new layout
 */
async function testTaskDetailWithIterationReports() {
  console.log('\n--- testTaskDetailWithIterationReports ---');

  const taskData = {
    id: 'TEST-ITER-RPT',
    title: 'Iteration Report Test',
    status: 'pending',
    phase: 'execute',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  writeTaskFile('TEST-ITER-RPT', taskData);

  // Create an iteration directory with a mock report in both locations
  const mockReport = {
    role: 'code_reviewer',
    task_id: 'TEST-ITER-RPT',
    iteration: 1,
    scores: {
      architecture: 8,
      code_quality: 9,
      overall: 8.5
    },
    passed: true,
    summary: 'Test report'
  };

  for (const base of [TASKS_DIR_WATCHER, TASKS_DIR_API]) {
    const iterDir = path.join(base, 'TEST-ITER-RPT', 'iteration-1');
    ensureDir(iterDir);
    fs.writeFileSync(path.join(iterDir, 'code_reviewer_report.json'), JSON.stringify(mockReport, null, 2));
  }

  try {
    const res = await get('/api/tasks/TEST-ITER-RPT');
    assert(res.status === 200, `/api/tasks/:id returns 200 for new layout task (got ${res.status})`);
    if (res.json) {
      assert(res.json.id === 'TEST-ITER-RPT', `Task detail has correct id`);
      const reports = res.json.reports;
      assert(Array.isArray(reports), `Task detail has reports array`);
      const codeReviewReport = reports.find(r => r.role === 'code_reviewer');
      assert(codeReviewReport !== undefined, `Reports include code_reviewer`);
      if (codeReviewReport) {
        assert(codeReviewReport.iteration === 1, `Report has correct iteration number`);
        assert(codeReviewReport.report !== undefined, `Report has report object`);
      }
    }
  } finally {
    removeTaskDir('TEST-ITER-RPT');
  }
}

/**
 * Test: /api/tasks/:id returns 404 for nonexistent task
 */
async function testTaskDetailNotFound() {
  console.log('\n--- testTaskDetailNotFound ---');
  const res = await get('/api/tasks/NONEXISTENT-99999');
  assert(res.status === 404, `/api/tasks/:id returns 404 for nonexistent task (got ${res.status})`);
}

/**
 * Test: SSE events include the full task object in data
 */
async function testSSEEventIncludesTaskObject() {
  console.log('\n--- testSSEEventIncludesTaskObject ---');

  const taskData = {
    id: 'TEST-SSE-OBJ',
    title: 'SSE Object Test',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  try {
    const eventPromise = waitForEvent(5000, (e) =>
      e.event === 'task_created' && e.data && e.data.id === 'TEST-SSE-OBJ'
    );
    await new Promise(r => setTimeout(r, 200));

    writeTaskFile('TEST-SSE-OBJ', taskData);

    const event = await eventPromise;
    assert(event !== null, `Received task_created event with matching id`);

    if (event && event.data) {
      assert(event.data.task !== undefined, `Event data includes task object`);
      assert(event.data.task.id === 'TEST-SSE-OBJ', `Task object has correct id`);
      // readAllTasks returns summary objects with specific fields
      assert(event.data.task.status !== undefined, `Task object has status field`);
      assert(event.data.task.phase !== undefined, `Task object has phase field`);
    }
  } finally {
    removeTaskDir('TEST-SSE-OBJ');
  }
}

// ---------- main ----------

async function main() {
  console.log('Starting test server on port', PORT);
  await startServer();

  try {
    // Archive endpoint tests
    await testArchiveEndpointEmpty();
    await testArchiveDetailNotFound();
    await testArchiveReadsNewLayout();

    // SSE granular event tests
    await testSSETaskCreatedNewLayout();
    await testSSETaskUpdated();
    await testSSETaskArchived();
    await testSSETasksRefreshAlongsideGranular();
    await testSSEEventIncludesTaskObject();

    // Task detail with iteration reports
    await testTaskDetailWithIterationReports();
    await testTaskDetailNotFound();
  } catch (err) {
    console.error('Test error:', err);
    failed++;
  } finally {
    stopServer();
  }

  console.log(`\n========== RESULTS ==========`);
  console.log(`  Passed: ${passed}`);
  console.log(`  Failed: ${failed}`);
  console.log(`  Total:  ${passed + failed}`);
  console.log(`=============================`);

  process.exit(failed > 0 ? 1 : 0);
}

main();
