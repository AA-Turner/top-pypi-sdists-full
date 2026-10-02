//! Port of `software.amazon.kinesis.processor.ShutdownNotificationAware`.

use std::sync::Arc;

use crate::processor::record_processor_checkpointer::RecordProcessorCheckpointer;

/// Allows a record processor to indicate it is aware of requested shutdowns and
/// handle the request.
///
/// Ported as a **synchronous** trait for API completeness. Deprecated: this
/// interface is unused in the current KCL flow — [`ShardRecordProcessor`] already
/// provides `shutdown_requested` notifications.
///
/// [`ShardRecordProcessor`]: crate::processor::ShardRecordProcessor
#[deprecated(
    note = "Unused; ShardRecordProcessor::shutdown_requested provides shutdown notifications already."
)]
pub trait ShutdownNotificationAware {
    /// Called when the worker has been requested to shut down, giving the record
    /// processor a chance to checkpoint. The processor will still have shutdown
    /// called afterward.
    fn shutdown_requested(
        &mut self,
        checkpointer: Arc<dyn RecordProcessorCheckpointer + Send + Sync>,
    );
}
