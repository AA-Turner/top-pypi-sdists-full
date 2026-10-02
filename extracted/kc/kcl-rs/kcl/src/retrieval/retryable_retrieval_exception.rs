//! Port of `software.amazon.kinesis.retrieval.RetryableRetrievalException`.
//!
//! In Java this is a marker subclass of `KinesisClientLibRetryableException`
//! thrown from the `SubscribeToShard`/`GetRecords` retrieval paths (timeouts,
//! invalid results). It is caught specially by `PrefetchRecordsPublisher`'s
//! daemon loop (logged + retried, not fatal) and by `ShardConsumerSubscriber`
//! (which matches on the message containing `"ReadTimeout"`).
//!
//! # Design decision
//!
//! Rather than fold this into the existing
//! [`KinesisClientLibError`](crate::exceptions::KinesisClientLibError) `Io`
//! variant, we model it as its own small `thiserror` enum
//! [`RetrievalError`] with a dedicated [`RetrievalError::Retryable`] variant.
//! This keeps the retrieval subsystem's "retryable retrieval failure" concept
//! distinct and lets the polling/fan-out waves match on it precisely (mirroring
//! Java's `instanceof RetryableRetrievalException`), while
//! [`RetrievalError::is_retryable`] preserves the retryable/non-retryable split
//! established by `KinesisClientLibError::is_retryable`.
//!
//! `RetryableRetrievalException` is retryable; a non-retryable
//! [`RetrievalError::Other`] variant is provided for the invalid-state failures
//! that some call sites surface alongside it.

use crate::exceptions::BoxError;

/// Errors originating from the record-retrieval paths.
///
/// The [`Retryable`](RetrievalError::Retryable) variant is the port of
/// `RetryableRetrievalException`.
#[derive(Debug, thiserror::Error)]
pub enum RetrievalError {
    /// Port of `RetryableRetrievalException` (retryable): a `SubscribeToShard`
    /// or `GetRecords` failure the caller should retry (e.g. a timeout or an
    /// invalid GetRecords result).
    #[error("RetryableRetrievalException: {message}")]
    Retryable {
        /// The human-readable message (Java `getMessage()`).
        message: String,
        /// The wrapped cause, if any (Java `getCause()`).
        #[source]
        source: Option<BoxError>,
    },

    /// A non-retryable retrieval failure (e.g. an invalid-state condition that
    /// should not be retried). Not part of the Java
    /// `RetryableRetrievalException` type, but useful where the retrieval paths
    /// surface a fatal error next to a retryable one.
    #[error("{message}")]
    Other {
        /// The human-readable message.
        message: String,
        /// The wrapped cause, if any.
        #[source]
        source: Option<BoxError>,
    },
}

impl RetrievalError {
    /// Construct a retryable retrieval error with just a message (Java
    /// `RetryableRetrievalException(String)`).
    pub fn retryable(message: impl Into<String>) -> Self {
        Self::Retryable {
            message: message.into(),
            source: None,
        }
    }

    /// Construct a retryable retrieval error with a message and cause (Java
    /// `RetryableRetrievalException(String, Exception)`).
    pub fn retryable_caused_by(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self::Retryable {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    /// Construct a non-retryable retrieval error.
    pub fn other(message: impl Into<String>) -> Self {
        Self::Other {
            message: message.into(),
            source: None,
        }
    }

    /// Whether this error is retryable. Mirrors
    /// `KinesisClientLibError::is_retryable`: the `Retryable` variant (Java
    /// `RetryableRetrievalException extends KinesisClientLibRetryableException`)
    /// is retryable; `Other` is not.
    pub fn is_retryable(&self) -> bool {
        matches!(self, Self::Retryable { .. })
    }

    /// The human-readable message.
    pub fn message(&self) -> &str {
        match self {
            Self::Retryable { message, .. } | Self::Other { message, .. } => message,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn retryable_is_retryable() {
        let e = RetrievalError::retryable("ReadTimeout on shard");
        assert!(e.is_retryable());
        assert_eq!(
            e.to_string(),
            "RetryableRetrievalException: ReadTimeout on shard"
        );
        assert_eq!(e.message(), "ReadTimeout on shard");
    }

    #[test]
    fn other_is_not_retryable() {
        let e = RetrievalError::other("bad state");
        assert!(!e.is_retryable());
    }

    #[test]
    fn caused_by_preserves_source() {
        use std::error::Error;
        let cause = std::io::Error::new(std::io::ErrorKind::TimedOut, "boom");
        let e = RetrievalError::retryable_caused_by("timeout", cause);
        assert!(e.source().is_some());
    }
}
