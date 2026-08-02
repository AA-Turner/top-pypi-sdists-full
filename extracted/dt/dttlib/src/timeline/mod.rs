//! Calculate and distribute a timeline struct
//! that defines all the different time points in  a test

mod constraints;
mod ffttools;
pub mod general;
pub mod init;

use crate::analysis::graph::analysis::AnalysisGraph;
#[cfg(feature = "python-pipe")]
use crate::analysis::graph::scheme::add_custom_pipelines;
use crate::analysis::graph::scheme::{SchemeEdge, SchemeGraph, SchemeNode, SchemePipelineType};
use crate::analysis::result::ResultsReceiver;
use crate::data_source::DataSourceRef;
use crate::data_source::no_data::NoData;
use crate::errors::DTTError;
use crate::gds_sigp::fft::{FFTParam, FFTTypeInfo};
use crate::params::channel_params::ChannelSettings;
use crate::params::excitation_params::ExcitationSettings;
use crate::params::test_params::{StartTime, TestParams, TestType};
use crate::run_context::RunContext;
use crate::timeline::init::TimelineInit;
use ligo_hires_gps_time::{PipDuration, PipInstant};

#[cfg(feature = "python")]
use pyo3::pyclass;

#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;

#[derive(Clone, Debug)]
pub enum CountSegments {
    Indefinite,
    N(u64),
}

#[derive(Clone, Debug)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(frozen))]
pub struct Timeline {
    pub measurement_channels: Vec<ChannelSettings>,
    pub excitations: Vec<ExcitationSettings>,

    /// # Time slice definitions
    /// setup bandwidth
    pub bandwidth_hz: f64,
    /// bandwidth normalized by the attenuation window
    pub windowed_bandwidth_hz: f64,
    /// Total span of measurement
    pub frequency_span_hz: f64,
    /// Time span of single segment
    pub measurement_time_pip: PipDuration,
    /// number of segments in the test
    pub segment_count: CountSegments,
    /// delta between start of segments
    pub segment_pitch_pip: PipDuration,
    /// maximum frequency of interest
    pub max_meas_hz: f64,
    /// maximum sampling frequency
    pub sample_max_hz: f64,
    /// minimum sampling frequency
    pub sample_min_hz: f64,
    /// analysis frequency range
    pub start_hz: f64,
    pub stop_hz: f64,

    /// measurement time step
    pub time_step_s: f64,

    pub start_time_pip: StartTime,

    /// the heterodyne frequencies,
    /// called the Zoom frequency sometimes
    /// there does seem to be only one zoom frequency for the whole test
    /// rather than one per channel.
    pub heterodyne_freq_hz: f64,
    /// sample rate to decimate to for heterodyned data
    /// this is applied directly to complex channels (already heterodyned)
    /// and to real channels after they are heterodyned.
    pub heterodyned_sample_rate_hz: f64,

    /// True if complex channels are assumed to be already heterodyned
    /// and real channels will be heterodyned.
    pub heterodyned: bool,

    /// relative time after start that serves as a reference for the
    /// heterodyne function, should the heterodyne function be used.
    pub heterodyne_start_pip: PipDuration,

    /// When true, remove the mean value from a signal prior to analysis
    pub remove_mean: bool,

    /// keep a copy of the params so we can always trace the params used
    pub test_params: TestParams,
}

impl From<TimelineInit> for Timeline {
    /// this function can panic if the TimelineInit is
    /// not properly initialized.  This is fully checked in
    /// unit tests
    fn from(mut value: TimelineInit) -> Self {
        Self {
            measurement_channels: value.measurement_channels.take().unwrap(),
            excitations: value.excitations.take().unwrap(),
            bandwidth_hz: value.bandwidth_hz.take().unwrap(),
            windowed_bandwidth_hz: value.windowed_bandwidth_hz.take().unwrap(),
            frequency_span_hz: value.frequency_span_hz.take().unwrap(),
            measurement_time_pip: value.measurement_time_pip.take().unwrap(),
            segment_count: value.segment_count.take().unwrap(),
            segment_pitch_pip: value.segment_pitch_pip.take().unwrap(),
            max_meas_hz: value.max_meas_hz.take().unwrap(),
            sample_max_hz: value.sample_max_hz.take().unwrap(),
            sample_min_hz: value.sample_min_hz.take().unwrap(),
            start_hz: value.start_hz.take().unwrap(),
            stop_hz: value.stop_hz.take().unwrap(),
            time_step_s: value.time_step_s.take().unwrap(),
            start_time_pip: value.start_time_pip.take().unwrap(),
            heterodyne_freq_hz: value.heterodyne_freq_hz.take().unwrap(),
            heterodyned_sample_rate_hz: value.heterodyned_sample_rate_hz.take().unwrap(),
            heterodyned: value.heterodyned.take().unwrap(),
            heterodyne_start_pip: value.heterodyne_start_pip.take().unwrap(),
            remove_mean: value.remove_mean.take().unwrap(),
            test_params: value.test_params,
        }
    }
}

impl Timeline {
    /// Calculate various delay values used to
    /// compensate for the Decimation filters
    /// Both decimation and the delay compensation are part of
    /// the pre-processing stage
    pub fn calculate_delays(mut self) -> Result<Self, DTTError> {
        let is_heterodyne = self.heterodyned;
        let sample_max_hz = self.sample_max_hz;
        for channel in self.measurement_channels.iter_mut() {
            channel.calc_decimation_factors(
                self.test_params.remove_decimation_delay,
                is_heterodyne,
                sample_max_hz,
                self.heterodyned_sample_rate_hz,
            )?;
        }
        Ok(self)
    }

    pub fn do_nothing() {}

    // time from start_time_pip to the end of the test
    // If None, the test is indefinite and the
    // total time cannot be calculated.
    pub fn total_measurement_time_pip(&self) -> Option<PipDuration> {
        let pitch_pip = self.segment_pitch_pip;
        let seg_length_pip = self.measurement_time_pip;
        let count = match self.segment_count {
            CountSegments::Indefinite => return None,
            CountSegments::N(c) => c,
        };
        Some((count - 1) as i128 * pitch_pip + seg_length_pip)
    }

    /// Return the absolute end time of the timeline if the test is bounded otherwise None.
    /// Returns Error if start time is not bound yet.
    pub fn end_time_pip(&self) -> Result<Option<PipInstant>, DTTError> {
        match self.total_measurement_time_pip() {
            Some(e) => match self.start_time_pip {
                StartTime::Unbound() => Err(DTTError::UnboundStartTime),
                StartTime::Bound { start_pip } => Ok(Some(start_pip + e)),
            },
            None => Ok(None),
        }
    }

    /// get the per-channel and cross-channel scheme graphs
    fn get_scheme_graphs(
        &'_ self,
        rc: &'_ Box<RunContext>,
    ) -> Result<(SchemeGraph<'_>, SchemeGraph<'_>), DTTError> {
        let mut per_channel_scheme_graph = SchemeGraph::new();
        let cross_channel_scheme_graph = SchemeGraph::new();

        let ds_index = per_channel_scheme_graph.add_node(SchemeNode::new(
            "data_source",
            SchemePipelineType::DataSource,
        ));
        let cond_index = per_channel_scheme_graph.add_node(SchemeNode::new(
            "conditioning",
            SchemePipelineType::Conditioning,
        ));
        per_channel_scheme_graph.add_edge(ds_index, cond_index, SchemeEdge::new(1));

        #[allow(unused_mut)]
        let (mut per_chan, cross_chan) = match self.test_params.test_type {
            TestType::FFTTools => ffttools::get_scheme_graphs(
                rc,
                self,
                per_channel_scheme_graph,
                cross_channel_scheme_graph,
                cond_index,
            ),
            _ => todo!(),
        };

        #[cfg(feature = "python-pipe")]
        add_custom_pipelines(
            rc,
            &mut per_chan,
            self.test_params.custom_pipelines.as_slice(),
        )?;

        Ok((per_chan, cross_chan))
    }

    fn get_analysis_graph(&'_ self, rc: &Box<RunContext>) -> Result<AnalysisGraph<'_>, DTTError> {
        let (per_chan_scheme, cross_chan_scheme) = self.get_scheme_graphs(rc)?;

        if let Err(e) =
            AnalysisGraph::test_schemes(rc.clone(), &per_chan_scheme, &cross_chan_scheme)
        {
            rc.user_messages
                .set_error("AnalysisSchemeError", e.to_string());
            return Err(e);
        }

        rc.user_messages.clear_message("AnalysisSchemeError");

        match AnalysisGraph::create_analysis_graph(
            self.all_channels().as_slice(),
            &per_chan_scheme,
            &cross_chan_scheme,
        ) {
            Err(e) => {
                rc.user_messages
                    .set_error("AnalysisGraphError", e.to_string());
                Err(e)
            }
            Ok(g) => {
                rc.user_messages.clear_message("AnalysisGraphError");
                Ok(g)
            }
        }
    }

    /// Setup analysis pipelines that will generate various results
    pub async fn setup_analysis(
        &self,
        rc: &Box<RunContext>,
        source: DataSourceRef,
    ) -> Result<ResultsReceiver, DTTError> {
        let mut ag = self.get_analysis_graph(rc)?;
        ag.graph_to_dtt_pipeline(rc, self, &source).await
    }

    /// Analysis check during timeline creation
    /// Run a pipeline creation on a dummy data source to prove the pipelines can be created.
    /// Throws away the pipeline without using it after creation.
    pub fn analysis_check(&self, rc: &Box<RunContext>) -> Result<(), DTTError> {
        let dummy: DataSourceRef = NoData::new().into();
        let bound_tl = self.bind_start_time(&dummy);
        if let Err(e) =
            tokio::runtime::Handle::current().block_on(bound_tl.setup_analysis(rc, dummy))
        {
            let msg = format!("Failed to create analysis pipelines: {}", e.to_string());
            rc.user_messages.set_error("AnalysisCheck", msg.clone());
            return Err(e);
        }
        Ok(())
    }

    /// get all channels including read back channels for excitaitons
    pub fn all_channels(&self) -> Vec<ChannelSettings> {
        let mut chans = self.measurement_channels.clone();

        chans.extend(self.excitations.iter().map(|e| e.get_read_back_channel()));
        chans
    }

    /// return sample rate that all input data is decimated to.
    pub fn sample_rate_hz(&self) -> f64 {
        if self.heterodyned {
            self.heterodyned_sample_rate_hz
        } else {
            self.sample_max_hz
        }
    }

    /// Get the number of data points in single measurement segment
    pub fn segment_size(&self) -> usize {
        let rate_hz = self.sample_rate_hz();

        (self.measurement_time_pip / PipDuration::freq_hz_to_period(rate_hz)) as usize
    }

    /// Bind an unbound start time to the data source time
    /// Since timelines should be immutable, this creates a new timeline
    /// If start time is already bound, just clones self.
    pub fn bind_start_time(&self, data_source: &DataSourceRef) -> Self {
        let start_time_pip = match self.start_time_pip {
            StartTime::Unbound() => data_source.now() + START_ADVANCE,
            StartTime::Bound { start_pip } => start_pip,
        };
        let aligned_start_time_pip = self.snap_to_sample_step_pip(start_time_pip);
        Self {
            start_time_pip: StartTime::Bound {
                start_pip: aligned_start_time_pip,
            },
            ..self.clone()
        }
    }

    /// round a time in pips to the nearest multiple of the sample step size
    pub fn snap_to_sample_step_pip(&self, time: PipInstant) -> PipInstant {
        let step_pip = PipDuration::freq_hz_to_period(self.sample_rate_hz());
        time.snap_to_step(&step_pip)
    }

    /// create an fft param suitable for a single segment of the timeline
    pub fn fft_param<T: FFTTypeInfo + Default + Clone>(&self) -> Result<FFTParam, DTTError> {
        Ok(FFTParam::create::<T>(
            self.segment_size(),
            self.test_params.fft_window.clone(),
        )?)
    }

    /// Get the decimation delay for the whole timeline, which is the
    /// maximum delay for any one channel
    fn decim_delay_pip(&self) -> PipDuration {
        self.all_channels()
            .iter()
            .map(|x| PipDuration::from_seconds(x.decimation_delays.decimation_delay_s))
            .max()
            .unwrap_or(PipDuration::default())
            .snap_to_step(&PipDuration::freq_hz_to_period(self.sample_max_hz))
    }

    /// A multiplier of the decimation delay  that gives the maximum
    /// amount of lead-in time for a test
    /// This essentially gives the decimation filters time to settle before doing analysis
    const PREPROC_STARTUP: u64 = 10;

    /// A multiplier of the decimation delay that gives
    /// the maximum span of post-test data we'll continue to process.
    /// This accounts for possible shifting of data as part of delay correction.
    /// Also may potentially reduce correlation when running sequential tests
    const PREPROC_CONTINUE: u64 = 2;

    /// Return start time shifted earlier by a factor of the timeline decimation
    /// It's an error if the start time is still not bound.
    /// Data should actually flow from this time, since we need to account for the shift
    /// caused by decimation filters.
    pub fn extended_start_time_pip(&self) -> Result<PipInstant, DTTError> {
        match self.start_time_pip {
            StartTime::Unbound() => Err(DTTError::UnboundStartTime),
            StartTime::Bound { start_pip } => {
                let decim_delay_pip = self.decim_delay_pip();
                Ok(start_pip - Timeline::PREPROC_STARTUP as i128 * decim_delay_pip)
            }
        }
    }

    /// Return the end time shifted later by some decimation factor
    /// Data should actually flow from this time since later data
    /// is shifted back to correct for phase shifts from decimation filters.
    /// Returns None if there is no end point, but there is an end point and the start point is
    /// yet unbounded, that is an error.
    pub fn extended_end_time_pip(&self) -> Result<Option<PipInstant>, DTTError> {
        match self.end_time_pip()? {
            Some(t) => Ok(Some(
                t + Timeline::PREPROC_CONTINUE as i128 * self.decim_delay_pip(),
            )),
            None => Ok(None),
        }
    }
}

/// how far ahead of "now" should we set an unbound start time?
/// It should be not long enough to be annoying but long enough
/// for all the free work and communication.
const START_ADVANCE: PipDuration = PipDuration::from_sec(5);

pub type CalcTimelineResult = Result<Timeline, DTTError>;

// type CalcTimelineReceiver = oneshot::Receiver<CalcTimelineResult>;
