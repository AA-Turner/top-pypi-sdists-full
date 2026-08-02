// Tests for parallel_batch.workflow.js — the batch's parallel Workflow executor.
//
// The Workflow tool runs the script in a sandbox with injected globals (agent/parallel/log/args)
// and no filesystem/import. We reproduce that here: load the single source file into a node:vm
// context, wrap it in an async IIFE (so its top-level await/return work), inject fake
// agent/parallel/log/args, and assert on the recorded agent calls + the returned outcomes.
// This covers the JS orchestration (dependency waves, parallel phase-1, strictly serial merge,
// skipping non-ready tickets). The real agent/worktree behaviour is out of scope — live only.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const WORKFLOW = join(dirname(fileURLToPath(import.meta.url)), "parallel_batch.workflow.js");
const SRC = readFileSync(WORKFLOW, "utf8").replace(/^export\s+/m, ""); // `export const meta` → `const meta`

// A fake agent whose reply is chosen by the call's `label` ("impl:<ref>" / "merge:<ref>").
function makeAgent(replies) {
  const calls = [];
  const agent = async (prompt, opts) => {
    calls.push({ label: opts.label, phase: opts.phase, isolation: opts.isolation, prompt });
    const reply = replies[opts.label];
    if (reply === undefined) throw new Error(`no fake reply for ${opts.label}`);
    return typeof reply === "function" ? reply() : reply;
  };
  return { agent, calls };
}

async function runWorkflow(args, replies) {
  const { agent, calls } = makeAgent(replies);
  const parallelSizes = []; // one entry per parallel() call = a phase-1 batch
  const context = {
    // The Workflow runtime hands `args` in as a JSON string — mirror that so the tests
    // exercise the script's parse path (a live run caught this: object-args passed the
    // unit tests but the runtime string crashed on args.plan).
    args: JSON.stringify(args),
    agent,
    parallel: (thunks) => {
      parallelSizes.push(thunks.length);
      return Promise.all(thunks.map((t) => t()));
    },
    log: () => {},
    console,
  };
  vm.createContext(context);
  const result = await vm.runInNewContext(`(async () => {\n${SRC}\n})()`, context);
  return { result, calls, parallelSizes };
}

const idx = (calls, label) => calls.findIndex((c) => c.label === label);

const outcome = (ref, status, extra = {}) => {
  const [project_path, iid] = ref.split("#");
  return { ticket_iid: Number(iid), project_path, status, mr_iid: Number(iid), mr_url: `https://mr/${iid}`, escalation_reason: null, ...extra };
};

const baseArgs = (ordered, edges = []) => ({
  plan: { ordered, edges },
  concurrency: 4,
  mergeStrategy: "rebase",
  checkpointPath: "/tmp/ckpt.json",
  webUrlOf: Object.fromEntries(ordered.map((r) => [r, `https://gitlab.com/${r.split("#")[0]}/-/work_items/${r.split("#")[1]}`])),
});

test("no dependencies: every ticket is implemented then merged", async () => {
  const refs = ["p#1", "p#2", "p#3"];
  const replies = {};
  for (const r of refs) {
    replies[`impl:${r}`] = outcome(r, "ready_to_merge");
    replies[`merge:${r}`] = outcome(r, "success");
  }
  const { result, calls } = await runWorkflow(baseArgs(refs), replies);
  assert.equal(result.outcomes.length, 3);
  assert.ok(result.outcomes.every((o) => o.status === "success"));
  assert.equal(calls.filter((c) => c.label.startsWith("impl:")).length, 3);
  assert.equal(calls.filter((c) => c.label.startsWith("merge:")).length, 3);
  // phase-1 agents run in isolated worktrees
  assert.ok(calls.filter((c) => c.label.startsWith("impl:")).every((c) => c.isolation === "worktree"));
});

test("dependency: a blocked ticket is implemented only after its blocker merged", async () => {
  // p#2 is blocked by p#1 → wave 1 = [p#1], wave 2 = [p#2]
  const replies = {
    "impl:p#1": outcome("p#1", "ready_to_merge"),
    "merge:p#1": outcome("p#1", "success"),
    "impl:p#2": outcome("p#2", "ready_to_merge"),
    "merge:p#2": outcome("p#2", "success"),
  };
  const { calls } = await runWorkflow(baseArgs(["p#1", "p#2"], [{ blocker: "p#1", blocked: "p#2" }]), replies);
  const order = calls.map((c) => c.label);
  assert.deepEqual(order, ["impl:p#1", "merge:p#1", "impl:p#2", "merge:p#2"]);
});

test("merges are strictly serial and follow their wave's phase-1", async () => {
  const refs = ["p#1", "p#2"];
  const replies = {};
  for (const r of refs) {
    replies[`impl:${r}`] = outcome(r, "ready_to_merge");
    replies[`merge:${r}`] = outcome(r, "success");
  }
  const { calls } = await runWorkflow(baseArgs(refs), replies);
  // within a single wave: both phase-1 (parallel) complete, then the merges run one after another
  assert.deepEqual(
    calls.map((c) => c.label),
    ["impl:p#1", "impl:p#2", "merge:p#1", "merge:p#2"],
  );
});

test("a ticket that fails phase-1 is finalised (blocked), not merged", async () => {
  const esc = outcome("p#1", "escalated", { escalation_reason: "review did not converge" });
  const replies = { "impl:p#1": esc, "finalize:p#1": esc };
  const { result, calls } = await runWorkflow(baseArgs(["p#1"]), replies);
  assert.equal(calls.filter((c) => c.label.startsWith("merge:")).length, 0);
  assert.ok(calls.some((c) => c.label === "finalize:p#1")); // finalised in real time
  assert.equal(result.outcomes.length, 1);
  assert.equal(result.outcomes[0].status, "escalated");
});

test("phase-1 agent crash is caught as a failed outcome, finalised, no merge", async () => {
  const replies = {
    "impl:p#1": () => {
      throw new Error("agent died");
    },
    "finalize:p#1": outcome("p#1", "failed", { escalation_reason: "phase-1 agent crashed" }),
  };
  const { result, calls } = await runWorkflow(baseArgs(["p#1"]), replies);
  assert.equal(calls.filter((c) => c.label.startsWith("merge:")).length, 0);
  assert.ok(calls.some((c) => c.label === "finalize:p#1"));
  assert.equal(result.outcomes[0].status, "failed");
});

test("diamond dependencies: root first, join last, across waves", async () => {
  // p#1 → {p#2, p#3} → p#4
  const refs = ["p#1", "p#2", "p#3", "p#4"];
  const edges = [
    { blocker: "p#1", blocked: "p#2" },
    { blocker: "p#1", blocked: "p#3" },
    { blocker: "p#2", blocked: "p#4" },
    { blocker: "p#3", blocked: "p#4" },
  ];
  const replies = {};
  for (const r of refs) {
    replies[`impl:${r}`] = outcome(r, "ready_to_merge");
    replies[`merge:${r}`] = outcome(r, "success");
  }
  const { calls } = await runWorkflow(baseArgs(refs, edges), replies);
  // p#1 fully done (impl+merge) before its dependents' phase-1; p#4 after both p#2 and p#3
  assert.ok(idx(calls, "merge:p#1") < idx(calls, "impl:p#2"));
  assert.ok(idx(calls, "merge:p#1") < idx(calls, "impl:p#3"));
  assert.ok(idx(calls, "merge:p#2") < idx(calls, "impl:p#4"));
  assert.ok(idx(calls, "merge:p#3") < idx(calls, "impl:p#4"));
});

test("phase-1 is chunked by concurrency", async () => {
  const refs = ["p#1", "p#2", "p#3", "p#4", "p#5"];
  const replies = {};
  for (const r of refs) {
    replies[`impl:${r}`] = outcome(r, "ready_to_merge");
    replies[`merge:${r}`] = outcome(r, "success");
  }
  // one wave (no edges), concurrency 2 → phase-1 batches of 2, 2, 1
  const { parallelSizes } = await runWorkflow({ ...baseArgs(refs), concurrency: 2 }, replies);
  assert.deepEqual(parallelSizes, [2, 2, 1]);
});

test("a merge that escalates is recorded as escalated (not success)", async () => {
  const replies = {
    "impl:p#1": outcome("p#1", "ready_to_merge"),
    "merge:p#1": outcome("p#1", "escalated", { escalation_reason: "merge-gate: rebase conflict — foo.py" }),
  };
  const { result } = await runWorkflow(baseArgs(["p#1"]), replies);
  assert.equal(result.outcomes.length, 1);
  assert.equal(result.outcomes[0].status, "escalated");
});

test("prompts carry the exact commands the runtime must run", async () => {
  const replies = {
    "impl:p#1": outcome("p#1", "ready_to_merge"),
    "merge:p#1": outcome("p#1", "success"),
  };
  const { calls } = await runWorkflow(baseArgs(["p#1"]), replies);
  const implPrompt = calls.find((c) => c.label === "impl:p#1").prompt;
  const mergePrompt = calls.find((c) => c.label === "merge:p#1").prompt;
  // phase 1: the ticket URL + stop-before-merge, and returns only the footer
  assert.match(implPrompt, /\/code-autopilot https:\/\/gitlab\.com\/p\/-\/work_items\/1/);
  assert.match(implPrompt, /--stop-before-merge/);
  assert.match(implPrompt, /AUTOPILOT_RESULT/);
  // merge: the merge-gate command with the resolved strategy, and the conflict → rebase path
  assert.match(mergePrompt, /pysae-ai-tools agent merge-gate --strategy rebase/);
  assert.match(mergePrompt, /rebase conflict/);
  assert.match(mergePrompt, /\/mr-rebase !1 --rebase-only/);
  // finalisation folded into the merge step (real-time), not a bulk pass afterwards
  assert.match(mergePrompt, /agent label done p 1/);
  assert.match(mergePrompt, /agent label block p 1/);
  assert.match(mergePrompt, /agent watch-deploy/);
  assert.match(mergePrompt, /agent checkpoint append --path \/tmp\/ckpt\.json/);
});

test("noCi threads --no-ci into phase-1 and merge, and skips the deploy watch", async () => {
  const replies = { "impl:p#1": outcome("p#1", "ready_to_merge"), "merge:p#1": outcome("p#1", "success") };
  const { calls } = await runWorkflow({ ...baseArgs(["p#1"]), noCi: true }, replies);
  const impl = calls.find((c) => c.label === "impl:p#1").prompt;
  const merge = calls.find((c) => c.label === "merge:p#1").prompt;
  assert.match(impl, /--no-ci/);
  assert.match(merge, /agent merge-gate --strategy rebase --no-ci/);
  assert.doesNotMatch(merge, /agent watch-deploy/); // post-merge watch invocation skipped under no-ci
});

test("batchTarget retargets phase-1 onto the staging branch", async () => {
  const replies = { "impl:p#1": outcome("p#1", "ready_to_merge"), "merge:p#1": outcome("p#1", "success") };
  const { calls } = await runWorkflow(
    { ...baseArgs(["p#1"]), noCi: true, batchTarget: "staging/autopilot-batch-20260711-1200" },
    replies,
  );
  assert.match(calls.find((c) => c.label === "impl:p#1").prompt, /--target-branch staging\/autopilot-batch-20260711-1200/);
});
