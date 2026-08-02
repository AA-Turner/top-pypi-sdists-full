use std::fmt::Display;

#[cfg(feature = "nds")]
use nds2_client_rs::DataType;
use num_traits::FromPrimitive;

#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass_enum;

/// These values are taken from the NDS2 client
/// With a hoped-for extension for
/// Complex128
/// Note the names for complex take the total size of the number
/// Not the size of real or imaginary components as the actual NDS2 client does.
///
/// So an NDS2 Client type Complex32 is an NDSDataType::Complex64
#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(eq))]
#[derive(Clone, Debug, PartialEq, Hash, Default)]
pub enum NDSDataType {
    Int16,
    Int32,
    Int64,
    #[default]
    Float32,
    Float64,
    Complex64,
    UInt32,

    /// not yet implemented in NDS or Arrakis
    Complex128,
    UInt64,
    UInt16,
    Int8,
    UInt8,
    //String,
}

impl Display for NDSDataType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NDSDataType::Int16 => write!(f, "i16"),
            NDSDataType::Int32 => write!(f, "i32"),
            NDSDataType::Int64 => write!(f, "i64"),
            NDSDataType::Float32 => write!(f, "f32"),
            NDSDataType::Float64 => write!(f, "f64"),
            NDSDataType::Complex64 => write!(f, "c64"),
            NDSDataType::UInt32 => write!(f, "u32"),
            NDSDataType::Complex128 => write!(f, "c128"),
            NDSDataType::UInt64 => write!(f, "u64"),
            NDSDataType::UInt16 => write!(f, "u16"),
            NDSDataType::Int8 => write!(f, "i8"),
            NDSDataType::UInt8 => write!(f, "u8"),
        }
    }
}

impl FromPrimitive for NDSDataType {
    fn from_i64(n: i64) -> Option<Self> {
        Self::from_u64(u64::from_i64(n)?)
    }

    fn from_u64(n: u64) -> Option<Self> {
        match n {
            1 => Some(NDSDataType::Int16),
            2 => Some(NDSDataType::Int32),
            3 => Some(NDSDataType::Int64),
            4 => Some(NDSDataType::Float32),
            5 => Some(NDSDataType::Float64),
            6 => Some(NDSDataType::Complex64),
            7 => Some(NDSDataType::UInt32),
            8 => Some(NDSDataType::Complex128),
            _ => None,
        }
    }
}

#[cfg(feature = "nds")]
impl Into<DataType> for NDSDataType {
    fn into(self) -> DataType {
        match self {
            NDSDataType::Int16 => DataType::Int16,
            NDSDataType::Int32 => DataType::Int32,
            NDSDataType::Int64 => DataType::Int64,
            NDSDataType::Float32 => DataType::Float32,
            NDSDataType::Float64 => DataType::Float64,
            NDSDataType::Complex64 => DataType::Complex32,
            NDSDataType::UInt32 => DataType::UInt32,
            NDSDataType::Complex128
            | NDSDataType::UInt64
            | NDSDataType::UInt16
            | NDSDataType::Int8
            | NDSDataType::UInt8 => DataType::Unknown,
            //NDSDataType::String
        }
    }
}

impl Into<nds_cache_rs::buffer::DataType> for NDSDataType {
    fn into(self) -> nds_cache_rs::buffer::DataType {
        match self {
            NDSDataType::Int16 => nds_cache_rs::buffer::DataType::Int16,
            NDSDataType::Int32 => nds_cache_rs::buffer::DataType::Int32,
            NDSDataType::Int64 => nds_cache_rs::buffer::DataType::Int64,
            NDSDataType::Float32 => nds_cache_rs::buffer::DataType::Float32,
            NDSDataType::Float64 => nds_cache_rs::buffer::DataType::Float64,
            NDSDataType::UInt32 => nds_cache_rs::buffer::DataType::UInt32,
            NDSDataType::Complex64 => nds_cache_rs::buffer::DataType::Complex32,
            NDSDataType::Complex128
            | NDSDataType::UInt64
            | NDSDataType::UInt16
            | NDSDataType::Int8
            | NDSDataType::UInt8 => nds_cache_rs::buffer::DataType::Unknown,
            //NDSDataType::String
        }
    }
}

impl From<nds_cache_rs::buffer::DataType> for NDSDataType {
    fn from(nds_type: nds_cache_rs::buffer::DataType) -> Self {
        match nds_type {
            nds_cache_rs::buffer::DataType::Int8 => NDSDataType::Int8,
            nds_cache_rs::buffer::DataType::Int16 => NDSDataType::Int16,
            nds_cache_rs::buffer::DataType::Int32 => NDSDataType::Int32,
            nds_cache_rs::buffer::DataType::Int64 => NDSDataType::Int64,
            nds_cache_rs::buffer::DataType::Float32 => NDSDataType::Float32,
            nds_cache_rs::buffer::DataType::Float64 => NDSDataType::Float64,
            nds_cache_rs::buffer::DataType::UInt8 => NDSDataType::UInt8,
            nds_cache_rs::buffer::DataType::UInt16 => NDSDataType::UInt16,
            nds_cache_rs::buffer::DataType::UInt32 => NDSDataType::UInt32,
            nds_cache_rs::buffer::DataType::UInt64 => NDSDataType::UInt64,
            nds_cache_rs::buffer::DataType::Complex32 => NDSDataType::Complex64,
            nds_cache_rs::buffer::DataType::Complex64 => NDSDataType::Complex128,
            nds_cache_rs::buffer::DataType::Unknown => NDSDataType::UInt8,
        }
    }
}

impl NDSDataType {
    pub fn is_complex(&self) -> bool {
        match self {
            NDSDataType::Complex64 | NDSDataType::Complex128 => true,
            _ => false,
        }
    }
}
