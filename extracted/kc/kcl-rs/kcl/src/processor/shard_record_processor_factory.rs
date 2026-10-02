//! Port of `software.amazon.kinesis.processor.ShardRecordProcessorFactory`.

use crate::common::StreamIdentifier;
use crate::processor::shard_record_processor::ShardRecordProcessor;

/// Factory that creates a new [`ShardRecordProcessor`] per shard (KCL calls this
/// once per lease/shard assignment).
///
/// Ported as a **synchronous**, object-safe trait. The stream-aware method has a
/// default implementation delegating to the no-arg one (matching the Java
/// default method), so single-stream applications only implement
/// [`shard_record_processor`](ShardRecordProcessorFactory::shard_record_processor).
///
/// A shared factory may be invoked concurrently across shards, hence the
/// `Send + Sync` bound on the produced processors.
pub trait ShardRecordProcessorFactory {
    /// Returns a new [`ShardRecordProcessor`] instance.
    fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync>;

    /// Returns a new [`ShardRecordProcessor`] for a given stream identifier.
    ///
    /// Defaults to [`shard_record_processor`](Self::shard_record_processor),
    /// preserving backward-compatible fallback semantics for single-stream apps.
    fn shard_record_processor_for_stream(
        &self,
        _stream_identifier: &StreamIdentifier,
    ) -> Box<dyn ShardRecordProcessor + Send + Sync> {
        self.shard_record_processor()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::processor::shard_record_processor::MockShardRecordProcessor;

    struct TestFactory;

    impl ShardRecordProcessorFactory for TestFactory {
        fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
            Box::new(MockShardRecordProcessor::new())
        }
    }

    #[test]
    fn stream_aware_default_delegates_to_no_arg() {
        let factory = TestFactory;
        // Both paths produce a processor without panicking.
        let _ = factory.shard_record_processor();
        let id = StreamIdentifier::single_stream_instance("my-stream");
        let _ = factory.shard_record_processor_for_stream(&id);
    }
}
