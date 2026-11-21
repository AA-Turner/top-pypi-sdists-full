use super::remote_id_lists::RemoteIdListResolver;
use super::{Statsig, TAG};
use crate::evaluation::evaluation_details::EvaluationDetails;
use crate::evaluation::evaluator::SpecType;
use crate::id_lists_adapter::{
    SharedInitialBaseCache, StatsigSharedIdListsAdapter, id_list_load_timing,
};
use crate::networking::NetworkClient;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::spec_store::{SpecStore, SpecStoreData};
use crate::statsig_err::StatsigErr;
use crate::statsig_runtime::StatsigRuntime;
use crate::{
    IdListsAdapter, StatsigHttpIdListsAdapter, StatsigOptions, log_error_to_statsig_and_console,
};
use std::collections::HashMap;
use std::sync::{Arc, mpsc};
use std::time::{Duration, Instant};
use tokio::task::JoinSet;

/// Selects who loads ID lists for this SDK instance.
pub(super) enum LocalIdLists {
    Disabled,
    /// The caller supplies the adapter.
    Custom(Arc<dyn IdListsAdapter>),
    /// This worker fetches lists over HTTP, eagerly or on demand.
    Worker(Arc<StatsigHttpIdListsAdapter>),
    /// One publisher fetches lists for eager workers sharing a directory.
    Catalog(Arc<StatsigSharedIdListsAdapter>),
}

impl LocalIdLists {
    pub(super) fn new(
        sdk_key: &str,
        options: &StatsigOptions,
        spec_store: &Arc<SpecStore>,
    ) -> Self {
        if let Some(adapter) = &options.id_lists_adapter {
            return Self::Custom(adapter.clone());
        }
        if options.enable_id_lists != Some(true) {
            return Self::Disabled;
        }
        let can_share = !options.disable_disk_access.unwrap_or(false)
            && !options.disable_network.unwrap_or(false)
            && options.proxy_config.is_none()
            && options
                .shared_id_lists_dir
                .as_deref()
                .is_some_and(|path| !path.trim().is_empty());
        let base_cache = if can_share {
            SharedInitialBaseCache::from_options(sdk_key, options)
        } else {
            None
        };
        if can_share && base_cache.is_none() && options.lazy_load_id_lists != Some(true) {
            return Self::Catalog(Arc::new(
                StatsigSharedIdListsAdapter::new(sdk_key, options)
                    .with_listener(spec_store.clone()),
            ));
        }
        Self::Worker(Arc::new(
            StatsigHttpIdListsAdapter::new_with_store(sdk_key, options, spec_store.clone())
                .with_initial_base_cache(base_cache),
        ))
    }

    pub(super) fn adapter(&self) -> Option<Arc<dyn IdListsAdapter>> {
        match self {
            Self::Disabled => None,
            Self::Custom(adapter) => Some(adapter.clone()),
            Self::Worker(adapter) => Some(adapter.clone()),
            Self::Catalog(adapter) => Some(adapter.clone()),
        }
    }

    pub(super) fn force_shutdown(&self) {
        match self {
            Self::Worker(adapter) => adapter.force_shutdown(),
            Self::Catalog(adapter) => adapter.force_shutdown(),
            _ => {}
        }
    }

    pub(super) fn network(&self) -> Option<Arc<NetworkClient>> {
        match self {
            Self::Worker(adapter) => Some(adapter.network()),
            _ => None,
        }
    }

    pub(super) fn observe_revisions(&self, resolver: &Arc<RemoteIdListResolver>) {
        let slot = match self {
            Self::Worker(adapter) => &adapter.membership_resolver,
            Self::Catalog(adapter) => &adapter.membership_resolver,
            _ => return,
        };
        let _ = slot.set(Arc::downgrade(resolver));
    }

    fn load_missing(
        &self,
        missing: Vec<String>,
        runtime: &Arc<StatsigRuntime>,
        ops_stats: &Arc<OpsStatsForInstance>,
        remaining_wait: &mut Duration,
        waited: &mut Duration,
    ) -> LazyIdListLoadStatus {
        let Self::Worker(adapter) = self else {
            return LazyIdListLoadStatus::Failed;
        };
        let adapter = adapter.clone();
        let (sender, receiver) = mpsc::sync_channel(1);
        // Only actual loads enter timing collection; warm evaluations skip it.
        let record_wait = adapter.load_timings_enabled;
        let timing = record_wait.then(|| (Instant::now(), Arc::clone(ops_stats)));
        if let Err(error) = runtime.spawn(LAZY_ID_LIST_LOAD_TAG, move |_| async move {
            // Each adapter coalesces loads for the same list and limits
            // concurrent body downloads.
            let mut loads = JoinSet::new();
            for name in missing {
                let adapter = Arc::clone(&adapter);
                loads.spawn(async move { adapter.process_id_list(&name).await });
            }

            let mut load_result = Ok(());
            while let Some(result) = loads.join_next().await {
                let error = match result {
                    Ok(Ok(())) => continue,
                    Ok(Err(error)) => error,
                    Err(error) => StatsigErr::ThreadFailure(error.to_string()),
                };
                if load_result.is_ok() {
                    load_result = Err(error);
                }
            }
            // The receiver may be gone after a timeout; completed work
            // remains published for a later evaluation.
            let elapsed = timing.as_ref().map(|(started, _)| started.elapsed());
            let succeeded = load_result.is_ok();
            let _ = sender.send(load_result);
            if let Some(((_, ops_stats), elapsed)) = timing.zip(elapsed) {
                id_list_load_timing::record_duration(
                    &ops_stats,
                    "lazy_id_list_load.batch_ms",
                    elapsed,
                    if succeeded { "success" } else { "error" },
                );
            }
        }) {
            log_error_to_statsig_and_console!(ops_stats, TAG, error);
            return LazyIdListLoadStatus::Failed;
        }

        let wait_started = Instant::now();
        let result = receiver.recv_timeout(*remaining_wait);
        let elapsed = wait_started.elapsed();
        *remaining_wait = remaining_wait.saturating_sub(elapsed);
        if record_wait {
            *waited += elapsed;
        }

        match result {
            Ok(Ok(())) => LazyIdListLoadStatus::Ready,
            Ok(Err(error)) => {
                log_error_to_statsig_and_console!(ops_stats, TAG, error);
                LazyIdListLoadStatus::Failed
            }
            Err(mpsc::RecvTimeoutError::Timeout) => LazyIdListLoadStatus::Timeout,
            Err(mpsc::RecvTimeoutError::Disconnected) => LazyIdListLoadStatus::Failed,
        }
    }
}

const LAZY_ID_LIST_LOAD_TAG: &str = "LAZY_ID_LIST_LOAD";
const LAZY_ID_LIST_LOAD_TIMEOUT: Duration = Duration::from_millis(30);

#[derive(Clone, Copy)]
pub(super) enum LazyIdListLoadStatus {
    Ready,
    Timeout,
    Failed,
}

impl LazyIdListLoadStatus {
    pub(super) fn has_unresolved_lists(self) -> bool {
        !matches!(self, Self::Ready)
    }

    fn metric_outcome(self) -> &'static str {
        match self {
            Self::Ready => "success",
            Self::Timeout => "timeout",
            Self::Failed => "failure",
        }
    }

    fn partial_evaluation_reason(self) -> Option<&'static str> {
        match self {
            Self::Ready => None,
            Self::Timeout => Some("IdListLoadTimeout"),
            Self::Failed => Some("IdListLoadFailure"),
        }
    }
}

pub(super) struct LazyIdListLoadOutcome {
    pub(super) status: LazyIdListLoadStatus,
    /// The exact store snapshot whose dependencies were checked. Evaluation
    /// must use this snapshot rather than loading the store again.
    pub(super) data: Arc<SpecStoreData>,
}

fn lazy_id_list_spec_type_name(spec_type: &SpecType) -> &'static str {
    match spec_type {
        SpecType::Gate => "gate",
        SpecType::DynamicConfig => "dynamic_config",
        SpecType::Experiment => "experiment",
        SpecType::Layer => "layer",
        SpecType::ParameterStore => "parameter_store",
    }
}

pub(super) fn mark_partial_id_list_evaluation(
    details: &mut EvaluationDetails,
    status: LazyIdListLoadStatus,
) {
    if let Some(reason) = status
        .partial_evaluation_reason()
        .filter(|_| !details.is_blob_unavailable())
    {
        details.reason = format!("{}:PartialEvaluation:{reason}", details.reason);
    }
}

impl Statsig {
    /// Makes every ID list referenced by an evaluation's current dependency
    /// graph available before synchronous evaluation. The returned snapshot is
    /// the exact one that was validated and must also be used for evaluation.
    pub(super) fn ensure_spec_id_lists(
        &self,
        spec_name: &str,
        spec_type: &SpecType,
    ) -> LazyIdListLoadOutcome {
        let mut data = self.spec_store.load_data();
        if self.options.lazy_load_id_lists != Some(true) {
            return LazyIdListLoadOutcome {
                status: LazyIdListLoadStatus::Ready,
                data,
            };
        }

        // The 30 ms budget applies only to waiting for asynchronous body loads.
        // Dependency walking and snapshot validation do not consume it.
        let mut remaining_wait = LAZY_ID_LIST_LOAD_TIMEOUT;
        let mut waited = Duration::ZERO;
        let status = loop {
            let required = data.id_list_dependencies(spec_name, spec_type);
            let missing = required
                .iter()
                .filter(|name| !data.id_lists.contains_key(name.as_str()))
                .cloned()
                .collect::<Vec<_>>();
            if missing.is_empty() {
                break LazyIdListLoadStatus::Ready;
            }

            let status = self.id_lists_adapter.load_missing(
                missing,
                &self.statsig_runtime,
                &self.ops_stats,
                &mut remaining_wait,
                &mut waited,
            );
            if status.has_unresolved_lists() {
                break status;
            }
            let current = self.spec_store.load_data();
            if !Arc::ptr_eq(&data.snapshot, &current.snapshot) {
                // The spec graph changed while loading. Recompute from
                // the new snapshot and use only the remaining wait budget.
                data = current;
                if remaining_wait.is_zero() {
                    break LazyIdListLoadStatus::Timeout;
                }
                continue;
            }
            data = current;
            break if required
                .iter()
                .all(|name| data.id_lists.contains_key(name.as_str()))
            {
                LazyIdListLoadStatus::Ready
            } else {
                LazyIdListLoadStatus::Failed
            };
        };
        if !matches!(status, LazyIdListLoadStatus::Ready) {
            self.ops_stats.log(ObservabilityEvent::new_event(
                MetricType::Increment,
                "lazy_id_list_load.count".to_string(),
                1.0,
                Some(HashMap::from([
                    ("outcome".to_string(), status.metric_outcome().to_string()),
                    (
                        "spec_type".to_string(),
                        lazy_id_list_spec_type_name(spec_type).to_string(),
                    ),
                ])),
            ));
        }
        if !waited.is_zero() {
            id_list_load_timing::record_duration(
                &self.ops_stats,
                "lazy_id_list_load.wait_ms",
                waited,
                match status {
                    LazyIdListLoadStatus::Ready => "success",
                    LazyIdListLoadStatus::Timeout => "timeout",
                    LazyIdListLoadStatus::Failed => "error",
                },
            );
        }
        LazyIdListLoadOutcome { status, data }
    }
}
