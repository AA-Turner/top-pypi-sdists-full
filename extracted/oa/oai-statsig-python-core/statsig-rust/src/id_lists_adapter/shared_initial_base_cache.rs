use super::shared_id_list_format::{digest, hex};
use super::{IdList, IdListEncoding, IdListMetadata};
use crate::StatsigOptions;
use crate::networking::normalize_default_cdn_id_lists_manifest_url;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use std::io;
use std::path::PathBuf;
use std::sync::Arc;
use store::BaseStore;
use tokio::sync::Semaphore;

#[path = "shared_id_list_store.rs"]
mod store;

const CACHE_DIR: &str = "initial-base-v1";
const STORAGE_WORKERS: u32 = 2;

/// One immutable prefix per list. Each worker's manifest authorizes reads.
pub(crate) struct SharedInitialBaseCache {
    directory: PathBuf,
    source: String,
    ops_stats: Arc<OpsStatsForInstance>,
    pub(super) encoding: IdListEncoding,
    pub(super) permits: Arc<Semaphore>,
}

impl SharedInitialBaseCache {
    pub(super) fn from_options(
        sdk_key: &str,
        options: &StatsigOptions,
        ops_stats: &Arc<OpsStatsForInstance>,
    ) -> Option<Self> {
        if options.disable_disk_access == Some(true)
            || options.disable_network == Some(true)
            || options.proxy_config.is_some()
        {
            return None;
        }
        let root = options
            .shared_id_lists_dir
            .as_deref()
            .filter(|s| !s.trim().is_empty())?;
        let directory = std::path::absolute(root).ok()?.join(CACHE_DIR);
        let source = serde_json::to_vec(&(
            CACHE_DIR,
            sdk_key,
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref()),
            &options.download_id_list_file_api,
            options.fallback_to_statsig_api.unwrap_or(false),
        ))
        .expect("ID-list source options serialize");
        Some(Self {
            encoding: IdListEncoding::from_options(Some(options)),
            directory,
            source: hex(&digest(&source)),
            ops_stats: ops_stats.clone(),
            permits: Arc::new(Semaphore::new(STORAGE_WORKERS as usize)),
        })
    }

    pub(super) async fn drain(&self) {
        drop(self.permits.acquire_many(STORAGE_WORKERS).await);
    }

    pub(super) fn eligible(metadata: &IdListMetadata) -> bool {
        metadata.size > 0
            && metadata.creation_time >= 0
            && metadata.file_id.as_deref().is_some_and(|id| !id.is_empty())
    }

    fn store(&self, name: &str) -> io::Result<BaseStore> {
        BaseStore::new(&self.directory, &self.source, name, self.encoding)
    }

    pub(super) fn lookup(&self, target: &IdListMetadata) -> Option<IdList> {
        let cached = self
            .store(&target.name)
            .inspect_err(|_| self.record_failure("read"))
            .and_then(|store| self.read_compatible(&store, target, target.size))
            .ok()?;
        self.record_lookup(cached.is_some());
        cached
    }

    fn read_compatible(
        &self,
        store: &BaseStore,
        target: &IdListMetadata,
        manifest_size: u64,
    ) -> io::Result<Option<IdList>> {
        let cached = store
            .load(&target.name, |meta| compatible(meta, target, manifest_size))
            .inspect_err(|_| self.record_failure("read"))?;
        Ok(cached.map(|list| with_manifest_url(list, target)))
    }

    pub(super) fn offer_prefix(&self, candidate: IdList, manifest_size: u64) -> IdList {
        self.install(&candidate, manifest_size)
            .inspect_err(|_| self.record_failure("publish"))
            .ok()
            .flatten()
            .unwrap_or(candidate)
    }

    fn record_lookup(&self, hit: bool) {
        let result = if hit { "hit" } else { "miss" };
        self.increment("shared_id_lists.cache.lookup", "result", result);
    }

    fn record_failure(&self, reason: &'static str) {
        self.increment("shared_id_lists.failure", "reason", reason);
    }

    fn increment(&self, metric: &'static str, tag: &'static str, value: &'static str) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            metric.into(),
            1.0,
            Some([(tag.into(), value.into())].into()),
        ));
    }

    fn install(&self, candidate: &IdList, manifest_size: u64) -> io::Result<Option<IdList>> {
        let target = &candidate.metadata;
        let store = self.store(&target.name)?;
        let Some(lock) = store.try_lock()? else {
            return Ok(self
                .read_compatible(&store, target, manifest_size)
                .unwrap_or_default());
        };
        // Validate only bases new enough to keep.
        let existing = match store.load(&target.name, |meta| {
            meta.creation_time >= target.creation_time
        }) {
            Ok(list) => list,
            Err(error)
                if matches!(
                    error.kind(),
                    io::ErrorKind::InvalidData | io::ErrorKind::NotFound
                ) =>
            {
                None
            }
            Err(error) => return Err(error),
        };
        if let Some(existing) = existing {
            if compatible(&existing.metadata, target, manifest_size) {
                return Ok(Some(with_manifest_url(existing, target)));
            }
            // File IDs have no ordering. Keep the first valid prefix on timestamp ties.
            return Ok(None);
        }
        store.publish(&lock, candidate).map(Some)
    }
}

fn compatible(meta: &IdListMetadata, target: &IdListMetadata, manifest_size: u64) -> bool {
    meta.file_id == target.file_id
        && meta.creation_time == target.creation_time
        && meta.size > 0
        && meta.size <= manifest_size
}

fn with_manifest_url(mut list: IdList, target: &IdListMetadata) -> IdList {
    list.metadata.url.clone_from(&target.url);
    list
}

#[cfg(test)]
#[path = "__tests__/shared_initial_base_cache_tests.rs"]
mod tests;
