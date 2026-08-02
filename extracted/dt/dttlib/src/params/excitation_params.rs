use super::channel_params::{Activate, Channel, ChannelSettings};
#[cfg(feature = "python")]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass;

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ExcitationSettings {
    pub channel: ChannelSettings,
    pub read_back_channel: Option<ChannelSettings>,
}

impl ExcitationSettings {
    /// Return the read back channel
    pub fn get_read_back_channel(&self) -> ChannelSettings {
        match &self.read_back_channel {
            None => self.channel.clone(),
            Some(c) => c.clone(),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ExcitationSettingsParams {
    pub active: bool,
    pub excitation: ExcitationSettings,
}

impl Activate for ExcitationSettingsParams {
    fn is_active(&self) -> bool {
        self.active
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct Excitation {
    pub channel: Channel,
    pub read_back_channel: Option<Channel>,
}

impl Excitation {
    pub fn get_read_back_channel(&self) -> Channel {
        match &self.read_back_channel {
            None => self.channel.clone(),
            Some(c) => c.clone(),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python"), pyclass(get_all))]
#[derive(Clone, Debug)]
pub struct ExcitationParams {
    pub active: bool,
    pub excitation: Excitation,
}

impl Activate for ExcitationParams {
    fn is_active(&self) -> bool {
        self.active
    }
}

impl From<ExcitationSettings> for Excitation {
    fn from(excitation: ExcitationSettings) -> Self {
        Excitation {
            channel: excitation.channel.into(),
            read_back_channel: excitation.read_back_channel.map(|c| c.into()),
        }
    }
}

impl From<Excitation> for ExcitationSettings {
    fn from(value: Excitation) -> Self {
        ExcitationSettings {
            channel: value.channel.into(),
            read_back_channel: value.read_back_channel.map(|c| c.into()),
        }
    }
}

impl From<ExcitationSettingsParams> for ExcitationParams {
    fn from(value: ExcitationSettingsParams) -> Self {
        ExcitationParams {
            active: value.active,
            excitation: value.excitation.into(),
        }
    }
}

impl From<ExcitationParams> for ExcitationSettingsParams {
    fn from(value: ExcitationParams) -> Self {
        ExcitationSettingsParams {
            active: value.active,
            excitation: value.excitation.into(),
        }
    }
}
