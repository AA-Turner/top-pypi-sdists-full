use nds_cache_rs::buffer::TimeSeriesError;

#[derive(thiserror::Error, Debug, Clone)]
pub enum DTTError {
    #[error("Timeline Calculation Failed: {0}")]
    TimelineCalcFailed(String),
    #[error("Failed to create async runtime: {0}")]
    RuntimeCreationFailed(String),
    #[error("A bad test parameter '{0}' caused a failure")]
    BadTestParameter(String),
    #[error("A constraint could not be satisfied")]
    UnsatisfiedConstraint,
    #[error("Blocking task join error: {0}")]
    BlockingTaskJoinFailed(String),
    #[error("Timed out while {0}")]
    TimedOut(String),
    #[error("Channel closed")]
    ChannelClosed,
    #[error("Bad Argument in {0}: {1} {2}")]
    BadArgument(&'static str, &'static str, &'static str),
    #[error("Error in calculation: {0}")]
    CalcError(String),
    #[error("Unrecognized Error: {0}")]
    UnrecognizedError(String),
    #[error("out of memory: {0}")]
    OutOfMemory(&'static str),
    #[cfg(feature = "nds")]
    #[error("{0}")]
    NDSClientError(#[from] nds2_client_rs::NDSError),
    #[error("NDS cache error: {0}")]
    NDSCacheError(String),
    #[error("A calculation that needs a bound start time was made on an unbound start time")]
    UnboundStartTime,
    #[error("MPSC send error {0}")]
    TokioMPSCSend(String),
    #[error("Send failure on tokio watch channel: {0}")]
    TokioWatchSend(String),
    #[error("Failure on tokio join: {0}")]
    TokioJoinError(String),
    #[error("Unimplemented Option: {0}, {1}")]
    UnimplementedOption(String, String),
    #[error("Error in constructed analysis pipelines: {0}")]
    AnalysisPipelineError(String),
    #[error("Warning in constructed analysis pipelines: {0}")]
    AnalysisPipelineWarning(String),
    #[error("Mismatched types: {0}")]
    MismatchedTypesError(String),
    #[error("Unsupported type {0} when {1}")]
    UnsupportedTypeError(&'static str, &'static str),
    #[error("Missing data stream: {0}")]
    MissingDataStreamError(String),
    #[error["{0} does not have the capability to {1}"]]
    NoCapabaility(String, String),
    #[error("View closed")]
    ViewClosed,
    #[error("Error while configuring view: {0}")]
    ViewConfig(String),
    #[error("Unknown Trend type: {0}")]
    UnknownTrendType(String),
    #[error("Unknown Trend Stat: {0}")]
    UnknownTrendStat(String),
    #[error("Bad Trend Specifier: {0}: {1}, found in channel {2}")]
    BadTrendSpecifier(String, String, String),
    #[error("Error while exporting to '{0}': {1}")]
    Export(String, String),
    #[error("TimeSeriesTree Error: {0}")]
    TimeSeriesTree(TimeSeriesError),
}

impl<T> From<tokio::sync::mpsc::error::SendError<T>> for DTTError {
    fn from(value: tokio::sync::mpsc::error::SendError<T>) -> Self {
        DTTError::TokioMPSCSend(value.to_string())
    }
}

impl From<tokio::task::JoinError> for DTTError {
    fn from(value: tokio::task::JoinError) -> Self {
        DTTError::TokioJoinError(value.to_string())
    }
}

impl<T> From<tokio::sync::watch::error::SendError<T>> for DTTError {
    fn from(value: tokio::sync::watch::error::SendError<T>) -> Self {
        DTTError::TokioWatchSend(value.to_string())
    }
}

impl From<nds_cache_rs::Error> for DTTError {
    fn from(value: nds_cache_rs::Error) -> Self {
        DTTError::NDSCacheError(value.to_string())
    }
}

#[cfg(any(feature = "python", feature = "python-pipe"))]
impl From<DTTError> for pyo3::PyErr {
    fn from(value: DTTError) -> Self {
        pyo3::exceptions::PyRuntimeError::new_err(value.to_string())
    }
}

impl From<TimeSeriesError> for DTTError {
    fn from(value: TimeSeriesError) -> Self {
        Self::TimeSeriesTree(value)
    }
}

impl From<pipelines::PipelineError> for DTTError {
    fn from(value: pipelines::PipelineError) -> Self {
        Self::AnalysisPipelineError(value.to_string())
    }
}
