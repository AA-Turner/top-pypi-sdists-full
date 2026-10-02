//! Port of `software.amazon.kinesis.retrieval.AWSExceptionManager`.
//!
//! The Java class traverses a `Throwable`'s class inheritance chain looking for
//! a registered mapping function that converts the throwable into a
//! `RuntimeException`; if none is found the default function is applied. It is
//! used by `CloudWatchMetricsPublisher` to pass a `CloudWatchException` through
//! unchanged while wrapping any other cause in a generic `RuntimeException`.
//!
//! Rust has no exception class hierarchy to walk, so the faithful analog is a
//! registry of typed handlers keyed on a caller-supplied predicate over a boxed
//! error. Each handler decides whether it matches the concrete error and, if so,
//! maps it into a boxed error to (re)throw. When no handler matches, the default
//! function is applied. This keeps the behavior — first matching registration
//! wins, otherwise fall back to the default — while remaining idiomatic Rust.

/// A boxed, thread-safe error, standing in for a Java `Throwable`.
pub type BoxError = Box<dyn std::error::Error + Send + Sync + 'static>;

type Matcher = Box<dyn Fn(&BoxError) -> bool + Send + Sync>;
type Mapper = Box<dyn Fn(BoxError) -> BoxError + Send + Sync>;

/// Dispatches an error-cause to a registered handler, mirroring the Java
/// `AWSExceptionManager`.
///
/// Handlers are consulted in registration order; the first whose matcher accepts
/// the error maps it. If none match, [`default_function`](Self::default_function)
/// is applied (by default an identity pass-through, since Rust has no distinct
/// "wrap in RuntimeException" step — the error is already a boxed error).
pub struct AwsExceptionManager {
    handlers: Vec<(Matcher, Mapper)>,
    default_function: Mapper,
}

impl Default for AwsExceptionManager {
    fn default() -> Self {
        Self::new()
    }
}

impl AwsExceptionManager {
    /// Creates a manager with an identity default function.
    ///
    /// Java's default is `RuntimeException::new`, which wraps the cause. In Rust
    /// the cause is already a boxed error, so the faithful default simply passes
    /// it through unchanged.
    pub fn new() -> Self {
        Self {
            handlers: Vec::new(),
            default_function: Box::new(|t| t),
        }
    }

    /// Registers a handler: `matcher` decides whether an error is of the type
    /// this handler cares about (Java's class/superclass match), and `mapper`
    /// converts it (Java's `Function<T, RuntimeException>`).
    ///
    /// Mirrors Java `add(Class<T>, Function<T, RuntimeException>)`.
    pub fn add<M, F>(&mut self, matcher: M, mapper: F)
    where
        M: Fn(&BoxError) -> bool + Send + Sync + 'static,
        F: Fn(BoxError) -> BoxError + Send + Sync + 'static,
    {
        self.handlers.push((Box::new(matcher), Box::new(mapper)));
    }

    /// Sets the default function applied when no handler matches (Java's
    /// `defaultFunction` fluent setter).
    pub fn set_default_function<F>(&mut self, f: F)
    where
        F: Fn(BoxError) -> BoxError + Send + Sync + 'static,
    {
        self.default_function = Box::new(f);
    }

    /// Applies the first matching handler to `t`, or the default function if
    /// none match. Mirrors Java `apply(Throwable)`.
    pub fn apply(&self, t: BoxError) -> BoxError {
        for (matcher, mapper) in &self.handlers {
            if matcher(&t) {
                return mapper(t);
            }
        }
        (self.default_function)(t)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fmt;

    #[derive(Debug)]
    struct SpecificError(&'static str);
    impl fmt::Display for SpecificError {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "{}", self.0)
        }
    }
    impl std::error::Error for SpecificError {}

    #[derive(Debug)]
    struct OtherError;
    impl fmt::Display for OtherError {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "other")
        }
    }
    impl std::error::Error for OtherError {}

    #[test]
    fn matching_handler_maps_error() {
        let mut mgr = AwsExceptionManager::new();
        mgr.add(
            |e| e.downcast_ref::<SpecificError>().is_some(),
            |_e| Box::new(SpecificError("mapped")) as BoxError,
        );
        let out = mgr.apply(Box::new(SpecificError("in")));
        assert_eq!(out.to_string(), "mapped");
    }

    #[test]
    fn passes_through_registered_type_unchanged() {
        // Mirrors CW_EXCEPTION_MANAGER.add(CloudWatchException.class, t -> t).
        let mut mgr = AwsExceptionManager::new();
        mgr.add(|e| e.downcast_ref::<SpecificError>().is_some(), |e| e);
        let out = mgr.apply(Box::new(SpecificError("keep")));
        assert!(out.downcast_ref::<SpecificError>().is_some());
    }

    #[test]
    fn unmatched_uses_default_function() {
        let mut mgr = AwsExceptionManager::new();
        mgr.add(|e| e.downcast_ref::<SpecificError>().is_some(), |e| e);
        let out = mgr.apply(Box::new(OtherError));
        // Default is identity pass-through.
        assert!(out.downcast_ref::<OtherError>().is_some());
    }

    // Port of AWSExceptionManagerTest.testParentException. Java relies on a
    // class-hierarchy walk (most-specific ancestor wins). Rust has no exception
    // hierarchy, so the matcher model resolves precedence by registration order
    // (first match wins) — the caller registers the most-specific matcher first,
    // which is what a correct hierarchy walk would select.
    #[test]
    fn parent_exception_most_specific_matcher_wins() {
        let mut mgr = AwsExceptionManager::new();
        // Most-specific first: the SpecificError matcher precedes the broad one.
        mgr.add(
            |e| e.downcast_ref::<SpecificError>().is_some(),
            |_e| Box::new(SpecificError("specific-handled")) as BoxError,
        );
        mgr.add(
            // A broad "any error" matcher standing in for `Exception.class`.
            |_e| true,
            |_e| Box::new(SpecificError("broad-handled")) as BoxError,
        );
        let out = mgr.apply(Box::new(SpecificError("in")));
        assert_eq!(out.to_string(), "specific-handled");
    }

    // Port of AWSExceptionManagerTest.testDefaultHandler: no matcher accepts a
    // StackOverflowError-analog, so the (customized) default function runs.
    #[test]
    fn default_handler_runs_when_no_matcher_accepts() {
        let mut mgr = AwsExceptionManager::new();
        mgr.set_default_function(|_e| Box::new(SpecificError("default-marker")) as BoxError);
        mgr.add(|e| e.downcast_ref::<SpecificError>().is_some(), |e| e);
        let out = mgr.apply(Box::new(OtherError));
        assert_eq!(out.to_string(), "default-marker");
    }
}
