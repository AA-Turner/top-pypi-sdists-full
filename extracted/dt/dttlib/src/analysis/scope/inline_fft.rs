//! Create a vector of FFTs from a time domain segment,
//! where each FFT is a block of a subsegment
//! segment is divided first to get specified bandwidth
//! next, to get specified overlap as close as possible.
//! results are suitable for use in Welch's method to get ASD
//! or transfer functions.

use std::sync::Arc;

use ligo_hires_gps_time::{PipDuration, PipInstant};

use crate::analysis::types::MutableAccumulation;
use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::c_math::round_p2;
use crate::errors::DTTError;
use crate::gds_sigp::fft::{FFTParam, FFTTypeInfo, fft};
use crate::params::test_params::FFTWindow;
#[cfg(not(feature = "python"))]
use dtt_macros::new;
use pipelines::complex::c128;
use pipelines::{PipeData, PipeDataPrimitive, PipeResult, PipelineSubscriber};
#[cfg(any(feature = "python"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use user_messages::UserMsgProvider;

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all, set_all))]
#[derive(Clone, Default, Debug)]
pub struct InlineFFTParams {
    pub bandwidth_hz: f64,
    pub overlap: f64,
    pub start_pip: PipInstant,
    pub end_pip: PipInstant,
    pub window: FFTWindow,
}

// #[derive(Clone, Debug)]
// #[cfg_attr(any(feature = "python-pipe", feature = "python"),pyclass(frozen))]
// pub (crate) enum StreamedFFTs {
//     Done(),
//     FFT(FreqDomainArray<c128>),
// }
//
// impl PipeData for StreamedFFTs {}
//
// impl StreamedFFTs {
//     pub (crate) fn set_accumulation_stats(&mut self, stats: crate::AccumulationStats) {
//         match self {
//             Self::Done() => (),
//             Self::FFT(f) => { f.set_accumulation_stats(stats); }
//         }
//     }
// }

impl InlineFFTParams {
    /// Return subsegments that should be passed to the FFT function
    /// Try first to match bandwidth, then overlap.
    fn subsegment<'b, T>(
        &self,
        rc: Box<dyn UserMsgProvider>,
        input: &'b TimeDomainArray<T>,
    ) -> (f64, Vec<&'b [T]>)
    where
        T: PipeData,
    {
        let period = PipDuration::freq_hz_to_period(input.rate_hz());

        let desired_length = (input.rate_hz() / self.bandwidth_hz) as usize;

        // must be power of two
        let length_p2 = round_p2(desired_length as f64) as usize;

        // get real start indexes as constrained by data
        let real_start_pip = self
            .start_pip
            .snap_down_to_step(&period)
            .max(input.start_gps_pip);
        let real_end_pip = self
            .end_pip
            .snap_down_to_step(&period)
            .min(input.end_gps_pip());

        if real_start_pip >= real_end_pip {
            rc.user_message_handle().set_error(
                "FFT Stream Error",
                "Intersection of FFT span with input is empty.",
            );
            return (0.0, vec![]);
        }

        let real_input_length = ((real_end_pip - real_start_pip) / period) as usize;

        let mut length = length_p2;
        while length > real_input_length {
            length /= 2;
        }

        // if there's no data, just quit with nothing.
        if length == 0 {
            rc.user_message_handle()
                .set_error("FFT Stream Error", "No data in FFT range.");
            return (0.0, vec![]);
        }

        if self.overlap >= 1.0 || self.overlap < 0.0 {
            rc.user_message_handle()
                .set_error("FFT Stream Error", "Overlap must be in [0,1) range.");
            return (0.0, vec![]);
        }

        rc.user_message_handle().clear_message("FFT Stream Error");

        // figure out best overlap
        let seg_count = 1.0
            + (real_input_length as f64 - length as f64) / (length as f64 * (1.0 - self.overlap));
        let real_seg_count = seg_count.round() as usize;

        let real_overlap = 1.0
            - (real_input_length as f64 / (length as f64) - 1.0) / (real_seg_count as f64 + 1.0);

        let mut segments = Vec::new();

        let real_seg_duration = length * period;

        for i in 0..real_seg_count {
            let seg_start_pip = real_start_pip + (real_seg_duration * i) * (1.0 - real_overlap);
            let start_index = input.ligo_hires_gps_time_to_index(seg_start_pip);
            segments.push(&input.data[start_index..start_index + length]);
        }

        (real_overlap, segments)
    }

    fn generate<'a, T>(
        rc: Box<dyn UserMsgProvider>,
        config: &'a InlineFFTParams,
        _state: &'a mut (),
        input: Arc<TimeDomainArray<T>>,
    ) -> PipeResult<FreqDomainArray<c128>>
    where
        T: PipeDataPrimitive + FFTTypeInfo + Default,
    {
        // generate segments
        let (real_overlap, segs) = config.subsegment(rc.ump_clone(), input.as_ref());

        if segs.is_empty() {
            return vec![].into();
        }

        // generate fft plan
        let fft_plan = match FFTParam::create::<T>(segs[0].len(), config.window.clone()) {
            Ok(p) => p,
            Err(e) => {
                rc.user_message_handle()
                    .set_error("InlineFFT", format!("Error creating FFT plan: {}", e));
                return vec![].into();
            }
        };

        // take ffts
        let mut ffts = Vec::with_capacity(segs.len());
        let bucket_width_hz = input.rate_hz() / (segs[0].len() as f64);
        let num_segs = segs.len();
        for (i, seg) in segs.into_iter().enumerate() {
            let fft = match fft(seg, &fft_plan, bucket_width_hz, false) {
                Ok(f) => f,
                Err(e) => {
                    rc.user_message_handle()
                        .set_error("InlineFFT", format!("Error taking FFT: {}", e));
                    return vec![].into();
                }
            };
            let mut freq_array = FreqDomainArray::new(
                input.id.clone(),
                input.unit.clone(),
                input.start_gps_pip,
                0.0,
                bucket_width_hz,
                real_overlap,
                fft,
                input.accumulation_stats,
            );
            freq_array.set_mut_sequence_values(i, num_segs);
            ffts.push(Arc::new(freq_array));
        }

        // clean up fft plan
        rc.user_message_handle().clear_message("InlineFFT");
        ffts.into()
    }

    pub(crate) async fn create<T>(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        config_rx: tokio::sync::watch::Receiver<InlineFFTParams>,
        input: &PipelineSubscriber<TimeDomainArray<T>>,
    ) -> Result<PipelineSubscriber<FreqDomainArray<c128>>, DTTError>
    where
        T: PipeDataPrimitive + FFTTypeInfo + Default,
    {
        Ok(pipelines::unsynced_pipe::UnsyncPipe1::create(
            rc,
            name.into(),
            InlineFFTParams::generate,
            Some(config_rx),
            (),
            None,
            None,
            input,
        )
        .await?)
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python"), pymethods)]
impl InlineFFTParams {
    #[new]
    pub fn new() -> Self {
        InlineFFTParams::default()
    }
}
