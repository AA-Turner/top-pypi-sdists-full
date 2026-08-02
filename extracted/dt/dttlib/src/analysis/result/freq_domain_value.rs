#[cfg(feature = "all")]
use crate::analysis::types::frequency_domain_array::PyFreqDomainArray;
use crate::params::channel_params::Unit;
use pipelines::{PipeData, PipeDataPrimitive};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{Bound, FromPyObject, IntoPyObject, IntoPyObjectExt, PyAny, PyErr, PyResult, Python};
#[cfg(feature = "all")]
use pyo3_stub_gen::{PyStubType, TypeInfo};
use std::fmt::{Display, Formatter};
use std::ops::{Add, Mul};
use std::sync::Arc;

use crate::analysis::types::frequency_domain_array::FreqDomainArray;
use crate::errors::DTTError;
use crate::{Accumulation, AccumulationStats, AnalysisId};
use std::hash::{Hash, Hasher};

/// Frequency domain results
#[derive(Clone, Debug)]
pub enum FreqDomainValue<T> {
    FixedStepArray(Arc<FreqDomainArray<T>>),
}

impl<T> PartialEq<Self> for FreqDomainValue<T> {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (FreqDomainValue::FixedStepArray(f), FreqDomainValue::FixedStepArray(g)) => f == g,
        }
    }
}

impl<T> From<Arc<FreqDomainArray<T>>> for FreqDomainValue<T> {
    fn from(value: Arc<FreqDomainArray<T>>) -> Self {
        FreqDomainValue::FixedStepArray(value)
    }
}

impl<T> From<FreqDomainArray<T>> for FreqDomainValue<T> {
    fn from(value: FreqDomainArray<T>) -> Self {
        Arc::new(value).into()
    }
}

impl<T> Eq for FreqDomainValue<T> {}

impl<T> Hash for FreqDomainValue<T> {
    /// don't hash anything.  always overwrite an old freq domain value with a new one.
    fn hash<H: Hasher>(&self, _state: &mut H) {}
}

impl<T> Display for FreqDomainValue<T>
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
impl<T> Add<&FreqDomainValue<T>> for FreqDomainValue<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<FreqDomainValue<T>, DTTError>;

    fn add(self, rhs: &FreqDomainValue<T>) -> Self::Output {
        match (self, rhs) {
            (FreqDomainValue::FixedStepArray(a), FreqDomainValue::FixedStepArray(b)) => {
                Ok((a.as_ref() + b.clone())?.into())
            }
        }
    }
}

impl<T> Mul<f64> for FreqDomainValue<T>
where
    T: Copy + Mul<f64, Output = T>,
{
    type Output = FreqDomainValue<T>;

    fn mul(self, rhs: f64) -> Self::Output {
        match self {
            FreqDomainValue::FixedStepArray(a) => (a.as_ref().clone() * rhs).into(),
        }
    }
}

impl<T> PipeData for FreqDomainValue<T> where T: PipeDataPrimitive {}

impl<T: Clone> Accumulation for FreqDomainValue<T> {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self {
        match self {
            FreqDomainValue::FixedStepArray(t) => {
                FreqDomainValue::FixedStepArray(Arc::new(t.set_accumulation_stats(stats)))
            }
        }
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        match self {
            FreqDomainValue::FixedStepArray(t) => t.get_accumulation_stats(),
        }
    }
}

impl<T> FreqDomainValue<T> {
    pub fn len(&self) -> usize {
        match self {
            Self::FixedStepArray(a) => a.len(),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    pub fn id(&self) -> AnalysisId {
        match self {
            Self::FixedStepArray(a) => a.id.clone(),
        }
    }

    pub fn unit(&self) -> Unit {
        match self {
            Self::FixedStepArray(a) => a.unit.clone(),
        }
    }
}

/// # Python interface
#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> FromPyObject<'py> for FreqDomainValue<T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        FreqDomainArray::<T>::extract_bound(ob).map(|x| x.into())
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeDataPrimitive> IntoPyObject<'py> for FreqDomainValue<T> {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            FreqDomainValue::FixedStepArray(a) => Ok(a.as_ref().clone().into_bound_py_any(py)?),
        }
    }
}

#[cfg(feature = "all")]
impl<T: PipeData> PyStubType for FreqDomainValue<T> {
    fn type_output() -> TypeInfo {
        PyFreqDomainArray::type_output()
    }
}
