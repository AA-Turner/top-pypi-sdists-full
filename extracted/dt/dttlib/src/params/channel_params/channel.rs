use super::{ChannelSettings, ChannelType, NDSDataType, TrendStat, TrendType, Unit};
use crate::errors::DTTError;
#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::{getter, new};
use ligo_hires_gps_time::PipDuration;
use nds_cache_rs::buffer::Buffer;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::cmp::Ordering;
use std::fmt::Display;
use std::hash::{Hash, Hasher};

#[derive(Clone, Debug, Default)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(eq, get_all, hash, frozen, str, ord)
)]
pub struct Channel {
    pub name: String,
    pub data_type: NDSDataType,
    pub channel_type: ChannelType,
    pub period: PipDuration,
    pub dcu_id: Option<i64>,
    pub channel_number: Option<i64>,
    pub calibration: Option<i64>,
    pub heterodyne_freq_hz: Option<f64>,
    pub gain: Option<f64>,
    pub slope: Option<f64>,
    pub offset: Option<f64>,
    pub use_active_time: bool,
    pub units: Unit,

    // trend info
    pub trend_stat: TrendStat,
    pub trend_type: TrendType,
}

impl Display for Channel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}:{}:{}:{}",
            self.name, self.data_type, self.trend_stat, self.trend_type
        )
    }
}

/// Identification and calibration data for a channel
/// The sort of info we might expect from a data server channel list.
impl Hash for Channel {
    /// always update hash and PartialEq::eq to use the same data subset
    fn hash<H: Hasher>(&self, state: &mut H) {
        // channel name
        self.name.hash(state);

        // rate
        // get period in pips_per_sec
        let period_pips = self.period;
        period_pips.hash(state);

        // type
        self.data_type.hash(state);

        // trend info
        self.trend_stat.hash(state);
        self.trend_type.hash(state);
    }
}

impl PartialEq<Self> for Channel {
    /// always update hash and PartialEq::eq to use the same data subset
    fn eq(&self, other: &Self) -> bool {
        let self_period_pips = self.period;
        let other_period_pips = self.period;

        (self.name == other.name)
            && (self_period_pips == other_period_pips)
            && (self.data_type == other.data_type)
            && (self.trend_stat == other.trend_stat)
            && (self.trend_type == other.trend_type)
    }
}

impl Eq for Channel {}

#[cfg(feature = "nds")]
impl From<Channel> for nds2_client_rs::Channel {
    fn from(value: Channel) -> Self {
        let sample_rate = value.rate_hz();
        Self {
            name: value.name,
            channel_type: value.channel_type.into(),
            data_type: value.data_type.into(),
            sample_rate,
            gain: value.gain.unwrap_or(1.0) as f32,
            slope: value.slope.unwrap_or(1.0) as f32,
            offset: value.offset.unwrap_or(0.0) as f32,
            units: value.units.to_string(),
        }
    }
}

impl From<Channel> for nds_cache_rs::buffer::Channel {
    fn from(value: Channel) -> Self {
        nds_cache_rs::buffer::Channel::new(
            value.name,
            nds_cache_rs::buffer::ChannelType::Raw,
            value.data_type.into(),
            value.period,
            value.gain.unwrap_or(1.0) as f32,
            value.slope.unwrap_or(1.0) as f32,
            value.offset.unwrap_or(0.0) as f32,
            value.units.to_string(),
        )
    }
}

/// break down an NDS2 channel name into name, trend type, and trend stat
fn nds_name_to_name_and_trend(name: &str) -> Result<(String, TrendType, TrendStat), DTTError> {
    match name.rsplit_once('.') {
        Some((prefix, trend_info)) => {
            match trend_info.rsplit_once(',') {
                Some((stat, trend)) => {
                    Ok((prefix.to_string(), trend.try_into()?, stat.try_into()?))
                }
                None => Ok((name.to_string(), TrendType::Raw, TrendStat::Raw)), // Err(DTTError::BadTrendSpecifier(trend_info.to_string(),not all channels
                                                                                //     "No comma found.\n\tMust be in the form <trend_stat>,<trend_type>".to_string(),
                                                                                //     name.to_string()
                                                                                // ))
            }
        }
        None => Ok((name.to_string(), TrendType::Raw, TrendStat::Raw)),
    }
}

impl TryFrom<nds_cache_rs::buffer::Channel> for Channel {
    type Error = DTTError;

    fn try_from(value: nds_cache_rs::buffer::Channel) -> Result<Self, Self::Error> {
        let (name, trend_type, trend_stat) = nds_name_to_name_and_trend(value.name())?;

        // NDS channels without units are picking up "undef" somewhere
        // also, testpoints get "none"
        let units = if value.units() == "undef" {
            Unit::default()
        } else if value.units() == "none" {
            Unit::default()
        } else if value.units() == "" {
            Unit::default()
        } else {
            value.units().to_owned().into()
        };

        Ok(Self {
            name,
            data_type: value.data_type().into(),
            channel_type: value.channel_type().into(),
            period: value.period(),
            gain: Some(value.gain() as f64),
            offset: Some(value.offset() as f64),
            slope: Some(value.slope() as f64),
            units,
            trend_type,
            trend_stat,
            ..Default::default()
        })
    }
}

impl TryFrom<&crate::data_source::buffer::Buffer> for Channel {
    type Error = DTTError;

    fn try_from(value: &crate::data_source::buffer::Buffer) -> Result<Self, Self::Error> {
        (&value.cache_buffer).try_into()
    }
}

impl TryFrom<&Buffer> for Channel {
    type Error = DTTError;

    fn try_from(buffer: &Buffer) -> Result<Self, Self::Error> {
        buffer.channel().clone().try_into()
    }
}

impl From<ChannelSettings> for Channel {
    fn from(value: ChannelSettings) -> Self {
        value.channel
    }
}

impl From<(&Channel, TrendType)> for Channel {
    fn from(value: (&Channel, TrendType)) -> Self {
        let mut newchan = value.0.clone();
        newchan.trend_type = value.1;
        newchan
    }
}

impl PartialOrd for Channel {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.name < other.name {
            Some(Ordering::Less)
        } else if self.name > other.name {
            Some(Ordering::Greater)
        } else if self.period > other.period {
            Some(Ordering::Less)
        } else if self.period < other.period {
            Some(Ordering::Greater)
        } else if self.data_type == other.data_type {
            Some(Ordering::Equal)
        } else {
            None
        }
    }
}

impl Ord for Channel {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl Channel {
    #[new]
    pub fn new(name: String, data_type: NDSDataType, period: PipDuration) -> Self {
        Channel {
            name,
            data_type,
            period,
            ..Default::default()
        }
    }

    ///
    #[getter]
    pub fn online(&self) -> bool {
        self.channel_type == ChannelType::Online || self.channel_type == ChannelType::TestPoint
    }

    #[getter]
    pub fn testpoint(&self) -> bool {
        self.channel_type == ChannelType::TestPoint
    }

    #[getter]
    pub fn rate_hz(&self) -> f64 {
        self.period.period_to_freq_hz()
    }
}
