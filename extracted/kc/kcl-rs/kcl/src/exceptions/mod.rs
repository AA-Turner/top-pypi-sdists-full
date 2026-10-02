//! Port of `software.amazon.kinesis.exceptions`.
//!
//! Java models KCL failures as a checked-exception hierarchy rooted at
//! `KinesisClientLibException`, split into retryable and non-retryable
//! branches. Rust has no exceptions or inheritance, so the hierarchy is
//! flattened into a single [`KinesisClientLibError`] enum whose variants map
//! one-to-one onto the concrete Java exception classes. The retryable /
//! non-retryable distinction — which callers switch on to decide whether to
//! back off and retry — is preserved by [`KinesisClientLibError::is_retryable`].
//!
//! | Java class                               | Variant                      | Retryable |
//! |------------------------------------------|------------------------------|-----------|
//! | `InvalidStateException`                  | [`InvalidState`]             | no        |
//! | `ShutdownException`                      | [`Shutdown`]                 | no        |
//! | `ThrottlingException`                    | [`Throttling`]               | yes       |
//! | `KinesisClientLibDependencyException`    | [`Dependency`]               | yes       |
//! | `internal.BlockedOnParentShardException` | [`BlockedOnParentShard`]     | yes       |
//! | `internal.KinesisClientLibIOException`   | [`Io`]                       | yes       |
//!
//! [`InvalidState`]: KinesisClientLibError::InvalidState
//! [`Shutdown`]: KinesisClientLibError::Shutdown
//! [`Throttling`]: KinesisClientLibError::Throttling
//! [`Dependency`]: KinesisClientLibError::Dependency
//! [`BlockedOnParentShard`]: KinesisClientLibError::BlockedOnParentShard
//! [`Io`]: KinesisClientLibError::Io

use thiserror::Error;

/// A boxed, thread-safe error used to carry a Java `Throwable` "cause".
pub type BoxError = Box<dyn std::error::Error + Send + Sync + 'static>;

/// Port of the `KinesisClientLibException` hierarchy.
///
/// Each variant corresponds to a concrete Java exception class. Variants carry
/// a human-readable message and, optionally, a wrapped cause (the Java
/// `Throwable cause`), mirroring the two-argument constructors on the Java
/// classes.
#[derive(Debug, Error)]
pub enum KinesisClientLibError {
    /// Port of `InvalidStateException` (non-retryable). Unable to store the
    /// checkpoint, e.g. because the DynamoDB table does not exist.
    #[error("InvalidStateException: {message}")]
    InvalidState {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `ShutdownException` (non-retryable). The record processor has
    /// been shut down; another worker may already be processing these records.
    #[error("ShutdownException: {message}")]
    Shutdown {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `ThrottlingException` (retryable). Can be caused by
    /// checkpointing too frequently.
    #[error("ThrottlingException: {message}")]
    Throttling {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `KinesisClientLibDependencyException` (retryable). Encountered an
    /// issue when storing the checkpoint; the application can back off and retry.
    #[error("KinesisClientLibDependencyException: {message}")]
    Dependency {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `internal.BlockedOnParentShardException` (retryable). The parent
    /// shard has not been fully processed, so this shard cannot start yet.
    #[error("BlockedOnParentShardException: {message}")]
    BlockedOnParentShard {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `internal.KinesisClientLibIOException` (retryable). Thrown when
    /// the retrieved shard information is inconsistent.
    #[error("KinesisClientLibIOException: {message}")]
    Io {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
}

impl KinesisClientLibError {
    /// Whether this error is a `KinesisClientLibRetryableException` in Java.
    ///
    /// Callers use this to decide whether an operation may be safely retried
    /// (after backoff) or must be surfaced to the application.
    pub fn is_retryable(&self) -> bool {
        matches!(
            self,
            Self::Throttling { .. }
                | Self::Dependency { .. }
                | Self::BlockedOnParentShard { .. }
                | Self::Io { .. }
        )
    }

    /// The exception message (Java `getMessage`).
    pub fn message(&self) -> &str {
        match self {
            Self::InvalidState { message, .. }
            | Self::Shutdown { message, .. }
            | Self::Throttling { message, .. }
            | Self::Dependency { message, .. }
            | Self::BlockedOnParentShard { message, .. }
            | Self::Io { message, .. } => message,
        }
    }

    // --- Convenience constructors mirroring the Java single/two-arg ctors. ---

    pub fn invalid_state(message: impl Into<String>) -> Self {
        Self::InvalidState {
            message: message.into(),
            source: None,
        }
    }

    pub fn invalid_state_caused_by(
        message: impl Into<String>,
        source: impl Into<BoxError>,
    ) -> Self {
        Self::InvalidState {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    pub fn shutdown(message: impl Into<String>) -> Self {
        Self::Shutdown {
            message: message.into(),
            source: None,
        }
    }

    pub fn shutdown_caused_by(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self::Shutdown {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    pub fn throttling(message: impl Into<String>) -> Self {
        Self::Throttling {
            message: message.into(),
            source: None,
        }
    }

    pub fn throttling_caused_by(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self::Throttling {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    pub fn dependency(message: impl Into<String>) -> Self {
        Self::Dependency {
            message: message.into(),
            source: None,
        }
    }

    pub fn dependency_caused_by(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self::Dependency {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    pub fn blocked_on_parent_shard(message: impl Into<String>) -> Self {
        Self::BlockedOnParentShard {
            message: message.into(),
            source: None,
        }
    }

    pub fn io(message: impl Into<String>) -> Self {
        Self::Io {
            message: message.into(),
            source: None,
        }
    }

    pub fn io_caused_by(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self::Io {
            message: message.into(),
            source: Some(source.into()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn retryable_classification_matches_java_hierarchy() {
        assert!(!KinesisClientLibError::invalid_state("x").is_retryable());
        assert!(!KinesisClientLibError::shutdown("x").is_retryable());
        assert!(KinesisClientLibError::throttling("x").is_retryable());
        assert!(KinesisClientLibError::dependency("x").is_retryable());
        assert!(KinesisClientLibError::blocked_on_parent_shard("x").is_retryable());
        assert!(KinesisClientLibError::io("x").is_retryable());
    }

    #[test]
    fn display_includes_class_name_and_message() {
        let e = KinesisClientLibError::invalid_state("table missing");
        assert_eq!(e.to_string(), "InvalidStateException: table missing");
    }

    #[test]
    fn cause_is_exposed_as_error_source() {
        use std::error::Error;
        let cause = std::io::Error::other("boom");
        let e = KinesisClientLibError::dependency_caused_by("wrapped", cause);
        assert!(e.source().is_some());
        assert_eq!(e.message(), "wrapped");
    }
}
