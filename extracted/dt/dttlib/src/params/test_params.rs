use super::{channel_params::ChannelSettingsParams, excitation_params::ExcitationSettingsParams};
use crate::params::channel_params::ChannelParams;
#[cfg(feature = "python-pipe")]
use crate::params::custom_pipeline::CustomPipeline;
use dtt_macros::builder_lite;
#[cfg(not(feature = "python"))]
use dtt_macros::staticmethod;
use ligo_hires_gps_time::{PipDuration, PipInstant};
#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{
    gen_stub_pyclass, gen_stub_pyclass_complex_enum, gen_stub_pyclass_enum, gen_stub_pymethods,
};
use std::fmt::{Display, Formatter};

/// Parameters unique to the test type
#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(any(feature = "python"), pyclass(frozen, eq, eq_int))]
#[derive(Clone, Debug, Default, PartialEq)]
pub enum TestType {
    #[default]
    FFTTools,
    SweptSine,
    SineResponse,
    TimeSeries,
}

impl Display for TestType {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let s = match self {
            TestType::FFTTools => "FFTTools",
            TestType::SweptSine => "SweptSine",
            TestType::SineResponse => "SineResponse",
            TestType::TimeSeries => "TimeSeries",
        };
        f.write_str(s)
    }
}

const TEST_PARAMS_VERSION: i32 = 1;

/// An unbound StartTime will be bound when the run starts.
#[cfg_attr(feature = "all", gen_stub_pyclass_complex_enum)]
#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(Clone, Debug)]
pub enum StartTime {
    /// An unbound start time means the start of the test is not yet determined.
    Unbound(),
    /// A bound start time holds the start time of the test
    Bound {
        /// The start time of the test.
        start_pip: PipInstant,
    },
}

impl Default for StartTime {
    fn default() -> Self {
        Self::Unbound()
    }
}

impl StartTime {
    /// Panic if the start time is not bound,
    /// otherwise return the start time.
    ///
    /// There are some points in the library where Startpoint must already be bound.
    /// If not, it's a bug.
    pub fn unwrap(self) -> PipInstant {
        match self {
            StartTime::Bound { start_pip } => start_pip,
            StartTime::Unbound() => panic!("Unwrapped an unbound start time"),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl StartTime {
    #[staticmethod]
    pub fn new(start_pip: Option<PipInstant>) -> Self {
        if let Some(start_pip) = start_pip {
            Self::Bound { start_pip }
        } else {
            Self::Unbound()
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(any(feature = "python"), pyclass(frozen, eq, eq_int))]
#[derive(Clone, Debug, Default, PartialEq)]
pub enum AverageType {
    #[default]
    // average n values
    Fixed,

    // average at a fixed rate of 1/lambda
    Exponential,

    // average n values continuously (?)
    Accumulative,

    // average at max(1/n, 1/lambda).
    // like exponential but converges faster at the start
    ConvergingExponential,
}

impl Display for AverageType {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let s = match self {
            AverageType::Fixed => "Fixed",
            AverageType::Exponential => "Exponential",
            AverageType::Accumulative => "Accumulative",
            AverageType::ConvergingExponential => "ConvergingExponential",
        };
        f.write_str(s)
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(feature = "python", pyclass(frozen, eq, eq_int))]
#[derive(Clone, Debug, Default, PartialEq)]
pub enum FFTWindow {
    #[default]
    Uniform,
    Hann,
    FlatTop,
    Welch,
    Bartlett,
    BlackmanHarris,
    Hamming,
}

impl From<FFTWindow> for i32 {
    fn from(value: FFTWindow) -> i32 {
        value as i32
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all))]
#[derive(Clone, Debug, Default)]
#[builder_lite]
pub struct TestParams {
    /// # Version
    /// increment this number if releasing a new version of the struct
    #[no_builder]
    pub version: i32,

    /// # Test Type
    pub test_type: TestType,

    /// # Start Time
    pub start_time_pip: StartTime,

    /// # time constraints
    /// if both time and cycles are set to true,
    /// then the measurement span will be
    /// the least time that satisfies both.
    /// minimum time span of a single segment
    pub measurement_time_pip: PipDuration,
    pub use_measurement_time: bool,

    /// minimum number of cycles
    pub measurement_cycles: i64,
    pub use_measurement_cycles: bool,

    /// # ramps and settling
    /// fraction of measurement time needed to "settle" the system
    pub settling_time_frac: f64,

    /// time to ramp down excitations
    pub ramp_down_pip: PipDuration,
    /// time to ramp up excitations
    pub ramp_up_pip: PipDuration,

    /// # sine_options config
    /// Whether to calculate power spectrum
    /// Needed for sine response and swept sine
    pub calc_power_spectrum: bool,

    /// Maximum harmonic order to calculate
    ///
    pub max_harmonic_order: u32,

    /// # Averaging
    /// Total number of segments to average
    pub average_size: u64,
    pub average_type: AverageType,

    /// ## channel parameters
    #[no_builder]
    pub(crate) measurement_channels: Vec<ChannelSettingsParams>,
    #[no_builder]
    pub(crate) excitations: Vec<ExcitationSettingsParams>,

    /// # FFT Tools params
    pub start_hz: f64,
    pub stop_hz: f64,
    pub band_width_hz: f64,

    /// as a fraction of the length of one segment
    pub overlap: f64,

    /// when true, subtract out the mean
    pub remove_mean: bool,

    /// time of from end of excitation to end of measurement
    /// purpose is to prevent correlation from one segment to the next
    /// due to time delay when using a random input
    pub quiet_time_pip: PipDuration,

    /// when false, don't remove the delay incurred by decimation filters
    /// this should maybe always be true!
    pub remove_decimation_delay: bool,

    /// Attenuation window to use on FFT input
    pub fft_window: FFTWindow,

    /// Custom pipelines
    /// User-provided pipelines written in python.    
    #[no_builder]
    #[cfg(feature = "python-pipe")]
    pub custom_pipelines: Vec<CustomPipeline>,
}

/// # Methods
#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python"), pymethods)]
impl TestParams {
    #[staticmethod]
    pub fn default_fft_params() -> Self {
        TestParams {
            version: TEST_PARAMS_VERSION,
            start_time_pip: StartTime::Unbound(),
            test_type: TestType::FFTTools,
            measurement_channels: Default::default(),
            excitations: Default::default(),
            measurement_time_pip: PipDuration::from_sec(1),
            use_measurement_time: true,
            measurement_cycles: 10,
            use_measurement_cycles: true,
            settling_time_frac: 0.10,
            ramp_down_pip: PipDuration::from_sec(1),
            ramp_up_pip: PipDuration::from_sec(1),
            calc_power_spectrum: true,
            max_harmonic_order: 1,
            average_size: 10,
            average_type: AverageType::Fixed,
            start_hz: 0.0,
            stop_hz: 900.0,
            band_width_hz: 1.0,
            overlap: 0.50,
            remove_mean: true,
            quiet_time_pip: PipDuration::from_sec(0),
            remove_decimation_delay: true,
            fft_window: FFTWindow::Hamming,
            #[cfg(feature = "python-pipe")]
            custom_pipelines: Vec::new(),
        }
    }
}

impl TestParams {
    /// builder function for setting measurement channels
    pub fn with_measurement_channels(mut self, channels: Vec<ChannelParams>) -> Self {
        let chans: Vec<_> = channels.into_iter().map(|c| c.into()).collect();
        self.measurement_channels = chans;
        self
    }
}
