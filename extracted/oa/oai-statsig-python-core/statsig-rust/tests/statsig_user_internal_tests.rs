use statsig_rust::{
    dyn_value,
    evaluation::dynamic_string::DynamicString,
    user::{
        fast_statsig_user::{FastStatsigUser, FastUserData, FastUserUnitIDMap},
        user_value::{UserValue, UserValueMap, UserValueRef},
        StatsigUserInternal,
    },
    StatsigUser,
};

#[test]
fn test_get_user_value() {
    let mut user = StatsigUser::with_user_id("user1");
    user.set_email("user1@example.com");
    let user_internal = StatsigUserInternal::new(&user, None);
    let field = DynamicString::from("email".to_string());
    let user_value = user_internal.get_user_value(&Some(field));
    assert_eq!(
        user_value.and_then(UserValueRef::string_value),
        Some("user1@example.com")
    );
}

#[test]
fn test_fast_user_get_user_value_matches_public_user() {
    let mut public_user = StatsigUser::with_user_id("user1");
    public_user.set_email("user1@example.com");

    let fast_user = FastStatsigUser::new(FastUserData {
        user_id: Some(UserValue::from("user1")),
        email: Some(UserValue::from("user1@example.com")),
        ..FastUserData::default()
    });

    let field = Some(DynamicString::from("email".to_string()));
    let public_user_internal = StatsigUserInternal::new(&public_user, None);
    let fast_user_internal = StatsigUserInternal::from_fast_user(&fast_user, None);

    assert_eq!(
        public_user_internal
            .get_user_value(&field)
            .and_then(UserValueRef::string_value),
        fast_user_internal
            .get_user_value(&field)
            .and_then(UserValueRef::string_value),
    );
}

#[test]
fn test_fast_user_loggable_matches_public_user() {
    let mut public_user = StatsigUser::with_user_id("user1");
    public_user.set_custom_ids(std::collections::HashMap::from([
        ("stableID".to_string(), "stable-1".to_string()),
        ("account_id".to_string(), "acct-1".to_string()),
    ]));

    let fast_user = FastStatsigUser::new(FastUserData {
        user_id: Some(UserValue::from("user1")),
        custom_ids: Some(FastUserUnitIDMap::from_iter([
            ("stableID".to_string(), UserValue::from("stable-1")),
            ("account_id".to_string(), UserValue::from("acct-1")),
        ])),
        ..FastUserData::default()
    });

    let public_user_internal = StatsigUserInternal::new(&public_user, None);
    let fast_user_internal = StatsigUserInternal::from_fast_user(&fast_user, None);

    assert_eq!(
        serde_json::to_value(public_user_internal.to_loggable()).unwrap(),
        serde_json::to_value(fast_user_internal.to_loggable()).unwrap(),
    );
}

#[test]
fn test_fast_user_loggable_matches_public_user_for_full_payload() {
    let mut public_user = StatsigUser::with_user_id("user1");
    public_user.set_custom_ids(std::collections::HashMap::from([
        ("stableID".to_string(), "stable-1".to_string()),
        ("account_id".to_string(), "acct-1".to_string()),
    ]));
    public_user.set_email("user1@example.com");
    public_user.set_ip("127.0.0.1");
    public_user.set_user_agent("agent");
    public_user.set_country("US");
    public_user.set_locale("en-US");
    public_user.set_app_version("1.2.3");
    public_user.set_custom(std::collections::HashMap::from([
        ("plan_type".to_string(), dyn_value!("plus")),
        ("organizations".to_string(), dyn_value!(["org-1", "org-2"])),
    ]));

    let fast_user = FastStatsigUser::new(FastUserData {
        user_id: Some(UserValue::from("user1")),
        custom_ids: Some(FastUserUnitIDMap::from_iter([
            ("stableID".to_string(), UserValue::from("stable-1")),
            ("account_id".to_string(), UserValue::from("acct-1")),
        ])),
        email: Some(UserValue::from("user1@example.com")),
        ip: Some(UserValue::from("127.0.0.1")),
        user_agent: Some(UserValue::from("agent")),
        country: Some(UserValue::from("US")),
        locale: Some(UserValue::from("en-US")),
        app_version: Some(UserValue::from("1.2.3")),
        custom: Some(UserValueMap::from_iter([
            ("plan_type".to_string(), UserValue::from("plus")),
            (
                "organizations".to_string(),
                UserValue::from_array(vec![UserValue::from("org-1"), UserValue::from("org-2")]),
            ),
        ])),
        ..FastUserData::default()
    });

    let public_user_internal = StatsigUserInternal::new(&public_user, None);
    let fast_user_internal = StatsigUserInternal::from_fast_user(&fast_user, None);

    assert_eq!(
        serde_json::to_value(public_user_internal.to_loggable()).unwrap(),
        serde_json::to_value(fast_user_internal.to_loggable()).unwrap(),
    );
}

// todo: test get_unit_id
// todo: test get_value_from_environment
// todo: test to_loggable
