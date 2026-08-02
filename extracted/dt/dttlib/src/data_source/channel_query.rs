use crate::params::channel_params::{ChannelType, NDSDataType};
use ligo_hires_gps_time::PipInstant;

use nds_cache_rs::Predicate;

use dtt_macros::builder_lite;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

/// Constraints on a channel query
/// to a data source
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(frozen))]
#[derive(Debug, Clone, Default)]
#[builder_lite]
pub struct ChannelQuery {
    pattern: Option<String>,
    channel_types: Vec<ChannelType>,
    data_types: Vec<NDSDataType>,
    min_sample_rate: Option<f64>,
    max_sample_rate: Option<f64>,
    gps_start_pip: Option<PipInstant>,
    gps_end_pip: Option<PipInstant>,
}

impl From<ChannelQuery> for Predicate {
    fn from(value: ChannelQuery) -> Self {
        let channel_types = value.channel_types.into_iter().map(|x| x.into()).collect();
        let data_types = value.data_types.into_iter().map(|x| x.into()).collect();

        Self {
            pattern: value.pattern.unwrap_or(String::from("*")),
            channel_types,
            data_types,
            min_sample_rate: value.min_sample_rate.unwrap_or(0.0),
            max_sample_rate: value.max_sample_rate.unwrap_or(f64::MAX),
            gps_start: value
                .gps_start_pip
                .map(|x| x.to_gpst_sec() as u64)
                .unwrap_or(0),
            gps_end: value
                .gps_end_pip
                .map(|x| { x.to_gpst_sec() } as u64)
                .unwrap_or(1999999999),
        }
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg(any(feature = "python", feature = "python-pipe"))]
#[pymethods]
impl ChannelQuery {
    #[new]
    #[pyo3(signature = (pattern=None, channel_types=None, data_types=None,
        min_sample_rate=None, max_sample_rate=None, gps_start=None, gps_end=None))]
    fn new(
        pattern: Option<String>,
        channel_types: Option<Vec<ChannelType>>,
        data_types: Option<Vec<NDSDataType>>,
        min_sample_rate: Option<f64>,
        max_sample_rate: Option<f64>,
        gps_start: Option<u64>,
        gps_end: Option<u64>,
    ) -> Self {
        let channel_types = channel_types.unwrap_or(vec![]);
        let data_types = data_types.unwrap_or(vec![]);

        Self {
            pattern,
            channel_types,
            data_types,
            min_sample_rate,
            max_sample_rate,
            gps_start_pip: gps_start.map(|x| PipInstant::from_gpst_sec(x as i64)),
            gps_end_pip: gps_end.map(|x| PipInstant::from_gpst_sec(x as i64)),
        }
    }
}
