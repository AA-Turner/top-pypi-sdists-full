/**
 * API tests for Dashboard server.
 * Uses Node.js native http module -- no test framework required.
 *
 * Run: node tests/api.test.js
 */

const http = require('http');
const { spawn } = require('child_process');
const path = require('path');

const PORT = 3199; // Use a non-default port for testing
const BASE = `http://localhost:${PORT}`;

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

function request(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, BASE);
    const options = { method, headers: {} };
    if (body) {
      options.headers['Content-Type'] = 'application/json';
    }
    const req = http.request(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        let parsed = null;
        try { parsed = JSON.parse(data); } catch (_) {}
        resolve({ status: res.statusCode, headers: res.headers, body: data, json: parsed });
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function get(urlPath) {
  return request('GET', urlPath);
}

// ---------- setup / teardown ----------

function waitForPort(port, timeoutMs) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function tryConnect() {
      const req = http.request(`http://localhost:${port}/api/config`, { method: 'GET' }, (res) => {
        res.resume(); // drain the response
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

    // Wait until the server actually accepts connections
    waitForPort(PORT, 10000).then(resolve, reject);
  });
}

function stopServer() {
  if (serverProcess) {
    serverProcess.kill('SIGTERM');
    serverProcess = null;
  }
}

// ---------- test suites ----------

async function testErrorResponsesNoMessageLeak() {
  console.log('\n--- testErrorResponsesNoMessageLeak ---');
  // Test that error responses do not contain err.message (detail field)
  // We trigger a 404 for a task, which should not leak server details
  const res = await get('/api/tasks/NOEXIST-TASK-99999');
  assert(res.status === 404, `Non-existent task returns 404 (got ${res.status})`);
  if (res.json) {
    assert(!res.json.detail, 'Error response does not contain detail field');
    const bodyStr = JSON.stringify(res.json);
    assert(!bodyStr.includes('ENOENT'), 'Error response does not leak ENOENT');
    assert(!bodyStr.includes('.json'), 'Error response does not leak file paths');
  }

  // Also verify archived tasks endpoint does not leak details on 404
  const res2 = await get('/api/archived-tasks/NOEXIST-TASK-99999');
  assert(res2.status === 404, `Non-existent archived task returns 404 (got ${res2.status})`);
  if (res2.json) {
    assert(!res2.json.detail, 'Archived task error response does not contain detail field');
    const bodyStr2 = JSON.stringify(res2.json);
    assert(!bodyStr2.includes('ENOENT'), 'Archived task error response does not leak ENOENT');
  }
}

async function testNormalEndpointsReturn200() {
  console.log('\n--- testNormalEndpointsReturn200 ---');
  const configRes = await get('/api/config');
  assert(configRes.status === 200, `/api/config returns 200 (got ${configRes.status})`);

  const workflowRes = await get('/api/workflow');
  assert(workflowRes.status === 200, `/api/workflow returns 200 (got ${workflowRes.status})`);

  const tasksRes = await get('/api/tasks');
  assert(tasksRes.status === 200, `/api/tasks returns 200 (got ${tasksRes.status})`);
  assert(Array.isArray(tasksRes.json), `/api/tasks returns an array`);
}

// --- Archived Tasks API Tests ---

async function testArchivedTasksReturnsArray() {
  console.log('\n--- testArchivedTasksReturnsArray ---');
  const res = await get('/api/archived-tasks');
  assert(res.status === 200, `/api/archived-tasks returns 200 (got ${res.status})`);
  assert(Array.isArray(res.json), '/api/archived-tasks returns an array');
}

async function testArchivedTasksItemFormat() {
  console.log('\n--- testArchivedTasksItemFormat ---');
  const res = await get('/api/archived-tasks');
  assert(res.status === 200, `/api/archived-tasks returns 200`);
  if (res.json && res.json.length > 0) {
    const task = res.json[0];
    assert(typeof task.id === 'string', 'Archived task has string id');
    assert(typeof task.title === 'string', 'Archived task has string title');
    // These fields should exist (may be null/undefined for old data)
    assert('status' in task, 'Archived task has status field');
    assert('phase' in task, 'Archived task has phase field');
    assert('iteration' in task, 'Archived task has iteration field');
    assert('created_at' in task, 'Archived task has created_at field');
    assert('updated_at' in task, 'Archived task has updated_at field');
  } else {
    // No archived tasks -- still pass, the endpoint works correctly
    console.log('  PASS: No archived tasks present (empty array is valid)');
  }
}

async function testArchivedTaskDetailNotFound() {
  console.log('\n--- testArchivedTaskDetailNotFound ---');
  const res = await get('/api/archived-tasks/NOEXIST-TASK-99999');
  assert(res.status === 404, `/api/archived-tasks/:id returns 404 for non-existent (got ${res.status})`);
  assert(res.json && res.json.error, 'Response contains error field');
}

async function testArchivedTaskDetailFormat() {
  console.log('\n--- testArchivedTaskDetailFormat ---');
  // First get the list of archived tasks
  const listRes = await get('/api/archived-tasks');
  if (listRes.json && listRes.json.length > 0) {
    const taskId = listRes.json[0].id;
    const detailRes = await get(`/api/archived-tasks/${taskId}`);
    assert(detailRes.status === 200, `/api/archived-tasks/:id returns 200 for existing task (got ${detailRes.status})`);
    assert(detailRes.json.id === taskId, 'Detail response has correct id');
    assert(Array.isArray(detailRes.json.reports), 'Detail response has reports array');
    assert(typeof detailRes.json.title === 'string', 'Detail response has title');
  } else {
    console.log('  PASS: No archived tasks to test detail (skipped)');
  }
}

async function testDocsEndpointRemoved() {
  console.log('\n--- testDocsEndpointRemoved ---');
  // Verify /api/docs and /api/docs/* return 404 (no longer handled)
  const res1 = await get('/api/docs');
  assert(res1.status === 404, `/api/docs returns 404 after removal (got ${res1.status})`);
  const res2 = await get('/api/docs/some-file.md');
  assert(res2.status === 404, `/api/docs/some-file.md returns 404 after removal (got ${res2.status})`);
}

// --- Path traversal regression tests ---

async function testPathTraversalTasksEndpoint() {
  console.log('\n--- testPathTraversalTasksEndpoint ---');
  // URL-encoded ".." -- /api/tasks/..%2F..%2Fconfig
  const res = await get('/api/tasks/..%2F..%2Fconfig');
  assert(res.status === 400, `Path traversal /api/tasks/..%2F..%2Fconfig returns 400 (got ${res.status})`);
  assert(res.json && res.json.error, 'Response contains error field');
  assert(
    res.json.error.includes('Invalid') || res.json.error.includes('invalid'),
    `Error message mentions invalid ID (got: ${res.json.error})`
  );
}

async function testPathTraversalArchiveEndpoint() {
  console.log('\n--- testPathTraversalArchiveEndpoint ---');
  const res = await get('/api/archive/..%2F..%2Fconfig');
  assert(res.status === 400, `Path traversal /api/archive/..%2F..%2Fconfig returns 400 (got ${res.status})`);
  assert(res.json && res.json.error, 'Response contains error field');
}

async function testPathTraversalArchivedTasksEndpoint() {
  console.log('\n--- testPathTraversalArchivedTasksEndpoint ---');
  const res = await get('/api/archived-tasks/..%2F..%2Fconfig');
  assert(res.status === 400, `Path traversal /api/archived-tasks/..%2F..%2Fconfig returns 400 (got ${res.status})`);
  assert(res.json && res.json.error, 'Response contains error field');
}

async function testPathTraversalWithBackslash() {
  console.log('\n--- testPathTraversalWithBackslash ---');
  // URL-encoded backslash "..\" variant: /api/tasks/..%5C..%5Cconfig
  const res = await get('/api/tasks/..%5C..%5Cconfig');
  assert(res.status === 400, `Path traversal /api/tasks/..%5C..%5Cconfig returns 400 (got ${res.status})`);
  assert(res.json && res.json.error, 'Response contains error field');
}

async function testValidTaskIdStillWorks() {
  console.log('\n--- testValidTaskIdStillWorks ---');
  // Ensure legitimate task IDs with no ".." are not rejected
  // Even a non-existent ID should return 404, not 400
  const res1 = await get('/api/tasks/TASK-99999');
  assert(res1.status === 404, `Legitimate ID /api/tasks/TASK-99999 returns 404 not 400 (got ${res1.status})`);

  const res2 = await get('/api/archive/TASK-99999');
  assert(res2.status === 404, `Legitimate ID /api/archive/TASK-99999 returns 404 not 400 (got ${res2.status})`);

  const res3 = await get('/api/archived-tasks/TASK-99999');
  assert(res3.status === 404, `Legitimate ID /api/archived-tasks/TASK-99999 returns 404 not 400 (got ${res3.status})`);
}

// --- Task ID length limit regression tests (#67) ---

async function testTaskIdTooLongRejected() {
  console.log('\n--- testTaskIdTooLongRejected ---');
  // 21-character ID should be rejected with 400
  const longId = 'TASK-1234567890123456'; // 21 chars
  const routes = [
    `/api/tasks/${longId}`,
    `/api/archive/${longId}`,
    `/api/archived-tasks/${longId}`,
    `/api/tasks/${longId}/retrospective`,
    `/api/archived-tasks/${longId}/retrospective`,
  ];
  for (const route of routes) {
    const res = await get(route);
    assert(res.status === 400, `${route} with ${longId.length}-char ID returns 400 (got ${res.status})`);
    assert(res.json && res.json.error, `${route} response contains error field`);
  }
}

async function testTaskIdMaxLengthAccepted() {
  console.log('\n--- testTaskIdMaxLengthAccepted ---');
  // 20-character ID should NOT be rejected (should get 404 not 400)
  const maxId = 'TASK-123456789012345'; // 20 chars
  const routes = [
    `/api/tasks/${maxId}`,
    `/api/archive/${maxId}`,
    `/api/archived-tasks/${maxId}`,
    `/api/tasks/${maxId}/retrospective`,
    `/api/archived-tasks/${maxId}/retrospective`,
  ];
  for (const route of routes) {
    const res = await get(route);
    assert(res.status !== 400, `${route} with ${maxId.length}-char ID is not rejected as invalid (got ${res.status}, expected 404)`);
  }
}

// ---------- main ----------

async function testSettingsAPIs() {
  console.log('\n--- Settings API ---');

  // PUT /api/config — valid payload
  {
    const res = await request('PUT', '/api/config', { project: 'test-project' });
    assert(res.status === 200, 'PUT config returns 200');
    assert(res.json && res.json.success === true, 'PUT config returns success');
  }

  // PUT /api/config — invalid payload
  {
    const res = await request('PUT', '/api/config', { budget: { warning_threshold: 2.0 } });
    assert(res.status === 400, 'PUT config invalid returns 400');
    assert(res.json && res.json.error, 'PUT config invalid has error message');
  }

  // GET /api/config — verify write persisted
  {
    const res = await get('/api/config');
    assert(res.status === 200, 'GET config after PUT returns 200');
    assert(res.json && res.json.project === 'test-project', 'GET config reflects PUT changes');
  }

  // PUT /api/workflow — valid payload
  {
    const res = await request('PUT', '/api/workflow', { pass_threshold: 9.0 });
    assert(res.status === 200, 'PUT workflow returns 200');
    assert(res.json && res.json.success === true, 'PUT workflow returns success');
  }

  // PUT /api/workflow — invalid pass_threshold
  {
    const res = await request('PUT', '/api/workflow', { pass_threshold: 15.0 });
    assert(res.status === 400, 'PUT workflow invalid returns 400');
  }

  // Restore original config
  {
    await request('PUT', '/api/config', { project: '' });
  }
}

async function main() {
  console.log('Starting test server on port', PORT);
  await startServer();

  try {
    await testErrorResponsesNoMessageLeak();
    await testNormalEndpointsReturn200();
    // Archived tasks API tests
    await testArchivedTasksReturnsArray();
    await testArchivedTasksItemFormat();
    await testArchivedTaskDetailNotFound();
    await testArchivedTaskDetailFormat();
    await testDocsEndpointRemoved();
    // Path traversal regression tests
    await testPathTraversalTasksEndpoint();
    await testPathTraversalArchiveEndpoint();
    await testPathTraversalArchivedTasksEndpoint();
    await testPathTraversalWithBackslash();
    await testValidTaskIdStillWorks();
    // Task ID length limit tests (#67)
    await testTaskIdTooLongRejected();
    await testTaskIdMaxLengthAccepted();

    // Settings API Tests
    await testSettingsAPIs();
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
