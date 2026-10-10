/** Shared by every Slack report so the wording of a runner cannot drift between them. */
const DESCRIPTIONS = {
  wait_write:
    "start a run and wait for its result (run execution and checkpointing)",
  stream_write: "start a run and read its event stream to the end (streaming)",
  threads_search_metadata:
    "create, update, search and delete threads by metadata (database and metadata search)",
  thread_runs_metadata_search: "create a run and search it back by run metadata",
  threads: "create, read, update, count and delete a thread (thread CRUD)",
  assistants: "create, read, update and delete assistants (assistant CRUD)",
  store: "write, read, verify and delete one Store item (the Store)",
  enqueued_runs_order:
    "enqueue several runs on one thread and check they complete in order",
  cancel_first_second_completes:
    "start two runs, cancel the first, check the second completes",
  delta_turns:
    "add one turn per iteration to a long thread and time it by depth (checkpoint read cost)",
  meta_workload: "a random mix of the other runners",
};

const SHORT_NAMES = {
  threads_search_metadata: "threads_search",
  thread_runs_metadata_search: "runs_search",
  cancel_first_second_completes: "cancel_first",
};

// One word each, so the table fits a phone.
const COLUMN_NAMES = {
  wait_write: "wait",
  stream_write: "stream",
  threads_search_metadata: "search",
};

const GLOSSES = {
  wait_write: "run and wait",
  stream_write: "run and stream",
  threads_search_metadata: "thread CRUD + metadata search",
};

export function describeRunner(benchmarkType) {
  return DESCRIPTIONS[benchmarkType] ?? `run the \`${benchmarkType}\` runner`;
}

export function runnerShortName(benchmarkType) {
  return SHORT_NAMES[benchmarkType] ?? String(benchmarkType);
}

export function runnerGloss(benchmarkType) {
  return GLOSSES[benchmarkType] ?? runnerShortName(benchmarkType);
}

export function runnerColumnName(benchmarkType) {
  return COLUMN_NAMES[benchmarkType] ?? runnerShortName(benchmarkType);
}

export function describeRunnerBriefly(benchmarkType) {
  return describeRunner(benchmarkType).replace(/ \([^)]*\)$/, "");
}
