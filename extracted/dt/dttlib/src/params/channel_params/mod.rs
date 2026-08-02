pub mod channel;
pub(crate) mod channel_id;
pub(crate) mod channel_name;
mod channel_settings;
mod channel_type;
pub(crate) mod decimation_parameters;
pub mod nds_data_type;
pub mod unit;

#[cfg(feature = "python")]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;
use std::vec::IntoIter;

pub use channel::Channel;
pub use channel_id::{ChannelHeader, ChannelId, TrendStat, TrendType};
pub use channel_name::ChannelName;
pub use channel_type::ChannelType;
pub use nds_data_type::NDSDataType;
pub use unit::Unit;

pub(crate) use channel_settings::ChannelSettings;

pub trait Activate {
    fn is_active(&self) -> bool;
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all))]
#[derive(Clone, Debug)]
pub(crate) struct ChannelSettingsParams {
    pub active: bool,
    pub channel: ChannelSettings,
}

impl Activate for ChannelSettingsParams {
    fn is_active(&self) -> bool {
        self.active
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ChannelParams {
    pub active: bool,
    pub channel: Channel,
}

impl Activate for ChannelParams {
    fn is_active(&self) -> bool {
        self.active
    }
}

impl From<ChannelParams> for ChannelSettingsParams {
    fn from(c: ChannelParams) -> Self {
        Self {
            active: c.active,
            channel: c.channel.into(),
        }
    }
}

pub trait ActiveList<T> {
    fn active_iter(&self) -> IntoIter<&T>;
}

impl<T> ActiveList<T> for Vec<T>
where
    T: Activate,
{
    fn active_iter(&self) -> IntoIter<&T> {
        self.into_iter()
            .filter(|s| (*s).is_active())
            .collect::<Vec<&T>>()
            .into_iter()
    }
}
