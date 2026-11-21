use super::shared_id_list_format::{digest, hex};
use super::{IdList, IdListEncoding, IdListMetadata, SharedIdListStore};
use crate::StatsigOptions;
use crate::networking::normalize_default_cdn_id_lists_manifest_url;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use std::collections::HashMap;
use std::io;
use std::path::PathBuf;
use std::sync::Arc;
use tokio::sync::Semaphore;

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
    pub(crate) fn from_options(sdk_key: &str, options: &StatsigOptions) -> Option<Self> {
        let flags = options.experimental_flags.as_ref()?;
        if !flags.contains("shared_initial_id_list_base") {
            return None;
        }
        // LocalIdLists checks whether this worker can share files.
        let directory = PathBuf::from(options.shared_id_lists_dir.as_deref()?).join(CACHE_DIR);
        let source = serde_json::to_vec(&(
            CACHE_DIR,
            sdk_key,
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref()),
            &options.download_id_list_file_api,
            options.fallback_to_statsig_api.unwrap_or(false),
        ))
        .expect("ID-list source options serialize");
        let _output_scope = crate::output_policy::OutputPolicy::from_options(Some(options)).enter();
        Some(Self {
            encoding: if options.enable_id_list_elias_fano == Some(true) {
                IdListEncoding::EliasFano
            } else {
                IdListEncoding::Hash
            },
            directory: std::path::absolute(&directory).unwrap_or(directory),
            source: hex(&digest(&source)),
            ops_stats: OPS_STATS
                .get_for_instance_with_options(options.get_sdk_instance_id(sdk_key), Some(options)),
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

    fn store(&self, name: &str) -> io::Result<SharedIdListStore> {
        SharedIdListStore::for_initial_base(&self.directory, &self.source, name, self.encoding)
    }

    pub(super) fn lookup(&self, target: &IdListMetadata) -> Option<IdList> {
        let cached = self
            .store(&target.name)
            .and_then(|store| {
                store.load_initial_base(&target.name, |meta| {
                    meta.file_id == target.file_id
                        && meta.creation_time == target.creation_time
                        && meta.size > 0
                        && meta.size <= target.size
                })
            })
            .inspect_err(|_| self.record_failure("read"))
            .ok()?;
        self.record_lookup(cached.is_some());
        cached.map(|list| with_manifest_url(list, target))
    }

    pub(super) fn offer(&self, candidate: IdList) -> IdList {
        self.install(&candidate)
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

    fn install(&self, candidate: &IdList) -> io::Result<Option<IdList>> {
        let target = &candidate.metadata;
        let store = self.store(&target.name)?;
        let Some(lease) = store.try_acquire_lease()? else {
            return Ok(None);
        };
        // Validate only bases new enough to keep.
        let existing = match store.load_initial_base(&target.name, |meta| {
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
        let _ = store.cleanup(&lease);
        if let Some(existing) = existing {
            if existing.metadata.file_version() == target.file_version() {
                return Ok(Some(with_manifest_url(existing, target)));
            }
            // File IDs have no ordering. Keep the first valid prefix on timestamp ties.
            return Ok(None);
        }
        let mut base = candidate.clone();
        base.metadata.url.clear();
        let mut catalog = store.publish_with_clock(
            &lease,
            &HashMap::from([(target.name.clone(), base)]),
            &HashMap::new(),
            &HashMap::new(),
            None,
            || 0,
        )?;
        Ok(catalog
            .lists
            .remove(&target.name)
            .map(|list| with_manifest_url(list, target)))
    }
}

fn with_manifest_url(mut list: IdList, target: &IdListMetadata) -> IdList {
    list.metadata.url.clone_from(&target.url);
    list
}

#[cfg(test)]
#[path = "__tests__/shared_initial_base_cache_tests.rs"]
mod tests;
