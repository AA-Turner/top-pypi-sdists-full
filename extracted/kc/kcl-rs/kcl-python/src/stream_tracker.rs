//! A minimal multi-stream [`StreamTracker`] built from Python-supplied stream
//! identifiers.
//!
//! The Rust core exposes [`SingleStreamTracker`] (a concrete struct) but only a
//! *marker trait* `MultiStreamTracker` — there is no concrete multi-stream
//! tracker to hand to `ConfigsBuilder::new`. This module provides one: a small
//! [`StreamTracker`] implementation that wraps a list of [`StreamConfig`]s,
//! reports `is_multi_stream() == true`, and never deletes former-stream leases
//! (the `NoLeaseDeletionStrategy`, matching the Java default).
//!
//! Each stream is identified by a *serialized multi-stream identifier* of the
//! form `<accountId>:<streamName>:<creationEpoch>` — the same form the KCL uses
//! as the lease-key prefix in multi-stream mode (see
//! [`StreamIdentifier::multi_stream_instance`]).

use kcl::common::{InitialPositionInStreamExtended, StreamConfig, StreamIdentifier};
use kcl::processor::{
    FormerStreamsLeasesDeletionStrategy, MultiStreamTracker, NoLeaseDeletionStrategy, StreamTracker,
};

/// A concrete multi-stream [`StreamTracker`] over a fixed list of streams.
pub struct PyMultiStreamTracker {
    stream_configs: Vec<StreamConfig>,
}

impl PyMultiStreamTracker {
    /// Build from serialized multi-stream identifiers
    /// (`accountId:streamName:creationEpoch`), all sharing one initial position.
    ///
    /// Returns an error string if the list is empty or an identifier does not
    /// parse (rather than panicking, since these come straight from Python).
    pub fn from_serialized(
        serialized_identifiers: &[String],
        initial_position: InitialPositionInStreamExtended,
    ) -> Result<Self, String> {
        if serialized_identifiers.is_empty() {
            return Err("multi-stream mode requires at least one stream identifier".to_string());
        }
        let mut stream_configs = Vec::with_capacity(serialized_identifiers.len());
        for serialized in serialized_identifiers {
            // `multi_stream_instance` panics on a bad identifier; validate the
            // shape first so we can return a clean Python error instead.
            let identifier = parse_multi_stream_identifier(serialized)?;
            stream_configs.push(StreamConfig::new(identifier, initial_position));
        }
        Ok(Self { stream_configs })
    }
}

/// Validate + parse a serialized `accountId:streamName:creationEpoch` identifier.
///
/// `StreamIdentifier::multi_stream_instance` panics on a malformed input; we
/// pre-validate the three colon-separated, non-empty parts (with a numeric
/// creation epoch) so a bad value from Python surfaces as a `ValueError` rather
/// than a panic that would abort the interpreter.
fn parse_multi_stream_identifier(serialized: &str) -> Result<StreamIdentifier, String> {
    let parts: Vec<&str> = serialized.split(':').collect();
    if parts.len() != 3 || parts.iter().any(|p| p.is_empty()) {
        return Err(format!(
            "invalid multi-stream identifier {serialized:?}; expected \
             'accountId:streamName:creationEpoch'"
        ));
    }
    if parts[2].parse::<i64>().is_err() {
        return Err(format!(
            "invalid multi-stream identifier {serialized:?}; creationEpoch \
             (third part) must be an integer"
        ));
    }
    Ok(StreamIdentifier::multi_stream_instance(serialized))
}

impl StreamTracker for PyMultiStreamTracker {
    fn stream_config_list(&self) -> Vec<StreamConfig> {
        self.stream_configs.clone()
    }

    fn former_streams_leases_deletion_strategy(
        &self,
    ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync> {
        Box::new(NoLeaseDeletionStrategy)
    }

    fn is_multi_stream(&self) -> bool {
        true
    }
}

impl MultiStreamTracker for PyMultiStreamTracker {}

#[cfg(test)]
mod tests {
    use super::*;
    use kcl::common::{InitialPositionInStream, InitialPositionInStreamExtended};

    fn latest() -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
    }

    #[test]
    fn builds_multi_stream_configs() {
        let tracker = PyMultiStreamTracker::from_serialized(
            &[
                "123456789012:stream-a:1680000000".to_string(),
                "123456789012:stream-b:1680000001".to_string(),
            ],
            latest(),
        )
        .unwrap();
        assert!(tracker.is_multi_stream());
        let configs = tracker.stream_config_list();
        assert_eq!(configs.len(), 2);
        assert_eq!(configs[0].stream_identifier().stream_name(), "stream-a");
        assert_eq!(configs[1].stream_identifier().stream_name(), "stream-b");
    }

    #[test]
    fn empty_list_is_rejected() {
        assert!(PyMultiStreamTracker::from_serialized(&[], latest()).is_err());
    }

    #[test]
    fn malformed_identifier_is_rejected_not_panicked() {
        assert!(
            PyMultiStreamTracker::from_serialized(&["not-serialized".to_string()], latest())
                .is_err()
        );
        assert!(PyMultiStreamTracker::from_serialized(
            &["acct:name:notanumber".to_string()],
            latest()
        )
        .is_err());
    }
}
