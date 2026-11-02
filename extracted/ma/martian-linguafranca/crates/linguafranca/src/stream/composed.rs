use crate::error::{ConversionError, ConversionWarning};

use super::StreamTransform;

/// Fuses two transforms: source→mid (A) and mid→target (B).
pub struct ComposedStream<A, B> {
    first: A,
    second: B,
}

impl<A, B> ComposedStream<A, B> {
    pub fn new(first: A, second: B) -> Self {
        Self { first, second }
    }
}

impl<A, B> StreamTransform for ComposedStream<A, B>
where
    A: StreamTransform,
    B: StreamTransform<Input = A::Output>,
{
    type Input = A::Input;
    type Output = B::Output;

    fn transform(&mut self, input: Self::Input) -> Result<Vec<Self::Output>, ConversionError> {
        let mid = self.first.transform(input)?;
        let mut out = Vec::new();
        for m in mid {
            out.extend(self.second.transform(m)?);
        }
        Ok(out)
    }

    fn flush(&mut self) -> Result<Vec<Self::Output>, ConversionError> {
        let mid = self.first.flush()?;
        let mut out = Vec::new();
        for m in mid {
            out.extend(self.second.transform(m)?);
        }
        out.extend(self.second.flush()?);
        Ok(out)
    }

    fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        let mut warnings = self.first.take_warnings();
        warnings.extend(self.second.take_warnings());
        warnings
    }
}
