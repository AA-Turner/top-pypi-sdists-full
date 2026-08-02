pub mod analysis_id;
pub(crate) mod analysis_result;
pub(crate) mod edge_data_type;
pub(crate) mod freq_domain_value;
pub mod record;
pub(crate) mod time_domain_value;

use std::fmt::{Display, Formatter};

pub use analysis_id::{AnalysisId, AnalysisNameId, AnalysisRequestId, AnalysisSettingsId};
pub use analysis_result::AnalysisResult;
pub(crate) use edge_data_type::EdgeDataType;
use time_domain_value::TimeDomainValue::FixedStepArray;

/// Give the result that should be used if a particular edge is sending a result to the app
#[derive(Clone, Debug)]
#[allow(dead_code)]
pub(crate) enum EdgeResultsWrapper {
    TimeDomainReal,
    ASD,
    AnalysisResult,
}

impl Display for EdgeResultsWrapper {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::TimeDomainReal => f.write_str("TimeDomainReal"),
            Self::ASD => f.write_str("ASD"),
            Self::AnalysisResult => f.write_str("AnalysisResult"),
        }
    }
}

pub type ResultsSender = tokio::sync::mpsc::Sender<AnalysisResult>;
pub type ResultsReceiver = tokio::sync::mpsc::Receiver<AnalysisResult>;
