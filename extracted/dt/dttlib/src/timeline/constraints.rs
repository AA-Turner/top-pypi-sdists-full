use super::Timeline;
use crate::constraints::Constraint;
use user_messages::Severity;

pub const NUM_TIMELINE_CONSTRAINTS: usize = 7;

/// Constraints on finished timelines
/// # FFT Param timelines
pub const fn fft_tools_timeline_constraints() -> [Constraint<Timeline>; NUM_TIMELINE_CONSTRAINTS] {
    [
        Constraint::new(
            "ConstrainBandwidthToSpan",
            "Bandwidth must be smaller than 1/16th of the frequency span.",
            Severity::Error,
            |tl: &Timeline| tl.bandwidth_hz * 16.0 < tl.frequency_span_hz - 1e-12,
        ),
        Constraint::new(
            "ConstrainBandwidthToGreaterThanZero",
            "Bandwidth must be greater than zero",
            Severity::Error,
            |tl: &Timeline| tl.bandwidth_hz > 0.0,
        ),
        Constraint::new(
            "ConstrainNonHeterodyneSamplingFreqs",
            "Sampling rate of at least one channel is too slow.",
            Severity::Error,
            |tl: &Timeline| {
                (tl.heterodyne_freq_hz != 0.0) || (tl.sample_min_hz >= tl.sample_max_hz - 1e-12)
            },
        ),
        Constraint::new(
            "StartStopHeterodyneCompat",
            "Start/stop frequency incompatible with heterodyne frequency.",
            Severity::Error,
            |tl: &Timeline| {
                (tl.heterodyne_freq_hz == 0.0)
                    || ((tl.start_hz < tl.heterodyne_freq_hz)
                        && (tl.start_hz > tl.heterodyne_freq_hz - (tl.frequency_span_hz / 2.0))
                        && (tl.stop_hz > tl.heterodyne_freq_hz)
                        && (tl.stop_hz <= tl.heterodyne_freq_hz + (tl.frequency_span_hz * 2.0)))
            },
        ),
        Constraint::new(
            "ConstrainHeterodyneSamplingFreqs",
            "Sampling rate of at least one channel is too slow.",
            Severity::Error,
            |tl: &Timeline| {
                (tl.heterodyne_freq_hz == 0.0) || (tl.sample_min_hz >= tl.frequency_span_hz - 1e-12)
            },
        ),
        Constraint::new(
            "ConsistentHeterodyneValues1",
            "fZoom (Heterodyne) frequency not zero, but output is not heterodyned.",
            Severity::Error,
            |tl: &Timeline| tl.heterodyned || (tl.heterodyne_freq_hz == 0.0),
        ),
        Constraint::new(
            "ConsistentHeterodyneValues2",
            "fZoom (Heterodyne) frequency iz zero, but input is heterodyned.",
            Severity::Error,
            |tl: &Timeline| (!tl.heterodyned) || (tl.heterodyne_freq_hz != 0.0),
        ),
    ]
}
