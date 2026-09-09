/**
 * Run with: npm test  (node's built-in runner, no dependencies)
 *
 * Drives pollRevisionDeployed against a stub Host v2 that reproduces the race:
 * the control plane keeps serving the previous, already-DEPLOYED revision for
 * a moment after a mutation is accepted.
 */

import assert from "node:assert/strict";
import { createServer } from "node:http";
import test from "node:test";

/**
 * Serve a scripted sequence of revisions, one entry per GET.
 * The last entry repeats once the script is exhausted.
 */
function stubHost(script) {
  const calls = [];
  const server = createServer((req, res) => {
    calls.push(req.url);
    const revision = script[Math.min(calls.length - 1, script.length - 1)];
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ resources: [revision] }));
  });
  return new Promise((resolve) => {
    server.listen(0, () => {
      resolve({
        base: `http://127.0.0.1:${server.address().port}/v2`,
        calls,
        close: () => new Promise((done) => server.close(done)),
      });
    });
  });
}

/**
 * Import host-v2 fresh so it picks up HOST_API_V2_BASE and the compressed poll
 * interval. 5ms stands in for the production 10s; the loops are driven by the
 * scripted response sequence, not elapsed time, so the value is arbitrary.
 */
async function loadHostV2(base) {
  process.env.HOST_API_V2_BASE = base;
  process.env.HOST_POLL_INTERVAL_MS = "5";
  return import(`./host-v2.js?t=${Math.random()}`);
}

const OLD = { id: "rev-old", status: "DEPLOYED" };
const NEW_PENDING = { id: "rev-new", status: "DEPLOYING" };
const NEW_DONE = { id: "rev-new", status: "DEPLOYED" };

test("without a revisionId the stale revision is accepted (the bug)", async () => {
  const host = await stubHost([OLD]);
  try {
    const { pollRevisionDeployed } = await loadHostV2(host.base);
    const revision = await pollRevisionDeployed("dep", "key");
    assert.equal(revision.id, "rev-old");
  } finally {
    await host.close();
  }
});

test("a revisionId waits for that exact revision to surface and deploy", async () => {
  const host = await stubHost([OLD, OLD, NEW_PENDING, NEW_DONE]);
  try {
    const { pollRevisionDeployed } = await loadHostV2(host.base);
    const revision = await pollRevisionDeployed("dep", "key", {
      revisionId: "rev-new",
    });
    assert.equal(revision.id, "rev-new");
    assert.equal(revision.status, "DEPLOYED");
    assert.ok(host.calls.length >= 4, `polled ${host.calls.length} times`);
  } finally {
    await host.close();
  }
});

test("a revision already deployed when we ask returns straight away", async () => {
  const host = await stubHost([NEW_DONE]);
  try {
    const { pollRevisionDeployed } = await loadHostV2(host.base);
    const revision = await pollRevisionDeployed("dep", "key", {
      revisionId: "rev-new",
    });
    assert.equal(revision.id, "rev-new");
    assert.equal(host.calls.length, 1, "no extra polling needed");
  } finally {
    await host.close();
  }
});

test("health check requires a sustained streak, not a single 200", async () => {
  const script = [true, false, true, true, true];
  let i = 0;
  const server = createServer((req, res) => {
    const ok = script[Math.min(i++, script.length - 1)];
    res.writeHead(ok ? 200 : 503, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok }));
  });
  await new Promise((r) => server.listen(0, r));
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    const { pollDeploymentHealthy } = await loadHostV2(`${base}/v2`);
    await pollDeploymentHealthy(base, null, { checkDb: false, consecutive: 3 });
    assert.equal(i, 5, `expected 5 probes, saw ${i}`);
  } finally {
    await new Promise((done) => server.close(done));
  }
});
