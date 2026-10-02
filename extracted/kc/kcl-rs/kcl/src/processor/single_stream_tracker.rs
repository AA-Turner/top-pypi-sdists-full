//! Port of `software.amazon.kinesis.processor.SingleStreamTracker`.

use crate::common::arn::Arn;
use crate::common::{InitialPositionInStreamExtended, StreamConfig, StreamIdentifier};
use crate::processor::former_streams_leases_deletion_strategy::{
    FormerStreamsLeasesDeletionStrategy, NoLeaseDeletionStrategy,
};
use crate::processor::stream_tracker::StreamTracker;

/// Concrete [`StreamTracker`] for consuming exactly one Kinesis stream.
///
/// Wraps a single [`StreamIdentifier`]/[`StreamConfig`], never deletes leases,
/// and reports `is_multi_stream() == false`. Port of the Lombok
/// `@EqualsAndHashCode @ToString` class over the `stream_identifier` and
/// `stream_configs` fields. All 6 Java constructors funnel to
/// [`new`](SingleStreamTracker::new); the others are convenience constructors.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct SingleStreamTracker {
    stream_identifier: StreamIdentifier,
    stream_configs: Vec<StreamConfig>,
}

impl SingleStreamTracker {
    /// Primary constructor: `(StreamIdentifier, StreamConfig)`.
    pub fn new(stream_identifier: StreamIdentifier, stream_config: StreamConfig) -> Self {
        Self {
            stream_identifier,
            stream_configs: vec![stream_config],
        }
    }

    /// From a stream name, using the default initial position (`LATEST`).
    pub fn from_stream_name(stream_name: &str) -> Self {
        Self::from_identifier(StreamIdentifier::single_stream_instance(stream_name))
    }

    /// From a stream ARN, using the default initial position (`LATEST`).
    pub fn from_arn(stream_arn: Arn) -> Self {
        Self::from_identifier(StreamIdentifier::single_stream_instance_from_arn(
            stream_arn,
        ))
    }

    /// From a stream identifier, using the default initial position (`LATEST`).
    pub fn from_identifier(stream_identifier: StreamIdentifier) -> Self {
        Self::from_identifier_with_position(
            stream_identifier,
            <Self as StreamTracker>::default_position_in_stream(),
        )
    }

    /// From a stream identifier and an explicit initial position.
    pub fn from_identifier_with_position(
        stream_identifier: StreamIdentifier,
        initial_position: InitialPositionInStreamExtended,
    ) -> Self {
        let config = StreamConfig::new(stream_identifier.clone(), initial_position);
        Self::new(stream_identifier, config)
    }

    /// From a stream name and an explicit initial position.
    pub fn from_stream_name_with_position(
        stream_name: &str,
        initial_position: InitialPositionInStreamExtended,
    ) -> Self {
        Self::from_identifier_with_position(
            StreamIdentifier::single_stream_instance(stream_name),
            initial_position,
        )
    }
}

impl StreamTracker for SingleStreamTracker {
    fn stream_config_list(&self) -> Vec<StreamConfig> {
        self.stream_configs.clone()
    }

    fn former_streams_leases_deletion_strategy(
        &self,
    ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync> {
        Box::new(NoLeaseDeletionStrategy)
    }

    fn is_multi_stream(&self) -> bool {
        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use crate::processor::former_streams_leases_deletion_strategy::StreamsLeasesDeletionType;

    const STREAM_NAME: &str = "SingleStreamTrackerTest";

    fn validate(tracker: &SingleStreamTracker, expected_position: InitialPositionInStreamExtended) {
        assert_eq!(tracker.stream_config_list().len(), 1);
        assert!(!tracker.is_multi_stream());
        assert_eq!(
            tracker
                .former_streams_leases_deletion_strategy()
                .lease_deletion_type(),
            StreamsLeasesDeletionType::NoStreamsLeasesDeletion
        );
        let config = &tracker.stream_config_list()[0];
        assert_eq!(config.stream_identifier().stream_name(), STREAM_NAME);
        assert_eq!(
            config.initial_position_in_stream_extended(),
            &expected_position
        );
    }

    #[test]
    fn test_defaults() {
        let default_pos = <SingleStreamTracker as StreamTracker>::default_position_in_stream();
        validate(
            &SingleStreamTracker::from_stream_name(STREAM_NAME),
            default_pos,
        );
        validate(
            &SingleStreamTracker::from_identifier(StreamIdentifier::single_stream_instance(
                STREAM_NAME,
            )),
            default_pos,
        );
    }

    #[test]
    fn test_initial_position_constructor() {
        let expected_position = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        assert_ne!(
            expected_position,
            <SingleStreamTracker as StreamTracker>::default_position_in_stream()
        );
        let tracker = SingleStreamTracker::from_identifier_with_position(
            StreamIdentifier::single_stream_instance(STREAM_NAME),
            expected_position,
        );
        validate(&tracker, expected_position);
    }

    #[test]
    fn equality_and_hashing() {
        use std::collections::HashSet;
        let a = SingleStreamTracker::from_stream_name(STREAM_NAME);
        let b = SingleStreamTracker::from_stream_name(STREAM_NAME);
        assert_eq!(a, b);
        let mut set = HashSet::new();
        set.insert(a);
        assert!(set.contains(&b));
    }
}
