//! Integration tests for the ScaiError derive macro.
//!
//! Run with: cargo test -p scai-error-derive --test derive_integration
//!
//! The ScaiError macro generates code referencing `crate::error_trace::*`, so
//! this test defines a local `mod error_trace` to satisfy those paths.

use err_code::ErrorCode;
use scai_error_derive::ScaiError;
use snafu::{IntoError, Snafu};

// ── Runtime types (mirrors scai-state-core::error_trace) ──

pub mod error_trace {
    #[derive(Debug, Clone, PartialEq)]
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

    #[derive(Debug, Clone)]
    pub struct ErrorTraceEntry {
        pub location: Location,
        pub message: String,
    }

    pub trait ErrorTrace {
        fn error_trace(&self) -> Vec<ErrorTraceEntry>;
    }

    /// Wrapper for autoref specialization: when `T: ErrorTrace`, the inherent
    /// method is preferred over the blanket `ErrorTraceFallback` trait impl.
    pub struct ErrorTraceResolver<'a, T: ?Sized>(pub &'a T);

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
}

use error_trace::{ErrorTrace, ErrorTraceEntry};

// ── Test error enum ──

#[derive(Debug, Snafu, ErrorCode, ScaiError)]
#[error_code(type = "u32")]
enum TestError {
    #[snafu(display("Not found: {id}"))]
    #[error_code(2001)]
    NotFound {
        id: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Invalid transition from {from} to {to}"))]
    #[error_code(2002)]
    InvalidTransition {
        from: String,
        to: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("IO error: {source}"))]
    #[snafu(context(false))]
    #[error_code(2003)]
    Io {
        source: std::io::Error,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Wrapper error"))]
    #[error_code(2004)]
    Wrapper {
        source: Box<TestError>,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Reentrant call"))]
    #[error_code(2005)]
    Reentrant {
        #[snafu(implicit)]
        location: snafu::Location,
    },
}

impl ErrorTrace for TestError {
    fn error_trace(&self) -> Vec<ErrorTraceEntry> {
        self.error_trace()
    }
}

// ── Behavior 1: error_trace() extracts location from every variant ──

#[test]
fn trace_extracts_location_from_simple_variant() {
    let e = NotFoundSnafu { id: "abc" }.build();
    let trace = e.error_trace();
    assert_eq!(trace.len(), 1);
    assert!(
        trace[0].location.file.contains("derive_integration.rs"),
        "expected derive_integration.rs in location, got: {}",
        trace[0].location.file
    );
    assert_eq!(trace[0].message, "Not found: abc");
}

#[test]
fn trace_extracts_location_from_unit_like_variant() {
    let e = ReentrantSnafu.build();
    let trace = e.error_trace();
    assert_eq!(trace.len(), 1);
    assert!(trace[0].location.file.contains("derive_integration.rs"));
    assert_eq!(trace[0].message, "Reentrant call");
}

// ── Behavior 2: error_trace() recurses into source fields ──

#[test]
fn trace_recurses_into_error_trace_source() {
    let inner = NotFoundSnafu { id: "nested" }.build();
    let outer = WrapperSnafu.into_error(Box::new(inner));
    let trace = outer.error_trace();
    assert_eq!(trace.len(), 2, "expected 2 trace entries, got: {trace:#?}");
    assert_eq!(trace[0].message, "Wrapper error");
    assert_eq!(trace[1].message, "Not found: nested");
}

#[test]
fn trace_stops_at_non_error_trace_source() {
    let io_err = std::io::Error::new(std::io::ErrorKind::NotFound, "gone");
    let e = TestError::from(io_err);
    let trace = e.error_trace();
    assert_eq!(trace.len(), 1, "non-ErrorTrace source should not recurse");
    assert!(trace[0].message.contains("gone"));
}

// ── Behavior 3: details() with camelCase keys ──

#[test]
fn details_serializes_data_fields_as_camel_case() {
    let e = InvalidTransitionSnafu {
        from: "draft",
        to: "published",
    }
    .build();
    let details = e.details().expect("should have details");
    assert_eq!(details["from"], "draft");
    assert_eq!(details["to"], "published");
    assert!(
        details.get("location").is_none(),
        "location must be excluded"
    );
}

#[test]
fn details_includes_single_data_field() {
    let e = NotFoundSnafu { id: "xyz" }.build();
    let details = e.details().expect("should have details");
    assert_eq!(details["id"], "xyz");
}

// ── Behavior 4: details() returns None for no-data variants ──

#[test]
fn details_returns_none_when_only_location() {
    let e = ReentrantSnafu.build();
    assert!(e.details().is_none());
}

#[test]
fn details_returns_none_when_only_source_and_location() {
    let io_err = std::io::Error::other("oops");
    let e = TestError::from(io_err);
    assert!(e.details().is_none());
}

// ── Behavior 5: all_codes() matches err_code values ──

#[test]
fn all_codes_returns_correct_pairs() {
    let codes = TestError::all_codes();
    assert_eq!(codes.len(), 5);

    let expected = vec![
        ("NotFound", 2001),
        ("InvalidTransition", 2002),
        ("Io", 2003),
        ("Wrapper", 2004),
        ("Reentrant", 2005),
    ];
    assert_eq!(codes, expected);
}

#[test]
fn all_codes_match_error_code_derive() {
    let e = NotFoundSnafu { id: "x" }.build();
    assert_eq!(e.error_code() as i32, 2001);

    let codes = TestError::all_codes();
    let found = codes.iter().find(|(name, _)| *name == "NotFound");
    assert_eq!(found, Some(&("NotFound", 2001)));
}
