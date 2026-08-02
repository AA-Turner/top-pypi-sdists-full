//! Give the real value of a complex frequency domain input.

use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::errors::DTTError;
use crate::{AnalysisId, analysis_id};
use pipelines::PipelineSubscriber;
use pipelines::complex::c128;
use pipelines::stateless::pure::PureStatelessPipeline1;
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn real(input: &FreqDomainArray<c128>) -> FreqDomainArray<f64> {
    let data = input.data.iter().map(|x| x.re).collect();
    let id = analysis_id!("Re", input.id.clone());
    let unit = input.unit.clone();
    input.clone_metadata(id, unit, data)
}

fn generate(
    _rc: Box<dyn UserMsgProvider>,
    _name: String,
    input: Arc<FreqDomainArray<c128>>,
) -> Arc<FreqDomainArray<f64>> {
    let r = real(input.as_ref());
    Arc::new(r)
}

pub(crate) async fn create(
    rc: Box<dyn UserMsgProvider>,
    name: String,
    input: &PipelineSubscriber<FreqDomainArray<c128>>,
) -> Result<PipelineSubscriber<FreqDomainArray<f64>>, DTTError> {
    Ok(PureStatelessPipeline1::start(rc, name, input, generate).await?)
}
