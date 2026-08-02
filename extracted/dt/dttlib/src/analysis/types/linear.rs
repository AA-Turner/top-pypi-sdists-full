use std::ops::{Add, Mul};
use std::sync::Arc;
//use pipelines::complex::c128;
use crate::errors::DTTError;

///Can be multiplied by a real scalar
/// or added to another of the same type
pub(crate) trait Linear<'a, T: 'static>:
    Mul<f64, Output = T> + Add<Arc<T>, Output = Result<T, DTTError>>
{
}

/// Can be multiplied by a complex value
/// In addition to being Linear
//pub (crate) trait ComplexLinear<'a, T: 'static, C: 'static>: Linear<'a, T> + Mul<c128, Output = C> {}

impl<'a, T, Z> Linear<'a, T> for Z
where
    Z: Mul<f64, Output = T> + Add<Arc<T>, Output = Result<T, DTTError>>,
    T: 'static,
{
}
//
// impl<'a, T, C, Z> ComplexLinear<'a, T, C> for Z
// where
//     Z: Mul<c128, Output = C> + Linear<'a, T>,
//     T: 'static,
//     C: 'static
// {}
