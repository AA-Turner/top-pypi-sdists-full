use crate::StatsigOptions;

#[test]
fn test_prefer_http2_supported_option() {
    use crate::networking::http2::http2_enabled;

    assert!(http2_enabled(None));
    assert!(http2_enabled(Some(&StatsigOptions::default())));
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
    assert!(http2_enabled(Some(&old_flag_only)));
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
