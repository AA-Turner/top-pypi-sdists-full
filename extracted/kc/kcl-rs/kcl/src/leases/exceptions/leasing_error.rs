//! Port of the `software.amazon.kinesis.leases.exceptions.LeasingException`
//! hierarchy.
//!
//! Java models leasing-infrastructure failures as a shallow checked-exception
//! hierarchy rooted at `LeasingException`, with three concrete subclasses.
//! Rust has no exceptions or inheritance, so the hierarchy is flattened into a
//! single [`LeasingError`] enum whose variants map one-to-one onto the concrete
//! Java subclasses. This mirrors the [`KinesisClientLibError`] pattern.
//!
//! | Java class                       | Variant                                    |
//! |----------------------------------|--------------------------------------------|
//! | `DependencyException`            | [`Dependency`]                             |
//! | `InvalidStateException`          | [`InvalidState`]                           |
//! | `ProvisionedThroughputException` | [`ProvisionedThroughput`]                  |
//!
//! The base class `LeasingException` itself is never thrown directly (it is
//! abstract-in-practice), so it has no variant; callers that caught
//! `LeasingException` in Java simply match on the whole `LeasingError` enum.
//!
//! [`Dependency`]: LeasingError::Dependency
//! [`InvalidState`]: LeasingError::InvalidState
//! [`ProvisionedThroughput`]: LeasingError::ProvisionedThroughput
//! [`KinesisClientLibError`]: crate::exceptions::KinesisClientLibError

use thiserror::Error;

use crate::exceptions::BoxError;

/// Port of the `LeasingException` hierarchy: failures of the leasing subsystem
/// (backed by DynamoDB).
///
/// Each variant corresponds to a concrete Java exception class and carries a
/// human-readable message plus an optional wrapped cause (the Java
/// `Throwable cause`).
#[derive(Debug, Error)]
pub enum LeasingError {
    /// Port of `DependencyException`. A dependency of the leasing system failed
    /// unexpectedly — DynamoDB threw an `InternalServerException` or a generic
    /// `AmazonClientException` not otherwise handled.
    #[error("DependencyException: {message}")]
    Dependency {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `InvalidStateException`. DynamoDB is in an invalid state; most
    /// commonly the lease table has not been created yet.
    #[error("InvalidStateException: {message}")]
    InvalidState {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
    /// Port of `ProvisionedThroughputException`. The operation failed due to
    /// lack of provisioned throughput on the DynamoDB lease table.
    #[error("ProvisionedThroughputException: {message}")]
    ProvisionedThroughput {
        message: String,
        #[source]
        source: Option<BoxError>,
    },
}

impl LeasingError {
    /// The exception message (Java `getMessage`).
    pub fn message(&self) -> &str {
        match self {
            Self::Dependency { message, .. }
            | Self::InvalidState { message, .. }
            | Self::ProvisionedThroughput { message, .. } => message,
        }
    }

    // --- Convenience constructors mirroring the Java single/two-arg ctors. ---
    //
    // `DependencyException` and `ProvisionedThroughputException` only expose
    // `(Throwable)` / `(String, Throwable)` constructors in Java (no
    // message-only ctor), whereas `InvalidStateException` also has a
    // message-only ctor. We provide the full set for ergonomics; the
    // message-only helpers on Dependency/ProvisionedThroughput are additive and
    // harmless.

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

    pub fn provisioned_throughput(message: impl Into<String>) -> Self {
        Self::ProvisionedThroughput {
            message: message.into(),
            source: None,
        }
    }

    pub fn provisioned_throughput_caused_by(
        message: impl Into<String>,
        source: impl Into<BoxError>,
    ) -> Self {
        Self::ProvisionedThroughput {
            message: message.into(),
            source: Some(source.into()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn display_includes_class_name_and_message() {
        assert_eq!(
            LeasingError::invalid_state("table missing").to_string(),
            "InvalidStateException: table missing"
        );
        assert_eq!(
            LeasingError::dependency("ddb down").to_string(),
            "DependencyException: ddb down"
        );
        assert_eq!(
            LeasingError::provisioned_throughput("throttled").to_string(),
            "ProvisionedThroughputException: throttled"
        );
    }

    #[test]
    fn cause_is_exposed_as_error_source() {
        use std::error::Error;
        let cause = std::io::Error::other("boom");
        let e = LeasingError::dependency_caused_by("wrapped", cause);
        assert!(e.source().is_some());
        assert_eq!(e.message(), "wrapped");
    }
}
