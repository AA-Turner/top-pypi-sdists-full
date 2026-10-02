//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamIdCache`.
//!
//! Process-global singleton exposing a bare `StreamIdCache::get()` /
//! `get(streamIdentifier)` for retrieving the current stream's Kinesis
//! `streamId` from arbitrary user record-processor code (no threaded reference).
//!
//! # Deviations
//!
//! - **Singleton via `OnceLock`.** Java uses a `static volatile StreamIdCache`
//!   set once at Scheduler startup. Rust uses a `std::sync::RwLock<Option<...>>`
//!   guarding an `Arc<StreamIdCache>` (a `reset()` test seam is needed, which a
//!   plain `OnceLock` cannot provide). This matches the "one Scheduler per
//!   process" contract; the `initialize()`-once guard mirrors Java's benign
//!   check-then-act.
//! - **Sync resolver.** `StreamIdCache::get()` must be callable from sync user
//!   code, but [`StreamIdCacheManager::get`](super::StreamIdCacheManager::get) is
//!   async. So the cache holds a sync [`StreamIdResolver`] trait object
//!   (`#[automock]` for the tests, which mock the manager's `get`). The
//!   [`StreamIdCacheResolverBridge`] (wired by the Scheduler in wave 10d) adapts
//!   the async manager to this sync interface by blocking on a
//!   `tokio::runtime::Handle` — the async→sync bridge.

use std::sync::{Arc, RwLock};

use crate::common::StreamIdentifier;
use crate::coordinator::stream_info::stream_id_cache_manager::StreamIdCacheManager;
use crate::coordinator::stream_info::StreamIdOnboardingState;
use crate::leases::exceptions::LeasingError;

/// Sync resolver of a `streamId` for a stream. The real
/// [`StreamIdCacheManager`](super::StreamIdCacheManager) is async; a wave-10d
/// bridge adapts it to this sync interface. Modeled as a trait so the ported
/// [`StreamIdCache`] tests mock it (as the Java tests mock `StreamIdCacheManager`).
#[cfg_attr(test, mockall::automock)]
pub trait StreamIdResolver: Send + Sync {
    /// Analogue of `StreamIdCacheManager.get(StreamIdentifier)`.
    // Owned `Option<StreamIdentifier>` (not `Option<&_>`): `mockall::automock`
    // cannot synthesize a lifetime for a reference nested inside `Option`.
    // `StreamIdentifier` is cheap to clone at this (rare) call site.
    fn get(
        &self,
        stream_identifier: Option<StreamIdentifier>,
    ) -> Result<Option<String>, LeasingError>;
}

/// Async→sync bridge adapting an async [`StreamIdCacheManager`] to the sync
/// [`StreamIdResolver`] the process-global [`StreamIdCache`] exposes to arbitrary
/// (sync) user record-processor code.
///
/// The Scheduler owns the [`StreamIdCacheManager`] and, at `initialize()` time,
/// wraps it in this bridge and passes it to [`StreamIdCache::initialize`]. The
/// bridge holds a `tokio::runtime::Handle` and, on each sync `get`, drives the
/// manager's async `get` to completion via
/// [`tokio::task::block_in_place`] + `Handle::block_on` (the same
/// blocking-from-async pattern the lifecycle wave uses; requires a multi-thread
/// runtime).
pub struct StreamIdCacheResolverBridge {
    cache_manager: Arc<StreamIdCacheManager>,
    handle: tokio::runtime::Handle,
}

impl StreamIdCacheResolverBridge {
    /// Build a bridge over the given manager, capturing the current tokio runtime
    /// handle (the Scheduler constructs this inside its runtime).
    pub fn new(cache_manager: Arc<StreamIdCacheManager>) -> Self {
        Self {
            cache_manager,
            handle: tokio::runtime::Handle::current(),
        }
    }

    /// Build a bridge with an explicit runtime handle (for tests / non-current
    /// runtime construction).
    pub fn with_handle(
        cache_manager: Arc<StreamIdCacheManager>,
        handle: tokio::runtime::Handle,
    ) -> Self {
        Self {
            cache_manager,
            handle,
        }
    }
}

impl StreamIdResolver for StreamIdCacheResolverBridge {
    fn get(
        &self,
        stream_identifier: Option<StreamIdentifier>,
    ) -> Result<Option<String>, LeasingError> {
        let cache_manager = Arc::clone(&self.cache_manager);
        let handle = self.handle.clone();
        // Block on the async manager (flavor-aware bridge: yields a multi-thread
        // worker; no panic on a current-thread runtime).
        crate::utils::sync_bridge::run_sync_on(handle, async move {
            cache_manager.get(stream_identifier.as_ref()).await
        })
    }
}

static INSTANCE: RwLock<Option<Arc<StreamIdCache>>> = RwLock::new(None);

/// Process-global singleton facade. Java `StreamIdCache`.
///
/// # Process-global caveat (multiple Schedulers in one process)
///
/// Like Java's static `StreamIdCache`, this singleton is initialized by the
/// **first** Scheduler and only that once: the installed resolver bridge
/// captures that Scheduler's runtime `Handle` and AWS clients. With the default
/// `NotOnboarded` state every read short-circuits to `None` before touching the
/// resolver, so co-hosted Schedulers (e.g. parallel `#[tokio::test]`s) are
/// unaffected. In `Onboarded`/`Onboarding` mode, however, a second Scheduler in
/// the same process would resolve through the FIRST Scheduler's runtime and
/// clients — and through a dead runtime once that test/scheduler exits. Run one
/// onboarded Scheduler per process (the Java daemon model) until per-scheduler
/// scoping is introduced.
pub struct StreamIdCache {
    cache_manager: Arc<dyn StreamIdResolver>,
    onboarding_state: StreamIdOnboardingState,
}

impl StreamIdCache {
    /// Java `initialize(cacheManager, onboardingState)` — only takes effect on
    /// the first call.
    pub fn initialize(
        cache_manager: Arc<dyn StreamIdResolver>,
        onboarding_state: StreamIdOnboardingState,
    ) {
        let mut guard = INSTANCE.write().expect("StreamIdCache lock poisoned");
        if guard.is_none() {
            *guard = Some(Arc::new(StreamIdCache {
                cache_manager,
                onboarding_state,
            }));
        }
    }

    /// Java `getInstance()`.
    ///
    /// # Panics
    /// Panics (Java `IllegalStateException`) if not yet initialized.
    pub fn get_instance() -> Arc<StreamIdCache> {
        INSTANCE
            .read()
            .expect("StreamIdCache lock poisoned")
            .clone()
            .unwrap_or_else(|| panic!("StreamIdCache has not been initialized"))
    }

    /// The current onboarding state (Java Lombok getter `getOnboardingState()`).
    pub fn onboarding_state(&self) -> StreamIdOnboardingState {
        self.onboarding_state
    }

    /// Java `static String get()` — single-stream-mode convenience
    /// (`get(null)`).
    pub fn get() -> Option<String> {
        Self::get_for(None)
    }

    /// Java `static String get(StreamIdentifier)`. Returns `None` if not
    /// onboarded or not found; re-raises as a panic (Java `RuntimeException`)
    /// only in `Onboarded` mode.
    ///
    /// # Panics
    /// Panics if not yet initialized, or (in `Onboarded` mode) if the underlying
    /// resolver errors.
    pub fn get_for(stream_identifier: Option<&StreamIdentifier>) -> Option<String> {
        let instance = {
            let guard = INSTANCE.read().expect("StreamIdCache lock poisoned");
            guard
                .clone()
                .unwrap_or_else(|| panic!("StreamIdCache has not been initialized"))
        };
        if instance.onboarding_state == StreamIdOnboardingState::NotOnboarded {
            return None;
        }
        match instance.cache_manager.get(stream_identifier.cloned()) {
            Ok(v) => v,
            Err(e) => {
                if instance.onboarding_state == StreamIdOnboardingState::Onboarded {
                    panic!("Error getting stream ID {stream_identifier:?}: {e}");
                }
                tracing::info!(error = %e, "Error getting stream ID but it will be retried");
                None
            }
        }
    }

    /// Like [`get_for`](Self::get_for) but returns `None` (instead of panicking)
    /// when the singleton has not been initialized.
    ///
    /// Used by the retrieval layer to populate the `streamId` request field:
    /// before the Scheduler initializes the cache (or in retrieval unit tests
    /// that never initialize it), this yields `None` and the request field is
    /// left unset — the common Java path where `StreamIdCache` is uninitialized.
    /// Once the Scheduler has initialized the cache this behaves exactly like
    /// [`get_for`](Self::get_for).
    pub fn try_get_for(stream_identifier: Option<&StreamIdentifier>) -> Option<String> {
        let is_initialized = {
            let guard = INSTANCE.read().expect("StreamIdCache lock poisoned");
            guard.is_some()
        };
        if is_initialized {
            Self::get_for(stream_identifier)
        } else {
            None
        }
    }

    /// Test-only: reset the singleton. Java `@VisibleForTesting reset()`.
    #[cfg(test)]
    pub fn reset() {
        *INSTANCE.write().expect("StreamIdCache lock poisoned") = None;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // These tests share the process-global singleton, so they must run
    // sequentially (a shared mutex serializes them).
    use std::sync::Mutex as StdMutex;
    static TEST_LOCK: StdMutex<()> = StdMutex::new(());

    fn stream_identifier() -> StreamIdentifier {
        StreamIdentifier::single_stream_instance("test-stream")
    }

    fn resolver_returning(
        value: Result<Option<String>, LeasingError>,
    ) -> Arc<dyn StreamIdResolver> {
        let mut m = MockStreamIdResolver::new();
        m.expect_get().returning(move |_| match &value {
            Ok(v) => Ok(v.clone()),
            Err(_) => Err(LeasingError::dependency("Cache error")),
        });
        Arc::new(m)
    }

    #[test]
    fn get_instance_when_not_initialized_panics() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        let r = std::panic::catch_unwind(StreamIdCache::get_instance);
        assert!(r.is_err());
    }

    #[test]
    fn initialize_only_once() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Ok(None)),
            StreamIdOnboardingState::Onboarded,
        );
        // Re-initialize without reset is ignored.
        StreamIdCache::initialize(
            resolver_returning(Ok(None)),
            StreamIdOnboardingState::InTransition,
        );
        assert_eq!(
            StreamIdCache::get_instance().onboarding_state(),
            StreamIdOnboardingState::Onboarded
        );
    }

    #[test]
    fn get_when_not_onboarded_returns_none_without_calling_resolver() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        let mut m = MockStreamIdResolver::new();
        m.expect_get().never();
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::NotOnboarded);
        assert_eq!(StreamIdCache::get_for(Some(&stream_identifier())), None);
    }

    #[test]
    fn get_when_onboarded_returns_value() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Ok(Some("stream-id-123".to_string()))),
            StreamIdOnboardingState::Onboarded,
        );
        assert_eq!(
            StreamIdCache::get_for(Some(&stream_identifier())),
            Some("stream-id-123".to_string())
        );
    }

    #[test]
    fn get_when_onboarded_returns_none() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Ok(None)),
            StreamIdOnboardingState::Onboarded,
        );
        assert_eq!(StreamIdCache::get_for(Some(&stream_identifier())), None);
    }

    #[test]
    fn get_when_in_transition_returns_value() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Ok(Some("stream-id-123".to_string()))),
            StreamIdOnboardingState::InTransition,
        );
        assert_eq!(
            StreamIdCache::get_for(Some(&stream_identifier())),
            Some("stream-id-123".to_string())
        );
    }

    #[test]
    fn get_with_exception_when_onboarded_panics() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Err(LeasingError::dependency("Cache error"))),
            StreamIdOnboardingState::Onboarded,
        );
        let r = std::panic::catch_unwind(|| StreamIdCache::get_for(Some(&stream_identifier())));
        assert!(r.is_err());
    }

    #[test]
    fn get_with_exception_when_in_transition_returns_none() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Err(LeasingError::dependency("Cache error"))),
            StreamIdOnboardingState::InTransition,
        );
        assert_eq!(StreamIdCache::get_for(Some(&stream_identifier())), None);
    }

    #[test]
    fn get_with_null_identifier_onboarded() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        StreamIdCache::initialize(
            resolver_returning(Ok(Some("stream-id-123".to_string()))),
            StreamIdOnboardingState::Onboarded,
        );
        assert_eq!(StreamIdCache::get(), Some("stream-id-123".to_string()));
    }

    #[test]
    fn get_with_null_identifier_not_onboarded_returns_none() {
        let _g = TEST_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        StreamIdCache::reset();
        let mut m = MockStreamIdResolver::new();
        m.expect_get().never();
        StreamIdCache::initialize(Arc::new(m), StreamIdOnboardingState::NotOnboarded);
        assert_eq!(StreamIdCache::get(), None);
    }
}
