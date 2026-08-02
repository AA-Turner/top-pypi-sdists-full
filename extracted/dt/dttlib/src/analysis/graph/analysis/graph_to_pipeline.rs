use ligo_hires_gps_time::PipDuration;
use petgraph::graph::EdgeIndex;
use petgraph::graph::NodeIndex;
use petgraph::visit::{EdgeRef, Topo};
use petgraph::{Incoming, Outgoing};

#[cfg(feature = "python-pipe")]
use pipelines::python;

use pipelines::PipelineSubscriber;

use crate::analysis;
use crate::analysis::graph::analysis::AnalysisEdge;
use user_messages::UserMsgProvider;

use crate::analysis::conditioning::convert::start_pipe_converter;
#[cfg(feature = "python-pipe")]
use crate::analysis::result::analysis_result::AnalysisResult;
use crate::analysis::result::analysis_result::{analysis_result_sender, analysis_result_wrapper};

use crate::analysis::conditioning::time_shift::start_timeshift;
use crate::analysis::fourier_tools::asd::ASD;
use crate::analysis::fourier_tools::fft::FFT;
use crate::analysis::graph::analysis::{AnalysisGraph, OutputSource};
use crate::analysis::graph::scheme::SchemePipelineType;
use crate::analysis::result::{EdgeResultsWrapper, ResultsReceiver};
use crate::analysis::types::time_domain_array::TimeDomainArray;
use crate::data_source::DataSourceRef;
use crate::data_source::data_distributor::add_distributor_to_graph;
use crate::errors::DTTError;
use crate::params::channel_params::channel::Channel;
#[cfg(feature = "python-pipe")]
use crate::params::custom_pipeline::CustomPipeline;
use crate::params::test_params::AverageType;
use crate::run_context::RunContext;
use crate::timeline::Timeline;

impl<'a> AnalysisGraph<'a> {
    /// create the entire set of analysis pipelines from a graph and data source
    /// This is specifically DTT analysis graph from a DTT pipeline.
    /// Scope windows have a separate function for converting graphs to pipelines
    pub(crate) async fn graph_to_dtt_pipeline(
        &mut self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        data_source: &DataSourceRef,
    ) -> Result<ResultsReceiver, DTTError> {
        let mut topo = Topo::new(&**self);

        let mut final_out = Err(DTTError::AnalysisPipelineError(
            "pipeline creation terminated without processing the results node".to_string(),
        ));

        loop {
            let node_idx = match topo.next(&**self) {
                None => break,
                Some(n) => n,
            };
            let node = match self.node_weight(node_idx) {
                Some(n) => n,
                None => return Err(DTTError::AnalysisPipelineError(
                    "node not in graph, though it was found in a topological sort of the same graph."
                        .to_string(),
                )),
            };

            match node.pipeline_type {
                SchemePipelineType::DataSource => {
                    let chan_records: Vec<Channel> = timeline
                        .all_channels()
                        .into_iter()
                        .map(|x| x.channel.clone())
                        .collect();

                    let block_rx = data_source.stream_data(
                        rc.clone(),
                        chan_records.as_slice(),
                        timeline.extended_start_time_pip()?,
                        timeline.extended_end_time_pip()?,
                    )?;

                    add_distributor_to_graph(rc, self, node_idx, block_rx)?
                }
                SchemePipelineType::Results => {
                    let out = self.wrap_results(rc, node_idx).await;
                    final_out = out;
                }
                SchemePipelineType::StoreResultsToView => {
                    let msg = format!(
                        "{} is a 'store results to view' pipeline. 'Store results to view pipelines' can't be used.",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Average => {
                    self.create_average(rc, timeline.test_params.average_type.clone(), node_idx)
                        .await?
                }
                SchemePipelineType::Identity => {
                    self.create_identity(rc, timeline, node_idx).await?
                }
                SchemePipelineType::Conditioning => {
                    self.create_view_conditioning(rc, timeline, node_idx)
                        .await?
                }
                SchemePipelineType::FFT => self.create_fft(rc, timeline, node_idx).await?,
                SchemePipelineType::ASD => self.create_asd(rc, timeline, node_idx).await?,
                SchemePipelineType::PerChannelBSource(_)
                | SchemePipelineType::PerChannelASource(_) => {
                    let node_name = node.name.clone();
                    let msg = format!(
                        "PerChannel node {} should have been elided before creating pipelines.",
                        node_name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                #[cfg(feature = "python-pipe")]
                SchemePipelineType::Custom(c) => {
                    self.create_custom_1_input(rc, timeline, node_idx, c)
                        .await?
                }
                SchemePipelineType::Dummy(_) => {
                    let msg = format!(
                        "{} is a Dummy pipeline. Dummy pipeline can't be used.",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Splice => {
                    let msg = format!(
                        "Splice pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Downsample => {
                    let msg = format!(
                        "Downsample pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::InlineFFT => {
                    let msg = format!(
                        "InlineFFT pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Real => {
                    let msg = format!(
                        "Real pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::CSD => {
                    let msg = format!(
                        "CSD pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Sqrt => {
                    let msg = format!(
                        "Sqrt pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Complex => {
                    let msg = format!(
                        "Complex pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::Phase => {
                    let msg = format!(
                        "Phase pipeline {} is not supported for DTT type analysis",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                SchemePipelineType::TimeShift { shift } => {
                    self.create_timeshift(rc, node_idx, shift).await?
                }
            }
        }
        final_out
    }

    pub(crate) async fn wrap_results(
        &self,
        rc: &'_ Box<RunContext>,
        node_idx: NodeIndex,
    ) -> Result<ResultsReceiver, DTTError> {
        let (results_tx, results_rx) = tokio::sync::mpsc::channel(128);

        let edges: Vec<_> = self
            .edges_directed(node_idx, Incoming)
            .map(|e| e.id())
            .collect();
        for edge_idx in edges {
            let edge = self.edge_weight(edge_idx).ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot convert graph to pipeline when an edge has no weight".to_string(),
                )
            })?;
            match &edge.results_wrapper {
                Some(EdgeResultsWrapper::ASD) => match &edge.output_source {
                    OutputSource::PipelineFreqArrayFloat64(x) => {
                        analysis_result_wrapper(rc, &x, results_tx.clone()).await?
                    }
                    s => {
                        let msg = format!(
                            "An ASD result requires a real-valued frequency array as output, but was {}",
                            s
                        );
                        rc.user_messages.set_error("WrongResultType", msg.clone());
                        return Err(DTTError::AnalysisPipelineError(msg));
                    }
                },
                Some(EdgeResultsWrapper::AnalysisResult) => match &edge.output_source {
                    OutputSource::PipelineResultValue(x) => {
                        analysis_result_sender(rc, &x, results_tx.clone()).await?;
                    }
                    s => {
                        let msg = format!(
                            "A general result requires a Result-value as output, but was {}",
                            s
                        );
                        rc.user_messages.set_error("WrongResultType", msg.clone());
                        return Err(DTTError::AnalysisPipelineError(msg));
                    }
                },
                Some(EdgeResultsWrapper::TimeDomainReal) => match &edge.output_source {
                    OutputSource::PipelineTDArrayFloat64(x) => {
                        analysis_result_wrapper(rc, x, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayInt8(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayInt16(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayInt32(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayInt64(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayUInt8(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayUInt16(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayUInt32(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    OutputSource::PipelineTDArrayUInt64(x) => {
                        let convert_subscriber: PipelineSubscriber<TimeDomainArray<f64>> =
                            start_pipe_converter(rc.clone(), "result_conversion", x).await?;
                        analysis_result_wrapper(rc, &convert_subscriber, results_tx.clone()).await?
                    }
                    s => {
                        let msg = format!(
                            "A real time-domain result requires a real-valued time domain array as output, but was {}",
                            s
                        );
                        rc.user_messages.set_error("WrongResultType", msg.clone());
                        return Err(DTTError::AnalysisPipelineError(msg));
                    }
                },
                // Some(r) => {
                //     let msg = format!("analysis pipeline result wrapper {} is not implemented.", r);
                //     rc.user_messages.set_error("WrongResultType", msg);
                // },
                None => {
                    let msg = "No result wrapper was specified.".to_string();
                    rc.user_messages.set_error("WrongResultType", msg.clone());
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
            }
        }

        rc.user_messages.clear_message("WrongResultType");

        Ok(results_rx)
    }

    pub(crate) fn get_only_incoming_edge(
        &self,
        node_idx: NodeIndex,
    ) -> Result<EdgeIndex, DTTError> {
        Ok(self
            .edges_directed(node_idx, Incoming)
            .next()
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "cannot get incoming edge on a node with no edge".to_string(),
                )
            })?
            .id())
    }

    pub(crate) fn get_incoming_edges(&self, node_idx: NodeIndex) -> Vec<EdgeIndex> {
        self.edges_directed(node_idx, Incoming)
            .map(|e| e.id())
            .collect()
    }

    /// return a list of edge indexes ordered by "to" port number.
    ///
    /// Returns an error if expected_edge_count is not None and the count doesn't match.
    /// Returns an error if there's a missing or duplicat port number.
    pub(crate) fn get_ordered_incoming_edge_indexes(
        &'a self,
        node_idx: NodeIndex,
        expected_edge_count: Option<usize>,
    ) -> Result<Vec<EdgeIndex>, DTTError> {
        let mut indexes = self.get_incoming_edges(node_idx);

        if let Some(n) = expected_edge_count {
            if indexes.len() != n {
                return Err(DTTError::AnalysisPipelineError(format!(
                    "Expected {} incoming edges but got {} for node '{}'",
                    n,
                    indexes.len(),
                    self.get_node_name(node_idx)?
                )));
            }
        }

        indexes.sort_by(|a, b| {
            let w_a = self
                .edge_weight(*a)
                .expect("weightless nodes not allowed on incoming edges");
            let w_b = self
                .edge_weight(*b)
                .expect("weightless nodes not allowed on incoming edges");
            w_a.cmp(w_b)
        });

        Ok(indexes)
    }

    /// return a list of edge weights ordered by "to" port number.
    ///
    /// Returns an error if expected_edge_count is not None and the count doesn't match.
    /// Returns an error if there's a missing or duplicate port number.
    pub(crate) fn get_ordered_incoming_edges(
        &'a self,
        node_idx: NodeIndex,
        expected_edge_count: Option<usize>,
    ) -> Result<Vec<&'a AnalysisEdge>, DTTError> {
        let indexes = self.get_ordered_incoming_edge_indexes(node_idx, expected_edge_count)?;

        let edges_opt: Option<Vec<_>> = indexes.into_iter().map(|i| self.edge_weight(i)).collect();
        let edges = edges_opt.ok_or_else(|| {
            DTTError::AnalysisPipelineError(format!(
                "Found an edge without a weight into node '{}'",
                self.get_node_name(node_idx).unwrap_or("<not_found>")
            ))
        })?;

        for (i, edge) in edges.iter().enumerate() {
            if i + 1 != edge.port {
                return Err(DTTError::AnalysisPipelineError(format!(
                    "Edge with port #{} was found on port #{} on node '{}'",
                    edge.port,
                    i + 1,
                    self.get_node_name(node_idx)?
                )));
            }
        }

        Ok(edges)
    }

    pub(crate) fn get_node_name(&self, node_idx: NodeIndex) -> Result<&str, DTTError> {
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(format!(
                "Couldn't get weight for node while trying to find its name"
            ))
        })?;

        Ok(&node.name)
    }

    /// write the output source to every outgoing edge of a node
    pub(crate) fn populate_output_source(
        &mut self,
        node_idx: NodeIndex,
        output_source: &OutputSource,
    ) -> Result<(), DTTError> {
        let edges: Vec<_> = self
            .edges_directed(node_idx, Outgoing)
            .map(|e| e.id())
            .collect();
        for edge_idx in edges {
            let edge_weight = self.edge_weight_mut(edge_idx).ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot populate output source when an edge has no weight".to_string(),
                )
            })?;
            edge_weight.output_source = output_source.almost_copy();
        }
        Ok(())
    }

    /// simply pass the input into the output
    async fn create_identity(
        &mut self,
        _rc: &Box<RunContext>,
        _timeline: &Timeline,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create identity when an edge has no weight".to_string(),
            )
        })?;

        let out_source = edge.output_source.almost_copy();

        self.populate_output_source(node_idx, &out_source)
    }

    // time shift the input to the output
    pub(crate) async fn create_timeshift(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: NodeIndex,
        shift: PipDuration,
    ) -> Result<(), DTTError> {
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create timeshift when a node has no weight".to_string(),
            )
        })?;
        let node_name = node.name.clone();
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create timeshift when an edge has no weight".to_string(),
            )
        })?;

        // shift trends later in time by 1/2 step to make their time stamps centered in the time
        // region they summarize
        //
        // this is just period/2, but a more correct formula would be period *  (n-1)/2*n)
        // where n is the number of points per region.

        let out_source = match &edge.output_source {
            OutputSource::PipelineTDArrayInt8(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayInt8(p)
            }
            OutputSource::PipelineTDArrayInt16(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayInt16(p)
            }
            OutputSource::PipelineTDArrayInt32(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayInt32(p)
            }
            OutputSource::PipelineTDArrayInt64(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayInt64(p)
            }
            OutputSource::PipelineTDArrayUInt8(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayUInt8(p)
            }
            OutputSource::PipelineTDArrayUInt16(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayUInt16(p)
            }
            OutputSource::PipelineTDArrayUInt32(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayUInt32(p)
            }
            OutputSource::PipelineTDArrayUInt64(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayUInt64(p)
            }
            OutputSource::PipelineTDArrayFloat64(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayFloat64(p)
            }
            OutputSource::PipelineTDArrayComplex128(f) => {
                let p = start_timeshift(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        &node_name
                    ),
                    shift,
                    f,
                )
                .await?;
                OutputSource::PipelineTDArrayComplex128(p)
            }
            s => {
                let msg = format!(
                    "Time-shfit on node {} must be a time domain value.  Got {}",
                    node_name, s
                );
                rc.user_messages
                    .set_error("TimeShiftWrongInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        }
        .into();

        rc.user_messages.clear_message("TimeShiftWrongInput");

        self.populate_output_source(node_idx, &out_source)
    }

    pub(crate) async fn create_average(
        &mut self,
        rc: &Box<RunContext>,
        average_type: AverageType,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let (source_idx, _) = self.edge_endpoints(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create average when an edge has no endpoints".to_string(),
            )
        })?;

        let avg_name = self
            .node_weight(source_idx)
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot create average when an node has no weight".to_string(),
                )
            })?
            .name
            .clone()
            + ".avg";

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create average when an node has no weight (2)".to_string(),
            )
        })?;

        let node_name = node.name.clone();

        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create average when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match average_type {
            AverageType::Fixed => match &edge.output_source {
                OutputSource::NotSet
                | OutputSource::BufferRx(_)
                | OutputSource::PipelineTDArrayComplex128(_)
                | OutputSource::PipelineTDArrayFloat64(_)
                | OutputSource::PipelineTDArrayInt64(_)
                | OutputSource::PipelineTDArrayInt32(_)
                | OutputSource::PipelineTDArrayInt16(_)
                | OutputSource::PipelineTDArrayInt8(_)
                | OutputSource::PipelineTDArrayUInt64(_)
                | OutputSource::PipelineTDArrayUInt32(_)
                | OutputSource::PipelineTDArrayUInt16(_)
                | OutputSource::PipelineTDArrayUInt8(_)
                | OutputSource::PipelineResultValue(_) => {
                    let msg = format!(
                        "Average node {} requires an addable pipeline input",
                        node_name
                    );
                    rc.user_messages.set_error("MissingInput", msg.clone());
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
                OutputSource::PipelineFreqArrayFloat64(p) => {
                    rc.user_messages.clear_message("MissingInput");
                    let avg_pipe =
                        analysis::arithmetic::average::create(rc.clone(), avg_name, &p).await?;
                    OutputSource::PipelineFreqArrayFloat64(avg_pipe)
                }
                OutputSource::PipelineFreqArrayComplex128(p) => {
                    rc.user_messages.clear_message("MissingInput");
                    let avg_pipe =
                        analysis::arithmetic::average::create(rc.clone(), avg_name, &p).await?;
                    OutputSource::PipelineFreqArrayComplex128(avg_pipe)
                }
            },
            a => {
                return Err(DTTError::UnimplementedOption(
                    "Average type".to_string(),
                    a.to_string(),
                ));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_view_conditioning(
        &mut self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create conditioning when an edge has no weight".to_string(),
            )
        })?;
        let in_source_result = edge.take_nds_buffer_rx();
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create conditioning when a node has no weight".to_string(),
            )
        })?;
        let channel = &node
            .id
            .clone()
            .expect("condition pipeline should always have an id")
            .first_channel()?;

        let node_name = node.name.clone();

        let buffer_rx = match in_source_result {
            Ok(r) => r,
            Err(s) => {
                let msg = format!(
                    "Conditioning pipeline {} only accepts NDS buffer pipes as input but got {}",
                    node_name, s
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        let out_source = channel
            .create_conditioning_pipeline(rc, timeline, buffer_rx)
            .await?
            .into();

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_fft(
        &mut self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create fft when a node has no weight".to_string(),
            )
        })?;
        let node_name = node.name.clone();
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create fft when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::PipelineTDArrayFloat64(t) => {
                FFT::create(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        ":fft(real)"
                    ),
                    timeline,
                    t,
                )
                .await?
            }
            OutputSource::PipelineTDArrayComplex128(t) => {
                FFT::create(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        ":fft(complex)"
                    ),
                    timeline,
                    t,
                )
                .await?
            }
            s => {
                let msg = format!(
                    "FFT input on node {} must be time domain.  Got {}",
                    node_name, s
                );
                rc.user_messages.set_error("FFTWrongInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        }
        .into();

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_asd(
        &mut self,
        rc: &Box<RunContext>,
        timeline: &Timeline,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create ASD when a node has no weight".to_string(),
            )
        })?;
        let node_name = node.name.clone();
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create ASD when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::PipelineFreqArrayComplex128(f) => {
                ASD::create(
                    rc.ump_clone(),
                    format!(
                        "{}{}",
                        node.id
                            .clone()
                            .expect("timeshift should always have a node id"),
                        ":asd"
                    ),
                    timeline.heterodyned,
                    f,
                )
                .await?
            }
            s => {
                let msg = format!(
                    "FFT input on node {} must be a complex frequency domain value.  Got {}",
                    node_name, s
                );
                rc.user_messages.set_error("FFTWrongInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        }
        .into();

        self.populate_output_source(node_idx, &out_source)
    }

    #[cfg(feature = "python-pipe")]
    async fn create_custom_1_input(
        &mut self,
        rc: &Box<RunContext>,
        _timeline: &Timeline,
        node_idx: NodeIndex,
        custom_pipeline: &CustomPipeline,
    ) -> Result<(), DTTError> {
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create custom-1-input when a node has no weight".to_string(),
            )
        })?;
        let node_name = node.name.clone();
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create custom-1-input when an edge has no weight".to_string(),
            )
        })?;

        let wrapped_in_source = edge
            .output_source
            .to_value_pipeline(rc, node_name.clone() + ".input_wrapper")
            .await?;

        let out_pipe: PipelineSubscriber<AnalysisResult> = python::PythonPipeState::create(
            rc.ump_clone(),
            node_name,
            custom_pipeline.py_module.as_ref(),
            &wrapped_in_source,
        )
        .await?;

        let out_source = out_pipe.into();
        self.populate_output_source(node_idx, &out_source)
    }
}
