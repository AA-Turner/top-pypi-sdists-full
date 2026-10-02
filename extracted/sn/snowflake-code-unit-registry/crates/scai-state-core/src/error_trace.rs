//! Runtime types for the `ScaiError` derive macro.
//!
//! The `ScaiError` proc macro generates code that references types from
//! `crate::error_trace::*`. This module provides those types.

use serde::Serialize;

/// A single entry in an error's location trace.
#[derive(Debug, Clone, Serialize)]
pub struct ErrorTraceEntry {
    pub location: Location,
    pub message: String,
}

/// Source-code location (owned strings, safe to cross FFI boundaries).
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Location {
    pub file: String,
    pub line: u32,
    pub column: u32,
}

impl std::fmt::Display for Location {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}:{}:{}", self.file, self.line, self.column)
    }
}

/// Trait implemented by error types whose trace can be recursively collected.
///
/// The `ScaiError` derive generates an inherent `error_trace()` method.
/// Implement this trait to delegate to it, enabling recursive trace collection
/// when one error variant wraps another.
pub trait ErrorTrace {
    fn error_trace(&self) -> Vec<ErrorTraceEntry>;
}

// ── Autoref specialization for source-chain traversal ──
//
// When the `ScaiError` macro encounters a `source` field, it wraps the
// reference in `ErrorTraceResolver` and calls `(&resolver).resolve()`.
//
// - If the source type implements `ErrorTrace`, the inherent method on
//   `ErrorTraceResolver` is found first (zero autorefs) → recurses.
// - Otherwise, the blanket `ErrorTraceFallback` impl on `&ErrorTraceResolver`
//   is found (one autoref) → returns an empty vec, stopping the chain.

/// Wrapper used by generated code for autoref-based specialization.
pub struct ErrorTraceResolver<'a, T: ?Sized>(pub &'a T);

/// Fallback trait: returns an empty trace for non-`ErrorTrace` source types.
pub trait ErrorTraceFallback {
    fn resolve(&self) -> Vec<ErrorTraceEntry>;
}

impl<T: ?Sized> ErrorTraceFallback for &ErrorTraceResolver<'_, T> {
    fn resolve(&self) -> Vec<ErrorTraceEntry> {
        vec![]
    }
}

impl<T: ErrorTrace + ?Sized> ErrorTraceResolver<'_, T> {
    pub fn resolve(&self) -> Vec<ErrorTraceEntry> {
        self.0.error_trace()
    }
}

// Blanket impls so `Box<E>` and `&E` delegate to the inner type.

impl<T: ErrorTrace + ?Sized> ErrorTrace for Box<T> {
    fn error_trace(&self) -> Vec<ErrorTraceEntry> {
        (**self).error_trace()
    }
}

impl<T: ErrorTrace + ?Sized> ErrorTrace for &T {
    fn error_trace(&self) -> Vec<ErrorTraceEntry> {
        (**self).error_trace()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use err_code::ErrorCode;
    use scai_error_derive::ScaiError;
    use snafu::{IntoError, Snafu};

    /// Minimal enum that derives ScaiError against the real runtime types
    /// in this module — proves the generated `crate::error_trace::*` paths
    /// resolve to actual `scai-state-core::error_trace` types.
    #[derive(Debug, Snafu, ErrorCode, ScaiError)]
    #[error_code(type = "u32")]
    enum MiniError {
        #[snafu(display("not found: {id}"))]
        #[error_code(8001)]
        NotFound {
            id: String,
            #[snafu(implicit)]
            location: snafu::Location,
        },

        #[snafu(display("inner error"))]
        #[error_code(8002)]
        Wrapper {
            source: Box<MiniError>,
            #[snafu(implicit)]
            location: snafu::Location,
        },

        #[snafu(display("io: {source}"))]
        #[snafu(context(false))]
        #[error_code(8003)]
        Io {
            source: std::io::Error,
            #[snafu(implicit)]
            location: snafu::Location,
        },
    }

    impl ErrorTrace for MiniError {
        fn error_trace(&self) -> Vec<ErrorTraceEntry> {
            self.error_trace()
        }
    }

    #[test]
    fn trace_uses_real_runtime_types() {
        let e = NotFoundSnafu { id: "x" }.build();
        let trace: Vec<ErrorTraceEntry> = e.error_trace();
        assert_eq!(trace.len(), 1);
        assert!(trace[0].location.file.contains("error_trace.rs"));
        assert_eq!(trace[0].message, "not found: x");
    }

    #[test]
    fn trace_recurses_through_real_types() {
        let inner = NotFoundSnafu { id: "y" }.build();
        let outer = WrapperSnafu.into_error(Box::new(inner));
        let trace = outer.error_trace();
        assert_eq!(trace.len(), 2);
        assert_eq!(trace[0].message, "inner error");
        assert_eq!(trace[1].message, "not found: y");
    }

    #[test]
    fn trace_stops_at_non_error_trace_source() {
        let io_err = std::io::Error::other("disk");
        let e = MiniError::from(io_err);
        let trace = e.error_trace();
        assert_eq!(trace.len(), 1);
    }

    #[test]
    fn details_with_real_types() {
        let e = NotFoundSnafu { id: "z" }.build();
        let d = e.details().expect("should have details");
        assert_eq!(d["id"], "z");
    }

    #[test]
    fn all_codes_with_real_types() {
        let codes = MiniError::all_codes();
        assert_eq!(
            codes,
            vec![("NotFound", 8001), ("Wrapper", 8002), ("Io", 8003)]
        );
    }
}
