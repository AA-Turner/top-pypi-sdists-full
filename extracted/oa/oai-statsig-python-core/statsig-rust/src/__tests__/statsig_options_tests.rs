use crate::StatsigOptions;

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
