//! Calculate real or complex FFT.  Also, trim result to the desired frequency range
//! use a stateless pipeline
//!
//!    This can be real or complex input, but only is complex if Zoom frequency not zero
//!    So I think the possibility of a complex channel without a zoom frequency isn't handled.
//!    Since all channels are reduced to the same rate, and therefore the same sized FFT
//!    Then the entire test can use the same FFT plan.  It only needs to be calculated once
//!    at the start.

use crate::AccumulationStats;
use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::gds_sigp::fft::{FFTParam, FFTTypeInfo, fft};
use crate::timeline::Timeline;
use futures::future::FutureExt;
use ligo_hires_gps_time::PipInstant;
use pipeline_macros::box_async;
use pipelines::complex::c128;
use pipelines::pipe::Pipe1;
use pipelines::{PipeDataPrimitive, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

#[derive(Clone, Debug)]
pub struct FFT {
    start_freq_hz: f64,
    end_freq_hz: f64,
    zoom_freq_hz: f64,
    fft_plan: Arc<FFTParam>,
    remove_dc: bool,
    last_start_pip: Option<PipInstant>,
}

unsafe impl Sync for FFT {}

unsafe impl Send for FFT {}

impl FFT {
    #[box_async]
    fn generate<T: PipeDataPrimitive + FFTTypeInfo>(
        rc: Box<dyn UserMsgProvider>,
        config: &mut Self,
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<FreqDomainArray<c128>> {
        let result = match fft(
            input.data.as_slice(),
            &config.fft_plan,
            input.time_step(),
            config.remove_dc,
        ) {
            Ok(r) => r,
            Err(e) => {
                let msg = format!("In FFT pipeline: {}", e.to_string());
                rc.user_message_handle().error(msg);
                return PipeResult::Close;
            }
        };

        // generate the freq domain structure from the output
        let time_span_pip = input.data.len() as f64 * input.period_pip;
        let bucket_width_hz = time_span_pip.period_to_freq_hz();

        let overlap = match config.last_start_pip {
            None => 0.0,
            Some(s) => {
                1.0 - ((input.start_gps_pip - s) / (input.end_gps_pip() - input.start_gps_pip))
                    as f64
            }
        };

        config.last_start_pip = Some(input.start_gps_pip);

        let id = input.id.clone();
        let unit = input.unit.clone();

        let mut output = FreqDomainArray::new(
            id,
            unit,
            input.start_gps_pip,
            config.start_freq_hz,
            bucket_width_hz,
            overlap,
            Vec::new(),
            AccumulationStats::default(),
        );

        if config.zoom_freq_hz == 0.0 {
            output.insert_and_trim_oneside(result, config.end_freq_hz);
        } else {
            let rot_result = rotate_complex_fft(result.as_slice());
            output.insert_and_trim_twoside(rot_result, config.zoom_freq_hz);
        };

        Arc::new(output).into()
    }

    pub async fn create<T: PipeDataPrimitive + FFTTypeInfo + Default>(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        timeline: &Timeline,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<FreqDomainArray<c128>>, DTTError> {
        let fft_plan = Arc::new(timeline.fft_param::<T>()?);

        let config = Self {
            start_freq_hz: timeline.start_hz,
            end_freq_hz: timeline.stop_hz,
            zoom_freq_hz: timeline.heterodyne_freq_hz,
            remove_dc: timeline.remove_mean,
            last_start_pip: None,
            fft_plan,
        };

        // Turned into a regular pipeline
        // Can't be Stateless because the fftplan is not thread-safe.
        Ok(Pipe1::create(rc, name.into(), Self::generate, config, None, None, input).await?)
    }
}

/// Complex FFTs are returned in 0...nyq...-nyq+1 format, but
/// we want it in -nyq...0...nyq-1 format.  so the first and last halves
/// of the array need to be swapped.  This function does that.
fn rotate_complex_fft(fft_data: &[c128]) -> Vec<c128> {
    let nyq = fft_data.len() / 2;
    let mut new_result = fft_data[nyq..].to_vec();
    new_result.extend_from_slice(&fft_data[0..nyq]);
    new_result
}
