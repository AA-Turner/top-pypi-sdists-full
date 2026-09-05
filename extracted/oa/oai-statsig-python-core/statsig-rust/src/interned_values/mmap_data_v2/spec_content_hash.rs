use crate::{
    evaluation::{
        dynamic_returnable::{DynamicReturnable, DynamicReturnableValue},
        rkyv_value::push_stable_object_hash,
    },
    hashing::U64HashBuilder,
    interned_string::InternedString,
    specs_response::spec_types::Spec,
};

// Per-spec checksums are transport-dependent and are absent from JSON DCS. This
// fingerprint covers the evaluation fields so readers can safely bind an
// unchanged spec to mmap after parsing either transport.
pub(crate) fn spec_content_hash(spec: &Spec) -> u64 {
    let mut values = U64HashBuilder::with_capacity(32 + spec.rules.len() * 16);
    values.push(spec._type.hash);
    values.push(spec.salt.hash);
    push_returnable(&mut values, &spec.default_value);
    values.push(u64::from(spec.enabled));
    values.push(spec.rules.len() as u64);
    for rule in &spec.rules {
        values.push(rule.name.hash);
        values.push(rule.pass_percentage.to_bits());
        push_returnable(&mut values, &rule.return_value);
        values.push(rule.id.hash);
        push_optional_hash(&mut values, rule.salt.as_ref().map(|value| value.hash));
        push_strings(&mut values, Some(&rule.conditions));
        values.push(rule.id_type.value.hash);
        values.push(rule.id_type.lowercased_value.hash);
        push_optional_hash(
            &mut values,
            rule.group_name.as_ref().map(|value| value.hash),
        );
        push_optional_hash(
            &mut values,
            rule.config_delegate.as_ref().map(|value| value.hash),
        );
        push_optional_bool(&mut values, rule.is_experiment_group);
        push_optional_hash(&mut values, rule.sampling_rate);
        if let Some(shared_control_experiments) = &rule.shared_control_experiments {
            values.push(shared_control_experiments.len() as u64);
            for experiment in shared_control_experiments.iter() {
                values.push(experiment.name.hash);
                values.push(experiment.control_group_id.hash);
            }
        }
    }
    values.push(spec.id_type.hash);
    push_strings(
        &mut values,
        spec.explicit_parameters
            .as_ref()
            .map(|parameters| parameters.as_slice()),
    );
    values.push(spec.entity.hash);
    push_optional_bool(&mut values, spec.has_shared_params);
    push_optional_bool(&mut values, spec.is_active);
    push_optional_hash(&mut values, spec.version.map(u64::from));
    push_strings(&mut values, spec.target_app_ids.as_deref());
    push_optional_bool(&mut values, spec.forward_all_exposures);
    push_strings(&mut values, spec.fields_used.as_deref());
    push_optional_bool(&mut values, spec.use_new_layer_eval);
    values.finish()
}

fn push_returnable(values: &mut U64HashBuilder, value: &DynamicReturnable) {
    match &value.value {
        DynamicReturnableValue::Null => values.push(0),
        DynamicReturnableValue::Bool(false) => values.push(1),
        DynamicReturnableValue::Bool(true) => values.push(2),
        DynamicReturnableValue::JsonPointer(value) => {
            values.push(3);
            push_stable_object_hash(
                values,
                value.iter().map(|(key, value)| (key.as_str(), value)),
            );
        }
        DynamicReturnableValue::JsonStatic(value) => {
            values.push(3);
            push_stable_object_hash(
                values,
                value.iter().map(|(key, value)| (key.as_str(), value)),
            );
        }
        DynamicReturnableValue::JsonArchived(value) => {
            values.push(3);
            push_stable_object_hash(
                values,
                value.iter().map(|(key, value)| (key.as_str(), value)),
            );
        }
    }
}

fn push_optional_hash(values: &mut U64HashBuilder, value: Option<u64>) {
    match value {
        Some(value) => {
            values.push(1);
            values.push(value);
        }
        None => values.push(0),
    }
}

fn push_optional_bool(values: &mut U64HashBuilder, value: Option<bool>) {
    values.push(match value {
        None => 0,
        Some(false) => 1,
        Some(true) => 2,
    });
}

fn push_strings(values: &mut U64HashBuilder, strings: Option<&[InternedString]>) {
    let Some(strings) = strings else {
        values.push(0);
        return;
    };
    values.push(1);
    values.push(strings.len() as u64);
    for value in strings {
        values.push(value.hash);
    }
}
