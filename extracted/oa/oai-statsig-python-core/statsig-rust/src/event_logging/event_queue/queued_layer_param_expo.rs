use crate::{
    EvaluationDetails, SecondaryExposure,
    evaluation::evaluation_types::{ExtraExposureInfo, SharedControlLayerExposure},
    event_logging::{
        event_logger::ExposureTrigger,
        exposure_sampling::{EvtSamplingDecision, ExposureSamplingKey},
        exposure_utils::{get_metadata_with_details, get_statsig_metadata_with_sampling_decision},
        statsig_event::StatsigEvent,
        statsig_event_internal::{LAYER_EXPOSURE_EVENT_NAME, StatsigEventInternal},
    },
    hashing::ahash_str,
    interned_string::InternedString,
    statsig_types::Layer,
    user::StatsigUserLoggable,
};

use super::queued_event::{EnqueueOperation, QueuedEvent, QueuedExposure};
use crate::event_logging::statsig_event::string_metadata_to_value_metadata;

pub enum EnqueueLayerParamExpoOp<'a> {
    LayerRef(u64, &'a Layer, &'a str, ExposureTrigger),
    LayerOwned(u64, Box<Layer>, String, ExposureTrigger),
    SharedControlRef(
        u64,
        &'a Layer,
        &'a str,
        &'a SharedControlLayerExposure,
        ExposureTrigger,
    ),
}

impl<'a> EnqueueLayerParamExpoOp<'a> {
    fn get_layer_ref(&'a self) -> &'a Layer {
        match self {
            EnqueueLayerParamExpoOp::LayerRef(_, layer, _, _) => layer,
            EnqueueLayerParamExpoOp::LayerOwned(_, layer, _, _) => layer,
            EnqueueLayerParamExpoOp::SharedControlRef(_, layer, _, _, _) => layer,
        }
    }

    fn get_parameter_name_ref(&'a self) -> &'a str {
        match self {
            EnqueueLayerParamExpoOp::LayerRef(_, _, parameter_name, _) => parameter_name,
            EnqueueLayerParamExpoOp::LayerOwned(_, _, parameter_name, _) => parameter_name.as_str(),
            EnqueueLayerParamExpoOp::SharedControlRef(_, _, parameter_name, _, _) => parameter_name,
        }
    }
}

impl EnqueueOperation for EnqueueLayerParamExpoOp<'_> {
    fn as_exposure(&self) -> Option<&impl QueuedExposure<'_>> {
        Some(self)
    }

    fn into_queued_event(self, sampling_decision: EvtSamplingDecision) -> QueuedEvent {
        let event = match self {
            EnqueueLayerParamExpoOp::LayerRef(exposure_time, layer, parameter_name, trigger) => {
                extract_from_layer_ref(
                    exposure_time,
                    layer,
                    parameter_name,
                    trigger,
                    sampling_decision,
                )
            }
            EnqueueLayerParamExpoOp::LayerOwned(exposure_time, layer, parameter_name, trigger) => {
                extract_from_layer_owned(
                    exposure_time,
                    layer,
                    parameter_name,
                    trigger,
                    sampling_decision,
                )
            }
            EnqueueLayerParamExpoOp::SharedControlRef(
                exposure_time,
                layer,
                parameter_name,
                shared_control_exposure,
                trigger,
            ) => extract_from_shared_control_layer(
                exposure_time,
                layer,
                parameter_name,
                shared_control_exposure,
                trigger,
                sampling_decision,
            ),
        };

        QueuedEvent::LayerParamExposure(event)
    }
}

impl<'a> QueuedExposure<'a> for EnqueueLayerParamExpoOp<'a> {
    fn create_exposure_sampling_key(&self) -> ExposureSamplingKey {
        let layer = self.get_layer_ref();

        let evaluation = layer.__evaluation.as_ref().map(|e| &e.base);
        let unit_id_type = layer
            .__evaluation
            .as_ref()
            .and_then(|e| e.id_type.as_ref())
            .map(|id| id.as_str());
        // todo: use Cow and pre-hash the parameter name
        let pname = self.get_parameter_name_ref();
        let pname_hash = ahash_str(pname);
        let mut sampling_key = ExposureSamplingKey::new_from_user_values_hash(
            evaluation,
            layer.__user.create_exposure_dedupe_user_hash(unit_id_type),
            pname_hash,
        );
        if let EnqueueLayerParamExpoOp::SharedControlRef(_, _, _, exposure, _) = self {
            sampling_key.rule_id_hash = exposure.control_group_id.hash;
        }
        sampling_key
    }

    fn get_rule_id_ref(&'a self) -> &'a str {
        match self {
            EnqueueLayerParamExpoOp::SharedControlRef(_, _, _, exposure, _) => {
                exposure.control_group_id.as_str()
            }
            _ => &self.get_layer_ref().rule_id,
        }
    }

    fn get_extra_exposure_info_ref(&'a self) -> Option<&'a ExtraExposureInfo> {
        match self {
            EnqueueLayerParamExpoOp::SharedControlRef(_, _, _, exposure, _) => {
                Some(&exposure.exposure_info)
            }
            _ => get_layer_exposure_info(self.get_layer_ref()),
        }
    }
}

pub struct QueuedLayerParamExposureEvent {
    pub user: StatsigUserLoggable,
    pub layer_name: String,
    pub rule_id: String,
    pub parameter_name: String,
    pub secondary_exposures: Option<Vec<SecondaryExposure>>,
    pub evaluation_details: EvaluationDetails,
    pub version: Option<u32>,
    pub exposure_trigger: ExposureTrigger,
    pub sampling_decision: EvtSamplingDecision,
    pub override_config_name: Option<InternedString>,
    pub is_explicit: bool,
    pub allocated_experiment: Option<InternedString>,
    pub exposure_time: u64,
}

impl QueuedLayerParamExposureEvent {
    pub fn into_statsig_event_internal(self) -> StatsigEventInternal {
        let mut metadata = get_metadata_with_details(self.evaluation_details);
        metadata.insert("config".into(), self.layer_name);
        metadata.insert("ruleID".into(), self.rule_id);
        metadata.insert(
            "allocatedExperiment".into(),
            self.allocated_experiment
                .unwrap_or_default()
                .unperformant_to_string(),
        );
        metadata.insert("parameterName".into(), self.parameter_name);
        metadata.insert("isExplicitParameter".into(), self.is_explicit.to_string());

        if let Some(version) = self.version {
            metadata.insert("configVersion".into(), version.to_string());
        }

        if self.exposure_trigger == ExposureTrigger::Manual {
            metadata.insert("isManualExposure".into(), "true".into());
        }

        if let Some(override_config_name) = self.override_config_name {
            metadata.insert(
                "overrideConfigName".into(),
                override_config_name.unperformant_to_string(),
            );
        }

        let statsig_metadata = get_statsig_metadata_with_sampling_decision(self.sampling_decision);

        let event = StatsigEvent {
            event_name: LAYER_EXPOSURE_EVENT_NAME.into(),
            value: None,
            metadata: Some(string_metadata_to_value_metadata(metadata)),
            statsig_metadata: Some(statsig_metadata),
        };

        StatsigEventInternal::new(
            self.exposure_time,
            self.user,
            event,
            Some(self.secondary_exposures.unwrap_or_default()),
        )
    }
}

type ExtractFromEvaluationResult = (
    bool,
    Option<InternedString>,
    Option<Vec<SecondaryExposure>>,
    Option<u32>,
    Option<InternedString>,
);

fn extract_exposure_info(layer: &Layer, parameter_name: &str) -> ExtractFromEvaluationResult {
    let evaluation = match layer.__evaluation.as_ref() {
        Some(eval) => eval,
        None => return (false, None, None, None, None),
    };

    let is_explicit = evaluation.explicit_parameters.contains(parameter_name);
    let secondary_exposures;
    let mut allocated_experiment = None;

    if is_explicit {
        allocated_experiment = evaluation.allocated_experiment_name.clone();
        secondary_exposures = Some(evaluation.base.secondary_exposures.clone());
    } else {
        secondary_exposures = evaluation.undelegated_secondary_exposures.clone();
    }

    // version might be on the top level or the exposure info
    let mut version = layer.__version;
    let mut override_config_name = None;

    if let Some(exposure_info) = get_layer_exposure_info(layer) {
        version = exposure_info.version;
        override_config_name = exposure_info.override_config_name.clone();
    }

    (
        is_explicit,
        allocated_experiment,
        secondary_exposures,
        version,
        override_config_name,
    )
}

fn get_layer_exposure_info(layer: &Layer) -> Option<&ExtraExposureInfo> {
    layer
        .__evaluation
        .as_ref()
        .and_then(|eval| eval.base.exposure_info.as_ref())
        .or(layer.__exposure_info.as_ref())
}

fn extract_from_layer_ref(
    exposure_time: u64,
    layer: &Layer,
    param_name: &str,
    trigger: ExposureTrigger,
    sampling_decision: EvtSamplingDecision,
) -> QueuedLayerParamExposureEvent {
    let parameter_name = param_name.to_string();
    let (is_explicit, allocated_experiment, secondary_exposures, version, override_config_name) =
        extract_exposure_info(layer, &parameter_name);

    let rule_id = match layer.__parameter_rule_ids {
        Some(ref rule_ids) => rule_ids
            .get(&InternedString::from_str_ref(param_name))
            .map(|s| s.unperformant_to_string())
            .unwrap_or_else(|| layer.rule_id.clone()),
        None => layer.rule_id.clone(),
    };

    QueuedLayerParamExposureEvent {
        exposure_time,
        user: layer.__user.clone(),
        layer_name: layer.name.clone(),
        rule_id,
        parameter_name,
        exposure_trigger: trigger,
        evaluation_details: layer.details.clone(),
        version,
        sampling_decision,
        override_config_name,
        secondary_exposures,
        is_explicit,
        allocated_experiment,
    }
}

fn extract_from_layer_owned(
    exposure_time: u64,
    layer: Box<Layer>,
    parameter_name: String,
    trigger: ExposureTrigger,
    sampling_decision: EvtSamplingDecision,
) -> QueuedLayerParamExposureEvent {
    let (is_explicit, allocated_experiment, secondary_exposures, version, override_config_name) =
        extract_exposure_info(&layer, &parameter_name);

    let rule_id = match layer.__parameter_rule_ids {
        Some(ref rule_ids) => rule_ids
            .get(&InternedString::from_str_ref(parameter_name.as_str()))
            .map(|s| s.unperformant_to_string())
            .unwrap_or_else(|| layer.rule_id.clone()),
        None => layer.rule_id.clone(),
    };

    QueuedLayerParamExposureEvent {
        exposure_time,
        user: layer.__user,
        layer_name: layer.name,
        rule_id,
        parameter_name,
        exposure_trigger: trigger,
        evaluation_details: layer.details,
        version,
        sampling_decision,
        override_config_name,
        secondary_exposures,
        is_explicit,
        allocated_experiment,
    }
}

fn extract_from_shared_control_layer(
    exposure_time: u64,
    layer: &Layer,
    parameter_name: &str,
    shared_control_exposure: &SharedControlLayerExposure,
    trigger: ExposureTrigger,
    sampling_decision: EvtSamplingDecision,
) -> QueuedLayerParamExposureEvent {
    QueuedLayerParamExposureEvent {
        exposure_time,
        user: layer.__user.clone(),
        layer_name: layer.name.clone(),
        rule_id: shared_control_exposure
            .control_group_id
            .unperformant_to_string(),
        parameter_name: parameter_name.to_string(),
        exposure_trigger: trigger,
        evaluation_details: layer.details.clone(),
        version: shared_control_exposure.exposure_info.version,
        sampling_decision,
        override_config_name: shared_control_exposure
            .exposure_info
            .override_config_name
            .clone(),
        secondary_exposures: Some(shared_control_exposure.secondary_exposures.clone()),
        is_explicit: true,
        allocated_experiment: Some(shared_control_exposure.allocated_experiment_name.clone()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        evaluation::evaluation_types::SharedControlLayerExposure,
        specs_response::explicit_params::ExplicitParameters,
    };

    #[test]
    fn shared_control_layer_exposure_uses_control_attribution() {
        let layer = Layer {
            name: "ads_layer".to_string(),
            rule_id: "sharedControl".to_string(),
            id_type: "userID".to_string(),
            group_name: None,
            details: EvaluationDetails::unrecognized_no_data(),
            allocated_experiment_name: None,
            is_experiment_active: false,
            __parameter_rule_ids: None,
            __evaluation: None,
            __value: Default::default(),
            __user: StatsigUserLoggable::null(),
            __disable_exposure: false,
            __shared_control_exposures: Vec::new(),
            __version: None,
            __exposure_info: None,
            __event_logger_ptr: None,
        };
        let shared_control_exposure = SharedControlLayerExposure {
            allocated_experiment_name: InternedString::from_str_ref("ranking_experiment"),
            control_group_id: InternedString::from_str_ref("control_group"),
            secondary_exposures: Vec::new(),
            explicit_parameters: ExplicitParameters::from_vec(vec!["ranking_model".to_string()]),
            exposure_info: ExtraExposureInfo {
                sampling_rate: Some(201),
                forward_all_exposures: Some(true),
                has_seen_analytical_gates: Some(true),
                override_config_name: None,
                version: Some(12),
                rule_pass_percentage: None,
            },
        };

        let operation = EnqueueLayerParamExpoOp::SharedControlRef(
            123,
            &layer,
            "ranking_model",
            &shared_control_exposure,
            ExposureTrigger::Auto,
        );
        let exposure_info = operation
            .get_extra_exposure_info_ref()
            .expect("shared-control exposure metadata should be preserved");
        assert_eq!(exposure_info.sampling_rate, Some(201));
        assert_eq!(exposure_info.forward_all_exposures, Some(true));
        assert_eq!(exposure_info.has_seen_analytical_gates, Some(true));
        assert_eq!(
            operation.create_exposure_sampling_key().rule_id_hash,
            shared_control_exposure.control_group_id.hash
        );

        let event = extract_from_shared_control_layer(
            123,
            &layer,
            "ranking_model",
            &shared_control_exposure,
            ExposureTrigger::Auto,
            EvtSamplingDecision::ForceSampled,
        );

        assert_eq!(event.layer_name, "ads_layer");
        assert_eq!(event.rule_id, "control_group");
        assert_eq!(event.parameter_name, "ranking_model");
        assert_eq!(
            event
                .allocated_experiment
                .as_ref()
                .map(InternedString::as_str),
            Some("ranking_experiment")
        );
        assert!(event.is_explicit);
        assert_eq!(event.version, Some(12));
    }
}
