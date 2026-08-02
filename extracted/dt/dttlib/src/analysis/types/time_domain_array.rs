#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::AnalysisResult;
use crate::analysis::result::AnalysisId;
#[cfg(any(feature = "python-pipe", feature = "python"))]
use crate::analysis::result::analysis_result::PyIntoAnalysisResult;
use crate::analysis::types::math_traits::{Phase, Sqrt, ToComplex};
use crate::analysis::types::{Accumulation, AccumulationStats, MutableAccumulation, Scalar};
use crate::analysis_id;
use crate::data_source::buffer::{Buffer, Fields};
use crate::errors::DTTError;
use crate::params::channel_params::{Channel, Unit};
use ligo_hires_gps_time::{PipDuration, PipInstant};
use nds_cache_rs::buffer::TimeSeries;
use num::complex::ComplexFloat;
use num::{Complex, Float};
use num_traits::FromPrimitive;
#[cfg(any(feature = "python-pipe", feature = "python"))]
use numpy::array::PyArray;
use pipelines::complex::{c64, c128};
use pipelines::{PipeData, PipeDataPrimitive};
#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::{
    Bound, FromPyObject, IntoPyObject, Py, PyAny, PyErr, PyResult, Python, pyclass, pymethods,
    types::PyAnyMethods,
};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use std::fmt::{Display, Formatter};
use std::ops::{Add, Mul, Sub};
use std::sync::Arc;
use user_messages::UserMsgProvider;

// use ts_tree_rs::time_series::TimeSeries;

/// # Fixed pitch data blocks
/// ## Time Domain array
#[derive(Clone, Debug)]
pub struct TimeDomainArray<T> {
    pub start_gps_pip: PipInstant,

    /// Useful for sub-sampled arrays to show where the
    /// real data ends if not exactly on a one-step boundary.
    pub real_end_gps_pip: Option<PipInstant>,
    pub period_pip: PipDuration,
    pub data: Vec<T>,
    pub accumulation_stats: AccumulationStats,
    /// total number of points that have been added to fill gaps
    pub total_gap_size: usize,

    pub id: AnalysisId,
    pub unit: Unit,
}

impl<T> Default for TimeDomainArray<T> {
    fn default() -> Self {
        Self {
            start_gps_pip: PipInstant::gpst_epoch(),
            real_end_gps_pip: None,
            period_pip: PipDuration::from_seconds(1.0),
            data: Vec::new(),
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: 0,
            id: AnalysisId::default(),
            unit: Unit::default(),
        }
    }
}

/// Equality in time, not in value
impl<T> PartialEq<Self> for TimeDomainArray<T> {
    fn eq(&self, other: &Self) -> bool {
        self.start_gps_pip == other.start_gps_pip && self.period_pip == other.period_pip
    }
}

impl<T> Add<Arc<TimeDomainArray<T>>> for TimeDomainArray<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<TimeDomainArray<T>, DTTError>;

    fn add(mut self, rhs: Arc<TimeDomainArray<T>>) -> Self::Output {
        if self.period_pip != rhs.period_pip {
            let msg = format!(
                "Can't add time domain arrays.  Sample rates differ: ({}, {})",
                self.rate_hz(),
                rhs.rate_hz()
            );
            return Err(DTTError::CalcError(msg));
        };
        if self.data.len() != rhs.data.len() {
            let msg = format!(
                "Can't add time domain arrays.  Lengths differ: ({}, {})",
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

impl<T> Add<Arc<TimeDomainArray<T>>> for &TimeDomainArray<T>
where
    T: Copy + Add<T, Output = T>,
{
    type Output = Result<TimeDomainArray<T>, DTTError>;

    fn add(self, rhs: Arc<TimeDomainArray<T>>) -> Self::Output {
        let sum: TimeDomainArray<T> = self.clone();
        sum + rhs
    }
}

impl<T> Mul<f64> for TimeDomainArray<T>
where
    T: Copy + Mul<f64, Output = T>,
{
    type Output = TimeDomainArray<T>;

    fn mul(mut self, rhs: f64) -> Self::Output {
        for i in 0..self.data.len() {
            self.data[i] = self.data[i] * rhs
        }
        self
    }
}

impl<T> Eq for TimeDomainArray<T> {}

impl<T> Display for TimeDomainArray<T> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "[x=t y={} s={}, e={}, r={} n={}]",
            self.id,
            self.start_gps_pip.to_gpst_seconds(),
            self.real_end_gps_pip
                .unwrap_or_else(|| { self.end_gps_pip() })
                .to_gpst_seconds(),
            self.rate_hz(),
            self.len(),
        )
    }
}

impl<T: PipeDataPrimitive> PipeData for TimeDomainArray<T> {}

impl<T> TimeDomainArray<T>
where
    T: Scalar,
{
    pub fn mean(&self) -> T {
        if self.data.is_empty() {
            return T::default();
        }

        let mut mean = T::default();
        for element in &self.data {
            mean += *element;
        }

        let n = f64::from_usize(self.data.len()).unwrap_or(1.0);
        mean /= n.into();
        mean
    }
}

impl<T> TimeDomainArray<T> {
    pub fn len(&self) -> usize {
        self.data.len()
    }

    pub fn rate_hz(&self) -> f64 {
        self.period_pip.period_to_freq_hz()
    }

    /// set extra values form buffer
    /// used in Buffer::into() -> TimeDomainArray
    fn set_from_buffer_fields(mut self, buffer: Fields) -> Self {
        self.total_gap_size = buffer.total_gap_size;
        self
    }
}

/// Convert a TimeSeries of type f32 to a TimeDomainArray of type f64
pub fn from_time_series_f32_to_f64<C>(
    value: TimeSeries<C, f32>,
) -> Result<TimeDomainArray<f64>, DTTError>
where
    C: TryInto<Channel> + Clone,
    DTTError: From<<C as TryInto<Channel>>::Error>,
{
    let start_gps_pip = value.start();
    let period_pip = value.period();
    let chan: Channel = value.id().clone().try_into()?;
    let unit = chan.units.clone();
    let id: AnalysisId = chan.into();
    let data_vec: Vec<_> = value.into();
    Ok(TimeDomainArray {
        start_gps_pip,
        real_end_gps_pip: None,
        period_pip,
        data: data_vec.into_iter().map(|x| x as f64).collect(),
        accumulation_stats: AccumulationStats::default(),
        total_gap_size: 0,
        id,
        unit,
    })
}

impl<C, T> TryFrom<TimeSeries<C, T>> for TimeDomainArray<T>
where
    T: Clone,
    C: Clone + TryInto<Channel>,
    DTTError: From<<C as TryInto<Channel>>::Error>,
{
    type Error = DTTError;

    fn try_from(value: TimeSeries<C, T>) -> Result<Self, Self::Error> {
        let chan: Channel = value.id().clone().try_into()?;
        let unit = chan.units.clone();
        let id: AnalysisId = chan.into();
        Ok(Self {
            start_gps_pip: value.start(),
            real_end_gps_pip: None,
            period_pip: value.period(),
            data: value.into(),
            accumulation_stats: AccumulationStats::default(),
            total_gap_size: 0,
            id,
            unit,
        })
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i8> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Int8(t) => {
                Ok(TimeDomainArray::<i8>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type i8";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i16> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Int16(t) => {
                Ok(TimeDomainArray::<i16>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type i16";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Int32(t) => {
                Ok(TimeDomainArray::<i32>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type i32";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<i64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Int64(t) => {
                Ok(TimeDomainArray::<i64>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type i64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<f32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Float32(t) => {
                Ok(TimeDomainArray::<f32>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            t => {
                let msg = format!("Expected data buffer of type f32, got {:?}", t);
                Err(DTTError::MismatchedTypesError(msg))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<f64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Float64(t) => {
                Ok(TimeDomainArray::<f64>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            nds_cache_rs::buffer::Buffer::Float32(t) => from_time_series_f32_to_f64(t),
            _ => {
                let msg = "Expected data buffer of type f64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<c64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Complex32(t) => {
                Ok(TimeDomainArray::<c64>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type c64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u8> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::UInt8(t) => {
                Ok(TimeDomainArray::<u8>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type u8";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u16> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::UInt16(t) => {
                Ok(TimeDomainArray::<u16>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type u16";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u32> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::UInt32(t) => {
                Ok(TimeDomainArray::<u32>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type u32";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<u64> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::UInt64(t) => {
                Ok(TimeDomainArray::<u64>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffer of type u64";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<c128> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            nds_cache_rs::buffer::Buffer::Complex64(t) => {
                Ok(TimeDomainArray::<c128>::try_from(t)?.set_from_buffer_fields(value.fields))
            }
            _ => {
                let msg = "Expected data buffers of type c128";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl TryFrom<Buffer> for TimeDomainArray<String> {
    type Error = DTTError;

    fn try_from(value: Buffer) -> Result<Self, Self::Error> {
        match value.cache_buffer {
            _ => {
                let msg = "Data buffers of type String are not supported";
                Err(DTTError::MismatchedTypesError(msg.into()))
            }
        }
    }
}

impl<T: Clone> TimeDomainArray<T> {
    /// return a copy of a subsection of the time series
    pub fn copy_from(&self, start: PipInstant, end: PipInstant) -> Self {
        let s = self.ligo_hires_gps_time_to_index(start);
        let e = self.ligo_hires_gps_time_to_index(end);

        let new_data = Vec::from_iter(self.data[s..e].iter().cloned());

        Self {
            start_gps_pip: start,
            // we loose any pre-sampling end point by trimming the end
            real_end_gps_pip: None,
            period_pip: self.period_pip,
            data: new_data,
            accumulation_stats: self.accumulation_stats.clone(),

            // best guess!
            total_gap_size: self.total_gap_size,
            id: self.id.clone(),
            unit: self.unit.clone(),
        }
    }
}

impl<T> TimeDomainArray<T> {
    /// return the time of the first timestamp after the end of the time series
    /// equal to the start time of the following series if it is contiguous.
    pub fn end_gps_pip(&self) -> PipInstant {
        // assume rate is a power of two
        self.index_to_gps_instant(self.data.len())
    }

    /// snap a pip value to the nearest integer value of the step size of the array
    pub fn snap_to_step_pip(&self, raw_pip: PipDuration) -> PipDuration {
        let pip_per_cyc = self.period_pip;
        raw_pip.snap_to_step(&pip_per_cyc)
    }

    /// snap a pip value to the nearest integer value of the step size of the array
    pub fn snap_to_step_pip_instant(&self, raw_pip: PipInstant) -> PipInstant {
        let pip_per_cyc = self.period_pip;
        raw_pip.snap_to_step(&pip_per_cyc)
    }

    /// Trim the time series to start at the new value.
    pub fn trim_to(
        &mut self,
        rc: Box<dyn UserMsgProvider>,
        raw_new_start: PipInstant,
    ) -> Result<(), DTTError> {
        let new_start = self.snap_to_step_pip_instant(raw_new_start);
        if new_start < self.start_gps_pip {
            let msg = "Requested start time was earlier than saved data when trimming a time domain array";
            rc.user_message_handle().error(msg);
            return Err(DTTError::CalcError(msg.to_string()));
        }
        let s = self.ligo_hires_gps_time_to_index(new_start);
        if s >= self.data.len() {
            self.start_gps_pip = self.end_gps_pip();
            self.data.clear();
        } else {
            self.data.drain(0..s);
            self.start_gps_pip = new_start;
        }
        Ok(())
    }

    /// convert a gps time into an array index
    /// not guaranteed to be in bounds
    pub(crate) fn ligo_hires_gps_time_to_index(&self, t: PipInstant) -> usize {
        let span: PipDuration = t - self.start_gps_pip;
        let pip_per_cyc = self.period_pip;
        (span / pip_per_cyc) as usize
    }

    pub(crate) fn index_to_gps_instant(&self, index: usize) -> PipInstant {
        let pip_per_cyc = self.period_pip;
        self.start_gps_pip + (pip_per_cyc * u64::from_usize(index).unwrap_or(0))
    }

    pub fn time_step(&self) -> f64 {
        self.period_pip.to_seconds()
    }

    /// align the start point to a multiple of the sample period
    pub fn align_start(mut self) -> Self {
        let step_pip = self.period_pip;
        self.start_gps_pip = self.start_gps_pip.snap_to_step(&step_pip);
        self
    }

    /// get the real end point of the array
    /// for sub-sampled arrays, this will be
    /// the end point of the pre-sampled data
    /// which can be different than the calculated
    /// end point given by end_gps_pip()
    pub fn get_real_end_gps_pip(&self) -> PipInstant {
        self.real_end_gps_pip.unwrap_or(self.end_gps_pip())
    }

    pub fn set_real_end_gps_pip(&mut self, real_end: PipInstant) {
        self.real_end_gps_pip = Some(real_end);
    }

    /// Add self into data, filling in gaps and combining contiguous segemnts
    /// data is assumed to be in time order with no overlaps and will remain so
    /// return true if something has changed.
    /// will returned false if self is entirely contained within data already
    ///
    /// Does *not* check if the values in self match the values in data.  Only
    /// splices based on range of time.
    pub(crate) fn splice_into(self, data: &mut Vec<Self>) -> bool {
        let self_end_pip = self.end_gps_pip();

        if data.is_empty()
            || self.start_gps_pip
                > data
                    .last()
                    .expect("code should ensure data is not empty")
                    .end_gps_pip()
        {
            data.push(self);
            return true;
        }

        if self_end_pip < data[0].start_gps_pip {
            data.insert(0, self);
            return true;
        }

        let mut lo = 0;
        let mut hi = data.len();
        while lo + 1 < hi {
            let mid = (lo + hi) / 2;
            let mid_end = data[mid].end_gps_pip();
            if self.start_gps_pip <= mid_end {
                hi = mid;
            } else {
                lo = mid;
            }
        }

        let start_index = if hi == data.len() || data[lo].end_gps_pip() >= self.start_gps_pip {
            lo
        } else {
            hi
        };

        // println!("start = {} end = {} start_index = {} start_si = {} end_si = {}",
        //     self.start_gps_pip.to_gpst_seconds(),
        //     self_end_pip.to_gpst_seconds(),
        //          start_index,
        //     data[start_index].start_gps_pip.to_gpst_seconds(),
        //     data[start_index].end_gps_pip().to_gpst_seconds(),
        // );

        let mut look = self;
        let mut spliced = true;
        while start_index < data.len() {
            if look.end_gps_pip() < data[start_index].start_gps_pip {
                data.insert(start_index, look);
                return spliced;
            }
            let s = data.remove(start_index);
            (look, spliced) = look
                .union(s)
                .expect("code should ensure that data overlaps");
        }
        data.push(look);
        spliced
    }

    /// return the time history that's the union of
    /// the two time histories.
    /// Time histories must overlap or be contiguous.  It's an error otherwise.
    /// Returns the union and a bool that is true iff
    /// union != other
    /// this bool is used to determine whether a splice_into() call results in any change
    fn union(mut self, mut other: Self) -> Result<(Self, bool), DTTError> {
        if self.end_gps_pip() < other.start_gps_pip && self.start_gps_pip < other.end_gps_pip() {
            let msg =
                "Cannot take union of time domain arrays that don't overlap or arent contiguous."
                    .to_string();
            return Err(DTTError::CalcError(msg));
        }

        if self.start_gps_pip >= other.start_gps_pip && self.end_gps_pip() <= other.end_gps_pip() {
            return Ok((other, false));
        }

        if self.start_gps_pip <= other.start_gps_pip && self.end_gps_pip() >= other.end_gps_pip() {
            return Ok((self, true));
        }

        if self.start_gps_pip < other.start_gps_pip {
            let new_end = self.ligo_hires_gps_time_to_index(other.start_gps_pip);
            self.data.drain(new_end..);
            self.data.append(&mut other.data);
            return Ok((self, true));
        }

        let new_end = other.ligo_hires_gps_time_to_index(self.start_gps_pip);
        other.data.drain(new_end..);
        other.data.append(&mut self.data);
        Ok((other, true))
    }

    /// clone the meta data of an array, but put in a new data array
    fn clone_metadata<U: PipeData>(
        &self,
        id: AnalysisId,
        unit: Unit,
        data: Vec<U>,
    ) -> TimeDomainArray<U> {
        TimeDomainArray {
            start_gps_pip: self.start_gps_pip,
            // we don't have any presampling info
            real_end_gps_pip: None,
            period_pip: self.period_pip,
            data,
            accumulation_stats: self.accumulation_stats.clone(),
            total_gap_size: self.total_gap_size,
            id,
            unit,
        }
    }
}

impl<T: PipeData + Copy> TimeDomainArray<T> {
    /// from a set of ordered, non overlaping arrays, return a single array
    /// with any gaps filled in by a specific value
    pub(crate) fn fill_gaps(data: &Vec<Self>, gap_value: T) -> Option<Self> {
        if data.is_empty() {
            return None;
        }
        if data.len() == 1 {
            return Some(data[0].clone());
        }
        let mut new_data = data[0].clone();

        let step_pip = new_data.period_pip;

        for i in 1..data.len() {
            let diff_pip = data[i].start_gps_pip - new_data.end_gps_pip();
            let diff_steps = diff_pip / step_pip;
            let gap = vec![gap_value; diff_steps as usize];
            new_data.data.extend(gap);
            new_data.data.append(&mut data[i].data.clone());
        }
        Some(new_data)
    }
}

impl<T: Clone> Accumulation for TimeDomainArray<T> {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self {
        let mut n = self.clone();
        n.accumulation_stats = stats;
        n
    }

    fn get_accumulation_stats(&self) -> &AccumulationStats {
        &self.accumulation_stats
    }
}

impl<T: Clone> MutableAccumulation for TimeDomainArray<T> {
    fn set_mut_accumulation_stats(&mut self, stats: AccumulationStats) {
        self.accumulation_stats = stats;
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeDataPrimitive> IntoPyObject<'py> for TimeDomainArray<T> {
    type Target = PyTimeDomainArray;
    type Output = Bound<'py, PyTimeDomainArray>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let data = PyArray::from_vec(py, self.data);
        let ptda = PyTimeDomainArray {
            start_gps_pip: self.start_gps_pip,
            real_end_gps_pip: self.real_end_gps_pip,
            period_pip: self.period_pip,
            total_gap_size: self.total_gap_size,
            n: self.accumulation_stats.n,
            sequence_index: self.accumulation_stats.sequence_index,
            sequence_size: self.accumulation_stats.sequence_size,
            id: self.id,
            unit: self.unit,
            data: data.into_any().unbind(),
        };
        //Python::with_gil(|py| {
        let obj = ptda.into_pyobject(py)?;

        Ok(obj)
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[pyclass(frozen, name = "TimeDomainArray", str)]
pub struct PyTimeDomainArray {
    #[pyo3(get)]
    start_gps_pip: PipInstant,
    #[pyo3(get)]
    real_end_gps_pip: Option<PipInstant>,
    #[pyo3(get)]
    period_pip: PipDuration,
    #[pyo3(get)]
    n: f64,
    #[pyo3(get)]
    sequence_index: usize,
    #[pyo3(get)]
    sequence_size: usize,
    #[pyo3(get)]
    data: Py<PyAny>,
    #[pyo3(get)]
    total_gap_size: usize,
    #[pyo3(get)]
    id: AnalysisId,
    #[pyo3(get)]
    unit: Unit,
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py> PyIntoAnalysisResult<'py> for PyTimeDomainArray {
    fn extract_result_value(ob: &Bound<'py, PyAny>) -> PyResult<AnalysisResult> {
        let pytdarray: &Bound<'py, Self> = ob.downcast()?;
        let complex = false;
        if complex {
            let fda: TimeDomainArrayComplex = pytdarray.try_into()?;
            Ok(fda.into())
        } else {
            let fda: TimeDomainArrayReal = pytdarray.try_into()?;
            Ok(fda.into())
        }
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> TryFrom<&Bound<'py, PyTimeDomainArray>> for TimeDomainArray<T> {
    type Error = PyErr;

    fn try_from(value: &Bound<'py, PyTimeDomainArray>) -> PyResult<Self> {
        let valptr = value.borrow();
        let data = valptr.data.extract(value.py())?;

        //value.data.extract(py)?
        Ok(Self {
            start_gps_pip: valptr.start_gps_pip,
            real_end_gps_pip: valptr.real_end_gps_pip,
            period_pip: valptr.period_pip,
            total_gap_size: valptr.total_gap_size,
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
impl Display for PyTimeDomainArray {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "[x=t y={} s={} r={} n={}]",
            self.id,
            self.start_gps_pip.to_gpst_seconds(),
            self.rate_hz(),
            self.n
        )
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[pymethods]
impl PyTimeDomainArray {
    /// return the time of the first timestamp after the end of the time series
    /// equal to the start time of the following series if it is contiguous.
    pub fn end_gps_pip(&self) -> Result<PipInstant, PyErr> {
        // assume rate is a power of two
        Ok(self.index_to_gps_instant(self.len()?))
    }

    pub fn len(&self) -> Result<usize, PyErr> {
        Python::with_gil(|py| {
            let bound = self.data.bind(py);
            bound.len()
        })
    }

    pub fn is_empty(&self) -> Result<bool, PyErr> {
        Ok(self.len()? == 0)
    }

    pub fn index_to_gps_instant(&self, index: usize) -> PipInstant {
        let pip_per_cyc = self.period_pip;
        self.start_gps_pip + (pip_per_cyc * u64::from_usize(index).unwrap_or(0))
    }

    #[getter]
    pub fn rate_hz(&self) -> f64 {
        self.period_pip.period_to_freq_hz()
    }

    /// return the a non-negative index that's closes to the time given
    /// if the time given is before the start, the return value is zero
    /// but the return value can be greater or equal to the length of the array
    /// and therefore out of bounds
    pub fn gps_instant_to_index(&self, instant: PipInstant) -> usize {
        if instant <= self.start_gps_pip {
            0
        } else {
            let rounded_delta = (instant - self.start_gps_pip).snap_to_step(&self.period_pip);
            (rounded_delta / self.period_pip) as usize
        }
    }

    pub fn timestamps(&self) -> Result<Vec<PipInstant>, PyErr> {
        let n = self.len()?;
        let mut t = Vec::with_capacity(n);
        for i in 0..n {
            t.push(self.start_gps_pip + i * self.period_pip);
        }
        // let t = (0..n)
        //     .into_iter()
        //     .map(|x| self.start_gps_pip + x * self.period_pip)
        //     .collect();
        Ok(t)
    }

    /// Get the timestamps transformed into a delta time from some t0
    /// return values in seconds as floating point
    /// Useful for getting relative timestamps to a point of time on a graph
    pub fn delta_t_seconds(&self, t0: PipInstant) -> Result<Vec<f64>, PyErr> {
        let n = self.len()?;
        let t_offset = (self.start_gps_pip - t0).to_seconds();
        let period_sec = self.period_pip.to_seconds();
        let t = (0..n)
            .into_iter()
            //.map(|x| (t_offset + x * self.period_pip).to_seconds())
            .map(|x| t_offset + x as f64 * period_sec)
            .collect();
        Ok(t)
    }
}

#[cfg(any(feature = "python-pipe", feature = "python"))]
impl<'py, T: PipeData> FromPyObject<'py> for TimeDomainArray<T> {
    fn extract_bound(ob: &Bound<'py, PyAny>) -> PyResult<Self> {
        Python::with_gil(|_py| {
            let start_gps_pip: PipInstant = ob.getattr("start_gps_pip")?.extract()?;
            let real_end_gps_pip: Option<PipInstant> = ob.getattr("start_gps_pip")?.extract()?;
            let period_pip: PipDuration = ob.getattr("period_pip")?.extract()?;
            let data = ob.getattr("data")?.extract()?;
            let n = ob.getattr("n")?.extract()?;
            let sequence_index: usize = ob.getattr("sequence_index")?.extract()?;
            let sequence_size: usize = ob.getattr("sequence_size")?.extract()?;
            let total_gap_size: usize = ob.getattr("total_gap_size")?.extract()?;
            let unit: Unit = ob.getattr("unit")?.extract()?;
            let id: AnalysisId = ob.getattr("id")?.extract()?;
            PyResult::Ok(TimeDomainArray {
                start_gps_pip,
                real_end_gps_pip,
                period_pip,
                data,
                total_gap_size,
                id,
                unit,
                accumulation_stats: AccumulationStats {
                    n,
                    sequence_index,
                    sequence_size,
                },
            })
        })
    }
}

impl<T> Sub<T> for TimeDomainArray<T>
where
    T: Scalar,
{
    type Output = TimeDomainArray<T>;

    fn sub(mut self, rhs: T) -> Self::Output {
        for x in self.data.iter_mut() {
            *x -= rhs;
        }
        self
    }
}

pub type TimeDomainArrayReal = TimeDomainArray<f64>;
pub type TimeDomainArrayComplex = TimeDomainArray<c128>;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::run_context::tests::start_runtime;

    fn setup_td() -> TimeDomainArray<f64> {
        let data = (0..2048).map(|x| x as f64).collect();

        TimeDomainArray {
            // a bit less than one microsecond
            start_gps_pip: 1024000000000i128.into(),
            period_pip: PipDuration::freq_hz_to_period(2048.0),
            data,
            ..TimeDomainArray::default()
        }
    }

    const BLOCK_SIZE: usize = 2048;
    const STEP_SIZE: i128 = 1024000000000i128;

    const BIG_BLOCK: usize = BLOCK_SIZE * 2;
    const SMALL_BLOCK: usize = BLOCK_SIZE / 2;

    const FIRST_START: usize = BLOCK_SIZE + 2;
    const SECOND_START: usize = FIRST_START + 2 + BLOCK_SIZE * 2;
    const THIRD_START: usize = SECOND_START + BIG_BLOCK + BLOCK_SIZE;

    fn setup_td_start(start_step: usize) -> TimeDomainArray<f64> {
        let data = (0..BLOCK_SIZE).map(|x| x as f64).collect();
        let step = PipDuration::from_pips(STEP_SIZE);
        TimeDomainArray {
            // a bit less than one microsecond
            start_gps_pip: PipInstant::gpst_epoch() + step * start_step,
            period_pip: PipDuration::freq_hz_to_period(2048.0),
            data,
            ..TimeDomainArray::default()
        }
    }

    fn setup_td_array() -> Vec<TimeDomainArray<f64>> {
        let data = (0..BLOCK_SIZE).map(|x| x as f64).collect();
        let step = PipDuration::from_pips(STEP_SIZE);
        let first = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step * (FIRST_START),
            period_pip: PipDuration::freq_hz_to_period(2048.0),
            data,
            ..TimeDomainArray::default()
        };

        let data = (0..BIG_BLOCK).map(|x| x as f64).collect();
        let second = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step * (SECOND_START),
            period_pip: PipDuration::freq_hz_to_period(2048.0),
            data,
            ..TimeDomainArray::default()
        };

        let data = (0..SMALL_BLOCK).map(|x| x as f64).collect();
        let third = TimeDomainArray {
            start_gps_pip: PipInstant::gpst_epoch() + step * (THIRD_START),
            period_pip: PipDuration::freq_hz_to_period(2048.0),
            data,
            ..TimeDomainArray::default()
        };

        vec![first, second, third]
    }

    #[test]
    fn test_trim() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut td = setup_td();
        let end1 = td.end_gps_pip();
        let period = td.period_pip;
        // trim off first 116 values
        let new_start_pip = td.start_gps_pip + period * 116;
        td.trim_to(rc, new_start_pip).unwrap();
        let end2 = td.end_gps_pip();
        assert_eq!(end2, end1);
        assert_eq!(td.data.len(), 2048 - 116);
    }

    #[test]
    fn test_over_trim() {
        let (mut _uc, mut _or, rc) = start_runtime();

        let mut td = setup_td();
        let end1 = td.end_gps_pip();
        // trim off first 116 values
        let new_start_pip = td.start_gps_pip + PipDuration::from_sec(1) * 2164 / 2048.0;
        td.trim_to(rc, new_start_pip).unwrap();
        let end2 = td.end_gps_pip();
        assert_eq!(end2, end1);
        assert_eq!(td.data.len(), 0);
    }

    #[test]
    fn test_splice_empty() {
        let mut array = vec![];
        let td = setup_td();
        td.clone().splice_into(&mut array);
        assert_eq!(array.len(), 1);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len());
        assert_eq!(array[0].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_before() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td();

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len());
        assert_eq!(array[0].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_before_join() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START - BLOCK_SIZE);

        let start_len = array[0].data.len();
        assert_eq!(td.end_gps_pip(), array[0].start_gps_pip);
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len() + start_len);
        assert_eq!(array[0].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_before_overlap() {
        let (_uc, _orstart_gps_pip, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START - BLOCK_SIZE + 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len() + start_len - 1);
        assert_eq!(array[0].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_first_exact() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(FIRST_START);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(!changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), start_len);
        assert_eq!(array[0].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_between() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(SECOND_START - BLOCK_SIZE - 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[1].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[1].data.len(), start_len);
        assert_eq!(array[1].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_subsumed() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(SECOND_START + 1);

        let start_len = array[1].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(!changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[1].data.len(), start_len);
        assert_eq!(array[1].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_exact_join() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START - BLOCK_SIZE);

        let start_len = array[1].data.len();
        let start_len2 = array[2].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 2);
        assert_eq!(array[1].data.len(), start_len + start_len2 + td.data.len());
        assert_eq!(array[1].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_cover() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START - 1);

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 3);
        assert_eq!(array[2].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[2].data.len(), td.data.len());
        assert_eq!(array[2].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_after() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let td = setup_td_start(THIRD_START + SMALL_BLOCK + 1);

        let start_len = array[0].data.len();
        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 4);
        assert_eq!(array[3].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[3].data.len(), start_len);
        assert_eq!(array[3].period_pip, td.period_pip);
    }

    #[test]
    fn test_splice_big() {
        let (_uc, _or, _rc) = start_runtime();

        let mut array = setup_td_array();
        let mut td = setup_td_start(1);
        td.data = (0..20480).map(|x| x as f64).collect();

        let changed = td.clone().splice_into(&mut array);
        assert!(changed);
        assert_eq!(array.len(), 1);
        assert_eq!(array[0].start_gps_pip, td.start_gps_pip);
        assert_eq!(array[0].data.len(), td.data.len());
        assert_eq!(array[0].period_pip, td.period_pip);
    }
}

// some more trait implementations

impl<T, U> Sqrt for TimeDomainArray<T>
where
    T: Sqrt<Output = U> + PipeDataPrimitive,
    U: PipeDataPrimitive,
{
    type Output = TimeDomainArray<U>;

    fn square_root(&self) -> Self::Output {
        let data = self.data.iter().map(|x| x.square_root()).collect();
        let id = analysis_id!("sqrt", self.id.clone());
        let unit = self.unit.root(2);
        self.clone_metadata(id, unit, data)
    }
}

impl<T> Phase for TimeDomainArray<T>
where
    T: ComplexFloat + PipeDataPrimitive,
    T::Real: PipeDataPrimitive,
{
    type Output = TimeDomainArray<T::Real>;

    fn phase(&self) -> Self::Output {
        let data = self.data.iter().map(|v| v.im().atan2(v.re())).collect();
        let id = analysis_id!("phase", self.id.clone());
        self.clone_metadata(id, "rad".into(), data)
    }
}

impl<T> ToComplex for TimeDomainArray<T>
where
    T: Float + PipeDataPrimitive + Copy + Clone,
    Complex<T>: PipeDataPrimitive,
{
    type Output = TimeDomainArray<Complex<T>>;

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
