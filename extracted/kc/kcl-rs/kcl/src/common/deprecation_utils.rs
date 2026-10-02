//! Port of `software.amazon.kinesis.common.DeprecationUtils`.
//!
//! Bridges the modern `StreamTracker` abstraction to the deprecated
//! `Either<MultiStreamTracker, String>` convention used by the legacy
//! `ConfigsBuilder.appStreamTracker` / `RetrievalConfig.appStreamTracker` fields.
//!
//! # Deviation from Java
//!
//! Java's `convert(StreamTracker, Function<SingleStreamTracker, R>)` uses runtime
//! `instanceof` to classify an interface value as one of exactly two known
//! implementations. Rust `dyn StreamTracker` cannot be downcast to a concrete
//! type without `Any`, and the arch map recommends modeling this closed set as an
//! idiomatic **sum type** instead of dynamic downcasting. Accordingly this port
//! operates on an explicit [`StreamTrackerKind`] classification, which is the
//! natural Rust representation of "one of `MultiStreamTracker` / `SingleStreamTracker`".
//!
//! This entire utility exists only for the deprecated `appStreamTracker`
//! back-compat surface; the modern code paths expose only the `StreamTracker`
//! equivalent. It is ported for fidelity/testability but is expected to be used
//! only by the (deferred) `ConfigsBuilder` / `RetrievalConfig` waves, if at all.

/// A minimal port of `software.amazon.awssdk.utils.Either<L, R>`: a value that is
/// either `Left(L)` or `Right(R)`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Either<L, R> {
    /// The left variant.
    Left(L),
    /// The right variant.
    Right(R),
}

/// Classification of a `StreamTracker` into the closed set of its two known
/// implementations, replacing Java's `instanceof` dispatch. `Other` models the
/// "unhandled StreamTracker" case that Java rejects with `IllegalArgumentException`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StreamTrackerKind {
    /// A `MultiStreamTracker` (Java `instanceof MultiStreamTracker`).
    Multi,
    /// A `SingleStreamTracker` (Java `instanceof SingleStreamTracker`).
    Single,
    /// Any other `StreamTracker` implementation (Java's `else` branch).
    Other,
}

/// Convert a stream tracker into the deprecated `Either<M, R>` convention.
///
/// Mirrors Java's `convert(StreamTracker, Function<SingleStreamTracker, R>)`:
/// - a multi-stream tracker maps to `Either::Left(multi)`;
/// - a single-stream tracker maps to `Either::Right(converter(single))`;
/// - any other tracker panics (Java `IllegalArgumentException`).
///
/// The `multi` / `single` values are the concrete tracker payloads for the two
/// known kinds; only the one matching `kind` is used.
///
/// # Panics
///
/// Panics with `"Unhandled StreamTracker"` for [`StreamTrackerKind::Other`]
/// (Java throws `IllegalArgumentException`).
pub fn convert<M, S, R>(
    kind: StreamTrackerKind,
    multi: M,
    single: S,
    converter: impl FnOnce(S) -> R,
) -> Either<M, R> {
    match kind {
        StreamTrackerKind::Multi => Either::Left(multi),
        StreamTrackerKind::Single => Either::Right(converter(single)),
        StreamTrackerKind::Other => panic!("Unhandled StreamTracker"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // Port of DeprecationUtilsTest.testTrackerConversion: a multi tracker becomes
    // Either::Left, a single tracker becomes Either::Right(identity(single)).
    #[test]
    fn tracker_conversion() {
        let left: Either<&str, &str> = convert(StreamTrackerKind::Multi, "multi", "single", |s| s);
        assert_eq!(left, Either::Left("multi"));

        let right: Either<&str, &str> =
            convert(StreamTrackerKind::Single, "multi", "single", |s| s);
        assert_eq!(right, Either::Right("single"));
    }

    // Port of DeprecationUtilsTest.testUnsupportedStreamTrackerConversion.
    #[test]
    #[should_panic(expected = "Unhandled StreamTracker")]
    fn unsupported_stream_tracker_conversion() {
        let _: Either<&str, &str> = convert(StreamTrackerKind::Other, "multi", "single", |s| s);
    }

    #[test]
    fn converter_is_applied_to_single() {
        // Right variant runs the converter on the single-tracker payload.
        let r: Either<i32, usize> = convert(StreamTrackerKind::Single, 0, "abc", |s: &str| s.len());
        assert_eq!(r, Either::Right(3));
    }
}
