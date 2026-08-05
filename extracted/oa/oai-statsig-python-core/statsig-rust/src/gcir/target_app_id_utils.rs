use crate::{
    ClientInitResponseOptions, DynamicValue, HashAlgorithm, evaluation::evaluation_data::SpecView,
    hashing::HashUtil, interned_string::InternedString,
    specs_response::spec_types::SpecsResponseFull,
};

pub(crate) fn select_app_id_for_gcir<'a>(
    options: &'a ClientInitResponseOptions,
    dcs_values: &'a SpecsResponseFull,
    hashing: &HashUtil,
) -> Option<&'a DynamicValue> {
    let mut app_id = dcs_values.app_id.as_ref();

    let client_sdk_key = match options.client_sdk_key.as_ref() {
        Some(client_sdk_key) => client_sdk_key,
        None => return app_id,
    };

    if let Some(app_id_value) = &dcs_values.sdk_keys_to_app_ids {
        app_id = app_id_value.get(client_sdk_key);
    }

    if let Some(app_id_value) = &dcs_values.hashed_sdk_keys_to_app_ids {
        let hashed_key = &hashing.hash(client_sdk_key, &HashAlgorithm::Djb2);
        app_id = app_id_value.get(hashed_key);
    }

    app_id
}

pub(crate) fn should_filter_spec_for_app(
    spec: SpecView<'_>,
    app_id: &Option<&DynamicValue>,
    client_sdk_key: &Option<String>,
) -> bool {
    if client_sdk_key.is_none() {
        return false;
    }

    let Some(string_app_id) = app_id.and_then(|value| value.string_value.as_ref()) else {
        return false;
    };

    !spec
        .target_app_ids_contains(string_app_id.value.as_str())
        .unwrap_or(false)
}

pub(crate) fn should_filter_config_for_app(
    target_app_ids: Option<&Vec<InternedString>>,
    app_id: &Option<&DynamicValue>,
    client_sdk_key: &Option<String>,
) -> bool {
    let _client_sdk_key = match client_sdk_key {
        Some(client_sdk_key) => client_sdk_key,
        None => return false,
    };

    let app_id = match app_id {
        Some(app_id) => app_id,
        None => return false,
    };

    let string_app_id = match app_id.string_value.as_ref() {
        Some(string_app_id) => string_app_id,
        None => return false,
    };

    let target_app_ids = match target_app_ids {
        Some(target_app_ids) => target_app_ids,
        None => return true,
    };

    if !target_app_ids.iter().any(|id| id == &string_app_id.value) {
        return true;
    }
    false
}
