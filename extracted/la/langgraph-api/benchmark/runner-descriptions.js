/** Shared by every Slack report so the wording of a runner cannot drift between them. */
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

export function runnerShortName(benchmarkType) {
  return SHORT_NAMES[benchmarkType] ?? String(benchmarkType);
}

export function runnerColumnName(benchmarkType) {
  return COLUMN_NAMES[benchmarkType] ?? runnerShortName(benchmarkType);
}
