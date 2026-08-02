use std::fmt::{Display, Formatter};

use pipelines::{PipelineSubscriber, complex::c128, stateless::pure::PureStatelessPipeline1};
use tokio::sync::mpsc;
use user_messages::UserMsgProvider;

use crate::{
    AnalysisResult,
    analysis::{
        conditioning::StandardPipeOutput,
        general,
        types::{
            frequency_domain_array::{
                FreqDomainArray, FreqDomainArrayComplex, FreqDomainArrayReal,
            },
            time_domain_array::{TimeDomainArray, TimeDomainArrayComplex, TimeDomainArrayReal},
        },
    },
    data_source::buffer::Buffer,
    errors::DTTError,
    run_context::RunContext,
};

/// owns the output structure for an edge
/// so that target nodes know what to link to
#[derive(Default, Debug)]
pub(crate) enum OutputSource {
    #[default]
    NotSet,
    // receiver for NDS buffer
    BufferRx(mpsc::Receiver<Buffer>),

    // pipeline subscribers
    PipelineTDArrayFloat64(PipelineSubscriber<TimeDomainArray<f64>>),
    PipelineTDArrayComplex128(PipelineSubscriber<TimeDomainArray<c128>>),
    PipelineFreqArrayFloat64(PipelineSubscriber<FreqDomainArray<f64>>),
    PipelineFreqArrayComplex128(PipelineSubscriber<FreqDomainArray<c128>>),

    PipelineTDArrayInt64(PipelineSubscriber<TimeDomainArray<i64>>),
    PipelineTDArrayInt32(PipelineSubscriber<TimeDomainArray<i32>>),
    PipelineTDArrayInt16(PipelineSubscriber<TimeDomainArray<i16>>),
    PipelineTDArrayInt8(PipelineSubscriber<TimeDomainArray<i8>>),

    PipelineTDArrayUInt64(PipelineSubscriber<TimeDomainArray<u64>>),
    PipelineTDArrayUInt32(PipelineSubscriber<TimeDomainArray<u32>>),
    PipelineTDArrayUInt16(PipelineSubscriber<TimeDomainArray<u16>>),
    PipelineTDArrayUInt8(PipelineSubscriber<TimeDomainArray<u8>>),

    // here we've given up on trying to match types on compile time
    // and are just using an enum
    // a PipelineResultValue must also have a string name to use as an identifier
    PipelineResultValue(PipelineSubscriber<AnalysisResult>),
}

impl Display for OutputSource {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            OutputSource::NotSet => write!(f, "Not Set"),
            OutputSource::BufferRx(_) => write!(f, "NDS Buffer Receiver"),
            OutputSource::PipelineFreqArrayFloat64(_) => write!(f, "Real-valued frequency array"),
            OutputSource::PipelineFreqArrayComplex128(_) => {
                write!(f, "Complex-valued frequency array")
            }
            OutputSource::PipelineTDArrayFloat64(_) => write!(f, "Real-valued time-domain array"),
            OutputSource::PipelineTDArrayComplex128(_) => {
                write!(f, "Complex-valued time-domain array")
            }

            OutputSource::PipelineTDArrayInt64(_) => write!(f, "int 64 Time domain array"),
            OutputSource::PipelineTDArrayInt32(_) => write!(f, "int 32 Time domain array"),
            OutputSource::PipelineTDArrayInt16(_) => write!(f, "int 16 Time domain array"),
            OutputSource::PipelineTDArrayInt8(_) => write!(f, "int 8 Time domain array"),
            OutputSource::PipelineTDArrayUInt64(_) => {
                write!(f, "unsigned int 64 Time domain array")
            }
            OutputSource::PipelineTDArrayUInt32(_) => {
                write!(f, "unsigned int 32 Time domain array")
            }
            OutputSource::PipelineTDArrayUInt16(_) => {
                write!(f, "unsigned int 16 Time domain array")
            }
            OutputSource::PipelineTDArrayUInt8(_) => write!(f, "unsigned int 8 Time domain array"),

            OutputSource::PipelineResultValue(_) => write!(f, "Result"),
        }
    }
}

impl From<StandardPipeOutput> for OutputSource {
    fn from(standard_pipe: StandardPipeOutput) -> Self {
        match standard_pipe {
            StandardPipeOutput::Float64(subscriber) => {
                OutputSource::PipelineTDArrayFloat64(subscriber)
            }
            StandardPipeOutput::Complex128(subscriber) => {
                OutputSource::PipelineTDArrayComplex128(subscriber)
            }

            StandardPipeOutput::Int64(subscriber) => OutputSource::PipelineTDArrayInt64(subscriber),
            StandardPipeOutput::Int32(subscriber) => OutputSource::PipelineTDArrayInt32(subscriber),
            StandardPipeOutput::Int16(subscriber) => OutputSource::PipelineTDArrayInt16(subscriber),
            StandardPipeOutput::Int8(subscriber) => OutputSource::PipelineTDArrayInt8(subscriber),

            StandardPipeOutput::UInt64(subscriber) => {
                OutputSource::PipelineTDArrayUInt64(subscriber)
            }
            StandardPipeOutput::UInt32(subscriber) => {
                OutputSource::PipelineTDArrayUInt32(subscriber)
            }
            StandardPipeOutput::UInt16(subscriber) => {
                OutputSource::PipelineTDArrayUInt16(subscriber)
            }
            StandardPipeOutput::UInt8(subscriber) => OutputSource::PipelineTDArrayUInt8(subscriber),
            //StandardPipeOutput::String(subscriber ) => OutputSource::PipelineTDArrayString(subscriber),
        }
    }
}

impl From<PipelineSubscriber<TimeDomainArrayReal>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArrayReal>) -> Self {
        OutputSource::PipelineTDArrayFloat64(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArrayComplex>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArrayComplex>) -> Self {
        OutputSource::PipelineTDArrayComplex128(value)
    }
}

impl From<PipelineSubscriber<FreqDomainArrayReal>> for OutputSource {
    fn from(value: PipelineSubscriber<FreqDomainArrayReal>) -> Self {
        OutputSource::PipelineFreqArrayFloat64(value)
    }
}

impl From<PipelineSubscriber<FreqDomainArrayComplex>> for OutputSource {
    fn from(value: PipelineSubscriber<FreqDomainArrayComplex>) -> Self {
        OutputSource::PipelineFreqArrayComplex128(value)
    }
}

impl From<PipelineSubscriber<AnalysisResult>> for OutputSource {
    fn from(value: PipelineSubscriber<AnalysisResult>) -> Self {
        OutputSource::PipelineResultValue(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<i64>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<i64>>) -> Self {
        OutputSource::PipelineTDArrayInt64(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<i32>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<i32>>) -> Self {
        OutputSource::PipelineTDArrayInt32(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<i16>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<i16>>) -> Self {
        OutputSource::PipelineTDArrayInt16(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<i8>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<i8>>) -> Self {
        OutputSource::PipelineTDArrayInt8(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<u64>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<u64>>) -> Self {
        OutputSource::PipelineTDArrayUInt64(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<u32>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<u32>>) -> Self {
        OutputSource::PipelineTDArrayUInt32(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<u16>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<u16>>) -> Self {
        OutputSource::PipelineTDArrayUInt16(value)
    }
}

impl From<PipelineSubscriber<TimeDomainArray<u8>>> for OutputSource {
    fn from(value: PipelineSubscriber<TimeDomainArray<u8>>) -> Self {
        OutputSource::PipelineTDArrayUInt8(value)
    }
}

impl OutputSource {
    /// copy any value except NDSBufferRX, which isn't cloneable.
    /// NDSBufferRX is changed to NotSet
    pub(crate) fn almost_copy(&self) -> Self {
        match self {
            OutputSource::NotSet => OutputSource::NotSet,
            OutputSource::BufferRx(_) => OutputSource::NotSet,
            OutputSource::PipelineTDArrayFloat64(x) => {
                OutputSource::PipelineTDArrayFloat64(x.clone())
            }
            OutputSource::PipelineTDArrayComplex128(x) => {
                OutputSource::PipelineTDArrayComplex128(x.clone())
            }
            OutputSource::PipelineFreqArrayFloat64(x) => {
                OutputSource::PipelineFreqArrayFloat64(x.clone())
            }
            OutputSource::PipelineFreqArrayComplex128(x) => {
                OutputSource::PipelineFreqArrayComplex128(x.clone())
            }
            OutputSource::PipelineResultValue(x) => OutputSource::PipelineResultValue(x.clone()),

            OutputSource::PipelineTDArrayInt64(x) => OutputSource::PipelineTDArrayInt64(x.clone()),
            OutputSource::PipelineTDArrayInt32(x) => OutputSource::PipelineTDArrayInt32(x.clone()),
            OutputSource::PipelineTDArrayInt16(x) => OutputSource::PipelineTDArrayInt16(x.clone()),
            OutputSource::PipelineTDArrayInt8(x) => OutputSource::PipelineTDArrayInt8(x.clone()),

            OutputSource::PipelineTDArrayUInt64(x) => {
                OutputSource::PipelineTDArrayUInt64(x.clone())
            }
            OutputSource::PipelineTDArrayUInt32(x) => {
                OutputSource::PipelineTDArrayUInt32(x.clone())
            }
            OutputSource::PipelineTDArrayUInt16(x) => {
                OutputSource::PipelineTDArrayUInt16(x.clone())
            }
            OutputSource::PipelineTDArrayUInt8(x) => OutputSource::PipelineTDArrayUInt8(x.clone()),
            //OutputSource::PipelineTDArrayString(x) => OutputSource::PipelineTDArrayString(x.clone()),
        }
    }

    #[allow(dead_code)]
    /// Creates a results pipeline subscriber
    pub(crate) async fn to_value_pipeline(
        &self,
        rc: &Box<RunContext>,
        name: impl Into<String>,
    ) -> Result<PipelineSubscriber<AnalysisResult>, DTTError> {
        match self {
            OutputSource::NotSet | OutputSource::BufferRx(_) => {
                Err(DTTError::AnalysisPipelineError(
                    "value_pipeline can only be created from another pipeline".to_string(),
                ))
            }
            OutputSource::PipelineFreqArrayComplex128(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineFreqArrayFloat64(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayFloat64(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayComplex128(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }

            OutputSource::PipelineTDArrayInt64(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayInt32(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayInt16(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayInt8(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }

            OutputSource::PipelineTDArrayUInt64(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayUInt32(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayUInt16(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }
            OutputSource::PipelineTDArrayUInt8(a) => {
                Ok(
                    PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate)
                        .await?,
                )
            }

            // OutputSource::PipelineTDArrayString(a) => {
            //     Ok( PureStatelessPipeline1::start(rc.ump_clone(), name, a, general::into::generate).await )
            // },
            OutputSource::PipelineResultValue(a) => Ok(a.clone()),
        }
    }
}
