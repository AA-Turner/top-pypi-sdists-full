#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::analysis::types::frequency_domain_array::PyFreqDomainArray;
#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::analysis::types::time_domain_array::PyTimeDomainArray;
use pipelines::PipeData;
use pipelines::{PipelineSubscriber, complex::c128};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{
    Bound, FromPyObject, IntoPyObject, IntoPyObjectExt, PyAny, PyErr, PyResult, Python,
    exceptions::PyTypeError,
    types::{PyAnyMethods, PyTypeMethods},
};
#[cfg(feature = "all")]
use pyo3_stub_gen::{PyStubType, TypeInfo};
use std::sync::Arc;
use std::{fmt::Display, ops::Add};

use crate::AnalysisResult::{
    FreqDomainValueComplex, FreqDomainValueReal, TimeDomainValueComplex, TimeDomainValueInt8,
    TimeDomainValueInt16, TimeDomainValueInt32, TimeDomainValueInt64, TimeDomainValueReal,
    TimeDomainValueUInt8, TimeDomainValueUInt16, TimeDomainValueUInt32, TimeDomainValueUInt64,
};
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::errors::DTTError;
use crate::params::channel_params::Unit;
use crate::{Accumulation, AccumulationStats, FreqDomainValue, TimeDomainValue};
use crate::{
    AnalysisId,
    analysis::{result::ResultsSender, types::frequency_domain_array::FreqDomainArray},
    run_context::RunContext,
};

/// A generic results value
/// Could be used in custom pipelines for example
#[derive(Clone, Hash, Debug, PartialEq, Eq)]
// #[cfg_attr(feature = "all", gen_stub_pyclass_complex_enum)]
// #[cfg_attr(any(feature = "python-pipe", feature = "python"), pyclass(frozen, eq, str))]
pub enum AnalysisResult {
    FreqDomainValueReal(FreqDomainValue<f64>),
    FreqDomainValueComplex(FreqDomainValue<c128>),
    TimeDomainValueReal(TimeDomainValue<f64>),
    TimeDomainValueComplex(TimeDomainValue<c128>),

    TimeDomainValueInt64(TimeDomainValue<i64>),
    TimeDomainValueInt32(TimeDomainValue<i32>),
    TimeDomainValueInt16(TimeDomainValue<i16>),
    TimeDomainValueInt8(TimeDomainValue<i8>),

    TimeDomainValueUInt64(TimeDomainValue<u64>),
    TimeDomainValueUInt32(TimeDomainValue<u32>),
    TimeDomainValueUInt16(TimeDomainValue<u16>),
    TimeDomainValueUInt8(TimeDomainValue<u8>),
}

impl From<FreqDomainValue<f64>> for AnalysisResult {
    fn from(value: FreqDomainValue<f64>) -> Self {
        FreqDomainValueReal(value)
    }
}

impl From<FreqDomainValue<c128>> for AnalysisResult {
    fn from(value: FreqDomainValue<c128>) -> Self {
        FreqDomainValueComplex(value)
    }
}

impl From<TimeDomainValue<f64>> for AnalysisResult {
    fn from(value: TimeDomainValue<f64>) -> Self {
        TimeDomainValueReal(value)
    }
}

impl From<TimeDomainValue<c128>> for AnalysisResult {
    fn from(value: TimeDomainValue<c128>) -> Self {
        TimeDomainValueComplex(value)
    }
}

impl From<TimeDomainValue<i64>> for AnalysisResult {
    fn from(value: TimeDomainValue<i64>) -> Self {
        TimeDomainValueInt64(value)
    }
}

impl From<TimeDomainValue<i32>> for AnalysisResult {
    fn from(value: TimeDomainValue<i32>) -> Self {
        TimeDomainValueInt32(value)
    }
}

impl From<TimeDomainValue<i16>> for AnalysisResult {
    fn from(value: TimeDomainValue<i16>) -> Self {
        TimeDomainValueInt16(value)
    }
}

impl From<TimeDomainValue<i8>> for AnalysisResult {
    fn from(value: TimeDomainValue<i8>) -> Self {
        TimeDomainValueInt8(value)
    }
}

impl From<TimeDomainValue<u64>> for AnalysisResult {
    fn from(value: TimeDomainValue<u64>) -> Self {
        TimeDomainValueUInt64(value)
    }
}

impl From<TimeDomainValue<u32>> for AnalysisResult {
    fn from(value: TimeDomainValue<u32>) -> Self {
        TimeDomainValueUInt32(value)
    }
}

impl From<TimeDomainValue<u16>> for AnalysisResult {
    fn from(value: TimeDomainValue<u16>) -> Self {
        TimeDomainValueUInt16(value)
    }
}

impl From<TimeDomainValue<u8>> for AnalysisResult {
    fn from(value: TimeDomainValue<u8>) -> Self {
        TimeDomainValueUInt8(value)
    }
}

impl<T> From<TimeDomainArray<T>> for AnalysisResult
where
    TimeDomainArray<T>: Into<TimeDomainValue<T>>,
    TimeDomainValue<T>: Into<AnalysisResult>,
{
    fn from(value: TimeDomainArray<T>) -> Self {
        let v: TimeDomainValue<T> = value.into();
        v.into()
    }
}

impl<T> From<FreqDomainArray<T>> for AnalysisResult
where
    FreqDomainArray<T>: Into<FreqDomainValue<T>>,
    FreqDomainValue<T>: Into<AnalysisResult>,
{
    fn from(value: FreqDomainArray<T>) -> Self {
        let v: FreqDomainValue<T> = value.into();
        v.into()
    }
}

impl<T> From<Arc<TimeDomainArray<T>>> for AnalysisResult
where
    Arc<TimeDomainArray<T>>: Into<TimeDomainValue<T>>,
    TimeDomainValue<T>: Into<AnalysisResult>,
{
    fn from(value: Arc<TimeDomainArray<T>>) -> Self {
        let v: TimeDomainValue<T> = value.into();
        v.into()
    }
}

impl<T> From<Arc<FreqDomainArray<T>>> for AnalysisResult
where
    Arc<FreqDomainArray<T>>: Into<FreqDomainValue<T>>,
    FreqDomainValue<T>: Into<AnalysisResult>,
{
    fn from(value: Arc<FreqDomainArray<T>>) -> Self {
        let v: FreqDomainValue<T> = value.into();
        v.into()
    }
}

/// Make linear
impl Add<Arc<AnalysisResult>> for AnalysisResult {
    type Output = Result<Self, DTTError>;

    fn add(self, rhs: Arc<AnalysisResult>) -> Self::Output {
        match (self, rhs.as_ref()) {
            (TimeDomainValueReal(a), TimeDomainValueReal(b)) => Ok((a + b)?.into()),
            (TimeDomainValueComplex(a), TimeDomainValueComplex(b)) => Ok((a + b)?.into()),
            (FreqDomainValueComplex(a), FreqDomainValueComplex(b)) => Ok((a + b)?.into()),
            (FreqDomainValueReal(a), FreqDomainValueReal(b)) => Ok((a + b)?.into()),
            _ => Err(DTTError::AnalysisPipelineError(
                "Mismatched types in Results Value addition".to_string(),
            )),
        }
    }
}

impl PipeData for AnalysisResult {}

impl Accumulation for AnalysisResult {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self {
        match self {
            TimeDomainValueReal(t) => TimeDomainValueReal(t.set_accumulation_stats(stats)),
            TimeDomainValueComplex(t) => TimeDomainValueComplex(t.set_accumulation_stats(stats)),
            FreqDomainValueComplex(f) => FreqDomainValueComplex(f.set_accumulation_stats(stats)),
            FreqDomainValueReal(f) => FreqDomainValueReal(f.set_accumulation_stats(stats)),

            TimeDomainValueInt64(f) => TimeDomainValueInt64(f.set_accumulation_stats(stats)),
            TimeDomainValueInt32(f) => TimeDomainValueInt32(f.set_accumulation_stats(stats)),
            TimeDomainValueInt16(f) => TimeDomainValueInt16(f.set_accumulation_stats(stats)),
            TimeDomainValueInt8(f) => TimeDomainValueInt8(f.set_accumulation_stats(stats)),

            TimeDomainValueUInt64(f) => TimeDomainValueUInt64(f.set_accumulation_stats(stats)),
            TimeDomainValueUInt32(f) => TimeDomainValueUInt32(f.set_accumulation_stats(stats)),
            TimeDomainValueUInt16(f) => TimeDomainValueUInt16(f.set_accumulation_stats(stats)),
            TimeDomainValueUInt8(f) => TimeDomainValueUInt8(f.set_accumulation_stats(stats)),
        }
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        match self {
            TimeDomainValueReal(t) => t.get_accumulation_stats(),
            TimeDomainValueComplex(t) => t.get_accumulation_stats(),
            FreqDomainValueComplex(f) => f.get_accumulation_stats(),
            FreqDomainValueReal(f) => f.get_accumulation_stats(),

            TimeDomainValueInt64(t) => t.get_accumulation_stats(),
            TimeDomainValueInt32(t) => t.get_accumulation_stats(),
            TimeDomainValueInt16(t) => t.get_accumulation_stats(),
            TimeDomainValueInt8(t) => t.get_accumulation_stats(),

            TimeDomainValueUInt64(t) => t.get_accumulation_stats(),
            TimeDomainValueUInt32(t) => t.get_accumulation_stats(),
            TimeDomainValueUInt16(t) => t.get_accumulation_stats(),
            TimeDomainValueUInt8(t) => t.get_accumulation_stats(),
        }
    }
}

impl AnalysisResult {
    pub fn len(&self) -> usize {
        match self {
            TimeDomainValueReal(t) => t.len(),
            TimeDomainValueComplex(t) => t.len(),
            FreqDomainValueComplex(f) => f.len(),
            FreqDomainValueReal(f) => f.len(),

            TimeDomainValueInt64(t) => t.len(),
            TimeDomainValueInt32(t) => t.len(),
            TimeDomainValueInt16(t) => t.len(),
            TimeDomainValueInt8(t) => t.len(),

            TimeDomainValueUInt64(t) => t.len(),
            TimeDomainValueUInt32(t) => t.len(),
            TimeDomainValueUInt16(t) => t.len(),
            TimeDomainValueUInt8(t) => t.len(),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    pub fn unit(&self) -> Unit {
        match self {
            TimeDomainValueReal(t) => t.unit(),
            TimeDomainValueComplex(t) => t.unit(),
            FreqDomainValueComplex(f) => f.unit(),
            FreqDomainValueReal(f) => f.unit(),

            TimeDomainValueInt64(t) => t.unit(),
            TimeDomainValueInt32(t) => t.unit(),
            TimeDomainValueInt16(t) => t.unit(),
            TimeDomainValueInt8(t) => t.unit(),

            TimeDomainValueUInt64(t) => t.unit(),
            TimeDomainValueUInt32(t) => t.unit(),
            TimeDomainValueUInt16(t) => t.unit(),
            TimeDomainValueUInt8(t) => t.unit(),
        }
    }
}

// #[cfg_attr(feature = "all", gen_stub_pymethods)]
// #[cfg_attr(any(feature = "python-pipe", feature = "python"), pymethods)]
impl AnalysisResult {
    pub fn __len__(&self) -> usize {
        self.len()
    }

    pub fn id(&self) -> AnalysisId {
        match self {
            TimeDomainValueReal(t) => t.id(),
            TimeDomainValueComplex(t) => t.id(),
            FreqDomainValueComplex(f) => f.id(),
            FreqDomainValueReal(f) => f.id(),

            TimeDomainValueInt64(t) => t.id(),
            TimeDomainValueInt32(t) => t.id(),
            TimeDomainValueInt16(t) => t.id(),
            TimeDomainValueInt8(t) => t.id(),

            TimeDomainValueUInt64(t) => t.id(),
            TimeDomainValueUInt32(t) => t.id(),
            TimeDomainValueUInt16(t) => t.id(),
            TimeDomainValueUInt8(t) => t.id(),
        }
    }

    // /// This should be used in python only to  get the pyload of the result
    // pub fn get(&self, index: usize) -> PyAny {
    //
    //         match self {
    //             TimeDomainValueReal(t) => t.clone().into_bound_py_any()?.unbind(),
    //             TimeDomainValueComplex(t) => t.into(),
    //             FreqDomainValueComplex(f) => f.into(),
    //             FreqDomainValueReal(f) => f.into(),
    //
    //             TimeDomainValueInt64(t) => t.into(),
    //             TimeDomainValueInt32(t) => t.into(),
    //             TimeDomainValueInt16(t) => t.into(),
    //             TimeDomainValueInt8(t) => t.into(),
    //
    //             TimeDomainValueUInt64(t) => t.into(),
    //             TimeDomainValueUInt32(t) => t.into(),
    //             TimeDomainValueUInt16(t) => t.into(),
    //             TimeDomainValueUInt8(t) => t.into(),
    //         }
    // }
}

impl Display for AnalysisResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FreqDomainValueReal(v) => write!(f, "{} [f64]", v),
            FreqDomainValueComplex(v) => write!(f, "{} [c128]", v),
            TimeDomainValueReal(v) => write!(f, "{} [f64]", v),
            TimeDomainValueComplex(v) => write!(f, "{} [c128]", v),

            TimeDomainValueInt64(v) => write!(f, "{} [i64]", v),
            TimeDomainValueInt32(v) => write!(f, "{} [i32]", v),
            TimeDomainValueInt16(v) => write!(f, "{} [i16]", v),
            TimeDomainValueInt8(v) => write!(f, "{} [i8]", v),

            TimeDomainValueUInt64(v) => write!(f, "{} [u64]", v),
            TimeDomainValueUInt32(v) => write!(f, "{} [u32]", v),
            TimeDomainValueUInt16(v) => write!(f, "{} [u16]", v),
            TimeDomainValueUInt8(v) => write!(f, "{} [u8]", v),
        }
    }
}

/// send an Arc<data> transformed into an analysis result
/// take from a pipeline output
pub(crate) async fn analysis_result_wrapper<C>(
    _rc: &Box<RunContext>,
    input: &PipelineSubscriber<C>,
    output: ResultsSender,
) -> Result<(), DTTError>
where
    C: PipeData,
    Arc<C>: Into<AnalysisResult>,
{
    let mut inp_rx = input.subscribe().await?;
    tokio::spawn(async move {
        log::debug!("starting analysis_result_wrapper");
        'main: loop {
            let result = match inp_rx.recv().await {
                Some(r) => r,
                None => break 'main,
            };

            if let Err(_) = output.send(result.value.into()).await {
                break 'main;
            }
        }
        log::debug!("ending analysis_result_wrapper");
    });
    Ok(())
}

/// Send an already prepared analasys result from a pipeline
pub(crate) async fn analysis_result_sender(
    _rc: &Box<RunContext>,
    input: &PipelineSubscriber<AnalysisResult>,
    output: ResultsSender,
) -> Result<(), DTTError> {
    let mut inp_rx = input.subscribe().await?;
    tokio::spawn(async move {
        'main: loop {
            let result = match inp_rx.recv().await {
                Some(r) => r,
                None => break 'main,
            };

            // clone is OK here because underyling value must be an Arc<>
            if let Err(_) = output.send(result.value.as_ref().clone()).await {
                break 'main;
            }
        }
    });
    Ok(())
}

/// Sub parts of a ResultsValue implement this to create a ResultsValue object from the corresponding python object
/// Used to handle return values from user defined functions.
#[cfg(any(feature = "python-pipe", feature = "python"))]
pub(crate) trait PyIntoAnalysisResult<'py> {
    fn extract_result_value(ob: &Bound<'py, PyAny>) -> PyResult<AnalysisResult>;
}

// # python

/// # Python interface
/// Any python type that needs to be returned as an analysis result from
/// a custom calculation has to be handled here
#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py> FromPyObject<'py> for AnalysisResult {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        let type_name_res =
            Python::with_gil(|py| ob.get_type().name()?.unbind().extract::<String>(py))?;

        if type_name_res == "FreqDomainArray" {
            PyFreqDomainArray::extract_result_value(ob)
        } else if type_name_res == "TimeDomainArray" {
            PyTimeDomainArray::extract_result_value(ob)
        } else {
            Err(PyErr::new::<PyTypeError, _>(format!(
                "Could not convert type '{}' to AnalysisResult",
                type_name_res
            )))
        }
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py> IntoPyObject<'py> for AnalysisResult {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            FreqDomainValueReal(v) => Ok(v.into_bound_py_any(py)?),
            FreqDomainValueComplex(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueReal(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueComplex(v) => Ok(v.into_bound_py_any(py)?),

            TimeDomainValueInt64(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueInt32(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueInt16(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueInt8(v) => Ok(v.into_bound_py_any(py)?),

            TimeDomainValueUInt64(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueUInt32(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueUInt16(v) => Ok(v.into_bound_py_any(py)?),
            TimeDomainValueUInt8(v) => Ok(v.into_bound_py_any(py)?),
        }
    }
}

#[cfg(feature = "all")]
impl PyStubType for AnalysisResult {
    fn type_output() -> TypeInfo {
        TypeInfo::any()
    }
}
