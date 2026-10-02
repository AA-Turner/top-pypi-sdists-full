//! Port of `software.amazon.kinesis.processor.ProcessorConfig`.

use std::sync::Arc;

use crate::processor::shard_record_processor_factory::ShardRecordProcessorFactory;

/// Top-level configuration for the processing stage: the mandatory
/// [`ShardRecordProcessorFactory`] and a flag controlling whether
/// `process_records` is invoked for empty record batches.
///
/// Port of the Lombok `@Data @Accessors(fluent=true)` class. The factory field
/// is `final` in Java (no setter, `@NonNull`) — modelled here as an immutable
/// field set once at construction (`Arc` because the factory is shared across
/// shards). `callProcessRecordsEvenForEmptyRecordList` defaults to `false` and
/// has a fluent setter.
#[derive(Clone)]
pub struct ProcessorConfig {
    shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    call_process_records_even_for_empty_record_list: bool,
}

impl ProcessorConfig {
    /// Construct with the (non-null) factory. `@NonNull` is enforced by the
    /// non-`Option` parameter type.
    pub fn new(
        shard_record_processor_factory: Arc<dyn ShardRecordProcessorFactory + Send + Sync>,
    ) -> Self {
        Self {
            shard_record_processor_factory,
            call_process_records_even_for_empty_record_list: false,
        }
    }

    /// The shard record processor factory (no setter — `final` in Java).
    pub fn shard_record_processor_factory(
        &self,
    ) -> &Arc<dyn ShardRecordProcessorFactory + Send + Sync> {
        &self.shard_record_processor_factory
    }

    /// Whether `process_records` is called for empty record lists.
    pub fn call_process_records_even_for_empty_record_list(&self) -> bool {
        self.call_process_records_even_for_empty_record_list
    }

    /// Fluent setter for `callProcessRecordsEvenForEmptyRecordList`.
    ///
    /// Returns `self` for chaining, matching Lombok's `@Accessors(fluent=true)`
    /// setter.
    pub fn set_call_process_records_even_for_empty_record_list(mut self, value: bool) -> Self {
        self.call_process_records_even_for_empty_record_list = value;
        self
    }
}

impl std::fmt::Debug for ProcessorConfig {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ProcessorConfig")
            .field(
                "call_process_records_even_for_empty_record_list",
                &self.call_process_records_even_for_empty_record_list,
            )
            .finish_non_exhaustive()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::StreamIdentifier;
    use crate::processor::shard_record_processor::{
        MockShardRecordProcessor, ShardRecordProcessor,
    };

    struct TestFactory;
    impl ShardRecordProcessorFactory for TestFactory {
        fn shard_record_processor(&self) -> Box<dyn ShardRecordProcessor + Send + Sync> {
            Box::new(MockShardRecordProcessor::new())
        }
    }

    #[test]
    fn default_flag_is_false_and_settable() {
        let config = ProcessorConfig::new(Arc::new(TestFactory));
        assert!(!config.call_process_records_even_for_empty_record_list());

        let config = config.set_call_process_records_even_for_empty_record_list(true);
        assert!(config.call_process_records_even_for_empty_record_list());

        // Factory is usable.
        let id = StreamIdentifier::single_stream_instance("s");
        let _ = config
            .shard_record_processor_factory()
            .shard_record_processor_for_stream(&id);
    }
}
