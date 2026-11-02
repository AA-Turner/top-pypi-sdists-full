pub mod composed;
pub mod dynamic;

use crate::error::{ConversionError, ConversionWarning};

pub trait StreamTransform {
    type Input;
    type Output;

    fn transform(&mut self, input: Self::Input) -> Result<Vec<Self::Output>, ConversionError>;
    fn flush(&mut self) -> Result<Vec<Self::Output>, ConversionError>;

    fn take_warnings(&mut self) -> Vec<ConversionWarning>;
}
