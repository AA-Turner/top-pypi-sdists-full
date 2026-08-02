use crate::params::channel_params::{Channel, ChannelHeader};
use crate::params::channel_params::{ChannelId, ChannelSettings};
#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::new;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::fmt::Display;

/// Provides enough info to query a channel from an NDS server by name.
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, get_all, hash, eq, str, ord)
)]
#[derive(Clone, Debug, Hash, Eq, PartialEq, Default, Ord, PartialOrd)]
pub struct ChannelName {
    pub name: String,
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl ChannelName {
    #[new]
    pub fn new(name: String) -> Self {
        Self { name }
    }
}

impl<T> From<T> for ChannelName
where
    T: Into<String>,
{
    fn from(s: T) -> Self {
        Self::new(s.into())
    }
}

impl From<ChannelSettings> for ChannelName {
    fn from(value: ChannelSettings) -> Self {
        Self {
            name: value.channel.name,
        }
    }
}

impl From<Channel> for ChannelName {
    fn from(value: Channel) -> Self {
        Self { name: value.name }
    }
}

impl From<ChannelId> for ChannelName {
    fn from(value: ChannelId) -> Self {
        Self { name: value.name }
    }
}

impl From<ChannelHeader> for ChannelName {
    fn from(value: ChannelHeader) -> Self {
        Self { name: value.name }
    }
}

impl Display for ChannelName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "{}", self.name)
    }
}
