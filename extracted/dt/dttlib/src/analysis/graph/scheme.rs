#[cfg(feature = "python-pipe")]
use std::collections::HashMap;
use std::fmt::Display;

use crate::analysis::result::EdgeResultsWrapper;
#[cfg(feature = "python-pipe")]
use crate::errors::DTTError;
#[cfg(feature = "python-pipe")]
use crate::params::custom_pipeline::CustomPipeline;
#[cfg(feature = "python-pipe")]
use crate::run_context::RunContext;
use ligo_hires_gps_time::PipDuration;
use petgraph::graph::Graph;

/// Analysis single pipeline node
#[derive(Clone, Debug)]
#[allow(dead_code)]
pub enum SchemePipelineType<'a> {
    DataSource,
    Conditioning,
    ASD,
    FFT,
    Identity,
    Downsample,
    Average,
    /// the argument is the name of the custom pipeline
    #[cfg(feature = "python-pipe")]
    Custom(&'a CustomPipeline),
    /// this type only exists to have reference when not built with python.
    /// the value is never used.
    Dummy(&'a str),
    Results,
    /// send results to a ScopeView command task
    /// meant to be stored by the view as a reference for later
    /// Separate from Results node so that different results can be sent to app
    /// than what the view stores.
    StoreResultsToView,
    /// # per-channel source nodes into a cross-channel scheme
    /// for the A channel
    PerChannelASource(String),
    /// for the B channel
    PerChannelBSource(String),
    Splice,

    InlineFFT,
    CSD,
    Real,
    Sqrt,
    /// Combine a real and an imaginary into a complex signal.
    Complex,
    /// Get the phase of a complex signal
    Phase,

    /// shifts time stamp earlier by shift
    /// can be negative
    TimeShift {
        shift: PipDuration,
    },
}

impl<'a> Display for SchemePipelineType<'a> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SchemePipelineType::DataSource => write!(f, "data source"),
            SchemePipelineType::Conditioning => write!(f, "conditioning"),
            SchemePipelineType::Identity => write!(f, "identity"),
            SchemePipelineType::ASD => write!(f, "ASD"),
            SchemePipelineType::FFT => write!(f, "FFT"),
            SchemePipelineType::Average => write!(f, "average"),
            #[cfg(feature = "python-pipe")]
            SchemePipelineType::Custom(c) => write!(f, "Custom pipeline '{}'", c.name),
            SchemePipelineType::Dummy(_) => write!(f, "dummy"),
            SchemePipelineType::Results => write!(f, "results"),
            SchemePipelineType::StoreResultsToView => write!(f, "store results to view"),
            SchemePipelineType::PerChannelASource(n) => write!(f, "A:{}", n),
            SchemePipelineType::PerChannelBSource(n) => write!(f, "B:{}", n),
            SchemePipelineType::Splice => write!(f, "splice"),
            SchemePipelineType::Downsample => write!(f, "downsample"),
            SchemePipelineType::InlineFFT => write!(f, "inline FFT"),
            SchemePipelineType::CSD => write!(f, "coss-spectral density"),
            SchemePipelineType::Real => write!(f, "real"),
            SchemePipelineType::Sqrt => write!(f, "sqrt"),
            SchemePipelineType::Complex => write!(f, "complex"),
            SchemePipelineType::Phase => write!(f, "phase"),
            SchemePipelineType::TimeShift { shift } => write!(f, "time_shift({})", shift),
        }
    }
}

impl<'a> SchemePipelineType<'a> {
    /// number of input ports
    pub fn port_count(&self) -> Option<usize> {
        let port_num = match self {
            SchemePipelineType::DataSource => 0,
            SchemePipelineType::Conditioning => 1,
            SchemePipelineType::ASD => 1,
            SchemePipelineType::FFT => 1,
            SchemePipelineType::Average => 1,
            SchemePipelineType::Identity => 1,
            #[cfg(feature = "python-pipe")]
            SchemePipelineType::Custom(c) => c.port_count(),
            SchemePipelineType::Dummy(_) => 0,
            SchemePipelineType::Results => return None,
            SchemePipelineType::StoreResultsToView => return None,
            SchemePipelineType::PerChannelASource(_) => 0,
            SchemePipelineType::PerChannelBSource(_) => 0,
            SchemePipelineType::Splice => 1,
            SchemePipelineType::Downsample => 1,
            SchemePipelineType::InlineFFT => 1,
            SchemePipelineType::CSD => 2,
            SchemePipelineType::Real => 1,
            SchemePipelineType::Sqrt => 1,
            SchemePipelineType::Complex => 2,
            SchemePipelineType::Phase => 1,
            SchemePipelineType::TimeShift { shift: _ } => 1,
        };
        Some(port_num)
    }
}

#[derive(Clone)]
pub struct SchemeNode<'a> {
    pub pipeline_type: SchemePipelineType<'a>,
    pub name: String,
    /// When an AnalysisNode is created from this node
    /// this field is used to create teh AnalysisId associated
    /// with the pipeline that will eventually be created
    /// from teh analysis node.
    ///
    /// If None, then the node's id is the same as the <input_id_1> for port 1
    /// If Some(<tag>) then the id is <tag>(<input_id_1>, <input_id_2>, ... )
    pub id_tag: Option<String>,
}

impl<'a> SchemeNode<'a> {
    pub fn new(name: impl Into<String>, pipeline_type: SchemePipelineType<'a>) -> Self {
        Self {
            name: name.into(),
            pipeline_type,
            id_tag: None,
        }
    }
}

#[derive(Clone)]
pub struct SchemeEdge {
    /// 0-based port of destination node that receives the value from the source
    pub port: usize,
    /// Which kind of result should be sent on this edge to the app.
    pub result_wrapper: Option<EdgeResultsWrapper>,
}

impl SchemeEdge {
    pub(crate) fn new(port: usize) -> Self {
        Self {
            port,
            result_wrapper: None,
        }
    }

    pub(crate) fn set_result_wrapper(mut self, result_wrapper: EdgeResultsWrapper) -> Self {
        self.result_wrapper = Some(result_wrapper);
        self
    }
}

pub(crate) type SchemeGraph<'a> = Graph<SchemeNode<'a>, SchemeEdge>;

#[cfg(feature = "python-pipe")]
pub fn add_custom_pipelines<'a>(
    rc: &'_ Box<RunContext>,
    graph: &'_ mut SchemeGraph<'a>,
    custom_pipes: &'a [CustomPipeline],
) -> Result<(), DTTError> {
    let mut name_map = HashMap::new();

    for node_idx in graph.node_indices() {
        let name = graph
            .node_weight(node_idx)
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot add custom pipeline when a node has no weight".to_string(),
                )
            })?
            .name
            .clone();

        name_map.insert(name, node_idx);
    }

    let results_idx = name_map
        .get("results")
        .ok_or(DTTError::AnalysisPipelineError(
            "Scheme graph must have results node".to_string(),
        ))?
        .clone();

    // populate the nodes
    for custom_pipe in custom_pipes {
        let name = custom_pipe.name.clone();

        let new_idx = graph.add_node(SchemeNode::new(
            name.clone(),
            SchemePipelineType::<'a>::Custom(custom_pipe),
        ));

        if name_map.contains_key(&name) {
            let msg = format!(
                "Two pipelines with the name {} were found. Names must be unique.",
                name
            );
            rc.user_messages
                .set_error("DuplicateCustomPipeName", msg.clone());
            return Err(DTTError::AnalysisPipelineError(msg));
        }

        name_map.insert(name, new_idx);
    }

    rc.user_messages.clear_message("DuplicateCustomPipeName");

    // populate the edges
    for custom_pipe in custom_pipes {
        let target_idx = name_map
            .get(&custom_pipe.name)
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(format!(
                    "name map did not contain custom pipe name '{}'",
                    &custom_pipe.name
                ))
            })?
            .clone();
        let mut port = 1;
        for in_name in &custom_pipe.inputs {
            if !name_map.contains_key(in_name) {
                let msg = format! {"Input name '{}' on custom pipeline '{}' does not exist.", in_name, custom_pipe.name.clone()};
                rc.user_messages
                    .set_error("MissingCustomInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
            let source_idx = name_map
                .get(in_name)
                .ok_or_else(|| {
                    DTTError::AnalysisPipelineError(format!(
                        "name map did not contain custom pipe name (2) '{}'",
                        in_name
                    ))
                })?
                .clone();
            graph.add_edge(source_idx, target_idx, SchemeEdge::new(port));
            port += 1;
        }

        // all custom pipelines generate results
        graph.add_edge(
            target_idx,
            results_idx,
            SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::AnalysisResult),
        );
    }

    rc.user_messages.clear_message("MissingCustomInput");

    Ok(())
}
