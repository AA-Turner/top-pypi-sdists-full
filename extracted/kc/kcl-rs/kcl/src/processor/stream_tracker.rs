//! Port of `software.amazon.kinesis.processor.StreamTracker`.

use crate::common::{
    InitialPositionInStream, InitialPositionInStreamExtended, StreamConfig, StreamIdentifier,
};
use crate::processor::former_streams_leases_deletion_strategy::FormerStreamsLeasesDeletionStrategy;

/// SPI telling KCL which stream(s)/[`StreamConfig`]s to process, how to configure
/// orphaned streams, and how to clean up leases for streams no longer tracked.
///
/// Port of the Java interface, including its default methods
/// (`orphaned_stream_initial_position_in_stream`, `create_stream_config`) and
/// the `DEFAULT_POSITION_IN_STREAM` static. Since
/// [`InitialPositionInStreamExtended`] cannot be built in a `const` context, the
/// Java `static final DEFAULT_POSITION_IN_STREAM` is exposed as the associated
/// function [`default_position_in_stream`](StreamTracker::default_position_in_stream)
/// (= `LATEST`).
///
/// `is_multi_stream` is documented as an invariant that must be consistent at
/// runtime, matching the Java contract.
pub trait StreamTracker {
    /// Default position to begin consuming from a Kinesis stream (`LATEST`).
    ///
    /// Port of the `DEFAULT_POSITION_IN_STREAM` static final field.
    fn default_position_in_stream() -> InitialPositionInStreamExtended
    where
        Self: Sized,
    {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
    }

    /// The list of stream configs to be processed. May change during runtime;
    /// KCL calls this periodically to learn about stream changes.
    fn stream_config_list(&self) -> Vec<StreamConfig>;

    /// Strategy for deleting leases of old streams. Must not change during runtime.
    fn former_streams_leases_deletion_strategy(
        &self,
    ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync>;

    /// The initial position for an "orphaned" stream (present in the lease table
    /// but not tracked). Defaults to `LATEST` for faster shard end.
    fn orphaned_stream_initial_position_in_stream(&self) -> InitialPositionInStreamExtended {
        InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest)
    }

    /// Create a new [`StreamConfig`] for the provided stream identifier, using
    /// [`orphaned_stream_initial_position_in_stream`](Self::orphaned_stream_initial_position_in_stream).
    fn create_stream_config(&self, stream_identifier: StreamIdentifier) -> StreamConfig {
        StreamConfig::new(
            stream_identifier,
            self.orphaned_stream_initial_position_in_stream(),
        )
    }

    /// Whether this application should consume more than one Kinesis stream.
    ///
    /// **Must be consistent** across calls; varying the value has indeterminate
    /// effects (mirroring the Java contract).
    fn is_multi_stream(&self) -> bool;
}
