use crate::StatsigOptions;

#[test]
fn private_id_list_format_serializes_only_when_set() {
    for flag in [None, Some(false), Some(true)] {
        let options = StatsigOptions::builder()
            .enable_id_list_elias_fano(flag)
            .build();
        let serialized = serde_json::to_value(options).unwrap();
        assert_eq!(
            serialized.get("enable_id_list_elias_fano").cloned(),
            flag.map(Into::into)
        );
        assert!(serialized.get("enable_id_lists").is_none());
    }
}

#[test]
fn test_prefer_http2_supported_option() {
    use crate::networking::http2::http2_enabled;

    assert!(!http2_enabled(None));
    assert!(!http2_enabled(Some(&StatsigOptions::default())));
    for enabled in [true, false] {
        let options = StatsigOptions::builder()
            .prefer_http2(Some(enabled))
            .build();
        assert_eq!(http2_enabled(Some(&options)), enabled);
        assert_eq!(
            serde_json::to_value(&options).unwrap()["prefer_http2"],
            enabled
        );
        assert!(options.experimental_flags.is_none());
    }

    let old_flag_only = StatsigOptions {
        experimental_flags: Some(["prefer_http2".to_string()].into()),
        ..Default::default()
    };
    assert!(!http2_enabled(Some(&old_flag_only)));
    let explicit_off = StatsigOptions {
        prefer_http2: Some(false),
        ..old_flag_only
    };
    assert!(!http2_enabled(Some(&explicit_off)));
}

#[test]
fn test_sdk_instance_id_defaults_to_sdk_key() {
    let options = StatsigOptions::new();

    assert_eq!(options.get_sdk_instance_id("secret-key"), "secret-key");
}

#[test]
fn test_sdk_instance_id_can_be_overridden() {
    let options = StatsigOptions::builder()
        .sdk_instance_id(Some("validator:route:target".to_string()))
        .build();

    assert_eq!(
        options.get_sdk_instance_id("secret-key"),
        "validator:route:target"
    );
}

#[test]
fn test_lazy_id_list_options_are_built_and_serialized() {
    let options = StatsigOptions::builder()
        .lazy_load_id_lists(Some(true))
        .build();

    assert_eq!(options.lazy_load_id_lists, Some(true));

    let json = serde_json::to_value(&options).unwrap();
    assert_eq!(json["lazy_load_id_lists"], true);
}
