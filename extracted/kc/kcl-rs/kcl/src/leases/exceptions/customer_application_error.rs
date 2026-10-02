//! Port of
//! `software.amazon.kinesis.leases.exceptions.CustomerApplicationException`.

use thiserror::Error;

use crate::exceptions::BoxError;

/// Error type for failures thrown by customer-implemented code (e.g. a record
/// processor callback).
///
/// Kept deliberately **separate** from [`LeasingError`] so callers can
/// distinguish a customer bug from a leasing-infrastructure failure — the same
/// distinction the Java `CustomerApplicationException` (a standalone `Exception`
/// subclass, *not* part of the `LeasingException` hierarchy) encodes.
///
/// [`LeasingError`]: crate::leases::exceptions::LeasingError
#[derive(Debug, Error)]
#[error("CustomerApplicationException: {message}")]
pub struct CustomerApplicationError {
    message: String,
    #[source]
    source: Option<BoxError>,
}

impl CustomerApplicationError {
    /// Java `CustomerApplicationException(String)`.
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
            source: None,
        }
    }

    /// Java `CustomerApplicationException(String, Throwable)`.
    pub fn with_cause(message: impl Into<String>, source: impl Into<BoxError>) -> Self {
        Self {
            message: message.into(),
            source: Some(source.into()),
        }
    }

    /// Java `CustomerApplicationException(Throwable)`.
    ///
    /// Java's single-`Throwable` `Exception` constructor sets the message to the
    /// cause's `toString()`; we mirror that.
    pub fn from_cause(source: impl Into<BoxError>) -> Self {
        let source = source.into();
        let message = source.to_string();
        Self {
            message,
            source: Some(source),
        }
    }

    /// The exception message (Java `getMessage`).
    pub fn message(&self) -> &str {
        &self.message
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn message_only() {
        let e = CustomerApplicationError::new("processor blew up");
        assert_eq!(e.message(), "processor blew up");
        assert_eq!(
            e.to_string(),
            "CustomerApplicationException: processor blew up"
        );
    }

    #[test]
    fn from_cause_uses_cause_string_as_message() {
        use std::error::Error;
        let cause = std::io::Error::other("root cause");
        let e = CustomerApplicationError::from_cause(cause);
        assert_eq!(e.message(), "root cause");
        assert!(e.source().is_some());
    }
}
