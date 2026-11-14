use std::{
    collections::{HashMap, HashSet},
    sync::Arc,
};

use ahash::HashMap as AHashMap;
use serde::{Deserialize, Deserializer, Serialize, Serializer};
use serde_json::value::RawValue;
use serde_with::skip_serializing_none;

use crate::evaluation::cron_window::CronWindow;
use crate::evaluation::dynamic_string::DynamicString;
use crate::evaluation::{
    dynamic_returnable::DynamicReturnable,
    evaluator_value::{EvaluatorArrayKeyMode, EvaluatorValue},
};
use crate::gcir::gcir_formatter::GCIRHashable;
use crate::hashing::opt_bool_to_hashable;
use crate::interned_string::InternedString;
use crate::specs_response::explicit_params::ExplicitParameters;
use crate::specs_response::parse_options::{SpecsResponseParseOptions, with_parse_options};
use crate::specs_response::specs_hash_map::{
    SpecsHashMap, deserialize_dynamic_configs, deserialize_inline_only_map,
    raw_rules_have_remote_metadata,
};
use crate::{DynamicValue, hashing};

use super::{cmab_types::CMABConfig, param_store_types::ParameterStore};

// Only populated on partial snapshots. None identifies the default, Some(i) the wire rule index.
pub(crate) type UnavailableValues = HashMap<InternedString, HashSet<Option<usize>>>;

// DO_NOT_CLONE: Please do not add the Clone trait to this struct. We intentionally
// avoid cloning this data at all costs as it can be quite large.

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
#[serde(rename_all = "camelCase")]
pub struct Spec {
    pub checksum: Option<InternedString>,
    #[serde(rename = "type")]
    pub _type: InternedString,
    pub salt: InternedString,
    pub default_value: DynamicReturnable,
    pub enabled: bool,
    pub rules: Vec<Rule>,
    pub id_type: InternedString,
    pub explicit_parameters: Option<ExplicitParameters>,
    pub entity: InternedString,
    pub has_shared_params: Option<bool>,
    pub is_active: Option<bool>,
    pub version: Option<u32>,
    #[serde(rename = "targetAppIDs")]
    pub target_app_ids: Option<Vec<InternedString>>,
    pub forward_all_exposures: Option<bool>,
    pub fields_used: Option<Vec<InternedString>>,
    pub use_new_layer_eval: Option<bool>,
    pub session_update_mode: Option<InternedString>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
#[serde(rename_all = "camelCase")]
pub struct Rule {
    pub name: InternedString,
    pub pass_percentage: f64,
    pub return_value: DynamicReturnable,
    pub id: InternedString,
    pub salt: Option<InternedString>,
    pub conditions: Vec<InternedString>,
    pub id_type: DynamicString,
    pub group_name: Option<InternedString>,
    pub config_delegate: Option<InternedString>,
    pub is_experiment_group: Option<bool>,
    pub sampling_rate: Option<u64>,
    pub shared_control_experiments: Option<SharedControlExperiments>,
}

#[derive(Clone, Debug, PartialEq)]
pub struct SharedControlExperiments {
    experiments: Arc<Vec<SharedControlExperiment>>,
}

impl From<Vec<SharedControlExperiment>> for SharedControlExperiments {
    fn from(experiments: Vec<SharedControlExperiment>) -> Self {
        Self {
            experiments: Arc::new(experiments),
        }
    }
}

impl std::ops::Deref for SharedControlExperiments {
    type Target = [SharedControlExperiment];

    fn deref(&self) -> &Self::Target {
        self.experiments.as_slice()
    }
}

impl<'de> Deserialize<'de> for SharedControlExperiments {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        Vec::<SharedControlExperiment>::deserialize(deserializer).map(Self::from)
    }
}

impl Serialize for SharedControlExperiments {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.experiments.as_slice().serialize(serializer)
    }
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug, Clone)]
#[serde(rename_all = "camelCase")]
pub struct SharedControlExperiment {
    pub name: InternedString,
    #[serde(rename = "controlGroupID")]
    pub control_group_id: InternedString,
}

#[repr(u8)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum ConditionType {
    Public,
    FailGate,
    PassGate,
    ExperimentGroup,
    UaBased,
    IpBased,
    UserField,
    EnvironmentField,
    CurrentTime,
    UserBucket,
    TargetApp,
    UnitId,
    Unknown,
}

impl ConditionType {
    pub(crate) fn from_str(value: &str) -> Self {
        match value {
            "public" => Self::Public,
            "fail_gate" => Self::FailGate,
            "pass_gate" => Self::PassGate,
            "experiment_group" => Self::ExperimentGroup,
            "ua_based" => Self::UaBased,
            "ip_based" => Self::IpBased,
            "user_field" => Self::UserField,
            "environment_field" => Self::EnvironmentField,
            "current_time" => Self::CurrentTime,
            "user_bucket" => Self::UserBucket,
            "target_app" => Self::TargetApp,
            "unit_id" => Self::UnitId,
            _ => Self::Unknown,
        }
    }
}

#[repr(u8)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum ConditionOperator {
    Missing,
    Gt,
    Gte,
    Lt,
    Lte,
    VersionGt,
    VersionGte,
    VersionLt,
    VersionLte,
    VersionEq,
    VersionNeq,
    Any,
    NoneOf,
    StrStartsWithAny,
    StrEndsWithAny,
    StrContainsAny,
    StrContainsNone,
    AnyCaseSensitive,
    NoneCaseSensitive,
    StrMatches,
    Before,
    After,
    On,
    Eq,
    Neq,
    InSegmentList,
    NotInSegmentList,
    ArrayContainsAny,
    ArrayContainsNone,
    ArrayContainsAll,
    NotArrayContainsAll,
    InCronWindow,
    Unknown,
}

impl ConditionOperator {
    pub(crate) fn evaluator_array_key_mode(self) -> EvaluatorArrayKeyMode {
        match self {
            Self::AnyCaseSensitive | Self::NoneCaseSensitive => EvaluatorArrayKeyMode::ExactCase,
            _ => EvaluatorArrayKeyMode::Normalized,
        }
    }

    pub(crate) fn from_str(value: Option<&str>) -> Self {
        match value {
            None => Self::Missing,
            Some("gt") => Self::Gt,
            Some("gte") => Self::Gte,
            Some("lt") => Self::Lt,
            Some("lte") => Self::Lte,
            Some("version_gt") => Self::VersionGt,
            Some("version_gte") => Self::VersionGte,
            Some("version_lt") => Self::VersionLt,
            Some("version_lte") => Self::VersionLte,
            Some("version_eq") => Self::VersionEq,
            Some("version_neq") => Self::VersionNeq,
            Some("any") => Self::Any,
            Some("none") => Self::NoneOf,
            Some("str_starts_with_any") => Self::StrStartsWithAny,
            Some("str_ends_with_any") => Self::StrEndsWithAny,
            Some("str_contains_any") => Self::StrContainsAny,
            Some("str_contains_none") => Self::StrContainsNone,
            Some("any_case_sensitive") => Self::AnyCaseSensitive,
            Some("none_case_sensitive") => Self::NoneCaseSensitive,
            Some("str_matches") => Self::StrMatches,
            Some("before") => Self::Before,
            Some("after") => Self::After,
            Some("on") => Self::On,
            Some("eq") => Self::Eq,
            Some("neq") => Self::Neq,
            Some("in_segment_list") => Self::InSegmentList,
            Some("not_in_segment_list") => Self::NotInSegmentList,
            Some("array_contains_any") => Self::ArrayContainsAny,
            Some("array_contains_none") => Self::ArrayContainsNone,
            Some("array_contains_all") => Self::ArrayContainsAll,
            Some("not_array_contains_all") => Self::NotArrayContainsAll,
            Some("in_cron_window") => Self::InCronWindow,
            Some(_) => Self::Unknown,
        }
    }
}

#[derive(Serialize, PartialEq, Debug, Clone /* TEMP: Make this an Arc */)] /* DO_NOT_CLONE */
#[serde(rename_all = "camelCase")]
pub struct Condition {
    #[serde(rename = "type")]
    pub condition_type: InternedString,
    #[serde(skip)]
    pub(crate) compiled_condition_type: ConditionType,
    pub target_value: Option<EvaluatorValue>,
    pub operator: Option<InternedString>,
    #[serde(skip)]
    pub(crate) compiled_operator: ConditionOperator,
    #[serde(skip)]
    pub(crate) compiled_cron_window: Option<Arc<CronWindow>>,
    pub field: Option<DynamicString>,
    pub additional_values: Option<HashMap<InternedString, InternedString>>,
    pub id_type: DynamicString,
    pub checksum: Option<InternedString>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct OverrideRule {
    pub rule_name: String,
    pub start_time: Option<i64>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct ConfigMapping {
    pub new_config_name: InternedString,
    pub rules: Vec<OverrideRule>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct SessionReplayTrigger {
    pub sampling_rate: Option<f64>,
    pub values: Option<Vec<InternedString>>,
    pub passes_sampling: Option<bool>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug, Clone)] /* DO_NOT_CLONE */
pub struct SessionReplayPrivacySetting {
    pub privacy_mode: InternedString,
    pub unmasked_elements: Option<Vec<InternedString>>,
    pub masked_elements: Option<Vec<InternedString>>,
    pub blocked_elements: Option<Vec<InternedString>>,
}

impl GCIRHashable for SessionReplayTrigger {
    fn create_hash(&self, name: &InternedString) -> u64 {
        let mut hash_array = Vec::new();
        hash_array.push(name.hash);
        hash_array.push(opt_bool_to_hashable(&self.passes_sampling));
        if let Some(values) = &self.values {
            for value in values {
                hash_array.push(value.hash);
            }
        }
        hashing::hash_one(hash_array)
    }
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct SessionReplayInfo {
    pub sampling_rate: Option<f64>,
    pub targeting_gate: Option<String>,
    pub recording_blocked: Option<bool>,
    pub session_recording_event_triggers: Option<HashMap<InternedString, SessionReplayTrigger>>,
    pub session_recording_exposure_triggers: Option<HashMap<InternedString, SessionReplayTrigger>>,
    pub session_recording_privacy_settings: Option<SessionReplayPrivacySetting>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct AutoCaptureSettings {
    pub disabled_events: HashMap<InternedString, bool>,
}

#[skip_serializing_none]
#[derive(Serialize, Deserialize, PartialEq, Debug)] /* DO_NOT_CLONE */
pub struct GCIRConfig {
    pub remove_default_value_gates: bool,
}

// All this macro logic is to ensure that new fields that are added are automatically handled by the merge_from_partial method.
macro_rules! flatten_struct {
    (
        $name:ident,
        { $( $(#[$common_attr:meta])* $common_vis:vis $common_field:ident : $common_ty:ty ),* $(,)? },
        { $( $(#[$special_attr:meta])* $special_vis:vis $special_field:ident : $special_ty:ty ),* $(,)? }
    ) => {

        #[skip_serializing_none]
        #[derive(Serialize, Deserialize, PartialEq, Debug, Default)] /* DO_NOT_CLONE */
        pub struct $name {
            $( $(#[$common_attr])* $common_vis $common_field: $common_ty, )*
            $( $(#[$special_attr])* $special_vis $special_field : $special_ty, )*
        }

        impl $name {
            pub fn merge_from_partial(&mut self, partial: SpecsResponsePartial) {
                $( self.$common_field = partial.$common_field; )*
            }

            #[allow(dead_code)]
            pub(super) fn copy_common_fields_from(&mut self, other: &Self) -> serde_json::Result<()> {
                #[derive(Serialize)]
                struct CommonFields<'a> { $( $common_field: &'a $common_ty, )* }
                let fields = CommonFields { $( $common_field: &other.$common_field, )* };
                self.merge_from_partial(serde_json::from_slice(&serde_json::to_vec(&fields)?)?);
                Ok(())
            }

            #[allow(dead_code)]
            pub(crate) fn common_fields_match(&self, other: &SpecsResponseFull) -> bool {
                true $( && self.$common_field == other.$common_field )*
            }
        }
    };
}

macro_rules! response_struct {
    ( $name:ident, { $( $special:tt )* } ) => {
        flatten_struct!(
            $name,
            {
                pub app_id: Option<DynamicValue>,
                pub cmab_configs: Option<HashMap<String, CMABConfig>>,
                pub default_environment: Option<String>,
                pub diagnostics: Option<HashMap<String, f64>>,
                pub experiment_to_layer: HashMap<String, String>,
                pub hashed_sdk_keys_to_app_ids: Option<HashMap<String, DynamicValue>>,
                pub id_lists: Option<HashMap<String, bool>>,
                #[serde(default, deserialize_with = "deserialize_inline_only_map")]
                pub override_rules: Option<HashMap<String, Rule>>,
                pub overrides: Option<HashMap<String, Vec<ConfigMapping>>>,
                pub sdk_configs: Option<HashMap<String, DynamicValue>>,
                pub sdk_flags: Option<HashMap<String, bool>>,
                pub sdk_keys_to_app_ids: Option<HashMap<String, DynamicValue>>,
                pub session_replay_info: Option<SessionReplayInfo>,
                pub auto_capture_settings: Option<AutoCaptureSettings>,
                pub gcir_config: Option<GCIRConfig>,
                // Add new fields here
            },
            { $( $special )* }
        );
    };
}

response_struct!(SpecsResponseFull, {
    // Special Case Proto Fields
    pub checksum: Option<String>,
    pub company_id: Option<String>,
    #[serde(deserialize_with = "deserialize_condition_map")]
    pub condition_map: AHashMap<InternedString, Condition>,
    #[serde(deserialize_with = "deserialize_dynamic_configs")]
    pub dynamic_configs: SpecsHashMap,
    pub feature_gates: SpecsHashMap,
    pub has_updates: bool,
    pub layer_configs: SpecsHashMap,
    #[serde(default, deserialize_with = "deserialize_inline_only_map")]
    pub param_stores: Option<HashMap<InternedString, ParameterStore>>,
    pub response_format: Option<String>,
    pub time: u64,
    // DO NOT add new fields here unless you know how the Protobuf parser handles them.
});

// Think of SpecsResponsePartial as the Typescript type Omit<SpecsResponseFull, "checksum" | "company_id" | etc...>
// This is used by the protobuf parser to populate the top level fields of SpecsResponseFull.
response_struct!(SpecsResponsePartial, {
    // No Special Fields
});

impl SpecsResponseFull {
    pub fn deserialize_json_with_options(
        data: &[u8],
        options: SpecsResponseParseOptions,
    ) -> Result<Self, serde_json::Error> {
        with_parse_options(options, || serde_json::from_slice(data))
    }

    pub fn reset(&mut self) {
        *self = SpecsResponseFull::default();
    }

    pub fn is_empty(&self) -> bool {
        self.checksum.is_none()
            && self.feature_gates.len() == 0
            && self.dynamic_configs.len() == 0
            && self.layer_configs.len() == 0
            && self.condition_map.len() == 0
            && self.time == 0
    }
}

#[skip_serializing_none]
#[derive(Deserialize)]
pub struct SpecsResponseNoUpdates {
    pub has_updates: bool,
}

impl Condition {
    pub(crate) fn has_same_targeting(&self, other: &Self) -> bool {
        self.condition_type == other.condition_type
            && self.id_type == other.id_type
            && self.field == other.field
            && self.operator == other.operator
            && self.target_value == other.target_value
            && self.additional_values == other.additional_values
    }

    pub(crate) fn compile_cron_window(&mut self) {
        self.compiled_cron_window = None;
        if !matches!(self.compiled_condition_type, ConditionType::CurrentTime)
            || !matches!(self.compiled_operator, ConditionOperator::InCronWindow)
        {
            return;
        }

        self.compiled_cron_window = self
            .target_value
            .as_ref()
            .and_then(|value| value.as_value_ref().string_value())
            .and_then(|value| CronWindow::parse(value).ok())
            .map(Arc::new);
    }
}

// Keep the marker on the wire only: ordinary conditions are decoded once, and
// a later entry with the same ID can replace an earlier invalid declaration.
struct WireCondition(Condition, bool);

fn deserialize_condition_map<'de, D: Deserializer<'de>>(
    deserializer: D,
) -> Result<AHashMap<InternedString, Condition>, D::Error> {
    use serde::de::{Error, MapAccess, Visitor};

    struct Conditions;
    impl<'de> Visitor<'de> for Conditions {
        type Value = AHashMap<InternedString, Condition>;

        fn expecting(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            f.write_str("a condition map")
        }

        fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
            let mut conditions = AHashMap::default();
            let mut invalid = std::collections::HashSet::new();
            while let Some((id, WireCondition(condition, has_remote))) =
                map.next_entry::<InternedString, WireCondition>()?
            {
                if has_remote {
                    invalid.insert(id);
                } else {
                    if !invalid.is_empty() {
                        invalid.remove(&id);
                    }
                    conditions.insert(id, condition);
                }
            }
            if !invalid.is_empty() {
                return Err(A::Error::custom(
                    crate::specs_adapter::remote_config_value_hydrator::unsupported_entity_error(),
                ));
            }
            Ok(conditions)
        }
    }
    deserializer.deserialize_map(Conditions)
}

impl<'de> Deserialize<'de> for Condition {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        let WireCondition(condition, has_remote) = WireCondition::deserialize(deserializer)?;
        if has_remote {
            return Err(serde::de::Error::custom(
                crate::specs_adapter::remote_config_value_hydrator::unsupported_entity_error(),
            ));
        }
        Ok(condition)
    }
}

fn declared_metadata<'de, D: Deserializer<'de>>(deserializer: D) -> Result<bool, D::Error> {
    serde::de::IgnoredAny::deserialize(deserializer)?;
    Ok(true)
}

impl<'de> Deserialize<'de> for WireCondition {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        #[derive(Deserialize)]
        #[serde(rename_all = "camelCase")]
        struct ConditionInternal {
            #[serde(
                rename = "remoteConfigMetadata",
                default,
                deserialize_with = "declared_metadata"
            )]
            has_remote_metadata: bool,
            rules: Option<Box<RawValue>>,
            #[serde(rename = "type")]
            condition_type: InternedString,
            target_value: Option<Box<RawValue>>,
            operator: Option<InternedString>,
            field: Option<DynamicString>,
            additional_values: Option<HashMap<InternedString, InternedString>>,
            id_type: DynamicString,
            checksum: Option<InternedString>,
        }

        let internal = ConditionInternal::deserialize(deserializer)?;
        let compiled_condition_type = ConditionType::from_str(internal.condition_type.as_str());
        let compiled_operator = ConditionOperator::from_str(internal.operator.as_deref());
        // The operator determines which spellings the target map must retain.
        // Defer parsing until it is known, regardless of JSON field order.
        let mut target_value = internal.target_value.map(|value| {
            EvaluatorValue::from_raw_value_with_array_key_mode(
                std::borrow::Cow::Owned(value),
                compiled_operator.evaluator_array_key_mode(),
            )
        });

        if let Some(ref op) = internal.operator {
            if op == "str_matches" {
                if let Some(ref mut tv) = target_value {
                    tv.compile_regex();
                }
            }
        }

        let mut condition = Condition {
            condition_type: internal.condition_type,
            compiled_condition_type,
            target_value,
            operator: internal.operator,
            compiled_operator,
            compiled_cron_window: None,
            field: internal.field,
            additional_values: internal.additional_values,
            id_type: internal.id_type,
            checksum: internal.checksum,
        };
        condition.compile_cron_window();
        let has_remote = internal.has_remote_metadata
            || internal
                .rules
                .as_deref()
                .is_some_and(raw_rules_have_remote_metadata);
        Ok(WireCondition(condition, has_remote))
    }
}

#[cfg(test)]
mod condition_dispatch_tests {
    use chrono::DateTime;
    use serde_json::json;

    use super::{Condition, ConditionOperator, ConditionType, SpecsResponseFull};

    fn console_cron_window_e2e_payload(condition: serde_json::Value) -> serde_json::Value {
        json!({
            "dynamic_configs": {
                "e2e_cron_window_2026-09-22_ada": {
                    "type": "dynamic_config",
                    "salt": "ca8fba93-c621-404a-afe9-a7d9774f9a63",
                    "enabled": true,
                    "defaultValue": { "enabled": false },
                    "rules": [{
                        "name": "43yUbYMbtevJ7vxUMsL5xG-43yUbX790WmeO5ZZbkPseE",
                        "passPercentage": 100,
                        "conditions": ["1349838392"],
                        "returnValue": { "enabled": true },
                        "id": "43yUbYMbtevJ7vxUMsL5xG-43yUbX790WmeO5ZZbkPseE",
                        "salt": "8182045d-cb5c-4d69-8c61-504ef42ecbad",
                        "idType": "userID"
                    }],
                    "idType": "userID",
                    "entity": "dynamic_config",
                    "version": 2,
                    "checksum": "244349174"
                }
            },
            "feature_gates": {},
            "layer_configs": {},
            "experiment_to_layer": {},
            "condition_map": { "1349838392": condition },
            "has_updates": true,
            "response_format": "dcs-v2",
            "time": 1790107014475_u64
        })
    }

    fn millis(value: &str) -> i64 {
        DateTime::parse_from_rfc3339(value)
            .unwrap()
            .timestamp_millis()
    }

    #[test]
    fn dispatch_tags_are_one_byte() {
        assert_eq!(std::mem::size_of::<ConditionType>(), 1);
        assert_eq!(std::mem::size_of::<ConditionOperator>(), 1);
    }

    #[test]
    fn classifies_known_and_unknown_condition_types() {
        assert_eq!(
            ConditionType::from_str("user_field"),
            ConditionType::UserField
        );
        assert_eq!(
            ConditionType::from_str("future_condition_type"),
            ConditionType::Unknown
        );
    }

    #[test]
    fn distinguishes_missing_none_and_unknown_operators() {
        assert_eq!(
            ConditionOperator::from_str(None),
            ConditionOperator::Missing
        );
        assert_eq!(
            ConditionOperator::from_str(Some("none")),
            ConditionOperator::NoneOf
        );
        assert_eq!(
            ConditionOperator::from_str(Some("gte")),
            ConditionOperator::Gte
        );
        assert_eq!(
            ConditionOperator::from_str(Some("in_cron_window")),
            ConditionOperator::InCronWindow
        );
        assert_eq!(
            ConditionOperator::from_str(Some("future_operator")),
            ConditionOperator::Unknown
        );
    }

    fn decode_condition() -> Condition {
        serde_json::from_value(json!({
            "type": "user_field",
            "targetValue": ["match@example.com"],
            "operator": "any",
            "field": "email",
            "idType": "userID"
        }))
        .unwrap()
    }

    #[test]
    fn json_decode_populates_compiled_tags() {
        let condition = decode_condition();
        assert_eq!(condition.compiled_condition_type, ConditionType::UserField);
        assert_eq!(condition.compiled_operator, ConditionOperator::Any);
    }

    #[test]
    fn serialization_omits_compiled_tags() {
        let condition = decode_condition();
        let serialized = serde_json::to_value(condition).unwrap();
        assert_eq!(serialized["type"], "user_field");
        assert_eq!(serialized["operator"], "any");
        assert!(serialized.get("compiledConditionType").is_none());
        assert!(serialized.get("compiledOperator").is_none());
    }

    #[test]
    fn json_decode_compiles_cron_window() {
        let condition: Condition = serde_json::from_value(json!({
            "type": "current_time",
            "targetValue": "0 22 * * *|43200",
            "operator": "in_cron_window",
            "field": null,
            "idType": "userID"
        }))
        .unwrap();

        assert_eq!(
            condition.compiled_condition_type,
            ConditionType::CurrentTime
        );
        assert_eq!(condition.compiled_operator, ConditionOperator::InCronWindow);
        assert!(condition.compiled_cron_window.is_some());

        let serialized = serde_json::to_value(condition).unwrap();
        assert!(serialized.get("compiledCronWindow").is_none());
    }

    #[test]
    fn deployed_console_e2e_payload_safely_marks_missing_cron_operator() {
        let response: SpecsResponseFull =
            serde_json::from_value(console_cron_window_e2e_payload(json!({
                "type": "current_time",
                "operator": null,
                "field": null,
                "additionalValues": {},
                "idType": "userID",
                "checksum": "2648535423"
            })))
            .unwrap();
        let condition = response.condition_map.values().next().unwrap();

        assert_eq!(
            condition.compiled_condition_type,
            ConditionType::CurrentTime
        );
        assert_eq!(condition.compiled_operator, ConditionOperator::Missing);
        assert!(condition.target_value.is_none());
        assert!(condition.compiled_cron_window.is_none());
    }

    #[test]
    fn corrected_console_e2e_payload_compiles_and_observes_window_boundaries() {
        let response: SpecsResponseFull =
            serde_json::from_value(console_cron_window_e2e_payload(json!({
                "type": "current_time",
                "operator": "in_cron_window",
                "targetValue": "0 22 * * *|43200",
                "field": null,
                "additionalValues": {},
                "idType": "userID"
            })))
            .unwrap();
        let condition = response.condition_map.values().next().unwrap();
        let window = condition.compiled_cron_window.as_ref().unwrap();

        assert_eq!(
            condition.compiled_condition_type,
            ConditionType::CurrentTime
        );
        assert_eq!(condition.compiled_operator, ConditionOperator::InCronWindow);
        assert!(!window.is_active_at_millis(millis("2026-09-18T21:59:59Z")));
        assert!(window.is_active_at_millis(millis("2026-09-18T22:00:00Z")));
        assert!(window.is_active_at_millis(millis("2026-09-19T09:59:59Z")));
        assert!(!window.is_active_at_millis(millis("2026-09-19T10:00:00Z")));
    }
}
