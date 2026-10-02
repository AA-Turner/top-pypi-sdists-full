//! Flavor-aware sync→async bridge.
//!
//! The KCL's public sync seams (leader deciders, stream-id resolution, consumer
//! ARN registration, the `ShardConsumer` input handler) must drive async work to
//! completion from a synchronous method. On a **multi-thread** runtime the
//! canonical bridge is [`tokio::task::block_in_place`] + `Handle::block_on`; on a
//! **current-thread** runtime `block_in_place` panics, so the future is driven on
//! the target runtime from a short-lived scoped thread instead (legal: a
//! `Handle::block_on` from a non-runtime thread polls the future on that thread,
//! using the handle's runtime only for `spawn`/resources).
//!
//! Production runs multi-threaded (the kcl-python bindings build a multi-thread
//! runtime; the scheduler docs require one for the consumer data path), so the
//! current-thread branch exists to keep library embedders and
//! `#[tokio::test]`-style harnesses from panicking outright.

use std::future::Future;

/// Run `fut` to completion on `handle`'s runtime from a synchronous context.
///
/// * Called on a **multi-thread** runtime worker: `block_in_place` yields the
///   worker, then blocks on `fut` (the canonical bridge).
/// * Called inside a **current-thread** runtime (where `block_in_place` would
///   panic): drive `fut` via `handle.block_on` on a scoped helper thread.
///   Caveat: if `handle` refers to that same (now parked) current-thread
///   runtime, futures needing its timer/IO driver cannot make progress — only
///   coordination futures (channels, `tokio::sync` primitives, `spawn_blocking`)
///   complete. This still strictly dominates the previous behavior (immediate
///   panic).
/// * Called with no ambient runtime: block on `handle` directly.
pub(crate) fn run_sync_on<F>(handle: tokio::runtime::Handle, fut: F) -> F::Output
where
    F: Future + Send,
    F::Output: Send,
{
    match tokio::runtime::Handle::try_current() {
        Ok(current) => match current.runtime_flavor() {
            tokio::runtime::RuntimeFlavor::CurrentThread => {
                std::thread::scope(|s| s.spawn(|| handle.block_on(fut)).join().unwrap())
            }
            _ => tokio::task::block_in_place(|| handle.block_on(fut)),
        },
        Err(_) => handle.block_on(fut),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn bridges_on_multi_thread_runtime() {
        let handle = tokio::runtime::Handle::current();
        let out = tokio::task::spawn_blocking(move || run_sync_on(handle, async { 1 + 1 }))
            .await
            .unwrap();
        assert_eq!(out, 2);
        // Also legal directly on a worker (block_in_place path).
        let handle = tokio::runtime::Handle::current();
        assert_eq!(run_sync_on(handle, async { 40 + 2 }), 42);
    }

    #[tokio::test]
    async fn does_not_panic_on_current_thread_runtime() {
        // Pre-fix, a bare `block_in_place` here panicked. The bridge must
        // complete coordination-only futures.
        let handle = tokio::runtime::Handle::current();
        let (tx, rx) = tokio::sync::oneshot::channel::<u32>();
        tx.send(7).unwrap();
        assert_eq!(run_sync_on(handle, async { rx.await.unwrap() }), 7);
    }

    #[test]
    fn bridges_with_no_ambient_runtime() {
        let rt = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(1)
            .enable_all()
            .build()
            .unwrap();
        assert_eq!(run_sync_on(rt.handle().clone(), async { 5 }), 5);
    }
}
