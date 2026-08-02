use super::test_params::TestParams;
use crate::constraints::Constraint;
use crate::params::channel_params::ActiveList;
use user_messages::Severity;

const MIN_PARAM_DELTA: f64 = 1e-6;

pub const NUM_FFT_PARAM_CONSTRAINTS: usize = 5;

pub const fn fft_param_constraints() -> [Constraint<TestParams>; NUM_FFT_PARAM_CONSTRAINTS] {
    [
        Constraint::new(
            "SettlingTimeNegative",
            "Settling time must be zero or greater.",
            Severity::Error,
            |tp: &TestParams| tp.settling_time_frac >= 0.0,
        ),
        Constraint::new(
            "AveragesOutOfRange",
            "Averages must be one or greater",
            Severity::Error,
            |tp: &TestParams| tp.average_size >= 1,
        ),
        Constraint::new(
            "StartFreqNegative",
            "Start frequency cannot be negative",
            Severity::Error,
            |tp: &TestParams| tp.start_hz >= 0.0,
        ),
        Constraint::new(
            "StartFreqGTEStopFreq",
            "Start frequency must be lower than stop frequency.",
            Severity::Error,
            |tp: &TestParams| tp.start_hz + MIN_PARAM_DELTA <= tp.stop_hz,
        ),
        Constraint::new(
            "OverlapOutOfRange",
            "Overlap must be at least 0 and at most 1.",
            Severity::Error,
            |tp: &TestParams| tp.overlap >= 0.0 && tp.overlap <= 1.0,
        ),
    ]
}

pub const NUM_GENERAL_PARAM_CONSTRAINTS: usize = 1;

pub const fn general_param_constraints() -> [Constraint<TestParams>; NUM_GENERAL_PARAM_CONSTRAINTS]
{
    [Constraint::new(
        "MissingMeasurementChannel",
        "Must have at least one measurement channel.",
        Severity::Error,
        |tp: &TestParams| tp.measurement_channels.active_iter().len() > 0,
    )]
}
