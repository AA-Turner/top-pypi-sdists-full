use super::FixedStepArray;
#[cfg(feature = "all")]
use crate::analysis::types::time_domain_array::PyTimeDomainArray;
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::params::channel_params::Unit;
use crate::{Accumulation, AccumulationStats, AnalysisId};
use pipelines::{PipeData, PipeDataPrimitive};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{Bound, FromPyObject, IntoPyObject, IntoPyObjectExt, PyAny, PyErr, PyResult, Python};
#[cfg(feature = "all")]
use pyo3_stub_gen::{PyStubType, TypeInfo};
use std::fmt::{Display, Formatter};
use std::hash::{Hash, Hasher};
use std::ops::{Add, Mul};
use std::sync::Arc;

/// Time domain results
#[derive(Clone, Debug)]
pub enum TimeDomainValue<T> {
    FixedStepArray(Arc<TimeDomainArray<T>>),
}

impl<T> From<Arc<TimeDomainArray<T>>> for TimeDomainValue<T> {
    fn from(arc: Arc<TimeDomainArray<T>>) -> Self {
        FixedStepArray(arc)
    }
}

impl<T> From<TimeDomainArray<T>> for TimeDomainValue<T> {
    fn from(value: TimeDomainArray<T>) -> Self {
        Arc::new(value).into()
    }
}

impl<T> PartialEq<Self> for TimeDomainValue<T> {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (FixedStepArray(f), FixedStepArray(g)) => f == g,
        }
    }
}

impl<T> Eq for TimeDomainValue<T> {}

impl<T> Hash for TimeDomainValue<T> {
    /// hash the start time so different time slices are stored separately
    fn hash<H: Hasher>(&self, state: &mut H) {
        match self {
            FixedStepArray(t) => t.start_gps_pip.hash(state),
        }
    }
}

impl<T> Display for TimeDomainValue<T>
where
    T: Display,
{
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::FixedStepArray(t) => t.fmt(f),
        }
    }
}

/// needed for Average pipeline
impl<T> Add<&TimeDomainValue<T>> for TimeDomainValue<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<TimeDomainValue<T>, DTTError>;

    fn add(self, rhs: &TimeDomainValue<T>) -> Self::Output {
        match (self, rhs) {
            (FixedStepArray(a), FixedStepArray(b)) => Ok((a.as_ref() + b.clone())?.into()),
        }
    }
}

impl<T> Mul<f64> for TimeDomainValue<T>
where
    T: Copy + Mul<f64, Output = T>,
{
    type Output = TimeDomainValue<T>;

    fn mul(self, rhs: f64) -> Self::Output {
        match self {
            FixedStepArray(a) => (a.as_ref().clone() * rhs).into(),
        }
    }
}

impl<T> PipeData for TimeDomainValue<T> where T: PipeDataPrimitive {}

impl<T: Clone> Accumulation for TimeDomainValue<T> {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self {
        match self {
            FixedStepArray(t) => FixedStepArray(Arc::new(t.set_accumulation_stats(stats))),
        }
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        match self {
            FixedStepArray(t) => t.get_accumulation_stats(),
        }
    }
}

impl<T> TimeDomainValue<T> {
    pub fn len(&self) -> usize {
        match self {
            FixedStepArray(a) => a.len(),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    pub fn id(&self) -> AnalysisId {
        match self {
            FixedStepArray(a) => a.id.clone(),
        }
    }

    pub fn unit(&self) -> Unit {
        match self {
            FixedStepArray(a) => a.unit.clone(),
        }
    }
}

/// # Python interface
#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> FromPyObject<'py> for TimeDomainValue<T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        TimeDomainArray::<T>::extract_bound(ob).map(|x| x.into())
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeDataPrimitive> IntoPyObject<'py> for TimeDomainValue<T> {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            FixedStepArray(a) => Ok(a.as_ref().clone().into_bound_py_any(py)?),
        }
    }
}

#[cfg(feature = "all")]
impl<T: PipeData> PyStubType for TimeDomainValue<T> {
    fn type_output() -> TypeInfo {
        PyTimeDomainArray::type_output()
    }
}
