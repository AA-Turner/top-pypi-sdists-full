//! Heterodyne, or downconverting, or Mixdown,
//! is the process of multiplying a signal by a complex sine wave
//! of a certain frequency
//! this has the effect of shifting signal components down in frequency, centered around
//! the frequency of the sine wave, so that frequencies below the sine wave frequency end up
//! as low-amplitude negative frequencies, and frequencies above the sine wave frequency end up
//! as low-amplitude positive frequencies.  this allows capturing of a
//! narrow band with a high center frequency at nyquist frequency that depends on the band width
//! rather than the upper frequency of the band.
//!
//! Because the sine wave is complex, cos (2 pi f) + i * sin(2 pi f), the output is always complex.
//!
//! This pipeline takes a real-valued signal and mixes it down into a complex signal.

use crate::AccumulationStats;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::gds_sigp::heterodyne::mix_down;
use futures::FutureExt;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use pipeline_macros::box_async;
use pipelines::complex::c128;
use pipelines::stateless::Stateless1;
use pipelines::{PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[derive(Clone, Debug)]
pub struct Heterodyne {
    mix_freq_hz: f64,
    start_time_pip: PipInstant,
    time_offset_pip: PipDuration,
    sample_period_pip: PipDuration,
}

impl Heterodyne {
    /// Offset calculation references process() in cds-crtools channelinput.cc
    /// ### References
    /// 1. cds-crtools channelinput.cc process()
    ///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/storage/channelinput.cc#L669
    #[box_async]
    fn generate(
        _rc: Box<dyn UserMsgProvider>,
        _name: String,
        config: &Heterodyne,
        input: Arc<TimeDomainArray<f64>>,
    ) -> PipeResult<TimeDomainArray<c128>> {
        let offset_pip: PipDuration =
            input.start_gps_pip - config.time_offset_pip - config.start_time_pip;
        let y = mix_down(
            input.data.as_slice(),
            config.sample_period_pip.to_seconds(),
            offset_pip.to_seconds(),
            config.mix_freq_hz,
        );
        TimeDomainArray {
            start_gps_pip: input.start_gps_pip,
            period_pip: input.period_pip,
            data: y,
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: input.total_gap_size,
            id: input.id.clone(),
            unit: input.unit.clone(),
            real_end_gps_pip: None,
        }
        .into()
    }

    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        mix_freq_hz: f64,
        start_time_pip: PipInstant,
        time_offset_pip: PipDuration,
        sample_period_pip: PipDuration,
        input: &PipelineSubscriber<TimeDomainArray<f64>>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<c128>>, DTTError> {
        let config = Heterodyne {
            mix_freq_hz,
            start_time_pip,
            time_offset_pip,
            sample_period_pip,
        };

        Ok(Stateless1::create(rc, name.into(), Heterodyne::generate, config, input).await?)
    }
}
