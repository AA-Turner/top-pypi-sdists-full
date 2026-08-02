use crate::errors::DTTError;
use pipelines::PipelineError;
use pipelines::complex::c128;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::gen_stub_pyclass_enum;
use std::ffi::c_void;
use std::ptr::{null, null_mut};

#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, eq, eq_int)
)]
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum DecimationFilter {
    FirLS1,
    FirPM1,
    FirLS2,
    FirLS3,
}

impl From<DecimationFilter> for i32 {
    fn from(value: DecimationFilter) -> Self {
        match value {
            DecimationFilter::FirLS1 => 1,
            DecimationFilter::FirPM1 => 2,
            DecimationFilter::FirLS2 => 3,
            DecimationFilter::FirLS3 => 4,
        }
    }
}

impl Default for DecimationFilter {
    fn default() -> Self {
        DecimationFilter::FirLS1
    }
}

/// # FiltHistory
/// Pointer to C-allocated filter history to be used in sequential calls to decimate_* on the same
/// data stream
/// allocate with open_decimate...
/// deallocate with close_decimate...
#[derive(Clone, Debug)]
pub struct FiltHistory<T>(*mut T);

unsafe impl<T> Send for FiltHistory<T> {}

unsafe impl<T> Sync for FiltHistory<T> {}

impl<T> Into<*mut T> for FiltHistory<T> {
    fn into(self) -> *mut T {
        self.0
    }
}

impl<T: IsComplex> IsComplex for FiltHistory<T> {
    fn is_complex() -> bool {
        return T::is_complex();
    }
}

impl<T> FiltHistory<T> {
    pub fn new() -> Self {
        FiltHistory(null_mut())
    }
}

pub trait IsComplex {
    fn is_complex() -> bool;
}

impl IsComplex for f64 {
    fn is_complex() -> bool {
        false
    }
}

impl IsComplex for c128 {
    fn is_complex() -> bool {
        true
    }
}

/// wrapper around gds_sigp decimate()
/// x is the input vector for the filter.  prev and next can be considered "black box" filter history containers
/// Used when decimating a stream.
///
/// prev should be null ptr on first call of the stream and next should be null on the last
/// prev is always freed by the call.  Pass the value pointed at by next to prev of the next call.
///
/// num_dec is the number of x2 decimations, so the decimation factor is 2^num_dec
///
/// decimate enough lead time (10x times filter taps is typical) to attenuate any effects from starting with an empty history
pub fn decimate<T: Clone + IsComplex + Default>(
    filt: DecimationFilter,
    x: &[T],
    num_dec: i32,
    prev: &mut FiltHistory<T>,
) -> Result<Vec<T>, DTTError> {
    // check arguments
    if num_dec < 1 {
        return Err(DTTError::BadArgument(
            "decimate",
            "dec_factor",
            "must be positive",
        ));
    }

    let decf = num_dec as usize;

    // 2 ^ decf
    let decf_exp = 1 << decf;

    if x.len() % decf_exp != 0 {
        return Err(DTTError::BadArgument(
            "decimate",
            "x",
            "must be a multiple of dec_factor",
        ));
    }

    // setup output
    let mut y = Vec::with_capacity(x.len() / decf);
    y.resize(x.len() / decf_exp, T::default());

    let n = x.len() as i32;
    let next = &mut prev.0 as *mut *mut T;
    unsafe {
        crate::decimate_generic(
            filt.into(),
            T::is_complex().into(),
            x.as_ptr() as *const c_void,
            y.as_mut_ptr() as *mut c_void,
            n,
            num_dec,
            prev.0 as *mut c_void,
            next as *mut *mut c_void,
        );
    };
    Ok(y)
}

/// call before calling decimate() to allocate a filter history block
/// The "next" argument will be allocated.  It should be used as "prev" for all future
/// calls to decimate.
///
/// finally, when done with decimation, close_decimate should be called with the FiltHistory
pub fn open_decimate<T: IsComplex>(
    filt: DecimationFilter,
    num_dec: i32,
    next: &mut FiltHistory<T>,
) -> Result<(), PipelineError> {
    if num_dec < 1 {
        return Err(PipelineError::BadArgument(
            "decimate",
            "dec_factor",
            "must be positive",
        ));
    }

    let next_p = &mut next.0 as *mut *mut T;

    unsafe {
        crate::decimate_generic(
            filt.into(),
            T::is_complex().into(),
            null(),
            null_mut(),
            0,
            num_dec,
            null_mut(),
            next_p as *mut *mut c_void,
        );
    };
    Ok(())
}

/// call on the FilterHistory when finished with decimation to
/// free its memory
pub fn close_decimate<T: IsComplex>(filt: DecimationFilter, prev: &FiltHistory<T>) {
    unsafe {
        crate::decimate_generic(
            filt.into(),
            T::is_complex().into(),
            null(),
            null_mut(),
            0,
            1,
            prev.0 as *mut c_void,
            null_mut(),
        );
    };
}

/// # Support functions for decimate
pub fn firphase(filt: DecimationFilter, dec_factor: i32) -> f64 {
    unsafe { crate::firphase(filt.into(), dec_factor) }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_decimate() {
        let x = [1.0, -1.0, 1.5, -1.0];
        let mut history = FiltHistory::new();
        open_decimate(DecimationFilter::FirLS1, 1, &mut history).unwrap();
        let y = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        close_decimate(DecimationFilter::FirLS1, &history);
        assert_eq!(y.len(), 2);
    }

    #[test]
    fn test_double_decimate() {
        let x = [1.0, -1.0, 1.5, -1.0];
        let mut history = FiltHistory::new();
        open_decimate(DecimationFilter::FirLS1, 1, &mut history).unwrap();
        let y = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        assert_eq!(y.len(), 2);
        let y2 = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        assert_eq!(y2.len(), 2);
        let y3 = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        close_decimate::<f64>(DecimationFilter::FirLS1, &history);
        assert_eq!(y3.len(), 2);

        // target results taken from the original C function
        let from_c = [0.0020601588869841349, 0.00057130068110256699];
        assert_eq!(from_c, y3.as_slice());
    }

    #[test]
    fn test_complex_decimate() {
        let x = [
            c128::new(1.0, -1.0),
            c128::new(-1.0, 1.0),
            c128::new(1.5, -1.5),
            c128::new(-1.0, 1.0),
        ];
        let mut history = FiltHistory::new();
        open_decimate(DecimationFilter::FirLS1, 1, &mut history).unwrap();
        let y = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        assert_eq!(y.len(), 2);
        let y2 = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        assert_eq!(y2.len(), 2);
        let y3 = decimate(DecimationFilter::FirLS1, &x, 1, &mut history).unwrap();
        close_decimate::<c128>(DecimationFilter::FirLS1, &history);
        assert_eq!(y3.len(), 2);

        // target results taken from the original C function
        let from_c = [
            c128::new(0.0020601588869841349, -0.0020601588869841349),
            c128::new(0.00057130068110256699, -0.00057130068110256699),
        ];
        assert_eq!(from_c, y3.as_slice());
    }
}
