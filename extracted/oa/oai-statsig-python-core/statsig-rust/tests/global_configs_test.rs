#[path = "../examples/support/synthetic_specs.rs"]
mod codec;

use serde_json::json;
use statsig_rust::{
    SpecStore, SpecsSource, SpecsUpdate, StatsigRuntime, global_configs::GlobalConfigs,
    networking::ResponseData, sdk_event_emitter::SdkEventEmitter,
};
use std::{collections::HashMap, fs};

fn create_test_spec_store(sdk_key: &str) -> SpecStore {
    SpecStore::new(
        sdk_key,
        sdk_key.to_string(),
        StatsigRuntime::get_runtime(),
        std::sync::Arc::new(SdkEventEmitter::default()),
        None,
    )
}

#[test]
fn only_full_snapshots_clear_an_omitted_special_case_sampling_rate() {
    let key = "secret-sampling-rate-refresh";
    let store = create_test_spec_store(key);
    let globals = GlobalConfigs::get_instance(key);
    let number =
        |name: &str| globals.use_sdk_config_value(name, |value| value.and_then(|v| v.float_value));
    let apply = |data| {
        store
            .set_values(SpecsUpdate {
                data,
                source: SpecsSource::Network,
                received_at: 0,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
    };
    let full = |time, checksum| {
        json!({
            "time": time, "checksum": checksum, "response_format": "dcs-v2", "has_updates": true,
            "experiment_to_layer": {}, "condition_map": {}, "feature_gates": {},
            "dynamic_configs": {}, "layer_configs": {}
        })
    };
    let proto_headers = HashMap::from([
        ("content-type".into(), "application/octet-stream".into()),
        ("content-encoding".into(), "statsig-zstd".into()),
    ]);
    let proto = |bytes| ResponseData::from_bytes_with_headers(bytes, Some(proto_headers.clone()));

    let mut initial = full(1, "initial");
    initial["sdk_configs"] = json!({"special_case_sampling_rate": 101});
    apply(proto(codec::encode_full(&initial).unwrap()));
    assert_eq!(number("special_case_sampling_rate"), Some(101.0));

    let mut delta = full(2, "delta");
    delta["sdk_configs"] = json!({"event_queue_size": 250});
    apply(proto(codec::encode_delta(&initial, &delta).unwrap()));
    assert_eq!(number("event_queue_size"), Some(250.0));
    assert_eq!(number("special_case_sampling_rate"), Some(101.0));

    let mut refresh = full(3, "refresh");
    refresh["sdk_configs"] = delta["sdk_configs"].clone();
    apply(ResponseData::from_bytes(
        serde_json::to_vec(&refresh).unwrap(),
    ));
    assert_eq!(number("special_case_sampling_rate"), None);

    let mut enabled_again = full(4, "enabled-again");
    enabled_again["sdk_configs"] = json!({"special_case_sampling_rate": 17});
    apply(proto(codec::encode_full(&enabled_again).unwrap()));
    assert_eq!(number("special_case_sampling_rate"), Some(17.0));
    apply(proto(
        codec::encode_full(&full(5, "no-sdk-configs")).unwrap(),
    ));
    assert_eq!(number("special_case_sampling_rate"), None);
    assert_eq!(number("event_queue_size"), Some(250.0));
}

#[test]
fn test_set_values_and_get_config_num_value() {
    let sdk_key = "secret-key-set-global-configs-test";
    let spec_store = create_test_spec_store(sdk_key);
    let global_config_instance = GlobalConfigs::get_instance(sdk_key);
    // Load JSON data from file
    let data =
        fs::read_to_string("tests/data/dcs_with_sdk_configs.json").expect("Unable to read file");

    let specs_update = SpecsUpdate {
        data: ResponseData::from_bytes(data.into_bytes()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    };

    match spec_store.set_values(specs_update) {
        Ok(()) => println!("set_values succeeded"),
        Err(e) => println!("set_values failed: {e:?}"),
    }

    assert_eq!(
        global_config_instance.use_sdk_config_value("event_queue_size", |v| v.unwrap().float_value),
        Some(1800.0)
    );

    assert_eq!(
        global_config_instance
            .use_sdk_config_value("event_logging_interval_seconds", |v| v.unwrap().float_value),
        Some(1.0)
    );

    assert_eq!(
        global_config_instance
            .use_sdk_config_value("special_case_sampling_rate", |v| v.unwrap().float_value),
        Some(101.0)
    );

    assert_eq!(
        global_config_instance.use_sdk_config_value("non_existent_key", |v| v.cloned()),
        None
    );
}

#[test]
fn test_set_values_and_get_config_str_value() {
    let sdk_key = "secret-key-get-global-configs-test";
    let spec_store: SpecStore = create_test_spec_store(sdk_key);
    let global_config_instance = GlobalConfigs::get_instance(sdk_key);

    let data =
        fs::read_to_string("tests/data/dcs_with_sdk_configs.json").expect("Unable to read file");

    let specs_update = SpecsUpdate {
        data: ResponseData::from_bytes(data.into_bytes()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    };

    spec_store.set_values(specs_update).unwrap();

    assert_eq!(
        global_config_instance.use_sdk_config_value("sampling_mode", |v| v
            .unwrap()
            .string_value
            .clone()
            .unwrap()
            .value),
        "shadow".to_string()
    );
    assert_eq!(
        global_config_instance.use_sdk_config_value("non_existent_key", |v| v.cloned()),
        None
    );
}

#[test]
fn test_get_default_diagnostics_sampling_rate() {
    let global_config_instance = GlobalConfigs::get_instance("");
    let init_rate =
        global_config_instance.use_diagnostics_sampling_rate("initialize", |x| x.cloned());
    let config_sync_rate =
        global_config_instance.use_diagnostics_sampling_rate("config_sync", |x| x.cloned());
    let dcs_rate = global_config_instance.use_diagnostics_sampling_rate("dcs", |x| x.cloned());
    let get_id_list_rate =
        global_config_instance.use_diagnostics_sampling_rate("get_id_list", |x| x.cloned());

    assert_eq!(init_rate, Some(10000.0));
    assert_eq!(config_sync_rate, Some(1000.0));
    assert_eq!(dcs_rate, Some(1000.0));
    assert_eq!(get_id_list_rate, Some(100.0));
}

#[test]
fn test_set_and_get_sampling_rate() {
    let sdk_key = "secret-key-sampling-global-configs-test";
    let spec_store: SpecStore = create_test_spec_store(sdk_key);
    let data =
        fs::read_to_string("tests/data/dcs_with_sdk_configs.json").expect("Unable to read file");

    let specs_update = SpecsUpdate {
        data: ResponseData::from_bytes(data.into_bytes()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    };

    match spec_store.set_values(specs_update) {
        Ok(()) => println!("set_values succeeded"),
        Err(e) => println!("set_values failed: {e:?}"),
    }

    let global_config_instance = GlobalConfigs::get_instance(sdk_key);
    let init_rate =
        global_config_instance.use_diagnostics_sampling_rate("initialize", |x| x.cloned());
    let config_sync_rate =
        global_config_instance.use_diagnostics_sampling_rate("config_sync", |x| x.cloned());
    let dcs_rate = global_config_instance.use_diagnostics_sampling_rate("dcs", |x| x.cloned());
    let get_id_list_rate =
        global_config_instance.use_diagnostics_sampling_rate("get_id_list", |x| x.cloned());

    assert_eq!(init_rate, Some(9999.0));
    assert_eq!(config_sync_rate, Some(1000.0));
    assert_eq!(dcs_rate, Some(999.0));
    assert_eq!(get_id_list_rate, Some(99.0));
}

#[test]
fn test_set_and_get_sdk_flag() {
    let sdk_key = "secret-key-with-sdk-flags";
    let spec_store: SpecStore = create_test_spec_store(sdk_key);
    let data =
        fs::read_to_string("tests/data/dcs_with_sdk_configs.json").expect("Unable to read file");
    let specs_update = SpecsUpdate {
        data: ResponseData::from_bytes(data.into_bytes()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    };

    match spec_store.set_values(specs_update) {
        Ok(()) => println!("set_values succeeded"),
        Err(e) => println!("set_values failed: {e:?}"),
    }

    let global_config_instance = GlobalConfigs::get_instance(sdk_key);
    let disable_console_capture =
        global_config_instance.get_sdk_flag_value("disable_console_capture");

    assert!(disable_console_capture);
}

#[test]
fn test_set_and_get_sdk_flag_when_dcs_has_no_sdk_flags() {
    let sdk_key = "secret-key-without-sdk-flags";
    let spec_store: SpecStore = create_test_spec_store(sdk_key);
    let data = fs::read_to_string("tests/data/eval_proj_dcs.json").expect("Unable to read file");

    let specs_update = SpecsUpdate {
        data: ResponseData::from_bytes(data.into_bytes()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    };

    match spec_store.set_values(specs_update) {
        Ok(()) => println!("set_values succeeded"),
        Err(e) => println!("set_values failed: {e:?}"),
    }

    let global_config_instance = GlobalConfigs::get_instance(sdk_key);
    let disable_console_capture =
        global_config_instance.get_sdk_flag_value("disable_console_capture");

    assert!(!disable_console_capture);
}
