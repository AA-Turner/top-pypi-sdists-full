#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::AnalysisResult;
#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::analysis::result::analysis_result::PyIntoAnalysisResult;
use crate::analysis_id;
use crate::errors::DTTError;
use ligo_hires_gps_time::PipInstant;
use num::complex::ComplexFloat;
use num::{Complex, Float};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use numpy::PyArray;
use pipelines::complex::c128;
use pipelines::{PipeData, PipeDataPrimitive};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{
    Bound, FromPyObject, IntoPyObject, Py, PyAny, PyErr, PyResult, Python, pyclass, pymethods,
    types::PyAnyMethods,
};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::fmt::Display;
use std::ops::{Add, Mul};
use std::sync::Arc;

use crate::analysis::result::AnalysisId;
use crate::analysis::types::math_traits::{Phase, Sqrt, ToComplex};
use crate::analysis::types::{Accumulation, AccumulationStats, MutableAccumulation};
use crate::params::channel_params::Unit;

/// ## Frequency domain data
#[derive(Clone, Debug)]
pub struct FreqDomainArray<T> {
    pub start_gps_pip: PipInstant,
    pub start_hz: f64,
    pub bucket_width_hz: f64,
    pub data: Vec<T>,
    /// used by accumulated values to describe overlap of
    /// time domain segments
    pub overlap: f64,
    accumulation_stats: AccumulationStats,
    pub id: AnalysisId,
    pub unit: Unit,
}

/// equal in start window only, not value
impl<T> PartialEq<Self> for FreqDomainArray<T> {
    fn eq(&self, other: &Self) -> bool {
        self.start_hz == other.start_hz && self.bucket_width_hz == other.bucket_width_hz
    }
}

impl<T> Eq for FreqDomainArray<T> {}

impl<T> Display for FreqDomainArray<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "[x=f y={} s={} w={} l={}]",
            self.id,
            self.start_hz,
            self.bucket_width_hz,
            self.len()
        )
    }
}

impl<T: PipeDataPrimitive> PipeData for FreqDomainArray<T> {}

impl<T: PipeData> FreqDomainArray<T> {
    pub fn new(
        id: AnalysisId,
        unit: Unit,
        start_gps_pip: PipInstant,
        mut start_hz: f64,
        bucket_width_hz: f64,
        overlap: f64,
        data: Vec<T>,
        accumulation_stats: AccumulationStats,
    ) -> Self {
        start_hz = ((start_hz / bucket_width_hz).floor()) * bucket_width_hz;

        Self {
            start_gps_pip,
            start_hz,
            bucket_width_hz,
            data,
            accumulation_stats,
            overlap,
            id,
            unit,
        }
    }

    /// Get the nearest index into data as if start_hz were zero
    /// Useful when dealing with un-trimmed data
    /// Assumes values run from 0Hz to nyquist
    fn raw_index_from_hz_onseside(&self, f_hz: f64) -> usize {
        (f_hz / self.bucket_width_hz).round() as usize
    }

    /// get the index for a frequency assuming the array
    /// is -nyq ... 0 ... +(nyq-1)
    /// The "rotated" arrangement for a complex FFT produced by the FFT pipeline
    fn _raw_index_from_hz_twoside(&self, f_hz: f64, raw_size: usize) -> usize {
        (f_hz / self.bucket_width_hz).round() as usize + raw_size / 2
    }

    /// insert an untrimmed frequency array.
    /// Trim to start_hz and end_hz argument
    /// Assumes first element of the array is zero Hz
    pub fn insert_and_trim_oneside(&mut self, new_data: Vec<T>, end_hz: f64) {
        let end_i = (end_hz / self.bucket_width_hz).ceil() as usize;
        let start_i = self.raw_index_from_hz_onseside(self.start_hz);
        self.data = new_data[start_i..=end_i].to_vec();
    }

    /// insert an untrimmed frequency array.
    /// Frequency array must start at -nyquist, then rise through negatives to zero
    /// at the half-way mark, then rise through positive freqs to the bucket
    /// just below nyquist
    /// This is a "rotated" output of Complex FFT.
    /// zoom_hz is assumed to be shifted to 0 hz,
    /// so start freq is shifted to start - zoom (a negative frequency)
    /// The  array is preserved form [(start - zoom), (zoom - start)] so
    /// that it's always centered on the zoom frequency.
    pub fn insert_and_trim_twoside(&mut self, new_data: Vec<T>, zoom_hz: f64) {
        // start_hz index assuming array is centered on zoom_hz
        let start_i = ((self.start_hz - zoom_hz) / self.bucket_width_hz).floor() as usize
            + new_data.len() / 2;
        let end_i = new_data.len() - start_i;
        self.data = new_data[start_i..=end_i].to_vec();
    }

    /// given an index into data, return the frequency of that value
    pub fn index_to_hz(&self, index: usize) -> f64 {
        self.start_hz + self.bucket_width_hz * index as f64
    }

    /// Create a new array with all the same metadata, but
    /// a different data array.
    pub fn clone_metadata<U>(
        &self,
        id: AnalysisId,
        unit: Unit,
        data: Vec<U>,
    ) -> FreqDomainArray<U> {
        FreqDomainArray {
            start_gps_pip: self.start_gps_pip,
            start_hz: self.start_hz,
            bucket_width_hz: self.bucket_width_hz,
            overlap: self.overlap,
            accumulation_stats: self.accumulation_stats.clone(),
            data,
            id,
            unit,
        }
    }
}

impl<T> FreqDomainArray<T> {
    pub fn len(&self) -> usize {
        self.data.len()
    }
}

impl<T> Mul<f64> for FreqDomainArray<T>
where
    T: Copy + Mul<f64, Output = T>,
{
    type Output = FreqDomainArray<T>;

    fn mul(mut self, rhs: f64) -> Self::Output {
        for i in 0..self.data.len() {
            self.data[i] = self.data[i] * rhs
        }
        self
    }
}

impl<T> Add<Arc<FreqDomainArray<T>>> for FreqDomainArray<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<FreqDomainArray<T>, DTTError>;

    fn add(mut self, rhs: Arc<FreqDomainArray<T>>) -> Self::Output {
        if self.start_hz != rhs.start_hz {
            let msg = format!(
                "Can't add frequency arrays.  Starting frequencies differ: ({}, {})",
                self.start_hz, rhs.start_hz
            );
            return Err(DTTError::CalcError(msg));
        };
        if self.bucket_width_hz != rhs.bucket_width_hz {
            let msg = format!(
                "Can't add frequency arrays with different bandwidths: ({}, {})",
                self.bucket_width_hz, rhs.bucket_width_hz
            );
            return Err(DTTError::CalcError(msg));
        }
        if self.data.len() != rhs.data.len() {
            let msg = format!(
                "Can't add frequency arrays.  Lengths differ: ({}, {})",
                self.data.len(),
                rhs.data.len()
            );
            return Err(DTTError::CalcError(msg));
        }
        for i in 0..self.data.len() {
            self.data[i] = self.data[i] + rhs.data[i]
        }
        Ok(self)
    }
}

impl<T> Add<Arc<FreqDomainArray<T>>> for &FreqDomainArray<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<FreqDomainArray<T>, DTTError>;

    fn add(self, rhs: Arc<FreqDomainArray<T>>) -> Self::Output {
        let sum: FreqDomainArray<T> = self.clone();
        sum + rhs
    }
}

impl<T: Clone> Accumulation for FreqDomainArray<T> {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self {
        let mut n = self.clone();
        n.accumulation_stats = stats;
        n
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        &self.accumulation_stats
    }
}

impl<T: Clone> MutableAccumulation for FreqDomainArray<T> {
    fn set_mut_accumulation_stats(&mut self, stats: AccumulationStats) {
        self.accumulation_stats = stats;
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeDataPrimitive> IntoPyObject<'py> for FreqDomainArray<T> {
    type Target = PyFreqDomainArray;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let data = PyArray::from_slice(py, self.data.as_slice());
        PyFreqDomainArray {
            start_gps_pip: self.start_gps_pip,
            start_hz: self.start_hz,
            bucket_width_hz: self.bucket_width_hz,
            sequence_index: self.accumulation_stats.sequence_index,
            sequence_size: self.accumulation_stats.sequence_size,
            n: self.accumulation_stats.n,
            overlap: self.overlap,
            id: self.id,
            unit: self.unit,
            data: data.into_any().unbind(),
        }
        .into_pyobject(py)
    }
}

pub type FreqDomainArrayReal = FreqDomainArray<f64>;
pub type FreqDomainArrayComplex = FreqDomainArray<c128>;

//#[cfg_attr(any(feature = "python-pipe", feature = "python"), pyclass(frozen, name="FreqDomainArray"))]
#[cfg(any(feature = "python-pipe", feature = "python"))]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[pyclass(frozen, name = "FreqDomainArray")]
pub struct PyFreqDomainArray {
    #[pyo3(get)]
    start_gps_pip: PipInstant,
    #[pyo3(get)]
    start_hz: f64,
    #[pyo3(get)]
    bucket_width_hz: f64,
    #[pyo3(get)]
    overlap: f64,
    #[pyo3(get)]
    sequence_index: usize,
    #[pyo3(get)]
    sequence_size: usize,
    #[pyo3(get)]
    n: f64,
    #[pyo3(get)]
    data: Py<PyAny>,
    #[pyo3(get)]
    id: AnalysisId,
    #[pyo3(get)]
    unit: Unit,
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py> PyIntoAnalysisResult<'py> for PyFreqDomainArray {
    fn extract_result_value(ob: &Bound<'py, PyAny>) -> PyResult<AnalysisResult> {
        let pytdarray: &Bound<'py, Self> = ob.downcast()?;
        let complex = false;
        if complex {
            let fda: FreqDomainArrayComplex = pytdarray.try_into()?;
            Ok(fda.into())
        } else {
            let fda: FreqDomainArrayReal = pytdarray.try_into()?;
            Ok(fda.into())
        }
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> TryFrom<&Bound<'py, PyFreqDomainArray>> for FreqDomainArray<T> {
    type Error = PyErr;

    fn try_from(value: &Bound<'py, PyFreqDomainArray>) -> PyResult<Self> {
        let valptr = value.borrow();
        let data = valptr.data.extract(value.py())?;

        //value.data.extract(py)?
        Ok(Self {
            start_gps_pip: valptr.start_gps_pip,
            start_hz: valptr.start_hz,
            bucket_width_hz: valptr.bucket_width_hz,
            overlap: valptr.overlap,
            accumulation_stats: AccumulationStats {
                n: valptr.n,
                sequence_index: valptr.sequence_index,
                sequence_size: valptr.sequence_size,
            },
            id: valptr.id.clone(),
            unit: valptr.unit.clone(),
            data,
        })
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> FromPyObject<'py> for FreqDomainArray<T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        let obj = ob.downcast::<PyFreqDomainArray>()?;
        Ok(obj.try_into()?)
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[pymethods]
//#[cfg_attr(any(feature = "python-pipe", feature = "python"), pymethods)]
impl PyFreqDomainArray {
    /// Copy everything from another object except replace the data
    /// with a new python list of data
    #[cfg(any(feature = "python-pipe", feature = "python"))]
    pub fn clone_metadata(&self, id: AnalysisId, unit: Unit, new_data: &Bound<PyAny>) -> Self {
        Self {
            start_gps_pip: self.start_gps_pip,
            start_hz: self.start_hz,
            bucket_width_hz: self.bucket_width_hz,
            overlap: self.overlap,
            sequence_index: self.sequence_index,
            sequence_size: self.sequence_size,
            n: self.n,
            id,
            unit,
            data: new_data.clone().unbind(),
        }
    }
}

// some more trait implementations

impl<T, U> Sqrt for FreqDomainArray<T>
where
    T: Sqrt<Output = U> + PipeDataPrimitive,
    U: PipeDataPrimitive,
{
    type Output = FreqDomainArray<U>;

    fn square_root(&self) -> Self::Output {
        let data = self.data.iter().map(|x| x.square_root()).collect();
        let id = analysis_id!("sqrt", self.id.clone());
        let unit = self.unit.root(2);
        self.clone_metadata(id, unit, data)
    }
}

impl<T> Phase for FreqDomainArray<T>
where
    T: ComplexFloat + PipeDataPrimitive,
    T::Real: PipeDataPrimitive,
{
    type Output = FreqDomainArray<T::Real>;

    fn phase(&self) -> Self::Output {
        let data = self.data.iter().map(|v| v.im().atan2(v.re())).collect();
        let id = analysis_id!("phase", self.id.clone());
        self.clone_metadata(id, "rad".into(), data)
    }
}

impl<T> ToComplex for FreqDomainArray<T>
where
    T: Float + PipeDataPrimitive + Copy + Clone,
    Complex<T>: PipeDataPrimitive,
{
    type Output = FreqDomainArray<Complex<T>>;

    fn to_complex(&self, imag: &Self) -> Self::Output {
        let data = self
            .data
            .iter()
            .zip(imag.data.iter())
            .map(|(t1, t2)| Complex::new(t1.clone(), t2.clone()))
            .collect();
        let id = analysis_id!("complex", self.id.clone(), imag.id.clone());
        self.clone_metadata(id, self.unit.clone(), data)
    }
}
