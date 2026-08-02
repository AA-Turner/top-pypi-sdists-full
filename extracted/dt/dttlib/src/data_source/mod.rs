//! # handle data sources
//! such as NDS to servers, cache etc

pub(crate) mod buffer;
pub mod data_distributor;
pub mod data_source_pipeline;
pub mod dummy;
pub mod nds2_direct;
pub mod random;

mod channel_query;
pub mod nds_cache;
pub mod no_data;
pub use channel_query::ChannelQuery;

use crate::errors::DTTError;
use crate::params::test_params::StartTime;
use crate::run_context::RunContext;
use crate::timeline::{CountSegments, Timeline};
use buffer::Buffer;
use ligo_hires_gps_time::PipInstant;
use std::collections::{HashMap, HashSet};
use std::fmt::{Debug, Display, Formatter};
use std::ops::Deref;
use std::sync::Arc;
use tokio::sync::mpsc;

pub(crate) type DataBlockSender = mpsc::Sender<DataBlock>;
pub(crate) type DataBlockReceiver = mpsc::Receiver<DataBlock>;

use crate::params::channel_params::channel::Channel;
use crate::scope_view::ScopeView;
#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

#[derive(PartialEq, Eq, Hash)]
pub enum DataSourceFeatures {
    // /// Supports fetch operations (get a single block of data)
    // Fetch,
    /// Supports stream operations: send multiple blocks via channel
    Stream,

    /// Send live data in perpetuity via stream
    LiveStream,

    /// Query for channels
    QueryChannels,
}

impl Display for DataSourceFeatures {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            DataSourceFeatures::Stream => f.write_str("Stream"),
            DataSourceFeatures::LiveStream => f.write_str("LiveStream"),
            DataSourceFeatures::QueryChannels => f.write_str("QueryChannels"),
        }
    }
}

/// represents a single block of multichannel data
/// modeled after data returned from an NDS server
pub(crate) type DataBlock = HashMap<Channel, Vec<Buffer>>;

/// All data sources implement this trait
pub trait DataSource: Send + Sync {
    /// Stream data in chunks over a channel
    /// If end_pip is None, then live data is streamed indefinitely
    /// This is in order data meant for a single DTT test.
    fn stream_data(
        &self,
        rc: Box<RunContext>,
        channels: &[Channel],
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError>;

    /// continuously send (possibly) out of order data, as with ndscope.
    fn start_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError>;

    /// update an existing scope data stream with a DataBlockSender that was previously
    /// returned by a start_scope_data() call
    fn update_scope_data(&self, rc: Box<RunContext>, view: &mut ScopeView) -> Result<(), DTTError>;

    /// Get a list of available features for the data source
    fn capabilities(&self) -> HashSet<DataSourceFeatures>;

    fn as_ref(&self) -> DataSourceRef;

    /// Send to the user a message containing the results of the given channel query
    fn find_channels(&self, rc: Box<RunContext>, query: &ChannelQuery) -> Result<(), DTTError>;

    /// Returns true if the data source has the capabilities to complete the timeline.
    fn check_timeline_against_capabilities(
        &self,
        timeline: &Timeline,
    ) -> Result<(), HashSet<DataSourceFeatures>> {
        let mut missing_caps = HashSet::new();

        let cap = self.capabilities();
        if let StartTime::Unbound() = &timeline.start_time_pip {
            if !cap.contains(&DataSourceFeatures::LiveStream) {
                missing_caps.insert(DataSourceFeatures::LiveStream);
            }
        }
        if let CountSegments::Indefinite = &timeline.segment_count {
            if !cap.contains(&DataSourceFeatures::LiveStream) {
                missing_caps.insert(DataSourceFeatures::LiveStream);
            }
        }

        if !cap.contains(&DataSourceFeatures::Stream) {
            missing_caps.insert(DataSourceFeatures::Stream);
        }

        if missing_caps.len() > 0 {
            Err(missing_caps)
        } else {
            Ok(())
        }
    }

    /// Get the current time at the data source.  A good data source should override
    /// and actually query the data source.
    /// The default just gets the system time.  Just hope it's in sync!
    fn now(&self) -> PipInstant {
        PipInstant::now().unwrap_or(PipInstant::gpst_epoch())
    }
}

impl Debug for dyn DataSource {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "DataSource")
    }
}

/// wrappers needed for python

#[derive(Clone, Debug)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(name = "DataSource"))]
pub struct DataSourceRef(Arc<dyn DataSource>);

impl DataSourceRef {
    pub fn new(ds: Arc<dyn DataSource>) -> Self {
        Self(ds)
    }

    pub(crate) fn stream_data(
        &self,
        rc: Box<RunContext>,
        channels: &[Channel],
        start_pip: PipInstant,
        end_pip: Option<PipInstant>,
    ) -> Result<DataBlockReceiver, DTTError> {
        tokio::task::block_in_place(|| self.0.stream_data(rc, channels, start_pip, end_pip))
    }

    /// continuously send (possibly) out of order data, as with ndscope.
    pub(crate) fn start_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<DataBlockReceiver, DTTError> {
        tokio::task::block_in_place(|| self.0.start_scope_data(rc, view))
    }

    /// update an existing scope data stream with a DataBlockSender that was previously
    /// returned by a start_scope_data() call
    pub(crate) fn update_scope_data(
        &self,
        rc: Box<RunContext>,
        view: &mut ScopeView,
    ) -> Result<(), DTTError> {
        tokio::task::block_in_place(|| self.0.update_scope_data(rc, view))
    }
}

impl From<DataSourceRef> for Arc<dyn DataSource> {
    fn from(ds: DataSourceRef) -> Self {
        ds.0
    }
}

impl<T: DataSource + 'static> From<T> for DataSourceRef {
    fn from(ds: T) -> Self {
        DataSourceRef::new(Arc::new(ds))
    }
}

impl<T: DataSource + 'static> From<Arc<T>> for DataSourceRef {
    fn from(ds: Arc<T>) -> Self {
        DataSourceRef::new(ds)
    }
}

// Implement functions that look like an implementation of DataSource but aren't
// So it can be used as a DataSource, sort of.
#[cfg_attr(feature = "all", gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl DataSourceRef {
    pub fn now(&self) -> PipInstant {
        self.0.now()
    }
}

impl Deref for DataSourceRef {
    type Target = dyn DataSource;

    fn deref(&self) -> &Self::Target {
        self.0.as_ref()
    }
}
