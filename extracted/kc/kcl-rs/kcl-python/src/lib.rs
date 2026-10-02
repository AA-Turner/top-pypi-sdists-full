//! Python bindings for the Rust KCL port (native module `kcl_rs._native`).
//!
//! # Design: control from Python, everything else GIL-free
//!
//! The Rust KCL runs on its **own** multi-threaded tokio runtime, on background
//! threads, without holding the Python GIL. Python code only:
//!   1. constructs configuration and starts a [`Scheduler`], and
//!   2. supplies a `RecordProcessor` whose lifecycle callbacks
//!      (`initialize`, `process_records`, `lease_lost`, `shard_ended`,
//!      `shutdown_requested`) are invoked from Rust — acquiring the GIL only for
//!      the duration of each callback.
//!
//! The public Python interface mirrors `amazon_kclpy` (v3 `RecordProcessorBase`,
//! the `*Input` message types, `Record`, and `Checkpointer` / `CheckpointError`).
//!
//! ## GIL / runtime model (as implemented)
//!
//! * The core scheduler drive runs inside `Python::allow_threads` (GIL released)
//!   on a dedicated tokio runtime — see [`scheduler`].
//! * The core lifecycle invokes the **synchronous** `ShardRecordProcessor` trait
//!   via `spawn_blocking` (off the tokio worker threads). The bridge
//!   ([`processor::PyRecordProcessor`]) acquires the GIL (`Python::with_gil`)
//!   only for the brief span of each Python callback, then releases it.
//! * `Checkpointer::checkpoint` releases the GIL while the synchronous Rust
//!   checkpoint runs (which may hit DynamoDB via a sync→async bridge).
//!
//! The pure-Python shim package (`python/kcl_rs/`) re-exports these classes
//! and provides the `RecordProcessorBase` abstract base users subclass.
//!
//! ## Logging
//!
//! The core (`kcl`) crate logs retrieval/lifecycle failures via `tracing::`,
//! but never installs a subscriber itself -- without one, every core log is
//! silently dropped, which is exactly what made a field failure (a polling
//! consumer that acquired its lease and then never polled, with the
//! definitive error unknowable) invisible to Python users. Importing this
//! module installs a default subscriber: `WARN` and above, to stderr,
//! overridable via the `RUST_LOG` env var (e.g. `RUST_LOG=kcl=debug`). It uses
//! `try_init` and never overrides an existing global subscriber, so an
//! embedder or test harness that installs its own is respected.

use pyo3::prelude::*;
use tracing_subscriber::EnvFilter;

mod checkpointer;
mod inputs;
mod processor;
mod record;
mod scheduler;
mod stream_tracker;

pub use checkpointer::{checkpoint_error, Checkpointer, PreparedCheckpointer};
pub use processor::{PyRecordProcessor, PyRecordProcessorFactory};
pub use record::Record;
pub use scheduler::Scheduler;

/// Native Rust KCL bindings (kcl_rs).
///
/// Importing this module installs a default `tracing` subscriber (`WARN` and
/// above, stderr, `RUST_LOG`-overridable) so core log output -- most
/// importantly retrieval/lifecycle failure diagnostics -- is visible by
/// default instead of silently dropped. See the crate-level docs' "Logging"
/// section.
// The doc comment above becomes the module's `__doc__` (adding it via
// `m.add("__doc__", ...)` would also leak "__doc__" into the auto-generated
// `__all__`, which trips `mypy.stubtest` against `_native.pyi`).
#[pymodule]
fn _native(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Default-warn, RUST_LOG-overridable, stderr subscriber. `try_init` is a
    // no-op (returns Err, ignored) if a global subscriber is already installed
    // -- e.g. an embedding application, or a test harness -- so we never
    // clobber one that's already there.
    let _ = tracing_subscriber::fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("warn")),
        )
        .with_writer(std::io::stderr)
        .try_init();

    // Input message types (mirror amazon_kclpy.messages).
    m.add_class::<inputs::InitializeInput>()?;
    m.add_class::<inputs::ProcessRecordsInput>()?;
    m.add_class::<inputs::LeaseLostInput>()?;
    m.add_class::<inputs::ShardEndedInput>()?;
    m.add_class::<inputs::ShutdownRequestedInput>()?;
    m.add_class::<record::Record>()?;

    // Checkpointing (mirror amazon_kclpy.kcl.Checkpointer / CheckpointError).
    m.add_class::<checkpointer::Checkpointer>()?;
    m.add_class::<checkpointer::PreparedCheckpointer>()?;
    m.add(
        "CheckpointError",
        m.py().get_type::<checkpointer::CheckpointError>(),
    )?;

    // The control surface.
    m.add_class::<scheduler::Scheduler>()?;

    Ok(())
}

#[cfg(test)]
mod tests;
