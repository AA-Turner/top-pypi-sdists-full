//! Test helpers for worker-metric unit tests.
//!
//! Port of `software.amazon.kinesis.worker.metric.WorkerMetricsTestUtils`
//! (`writeLineToFile`) plus small temp-dir helpers standing in for JUnit's
//! `@TempDir`.

use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

static COUNTER: AtomicU64 = AtomicU64::new(0);

/// Create (and return) a unique temp directory for a test. Mirrors JUnit
/// `@TempDir` — a fresh, isolated directory per use.
pub fn temp_dir(tag: &str) -> PathBuf {
    let n = COUNTER.fetch_add(1, Ordering::SeqCst);
    let dir = std::env::temp_dir().join(format!("kcl-worker-{}-{}-{}", tag, std::process::id(), n));
    std::fs::create_dir_all(&dir).unwrap();
    dir
}

/// Remove a temp directory tree, ignoring errors.
pub fn cleanup(dir: &Path) {
    std::fs::remove_dir_all(dir).ok();
}

/// Write `line` to `file`, overwriting (Java `WorkerMetricsTestUtils.writeLineToFile`).
pub fn write_line_to_file(file: &Path, line: &str) {
    std::fs::write(file, line).unwrap();
}
