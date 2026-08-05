use crate::console_capture::console_log_line_levels::StatsigLogLineLevel;
use crate::evaluation::secondary_exposure_key::SecondaryExposureKey;
use crate::event_logging::statsig_event::StatsigEvent;
use crate::event_logging::statsig_event::string_metadata_to_value_metadata;
use crate::sdk_diagnostics::diagnostics::DIAGNOSTICS_EVENT;
use crate::user::StatsigUserLoggable;
use crate::{evaluation::evaluation_types::SecondaryExposure, statsig_metadata::StatsigMetadata};

use ahash::AHashSet;
use chrono::Utc;
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::collections::HashMap;

pub const GATE_EXPOSURE_EVENT_NAME: &str = "statsig::gate_exposure";
pub const CONFIG_EXPOSURE_EVENT_NAME: &str = "statsig::config_exposure";
pub const LAYER_EXPOSURE_EVENT_NAME: &str = "statsig::layer_exposure";
pub const STATSIG_LOG_LINE_EVENT_NAME: &str = "statsig::log_line";

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct StatsigEventInternal {
    #[serde(flatten)]
    pub event_data: StatsigEvent,

    pub user: StatsigUserLoggable,
    pub time: u64,
    pub secondary_exposures: Option<Vec<SecondaryExposure>>,
}

impl StatsigEventInternal {
    pub fn new(
        time: u64,
        user: StatsigUserLoggable,
        event: StatsigEvent,
        secondary_exposures: Option<Vec<SecondaryExposure>>,
    ) -> Self {
        StatsigEventInternal {
            event_data: event,
            user,
            time,
            secondary_exposures: secondary_exposures.map(dedupe_secondary_exposures),
        }
    }

    pub fn new_custom_event(
        user: StatsigUserLoggable,
        event_name: String,
        value: Option<Value>,
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        let metadata = metadata.map(string_metadata_to_value_metadata);
        StatsigEventInternal::new(
            Utc::now().timestamp_millis() as u64,
            user,
            StatsigEvent {
                event_name,
                value,
                metadata,
                statsig_metadata: None,
            },
            None,
        )
    }

    pub fn new_custom_event_with_typed_metadata(
        user: StatsigUserLoggable,
        event_name: String,
        value: Option<Value>,
        metadata: Option<HashMap<String, Value>>,
    ) -> Self {
        StatsigEventInternal::new_custom_event_with_typed_metadata_and_timestamp(
            user, event_name, value, metadata, None,
        )
    }

    pub(crate) fn new_custom_event_with_typed_metadata_and_timestamp(
        user: StatsigUserLoggable,
        event_name: String,
        value: Option<Value>,
        metadata: Option<HashMap<String, Value>>,
        timestamp_override: Option<u64>,
    ) -> Self {
        StatsigEventInternal::new(
            timestamp_override.unwrap_or(Utc::now().timestamp_millis() as u64),
            user,
            StatsigEvent {
                event_name,
                value,
                metadata,
                statsig_metadata: None,
            },
            None,
        )
    }

    pub fn new_diagnostic_event(metadata: HashMap<String, String>) -> Self {
        StatsigEventInternal {
            event_data: StatsigEvent {
                event_name: DIAGNOSTICS_EVENT.to_string(),
                value: None,
                metadata: Some(string_metadata_to_value_metadata(metadata)),
                statsig_metadata: None,
            },
            user: StatsigUserLoggable::null(),
            time: Utc::now().timestamp_millis() as u64,
            secondary_exposures: None,
        }
    }

    pub fn new_non_exposed_checks_event(checks: HashMap<String, u64>) -> Self {
        let checks_json = match serde_json::to_string(&checks) {
            Ok(json) => json,
            Err(_) => "STATSIG_ERROR_SERIALIZING_NON_EXPOSED_CHECKS".into(),
        };

        let event = StatsigEvent {
            event_name: "statsig::non_exposed_checks".to_string(),
            value: None,
            metadata: Some(string_metadata_to_value_metadata(HashMap::from([(
                "checks".into(),
                checks_json,
            )]))),
            statsig_metadata: None,
        };

        StatsigEventInternal {
            event_data: event,
            user: StatsigUserLoggable::null(),
            time: Utc::now().timestamp_millis() as u64,
            secondary_exposures: None,
        }
    }

    pub fn new_statsig_log_line_event(
        user: StatsigUserLoggable,
        log_level: StatsigLogLineLevel,
        value: Option<String>,
        metadata: Option<HashMap<String, String>>,
        timestamp_override: Option<u64>,
    ) -> Self {
        let mut populated_metadata = metadata.unwrap_or_default();
        populated_metadata.insert("status".to_string(), log_level.to_status_string());
        populated_metadata.insert(
            "source".to_string(),
            StatsigMetadata::get_metadata().sdk_type.to_string(),
        );
        populated_metadata.insert("log_level".to_string(), format!("{:?}", log_level));

        StatsigEventInternal {
            event_data: StatsigEvent {
                event_name: STATSIG_LOG_LINE_EVENT_NAME.to_string(),
                value: value.map(|v| json!(v)),
                metadata: Some(string_metadata_to_value_metadata(populated_metadata)),
                statsig_metadata: None,
            },
            user,
            time: timestamp_override.unwrap_or(Utc::now().timestamp_millis() as u64),
            secondary_exposures: None,
        }
    }

    pub fn is_exposure_event(&self) -> bool {
        self.event_data.event_name == GATE_EXPOSURE_EVENT_NAME
            || self.event_data.event_name == CONFIG_EXPOSURE_EVENT_NAME
            || self.event_data.event_name == LAYER_EXPOSURE_EVENT_NAME
    }

    pub fn is_diagnostic_event(&self) -> bool {
        self.event_data.event_name == DIAGNOSTICS_EVENT
    }
}

/// Consumes an event-local exposure vector and retains the first occurrence of
/// each `(gate, rule ID, gate value)` tuple, preserving the original order.
fn dedupe_secondary_exposures(
    mut secondary_exposures: Vec<SecondaryExposure>,
) -> Vec<SecondaryExposure> {
    let mut seen = AHashSet::with_capacity(secondary_exposures.len());
    secondary_exposures.retain(|exposure| seen.insert(SecondaryExposureKey::from(exposure)));
    secondary_exposures
}

#[cfg(test)]
mod statsig_event_internal_tests {
    use crate::StatsigUser;
    use crate::evaluation::evaluation_types::SecondaryExposure;
    use crate::event_logging::statsig_event::StatsigEvent;
    use crate::event_logging::statsig_event_internal::{
        StatsigEventInternal, dedupe_secondary_exposures,
    };
    use crate::interned_string::InternedString;
    use crate::user::StatsigUserInternal;
    use chrono::Utc;
    use serde_json::{Value, json};
    use std::collections::HashMap;

    fn create_test_event() -> StatsigEventInternal {
        let user_data = StatsigUser::with_user_id("a-user");
        let user = StatsigUserInternal::new(&user_data, None);
        let mut sampling_statsig_metadata: HashMap<String, Value> = HashMap::new();
        sampling_statsig_metadata.insert("samplingMode".into(), "on".into());
        sampling_statsig_metadata.insert("samplingRate".into(), 101.into());
        sampling_statsig_metadata.insert("shadowLogged".into(), "logged".into());

        StatsigEventInternal::new(
            Utc::now().timestamp_millis() as u64,
            user.to_loggable(),
            StatsigEvent {
                event_name: "foo".into(),
                value: Some(json!("bar")),
                metadata: Some(HashMap::from([(
                    "key".into(),
                    Value::String("value".into()),
                )])),
                statsig_metadata: Some(sampling_statsig_metadata),
            },
            None,
        )
    }

    fn secondary_exposure(gate: &str, rule_id: &str, gate_value: &str) -> SecondaryExposure {
        SecondaryExposure {
            gate: InternedString::from_str_ref(gate),
            rule_id: InternedString::from_str_ref(rule_id),
            gate_value: InternedString::from_str_ref(gate_value),
        }
    }

    #[test]
    fn test_custom_event_fields() {
        let event = create_test_event();
        let data = event.event_data;

        assert_eq!(data.event_name, "foo");
        assert_eq!(data.value.unwrap().as_str(), Some("bar"));
        assert_eq!(
            data.metadata.unwrap().get("key").unwrap().as_str(),
            Some("value")
        );
    }

    #[test]
    fn test_custom_event_serialization() {
        let event = create_test_event();

        let value = json!(event).as_object().cloned().unwrap();
        assert_eq!(value.get("eventName").unwrap(), "foo");
        assert_eq!(value.get("value").unwrap(), "bar");
        assert_eq!(
            value.get("metadata").unwrap().to_string(),
            "{\"key\":\"value\"}"
        );
    }

    #[test]
    fn test_secondary_exposure_duplicates_are_removed() {
        let duplicate = secondary_exposure("gate-a", "rule-a", "true");
        let exposures = dedupe_secondary_exposures(vec![duplicate.clone(), duplicate]);

        assert_eq!(exposures.len(), 1);
        assert_eq!(exposures[0].gate.as_str(), "gate-a");
        assert_eq!(exposures[0].rule_id.as_str(), "rule-a");
        assert_eq!(exposures[0].gate_value.as_str(), "true");
    }

    #[test]
    fn test_secondary_exposure_unique_order_is_preserved() {
        let exposures = dedupe_secondary_exposures(vec![
            secondary_exposure("gate-b", "rule-b", "false"),
            secondary_exposure("gate-a", "rule-a", "true"),
            secondary_exposure("gate-b", "rule-b", "false"),
            secondary_exposure("gate-b", "rule-c", "false"),
            secondary_exposure("gate-b", "rule-b", "true"),
            secondary_exposure("gate-a", "rule-a", "true"),
        ]);

        let exposure_values: Vec<(&str, &str, &str)> = exposures
            .iter()
            .map(|exposure| {
                (
                    exposure.gate.as_str(),
                    exposure.rule_id.as_str(),
                    exposure.gate_value.as_str(),
                )
            })
            .collect();
        assert_eq!(
            exposure_values,
            vec![
                ("gate-b", "rule-b", "false"),
                ("gate-a", "rule-a", "true"),
                ("gate-b", "rule-c", "false"),
                ("gate-b", "rule-b", "true"),
            ]
        );
    }
}
