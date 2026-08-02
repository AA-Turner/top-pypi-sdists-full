//! Create pipelines from a scope view analysis graph
//! dtt analysis graphs are created in a different function
use crate::analysis::fourier_tools::csd;
use crate::analysis::graph::analysis::{AnalysisGraph, OutputSource};
use crate::analysis::graph::scheme::SchemePipelineType;
use crate::analysis::result::ResultsReceiver;
use crate::analysis::scope::splice::{SpliceMode, SplicePipeline};
use crate::data_source::DataBlockReceiver;
use crate::data_source::data_distributor::add_distributor_to_graph;
use crate::errors::DTTError;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use num_traits::Float;
use petgraph::graph::NodeIndex;
use petgraph::visit::Topo;
use pipelines::complex::c128;
use user_messages::UserMsgProvider;

use crate::analysis::arithmetic::{complex, phase, real, sqrt};

use crate::analysis::scope::{downsample, inline_fft::InlineFFTParams};
use crate::params::test_params::AverageType;

impl<'a> AnalysisGraph<'a> {
    pub async fn view_graph_to_pipeline(
        &mut self,
        rc: &Box<RunContext>,
        view: &mut ScopeView,
        block_rx: DataBlockReceiver,
    ) -> Result<ResultsReceiver, DTTError> {
        let mut topo = Topo::new(&**self);

        let mut final_out = Err(DTTError::AnalysisPipelineError(
            "scope view pipeline creation terminated without processing the results node"
                .to_string(),
        ));

        let mut opt_block_rx = Some(block_rx);

        loop {
            let node_idx = match topo.next(&**self) {
                None => break,
                Some(n) => n,
            };
            let node = self.node_weight(node_idx).ok_or_else(|| {
                DTTError::AnalysisPipelineError(
                    "Cannot create pipeline from view graph when a node has no weight".to_string(),
                )
            })?;

            match node.pipeline_type {
                SchemePipelineType::DataSource => {
                    if let Some(b_rx) = opt_block_rx {
                        add_distributor_to_graph(rc, self, node_idx, b_rx)?
                    } else {
                        return Err(DTTError::AnalysisPipelineError(
                            "Two data source nodes are not allowed".to_string(),
                        ));
                    };
                    opt_block_rx = None;
                }
                SchemePipelineType::Results => {
                    let out = self.wrap_results(rc, node_idx).await;
                    final_out = out;
                }
                SchemePipelineType::StoreResultsToView => {
                    self.wrap_store_results_to_view(rc, view, node_idx).await?
                }
                SchemePipelineType::Identity => {
                    return Err(DTTError::UnimplementedOption(
                        "Identity type".to_string(),
                        "scope view".to_string(),
                    ));
                }
                SchemePipelineType::Average => {
                    self.create_average(rc, AverageType::Fixed, node_idx)
                        .await?
                }
                SchemePipelineType::Conditioning => self.create_conditioning(rc, node_idx).await?,
                SchemePipelineType::Splice => self.create_splice(rc, node_idx, view).await?,
                SchemePipelineType::Downsample => self.create_downsample(rc, node_idx).await?,
                SchemePipelineType::InlineFFT => {
                    self.create_inline_fft(rc, view.fft_config_tx.subscribe(), node_idx)
                        .await?
                }
                SchemePipelineType::CSD => self.create_csd(rc, node_idx).await?,
                SchemePipelineType::Real => self.create_real(rc, node_idx).await?,
                SchemePipelineType::Sqrt => self.create_sqrt(rc, node_idx).await?,
                SchemePipelineType::Phase => self.create_phase(rc, node_idx).await?,
                SchemePipelineType::Complex => self.create_complex(rc, node_idx).await?,
                SchemePipelineType::TimeShift { shift } => {
                    self.create_timeshift(rc, node_idx, shift).await?
                }
                SchemePipelineType::FFT => {
                    return Err(DTTError::UnimplementedOption(
                        "FFT type".to_string(),
                        "scope view".to_string(),
                    ));
                }
                SchemePipelineType::ASD => {
                    return Err(DTTError::UnimplementedOption(
                        "ASD type".to_string(),
                        "scope view".to_string(),
                    ));
                }
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
                SchemePipelineType::Custom(_) => {
                    return Err(DTTError::UnimplementedOption(
                        "Average type".to_string(),
                        "scope view".to_string(),
                    ));
                }
                SchemePipelineType::Dummy(_create_timeshift) => {
                    let msg = format!(
                        "{} is a Dummy pipeline. Dummy pipeline can't be used.",
                        node.name
                    );
                    return Err(DTTError::AnalysisPipelineError(msg));
                }
            }
        }

        rc.user_messages.clear_message("BadInput");

        final_out.map(|r| r)
    }

    async fn create_conditioning(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;
        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view conditioning when an edge has no weight".to_string(),
            )
        })?;
        let in_source_result = edge.take_nds_buffer_rx();
        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view conditioning when a node has no weight".to_string(),
            )
        })?;
        let channel = &node
            .id
            .clone()
            .ok_or_else(|| {
                DTTError::AnalysisPipelineError(format!("Conditioning pipeline must have an id"))
            })?
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

        let ds: OutputSource = channel
            .create_data_source_pipeline(rc, buffer_rx)
            .await?
            .into();

        self.populate_output_source(node_idx, &ds)
    }

    async fn create_splice(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
        view: &ScopeView,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view splice when a node has no weight".to_string(),
            )
        })?;

        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".splice";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view splice when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::NotSet
            | OutputSource::BufferRx(_)
            | OutputSource::PipelineFreqArrayFloat64(_)
            | OutputSource::PipelineResultValue(_)
            | OutputSource::PipelineFreqArrayComplex128(_) => {
                let msg = format!(
                    "{} not a valid input type for a splice pipeline: Must be a time-domain array.",
                    edge.output_source
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
            OutputSource::PipelineTDArrayFloat64(t) => {
                SplicePipeline::create(
                    rc.ump_clone(),
                    pipe_name,
                    view.span.start_pip,
                    view.span.span_pip,
                    //SpliceMode::FillGaps(f64::nan()), view.span.online,  t).await.into(),
                    SpliceMode::ContiguousLatest,
                    view.span.online,
                    t,
                )
                .await?
                .into()
            }
            OutputSource::PipelineTDArrayComplex128(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(c128::new(f64::nan(), f64::nan())),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayInt64(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0i64),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayInt32(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0i32),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayInt16(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0i16),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayInt8(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0i8),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayUInt64(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0u64),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayUInt32(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0u32),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayUInt16(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0u16),
                view.span.online,
                t,
            )
            .await?
            .into(),
            OutputSource::PipelineTDArrayUInt8(t) => SplicePipeline::create(
                rc.ump_clone(),
                pipe_name,
                view.span.start_pip,
                view.span.span_pip,
                SpliceMode::FillGaps(0u8),
                view.span.online,
                t,
            )
            .await?
            .into(),
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_downsample(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create downsample when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".downsample";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create downsample when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::NotSet
            | OutputSource::BufferRx(_)
            | OutputSource::PipelineTDArrayComplex128(_)
            | OutputSource::PipelineFreqArrayFloat64(_)
            | OutputSource::PipelineResultValue(_)
            | OutputSource::PipelineFreqArrayComplex128(_) => {
                let msg = format!(
                    "{} not a valid input type for a downsample pipeline: Must be an f64 or c128 time domain array.",
                    edge.output_source
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
            OutputSource::PipelineTDArrayFloat64(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayInt8(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayInt16(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayInt32(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayInt64(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayUInt8(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayUInt16(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayUInt32(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
            OutputSource::PipelineTDArrayUInt64(t) => {
                downsample::DownsampleCache::create(rc.ump_clone(), pipe_name, t)
                    .await?
                    .into()
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_inline_fft(
        &mut self,
        rc: &Box<RunContext>,
        fft_config_rx: tokio::sync::watch::Receiver<InlineFFTParams>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create inline fft when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".inline_fft";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create inline fft when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::NotSet
            | OutputSource::BufferRx(_)
            | OutputSource::PipelineFreqArrayComplex128(_)
            | OutputSource::PipelineFreqArrayFloat64(_)
            | OutputSource::PipelineResultValue(_)
            | OutputSource::PipelineTDArrayInt8(_)
            | OutputSource::PipelineTDArrayInt16(_)
            | OutputSource::PipelineTDArrayInt32(_)
            | OutputSource::PipelineTDArrayInt64(_)
            | OutputSource::PipelineTDArrayUInt8(_)
            | OutputSource::PipelineTDArrayUInt16(_)
            | OutputSource::PipelineTDArrayUInt32(_)
            | OutputSource::PipelineTDArrayUInt64(_) => {
                let msg = format!(
                    "{} not a valid input type for a inline fft pipeline: Must be an f64 or c128 time domain array.",
                    edge.output_source
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
            OutputSource::PipelineTDArrayFloat64(t) => {
                InlineFFTParams::create(rc.ump_clone(), pipe_name, fft_config_rx, t)
                    .await?
                    .into()
            }

            OutputSource::PipelineTDArrayComplex128(t) => {
                InlineFFTParams::create(rc.ump_clone(), pipe_name, fft_config_rx, t)
                    .await?
                    .into()
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_csd(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edges_idx = self.get_incoming_edges(node_idx);

        if edges_idx.len() != 2 {
            let msg = format!("{} must have exactly 2 incoming edges.", node_idx.index());
            rc.user_messages.set_error("BadInput", msg.clone());
            return Err(DTTError::AnalysisPipelineError(msg));
        }

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view CSD when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".csd";

        let edge1 = self.edge_weight(edges_idx[0]).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view CSD when an edge has no weight (1)".to_string(),
            )
        })?;
        let edge2 = self.edge_weight(edges_idx[1]).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view CSD when an edge has no weight (2)".to_string(),
            )
        })?;

        let out_source = match (&edge1.output_source, &edge2.output_source) {
            (
                OutputSource::PipelineFreqArrayComplex128(t1),
                OutputSource::PipelineFreqArrayComplex128(t2),
            ) => csd::create(rc.ump_clone(), pipe_name, t1, t2).await?.into(),
            (a, b) => {
                let msg = format!(
                    "{} x {} are not valid input types for a csd pipeline. must be  c128 freq. domain arrays.",
                    a, b
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_real(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view real when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".real";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view real when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::PipelineFreqArrayComplex128(t) => {
                real::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            a => {
                let msg = format!(
                    "{} is not valid input type for a real pipeline. must be  complex 128 freq. domain array.",
                    a
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_sqrt(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view SQRT when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".sqrt";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view SQRT when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::PipelineFreqArrayComplex128(t) => {
                sqrt::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            OutputSource::PipelineFreqArrayFloat64(t) => {
                sqrt::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            OutputSource::PipelineTDArrayComplex128(t) => {
                sqrt::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            OutputSource::PipelineTDArrayFloat64(t) => {
                sqrt::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            a => {
                let msg = format!(
                    "{} is not valid input type for a sqrt pipeline. must be a floating point array.",
                    a
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_phase(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edge_idx = self.get_only_incoming_edge(node_idx)?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view Phase when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".phase";

        let edge = self.edge_weight_mut(edge_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view Phase when an edge has no weight".to_string(),
            )
        })?;

        let out_source = match &edge.output_source {
            OutputSource::PipelineFreqArrayComplex128(t) => {
                phase::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            OutputSource::PipelineTDArrayComplex128(t) => {
                phase::create(rc.ump_clone(), pipe_name, t).await?.into()
            }
            a => {
                let msg = format!(
                    "{} is not valid input type for a phase pipeline. must be a complex array.",
                    a
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn create_complex(
        &mut self,
        rc: &Box<RunContext>,
        node_idx: petgraph::graph::NodeIndex,
    ) -> Result<(), DTTError> {
        let edges = self.get_ordered_incoming_edges(node_idx, 2.into())?;

        let node = self.node_weight(node_idx).ok_or_else(|| {
            DTTError::AnalysisPipelineError(
                "Cannot create view Complex when a node has no weight".to_string(),
            )
        })?;
        let pipe_name = node
            .id
            .clone()
            .map(|i| i.to_string())
            .unwrap_or("<unk>".to_string())
            + ".complex";

        let out_source = match (&edges[0].output_source, &edges[1].output_source) {
            (
                OutputSource::PipelineFreqArrayFloat64(t1),
                OutputSource::PipelineFreqArrayFloat64(t2),
            ) => complex::create(rc.ump_clone(), pipe_name, t1, t2)
                .await?
                .into(),
            (
                OutputSource::PipelineTDArrayFloat64(t1),
                OutputSource::PipelineTDArrayFloat64(t2),
            ) => complex::create(rc.ump_clone(), pipe_name, t1, t2)
                .await?
                .into(),
            (a, b) => {
                let msg = format!(
                    "{} x {} are not valid input types for a complex pipeline. must be  real arrays.",
                    a, b
                );
                rc.user_messages.set_error("BadInput", msg.clone());
                return Err(DTTError::AnalysisPipelineError(msg));
            }
        };

        self.populate_output_source(node_idx, &out_source)
    }

    async fn wrap_store_results_to_view(
        &self,
        rc: &'_ Box<RunContext>,
        view: &mut ScopeView,
        node_idx: NodeIndex,
    ) -> Result<(), DTTError> {
        let results_rx = self.wrap_results(rc, node_idx).await?;

        view.add_results(results_rx).await?;

        Ok(())
    }
}
