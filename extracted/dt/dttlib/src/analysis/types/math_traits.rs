use pipelines::PipeData;
use pipelines::complex::c128;

pub(crate) trait Sqrt {
    type Output: PipeData;

    fn square_root(&self) -> Self::Output;
}

impl Sqrt for f64 {
    type Output = f64;

    fn square_root(&self) -> Self::Output {
        (*self).sqrt()
    }
}

impl Sqrt for c128 {
    type Output = c128;

    fn square_root(&self) -> Self::Output {
        (*self).sqrt()
    }
}

pub(crate) trait Phase {
    type Output: PipeData;

    fn phase(&self) -> Self::Output;
}

pub(crate) trait ToComplex {
    type Output: PipeData;

    fn to_complex(&self, other: &Self) -> Self::Output;
}
