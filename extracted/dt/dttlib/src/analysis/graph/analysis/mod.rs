//! the actual analysis graph, built up from scheme graphs and a test timeline
mod analysis_edge;
mod analysis_node;
mod graph_to_pipeline;
mod output_source;
mod view_graph_to_pipeline;

use crate::analysis::graph::scheme::{SchemeGraph, SchemePipelineType};

use crate::analysis::result::EdgeDataType;

use crate::AnalysisSettingsId;
use crate::errors::DTTError;
use crate::params::channel_params::ChannelSettings;
use crate::params::channel_params::channel::Channel;
use crate::params::channel_params::nds_data_type::NDSDataType::Float32;
use crate::run_context::RunContext;
use ligo_hires_gps_time::PipDuration;
use petgraph::algo::{connected_components, toposort};
use petgraph::graph::NodeIndex;
use petgraph::visit::{EdgeRef, Topo};
use petgraph::{Directed, Direction, Graph};
use std::collections::{HashMap, HashSet};
use std::fmt::{Debug, Formatter};
use std::ops::{Deref, DerefMut};

pub(crate) use analysis_edge::AnalysisEdge;
pub(crate) use analysis_node::AnalysisNode;
pub(crate) use output_source::OutputSource;

type AnalysisGraphType<'a> = Graph<AnalysisNode<'a>, AnalysisEdge, Directed>;
pub(crate) struct AnalysisGraph<'a>(AnalysisGraphType<'a>);

impl<'a> Deref for AnalysisGraph<'a> {
    type Target = AnalysisGraphType<'a>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<'a> DerefMut for AnalysisGraph<'a> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Debug for AnalysisGraph<'_> {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        self.0.fmt(f)
    }
}

impl<'a> AnalysisGraph<'a> {
    pub(crate) fn new() -> Self {
        Self(AnalysisGraphType::<'_>::new())
    }

    pub(crate) fn extend_graph(
        &mut self,
        base_map: &'_ mut HashMap<AnalysisNode<'a>, NodeIndex>,
        other_graph: &'_ AnalysisGraph<'a>,
    ) -> Result<(), DTTError> {
        // A mapping from node index in other_graph to corresponding node index in the base graph
        let mut idx_map = HashMap::new();

        for node_idx in other_graph.node_indices() {
            let node = match other_graph.node_weight(node_idx) {
                Some(n) => n,
                None => {
                    return Err(DTTError::AnalysisPipelineError(
                        "Can't extend from graph node that has no wieght".to_string(),
                    ));
                }
            }
            .clone();

            let base_idx = if base_map.contains_key(&node) {
                base_map
                    .get(&node)
                    .expect("basemap must contain the node")
                    .clone()
            } else {
                self.add_node(node.clone())
            };

            base_map.insert(node, base_idx);

            idx_map.insert(node_idx, base_idx);
        }

        for edge_idx in other_graph.edge_indices() {
            let edge = match other_graph.edge_weight(edge_idx) {
                Some(e) => e,
                None => {
                    return Err(DTTError::AnalysisPipelineError(
                        "Can't extend graph edge that has no weight".to_string(),
                    ));
                }
            };
            let (source, target) = match other_graph.edge_endpoints(edge_idx) {
                Some(i) => i,
                None => {
                    return Err(DTTError::AnalysisPipelineError(
                        "Cannot extend graph using an edge with no endpoints".to_string(),
                    ));
                }
            };

            let a = match idx_map.get(&source) {
                Some(n) => n,
                None => {
                    return Err(DTTError::AnalysisPipelineError(
                        "node A not found in temporary map while extending graph".to_string(),
                    ));
                }
            }
            .clone();
            let b = match idx_map.get(&target) {
                Some(n) => n,
                None => {
                    return Err(DTTError::AnalysisPipelineError(
                        "node A not found in temporary map while extending graph".to_string(),
                    ));
                }
            }
            .clone();

            self.add_edge(a, b, edge.almost_copy());
        }
        Ok(())
    }

    pub(crate) fn set_result_types(&mut self) -> Result<(), DTTError> {
        let mut topo = Topo::new(&**self);

        loop {
            let next = match topo.next(&**self) {
                None => break,
                Some(n) => n,
            };
            self.determine_result_type(next)?;
        }
        Ok(())
    }

    pub(crate) fn from_per_channel_scheme(
        channel: &'_ ChannelSettings,
        scheme_graph: &'_ SchemeGraph<'a>,
    ) -> Result<Self, DTTError> {
        let mut analysis_to_scheme = HashMap::with_capacity(scheme_graph.node_count());

        let mut new_graph = AnalysisGraph::new();
        let (nodes, edges) = scheme_graph.clone().into_nodes_edges();
        for node in nodes {
            let a_node = new_graph.add_node(AnalysisNode::from_scheme_node(&node.weight));
            analysis_to_scheme.insert(a_node, node);
        }
        for edge in edges {
            // set every edge to the same result type,
            // but we only really care about the DataSource -> Conditioning edge.
            // Every other edge will be set again by determine_result_type()
            new_graph.add_edge(
                edge.source(),
                edge.target(),
                AnalysisEdge::new(edge.weight, channel.data_type().into()),
            );
        }

        // fix all types
        let mut topo = Topo::new(&*new_graph);

        loop {
            let next = match topo.next(&*new_graph) {
                None => break,
                Some(n) => n,
            };

            let inputs_idx = new_graph.get_ordered_incoming_edge_indexes(next, None)?;

            let node_type = new_graph
                .node_weight(next)
                .expect("node must have a weight")
                .pipeline_type
                .clone();

            let id = match node_type {
                SchemePipelineType::DataSource
                | SchemePipelineType::Results
                | SchemePipelineType::StoreResultsToView => None, // must be None so that later code will merge nodes (Hash will be the same).
                _ => {
                    if inputs_idx.is_empty() {
                        None
                    } else {
                        let scheme_node = analysis_to_scheme
                            .get(&next)
                            .expect("since this was mapped earlier in the function, it must exist");
                        Some(match &scheme_node.weight.id_tag {
                            Some(name) => {
                                let args = inputs_idx
                                    .iter()
                                    .map(|e| {
                                        new_graph
                                            .node_weight(
                                                new_graph
                                                    .edge_endpoints(*e)
                                                    .expect("edge recently created so should exist")
                                                    .0,
                                            )
                                            .expect("created node must have a weight")
                                            .id
                                            .clone()
                                            .expect("input node must have an id")
                                    })
                                    .collect();
                                AnalysisSettingsId::Compound {
                                    name: name.clone(),
                                    args,
                                }
                            }
                            None => {
                                // take the id from tine input
                                // or create a simple one froma channel if there is no input id
                                let (in_node_0, _) = new_graph
                                    .edge_endpoints(inputs_idx[0])
                                    .expect("there must be nodes for this edge");
                                match new_graph
                                    .node_weight(in_node_0)
                                    .expect("node known to exist already")
                                    .id
                                    .clone()
                                {
                                    None => {
                                        AnalysisSettingsId::from_channel(channel.clone().into())
                                    }
                                    Some(id) => id,
                                }
                            }
                        })
                    }
                }
            };

            new_graph
                .node_weight_mut(next)
                .expect("mapped node must have a weight")
                .id = id;

            new_graph.determine_result_type(next)?;
        }

        Ok(new_graph)
    }

    pub(crate) fn from_cross_channel_scheme(
        a_channel: &'_ ChannelSettings,
        b_channel: &'_ ChannelSettings,
        scheme_graph: &'_ SchemeGraph<'a>,
    ) -> Result<Self, DTTError> {
        let mut analysis_to_scheme = HashMap::with_capacity(scheme_graph.node_count());

        let mut new_graph = AnalysisGraph::new();
        let (nodes, edges) = scheme_graph.clone().into_nodes_edges();
        for node in nodes {
            let a_node = new_graph.add_node(AnalysisNode::from_scheme_node(&node.weight));
            analysis_to_scheme.insert(a_node, node);
        }

        for edge in edges {
            // for cross channel graphs, the initial edge types don't matter, since they will all be
            // set by determine_result_type()
            new_graph.add_edge(
                edge.source(),
                edge.target(),
                AnalysisEdge::new(edge.weight, EdgeDataType::TimeDomainValueReal),
            );
        }

        // fix all types
        let mut topo = Topo::new(&*new_graph);

        loop {
            let next = match topo.next(&*new_graph) {
                None => break,
                Some(n) => n,
            };

            let inputs_idx = new_graph.get_ordered_incoming_edge_indexes(next, None)?;

            let node_type = new_graph
                .node_weight(next)
                .expect("node must have a weight")
                .pipeline_type
                .clone();

            let id = match node_type {
                SchemePipelineType::DataSource
                | SchemePipelineType::Results
                | SchemePipelineType::StoreResultsToView => None, // must be None so that later code will merge nodes (Hash will be the same).
                _ => {
                    if inputs_idx.is_empty() {
                        // the beginning of the cross-channel graph
                        // in this case, the scheme node must have an id tag, and we assume
                        // the channels are the inputs

                        let scheme_node = analysis_to_scheme
                            .get(&next)
                            .expect("a mapped node must exist");
                        let tag = scheme_node.weight.id_tag.clone().ok_or_else(|| {
                            DTTError::AnalysisPipelineError(format!(
                                "Leading node '{}' in the cross-channel scheme must have a tag",
                                scheme_node.weight.name
                            ))
                        })?;
                        let a_id = AnalysisSettingsId::from_channel(a_channel.clone());
                        let b_id = AnalysisSettingsId::from_channel(b_channel.clone());
                        Some(AnalysisSettingsId::Compound {
                            name: tag,
                            args: vec![a_id, b_id],
                        })
                    } else {
                        let scheme_node = analysis_to_scheme
                            .get(&next)
                            .expect("since this was mapped earlier in the function, it must exist");
                        Some(match &scheme_node.weight.id_tag {
                            Some(name) => {
                                let args = inputs_idx
                                    .iter()
                                    .map(|e| {
                                        new_graph
                                            .node_weight(
                                                new_graph
                                                    .edge_endpoints(*e)
                                                    .expect("edge recently created so should exist")
                                                    .0,
                                            )
                                            .expect("created node must have a weight")
                                            .id
                                            .clone()
                                            .expect("input node must have an id")
                                    })
                                    .collect();
                                AnalysisSettingsId::Compound {
                                    name: name.clone(),
                                    args,
                                }
                            }
                            None => {
                                let (in_node_0, _) = new_graph
                                    .edge_endpoints(inputs_idx[0])
                                    .expect("there must be nodes for this edge");
                                new_graph
                                    .node_weight(in_node_0)
                                    .expect("node known to exist already")
                                    .id
                                    .clone()
                                    .ok_or_else(|| DTTError::AnalysisPipelineError(format!("")))?
                                    .clone()
                            }
                        })
                    }
                }
            };

            new_graph
                .node_weight_mut(next)
                .expect("mapped node must have a weight")
                .id = id;

            new_graph.determine_result_type(next)?;
        }

        Ok(new_graph)
    }

    /// Get the result types for the sources of a node,
    /// Returning an error if the count of sources doesn't match the
    /// given value
    fn get_sources(&self, n: NodeIndex, num_sources: usize) -> Result<Vec<EdgeDataType>, DTTError> {
        let source_types: Vec<_> = self
            .edges_directed(n, Direction::Incoming)
            .map(|x| x.weight().result_type.clone())
            .collect();
        let pipe_type = match self.node_weight(n) {
            Some(w) => w,
            None => {
                return Err(DTTError::AnalysisPipelineError(
                    "cannot get sources when some nodes don't have a weight".to_string(),
                ));
            }
        }
        .pipeline_type
        .clone();
        if source_types.len() != num_sources {
            let msg = format!(
                "{} pipeline must have exactly {} input, but got {}",
                pipe_type,
                num_sources,
                source_types.len()
            );
            return Err(DTTError::AnalysisPipelineError(msg));
        }
        Ok(source_types)
    }

    /// iterate through all output edges
    /// and set the result type to the corresponding type
    fn set_node_result_type(&mut self, n: NodeIndex, result_type: &EdgeDataType) {
        let out_edges: Vec<_> = self
            .edges_directed(n, Direction::Outgoing)
            .map(|x| x.id())
            .collect();

        for edge in out_edges {
            self[edge].result_type = result_type.clone();
        }
    }

    /// Set the result types correctly for a pipeline
    /// Assumes source node types are already set
    /// Also checks some constraints and will return a failure if they aren't met
    fn determine_result_type(&mut self, n: NodeIndex) -> Result<(), DTTError> {
        let pipe_type = self
            .node_weight(n)
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot determine result type for a node without a weight".to_string(),
                )
            })?
            .pipeline_type
            .clone();
        let node_result_type = match pipe_type {
            SchemePipelineType::Results
            | SchemePipelineType::DataSource
            | SchemePipelineType::StoreResultsToView
            | SchemePipelineType::PerChannelBSource(_)
            | SchemePipelineType::PerChannelASource(_) => return Ok(()), // nothing to be done here
            SchemePipelineType::Conditioning => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                if !source_type.is_time_domain() {
                    return Err(DTTError::AnalysisPipelineError(
                        "Channel conditioning pipelines only take time domain input".to_string(),
                    ));
                }
                if self.node_weight(n)
                    .ok_or_else(||DTTError::AnalysisPipelineError("While determing result type: Node did not have a weight though it was checked earlier".to_string()))?
                    .id.clone().ok_or_else(||DTTError::AnalysisPipelineError(format!("{} type node must have an id.", pipe_type )))?
                    .first_channel()?
                    .do_heterodyne
                    || source_type.is_complex() {
                    EdgeDataType::TimeDomainValueComplex
                } else {
                    EdgeDataType::TimeDomainValueReal
                }
            }
            SchemePipelineType::FFT => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                if !source_type.is_time_domain() {
                    return Err(DTTError::AnalysisPipelineError(
                        "FFT pipeline only takes time domain input".to_string(),
                    ));
                }
                EdgeDataType::FreqDomainValueComplex
            }
            SchemePipelineType::InlineFFT => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                if !source_type.is_time_domain() {
                    return Err(DTTError::AnalysisPipelineError(
                        "InlineFFT pipeline only takes time domain input".to_string(),
                    ));
                }
                EdgeDataType::FreqDomainValueComplex
            }
            SchemePipelineType::CSD => {
                let mut sources_types = self.get_sources(n, 2)?;
                if sources_types[0] != sources_types[1] {
                    return Err(DTTError::AnalysisPipelineError(
                        "CSD pipeline inputs must be the same type".to_string(),
                    ));
                }
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueComplex => (),
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "CSD pipeline only takes complex frequency domain input".to_string(),
                        ));
                    }
                }
                EdgeDataType::FreqDomainValueComplex
            }
            SchemePipelineType::Real => {
                let mut sources_types = self.get_sources(n, 1)?;
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueComplex => (),
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "Real pipeline only takes complex frequency domain input".to_string(),
                        ));
                    }
                }
                EdgeDataType::FreqDomainValueReal
            }
            SchemePipelineType::Sqrt => {
                let mut sources_types = self.get_sources(n, 1)?;
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueComplex
                    | EdgeDataType::FreqDomainValueReal
                    | EdgeDataType::TimeDomainValueReal
                    | EdgeDataType::TimeDomainValueComplex => (),
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "Sqrt pipeline only takes real or complex floating point input"
                                .to_string(),
                        ));
                    }
                }
                source_type
            }
            SchemePipelineType::Phase => {
                let mut sources_types = self.get_sources(n, 1)?;
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueComplex => EdgeDataType::FreqDomainValueReal,
                    EdgeDataType::TimeDomainValueComplex => EdgeDataType::TimeDomainValueReal,
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "Phase pipeline only takes complex floating point input".to_string(),
                        ));
                    }
                }
            }
            SchemePipelineType::Complex => {
                let mut sources_types = self.get_sources(n, 2)?;
                if sources_types[0] != sources_types[1] {
                    return Err(DTTError::AnalysisPipelineError(
                        "Complex pipeline inputs must be the same type".to_string(),
                    ));
                }
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueReal => EdgeDataType::FreqDomainValueComplex,
                    EdgeDataType::TimeDomainValueReal => EdgeDataType::TimeDomainValueComplex,
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "Complex pipeline only takes real input".to_string(),
                        ));
                    }
                }
            }
            SchemePipelineType::ASD => {
                let mut sources_types = self.get_sources(n, 1)?;
                let source_type = sources_types.remove(0);
                match source_type {
                    EdgeDataType::FreqDomainValueComplex => (),
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "ASD pipeline only takes complex frequency domain input".to_string(),
                        ));
                    }
                }
                EdgeDataType::FreqDomainValueReal
            }
            SchemePipelineType::TimeShift { shift: _ }
            | SchemePipelineType::Average
            | SchemePipelineType::Identity => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                source_type
            }
            SchemePipelineType::Downsample => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                match source_type {
                    EdgeDataType::TimeDomainValueReal => EdgeDataType::TimeDomainValueReal,
                    EdgeDataType::TimeDomainValueInt64 => EdgeDataType::TimeDomainValueInt64,
                    EdgeDataType::TimeDomainValueInt32 => EdgeDataType::TimeDomainValueInt32,
                    EdgeDataType::TimeDomainValueInt16 => EdgeDataType::TimeDomainValueInt16,
                    EdgeDataType::TimeDomainValueInt8 => EdgeDataType::TimeDomainValueInt8,
                    EdgeDataType::TimeDomainValueUInt64 => EdgeDataType::TimeDomainValueUInt64,
                    EdgeDataType::TimeDomainValueUInt32 => EdgeDataType::TimeDomainValueUInt32,
                    EdgeDataType::TimeDomainValueUInt16 => EdgeDataType::TimeDomainValueUInt16,
                    EdgeDataType::TimeDomainValueUInt8 => EdgeDataType::TimeDomainValueUInt8,
                    _ => {
                        return Err(DTTError::AnalysisPipelineError(
                            "Downsample pipeline only takes real time-domain input".to_string(),
                        ));
                    }
                }
            }
            #[cfg(feature = "python-pipe")]
            SchemePipelineType::Custom(c) => {
                let source_types = self.get_sources(n, c.inputs.len())?;
                c.determine_result_type(&source_types)
            }
            SchemePipelineType::Dummy(_) => {
                return Err(DTTError::AnalysisPipelineError(
                    "Dummy pipeline cannot produce a result".to_string(),
                ));
            }
            SchemePipelineType::Splice => {
                let mut source_types = self.get_sources(n, 1)?;
                let source_type = source_types.remove(0);
                source_type.clone()
            }
        };
        self.set_node_result_type(n, &node_result_type);
        Ok(())
    }

    /// test a per-channel scheme and a cross-channel scheme together
    /// by creating two fake channels, then an analysis graph consisting of
    /// two per-channel and one cross-channel in a single graph.
    ///
    /// This would also be a great graph to send to the user
    pub(crate) fn test_schemes(
        rc: Box<RunContext>,
        per_channel_scheme: &'_ SchemeGraph<'a>,
        cross_channel_scheme: &'_ SchemeGraph<'a>,
    ) -> Result<Self, DTTError> {
        check_duplicate_names("per-channel scheme", per_channel_scheme)?;
        check_duplicate_names("cross-channel scheme", cross_channel_scheme)?;

        let a_chan = Channel::new(
            "a_channel".to_string(),
            Float32,
            PipDuration::from_seconds(1.0),
        )
        .into();

        let b_chan = Channel::new(
            "b_channel".to_string(),
            Float32,
            PipDuration::from_seconds(1.0),
        )
        .into();

        let channels = vec![a_chan, b_chan];

        let analysis_graph = Self::create_analysis_graph(
            channels.as_slice(),
            &per_channel_scheme,
            &cross_channel_scheme,
        )?;

        analysis_graph.check_graph_errors(rc)?;

        Ok(analysis_graph)
    }

    /// this function creates an analysis graph from
    /// it's assumed that every pair of channels in channel get a set of cross pipelines
    /// in both orderings!
    ///
    /// We don't do a channel crossed with itself.
    ///
    /// This is different from old DTT, where only some channels were A channels and other channels B channels
    pub(crate) fn create_analysis_graph(
        channels: &'_ [ChannelSettings],
        per_channel: &'_ SchemeGraph<'a>,
        cross_channel: &'_ SchemeGraph<'a>,
    ) -> Result<Self, DTTError> {
        let mut analysis_graph = AnalysisGraph::new();

        let mut node_map = HashMap::new();

        // create per-channel nodes
        for chan in channels {
            let per_chan_graph = Self::from_per_channel_scheme(chan, per_channel)?;
            analysis_graph.extend_graph(&mut node_map, &per_chan_graph)?;
        }

        // create cross-channel nodes
        for a_chan in channels {
            for b_chan in channels {
                if a_chan != b_chan {
                    let cross_chan_graph =
                        Self::from_cross_channel_scheme(a_chan, b_chan, &cross_channel)?;
                    analysis_graph.extend_graph(&mut node_map, &cross_chan_graph)?;
                }
            }
        }

        analysis_graph.set_result_types()?;

        Ok(analysis_graph)
    }

    fn check_graph_errors(&self, rc: Box<RunContext>) -> Result<(), DTTError> {
        // Check for errors
        // 1. A disconnected part of the graph.
        if connected_components(&**self) > 1 {
            return Err(DTTError::AnalysisPipelineError(
                "Disconnection found in analysis graph".to_string(),
            ));
        }

        // 2. A cycle in the graph.
        if let Err(c) = toposort(&**self, None) {
            let cyc_node = self
                .node_weight(c.node_id())
                .ok_or_else(|| {
                    DTTError::AnalysisPipelineError(
                        "Cannot search for graph cycles when a node has no weight".to_string(),
                    )
                })?
                .clone();
            let msg = format!(
                "The analysis pipelines contain a cycle.  Node {} depends on itself.",
                cyc_node.name
            );
            return Err(DTTError::AnalysisPipelineError(msg));
        }

        let mut no_output_warning = false;

        for node_idx in self.node_indices() {
            let node = self.node_weight(node_idx).ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot search for graph cycles when a node has no weight (2)".to_string(),
                )
            })?;

            // 3. A source that's not a data source.
            let in_edges: Vec<_> = self
                .edges_directed(node_idx, Direction::Incoming)
                .map(|x| x.id())
                .collect();

            if in_edges.len() == 0 {
                match node.pipeline_type {
                    SchemePipelineType::DataSource => (),
                    _ => {
                        let msg = format!("Node {} needs inputs, but has none.", node.name);
                        return Err(DTTError::AnalysisPipelineError(msg));
                    }
                }
            }

            // 5. Input ports that don't have exactly 1 input.
            let mut port_map = HashSet::new();
            match node.pipeline_type {
                SchemePipelineType::Results => (), // don't care about port numbers on the results node
                _ => {
                    for edge_idx in in_edges {
                        let edge = self.edge_weight(edge_idx).ok_or_else(|| {
                            DTTError::AnalysisPipelineError(
                                "Cannot search for graph cycles when an edge has no weight"
                                    .to_string(),
                            )
                        })?;
                        let port_num = edge.port;
                        if port_map.contains(&port_num) {
                            let msg = format!(
                                "Node {} has more than one input to port {}",
                                node.name, port_num
                            );
                            return Err(DTTError::AnalysisPipelineError(msg));
                        } else {
                            port_map.insert(port_num);
                        }
                    }
                }
            }

            if let Some(num_ports) = node.pipeline_type.port_count() {
                for p in 1..=num_ports {
                    if !port_map.contains(&p) {
                        let msg = format!("Node {} is missing an input on port {}", node.name, p);
                        return Err(DTTError::AnalysisPipelineError(msg));
                    }
                }
            }

            // 4. A sink that's not the result node
            let out_edges: Vec<_> = self
                .edges_directed(node_idx, Direction::Outgoing)
                .map(|x| x.id())
                .collect();

            if out_edges.len() == 0 {
                match node.pipeline_type {
                    SchemePipelineType::StoreResultsToView | SchemePipelineType::Results => (),
                    _ => {
                        let msg = format!("Node {} doesn't output to anything.", node.name);
                        no_output_warning = true;
                        rc.user_messages.set_warning("NoPipelineOutput", msg);
                    }
                }
            }
        }

        if !no_output_warning {
            rc.user_messages.clear_message("NoPipelineOutput");
        }

        Ok(())
    }
}

/// graph name is for error reporting
fn check_duplicate_names(graph_name: &str, graph: &'_ SchemeGraph) -> Result<(), DTTError> {
    let mut names = HashSet::new();
    for node in graph.raw_nodes() {
        if names.contains(&node.weight.name) {
            return Err(DTTError::AnalysisPipelineError(format!(
                "Duplicate node name '{}' in {} graph",
                node.weight.name, graph_name
            )));
        }
        names.insert(node.weight.name.clone());
    }
    Ok(())
}
