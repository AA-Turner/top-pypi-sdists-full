//! take the square root of the input

use crate::analysis::types::math_traits::Sqrt;
use crate::errors::DTTError;
use pipelines::stateless::pure::PureStatelessPipeline1;
use pipelines::{PipeData, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn sqrt<T>(_rc: Box<dyn UserMsgProvider>, _name: String, input: Arc<T>) -> Arc<T::Output>
where
    T: Sqrt,
{
    Arc::new(input.square_root())
}

pub(crate) async fn create<T>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input: &PipelineSubscriber<T>,
) -> Result<PipelineSubscriber<<T as Sqrt>::Output>, DTTError>
where
    T: Sqrt + PipeData,
{
    Ok(PureStatelessPipeline1::start(rc, name, input, sqrt).await?)
}
