use std::collections::HashMap;
use std::time::{Duration, Instant};

use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::{StatsigErr, log_d};

use super::errors::{HydrationFailureReason, HydrationTimeoutStep, hydration_error};
use super::{HYDRATION_TIMEOUT, RemoteConfigValueHydrator, TAG};

const HYDRATION_COUNT_METRIC: &str = "remote_config_hydration.count";
const HYDRATION_LATENCY_METRIC: &str = "remote_config_hydration.latency";
const HYDRATION_BYTES_METRIC: &str = "remote_config_hydration.bytes";
const HYDRATION_RESULT_METRIC: &str = "remote_config_hydration.result";

#[derive(Clone, Copy)]
pub(crate) enum HydrationPhase {
    JsonParse,
    JsonApply,
    ProtobufParse,
    ProtobufApply,
    ProtobufResponse,
    ResponsePermit,
    ResponseExpansionPermit,
    DownloadSlotPermit,
    DownloadBytesPermit,
    DownloadWait,
    Verify,
}
impl HydrationPhase {
    fn as_str(self) -> &'static str {
        match self {
            Self::JsonParse => "json_parse",
            Self::JsonApply => "json_apply",
            Self::ProtobufParse => "protobuf_parse",
            Self::ProtobufApply => "protobuf_apply",
            Self::ProtobufResponse => "protobuf_response",
            Self::ResponsePermit => "response_permit",
            Self::ResponseExpansionPermit => "response_expansion_permit",
            Self::DownloadSlotPermit => "download_slot_permit",
            Self::DownloadBytesPermit => "download_bytes_permit",
            Self::DownloadWait => "download_wait",
            Self::Verify => "verify",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum HydrationOutcome {
    Success,
    Failure,
}

impl HydrationOutcome {
    const fn as_str(self) -> &'static str {
        match self {
            Self::Success => "success",
            Self::Failure => "failure",
        }
    }
}

/// One terminal result for a response containing actual remote metadata. The
/// legacy count also includes probe failures, so it cannot be this denominator.
pub(super) struct HydrationResult<'a> {
    hydrator: &'a RemoteConfigValueHydrator,
    saw_remote_metadata: bool,
    finished: bool,
    download_failure: Option<HydrationFailureReason>,
}

impl<'a> HydrationResult<'a> {
    pub(super) fn new(hydrator: &'a RemoteConfigValueHydrator) -> Self {
        Self {
            hydrator,
            saw_remote_metadata: false,
            finished: false,
            download_failure: None,
        }
    }

    pub(super) fn mark_remote_metadata(&mut self) {
        self.saw_remote_metadata = true;
    }

    pub(super) fn record_download_error(&mut self, error: &StatsigErr) {
        self.download_failure = Some(
            HydrationFailureReason::from_error(error)
                .unwrap_or(HydrationFailureReason::BodyReadFailed),
        );
    }

    pub(super) fn finish(&mut self, result: Result<(), &StatsigErr>) {
        if self.finished {
            return;
        }
        self.finished = true;
        let (outcome, reason) = match result {
            Ok(()) => ("success", "none"),
            Err(error) => match self
                .download_failure
                .or_else(|| HydrationFailureReason::from_error(error))
            {
                Some(reason) => ("failure", reason.as_str()),
                None if matches!(error, StatsigErr::ProtobufParseError(tag, _) if tag == "proto::RemoteConfigMetadata") => {
                    ("failure", "invalid_metadata_marker")
                }
                // Integrated protobuf parsing can fail after hydration for an
                // unrelated reason. Keep it visible without calling it a blob failure.
                None => ("aborted", "response_processing_failed"),
            },
        };
        self.log(outcome, reason);
    }

    fn log(&self, outcome: &str, failure_reason: &str) {
        if !self.saw_remote_metadata {
            return;
        }
        self.hydrator.log_metric(
            MetricType::Increment,
            HYDRATION_RESULT_METRIC,
            1.0,
            Some(HashMap::from([
                ("outcome".to_string(), outcome.to_string()),
                ("failure_reason".to_string(), failure_reason.to_string()),
            ])),
        );
    }
}

impl Drop for HydrationResult<'_> {
    fn drop(&mut self) {
        if !self.finished {
            self.log("aborted", "cancelled");
        }
    }
}

impl RemoteConfigValueHydrator {
    pub(crate) fn log_phase_latency(&self, elapsed: Duration, phase: HydrationPhase) {
        self.log_metric(
            MetricType::Dist,
            "remote_config_hydration.phase_latency",
            elapsed.as_secs_f64() * 1000.0,
            Some(HashMap::from([("phase".into(), phase.as_str().into())])),
        );
    }

    pub(super) fn total_timeout_error(
        &self,
        started_at: Instant,
        step: HydrationTimeoutStep,
    ) -> StatsigErr {
        self.log_metric(
            MetricType::Dist,
            "remote_config_hydration.timeout",
            started_at.elapsed().as_secs_f64() * 1000.0,
            Some(HashMap::from([("step".into(), step.as_str().into())])),
        );
        hydration_error(
            HydrationFailureReason::TotalTimeout,
            &format!(
                "hydration exceeded {} seconds at {}",
                HYDRATION_TIMEOUT.as_secs_f64(),
                step.as_str()
            ),
        )
    }

    pub(super) fn log_hydration_success(&self, reference_count: usize, total_bytes: u64) {
        self.log_metric(
            MetricType::Dist,
            HYDRATION_BYTES_METRIC,
            total_bytes as f64,
            None,
        );
        log_d!(
            TAG,
            "Hydrated {} remote dynamic config values ({} bytes)",
            reference_count,
            total_bytes
        );
    }

    pub(super) fn log_hydration_outcome(&self, started_at: Instant, outcome: HydrationOutcome) {
        let tags = || {
            Some(HashMap::from([(
                "outcome".to_string(),
                outcome.as_str().to_string(),
            )]))
        };
        self.log_metric(MetricType::Increment, HYDRATION_COUNT_METRIC, 1.0, tags());
        self.log_metric(
            MetricType::Dist,
            HYDRATION_LATENCY_METRIC,
            started_at.elapsed().as_secs_f64() * 1000.0,
            tags(),
        );
    }

    fn log_metric(
        &self,
        metric_type: MetricType,
        name: &str,
        value: f64,
        tags: Option<HashMap<String, String>>,
    ) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            metric_type,
            name.to_string(),
            value,
            tags,
        ));
    }
}
