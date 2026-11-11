//! Restricted cross-service experiment measurement. The caller owns the exposure point.
use super::*;
use crate::SecondaryExposure;
use crate::evaluation::dynamic_string::DynamicString;
use crate::evaluation::evaluation_types::ExtraExposureInfo;
use crate::user::user_data::{UserData, UserDataMap};
use serde::Deserialize;

/// This private wire format contains the IDs used for exposure attribution.
#[derive(Serialize, Deserialize)]
struct ExposureIdentity {
    #[serde(rename = "userID", skip_serializing_if = "Option::is_none")]
    user_id: Option<DynamicValue>,
    #[serde(rename = "customIDs", skip_serializing_if = "Option::is_none")]
    custom_ids: Option<UserDataMap>,
}

#[derive(Serialize, Deserialize)]
enum SavedExperimentExposure {
    V1 {
        experiment: InternedString,
        rule_id: InternedString,
        id_type: String,
        user: ExposureIdentity,
        details: EvaluationDetails,
        secondary_exposures: Vec<SecondaryExposure>,
        exposure_info: ExtraExposureInfo,
    },
}

impl Statsig {
    /// Error-prone. Consult the Statsig team before using this for a custom
    /// cross-service exposure. Prefer get_layer and reading the actual parameter.
    pub fn evaluate_layer_for_deferred_experiment_exposure(
        &self,
        user: &StatsigUserInternal,
        layer_name: &str,
    ) -> Result<(Layer, Option<String>), StatsigErr> {
        let _scope = self.output_policy.enter();
        let load = self.ensure_spec_id_lists(layer_name, &SpecType::Layer);
        let specs = Arc::clone(&load.data);
        let layer = self.get_layer_impl(
            user.clone(),
            layer_name,
            LayerEvaluationOptions {
                disable_exposure_logging: true,
                ..Default::default()
            },
            load,
        );
        let payload = if self.options.disable_all_logging == Some(true) {
            None
        } else {
            SavedExperimentExposure::from_layer(&layer, &specs, user)
                .map(|saved| serde_json::to_string(&saved))
                .transpose()
                .map_err(|error| StatsigErr::SerializationError(error.to_string()))?
        };
        Ok((layer, payload))
    }

    /// Error-prone. Consult the Statsig team first. Prefer get_layer and reading
    /// a parameter. Consume trusted SDK output once, when its assignment is used.
    pub fn log_deferred_experiment_exposure(&self, payload: &str) -> Result<(), StatsigErr> {
        let _scope = self.output_policy.enter();
        let SavedExperimentExposure::V1 {
            experiment,
            rule_id,
            id_type,
            user,
            details,
            secondary_exposures,
            exposure_info,
        } = serde_json::from_str(payload).map_err(|_| {
            StatsigErr::InvalidOperation("Invalid saved experiment exposure".into())
        })?;
        let user = StatsigUser::new(UserData {
            user_id: user.user_id,
            custom_ids: user.custom_ids,
            ..Default::default()
        });
        let user = StatsigUserInternal::new(&user, Some(self));
        if !has_assignment_unit(&user, &id_type) {
            return Err(StatsigErr::InvalidOperation(
                "Missing saved experiment assignment unit".into(),
            ));
        }
        let evaluation = EvaluatorResult {
            rule_id: Some(rule_id),
            is_experiment_group: true,
            secondary_exposures,
            sampling_rate: exposure_info.sampling_rate,
            forward_all_exposures: exposure_info.forward_all_exposures,
            has_seen_analytical_gates: exposure_info.has_seen_analytical_gates,
            version: exposure_info.version,
            override_config_name: exposure_info.override_config_name,
            ..Default::default()
        };
        self.event_logger
            .enqueue(EnqueueExposureOp::experiment_exposure(
                &user,
                &experiment,
                ExposureTrigger::Manual,
                details,
                Some(evaluation),
            ));
        Ok(())
    }
}

impl SavedExperimentExposure {
    fn from_layer(
        layer: &Layer,
        specs: &SpecStoreData,
        user: &StatsigUserInternal,
    ) -> Option<Self> {
        let eval = layer.__evaluation.as_ref()?;
        if eval.is_user_in_experiment != Some(true)
            || !layer.details.reason.ends_with(":Recognized")
        {
            return None;
        }
        let experiment = eval.allocated_experiment_name.as_ref()?;
        let group = eval.group_name.as_ref()?;
        // The layer and experiment can have different versions and sampling settings.
        // Resolve the already-selected rule in the exact snapshot used above.
        let spec = specs.snapshot.dynamic_configs.get(experiment)?.view();
        let rule = (0..spec.rules_len()).map(|i| spec.rule(i)).find(|rule| {
            rule.is_experiment_group()
                && rule.id().as_str() == layer.rule_id
                && rule
                    .group_name()
                    .is_some_and(|name| name.as_str() == group.as_str())
        })?;
        let id_type = rule.id_type().value();
        if !has_assignment_unit(user, id_type) {
            return None;
        }
        let identity = user.with_public_user(|user| ExposureIdentity {
            user_id: user.data.user_id.clone(),
            custom_ids: user.data.custom_ids.clone(),
        });
        let mut details = layer.details.clone();
        details.version = spec.version();
        let exposure_info = ExtraExposureInfo {
            sampling_rate: rule.sampling_rate(),
            forward_all_exposures: spec.forward_all_exposures(),
            version: spec.version(),
            ..eval.base.exposure_info.clone().unwrap_or_default()
        };
        Some(Self::V1 {
            experiment: experiment.clone(),
            rule_id: rule.id().to_interned(),
            id_type: id_type.to_owned(),
            user: identity,
            details,
            secondary_exposures: eval.base.secondary_exposures.clone(),
            exposure_info,
        })
    }
}

fn has_assignment_unit(user: &StatsigUserInternal, id_type: &str) -> bool {
    user.get_unit_id(&DynamicString::from(id_type.to_owned()))
        .is_some_and(|unit| unit.string_value().is_some_and(|id| !id.is_empty()))
}
