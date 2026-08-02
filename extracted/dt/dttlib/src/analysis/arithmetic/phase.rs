//! Get the phase of a complex signal

use crate::analysis::types::math_traits::Phase;
use crate::errors::DTTError;
use pipelines::stateless::pure::PureStatelessPipeline1;
use pipelines::{PipeData, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn phase<T>(_rc: Box<dyn UserMsgProvider>, _name: String, input: Arc<T>) -> Arc<T::Output>
where
    T: Phase + std::fmt::Debug,
{
    log::debug!("getting phase from complex");
    let out = Arc::new(input.phase());
    out
}

pub(crate) async fn create<T>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input: &PipelineSubscriber<T>,
) -> Result<PipelineSubscriber<<T as Phase>::Output>, DTTError>
where
    T: Phase + PipeData + std::fmt::Debug,
{
    log::debug!("creating phase pipeline");
    Ok(PureStatelessPipeline1::start(rc, name, input, phase).await?)
}
