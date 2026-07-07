use std::collections::HashMap;

use ahash::HashMap as AHashMap;
use serde::{Deserialize, Deserializer, Serialize};
use serde_with::skip_serializing_none;

use crate::evaluation::dynamic_string::DynamicString;
use crate::evaluation::{dynamic_returnable::DynamicReturnable, evaluator_value::EvaluatorValue};
use crate::gcir::gcir_formatter::GCIRHashable;
use crate::hashing::opt_bool_to_hashable;
use crate::interned_string::InternedString;
use crate::specs_response::explicit_params::ExplicitParameters;
use crate::specs_response::specs_hash_map::SpecsHashMap;
use crate::{hashing, DynamicValue};

use super::{cmab_types::CMABConfig, param_store_types::ParameterStore};

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
    Unknown,
}

impl ConditionOperator {
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
    pub condition_map: AHashMap<InternedString, Condition>,
    pub dynamic_configs: SpecsHashMap,
    pub feature_gates: SpecsHashMap,
    pub has_updates: bool,
    pub layer_configs: SpecsHashMap,
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

impl<'de> Deserialize<'de> for Condition {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        #[derive(Deserialize)]
        #[serde(rename_all = "camelCase")]
        struct ConditionInternal {
            #[serde(rename = "type")]
            condition_type: InternedString,
            target_value: Option<EvaluatorValue>,
            operator: Option<InternedString>,
            field: Option<DynamicString>,
            additional_values: Option<HashMap<InternedString, InternedString>>,
            id_type: DynamicString,
            checksum: Option<InternedString>,
        }

        let mut internal = ConditionInternal::deserialize(deserializer)?;

        if let Some(ref op) = internal.operator {
            if op == "str_matches" {
                if let Some(ref mut tv) = internal.target_value {
                    tv.compile_regex();
                }
            }
        }

        let compiled_condition_type = ConditionType::from_str(internal.condition_type.as_str());
        let compiled_operator = ConditionOperator::from_str(internal.operator.as_deref());

        Ok(Condition {
            condition_type: internal.condition_type,
            compiled_condition_type,
            target_value: internal.target_value,
            operator: internal.operator,
            compiled_operator,
            field: internal.field,
            additional_values: internal.additional_values,
            id_type: internal.id_type,
            checksum: internal.checksum,
        })
    }
}

#[cfg(test)]
mod condition_dispatch_tests {
    use serde_json::json;

    use super::{Condition, ConditionOperator, ConditionType};

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
}
