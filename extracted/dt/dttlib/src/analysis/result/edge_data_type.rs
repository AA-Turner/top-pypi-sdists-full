use std::fmt::{Display, Formatter};

use crate::params::channel_params::NDSDataType;

/// an unencumbered simple enum of result type to help with
/// graphs of the analysis
#[allow(dead_code)]
#[derive(Clone, PartialEq, Eq, Debug)]
pub enum EdgeDataType {
    FreqDomainValueComplex,
    FreqDomainValueReal,
    TimeDomainValueReal,
    TimeDomainValueComplex,
    CustomFreqDomainReal,
    CustomFreqDomainComplex,

    TimeDomainValueInt64,
    TimeDomainValueInt32,
    TimeDomainValueInt16,
    TimeDomainValueInt8,

    TimeDomainValueUInt64,
    TimeDomainValueUInt32,
    TimeDomainValueUInt16,
    TimeDomainValueUInt8,

    TimeDomainValueString,
    // TimeDomainMinMaxReal,
    // TimeDomainMinMaxInt64,
    // TimeDomainMinMaxInt32,
    // TimeDomainMinMaxInt16,
    // TimeDomainMinMaxInt8,
    // TimeDomainMinMaxUInt64,
    // TimeDomainMinMaxUInt32,
    // TimeDomainMinMaxUInt16,
    // TimeDomainMinMaxUInt8,
}

impl Display for EdgeDataType {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::FreqDomainValueComplex => write!(f, "FFT"),
            Self::FreqDomainValueReal => write!(f, "ASD"),
            Self::TimeDomainValueReal => write!(f, "Real-valued time-domain array"),
            Self::TimeDomainValueComplex => write!(f, "Complex-valued time-domain array"),
            Self::CustomFreqDomainComplex => {
                write!(f, "Custom complex-valued frequency-domain array")
            }
            Self::CustomFreqDomainReal => write!(f, "Custom real-valued frequency-domain array"),
            Self::TimeDomainValueInt64 => write!(f, "64-bit integer time-domain array"),
            Self::TimeDomainValueInt32 => write!(f, "32-bit integer time-domain array"),
            Self::TimeDomainValueInt16 => write!(f, "16-bit integer time-domain array"),
            Self::TimeDomainValueInt8 => write!(f, "8-bit integer time-domain array"),
            Self::TimeDomainValueUInt64 => write!(f, "64-bit unsigned integer time-domain array"),
            Self::TimeDomainValueUInt32 => write!(f, "32-bit unsigned integer time-domain array"),
            Self::TimeDomainValueUInt16 => write!(f, "16-bit unsigned integer time-domain array"),
            Self::TimeDomainValueUInt8 => write!(f, "8-bit unsigned integer time-domain array"),
            Self::TimeDomainValueString => write!(f, "String time-domain array"),
            // Self::TimeDomainMinMaxReal => write!(
            //     f,
            //     "Pair of real-valued time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxInt64 => write!(
            //     f,
            //     "Pair of 64-bit integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxInt32 => write!(
            //     f,
            //     "Pair of 32-bit integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxInt16 => write!(
            //     f,
            //     "Pair of 16-bit integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxInt8 => write!(
            //     f,
            //     "Pair of 8-bit integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxUInt64 => write!(
            //     f,
            //     "Pair of 64-bit unsigned integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxUInt32 => write!(
            //     f,
            //     "Pair of 32-bit unsigned integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxUInt16 => write!(
            //     f,
            //     "Pair of 16-bit unsigned integer time-domain arrays representing min and max"
            // ),
            // Self::TimeDomainMinMaxUInt8 => write!(
            //     f,
            //     "Pair of 8-bit unsigned integer time-domain arrays representing min and max"
            // ),
        }
    }
}

/// convert NDSDataType to a ResultType for a DataSource pipeline source
impl From<NDSDataType> for EdgeDataType {
    fn from(value: NDSDataType) -> Self {
        match value {
            NDSDataType::Complex64 | NDSDataType::Complex128 => Self::TimeDomainValueComplex,
            NDSDataType::Float64 | NDSDataType::Float32 => Self::TimeDomainValueReal,
            NDSDataType::Int64 => Self::TimeDomainValueInt64,
            NDSDataType::Int32 => Self::TimeDomainValueInt32,
            NDSDataType::Int16 => Self::TimeDomainValueInt16,
            NDSDataType::Int8 => Self::TimeDomainValueInt8,
            NDSDataType::UInt64 => Self::TimeDomainValueUInt64,
            NDSDataType::UInt32 => Self::TimeDomainValueUInt32,
            NDSDataType::UInt16 => Self::TimeDomainValueUInt16,
            NDSDataType::UInt8 => Self::TimeDomainValueUInt8,
            //NDSDataType::String => Self::TimeDomainValueString,
        }
    }
}

impl EdgeDataType {
    pub(crate) fn is_complex(&self) -> bool {
        match self {
            Self::CustomFreqDomainComplex
            | Self::FreqDomainValueComplex
            | Self::TimeDomainValueComplex => true,
            Self::CustomFreqDomainReal
            | Self::FreqDomainValueReal
            | Self::TimeDomainValueReal
            | Self::TimeDomainValueInt64
            // | Self::TimeDomainMinMaxReal
            // | Self::TimeDomainMinMaxInt64
            // | Self::TimeDomainMinMaxInt32
            // | Self::TimeDomainMinMaxInt16
            // | Self::TimeDomainMinMaxInt8
            // | Self::TimeDomainMinMaxUInt64
            // | Self::TimeDomainMinMaxUInt32
            // | Self::TimeDomainMinMaxUInt16
            // | Self::TimeDomainMinMaxUInt8
            | Self::TimeDomainValueInt32
            | Self::TimeDomainValueInt16
            | Self::TimeDomainValueInt8
            | Self::TimeDomainValueUInt64
            | Self::TimeDomainValueUInt32
            | Self::TimeDomainValueUInt16
            | Self::TimeDomainValueUInt8
            | Self::TimeDomainValueString => false,
        }
    }

    #[allow(dead_code)]
    pub(crate) fn is_real(&self) -> bool {
        match self {
            Self::CustomFreqDomainComplex
            | Self::FreqDomainValueComplex
            | Self::TimeDomainValueComplex
            | Self::TimeDomainValueString => false,
            Self::CustomFreqDomainReal
            | Self::FreqDomainValueReal
            | Self::TimeDomainValueReal
            | Self::TimeDomainValueInt64
            // | Self::TimeDomainMinMaxReal
            // | Self::TimeDomainMinMaxInt64
            // | Self::TimeDomainMinMaxInt32
            // | Self::TimeDomainMinMaxInt16
            // | Self::TimeDomainMinMaxInt8
            // | Self::TimeDomainMinMaxUInt64
            // | Self::TimeDomainMinMaxUInt32
            // | Self::TimeDomainMinMaxUInt16
            // | Self::TimeDomainMinMaxUInt8
            | Self::TimeDomainValueInt32
            | Self::TimeDomainValueInt16
            | Self::TimeDomainValueInt8
            | Self::TimeDomainValueUInt64
            | Self::TimeDomainValueUInt32
            | Self::TimeDomainValueUInt16
            | Self::TimeDomainValueUInt8 => true,
        }
    }

    pub(crate) fn is_time_domain(&self) -> bool {
        match self {
            Self::TimeDomainValueReal
            | Self::TimeDomainValueComplex
            | Self::TimeDomainValueInt64
            | Self::TimeDomainValueInt32
            | Self::TimeDomainValueInt16
            | Self::TimeDomainValueInt8
            | Self::TimeDomainValueUInt64
            | Self::TimeDomainValueUInt32
            | Self::TimeDomainValueUInt16
            | Self::TimeDomainValueUInt8
            | Self::TimeDomainValueString => true,
            // | Self::TimeDomainMinMaxReal
            // | Self::TimeDomainMinMaxInt64
            // | Self::TimeDomainMinMaxInt32
            // | Self::TimeDomainMinMaxInt16
            // | Self::TimeDomainMinMaxInt8
            // | Self::TimeDomainMinMaxUInt64
            // | Self::TimeDomainMinMaxUInt32
            // | Self::TimeDomainMinMaxUInt16
            // | Self::TimeDomainMinMaxUInt8 => true,
            Self::CustomFreqDomainComplex
            | Self::CustomFreqDomainReal
            | Self::FreqDomainValueReal
            | Self::FreqDomainValueComplex => false,
        }
    }

    #[allow(dead_code)]
    pub(crate) fn is_freq_domain(&self) -> bool {
        match self {
            Self::TimeDomainValueReal
            | Self::TimeDomainValueComplex
            | Self::TimeDomainValueInt64
            | Self::TimeDomainValueInt32
            | Self::TimeDomainValueInt16
            | Self::TimeDomainValueInt8
            | Self::TimeDomainValueUInt64
            | Self::TimeDomainValueUInt32
            | Self::TimeDomainValueUInt16
            | Self::TimeDomainValueUInt8
            | Self::TimeDomainValueString => false,
            // | Self::TimeDomainMinMaxReal
            // | Self::TimeDomainMinMaxInt64
            // | Self::TimeDomainMinMaxInt32
            // | Self::TimeDomainMinMaxInt16
            // | Self::TimeDomainMinMaxInt8
            // | Self::TimeDomainMinMaxUInt64
            // | Self::TimeDomainMinMaxUInt32
            // | Self::TimeDomainMinMaxUInt16
            // | Self::TimeDomainMinMaxUInt8 => false,
            Self::CustomFreqDomainComplex
            | Self::CustomFreqDomainReal
            | Self::FreqDomainValueComplex
            | Self::FreqDomainValueReal => true,
        }
    }
}
