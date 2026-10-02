//! Port of `software.amazon.kinesis.common.StreamConfig`.

use crate::common::{InitialPositionInStreamExtended, StreamIdentifier};

/// Configuration for a single Kinesis stream: its identity, the initial position
/// to start consuming from, and an optional consumer ARN (set for enhanced
/// fan-out consumers).
///
/// Port of the Lombok `@Data @Accessors(fluent = true)` class. `streamIdentifier`
/// and `initialPositionInStreamExtended` are `final` (set at construction);
/// `consumerArn` is mutable via a fluent setter. `@NonNull` on `streamIdentifier`
/// is a compile-time guarantee here (non-`Option` field).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct StreamConfig {
    stream_identifier: StreamIdentifier,
    initial_position_in_stream_extended: InitialPositionInStreamExtended,
    consumer_arn: Option<String>,
}

impl StreamConfig {
    /// Construct with a stream identifier and initial position; `consumerArn`
    /// defaults to unset (Java `@RequiredArgsConstructor`).
    pub fn new(
        stream_identifier: StreamIdentifier,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> Self {
        Self {
            stream_identifier,
            initial_position_in_stream_extended,
            consumer_arn: None,
        }
    }

    /// Construct with all fields (Java `@AllArgsConstructor`).
    pub fn with_consumer_arn(
        stream_identifier: StreamIdentifier,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
        consumer_arn: Option<String>,
    ) -> Self {
        Self {
            stream_identifier,
            initial_position_in_stream_extended,
            consumer_arn,
        }
    }

    /// The stream identifier.
    pub fn stream_identifier(&self) -> &StreamIdentifier {
        &self.stream_identifier
    }

    /// The initial position in the stream.
    pub fn initial_position_in_stream_extended(&self) -> &InitialPositionInStreamExtended {
        &self.initial_position_in_stream_extended
    }

    /// The consumer ARN, if set.
    pub fn consumer_arn(&self) -> Option<&str> {
        self.consumer_arn.as_deref()
    }

    /// Fluent setter for the consumer ARN (Lombok generated `consumerArn(String)`).
    ///
    /// Returns `self` for chaining, mirroring Lombok's `@Accessors(fluent=true)`
    /// setter which returns the mutated instance.
    pub fn set_consumer_arn(mut self, consumer_arn: impl Into<String>) -> Self {
        self.consumer_arn = Some(consumer_arn.into());
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::InitialPositionInStream;

    #[test]
    fn stores_identifier_and_position() {
        let si = StreamIdentifier::single_stream_instance("my-stream");
        let pos = InitialPositionInStreamExtended::new_initial_position(
            InitialPositionInStream::TrimHorizon,
        );
        let config = StreamConfig::new(si.clone(), pos);
        assert_eq!(config.stream_identifier(), &si);
        assert_eq!(config.initial_position_in_stream_extended(), &pos);
        assert_eq!(config.consumer_arn(), None);
    }

    #[test]
    fn consumer_arn_is_settable() {
        let si = StreamIdentifier::single_stream_instance("my-stream");
        let pos =
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest);
        let config = StreamConfig::new(si, pos).set_consumer_arn("arn:aws:kinesis:...:consumer/x");
        assert_eq!(
            config.consumer_arn(),
            Some("arn:aws:kinesis:...:consumer/x")
        );
    }

    // Java StreamConfigTest.testNullStreamIdentifier expects NullPointerException
    // when the stream identifier is null. In Rust the field is non-`Option`, so a
    // null identifier is unrepresentable at compile time — the invariant is
    // enforced by the type system rather than a runtime check.
}
