use serde::Serialize;
use serde::de::DeserializeOwned;

use crate::error::ConversionError;

use super::StreamTransform;

/// Type-erased stream transform for the Python boundary.
/// Input/output are `serde_json::Value` so Python can pass dicts.
pub trait DynStreamTransform: Send {
    fn transform_value(
        &mut self,
        input: serde_json::Value,
    ) -> Result<Vec<serde_json::Value>, ConversionError>;

    fn flush_value(&mut self) -> Result<Vec<serde_json::Value>, ConversionError>;

    fn take_warnings_value(&mut self) -> Vec<serde_json::Value>;
}

impl<T> DynStreamTransform for T
where
    T: StreamTransform + Send,
    T::Input: DeserializeOwned,
    T::Output: Serialize,
{
    fn transform_value(
        &mut self,
        input: serde_json::Value,
    ) -> Result<Vec<serde_json::Value>, ConversionError> {
        let typed: T::Input = serde_json::from_value(input)?;
        let results = self.transform(typed)?;
        results
            .into_iter()
            .map(|o| serde_json::to_value(o).map_err(ConversionError::from))
            .collect()
    }

    fn flush_value(&mut self) -> Result<Vec<serde_json::Value>, ConversionError> {
        let results = self.flush()?;
        results
            .into_iter()
            .map(|o| serde_json::to_value(o).map_err(ConversionError::from))
            .collect()
    }

    fn take_warnings_value(&mut self) -> Vec<serde_json::Value> {
        self.take_warnings()
            .into_iter()
            .map(|w| {
                serde_json::to_value(w).expect("ConversionWarning serialization is infallible")
            })
            .collect()
    }
}
