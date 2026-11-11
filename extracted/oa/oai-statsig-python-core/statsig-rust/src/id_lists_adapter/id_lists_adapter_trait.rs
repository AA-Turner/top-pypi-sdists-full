use crate::{StatsigErr, StatsigRuntime};
use async_trait::async_trait;
use std::sync::Arc;
use std::time::Duration;
use std::{collections::HashMap, fmt};

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct IdListMetadata {
    #[serde(alias = "key")]
    pub name: String,
    pub url: String,

    #[serde(rename = "fileID")]
    pub file_id: Option<String>,

    pub size: u64,
    pub creation_time: i64,
}

pub struct IdListUpdate {
    pub raw_changeset: Option<String>,
    pub new_metadata: IdListMetadata,
}

/// Private HTTP adapter handoff. Capture the previously committed cursor so
/// a concurrent replacement cannot install an older image or raw fallback.
#[doc(hidden)]
pub struct IdListUpdateBase {
    pub(crate) previous: Option<IdListMetadata>,
    pub(crate) list: Option<super::IdList>,
}

#[async_trait]
pub trait IdListsAdapter: Send + Sync {
    /// Called during Statsig::initialize. Mostly to attach the listener.
    /// Scheduling background threads should be done in the IdListsAdapter::schedule_background_sync function.
    ///
    /// # Arguments
    ///
    /// * `statsig_runtime` - The Statsig runtime instance.
    /// * `listener` - The listener to push updates to.
    async fn start(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
        listener: Arc<dyn IdListsUpdateListener + Send + Sync>,
    ) -> Result<(), StatsigErr>;

    /// Called during Statsig::shutdown or Statsig::shutdown_with_timeout.
    /// This function gives some grace period to the adapter to finish its work.
    ///
    /// # Arguments
    ///
    /// * `timeout` - The timeout for the shutdown.
    async fn shutdown(&self, timeout: Duration) -> Result<(), StatsigErr>;

    /// Called during Statsig::initialize.
    /// This function is used to schedule the background sync thread and is called just after IdListsAdapter::start
    ///
    /// # Arguments
    ///
    /// * `statsig_runtime` - The Statsig runtime instance.
    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr>;

    /// Returns the type name of the adapter. Used for logging and error messages.
    fn get_type_name(&self) -> String;
}

pub trait IdListsUpdateListener: Send + Sync {
    fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata>;

    fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>);

    fn did_receive_id_list_updates_with_propagation(
        &self,
        updates: HashMap<String, IdListUpdate>,
        _propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) {
        self.did_receive_id_list_updates(updates);
    }

    /// Applies a subset of ID-list updates without deleting lists omitted from
    /// the update. Lazy materialization uses this path for on-demand loads.
    fn did_receive_partial_id_list_updates_with_propagation(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) {
        self.did_receive_id_list_updates_with_propagation(updates, propagation);
    }

    /// Fallible publication hook used by adapters that persist a committed snapshot.
    /// Existing listeners retain their current callback behavior by default.
    fn try_receive_id_list_updates_with_propagation(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) -> Result<(), StatsigErr> {
        self.did_receive_id_list_updates_with_propagation(updates, propagation);
        Ok(())
    }

    /// Replaces the installed catalog after one or more file downloads failed.
    /// The map includes retained lists; omitted names may be removed. Persistent
    /// listeners must not advance their last successful refresh timestamp.
    fn try_receive_incomplete_id_list_refresh(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) -> Result<(), StatsigErr> {
        self.try_receive_id_list_updates_with_propagation(updates, propagation)
    }

    /// Whether eager private HTTP initialization should offload index builds to a blocking worker.
    fn uses_parallel_id_list_init(&self) -> bool {
        false
    }

    /// Publishes an opted-in startup batch. Only successfully downloaded bodies need indexing.
    fn try_receive_eager_id_list_updates(
        &self,
        updates: HashMap<String, IdListUpdate>,
        propagation: HashMap<String, super::IdListPropagationUpdate>,
        incomplete: bool,
        _successful_downloads: u64,
    ) -> Result<(), StatsigErr> {
        if incomplete {
            self.try_receive_incomplete_id_list_refresh(updates, propagation)
        } else {
            self.try_receive_id_list_updates_with_propagation(updates, propagation)
        }
    }

    #[doc(hidden)]
    fn supports_id_list_snapshot_updates(&self) -> bool {
        false
    }

    /// Publish verified private EF bases and ordinary raw updates together.
    #[doc(hidden)]
    fn try_receive_id_list_snapshot_updates(
        &self,
        _updates: HashMap<String, IdListUpdate>,
        _bases: HashMap<String, IdListUpdateBase>,
        _propagation: HashMap<String, super::IdListPropagationUpdate>,
        _mode: IdListPublicationMode,
        _eager_downloads: Option<u64>,
    ) -> Result<(), StatsigErr> {
        Err(StatsigErr::InvalidOperation(
            "unsupported ID-list snapshot update".into(),
        ))
    }

    /// Whether HTTP publication must run on a blocking worker.
    fn requires_blocking_id_list_publication(&self) -> bool {
        false
    }

    /// Whether this listener can install immutable membership storage directly.
    fn supports_id_list_snapshots(&self) -> bool {
        false
    }

    /// Atomically installs a complete materialized catalog without replaying strings.
    /// Unsupported listeners use the ordinary HTTP changeset path instead.
    fn did_receive_id_list_snapshot(
        &self,
        _lists: HashMap<String, super::IdList>,
        _propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) -> Result<(), StatsigErr> {
        Err(StatsigErr::InvalidOperation(
            "ID-list listener does not support immutable snapshots".to_string(),
        ))
    }
}

impl fmt::Debug for dyn IdListsAdapter {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.get_type_name())
    }
}

#[derive(Clone, Copy, PartialEq, Eq)]
#[doc(hidden)]
pub enum IdListPublicationMode {
    Replace,
    IncompleteRefresh,
    Merge,
}
