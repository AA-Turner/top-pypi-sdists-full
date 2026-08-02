//! pre-calculate the various factors needed to run an FFT tools test
//! References in general are taken from DTT version 4.1.1, src/diag/ffttools.cc
//! Line# citations are given for each function.

use crate::analysis::graph::scheme::{SchemeEdge, SchemeGraph, SchemeNode, SchemePipelineType};
use crate::analysis::result::EdgeResultsWrapper;
use crate::c_math::round_up_p2;
use crate::constraints::check_constraint_list;
use crate::params::channel_params::ChannelSettings;
use crate::params::constraints::NUM_FFT_PARAM_CONSTRAINTS;
use crate::params::excitation_params::ExcitationSettings;
use crate::timeline::constraints::{NUM_TIMELINE_CONSTRAINTS, fft_tools_timeline_constraints};
use crate::timeline::general::{initial_heterodyne_freq_hz, sample_frequency_hz};
use crate::timeline::init::TimelineInit;
use crate::timeline::{CountSegments, Timeline};
use crate::{
    constraints::Constraint,
    errors::DTTError,
    params::{constraints::fft_param_constraints, test_params::TestParams},
    run_context::RunContext,
    timeline::CalcTimelineResult,
};
use ligo_hires_gps_time::PipDuration;
use petgraph::graph::NodeIndex;
use user_messages::UserMsgProvider;

const FFT_SPAN_FACTOR: f64 = 1.1;

/// this function panics any initialization is done out of order
/// that is a bug in the function and it will never succeed.
/// A single unit test for success is enough
/// to show it won't panic
pub fn calculate_timeline(
    rc: Box<RunContext>,
    params: &TestParams,
    timeline: TimelineInit,
) -> CalcTimelineResult {
    const TP_CONSTRAINTS: [Constraint<TestParams>; NUM_FFT_PARAM_CONSTRAINTS] =
        fft_param_constraints();

    let go_ahead = check_constraint_list(rc.clone(), &TP_CONSTRAINTS, &params);

    if !go_ahead {
        return Err(DTTError::UnsatisfiedConstraint);
    }

    // if this becomes zero here, it may yet become non-zero later
    timeline
        .heterodyne_freq_hz
        .set(heterodyne_freq_hz(rc.clone(), params)?)
        .unwrap();

    timeline
        .heterodyned
        .set(*timeline.heterodyne_freq_hz.get().unwrap() > 0.0)
        .unwrap();

    timeline
        .frequency_span_hz
        .set(frequency_span_hz(params, &timeline))
        .unwrap();

    // Set bandwidth to a power of 2
    timeline
        .bandwidth_hz
        .set(snap_bandwidth_hz(params))
        .unwrap();

    timeline
        .measurement_time_pip
        .set(measurement_time_pip(&timeline))
        .unwrap();

    // set the maximum measurement frequency
    timeline
        .max_meas_hz
        .set(maximum_frequency_hz(params, &timeline))
        .unwrap();

    // set sample frequency
    let (sample_min_hz, sample_max_hz) = sample_frequency_hz(&timeline);
    timeline.sample_min_hz.set(sample_min_hz).unwrap();
    timeline.sample_max_hz.set(sample_max_hz).unwrap();

    timeline
        .heterodyned_sample_rate_hz
        .set(heterodyned_sample_rate_hz(&timeline))
        .unwrap();

    timeline
        .heterodyne_start_pip
        .set(heterodyne_start_pip(rc.ump_clone(), &timeline))
        .unwrap();

    // Get the segment pitch
    timeline
        .segment_pitch_pip
        .set(segment_pitch_pip(&timeline))
        .unwrap();

    // check the constraints before proceeding.
    // is this necessary?

    // set time step
    timeline
        .time_step_s
        .set(calc_time_step(
            timeline.sample_min_hz.get().unwrap() / 2.0,
            &timeline.measurement_channels.get().unwrap(),
            &timeline.excitations.get().unwrap(),
        )?)
        .unwrap();

    // set remove mean
    timeline
        .remove_mean
        .set(remove_mean(params, &timeline))
        .unwrap();

    timeline
        .windowed_bandwidth_hz
        .set(windowed_bandwidth_hz(&timeline)?)
        .unwrap();

    timeline
        .segment_count
        .set(CountSegments::N(params.average_size))
        .unwrap();

    // timeline must be totally initialized by this point
    let finished_timeline = timeline.into();

    const TL_CONSTRAINTS: [Constraint<Timeline>; NUM_TIMELINE_CONSTRAINTS] =
        fft_tools_timeline_constraints();
    if !check_constraint_list(rc.clone(), &TL_CONSTRAINTS, &finished_timeline) {
        return Err(DTTError::UnsatisfiedConstraint);
    }

    // check that constraints still hold
    if check_constraint_list(rc.clone(), &TL_CONSTRAINTS, &finished_timeline) {
        Ok(finished_timeline)
    } else {
        Err(DTTError::UnsatisfiedConstraint)
    }
}
/// # Functions for constructing parts of the timeline
///
/// ### References
/// 1.  cds-crtools ffttools.cc calcTimes() 497
///     https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L497
fn heterodyne_freq_hz(rc: Box<RunContext>, params: &TestParams) -> Result<f64, DTTError> {
    let hf_hz = initial_heterodyne_freq_hz(rc.clone(), params)?;
    if hf_hz == 0.0 {
        if params.start_hz < 1e-12 || (params.start_hz < params.stop_hz / 2.0) {
            Ok(0.0)
        } else {
            // make sure to round to an exact band value
            Ok(
                ((params.stop_hz - params.start_hz) / (2.0 * params.band_width_hz)).round()
                    * params.band_width_hz
                    + params.start_hz,
            )
        }
    } else {
        Ok(hf_hz)
    }
}

/// ### References
/// 1. DTT ffttools.cc caclTimes()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L337
fn frequency_span_hz(params: &TestParams, timeline: &TimelineInit) -> f64 {
    let het_freq_hz = timeline.heterodyne_freq_hz.get().unwrap();
    let fspan_hz = if *timeline.heterodyned.get().unwrap() {
        FFT_SPAN_FACTOR * 2.0 * (params.stop_hz - het_freq_hz).max(het_freq_hz - params.start_hz)
    } else {
        FFT_SPAN_FACTOR * (params.stop_hz - params.start_hz)
    };

    round_up_p2(fspan_hz - 1e-12)
}

/// Fix bandwidth to be a power of two
///
/// ### References:
/// 1. DTT ffttools.cc calcTimes()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L348
fn snap_bandwidth_hz(params: &TestParams) -> f64 {
    round_up_p2(params.band_width_hz / 2f64.sqrt())
}

fn measurement_time_pip(timeline: &TimelineInit) -> PipDuration {
    PipDuration::freq_hz_to_period(*timeline.bandwidth_hz.get().unwrap())
}

/// Sets the delta time between the start of two segments, which can be
/// less than the length of one segment
///
/// ### References
/// 1. DTT ffttools.cc calcTimes()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L511
fn segment_pitch_pip(timeline: &TimelineInit) -> PipDuration {
    let counts_per_step = PipDuration::freq_hz_to_period(timeline.sample_rate_hz());
    let pitch_pip =
        timeline.measurement_time_pip.get().unwrap() * (1.0 - timeline.test_params.overlap);
    pitch_pip.snap_to_step(&counts_per_step)
}

/// ### References
/// Modified so that when heterodyne is not zero, maximum span/stop_hz still used
/// This is because the value is still needed by real-valued channels
/// that aren't heterodyned
///
/// the cds-crtools code use fZoom (heterodyne_freq) as a flag, so at the point of reference
/// fZoom is only not zero if there are complex channels.  This leaves real channels high and dry.
///
/// complex channels will now just use the frequency_span_hz / 2.0 as a decimation target
///
/// calculated with heterodyned_sample_hz() on Timeline
///
/// 1. DTT ffttools.cc calcTimes()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L360
fn maximum_frequency_hz(params: &TestParams, timeline: &TimelineInit) -> f64 {
    timeline
        .frequency_span_hz
        .get()
        .unwrap()
        .max(params.stop_hz)
}

/// based on sample_frequency_hz
/// Basically get the next power of two above the frequency span.
/// Frequency span is the total span of the heterodyned output
/// so maximum freq is frequency_span_hz / 2.0, so we guarantee target is at least that much.
fn heterodyned_sample_rate_hz(timeline: &TimelineInit) -> f64 {
    round_up_p2(timeline.frequency_span_hz.get().unwrap() - 1e-8)
}

/// ### References
/// 1. DTT ffttools.cc calcTimes()
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L422
fn calc_time_step(
    f_max: f64,
    meas_chans: &[ChannelSettings],
    exc_chans: &[ExcitationSettings],
) -> Result<f64, DTTError> {
    let mut time_step_s = exc_chans
        .iter()
        .filter(|e| e.read_back_channel.is_some())
        .map(|e| {
            e.read_back_channel
                .clone()
                .expect("should be checked previously is not None")
        })
        .collect::<Vec<ChannelSettings>>()
        .iter()
        .chain(meas_chans.into_iter())
        .map(|c| 1.0 / c.rate_hz())
        .reduce(|a, b| f64::max(a, b))
        .ok_or_else(|| DTTError::UnsatisfiedConstraint)?;
    while (1.0 / time_step_s) > (2.0 * f_max + 1e-12) {
        time_step_s *= 2.0;
    }
    Ok(time_step_s)
}

/// Variable at reference is calculated then added to
///
/// ### References
/// 1. calcTimes in ffttools.cc 431
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L431
fn heterodyne_start_pip(_rc: Box<dyn UserMsgProvider>, timeline: &TimelineInit) -> PipDuration {
    timeline
        .test_params
        .ramp_up_pip
        .max(timeline.settling_time_pip() as PipDuration)
}

fn remove_mean(params: &TestParams, timeline: &TimelineInit) -> bool {
    params.remove_mean && !timeline.heterodyned.get().unwrap()
}

/// Bandwidth normalized by the average window height
///
/// ### References
/// 1. calcTimes in FFTTools.cc 583
///    https://git.ligo.org/cds/software/dtt/-/blob/4.1.1/src/dtt/diag/ffttools.cc#L583
fn windowed_bandwidth_hz(timeline: &TimelineInit) -> Result<f64, DTTError> {
    let fftparam = timeline.fft_param::<f64>()?;
    let window = fftparam.get_window_coeffs();
    let norm: f64 = window.iter().sum();

    Ok(timeline.bandwidth_hz.get().unwrap() / norm)
}

// flesh out the per-channel and cross-channel graphs for an FFT Tools test
pub fn get_scheme_graphs<'a>(
    _rc: &Box<RunContext>,
    _timeline: &'a Timeline,
    mut per_chan_graph: SchemeGraph<'a>,
    cross_chan_graph: SchemeGraph<'a>,
    cond_idx: NodeIndex,
) -> (SchemeGraph<'a>, SchemeGraph<'a>) {
    // take the fft
    let fft_idx = per_chan_graph.add_node(SchemeNode::new("fft", SchemePipelineType::FFT));
    per_chan_graph.add_edge(cond_idx, fft_idx, SchemeEdge::new(1));

    // get the per-segment asd from the fft
    let asd_idx = per_chan_graph.add_node(SchemeNode::new("asd", SchemePipelineType::ASD));
    per_chan_graph.add_edge(fft_idx, asd_idx, SchemeEdge::new(1));

    // get the average over segments of the asd
    let asd_avg_idx =
        per_chan_graph.add_node(SchemeNode::new("asd_avg", SchemePipelineType::Average));
    per_chan_graph.add_edge(asd_idx, asd_avg_idx, SchemeEdge::new(1));

    // collect results
    let results_idx =
        per_chan_graph.add_node(SchemeNode::new("results", SchemePipelineType::Results));
    per_chan_graph.add_edge(
        asd_avg_idx,
        results_idx,
        SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::ASD),
    );

    // TODO: Custom per_channel

    // TODO: all the cross-channel analysis

    // TODO: Custom cross-channel

    (per_chan_graph, cross_chan_graph)
}
