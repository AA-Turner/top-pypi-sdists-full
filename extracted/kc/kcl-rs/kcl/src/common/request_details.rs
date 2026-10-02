//! Port of `software.amazon.kinesis.common.RequestDetails`.

use std::fmt;

/// Placeholder used in logs when no successful request has been made.
const NONE: &str = "NONE";

/// Lightweight holder for the request id + timestamp of the last successful AWS
/// API call, used for diagnostic logging when a subsequent request fails (so
/// operators can correlate a failed request with the last successful one).
///
/// Port of the Java class. `getRequestId()`/`getTimestamp()` return the stored
/// value or the literal `"NONE"` when absent; [`Display`](fmt::Display) mirrors
/// the exact `"request id - {}, timestamp - {}"` format.
///
/// Both fields are effectively immutable after construction.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RequestDetails {
    request_id: Option<String>,
    timestamp: Option<String>,
}

impl Default for RequestDetails {
    /// Java no-arg constructor: both fields empty.
    fn default() -> Self {
        Self {
            request_id: None,
            timestamp: None,
        }
    }
}

impl RequestDetails {
    /// Java no-arg constructor: both fields empty.
    pub fn empty() -> Self {
        Self::default()
    }

    /// Java 2-arg constructor: wraps both values as present.
    pub fn new(request_id: impl Into<String>, timestamp: impl Into<String>) -> Self {
        Self {
            request_id: Some(request_id.into()),
            timestamp: Some(timestamp.into()),
        }
    }

    /// The last successful request's request id, or `"NONE"` if absent.
    pub fn request_id(&self) -> &str {
        self.request_id.as_deref().unwrap_or(NONE)
    }

    /// The last successful request's timestamp, or `"NONE"` if absent.
    pub fn timestamp(&self) -> &str {
        self.timestamp.as_deref().unwrap_or(NONE)
    }
}

impl fmt::Display for RequestDetails {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "request id - {}, timestamp - {}",
            self.request_id(),
            self.timestamp()
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_renders_none() {
        let d = RequestDetails::empty();
        assert_eq!(d.request_id(), "NONE");
        assert_eq!(d.timestamp(), "NONE");
        assert_eq!(d.to_string(), "request id - NONE, timestamp - NONE");
    }

    #[test]
    fn present_values_render() {
        let d = RequestDetails::new("req-123", "2024-01-01T00:00:00Z");
        assert_eq!(d.request_id(), "req-123");
        assert_eq!(d.timestamp(), "2024-01-01T00:00:00Z");
        assert_eq!(
            d.to_string(),
            "request id - req-123, timestamp - 2024-01-01T00:00:00Z"
        );
    }

    #[test]
    fn default_is_empty() {
        assert_eq!(RequestDetails::default(), RequestDetails::empty());
    }
}
