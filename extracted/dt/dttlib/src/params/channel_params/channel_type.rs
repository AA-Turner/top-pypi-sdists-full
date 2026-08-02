#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass_enum;

/// channel type is used in NDS queries.  I'm not sure how
/// important these are, or how they map to NDS records.
#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(frozen, eq))]
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub enum ChannelType {
    Unknown,
    Online,
    #[default]
    Raw,
    RDS,
    STrend,
    MTrend,
    TestPoint,
    Static,
}

#[cfg(feature = "nds")]
impl From<nds2_client_rs::ChannelType> for ChannelType {
    fn from(c: nds2_client_rs::ChannelType) -> Self {
        match c {
            nds2_client_rs::ChannelType::Unknown => ChannelType::Unknown,
            nds2_client_rs::ChannelType::Online => ChannelType::Online,
            nds2_client_rs::ChannelType::Raw => ChannelType::Raw,
            nds2_client_rs::ChannelType::RDS => ChannelType::RDS,
            nds2_client_rs::ChannelType::STrend => ChannelType::STrend,
            nds2_client_rs::ChannelType::MTrend => ChannelType::MTrend,
            nds2_client_rs::ChannelType::TestPoint => ChannelType::TestPoint,
            nds2_client_rs::ChannelType::Static => ChannelType::Static,
            nds2_client_rs::ChannelType { repr: _ } => ChannelType::Unknown,
        }
    }
}

#[cfg(feature = "nds")]
impl From<ChannelType> for nds2_client_rs::ChannelType {
    fn from(c: ChannelType) -> Self {
        match c {
            ChannelType::Unknown => nds2_client_rs::ChannelType::Unknown,
            ChannelType::Online => nds2_client_rs::ChannelType::Online,
            ChannelType::Raw => nds2_client_rs::ChannelType::Raw,
            ChannelType::RDS => nds2_client_rs::ChannelType::RDS,
            ChannelType::STrend => nds2_client_rs::ChannelType::STrend,
            ChannelType::MTrend => nds2_client_rs::ChannelType::MTrend,
            ChannelType::TestPoint => nds2_client_rs::ChannelType::TestPoint,
            ChannelType::Static => nds2_client_rs::ChannelType::Static,
        }
    }
}

impl From<ChannelType> for nds_cache_rs::buffer::ChannelType {
    fn from(c: ChannelType) -> Self {
        match c {
            ChannelType::Unknown => nds_cache_rs::buffer::ChannelType::Unknown,
            ChannelType::Online => nds_cache_rs::buffer::ChannelType::Online,
            ChannelType::Raw => nds_cache_rs::buffer::ChannelType::Raw,
            ChannelType::RDS => nds_cache_rs::buffer::ChannelType::RDS,
            ChannelType::STrend => nds_cache_rs::buffer::ChannelType::STrend,
            ChannelType::MTrend => nds_cache_rs::buffer::ChannelType::MTrend,
            ChannelType::TestPoint => nds_cache_rs::buffer::ChannelType::TestPoint,
            ChannelType::Static => nds_cache_rs::buffer::ChannelType::Static,
        }
    }
}

impl From<nds_cache_rs::buffer::ChannelType> for ChannelType {
    fn from(c: nds_cache_rs::buffer::ChannelType) -> Self {
        match c {
            nds_cache_rs::buffer::ChannelType::Unknown => ChannelType::Unknown,
            nds_cache_rs::buffer::ChannelType::Online => ChannelType::Online,
            nds_cache_rs::buffer::ChannelType::Raw => ChannelType::Raw,
            nds_cache_rs::buffer::ChannelType::RDS => ChannelType::RDS,
            nds_cache_rs::buffer::ChannelType::STrend => ChannelType::STrend,
            nds_cache_rs::buffer::ChannelType::MTrend => ChannelType::MTrend,
            nds_cache_rs::buffer::ChannelType::TestPoint => ChannelType::TestPoint,
            nds_cache_rs::buffer::ChannelType::Static => ChannelType::Static,
        }
    }
}
