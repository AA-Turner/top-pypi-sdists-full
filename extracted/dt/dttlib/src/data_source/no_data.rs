//! A data source that immediately dies without sending any data
//! Useful for checking analysis pipelines without running them.

use crate::data_source::{
    ChannelQuery, DataBlockReceiver, DataSource, DataSourceFeatures, DataSourceRef,
};
use crate::errors::DTTError;
use crate::params::channel_params::channel::Channel;
use crate::run_context::RunContext;
use crate::scope_view::ScopeView;
use ligo_hires_gps_time::PipInstant;
use std::collections::HashSet;
use tokio::sync::mpsc;

pub struct NoData {}

impl DataSource for NoData {
    fn stream_data(
        &self,
        _rc: Box<RunContext>,
        _channels: &[Channel],
        _start_pip: PipInstant,
        _end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError> {
        // _db_tx is dropped, so as soon as the pipelines start reading data, they close.
        let (_db_tx, db_rx) = mpsc::channel(4);

        Ok(db_rx)
    }

    fn start_scope_data(
        &self,
        _rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError> {
        let (db_tx, db_rx) = mpsc::channel(4);

        view.block_tx = Some(db_tx.clone());

        Ok(db_rx)
    }

    fn update_scope_data(
        &self,
        _rc: Box<RunContext>,
        _view: &mut ScopeView,
    ) -> Result<(), DTTError> {
        Ok(())
    }

    fn capabilities(&self) -> HashSet<DataSourceFeatures> {
        HashSet::from([DataSourceFeatures::LiveStream, DataSourceFeatures::Stream])
    }

    fn as_ref(&self) -> DataSourceRef {
        NoData {}.into()
    }

    fn find_channels(&self, _rc: Box<RunContext>, _query: &ChannelQuery) -> Result<(), DTTError> {
        Err(DTTError::NoCapabaility(
            "NoData data source".into(),
            "find channels".into(),
        ))
    }
}

impl NoData {
    pub fn new() -> Self {
        Self {}
    }
}
