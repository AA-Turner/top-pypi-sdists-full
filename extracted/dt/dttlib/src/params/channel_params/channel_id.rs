use crate::params::channel_params::Channel;
use crate::{errors::DTTError, params::channel_params::ChannelName};
#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::new;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyclass_enum, gen_stub_pymethods};
use std::fmt::Display;

#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, eq, eq_int, hash, ord)
)]
#[derive(Clone, Debug, Hash, PartialEq, Eq, Default, PartialOrd, Ord)]
/// The trend of a ChannelId
pub enum TrendType {
    #[default]
    Raw,
    Minute,
    Second,
}

impl Display for TrendType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            TrendType::Raw => write!(f, ""),
            TrendType::Minute => write!(f, "m-trend"),
            TrendType::Second => write!(f, "s-trend"),
        }
    }
}

/// Channel statistics type for a trend channel, or Raw for raw channels
#[derive(Clone, Debug, Default, Hash, PartialEq, Eq, Ord, PartialOrd)]
#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, eq, eq_int, hash, ord)
)]
pub enum TrendStat {
    /// Raw data, not a trend channel
    #[default]
    Raw,
    Mean,
    /// Root-mean-square
    Rms,
    Min,
    Max,
    /// Number of data points in the trend bucket
    N,
}

impl Display for TrendStat {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            TrendStat::Raw => write!(f, ""),
            TrendStat::Mean => write!(f, "mean"),
            TrendStat::Rms => write!(f, "rms"),
            TrendStat::Min => write!(f, "min"),
            TrendStat::Max => write!(f, "max"),
            TrendStat::N => write!(f, "n"),
        }
    }
}

impl TryFrom<&str> for TrendStat {
    type Error = DTTError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "" => Ok(TrendStat::Raw),
            "mean" => Ok(TrendStat::Mean),
            "rms" => Ok(TrendStat::Rms),
            "min" => Ok(TrendStat::Min),
            "max" => Ok(TrendStat::Max),
            "n" => Ok(TrendStat::N),
            _ => Err(DTTError::UnknownTrendStat(value.to_string())),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl TrendStat {
    /// used for names of exported data blocks
    pub fn data_name(&self) -> &'static str {
        match self {
            TrendStat::Raw => "raw",
            TrendStat::Mean => "mean",
            TrendStat::Rms => "rms",
            TrendStat::Min => "min",
            TrendStat::Max => "max",
            TrendStat::N => "n",
        }
    }
}

impl TryFrom<&str> for TrendType {
    type Error = DTTError;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "" => Ok(TrendType::Raw),
            "m-trend" => Ok(TrendType::Minute),
            "s-trend" => Ok(TrendType::Second),
            _ => Err(DTTError::UnknownTrendType(value.to_string())),
        }
    }
}

/// Used internally to map full name and trend info

/// this is the minimum needed information
/// to generate a request to the cache or other data source
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, get_all, hash, eq, ord)
)]
#[derive(Clone, Debug, Hash, Eq, PartialEq, Default, Ord, PartialOrd)]
pub struct ChannelHeader {
    pub name: String,
    pub trend_type: TrendType,
    pub trend_stat: TrendStat,
}

impl From<&Channel> for ChannelHeader {
    fn from(c: &Channel) -> Self {
        Self {
            name: c.name.clone(),
            trend_type: c.trend_type.clone(),
            trend_stat: c.trend_stat.clone(),
        }
    }
}

impl ChannelHeader {
    pub fn new(name: String, trend_type: TrendType, trend_stat: TrendStat) -> Self {
        Self {
            name,
            trend_type,
            trend_stat,
        }
    }

    /// get the name needed to request the channel from NDS
    pub fn nds_name(&self) -> String {
        if self.trend_type == TrendType::Raw {
            self.name.clone()
        } else {
            format!("{}.{},{}", self.name, self.trend_stat, self.trend_type)
        }
    }
}

impl From<(&ChannelHeader, TrendType)> for ChannelHeader {
    fn from(value: (&ChannelHeader, TrendType)) -> Self {
        Self {
            trend_type: value.1,
            ..value.0.clone()
        }
    }
}

/// Provides enough info to query a channel from an NDS server by name.
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, get_all, hash, eq, str)
)]
#[derive(Clone, Debug, Hash, Eq, PartialEq, Default, PartialOrd, Ord)]
pub struct ChannelId {
    pub name: String,
    pub trend_type: TrendType,
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl ChannelId {
    #[new]
    pub fn new(name: String, trend_type: TrendType) -> Self {
        Self { name, trend_type }
    }

    /// These are the stats we expect to get for a single trend request.
    /// One ChannelID will return into a channel for each.
    pub fn expected_stats(&self) -> Vec<TrendStat> {
        vec![
            TrendStat::Max,
            TrendStat::Min,
            TrendStat::Mean,
            TrendStat::Rms,
        ]
    }
}

impl ChannelId {
    /// Convert to the headers needed to
    /// mark unresolved channels in a ViewSet
    pub(crate) fn to_channel_headers(&self) -> Vec<ChannelHeader> {
        match self.trend_type {
            TrendType::Raw => vec![ChannelHeader::new(
                self.name.clone(),
                TrendType::Raw,
                TrendStat::Raw,
            )],
            ref t => self
                .expected_stats()
                .iter()
                .map(|x| ChannelHeader::new(self.name.clone(), t.clone(), x.clone()))
                .collect(),
        }
    }
}

impl From<&str> for ChannelId {
    fn from(s: &str) -> Self {
        Self::new(s.to_string(), TrendType::Raw)
    }
}

impl Display for ChannelId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.trend_type == TrendType::Raw {
            writeln!(f, "{} [{}]", self.name, self.trend_type)
        } else {
            writeln!(f, "{}", self.name)
        }
    }
}

impl From<(&ChannelName, TrendType)> for ChannelId {
    fn from(value: (&ChannelName, TrendType)) -> Self {
        Self {
            name: value.0.name.clone(),
            trend_type: value.1,
        }
    }
}

impl From<(&ChannelId, TrendType)> for ChannelId {
    fn from(value: (&ChannelId, TrendType)) -> Self {
        Self {
            name: value.0.name.clone(),
            trend_type: value.1,
        }
    }
}
