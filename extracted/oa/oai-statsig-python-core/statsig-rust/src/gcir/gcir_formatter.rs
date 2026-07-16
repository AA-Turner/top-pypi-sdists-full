use crate::gcir::dynamic_configs_processor::{
    get_dynamic_config_evaluations_init_v2, get_dynamic_config_evaluations_with_plan,
};
use crate::gcir::evaluation_plan::GcirEvaluationPlan;
use crate::gcir::feature_gates_processor::{
    get_gate_evaluations, get_gate_evaluations_init_v2, get_gate_evaluations_with_plan,
};
use crate::gcir::layer_configs_processor::{
    get_layer_evaluations_init_v2, get_layer_evaluations_with_plan,
};
use crate::hashing::opt_bool_to_hashable;
use ahash::AHashMap;

use crate::initialize_v2_response::InitializeV2Response;
use crate::interned_string::InternedString;
use crate::specs_response::spec_types::{SessionReplayPrivacySetting, SessionReplayTrigger};
use crate::{
    evaluation::evaluator::{Evaluator, SpecType},
    evaluation::evaluator_context::EvaluatorContext,
    initialize_evaluations_response::InitializeEvaluationsResponse,
    initialize_response::InitializeResponse,
    statsig_metadata::StatsigMetadata,
    StatsigErr,
};

use crate::{
    evaluation::dynamic_string::DynamicString, hashing, user::StatsigUserInternal, StatsigUser,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use super::dynamic_configs_processor::{
    get_dynamic_config_evaluations, get_dynamic_config_evaluations_v2,
};
use super::feature_gates_processor::get_gate_evaluations_v2;
use super::gcir_options::ClientInitResponseOptions;
use super::layer_configs_processor::{get_layer_evaluations, get_layer_evaluations_v2};
use super::param_stores_processor::get_serializeable_param_stores;

#[derive(Deserialize)]
pub enum GCIRResponseFormat {
    Initialize,                             // v1
    InitializeWithSecondaryExposureMapping, // v2
    InitializeV2,                           // v3
}

pub trait GCIRHashable {
    fn create_hash(&self, name: &InternedString) -> u64;
}

impl GCIRResponseFormat {
    #[must_use]
    pub fn from_string(input: &str) -> Option<Self> {
        match input {
            "v1" => Some(GCIRResponseFormat::Initialize),
            "v2" => Some(GCIRResponseFormat::InitializeWithSecondaryExposureMapping),
            "init_v2" => Some(GCIRResponseFormat::InitializeV2),
            _ => None,
        }
    }
}

pub struct GCIRFormatter;

impl GCIRFormatter {
    pub fn generate_v1_format(
        context: &mut EvaluatorContext,
        options: &ClientInitResponseOptions,
    ) -> Result<InitializeResponse, StatsigErr> {
        Self::generate_v1_format_internal(context, options, None)
    }

    pub fn generate_v1_format_with_plan(
        context: &mut EvaluatorContext,
        options: &ClientInitResponseOptions,
        plan: &GcirEvaluationPlan,
    ) -> Result<InitializeResponse, StatsigErr> {
        gcir_time!("v1.total", {
            Self::generate_v1_format_internal(context, options, Some(plan))
        })
    }

    fn generate_v1_format_internal(
        context: &mut EvaluatorContext,
        options: &ClientInitResponseOptions,
        plan: Option<&GcirEvaluationPlan>,
    ) -> Result<InitializeResponse, StatsigErr> {
        let mut sec_expo_hash_memo = gcir_time!("v1.sec_expo_memo_alloc", {
            HashMap::with_capacity(plan.map_or(0, GcirEvaluationPlan::total_evaluation_count))
        });

        let gates = gcir_time!("v1.gates", {
            match plan {
                Some(plan) => {
                    get_gate_evaluations_with_plan(context, options, &mut sec_expo_hash_memo, plan)
                }
                None => get_gate_evaluations(context, options, &mut sec_expo_hash_memo)
                    .map(intern_response_keys),
            }
        })?;
        let configs = gcir_time!("v1.configs", {
            match plan {
                Some(plan) => get_dynamic_config_evaluations_with_plan(
                    context,
                    options,
                    &mut sec_expo_hash_memo,
                    plan,
                ),
                None => get_dynamic_config_evaluations(context, options, &mut sec_expo_hash_memo)
                    .map(intern_response_keys),
            }
        })?;
        let layers = gcir_time!("v1.layers", {
            match plan {
                Some(plan) => {
                    get_layer_evaluations_with_plan(context, options, &mut sec_expo_hash_memo, plan)
                }
                None => get_layer_evaluations(context, options, &mut sec_expo_hash_memo)
                    .map(intern_response_keys),
            }
        })?;

        let param_stores = gcir_time!("v1.param_stores", {
            get_serializeable_param_stores(context, options)
        });
        let evaluated_keys = gcir_time!("v1.evaluated_keys", {
            EvaluatedKeys::from_internal_user(context.user)
        });
        let session_replay_info = gcir_time!("v1.session_replay_info", {
            get_session_replay_info(context, options)
        });

        let mut should_return_blank = false;
        let full_response_hash = gcir_time!("v1.full_response_checksum", {
            if let Some(previous_full_hash) = &options.previous_response_hash {
                let new_full_hash = hashing::hash_one(context.gcir_hashes.clone()).to_string();
                if previous_full_hash.as_str() == new_full_hash {
                    should_return_blank = true;
                    None
                } else {
                    Some(new_full_hash)
                }
            } else {
                None
            }
        });
        if should_return_blank {
            return Ok(InitializeResponse::blank_without_user());
        }

        Ok(gcir_time!("v1.response_assembly", {
            InitializeResponse {
                feature_gates: gates,
                dynamic_configs: configs,
                layer_configs: layers,
                time: context.specs_data.time,
                has_updates: true,
                hash_used: options.get_hash_algorithm().to_string(),
                user: context.user.to_loggable(),
                sdk_params: HashMap::new(),
                evaluated_keys,
                sdk_info: get_sdk_info(),
                param_stores,
                can_record_session: session_replay_info.can_record_session,
                session_recording_rate: session_replay_info.session_recording_rate,
                recording_blocked: session_replay_info.recording_blocked,
                passes_session_recording_targeting: session_replay_info
                    .passes_session_recording_targeting,
                session_recording_event_triggers: session_replay_info
                    .session_recording_event_triggers,
                session_recording_exposure_triggers: session_replay_info
                    .session_recording_exposure_triggers,
                session_recording_privacy_settings: session_replay_info
                    .session_recording_privacy_settings,
                pa_hash: context.user.get_hashed_private_attributes(),
                full_checksum: full_response_hash,
            }
        }))
    }

    pub fn generate_v2_format(
        context: &mut EvaluatorContext,
        options: &ClientInitResponseOptions,
    ) -> Result<InitializeEvaluationsResponse, StatsigErr> {
        let mut sec_expo_hash_memo = HashMap::new();
        let mut exposures = HashMap::new();

        let param_stores = get_serializeable_param_stores(context, options);
        let evaluated_keys = EvaluatedKeys::from_internal_user(context.user);
        let session_replay_info = get_session_replay_info(context, options);

        Ok(InitializeEvaluationsResponse {
            feature_gates: get_gate_evaluations_v2(
                context,
                options,
                &mut sec_expo_hash_memo,
                &mut exposures,
            )?,
            dynamic_configs: get_dynamic_config_evaluations_v2(
                context,
                options,
                &mut sec_expo_hash_memo,
                &mut exposures,
            )?,
            layer_configs: get_layer_evaluations_v2(
                context,
                options,
                &mut sec_expo_hash_memo,
                &mut exposures,
            )?,
            time: context.specs_data.time,
            has_updates: true,
            hash_used: options.get_hash_algorithm().to_string(),
            user: context.user.to_loggable(),
            pa_hash: context.user.get_hashed_private_attributes(),
            sdk_params: HashMap::new(),
            evaluated_keys,
            sdk_info: get_sdk_info(),
            param_stores,
            exposures,
            can_record_session: session_replay_info.can_record_session,
            session_recording_rate: session_replay_info.session_recording_rate,
            recording_blocked: session_replay_info.recording_blocked,
            passes_session_recording_targeting: session_replay_info
                .passes_session_recording_targeting,
            session_recording_event_triggers: session_replay_info.session_recording_event_triggers,
            session_recording_exposure_triggers: session_replay_info
                .session_recording_exposure_triggers,
            session_recording_privacy_settings: session_replay_info
                .session_recording_privacy_settings,
        })
    }

    pub fn generate_init_v2_format(
        context: &mut EvaluatorContext,
        options: &ClientInitResponseOptions,
    ) -> Result<InitializeV2Response, StatsigErr> {
        let mut values = HashMap::new();
        let mut val_map = AHashMap::new();
        let mut exposure_map = AHashMap::new();
        let mut exposures = HashMap::new();
        let param_stores = get_serializeable_param_stores(context, options);
        let evaluated_keys = EvaluatedKeys::from_internal_user(context.user);
        let session_replay_info = get_session_replay_info(context, options);

        Ok(InitializeV2Response {
            feature_gates: get_gate_evaluations_init_v2(
                context,
                options,
                &mut exposures,
                &mut exposure_map,
            )?,
            dynamic_configs: get_dynamic_config_evaluations_init_v2(
                context,
                options,
                &mut exposures,
                &mut exposure_map,
                &mut values,
                &mut val_map,
            )?,
            layer_configs: get_layer_evaluations_init_v2(
                context,
                options,
                &mut exposures,
                &mut exposure_map,
                &mut values,
                &mut val_map,
            )?,
            param_stores,
            time: context.specs_data.time,
            has_updates: true,
            hash_used: options.get_hash_algorithm().to_string(),
            user: context.user.to_loggable(),
            pa_hash: context.user.get_hashed_private_attributes(),
            sdk_params: HashMap::new(),
            evaluated_keys,
            sdk_info: get_sdk_info(),
            exposures,
            can_record_session: session_replay_info.can_record_session,
            session_recording_rate: session_replay_info.session_recording_rate,
            recording_blocked: session_replay_info.recording_blocked,
            passes_session_recording_targeting: session_replay_info
                .passes_session_recording_targeting,
            session_recording_event_triggers: session_replay_info.session_recording_event_triggers,
            session_recording_exposure_triggers: session_replay_info
                .session_recording_exposure_triggers,
            session_recording_privacy_settings: session_replay_info
                .session_recording_privacy_settings,
            values,
            response_format: "init-v2".to_string(),
        })
    }
}

fn intern_response_keys<T>(map: HashMap<String, T>) -> HashMap<InternedString, T> {
    map.into_iter()
        .map(|(key, value)| (InternedString::from_string(key), value))
        .collect()
}

fn get_sdk_info() -> HashMap<String, String> {
    let metadata = StatsigMetadata::get_metadata();
    HashMap::from([
        ("sdkType".to_string(), metadata.sdk_type),
        ("sdkVersion".to_string(), metadata.sdk_version),
        ("sessionId".to_string(), metadata.session_id),
    ])
}

pub struct GCIRSessionReplayInfo {
    pub can_record_session: Option<bool>,
    pub session_recording_rate: Option<f64>,
    pub recording_blocked: Option<bool>,
    pub passes_session_recording_targeting: Option<bool>,
    pub session_recording_event_triggers: Option<HashMap<String, SessionReplayTrigger>>,
    pub session_recording_exposure_triggers: Option<HashMap<String, SessionReplayTrigger>>,
    pub session_recording_privacy_settings: Option<SessionReplayPrivacySetting>,
}

impl GCIRHashable for GCIRSessionReplayInfo {
    fn create_hash(&self, _: &InternedString) -> u64 {
        let hash_array = vec![
            opt_bool_to_hashable(&self.can_record_session),
            opt_bool_to_hashable(&self.recording_blocked),
            opt_bool_to_hashable(&self.passes_session_recording_targeting),
        ];
        hashing::hash_one(hash_array)
    }
}

fn get_session_replay_info(
    context: &mut EvaluatorContext,
    options: &ClientInitResponseOptions,
) -> GCIRSessionReplayInfo {
    let mut session_replay_info = GCIRSessionReplayInfo {
        can_record_session: None,
        session_recording_rate: None,
        recording_blocked: None,
        passes_session_recording_targeting: None,
        session_recording_event_triggers: None,
        session_recording_exposure_triggers: None,
        session_recording_privacy_settings: None,
    };

    let session_replay_data = match &context.specs_data.session_replay_info {
        Some(data) => data,
        None => {
            context.gcir_hashes.push(0);
            return session_replay_info;
        }
    };

    session_replay_info.can_record_session = Some(true);
    session_replay_info.recording_blocked = session_replay_data.recording_blocked;
    if session_replay_data.recording_blocked == Some(true) {
        session_replay_info.can_record_session = Some(false);
    }

    let targeting_gate_name = &session_replay_data.targeting_gate;

    if let Some(gate_name) = targeting_gate_name {
        match Evaluator::evaluate(context, gate_name, &SpecType::Gate) {
            Ok(_result) => {
                session_replay_info.passes_session_recording_targeting =
                    Some(context.result.bool_value);
                if !context.result.bool_value {
                    session_replay_info.can_record_session = Some(false);
                }
            }
            Err(_e) => {
                session_replay_info.passes_session_recording_targeting = Some(false);
                session_replay_info.can_record_session = Some(false);
            }
        }
    }

    let session_id_field = Some(DynamicString::from("sessionID".to_string()));
    let session_id = context
        .user
        .get_user_value(&session_id_field)
        .and_then(|value| value.string_value())
        .unwrap_or_default()
        .to_string();
    let session_replay_bucket = context
        .hashing
        .evaluation_hash(&session_id)
        .map(|hash| hash % 1000);

    if let Some(rate) = &session_replay_data.sampling_rate {
        session_replay_info.session_recording_rate = Some(*rate);
        if !passes_session_replay_sampling(session_replay_bucket, *rate) {
            session_replay_info.can_record_session = Some(false);
        }
    }

    let mut event_triggers_hash = Vec::new();
    if let Some(triggers) = &session_replay_data.session_recording_event_triggers {
        let mut new_event_triggers = HashMap::new();
        for (key, trigger) in triggers {
            let mut new_trigger = SessionReplayTrigger {
                values: trigger.values.clone(),
                sampling_rate: None,
                passes_sampling: None,
            };
            if let Some(rate) = &trigger.sampling_rate {
                new_trigger.passes_sampling =
                    Some(passes_session_replay_sampling(session_replay_bucket, *rate));
            }
            if options.previous_response_hash.is_some() {
                event_triggers_hash.push(new_trigger.create_hash(key));
            }
            new_event_triggers.insert(key.unperformant_to_string(), new_trigger);
        }
        session_replay_info.session_recording_event_triggers = Some(new_event_triggers);
    }

    let mut exposure_triggers_hash = Vec::new();
    if let Some(triggers) = &session_replay_data.session_recording_exposure_triggers {
        let mut new_exposure_triggers = HashMap::new();
        for (key, trigger) in triggers {
            let mut new_trigger = SessionReplayTrigger {
                values: trigger.values.clone(),
                sampling_rate: None,
                passes_sampling: None,
            };
            if let Some(rate) = &trigger.sampling_rate {
                new_trigger.passes_sampling =
                    Some(passes_session_replay_sampling(session_replay_bucket, *rate));
            }
            if options.previous_response_hash.is_some() {
                exposure_triggers_hash.push(new_trigger.create_hash(key));
            }
            new_exposure_triggers.insert(
                context
                    .hashing
                    .hash(key.as_str(), options.get_hash_algorithm()),
                new_trigger,
            );
        }
        session_replay_info.session_recording_exposure_triggers = Some(new_exposure_triggers);
    }
    if options.previous_response_hash.is_some() {
        let combined_hashes = vec![
            session_replay_info.create_hash(InternedString::empty_ref()),
            hashing::hash_unordered(event_triggers_hash),
            hashing::hash_unordered(exposure_triggers_hash),
        ];
        context.gcir_hashes.push(hashing::hash_one(combined_hashes));
    }

    session_replay_info.session_recording_privacy_settings = session_replay_data
        .session_recording_privacy_settings
        .clone();

    session_replay_info
}

fn passes_session_replay_sampling(bucket: Option<u64>, rate: f64) -> bool {
    bucket.is_some_and(|bucket| (bucket as f64) < rate * 1000.0)
}

#[derive(Serialize, Deserialize, Default)]
pub struct EvaluatedKeys {
    #[serde(rename = "userID", skip_serializing_if = "Option::is_none")]
    pub user_id: Option<InternedString>,
    #[serde(rename = "customIDs", skip_serializing_if = "Option::is_none")]
    pub custom_ids: Option<HashMap<InternedString, InternedString>>,
}

impl EvaluatedKeys {
    pub fn from_user(user: &StatsigUser) -> Self {
        let user_id = user.data.user_id.as_ref().and_then(|u| {
            u.string_value
                .as_ref()
                .map(|s| s.value.as_str())
                .and_then(|s| {
                    if s.is_empty() {
                        None
                    } else {
                        Some(InternedString::from_str_ref(s))
                    }
                })
        });

        let custom_ids = user.data.custom_ids.as_ref().and_then(|c| {
            let mut custom_ids = HashMap::new();
            for (key, value) in c {
                custom_ids.insert(
                    InternedString::from_str_ref(key.as_str()),
                    value
                        .string_value
                        .as_ref()
                        .map(|value| InternedString::from_str_ref(value.value.as_str()))
                        .unwrap_or_default(),
                );
            }

            if custom_ids.is_empty() {
                None
            } else {
                Some(custom_ids)
            }
        });

        Self {
            user_id,
            custom_ids,
        }
    }

    pub fn from_internal_user(user: &StatsigUserInternal<'_, '_>) -> Self {
        let user_id = user.get_user_id_str().and_then(|value| {
            if value.is_empty() {
                None
            } else {
                Some(InternedString::from_str_ref(value))
            }
        });

        let custom_ids = {
            let mut custom_ids = HashMap::new();
            for (key, value) in user.custom_id_pairs() {
                custom_ids.insert(
                    InternedString::from_str_ref(key),
                    InternedString::from_str_ref(value),
                );
            }

            if custom_ids.is_empty() {
                None
            } else {
                Some(custom_ids)
            }
        };

        Self {
            user_id,
            custom_ids,
        }
    }
}

#[cfg(test)]
mod tests {
    use std::collections::{HashMap, HashSet};

    use crate::{
        dcs_str::DCS_STR,
        evaluation::{
            dynamic_value::DynamicValue,
            evaluator_context::{EvaluatorContext, IdListResolution},
        },
        gcir::{evaluation_plan::GcirEvaluationPlan, gcir_formatter::GCIRFormatter},
        hashing::{HashAlgorithm, HashUtil},
        interned_string::InternedString,
        specs_response::{
            spec_types::{SessionReplayInfo, SessionReplayTrigger, Spec, SpecsResponseFull},
            specs_hash_map::SpecPointer,
        },
        user::{StatsigUser, StatsigUserInternal},
        ClientInitResponseOptions,
    };

    fn planned_and_unplanned_response_values(
        options: &ClientInitResponseOptions,
    ) -> (serde_json::Value, serde_json::Value) {
        planned_and_unplanned_response_values_with_specs(options, None, |_| {})
    }

    fn planned_and_unplanned_response_values_with_specs(
        options: &ClientInitResponseOptions,
        app_id: Option<&DynamicValue>,
        update_specs: impl FnOnce(&mut SpecsResponseFull),
    ) -> (serde_json::Value, serde_json::Value) {
        let mut specs: SpecsResponseFull = serde_json::from_str(DCS_STR).unwrap();
        specs.session_replay_info = None;
        update_specs(&mut specs);

        let hashing = HashUtil::new();
        let plan = GcirEvaluationPlan::new(&specs, &hashing);
        let user = StatsigUser::with_user_id("user-in-test");
        let user_internal = StatsigUserInternal::new(&user, None);
        let id_list_callback = |_: &str, _: &str| false;

        let mut unplanned_context = EvaluatorContext::new(
            &user_internal,
            &specs,
            IdListResolution::Callback(&id_list_callback),
            &hashing,
            app_id,
            None,
            false,
            None,
            true,
        );
        let unplanned = GCIRFormatter::generate_v1_format(&mut unplanned_context, options).unwrap();

        let mut planned_context = EvaluatorContext::new(
            &user_internal,
            &specs,
            IdListResolution::Callback(&id_list_callback),
            &hashing,
            app_id,
            None,
            false,
            None,
            true,
        );
        let planned =
            GCIRFormatter::generate_v1_format_with_plan(&mut planned_context, options, &plan)
                .unwrap();

        (
            serde_json::to_value(unplanned).unwrap(),
            serde_json::to_value(planned).unwrap(),
        )
    }

    fn session_replay_response(session_id: &str) -> serde_json::Value {
        let mut specs: SpecsResponseFull = serde_json::from_str(DCS_STR).unwrap();
        specs.session_replay_info = Some(SessionReplayInfo {
            sampling_rate: Some(0.4),
            targeting_gate: None,
            recording_blocked: Some(false),
            session_recording_event_triggers: Some(HashMap::from([(
                InternedString::from_str_ref("checkout"),
                SessionReplayTrigger {
                    sampling_rate: Some(0.4),
                    values: None,
                    passes_sampling: None,
                },
            )])),
            session_recording_exposure_triggers: Some(HashMap::from([(
                InternedString::from_str_ref("experiment"),
                SessionReplayTrigger {
                    sampling_rate: Some(0.3),
                    values: None,
                    passes_sampling: None,
                },
            )])),
            session_recording_privacy_settings: None,
        });

        let hashing = HashUtil::new();
        let mut user = StatsigUser::with_user_id("user-in-test");
        user.set_custom(HashMap::from([(
            "sessionID".to_string(),
            DynamicValue::from_string(session_id),
        )]));
        let user_internal = StatsigUserInternal::new(&user, None);
        let id_list_callback = |_: &str, _: &str| false;
        let mut context = EvaluatorContext::new(
            &user_internal,
            &specs,
            IdListResolution::Callback(&id_list_callback),
            &hashing,
            None,
            None,
            false,
            None,
            true,
        );
        let options = ClientInitResponseOptions {
            previous_response_hash: Some("stale-checksum".to_string()),
            ..Default::default()
        };

        serde_json::to_value(GCIRFormatter::generate_v1_format(&mut context, &options).unwrap())
            .unwrap()
    }

    #[test]
    fn session_replay_sampling_is_deterministic_and_matches_scrapi() {
        let hashing = HashUtil::new();
        let session_a = "session-a".to_string();
        let session_b = "session-b".to_string();
        assert_eq!(hashing.evaluation_hash(&session_a).unwrap() % 1000, 378);
        assert_eq!(hashing.evaluation_hash(&session_b).unwrap() % 1000, 463);

        let first = session_replay_response(&session_a);
        let repeated = session_replay_response(&session_a);
        assert_eq!(first, repeated);
        assert_eq!(first["can_record_session"], true);
        assert_eq!(
            first["session_recording_event_triggers"]["checkout"]["passes_sampling"],
            true
        );
        assert_eq!(
            first["session_recording_exposure_triggers"]
                .as_object()
                .unwrap()
                .values()
                .next()
                .unwrap()["passes_sampling"],
            false
        );

        let different_session = session_replay_response(&session_b);
        assert_eq!(different_session["can_record_session"], false);
        assert_eq!(
            different_session["session_recording_event_triggers"]["checkout"]["passes_sampling"],
            false
        );
        assert_ne!(first["full_checksum"], different_session["full_checksum"]);
    }

    #[test]
    fn planned_v1_format_matches_unplanned_across_plan_modes() {
        for (has_checksum, has_filters) in
            [(false, false), (false, true), (true, false), (true, true)]
        {
            let options = ClientInitResponseOptions {
                hash_algorithm: Some(HashAlgorithm::Sha256),
                client_sdk_key: Some("client-key".to_string()),
                previous_response_hash: has_checksum.then(|| "stale-checksum".to_string()),
                feature_gate_filter: has_filters.then(|| HashSet::from(["test_50_50".to_string()])),
                dynamic_config_filter: has_filters
                    .then(|| HashSet::from(["operating_system_config".to_string()])),
                layer_filter: has_filters.then(|| HashSet::from(["test_layer".to_string()])),
                ..Default::default()
            };

            let (unplanned, planned) = planned_and_unplanned_response_values(&options);

            assert_eq!(
                unplanned, planned,
                "has_checksum={has_checksum}, has_filters={has_filters}"
            );
        }
    }

    #[test]
    fn planned_v1_format_respects_app_id_filtering() {
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-key".to_string()),
            ..Default::default()
        };
        let app_id = DynamicValue::from_string("other-app");

        let (unplanned, planned) =
            planned_and_unplanned_response_values_with_specs(&options, Some(&app_id), |specs| {
                let spec: Spec = serde_json::from_value(serde_json::json!({
                    "type": "feature_gate",
                    "salt": "targeted-gate-salt",
                    "defaultValue": false,
                    "enabled": true,
                    "rules": [],
                    "idType": "userID",
                    "entity": "feature_gate",
                    "targetAppIDs": ["allowed-app"]
                }))
                .unwrap();
                specs.feature_gates.insert(
                    InternedString::from_str_ref("targeted_gate"),
                    SpecPointer::from_spec(spec),
                );
            });

        assert_eq!(unplanned, planned);
        assert!(!planned["feature_gates"]
            .as_object()
            .unwrap()
            .contains_key("targeted_gate"));
    }

    #[test]
    fn planned_v1_format_removes_default_value_gates() {
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-key".to_string()),
            previous_response_hash: Some("stale-checksum".to_string()),
            remove_default_value_gates: Some(true),
            ..Default::default()
        };

        let (unplanned, planned) =
            planned_and_unplanned_response_values_with_specs(&options, None, |specs| {
                let spec: Spec = serde_json::from_value(serde_json::json!({
                    "type": "feature_gate",
                    "salt": "default-gate-salt",
                    "defaultValue": false,
                    "enabled": true,
                    "rules": [],
                    "idType": "userID",
                    "entity": "feature_gate"
                }))
                .unwrap();
                specs.feature_gates.insert(
                    InternedString::from_str_ref("default_false_gate"),
                    SpecPointer::from_spec(spec),
                );
            });

        assert_eq!(unplanned, planned);
        assert!(!planned["feature_gates"]
            .as_object()
            .unwrap()
            .contains_key("default_false_gate"));
    }

    #[test]
    fn planned_v1_format_removes_layered_experiments_before_response() {
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-key".to_string()),
            remove_experiments_in_layers: Some(true),
            ..Default::default()
        };

        let (unplanned, planned) = planned_and_unplanned_response_values(&options);

        assert_eq!(unplanned, planned);
        assert!(!planned["dynamic_configs"]
            .as_object()
            .unwrap()
            .contains_key("running_exp_in_layer_no_holdout"));
    }

    #[test]
    fn planned_v1_format_keeps_allowlisted_layered_experiments() {
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-key".to_string()),
            remove_experiments_in_layers: Some(true),
            experiments_in_layers_allowlist: Some(HashSet::from([
                "running_exp_in_layer_no_holdout".to_string(),
            ])),
            ..Default::default()
        };

        let (unplanned, planned) = planned_and_unplanned_response_values(&options);

        assert_eq!(unplanned, planned);
        assert!(planned["dynamic_configs"]
            .as_object()
            .unwrap()
            .contains_key("running_exp_in_layer_no_holdout"));
    }
}
