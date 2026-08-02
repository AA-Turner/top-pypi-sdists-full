use crate::analysis::conditioning::convert::{ConvertTo, start_pipe_converter};
use crate::analysis::conditioning::{
    StandardPipeOutput, setup_conditioning_pipeline_complex,
    setup_conditioning_pipeline_heterodyned_real, setup_conditioning_pipeline_non_heterodyned_real,
};
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::data_source::buffer::Buffer;
use crate::data_source::data_source_pipeline::DataSourcePipeline;
use crate::errors::DTTError;
use crate::gds_sigp::decimate::DecimationFilter;
use crate::params::channel_params::TrendType;
use crate::params::channel_params::channel::Channel;
use crate::params::channel_params::decimation_parameters::{
    DecimationDelays, DecimationParameters,
};
use crate::params::channel_params::nds_data_type::NDSDataType;
use crate::run_context::RunContext;
use crate::timeline::Timeline;
#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::{getter, new};
use ligo_hires_gps_time::PipDuration;
use pipelines::complex::{c64, c128};
use pipelines::{PipeDataPrimitive, PipelineSubscriber};
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;
use std::fmt::Display;
use std::hash::Hash;
use std::ops::Deref;
use user_messages::UserMsgProvider;

/// full record of a channel including some pre-calculated timeline info used
/// in DTT tests.
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(get_all))]
#[derive(Clone, Debug, Default)]
pub struct ChannelSettings {
    pub channel: Channel,

    // decimation stage done on raw data
    // before it's heterodyned
    pub raw_decimation_params: DecimationParameters,

    // decimation stage done on data after it's heterodyned
    pub heterodyned_decimation_params: DecimationParameters,

    // when true, add in a heterodyne pipeline between decimations
    pub do_heterodyne: bool,

    pub decimation_delays: DecimationDelays,
}

impl Deref for ChannelSettings {
    type Target = Channel;

    fn deref(&self) -> &Self::Target {
        &self.channel
    }
}

impl Display for ChannelSettings {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.channel.fmt(f)
    }
}

impl From<Channel> for ChannelSettings {
    fn from(channel_record: Channel) -> Self {
        Self {
            channel: channel_record,
            ..Default::default()
        }
    }
}

/// needed for the analysis_id macro
impl From<(&ChannelSettings, TrendType)> for ChannelSettings {
    fn from(value: (&ChannelSettings, TrendType)) -> Self {
        let channel = (&value.0.channel, value.1).into();

        Self {
            channel,
            ..value.0.clone()
        }
    }
}

// impl From<ChannelSettings> for String {
//     fn from(value: ChannelSettings) -> Self {
//         value.channel.into()
//     }
// }

impl PartialEq for ChannelSettings {
    fn eq(&self, other: &Self) -> bool {
        self.channel == other.channel
    }
}

impl Eq for ChannelSettings {}

impl Ord for ChannelSettings {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.channel.cmp(&other.channel)
    }
}

impl PartialOrd for ChannelSettings {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.channel.partial_cmp(&other.channel)
    }
}

impl Hash for ChannelSettings {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.channel.hash(state);
    }
}

#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl ChannelSettings {
    #[new]
    pub fn new(channel_name: String, data_type: NDSDataType, period: PipDuration) -> Self {
        let channel = Channel::new(channel_name, data_type, period);
        Self {
            channel,
            ..Self::default()
        }
    }

    #[getter]
    pub fn name(&self) -> &String {
        &self.channel.name
    }

    #[getter]
    pub fn data_type(&self) -> NDSDataType {
        self.channel.data_type.clone()
    }

    #[getter]
    pub fn rate_hz(&self) -> f64 {
        self.channel.rate_hz()
    }
}

impl ChannelSettings {
    /// Calculate decimation factors and delays
    /// heterodyned = true if the channel is heterodyned or is to be heterodyned
    /// sample_max_hz is the desired decimated rate before heterodyning (downconverting) or if not heterodyned
    /// heterodyned_sample_rate_hz is the desired decimated rate *after* heterodyning
    pub(crate) fn calc_decimation_factors(
        &mut self,
        remove_delay: bool,
        is_heterodyne: bool,
        sample_max_hz: f64,
        heterodyned_sample_rate_hz: f64,
    ) -> Result<(), DTTError> {
        let is_complex = self.channel.data_type.is_complex();

        if is_heterodyne {
            if is_complex {
                self.raw_decimation_params = DecimationParameters::new(
                    DecimationFilter::FirLS3,
                    self.channel.rate_hz(),
                    heterodyned_sample_rate_hz,
                )?;

                self.heterodyned_decimation_params = DecimationParameters::default();
            } else {
                // real channels in a heterodyne test have to be heterodyned (downconverted).
                self.do_heterodyne = true;

                // decimation down to the raw sample rate first, but don't time shift.
                self.raw_decimation_params = DecimationParameters::new(
                    DecimationFilter::FirLS3,
                    self.channel.rate_hz(),
                    sample_max_hz,
                )?;

                // decimation down to heterodyne rate after the heterodyne
                self.heterodyned_decimation_params = DecimationParameters::new(
                    DecimationFilter::FirLS3,
                    sample_max_hz,
                    heterodyned_sample_rate_hz,
                )?;
            }
        } else {
            // not heterodyned
            self.raw_decimation_params = DecimationParameters::new(
                DecimationFilter::FirLS1,
                self.channel.rate_hz(),
                sample_max_hz,
            )?;
            self.heterodyned_decimation_params = DecimationParameters::default();
        }

        // calculate the delays from the decimations
        let total_decs =
            self.heterodyned_decimation_params.num_decs + self.raw_decimation_params.num_decs;

        self.decimation_delays = DecimationDelays::new(
            remove_delay,
            self.channel.rate_hz(),
            total_decs,
            self.raw_decimation_params.filter,
        );

        Ok(())
    }

    pub(crate) async fn create_data_source_pipeline(
        &self,
        rc: &Box<RunContext>,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> Result<StandardPipeOutput, DTTError> {
        Ok(match self.channel.data_type {
            NDSDataType::Int8 => {
                StandardPipeOutput::Int8(self.create_data_source::<i8>(rc, buffer_rx).await)
            }
            NDSDataType::Int16 => {
                StandardPipeOutput::Int16(self.create_data_source::<i16>(rc, buffer_rx).await)
            }
            NDSDataType::Int32 => {
                StandardPipeOutput::Int32(self.create_data_source::<i32>(rc, buffer_rx).await)
            }
            NDSDataType::Int64 => {
                StandardPipeOutput::Int64(self.create_data_source::<i64>(rc, buffer_rx).await)
            }
            //NDSDataType::Float32 =>     StandardPipeOutput::Float64(self.create_data_source_convert::<f32, f64>(rc, buffer_rx).await),
            NDSDataType::Float32 => {
                StandardPipeOutput::Float64(self.create_data_source::<f64>(rc, buffer_rx).await)
            }
            NDSDataType::Float64 => {
                StandardPipeOutput::Float64(self.create_data_source::<f64>(rc, buffer_rx).await)
            }
            NDSDataType::UInt8 => {
                StandardPipeOutput::UInt8(self.create_data_source::<u8>(rc, buffer_rx).await)
            }
            NDSDataType::UInt16 => {
                StandardPipeOutput::UInt16(self.create_data_source::<u16>(rc, buffer_rx).await)
            }
            NDSDataType::UInt32 => {
                StandardPipeOutput::UInt32(self.create_data_source::<u32>(rc, buffer_rx).await)
            }
            NDSDataType::UInt64 => {
                StandardPipeOutput::UInt64(self.create_data_source::<u64>(rc, buffer_rx).await)
            }
            NDSDataType::Complex64 => StandardPipeOutput::Complex128(
                self.create_data_source_convert::<c64, c128>(rc, buffer_rx)
                    .await?,
            ),
            NDSDataType::Complex128 => {
                StandardPipeOutput::Complex128(self.create_data_source::<c128>(rc, buffer_rx).await)
            } //NDSDataType::String =>  StandardPipeOutput::String(self.create_data_source::<String>(rc, buffer_rx).await),
        })
    }

    /// Create a super pipeline that is a data source of TimeDomainArray<T>
    /// And converts to an output of TimeDomainArray<U>
    async fn create_data_source_convert<T, U>(
        &self,
        rc: &Box<RunContext>,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> Result<PipelineSubscriber<TimeDomainArray<U>>, DTTError>
    where
        U: PipeDataPrimitive + Copy,
        T: PipeDataPrimitive + Copy + ConvertTo<U>,
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        let ds = self.create_data_source::<T>(rc, buffer_rx).await;

        start_pipe_converter(rc.ump_clone(), self.channel.name.clone() + ":convert", &ds).await
    }

    /// Create a data source of TimeDomainArray<T>
    async fn create_data_source<T>(
        &self,
        rc: &Box<RunContext>,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> PipelineSubscriber<TimeDomainArray<T>>
    where
        T: PipeDataPrimitive,
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        DataSourcePipeline::create::<T>(
            rc.ump_clone(),
            self.channel.name.clone() + ":source",
            buffer_rx,
        )
    }

    pub(crate) async fn create_conditioning_pipeline(
        &self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> Result<StandardPipeOutput, DTTError> {
        match self.channel.data_type {
            NDSDataType::Int8 => {
                self.create_conditioning_pipeline_generic_real::<i8>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Int16 => {
                self.create_conditioning_pipeline_generic_real::<i16>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Int32 => {
                self.create_conditioning_pipeline_generic_real::<i32>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Int64 => {
                self.create_conditioning_pipeline_generic_real::<i64>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Float32 => {
                self.create_conditioning_pipeline_generic_real::<f32>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Float64 => {
                self.create_conditioning_pipeline_generic_real::<f64>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::UInt64 => {
                self.create_conditioning_pipeline_generic_real::<u64>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::UInt32 => {
                self.create_conditioning_pipeline_generic_real::<u32>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::UInt16 => {
                self.create_conditioning_pipeline_generic_real::<u16>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::UInt8 => {
                self.create_conditioning_pipeline_generic_real::<u8>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Complex64 => {
                self.create_conditioning_pipeline_generic_complex::<c64>(rc, timeline, buffer_rx)
                    .await
            }
            NDSDataType::Complex128 => {
                self.create_conditioning_pipeline_generic_complex::<c128>(rc, timeline, buffer_rx)
                    .await
            } //NDSDataType::String => return Err(DTTError::UnsupportedTypeError("String", "when creating conditioning pipeline")),
        }
    }

    async fn create_conditioning_pipeline_generic_real<T>(
        &self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> Result<StandardPipeOutput, DTTError>
    where
        T: ConvertTo<f64> + PipeDataPrimitive + Copy,
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        let ds = DataSourcePipeline::create::<T>(
            rc.clone(),
            self.channel.name.clone() + ":source",
            buffer_rx,
        );

        if self.do_heterodyne {
            setup_conditioning_pipeline_heterodyned_real(rc.ump_clone(), self, timeline, &ds).await
        } else {
            setup_conditioning_pipeline_non_heterodyned_real(rc.ump_clone(), self, timeline, &ds)
                .await
        }
    }

    async fn create_conditioning_pipeline_generic_complex<T>(
        &self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        buffer_rx: tokio::sync::mpsc::Receiver<Buffer>,
    ) -> Result<StandardPipeOutput, DTTError>
    where
        T: ConvertTo<c128> + PipeDataPrimitive + Copy,
        TimeDomainArray<T>: TryFrom<Buffer, Error = DTTError>,
    {
        let ds = DataSourcePipeline::create::<T>(
            rc.clone(),
            self.channel.name.clone() + ":source",
            buffer_rx,
        );

        setup_conditioning_pipeline_complex(rc.ump_clone(), self, timeline, &ds).await
    }
}
