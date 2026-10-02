//! Port of `software.amazon.kinesis.processor.MultiStreamTracker`.

use crate::processor::stream_tracker::StreamTracker;

/// Refinement of [`StreamTracker`] for applications consuming multiple Kinesis
/// streams.
///
/// In Java this is a marker interface whose only content is a default method
/// override forcing `isMultiStream()` to `true`. Rust subtraits cannot override
/// a supertrait's default method, so this is a marker trait; implementors must
/// return `true` from [`StreamTracker::is_multi_stream`]. The marker still lets
/// call sites bound on `MultiStreamTracker` to express the multi-stream
/// requirement.
pub trait MultiStreamTracker: StreamTracker {}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::StreamConfig;
    use crate::processor::former_streams_leases_deletion_strategy::{
        FormerStreamsLeasesDeletionStrategy, NoLeaseDeletionStrategy,
    };

    struct MyMultiTracker {
        configs: Vec<StreamConfig>,
    }

    impl StreamTracker for MyMultiTracker {
        fn stream_config_list(&self) -> Vec<StreamConfig> {
            self.configs.clone()
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

    impl MultiStreamTracker for MyMultiTracker {}

    #[test]
    fn multi_stream_tracker_reports_true() {
        let t = MyMultiTracker { configs: vec![] };
        assert!(t.is_multi_stream());
    }
}
