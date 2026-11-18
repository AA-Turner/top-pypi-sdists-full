use std::{cell::Cell, future::Future};

use super::HydrationFailureReason;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::spec_store::{SpecStore, SpecStoreData};
use crate::{InitializeDetails, StatsigErr};

#[derive(Clone, Copy)]
enum SpecsOutcome {
    Pending,
    BlobRejected,
    Accepted,
    ReadinessSample(bool),
}

impl SpecsOutcome {
    fn blocked_by_blob(self, data: &SpecStoreData) -> bool {
        match self {
            Self::Pending => false,
            Self::BlobRejected => data.evaluation_lcut() == 0,
            Self::Accepted => data.has_unavailable_blob_values(),
            Self::ReadinessSample(blocked) => blocked,
        }
    }
}

tokio::task_local! {
    static OUTCOME: Cell<SpecsOutcome>;
}

pub(crate) fn begin_source() {
    let _ = OUTCOME.try_with(|outcome| outcome.set(SpecsOutcome::Pending));
}

// Preserve the cause before an adapter wraps the hydration error.
pub(crate) fn record_error(error: &StatsigErr) {
    let _ = OUTCOME.try_with(|outcome| {
        if HydrationFailureReason::recoverable(error).is_some() {
            outcome.set(SpecsOutcome::BlobRejected);
        }
    });
}

pub(crate) fn record_start_result(result: &Result<(), StatsigErr>) {
    match result {
        Ok(()) => {
            let _ = OUTCOME.try_with(|outcome| outcome.set(SpecsOutcome::Accepted));
        }
        Err(error) => record_error(error),
    }
}

pub(crate) fn record_readiness(data: &SpecStoreData) {
    let _ = OUTCOME.try_with(|outcome| {
        outcome.set(SpecsOutcome::ReadinessSample(
            outcome.get().blocked_by_blob(data),
        ))
    });
}

pub(crate) async fn report_if_unready(
    store: &SpecStore,
    ops_stats: &OpsStatsForInstance,
    initialize: impl Future<Output = Result<InitializeDetails, StatsigErr>>,
) -> Result<InitializeDetails, StatsigErr> {
    if !matches!(
        std::env::var("STATSIG_REPORT_BLOB_INIT_FAILURE").as_deref(),
        Ok("1" | "true")
    ) {
        return initialize.await;
    }
    OUTCOME
        .scope(Cell::new(SpecsOutcome::Pending), async {
            let result = initialize.await;
            if result
                .as_ref()
                .is_ok_and(|details| !details.is_config_spec_ready)
                && OUTCOME.with(|outcome| match outcome.get() {
                    SpecsOutcome::ReadinessSample(blocked) => blocked,
                    outcome => outcome.blocked_by_blob(&store.load_data()),
                })
            {
                ops_stats.log(ObservabilityEvent::new_event(
                    MetricType::Increment,
                    "initialization.config_spec_not_ready_due_to_blob".to_owned(),
                    1.0,
                    None,
                ));
            }
            result
        })
        .await
}
