//! Calculate the ASD directly from an FFT
//! Since ASD should be calculated from a PSD, this should not be used.

use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::errors::DTTError;
use crate::gds_sigp::asd::asd;
use crate::{Accumulation, AnalysisId, analysis_id};
use futures::FutureExt;
use pipeline_macros::box_async;
use pipelines::complex::c128;
use pipelines::stateless::Stateless1;
use pipelines::{PipeResult, PipelineSubscriber};
/// Pipeline for calculating Asd from FFT
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[derive(Clone, Debug)]
pub struct ASD {
    has_dc: bool,
}

impl ASD {
    #[box_async]
    fn generate(
        _rc: Box<dyn UserMsgProvider>,
        _name: String,
        config: &Self,
        input: Arc<FreqDomainArray<c128>>,
    ) -> PipeResult<FreqDomainArray<f64>> {
        let a = asd(input.data.as_slice(), config.has_dc);
        let id = analysis_id!("ASD", input.id.clone());
        let unit = input.unit.clone();
        Arc::new(FreqDomainArray::new(
            id,
            unit,
            input.start_gps_pip,
            input.start_hz,
            input.bucket_width_hz,
            input.overlap,
            a,
            input.get_accumulation_stats().clone(),
        ))
        .into()
    }

    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        has_dc: bool,
        input: &PipelineSubscriber<FreqDomainArray<c128>>,
    ) -> Result<PipelineSubscriber<FreqDomainArray<f64>>, DTTError> {
        let config = Self { has_dc };

        Ok(Stateless1::create(rc, name.into(), Self::generate, config, input).await?)
    }
}
