use crate::config::ConversionConfig;
use crate::error::{ConversionError, ConversionResult};

pub trait IntoOpenResponses {
    type Target;
    fn into_open_responses(
        self,
        config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self::Target>, ConversionError>;
}

pub trait FromOpenResponses: Sized {
    type Source;
    fn from_open_responses(
        source: Self::Source,
        config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self>, ConversionError>;
}

/// Collect a stream of events into a single non-streaming response.
pub trait CollectStream {
    type Event;
    type Response;
    fn collect_stream(
        events: impl IntoIterator<Item = Self::Event>,
    ) -> Result<ConversionResult<Self::Response>, ConversionError>;
}

/// Decompose a non-streaming response into a sequence of stream events.
pub trait DecomposeToStream {
    type Event;
    fn decompose_to_stream(self) -> Result<ConversionResult<Vec<Self::Event>>, ConversionError>;
}
