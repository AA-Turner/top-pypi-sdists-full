//! Handle NDScope style scope views.
//! These views take an arbitrary number of channels and functions on those channels as a ViewSet.
//! And also a ViewSpan, a time span, and continuously and asynchronously produce time domain results
//! across that time span for the ViewSet.

mod pipeline_graph;
mod view_set;

use crate::AnalysisResult;
use crate::analysis::result::{AnalysisId, ResultsReceiver};
use crate::data_source::{DataBlockReceiver, DataBlockSender, DataSourceRef};
use crate::errors::DTTError;
use crate::run_context::RunContext;
use crate::scope_view::pipeline_graph::create_pipeline_graph;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use log::debug;
use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio_util::sync::CancellationToken;

use crate::analysis::scope::inline_fft::InlineFFTParams;
use crate::user::ResponseToUser::{ScopeViewDone, ScopeViewResult};
#[cfg(not(feature = "python"))]
use dtt_macros::{getter, pyo3};
#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

pub use view_set::{SetMember, ViewSet};

/// When the span is online, the start is just a beginning marker taken
/// from the current time.
#[derive(Clone, Debug)]
pub(crate) struct ViewSpan {
    pub online: bool,
    pub start_pip: PipInstant,
    pub span_pip: PipDuration,
}

impl ViewSpan {
    pub(crate) fn optional_end_pip(&self) -> Option<PipInstant> {
        if self.online {
            None
        } else {
            Some(self.end_pip())
        }
    }

    pub(crate) fn end_pip(&self) -> PipInstant {
        self.start_pip + self.span_pip
    }

    fn new_fixed(start_pip: PipInstant, end_pip: PipInstant) -> Self {
        Self {
            online: false,
            start_pip,
            span_pip: end_pip - start_pip,
        }
    }

    fn new_online(span: PipDuration) -> ViewSpan {
        let start_pip = PipInstant::from_gpst_seconds(0.0);

        ViewSpan {
            online: true,
            start_pip,
            span_pip: span,
        }
    }
}

#[derive(Debug)]
pub(crate) enum ScopeViewCommand {
    SetFFTParams { params: InlineFFTParams },
    SetSpan { span: ViewSpan },
    UpdateResults(AnalysisResult),
    GetResults(tokio::sync::oneshot::Sender<ResultsStore>),
    Close,
}

type ResultsStore = HashMap<AnalysisId, AnalysisResult>;

#[derive(Debug)]
pub struct ScopeView {
    pub(crate) id: usize,
    pub(crate) set: ViewSet,
    pub(crate) span: ViewSpan,

    /// Once created, this value can be used to
    /// Update the scope window
    pub(crate) block_tx: Option<DataBlockSender>,

    /// Used to cancel the data task if the view is updated
    pub(crate) data_task_cancel_token: Option<CancellationToken>,

    /// Used to update a span of unordered live request in place
    pub(crate) span_update_tx: Option<tokio::sync::watch::Sender<PipDuration>>,

    /// Used to update frequency domain configuration for on-the-fly
    /// frequency domain results
    pub(crate) fft_config_tx: tokio::sync::watch::Sender<InlineFFTParams>,

    /// Number of times span has been hard-reset (as opposed to just updated)
    /// useful for debugging.
    pub(crate) reset_count: u64,

    /// used to change the view while running
    pub(crate) command_rx: tokio::sync::mpsc::UnboundedReceiver<ScopeViewCommand>,

    /// used at startup for some things other than handles
    /// that need to send commands
    /// dropped before the command loop starts
    pub(crate) command_tx: Option<tokio::sync::mpsc::UnboundedSender<ScopeViewCommand>>,

    /// Store the latest results per channel
    /// Useful for exporting
    pub(crate) results_store: ResultsStore,

    /// When upstream data source is done, close the view
    /// Useful for indicating to apps that data is finished
    /// Otherwise the view is kept open.  In this mode, similar
    /// requests that use the same pipeline are handled more efficiently
    /// by not recreating the pipeline.
    close_when_done: bool,

    /// whether to route results values through a decimation pipeline first
    /// useful for slow code like ndscope
    decimate: bool,

    /// A snapshot view gets data from the cache but tells
    /// the cache not to query any data sources
    /// Useful for fast re-retrieval of data
    pub(crate) snapshot: bool,
}

impl ScopeView {
    pub(crate) fn create(
        rc: Box<RunContext>,
        data_source: DataSourceRef,
        id: usize,
        set: ViewSet,
        span: ViewSpan,
        decimate: bool,
        snapshot: bool,
        close_when_done: bool,
    ) -> tokio::sync::mpsc::UnboundedSender<ScopeViewCommand> {
        let (fft_config_tx, _) = tokio::sync::watch::channel(InlineFFTParams::default());
        let (command_tx, command_rx) = tokio::sync::mpsc::unbounded_channel();

        let view = Self {
            id,
            set,
            span,
            block_tx: None,
            data_task_cancel_token: None,
            span_update_tx: None,
            fft_config_tx,
            reset_count: 0,
            command_rx,
            command_tx: Some(command_tx.clone()),
            results_store: ResultsStore::new(),
            close_when_done,
            decimate,
            snapshot,
        };

        tokio::spawn(view.run_loop(rc, data_source));

        command_tx
    }

    async fn setup_analysis(
        &mut self,
        rc: &Box<RunContext>,
        block_rx: DataBlockReceiver,
    ) -> Result<ResultsReceiver, DTTError> {
        let mut ag = create_pipeline_graph(rc.clone(), self)?;

        ag.view_graph_to_pipeline(rc, self, block_rx).await
    }

    async fn start_results_loop(&mut self, rc: &Box<RunContext>, rr: ResultsReceiver) {
        let ct = CancellationToken::new();
        let ct2 = ct.clone();
        tokio::spawn(ScopeView::results_loop(rc.clone(), self.id, rr, ct2));
    }

    /// Send pipeline results to application
    async fn results_loop(
        rc: Box<RunContext>,
        id: usize,
        mut rr: ResultsReceiver,
        cancel_token: CancellationToken,
    ) {
        log::debug!("starting results loop");
        loop {
            tokio::select! {
                _ = cancel_token.cancelled() => {
                    break
                },
                r = rr.recv() => {
                    match r {
                        Some(m) => if rc.output_handle.send(rc.clone(), ScopeViewResult{id, result: m}).is_err() {
                                   break;
                        },
                        None => {
                            break;
                        }
                    }
                },
            }
        }
        if rc
            .output_handle
            .send(rc.clone(), ScopeViewDone { id })
            .is_err()
        {
            rc.user_messages
                .error("Failed to send scope view done to user app");
        }
        log::debug!("ending results loop");
    }

    fn set_span(
        &mut self,
        rc: &Box<RunContext>,
        data_source: DataSourceRef,
        span: ViewSpan,
    ) -> Result<(), DTTError> {
        if span.online == self.span.online {
            self.span = span;
            data_source.clone().update_scope_data(rc.clone(), self)
        } else {
            Err(DTTError::ViewConfig("Cannot switch an existing view between online and fixed.  Create a new view instead.".into()))
        }
    }

    fn set_fft_params(&mut self, params: InlineFFTParams) {
        let _ = self.fft_config_tx.send(params);
    }

    /// If the return value is true, close the view
    async fn handle_command(
        &mut self,
        rc: &Box<RunContext>,
        data_source: DataSourceRef,
        command: ScopeViewCommand,
    ) -> bool {
        match command {
            ScopeViewCommand::SetFFTParams { params } => {
                self.set_fft_params(params);
            }
            ScopeViewCommand::SetSpan { span } => {
                if let Err(e) = self.set_span(rc, data_source, span) {
                    rc.user_messages.error(format!("Error setting span: {}", e));
                }
            }
            ScopeViewCommand::Close => {
                if let Some(c) = &self.data_task_cancel_token {
                    c.cancel();
                    return true;
                }
            }
            ScopeViewCommand::UpdateResults(result) => {
                self.update_results(result);
            }
            ScopeViewCommand::GetResults(tx) => {
                let _ = tx.send(self.results_store.clone());
            }
        }
        false
    }

    fn update_results(&mut self, result: AnalysisResult) {
        self.results_store.insert(result.id().clone(), result);
    }

    async fn run_loop(mut self, rc: Box<RunContext>, data_source: DataSourceRef) {
        debug!("View {} Started", self.id);

        //self.set.fill_out_analysis_requests().await;

        let mut block_rx = match data_source.clone().start_scope_data(rc.clone(), &mut self) {
            Ok(b) => b,
            Err(e) => {
                rc.clone()
                    .user_messages
                    .error(format!("Error starting data source: {}", e));
                return;
            }
        };

        let mut fuse_block_channels = false;
        let (bs_tx, block_splice_rx) = tokio::sync::mpsc::channel(1);

        // wrap the tx up in an Option to manage the case where the block stream is closed
        //let mut block_splice_tx_opt = Some(bs_tx);

        let mut bs_rx = Some(block_splice_rx);

        if self.close_when_done {
            // the view closes if the data source closes
            self.block_tx = None;
        }

        loop {
            tokio::select! {
                r = block_rx.recv() => {
                    match r {
                        Some(b) => {

                            if fuse_block_channels {
                                if bs_tx.send(b).await.is_err() {
                                    break;
                                };
                            } else {
                                match self.set.resolve_channels(b).await {
                                    Some(b) => {
                                        fuse_block_channels = true;
                                        let rx = match bs_rx {
                                            Some(rx) => rx,
                                            None => {
                                                rc.clone().user_messages.error("Error resolving channels: block receive channel already used");
                                                break;
                                            }
                                        };
                                        let rr = match self.setup_analysis(&rc, rx).await {
                                        Ok(rr) => rr,
                                        Err(e) => {
                                                rc.clone().user_messages.error(format!("View {}: Error setting up analysis: {}", self.id, e));
                                                break;
                                            }
                                        };
                                        self.start_results_loop(&rc, rr).await;
                                        bs_rx = None;
                                        if bs_tx.send(b).await.is_err() {
                                            break;
                                        };
                                    },
                                    None => {

                                    },
                                }
                            }

                        },
                        None => {
                            break;
                        }
                    }
                }
                r = self.command_rx.recv() => {
                    match r {
                        None => break,
                        Some(c) => {
                            if self.handle_command(&rc, data_source.clone(), c).await {
                                break;
                            }
                        }
                    }
                }
            }
        }
        debug!("View {} Closed", self.id);
    }

    /// Track a results channel.  Send results to the command loop.    
    pub(crate) async fn add_results(
        &self,
        mut results_rx: ResultsReceiver,
    ) -> Result<(), DTTError> {
        let cmd_tx = self
            .command_tx
            .clone()
            .ok_or(DTTError::AnalysisPipelineError(
                "Could not get command channel for view while adding a result.".to_string(),
            ))?;

        tokio::spawn(async move {
            loop {
                match results_rx.recv().await {
                    None => break,
                    Some(r) => {
                        if let Err(_) = cmd_tx.send(ScopeViewCommand::UpdateResults(r)) {
                            break;
                        }
                    }
                }
            }
        });
        Ok(())
    }
}

static NEXT_SCOPE_VIEW_ID: AtomicUsize = AtomicUsize::new(0);

/// Clonable handle used to update a view
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(frozen))]
#[derive(Clone, Debug)]
pub struct ScopeViewHandle {
    id: usize,
    command_tx: tokio::sync::mpsc::UnboundedSender<ScopeViewCommand>,
}

impl ScopeViewHandle {
    fn set_span(&self, span: ViewSpan) -> Result<(), DTTError> {
        self.command_tx
            .send(ScopeViewCommand::SetSpan { span })
            .map_err(|x| x.into())
    }

    pub(crate) fn new_online(
        rc: Box<RunContext>,
        data_source: DataSourceRef,
        set: ViewSet,
        span_pip: PipDuration,
    ) -> Self {
        let span = ViewSpan::new_online(span_pip);
        let id = NEXT_SCOPE_VIEW_ID.fetch_add(1, Ordering::Relaxed);
        // online views are always decimated
        let command_tx = ScopeView::create(rc, data_source, id, set, span, true, false, false);
        Self { id, command_tx }
    }

    pub(crate) fn new_fixed(
        rc: Box<RunContext>,
        data_source: DataSourceRef,
        set: ViewSet,
        start_pip: PipInstant,
        end_pip: PipInstant,
    ) -> Self {
        let span = ViewSpan::new_fixed(start_pip, end_pip);
        let id = NEXT_SCOPE_VIEW_ID.fetch_add(1, Ordering::Relaxed);
        let command_tx = ScopeView::create(rc, data_source, id, set, span, true, false, false);
        Self { id, command_tx }
    }

    pub(crate) fn new_snapshot(
        rc: Box<RunContext>,
        data_source: DataSourceRef,
        set: ViewSet,
        start_pip: PipInstant,
        end_pip: PipInstant,
    ) -> Self {
        let span = ViewSpan::new_fixed(start_pip, end_pip);
        let id = NEXT_SCOPE_VIEW_ID.fetch_add(1, Ordering::Relaxed);
        let command_tx = ScopeView::create(rc, data_source, id, set, span, false, true, true);
        Self { id, command_tx }
    }

    // single shot closes when it's done gathering data
    // good for --single-shot runs in ndscope, but bad
    // for performance when moving the trace around
    pub(crate) fn new_singleshot(
        rc: Box<RunContext>,
        data_source: DataSourceRef,
        set: ViewSet,
        start_pip: PipInstant,
        end_pip: PipInstant,
    ) -> Self {
        let span = ViewSpan::new_fixed(start_pip, end_pip);
        let id = NEXT_SCOPE_VIEW_ID.fetch_add(1, Ordering::Relaxed);
        let command_tx = ScopeView::create(rc, data_source, id, set, span, false, false, true);
        Self { id, command_tx }
    }

    pub fn update_online(&self, span_pip: PipDuration) -> Result<(), DTTError> {
        let span = ViewSpan::new_online(span_pip);
        self.set_span(span)
    }

    pub fn update_fixed(&self, start_pip: PipInstant, end_pip: PipInstant) -> Result<(), DTTError> {
        let span = ViewSpan::new_fixed(start_pip, end_pip);
        self.set_span(span)
    }
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl ScopeViewHandle {
    #[getter]
    pub fn id(&self) -> usize {
        self.id
    }

    pub fn set_fft_params(&self, params: InlineFFTParams) -> Result<(), DTTError> {
        self.command_tx
            .send(ScopeViewCommand::SetFFTParams { params })
            .map_err(|x| x.into())
    }

    /// Update the span of a view.  This is a pythonic wrapper.  Rust code should call update_online() or update_fixed().
    //#[cfg(python)]
    //#[cfg_attr(feature="python", pyo3(text_signature = "(data_source, span_pip=None, start_pip=None, end_pip=None)"))]
    //#[pyo3(text_signature = "(span_pip: PipDuration=None, start_pip: PipInstant=None, end_pip: PipInstant=None)")]
    #[pyo3(signature = (span_pip=None, start_pip=None, end_pip=None))]
    pub fn update(
        &self,
        span_pip: Option<PipDuration>,
        start_pip: Option<PipInstant>,
        end_pip: Option<PipInstant>,
    ) -> Result<(), DTTError> {
        match (span_pip, start_pip, end_pip) {
            (Some(span_pip), Some(start_pip), None) => {
                self.update_fixed(start_pip, start_pip + span_pip)
            },
            (None, Some(start_pip), Some(end_pip)) => {
                self.update_fixed(start_pip, end_pip)
            },
            (Some(span_pip), None, None) => {
                self.update_online(span_pip)
            },
            _ => {
                Err(DTTError::ViewConfig("Invalid view configuration.  For an online span, set only span_pip.  For a fixed span, set start_pip and either span_pip or end_pip.".into()))
            },
        }
    }

    pub fn close(&self) -> Result<(), DTTError> {
        self.command_tx
            .send(ScopeViewCommand::Close)
            .map_err(|x| x.into())
    }

    pub fn get_result_store(&self) -> Result<ResultsStore, DTTError> {
        let (tx, rx) = tokio::sync::oneshot::channel();
        self.command_tx.send(ScopeViewCommand::GetResults(tx))?;
        rx.blocking_recv().or(Err(DTTError::Export(
            "unknown".to_string(),
            "did not receive ResultsStore".to_string(),
        )))
    }
}
