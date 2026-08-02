//! shift start time
//! this is functionally different from timedelay how?
//! yet cds-crtools channelinput.cc process() does both
//! ### References
//! 1. cds-crtools channelinput.cc process()
//!    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L702

use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use futures::FutureExt;
use ligo_hires_gps_time::PipDuration;
use pipeline_macros::box_async;
use pipelines::stateless::Stateless1;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[box_async]
fn time_shift_gen<T: PipeDataPrimitive>(
    _rc: Box<dyn UserMsgProvider>,
    _name: String,
    time_shift_pip: &PipDuration,
    input: Arc<TimeDomainArray<T>>,
) -> PipeResult<TimeDomainArray<T>> {
    let mut new_array = input.as_ref().clone();
    let ts = time_shift_pip.clone();
    new_array.start_gps_pip -= ts;
    new_array.into()
}

pub(crate) async fn start_timeshift<T: PipeDataPrimitive>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    time_shift_pip: PipDuration,
    input: &PipelineSubscriber<TimeDomainArray<T>>,
) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError> {
    Ok(Stateless1::create(rc, name.into(), time_shift_gen, time_shift_pip, input).await?)
}
