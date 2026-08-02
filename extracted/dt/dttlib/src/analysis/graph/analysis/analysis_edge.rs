use tokio::sync::mpsc;

use crate::{
    analysis::{
        graph::{analysis::OutputSource, scheme::SchemeEdge},
        result::{EdgeDataType, EdgeResultsWrapper},
    },
    data_source::buffer::Buffer,
};

#[derive(Debug)]
pub(crate) struct AnalysisEdge {
    pub(crate) port: usize,
    pub(crate) result_type: EdgeDataType,
    pub(crate) output_source: OutputSource,
    pub(crate) results_wrapper: Option<EdgeResultsWrapper>,
}

impl AnalysisEdge {
    pub(crate) fn new(value: SchemeEdge, result_type: EdgeDataType) -> Self {
        Self {
            port: value.port,
            result_type,
            output_source: Default::default(),
            results_wrapper: value.result_wrapper,
        }
    }

    /// copy another edge, but fail if that edge has output_source == NDSBufferRX, which isn't
    /// cloneable
    pub(super) fn almost_copy(&self) -> Self {
        Self {
            port: self.port,
            result_type: self.result_type.clone(),
            results_wrapper: self.results_wrapper.clone(),
            output_source: self.output_source.almost_copy(),
        }
    }

    /// If the output_source is NDSBufferRx, return the Receiver and set output_source to NotSet, otherwise return a copy
    /// of the output_source as an error so it can be printed out
    /// needed because the Receiver isn't cloneable.
    pub(crate) fn take_nds_buffer_rx(&mut self) -> Result<mpsc::Receiver<Buffer>, OutputSource> {
        let orig_out_source = std::mem::replace(&mut self.output_source, OutputSource::NotSet);
        let (new_source, result) = match orig_out_source {
            OutputSource::BufferRx(rx) => (OutputSource::NotSet, Ok(rx)),
            s => (s.almost_copy(), Err(s)),
        };

        self.output_source = new_source;

        result
    }
}

impl PartialEq for AnalysisEdge {
    fn eq(&self, other: &Self) -> bool {
        self.port == other.port
    }
}

impl PartialOrd for AnalysisEdge {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        if self.port < other.port {
            Some(std::cmp::Ordering::Less)
        } else if self.port > other.port {
            Some(std::cmp::Ordering::Greater)
        } else {
            Some(std::cmp::Ordering::Equal)
        }
    }
}

impl Eq for AnalysisEdge {}

impl Ord for AnalysisEdge {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        return self
            .partial_cmp(other)
            .expect("Partial cmp should not return None");
    }
}
