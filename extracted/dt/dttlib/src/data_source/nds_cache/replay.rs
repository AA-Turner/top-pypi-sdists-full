use ligo_hires_gps_time::PipInstant;

#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass_complex_enum;

#[cfg_attr(feature = "all", gen_stub_pyclass_complex_enum)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(frozen))]
#[derive(Clone, Debug)]
pub enum Replay {
    NoReplay(),
    Id(String),
    TimeBased(PipInstant, PipInstant),
}

impl From<Replay> for nds_cache_rs::Replay {
    fn from(value: Replay) -> Self {
        match value {
            Replay::NoReplay() => nds_cache_rs::Replay::None,
            Replay::Id(id) => nds_cache_rs::Replay::Id(id),
            Replay::TimeBased(s, e) => nds_cache_rs::Replay::TimeBased(s, e),
        }
    }
}
