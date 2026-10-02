//! Error types for the SCAI state library

use err_code::ErrorCode;
use scai_error_derive::ScaiError;
use serde::Serialize;
use snafu::{IntoError, Snafu};

use crate::error_trace::{ErrorTrace, ErrorTraceEntry};

/// Main error type for SCAI state operations.
///
/// Each variant carries a stable numeric error code via the `#[error_code]`
/// attribute. These codes are the cross-language contract shared with Python,
/// C#, and any future bindings.
///
/// Call [`Error::error_code()`] to obtain the numeric value.
#[derive(Debug, Snafu, ErrorCode, ScaiError)]
#[snafu(visibility(pub(crate)))]
#[error_code(type = "u32")]
pub enum Error {
    #[snafu(display("Registry not found at path: {path}"))]
    #[error_code(1001)]
    RegistryNotFound {
        path: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Registry already exists at path: {path}"))]
    #[error_code(1002)]
    RegistryAlreadyExists {
        path: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Code unit not found: {id}"))]
    #[error_code(1003)]
    CodeUnitNotFound {
        id: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Code unit already exists: {id}"))]
    #[error_code(1004)]
    CodeUnitAlreadyExists {
        id: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Invalid state transition from {from} to {to}"))]
    #[error_code(1005)]
    InvalidStateTransition {
        from: String,
        to: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Lock acquisition failed: {message}"))]
    #[error_code(1006)]
    LockError {
        message: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Validation error: {message}"))]
    #[error_code(1007)]
    ValidationError {
        message: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("IO error: {source}"))]
    #[snafu(context(false))]
    #[error_code(1008)]
    IoError {
        source: std::io::Error,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("JSON error: {source}"))]
    #[snafu(context(false))]
    #[error_code(1009)]
    JsonError {
        source: serde_json::Error,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Invalid path: {path}"))]
    #[error_code(1010)]
    InvalidPath {
        path: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Filter error: {message}"))]
    #[error_code(1011)]
    FilterError {
        message: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display(
        "Invalid checksum mode '{input}': expected one of none, source, converted, snapshot, all"
    ))]
    #[error_code(1013)]
    InvalidChecksumMode {
        input: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Dependency cycle detected: {message}"))]
    #[error_code(1014)]
    CycleDetected {
        message: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Write succeeded but dependency refresh failed"))]
    #[error_code(1015)]
    WriteSucceededRefreshFailed {
        source: Box<Error>,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Scoped refresh requires a full refresh first: {message}"))]
    #[error_code(1016)]
    ScopedRefreshRequiresFullRefresh {
        message: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Scoped refresh encountered unresolved dependency ID: {id}"))]
    #[error_code(1017)]
    ScopedRefreshUnresolvedDependency {
        id: String,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Write methods cannot be called from inside a before_persist hook"))]
    #[error_code(1018)]
    HookReentrant {
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Batch contains duplicate ID '{id}' (first at index {first_index}, duplicate at index {duplicate_index} of {batch_size})"))]
    #[error_code(1019)]
    DuplicateBatchId {
        id: String,
        first_index: usize,
        duplicate_index: usize,
        batch_size: usize,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display(
        "Schema version {document_version} is newer than supported version {supported_version}. \
         Upgrade the library to read this document."
    ))]
    #[error_code(1020)]
    SchemaVersionNewerThanSupported {
        document_version: i64,
        supported_version: i64,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display("Schema migration failed: {message}"))]
    #[error_code(1021)]
    SchemaMigrationError {
        message: String,
        context: Option<serde_json::Value>,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    #[snafu(display(
        "Document at schema version {document_version} requires registry-aware migration \
         to reach version {target_version}. Run migrate_schema_all() first."
    ))]
    #[error_code(1022)]
    RegistrySchemaMigrationRequired {
        document_version: i64,
        target_version: i64,
        #[snafu(implicit)]
        location: snafu::Location,
    },

    /// I/O failure scoped to a known filesystem path.
    ///
    /// Distinct from [`Error::IoError`] (which auto-wraps any `io::Error` via `?` for incidental I/O) because
    /// callers — especially across the FFI boundary — frequently need to know *which* path failed and *what*
    /// operation was attempted (`open`, `read`, `write`, …) without parsing a free-form message. Both fields
    /// are surfaced as structured `details` JSON via [`Error::info`].
    #[snafu(display("Failed to {op} '{path}': {source}"))]
    #[error_code(1023)]
    FileIoError {
        op: String,
        path: String,
        source: std::io::Error,
        #[snafu(implicit)]
        location: snafu::Location,
    },
}

impl ErrorTrace for Error {
    fn error_trace(&self) -> Vec<ErrorTraceEntry> {
        self.error_trace()
    }
}

impl From<scai_log::Error> for Error {
    fn from(e: scai_log::Error) -> Self {
        match e {
            scai_log::Error::Io { op, path, source } => FileIoSnafu { op, path }.into_error(source),
            scai_log::Error::InvalidLogLevel(msg) => Error::validation(msg),
        }
    }
}

impl Error {
    /// Construct an [`InvalidPath`](Error::InvalidPath) error.
    ///
    /// Provided for binding crates that need to synthesize this variant
    /// without depending on the snafu-generated selector.
    #[track_caller]
    pub fn invalid_path(path: impl Into<String>) -> Self {
        InvalidPathSnafu { path: path.into() }.build()
    }

    /// Construct a [`ValidationError`](Error::ValidationError).
    ///
    /// Provided for binding crates that need to synthesize this variant
    /// without depending on the snafu-generated selector.
    #[track_caller]
    pub fn validation(message: impl Into<String>) -> Self {
        ValidationSnafu {
            message: message.into(),
        }
        .build()
    }

    /// Stable i32 error code for cross-language bindings.
    ///
    /// Delegates to the auto-generated `error_code() -> u32` and casts to
    /// `i32`, which is the type expected by C# and Python consumers.
    pub fn error_code_i32(&self) -> i32 {
        self.error_code() as i32
    }

    /// Build a canonical [`ErrorInfo`] snapshot from this error.
    pub fn info(&self) -> ErrorInfo {
        ErrorInfo {
            code: self.error_code_i32(),
            message: self.to_string(),
            trace: self
                .error_trace()
                .into_iter()
                .map(|e| TraceEntry {
                    location: e.location.to_string(),
                    message: e.message,
                })
                .collect(),
            details: self.details(),
        }
    }
}

/// Canonical public error payload shared across all language bindings.
///
/// This is the single structured error type exposed to Python, C#, and Node.js.
/// Callers match on `code` using the per-language `ErrorCode` enums.
#[derive(Debug, Clone, Serialize)]
pub struct ErrorInfo {
    pub code: i32,
    pub message: String,
    pub trace: Vec<TraceEntry>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub details: Option<serde_json::Value>,
}

/// A single entry in the error trace (wire format).
#[derive(Debug, Clone, Serialize)]
pub struct TraceEntry {
    pub location: String,
    pub message: String,
}

/// Bump this when adding or removing a variant.
#[cfg(test)]
const EXPECTED_VARIANT_COUNT: usize = 22;

/// Result type alias for SCAI state operations
pub type Result<T> = std::result::Result<T, Error>;

/// A single failure inside a [`BatchResult`].
#[derive(Debug, Clone, Serialize)]
pub struct BatchFailure {
    pub id: String,
    pub error: ErrorInfo,
}

/// Result of a batch operation (create_batch, update_batch, update_where, upsert_batch)
#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct BatchResult {
    /// IDs of successfully processed items
    pub succeeded: Vec<String>,
    /// Per-item failures carrying structured [`ErrorInfo`]
    pub failed: Vec<BatchFailure>,
    /// IDs added by hooks that were not in the original caller-supplied input
    pub side_effect_ids: Vec<String>,
}

impl BatchResult {
    pub fn new() -> Self {
        Self {
            succeeded: Vec::new(),
            failed: Vec::new(),
            side_effect_ids: Vec::new(),
        }
    }

    pub fn success(&mut self, id: String) {
        self.succeeded.push(id);
    }

    pub fn failure(&mut self, id: String, error: &Error) {
        self.failed.push(BatchFailure {
            id,
            error: error.info(),
        });
    }

    pub fn has_failed(&self, id: &str) -> bool {
        self.failed.iter().any(|f| f.id == id)
    }

    pub fn total(&self) -> usize {
        self.succeeded.len() + self.failed.len()
    }
}

impl Default for BatchResult {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use snafu::IntoError;
    use test_case::test_case;

    #[test_case(RegistryNotFoundSnafu { path: "/tmp/x" }.build()                => 1001 ; "RegistryNotFound")]
    #[test_case(CodeUnitNotFoundSnafu { id: "abc" }.build()                     => 1003 ; "CodeUnitNotFound")]
    #[test_case(FilterSnafu { message: "bad" }.build()                          => 1011 ; "FilterError")]
    #[test_case(CycleDetectedSnafu { message: "a -> b" }.build()                => 1014 ; "CycleDetected")]
    #[test_case(WriteSucceededRefreshFailedSnafu.into_error(Box::new(ValidationSnafu { message: "msg" }.build())) => 1015 ; "WriteSucceededRefreshFailed")]
    #[test_case(ScopedRefreshRequiresFullRefreshSnafu { message: "run" }.build() => 1016 ; "ScopedRefreshRequiresFullRefresh")]
    #[test_case(ScopedRefreshUnresolvedDependencySnafu { id: "id" }.build()      => 1017 ; "ScopedRefreshUnresolvedDependency")]
    #[test_case(SchemaVersionNewerThanSupportedSnafu { document_version: 3i64, supported_version: 2i64 }.build() => 1020 ; "SchemaVersionNewerThanSupported")]
    #[test_case(SchemaMigrationSnafu { message: "failed", context: None }.build() => 1021 ; "SchemaMigrationError")]
    #[test_case(RegistrySchemaMigrationRequiredSnafu { document_version: 1i64, target_version: 2i64 }.build() => 1022 ; "RegistrySchemaMigrationRequired")]
    #[test_case(FileIoSnafu { op: "open", path: "/tmp/x" }.into_error(std::io::Error::from(std::io::ErrorKind::NotFound)) => 1023 ; "FileIoError")]
    fn error_code_is_stable(err: Error) -> i32 {
        err.error_code_i32()
    }

    #[test]
    fn all_codes_covers_every_variant() {
        let codes = Error::all_codes();
        assert_eq!(
            codes.len(),
            EXPECTED_VARIANT_COUNT,
            "Error::all_codes() returned {} entries but EXPECTED_VARIANT_COUNT is {} — \
             update the constant in error.rs when adding/removing variants",
            codes.len(),
            EXPECTED_VARIANT_COUNT,
        );

        let mut seen_names = std::collections::HashSet::new();
        let mut seen_codes = std::collections::HashSet::new();
        for (name, code) in &codes {
            assert!(
                seen_names.insert(*name),
                "duplicate variant name in all_codes(): {name}"
            );
            assert!(
                seen_codes.insert(*code),
                "duplicate error code in all_codes(): {code}"
            );
            assert!(
                *code >= 1001,
                "error code for {name} is {code}, expected >= 1001"
            );
        }
    }

    #[test]
    fn batch_failure_captures_code_and_message() {
        let mut result = BatchResult::new();
        let err = CodeUnitNotFoundSnafu { id: "abc" }.build();
        result.failure("id1".into(), &err);

        assert_eq!(result.failed.len(), 1);
        assert_eq!(result.failed[0].id, "id1");
        assert_eq!(result.failed[0].error.code, 1003);
        assert_eq!(result.failed[0].error.message, "Code unit not found: abc");
    }

    #[test]
    fn error_info_populates_details_for_data_bearing_variants() {
        let err = InvalidStateTransitionSnafu {
            from: "draft",
            to: "archived",
        }
        .build();
        let info = err.info();
        assert_eq!(info.code, 1005);
        let details = info.details.unwrap();
        assert_eq!(details["from"], "draft");
        assert_eq!(details["to"], "archived");

        let err = InvalidChecksumModeSnafu { input: "bad_mode" }.build();
        let info = err.info();
        assert_eq!(info.code, 1013);
        let details = info.details.unwrap();
        assert_eq!(details["input"], "bad_mode");

        let err = DuplicateBatchIdSnafu {
            id: "dup-42",
            first_index: 0usize,
            duplicate_index: 3usize,
            batch_size: 5usize,
        }
        .build();
        let info = err.info();
        assert_eq!(info.code, 1019);
        let details = info.details.unwrap();
        assert_eq!(details["id"], "dup-42");
        assert_eq!(details["firstIndex"], 0);
        assert_eq!(details["duplicateIndex"], 3);
        assert_eq!(details["batchSize"], 5);
    }

    #[test]
    fn error_info_populates_trace_for_write_succeeded_refresh_failed() {
        let inner = CycleDetectedSnafu { message: "a -> b" }.build();
        let outer = WriteSucceededRefreshFailedSnafu.into_error(Box::new(inner));
        let info = outer.info();
        assert_eq!(info.code, 1015);

        assert_eq!(info.trace.len(), 2);
        assert_eq!(
            info.trace[0].message,
            "Write succeeded but dependency refresh failed"
        );
        assert!(info.trace[1].message.contains("a -> b"));
    }

    #[test]
    fn error_info_serializes_to_json() {
        let err = InvalidStateTransitionSnafu {
            from: "draft",
            to: "archived",
        }
        .build();
        let info = err.info();
        let json = serde_json::to_value(&info).unwrap();
        assert_eq!(json["code"], 1005);
        assert_eq!(json["details"]["from"], "draft");
        assert_eq!(json["details"]["to"], "archived");
        assert!(json["trace"].is_array());
    }

    #[test]
    fn error_info_trace_captures_location() {
        let err = HookReentrantSnafu.build();
        let info = err.info();
        assert_eq!(info.trace.len(), 1);
        assert!(info.trace[0].location.contains("error.rs"));
    }

    #[test]
    fn batch_result_initializes_side_effect_ids_empty() {
        let result = BatchResult::new();
        assert!(result.side_effect_ids.is_empty());
    }
}
