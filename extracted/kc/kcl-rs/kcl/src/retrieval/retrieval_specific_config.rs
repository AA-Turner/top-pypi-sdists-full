//! Port of `software.amazon.kinesis.retrieval.RetrievalSpecificConfig`.

use crate::retrieval::retrieval_factory::RetrievalFactory;

/// Marker/factory for a specific retrieval mode's configuration (fan-out vs
/// polling): produces its [`RetrievalFactory`] and validates multi-stream
/// compatibility.
///
/// Port of the Java interface. Implemented by `fanout.FanOutConfig` and
/// `polling.PollingConfig` (later waves), both of which override
/// [`validate_state`](Self::validate_state) to `panic!` (Java
/// `IllegalArgumentException`) when stream-specific fields are set in
/// multi-stream mode.
pub trait RetrievalSpecificConfig: Send + Sync {
    /// Create and return the retrieval factory for this configuration.
    ///
    /// Port of `retrievalFactory()`. Returns a boxed [`RetrievalFactory`] so the
    /// coordinator can hold `Box<dyn RetrievalSpecificConfig>`.
    fn retrieval_factory(&self) -> Box<dyn RetrievalFactory>;

    /// Validate that this instance is configured properly, given whether the
    /// application is in multi-stream mode. Should `panic!` (Java
    /// `IllegalArgumentException`) on misconfiguration.
    ///
    /// Port of the Java deprecated `default` `validateState(boolean)`; the
    /// default here is a no-op, matching the Java default body.
    fn validate_state(&self, _is_multi_stream: bool) {
        // Java default is a no-op (deprecated; implementers should override).
    }
}
