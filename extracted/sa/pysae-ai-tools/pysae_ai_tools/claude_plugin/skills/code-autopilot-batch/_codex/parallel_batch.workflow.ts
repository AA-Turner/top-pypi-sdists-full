// Codex-flow port of parallel_batch.workflow.js — parallel phase-1 (isolated worktrees) +
// strictly-serial, re-validated merge-gate for /code-autopilot-batch on Codex.
//
// codex-flow has no runtime `args`: the skill INJECTS the real batch plan by replacing the
// INPUT const below before `codex-flow run`, exactly like the bundled examples ("the skill
// replaces this with the real … list"). The default value is a null-safe placeholder so the
// workflow also runs under `--backend fake`.
//
// vs the Claude Workflow original: `agent()` returns `{status, output}` (not the value), so
// every call is null-checked; `phase(title, body)` wraps a body (it is not a marker); worktree
// isolation is `isolate + sandbox:'workspace-write' + cwd`; the per-call label is `nodeKey`.

// INPUT (skill-injected):
//   plan: { ordered: string[], edges: {blocker,blocked}[] }  — refs are "group/project#iid"
//   concurrency: number         — max parallel phase-1 tickets
//   mergeStrategy: 'rebase'|'train'
//   webUrlOf: { [ref]: string } — GitLab work_items URL per ref
//   checkpointPath / noCi / batchTarget — CI-control, mirror the JS original
const INPUT: any = {
  plan: { ordered: [], edges: [] },
  concurrency: 4,
  mergeStrategy: "rebase",
  webUrlOf: {},
  checkpointPath: "",
  noCi: false,
  batchTarget: "",
};

const OUTCOME_SCHEMA = {
  type: "object",
  required: ["ticket_iid", "project_path", "status"],
  properties: {
    ticket_iid: { type: "integer" },
    project_path: { type: "string" },
    status: { enum: ["success", "ready_to_merge", "escalated", "failed"] },
    mr_iid: { type: ["integer", "null"] },
    mr_url: { type: ["string", "null"] },
    escalation_reason: { type: ["string", "null"] },
  },
};

// Dependency waves (Kahn levels): a wave's tickets have all in-batch blockers in earlier
// waves, i.e. merged before this wave's phase-1 starts. No deps → a single wave (all parallel).
function waves(ordered: string[], edges: Array<{ blocker: string; blocked: string }>): string[][] {
  const indeg: Record<string, number> = {};
  const succ: Record<string, string[]> = {};
  for (const r of ordered) {
    indeg[r] = 0;
    succ[r] = [];
  }
  for (const e of edges) {
    if (indeg[e.blocked] === undefined || indeg[e.blocker] === undefined) continue;
    indeg[e.blocked]++;
    succ[e.blocker].push(e.blocked);
  }
  const out: string[][] = [];
  let cur = ordered.filter((r) => indeg[r] === 0);
  const seen = new Set(cur);
  while (cur.length) {
    out.push(cur);
    const next: string[] = [];
    for (const n of cur)
      for (const m of succ[n]) {
        if (--indeg[m] === 0 && !seen.has(m)) {
          seen.add(m);
          next.push(m);
        }
      }
    cur = next;
  }
  return out;
}

const iidOf = (ref: string): number => parseInt(ref.split("#")[1], 10);
const projectOf = (ref: string): string => ref.split("#")[0];

export default async function workflow(ctx: any) {
  const { agent, parallel, phase, log, budget } = ctx;
  budget.configure({ maxTokens: 2_000_000, maxNodes: 200, onExceeded: "throw" });

  const plan = INPUT.plan || { ordered: [], edges: [] };
  const concurrency = Math.max(1, INPUT.concurrency || 4);
  const mergeStrategy = INPUT.mergeStrategy || "rebase";
  const webUrl: Record<string, string> = INPUT.webUrlOf || {};
  const checkpointPath = INPUT.checkpointPath || "";
  const noCi = !!INPUT.noCi;
  const batchTarget = INPUT.batchTarget || "";

  const phase1Flags = `--approve=auto --stop-before-merge${noCi ? " --no-ci" : ""}${
    batchTarget ? ` --target-branch ${batchTarget}` : ""
  }`;

  const phase1Prompt = (ref: string): string =>
    `Run \`/code-autopilot ${webUrl[ref]} ${phase1Flags}\` to completion in this
isolated worktree: implement the issue, run the review loop${noCi ? "" : ", wait for a GREEN CI pipeline"}, approve the MR,
then STOP before merging.${noCi ? "" : " If a step waits on a pipeline, block until it is terminal — do not stop early."}
Return ONLY the AUTOPILOT_RESULT footer JSON (status will be "ready_to_merge" on success, else "escalated"/"failed").`;

  const ckptStep = (n: number): string =>
    checkpointPath
      ? `\n${n}. Append it to the checkpoint: \`echo '<FINAL>' | pysae-ai-tools agent checkpoint append --path ${checkpointPath}\`.`
      : "";

  const mergePrompt = (ref: string, outcome: any): string => {
    const project = projectOf(ref);
    const iid = iidOf(ref);
    return `Merge this ready-to-merge MR, re-validated against the current main, then finalise it. Steps:
1. Run: \`echo '${JSON.stringify(outcome)}' | pysae-ai-tools agent merge-gate --strategy ${mergeStrategy}${
      noCi ? " --no-ci" : ""
    }\`
2. If that outcome is "escalated" with an escalation_reason containing "rebase conflict": run
   \`/mr-rebase !${outcome.mr_iid} --rebase-only\` (auto-resolve + push), then re-run step 1. If
   /mr-rebase itself fails, keep the escalated outcome. Call the result FINAL.
3. Finalise the label from FINAL's status:
   - success → \`pysae-ai-tools agent label done ${project} ${iid}\`${
     noCi
       ? " (post-merge CI is disabled/deferred this run — do NOT run watch-deploy)."
       : `, then re-validate the deploy: \`FINAL=$(echo '<FINAL>' | pysae-ai-tools agent watch-deploy)\` (may demote success→escalated; do NOT re-label to blocked if it demotes — keep the label cleared, just carry the demoted FINAL).`
   }
   - escalated/failed → \`pysae-ai-tools agent label block ${project} ${iid} --reason "<FINAL.escalation_reason>"\`.${ckptStep(
     4,
   )}
Return ONLY the FINAL outcome JSON.`;
  };

  const blockPrompt = (ref: string, outcome: any): string =>
    `This ticket did not reach a mergeable state (phase 1: ${outcome.status}). Finalise it:
1. \`pysae-ai-tools agent label block ${projectOf(ref)} ${iidOf(ref)} --reason "${(
      outcome.escalation_reason || "phase 1 did not converge"
    ).replace(/"/g, "'")}"\`.${ckptStep(2).replace("<FINAL>", JSON.stringify(outcome))}
Return ONLY this outcome JSON unchanged: ${JSON.stringify(outcome)}`;

  const failedOutcome = (ref: string, reason: string) => ({
    ticket_iid: iidOf(ref),
    project_path: projectOf(ref),
    status: "failed",
    mr_iid: null,
    mr_url: null,
    escalation_reason: reason,
  });

  async function inBatches<T>(items: string[], cap: number, fn: (x: string) => Promise<T>): Promise<Array<T | null>> {
    const out: Array<T | null> = [];
    for (let i = 0; i < items.length; i += cap) {
      const chunk = await parallel(items.slice(i, i + cap).map((x: string) => () => fn(x)));
      out.push(...chunk);
    }
    return out;
  }

  const runAgent = async (prompt: string, nodeKey: string, opts: any = {}): Promise<any> => {
    const r = await agent(prompt, { schema: OUTCOME_SCHEMA, cwd: process.cwd(), nodeKey, ...opts });
    return r?.status === "ok" ? r.output : null;
  };

  const results: any[] = [];

  for (const [w, wave] of waves(plan.ordered, plan.edges).entries()) {
    log(`Wave ${w + 1}: ${wave.length} ticket(s) — phase 1 in parallel (concurrency ${concurrency})`);

    // Phase 1 — parallel, isolated worktrees, capped at `concurrency`.
    const phase1 = await phase(`wave-${w + 1}-implement`, async () =>
      inBatches(wave, concurrency, async (ref) => {
        try {
          const outcome = await runAgent(phase1Prompt(ref), `impl:${ref}`, {
            isolate: true,
            sandbox: "workspace-write",
          });
          return { ref, outcome: outcome || failedOutcome(ref, "phase-1 produced no outcome") };
        } catch {
          return { ref, outcome: failedOutcome(ref, "phase-1 agent crashed") };
        }
      }),
    );

    // Merge — strictly serial (one merge to main at a time), each re-validated on the current
    // main and FINALISED in place (label + checkpoint) so the board/checkpoint track reality live.
    await phase(`wave-${w + 1}-merge`, async () => {
      for (const entry of phase1) {
        if (!entry) continue;
        const { ref, outcome } = entry;
        if (!outcome || outcome.status !== "ready_to_merge") {
          const finalized = await runAgent(blockPrompt(ref, outcome), `finalize:${ref}`, {
            sandbox: "workspace-write",
          });
          results.push(finalized || outcome);
          log(`${ref} — ${(finalized || outcome).status} (not merged, finalised)`);
          continue;
        }
        const finalOutcome = await runAgent(mergePrompt(ref, outcome), `merge:${ref}`, {
          sandbox: "workspace-write",
        });
        const settled = finalOutcome || failedOutcome(ref, "merge step produced no outcome");
        results.push(settled);
        if (settled.status === "success") {
          log(`${ref} — merged (!${settled.mr_iid})`);
        } else {
          log(`${ref} — ${settled.status}: ${settled.escalation_reason || ""}`);
        }
      }
      return null;
    });
  }

  return { outcomes: results };
}
