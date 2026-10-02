//! SCAI State Core Library
//!
//! This library provides file operations for managing code unit state using
//! typed structs generated from the JSON Schema.

pub mod bindings;
pub mod canonical_name;
pub mod checksum;
pub mod database_bindings;
pub(crate) mod dependency_view;
pub mod error;
pub mod error_trace;
pub mod filter;
pub mod generated;
pub mod identity;
pub mod migration;
pub mod registry;
pub mod validation;

// Re-export generated types
pub use generated::query_reference::QUERY_REFERENCE;
pub use generated::types::*;

// Re-export core types
pub use bindings::{validate_bindings, BindingDiff};
pub use checksum::compute_buffer_checksum;
pub use checksum::compute_file_checksum;
pub use checksum::ChangeType;
pub use checksum::ChecksumMode;
pub use checksum::ChecksumScanError;
pub use checksum::ChecksumValidationEntry;
pub use checksum::ChecksumValidationReport;
pub use checksum::ChecksumValidationStatus;
pub use checksum::FileChange;
pub use checksum::FileType;
pub use checksum::SourceCodeChanges;
pub use database_bindings::{
    dollar_brace_token, parse_database_bindings, read_database_bindings, snow_cli_token,
    DatabaseBindings, TokenWrapper,
};
pub use error::BatchFailure;
pub use error::BatchResult;
pub use error::Error;
pub use error::ErrorInfo;
pub use error::TraceEntry;
pub use filter::Filter;
pub use registry::CodeUnitRegistry;
pub use registry::FindOptions;
pub use registry::WriteOptions;
pub use registry::UNKNOWN_ID;

// Re-export validation types
pub use validation::script_io::{validate_script_io, ProvidedIo, ScriptIoDiff};
pub use validation::ValidationIssue;
pub use validation::ValidationIssueKind;
pub use validation::ValidationReport;

// Re-export migration constants
pub use migration::CURRENT_SCHEMA_VERSION;

// Re-export identity helpers
pub use identity::generate_id;

// Re-export logging types from the scai-log crate
pub use scai_log::LogLevel;
pub use scai_log::ScaiLogger;
