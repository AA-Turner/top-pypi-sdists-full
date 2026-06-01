/**
 * SSE (Server-Sent Events) tests for Dashboard server.
 * Uses Node.js native http module -- no test framework required.
 *
 * Run: node tests/sse.test.js
 */

const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = 3200; // Use a different port from api.test.js to avoid conflicts
const BASE = `http://localhost:${PORT}`;
const KANBAN_ROOT = path.resolve(__dirname, '..');
const TASKS_DIR = path.join(KANBAN_ROOT, '..', 'tasks');

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

/**
 * Connect to the SSE endpoint and return a promise that resolves
 * with { response, events } after the specified duration.
 * events is an array of parsed SSE messages.
 */
function connectSSE(durationMs) {
  return new Promise((resolve, reject) => {
    const url = new URL('/api/events', BASE);
    const req = http.request(url, { method: 'GET' }, (res) => {
      const events = [];
      let buffer = '';

      res.on('data', (chunk) => {
        buffer += chunk.toString();
        // Parse SSE messages from buffer
        const parts = buffer.split('\n\n');
        // Keep the last (possibly incomplete) part in the buffer
        buffer = parts.pop() || '';
        for (const part of parts) {
          if (part.trim().length === 0) continue;
          const parsed = parseSSE(part);
          if (parsed) events.push(parsed);
        }
      });

      setTimeout(() => {
        // Parse any remaining buffer
        if (buffer.trim().length > 0) {
          const parsed = parseSSE(buffer);
          if (parsed) events.push(parsed);
        }
        resolve({ response: res, events });
      }, durationMs);
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
      const raw = line.substring(6);
      try { data = JSON.parse(raw); } catch (_) { data = raw; }
    }
  }

  // Only return if we found something meaningful
  if (eventType || data !== null || comment !== null) {
    return { event: eventType, data, comment };
  }
  return null;
}

/**
 * Wait for a specific SSE event type, with a timeout.
 * Returns the first matching event or null if timed out.
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

// ---------- test suites ----------

/**
 * Test 1: SSE connection basics
 * - Response status 200
 * - Content-Type contains text/event-stream
 * - Receive initial connected event
 */
async function testSSEConnection() {
  console.log('\n--- testSSEConnection ---');

  const url = new URL('/api/events', BASE);
  const result = await new Promise((resolve, reject) => {
    const req = http.request(url, { method: 'GET' }, (res) => {
      let firstChunk = '';
      const events = [];
      let buffer = '';

      res.on('data', (chunk) => {
        if (!firstChunk) firstChunk = chunk.toString();
        buffer += chunk.toString();
        const parts = buffer.split('\n\n');
        buffer = parts.pop() || '';
        for (const part of parts) {
          if (part.trim().length === 0) continue;
          const parsed = parseSSE(part);
          if (parsed) events.push(parsed);
        }
      });

      // Wait a short time to receive the initial event
      setTimeout(() => {
        if (buffer.trim().length > 0) {
          const parsed = parseSSE(buffer);
          if (parsed) events.push(parsed);
        }
        res.destroy();
        resolve({ status: res.statusCode, headers: res.headers, events });
      }, 1000);
    });

    req.on('error', reject);
    req.end();
  });

  assert(result.status === 200, `SSE endpoint returns 200 (got ${result.status})`);

  const contentType = result.headers['content-type'] || '';
  assert(
    contentType.includes('text/event-stream'),
    `Content-Type includes text/event-stream (got ${contentType})`
  );

  const connectedEvent = result.events.find(e => e.event === 'connected');
  assert(
    connectedEvent !== undefined,
    `Received initial 'connected' event`
  );

  if (connectedEvent) {
    assert(
      connectedEvent.data && typeof connectedEvent.data.time === 'number',
      `Connected event contains time field`
    );
  }
}

/**
 * Test 2: Heartbeat
 * The server sends ': heartbeat\n\n' every 30 seconds.
 * We wait up to 35 seconds to receive one.
 */
async function testHeartbeat() {
  console.log('\n--- testHeartbeat (waiting up to 35s) ---');

  const result = await connectSSE(35000);

  const heartbeatFound = result.events.some(e => e.comment === 'heartbeat');
  assert(heartbeatFound, `Received heartbeat comment within 35 seconds`);
}

/**
 * Test 3: File change triggers tasks:refresh event
 * Create a temporary task file, verify the SSE event arrives, then clean up.
 */
async function testFileChangeTriggersEvent() {
  console.log('\n--- testFileChangeTriggersEvent ---');

  // Ensure tasks directory exists
  if (!fs.existsSync(TASKS_DIR)) {
    fs.mkdirSync(TASKS_DIR, { recursive: true });
  }

  const testTaskFile = path.join(TASKS_DIR, 'TEST-SSE-TEMP.json');
  const testTaskData = {
    id: 'TEST-SSE-TEMP',
    title: 'SSE Test Task',
    status: 'pending',
    phase: 'idle',
    iteration: 1,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  // Start listening for events first
  const eventPromise = waitForEvent(5000, (e) => e.event === 'tasks:refresh');

  // Small delay to ensure SSE connection is established
  await new Promise(r => setTimeout(r, 200));

  // Write the test task file
  fs.writeFileSync(testTaskFile, JSON.stringify(testTaskData, null, 2));

  const event = await eventPromise;

  assert(event !== null, `Received tasks:refresh event after file change`);

  if (event && event.data) {
    assert(
      Array.isArray(event.data),
      `tasks:refresh event data is an array`
    );
    assert(
      event.data.some(t => t.id === 'TEST-SSE-TEMP'),
      `tasks:refresh event includes the test task in the array`
    );
  }

  // Now test deletion: remove the file and verify it triggers another event
  const deleteEventPromise = waitForEvent(5000, (e) =>
    e.event === 'tasks:refresh' && e.data && Array.isArray(e.data) && !e.data.some(t => t.id === 'TEST-SSE-TEMP')
  );

  // Small delay before deletion
  await new Promise(r => setTimeout(r, 200));

  // Delete the test file
  fs.unlinkSync(testTaskFile);

  const deleteEvent = await deleteEventPromise;

  assert(deleteEvent !== null, `Received tasks:refresh event after file deletion`);

  if (deleteEvent && deleteEvent.data) {
    assert(
      !deleteEvent.data.some(t => t.id === 'TEST-SSE-TEMP'),
      `tasks:refresh event no longer includes the deleted test task`
    );
  }
}

// ---------- main ----------

async function main() {
  console.log('Starting test server on port', PORT);
  await startServer();

  try {
    await testSSEConnection();
    await testHeartbeat();
    await testFileChangeTriggersEvent();
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
