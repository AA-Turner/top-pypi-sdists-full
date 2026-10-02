//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamIdOnboardingState`.

/// Tri-state flag describing an application's onboarding progress onto the
/// stream-ID cache/lookup feature, controlling whether missing-stream-ID
/// conditions are treated as hard errors or soft/best-effort.
///
/// - `NotOnboarded` short-circuits [`StreamIdCache::get`](super::StreamIdCache::get)
///   to always return `None` without calling into the cache manager.
/// - `Onboarded` is the only state where a missing/unresolvable stream ID is
///   escalated to an error.
/// - `InTransition` (and `NotOnboarded` for logging purposes) behaves leniently.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum StreamIdOnboardingState {
    NotOnboarded,
    InTransition,
    Onboarded,
}
