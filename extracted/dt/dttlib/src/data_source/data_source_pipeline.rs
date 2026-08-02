use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::data_source::buffer::Buffer;
use crate::errors::DTTError;
use futures::future::FutureExt;
use pipeline_macros::box_async;
use pipelines::pipe::Pipe0;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use tokio::sync::mpsc;
use user_messages::UserMsgProvider;

type _DataSourceSender = mpsc::Sender<Buffer>;
type DataSourceReceiver = mpsc::Receiver<Buffer>;

/// A 0-input pipeline (pipeline Source) for NDS data
/// produces output for the anlysis pipeline.
/// Each channel gets its own pipeline
///
/// The pipeline comes with a sender.
/// Send NDS2 Buffers to the pipeline.  they will be transformed
/// into TimneDomainArrays and sent as pipeline outputs.
pub struct DataSourcePipeline {
    source: DataSourceReceiver,
}

impl DataSourcePipeline {
    #[box_async]
    fn generate<T: PipeDataPrimitive>(
        rc: Box<dyn UserMsgProvider>,
        state: &mut DataSourcePipeline,
    ) -> PipeResult<TimeDomainArray<T>>
    where
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        let buffer = match state.source.recv().await {
            None => return PipeResult::Close,
            Some(b) => b,
        };
        let td: TimeDomainArray<T> = match buffer.try_into() {
            Ok(t) => t,
            Err(e) => {
                let msg = format!("Error when trying to source data: {}", e.to_string());
                rc.user_message_handle().error(msg);
                return PipeResult::Close;
            }
        };
        td.into()
    }

    /// create a pipeline subscriber and an mpsc channel to send NDS2 Client Buffers
    pub fn create<T: PipeDataPrimitive>(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        source: DataSourceReceiver,
    ) -> PipelineSubscriber<TimeDomainArray<T>>
    where
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        let ds = DataSourcePipeline { source };

        Pipe0::create(rc, name, DataSourcePipeline::generate, ds, None, None)
    }
}
