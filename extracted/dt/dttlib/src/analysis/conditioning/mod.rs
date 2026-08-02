//! These pipelines condition the data before analysis in most or all tests

use crate::analysis::conditioning::convert::ConvertTo;
use crate::analysis::conditioning::heterodyne::Heterodyne;
use crate::analysis::conditioning::partition::PartitionPipeline;
use crate::analysis::conditioning::time_delay::TimeDelay;
use crate::analysis::conditioning::time_shift::start_timeshift;
use crate::analysis::conditioning::{
    convert::start_pipe_converter, decimate::Decimate,
    subtract_start_average::SubtractStartAverage, trim::create_trim,
};
use crate::analysis::types::Scalar;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::gds_sigp::decimate::IsComplex;
use crate::params::channel_params::ChannelSettings;
use crate::params::test_params::StartTime;
use crate::timeline::Timeline;
use ligo_hires_gps_time::PipDuration;
use pipelines::complex::c128;
use pipelines::{PipeDataPrimitive, PipelineSubscriber};
use std::fmt::Debug;
use user_messages::UserMsgProvider;

pub mod convert;
mod decimate;
mod heterodyne;
mod partition;
mod subtract_start_average;
mod time_delay;
pub(crate) mod time_shift;
mod trim;
// Unpartitioned

// basic DTT pre-process
// https://git.ligo.org/cds/software/dtt/src/dtt/storage
// channelinput.cc line 157, 586 Process()

// 1. convert to double or complex double (f64 or c128) - Done, "Convert" pipeline
// 1. cut off data that ends less than 10x decimation delay before the test, or start more than 2x after. - Done, "Trim" pipeline
// 1. if zoom and not complex, subtract out average of first segment. Done subtract_start_average
// 1. remove delay from first decimation stage.  Could be part of decimation stage?  Done timedelay
// Decimate 1 if real  Done decimate
// Heterodyne if real and heterodyne on
// decimate 2.  Real and imaginary decimated separately.  I don't think this matters, though.  Done decimate
// time shift from decimate - move back start time by a certain amount
// partition the stream  done partition

// decimation delay is stored in channel params

/// Create a composite pipeline that decimates and partitions a single channel
/// down the sample rate
/// If input is complex then the output is complex 128 (double complex, c128)
/// If the input is real and the input is not heterodyne (not Zoom), then the output is f64.
/// If the input is real and heterodyned, then the output is complex 128.
async fn setup_condition_pre_heterodyne_pipeline<I, T>(
    rc: Box<dyn UserMsgProvider>,
    channel: &ChannelSettings,
    timeline: &Timeline,
    input: &PipelineSubscriber<TimeDomainArray<I>>,
) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError>
where
    I: PipeDataPrimitive + Copy + ConvertTo<T> + Debug,
    T: PipeDataPrimitive + Scalar + IsComplex,
{
    // setup the conversion
    let convert =
        start_pipe_converter(rc.ump_clone(), channel.name().clone() + ":converter", input).await?;

    let start_gps_pip = timeline.extended_start_time_pip()?;
    let end_gps_pip = timeline.extended_end_time_pip()?;

    // trim down
    let trim = create_trim(
        rc.ump_clone(),
        channel.name().clone() + ":trim",
        start_gps_pip,
        end_gps_pip,
        &convert,
    )
    .await?;

    let heterodyne_freq = channel.channel.heterodyne_freq_hz.unwrap_or_else(|| 0.0);

    // subtract
    let sub = if !channel.data_type().is_complex() && heterodyne_freq > 0.0 {
        SubtractStartAverage::create(
            rc.ump_clone(),
            channel.name().clone() + ":subtract_average",
            &trim,
        )
        .await?
    } else {
        trim
    };

    // remove delay
    // and decimate
    let delay = if channel.decimation_delays.delay_taps > 0 {
        TimeDelay::create(
            rc.ump_clone(),
            channel.name().clone() + ":delay",
            channel.decimation_delays.delay_taps,
            &sub,
        )
        .await?
    } else {
        sub
    };

    Ok(
        // first decimation
        if channel.raw_decimation_params.num_decs > 0 {
            Decimate::create(
                rc.ump_clone(),
                channel.name().clone() + ":decimate",
                &channel.raw_decimation_params,
                &delay,
            )
            .await?
        } else {
            delay
        },
    )
}

// heterodyne

async fn setup_conditioning_post_heterodyne_pipeline<T>(
    rc: Box<dyn UserMsgProvider>,
    channel: &ChannelSettings,
    timeline: &Timeline,
    input: PipelineSubscriber<TimeDomainArray<T>>,
) -> Result<PipelineSubscriber<TimeDomainArray<T>>, DTTError>
where
    T: PipeDataPrimitive + Scalar + IsComplex,
{
    let start_time_pip =
        match timeline.start_time_pip {
            StartTime::Bound { start_pip } => start_pip,
            StartTime::Unbound() => return Err(DTTError::AnalysisPipelineError(
                "Cannot create conditioning post heterodyne pipeline with an unbound startpoint"
                    .to_string(),
            )),
        };

    // decimate 2
    let decim2 = if channel.heterodyned_decimation_params.num_decs > 0 {
        Decimate::create(
            rc.ump_clone(),
            channel.name().clone() + ":decimate",
            &channel.heterodyned_decimation_params,
            &input,
        )
        .await?
    } else {
        input
    };

    // time shift output
    let time_shift = if channel.decimation_delays.delayshift_pip != 0.into() {
        start_timeshift(
            rc.ump_clone(),
            channel.name().clone() + ":timeshift",
            channel.decimation_delays.delayshift_pip,
            &decim2,
        )
        .await?
    } else {
        decim2
    };

    // partition
    PartitionPipeline::create(
        rc.ump_clone(),
        channel.name().clone() + ":partition",
        start_time_pip,
        timeline.measurement_time_pip,
        timeline.segment_pitch_pip,
        timeline.segment_count.clone(),
        &time_shift,
    )
    .await
}

/// create a standard pipeline for complex channels
/// these convert to c128 output and aren't heterodyned.
/// We assume they are already heterodyned at the source.
pub async fn setup_conditioning_pipeline_complex<I>(
    rc: Box<dyn UserMsgProvider>,
    channel: &ChannelSettings,
    timeline: &Timeline,
    input: &PipelineSubscriber<TimeDomainArray<I>>,
) -> Result<StandardPipeOutput, DTTError>
where
    I: PipeDataPrimitive + Copy + ConvertTo<c128>,
{
    let mid_pipe =
        setup_condition_pre_heterodyne_pipeline(rc.ump_clone(), channel, timeline, input).await?;
    Ok(StandardPipeOutput::Complex128(
        setup_conditioning_post_heterodyne_pipeline(rc, channel, timeline, mid_pipe).await?,
    ))
}

pub async fn setup_conditioning_pipeline_heterodyned_real<I>(
    rc: Box<dyn UserMsgProvider>,
    channel: &ChannelSettings,
    timeline: &Timeline,
    input: &PipelineSubscriber<TimeDomainArray<I>>,
) -> Result<StandardPipeOutput, DTTError>
where
    I: PipeDataPrimitive + Copy + ConvertTo<f64>,
{
    let start_time_pip =
        match timeline.start_time_pip {
            StartTime::Bound { start_pip } => start_pip,
            StartTime::Unbound() => return Err(DTTError::AnalysisPipelineError(
                "Cannot create conditioning post heterodyne pipeline with an unbound startpoint"
                    .to_string(),
            )),
        };

    let mid_pipe =
        setup_condition_pre_heterodyne_pipeline(rc.ump_clone(), channel, timeline, input).await?;

    let heterodyne = Heterodyne::create(
        rc.ump_clone(),
        channel.name().clone() + ":heterodyne",
        timeline.heterodyne_freq_hz,
        start_time_pip + timeline.heterodyne_start_pip,
        channel.decimation_delays.heterodyne_delay_pip,
        PipDuration::freq_hz_to_period(channel.rate_hz()),
        &mid_pipe,
    )
    .await?;

    Ok(StandardPipeOutput::Complex128(
        setup_conditioning_post_heterodyne_pipeline(rc, channel, timeline, heterodyne).await?,
    ))
}

pub async fn setup_conditioning_pipeline_non_heterodyned_real<I>(
    rc: Box<dyn UserMsgProvider>,
    channel: &ChannelSettings,
    timeline: &Timeline,
    input: &PipelineSubscriber<TimeDomainArray<I>>,
) -> Result<StandardPipeOutput, DTTError>
where
    I: PipeDataPrimitive + Copy + ConvertTo<f64>,
{
    let mid_pipe =
        setup_condition_pre_heterodyne_pipeline(rc.ump_clone(), channel, timeline, input).await?;

    Ok(StandardPipeOutput::Float64(
        setup_conditioning_post_heterodyne_pipeline(rc, channel, timeline, mid_pipe).await?,
    ))
}

/// represents the possible output types
/// for a standard pipeline
pub enum StandardPipeOutput {
    Float64(PipelineSubscriber<TimeDomainArray<f64>>),
    Complex128(PipelineSubscriber<TimeDomainArray<c128>>),
    Int64(PipelineSubscriber<TimeDomainArray<i64>>),
    Int32(PipelineSubscriber<TimeDomainArray<i32>>),
    Int16(PipelineSubscriber<TimeDomainArray<i16>>),
    Int8(PipelineSubscriber<TimeDomainArray<i8>>),
    UInt64(PipelineSubscriber<TimeDomainArray<u64>>),
    UInt32(PipelineSubscriber<TimeDomainArray<u32>>),
    UInt16(PipelineSubscriber<TimeDomainArray<u16>>),
    UInt8(PipelineSubscriber<TimeDomainArray<u8>>),
    //String(PipelineSubscriber<TimeDomainArray<String>>),
}
