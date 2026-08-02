mod gap_handler;

use super::buffer::Buffer;
use crate::data_source::{
    ChannelQuery, DataBlock, DataBlockReceiver, DataBlockSender, DataSource, DataSourceFeatures,
    DataSourceRef,
};
use crate::errors::DTTError;
use crate::params::channel_params::TrendType;
use crate::params::channel_params::channel::Channel;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use crate::user::ResponseToUser;
#[cfg(not(feature = "python"))]
use dtt_macros::new;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use log::debug;
use nds_cache_rs::{CacheHandle, init};
#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyclass_enum, gen_stub_pymethods};
use std::collections::{HashMap, HashSet};
use std::fmt::Display;
use std::ops::Range;
use std::sync::OnceLock;
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;
use user_messages::UserMessageProviderBase;

#[derive(Clone, Copy, PartialEq)]
#[cfg_attr(feature = "all", gen_stub_pyclass_enum)]
#[cfg_attr(feature = "python", pyclass(frozen, eq))]
pub enum DataFlow {
    /// Data is sent repeatedly as
    /// more of the request is filled in.
    ///
    /// Each response gives all the data available.
    ///
    /// This is how NDScope expects data.
    Unordered,

    /// Data is returned from the earliest time stamp to the latest.
    /// Data is returned only once.
    /// This is how DTT expects data.
    Ordered,
}

impl Display for DataFlow {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DataFlow::Unordered => write!(f, "Unordered"),
            DataFlow::Ordered => write!(f, "Ordered"),
        }
    }
}

/// The global cache handle used by all cache datasource objects
static cache_handle: OnceLock<CacheHandle> = OnceLock::new();

/// Data source that gets all its data directly from an NDS2 server (no local caching).
#[derive(Clone)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(frozen))]
pub struct NDS2Cache {
    /// default path to store cache when saving
    _default_file_path: String,

    size_bytes: usize,
}

/// How far ahead is "run forever"
const INDEFINITE_FUTURE_SEC: i64 = 366 * 24 * 60 * 60;

impl DataSource for NDS2Cache {
    fn stream_data(
        &self,
        rc: Box<RunContext>,
        channels: &[Channel],
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError> {
        let online = end_pip.is_none();

        let calc_end_pip = match end_pip {
            Some(t) => t,
            None => start_pip + PipDuration::from_sec(INDEFINITE_FUTURE_SEC),
        };

        let interval: Range<PipInstant> = Range {
            start: start_pip,
            end: calc_end_pip,
        };

        let (db_tx, db_rx) = mpsc::channel(4);

        let new_chan_names = channels.iter().map(|c| c.name.clone()).collect();

        let handle = tokio::runtime::Handle::current();
        let _guard = handle.enter();
        futures::executor::block_on(self.clone().ordered_stream_loop(
            rc,
            new_chan_names,
            interval,
            db_tx,
            online,
        ))?;

        Ok(db_rx)
    }

    fn start_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError> {
        let (db_tx, db_rx) = mpsc::channel(1);

        view.block_tx = Some(db_tx.clone());

        view.data_task_cancel_token = Some(CancellationToken::new());

        // the following two lines and the future::executor::block_on
        // on the third line are needed to call an async function
        // from within an async context from a non-async function.
        let handle = tokio::runtime::Handle::current();
        let _guard = handle.enter();
        futures::executor::block_on(self.clone().scope_view_stream_loop(rc, view))?;

        Ok(db_rx)
    }

    fn update_scope_data(&self, rc: Box<RunContext>, view: &mut ScopeView) -> Result<(), DTTError> {
        if let Some(tx) = &view.span_update_tx {
            if view.span.online {
                return tx.send(view.span.span_pip).map_err(|e| e.into());
            }
        }

        view.reset_count += 1;

        if let Some(c) = &view.data_task_cancel_token {
            c.cancel();
        }
        view.data_task_cancel_token = Some(CancellationToken::new());

        // the following two lines and the future::executor::block_on
        // on the third line are needed to call an async function
        // from within an async context from a non-async function.
        let handle = tokio::runtime::Handle::current();
        let _guard = handle.enter();
        futures::executor::block_on(self.clone().scope_view_stream_loop(rc, view))?;

        Ok(())
    }

    fn capabilities(&self) -> HashSet<DataSourceFeatures> {
        HashSet::from([
            DataSourceFeatures::LiveStream,
            DataSourceFeatures::Stream,
            DataSourceFeatures::QueryChannels,
        ])
    }

    fn as_ref(&self) -> DataSourceRef {
        self.clone().into()
    }

    fn find_channels(&self, rc: Box<RunContext>, query: &ChannelQuery) -> Result<(), DTTError> {
        let handle = tokio::runtime::Handle::current();
        let new_self = self.clone();
        let cloned_query = query.clone();
        handle.spawn(new_self.find_channels_blocking(rc, cloned_query));
        Ok(())
    }
}

async fn wrap_buffers(
    mut rx: tokio::sync::mpsc::Receiver<Vec<nds_cache_rs::buffer::Buffer>>,
) -> tokio::sync::mpsc::Receiver<Vec<Buffer>> {
    let (buf_tx, buf_rx) = tokio::sync::mpsc::channel(1);

    tokio::spawn(async move {
        loop {
            let buffers = match rx.recv().await {
                Some(b) => b.into_iter().map(|x| x.into()).collect(),
                None => break,
            };
            if let Err(_) = buf_tx.send(buffers).await {
                break;
            }
        }
    });

    buf_rx
}

impl NDS2Cache {
    /// For DTT stream.  All data must be consumed one-time only, and in order.
    /// The stream cannot drop any data from the cache.
    async fn ordered_stream_loop(
        self,
        rc: Box<RunContext>,
        channel_names: Vec<String>,
        interval: Range<PipInstant>,
        data_block_tx: DataBlockSender,
        online: bool,
    ) -> Result<(), DTTError> {
        let cache = self.initialize_cache().await?;

        let mut data_rx = if online {
            cache.get_live(channel_names).await
        } else {
            cache.get_past_ordered(interval, channel_names).await
        };

        let found_all = true;

        let mut count: u64 = 0;

        tokio::spawn(async move {
            'main: loop {
                debug!("Ordered: {}: cache data len = {}", count, data_rx.len());

                let rx = data_rx.recv().await;

                let buffs = match rx {
                    None => break 'main,
                    Some(b) => match b {
                        Ok(x) => x.into_iter().map(|b| b.into()).collect(),
                        Err(e) => {
                            rc.user_messages
                                .error(format!("Error reading data from cache: {}", e));
                            continue 'main;
                        }
                    },
                };

                count += 1;

                if let Err(e) = send_block(buffs, &data_block_tx).await {
                    match e {
                        DTTError::TokioMPSCSend(_) => break 'main,
                        e => {
                            rc.user_messages
                                .error(format!("Error sending data to analysis: {}", e));
                        }
                    }
                }
            }

            if found_all {
                rc.user_messages.clear_message("MissingCacheChannel");
            }
        });

        Ok(())
    }

    /// initialize cache if need be
    async fn initialize_cache(&self) -> Result<&CacheHandle, DTTError> {
        if cache_handle.get().is_none() {
            let size = self.size_bytes;

            let cache = init(size).await?;

            cache_handle.get_or_init(move || cache);
        }
        match cache_handle.get() {
            Some(h) => Ok(h),
            None => Err(DTTError::NDSCacheError(
                "Tried to get an uninitializede cache handle".to_string(),
            )),
        }
    }

    /// transform from nds_cache_rs buffers to dttlib buffers

    /// Produce a watch channel that always has the latest
    /// result from the cache
    async fn start_scope_view_get_latest(
        self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<mpsc::Receiver<Vec<Buffer>>, DTTError> {
        rc.clone()
            .user_message_handle()
            .clear_message("stream_error");

        let cache = self.initialize_cache().await?;

        let start_pip = view.span.start_pip;
        let end_pip = view.span.end_pip();

        let interval: Range<PipInstant> = start_pip..end_pip;

        let channel_names = view.set.to_resolved_channel_names();

        let (result_watch_tx, result_watch_rx_cache) = mpsc::channel(1);

        // transform output into wrapped buffer
        let result_watch_rx_orig = wrap_buffers(result_watch_rx_cache).await;

        let (span_update_tx, mut data_rx, result_watch_rx) = if view.span.online {
            rc.clone()
                .user_message_handle()
                .set_notice("online_status", "Retrieving online ...");
            let (d_tx, d_rx) = cache
                .get_live_with_window_unordered(end_pip - start_pip, channel_names)
                .await;
            (
                Some(d_tx),
                d_rx,
                gap_handler::setup_gap_handler(rc.clone(), result_watch_rx_orig, self.size_bytes)
                    .await,
            )
            //(Some(d_tx), d_rx, result_watch_rx_orig,)
        } else if view.snapshot {
            rc.clone()
                .user_message_handle()
                .set_notice("stream_status", "Retrieving snapshot ...");
            (
                None,
                cache.get_snapshot(interval, channel_names).await,
                gap_handler::setup_gap_handler(rc.clone(), result_watch_rx_orig, self.size_bytes)
                    .await,
            )
        } else {
            rc.clone()
                .user_message_handle()
                .set_notice("stream_status", "Retrieving stored ...");
            (
                None,
                cache.get_past_unordered(interval, channel_names).await,
                gap_handler::setup_gap_handler(rc.clone(), result_watch_rx_orig, self.size_bytes)
                    .await,
            )
        };

        view.span_update_tx = span_update_tx;

        let id = view.id;
        let reset_count = view.reset_count;
        let cancel_token = match &view.data_task_cancel_token {
            Some(s) => s.clone(),
            None => {
                return Err(DTTError::MissingDataStreamError(
                    "Cancel token missing for scope view data stream".into(),
                ));
            }
        };

        tokio::spawn(async move {
            let mut count: u64 = 0;
            let mut results = Vec::with_capacity(100);
            rc.clone()
                .user_message_handle()
                .clear_message("stream_error");

            'main: loop {
                results.clear();
                let buffs = tokio::select! {
                    _ = cancel_token.cancelled() => {
                        debug!("{}.{}: cancelled", id, reset_count);
                        break 'main;
                    },
                    x = data_rx.recv_many(&mut results, 100) =>  {
                        if 0 == x {
                            debug!("{}.{}: got 0 results from cache", id, reset_count);
                            break 'main
                        }
                        else {
                            debug!("{}.{}: got {} results from cache", id, reset_count, x);
                            let mut last_good = x;
                            for (i,r) in results[0..x].iter().enumerate() {
                                match r {
                                    Ok(z) => {
                                        last_good = i;
                                        debug!("{}.{}: got buff {}", id, reset_count, z.len());
                                    }
                                    Err(nds_cache_rs::Error::NDSClearError) => {
                                        rc.clone().user_message_handle().clear_message("stream_error");
                                    }
                                    Err(e) => {
                                        let severity = match &e {
                                            nds_cache_rs::Error::NDSRestarted(_) => user_messages::Severity::Warning,
                                            _ => user_messages::Severity::Error,
                                        };
                                        rc.clone().user_message_handle().set_message(severity, "stream_error", e.to_string());
                                    }
                                }
                            }
                            if last_good < x {
                                results.remove(last_good).expect("last_good must be guaranteed to be in range")
                            } else {
                                continue 'main;
                            }
                        }
                    }
                };

                count += 1;

                if count == 1 && buffs.len() > 0 {
                    let chan = buffs[0].channel().clone().try_into();
                    match chan {
                        Ok(Channel {
                            trend_type: TrendType::Raw,
                            ..
                        }) => {
                            rc.clone()
                                .user_message_handle()
                                .set_notice("stream_status", "Retrieving raw ...");
                        }
                        Ok(Channel {
                            trend_type: TrendType::Second,
                            ..
                        }) => {
                            rc.clone()
                                .user_message_handle()
                                .set_notice("stream_status", "Retrieving second trends ...");
                        }
                        Ok(Channel {
                            trend_type: TrendType::Minute,
                            ..
                        }) => {
                            rc.clone()
                                .user_message_handle()
                                .set_notice("stream_status", "Retrieving minute trends ...");
                        }
                        Err(_) => (),
                    }
                }

                if result_watch_tx.send(buffs).await.is_err() {
                    break 'main;
                }
            }
            rc.clone()
                .user_message_handle()
                .clear_message("stream_status");
            rc.user_message_handle().clear_message("online_status");
        });

        Ok(result_watch_rx)
    }

    /// Unordered stream loop only sends the latest data    
    async fn scope_view_stream_loop(
        self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<(), DTTError> {
        let dblock_tx = match &view.block_tx {
            Some(s) => s.clone(),
            None => {
                return Err(DTTError::MissingDataStreamError(
                    "A block channel is missing from scope view.  Cannot create a data stream."
                        .into(),
                ));
            }
        };

        let found_all = true;

        let mut results_watch_rx = self.start_scope_view_get_latest(rc.clone(), view).await?;

        let span_update_rx = view.span_update_tx.as_ref().map(|s| s.subscribe());

        tokio::spawn(async move {
            // track end points per-channel, only sending blocks with end points >= the latest end points
            let mut latest_ends: HashMap<String, PipInstant> = HashMap::new();
            'main: loop {
                let buffs = match results_watch_rx.recv().await {
                    Some(b) => b,
                    None => {
                        log::debug!("get_latest channel closed");
                        break 'main;
                    }
                };

                if let Err(e) = send_latest_block(buffs, &dblock_tx, &mut latest_ends).await {
                    match e {
                        DTTError::TokioMPSCSend(_) => {
                            // subtract off 1 because the last frame didn't make it through
                            break 'main;
                        }
                        e => {
                            rc.user_messages
                                .error(format!("Error sending data to analysis: {}", e));
                        }
                    }
                }
            }

            if found_all {
                rc.user_messages.clear_message("MissingCacheChannel");
            }
        });

        drop(span_update_rx);

        Ok(())
    }

    /// block on find channels, sending results to the user app
    /// when received
    async fn find_channels_blocking(self, rc: Box<RunContext>, query: ChannelQuery) {
        let handle = match self.initialize_cache().await {
            Ok(h) => h,
            Err(_) => {
                rc.user_messages
                    .error("Failed to open the interface to the local cache to request channels.");
                return;
            }
        };
        let c = match tokio::task::block_in_place(|| handle.find_channels(&(query.into()))) {
            Ok(c) => c,
            Err(e) => {
                rc.user_messages
                    .set_error("find_channels", format!("Error finding channels: {}", e));
                return;
            }
        };
        rc.user_messages.clear_message("find_channels");
        let channels = c
            .into_iter()
            .filter_map(|c| match c.try_into() {
                Ok(c) => Some(c),
                Err(e) => {
                    rc.user_messages
                        .error(format!("Error converting channel: {}", e));
                    None
                }
            })
            .collect();
        let rc2 = rc.clone();

        //we don't care if the channel has been closed
        let _ = rc
            .output_handle
            .send(rc2, ResponseToUser::ChannelQueryResult { channels });
    }
}

async fn send_latest_block(
    buffs: Vec<Buffer>,
    data_block_tx: &mpsc::Sender<DataBlock>,
    latest_ends: &mut HashMap<String, PipInstant>,
) -> Result<(), DTTError> {
    let mut block: HashMap<Channel, Vec<Buffer>> = HashMap::new();
    for buff in buffs {
        debug!(
            "sending block @ {} for {}",
            buff.start().to_gpst_seconds(),
            buff.channel().name()
        );
        let cname = buff.channel().name();

        // if let Some(e) = latest_ends.get(cname) {
        //     if buff.end() < *e {
        //         continue;
        //     }
        // }

        latest_ends.insert(cname.clone(), buff.end());

        let c1 = (&buff).try_into()?;

        match block.get_mut(&c1) {
            Some(v) => v.push(buff),
            None => {
                block.insert(c1, vec![buff]);
            }
        }
    }

    Ok(data_block_tx.send(block).await?)
}

async fn send_block(
    buffs: Vec<Buffer>,
    data_block_tx: &mpsc::Sender<DataBlock>,
) -> Result<(), DTTError> {
    let mut block: HashMap<Channel, Vec<Buffer>> = HashMap::new();
    for buff in buffs {
        let c1 = (&buff).try_into()?;

        match block.get_mut(&c1) {
            Some(v) => v.push(buff),
            None => {
                block.insert(c1, vec![buff]);
            }
        }
    }

    Ok(data_block_tx.send(block).await?)
}

#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl NDS2Cache {
    #[new]
    pub fn new(size_bytes: usize, default_file_path: String) -> Self {
        Self {
            _default_file_path: default_file_path,
            size_bytes,
        }
    }

    pub fn as_ref(&self) -> DataSourceRef {
        self.clone().into()
    }
}
