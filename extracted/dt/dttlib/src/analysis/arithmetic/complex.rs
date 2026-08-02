//! Get the a complex signal from a real and an imaginary part

use crate::analysis::types::math_traits::ToComplex;
use crate::errors::DTTError;
use pipelines::stateless::pure::PureStatelessPipeline2;
use pipelines::{PipeData, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn complex<T>(
    _rc: Box<dyn UserMsgProvider>,
    _name: String,
    input1: Arc<T>,
    input2: Arc<T>,
) -> Arc<T::Output>
where
    T: ToComplex,
{
    log::debug!("converting real and imaginary to complex");
    Arc::new(input1.to_complex(&input2))
}

pub(crate) async fn create<T>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input1: &PipelineSubscriber<T>,
    input2: &PipelineSubscriber<T>,
) -> Result<PipelineSubscriber<<T as ToComplex>::Output>, DTTError>
where
    T: ToComplex + PipeData,
{
    log::debug!("creating complex pipeline");
    Ok(PureStatelessPipeline2::start(rc, name, input1, input2, complex).await?)
}
