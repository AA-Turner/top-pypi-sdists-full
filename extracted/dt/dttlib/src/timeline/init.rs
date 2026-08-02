//! Use OnceCell to enforce correct initialization error
//! This is a different type from Timeline so that after initialization we can
//! copy these values into an immutable Timeline object that's easier to access

use crate::constraints::{Constraint, check_constraint_list};
use crate::errors::DTTError;
use crate::gds_sigp::fft::{FFTParam, FFTTypeInfo};
use crate::params::channel_params::{ActiveList, ChannelSettings};
use crate::params::constraints::{NUM_GENERAL_PARAM_CONSTRAINTS, general_param_constraints};
use crate::params::excitation_params::ExcitationSettings;
use crate::params::test_params::{StartTime, TestParams, TestType};
use crate::run_context::RunContext;
use crate::timeline::{CalcTimelineResult, CountSegments};
use ligo_hires_gps_time::PipDuration;
use std::cell::OnceCell;

/// Initialization structure for Timeline
/// Do Timeline construction with this struct
/// Then convert .into() a Timeline.
#[derive(Default)]
pub(crate) struct TimelineInit {
    pub(crate) measurement_channels: OnceCell<Vec<ChannelSettings>>,
    pub(crate) excitations: OnceCell<Vec<ExcitationSettings>>,

    /// # Time slice definitions
    /// setup bandwidth
    pub(crate) bandwidth_hz: OnceCell<f64>,
    /// bandwidth normalized by the attenuation window
    pub(crate) windowed_bandwidth_hz: OnceCell<f64>,
    /// Total span of measurement
    pub(crate) frequency_span_hz: OnceCell<f64>,
    /// Time span of single segment
    pub(crate) measurement_time_pip: OnceCell<PipDuration>,
    /// number of segments in the test
    pub(crate) segment_count: OnceCell<CountSegments>,
    /// delta between start of segments
    pub(crate) segment_pitch_pip: OnceCell<PipDuration>,
    /// maximum frequency of interest
    pub(crate) max_meas_hz: OnceCell<f64>,
    /// maximum sampling frequency
    pub(crate) sample_max_hz: OnceCell<f64>,
    /// minimum sampling frequency
    pub(crate) sample_min_hz: OnceCell<f64>,
    /// analysis frequency range
    pub(crate) start_hz: OnceCell<f64>,
    pub(crate) stop_hz: OnceCell<f64>,

    /// measurement time step
    pub(crate) time_step_s: OnceCell<f64>,

    pub(crate) start_time_pip: OnceCell<StartTime>,

    /// the heterodyne frequencies,
    /// called the Zoom frequency sometimes
    /// there does seem to be only one zoom frequency for the whole test
    /// rather than one per channel.
    pub(crate) heterodyne_freq_hz: OnceCell<f64>,
    /// sample rate to decimate to for heterodyned data
    /// this is applied directly to complex channels (already heterodyned)
    /// and to real channels after they are heterodyned.
    pub(crate) heterodyned_sample_rate_hz: OnceCell<f64>,

    /// True if complex channels are assumed to be already heterodyned
    /// and real channels will be heterodyned.
    pub(crate) heterodyned: OnceCell<bool>,

    /// relative time after start that serves as a reference for the
    /// heterodyne function, should the heterodyne function be used.
    pub(crate) heterodyne_start_pip: OnceCell<PipDuration>,

    pub(crate) remove_mean: OnceCell<bool>,

    // keep a copy of the params so we can always trace the params used
    pub(crate) test_params: TestParams,
}

impl TimelineInit {
    fn new(test_params: TestParams) -> Self {
        Self {
            test_params,
            ..Default::default()
        }
    }

    /// return sample rate that all input data is decimated to.
    ///
    /// this function can panic if values in the timeline
    /// aren't initialized in the correct order.  
    /// Invalid constructions will fail in unit tests.
    pub fn sample_rate_hz(&self) -> f64 {
        if *self.heterodyned.get().unwrap() {
            *self.heterodyned_sample_rate_hz.get().unwrap()
        } else {
            *self.sample_max_hz.get().unwrap()
        }
    }

    /// this function can panic if values in the timeline
    /// aren't initialized in the correct order.  
    /// Invalid constructions will fail in unit tests.
    pub fn settling_time_pip(&self) -> PipDuration {
        self.measurement_time_pip.get().unwrap() * self.test_params.settling_time_frac
    }

    /// create an fft param suitable for a single segment of the timeline    
    pub fn fft_param<T: FFTTypeInfo + Default + Clone>(&self) -> Result<FFTParam, DTTError> {
        Ok(FFTParam::create::<T>(
            self.segment_size(),
            self.test_params.fft_window.clone(),
        )?)
    }

    /// Get the number of data points in single measurement segment
    ///
    /// this function can panic if values in the timeline
    /// aren't initialized in the correct order.  
    /// Invalid constructions will fail in unit tests.
    pub fn segment_size(&self) -> usize {
        let rate_hz = self.sample_rate_hz();

        (self.measurement_time_pip.get().unwrap() / PipDuration::freq_hz_to_period(rate_hz))
            as usize
    }
}

/// Calculate timeline using tli.  We just unwrap sets because they should be in order
/// The OnceCells are just used to enforce correct initialization order.
/// Too many timeline bits depend on other timeline bits already being configured.
///
/// this function can panic if values in the timeline
/// aren't initialized in the correct order.  
/// Invalid constructions will fail in unit tests.
pub fn calculate_timeline(rc: Box<RunContext>, test_params: TestParams) -> CalcTimelineResult {
    let tli = TimelineInit::new(test_params.clone());

    tli.measurement_channels
        .set(
            test_params
                .measurement_channels
                .active_iter()
                .map(|p| p.channel.clone())
                .collect(),
        )
        .unwrap();

    tli.excitations
        .set(
            test_params
                .excitations
                .active_iter()
                .map(|p| p.excitation.clone())
                .collect(),
        )
        .unwrap();

    tli.start_hz.set(test_params.start_hz).unwrap();

    tli.stop_hz.set(test_params.stop_hz).unwrap();

    tli.start_time_pip
        .set(test_params.start_time_pip.clone())
        .unwrap();

    const PARAM_CONSTRAINTS: [Constraint<TestParams>; NUM_GENERAL_PARAM_CONSTRAINTS] =
        general_param_constraints();

    if !check_constraint_list(rc.clone(), &PARAM_CONSTRAINTS, &test_params) {
        return Err(DTTError::UnsatisfiedConstraint);
    }

    let tl = match test_params.test_type {
        TestType::FFTTools => super::ffttools::calculate_timeline(rc.clone(), &test_params, tli)?,
        _ => tli.into(),
    }
    .calculate_delays()?;

    tl.analysis_check(&rc)?;

    Ok(tl)
}

#[cfg(test)]
mod tests {

    use crate::user::new_user_output_channel;

    use super::*;

    #[test]
    fn test_calculate_timeline() {
        let rt = tokio::runtime::Runtime::new().unwrap();
        let (u_tx, _u_rx) = new_user_output_channel();
        let rc = Box::new(rt.block_on(RunContext::create(u_tx)));

        let test_params = TestParams::default_fft_params();
        assert!(calculate_timeline(rc, test_params).is_err());
    }
}
