export const meta = {
  name: 'autopilot-batch-parallel',
  description: 'Parallel phase-1 (worktrees) + serial re-validated merge-gate for code-autopilot-batch',
  whenToUse: 'Invoked by /code-autopilot-batch when concurrency > 1 to process the dependency-ordered pool in parallel.',
  phases: [
    { title: 'Implement', detail: 'per-ticket /code-autopilot --stop-before-merge in an isolated worktree' },
    { title: 'Merge', detail: 'serial agent merge-gate, rebasing/resolving conflicts on the current main' },
  ],
}

// args (from the skill): {
//   plan: { ordered: string[], edges: {blocker,blocked}[] },  // refs are "group/project#iid"
//   concurrency: number,          // max parallel phase-1 tickets
//   mergeStrategy: 'rebase'|'train',
//   webUrlOf: { [ref]: string },  // GitLab work_items URL per ref
// }
// The Workflow runtime may hand `args` in as a JSON string rather than a parsed object.
const input = typeof args === 'string' ? JSON.parse(args) : args || {}
const plan = input.plan
const concurrency = Math.max(1, input.concurrency || 4)
const mergeStrategy = input.mergeStrategy || 'rebase'
const webUrl = input.webUrlOf || {}
const checkpointPath = input.checkpointPath || ''
// CI control: noCi skips the per-ticket + merge-gate CI; batchTarget (a temp integration
// branch) retargets the phase-1 MRs and is where tickets merge (the end-of-batch CI + merge
// to main is done by the skill after this workflow returns, via `agent batch-branch finalize`).
const noCi = !!input.noCi
const batchTarget = input.batchTarget || ''

const OUTCOME_SCHEMA = {
  type: 'object',
  required: ['ticket_iid', 'project_path', 'status'],
  properties: {
    ticket_iid: { type: 'integer' },
    project_path: { type: 'string' },
    status: { enum: ['success', 'ready_to_merge', 'escalated', 'failed'] },
    mr_iid: { type: ['integer', 'null'] },
    mr_url: { type: ['string', 'null'] },
    escalation_reason: { type: ['string', 'null'] },
  },
}

// Dependency waves (Kahn levels): a wave's tickets have all in-batch blockers in earlier
// waves, i.e. merged before this wave's phase-1 starts. No deps → a single wave (all parallel).
function waves(ordered, edges) {
  const indeg = {}, succ = {}
  for (const r of ordered) { indeg[r] = 0; succ[r] = [] }
  for (const e of edges) {
    if (indeg[e.blocked] === undefined || indeg[e.blocker] === undefined) continue
    indeg[e.blocked]++
    succ[e.blocker].push(e.blocked)
  }
  const out = []
  let cur = ordered.filter((r) => indeg[r] === 0)
  const seen = new Set(cur)
  while (cur.length) {
    out.push(cur)
    const next = []
    for (const n of cur) for (const m of succ[n]) { if (--indeg[m] === 0 && !seen.has(m)) { seen.add(m); next.push(m) } }
    cur = next
  }
  return out
}

async function inBatches(items, cap, fn) {
  const out = []
  for (let i = 0; i < items.length; i += cap) {
    const chunk = await parallel(items.slice(i, i + cap).map((x) => () => fn(x)))
    out.push(...chunk)
  }
  return out
}

const iidOf = (ref) => parseInt(ref.split('#')[1], 10)
const projectOf = (ref) => ref.split('#')[0]

const phase1Flags = `--approve=auto --stop-before-merge${noCi ? ' --no-ci' : ''}${batchTarget ? ` --target-branch ${batchTarget}` : ''}`

function phase1Prompt(ref) {
  return `Run \`/code-autopilot ${webUrl[ref]} ${phase1Flags}\` to completion in this
isolated worktree: implement the issue, run the review loop${noCi ? '' : ', wait for a GREEN CI pipeline'}, approve the MR,
then STOP before merging.${noCi ? '' : ' If a step waits on a pipeline, block until it is terminal — do not stop early.'}
Return ONLY the AUTOPILOT_RESULT footer JSON (status will be "ready_to_merge" on success, else "escalated"/"failed").`
}

const ckptStep = (n) =>
  checkpointPath ? `\n${n}. Append it to the checkpoint: \`echo '<FINAL>' | pysae-ai-tools agent checkpoint append --path ${checkpointPath}\`.` : ''

// Merge + finalise a ready-to-merge ticket, all in one step so labels/checkpoint reflect
// reality the moment the merge lands (not in a bulk pass after the whole batch).
function mergePrompt(ref, outcome) {
  const project = projectOf(ref)
  const iid = iidOf(ref)
  return `Merge this ready-to-merge MR, re-validated against the current main, then finalise it. Steps:
1. Run: \`echo '${JSON.stringify(outcome)}' | pysae-ai-tools agent merge-gate --strategy ${mergeStrategy}${noCi ? ' --no-ci' : ''}\`
2. If that outcome is "escalated" with an escalation_reason containing "rebase conflict": run
   \`/mr-rebase !${outcome.mr_iid} --rebase-only\` (auto-resolve + push), then re-run step 1. If
   /mr-rebase itself fails, keep the escalated outcome. Call the result FINAL.
3. Finalise the label from FINAL's status:
   - success → \`pysae-ai-tools agent label done ${project} ${iid}\`${noCi ? ' (post-merge CI is disabled/deferred this run — do NOT run watch-deploy).' : `, then re-validate the deploy: \`FINAL=$(echo '<FINAL>' | pysae-ai-tools agent watch-deploy)\` (may demote success→escalated; do NOT re-label to blocked if it demotes — keep the label cleared, just carry the demoted FINAL).`}
   - escalated/failed → \`pysae-ai-tools agent label block ${project} ${iid} --reason "<FINAL.escalation_reason>"\`.${ckptStep(4)}
Return ONLY the FINAL outcome JSON.`
}

// Finalise a ticket that never became mergeable (phase-1 escalated/failed) — block + checkpoint,
// in real time, right when its fate is known.
function blockPrompt(ref, outcome) {
  return `This ticket did not reach a mergeable state (phase 1: ${outcome.status}). Finalise it:
1. \`pysae-ai-tools agent label block ${projectOf(ref)} ${iidOf(ref)} --reason "${(outcome.escalation_reason || 'phase 1 did not converge').replace(/"/g, "'")}"\`.${ckptStep(2).replace('<FINAL>', JSON.stringify(outcome))}
Return ONLY this outcome JSON unchanged: ${JSON.stringify(outcome)}`
}

const results = []
const merged = new Set()

for (const [w, wave] of waves(plan.ordered, plan.edges).entries()) {
  log(`Wave ${w + 1}: ${wave.length} ticket(s) — phase 1 in parallel (concurrency ${concurrency})`)

  // Phase 1 — parallel, isolated worktrees, capped at `concurrency`.
  const phase1 = await inBatches(wave, concurrency, (ref) =>
    agent(phase1Prompt(ref), { label: `impl:${ref}`, phase: 'Implement', isolation: 'worktree', schema: OUTCOME_SCHEMA })
      .then((o) => ({ ref, outcome: o }))
      .catch(() => ({ ref, outcome: { ticket_iid: iidOf(ref), project_path: projectOf(ref), status: 'failed', mr_iid: null, mr_url: null, escalation_reason: 'phase-1 agent crashed' } })),
  )

  // Merge — strictly serial (one merge to main at a time), each re-validated on the current main
  // and FINALISED in place (label + checkpoint) so the board/checkpoint track reality live.
  for (const { ref, outcome } of phase1) {
    if (!outcome || outcome.status !== 'ready_to_merge') {
      const finalized = await agent(blockPrompt(ref, outcome), { label: `finalize:${ref}`, phase: 'Merge', schema: OUTCOME_SCHEMA })
      results.push(finalized || outcome)
      log(`${ref} — ${(finalized || outcome).status} (not merged, finalised)`)
      continue
    }
    const finalOutcome = await agent(mergePrompt(ref, outcome), { label: `merge:${ref}`, phase: 'Merge', schema: OUTCOME_SCHEMA })
    results.push(finalOutcome)
    if (finalOutcome.status === 'success') { merged.add(ref); log(`${ref} — merged (!${finalOutcome.mr_iid})`) }
    else log(`${ref} — ${finalOutcome.status}: ${finalOutcome.escalation_reason || ''}`)
  }
}

return { outcomes: results }
