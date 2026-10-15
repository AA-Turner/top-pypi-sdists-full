//! Bounded parallelism for registry operations.
//!
//! Registry operations parse, validate and write documents with rayon. By
//! default that runs on rayon's global pool (one thread per core), so a
//! single read fans out across the whole machine. When many processes share
//! a host — e.g. dozens of agents each holding a registry — every one of
//! them spinning up all-core parallelism only adds scheduling overhead:
//! measured at 100k units, an all-core read burns 1.5–3× the CPU of the
//! same read on one thread.
//!
//! [`THREADS_ENV_VAR`] caps it: `N` runs every registry operation on a
//! dedicated pool of `N` threads (`1` = effectively sequential). Unset,
//! empty, or `0` keeps the global pool. The variable is read once per
//! process, at the first registry operation.
//!
//! # Callers on other rayon pools
//!
//! A registry operation called from a worker thread of *another* rayon pool
//! (the caller's own `par_iter`, say) must not run its parallel work there,
//! and must not `install` into our pool either. Both make the caller's worker
//! wait by *working*: it picks up the caller's other queued jobs, which can
//! re-enter the caller's own state (a `OnceLock` being initialized, a lock
//! held further down the same stack) and deadlock, and with every worker
//! inside registry calls nothing is left to run the parallel parts. Such
//! calls are instead handed to a registry pool through a short-lived plain
//! thread while the caller's worker *parks* (blocks without stealing). With
//! no pool configured, a default-sized registry pool is created on first use
//! for these callers only. Operations nested inside a registry operation
//! (already on a registry pool thread) run inline.

use std::sync::OnceLock;

use crate::error::*;

/// Environment variable limiting how many threads a registry operation may
/// use. See the module docs.
pub const THREADS_ENV_VAR: &str = "SCAI_REGISTRY_THREADS";

type PoolResult<T> = std::result::Result<T, String>;

/// The configured pool: `Ok(None)` = rayon's global pool; `Err` = invalid
/// setting, reported by every operation.
static POOL: OnceLock<PoolResult<Option<rayon::ThreadPool>>> = OnceLock::new();

/// Default-sized registry pool for callers on another rayon pool's thread
/// when no pool is configured (see the module docs).
static FALLBACK_POOL: OnceLock<PoolResult<rayon::ThreadPool>> = OnceLock::new();

/// Run a registry operation on the right thread pool (see the module docs).
pub(crate) fn run<T: Send>(f: impl FnOnce() -> Result<T> + Send) -> Result<T> {
    let configured = match POOL.get_or_init(build_pool) {
        Ok(pool) => pool.as_ref(),
        Err(message) => return Err(Error::validation(message.clone())),
    };
    let fallback = FALLBACK_POOL.get().and_then(|pool| pool.as_ref().ok());
    // Nested inside a registry operation: already on a registry pool thread.
    if configured
        .into_iter()
        .chain(fallback)
        .any(|pool| pool.current_thread_index().is_some())
    {
        return f();
    }
    let on_foreign_pool = rayon::current_thread_index().is_some();
    match (configured, on_foreign_pool) {
        (None, false) => f(),
        (Some(pool), false) => pool.install(with_caller_hooks(f)),
        (configured, true) => {
            let pool = match configured {
                Some(pool) => pool,
                None => FALLBACK_POOL
                    .get_or_init(|| build_sized_pool(None))
                    .as_ref()
                    .map_err(|message| Error::validation(message.clone()))?,
            };
            let f = with_caller_hooks(f);
            // A plain thread blocks inside `install` without stealing; the
            // caller's worker parks in `join` without stealing either.
            std::thread::scope(|scope| scope.spawn(|| pool.install(f)).join())
                .unwrap_or_else(|panic| std::panic::resume_unwind(panic))
        }
    }
}

/// Test hooks are thread-local; carry the caller's onto whichever thread
/// runs `f`. Must be called on the caller's thread.
fn with_caller_hooks<T>(f: impl FnOnce() -> T + Send) -> impl FnOnce() -> T + Send {
    #[cfg(test)]
    let f = {
        let hooks = super::test_hooks::snapshot();
        move || super::test_hooks::with_snapshot(hooks, f)
    };
    f
}

fn build_pool() -> PoolResult<Option<rayon::ThreadPool>> {
    let value = std::env::var(THREADS_ENV_VAR).ok();
    match parse_threads(value.as_deref())? {
        Some(threads) => build_sized_pool(Some(threads)).map(Some),
        None => Ok(None),
    }
}

/// A registry pool of `threads` threads (`None` = rayon's default size).
fn build_sized_pool(threads: Option<usize>) -> PoolResult<rayon::ThreadPool> {
    rayon::ThreadPoolBuilder::new()
        .num_threads(threads.unwrap_or(0))
        .thread_name(|i| format!("scai-registry-{i}"))
        .build()
        .map_err(|e| format!("{THREADS_ENV_VAR}: failed to start thread pool: {e}"))
}

/// Parse the setting: `None` = use the global pool.
fn parse_threads(value: Option<&str>) -> std::result::Result<Option<usize>, String> {
    let Some(value) = value.map(str::trim).filter(|v| !v.is_empty()) else {
        return Ok(None);
    };
    match value.parse::<usize>() {
        Ok(0) => Ok(None),
        Ok(n) => Ok(Some(n)),
        Err(_) => Err(format!(
            "{THREADS_ENV_VAR}: expected a non-negative integer thread count, got '{value}'"
        )),
    }
}

#[cfg(test)]
mod tests {
    use super::parse_threads;

    #[test]
    fn parses_thread_counts() {
        assert_eq!(parse_threads(None), Ok(None));
        assert_eq!(parse_threads(Some("")), Ok(None));
        assert_eq!(parse_threads(Some("  ")), Ok(None));
        assert_eq!(parse_threads(Some("0")), Ok(None));
        assert_eq!(parse_threads(Some("1")), Ok(Some(1)));
        assert_eq!(parse_threads(Some(" 4 ")), Ok(Some(4)));
        for bad in ["-1", "two", "1.5", "4 threads"] {
            let err = parse_threads(Some(bad)).unwrap_err();
            assert!(err.contains("SCAI_REGISTRY_THREADS"), "{bad}: {err}");
        }
    }
}
