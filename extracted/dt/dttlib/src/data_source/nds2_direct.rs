#![cfg(feature = "nds")]

use super::buffer;
use crate::data_source::{
    ChannelQuery, DataBlockReceiver, DataBlockSender, DataSource, DataSourceFeatures, DataSourceRef,
};
use crate::errors::DTTError;
use crate::params::channel_params::channel::Channel;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use ligo_hires_gps_time::{PipDuration, PipInstant};
use nds2_client_rs::{Stride, iterate};
use std::collections::{HashMap, HashSet};
use tokio::sync::mpsc;
use user_messages::UserMsgProvider;

/// Data source that gets all its data directly from an NDS2 server (no local caching).
#[derive(Clone)]
pub struct NDS2Direct {}

/// How far ahead is "run forever"
const INDEFINITE_FUTURE_SEC: f64 = 366.0 * 24.0 * 60.0 * 60.0;

impl DataSource for NDS2Direct {
    fn stream_data(
        &self,
        rc: Box<RunContext>,
        channels: &[Channel],
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError> {
        let calc_end_pip = match end_pip {
            Some(t) => t,
            None => start_pip + PipDuration::from_seconds(INDEFINITE_FUTURE_SEC),
        };

        let (db_tx, db_rx) = mpsc::channel(4);

        let new_chans_vec = Vec::from(channels);

        tokio::runtime::Handle::current().spawn_blocking(move || {
            Self::stream_loop(
                rc.ump_clone(),
                new_chans_vec,
                start_pip,
                calc_end_pip,
                Stride::Seconds(64),
                db_tx,
                true,
            )
        });

        Ok(db_rx)
    }

    fn start_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError> {
        let calc_end_pip = match view.span.optional_end_pip() {
            Some(t) => t,
            None => view.span.start_pip + PipDuration::from_seconds(INDEFINITE_FUTURE_SEC),
        };

        let (db_tx, db_rx) = mpsc::channel(4);

        let new_chans_vec = view.set.clone().into();

        view.block_tx = Some(db_tx.clone());

        let start_pip = view.span.start_pip;

        tokio::runtime::Handle::current().spawn_blocking(move || {
            Self::stream_loop(
                rc.ump_clone(),
                new_chans_vec,
                start_pip,
                calc_end_pip,
                Stride::Seconds(64),
                db_tx,
                false,
            )
        });

        Ok(db_rx)
    }

    fn update_scope_data(&self, rc: Box<RunContext>, view: &mut ScopeView) -> Result<(), DTTError> {
        let db_tx = match &view.block_tx {
            Some(s) => s.clone(),
            None => {
                return Err(DTTError::MissingDataStreamError(
                    "Data stream missing from scope view.  Cannot update.".into(),
                ));
            }
        };

        let calc_end_pip = match view.span.optional_end_pip() {
            Some(t) => t,
            None => view.span.start_pip + PipDuration::from_seconds(INDEFINITE_FUTURE_SEC),
        };

        let chans = view.set.clone().into();
        let start_pip = view.span.start_pip;

        tokio::runtime::Handle::current().spawn_blocking(move || {
            Self::stream_loop(
                rc.ump_clone(),
                chans,
                start_pip,
                calc_end_pip,
                Stride::Seconds(64),
                db_tx,
                false,
            )
        });

        Ok(())
    }

    fn capabilities(&self) -> HashSet<DataSourceFeatures> {
        HashSet::from([DataSourceFeatures::LiveStream, DataSourceFeatures::Stream])
    }

    fn as_ref(&self) -> DataSourceRef {
        self.clone().into()
    }

    fn find_channels(&self, _rc: Box<RunContext>, _query: &ChannelQuery) -> Result<(), DTTError> {
        Err(DTTError::NoCapabaility(
            "NDS2 direct data source".into(),
            "find channels".into(),
        ))
    }
}

impl NDS2Direct {
    fn stream_loop(
        rc: Box<dyn UserMsgProvider>,
        channels: Vec<Channel>,
        start_pip: PipInstant,
        end_pip: PipInstant,
        stride: Stride,
        data_block_tx: DataBlockSender,
        keep_alive: bool,
    ) {
        let chans: Vec<_> = channels.iter().map(|c| c.name.clone()).collect();

        let iter = match iterate(
            start_pip.to_gpst_seconds() as u64,
            (end_pip.to_gpst_seconds() as u64) + 1,
            stride,
            &chans,
        ) {
            Ok(i) => i,
            Err(e) => {
                let msg = format!("creation of NDS2 iterator failed: {}", e.to_string());
                rc.user_message_handle().error(msg);
                return;
            }
        };

        let _keep_alive_block_tx = if keep_alive {
            Some(data_block_tx.clone())
        } else {
            None
        };

        let mut weak_block_tx = data_block_tx.downgrade();

        'main: for buff in iter {
            let temp_block_tx = match weak_block_tx.upgrade() {
                Some(x) => x,
                None => break 'main,
            };

            // dtt expects cache::Buffer instead of a raw NDS2 buffer.
            let cache_buff: Vec<Vec<buffer::Buffer>> = match buff
                .iter()
                .map(|b| b.clone().try_into().and_then(|x| Ok(vec![x])))
                .collect()
            {
                Ok(b) => b,
                Err(e) => {
                    rc.user_message_handle()
                        .error(format!("Error converting NDS buffers: {}", e));
                    return;
                }
            };

            let chan_buf_pairs = channels.clone().into_iter().zip(cache_buff);

            let block = HashMap::from_iter(chan_buf_pairs);

            if let Err(_) = temp_block_tx.blocking_send(block) {
                break 'main;
            }

            weak_block_tx = temp_block_tx.downgrade();
        }
    }

    pub fn new() -> Self {
        NDS2Direct {}
    }
}
