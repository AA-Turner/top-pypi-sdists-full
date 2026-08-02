//! Create pipeline graph for a ScopeView

use std::collections::HashMap;

use petgraph::graph::NodeIndex;

use crate::analysis::graph::analysis::{AnalysisEdge, AnalysisGraph, AnalysisNode};
use crate::analysis::graph::scheme::{SchemeEdge, SchemePipelineType};
use crate::analysis::result::EdgeResultsWrapper;
use crate::errors::DTTError;
use crate::params::channel_params::{Channel, TrendStat};
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use crate::{AnalysisId, AnalysisSettingsId};

pub fn create_pipeline_graph<'b>(
    _rc: Box<RunContext>,
    view: &ScopeView,
) -> Result<AnalysisGraph<'b>, DTTError> {
    let mut nodes = HashMap::new();
    let mut graph = AnalysisGraph::new();

    let data_source = AnalysisNode {
        pipeline_type: SchemePipelineType::DataSource,
        name: "data_source".to_string(),
        id: None,
    };

    let ds_id = graph.add_node(data_source);

    let results = AnalysisNode {
        pipeline_type: SchemePipelineType::Results,
        name: "results".to_string(),
        id: None,
    };

    let result_id = graph.add_node(results);

    let results_store = AnalysisNode {
        pipeline_type: SchemePipelineType::StoreResultsToView,
        name: "results_store".to_string(),
        id: None,
    };

    let result_store_id = graph.add_node(results_store);

    for id in &view.set.members {
        add_id_to_graph(
            &mut graph,
            &mut nodes,
            id,
            ds_id,
            result_id,
            result_store_id,
            view.decimate,
        )?;
    }

    graph.set_result_types()?;

    Ok(graph)
}

fn add_id_to_graph<'a>(
    graph: &'_ mut AnalysisGraph,
    nodes: &'_ mut HashMap<&'a AnalysisId, NodeIndex>,
    id: &'a AnalysisId,
    ds_id: NodeIndex,
    result_id: NodeIndex,
    result_store_id: NodeIndex,
    decimate: bool,
) -> Result<NodeIndex, DTTError> {
    if nodes.contains_key(id) {
        return Ok(nodes.get(id).expect("checked for membership").clone());
    }

    let first_chan = id
        .first_channel()
        .expect("should always be at least one channel");

    let (connect_result, out_node) = match id {
        AnalysisId::Simple { channel } => {
            let (in_node, out_node) = add_simple_to_graph(graph, channel);

            let in_scheme_edge = SchemeEdge::new(1);
            let in_edge = AnalysisEdge::new(in_scheme_edge, channel.data_type.clone().into());
            graph.add_edge(ds_id, in_node, in_edge);
            let do_decim = !channel.data_type.is_complex();
            (do_decim, out_node)
        }
        AnalysisId::Compound { name, args } => {
            log::debug!("got compound analysis '{}'", name);

            let (connect_result, node_id) = if name == "complex" {
                let complex_id = graph.add_node(AnalysisNode {
                    pipeline_type: SchemePipelineType::Complex,
                    name: format!("{}.complex", id),
                    id: Some(id.clone().into()),
                });

                (false, complex_id)
            } else if name == "phase" {
                let phase_id = graph.add_node(AnalysisNode {
                    pipeline_type: SchemePipelineType::Phase,
                    name: format!("{}.phase", id),
                    id: Some(id.clone().into()),
                });

                (true, phase_id)
            } else {
                panic!("unrecognized analysis '{}'", name);
            };

            // connect up all the arguments, but first make
            // sure they are already graphed
            let mut arg_nodes = Vec::with_capacity(args.len());

            for arg in args {
                let arg_id = add_id_to_graph(
                    graph,
                    nodes,
                    arg,
                    ds_id,
                    result_id,
                    result_store_id,
                    decimate,
                )?;
                arg_nodes.push(arg_id);
            }

            for (i, arg_node) in arg_nodes.into_iter().enumerate() {
                graph.add_edge(
                    arg_node,
                    node_id,
                    AnalysisEdge::new(
                        SchemeEdge::new(i + 1),
                        args.get(i)
                            .expect("enumerated, so i must exist")
                            .try_into()?,
                    ),
                );
            }

            // only connect to result if output is real
            // complex outputs not yet handled.
            (connect_result, node_id)
        }
    };

    // attach decimator
    if connect_result {
        let decim_id = if decimate {
            let decim = AnalysisNode {
                pipeline_type: SchemePipelineType::Downsample,
                name: format!("{}_downsample", id),
                id: Some(id.clone().into()),
            };

            let decim_id = graph.add_node(decim);

            let decim_edge =
                AnalysisEdge::new(SchemeEdge::new(1), first_chan.data_type.clone().into());
            graph.add_edge(out_node, decim_id, decim_edge);
            decim_id
        } else {
            out_node
        };
        //let decim_id = out_node;

        // attach to results
        let results_scheme_edge =
            SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::TimeDomainReal);
        let results_edge =
            AnalysisEdge::new(results_scheme_edge, first_chan.data_type.clone().into());
        graph.add_edge(decim_id, result_id, results_edge);

        // attach to results store
        // let results_store_scheme_edge =
        //     SchemeEdge::new(1).set_result_wrapper(EdgeResultsWrapper::TimeDomainReal);
        // let results_store_edge = AnalysisEdge::new(
        //     results_store_scheme_edge,
        //     first_chan.data_type.clone().into(),
        // );
        // graph.add_edge(out_node, result_store_id, results_store_edge);
    };

    nodes.insert(id, out_node);

    Ok(out_node)
}

/// returns node to attach data source, node to get undecimated result
fn add_simple_to_graph<'a>(
    graph: &'a mut AnalysisGraph,
    channel: &'_ Channel,
) -> (NodeIndex, NodeIndex) {
    // Because we aren't handling functions yet, we can just hook data source to results
    // and pass it as a per-channel graph
    // When arbitrary functions are allowed on individual channels, then
    // Some more involved method will be needed.

    // for this early code we'll just assume if one channel is a trend then they are all trends of the same size.
    //
    // shift trends later in time by 1/2 step to make their time stamps centered in the time
    // region they summarize
    //
    // this is just period/2, but a more correct formula would be period *  (n-1)/2*n)
    // where n is the number of points per region.
    let trend_shift = if channel.trend_stat != TrendStat::Raw {
        Some(-(channel.period / 2usize))
    } else {
        None
    };

    let id = Some(AnalysisSettingsId::from_channel(channel.clone().into()));

    let condition = AnalysisNode {
        pipeline_type: SchemePipelineType::Conditioning,
        name: format!("{}_condition", channel),
        id: id.clone(),
    };
    let condition_index = graph.add_node(condition);

    // only shift if trend
    let shift_index = if let Some(shift) = trend_shift {
        let idx = graph.add_node(AnalysisNode {
            name: format!("{}_center_trend", channel),
            pipeline_type: SchemePipelineType::TimeShift { shift },
            id,
        });
        graph.add_edge(
            condition_index,
            idx,
            AnalysisEdge::new(SchemeEdge::new(1), channel.data_type.clone().into()),
        );
        idx
        //condition_index
    } else {
        condition_index
    };

    (condition_index, shift_index)
}
