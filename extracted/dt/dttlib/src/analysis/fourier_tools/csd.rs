//! Calculate the Cross Spectral Density (CSD) of an incoming FFT value
//! takes two fft inputs (X,Y) and calculates conj(X) * Y for every frequency bucket
//! the start times, sizes, and bucket width must be the same otherwise an error is issued
//! and no outputs are sent.

use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::errors::DTTError;
use crate::{Accumulation, AnalysisId, analysis_id};
use futures::future::FutureExt;
use pipeline_macros::box_async;
use pipelines::complex::c128;
use pipelines::stateless::Stateless2;
use pipelines::{PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn cross_spectral_density(
    x: &FreqDomainArray<c128>,
    y: &FreqDomainArray<c128>,
) -> Result<FreqDomainArray<c128>, DTTError> {
    // check that the arrays are compatible
    if x.bucket_width_hz != y.bucket_width_hz {
        return Err(DTTError::CalcError(
            "input frequency bucket widths do not match".into(),
        ));
    }

    if x.start_gps_pip != y.start_gps_pip {
        return Err(DTTError::CalcError("input start times do not match".into()));
    }

    if x.start_hz != y.start_hz {
        return Err(DTTError::CalcError(
            "input start frequencies do not match".into(),
        ));
    }

    let len = x.len().min(y.len());

    let mut csd = Vec::with_capacity(len);

    for i in 0..len {
        csd.push(x.data[i].conj() * y.data[i]);
    }

    let id = analysis_id!("CSD", x.id.clone(), y.id.clone());
    let unit = &x.unit * &y.unit;

    Ok(FreqDomainArray::new(
        id,
        unit,
        x.start_gps_pip,
        x.start_hz,
        x.bucket_width_hz,
        x.overlap,
        csd,
        x.get_accumulation_stats().clone(),
    ))
}

#[box_async]
fn generate(
    rc: Box<dyn UserMsgProvider>,
    name: String,
    _config: &(),
    input1: Arc<FreqDomainArray<c128>>,
    input2: Arc<FreqDomainArray<c128>>,
) -> PipeResult<FreqDomainArray<c128>> {
    let output = match cross_spectral_density(input1.as_ref(), input2.as_ref()) {
        Ok(csd) => Arc::new(csd),
        Err(e) => {
            rc.user_message_handle()
                .set_error("CSDError", format!("{}: {}", name, e));
            return PipeResult::Output(Vec::new());
        }
    };

    rc.user_message_handle().clear_message("CSDError");
    output.into()
}

pub(crate) async fn create(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input1: &PipelineSubscriber<FreqDomainArray<c128>>,
    input2: &PipelineSubscriber<FreqDomainArray<c128>>,
) -> Result<PipelineSubscriber<FreqDomainArray<c128>>, DTTError> {
    Ok(Stateless2::create(rc, name.into(), generate, (), input1, input2).await?)
}
