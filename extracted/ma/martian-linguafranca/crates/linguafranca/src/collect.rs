use serde::Serialize;
use serde::de::DeserializeOwned;

use crate::error::ConversionError;

/// Type-erased response collector for the Python boundary.
///
/// Accepts stream events as `serde_json::Value`, accumulates them, and
/// produces a single response when finalized. Analogous to
/// [`DynStreamTransform`](crate::stream::dynamic::DynStreamTransform) but
/// for the inverse direction (stream → non-stream).
pub trait DynResponseCollector: Send {
    /// Feed a single stream event into the collector.
    fn feed_value(&mut self, event: serde_json::Value) -> Result<(), ConversionError>;

    /// Finalize the collector and return `(response, warnings)`.
    ///
    /// The response and each warning are serialized as `serde_json::Value`.
    fn finalize_value(
        &mut self,
    ) -> Result<(serde_json::Value, Vec<serde_json::Value>), ConversionError>;
}

/// Blanket implementation for any concrete collector that operates on typed
/// events and responses.
///
/// Implement [`ResponseCollector`] for your type and you get
/// `DynResponseCollector` for free.
pub trait ResponseCollector: Send {
    type Event: DeserializeOwned;
    type Response: Serialize;

    fn feed(&mut self, event: Self::Event) -> Result<(), ConversionError>;
    fn finalize(
        &mut self,
    ) -> Result<crate::error::ConversionResult<Self::Response>, ConversionError>;
}

impl<T> DynResponseCollector for T
where
    T: ResponseCollector,
{
    fn feed_value(&mut self, event: serde_json::Value) -> Result<(), ConversionError> {
        let typed: T::Event = serde_json::from_value(event)?;
        self.feed(typed)
    }

    fn finalize_value(
        &mut self,
    ) -> Result<(serde_json::Value, Vec<serde_json::Value>), ConversionError> {
        let result = self.finalize()?;
        let response = serde_json::to_value(result.value)?;
        let warnings = result
            .warnings
            .into_iter()
            .map(|w| {
                serde_json::to_value(w).expect("ConversionWarning serialization is infallible")
            })
            .collect();
        Ok((response, warnings))
    }
}
